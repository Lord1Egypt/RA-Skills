#!/usr/bin/env python3
"""
上下文摘要生成脚本
将长上下文压缩为精简的关键信息摘要
"""

import json
import re
import sys
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field


@dataclass
class SummaryConfig:
    """摘要配置
    
    Attributes:
        style: 摘要风格
            - structured: 结构化 (markdown 格式)
            - concise: 简洁 (一行式)
            - bullet: 列表式
            - executive: 执行摘要式
        max_length: 最大长度 (字符数)
        preserve_recent: 保留最近N条消息
        compress_ratio: 压缩比
    """
    style: str = "structured"  # structured | concise | bullet | executive
    max_length: int = 2000      # 最大长度
    preserve_recent: int = 5    # 保留最近N条消息
    compress_ratio: float = 0.3 # 压缩比


def extract_key_info(messages: List[Dict]) -> Dict[str, Any]:
    """提取关键信息 - 改进版，带噪音过滤"""
    if not messages:
        return {"main_topic": "无", "key_points": [], "decisions": [], "entities": []}
    
    # 收集所有文本
    all_text = "\n".join(msg.get("content", "") for msg in messages if msg.get("content"))
    
    # 1. 提取主题 - 从用户第一条消息中提取，更精确的模式
    main_topic = ""
    for msg in messages:
        if msg.get("role") == "user":
            content = msg.get("content", "")
            # 尝试提取核心任务 - 按优先级排序
            task_patterns = [
                # 精确匹配：帮我开发/创建/实现 X
                (r'(?:帮我|请帮我|帮我|我想|需要)[: ]*(?:开发|创建|实现|做一个|构建|制作)[^\n，。]{5,40}', 0),
                # 精确匹配：请/帮/需要 X
                (r'(?:请|帮|需要)[: ]*[^\n，。]{5,40}(?:网站|系统|应用|项目|功能|博客|APP|平台)', 1),
                # 通用任务描述
                (r'[^\n，。]{10,50}(?:吧|呀|哈|哦)', 2),
            ]
            for pattern, priority in task_patterns:
                match = re.search(pattern, content)
                if match:
                    main_topic = match.group(0).strip()
                    # 清理常见前缀
                    main_topic = re.sub(r'^(用户[:：]|助手[:：]|user[:：])', '', main_topic).strip()
                    break
            if not main_topic and len(content) > 5:
                main_topic = content[:100]
                # 清理
                main_topic = re.sub(r'^(用户[:：]|助手[:：])', '', main_topic).strip()
            break
    
    # 2. 提取关键点 - 更有针对性的模式，带去重和噪音过滤
    key_points = []
    seen_points = set()
    
    # 需求类关键点 - 更严格的匹配，避免编号列表
    need_patterns = [
        (r'需要([^\n，。0-9)）]{4,25})(?![0-9])', 'need'),  # 排除数字编号
        (r'要有([^\n，。0-9]{4,20})', 'need'),
        (r'需要实现([^\n，。]{4,20})', 'need'),
    ]
    
    for pattern, ptype in need_patterns:
        matches = re.findall(pattern, all_text)
        for match in matches:
            # 过滤噪音：太短或包含数字编号
            if match and 3 < len(match) < 30:
                normalized = match.strip()
                # 标准化用于去重
                norm_key = re.sub(r'[\s\d]', '', normalized.lower())
                if norm_key and norm_key not in seen_points:
                    # 检查是否与已有的关键点重复
                    is_dup = False
                    for existing in seen_points:
                        if norm_key in existing or existing in norm_key:
                            is_dup = True
                            break
                    if not is_dup:
                        seen_points.add(norm_key)
                        key_points.append(normalized)
    
    # 功能类关键点 - 明确的实体
    func_patterns = [
        r'(用户登录|文章发布|评论功能|标签系统|搜索功能|后台管理|数据库|API|前端|后端|Docker|用户认证|文章CRUD)',
    ]
    for pattern in func_patterns:
        matches = re.findall(pattern, all_text)
        for match in matches:
            if match:
                norm_key = match.lower()
                # 检查是否与现有的key_points重复（包含关系）
                is_dup = False
                for existing in key_points:
                    existing_norm = re.sub(r'[\s]', '', existing.lower())
                    if norm_key in existing_norm or existing_norm in norm_key:
                        is_dup = True
                        break
                if not is_dup:
                    seen_points.add(norm_key)
                    key_points.append(match)
    
    key_points = key_points[:8]
    
    # 3. 提取决策 - 改进去重
    decision_keywords = ["决定", "选择", "采用", "使用", "确定", "用", "decided", "choose", "use", "adopt"]
    decisions = []
    seen_decisions = set()
    
    for msg in messages:
        content = msg.get("content", "")
        for kw in decision_keywords:
            if kw in content:
                # 找到包含决策关键词的完整句子
                sentences = re.split(r'[。.!?]', content)
                for sent in sentences:
                    # 过滤：太短或太长
                    if kw in sent and 10 < len(sent) < 80:
                        # 清理开头
                        cleaned = re.sub(r'^(好的|明白|好的，)', '', sent).strip()
                        if len(cleaned) > 5:
                            normalized = re.sub(r'[\s，。]', '', cleaned.lower())
                            # 去重
                            is_dup = False
                            for existing in seen_decisions:
                                if normalized in existing or existing in normalized:
                                    is_dup = True
                                    break
                            if not is_dup:
                                seen_decisions.add(normalized)
                                decisions.append(cleaned)
                                break
    
    decisions = decisions[:5]
    
    # 4. 提取最近上下文
    last_messages = messages[-3:] if len(messages) >= 3 else messages
    last_content = " ".join(msg.get("content", "") for msg in last_messages if msg.get("content"))
    
    # 5. 提取实体
    entities = re.findall(r'[A-Z][a-zA-Z]{2,}(?:\s+[A-Z][a-zA-Z]+)*', all_text)
    entities = list(dict.fromkeys(entities))[:10]
    
    return {
        "main_topic": main_topic or "无",
        "key_points": key_points,
        "decisions": decisions,
        "entities": entities,
        "recent_context": last_content[:300] if last_content else ""
    }


