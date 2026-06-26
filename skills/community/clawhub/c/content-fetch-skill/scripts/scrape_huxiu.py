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


async def extract_huxiu_content(page: Page) -> Dict:
    """提取虎嗅文章内容"""
    result = {}

    # 提取标题
    try:
        title_elem = page.locator('.t-article-title').first
        if await title_elem.count() == 0:
            title_elem = page.locator('h1.article-title').first
        if await title_elem.count() > 0:
            title = await title_elem.text_content(timeout=2000)
            result['title'] = clean_text(title)
        else:
            # 兜底用页面标题，去掉后缀
            title = await page.title()
            result['title'] = clean_text(title.replace('-虎嗅网', '').strip())
    except:
        title = await page.title()
        result['title'] = clean_text(title.replace('-虎嗅网', '').strip())

    # 提取作者
    try:
        author_elem = page.locator('.article-author .name').first
        if await author_elem.count() == 0:
            author_elem = page.locator('.author-name').first
        if await author_elem.count() == 0:
            author_elem = page.locator('.article-meta__author').first
        author = await author_elem.text_content(timeout=2000)
        result['author'] = clean_text(author)
    except:
        result['author'] = ''

    # 提取发布时间
    try:
        time_elem = page.locator('.article-time').first
        if await time_elem.count() == 0:
            time_elem = page.locator('.publish-time').first
        if await time_elem.count() == 0:
            time_elem = page.locator('.article-meta__time').first
        if await time_elem.count() == 0:
            time_elem = page.locator('.article-info .time').first
        time_str = await time_elem.text_content(timeout=2000)
        # 提取时间格式
        time_match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}', time_str)
        if time_match:
            time_str = time_match.group()
        # 也支持"2026年05月02日"格式
        time_match2 = re.search(r'(\d{4})年(\d{2})月(\d{2})日', time_str)
        if time_match2:
            time_str = f"{time_match2.group(1)}-{time_match2.group(2)}-{time_match2.group(3)}"
        result['created_at'] = clean_text(time_str)
    except:
        result['created_at'] = ''

    # 提取正文
    try:
        # 虎嗅正文容器选择器，按优先级排序
        content_selectors = [
            '.article-detail-content',
            '#article_content',
            '.article-main-content',
            '.article-content',
            '.article-body'
        ]
        content_elem = None
        for selector in content_selectors:
            try:
                elem = page.locator(selector).first
                if await elem.count() > 0:
                    # 检查元素是否有足够的内容，避免选到空元素
                    text = await elem.text_content(timeout=2000)
                    cleaned_text = clean_text(text)
                    if cleaned_text and len(cleaned_text) > 50:
                        content_elem = elem
                        break
            except Exception as e:
                print(f"⚠️ 尝试选择器 {selector} 失败: {e}")
                continue

        if not content_elem:
            # 最后兜底，提取body里所有内容
            content_elem = page.locator('body').first

        # 移除无用元素 - 虎嗅页面特殊元素
        await content_elem.evaluate('''
            element => {
                const uselessSelectors = [
                    // 虎嗅特有无关元素
                    '.more-content', '.article-tag', '.relate-article',
                    '.comment-section', '.author-bio', '.recommend-box',
                    '.hot-list', '.ad-box', '.article-footer-action',
                    '.copyright-info', '.share-wrap', '.like-wrap',
                    '.article-append', '.article-related', '.wx-share-box',
                    // 通用无关元素
                    '.article-extra', '.related-articles', '.ad-wrapper', '.comment-box',
                    '.recommend-list', '.copyright', '.article-footer', '.author-info',
                    '.share-box', '.like-box', '.tag-list', '.article-meta',
                    '.login-tip', '.popup', '.advertisement'
                ];
                uselessSelectors.forEach(selector => {
                    element.querySelectorAll(selector).forEach(el => el.remove());
                });

                // 展开所有折叠内容
                const foldBtns = element.querySelectorAll('.fold-btn, .show-more, .js-unfold');
                foldBtns.forEach(btn => {
                    if (btn.offsetParent !== null && btn.style.display !== 'none') {
                        btn.click();
                    }
                });
            }
        ''')

        await asyncio.sleep(1)

        # 更精准的提取方式：直接提取所有段落文本
        paragraphs = []
        p_elements = await content_elem.locator('p').all()
        for p in p_elements:
            try:
                text = await p.text_content(timeout=1000)
                cleaned_text = clean_text(text)
                if cleaned_text and len(cleaned_text) > 10:  # 过滤太短的无效段落
                    paragraphs.append(cleaned_text)
            except:
                continue

        # 如果提取到的段落足够多，就拼接它们
        if len(paragraphs) > 3:
            cleaned_content = ' '.join(paragraphs)
        else:
            # 降级到原来的提取方式
            content = await content_elem.text_content(timeout=5000)
            cleaned_content = clean_text(content)
            # 如果内容还是太短，尝试直接用innerText
            if len(cleaned_content) < 100:
                content = await content_elem.evaluate('element => element.innerText')
                cleaned_content = clean_text(content)

        # 第一步：清理开头的无关导航内容
        # 查找正文开始的位置，通常是在发布时间/作者信息之后
        start_markers = [
            # 匹配发布时间后面的位置，格式如"2026-05-02 12:16"
            r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}',
            # 匹配作者信息后面
            r'本文来自微信公众号',
            r'作者：',
            # 匹配标题后面的内容，标题就是当前文章的标题
            re.escape(result['title']) if 'title' in result else None
        ]

        start_pos = 0
        for marker in start_markers:
            if not marker:
                continue
            matches = list(re.finditer(marker, cleaned_content))
            if matches:
                # 取最后一个匹配的位置，因为标题可能在开头出现多次
                last_match = matches[-1]
                start_pos = last_match.end()
                break

        # 如果找到了开始位置，就从那里开始截取
        if start_pos > 0 and start_pos < len(cleaned_content) // 2:
            cleaned_content = cleaned_content[start_pos:].lstrip()

        # 第二步：清理JSON代码片段
        # 移除类似{"key":value}的JSON结构，这些通常是页面配置
        cleaned_content = re.sub(r'\{[^{}]*"[a-zA-Z0-9_]+":.*?\}', '', cleaned_content)
        # 移除数组结构
        cleaned_content = re.sub(r'\[[^\[\]]*"[a-zA-Z0-9_]+".*?\]', '', cleaned_content)

        # 第三步：清理末尾的无关内容
        end_pos = len(cleaned_content)
        # 先查找正文正常结束的位置
        end_markers = [
            r'本文来自微信公众号',
            r'本内容未经允许不得转载',
            r'正在改变与想要改变世界的人，都在虎嗅APP',
            r'©虎嗅网',
            r'责任编辑：',
            r'相关文章',
            r'热门推荐',
            r'评论\(\d+\)',
            r'大家都在看'
        ]

        for marker in end_markers:
            match = re.search(marker, cleaned_content)
            if match and match.start() < end_pos and match.start() > len(cleaned_content) // 2:
                end_pos = match.start()
                break

        # 如果没有找到明确的结束标记，再查找SVG/JS代码的开始位置
        if end_pos == len(cleaned_content):
            code_patterns = [
                r'#icon-',  # SVG图标定义开始
                r'window\.',  # JS代码开始
                r'dataLayer',  # 统计代码
                r'gtag\(',  # 谷歌统计代码
                r'var [a-zA-Z0-9_]+ = ',  # JS变量定义
                r'function [a-zA-Z0-9_]+\(',  # JS函数定义
            ]
            for pattern in code_patterns:
                # 只在最后3000字符中查找，避免误判正文内容
                if len(cleaned_content) > 3000:
                    search_range = cleaned_content[-3000:]
                    match = re.search(pattern, search_range)
                    if match:
                        pos = len(cleaned_content) - 3000 + match.start()
                        if pos < end_pos and pos > len(cleaned_content) // 2:
                            end_pos = pos

        # 截断内容
        if end_pos < len(cleaned_content):
            cleaned_content = cleaned_content[:end_pos].rstrip()

        # 移除可能残留的代码片段
        cleaned_content = re.sub(r'#icon-[a-z0-9_-]+[^{]*\{[^}]*\}', '', cleaned_content)  # 移除CSS图标定义
        cleaned_content = re.sub(r'\.[a-zA-Z0-9_-]+\s*\{[^}]*\}', '', cleaned_content)  # 移除其他CSS
        cleaned_content = re.sub(r'\s+', ' ', cleaned_content).strip()  # 清理多余空格

        # 最后确保内容长度合理，如果太短可能是截断出问题了，就回退到清理前的内容
        if len(cleaned_content) < 500 and len(content) > 2000:
            cleaned_content = clean_text(content)

        result['content'] = cleaned_content
    except Exception as e:
        print(f"⚠️ 内容提取失败: {e}")
        result['content'] = '提取内容失败'

    # 提取图片 - 仅提取正文内的图片
    images = []
    try:
        # 触发懒加载，仅触发正文内的图片
        await page.evaluate('''
            document.querySelectorAll('.article-detail-content img, #article_content img').forEach(img => {
                if (img.dataset.src && !img.src) {
                    img.src = img.dataset.src;
                }
                if (img.dataset.original && !img.src) {
                    img.src = img.dataset.original;
                }
                if (img.lazy && !img.src && img.getAttribute('data-src')) {
                    img.src = img.getAttribute('data-src');
                }
            });
        ''')
        await asyncio.sleep(2)

        # 仅从正文区域找图片
        img_selectors = [
            '.article-detail-content .content img',
            '#article_content .content img',
            '.article-detail-content img',
            '#article_content img'
        ]
        img_elements = []
        for selector in img_selectors:
            try:
                imgs = await page.locator(selector).all()
                img_elements.extend(imgs)
            except:
                continue

        for img in img_elements:
            try:
                src = await img.get_attribute('src', timeout=1000)
                if not src:
                    src = await img.get_attribute('data-src', timeout=1000)
                if not src:
                    src = await img.get_attribute('data-original', timeout=1000)
                if not src:
                    continue

                # 跳过base64和小占位图、广告图
                if src.startswith('data:') or 'placeholder' in src or 'loading' in src or 'advert' in src.lower() or 'ad.' in src:
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
    except Exception as e:
        print(f"⚠️ 图片提取失败: {e}")
        pass

    # 去重图片
    unique_images = []
    seen_urls = set()
    for img in images:
        if img['url'] not in seen_urls:
            seen_urls.add(img['url'])
            unique_images.append(img)
    result['images'] = unique_images
    return result


