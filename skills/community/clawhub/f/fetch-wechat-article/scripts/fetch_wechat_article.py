"""
fetch_wechat_article.py — 使用 Playwright headed 模式抓取微信公众号文章

保存格式:
  - .md — 结构清晰的 Markdown 文件
  - .html — 带排版的 HTML 文件，可直接浏览器打开

用法:
    python fetch_wechat_article.py [--browser auto|chromium|firefox] <文章URL> [输出目录]

示例:
    python fetch_wechat_article.py https://mp.weixin.qq.com/s/xxx
    python fetch_wechat_article.py --browser firefox https://mp.weixin.qq.com/s/xxx

依赖:
    pip install playwright
    playwright install msedge      # Windows
    playwright install firefox      # Linux（推荐）
    playwright install chromium     # Linux（备选）
"""

import asyncio
import re
import sys
import os
import platform
from datetime import datetime
from playwright.async_api import async_playwright

# 解决 Windows GBK 终端打印中文的问题
if sys.stdout.encoding and sys.stdout.encoding.upper() != "UTF-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def echo(msg):
    """安全打印，避免 GBK 编码错误"""
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode("utf-8", errors="replace").decode("utf-8", errors="replace"))


# ── HTML 转 Markdown ──────────────────────────────────────────


def html_to_markdown(html: str) -> str:
    """将公众号文章的内嵌 HTML 转为干净的 Markdown。"""
    text = html

    # ── 优先处理图片：微信公众号使用懒加载，真实 URL 在 data-src 中 ──
    # 情况 A: data-src 在 src 之前
    text = re.sub(
        r'(<img[^>]*?)data-src="([^"]+)"([^>]*?)src="[^"]*"([^>]*?>)',
        r'\1src="\2"\3\4',
        text,
    )
    # 情况 B: data-src 在 src 之后
    text = re.sub(
        r'(<img[^>]*?)src="[^"]*"([^>]*?)data-src="([^"]+)"([^>]*?>)',
        r'\1src="\3"\2\4',
        text,
    )
    # 情况 C: 只有 data-src 没有 src
    text = re.sub(
        r'(<img[^>]*?)data-src="([^"]+)"([^>]*?/?>)',
        r'\1src="\2"\3',
        text,
    )

    # 现在可以安全删除剩余 data-* 属性（没有 data-src 了）
    text = re.sub(r'data-[a-z]+="[^"]*"', '', text)
    text = re.sub(r'style="[^"]*"', '', text)
    text = re.sub(r'class="[^"]*"', '', text)

    # 块级标签换行
    for tag in ('section', 'div', 'article', 'blockquote'):
        text = re.sub(rf'</?{tag}[^>]*>', '\n', text)
    text = re.sub(r'<br\s*/?>', '\n', text)
    text = re.sub(r'</?p[^>]*>', '\n', text)

    # 列表
    text = re.sub(r'<li[^>]*>', '- ', text)
    text = re.sub(r'</li>', '\n', text)

    # 图片
    text = re.sub(r'<img[^>]*src="([^"]+)"[^>]*>', r'\n![图片](\1)\n', text)

    # 链接
    text = re.sub(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', r'[\2](\1)', text)

    # 加粗 / 斜体
    text = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', text, flags=re.DOTALL)
    text = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', text, flags=re.DOTALL)

    # 代码块
    text = re.sub(r'<pre[^>]*>(.*?)</pre>', lambda m: '\n```\n' + _clean_code(m.group(1)) + '\n```\n', text, flags=re.DOTALL)
    text = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', text, flags=re.DOTALL)

    # 移除剩余所有标签
    text = re.sub(r'<[^>]+>', '', text)

    # HTML 实体解码（尤其是 &amp; → &，影响图片 URL）
    text = (
        text.replace('&amp;', '&')
        .replace('&lt;', '<')
        .replace('&gt;', '>')
        .replace('&quot;', '"')
        .replace('&#39;', "'")
        .replace('&nbsp;', ' ')
    )

    # 清理多余空行
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'^\s+', '', text, flags=re.MULTILINE)

    return text.strip()


def _clean_code(code: str) -> str:
    code = re.sub(r'<[^>]+>', '', code)
    code = code.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&#39;', "'")
    return code.strip()

# ── 生成干净 HTML ────────────────────────────────────────────


