#!/usr/bin/env python3
"""大象沟通日报生成脚本。"""

import argparse
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

SKILL_DIR = Path("/Users/hongfei/.openclaw/skills/daxiang-daily-report")
WORKSPACE = Path(os.environ.get("DAXIANG_WORKSPACE", "/Users/hongfei/.openclaw/workspace-taizi"))
DATA_DIR = Path(os.environ.get("DAXIANG_DATA_DIR", str(WORKSPACE / "data")))
REPORT_DIR = Path(os.environ.get("DAXIANG_REPORT_DIR", str(DATA_DIR)))
SELF_NAME = os.environ.get("DAXIANG_SELF_NAME", "洪飞")
MAX_PERIOD_ROWS = int(os.environ.get("DAXIANG_PERIOD_ROWS", "8"))
MAX_PERSON_ROWS = int(os.environ.get("DAXIANG_PERSON_ROWS", "8"))
MAX_GROUP_ROWS = int(os.environ.get("DAXIANG_GROUP_ROWS", "10"))
MAX_TODO_ROWS = int(os.environ.get("DAXIANG_TODO_ROWS", "8"))

SYSTEM_KEYWORDS = (
    "avatar",
    "octo",
    "日历",
    "审批",
    "财务",
    "it",
    "系统",
    "告警",
    "监控",
    "通知",
    "提醒",
)

TOPIC_RULES: Sequence[Tuple[str, Sequence[str]]] = (
    ("AI/工具协作", ("ai", "agent", "模型", "claude", "gemini", "minimax", "openclaw", "提示词")),
    ("项目推进", ("项目", "上线", "排期", "进度", "发布", "交付", "方案", "计划", "需求")),
    ("团队管理", ("职责", "边界", "管理", "周会", "对齐", "老板", "组织", "汇报", "例会")),
    ("运维告警", ("告警", "报警", "监控", "p0", "故障", "红警", "sre", "恢复")),
    ("行政流程", ("报销", "审批", "财务", "it", "权限", "会议", "日历", "流程")),
)

TODO_KEYWORDS = (
    "请",
    "需要",
    "麻烦",
    "跟进",
    "同步",
    "安排",
    "确认",
    "处理",
    "推进",
    "对齐",
    "看下",
    "补充",
    "更新",
    "沟通",
    "review",
    "check",
    "follow",
)

PERIODS = (
    ("上午", "☀️", "9:00~14:00", lambda hour: 9 <= hour < 14),
    ("下午", "🌤️", "14:00~19:00", lambda hour: 14 <= hour < 19),
    ("晚间", "🌙", "19:00~23:00", lambda hour: 19 <= hour < 23),
    ("凌晨", "🌃", "23:00~次日凌晨9:00", lambda hour: hour >= 23 or hour < 9),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="大象沟通日报生成脚本")
    parser.add_argument("--date", type=str, help="指定日期，支持 YYYYMMDD 或 YYYY-MM-DD")
    parser.add_argument("--force", action="store_true", help="强制覆盖当天最新版本")
    return parser.parse_args()



