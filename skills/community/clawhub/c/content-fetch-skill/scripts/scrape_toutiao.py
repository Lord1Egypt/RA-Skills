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


async def extract_toutiao_content(page: Page) -> Dict:
    """提取今日头条文章内容"""
    result = {}

    # 提取标题
    try:
        title_elem = page.locator('.article-title').first
        if await title_elem.count() == 0:
            title_elem = page.locator('h1').first
        title = await title_elem.text_content(timeout=2000)
        result['title'] = clean_text(title)
    except:
        result['title'] = await page.title()

    # 提取作者
    try:
        author_elem = page.locator('.article-meta .name').first
        if await author_elem.count() == 0:
            author_elem = page.locator('.author-name').first
        author = await author_elem.text_content(timeout=2000)
        result['author'] = clean_text(author)
    except:
        result['author'] = ''

    # 提取发布时间
    try:
        time_elem = page.locator('.article-meta .time').first
        if await time_elem.count() == 0:
            time_elem = page.locator('.publish-time').first
        time_str = await time_elem.text_content(timeout=2000)
        # 提取时间
        time_match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}', time_str)
        if time_match:
            time_str = time_match.group()
        result['created_at'] = clean_text(time_str)
    except:
        result['created_at'] = ''

    # 提取正文
    try:
        content_elem = page.locator('.article-content').first
        if await content_elem.count() == 0:
            content_elem = page.locator('.content').first
        if await content_elem.count() == 0:
            content_elem = page.locator('.article-body').first

        # 移除无用元素
        await content_elem.evaluate('''
            element => {
                const useless = element.querySelectorAll('.tt-article-addon, .article-actions, .related-articles, .ad, .comment-section, .recommend');
                useless.forEach(el => el.remove());
            }
        ''')

        content = await content_elem.text_content(timeout=5000)
        result['content'] = clean_text(content)
    except:
        result['content'] = '提取内容失败'

    # 提取图片
    images = []
    try:
        # 触发懒加载图片
        await page.evaluate('''
            document.querySelectorAll('.article-content img, .content img, .article-body img').forEach(img => {
                if (img.dataset.src && !img.src) {
                    img.src = img.dataset.src;
                }
                if (img.dataset.lazy && !img.src) {
                    img.src = img.dataset.lazy;
                }
            });
        ''')
        await asyncio.sleep(2)

        img_elements = await page.locator('.article-content img, .content img, .article-body img').all()
        for img in img_elements:
            try:
                src = await img.get_attribute('src', timeout=1000)
                if not src:
                    src = await img.get_attribute('data-src', timeout=1000)
                if not src:
                    src = await img.get_attribute('data-lazy', timeout=1000)
                if not src:
                    continue

                # 处理相对路径
                if src.startswith('//'):
                    src = 'https:' + src
                if not src.startswith(('http://', 'https://')):
                    src = urljoin(page.url, src)

                # 去掉参数
                src = src.split('?')[0]

                alt = await img.get_attribute('alt', timeout=1000) or ''
                alt = clean_text(alt)

                images.append({
                    'url': src,
                    'alt': alt,
                    'local_path': ''
                })
            except:
                continue
    except:
        pass

    result['images'] = images
    return result


