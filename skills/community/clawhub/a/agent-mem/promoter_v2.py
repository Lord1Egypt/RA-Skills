#!/usr/bin/env python3
"""
记忆升级引擎 V2 - 增强版
功能：过滤噪音、精准去重、分类强化
只将真正重要的、提炼后的记忆写入 MEMORY.md
"""

import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

HOME = Path.home()
MEMORY_DIR = HOME / '.agent-mem/memory'
MEMORY_PATH = HOME / '.agent-mem/MEMORY.md'
MEMORY_ENGINE_STATE = HOME / '.agent-mem/memory/.memory-engine-state-v2.json'

CATEGORY_NAMES = {
    "person": "👤 人物/关系",
    "work": "💼 工作类",
    "tech": "⚙️ 技术类",
    "preference": "❤️ 偏好类",
    "schedule": "📅 日程类",
    "insight": "💡 洞察类",
    "system_change": "🔧 系统变更",
    "general": "📝 一般",
    "project": "📦 项目类"
}

# 噪音模式 - 这些行绝不进 MEMORY.md
NOISE_PATTERNS = [
    r'^-\s*\[',                           # 任何以 - [ 开头的（对话切片、系统消息）
    r'^\s*```',                           # 代码块
    r'^<\!--',                            # HTML注释
    r'^\*\*\*',                           # 分隔线
    r'^\.\.\.',                           # 省略号
    r'^(嗯|呃|啊|哦|哈|嘿|唉|切|呸)',     # 语气词开头
    r'^[\s]*$',                           # 空行
    r'Candidate:',                        # 梦境候选
    r'Sender \(untrusted',                # 系统元数据
    r'\*\*OpenClaw\*\*.*\*\*无法',         # 错误消息
    r'tool_calls>',                       # XML标签
    r'</invoke>',
    r'<｜｜DSML｜｜',
    r'^---$',
    r'^===',                              # 分隔线
    r'^```',                              # 代码块结束
    r'^ℹ️',                               # 信息消息
    r'^✅ .*运行完成',                      # 引擎运行报告
    r'^完成时间:',                         # 时间戳
    r'^处理文件:',                         # 处理统计
    r'^提取事实:',         
    r'^重要事实:',         
    r'^分类分布:',        
    r'^📁 文件列表:',    
    r'^\[.*\].*:.*\(code:',               # exec结果
    r'^System \(untrusted\)',              # 系统消息
    r'^- \[.*\] 等待',                     # 等待消息
    r'^- \[.*\] 任务',                     # 任务状态
    r'^- \*\*',                           # 粗体列表项（一般是对话）
    r'^✖',                                # 错误符号
    r'^❌',                               # 错误
    r'^⚠️',                               # 警告
    r'^📊.*引擎.*运行',                     # 引擎运行统计
    r'nvoke name=',                       # XML
    r'parseMessageWithAttachments',         # 系统日志
    r'dropped — model does not support',    # 系统日志
]

# 重要关键词（收紧，去掉太泛的）
IMPORTANT_KEYWORDS = [
    'P0', 'P1', 'P2',                     # 优先级
    '创建Agent', '新增Agent',              # Agent变更
    '重要决策', '重大变更',                 # 决策
    '上线', '部署', '发布',                # 新功能
    '收费', '涨价', '优惠', '活动',        # 商业
    '规则', '铁律', '必须', '禁止',         # 规则
    '修复.*bug', '修复.*问题',              # 修复
    '配置.*完毕', '配置.*完成',
    '技能.*配置', 'Skill.*配置',
]

# 过期时间（天）- 超过这个天数的完全不处理
MAX_AGE_DAYS = 14

def load_state():
    if not MEMORY_ENGINE_STATE.exists():
        return None
    with open(MEMORY_ENGINE_STATE, 'r') as f:
        return json.load(f)

def get_backup_path():
    return HOME / f'.agent-mem/MEMORY.md.bak.{datetime.now().strftime("%Y%m%d%H%M%S")}'