async def download_images(page: Page, images: List[Dict], output_dir: str) -> List[Dict]:
    """下载图片到本地"""
    images_dir = os.path.join(output_dir, 'images')
    os.makedirs(images_dir, exist_ok=True)

    # 设置防盗链头
    await page.set_extra_http_headers({
        'Referer': 'https://www.huxiu.com/'
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
    """虎嗅文章爬取任务"""
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
                    'Referer': 'https://www.huxiu.com/',
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
                window.chrome = {
                    runtime: {}
                };
            ''')

            # 创建页面
            page = await context.new_page()

            # 拦截不需要的资源
            await page.route("**/*.{png,jpg,jpeg,gif,webp,css,woff,woff2,ico}", lambda route: route.abort() if route.request.resource_type == 'stylesheet' or route.request.resource_type == 'font' else route.continue_())

            # 访问目标页面
            print(f"🌍 访问目标页面: {url}")
            response: Optional[Response] = await page.goto(url, timeout=60000, wait_until='domcontentloaded')

            if not response or not response.ok:
                status_code = response.status if response else 'N/A'
                raise Exception(f"页面访问失败，状态码: {status_code}")

            print(f"✅ 页面加载完成，当前URL: {page.url}")

            # 处理登录弹窗
            try:
                close_btn = page.locator('.modal-header .close, .login-modal .close-btn').first
                if await close_btn.count() > 0:
                    await close_btn.click(timeout=2000)
                    print("🔒 已自动关闭登录弹窗")
                    await asyncio.sleep(1)
            except:
                pass

            # 等待页面稳定
            await asyncio.sleep(2)

            # 滚动页面加载完整内容
            print("🔄 滚动页面加载完整内容...")
            previous_height = 0
            for _ in range(6):
                current_height = await page.evaluate('document.body.scrollHeight')
                if current_height == previous_height:
                    break
                previous_height = current_height
                await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                await asyncio.sleep(1)

            # 回到页面顶部
            await page.evaluate('window.scrollTo(0, 0)')
            await asyncio.sleep(0.5)

            # 恢复图片加载
            await page.route("**/*.{png,jpg,jpeg,gif,webp}", lambda route: route.continue_())
            await asyncio.sleep(2)

            # 保存页面截图
            screenshot_path = os.path.join(output_dir, 'page_screenshot.png')
            print(f"📸 保存页面截图...")
            await page.screenshot(
                path=screenshot_path,
                full_page=True,
                timeout=120000
            )

            # 提取虎嗅内容
            print("🔍 提取虎嗅文章内容...")
            content_data = await extract_huxiu_content(page)

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
