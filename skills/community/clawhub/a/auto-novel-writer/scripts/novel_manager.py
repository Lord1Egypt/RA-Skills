#!/usr/bin/env python3
"""
小说管理工具 - 用于管理长篇小说的目录结构和元数据
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple

# 默认小说根目录
DEFAULT_NOVELS_DIR = Path("novels")


def get_novels_dir() -> Path:
    """获取小说根目录"""
    return DEFAULT_NOVELS_DIR


def ensure_novels_dir():
    """确保小说根目录存在"""
    get_novels_dir().mkdir(exist_ok=True)


def sanitize_name(name: str) -> str:
    """将中文名转换为安全的目录名"""
    # 简单的拼音转换或保留中文
    # 这里保留中文，但替换不安全字符
    return re.sub(r'[\\/:*?"<>|]', '_', name)


def create_novel(name_cn: str, name_en: str = "", novel_type: str = "", 
                 estimated_words: int = 1000000) -> Path:
    """
    创建新小说目录结构
    
    Args:
        name_cn: 小说中文名
        name_en: 小说英文名（用于目录）
        novel_type: 小说类型标签
        estimated_words: 预计总字数
    
    Returns:
        小说根目录路径
    """
    ensure_novels_dir()
    
    # 使用英文名或拼音作为目录名
    if not name_en:
        name_en = sanitize_name(name_cn)
    
    novel_dir = get_novels_dir() / name_en
    
    if novel_dir.exists():
        raise FileExistsError(f"小说 '{name_cn}' 已存在")
    
    # 创建目录结构
    (novel_dir / "characters").mkdir(parents=True)
    (novel_dir / "settings").mkdir(parents=True)
    (novel_dir / "chapters").mkdir(parents=True)
    (novel_dir / "archive" / "drafts").mkdir(parents=True)
    
    # 创建元数据文件
    meta_content = f"""# {name_cn}

## 基本信息
- **中文名**：{name_cn}
- **英文名**：{name_en}
- **类型**：{novel_type}
- **状态**：规划中
- **创建时间**：{datetime.now().strftime('%Y-%m-%d')}

## 进度统计
- **当前卷数**：0
- **当前章节**：0
- **总字数**：0
- **预计总字数**：{estimated_words}
- **完成度**：0%

## 最近更新
- 无

## 备注
- 
"""
    (novel_dir / "meta.md").write_text(meta_content, encoding='utf-8')
    
    # 创建大纲文件模板
    outline_content = f"""# {name_cn} - 小说大纲

## 基本信息
- **书名**：{name_cn}
- **类型**：{novel_type}
- **主线**：【待填写】
- **预计字数**：{estimated_words}

## 核心卖点
- 【待填写】

## 世界观设定
- 详见：[settings/world.md](settings/world.md)

## 修炼/升级体系
- 详见：[settings/system.md](settings/system.md) 或 [settings/cultivation.md](settings/cultivation.md)

## 主要角色
- 详见：[characters/index.md](characters/index.md)

## 卷章规划

### 第一卷：【待命名】
**核心事件**：
**爽点设计**：

| 章节 | 标题 | 内容概要 | 爽点 |
|------|------|----------|------|
| 001 | 【待命名】 | 开局，主角处境 | |
| 002 | 【待命名】 | 金手指觉醒 | |
| 003 | 【待命名】 | | |
| ... | | | |

### 第二卷：【待命名】
...

## 伏笔清单
- 【待记录】