def backup_memory():
    if MEMORY_PATH.exists():
        backup = get_backup_path()
        with open(MEMORY_PATH, 'r') as f:
            content = f.read()
        with open(backup, 'w') as f:
            f.write(content)
        print(f"✅ 已备份 → {backup}")

def get_category(text: str) -> str:
    cat_keywords = {
        "tech": ["API", "脚本", "代码", "部署", "配置", "安装", "修复", "优化", "技术", "开发", "模型", "系统"],
        "work": ["任务", "工作", "项目", "完成", "进度", "计划", "执行", "广告", "运营"],
        "person": ["用户", "用户", "关系", "协作", "团队"],
        "schedule": ["日程", "会议", "提醒", "预约", "时间", "安排"],
        "insight": ["发现", "洞察", "分析", "总结", "规律", "教训", "经验"],
        "system_change": ["新增", "修改", "删除", "更新", "变更", "创建", "升级", "安装"],
        "project": ["项目", "Pixel", "Office", "记忆引擎", "Agent"]
    }
    for cat, keywords in cat_keywords.items():
        if any(kw in text for kw in keywords):
            return cat
    return "general"

def is_noise(line: str) -> bool:
    """检查是否是噪音行"""
    line_stripped = line.strip()
    if not line_stripped or len(line_stripped) < 8:
        return True
    
    # 匹配噪音模式
    for pattern in NOISE_PATTERNS:
        if re.search(pattern, line_stripped):
            return True
    
    return False

def is_meaningful_fact(text: str) -> bool:
    """判断是否是有意义的事实"""
    # 必须包含实际信息
    has_info = any([
        '配置' in text,
        '创建' in text,
        '完成' in text and len(text) > 20,
        '修复' in text,
        '更新' in text,
        '新建' in text,
        '部署' in text,
        '上线' in text,
        '规则' in text,
        'API' in text or 'api' in text.lower(),
        'Agent' in text,
        'Skill' in text or 'skill' in text.lower(),
        '飞书' in text,
        '知识库' in text,
        '模型' in text and len(text) > 15,
        '项目' in text and len(text) > 20,
    ])
    
    # 排除纯对话/非事实语句
    is_dialogue = any([
        text.startswith('我') and len(text) < 50,
        text.startswith('那你'),
        text.startswith('好的'),
        text.startswith('是的'),
        text.startswith('收到'),
        '老大' in text and len(text) < 30,
        text.startswith('让'),
        text.startswith('可以'),
        '对吧' in text,
        '是吗' in text,
    ])
    
    return has_info and not is_dialogue

def clean_text(text: str) -> str:
    """清理文本 - 去掉日期前缀、标记等"""
    # 去掉 - [2026-04-XX] 前缀
    text = re.sub(r'^-\s*\[[\d-]+\]\s*', '', text)
    # 去掉 Candidate: 前缀
    text = re.sub(r'^-\s*Candidate:\s*', '', text)
    # 去掉系统消息
    text = re.sub(r'^-\s*System\s*\(untrusted\).*?:\s*', '', text)
    # 去掉 Assistant: / User: 前缀
    text = re.sub(r'^-\s*(Assistant|User):\s*', '', text)
    # 去掉列表标记
    text = re.sub(r'^-\s+', '', text).strip()
    # 去掉星号标记
    text = re.sub(r'^\*\*\s*', '', text).strip()
    return text

def extract_facts_from_daily(force_all: bool = False) -> list:
    """从每日记忆文件提取有意义的事实"""
    facts = []
    seen_texts = set()
    
    days_range = MAX_AGE_DAYS if not force_all else 30
    
    for i in range(days_range):
        check_date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        day_file = MEMORY_DIR / f'{check_date}.md'
        if not day_file.exists():
            continue
            
        with open(day_file, 'r') as f:
            lines = f.readlines()
        
        for line in lines:
            stripped = line.strip()
            
            # 跳过噪音
            if is_noise(stripped):
                continue
            
            # 清理文本
            cleaned = clean_text(stripped)
            if not cleaned or len(cleaned) < 15:
                continue
            
            # 去重（基于前80字符的md5相似度）
            key = re.sub(r'\s+', '', cleaned)[:80].lower()
            if key in seen_texts:
                continue
            seen_texts.add(key)
            
            # 判断是否有意义
            if not is_meaningful_fact(cleaned):
                continue
            
            cat = get_category(cleaned)
            facts.append({
                'text': cleaned[:200],
                'category': cat,
                'date': check_date
            })
    
    return facts

