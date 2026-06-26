"""
时效性检查器 - Domain 层实现（全新业务规则版本）

检查文档日期（签发日期、有效期）是否符合实际审批业务场景。
遵循架构红线：
- 继承 Core 层的 BaseChecker
- 输入使用 Core 层的 Document 和配置
- 输出使用 Core 层的 CheckResult
- 不包含文件读取、LLM 调用逻辑
- 不导入任何 infrastructure 或旧的 tools 模块

全新业务规则（4步判定）：
1. 提取有效期（Validity Period）- 支持关键词定位+LLM提取
2. 提取落款日期（Sign Date）
3. 确定比对基准时间（Reference Time）
4. 核心判定矩阵
"""

import re
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, NamedTuple, TYPE_CHECKING
from dateutil.relativedelta import relativedelta

from ...core.checker_base import BaseChecker, CheckResult, CheckStatus
from ...core.checklist_model import Checklist
from ...core.document import Document

if TYPE_CHECKING:
    from ...core.interfaces import LLMClientProtocol, ValidityRetrieverProtocol

logger = logging.getLogger(__name__)


class ValidityPeriod(NamedTuple):
    """有效期数据结构"""

    value: int  # 数值
    unit: str  # 单位: years, months, days, permanent, unknown
    is_permanent: bool = False  # 是否长期有效


class DateMatch(NamedTuple):
    """日期匹配结果"""

    date: datetime
    position: int  # 在文本中的位置
    distance_to_keyword: int  # 距离最近关键词的字符数


class ValidityExtractionResult(NamedTuple):
    """有效期提取结果"""

    period: Optional[ValidityPeriod]
    source: str  # 提取来源: "regex", "llm", "none"


