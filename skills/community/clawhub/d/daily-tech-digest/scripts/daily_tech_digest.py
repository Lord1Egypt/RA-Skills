#!/usr/bin/env python3
"""
每日科技热点简报生成器（增强版）
- 收集 AI、数码、科技领域热点
- 抓取每篇文章正文并生成摘要
- 整理到 Obsidian（按主题分类，每天独立文件）
- 推送消息到用户设备
"""

import os
import sys
import json
import subprocess
import re
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from html.parser import HTMLParser

# 配置
OBSIDIAN_VAULT = "/home/sandbox/.openclaw/workspace/repo/obsidian-vault"
DIGEST_FOLDER = "每日科技简报"
SKILLS_PATH = "/home/sandbox/.openclaw/workspace/skills"

# 请求配置
TIMEOUT = 15
UA = "Mozilla/5.0 (compatible; DailyTechDigest/1.0)"


def log(msg: str) -> None:
    """调试信息写到 stderr"""
    print(msg, file=sys.stderr)


def fetch_url(url: str) -> str | None:
    """抓取 URL 返回 HTML 文本"""
    try:
        req = Request(url, headers={"User-Agent": UA})
        with urlopen(req, timeout=TIMEOUT) as resp:
            raw = resp.read()
            # 尝试常见编码
            for enc in ("utf-8", "gbk", "gb2312"):
                try:
                    return raw.decode(enc, errors="replace")
                except (LookupError, UnicodeDecodeError):
                    continue
            return raw.decode("utf-8", errors="replace")
    except (URLError, HTTPError, OSError) as e:
        log(f"抓取失败 {url}: {e}")
        return None


class ArticleExtractor(HTMLParser):
    """从 HTML 中提取正文内容（优化版）"""
    
    def __init__(self):
        super().__init__()
        self.paragraphs = []
        self._current_text = []
        self._in_article = False
        self._in_content_div = False
        self._depth = 0
        self._content_depth = 0
        
        # 正文容器的常见 class/id 关键词
        self._content_indicators = [
            'article', 'content', 'post', 'entry', 'text', 'body',
            'main', 'detail', 'news-content', 'article-content'
        ]
        
        # 需要跳过的标签
        self._skip_tags = {'script', 'style', 'nav', 'header', 'footer', 'aside', 
                          'iframe', 'noscript', 'form', 'button', 'input'}
        self._current_skip = False
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        if tag in self._skip_tags:
            self._current_skip = True
            return
            
        # 检测正文容器
        class_attr = attrs_dict.get('class', '').lower()
        id_attr = attrs_dict.get('id', '').lower()
        
        for indicator in self._content_indicators:
            if indicator in class_attr or indicator in id_attr:
                self._in_content_div = True
                self._content_depth = self._depth
                break
        
        # article 标签
        if tag == 'article':
            self._in_article = True
            
        # p 或 div 标签开始收集文本
        if tag in ('p', 'div'):
            self._current_text = []
            
        self._depth += 1
            
    def handle_endtag(self, tag):
        if tag in self._skip_tags:
            self._current_skip = False
            return
            
        self._depth -= 1
        
        # 结束正文容器
        if self._in_content_div and self._depth <= self._content_depth:
            self._in_content_div = False
            
        if tag == 'article':
            self._in_article = False
            
        # 收集段落
        if tag == 'p' and self._current_text:
            text = ''.join(self._current_text).strip()
            if len(text) > 20:  # 过滤太短的段落
                self.paragraphs.append(text)
            self._current_text = []
            
    def handle_data(self, data):
        if not self._current_skip and data.strip():
            # 只在正文区域内收集
            if self._in_content_div or self._in_article:
                self._current_text.append(data.strip())
    
    def get_text(self, max_length=500):
        """获取提取的文本，限制长度"""
        if not self.paragraphs:
            return ""
        
        # 合并段落
        text = '\n\n'.join(self.paragraphs[:5])  # 最多取前5段
        
        # 清理
        text = re.sub(r'\s+', ' ', text)
        
        # 限制长度
        if len(text) > max_length:
            # 尝试在句号处截断
            text = text[:max_length]
            last_period = text.rfind('。')
            if last_period > max_length // 2:
                text = text[:last_period + 1]
            else:
                text = text + '...'
        
        return text.strip()


