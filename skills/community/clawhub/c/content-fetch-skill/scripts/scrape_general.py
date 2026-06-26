#!/usr/bin/env python3
import os
import re
import json
import asyncio
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
from playwright.async_api import async_playwright, Browser, Page, Response


def clean_text(text: str) -> str:
    """清理文本，移除多余空格和换行"""
    if not text:
        return ''
    # 替换多个换行/空格为单个
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


async def extract_title(page: Page) -> str:
    """智能提取页面标题"""
    # 优先使用title标签
    title = await page.title()
    title = title.strip()
    if title and len(title) > 5:
        return title

    # 尝试查找h1标签
    h1_selectors = ['h1', '.title', '.article-title', '.post-title', '.entry-title']
    for selector in h1_selectors:
        try:
            element = page.locator(selector).first
            if element:
                text = await element.text_content(timeout=1000)
                text = text.strip() if text else ''
                if text and len(text) > 5:
                    return text
        except:
            continue

    # 尝试提取正文前50个字符作为标题
    try:
        content_selectors = ['article', '.content', '.post-content', '.entry-content', 'main', '#content']
        for selector in content_selectors:
            element = page.locator(selector).first
            if element:
                text = await element.text_content(timeout=1000)
                text = text.strip() if text else ''
                if text:
                    # 取前50个字符，截止到第一个句号或换行
                    short_text = text[:100].split('。')[0].split('\n')[0].strip()
                    if len(short_text) > 10:
                        return short_text
    except:
        pass

    return '无标题'


async def extract_content(page: Page) -> str:
    """智能提取正文内容"""
    # 优先查找常见的正文容器
    content_selectors = [
        'article',
        '.article-content', '.post-content', '.entry-content',
        '.content', '#content', '.main-content',
        '.post-body', '.entry-body', '.article-body'
    ]

    for selector in content_selectors:
        try:
            elements = await page.locator(selector).all()
            if elements:
                # 找到最长的内容块
                max_length = 0
                best_element = None
                for elem in elements:
                    text = await elem.text_content(timeout=1000)
                    text = text.strip() if text else ''
                    if len(text) > max_length:
                        max_length = len(text)
                        best_element = elem

                if best_element and max_length > 100:
                    # 移除无用标签（脚本、样式、导航、广告等）
                    await best_element.evaluate('''
                        element => {
                            const uselessSelectors = ['script', 'style', 'nav', 'header', 'footer', 'aside', '.ad', '.advertisement', '.sidebar', '.comment', '.comments'];
                            uselessSelectors.forEach(selector => {
                                element.querySelectorAll(selector).forEach(el => el.remove());
                            });
                        }
                    ''')

                    # 提取所有文本
                    text = await best_element.text_content(timeout=3000)
                    return clean_text(text)
        except Exception as e:
            print(f"⚠️ 提取内容失败 {selector}: {e}")
            continue

    #  fallback: 提取body中所有文本
    try:
        body = page.locator('body').first
        # 移除无用标签
        await body.evaluate('''
            element => {
                const uselessSelectors = ['script', 'style', 'nav', 'header', 'footer', 'aside', '.ad', '.advertisement', '.sidebar'];
                uselessSelectors.forEach(selector => {
                    element.querySelectorAll(selector).forEach(el => el.remove());
                });
            }
        ''')
        text = await body.text_content(timeout=3000)
        return clean_text(text)
    except:
        return '无内容'


async def extract_images(page: Page, base_url: str, output_dir: str) -> List[Dict]:
    """提取页面所有图片并保存到本地"""
    images_dir = os.path.join(output_dir, 'images')
    os.makedirs(images_dir, exist_ok=True)

    images = []
    img_elements = await page.locator('img').all()

    for i, img in enumerate(img_elements):
        try:
            # 获取图片URL
            src = await img.get_attribute('src', timeout=1000)
            if not src:
                src = await img.get_attribute('data-src', timeout=1000)
            if not src:
                continue

            # 转换为绝对URL
            absolute_url = urljoin(base_url, src)
            if not absolute_url.startswith(('http://', 'https://')):
                continue

            # 获取图片alt文本
            alt = await img.get_attribute('alt', timeout=1000) or ''
            alt = clean_text(alt)

            # 尝试下载图片
            try:
                # 生成文件名
                ext = os.path.splitext(urlparse(absolute_url).path)[1].lower() or '.jpg'
                if ext not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                    ext = '.jpg'
                filename = f'image_{i+1}{ext}'
                save_path = os.path.join(images_dir, filename)

                # 下载图片
                response = await page.request.get(absolute_url, timeout=10000)
                if response.ok:
                    image_data = await response.body()
                    with open(save_path, 'wb') as f:
                        f.write(image_data)

                    images.append({
                        'url': absolute_url,
                        'alt': alt,
                        'local_path': os.path.join('images', filename),
                        'size': len(image_data)
                    })
            except:
                # 下载失败，只保存URL
                images.append({
                    'url': absolute_url,
                    'alt': alt,
                    'local_path': ''
                })
        except:
            continue

    return images


