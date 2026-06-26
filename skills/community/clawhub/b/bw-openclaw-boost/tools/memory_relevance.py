#!/usr/bin/env python3
"""
相关性记忆检索系统 v2
参考 Claude Code 的 memdir findRelevantMemories 设计

功能：
1. scan_memory_files() — 扫描所有记忆文件，构建 manifest
2. score_memories() — 基于关键词匹配计算相关性分数
3. get_relevant_memories() — 返回 top N 最相关的记忆

集成方式：
- 可被 agent 会话调用，注入相关记忆到上下文
- 支持 freshness warning（旧记忆标注过时警告）
"""

import os
import re
import json
from pathlib import Path

# 技能本地目录
SKILL_ROOT = Path(__file__).parent.parent
from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field

MEMORY_ROOT = SKILL_ROOT / "memory"
MAX_RELEVANT = 5


@dataclass
class MemoryHeader:
    """记忆文件的头部信息"""
    name: str
    description: str
    type: str  # user / feedback / project / reference / log
    mtime: str
    path: str
    age_days: int
    content_preview: str = ""  # 前100字符预览


def scan_memory_files() -> List[MemoryHeader]:
    """扫描所有记忆文件，构建 manifest"""
    memories = []
    
    for root, dirs, files in os.walk(MEMORY_ROOT):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['logs']]
        
        for f in files:
            if not f.endswith('.md') or f == 'MEMORY.md':
                continue
            
            path = Path(root) / f
            try:
                full_content = path.read_text(encoding='utf-8')
                lines = full_content.split('\n')[:30]
                fm = _parse_frontmatter(lines)
                
                age_days = _calc_age_days(fm.get('mtime', ''))
                
                # 提取内容预览（frontmatter 之后的前100字符）
                body_start = full_content.find('---', 3)
                if body_start > 0:
                    preview = full_content[body_start+3:body_start+103].strip()
                else:
                    preview = '\n'.join(lines[3:10])[:100]
                
                memories.append(MemoryHeader(
                    name=fm.get('name', f.replace('.md', '')),
                    description=fm.get('description', ''),
                    type=fm.get('type', 'unknown'),
                    mtime=fm.get('mtime', ''),
                    path=str(path.relative_to(MEMORY_ROOT)),
                    age_days=age_days,
                    content_preview=preview
                ))
            except Exception as e:
                pass
    
    memories.sort(key=lambda x: x.mtime, reverse=True)
    return memories


def _parse_frontmatter(lines: List[str]) -> Dict[str, str]:
    """解析 YAML frontmatter"""
    fm = {}
    in_fm = False
    
    for line in lines:
        line = line.strip()
        if line == '---':
            in_fm = not in_fm if in_fm else True
            continue
        if in_fm and line == '---':
            break
        if ':' in line and in_fm:
            key, val = line.split(':', 1)
            fm[key.strip()] = val.strip()
    
    return fm


def _calc_age_days(mtime_str: str) -> int:
    """计算记忆的年龄（天）"""
    if not mtime_str:
        return 999
    try:
        mtime = datetime.fromisoformat(mtime_str.replace('Z', '+00:00'))
        return max(0, (datetime.now() - mtime).days)
    except:
        return 999


def score_memories(query: str, memories: List[MemoryHeader]) -> List[tuple]:
    """
    基于关键词匹配计算相关性分数
    
    评分维度：
    1. 名称匹配（权重 3x）
    2. 描述匹配（权重 2x）
    3. 类型匹配（权重 1x）
    4. 新鲜度奖励（1天以内 +2分，7天以内 +1分）
    5. 内容预览匹配（权重 1x）
    """
    query_lower = query.lower()
    query_words = set(re.findall(r'\w+', query_lower))
    
    scored = []
    
    for m in memories:
        score = 0
        
        # 名称匹配
        name_lower = m.name.lower()
        name_words = set(re.findall(r'\w+', name_lower))
        name_match = query_words & name_words
        score += len(name_match) * 3
        
        # 描述匹配
        desc_lower = m.description.lower()
        desc_words = set(re.findall(r'\w+', desc_lower))
        desc_match = query_words & desc_words
        score += len(desc_match) * 2
        
        # 内容预览匹配
        preview_lower = m.content_preview.lower()
        preview_words = set(re.findall(r'\w+', preview_lower))
        preview_match = query_words & preview_words
        score += len(preview_match) * 1
        
        # 类型匹配（如果有明确类型词）
        type_keywords = {
            'user': ['用户', '角色', '身份', '我是谁', '我的'],
            'feedback': ['教训', '纠正', '错误', '避免', '不要'],
            'project': ['项目', '进行中', '待处理', '工作'],
            'reference': ['配置', '技术', '工具', '系统', '栈'],
            'log': ['日志', '记录', '今天', '发生']
        }
        for mem_type, keywords in type_keywords.items():
            if m.type == mem_type:
                for kw in keywords:
                    if kw in query_lower:
                        score += 1
        
        # 新鲜度奖励
        if m.age_days <= 1:
            score += 2
        elif m.age_days <= 7:
            score += 1
        elif m.age_days > 30:
            score -= 1  # 惩罚过旧记忆
        
        scored.append((m, score))
    
    # 按分数降序排列
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored


def get_freshness_warning(m: MemoryHeader) -> str:
    """获取新鲜度警告"""
    if m.age_days == 0:
        return ""
    elif m.age_days == 1:
        return "[昨天更新]"
    elif m.age_days <= 7:
        return f"[{m.age_days}天前]"
    elif m.age_days <= 30:
        return f"[{m.age_days}天前，可能过时]"
    else:
        return f"[{m.age_days}天前，已过时]"


def format_manifest(memories: List[MemoryHeader], max_show: int = 20) -> str:
    """格式化 manifest 用于显示"""
    lines = []
    for m in memories[:max_show]:
        age = 'today' if m.age_days == 0 else f'{m.age_days}d'
        lines.append(f"- [{m.type}] {m.name} ({age}): {m.description}")
    if len(memories) > max_show:
        lines.append(f"... 还有 {len(memories) - max_show} 个")
    return '\n'.join(lines)


def get_relevant_memories(query: str, max_results: int = MAX_RELEVANT) -> List[MemoryHeader]:
    """主入口：获取最相关的记忆"""
    memories = scan_memory_files()
    if not memories:
        return []
    
    scored = score_memories(query, memories)
    
    # 返回 top N，且分数 > 0
    result = []
    for m, score in scored:
        if score > 0 or len(result) < 3:  # 至少返回3个
            result.append(m)
        if len(result) >= max_results:
            break
    
    return result


def get_memory_content(m: MemoryHeader) -> str:
    """读取记忆文件的完整内容"""
    path = MEMORY_ROOT / m.path
    try:
        content = path.read_text(encoding='utf-8')
        warning = get_freshness_warning(m)
        if warning:
            return f"{warning}\n\n{content}"
        return content
    except Exception as e:
        return f"Error: {e}"


def format_for_context(query: str) -> str:
    """
    主入口函数：生成可注入到上下文的记忆内容
    
    使用方式：
    在 AGENTS.md 的会话启动时调用，
    将返回的记忆内容注入到上下文中
    """
    memories = get_relevant_memories(query, max_results=5)
    
    if not memories:
        return ""
    
    lines = [
        "",
        "═" * 50,
        "📚 相关记忆（Relevance-based Retrieval）",
        "═" * 50,
        ""
    ]
    
    for m in memories:
        content = get_memory_content(m)
        warning = get_freshness_warning(m)
        
        lines.append(f"### {m.name} [{m.type}]{' ' + warning if warning else ''}")
        lines.append("")
        lines.append(content)
        lines.append("")
        lines.append("---")
        lines.append("")
    
    return '\n'.join(lines)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 memory_relevance.py scan           # 扫描所有记忆")
        print("  python3 memory_relevance.py relevant <查询>  # 查找相关记忆")
        print("  python3 memory_relevance.py inject <查询>   # 生成可注入的上下文")
        sys.exit(1)
    
    cmd = sys.argv[1]
    memories = scan_memory_files()
    
    if cmd == "scan":
        print(f"找到 {len(memories)} 个记忆文件:\n")
        print(format_manifest(memories))
    
    elif cmd == "relevant" and len(sys.argv) >= 3:
        query = sys.argv[2]
        relevant = get_relevant_memories(query)
        print(f"查询: {query}\n")
        print(f"找到 {len(relevant)} 个相关记忆:\n")
        for m in relevant:
            warning = get_freshness_warning(m)
            print(f"【{m.name}】[{m.type}]{' ' + warning if warning else ''}")
            print(f"  {m.description}")
            print(f"  分数: {score_memories(query, [m])[0][1]}")
            print()
    
    elif cmd == "inject" and len(sys.argv) >= 3:
        query = sys.argv[2]
        print(format_for_context(query))
    
    else:
        print("未知命令")
        sys.exit(1)