def extract_article_content(url: str, max_length: int = 500) -> str:
    """从文章 URL 提取正文摘要"""
    html = fetch_url(url)
    if not html:
        return "（无法获取正文）"
    
    try:
        extractor = ArticleExtractor()
        extractor.feed(html)
        content = extractor.get_text(max_length)
        
        if len(content) < 50:
            # 备用方案：使用正则提取
            # 查找 <p> 标签内容
            p_pattern = r'<p[^>]*>(.*?)</p>'
            matches = re.findall(p_pattern, html, re.DOTALL)
            
            texts = []
            for match in matches[:5]:
                # 移除 HTML 标签
                clean = re.sub(r'<[^>]+>', '', match)
                clean = re.sub(r'\s+', ' ', clean).strip()
                if len(clean) > 20:
                    texts.append(clean)
            
            if texts:
                content = ' '.join(texts)[:max_length]
        
        if len(content) < 50:
            return "（正文提取失败）"
        
        return content
    except Exception as e:
        log(f"解析失败 {url}: {e}")
        return "（解析失败）"


def get_tech_news_with_content():
    """获取科技新闻及其正文内容"""
    try:
        # 导入播报脚本的函数
        sys.path.insert(0, f"{SKILLS_PATH}/daily-tech-broadcast/scripts")
        import broadcast
        
        items = broadcast.fetch_news()
        
        log(f"获取到 {len(items)} 条新闻，开始过滤和抓取正文...")
        
        # 过滤过时新闻（检查 URL 中的日期）
        today = datetime.now()
        today_str = today.strftime("%Y-%m-%d")
        yesterday = today.replace(day=today.day - 1) if today.day > 1 else today
        yesterday_str = yesterday.strftime("%Y-%m-%d")
        
        def is_recent_news(url, content=None):
            """检查 URL 或内容是否包含今天或昨天的日期"""
            # 匹配 URL 中的日期格式：2026-04-22 或 20260422
            date_patterns = [
                r'/(\d{4}-\d{2}-\d{2})/',  # /2026-04-22/
                r'/(\d{8})/',               # /20260422/
                r'-(\d{8})-',               # -20260422-
            ]
            
            # 先检查 URL
            for pattern in date_patterns:
                match = re.search(pattern, url)
                if match:
                    date_str = match.group(1)
                    # 标准化日期格式
                    if len(date_str) == 8:
                        date_str = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
                    # 检查是否是今天或昨天
                    if date_str in [today_str, yesterday_str]:
                        return True
                    return False
            
            # URL 中没有日期，检查内容中的日期
            if content:
                # 匹配内容中的日期：2026年04月22日 或 2026-01-13
                content_date_patterns = [
                    r'(\d{4})年(\d{2})月(\d{2})日',  # 2026年04月22日
                    r'(\d{4}-\d{2}-\d{2})',           # 2026-01-13
                ]
                for pattern in content_date_patterns:
                    match = re.search(pattern, content)
                    if match:
                        if len(match.groups()) == 3:
                            date_str = f"{match.group(1)}-{match.group(2)}-{match.group(3)}"
                        else:
                            date_str = match.group(1)
                        # 检查是否是今天或昨天
                        if date_str in [today_str, yesterday_str]:
                            return True
                        return False
            
            # 直播链接等特殊 URL 保留
            if 'zhibo' in url or 'live' in url:
                return True
            
            return True  # 默认保留
        
        # 先快速过滤（仅 URL）
        quick_filtered = []
        for item in items:
            if is_recent_news(item['url']):
                quick_filtered.append(item)
        
        log(f"URL 过滤后剩余 {len(quick_filtered)} 条")
        
        # 为每条新闻抓取正文并进行二次过滤
        enriched_items = []
        for i, item in enumerate(quick_filtered, 1):
            log(f"处理 {i}/{len(quick_filtered)}: {item['title'][:30]}...")
            
            content = extract_article_content(item['url'], max_length=400)
            
            # 二次过滤：检查内容中的日期
            if not is_recent_news(item['url'], content):
                log(f"  跳过过时新闻: {item['title'][:30]}")
                continue
            
            item['content'] = content
            enriched_items.append(item)
        
        log(f"最终保留 {len(enriched_items)} 条今日新闻")
        return enriched_items
    except Exception as e:
        log(f"获取新闻失败: {e}")
        return []


