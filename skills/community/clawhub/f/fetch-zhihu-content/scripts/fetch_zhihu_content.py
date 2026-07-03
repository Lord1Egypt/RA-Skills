"""
fetch_zhihu_content.py — 使用 Playwright 抓取知乎文章/回答

用法:
    python fetch_zhihu_content.py [--browser auto|chromium|firefox] <一个或多个知乎URL> [输出目录]

示例:
    python fetch_zhihu_content.py https://zhuanlan.zhihu.com/p/123456
    python fetch_zhihu_content.py --browser firefox https://zhuanlan.zhihu.com/p/123456
    python fetch_zhihu_content.py https://zhuanlan.zhihu.com/p/123456 ./output

依赖:
    pip install playwright
    playwright install msedge      # Windows
    playwright install firefox      # Linux（推荐）
    playwright install chromium     # Linux（备选）
"""

import asyncio
import os
import sys
import re
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


# ── URL 识别 ──────────────────────────────────────────────────


def classify_url(url: str) -> str:
    """识别知乎 URL 类型：article / answer / question / unknown"""
    if "zhuanlan.zhihu.com/p/" in url:
        return "article"
    if "/question/" in url and "/answer/" in url:
        return "answer"
    if "/answer/" in url:
        return "answer"
    if "/question/" in url:
        return "question"
    return "unknown"


# ── 内容提取 ──────────────────────────────────────────────────


def html_to_markdown(html: str) -> str:
    """将 HTML 转为 Markdown，保留图片等信息。"""
    text = html

    # 图片：每个 <img> 只处理一次，过滤占位符并按 URL 去重
    seen_urls = set()

    def _replace_img(m):
        nonlocal seen_urls
        tag = m.group(0)
        # 跳过 data:image URI（SVG 占位符等）
        if 'src="data:image/' in tag:
            return ''
        # 优先取 data-actualsrc（知乎懒加载），其次 src
        m2 = re.search(r'data-actualsrc="([^"]+)"', tag)
        if m2:
            url = m2.group(1)
        else:
            m2 = re.search(r'src="([^"]+)"', tag)
            if m2:
                url = m2.group(1)
            else:
                return ''
        # 去重：相同 URL 不重复输出
        if url in seen_urls:
            return ''
        seen_urls.add(url)
        return '\n![图片](' + url + ')\n'

    text = re.sub(r'<img[^>]*>', _replace_img, text)

    # 链接
    text = re.sub(
        r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
        r'[\2](\1)',
        text,
        flags=re.DOTALL,
    )

    # 加粗 / 斜体
    text = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', text, flags=re.DOTALL)
    text = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', text, flags=re.DOTALL)

    # 代码块
    text = re.sub(
        r'<pre[^>]*>(.*?)</pre>',
        lambda m: '\n```\n' + re.sub(r'<[^>]+>', '', m.group(1)).strip() + '\n```\n',
        text,
        flags=re.DOTALL,
    )
    text = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', text, flags=re.DOTALL)

    # 块级标签换行
    for tag in ('section', 'div', 'article', 'blockquote', 'figure', 'p'):
        text = re.sub(rf'</?{tag}[^>]*>', '\n', text)
    text = re.sub(r'<br\s*/?>', '\n', text)

    # 列表
    text = re.sub(r'<li[^>]*>', '- ', text)
    text = re.sub(r'</li>', '\n', text)

    # 标题标签
    text = re.sub(r'</?h[1-6][^>]*>', '\n', text)

    # 移除剩余所有标签
    text = re.sub(r'<[^>]+>', '', text)

    # HTML 实体解码
    text = (
        text.replace('&amp;', '&')
        .replace('&lt;', '<')
        .replace('&gt;', '>')
        .replace('&quot;', '"')
        .replace('&#39;', "'")
        .replace('&nbsp;', ' ')
    )

    # 清理多余空行
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    text = re.sub(r'^\s+', '', text, flags=re.MULTILINE)

    return text.strip()