async def download_images(page: Page, images: List[Dict], output_dir: str) -> List[Dict]:
    """下载图片到本地"""
    images_dir = os.path.join(output_dir, 'images')
    os.makedirs(images_dir, exist_ok=True)

    # 设置防盗链头
    await page.set_extra_http_headers({
        'Referer': 'https://www.toutiao.com/'
    })

    for i, img in enumerate(images):
        try:
            src = img['url']
            if not src:
                continue

            # 生成文件名
            ext = os.path.splitext(urlparse(src).path)[1].lower() or '.jpg'
            if ext not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                ext = '.jpg'
            filename = f'image_{i+1}{ext}'
            save_path = os.path.join(images_dir, filename)

            # 下载图片
            response = await page.request.get(src, timeout=15000)
            if response.ok:
                image_data = await response.body()
                with open(save_path, 'wb') as f:
                    f.write(image_data)
                img['local_path'] = os.path.join('images', filename)
                img['size'] = len(image_data)
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
    """今日头条文章爬取任务"""
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
                '--disable-extensions',
                '--disable-plugins-discovery',
                '--disable-features=IsolateOrigins,site-per-process',
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
                ignore_https_errors=True,
                extra_http_headers={
                    'Referer': 'https://www.toutiao.com/',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
                }
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
            await context.add_init_script('''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5]
                });
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['zh-CN', 'zh', 'en-US', 'en']
                });
                Object.defineProperty(navigator, 'platform', {
                    get: () => 'MacIntel'
                });
                window.chrome = {
                    runtime: {},
                    loadTimes: () => {},
                    csi: () => {}
                };
                window.toutiao = {
                    is_mobile: false
                };
            ''')

            # 创建页面
            page = await context.new_page()

            # 拦截不需要的资源
            await page.route("**/*.{png,jpg,jpeg,gif,webp,css,woff,woff2,ico,mp4,avi}", lambda route: route.abort() if route.request.resource_type == 'stylesheet' or route.request.resource_type == 'font' or route.request.resource_type == 'media' else route.continue_())

            # 访问目标页面
            print(f"🌍 访问目标页面: {url}")
            response: Optional[Response] = await page.goto(url, timeout=60000, wait_until='domcontentloaded')

            if not response or not response.ok:
                status_code = response.status if response else 'N/A'
                raise Exception(f"页面访问失败，状态码: {status_code}")

            print(f"✅ 页面加载完成，当前URL: {page.url}")

            # 处理登录弹窗
            try:
                close_btn = page.locator('.close-btn, .modal-close').first
                if await close_btn.count() > 0:
                    await close_btn.click(timeout=2000)
                    print("🔒 已自动关闭登录弹窗")
                    await asyncio.sleep(1)
            except:
                pass

            # 等待页面稳定
            await asyncio.sleep(3)

            # 滚动页面加载完整内容
            print("🔄 滚动页面加载完整内容...")
            previous_height = 0
            for _ in range(8):
                current_height = await page.evaluate('document.body.scrollHeight')
                if current_height == previous_height:
                    break
                previous_height = current_height
                await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                await asyncio.sleep(1.5)

            # 回到页面顶部
            await page.evaluate('window.scrollTo(0, 0)')
            await asyncio.sleep(1)

            # 恢复图片加载，用于截图和下载
            await page.route("**/*.{png,jpg,jpeg,gif,webp}", lambda route: route.continue_())
            await asyncio.sleep(2)

            # 保存页面截图
            screenshot_path = os.path.join(output_dir, 'page_screenshot.png')
            print(f"📸 保存页面截图...")
            try:
                await page.screenshot(
                    path=screenshot_path,
                    full_page=True,
                    timeout=180000
                )
            except Exception as e:
                print(f"⚠️ 页面截图失败: {e}，跳过截图继续提取内容")

            # 提取今日头条内容
            print("🔍 提取今日头条内容...")
            content_data = await extract_toutiao_content(page)

            # 下载图片
            print(f"🖼️  开始下载 {len(content_data['images'])} 张图片...")
            content_data['images'] = await download_images(page, content_data['images'], output_dir)

            # 组织结果
            result = [{
                'title': content_data['title'],
                'content': content_data['content'],
                'url': page.url,
                'images': content_data['images'],
                'created_at': content_data['created_at'],
                'author': content_data['author'],
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

            print(f"📝 提取标题: {content_data['title'][:50]}..." if len(content_data['title']) > 50 else f"📝 提取标题: {content_data['title']}")
            print(f"📄 提取正文完成，共 {len(content_data['content'])} 字符")
            print(f"🖼️  成功下载 {len([img for img in content_data['images'] if img['local_path']])} 张图片")

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