def parse_date(date_str: Optional[str]) -> datetime:
    if not date_str:
        return datetime.now() - timedelta(days=1)

    for fmt in ("%Y%m%d", "%Y-%m-%d"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    raise ValueError(f"日期格式错误: {date_str}，支持 YYYYMMDD 或 YYYY-MM-DD")



def normalize_text(text: str) -> str:
    if not text:
        return ""
    compact = re.sub(r"\s+", " ", text.replace("|", "｜")).strip()
    return compact



def shorten(text: str, limit: int = 42) -> str:
    compact = normalize_text(text)
    if len(compact) <= limit:
        return compact
    return compact[: limit - 1].rstrip() + "…"



def is_system_name(name: str) -> bool:
    lowered = name.lower()
    return any(keyword in lowered for keyword in SYSTEM_KEYWORDS)



def format_display_date(target_date: datetime) -> str:
    return target_date.strftime("%Y年%m月%d日")



def fetch_messages_via_dx(date_key: str) -> List[Dict]:
    """通过DX CLI自动获取大象消息数据"""
    import subprocess
    from datetime import datetime
    
    # 计算日期时间戳
    year = int(date_key[:4])
    month = int(date_key[4:6])
    day = int(date_key[6:8])
    start_ts = int(datetime(year, month, day, 0, 0, 0).timestamp() * 1000)
    end_ts = int(datetime(year, month, day, 23, 59, 59).timestamp() * 1000)
    
    print(f"   通过DX CLI获取 {date_key} 的消息数据...")
    
    # 检查dx命令是否可用
    try:
        result = subprocess.run(['dx', '--help'], capture_output=True, text=True, timeout=5)
        if result.returncode != 0 and 'Daxiang' not in result.stdout:
            raise FileNotFoundError("dx command not found")
    except FileNotFoundError:
        raise FileNotFoundError("DX CLI未安装，请先安装：npm i -g @mtfe/meituan-dx --registry=http://r.npm.sankuai.com")
    
    all_messages = []
    
    # 获取私聊会话列表
    try:
        result = subprocess.run(
            ['dx', 'sessions', 'chats', '--full', '--limit', '100', '--json'],
            capture_output=True, text=True, timeout=60
        )
        sessions = json.loads(result.stdout) if result.stdout else []
        print(f"   获取到 {len(sessions)} 个私聊会话")
    except Exception as e:
        print(f"   获取会话列表失败: {e}")
        sessions = []
    
    # 获取每个私聊的历史消息
    for i, session in enumerate(sessions[:30]):  # 最多30个会话
        uid = session.get('id')
        name = session.get('name', '未知')
        
        try:
            result = subprocess.run(
                ['dx', 'sessions', 'show', uid, '--history', '100', '--json'],
                capture_output=True, text=True, timeout=30
            )
            data = json.loads(result.stdout) if result.stdout else {}
            messages = data.get('messages', [])
            
            # 过滤日期范围
            for m in messages:
                ts = m.get('timestamp', 0)
                if start_ts <= ts <= end_ts:
                    m['source_name'] = name
                    m['source_type'] = 'chat'
                    all_messages.append(m)
        except Exception as e:
            print(f"   获取会话 {name} 失败: {e}")
    
    # 获取群聊会话列表
    try:
        result = subprocess.run(
            ['dx', 'sessions', 'groups', '--full', '--limit', '50', '--json'],
            capture_output=True, text=True, timeout=60
        )
        groups = json.loads(result.stdout) if result.stdout else []
        print(f"   获取到 {len(groups)} 个群聊会话")
    except Exception as e:
        print(f"   获取群聊列表失败: {e}")
        groups = []
    
    # 获取每个群聊的历史消息
    for i, group in enumerate(groups[:30]):  # 最多30个群
        gid = group.get('id')
        name = group.get('name', '未知')
        
        try:
            result = subprocess.run(
                ['dx', 'sessions', 'show', gid, '--history', '100', '--json'],
                capture_output=True, text=True, timeout=30
            )
            data = json.loads(result.stdout) if result.stdout else {}
            messages = data.get('messages', [])
            
            # 过滤日期范围
            for m in messages:
                ts = m.get('timestamp', 0)
                if start_ts <= ts <= end_ts:
                    m['source_name'] = name
                    m['source_type'] = 'group'
                    all_messages.append(m)
        except Exception as e:
            print(f"   获取群 {name} 失败: {e}")
    
    print(f"   共获取 {len(all_messages)} 条消息")
    return all_messages


def detect_data_format(data: List[Dict]) -> str:
    """
    检测数据格式类型。
    
    旧格式：[{type: "chat", name: "xxx", messages: [...]}]
    新格式：[{id: "xxx", type: "chat", name: "xxx", text: "xxx", timestamp: xxx}]
    
    Returns:
        "old": 旧格式（按会话分组）
        "new": 新格式（扁平消息列表）
    """
    if not data or not isinstance(data, list):
        raise ValueError("数据格式错误：期望非空列表")
    
    first_item = data[0]
    
    # 旧格式特征：包含 `messages` 字段（消息数组）
    if "messages" in first_item and isinstance(first_item.get("messages"), list):
        return "old"
    
    # 新格式特征：直接包含 `text` 和 `timestamp` 字段（单条消息）
    if "text" in first_item and "timestamp" in first_item:
        return "new"
    
    # 无法识别格式
    raise ValueError(f"无法识别的数据格式：{list(first_item.keys())[:5]}...")


def normalize_conversations(data: List[Dict], format_type: str) -> List[Dict]:
    """
    将不同格式的数据统一转换为旧格式（按会话分组）。
    
    转换后的格式：
    [{type: "chat", name: "xxx", uid: "xxx", messages: [...]}]
    """
    if format_type == "old":
        # 已经是旧格式，直接返回
        return data
    
    if format_type == "new":
        # 新格式：扁平消息列表 -> 按会话分组
        print(f"   检测到新格式数据，共 {len(data)} 条消息，正在转换...")
        
        # 按 uid/type 分组
        groups: Dict[Tuple[str, str], Dict] = {}
        
        for msg in data:
            uid = msg.get("uid", "")
            msg_type = msg.get("type", "chat")
            key = (uid, msg_type)
            
            if key not in groups:
                groups[key] = {
                    "type": msg_type,
                    "name": msg.get("source_name") or msg.get("name", "未知"),
                    "uid": uid,
                    "messages": []
                }
            
            # 构建消息对象
            message_obj = {
                "id": msg.get("id", ""),
                "uid": uid,
                "type": msg_type,
                "name": msg.get("name", ""),
                "text": msg.get("text", ""),
                "timestamp": msg.get("timestamp", 0),
                "raw": msg.get("raw", {})
            }
            groups[key]["messages"].append(message_obj)
        
        # 转换为列表
        conversations = list(groups.values())
        print(f"   转换完成：{len(conversations)} 个会话")
        return conversations
    
    raise ValueError(f"不支持的格式类型: {format_type}")


def load_message_file(date_key: str, auto_fetch: bool = True) -> List[Dict]:
    """
    加载消息数据文件，自动检测并转换数据格式。
    
    支持两种格式：
    - 旧格式：[{type: "chat", name: "xxx", messages: [...]}]
    - 新格式：[{id: "xxx", type: "chat", name: "xxx", text: "xxx", timestamp: xxx}]
    
    Returns:
        统一格式的数据列表（按会话分组）
    """
    message_file = DATA_DIR / f"daxiang_messages_{date_key}_full.json"
    if not message_file.exists():
        if auto_fetch:
            # 尝试自动获取数据
            print(f"数据文件不存在，尝试通过DX CLI自动获取...")
            try:
                messages = fetch_messages_via_dx(date_key)
                if messages:
                    # 保存到文件
                    DATA_DIR.mkdir(parents=True, exist_ok=True)
                    with open(message_file, "w", encoding="utf-8") as f:
                        json.dump(messages, f, ensure_ascii=False, indent=2)
                    print(f"   数据已保存到: {message_file}")
                    return messages
                else:
                    raise FileNotFoundError("DX CLI未返回任何消息数据")
            except Exception as e:
                raise FileNotFoundError(f"自动获取数据失败: {e}\n\n请确保：\n1. DX CLI已安装：npm i -g @mtfe/meituan-dx --registry=http://r.npm.sankuai.com\n2. 已完成dx login登录\n3. 数据目录有写权限：{DATA_DIR}")
        else:
            # 提供友好的错误提示和解决方案
            hint = f"""
=== 数据文件缺失 ===

请确保已获取大象消息数据文件：
1. 数据文件路径：{message_file}
2. 文件命名格式：daxiang_messages_{{日期}}_full.json（如 daxiang_messages_20260317_full.json）
3. 获取方式：
   - 通过大象网页版导出聊天记录
   - 或使用 DX CLI 工具自动获取（推荐）

当前数据目录：{DATA_DIR}
请设置环境变量 DAXIANG_DATA_DIR 指定数据目录路径。
"""
            raise FileNotFoundError(hint)
    
    # 加载数据文件
    with open(message_file, "r", encoding="utf-8") as file:
        raw_data = json.load(file)
    
    # 自动检测数据格式并转换
    try:
        format_type = detect_data_format(raw_data)
        print(f"   检测到数据格式: {format_type} 格式")
        
        # 转换为统一格式
        conversations = normalize_conversations(raw_data, format_type)
        return conversations
    except ValueError as e:
        print(f"   ⚠️ 数据格式检测失败: {e}")
        print(f"   尝试直接使用原始数据...")
        # 兼容处理：直接返回原始数据
        return raw_data



def message_time(message: Dict) -> datetime:
    timestamp = message.get("timestamp") or message.get("raw", {}).get("time")
    if timestamp is None:
        return datetime.now()
    return datetime.fromtimestamp(int(timestamp) / 1000)



def select_period(hour: int) -> Tuple[str, str, str]:
    for period_name, emoji, label, matcher in PERIODS:
        if matcher(hour):
            return period_name, emoji, label
    return PERIODS[-1][:3]



def detect_topic(messages: Sequence[Dict], fallback: str = "日常沟通") -> str:
    """基于消息内容精确定位具体话题。"""
    texts = [normalize_text(m.get("text", "")) for m in messages]
    combined = " ".join(texts).lower()

    # 更精细的主题识别 - 增加更多具体话题关键词
    topic_patterns = (
        # AI/技术类 - 细化具体话题
        (("提示词", "prompt", "工作流", "agent", "智能体", "openclaw", "claude code", "codex"), "AI工作流/自动化"),
        (("模型", "minimax", "gemini", "api", "token", "调用", "接口"), "模型调用/技术选型"),
        (("ai", "人工智能", "gpt", "llm"), "AI技术交流"),
        # 项目推进类 - 细化具体话题
        (("上线", "发布", "部署", "发版", "版本"), "上线发布"),
        (("排期", "进度", "计划", "甘特", "timeline"), "项目排期/进度"),
        (("需求", "功能", "PRD", "评审"), "需求评审"),
        (("开发", "代码", "bug", "重构", "优化"), "开发推进"),
        (("测试", "验收", "回归", "用例"), "测试验收"),
        # 团队管理类
        (("周会", "例会", "复盘", "周报", "汇报"), "会议汇报"),
        (("职责", "边界", "分工", "角色", "权限"), "职责分工"),
        (("招聘", "面试", "hc", "入职", "离职"), "人员调配"),
        # 运维告警类
        (("告警", "报警", "监控", "p0", "故障", "红警", "sre", "可用性", "服务挂了"), "故障处理/运维"),
        # 行政流程类
        (("报销", "审批", "财务", "合同", "采购", "付款"), "财务/行政"),
        (("权限", "it", "账号", "设备", "网络"), "IT支持"),
        (("会议", "日历", "约", "安排时间"), "日程安排"),
        # 业务沟通类
        (("客户", "需求方", "业务方", "对接"), "客户对接"),
        (("收入", "营收", "销售", "订单", "收入"), "业务收入"),
        (("产品", "功能", "方案", "卖点"), "产品方案"),
        # 个人事务类
        (("请假", "休息", "调休", "年假", "病假"), "请假/休息"),
        (("吃饭", "聚", "聊", "见面", "约"), "私人聚会"),
        (("下班", "明天", "周末", "放假", "休息"), "日常事务"),
    )

    for keywords, topic in topic_patterns:
        matches = sum(1 for kw in keywords if kw in combined)
        if matches >= 1:  # 降低匹配阈值，更精准识别具体话题
            return topic

    return fallback



# 预设标签库
TOPIC_TAGS = {
    "AI/工具协作": ["AI", "agent", "智能体", "提示词", "工作流", "自动化"],
    "项目推进": ["项目", "上线", "发布", "排期", "进度", "需求", "开发", "测试"],
    "团队管理": ["周会", "例会", "职责", "分工", "汇报", "对齐"],
    "运维告警": ["告警", "故障", "监控", "SRE", "可用性"],
    "行政流程": ["报销", "审批", "财务", "权限", "IT", "会议"],
    "生活安排": ["吃饭", "聚会", "出行", "请客", "安排"],
    "日常沟通": ["闲聊", "问候", "日常"],
}

# 消息关键词标签映射
MESSAGE_TAG_PATTERNS = {
    "AI": ["ai", "agent", "模型", "提示词", "prompt", "claude", "openai", "gemini", "minimax"],
    "项目": ["项目", "需求", "上线", "发布", "排期", "进度", "开发", "bug"],
    "任务": ["请", "需要", "麻烦", "安排", "跟进", "确认", "处理", "todo"],
    "团队": ["周会", "例会", "对齐", "汇报", "职责", "分工"],
    "生活": ["吃饭", "聚", "请客", "出行", "玩", "周末"],
    "日常": ["好", "收到", "行", "可以", "哈哈", "嗯"],
}


def collect_snippets(messages: Sequence[Dict], limit: int = 6, prefer_other_side: bool = False) -> List[str]:
    """提取更多关键消息片段，用于展示对话要点。"""
    snippets: List[str] = []
    processed_texts = set()

    # 优先提取对方的关键消息
    for message in messages:
        sender = message.get("name", "")
        if prefer_other_side and sender == SELF_NAME:
            continue
        text = normalize_text(message.get("text", ""))
        if not text or len(text) < 4:
            continue
        # 避免重复内容
        if text in processed_texts:
            continue
        processed_texts.add(text)
        snippets.append(shorten(text, 40))
        if len(snippets) >= limit:
            break

    # 如果优先模式没找到足够的，补充任何消息
    if len(snippets) < limit:
        for message in messages:
            text = normalize_text(message.get("text", ""))
            if not text or len(text) < 4:
                continue
            if text in processed_texts:
                continue
            processed_texts.add(text)
            snippets.append(shorten(text, 40))
            if len(snippets) >= limit:
                break

    return snippets[:limit]


def extract_discussion_summary(messages: Sequence[Dict]) -> Tuple[str, str, str]:
    """
    提炼讨论主题和双方观点。
    返回: (主题, 对方观点总结, 父皇观点总结)
    """
    topic = detect_topic(messages, fallback="日常沟通")

    other_points = []
    self_points = []

    for message in messages:
        text = normalize_text(message.get("text", ""))
        if not text or len(text) < 8:
            continue
        sender = message.get("name", "")

        # 提取关键判断/建议/结论
        key_indicators = (
            "认为", "觉得", "判断", "结论", "关键是", "本质", "事实是",
            "建议", "应该", "最好", "要不要", "不如", "试试",
            "需要", "必须", "麻烦", "请", "安排",
            "确定", "不行", "可以", "就这么办", "行", "好的", "收到",
        )

        if any(ind in text for ind in key_indicators):
            if sender == SELF_NAME:
                self_points.append(text)
            else:
                other_points.append(text)

    # 提炼对方观点 - 总结性描述
    other_summary = ""
    if other_points:
        # 分析对方的主要观点，给出总结
        key_text = other_points[0].lower()
        if "请" in key_text or "我请" in key_text or "你请" in key_text:
            other_summary = "提出请客/安排"
        elif "不用" in key_text or "不需要" in key_text:
            other_summary = "表示不需要"
        elif "可以" in key_text or "行" in key_text:
            other_summary = "表示同意/可行"
        elif "哈哈" in key_text or "哈哈哈" in key_text:
            other_summary = "轻松回应"
        else:
            other_summary = "提出观点"

    # 提炼父皇观点
    self_summary = ""
    if self_points:
        key_text = self_points[0].lower()
        if "好" in key_text or "走" in key_text or "可以" in key_text:
            self_summary = "表示同意"
        elif "想吃" in key_text or "想吃啥" in key_text:
            self_summary = "表达需求"
        else:
            self_summary = "提出想法"

    return topic, other_summary, self_summary


def generate_message_summary(text: str) -> str:
    """将消息提炼为一句话概括，不是引用原文。"""
    text = normalize_text(text)
    if not text:
        return "（无内容）"

    # 问句 -> 询问/求助
    if "？" in text or "?" in text or "怎么" in text or "如何" in text or "有没有" in text:
        if len(text) <= 30:
            return f"询问：{text}"
        return "询问具体问题"

    # 确认/回复
    confirm_keywords = ("好的", "收到", "行", "可以", "没问题", "明白", "确定", "是的")
    for kw in confirm_keywords:
        if kw in text:
            return "确认/同意"

    # 安排/请客
    arrange_keywords = ("我请", "请你", "我安排", "我打车", "我买", "我来")
    for kw in arrange_keywords:
        if kw in text:
            if "吃饭" in text:
                return "主动请客"
            if "打车" in text:
                return "安排出行"
            return "主动安排"

    # 建议
    if "建议" in text or "最好" in text or "不如" in text:
        return "提出建议"

    # 分享经验
    if "我" in text and ("之前" in text or "试过" in text or "用的" in text):
        return "分享经验"

    # 简短回复
    if len(text) <= 10:
        return text

    # 一般情况：截断
    if len(text) > 35:
        return text[:35] + "…"
    return text


def extract_conversation_rounds(messages: Sequence[Dict]) -> List[Dict]:
    """识别对话轮次，提取完整的问答对。"""
    if not messages:
        return []

    rounds = []
    current_round: Dict = {"initiator": None, "messages": []}
    last_sender: Optional[str] = None

    for msg in messages:
        # 兼容两种格式：原始格式(name,text) 或 处理后格式(sender, content)
        sender = msg.get("name") or msg.get("sender", "") or "未知"
        text = msg.get("text") or msg.get("content", "") or ""
        time_str = msg.get("time", "")

        # 新一轮：发送者变化
        if sender != last_sender and last_sender is not None:
            if current_round["messages"]:
                # 当前轮次的 initiator 应该是第一个发送者
                current_round["initiator"] = current_round["messages"][0]["sender"]
                rounds.append(current_round)
            current_round = {"initiator": sender, "messages": []}

        current_round["messages"].append({
            "time": time_str,
            "sender": sender,
            "text": text,
            "summary": generate_message_summary(text)
        })
        last_sender = sender

    # 最后一轮
    if current_round["messages"]:
        current_round["initiator"] = current_round["messages"][0]["sender"]
        rounds.append(current_round)

    return rounds


def detect_conversation_context(messages: Sequence[Dict], topic: str) -> str:
    """根据对话内容推断对话背景/来龙去脉。"""
    if not messages:
        return "对话背景不明"

    other_texts = [normalize_text(m.get("text", "")) for m in messages if m.get("name") != SELF_NAME]
    self_texts = [normalize_text(m.get("text", "")) for m in messages if m.get("name") == SELF_NAME]
    combined_other = " ".join(other_texts)
    combined_self = " ".join(self_texts)
    combined = combined_other + combined_self
    msg_count = len(messages)

    # 判断对话发起方
    if other_texts and self_texts:
        first_sender = messages[0].get("name", "")
        if first_sender == SELF_NAME:
            context = "你主动发起"
        else:
            context = "对方主动发起"
    elif other_texts:
        context = "对方发起"
    else:
        context = "你主动发起"

    # 判断对话结果
    result = ""
    if any(w in combined for w in ("好的", "收到", "行", "可以", "没问题", "就这么办")):
        result = "，已达共识"
    elif any(w in combined for w in ("我再想想", "我再看看", "考虑")):
        result = "，待进一步确认"
    elif any(w in combined for w in ("我请", "我安排", "我来")):
        result = "，对方已安排"

    return f"{context}的{topic}讨论{result}" if result else f"{context}的{topic}讨论"


def detect_role_and_insight(messages: Sequence[Dict], topic: str) -> str:
    """分析对方角色，给出犀利洞察：方面 + 建议类型 + 具体观点。"""
    other_texts = [normalize_text(m.get("text", "")) for m in messages if m.get("name") != SELF_NAME]
    self_texts = [normalize_text(m.get("text", "")) for m in messages if m.get("name") == SELF_NAME]
    combined = " ".join(other_texts)
    count = len(messages)

    # 消息数量判断
    msg_count_note = ""
    if count >= 10:
        msg_count_note = "深度沟通"
    elif count >= 5:
        msg_count_note = "充分交流"
    elif count >= 2:
        msg_count_note = "简短交流"

    # 经验分享型：分享自己的做法/经历
    experience_keywords = ("我直接", "我找", "我通过", "我用的", "我之前", "我master", "我同学", "我试过", "我发现")
    if any(w in combined for w in experience_keywords):
        for text in other_texts:
            if any(kw in text for kw in experience_keywords):
                if "openai" in text.lower():
                    return f"对方有实战经验，分享'直接接OpenAI模型'的做法"
                if "gemini" in text.lower():
                    return f"对方有实战经验，分享'用gemini账号'的经验"
                if "claude" in text.lower():
                    return f"对方有实战经验，分享'通过北美同学'的渠道"
                return f"对方有实战经验，分享个人做法"
        return f"对方有实战经验"

    # 判断型：给出明确结论
    if any(w in combined for w in ("确定", "不行", "就这么办", "必须", "本质", "关键", "结论")):
        return f"对方直接给出明确判断，态度果断"

    # 保护型：关心风险
    risk_keywords = ("注意", "小心", "风险", "安全", "稳妥", "避免", "别", "隐患", "防止")
    if any(w in combined for w in risk_keywords):
        for text in other_texts:
            if any(kw in text.lower() for kw in risk_keywords):
                return f"对方关心风险，提出保护性建议"
        return f"对方关心风险，注重稳妥"

    # 建设型：提供建议
    suggestion_keywords = ("建议", "最好", "不如", "要不要", "方案", "思路", "可以", "可以试试")
    if any(w in combined for w in suggestion_keywords):
        for text in other_texts:
            if any(kw in text for kw in suggestion_keywords):
                if len(text) < 30:
                    return f"对方提出建设性建议：{text}"
                return f"对方提出建设性建议"
        return f"对方提供建议"

    # 主动型：主动安排/请客
    arrange_keywords = ("我请", "请你", "我安排", "我买", "我打车", "我请客", "我请吃饭", "我来")
    if any(w in combined for w in arrange_keywords):
        for text in other_texts:
            if any(kw in text for kw in arrange_keywords):
                if "吃饭" in text or "请客" in text:
                    return f"对方主动请客，展现积极态度"
                if "打车" in text:
                    return f"对方主动安排出行"
                if "买" in text:
                    return f"对方主动付出"
        return f"对方主动安排"

    # 激励型：鼓励认可
    if any(w in combined for w in ("好", "棒", "加油", "支持", "没问题", "放心", "相信", "不错")):
        return f"对方给予鼓励，态度积极"

    # 询问型：提问或寻求意见
    if any(w in combined for w in ("?", "？", "怎么", "如何", "你觉得", "你看", "你认为", "怎么办")):
        return f"对方主动询问，寻求你的看法"

    # 闲聊型
    return f"对方与你进行日常{msg_count_note}"


def detect_communication_style(messages: Sequence[Dict]) -> str:
    """分析对方的沟通风格：判断型/保护型/激励型/建设型。"""
    other_texts = [normalize_text(m.get("text", "")) for m in messages if m.get("name") != SELF_NAME]
    combined = " ".join(other_texts)

    styles = []

    # 判断型：包含明确结论、决策
    if any(w in combined for w in ("确定", "不行", "可以", "就这么办", "必须", "不能", "应该", "本质是", "关键是")):
        styles.append("判断型")

    # 保护型：关心风险、安全
    if any(w in combined for w in ("注意", "小心", "风险", "安全", "稳妥", "避免", "别", "防止", "隐患")):
        styles.append("保护型")

    # 激励型：鼓励、认可
    if any(w in combined for w in ("好", "棒", "不错", "可以", "加油", "支持", "没问题", "放心", "相信")):
        styles.append("激励型")

    # 建设型：提供建议、方案
    if any(w in combined for w in ("建议", "可以", "试试", "方案", "思路", "考虑", "看看", "要不要")):
        styles.append("建设型")

    return " / ".join(styles) if styles else "日常沟通"


def build_person_insight(name: str, topic: str, messages: Sequence[Dict]) -> str:
    """生成犀利的一句话洞察：直接说清对方的角色。"""
    # 获取洞察
    role_insight = detect_role_and_insight(messages, topic)
    return role_insight



def build_group_insight(name: str, topic: str, count: int) -> str:
    if count >= 30:
        tone = "持续高活跃"
    elif count >= 15:
        tone = "稳定活跃"
    else:
        tone = "阶段性活跃"
    return f"{name}围绕「{topic}」{tone}，可视为当天重要的多人协同场域。"



def extract_todos(conversations: Sequence[Dict]) -> List[Dict]:
    todos: List[Dict] = []
    seen = set()

    for conversation in conversations:
        for message in conversation.get("messages", []):
            text = normalize_text(message.get("text", ""))
            if not text:
                continue
            lowered = text.lower()
            if not any(keyword in lowered for keyword in TODO_KEYWORDS):
                continue

            task = shorten(text, 28)
            if task in seen:
                continue
            seen.add(task)

            timestamp = message_time(message)
            todos.append(
                {
                    "task": task,
                    "source": conversation.get("name", "未知来源"),
                    "time": timestamp.strftime("%H:%M"),
                    "note": detect_topic([message], fallback="待跟进"),
                    "priority": 2 if any(k in lowered for k in ("请", "需要", "麻烦", "跟进", "处理")) else 1,
                }
            )

    todos.sort(key=lambda item: (-item["priority"], item["time"], item["source"]))
    return todos[:MAX_TODO_ROWS]



def analyze_conversations(raw_conversations: Sequence[Dict]) -> Dict:
    personal_chats: List[Dict] = []
    group_chats: List[Dict] = []
    system_notices: List[Dict] = []
    period_stats = {period_name: [] for period_name, *_ in PERIODS}
    period_counts = Counter()
    total_messages = 0

    for conversation in raw_conversations:
        conversation_type = conversation.get("type", "chat")
        name = conversation.get("name", "未命名会话")
        messages = conversation.get("messages", [])
        if not messages:
            continue

        total_messages += len(messages)
        topic, other_view, self_view = extract_discussion_summary(messages)
        # 主要沟通内容：精炼总结
        if other_view and self_view:
            content_summary = f"讨论{topic}，对方{other_view}，你{self_view}"
        elif other_view:
            content_summary = f"讨论{topic}，对方{other_view}"
        elif self_view:
            content_summary = f"讨论{topic}，你{self_view}"
        else:
            content_summary = f"就{topic}进行讨论"

        snippets = collect_snippets(messages, limit=6, prefer_other_side=True)
        summary = "；".join(snippets) if snippets else "暂无关键内容"
        conversation_record = {
            "name": name,
            "message_count": len(messages),
            "topic": topic,
            "content": content_summary,
            "other_view": other_view,
            "self_view": self_view,
            "style": detect_communication_style(messages),
            "messages": [
                {
                    "time": message_time(message).strftime("%H:%M"),
                    "sender": message.get("name", ""),
                    "content": shorten(message.get("text", ""), 48),
                }
                for message in messages  # 保留所有消息，不限制数量
            ],
        }

        is_system = is_system_name(name)
        if is_system:
            system_notices.append(
                {
                    "name": name,
                    "message_count": len(messages),
                    "summary": summary,
                    "topic": topic,
                }
            )

        if conversation_type == "chat" and not is_system:
            conversation_record["insight"] = build_person_insight(name, topic, messages)
            conversation_record["style"] = detect_communication_style(messages)
            personal_chats.append(conversation_record)
        else:
            at_me_messages = [m for m in messages if f"@{SELF_NAME}" in normalize_text(m.get("text", "")) or SELF_NAME in normalize_text(m.get("text", ""))]
            conversation_record["at_me_count"] = len(at_me_messages)
            conversation_record["summary"] = summary
            conversation_record["at_me_summary"] = "；".join(collect_snippets(at_me_messages, limit=2)) if at_me_messages else "-"
            conversation_record["key_insight"] = build_group_insight(name, topic, len(messages))
            group_chats.append(conversation_record)

        period_bucket: Dict[str, List[Dict]] = {period_name: [] for period_name, *_ in PERIODS}
        for message in messages:
            dt = message_time(message)
            period_name, _, _ = select_period(dt.hour)
            period_bucket[period_name].append(message)
            period_counts[period_name] += 1

        display_type = "系统" if is_system else ("个人" if conversation_type == "chat" else "群")
        for period_name, bucket_messages in period_bucket.items():
            if not bucket_messages:
                continue
            period_stats[period_name].append(
                {
                    "name": name,
                    "type": display_type,
                    "message_count": len(bucket_messages),
                    "summary": "；".join(collect_snippets(bucket_messages, limit=2, prefer_other_side=(display_type == "个人"))),
                }
            )

    personal_chats.sort(key=lambda item: item["message_count"], reverse=True)
    group_chats.sort(key=lambda item: item["message_count"], reverse=True)
    system_notices.sort(key=lambda item: item["message_count"], reverse=True)
    for period_name in period_stats:
        period_stats[period_name].sort(key=lambda item: item["message_count"], reverse=True)

    todos = extract_todos(raw_conversations)
    return {
        "personal_chats": personal_chats,
        "group_chats": group_chats,
        "system_notices": system_notices,
        "period_stats": period_stats,
        "period_counts": period_counts,
        "todo_items": todos,
        "total_messages": total_messages,
    }



def render_period_section(period_name: str, emoji: str, label: str, rows: Sequence[Dict]) -> str:
    title = f"### {emoji} {period_name}时段（{label}）\n\n"
    if not rows:
        return title + "> （暂无数据）\n\n"

    section = title
    section += "| 沟通对象 | 类型 | 消息数 | 主要沟通方向和内容 |\n"
    section += "|:---------|:-----|-------:|:------------------|\n"
    for row in rows[:MAX_PERIOD_ROWS]:
        section += f"| **{row['name']}** | {row['type']} | {row['message_count']} | {shorten(row['summary'] or '暂无关键内容', 34)} |\n"

    top_row = rows[0]
    section += f"\n> 📝 **时段总结**: {period_name}以 **{top_row['name']}** 为最活跃沟通对象，重点围绕「{shorten(top_row['summary'] or '沟通推进', 22)}」。\n\n"
    return section



def render_person_section(personal_chats: Sequence[Dict]) -> str:
    """渲染单人沟通分析，完整展示所有沟通记录。"""
    section = "## 🗣️ 三、单人沟通分析\n\n"
    if not personal_chats:
        return section + "> 暂无单人沟通数据。\n\n"

    for index, chat in enumerate(personal_chats, start=1):
        stars = "⭐" * max(1, min(5, 6 - min(index, 5)))
        topic = chat.get("topic", "日常沟通")
        content = chat.get("content", "暂无关键内容")
        insight = chat.get("insight", "暂无洞察")

        # 获取对话消息
        messages = chat.get("messages", [])
        context = detect_conversation_context(messages, topic)

        section += f"### {stars} {chat['name']}（{chat['message_count']}条）\n\n"
        section += f"- **主题**: {topic}\n"
        section += f"- **对话背景**: {context}\n"
        section += f"- **沟通要点**: {content}\n"
        section += f"- **角色洞察**: {insight}\n\n"

        # 完整沟通内容表格：时间 | 说话人 | 具体内容
        if messages:
            section += "| 时间 | 说话人 | 具体内容 |\n"
            section += "|:-----|:-------|:---------|\n"
            for msg in messages:
                # 修复：使用正确的字段名 (analyze_conversations中存储为time/sender/content)
                msg_time = msg.get("time", "")
                sender = msg.get("sender", "未知")
                text = normalize_text(msg.get("content", ""))
                # 处理表格中的竖线符号，防止破坏表格结构
                text = text.replace("|", "｜")
                section += f"| {msg_time} | {sender} | {text} |\n"
            section += "\n"

    # 移除长度控制提示
    section += f"> 💡 共{len(personal_chats)}位单人沟通对象\n\n"
    return section



def render_group_section(group_chats: Sequence[Dict]) -> str:
    section = "## 💬 四、群聊汇总\n\n"
    section += "| 群名 | 消息数 | @我次数 | 主题 | 群聊摘要 |\n"
    section += "|:-----|-------:|--------:|:-----|:---------|\n"

    if not group_chats:
        section += "| - | 0 | 0 | 暂无数据 | 暂无数据 |\n\n"
        return section

    for chat in group_chats[:MAX_GROUP_ROWS]:
        section += (
            f"| **{chat['name']}** | {chat['message_count']} | {chat['at_me_count']} | {chat['topic']} | "
            f"{shorten(chat['summary'], 34)} |\n"
        )
    section += "\n"
    return section



def render_overall_insights(analysis: Dict) -> str:
    personal_chats = analysis["personal_chats"]
    group_chats = analysis["group_chats"]
    period_counts = analysis["period_counts"]
    todo_items = analysis["todo_items"]

    top_person = personal_chats[0]["name"] if personal_chats else "暂无"
    top_group = group_chats[0]["name"] if group_chats else "暂无"
    busiest_period = period_counts.most_common(1)[0][0] if period_counts else "上午"

    section = "## 💡 五、整体洞察\n\n"
    section += f"- **沟通重心**: 单人沟通以 **{top_person}** 最活跃，说明关键推进更多通过点对点快速对齐完成。\n"
    section += f"- **协同场域**: 群聊中 **{top_group}** 最活跃，代表当天最重要的多人协作上下文。\n"
    section += f"- **时间投入**: **{busiest_period}** 是消息峰值时段，建议把高优事项集中在该时段处理。\n"
    section += f"- **待办压力**: 共识别出 **{len(todo_items)}** 条潜在待办，可优先梳理需要跟进或确认的事项。\n\n"
    return section



def render_todo_section(todo_items: Sequence[Dict]) -> str:
    section = "## ✅ 六、todo清单\n\n"
    section += "| 待办事项 | 来源 | 时间 | 备注 |\n"
    section += "|:---------|:-----|:-----|:-----|\n"

    if not todo_items:
        section += "| 暂未识别到明确待办 | - | - | 可结合单人沟通人工补充 |\n\n"
        return section

    for todo in todo_items:
        section += f"| {todo['task']} | **{todo['source']}** | {todo['time']} | {todo['note']} |\n"
    section += "\n"
    return section



def generate_report(target_date: datetime, analysis: Dict, report_path: Path) -> str:
    display_date = format_display_date(target_date)
    period_stats = analysis["period_stats"]

    report = f"# 📊 {display_date}大象沟通汇总分析\n\n---\n\n"
    report += "## 📈 一、今日数据概览\n\n"
    report += "| 指标 | 数值 |\n"
    report += "|:-----|-----:|\n"
    report += f"| 个人对话 | **{len(analysis['personal_chats'])} 人** |\n"
    report += f"| 活跃群聊 | **{len(analysis['group_chats'])}** |\n"
    report += f"| 系统通知 | **{len(analysis['system_notices'])}** |\n"
    report += f"| 消息总数 | **{analysis['total_messages']} 条** |\n\n---\n\n"

    report += "## ⏰ 二、时间精力分布\n\n"
    for period_name, emoji, label, _ in PERIODS:
        report += render_period_section(period_name, emoji, label, period_stats[period_name])
        report += "---\n\n"

    report += render_person_section(analysis["personal_chats"])
    report += "---\n\n"
    report += render_group_section(analysis["group_chats"])
    report += "---\n\n"
    report += render_overall_insights(analysis)
    report += "---\n\n"
    report += render_todo_section(analysis["todo_items"])
    report += f"*📁 文件存储位置: `{report_path}`*\n\n"
    report += f"*⏰ 报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n"
    return report



def resolve_report_path(date_key: str, force: bool) -> Path:
    base_pattern = f"daxiang_{date_key}_v"
    versions = []
    for path in REPORT_DIR.glob(f"{base_pattern}*.md"):
        match = re.search(r"_v(\d+)\.md$", path.name)
        if match:
            versions.append(int(match.group(1)))

    if force and versions:
        return REPORT_DIR / f"daxiang_{date_key}_v{max(versions)}.md"

    next_version = (max(versions) + 1) if versions else 1
    return REPORT_DIR / f"daxiang_{date_key}_v{next_version}.md"



def main() -> int:
    args = parse_args()

    try:
        target_date = parse_date(args.date)
    except ValueError as error:
        print(f"❌ {error}")
        return 1

    date_key = target_date.strftime("%Y%m%d")
    report_path = resolve_report_path(date_key, args.force)

    print("=== 大象沟通日报生成任务开始 ===")
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"目标日期: {date_key}")

    try:
        raw_conversations = load_message_file(date_key)
    except FileNotFoundError as error:
        print(f"❌ {error}")
        return 1

    analysis = analyze_conversations(raw_conversations)
    report_content = generate_report(target_date, analysis, report_path)

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as file:
        file.write(report_content)

    print(f"报告已生成: {report_path}")
    print("=== 大象沟通日报生成任务完成 ===")
    return 0



if __name__ == "__main__":
    sys.exit(main())