async def extract_content(page) -> dict:
    """从页面提取标题和正文"""
    result = {"title": "", "content": ""}

    # 获取页面标题
    title = await page.title()
    if title:
        # 清理知乎页面标题后缀 " - 知乎"
        title = re.sub(r'\s*[-–—]\s*知乎\s*$', '', title).strip()
        result["title"] = title

    # 等待内容渲染
    await asyncio.sleep(2)
    # 滚动触发懒加载
    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    await asyncio.sleep(1)

    # 优先尝试多种正文选择器，先获取 HTML 以保留图片
    content_html = ""
    content_text = ""
    selectors = [
        ".RichText",                 # 知乎标准正文容器
        ".RichContent .RichText",    # 回答页正文
        ".Post-RichText",            # 专栏文章正文
        ".AnswerCard .RichText",     # 回答卡片
        ".ContentItem-content",      # 通用内容
        ".PostIndex-content",        # 专栏索引
        "article",                   # HTML5 article
        "[class*='Content']",        # 模糊匹配
    ]

    for sel in selectors:
        try:
            el = page.locator(sel).first
            if await el.count() > 0:
                html = (await el.inner_html()).strip()
                text = (await el.inner_text()).strip()
                if len(text) > 200:
                    content_html = html
                    content_text = text
                    break
        except Exception:
            continue

    # 兜底：从 body 过滤出正文
    if not content_html:
        try:
            content_html = await page.locator("body").inner_html()
            text = await page.locator("body").inner_text()
            lines = [l.strip() for l in text.split("\n") if l.strip() and len(l.strip()) > 20]
            skip_keywords = ["知乎", "广告", "登录", "注册", "下载 App"]
            filtered = []
            for line in lines:
                if any(kw in line for kw in skip_keywords) and len(line) < 30:
                    continue
                filtered.append(line)
            content_text = "\n".join(filtered)
        except Exception:
            pass

    # 将 HTML 转为 Markdown（保留图片等）
    if content_html:
        result["content"] = html_to_markdown(content_html)
    else:
        result["content"] = content_text
    return result


# ── 保存文件 ──────────────────────────────────────────────────