def update_memory_md(facts: list, stats: dict):
    """重新组织 MEMORY.md 结构"""
    backup_memory()
    
    # 读取现有MEMORY.md，保留顶部配置
    current = ""
    if MEMORY_PATH.exists():
        with open(MEMORY_PATH, 'r') as f:
            current = f.read()
    
    # 找到第一个"---"之后或者"## 📊 记忆强化记录"之前的配置部分
    # 策略：保留从开头到第一个"## "和项目/项目之间的内容
    sections = re.split(r'\n(?=## )', current)
    
    header_sections = []
    data_sections = []
    in_header = True
    
    for section in sections:
        if section.startswith('## 📊 记忆强化记录') or section.startswith('## 📊 记忆引擎统计'):
            in_header = False
        if in_header:
            header_sections.append(section)
        else:
            data_sections.append(section)
    
    header_content = '\n'.join(header_sections)
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 构建新的事实部分
    new_content = f"\n\n## 📊 记忆强化记录 ({today})\n\n"
    
    if stats:
        by_cat = stats.get('by_category', {})
        new_content += "### 分类分布\n"
        for cat_id, count in sorted(by_cat.items(), key=lambda x: -x[1]):
            cat_name = CATEGORY_NAMES.get(cat_id, cat_id)
            new_content += f"- {cat_name}: {count}条\n"
        new_content += f"\n### 累计统计\n- 总事实数: {stats.get('total_facts', 0)}\n- 重要事实: {stats.get('important_facts', 0)}\n"
    
    # 按分类组织事实
    if facts:
        by_cat = {}
        for fact in facts:
            by_cat.setdefault(fact['category'], []).append(fact)
        
        new_content += "\n### ⭐ 重要记忆\n"
        for cat, cat_facts in sorted(by_cat.items(), key=lambda x: -len(x[1])):
            cat_name = CATEGORY_NAMES.get(cat, cat)
            new_content += f"\n#### {cat_name}\n"
            for fact in cat_facts[:20]:  # 每个分类最多20条
                date_short = fact['date'][5:]  # MM-DD
                new_content += f"- [{date_short}] {fact['text']}\n"
    
    # 写回文件
    final_content = header_content.rstrip() + '\n' + new_content
    
    with open(MEMORY_PATH, 'w') as f:
        f.write(final_content)
    
    print(f"✅ MEMORY.md 已更新，写入 {len(facts)} 条有意义的事实")

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--force-all', action='store_true', help='扫描全部文件（30天）')
    parser.add_argument('--dry-run', action='store_true', help='只统计不写入')
    parser.add_argument('--list-noise', action='store_true', help='列出被过滤的噪音行')
    args = parser.parse_args()
    
    state = load_state()
    stats = state.get('stats', {}) if state else {}
    
    print(f"📡 扫描最近 {MAX_AGE_DAYS} 天的每日记忆...")
    
    facts = extract_facts_from_daily(force_all=args.force_all)
    
    print(f"📊 发现 {len(facts)} 条有意义的事实")
    
    # 按分类统计
    by_cat = {}
    for f in facts:
        by_cat.setdefault(f['category'], 0)
        by_cat[f['category']] += 1
    
    print("\n📊 分类分布:")
    for cat, count in sorted(by_cat.items(), key=lambda x: -x[1]):
        cat_name = CATEGORY_NAMES.get(cat, cat)
        print(f"  {cat_name}: {count}")
    
    if args.dry_run:
        print("\n🔍 Dry-run 模式，未写入")
        print("\n前20条事实预览:")
        for f in facts[:20]:
            print(f"  [{f['date']}] [{f['category']}] {f['text'][:60]}...")
        return
    
    if facts:
        update_memory_md(facts, stats)
    else:
        print("ℹ️ 没有新事实需要写入")

if __name__ == '__main__':
    main()