async def scrape_task(
    proxy: str,
    url: str,
    cookies: str = '',
    headless: bool = True,
    output_dir: str = '',
    output: str = ''
) -> List[Dict]:
    """
    通用网站爬取任务
    自动提取页面标题、正文、图片，保存截图
    返回格式统一的结果列表
    """
    browser: Optional[Browser] = None
    page: Optional[Page] = None

    try:
        # 启动浏览器
        print("🌐 启动浏览器...")
        async with async_playwright() as p:
            # 浏览器配置
            browser_args = [
                '--disable-blink-features=AutomationControlled',
                '--start-maximized',
                '--no-sandbox',
                '--disable-dev-shm-usage',
            ]

            # 代理配置
            proxy_config = None
            if proxy and proxy.lower() != 'none':
                proxy_config = {'server': proxy}
                print(f"🔧 使用代理: {proxy}")

            # 启动浏览器
            browser = await p.chromium.launch(
                headless=headless,
                args=browser_args,
                proxy=proxy_config
            )

            # 创建浏览器上下文
            context = await browser.new_context(
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
                viewport={'width': 1920, 'height': 1080},
                ignore_https_errors=True
            )

            # 加载Cookie
            if cookies and os.path.exists(cookies):
                print(f"🍪 加载Cookie文件: {cookies}")
                try:
                    with open(cookies, 'r', encoding='utf-8') as f:
                        cookie_list = json.load(f)
                    await context.add_cookies(cookie_list)
                    print("✅ Cookie已成功添加到浏览器上下文")
                except Exception as e:
                    print(f"⚠️ Cookie加载失败: {e}")

            # 反检测设置
            await context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });

                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5]
                });

                Object.defineProperty(navigator, 'languages', {
                    get: () => ['zh-CN', 'zh', 'en-US', 'en']
                });
            """)

            # 创建页面
            page = await context.new_page()

            # 访问目标页面
            print(f"🌍 访问目标页面: {url}")
            response: Optional[Response] = await page.goto(url, timeout=60000, wait_until='domcontentloaded')

            if not response or not response.ok:
                status_code = response.status if response else 'N/A'
                raise Exception(f"页面访问失败，状态码: {status_code}")

            print(f"✅ 页面加载完成，当前URL: {page.url}")

            # 等待页面稳定
            await asyncio.sleep(2)

            # 滚动页面加载完整内容
            print("🔄 滚动页面加载完整内容...")
            previous_height = 0
            for _ in range(5):  # 最多滚动5次
                current_height = await page.evaluate('document.body.scrollHeight')
                if current_height == previous_height:
                    break
                previous_height = current_height
                await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                await asyncio.sleep(1)

            # 回到页面顶部
            await page.evaluate('window.scrollTo(0, 0)')
            await asyncio.sleep(0.5)

            # 保存页面截图
            screenshot_path = os.path.join(output_dir, 'page_screenshot.png')
            print(f"📸 保存页面截图...")
            await page.screenshot(
                path=screenshot_path,
                full_page=True,
                timeout=120000  # 长页面截图增加超时
            )

            # 提取信息
            print("🔍 智能提取页面信息...")

            # 提取标题
            title = await extract_title(page)
            print(f"📝 提取标题: {title[:50]}..." if len(title) > 50 else f"📝 提取标题: {title}")

            # 提取正文
            content = await extract_content(page)
            print(f"📄 提取正文完成，共 {len(content)} 字符")

            # 提取图片
            images = await extract_images(page, url, output_dir)
            print(f"🖼️  提取到 {len(images)} 张图片")

            # 收集结果
            result = [{
                'title': title,
                'content': content,
                'url': page.url,
                'images': images,
                'created_at': '',  # 通用站点不提取时间，留空
                'author': '',      # 通用站点不提取作者，留空
                'like_count': 0,
                'retweet_count': 0,
                'reply_count': 0,
                'screenshot': 'page_screenshot.png'
            }]

            # 保存结果
            if output:
                with open(output, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                print(f"💾 结果已保存到: {output}")

            return result

    except Exception as e:
        print(f"❌ 爬取失败: {str(e)}")
        raise
    finally:
        # 清理资源
        if page:
            try:
                await page.close()
            except:
                pass
        if browser:
            try:
                await browser.close()
            except:
                pass