## 待填坑
- 【待记录】
"""
    (novel_dir / "outline.md").write_text(outline_content, encoding='utf-8')
    
    # 创建设定文件
    (novel_dir / "settings" / "world.md").write_text(
        "# 世界观设定\n\n## 背景\n\n## 地理\n\n## 势力分布\n\n## 规则体系\n", 
        encoding='utf-8'
    )
    (novel_dir / "settings" / "system.md").write_text(
        "# 系统/金手指设定\n\n## 系统名称\n\n## 功能说明\n\n## 升级规则\n\n## 限制条件\n", 
        encoding='utf-8'
    )
    (novel_dir / "settings" / "cultivation.md").write_text(
        "# 修炼体系\n\n## 等级划分\n\n## 每个等级的特征\n\n## 突破条件\n", 
        encoding='utf-8'
    )
    (novel_dir / "settings" / "items.md").write_text(
        "# 道具/材料图鉴\n\n## 武器\n\n## 丹药\n\n## 材料\n\n## 特殊物品\n", 
        encoding='utf-8'
    )
    (novel_dir / "settings" / "skills.md").write_text(
        "# 技能/功法图鉴\n\n## 主角技能\n\n## 常见技能\n\n## 稀有技能\n", 
        encoding='utf-8'
    )
    
    # 创建角色档案
    (novel_dir / "characters" / "index.md").write_text(
        "# 角色总览\n\n## 主角\n\n## 女主/重要女性角色\n\n## 反派\n\n## 配角\n\n## 势力/组织\n- 详见：[groups.md](groups.md)\n", 
        encoding='utf-8'
    )
    (novel_dir / "characters" / "groups.md").write_text(
        "# 势力/组织档案\n\n## 主角所属势力\n\n## 敌对势力\n\n## 中立势力\n", 
        encoding='utf-8'
    )
    
    # 创建归档文件
    (novel_dir / "archive" / "ideas.md").write_text(
        "# 灵感记录\n\n## 剧情灵感\n\n## 角色灵感\n\n## 设定灵感\n", 
        encoding='utf-8'
    )
    
    return novel_dir


def list_novels() -> List[Dict]:
    """列出所有小说"""
    ensure_novels_dir()
    novels = []
    
    for item in get_novels_dir().iterdir():
        if item.is_dir() and (item / "meta.md").exists():
            meta = parse_meta(item / "meta.md")
            novels.append({
                "name_en": item.name,
                "name_cn": meta.get("中文名", item.name),
                "type": meta.get("类型", ""),
                "status": meta.get("状态", ""),
                "chapters": meta.get("当前章节", 0),
                "words": meta.get("总字数", 0)
            })
    
    return novels


def parse_meta(meta_path: Path) -> Dict:
    """解析元数据文件"""
    content = meta_path.read_text(encoding='utf-8')
    meta = {}
    
    for line in content.split('\n'):
        if line.startswith('- **') and '**：' in line:
            key = line[4:line.index('**')]
            value = line[line.index('：') + 1:].strip()
            # 尝试转换为数字
            try:
                value = int(value)
            except ValueError:
                try:
                    value = float(value)
                except ValueError:
                    pass
            meta[key] = value
    
    return meta


def get_chapter_dir(novel_name: str, volume: int, chapter: int) -> Path:
    """获取章节目录路径"""
    return get_novels_dir() / novel_name / "chapters" / f"{volume:02d}-{chapter:03d}"


def create_chapter(novel_name: str, volume: int, chapter: int, 
                   title: str = "") -> Path:
    """
    创建新章节目录和文件
    
    Args:
        novel_name: 小说英文名
        volume: 卷号
        chapter: 章节号
        title: 章节标题
    
    Returns:
        章节目录路径
    """
    chapter_dir = get_chapter_dir(novel_name, volume, chapter)
    chapter_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建 content.md
    content_template = f"""# 第{chapter}章 {title}

【正文待写作】

（本章完）
"""
    (chapter_dir / "content.md").write_text(content_template, encoding='utf-8')
    
    # 创建 summary.md
    summary_template = f"""# 第{chapter}章摘要

## 情节概要
【待填写】

## 关键对话
【待填写】

## 爽点/高潮
【待填写】

## 伏笔/悬念
【待填写】
"""
    (chapter_dir / "summary.md").write_text(summary_template, encoding='utf-8')
    
    # 创建 note.md
    note_template = f"""# 第{chapter}章笔记

## 新角色
- 

## 新地点
- 

## 新技能/道具
- 

## 系统信息
- 