class TimelinessChecker(BaseChecker):
    """
    时效性检查器 - 全新业务规则实现

    核心判定逻辑：
    - 分支 A：有有效期但无落款日期 → 不通过
    - 分支 B：有落款日期但无有效期（长期有效）→ 落款日期 ≤ 基准时间则通过
    - 分支 C：两者都有 → 落款日期 ≤ 基准时间 ≤ 截止日期则通过
    
    有效期提取策略：
    1. 关键词定位：寻找"有效期"关键词
    2. 动态切片：截取关键词后50字符内的内容
    3. 快速探测：使用正则检测是否有数字/时间词
    4. LLM提取：如果检测到数字，使用LLM提取结构化有效期
    5. 未知处理：如果匹配到"有效期"但无法提取具体时间，标记为UNKNOWN
    """

    # 有效期关键词
    VALIDITY_KEYWORD = "有效期"
    
    # 长期/永久有效正则
    PERMANENT_PATTERN = re.compile(r"(长期有效|永久有效|长期|永久)", re.IGNORECASE)
    
    # 日期提取正则模式
    DATE_PATTERNS = [
        (r"(\d{4})年(\d{1,2})月(\d{1,2})日", "ymd"),  # 2024年3月15日
        (r"(\d{4})-(\d{2})-(\d{2})", "ymd"),  # 2024-03-15
        (r"(\d{4})/(\d{2})/(\d{2})", "ymd"),  # 2024/03/15
        (r"(\d{4})\.(\d{2})\.(\d{2})", "ymd"),  # 2024.03.15
    ]

    # 日期提取正则模式
    DATE_PATTERNS = [
        (r"(\d{4})年(\d{1,2})月(\d{1,2})日", "ymd"),  # 2024年3月15日
        (r"(\d{4})-(\d{2})-(\d{2})", "ymd"),  # 2024-03-15
        (r"(\d{4})/(\d{2})/(\d{2})", "ymd"),  # 2024/03/15
        (r"(\d{4})\.(\d{2})\.(\d{2})", "ymd"),  # 2024.03.15
    ]

    # 关键词列表（用于启发式定位落款日期）
    SIGN_KEYWORDS = [
        "签发",
        "日期",
        "盖章",
        "签字",
        "签署",
        "签章",
        "批准",
        "审批",
        "核准",
        "审核",
        "审定",
        "印发",
        "发布",
        "发文",
        "出具",
        "开具",
        "年月日",
        "签名",
        "盖章处",
    ]

    # 中文数字映射
    CHINESE_NUMBERS = {
        "一": 1,
        "二": 2,
        "三": 3,
        "四": 4,
        "五": 5,
        "六": 6,
        "七": 7,
        "八": 8,
        "九": 9,
        "十": 10,
        "百": 100,
        "千": 1000,
        "万": 10000,
    }

    def __init__(
        self,
        project_period: Optional[Dict[str, str]] = None,
        llm_client: Optional["LLMClientProtocol"] = None,
        validity_retriever: Optional["ValidityRetrieverProtocol"] = None,
    ):
        """
        初始化检查器

        Args:
            project_period: 可选的项目周期 {"start": "YYYY-MM", "end": "YYYY-MM"}
            llm_client: LLM 客户端，用于提取有效期（可选，未提供则使用正则提取）
            validity_retriever: Micro-RAG 检索器（可选，提供后会优先使用 RAG 定向检索）
        """
        self.project_period = project_period
        self.llm_client = llm_client
        self.validity_retriever = validity_retriever

    @property
    def name(self) -> str:
        return "timeliness"

    @property
    def description(self) -> str:
        return "检查文档时效性：验证有效期与落款日期的合规性"

    @property
    def version(self) -> str:
        return "3.0.0"

    def _chinese_to_number(self, chinese: str) -> int:
        """将中文数字转换为阿拉伯数字"""
        if not chinese:
            return 0

        # 简单处理，支持 "三十天"、"一年" 等
        result = 0
        temp = 0
        for char in chinese:
            if char in self.CHINESE_NUMBERS:
                num = self.CHINESE_NUMBERS[char]
                if num >= 10:
                    if temp == 0:
                        temp = 1
                    result += temp * num
                    temp = 0
                else:
                    temp = temp * 10 + num if temp > 0 else num
        result += temp
        return result if result > 0 else 1

    def _locate_validity_keyword(self, text: str) -> List[int]:
        """
        定位所有"有效期"关键词的位置
        
        策略：只匹配作为有效期声明的"有效期"，即后面跟着动词或标点的
        如"有效期为"、"有效期："、"有效期至"、"有效期1年"等
        排除作为普通词汇的"有效期"，如"有效期声明"中的"有效期"
        
        Args:
            text: 文档文本
            
        Returns:
            关键词起始位置列表
        """
        positions = []
        keyword = self.VALIDITY_KEYWORD
        start = 0
        
        # 有效期声明后面通常跟着的内容
        valid_follow_patterns = [
            r'[限\s为是至：:\d一二三四五六七八九十百千万]',  # 有效期为、有效期至、有效期：、有效期3年
            r'[\d]',  # 有效期3年
        ]
        
        while True:
            pos = text.find(keyword, start)
            if pos == -1:
                break
            
            # 检查"有效期"后面是否跟着声明相关的字符
            after_pos = pos + len(keyword)
            if after_pos < len(text):
                next_char = text[after_pos]
                # 如果后面跟着限、为、是、至、：、空格或数字/中文数字，认为是有效期声明
                valid_chars = '限为是至：: \t一二三四五六七八九十百千万1234567890'
                if next_char in valid_chars:
                    positions.append(pos)
            else:
                # "有效期"在文本末尾，也认为是声明
                positions.append(pos)
            
            start = pos + len(keyword)
        
        return positions
    
    def _extract_context_slice(self, text: str, keyword_pos: int, max_chars: int = 50) -> str:
        """
        动态切片：截取关键词后指定字符数内的内容
        
        Args:
            text: 文档文本
            keyword_pos: 关键词位置
            max_chars: 最大截取字符数
            
        Returns:
            切片内容
        """
        start = keyword_pos
        end = min(keyword_pos + len(self.VALIDITY_KEYWORD) + max_chars, len(text))
        return text[start:end]
    
    def _has_number_or_time(self, text: str) -> bool:
        """
        快速探测：检测文本中是否有有效期相关的数字或时间词
        
        策略：提取"有效期"到第一个标点/分隔符之间的内容，检查是否包含
        有效期相关的数字（如"3年"、"六个月"）或长期有效标记
        
        Args:
            text: 文本内容（已切片的关键词上下文）
            
        Returns:
            True 如果检测到有效期相关的数字或时间词
        """
        # 移除"有效期"关键词本身
        keyword_len = len(self.VALIDITY_KEYWORD)
        if text.startswith(self.VALIDITY_KEYWORD):
            content = text[keyword_len:]
        else:
            content = text
        
        # 提取到第一个标点符号或特定分隔符之前的内容
        # 分隔符包括：逗号、句号、分号、冒号、换行、"签发"、"日期"等
        delimiters = ['，', '。', '；', '：', '\n', '签发', '日期', '盖章', '签字']
        end_pos = len(content)
        for delimiter in delimiters:
            pos = content.find(delimiter)
            if pos > 0 and pos < end_pos:
                end_pos = pos
        
        core_content = content[:end_pos].strip()
        
        # 在核心内容中检测长期/永久有效
        if self.PERMANENT_PATTERN.search(core_content):
            return True
        
        # 在核心内容中检测数字+时间单位
        # 匹配：X年、X个月、X月、X天、X日、至XXXX年
        validity_number_pattern = re.compile(
            r'([\d一二三四五六七八九十百千万]+)\s*[年]|'
            r'([\d一二三四五六七八九十百千万]+)\s*个月|'
            r'([\d一二三四五六七八九十百千万]+)\s*[月天日]|'
            r'至\s*(\d{4})\s*年',
            re.IGNORECASE
        )
        
        matches = validity_number_pattern.findall(core_content)
        for match in matches:
            # match 是 tuple，取第一个非空组
            num_str = next((m for m in match if m), '')
            if num_str:
                # 匹配到任何数字+时间单位组合即认为有有效期信息
                return True
        
        return False
    
    async def _extract_validity_with_llm(self, context: str) -> Optional[ValidityPeriod]:
        """
        使用 LLM 从上下文中提取有效期
        
        Args:
            context: 包含有效期的文本片段
            
        Returns:
            ValidityPeriod 对象，提取失败返回 None
        """
        if not self.llm_client:
            return None
            
        prompt = f"""从以下文本中提取有效期信息，以JSON格式返回：

文本："{context}"

请分析文本中的有效期信息，返回以下JSON格式：
{{
    "has_validity": true/false,  // 是否包含有效期信息
    "value": 数字或null,  // 有效期数值，如 3
    "unit": "years/months/days/permanent/unknown",  // 单位：年/月/日/长期有效/未知
    "reason": "提取理由或失败原因"
}}

注意：
- 如果文本包含"长期有效"、"永久有效"等，unit 设为 "permanent"
- 如果提到有效期但无法确定具体时间，unit 设为 "unknown"
- 如果没有提到有效期，has_validity 设为 false

只返回JSON，不要其他内容。"""

        try:
            response = await self.llm_client.complete(prompt, temperature=0.1, max_tokens=500)
            import json
            
            # 尝试解析 JSON
            result = json.loads(response.strip())
            
            if not result.get("has_validity", False):
                return None
                
            unit = result.get("unit", "unknown")
            
            if unit == "permanent":
                return ValidityPeriod(value=0, unit="permanent", is_permanent=True)
            elif unit == "unknown":
                # 标记为未知有效期
                return ValidityPeriod(value=0, unit="unknown", is_permanent=False)
            else:
                value = result.get("value", 0)
                if value and value > 0:
                    return ValidityPeriod(value=value, unit=unit, is_permanent=False)
            
            return None
            
        except Exception as e:
            logger.warning(f"LLM 提取有效期失败: {e}")
            return None
    
    def _extract_validity_regex(self, text: str) -> Optional[ValidityPeriod]:
        """
        使用正则表达式提取有效期（备用方案）
        
        Args:
            text: 文本内容
            
        Returns:
            ValidityPeriod 对象，未找到返回 None
        """
        # 先检测长期有效
        if self.PERMANENT_PATTERN.search(text):
            return ValidityPeriod(value=0, unit="permanent", is_permanent=True)
        
        # 正则模式列表
        patterns = [
            # 数字 + 单位格式
            (r"有效期[限\s为]*[:：]?\s*(\d+)\s*年", "years"),
            (r"有效期[限\s为]*[:：]?\s*(\d+)\s*个月", "months"),
            (r"有效期[限\s为]*[:：]?\s*(\d+)\s*月", "months"),
            (r"有效期[限\s为]*[:：]?\s*(\d+)\s*天", "days"),
            (r"有效期[限\s为]*[:：]?\s*(\d+)\s*日", "days"),
            # 中文数字格式
            (r"有效期[限\s为]*[:：]?\s*([一二三四五六七八九十百千万]+)\s*年", "years_chinese"),
            (r"有效期[限\s为]*[:：]?\s*([一二三四五六七八九十百千万]+)\s*个月", "months_chinese"),
            (r"有效期[限\s为]*[:：]?\s*([一二三四五六七八九十百千万]+)\s*月", "months_chinese"),
            (r"有效期[限\s为]*[:：]?\s*([一二三四五六七八九十百千万]+)\s*天", "days_chinese"),
            (r"有效期[限\s为]*[:：]?\s*([一二三四五六七八九十百千万]+)\s*日", "days_chinese"),
        ]
        
        for pattern, unit in patterns:
            matches = list(re.finditer(pattern, text, re.IGNORECASE))
            if matches:
                match = matches[0]
                try:
                    value_str = match.group(1)
                    if "chinese" in unit:
                        value = self._chinese_to_number(value_str)
                        unit = unit.replace("_chinese", "")
                    else:
                        value = int(value_str)
                    return ValidityPeriod(value=value, unit=unit, is_permanent=False)
                except (ValueError, IndexError):
                    continue
        
        return None
    
    async def _extract_validity_period_async(self, text: str) -> ValidityExtractionResult:
        """
        步骤 1: 提取有效期（Validity Period）
            
        提取策略：
        0. 如果配置了 validity_retriever，优先走 RAG 分支：
           a. 不需要关键词定位，直接检索整篇文档
           b. 得分燃断：得分全部小于阈値时跳过 LLM，将 has_validity=False 返回
           c. 对 top-K Chunk 依次调用 _extract_validity_with_llm
           d. Top-K 均未提取有效期，回退到原有关键词+正则流程
        1. 先检测长期有效（不需要“有效期”关键词）
        2. 关键词定位：寻找“有效期”关键词
        3. 动态切片：截取关键词吀50字符内的内容
        4. 快速探测：使用正则检测是否有数字/时间词
        5. LLM提取：如果检测到数字，使用LLM提取结构化有效期
        6. 正则备用：LLM失败时使用正则提取
        7. 未知处理：如果匹配到“有效期”但无法提取具体时间，标记为UNKNOWN
            
        Args:
            text: 文档文本内容
                
        Returns:
            ValidityExtractionResult 对象
        """
        # --- RAG 分支（如果配置了 validity_retriever）---
        if self.validity_retriever is not None:
            try:
                has_validity, chunks = await self.validity_retriever.retrieve(text)
                if not has_validity:
                    # 得分燃断：文档中无有效期信息，跳过 LLM
                    logger.debug("RAG 得分燃断，文档中无有效期信息")
                    return ValidityExtractionResult(period=None, source="none")
    
                # 对 top-K Chunk 依次尝试 LLM 提取
                if self.llm_client:
                    for chunk in chunks:
                        period = await self._extract_validity_with_llm(chunk.text)
                        if period:
                            logger.debug(
                                f"RAG+LLM 提取有效期成功，得分={chunk.score:.3f}"
                            )
                            return ValidityExtractionResult(period=period, source="rag+llm")
    
                # Top-K 均未提取成功，回退到关键词+正则流程
                logger.debug("RAG Top-K 均未提取到有效期，回退到关键词正则流程")
    
            except Exception as e:
                logger.warning(f"RAG 检索异常，回退到原正则流程: {e}")
        # --- RAG 分支结束 ---
    
        # 1. 先检测长期有效（不需要“有效期”关键词）
        if self.PERMANENT_PATTERN.search(text):
            return ValidityExtractionResult(
                period=ValidityPeriod(value=0, unit="permanent", is_permanent=True),
                source="regex"
            )
            
        # 2. 关键词定位
        keyword_positions = self._locate_validity_keyword(text)
            
        if not keyword_positions:
            # 没有找到“有效期”关键词
            return ValidityExtractionResult(period=None, source="none")
            
        found_keyword_without_time = False
            
        # 对每个关键词位置尝试提取
        for pos in keyword_positions:
            # 3. 动态切片
            context = self._extract_context_slice(text, pos, max_chars=50)
                
            # 4. 快速探测
            if not self._has_number_or_time(context):
                # 匹配到“有效期”但没有数字/时间词
                logger.debug(f"匹配到'有效期'但无具体时间: {context}")
                found_keyword_without_time = True
                continue
                
            # 5. 尝试使用 LLM 提取
            if self.llm_client:
                period = await self._extract_validity_with_llm(context)
                if period:
                    return ValidityExtractionResult(period=period, source="llm")
                
            # 6. LLM 失败或未配置，使用正则备用
            period = self._extract_validity_regex(context)
            if period:
                return ValidityExtractionResult(period=period, source="regex")
            
        # 7. 所有位置都尝试过
        if found_keyword_without_time:
            # 匹配到“有效期”但无法提取具体时间，标记为UNKNOWN
            return ValidityExtractionResult(
                period=ValidityPeriod(value=0, unit="unknown", is_permanent=False),
                source="unknown"
            )
            
        return ValidityExtractionResult(period=None, source="none")
    
    def _extract_validity_period(self, text: str) -> Optional[ValidityPeriod]:
        """
        同步版本：提取有效期（供非异步上下文使用）
        
        注意：此方法只使用正则提取，不使用LLM
        
        Args:
            text: 文档文本内容
            
        Returns:
            ValidityPeriod 对象，未找到返回 None，匹配到但无法提取返回 UNKNOWN
        """
        # 先检测长期有效（不需要"有效期"关键词）
        if self.PERMANENT_PATTERN.search(text):
            return ValidityPeriod(value=0, unit="permanent", is_permanent=True)
        
        # 关键词定位
        keyword_positions = self._locate_validity_keyword(text)
        
        if not keyword_positions:
            return None
        
        found_keyword_without_time = False
        
        for pos in keyword_positions:
            context = self._extract_context_slice(text, pos, max_chars=50)
            
            if not self._has_number_or_time(context):
                # 匹配到"有效期"但无具体时间
                found_keyword_without_time = True
                continue
            
            period = self._extract_validity_regex(context)
            if period:
                return period
        
        # 所有位置都尝试过
        if found_keyword_without_time:
            # 匹配到"有效期"但无法提取具体时间，标记为UNKNOWN
            return ValidityPeriod(value=0, unit="unknown", is_permanent=False)
        
        return None

    def _extract_all_dates(self, text: str) -> List[DateMatch]:
        """
        提取文本中所有日期

        Args:
            text: 文档文本

        Returns:
            DateMatch 列表
        """
        dates = []
        for pattern, fmt in self.DATE_PATTERNS:
            for match in re.finditer(pattern, text):
                try:
                    groups = match.groups()
                    year = int(groups[0])
                    month = int(groups[1])
                    day = int(groups[2])

                    # 验证日期有效性
                    if 1900 <= year <= 2100 and 1 <= month <= 12 and 1 <= day <= 31:
                        dt = datetime(year, month, day)
                        dates.append(
                            DateMatch(
                                date=dt, position=match.start(), distance_to_keyword=float("inf")
                            )
                        )
                except (ValueError, IndexError):
                    continue
        return dates

    def _find_nearest_keyword_distance(self, text: str, position: int) -> int:
        """
        计算指定位置到最近关键词的字符距离

        Args:
            text: 文档文本
            position: 日期位置

        Returns:
            到最近关键词的字符距离（如果没有匹配到任何关键词，返回一个足够大的值）
        """
        min_distance = float("inf")

        for keyword in self.SIGN_KEYWORDS:
            for match in re.finditer(keyword, text):
                keyword_pos = match.start()
                distance = abs(position - keyword_pos)
                min_distance = min(min_distance, distance)

        # 如果没有匹配到任何关键词，返回一个足够大的值（大于阈值）
        # 确保调用方能够正确识别"无关键词"的情况
        KEYWORD_PROXIMITY_THRESHOLD = 500
        if min_distance == float("inf"):
            return KEYWORD_PROXIMITY_THRESHOLD + 1

        return int(min_distance)

    def _extract_sign_date(self, text: str) -> Optional[datetime]:
        """
        步骤 2: 提取落款日期（Sign Date）

        启发式规则：
        1. 优先选取距离"签发"、"日期"、"盖章"、"签字"等关键词最近的日期
        2. 如果无明显关键词，默认取文档末尾（倒序查找）的最后一个日期

        Args:
            text: 文档文本内容

        Returns:
            datetime 对象，未找到则返回 None
        """
        # 提取所有日期
        dates = self._extract_all_dates(text)

        if not dates:
            return None

        # 计算每个日期到最近关键词的距离
        dated_with_distance = []
        for dm in dates:
            distance = self._find_nearest_keyword_distance(text, dm.position)
            dated_with_distance.append(
                DateMatch(date=dm.date, position=dm.position, distance_to_keyword=distance)
            )

        # 检查是否有日期靠近关键词（距离小于阈值，比如500字符）
        KEYWORD_PROXIMITY_THRESHOLD = 500
        near_keyword_dates = [
            dm for dm in dated_with_distance if dm.distance_to_keyword < KEYWORD_PROXIMITY_THRESHOLD
        ]

        if near_keyword_dates:
            # 优先选择距离关键词最近的日期
            nearest = min(near_keyword_dates, key=lambda x: x.distance_to_keyword)
            return nearest.date
        else:
            # 无明显关键词，取文档末尾的最后一个日期（按位置排序，取最后一个）
            latest_position_date = max(dates, key=lambda x: x.position)
            return latest_position_date.date

    def _get_reference_time(self, config: Dict[str, Any]) -> datetime:
        """
        步骤 3: 确定比对基准时间（Reference Time）

        如果调用方传入了校验时间参数，则使用传入时间；
        如果未传入，则直接获取服务器当前真实时间（datetime.now()）作为基准时间。

        Args:
            config: 检查配置，可能包含 reference_time

        Returns:
            基准时间 datetime 对象
        """
        # 检查配置中是否有传入的校验时间
        reference_time_str = config.get("reference_time")

        if reference_time_str:
            try:
                # 尝试解析传入的时间字符串
                # 支持格式: YYYY-MM-DD, YYYY-MM-DD HH:MM:SS, ISO格式
                for fmt in ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"]:
                    try:
                        return datetime.strptime(reference_time_str, fmt)
                    except ValueError:
                        continue
                # 尝试 ISO 格式
                from datetime import timezone

                return datetime.fromisoformat(reference_time_str.replace("Z", "+00:00"))
            except Exception:
                logger.warning(f"无法解析传入的校验时间: {reference_time_str}，使用当前时间")

        # 使用当前服务器时间
        return datetime.now()

    def _calculate_expiry_date(self, sign_date: datetime, validity: ValidityPeriod) -> datetime:
        """
        根据落款日期和有效期计算截止日期

        Args:
            sign_date: 落款日期
            validity: 有效期

        Returns:
            截止日期
        """
        if validity.is_permanent:
            # 长期有效，返回一个极远的日期
            return datetime(2099, 12, 31)

        if validity.unit == "years":
            return sign_date + relativedelta(years=validity.value)
        elif validity.unit == "months":
            return sign_date + relativedelta(months=validity.value)
        elif validity.unit == "days":
            return sign_date + timedelta(days=validity.value)
        else:
            return sign_date + relativedelta(years=1)  # 默认一年

    def _build_validity_description(self, validity: Optional[ValidityPeriod]) -> str:
        """
        构建有效期说明文本
        
        Args:
            validity: 有效期对象
            
        Returns:
            有效期描述文本
        """
        if not validity:
            return "长期有效（未声明有效期）"
        
        if validity.is_permanent:
            return "长期有效"
        elif validity.unit == "years":
            return f"有效期{validity.value}年"
        elif validity.unit == "months":
            return f"有效期{validity.value}个月"
        elif validity.unit == "days":
            return f"有效期{validity.value}天"
        elif validity.unit == "unknown":
            return "有效期未知（文档中提到有效期但无法确定具体时间）"
        else:
            return f"有效期{validity.value}{validity.unit}"
    
    def _evaluate_with_validity(
        self,
        result: Dict[str, Any],
        validity: Optional[ValidityPeriod],
        sign_date: Optional[datetime],
        reference_time: datetime,
    ) -> Dict[str, Any]:
        """
        根据有效期和落款日期进行判定
        
        Args:
            result: 结果字典
            validity: 有效期对象
            sign_date: 落款日期
            reference_time: 基准时间
            
        Returns:
            更新后的结果字典
        """
        has_validity = validity is not None and validity.unit != "unknown"
        has_unknown_validity = validity is not None and validity.unit == "unknown"
        has_sign_date = sign_date is not None
        
        sign_date_str = result["sign_date"] if result["sign_date"] else "未提取到"
        ref_time_str = reference_time.strftime("%Y-%m-%d")
        validity_desc = self._build_validity_description(validity)
        
        # 处理有效期未知的情况
        if has_unknown_validity:
            result["branch"] = "UNKNOWN"
            result["passed"] = False
            if has_sign_date:
                result["reason"] = (
                    f"印章时间{sign_date_str}，{validity_desc}，无法完成时效性审查。"
                )
            else:
                result["reason"] = (
                    f"印章时间未提取到，{validity_desc}，无法完成时效性审查。"
                )
            return result
        
        # 分支 A：有有效期但无落款日期
        if has_validity and not has_sign_date:
            result["branch"] = "A"
            result["passed"] = False
            result["reason"] = (
                f"印章时间未提取到，{validity_desc}，晚于当前时间{ref_time_str}，有效期审查未通过。"
            )
            return result

        # 分支 B：有落款日期但无有效期（视为长期有效）
        if has_sign_date and not has_validity:
            result["branch"] = "B"
            result["validity"] = {"is_permanent": True}

            if sign_date <= reference_time:
                result["passed"] = True
                result["reason"] = (
                    f"印章时间{sign_date_str}，长期有效，早于当前时间{ref_time_str}，有效期审查通过。"
                )
            else:
                result["passed"] = False
                result["reason"] = (
                    f"印章时间{sign_date_str}，长期有效，晚于当前时间{ref_time_str}，有效期审查未通过。"
                )
            return result

        # 分支 C：两者都有
        if has_sign_date and has_validity and validity:
            result["branch"] = "C"
            expiry_date = self._calculate_expiry_date(sign_date, validity)
            result["expiry_date"] = expiry_date.strftime("%Y-%m-%d")
            expiry_date_str = result["expiry_date"]

            # 判定条件：落款日期 ≤ 基准时间 ≤ 截止日期
            if sign_date > reference_time:
                result["passed"] = False
                result["reason"] = (
                    f"印章时间{sign_date_str}，{validity_desc}，晚于当前时间{ref_time_str}，有效期审查未通过。"
                )
            elif reference_time > expiry_date:
                result["passed"] = False
                result["reason"] = (
                    f"印章时间{sign_date_str}，{validity_desc}，早于当前时间{ref_time_str}但已过期（有效期至{expiry_date_str}），有效期审查未通过。"
                )
            else:
                result["passed"] = True
                if validity.is_permanent:
                    result["reason"] = (
                        f"印章时间{sign_date_str}，{validity_desc}，早于当前时间{ref_time_str}，有效期审查通过。"
                    )
                else:
                    result["reason"] = (
                        f"印章时间{sign_date_str}，{validity_desc}，早于当前时间{ref_time_str}且在有效期内（至{expiry_date_str}），有效期审查通过。"
                    )
            return result

        # 特殊情况：两者都没有
        result["branch"] = "NONE"
        result["passed"] = False
        result["reason"] = f"印章时间未提取到，有效期信息缺失，无法完成时效性审查。"
        return result

    def evaluate_document(self, document: Document, reference_time: datetime) -> Dict[str, Any]:
        """
        步骤 4: 核心判定矩阵（同步版本）

        判定分支：
        - 分支 A：有有效期但无落款日期 → 不通过
        - 分支 B：有落款日期但无有效期（长期有效）→ 落款日期 ≤ 基准时间则通过
        - 分支 C：两者都有 → 落款日期 ≤ 基准时间 ≤ 截止日期则通过
        - 分支 UNKNOWN：有有效期声明但无法提取具体时间 → 不通过

        Args:
            document: 文档对象
            reference_time: 基准时间

        Returns:
            判定结果字典
        """
        text = document.content or ""

        # 提取有效期和落款日期
        validity = self._extract_validity_period(text)
        sign_date = self._extract_sign_date(text)

        result = {
            "document_name": document.name,
            "has_validity": validity is not None and validity.unit != "unknown",
            "has_sign_date": sign_date is not None,
            "validity": None,
            "sign_date": sign_date.strftime("%Y-%m-%d") if sign_date else None,
            "expiry_date": None,
            "reference_time": reference_time.strftime("%Y-%m-%d %H:%M:%S"),
            "passed": False,
            "reason": "",
            "branch": None,
        }

        if validity:
            result["validity"] = {
                "value": validity.value,
                "unit": validity.unit,
                "is_permanent": validity.is_permanent,
            }

        return self._evaluate_with_validity(result, validity, sign_date, reference_time)
    
    async def evaluate_document_async(self, document: Document, reference_time: datetime) -> Dict[str, Any]:
        """
        步骤 4: 核心判定矩阵（异步版本，支持LLM提取）

        判定分支：
        - 分支 A：有有效期但无落款日期 → 不通过
        - 分支 B：有落款日期但无有效期（长期有效）→ 落款日期 ≤ 基准时间则通过
        - 分支 C：两者都有 → 落款日期 ≤ 基准时间 ≤ 截止日期则通过
        - 分支 UNKNOWN：有有效期声明但无法提取具体时间 → 不通过

        Args:
            document: 文档对象
            reference_time: 基准时间

        Returns:
            判定结果字典
        """
        text = document.content or ""

        # 使用异步版本提取有效期（支持LLM）
        extraction_result = await self._extract_validity_period_async(text)
        validity = extraction_result.period
        sign_date = self._extract_sign_date(text)

        result = {
            "document_name": document.name,
            "has_validity": validity is not None and validity.unit != "unknown",
            "has_sign_date": sign_date is not None,
            "validity": None,
            "sign_date": sign_date.strftime("%Y-%m-%d") if sign_date else None,
            "expiry_date": None,
            "reference_time": reference_time.strftime("%Y-%m-%d %H:%M:%S"),
            "passed": False,
            "reason": "",
            "branch": None,
            "validity_source": extraction_result.source,  # 记录提取来源
        }

        if validity:
            result["validity"] = {
                "value": validity.value,
                "unit": validity.unit,
                "is_permanent": validity.is_permanent,
            }

        return self._evaluate_with_validity(result, validity, sign_date, reference_time)

    async def check(
        self, documents: List[Document], checklist: Optional[Checklist], config: Dict[str, Any]
    ) -> CheckResult:
        """
        执行时效性检查

        Args:
            documents: 文档列表
            checklist: 审核清单（可选）
            config: 检查配置
                - reference_time: 自定义校验时间（可选）
                - use_llm: 是否使用LLM提取有效期（可选，默认True如果llm_client已配置）

        Returns:
            CheckResult: 检查结果
        """
        if not documents:
            return CheckResult(
                check_type=self.name,
                status=CheckStatus.PASS,
                message="没有文档需要检查时效性",
                details={},
            )

        # 步骤 3: 确定基准时间
        reference_time = self._get_reference_time(config)
        
        # 检查是否使用LLM
        use_llm = config.get("use_llm", self.llm_client is not None)

        try:
            document_results = []
            passed_count = 0
            failed_count = 0
            unclear_count = 0
            unknown_count = 0
            issues = []

            for doc in documents:
                # 步骤 4: 对每个文档执行核心判定
                if use_llm and self.llm_client:
                    eval_result = await self.evaluate_document_async(doc, reference_time)
                else:
                    eval_result = self.evaluate_document(doc, reference_time)
                document_results.append(eval_result)

                if eval_result["passed"]:
                    passed_count += 1
                elif eval_result["branch"] == "NONE":
                    unclear_count += 1
                elif eval_result["branch"] == "UNKNOWN":
                    unknown_count += 1
                    failed_count += 1
                    issues.append(
                        {
                            "type": "timeliness_unknown",
                            "document": doc.name,
                            "branch": eval_result["branch"],
                            "reason": eval_result["reason"],
                            "sign_date": eval_result["sign_date"],
                            "expiry_date": eval_result["expiry_date"],
                        }
                    )
                else:
                    failed_count += 1
                    issues.append(
                        {
                            "type": "timeliness_failed",
                            "document": doc.name,
                            "branch": eval_result["branch"],
                            "reason": eval_result["reason"],
                            "sign_date": eval_result["sign_date"],
                            "expiry_date": eval_result["expiry_date"],
                        }
                    )

            # 确定整体状态
            if failed_count > 0:
                status = CheckStatus.FAIL
            elif unclear_count > 0:
                status = CheckStatus.UNAVAILABLE
            else:
                status = CheckStatus.PASS

            # 构建详细信息
            details = {
                "checked": len(documents),
                "passed": passed_count,
                "failed": failed_count,
                "unclear": unclear_count,
                "unknown": unknown_count,
                "reference_time": reference_time.strftime("%Y-%m-%d %H:%M:%S"),
                "documents": document_results,
            }

            # 构建消息
            message = f"时效性检查完成: {passed_count}/{len(documents)} 文档通过"
            if failed_count > 0:
                message += f", {failed_count} 个文档未通过"
            if unclear_count > 0:
                message += f", {unclear_count} 个文档信息不明确"
            if unknown_count > 0:
                message += f", {unknown_count} 个文档有效期未知"

            return CheckResult(
                check_type=self.name, status=status, message=message, details=details, issues=issues
            )

        except Exception as e:
            logger.exception(f"时效性检查失败: {e}")
            return CheckResult(
                check_type=self.name,
                status=CheckStatus.ERROR,
                message=f"检查执行异常: {str(e)}",
                details={"error": str(e)},
            )

    def validate_config(self, config: Dict[str, Any]) -> Tuple[bool, str]:
        """验证配置"""
        reference_time = config.get("reference_time")
        if reference_time and not isinstance(reference_time, str):
            return False, "reference_time 必须是字符串格式"
        return True, ""
