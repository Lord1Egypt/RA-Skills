"""
文本切块器模块

职责：
1. 文本清洗（降噪）：剔除表格线、全角空格、连续空白等干扰字符，提升文本密度
2. 滑动窗口分块：将长文本切成固定大小的重叠 Chunk
3. 语义边界回退：在切断点向前回退，找到最近的标点/空格，防止日期被截断

遵循架构规范：属于 Infrastructure 层，不依赖 Domain/Core 业务逻辑。
"""

import re
import logging
from typing import List, Tuple

logger = logging.getLogger(__name__)


class ValidityTextChunker:
    """
    有效期文本切块器

    负责对合规文档全文进行清洗和滑动窗口分块，
    确保每个 Chunk 都是相对完整的自然语言片段。

    设计要点：
    - 清洗阶段剔除噪声字符，提升后续 Embedding 质量
    - 语义边界回退：切断点优先对齐标点或空格，防止 "2024-12-" 被切断
    - 支持 overlap 参数，保证跨行日期不因分块丢失
    """

    # 语义边界字符：切断点可以回退到这些位置
    BOUNDARY_CHARS = set("，。；！？\n ；、：:;,.?! \t")

    # 最大回退步数：超过此距离则在原位切断（防止 Chunk 过短）
    MAX_LOOKBACK = 30

    def clean(self, text: str) -> str:
        """
        文本降噪与密度提升

        清洗步骤：
        1. 替换全角空格、制表符为普通空格
        2. 剔除表格线字符（│、─、┼、┃、━ 等）
        3. 剔除 PDF 提取常见的乱码符号（页眉页脚分隔线）
        4. 压缩连续空白（超过2个空格压缩为1个）
        5. 压缩连续换行（超过2个换行压缩为1个）

        Args:
            text: 原始文档文本

        Returns:
            清洗后的文本
        """
        if not text:
            return ""

        # 1. 全角空格、制表符 → 普通空格
        text = text.replace("\u3000", " ").replace("\t", " ")

        # 2. 剔除表格线字符（Unicode 制表符范围 U+2500-U+257F）
        text = re.sub(r"[\u2500-\u257f]+", " ", text)

        # 3. 剔除常见 PDF 噪声：连续的 ─ = - * ~ 等分隔线
        text = re.sub(r"[-=─*~_]{3,}", " ", text)

        # 4. 剔除不可见控制字符（保留换行）
        text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)

        # 5. 压缩连续空白（2个以上空格 → 1个）
        text = re.sub(r" {2,}", " ", text)

        # 6. 压缩连续换行（3个以上换行 → 2个）
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()

    def _find_boundary(self, text: str, ideal_end: int) -> int:
        """
        语义边界回退：从 ideal_end 向前找最近的语义边界字符。

        如果在 MAX_LOOKBACK 步内找到边界，则在该边界位置切断；
        否则在 ideal_end 原位切断，防止 Chunk 过短。

        Args:
            text: 文本内容
            ideal_end: 理想切断位置（exclusive）

        Returns:
            实际切断位置（exclusive）
        """
        # 不超出文本范围
        ideal_end = min(ideal_end, len(text))

        # 从 ideal_end 向前回溯
        lookback_start = max(0, ideal_end - self.MAX_LOOKBACK)

        for i in range(ideal_end - 1, lookback_start - 1, -1):
            if text[i] in self.BOUNDARY_CHARS:
                # 在边界字符之后切断（包含边界字符本身）
                return i + 1

        # 没找到边界，在原位切断
        return ideal_end

    def chunk(
        self,
        text: str,
        chunk_size: int = 200,
        overlap: int = 50,
    ) -> List[Tuple[str, int]]:
        """
        滑动窗口分块，带语义边界回退

        算法：
        1. 从 pos=0 开始，每次取 [pos, pos+chunk_size] 的文本
        2. 调用 _find_boundary 在切断点附近寻找最近标点
        3. 下一个 Chunk 从 (end_pos - overlap) 开始，保证重叠
        4. 返回 (chunk_text, start_pos) 元组列表

        Args:
            text: 清洗后的文本（建议先调用 clean()）
            chunk_size: 每个 Chunk 的目标字符数
            overlap: 相邻 Chunk 的重叠字符数

        Returns:
            [(chunk_text, start_pos), ...] 列表
        """
        if not text:
            return []

        chunks: List[Tuple[str, int]] = []
        pos = 0
        text_len = len(text)

        while pos < text_len:
            # 理想的切断终点
            ideal_end = pos + chunk_size

            if ideal_end >= text_len:
                # 最后一块，直接取到末尾
                chunk_text = text[pos:].strip()
                if chunk_text:
                    chunks.append((chunk_text, pos))
                break

            # 语义边界回退
            actual_end = self._find_boundary(text, ideal_end)

            # 防止死循环：如果 actual_end <= pos，强制前进
            if actual_end <= pos:
                actual_end = pos + chunk_size

            chunk_text = text[pos:actual_end].strip()
            if chunk_text:
                chunks.append((chunk_text, pos))

            # 下一个窗口起点（退回 overlap 个字符以保证重叠）
            next_pos = actual_end - overlap
            if next_pos <= pos:
                next_pos = pos + 1  # 保证至少前进 1 步

            pos = next_pos

        logger.debug(
            f"分块完成：文本长度={text_len}，chunk_size={chunk_size}，"
            f"overlap={overlap}，共 {len(chunks)} 个 Chunk"
        )
        return chunks
