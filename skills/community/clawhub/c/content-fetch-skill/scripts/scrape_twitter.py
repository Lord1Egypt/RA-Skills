#!/usr/bin/env python3
"""
Twitter/X.com 推文抓取脚本

使用方法:
    python3 scrape_twitter.py --proxy http://127.0.0.1:7890 --username <user> --password <pass> --target <target_user>

依赖:
    pip install playwright
    playwright install chromium
"""

import asyncio
import argparse
import json
import os
import re
from datetime import datetime
from typing import Optional
from playwright.async_api import async_playwright

class TwitterScraper:
    def __init__(self, proxy: str, email: str = None):
        self.proxy = proxy
        self.email = email
        self.tweets = []
        self.output_dir = '.'  # 默认输出目录为当前目录
        
    async def scrape(self, target_user: Optional[str] = None, scroll_count: int = 15, tweet_url: Optional[str] = None, session_file: str = './x_session.json', headless: bool = False, debug_port: str = '', cookies_file: str = '') -> list:
        """
        抓取推文
        如果提供tweet_url，则抓取单条指定推文；否则抓取target_user的主页所有推文

        Args:
            target_user: 目标用户名 (不含@)，不指定tweet_url时必填
            scroll_count: 滚动次数，默认15次，仅对用户主页抓取有效
            tweet_url: 单条推文的完整URL，指定后将忽略target_user和scroll_count
            session_file: 会话文件路径，用于保存和加载登录状态
            headless: 是否使用无头模式运行浏览器

        Returns:
            推文列表
        """
        print(f"🌐 启动浏览器...")
        if debug_port:
            print(f"🔌 连接到已运行的Chrome浏览器，调试端口: {debug_port}")
            print(f"💡 请确保Chrome已经打开并已登录X账号，且已开启远程调试")
        else:
            print(f"💡 会话文件: {session_file}")
            if not headless:
                print(f"💡 浏览器窗口已打开，请手动完成登录操作（如果需要）")

        async with async_playwright() as p:
            browser = None
            context = None
            page = None

            if debug_port:
                # 连接到已运行的Chrome浏览器
                try:
                    browser = await p.chromium.connect_over_cdp(f'http://127.0.0.1:{debug_port}')
                    # 获取默认上下文
                    context = browser.contexts[0]
                    # 新建页面或者使用现有页面
                    page = await context.new_page()
                    print("✅ 成功连接到已运行的Chrome浏览器")
                except Exception as e:
                    print(f"❌ 连接Chrome失败: {e}")
                    print("💡 请先按照以下步骤开启Chrome远程调试:")
                    print("1. 完全关闭Chrome浏览器")
                    print("2. 打开终端，运行:")
                    print("   /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port=9222")
                    print("3. 在打开的Chrome中登录X账号，然后重新运行脚本")
                    return []
            else:
                # 正常启动新的浏览器实例，增加反检测配置
                launch_kwargs = {
                    'headless': headless,
                    'args': [
                        '--disable-blink-features=AutomationControlled',  # 禁用自动化标识
                        '--start-maximized',  # 最大化窗口
                        '--disable-extensions',  # 禁用扩展
                        '--disable-notifications',  # 禁用通知
                        '--disable-infobars',  # 禁用信息栏
                        '--disable-dev-shm-usage',  # 解决资源限制问题
                        '--no-sandbox',  # 禁用沙箱
                        '--disable-gpu',  # 禁用GPU加速
                        '--ignore-certificate-errors',  # 忽略证书错误
                        '--allow-running-insecure-content',  # 允许加载不安全内容
                        '--disable-web-security',  # 禁用Web安全策略
                        '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
                    ]
                }
                # 只有代理不为空的时候才添加代理配置
                if self.proxy:
                    launch_kwargs['proxy'] = {'server': self.proxy}

                browser = await p.chromium.launch(**launch_kwargs)

                # 加载已保存的会话或Cookie
                context_kwargs = {
                    'viewport': {'width': 1280, 'height': 900},
                    'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
                    'locale': 'zh-CN,zh;q=0.9,en;q=0.8'
                }

                # 优先加载Cookie文件
                playwright_cookies = None
                if cookies_file and os.path.exists(cookies_file):
                    try:
                        with open(cookies_file, 'r', encoding='utf-8') as f:
                            cookies = json.load(f)
                            # 转换为Playwright兼容的Cookie格式
                            playwright_cookies = []
                            for cookie in cookies:
                                # 跳过无效Cookie
                                if not cookie.get('name') or not cookie.get('value'):
                                    continue
                                # 构建标准Cookie字段
                                pc = {
                                    'name': cookie['name'],
                                    'value': cookie['value'],
                                    'domain': cookie.get('domain', '.x.com'),
                                    'path': cookie.get('path', '/'),
                                    'secure': cookie.get('secure', True),
                                    'httpOnly': cookie.get('httpOnly', False),
                                }
                                # 处理过期时间
                                if 'expirationDate' in cookie and cookie['expirationDate']:
                                    pc['expires'] = int(cookie['expirationDate'])
                                # 处理sameSite
                                valid_same_site = {'Strict', 'Lax', 'None'}
                                if 'sameSite' in cookie and cookie['sameSite']:
                                    # EditThisCookie导出的sameSite可能是数字，转换为字符串
                                    same_site_map = {0: 'Lax', 1: 'Strict', 2: 'None'}
                                    samesite = same_site_map.get(cookie['sameSite'], str(cookie['sameSite']))
                                    # 只保留合法值，否则默认Lax
                                    if samesite in valid_same_site:
                                        pc['sameSite'] = samesite
                                    else:
                                        pc['sameSite'] = 'Lax'
                                else:
                                    # 没有sameSite字段，默认Lax
                                    pc['sameSite'] = 'Lax'
                                playwright_cookies.append(pc)
                            print(f"✅ 加载Cookie文件成功，共 {len(playwright_cookies)} 个Cookie")
                    except Exception as e:
                        print(f"⚠️ 加载Cookie失败: {e}，将尝试加载会话文件")
                # 没有Cookie文件则尝试加载会话文件
                elif os.path.exists(session_file):
                    try:
                        with open(session_file, 'r', encoding='utf-8') as f:
                            storage_state = json.load(f)
                            context_kwargs['storage_state'] = storage_state
                            print(f"✅ 加载已保存的会话状态")
                    except Exception as e:
                        print(f"⚠️ 加载会话失败: {e}，将使用全新会话")

                context = await browser.new_context(**context_kwargs)

                # 如果有Cookie，添加到上下文
                if playwright_cookies:
                    try:
                        await context.add_cookies(playwright_cookies)
                        print(f"✅ Cookie已成功添加到浏览器上下文")
                    except Exception as e:
                        print(f"⚠️ 添加Cookie失败: {e}")

                page = await context.new_page()

                # 反检测：修改webdriver属性，去掉自动化标识
                await page.add_init_script("""
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                    // 伪装其他浏览器特征
                    Object.defineProperty(navigator, 'plugins', {
                        get: () => [1, 2, 3]
                    });
                    Object.defineProperty(navigator, 'languages', {
                        get: () => ['zh-CN', 'zh', 'en']
                    });
                    // 禁用webdriver检测
                    window.navigator.chrome = {
                        runtime: {}
                    };
                """)

                # 跳过登录检测，直接访问目标页面（Cookie已经注入，会自动带上）
                print("💡 跳过登录检测，直接访问目标页面")
            
            # 访问目标URL
            if tweet_url:
                # 先访问页面，再判断类型
                print(f"🌍 访问目标页面: {tweet_url}")
                # 改为等待页面完全加载，包括所有资源
                await page.goto(tweet_url, wait_until='load', timeout=120000)
                await asyncio.sleep(20)
                # 滚动加载完整内容
                for i in range(3):
                    await page.evaluate('window.scrollBy(0, window.innerHeight/2)')
                    await asyncio.sleep(2)
                await page.evaluate('window.scrollTo(0, 0)')
                await asyncio.sleep(2)

                current_url = page.url
                print(f"  当前页面URL: {current_url}")

                # 检查是不是文章页面
                is_article = await page.evaluate('''() => {
                    // 更宽松的判断：包含/article/、有article元素、或者内容长度特别长都认为是长文
                    const hasArticleUrl = window.location.pathname.includes('/article/');
                    const hasArticleElement = document.querySelector('div[data-testid="article"], article') !== null;
                    const hasLongContent = document.body.innerText.length > 5000;
                    const hasArticleMarker = document.body.innerText.includes('Article written by') ||
                                            document.body.innerText.includes('文章作者') ||
                                            document.body.innerText.includes('Want to publish your own Article?');
                    return hasArticleUrl || hasArticleElement || hasLongContent || hasArticleMarker;
                }''')
                print(f"  检测是否为文章: {is_article}")

                # 处理长文(Article)类型
                if is_article or '/i/article/' in current_url:
                    # 处理长文(Article)类型
                    print(f"📄 检测到是X长文，用文章逻辑提取")

                    # 截图保存当前页面，方便调试
                    article_screenshot = os.path.join(self.output_dir, 'article_page.png')
                    await page.screenshot(path=article_screenshot, full_page=True, timeout=120000)  # 延长到2分钟超时
                    print(f"  已保存页面截图到 {article_screenshot}")

                    # 等待文章内容加载
                    print("  等待文章内容加载...")
                    try:
                        await page.wait_for_selector('div[data-testid="article"], article, div[data-testid="tweetText"]', timeout=15000)
                        await asyncio.sleep(2)
                    except:
                        print("  未找到标准文章容器，尝试直接提取内容")

                    # 提取文章内容
                    article_data = await self._parse_article(page)
                    if article_data:
                        self.tweets.append(article_data)
                        print(f"  成功抓取文章: {article_data.get('title', '无标题')}")

                    print(f"\n✅ 共获取 {len(self.tweets)} 篇文章")
                else:
                    # 处理普通推文
                    print(f"📱 检测到是普通推文，用推文逻辑提取")

                    # 截图保存当前页面，方便调试
                    tweet_screenshot = os.path.join(self.output_dir, 'tweet_page.png')
                    await page.screenshot(path=tweet_screenshot, full_page=True, timeout=120000)  # 延长到2分钟超时
                    print(f"  已保存页面截图到 {tweet_screenshot}")

                    # 检查是否是登录页
                    page_content = await page.content()
                    if 'Sign in to X' in page_content or '登录' in page_content:
                        print(f"  ⚠️ 页面是登录页，Cookie无效，请重新导出Cookie")

                    # 提取目标推文ID，用于匹配
                    target_tweet_id = tweet_url.split('/status/')[-1].split('/')[0].split('?')[0]

                    # 先尝试用标准选择器提取
                    elements = []
                    try:
                        await page.wait_for_selector('article[data-testid="tweet"]', timeout=30000)  # 30秒等待
                        await asyncio.sleep(2)
                    except Exception as e:
                        print(f"  等待推文元素超时，尝试直接提取: {e}")

                    # 无论是否超时，都尝试查找推文元素
                    elements = await page.query_selector_all('article[data-testid="tweet"]')
                    print(f"  找到 {len(elements)} 个推文元素")

                    for el in elements:
                        try:
                            # 点击"显示更多"展开完整内容
                            await self._expand_tweet(el)

                            tweet = await self._parse_tweet(el)
                            if tweet:
                                # 只保留ID匹配的目标推文，过滤掉相关推文、回复等
                                if tweet['id'] == target_tweet_id and not any(t['id'] == tweet['id'] for t in self.tweets):
                                    self.tweets.append(tweet)
                                    print(f"  成功匹配目标推文 ID: {tweet['id']}")
                        except Exception as e:
                            print(f"  解析单个推文元素出错: {e}")
                            continue

                    # 如果标准提取失败，用智能提取模式（和长文一样的逻辑）
                    if not self.tweets:
                        print("  启动智能提取模式...")
                        # 滚动一下加载完整内容
                        await page.evaluate('window.scrollTo(0, 0)')
                        await asyncio.sleep(1)

                        # 智能提取正文区域
                        content_info = await page.evaluate('''() => {
                            const fullText = document.body.innerText;
                            const lines = fullText.split('\\n').map(line => line.trim()).filter(line => line);

                            // 要过滤的导航关键词
                            const navKeywords = ['Home', 'Explore', 'Notifications', 'Chat', 'Grok', 'Bookmarks', 'Creator Studio', 'Profile', 'Premium', 'Post', 'keyboard shortcuts', 'View keyboard shortcuts', 'More'];
                            const spamKeywords = ['Relevant people', 'Who to follow', 'Trending', 'People also follow', 'Topics to follow', 'Sign in', '登录', 'ruichong', '@ruichong2'];

                            // 直接过滤所有包含导航关键词和垃圾关键词的行
                            const filteredLines = lines.filter(line => {
                                // 只要包含任何导航关键词或者垃圾关键词，就过滤掉，除非行很长（可能是正文包含了这些词）
                                const hasNavKeyword = navKeywords.some(keyword => line.includes(keyword));
                                const hasSpamKeyword = spamKeywords.some(keyword => line.includes(keyword));
                                if ((hasNavKeyword || hasSpamKeyword) && line.length < 50) {
                                    return false;
                                }
                                return line.length > 3;
                            });

                            // 去重
                            const uniqueLines = [];
                            const seen = new Set();
                            for (const line of filteredLines) {
                                if (!seen.has(line)) {
                                    uniqueLines.push(line);
                                    seen.add(line);
                                }
                            }

                            // 提取标题：找到第一个长度大于15的有效行作为标题（排除短的导航词）
                            let title = '';
                            let contentLines = uniqueLines;
                            for (let i = 0; i < uniqueLines.length; i++) {
                                const line = uniqueLines[i];
                                if (line.length > 15) {
                                    title = line;
                                    // 从正文中去掉标题行，避免重复
                                    contentLines = uniqueLines.slice(i + 1);
                                    break;
                                }
                            }

                            return {
                                content: contentLines.join('\\n\\n'),
                                title: title
                            };
                        }''')

                        content = content_info.get('content', '').strip()
                        title = content_info.get('title', '').strip()

                        # 提取发布时间
                        created_at = ''
                        time_el = await page.query_selector('time')
                        if time_el:
                            created_at = await time_el.get_attribute('datetime') or ''

                        # 提取互动数据
                        like_count = await self._get_count(page, 'like')
                        retweet_count = await self._get_count(page, 'retweet')
                        reply_count = await self._get_count(page, 'reply')

                        # 提取推文中的图片（支持长文所有类型的图片，处理懒加载）
                        images = []
                        # 滚动页面触发所有图片懒加载
                        await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                        await asyncio.sleep(2)
                        await page.evaluate('window.scrollTo(0, 0)')
                        await asyncio.sleep(1)
                        # 查找页面中所有图片
                        img_els = await page.query_selector_all('img')
                        # 去重处理，同时处理懒加载的data-src属性
                        seen_src = set()
                        for img in img_els:
                            try:
                                # 优先获取真实src，没有的话找懒加载的data-src
                                src = await img.get_attribute('src') or await img.get_attribute('data-src') or await img.get_attribute('data-url')
                                if src and src not in seen_src:
                                    # 过滤掉图标、头像、emoji等非内容图片
                                    if not src.endswith('.svg') and 'profile_images' not in src and 'emoji' not in src and 'icon' not in src and 'placeholder' not in src and 'loading.gif' not in src:
                                        # 只保留pbs.twimg.com域名下的真实推文图片
                                        if 'pbs.twimg.com' in src or 'twimg.com' in src:
                                            images.append(src)
                                            seen_src.add(src)
                            except Exception:
                                continue

                        # 清理内容
                        if content:
                            # 按段落分割去重
                            paragraphs = content.split('\n\n')
                            filtered_paragraphs = []
                            seen = set()
                            for para in paragraphs:
                                stripped_para = para.strip()
                                if stripped_para and len(stripped_para) > 5 and stripped_para not in seen:
                                    # 过滤无关内容
                                    if not any(k in stripped_para for k in ['·', '回复', '转发', '喜欢', 'Reply', 'Retweet', 'Like', 'Share', 'Article']):
                                        filtered_paragraphs.append(stripped_para)
                                        seen.add(stripped_para)
                            content = '\n\n'.join(filtered_paragraphs)

                        # 生成标题：取content前30个字符，没有的话就是"图片推文"
                        if not title:
                            title = content[:30].strip() if content else "图片推文"
                            if len(content) > 30:
                                title += "..."

                        # 内容就是纯文本，不再追加图片标签

                        if content or images:
                            self.tweets.append({
                                'id': target_tweet_id,
                                'type': 'tweet',
                                'title': title,
                                'created_at': created_at,
                                'content': content,
                                'images': images,
                                'url': tweet_url,
                                'like_count': like_count,
                                'retweet_count': retweet_count,
                                'reply_count': reply_count
                            })
                            print(f"  智能提取成功，推文 ID: {target_tweet_id}")

                    print(f"\n✅ 共获取 {len(self.tweets)} 条推文")
            else:
                target_url = f'https://x.com/{target_user}'
                print(f"📱 访问用户主页: {target_url}")
                await page.goto(target_url, wait_until='domcontentloaded', timeout=60000)
                await asyncio.sleep(3)

                # 抓取推文
                await self._fetch_tweets(page, scroll_count)
            
            await browser.close()
            
        return self.tweets
    
    async def _login(self, page):
        """登录 Twitter - 已废弃，请使用Cookie登录"""
        print("❌ 用户名密码登录已废弃，请使用Cookie文件登录")
        print("💡 请导出您的X.com Cookie为JSON文件，使用--cookies参数指定")
        raise Exception("用户名密码登录已废弃，请使用Cookie登录")
    
    async def _try_click_saved_account(self, page) -> bool:
        """尝试点击已保存的账户 - 已废弃"""
        return False
    
    async def _find_input(self, page, selectors: list):
        """查找输入框"""
        for sel in selectors:
            try:
                el = await page.wait_for_selector(sel, timeout=3000)
                if el:
                    return el
            except:
                continue
        return None
    
    async def _fetch_tweets(self, page, scroll_count: int):
        """抓取推文"""
        print(f"\n📜 开始抓取 (滚动 {scroll_count} 次)...")
        
        for i in range(scroll_count):
            elements = await page.query_selector_all('article[data-testid="tweet"]')
            
            for el in elements:
                try:
                    # 点击"显示更多"展开完整内容
                    await self._expand_tweet(el)
                    
                    tweet = await self._parse_tweet(el)
                    if tweet and not any(t['id'] == tweet['id'] for t in self.tweets):
                        self.tweets.append(tweet)
                except:
                    continue
            
            await page.evaluate('window.scrollBy(0, 1000)')
            await asyncio.sleep(2)
            print(f"  已获取 {len(self.tweets)} 条推文...")
        
        # 按时间排序
        self.tweets.sort(key=lambda x: x['created_at'], reverse=True)
        print(f"\n✅ 共获取 {len(self.tweets)} 条推文")
    
    async def _expand_tweet(self, el):
        """点击"显示更多"展开推文完整内容"""
        try:
            # 多种可能的选择器
            selectors = [
                'div[role="button"]',
                'span',
                'button'
            ]
            
            for sel in selectors:
                buttons = await el.query_selector_all(sel)
                for btn in buttons:
                    try:
                        text = await btn.inner_text()
                        text_lower = text.lower().strip()
                        # 匹配多种语言的"显示更多"
                        if any(kw in text_lower for kw in ['显示更多', 'show more', '阅读更多', 'read more', '展开', 'expand']):
                            print(f"    点击展开: {text[:20]}...")
                            await btn.click()
                            await asyncio.sleep(1)  # 等待内容展开
                            return
                    except:
                        continue
        except Exception as e:
            pass
    
    async def _parse_tweet(self, el) -> dict:
        """解析单条推文"""
        link = await el.query_selector('a[href*="/status/"]')
        if not link:
            return None

        href = await link.get_attribute('href')
        # 提取推文ID，去掉后面的路径参数
        tweet_id = href.split('/status/')[-1].split('/')[0].split('?')[0]

        # 首先获取整个推文的文本，用于提取标题部分
        full_text = await el.inner_text()
        lines = [line.strip() for line in full_text.split('\n') if line.strip()]

        # 提取可能的标题：跳过前两行（用户名和@id），寻找第一个长文本行（不是互动数据）
        possible_title = ''
        if len(lines) >= 3:
            for i in range(2, min(5, len(lines))):  # 检查前几行
                line = lines[i]
                # 检查是否是互动数据行
                is_interaction_line = False
                if line.replace('.', '', 1).replace('K', '', 1).replace('M', '', 1).isdigit():
                    is_interaction_line = True
                elif any(keyword in line for keyword in ['回复', '转发', '喜欢', 'Reply', 'Retweet', 'Like', 'share', 'Views', '查看', '查看翻译']):
                    is_interaction_line = True

                if not is_interaction_line and len(line) > 10:
                    possible_title = line
                    break

        # 优先使用官方tweetText选择器获取正文内容
        text = ''
        text_el = await el.query_selector('[data-testid="tweetText"]')
        if text_el:
            text = await text_el.inner_text().strip()

        # 如果还是没获取到内容，再用备用方式过滤
        if not text:
            # 提取推文文本：更健壮的逻辑
            text_lines = []
            in_content = False
            time_found = False

            for i, line in enumerate(lines):
                # 先找时间行（包含·或者日期格式）
                if not time_found and ('·' in line or ('202' in line and len(line) < 20) or '年' in line or '月' in line or '日' in line or 'ago' in line):
                    time_found = True
                    in_content = True
                    continue

                # 检测互动数据行：纯数字，或者包含K/M等单位，或者是回复/转发/喜欢等关键词
                is_interaction_line = False
                # 纯数字或者带K/M的数字
                if line.replace('.', '', 1).replace('K', '', 1).replace('M', '', 1).isdigit():
                    is_interaction_line = True
                # 包含互动关键词
                elif any(keyword in line for keyword in ['回复', '转发', '喜欢', 'Reply', 'Retweet', 'Like', 'share', 'Views', '查看', '查看翻译']):
                    is_interaction_line = True

                # 如果已经找到时间行，遇到互动数据行就停止
                if in_content and is_interaction_line:
                    break

                # 如果已经找到时间行，后面的都是内容
                if in_content:
                    text_lines.append(line)

            # 如果还是没找到内容，说明时间行识别失败，尝试另一种方式
            if not text_lines:
                # 跳过前两行（用户名和@id）
                i = 2
                # 第一部分：收集标题/前言，直到遇到互动数据行
                while i < len(lines):
                    line = lines[i]
                    # 检测互动数据行
                    is_interaction_line = False
                    if line.replace('.', '', 1).replace('K', '', 1).replace('M', '', 1).isdigit():
                        is_interaction_line = True
                    elif any(keyword in line for keyword in ['回复', '转发', '喜欢', 'Reply', 'Retweet', 'Like', 'share', 'Views', '查看', '查看翻译']):
                        is_interaction_line = True

                    if is_interaction_line:
                        break

                    text_lines.append(line)
                    i += 1

                # 跳过所有连续的互动数据行
                while i < len(lines):
                    line = lines[i]
                    is_interaction_line = False
                    if line.replace('.', '', 1).replace('K', '', 1).replace('M', '', 1).isdigit():
                        is_interaction_line = True
                    elif any(keyword in line for keyword in ['回复', '转发', '喜欢', 'Reply', 'Retweet', 'Like', 'share', 'Views', '查看', '查看翻译']):
                        is_interaction_line = True

                    if not is_interaction_line:
                        break
                    i += 1

                # 第二部分：收集正文内容，直到遇到底部的互动按钮行
                while i < len(lines):
                    line = lines[i]
                    # 检测底部的互动按钮行
                    if any(keyword in line for keyword in ['回复', '转发', '喜欢', 'Reply', 'Retweet', 'Like', 'share', 'Views']):
                        break
                    text_lines.append(line)
                    i += 1

            text = '\n'.join(text_lines).strip()

        # 合并标题和正文（如果标题不在正文开头）
        if possible_title and text and not text.startswith(possible_title[:10]):
            text = possible_title + '\n\n' + text

        time_el = await el.query_selector('time')
        created_at = await time_el.get_attribute('datetime') if time_el else ''

        # 互动数据
        like_count = await self._get_count(el, 'like')
        retweet_count = await self._get_count(el, 'retweet')
        reply_count = await self._get_count(el, 'reply')

        # 提取推文中的图片（支持普通推文和长文的所有图片，处理懒加载）
        images = []
        # 先滚动页面触发所有图片懒加载
        await el.evaluate('element => element.scrollIntoView({behavior: "smooth", block: "center"})')
        await asyncio.sleep(2)
        # 1. 先在当前推文元素内找所有图片
        img_els = await el.query_selector_all('img')
        # 2. 再扩大范围到整个页面找所有可能的图片
        img_els += await el.page.query_selector_all('img')
        # 3. 去重处理，同时处理懒加载的data-src属性
        seen_src = set()
        for img in img_els:
            try:
                # 优先获取真实src，没有的话找懒加载的data-src
                src = await img.get_attribute('src') or await img.get_attribute('data-src') or await img.get_attribute('data-url')
                if src and src not in seen_src:
                    # 过滤掉图标、头像、emoji等非内容图片
                    if not src.endswith('.svg') and 'profile_images' not in src and 'emoji' not in src and 'icon' not in src and 'placeholder' not in src and 'loading.gif' not in src:
                        # 只保留pbs.twimg.com域名下的真实推文图片
                        if 'pbs.twimg.com' in src or 'twimg.com' in src:
                            images.append(src)
                            seen_src.add(src)
            except Exception:
                continue

        # 生成标题：优先取正文第一行，如果没有正文就是"图片推文"
        if text:
            # 取第一行作为标题
            first_line = text.split('\n')[0].strip()
            if first_line:
                title = first_line[:50].strip()  # 标题最多50个字符
                if len(first_line) > 50:
                    title += "..."
            else:
                # 如果第一行是空的，取前30个字符
                title = text[:30].strip()
                if len(text) > 30:
                    title += "..."
        else:
            title = "图片推文"

        # 内容就是纯文本，不再追加图片标签
        content = text

        return {
            'id': tweet_id,
            'type': 'tweet',
            'title': title,
            'created_at': created_at,
            'content': content,
            'images': images,
            'url': f"https://x.com/status/{tweet_id}",
            'like_count': like_count,
            'retweet_count': retweet_count,
            'reply_count': reply_count
        }
    
    async def _get_count(self, el, type_: str) -> int:
        """获取互动数"""
        btn = await el.query_selector(f'[data-testid="{type_}"]')
        if btn:
            aria = await btn.get_attribute('aria-label') or ''
            match = re.search(r'(\d+)', aria.replace(',', ''))
            if match:
                return int(match.group(1))
        return 0

    async def _parse_article(self, page) -> Optional[dict]:
        """解析X长文(Article)内容"""
        try:
            # 提取文章ID
            if '/article/' in page.url:
                article_id = page.url.split('/article/')[-1].split('?')[0]
            else:
                article_id = page.url.split('/status/')[-1].split('?')[0]

            # 滚动页面加载完整内容
            print("  滚动页面加载完整内容...")
            # 先滚动到顶部
            await page.evaluate('window.scrollTo(0, 0)')
            await asyncio.sleep(1)
            # 逐步滚动加载所有内容
            for i in range(5):
                await page.evaluate('window.scrollBy(0, window.innerHeight/2)')
                await asyncio.sleep(2)
            # 回到顶部
            await page.evaluate('window.scrollTo(0, 0)')
            await asyncio.sleep(1)

            # 提取页面所有文本，直接过滤导航部分
            print("  智能分析正文区域...")
            content_info = await page.evaluate('''() => {
                const fullText = document.body.innerText;
                const lines = fullText.split('\\n').map(line => line.trim()).filter(line => line);

                // 要过滤的导航关键词
                const navKeywords = ['Home', 'Explore', 'Notifications', 'Chat', 'Grok', 'Bookmarks', 'Creator Studio', 'Profile', 'Premium', 'Post', 'keyboard shortcuts', 'View keyboard shortcuts', 'More'];
                const spamKeywords = ['Relevant people', 'Who to follow', 'Trending', 'People also follow', 'Topics to follow', 'Sign in', '登录', 'ruichong', '@ruichong2'];

                // 直接过滤所有包含导航关键词和垃圾关键词的行
                const filteredLines = lines.filter(line => {
                    // 只要包含任何导航关键词或者垃圾关键词，就过滤掉，除非行很长（可能是正文包含了这些词）
                    const hasNavKeyword = navKeywords.some(keyword => line.includes(keyword));
                    const hasSpamKeyword = spamKeywords.some(keyword => line.includes(keyword));
                    if ((hasNavKeyword || hasSpamKeyword) && line.length < 50) {
                        return false;
                    }
                    return line.length > 3;
                });

                // 去重
                const uniqueLines = [];
                const seen = new Set();
                for (const line of filteredLines) {
                    if (!seen.has(line)) {
                        uniqueLines.push(line);
                        seen.add(line);
                    }
                }

                // 提取标题：找到第一个长度大于15的有效行作为标题（排除短的导航词）
                let title = '';
                let contentLines = uniqueLines;
                for (let i = 0; i < uniqueLines.length; i++) {
                    const line = uniqueLines[i];
                    if (line.length > 15) {
                        title = line;
                        // 从正文中去掉标题行，避免重复
                        contentLines = uniqueLines.slice(i + 1);
                        break;
                    }
                }

                return {
                    content: contentLines.join('\\n\\n'),
                    title: title
                };
            }''')

            content = content_info.get('content', '').strip()
            title = content_info.get('title', '').strip()

            # 尝试提取标题
            if not title:
                title_selectors = [
                    'h1[data-testid="articleTitle"]',
                    'h1.css-1dbjc4n.r-18jsvk2.r-16dba41',
                    'h1',
                    'div[role="heading"]'
                ]
                for selector in title_selectors:
                    title_el = await page.query_selector(selector)
                    if title_el:
                        title = await title_el.inner_text()
                        if title.strip():
                            break

            # 提取发布时间
            created_at = ''
            time_el = await page.query_selector('time')
            if time_el:
                created_at = await time_el.get_attribute('datetime') or ''

            # 提取互动数据
            like_count = await self._get_count(page, 'like')
            retweet_count = await self._get_count(page, 'retweet')
            reply_count = await self._get_count(page, 'reply')

            # 提取文章中的图片
            images = []
            img_els = await page.query_selector_all('img[data-testid="tweetPhoto"], article img')
            for img in img_els:
                src = await img.get_attribute('src')
                if src and not src.endswith('.svg') and 'profile_images' not in src:
                    images.append(src)

            # 清理内容，去除重复和无关行
            if content:
                # 先按段落分割
                paragraphs = content.split('\n\n')
                filtered_paragraphs = []
                seen_paras = set()
                seen_lines = set()

                # 无关段落的关键词
                irrelevant_keywords = [
                    'Live on X', 'Reuters', 'Al Jazeera', 'AajTak', 'Terms of Service',
                    'Privacy Policy', 'Cookie Policy', 'Accessibility', 'Ads info',
                    '© 2026 X Corp.', 'See new posts', 'Post your reply', 'Follow',
                    'Upgrade to Premium', 'Want to publish your own Article?',
                    'View quotes', 'Relevant', 'Strait of Hormuz', 'Ron DeSantis',
                    'Governor DeSantis', 'LIVE: AL JAZEERA', 'क्या फूटने वाला है'
                ]

                for para in paragraphs:
                    stripped_para = para.strip()
                    if not stripped_para or len(stripped_para) < 10:
                        continue

                    # 段落去重
                    if stripped_para in seen_paras:
                        continue

                    # 检查是否包含无关关键词
                    has_irrelevant = any(k in stripped_para for k in irrelevant_keywords)
                    if has_irrelevant:
                        continue

                    # 过滤掉全是非中文且非技术相关的段落（比如纯英文新闻、印地语内容）
                    chinese_chars = sum(1 for c in stripped_para if '一' <= c <= '鿿')
                    if chinese_chars < 5 and not any(c in stripped_para for c in ['Claude', 'OpenRouter', 'opencode', 'CLI', 'API', 'http', 'GPT']):
                        continue

                    filtered_paragraphs.append(stripped_para)
                    seen_paras.add(stripped_para)

                # 再处理段落内的行，过滤无关行和重复行
                final_content = []
                for para in filtered_paragraphs:
                    lines = para.split('\n')
                    processed_lines = []
                    for line in lines:
                        stripped = line.strip()
                        if stripped and len(stripped) > 5:
                            # 行去重
                            if stripped in seen_lines:
                                continue
                            # 过滤掉明显无关的行
                            if any(k in stripped for k in ['·', '回复', '转发', '喜欢', 'Reply', 'Retweet', 'Like', 'Share', 'Article']):
                                continue
                            processed_lines.append(stripped)
                            seen_lines.add(stripped)
                    if processed_lines:
                        final_content.append('\n'.join(processed_lines))

                content = '\n\n'.join(final_content).strip()

            # 内容就是纯文本，不再追加图片标签

            return {
                'id': article_id,
                'type': 'article',
                'title': title.strip(),
                'created_at': created_at,
                'content': content,
                'images': images,
                'url': page.url,
                'like_count': like_count,
                'retweet_count': retweet_count,
                'reply_count': reply_count
            }

        except Exception as e:
            print(f"  解析文章出错: {e}")
            return None


