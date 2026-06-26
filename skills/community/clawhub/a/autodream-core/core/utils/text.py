"""
文本处理工具

标准化、规范化、生成稳定 ID。
"""

import hashlib
import re


def normalize(text: str) -> str:
    """
    标准化文本：去除多余空白
    
    示例:
    >>> normalize("  多个   空格   ")
    '多个 空格'
    """
    # 去除首尾空白
    text = text.strip()
    # 多个空白字符合并为一个
    text = re.sub(r'\s+', ' ', text)
    # 统一换行符
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    return text


def canonical(text: str) -> str:
    """
    规范化文本：用于去重比较
    
    - 转小写
    - 移除标点符号（保留字母数字和空白）
    - 标准化空白
    """
    s = normalize(text).lower()
    # 移除非字母数字字符（保留空白和少量符号）
    s = re.sub(r'[^a-z0-9\s:_-]', ' ', s)
    # 多个空白合并
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def stable_id(text: str) -> str:
    """
    生成稳定的条目 ID
    
    相同文本总是生成相同 ID。
    
    格式：ad_ + 16 字符 hash
    
    示例:
    >>> stable_id("测试文本")
    'ad_xxx...'
    """
    return "ad_" + hashlib.sha256(canonical(text).encode("utf-8")).hexdigest()[:16]


def detect_contradiction(entry1: dict, entry2: dict) -> bool:
    """
    检测两个条目是否矛盾
    
    矛盾场景:
    - 同一主题但决策相反（如"使用 Redis" vs "弃用 Redis"）
    - 同一功能但状态不同（如"启用缓存" vs "禁用缓存"）
    
    参数:
        entry1: 条目 1 {"text": "..."}
        entry2: 条目 2 {"text": "..."}
        
    返回:
        是否矛盾
    """
    # 使用原始文本（保留中文）进行检测
    text1 = entry1.get("text", "").lower()
    text2 = entry2.get("text", "").lower()
    
    # 对立词检测（中英文）
    opposites = [
        ("使用", "弃用"),
        ("启用", "禁用"),
        ("开始", "停止"),
        ("添加", "删除"),
        ("创建", "销毁"),
        ("prefer", "avoid"),
        ("use", "remove"),
        ("open", "close"),
        ("enable", "disable"),
    ]
    
    for word1, word2 in opposites:
        if word1 in text1 and word2 in text2:
            return True
        if word2 in text1 and word1 in text2:
            return True
    
    return False


def extract_entries_from_text(content: str) -> list:
    """
    从文本中提取条目列表
    
    支持格式:
    - 列表项：- 内容 / * 内容
    - 跳过代码块
    - 跳过标题和空行
    
    参数:
        content: 文件内容
        
    返回:
        [{"text": "...", "line": 1, "metadata": {}}, ...]
    """
    entries = []
    in_code = False
    
    for idx, raw in enumerate(content.splitlines(), start=1):
        line = raw.strip()
        
        # 跳过代码块
        if line.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        
        # 跳过标题和空行
        if not line or line.startswith("#"):
            continue
        
        # 提取列表项
        text = None
        if line.startswith(("- ", "* ")):
            text = line[2:].strip()
        elif line.startswith("-"):
            # 处理无空格的列表项
            text = line[1:].strip()
        
        if text:
            entries.append({
                "text": text,
                "line": idx,
                "metadata": {},
            })
    
    return entries