## 其他备注
- 
"""
    (chapter_dir / "note.md").write_text(note_template, encoding='utf-8')
    
    return chapter_dir


def get_recent_summaries(novel_name: str, count: int = 10) -> List[Dict]:
    """
    获取最近N章的摘要
    
    Args:
        novel_name: 小说英文名
        count: 获取章节数
    
    Returns:
        摘要列表，按时间顺序（旧→新）
    """
    chapters_dir = get_novels_dir() / novel_name / "chapters"
    
    if not chapters_dir.exists():
        return []
    
    # 获取所有章节目录
    chapter_dirs = []
    for item in chapters_dir.iterdir():
        if item.is_dir():
            # 解析卷-章编号
            match = re.match(r'(\d{2})-(\d{3})', item.name)
            if match:
                volume = int(match.group(1))
                chapter = int(match.group(2))
                chapter_dirs.append((volume, chapter, item))
    
    # 按卷、章排序
    chapter_dirs.sort(key=lambda x: (x[0], x[1]))
    
    # 取最近N章
    recent = chapter_dirs[-count:] if len(chapter_dirs) > count else chapter_dirs
    
    summaries = []
    for volume, chapter, dir_path in recent:
        summary_path = dir_path / "summary.md"
        content_path = dir_path / "content.md"
        
        summary_text = ""
        if summary_path.exists():
            summary_text = summary_path.read_text(encoding='utf-8')
            # 提取情节概要部分
            if "## 情节概要" in summary_text:
                summary_text = summary_text.split("## 情节概要")[1].split("##")[0].strip()
        
        word_count = 0
        if content_path.exists():
            content = content_path.read_text(encoding='utf-8')
            word_count = len(content.replace(' ', '').replace('\n', ''))
        
        summaries.append({
            "volume": volume,
            "chapter": chapter,
            "dir": dir_path.name,
            "summary": summary_text[:500] if summary_text else "暂无摘要",
            "word_count": word_count
        })
    
    return summaries


def update_meta(novel_name: str, **kwargs):
    """更新小说元数据"""
    meta_path = get_novels_dir() / novel_name / "meta.md"
    
    if not meta_path.exists():
        raise FileNotFoundError(f"小说 '{novel_name}' 不存在")
    
    content = meta_path.read_text(encoding='utf-8')
    
    for key, value in kwargs.items():
        pattern = rf'(- \*\*{key}\*\*：).*'
        replacement = rf'\g<1>{value}'
        content = re.sub(pattern, replacement, content)
    
    # 更新最近更新时间
    content = re.sub(
        r'(- \*\*最近更新\*\*：).*',
        rf'\g<1>{datetime.now().strftime("%Y-%m-%d %H:%M")}',
        content
    )
    
    meta_path.write_text(content, encoding='utf-8')


def get_novel_status(novel_name: str) -> Dict:
    """获取小说状态信息"""
    novel_dir = get_novels_dir() / novel_name
    
    if not novel_dir.exists():
        raise FileNotFoundError(f"小说 '{novel_name}' 不存在")
    
    meta = parse_meta(novel_dir / "meta.md")
    
    # 统计章节信息
    chapters_dir = novel_dir / "chapters"
    chapter_count = 0
    total_words = 0
    
    if chapters_dir.exists():
        for item in chapters_dir.iterdir():
            if item.is_dir():
                content_path = item / "content.md"
                if content_path.exists():
                    chapter_count += 1
                    content = content_path.read_text(encoding='utf-8')
                    total_words += len(content.replace(' ', '').replace('\n', ''))
    
    return {
        "meta": meta,
        "chapter_count": chapter_count,
        "total_words": total_words,
        "chapters_dir": chapters_dir
    }


def format_backlog(novel_name: str, count: int = 10) -> str:
    """
    格式化前文回顾
    
    Args:
        novel_name: 小说英文名
        count: 回顾章节数
    
    Returns:
        格式化的回顾文本
    """
    summaries = get_recent_summaries(novel_name, count)
    
    if not summaries:
        return "【无前文记录】"
    
    lines = ["【前文回顾 - 最近{}章】\n".format(len(summaries))]
    
    for s in summaries:
        lines.append(f"第{s['chapter']}章：{s['summary'][:200]}...")
    
    return '\n'.join(lines)


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("Usage: novel_manager.py <command> [args...]")
        print("Commands:")
        print("  create <name_cn> [name_en] [type] - 创建新小说")
        print("  list - 列出所有小说")
        print("  status <novel_name> - 查看小说状态")
        print("  chapter <novel_name> <volume> <chapter> [title] - 创建章节")
        print("  backlog <novel_name> [count] - 获取前文回顾")
        return
    
    command = sys.argv[1]
    
    if command == "create":
        if len(sys.argv) < 3:
            print("Usage: novel_manager.py create <name_cn> [name_en] [type]")
            return
        name_cn = sys.argv[2]
        name_en = sys.argv[3] if len(sys.argv) > 3 else ""
        novel_type = sys.argv[4] if len(sys.argv) > 4 else ""
        
        try:
            path = create_novel(name_cn, name_en, novel_type)
            print(f"创建成功：{path}")
        except FileExistsError as e:
            print(f"错误：{e}")
    
    elif command == "list":
        novels = list_novels()
        if not novels:
            print("暂无小说")
        else:
            print(f"{'英文名':<20} {'中文名':<30} {'类型':<15} {'状态':<10} {'章节':<8} {'字数':<10}")
            print("-" * 100)
            for n in novels:
                print(f"{n['name_en']:<20} {n['name_cn']:<30} {n['type']:<15} {n['status']:<10} {n['chapters']:<8} {n['words']:<10}")
    
    elif command == "status":
        if len(sys.argv) < 3:
            print("Usage: novel_manager.py status <novel_name>")
            return
        novel_name = sys.argv[2]
        try:
            status = get_novel_status(novel_name)
            meta = status["meta"]
            print(f"小说：{meta.get('中文名', novel_name)}")
            print(f"类型：{meta.get('类型', 'N/A')}")
            print(f"状态：{meta.get('状态', 'N/A')}")
            print(f"章节数：{status['chapter_count']}")
            print(f"总字数：{status['total_words']}")
        except FileNotFoundError as e:
            print(f"错误：{e}")
    
    elif command == "chapter":
        if len(sys.argv) < 5:
            print("Usage: novel_manager.py chapter <novel_name> <volume> <chapter> [title]")
            return
        novel_name = sys.argv[2]
        volume = int(sys.argv[3])
        chapter = int(sys.argv[4])
        title = sys.argv[5] if len(sys.argv) > 5 else ""
        
        try:
            path = create_chapter(novel_name, volume, chapter, title)
            print(f"创建成功：{path}")
        except Exception as e:
            print(f"错误：{e}")
    
    elif command == "backlog":
        if len(sys.argv) < 3:
            print("Usage: novel_manager.py backlog <novel_name> [count]")
            return
        novel_name = sys.argv[2]
        count = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        
        try:
            print(format_backlog(novel_name, count))
        except FileNotFoundError as e:
            print(f"错误：{e}")
    
    else:
        print(f"未知命令：{command}")


if __name__ == "__main__":
    main()