async def scrape_task(
    proxy: str,
    email: str = None,
    target: str = None,
    url: str = None,
    output: str = None,
    scroll: int = 15,
    session: str = './x_session.json',
    headless: bool = True,
    debug_port: str = '',
    cookies: str = '',
    output_dir: str = None
) -> list:
    """
    爬取任务核心函数，可被外部模块调用
    :param proxy: 代理地址
    :param email: 验证邮箱（可选）
    :param target: 目标用户名（和url二选一）
    :param url: 单条推文URL（和target二选一）
    :param output: 输出文件路径（可选）
    :param scroll: 滚动加载次数
    :param session: 会话文件路径
    :param headless: 是否无头模式
    :param debug_port: Chrome调试端口
    :param cookies: Cookie文件路径（必填）
    :param output_dir: 输出目录，用于保存截图等文件（可选）
    :return: 爬取结果列表
    """
    # 参数验证
    if not target and not url:
        raise ValueError("必须提供 target （目标用户名）或 url （单条推文URL）")

    # 如果指定了输出目录，创建目录
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # 设置默认输出路径
    if not output:
        default_output_dir = output_dir or os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'twitter_data')
        os.makedirs(default_output_dir, exist_ok=True)
        if url:
            if '/i/article/' in url:
                # 提取文章ID
                article_id = url.split('/article/')[-1].split('?')[0]
                output = os.path.join(default_output_dir, f'article_{article_id}.json')
            elif '/status/' in url:
                # 从URL中提取推文ID
                tweet_id = url.split('/status/')[-1].split('?')[0]
                output = os.path.join(default_output_dir, f'tweet_{tweet_id}.json')
            else:
                # 其他URL类型
                url_id = url.split('/')[-1].split('?')[0]
                output = os.path.join(default_output_dir, f'x_content_{url_id}.json')
        else:
            output = os.path.join(default_output_dir, f'tweets_{target}.json')

    scraper = TwitterScraper(
        proxy=proxy,
        email=email
    )

    # 如果指定了输出目录，设置截图保存路径
    if output_dir:
        scraper.output_dir = output_dir

    tweets = await scraper.scrape(
        target_user=target,
        scroll_count=scroll,
        tweet_url=url,
        session_file=session,
        headless=headless,
        debug_port=debug_port,
        cookies_file=cookies
    )

    # 如果指定了输出文件，保存结果
    if output:
        # 读取已有数据（如果存在）
        existing_tweets = []
        if os.path.exists(output):
            try:
                with open(output, 'r', encoding='utf-8') as f:
                    existing_tweets = json.load(f)
                    if not isinstance(existing_tweets, list):
                        existing_tweets = []
            except:
                existing_tweets = []

        # 合并推文（去重）
        existing_ids = {t['id'] for t in existing_tweets}
        new_tweets = [t for t in tweets if t['id'] not in existing_ids]
        all_tweets = existing_tweets + new_tweets

        # 按时间排序
        all_tweets.sort(key=lambda x: x['created_at'], reverse=True)

        # 保存结果
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(all_tweets, f, ensure_ascii=False, indent=2)

        print(f"\n💾 已保存到: {output}")
        print(f"   原有: {len(existing_tweets)} 条, 新增: {len(new_tweets)} 条, 合计: {len(all_tweets)} 条")

        # 显示摘要
        if tweets:
            print(f"\n📊 前5条内容:")
            for i, t in enumerate(tweets[:5], 1):
                date = t['created_at'][:10] if t.get('created_at') else 'N/A'
                print(f"\n[{i}] {date}")
                if t.get('type') == 'article':
                    # 文章类型
                    title = t.get('title', '无标题')
                    content = t.get('content', '')
                    print(f"    📄 {title[:60]}...")
                    if content:
                        print(f"    {content[:100].replace(chr(10), ' ')}...")
                else:
                    # 普通推文类型
                    text = t.get('text', '')
                    print(f"    {text[:60]}...")

    return tweets