def categorize_news(items):
    """按主题分类新闻"""
    categories = {
        "AI人工智能": [],
        "数码产品": [],
        "科技互联网": [],
        "行业动态": [],
        "其他热点": []
    }
    
    # AI 相关关键词
    ai_keywords = ["AI", "人工智能", "GPT", "ChatGPT", "Claude", "大模型", "机器学习", 
                   "深度学习", "OpenAI", "Anthropic", "Gemini", "文心", "通义", "智谱",
                   "字节跳动", "豆包", "Kimi", "Moonshot", "AI应用", "AI模型", "智能体"]
    
    # 数码相关关键词
    digital_keywords = ["手机", "iPhone", "华为", "小米", "OPPO", "vivo", "三星", 
                        "笔记本", "电脑", "平板", "耳机", "相机", "芯片", "处理器",
                        "显卡", "GPU", "显示器", "智能手表", "穿戴", "路由", "充电",
                        "硬件", "设备", "Mate", "Galaxy", "Pixel"]
    
    # 科技互联网关键词
    tech_keywords = ["互联网", "科技", "软件", "APP", "算法", "数据", "云计算", 
                     "区块链", "元宇宙", "自动驾驶", "新能源", "电动车", "特斯拉",
                     "比亚迪", "蔚来", "理想", "小鹏", "电商", "平台", "系统",
                     "Windows", "Android", "iOS", "鸿蒙"]
    
    def classify_item(title):
        title_lower = title.lower()
        
        # AI 分类
        for kw in ai_keywords:
            if kw.lower() in title_lower:
                return "AI人工智能"
        
        # 数码分类
        for kw in digital_keywords:
            if kw.lower() in title_lower:
                return "数码产品"
        
        # 科技互联网分类
        for kw in tech_keywords:
            if kw.lower() in title_lower:
                return "科技互联网"
        
        return "行业动态"
    
    for item in items:
        category = classify_item(item['title'])
        categories[category].append(item)
    
    return categories