def extract_todos(messages: List[Dict]) -> List[Dict[str, str]]:
    """提取待办事项"""
    todos = []
    
    todo_patterns = [
        r'[（\[].*?待[办做].*?[）\]]',
        r'[（\[].*?TODO.*?[）\]]',
        r'[（\[].*?todo.*?[）\]]',
        r'[●○]\s*\[?\s*\]?\s*',
        r'\d+[、.]\s*',
    ]
    
    all_text = "\n".join(msg.get("content", "") for msg in messages if msg.get("content"))
    
    for pattern in todo_patterns:
        matches = re.findall(pattern, all_text)
        for match in matches:
            # 判断是否已完成
            completed = "完成" in match or "done" in match.lower() or "✓" in match
            todos.append({
                "content": match.strip(),
                "completed": completed
            })
    
    return todos[:10]  # 最多10个


def compress_messages(messages: List[Dict], config: SummaryConfig) -> List[Dict]:
    """压缩消息列表"""
    if not messages:
        return []
    
    total = len(messages)
    
    # 保留最近的 N 条消息
    recent = messages[-config.preserve_recent:] if len(messages) > config.preserve_recent else messages
    
    # 压缩中间部分
    if total > config.preserve_recent * 2:
        middle_start = config.preserve_recent // 2
        middle_end = total - config.preserve_recent
        middle = messages[middle_start:middle_end]
        
        # 对中间部分进行简单压缩：只保留关键句子
        compressed_middle = []
        for msg in middle:
            content = msg.get("content", "")
            # 提取有意义的句子
            sentences = re.split(r'[。.!?\n]', content)
            key_sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
            if key_sentences:
                compressed_middle.append({
                    "role": msg.get("role", "unknown"),
                    "content": " | ".join(key_sentences[:3])  # 每条消息最多3句
                })
        
        # 合并
        result = list(messages[:config.preserve_recent // 2]) + compressed_middle + recent
    else:
        result = list(messages[:config.preserve_recent]) + recent
    
    return result


def generate_summary(context: Any, style: str = "structured", config: Optional[SummaryConfig] = None) -> Dict[str, Any]:
    """
    生成上下文摘要
    
    Args:
        context: 上下文内容（字符串或消息列表）
        style: 摘要风格 (structured|concise)
        config: 配置对象
    
    Returns:
        包含摘要信息的字典
    """
    if config is None:
        config = SummaryConfig(style=style)
    
    # 处理不同类型的输入
    if isinstance(context, str):
        text = context
        # 将字符串转换为消息格式
        if text.strip():
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            messages = [{"role": "user", "content": line} for line in lines]
        else:
            messages = []
    elif isinstance(context, list):
        messages = context
        text = "\n".join(msg.get("content", "") for msg in messages if msg.get("content"))
    else:
        text = str(context)
        messages = []
    
    # 1. 提取关键信息
    key_info = extract_key_info(messages)
    
    # 2. 提取待办事项
    todos = extract_todos(messages)
    
    # 3. 压缩消息
    compressed = compress_messages(messages, config)
    
    # 4. 生成摘要
    if style == "structured":
        # 结构化摘要 (Markdown)
        summary_parts = []
        
        # 核心任务
        if key_info["main_topic"]:
            summary_parts.append(f"### 核心任务\n{key_info['main_topic']}")
        
        # 关键信息
        if key_info["key_points"]:
            points = "\n".join(f"- {p}" for p in key_info["key_points"][:5])
            summary_parts.append(f"### 关键信息\n{points}")
        
        # 待办事项
        if todos:
            todo_items = "\n".join(
                f"- [{'x' if t['completed'] else ' '}] {t['content']}"
                for t in todos[:7]
            )
            summary_parts.append(f"### 待办事项\n{todo_items}")
        
        # 历史决策
        if key_info["decisions"]:
            decisions = "\n".join(f"- {d}" for d in key_info["decisions"])
            summary_parts.append(f"### 历史决策\n{decisions}")
        
        summary_text = "\n\n".join(summary_parts)
    
    elif style == "concise":
        # 简洁摘要 (单行)
        parts = []
        if key_info["main_topic"]:
            parts.append(f"主题: {key_info['main_topic']}")
        if key_info["decisions"]:
            parts.append(f"决策: {'; '.join(key_info['decisions'][:3])}")
        if todos:
            pending = [t for t in todos if not t["completed"]]
            if pending:
                parts.append(f"待办: {len(pending)}项")
        summary_text = " | ".join(parts)
    
    elif style == "bullet":
        # 列表式摘要
        bullet_parts = []
        
        if key_info["main_topic"]:
            bullet_parts.append(f"▸ 目标: {key_info['main_topic']}")
        
        for point in key_info["key_points"][:5]:
            bullet_parts.append(f"▸ {point}")
        
        for decision in key_info["decisions"][:3]:
            bullet_parts.append(f"✓ {decision}")
        
        pending_todos = [t for t in todos if not t["completed"]]
        for todo in pending_todos[:5]:
            bullet_parts.append(f"○ {todo['content']}")
        
        summary_text = "\n".join(bullet_parts)
    
    elif style == "executive":
        # 执行摘要 (适合向用户展示)
        lines = []
        
        # 概述
        lines.append("## 执行摘要\n")
        
        if key_info["main_topic"]:
            lines.append(f"**当前任务**: {key_info['main_topic']}")
        
        # 进度
        total_todos = len(todos)
        completed_todos = len([t for t in todos if t["completed"]])
        if total_todos > 0:
            progress = int(completed_todos / total_todos * 100)
            lines.append(f"**进度**: {completed_todos}/{total_todos} ({progress}%)")
        
        # 关键决策
        if key_info["decisions"]:
            lines.append("\n**关键决策**:")
            for d in key_info["decisions"][:3]:
                lines.append(f"- {d}")
        
        # 下一步
        if pending_todos := [t for t in todos if not t["completed"]]:
            lines.append("\n**下一步**:")
            for todo in pending_todos[:3]:
                lines.append(f"- {todo['content']}")
        
        summary_text = "\n".join(lines)
    
    else:
        # 默认结构化
        summary_text = key_info["main_topic"] or "无摘要"
    
    return {
        "summary": summary_text,
        "style": style,
        "key_info": key_info,
        "todos": todos,
        "compressed_messages": compressed,
        "stats": {
            "original_count": len(messages),
            "compressed_count": len(compressed),
            "compression_ratio": round(len(compressed) / max(1, len(messages)), 2)
        }
    }


def format_summary_markdown(summary: Dict[str, Any]) -> str:
    """格式化摘要为 Markdown"""
    output = "## 上下文摘要\n"
    
    output += summary["summary"]
    
    output += f"\n\n---\n📊 统计: 原始消息 {summary['stats']['original_count']} 条 → 压缩后 {summary['stats']['compressed_count']} 条 (压缩比 {summary['stats']['compression_ratio']})"
    
    return output


def main():
    """测试用主函数"""
    # 模拟测试数据
    test_messages = [
        {"role": "user", "content": "请帮我开发一个 Python 网站项目"},
        {"role": "assistant", "content": "好的，你想开发什么类型的网站？需要什么功能？"},
        {"role": "user", "content": "一个博客网站，需要有文章发布、评论、用户登录功能"},
        {"role": "assistant", "content": "明白了。我来帮你设计数据库结构和API。"},
        {"role": "user", "content": "好的，使用 Flask 框架"},
        {"role": "assistant", "content": "Flask 很好，很适合快速开发。我来创建项目结构。"},
        {"role": "user", "content": "记得加上 Docker 支持"},
        {"role": "assistant", "content": "好的，我会添加 Dockerfile 和 docker-compose.yml"},
        {"role": "user", "content": "（1）创建数据库模型 （2）实现用户认证 （3）实现文章CRUD （4）添加评论功能"},
        {"role": "assistant", "content": "好的，我们按顺序来实现。先创建数据库模型。"},
    ] * 3  # 重复模拟长上下文
    
    # 生成摘要
    summary = generate_summary(test_messages, style="structured")
    
    print(format_summary_markdown(summary))
    
    # JSON 输出
    if "--json" in sys.argv:
        print("\n--- JSON ---")
        print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