async def main():
    parser = argparse.ArgumentParser(description='Twitter/X.com 推文抓取')
    parser.add_argument('--proxy', required=True, help='代理地址，如 http://127.0.0.1:7890')
    parser.add_argument('--email', help='验证邮箱 (可选)')
    parser.add_argument('--target', required=False, help='目标用户名，不指定--url时必填')
    parser.add_argument('--url', help='单条推文的URL，指定后将只抓取该推文，无需指定--target')
    parser.add_argument('--output', default='', help='输出文件 (默认: twitter_data 目录下的对应文件)')
    parser.add_argument('--scroll', type=int, default=15, help='滚动次数')
    parser.add_argument('--session', default='./x_session.json', help='会话文件路径，用于保存登录状态 (默认: ./x_session.json)')
    parser.add_argument('--headless', action='store_true', default=True, help='是否使用无头模式运行浏览器 (默认: 无头模式，后台静默运行)')
    parser.add_argument('--debug-port', default='', help='Chrome调试端口，用于连接已打开的Chrome浏览器 (例如: 9222)，使用此模式会跳过登录流程')
    parser.add_argument('--cookies', required=True, help='Cookie文件路径 (JSON格式)，用于直接导入登录状态')
    parser.add_argument('--output-dir', default=None, help='输出目录，用于保存截图等文件 (可选)')

    args = parser.parse_args()

    await scrape_task(
        proxy=args.proxy,
        email=args.email,
        target=args.target,
        url=args.url,
        output=args.output,
        scroll=args.scroll,
        session=args.session,
        headless=args.headless,
        debug_port=args.debug_port,
        cookies=args.cookies,
        output_dir=args.output_dir
    )


if __name__ == '__main__':
    asyncio.run(main())
