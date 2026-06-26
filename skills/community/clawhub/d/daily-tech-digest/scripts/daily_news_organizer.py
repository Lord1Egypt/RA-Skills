#!/usr/bin/env python3
"""
每日新闻整理器
- 读取当天的科技简报
- 将每条新闻拆分为独立笔记
- 按主题分类存储到 Obsidian
"""

import os
import sys
import json
import re
from datetime import datetime
from pathlib import Path

# 配置
OBSIDIAN_VAULT = "/home/sandbox/.openclaw/workspace/repo/obsidian-vault"
DIGEST_FOLDER = "每日科技简报"
ARCHIVE_FOLDER = "归档"  # 归档根目录

# 分类到归档子文件夹的映射
CATEGORY_FOLDERS = {
    "AI人工智能": "AI人工智能",
    "数码产品": "数码产品", 
    "科技互联网": "科技互联网",
    "行业动态": "行业动态",
    "其他热点": "其他热点"
}


def log(msg: str) -> None:
    """调试信息写到 stderr"""
    print(msg, file=sys.stderr)


def read_daily_digest(date_str: str) -> str | None:
    """读取当天的简报文件"""
    digest_path = Path(OBSIDIAN_VAULT) / DIGEST_FOLDER / f"{date_str}.md"
    
    if not digest_path.exists():
        log(f"简报文件不存在: {digest_path}")
        return None
    
    with open(digest_path, 'r', encoding='utf-8') as f:
        return f.read()


def parse_digest_to_articles(digest_content: str) -> list[dict]:
    """解析简报，提取每条新闻"""
    articles = []
    
    # 按分类标题分割
    category_pattern = r'## ([🤖📱💻📊🔥]) (.+)\n\n'
    sections = re.split(category_pattern, digest_content)
    
    # sections 格式: [前言, emoji1, category1, content1, emoji2, category2, content2, ...]
    current_category = None
    
    for i in range(1, len(sections), 3):
        if i + 2 > len(sections):
            break
            
        emoji = sections[i]
        category = sections[i + 1]
        content = sections[i + 2]
        
        # 解析该分类下的每条新闻
        # 格式: ### 1. 标题\n\n> 📌 **来源**: xxx\n\n正文\n\n🔗 [阅读原文](url)
        article_pattern = r'### \d+\. (.+?)\n\n> 📌 \*\*来源\*\*: (.+?)\n\n(.+?)\n\n🔗 \[阅读原文\]\((.+?)\)'
        
        for match in re.finditer(article_pattern, content, re.DOTALL):
            title = match.group(1).strip()
            source = match.group(2).strip()
            body = match.group(3).strip()
            url = match.group(4).strip()
            
            articles.append({
                'title': title,
                'source': source,
                'category': category,
                'emoji': emoji,
                'content': body,
                'url': url
            })
    
    return articles


def generate_article_note(article: dict, date_str: str) -> str:
    """为单条新闻生成笔记内容"""
    
    # 从标题生成安全的文件名
    safe_title = re.sub(r'[^\w\s\u4e00-\u9fff]', '', article['title'])
    safe_title = re.sub(r'\s+', '_', safe_title)[:50]  # 限制长度
    
    # 生成标签
    tags = []
    if article['category'] == 'AI人工智能':
        tags = ['AI', '人工智能', '科技']
    elif article['category'] == '数码产品':
        tags = ['数码', '硬件', '科技']
    elif article['category'] == '科技互联网':
        tags = ['互联网', '科技']
    else:
        tags = ['科技', '行业']
    
    tags_str = ', '.join(tags)
    
    note_content = f"""---
title: {article['title']}
date: {date_str}
source: {article['source']}
category: {article['category']}
tags:
  - {tags_str}
url: {article['url']}
---

# {article['emoji']} {article['title']}

> 📌 **来源**: {article['source']}  
> 📅 **日期**: {date_str}  
> 📂 **分类**: {article['category']}

---

{article['content']}

---

## 🔗 相关链接

- [阅读原文]({article['url']})

---

*由小艺 Claw 自动整理于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    return note_content, safe_title


def save_article_notes(articles: list[dict], date_str: str) -> list[str]:
    """保存每条新闻为独立笔记，归档到 归档/分类/ 下"""
    saved_paths = []
    
    for article in articles:
        note_content, safe_title = generate_article_note(article, date_str)
        
        # 归档到 归档/分类/ 下
        category_folder_name = CATEGORY_FOLDERS.get(article['category'], article['category'])
        category_folder = Path(OBSIDIAN_VAULT) / ARCHIVE_FOLDER / category_folder_name
        category_folder.mkdir(parents=True, exist_ok=True)
        
        # 生成文件名：日期_标题.md
        filename = f"{date_str}_{safe_title}.md"
        file_path = category_folder / filename
        
        # 如果文件已存在，先删除旧文件（避免产生 _1, _2 等重复）
        if file_path.exists():
            file_path.unlink()
        
        # 同时清理可能的重复文件
        for old_file in category_folder.glob(f"{date_str}_{safe_title}_*.md"):
            old_file.unlink()
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(note_content)
        
        saved_paths.append(str(file_path))
        log(f"  ✅ [{category_folder_name}] {filename}")
    
    return saved_paths


def generate_index_note(articles: list[dict], date_str: str, saved_paths: list[str]) -> str:
    """生成每日索引笔记"""
    
    index_content = f"""---