def generate_html(title: str, author: str, publish_time: str, md_body: str) -> str:
    """将 Markdown 正文渲染为带样式的 HTML 页面。"""
    html_body = ""
    in_code = False
    for line in md_body.split('\n'):
        line = line.strip()
        if not line:
            if not in_code:
                continue
            else:
                html_body += "\n"
                continue
        if line.startswith('```'):
            if in_code:
                html_body += "</code></pre>\n"
                in_code = False
            else:
                html_body += "<pre><code>"
                in_code = True
            continue
        if in_code:
            html_body += line + "\n"
            continue
        if line.startswith('# '):
            html_body += f"<h1>{line[2:]}</h1>\n"
        elif line.startswith('## '):
            html_body += f"<h2>{line[3:]}</h2>\n"
        elif line.startswith('- '):
            html_body += f"<li>{line[2:]}</li>\n"
        elif line.startswith('> '):
            html_body += f"<blockquote><p>{line[2:]}</p></blockquote>\n"
        else:
            line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
            line = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2" target="_blank">\1</a>', line)
            line = re.sub(r'`(.+?)`', r'<code>\1</code>', line)
            html_body += f"<p>{line}</p>\n"

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title}</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{
    font-family: -apple-system, BlinkMacSystemFont, "PingFang SC",
                 "Noto Sans CJK SC", "Microsoft YaHei", sans-serif;
    background: #f5f5f5; color: #333; line-height: 1.8;
    letter-spacing: 0.5px;
}}
.container {{
    max-width: 720px; margin: 0 auto; background: #fff;
    min-height: 100vh; padding: 40px 24px 60px;
    box-shadow: 0 0 20px rgba(0,0,0,0.05);
}}
.header {{
    text-align: center; padding-bottom: 24px;
    border-bottom: 1px solid #e8e8e8; margin-bottom: 24px;
}}
.header h1 {{ font-size: 22px; color: #1a1a1a; margin-bottom: 10px; }}
.header .meta {{ font-size: 14px; color: #888; }}
.header .author {{ color: #07c160; font-weight: 500; }}
.content {{ font-size: 16px; }}
.content p {{ margin-bottom: 16px; text-indent: 2em; }}
.content h2 {{ margin: 28px 0 14px; padding-left: 12px;
    border-left: 4px solid #07c160; font-size: 20px; }}
.content h3 {{ margin: 24px 0 12px; font-size: 18px; }}
.content blockquote {{
    margin: 16px 0; padding: 12px 16px; background: #f8f8f8;
    border-left: 4px solid #07c160; color: #555; font-size: 14px;
    border-radius: 0 4px 4px 0;
}}
.content blockquote p {{ margin-bottom: 4px; text-indent: 0; }}
.content code {{
    font-family: "SF Mono", "Fira Code", "Consolas", monospace;
    background: #f0f0f0; padding: 2px 6px; border-radius: 3px;
    font-size: 14px; color: #d63384;
}}
.content pre {{
    background: #2d2d2d; color: #ccc; padding: 16px 20px;
    border-radius: 6px; overflow-x: auto; font-size: 13px;
    line-height: 1.6; margin: 16px 0;
    font-family: "SF Mono", "Fira Code", "Consolas", monospace;
}}
.content li {{ margin: 4px 0 4px 2em; list-style: disc; }}
.content a {{ color: #07c160; text-decoration: none;
    word-break: break-all; }}
.content a:hover {{ text-decoration: underline; }}
.content img {{ max-width: 100%; border-radius: 6px;
    margin: 12px 0; }}
@media (max-width: 480px) {{
    .container {{ padding: 20px 16px 40px; }}
    .header h1 {{ font-size: 20px; }}
    .content {{ font-size: 15px; }}
}}
</style>
</head>
<body>
<div class="container">
<div class="header">
  <h1>{title}</h1>
  <div class="meta">
    <span class="author">{author}</span>
    {" \xb7 " + publish_time if publish_time else ""}
  </div>
</div>
<div class="content">
{html_body}
</div>
</div>
</body>
</html>'''


# ── 提取发布时间 ──────────────────────────────────────────────


async def extract_publish_time(page) -> str:
    selectors = [
        "#publish_time",
        ".rich_media_meta .rich_media_meta_text:nth-child(2)",
        ".rich_media_meta_list .rich_media_meta:last-child .rich_media_meta_text",
    ]
    for sel in selectors:
        try:
            el = await page.query_selector(sel)
            if el:
                text = (await el.inner_text()).strip()
                if text:
                    return text
        except Exception:
            continue
    return ""


# ── 主函数 ────────────────────────────────────────────────────


async def fetch_article(url: str, output_dir: str = ".", browser_arg: str = "auto") -> dict:
    """抓取公众号文章，保存 .md 和 .html 文件。"""
    os.makedirs(output_dir, exist_ok=True)

    system = platform.system()
    has_display = bool(os.environ.get("DISPLAY")) or system == "Windows" or system == "Darwin"

    # ── 浏览器选择 ──
    if browser_arg in ("chromium", "firefox"):
        engine_name = browser_arg
        channel = None
    else:
        if system == "Windows":
            engine_name = "chromium"
            channel = "msedge"
        elif system == "Darwin":
            engine_name = "chromium"
            channel = "chrome"
        else:  # Linux
            engine_name = "firefox"
            channel = None

    headless = (system == "Linux" and not has_display) or False

    echo(f"  🖥️  平台: {system}, 引擎: {engine_name}")
    if channel:
        echo(f"  🔧 通道: {channel}")
    echo(f"  📺 模式: {'headless' if headless else 'headed'}")

    async with async_playwright() as p:
        engine = getattr(p, engine_name)
        launch_kwargs = {
            "headless": headless,
            "args": [
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ],
        }
        if channel:
            launch_kwargs["channel"] = channel

        browser = await engine.launch(**launch_kwargs)
        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Linux; Android 12; Pixel 6) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/125.0.0.0 Mobile Safari/537.36"
            ),
            viewport={"width": 375, "height": 812},
            locale="zh-CN",
            timezone_id="Asia/Shanghai",
        )
        # 反检测脚本
        anti_detect = """
            Object.defineProperty(navigator, 'webdriver', { get: () => false });
        """
        if headless and system == "Linux":
            anti_detect += """
            Object.defineProperty(navigator, 'plugins', { get: () => [1,2,3,4,5] });
            Object.defineProperty(navigator, 'languages', { get: () => ['zh-CN', 'zh'] });
            window.chrome = { runtime: {} };
        """
        await context.add_init_script(anti_detect)
        page = await context.new_page()

        echo("正在打开: " + url)
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)

        for i in range(15):
            await asyncio.sleep(2)
            body_text = await page.evaluate("document.body.innerText")
            current_url = page.url
            echo("  [{}s] {}".format(i*2+2, current_url))
            if "环境异常" not in body_text and "验证" not in body_text:
                echo("  [OK] 文章加载成功！")
                break
        else:
            echo("  [WARN] 页面可能被拦截，继续尝试提取内容...")

        # 提取元数据
        title_el = await page.query_selector("#activity-name")
        title = (await title_el.inner_text()).strip() if title_el else ""

        author_el = await page.query_selector(
            "#js_author_name, #js_name, .rich_media_meta_nickname"
        )
        author = (await author_el.inner_text()).strip() if author_el else ""

        publish_time = await extract_publish_time(page)

        # 提取正文 HTML
        content_el = await page.query_selector("#js_content")
        raw_html = ""
        if content_el:
            raw_html = await content_el.inner_html()
        else:
            raw_html = body_text

        await browser.close()

    # 构造文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_title = "".join(c if c.isalnum() or c in " _-." else "_" for c in title)[:60]
    basename = f"wechat_{safe_title}_{timestamp}" if safe_title else f"wechat_article_{timestamp}"

    # 转换为 Markdown
    md_body = html_to_markdown(raw_html)
    md_content = f"# {title}\n\n"
    md_content += f"> **作者：** {author}\n"
    if publish_time:
        md_content += f"> **时间：** {publish_time}\n"
    md_content += f"> **来源：** {url}\n"
    md_content += f"> **抓取：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    md_content += "---\n\n"
    md_content += md_body
    md_content += "\n\n---\n*由 fetch-wechat-article 抓取生成*"

    md_path = os.path.join(output_dir, f"{basename}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    # 生成干净 HTML
    html_content = generate_html(title, author, publish_time, md_body)
    html_path = os.path.join(output_dir, f"{basename}.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    echo("\n  [OK] Markdown: " + md_path + "  (" + str(len(md_body)) + " 字)")
    echo("  [OK] HTML:     " + html_path)

    return {
        "title": title,
        "author": author,
        "md_path": md_path,
        "html_path": html_path,
        "content_length": len(md_body),
    }


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("用法: python fetch_wechat_article.py [--browser auto|chromium|firefox] <文章URL> [输出目录]")
        print("示例:")
        print("  python fetch_wechat_article.py https://mp.weixin.qq.com/s/xxx")
        print("  python fetch_wechat_article.py --browser firefox https://mp.weixin.qq.com/s/xxx")
        sys.exit(1)

    url = None
    output_dir = "."
    browser_arg = "auto"

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--browser" and i + 1 < len(sys.argv):
            browser_arg = sys.argv[i + 1].lower()
            i += 2
        elif arg.startswith("http://") or arg.startswith("https://"):
            url = arg
            i += 1
        elif os.path.isdir(arg) and arg != ".":
            output_dir = arg
            i += 1
        else:
            i += 1

    if not url:
        print("❌ 未提供有效的文章 URL")
        sys.exit(1)

    result = asyncio.run(fetch_article(url, output_dir, browser_arg))
    echo("\nDone!")
    echo("  标题: " + result['title'])
    echo("  作者: " + result['author'])
    echo("  字数: " + str(result['content_length']))