def save_as_markdown(url: str, data: dict, output_dir: str) -> str:
    """保存为 Markdown 文件"""
    url_type = classify_url(url)
    title = data.get("title") or "无标题"
    content = data.get("content") or ""

    # 安全文件名
    safe_title = re.sub(r'[\\/:*?"<>|]', '_', title)[:40]
    if not safe_title:
        safe_title = "zhihu_article"

    type_label = {"article": "article", "answer": "answer", "question": "question"}.get(url_type, "zhihu")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"zhihu_{type_label}_{safe_title}_{timestamp}.md"
    filepath = os.path.join(output_dir, filename)

    md = f"""# {title}

> **来源：** {url}
> **类型：** {url_type}
> **抓取时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

{content}

---

*由 fetch-zhihu-content 自动抓取，来源：{url}*
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(md)

    return filepath


# ── 主函数 ──────────────────────────────────────────────────


async def fetch_zhihu(url: str, output_dir: str, browser) -> dict:
    """抓取单个知乎页面"""
    url_type = classify_url(url)
    echo(f"\n{'='*50}")
    echo(f"📄 [{url_type}] {url}")
    echo(f"{'='*50}")

    system = platform.system()
    is_headless = system == "Linux" and not os.environ.get("DISPLAY")

    context = await browser.new_context(
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/125.0.0.0 Safari/537.36"
        ),
        viewport={"width": 1280, "height": 800},
        locale="zh-CN",
        timezone_id="Asia/Shanghai",
    )
    # 反检测脚本
    anti_detect = """
        Object.defineProperty(navigator, 'webdriver', { get: () => false });
    """
    if is_headless:
        anti_detect += """
        // 补全 headless 缺失的 API
        Object.defineProperty(navigator, 'plugins', { get: () => [1,2,3,4,5] });
        Object.defineProperty(navigator, 'languages', { get: () => ['zh-CN', 'zh'] });
        window.chrome = { runtime: {} };
    """
    await context.add_init_script(anti_detect)

    page = await context.new_page()
    page.on("pageerror", lambda e: echo(f"  [PAGE ERROR] {e}"))

    try:
        # 尝试加载页面，等待网络空闲
        echo("  正在加载页面...")
        try:
            await page.goto(url, wait_until="networkidle", timeout=30000)
        except Exception as e:
            echo(f"  [网络] {str(e)[:60]}")
            # 如果 networkidle 超时，尝试 domcontentloaded
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=20000)
                await asyncio.sleep(3)
            except Exception:
                pass

        # 短暂等待确保页面稳定后再操作
        await asyncio.sleep(2)

        # 检查是否被拦截或 404
        try:
            body_text = await page.evaluate("document.body.innerText")
            if "你似乎来到了没有知识存在的荒原" in body_text:
                echo("  ⚠️  页面不存在 (404)")
                return {"title": "", "content": "", "url": url, "status": "404"}
            if "验证" in body_text and "环境异常" in body_text:
                echo("  ⚠️  触发反爬验证")
        except Exception:
            await asyncio.sleep(2)
            body_text = await page.evaluate("document.body.innerText")

        # 提取内容
        data = await extract_content(page)

        # 保存
        if data["content"]:
            filepath = save_as_markdown(url, data, output_dir)
            echo(f"  ✅ 获取到 {len(data['content'])} 字符")
            echo(f"  💾 {os.path.basename(filepath)}")
        else:
            echo("  ⚠️  未能提取到正文")
            data["status"] = "no_content"

        data["url"] = url
        return data

    except Exception as e:
        echo(f"  ❌ 错误: {e}")
        return {"title": "", "content": "", "url": url, "status": "error", "error": str(e)}

    finally:
        await page.close()
        await context.close()


def get_browser_config(browser_arg: str = "auto"):
    """根据平台自动配置浏览器通道和头模式。browser_arg: auto / chromium / firefox"""
    system = platform.system()
    has_display = bool(os.environ.get("DISPLAY")) or system == "Windows" or system == "Darwin"

    # 引擎选择
    if browser_arg in ("chromium", "firefox"):
        engine = browser_arg
        channel = None
    elif browser_arg != "auto":
        echo(f"  ⚠️  不支持的浏览器: {browser_arg}，使用 auto")
        engine = "chromium"
        channel = None
    else:
        # auto：按平台推断
        if system == "Windows":
            engine = "chromium"
            channel = "msedge"
        elif system == "Darwin":
            engine = "chromium"
            channel = "chrome"
        else:  # Linux
            engine = "firefox"
            channel = None

    # 头模式
    if system == "Linux":
        headless = not has_display
    else:
        headless = False

    if headless:
        echo("  [环境] Linux 无图形界面 → 使用 headless 模式")

    return {"engine": engine, "channel": channel, "headless": headless}


def parse_args():
    """解析命令行参数"""
    urls = []
    output_dir = "."
    browser_arg = "auto"

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--browser" and i + 1 < len(sys.argv):
            browser_arg = sys.argv[i + 1].lower()
            i += 2
        elif arg.startswith("http://") or arg.startswith("https://"):
            urls.append(arg)
            i += 1
        elif os.path.isdir(arg) and arg != ".":
            output_dir = arg
            i += 1
        else:
            if "zhihu.com" in arg:
                urls.append("https://" + arg if not arg.startswith("http") else arg)
            else:
                echo(f"  ⚠️  跳过无法识别的参数: {arg}")
            i += 1

    return urls, output_dir, browser_arg


async def launch_browser(p, cfg: dict):
    """根据配置启动浏览器"""
    engine_name = cfg["engine"]
    launch_kwargs = {
        "headless": cfg["headless"],
        "args": [
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-dev-shm-usage",
        ],
    }
    if cfg["channel"]:
        launch_kwargs["channel"] = cfg["channel"]

    engine = getattr(p, engine_name)
    echo(f"  启动浏览器: {engine_name}" + (f" ({cfg['channel']})" if cfg['channel'] else ""))
    return await engine.launch(**launch_kwargs)


async def main():
    if len(sys.argv) < 2:
        echo("用法: python fetch_zhihu_content.py [--browser auto|chromium|firefox] <一个或多个知乎URL> [输出目录]")
        echo("示例:")
        echo("  python fetch_zhihu_content.py https://zhuanlan.zhihu.com/p/123456")
        echo("  python fetch_zhihu_content.py --browser firefox https://zhuanlan.zhihu.com/p/123456")
        echo("  python fetch_zhihu_content.py https://zhuanlan.zhihu.com/p/123456 ./output")
        sys.exit(1)

    # 解析参数
    urls, output_dir, browser_arg = parse_args()

    if not urls:
        echo("❌ 未提供有效的知乎 URL")
        sys.exit(1)

    echo("")
    os.makedirs(output_dir, exist_ok=True)
    echo(f"📥 知乎内容下载工具")
    echo("   共 {} 个 URL，输出目录: {}".format(len(urls), output_dir))
    echo("")

    browser_cfg = get_browser_config(browser_arg)
    echo(f"  🖥️  平台: {platform.system()}, 引擎: {browser_cfg['engine']}")
    echo(f"  模式: {'headed' if not browser_cfg['headless'] else 'headless'}")
    echo("")

    async with async_playwright() as p:
        browser = await launch_browser(p, browser_cfg)

        results = []
        for url in urls:
            result = await fetch_zhihu(url, output_dir, browser)
            results.append(result)
            await asyncio.sleep(1)  # 礼貌间隔

        await browser.close()

    # 汇总
    echo(f"\n{'='*50}")
    echo("📊 下载汇总")
    echo(f"{'='*50}")
    success = [r for r in results if r.get("content")]
    echo(f"✅ 成功: {len(success)}/{len(results)}")
    for r in success:
        echo(f"   📄 {r.get('title', '无标题')[:40]} ({len(r.get('content', ''))} 字)")
    failed = [r for r in results if not r.get("content")]
    for r in failed:
        echo(f"   ❌ {r.get('url', '?')} — {r.get('status', 'unknown')}")


if __name__ == "__main__":
    asyncio.run(main())