def generate_obsidian_note(categories, date_str):
    """生成 Obsidian 笔记内容"""
    note_content = f"""---
title: 每日科技简报 - {date_str}
date: {date_str}
tags:
  - 科技简报
  - AI
  - 数码
  - 科技
---

# 📰 每日科技简报
**日期**: {date_str}

---

"""
    
    # 添加各分类内容
    emoji_map = {
        "AI人工智能": "🤖",
        "数码产品": "📱",
        "科技互联网": "💻",
        "行业动态": "📊",
        "其他热点": "🔥"
    }
    
    total_items = 0
    for category, items in categories.items():
        if items:
            total_items += len(items)
            emoji = emoji_map.get(category, "📌")
            note_content += f"## {emoji} {category}\n\n"
            
            for i, item in enumerate(items, 1):
                note_content += f"### {i}. {item['title']}\n\n"
                note_content += f"> 📌 **来源**: {item.get('source', '科技媒体')}\n\n"
                note_content += f"{item.get('content', '（暂无摘要）')}\n\n"
                note_content += f"🔗 [阅读原文]({item['url']})\n\n"
                note_content += "---\n\n"
    
    note_content += f"""*由小艺 Claw 自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    return note_content, total_items


def save_to_obsidian(content, date_str):
    """保存到 Obsidian"""
    folder_path = Path(OBSIDIAN_VAULT) / DIGEST_FOLDER
    folder_path.mkdir(parents=True, exist_ok=True)
    
    file_path = folder_path / f"{date_str}.md"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    log(f"✅ 笔记已保存: {file_path}")
    return str(file_path)


def generate_push_message(categories, total_items):
    """生成推送消息摘要"""
    if total_items == 0:
        return "📰 今日科技简报\n\n暂无热点数据，请稍后重试。"
    
    # 找出最重要的几条
    top_items = []
    for category, items in categories.items():
        for item in items[:2]:
            if len(top_items) < 5:
                top_items.append(item)
    
    msg = f"📰 今日科技简报已更新\n\n"
    msg += f"共收录 {total_items} 条热点，涵盖 AI、数码、科技等领域\n\n"
    
    if top_items:
        msg += "🔥 今日重点:\n"
        for i, item in enumerate(top_items, 1):
            title = item['title'][:35] + ('...' if len(item['title']) > 35 else '')
            msg += f"{i}. {title}\n"
            # 添加简短摘要
            content = item.get('content', '')
            if content and len(content) > 20:
                # 取第一句话
                first_sentence = content.split('。')[0][:50]
                msg += f"   {first_sentence}...\n"
    
    msg += "\n📱 详情请查看 Obsidian 笔记"
    return msg


def git_commit_and_push(date_str):
    """Git 提交并推送"""
    try:
        original_dir = os.getcwd()
        os.chdir(OBSIDIAN_VAULT)
        
        subprocess.run(["git", "pull"], capture_output=True, timeout=30)
        subprocess.run(["git", "add", "."], capture_output=True, timeout=10)
        subprocess.run(
            ["git", "commit", "-m", f"添加每日科技简报: {date_str}"],
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
        # 构建 JSON 数据
        task_data = {
            "task_name": task_name,
            "task_content": content,
            "task_result": result_status
        }
        
        # 写入临时 JSON 文件
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(task_data, f, ensure_ascii=False, indent=2)
            temp_path = f.name
        
        # 调用 today-task 技能推送
        push_script = f"{SKILLS_PATH}/today-task/scripts/task_push.py"
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


def generate_negative_screen_content(categories, total_items, date_str) -> str:
    """生成适合负一屏显示的内容"""
    if total_items == 0:
        return f"# 每日科技简报\n\n**{date_str}**\n\n暂无热点数据"
    
    content = f"# 📰 每日科技简报\n\n**{date_str}** · 共 {total_items} 条热点\n\n---\n\n"
    
    # 找出最重要的几条
    top_items = []
    for category, items in categories.items():
        for item in items[:2]:
            if len(top_items) < 5:
                top_items.append((category, item))
    
    if top_items:
        content += "## 🔥 今日重点\n\n"
        for i, (cat, item) in enumerate(top_items, 1):
            title = item['title'][:40] + ('...' if len(item['title']) > 40 else '')
            content += f"**{i}. {title}**\n\n"
            # 添加简短摘要
            summary = item.get('content', '')[:100]
            if summary:
                content += f"{summary}...\n\n"
    
    content += "---\n\n📱 详情请查看 Obsidian 笔记"
    return content


def main():
    """主函数"""
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    
    log(f"🚀 开始生成 {date_str} 科技简报（增强版）...")
    
    # 1. 获取新闻及正文
    log("📡 获取科技新闻及正文...")
    items = get_tech_news_with_content()
    
    # 2. 分类整理
    log("📊 分类整理...")
    categories = categorize_news(items)
    
    # 3. 生成笔记
    log("📝 生成 Obsidian 笔记...")
    note_content, total_items = generate_obsidian_note(categories, date_str)
    
    # 4. 保存到 Obsidian
    note_path = save_to_obsidian(note_content, date_str)
    
    # 5. Git 同步
    log("🔄 Git 同步...")
    git_commit_and_push(date_str)
    
    # 6. 推送到负一屏
    log("📱 推送到负一屏...")
    negative_screen_content = generate_negative_screen_content(categories, total_items, date_str)
    push_success = push_to_negative_screen(
        task_name=f"每日科技简报 - {date_str}",
        content=negative_screen_content,
        result_status="已完成" if total_items > 0 else "无数据"
    )
    
    # 7. 生成推送消息（备用）
    push_msg = generate_push_message(categories, total_items)
    
    # 输出推送消息
    log("\n" + "="*50)
    log(push_msg)
    log("="*50 + "\n")
    
    # 返回 JSON 格式结果
    result = {
        "success": True,
        "date": date_str,
        "note_path": note_path,
        "total_items": total_items,
        "categories": {k: len(v) for k, v in categories.items()},
        "push_message": push_msg,
        "negative_screen_push": push_success
    }
    print("__JSON_OUTPUT__:")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