title: 每日新闻索引 - {date_str}
date: {date_str}
tags:
  - 新闻索引
  - 日报
---

# 📰 {date_str} 新闻索引

**共收录 {len(articles)} 条新闻**

---

"""
    
    # 按分类分组
    categories = {}
    for article in articles:
        cat = article['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(article)
    
    # 生成索引
    emoji_map = {
        "AI人工智能": "🤖",
        "数码产品": "📱",
        "科技互联网": "💻",
        "行业动态": "📊",
        "其他热点": "🔥"
    }
    
    for category, items in categories.items():
        emoji = emoji_map.get(category, "📌")
        index_content += f"## {emoji} {category} ({len(items)}条)\n\n"
        
        for article in items:
            # 生成内部链接（指向归档/分类/文件）
            safe_title = re.sub(r'[^\w\s\u4e00-\u9fff]', '', article['title'])
            safe_title = re.sub(r'\s+', '_', safe_title)[:50]
            link = f"[[{ARCHIVE_FOLDER}/{category}/{date_str}_{safe_title}|{article['title']}]]"
            
            index_content += f"- {link}\n"
        
        index_content += "\n"
    
    index_content += f"---\n\n*由小艺 Claw 自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
    
    return index_content


def git_commit_and_push(date_str, article_count):
    """Git 提交并推送"""
    try:
        original_dir = os.getcwd()
        os.chdir(OBSIDIAN_VAULT)
        
        import subprocess
        subprocess.run(["git", "pull"], capture_output=True, timeout=30)
        subprocess.run(["git", "add", "."], capture_output=True, timeout=10)
        subprocess.run(
            ["git", "commit", "-m", f"整理每日新闻: {date_str} ({article_count}条归档)"],
            capture_output=True,
            timeout=10
        )
        result = subprocess.run(["git", "push"], capture_output=True, timeout=30)
        
        if result.returncode == 0:
            log("✅ Git 同步完成")
        else:
            log(f"Git push 警告: {result.stderr.decode()}")
        
        os.chdir(original_dir)
    except Exception as e:
        log(f"Git 操作失败: {e}")


def push_to_negative_screen(task_name: str, content: str, result_status: str = "已完成") -> bool:
    """推送到负一屏卡片"""
    try:
        import subprocess
        import tempfile
        
        # 构建 JSON 数据
        task_data = {
            "task_name": task_name,
            "task_content": content,
            "task_result": result_status
        }
        
        # 写入临时 JSON 文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(task_data, f, ensure_ascii=False, indent=2)
            temp_path = f.name
        
        # 调用 today-task 技能推送
        skills_path = "/home/sandbox/.openclaw/workspace/skills"
        push_script = f"{skills_path}/today-task/scripts/task_push.py"
        proc = subprocess.run(
            ["python3", push_script, "--data", temp_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # 清理临时文件
        os.unlink(temp_path)
        
        if proc.returncode == 0:
            log("✅ 负一屏推送成功")
            return True
        else:
            log(f"⚠️ 负一屏推送失败: {proc.stderr}")
            return False
    except Exception as e:
        log(f"⚠️ 负一屏推送异常: {e}")
        return False


def generate_negative_screen_content(articles, categories_count, date_str) -> str:
    """生成适合负一屏显示的内容"""
    if not articles:
        return f"# 新闻整理完成\n\n**{date_str}**\n\n暂无新闻需要整理"
    
    content = f"# 📰 新闻整理完成\n\n**{date_str}** · 共 {len(articles)} 条已归档\n\n---\n\n"
    content += "## 📂 分类统计\n\n"
    
    emoji_map = {
        "AI人工智能": "🤖",
        "数码产品": "📱",
        "科技互联网": "💻",
        "行业动态": "📊",
        "其他热点": "🔥"
    }
    
    for cat, count in categories_count.items():
        emoji = emoji_map.get(cat, "📌")
        content += f"- {emoji} **{cat}**: {count} 条\n"
    
    content += "\n---\n\n"
    content += f"📑 索引: [[{DIGEST_FOLDER}/{date_str}_索引]]"
    return content


def main():
    """主函数"""
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    
    log(f"🗂️ 开始整理 {date_str} 的新闻...")
    
    # 1. 读取当天简报
    log("📖 读取当天简报...")
    digest_content = read_daily_digest(date_str)
    
    if not digest_content:
        result = {
            "success": False,
            "date": date_str,
            "error": "简报文件不存在",
            "message": f"今天还没有生成简报，请先生成 {date_str} 的科技简报"
        }
        print("__JSON_OUTPUT__:")
        print(json.dumps(result, ensure_ascii=False))
        return
    
    # 2. 解析简报
    log("📋 解析简报内容...")
    articles = parse_digest_to_articles(digest_content)
    
    if not articles:
        result = {
            "success": False,
            "date": date_str,
            "error": "未能解析到新闻",
            "message": "简报中没有找到可整理的新闻"
        }
        print("__JSON_OUTPUT__:")
        print(json.dumps(result, ensure_ascii=False))
        return
    
    log(f"找到 {len(articles)} 条新闻")
    
    # 3. 保存每条新闻为独立笔记
    log("💾 保存独立笔记...")
    saved_paths = save_article_notes(articles, date_str)
    
    # 4. 生成索引笔记
    log("📑 生成索引笔记...")
    index_content = generate_index_note(articles, date_str, saved_paths)
    
    # 索引保存到每日科技简报文件夹
    index_path = Path(OBSIDIAN_VAULT) / DIGEST_FOLDER / f"{date_str}_索引.md"
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    # 5. 删除原简报长文，只保留索引
    log("🗑️ 清理原简报...")
    digest_path = Path(OBSIDIAN_VAULT) / DIGEST_FOLDER / f"{date_str}.md"
    if digest_path.exists():
        digest_path.unlink()
        log(f"  已删除: {date_str}.md")
    
    # 6. Git 同步
    log("🔄 Git 同步...")
    git_commit_and_push(date_str, len(articles))
    
    # 7. 生成分类统计
    categories_count = {}
    for article in articles:
        cat = article['category']
        categories_count[cat] = categories_count.get(cat, 0) + 1
    
    # 8. 推送到负一屏
    log("📱 推送到负一屏...")
    negative_screen_content = generate_negative_screen_content(articles, categories_count, date_str)
    push_success = push_to_negative_screen(
        task_name=f"新闻整理完成 - {date_str}",
        content=negative_screen_content,
        result_status="已完成"
    )
    
    # 9. 生成结果消息
    message = f"📰 {date_str} 新闻整理完成\n\n"
    message += f"共整理 {len(articles)} 条新闻，已归档到 {ARCHIVE_FOLDER}/ 各分类下\n\n"
    message += "📂 分类统计:\n"
    for cat, count in categories_count.items():
        message += f"  • {cat}: {count} 条\n"
    message += f"\n📑 索引文件: [[{DIGEST_FOLDER}/{date_str}_索引]]"
    
    log("\n" + "="*50)
    log(message)
    log("="*50)
    
    result = {
        "success": True,
        "date": date_str,
        "total_articles": len(articles),
        "categories": categories_count,
        "archive_folder": f"{ARCHIVE_FOLDER}",
        "message": message,
        "negative_screen_push": push_success
    }
    print("__JSON_OUTPUT__:")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
