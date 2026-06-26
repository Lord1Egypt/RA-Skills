#!/usr/bin/env python3
"""
连接已运行的点点数据浏览器，获取指定平台上架榜单数据
使用 CDP (Chrome DevTools Protocol) 连接

使用方法:
    # 获取 App Store 中国区数据
    python tools/diandian_connect.py
    
    # 获取华为渠道数据
    python tools/diandian_connect.py --platform huawei
    
    # 获取小米渠道数据
    python tools/diandian_connect.py --platform xiaomi
"""

import asyncio
import yaml
import httpx
import argparse
import sys
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright

try:
    import pandas as pd
except ImportError:
    pd = None

SKILL_DIR = Path(__file__).parent.parent
CONFIG_DIR = SKILL_DIR / "config"
REPORTS_DIR = SKILL_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)


# 平台映射表
# 根据实际 URL 格式更新：
# - App Store: line-1-0-0-{region_id}-0-3-0
# - 安卓渠道：line-{platform_type}-0-0-75-0-3-0
#   platform_type: 2=华为，3=小米/其他安卓
PLATFORM_MAP = {
    # App Store 国家/地区
    'appstore': {'url': 'https://app.diandian.com/rank/line-1-0-0-75-0-3-0', 'name': 'App Store', 'type': 'direct'},
    'appstore_us': {'url': 'https://app.diandian.com/rank/line-1-0-0-72-0-3-0', 'name': 'App Store 美国', 'type': 'direct'},
    'appstore_jp': {'url': 'https://app.diandian.com/rank/line-1-0-0-81-0-3-0', 'name': 'App Store 日本', 'type': 'direct'},
    # 国内安卓渠道（去掉?upkind=1 参数，获取全部上架数据）
    # 安卓渠道 URL 格式：line-{channel_id}-0-0-75-0-3-0
    'huawei': {'url': 'https://app.diandian.com/rank/line-2-0-0-75-0-3-0', 'name': '华为', 'type': 'direct'},
    'xiaomi': {'url': 'https://app.diandian.com/rank/line-3-0-0-75-0-3-0', 'name': '小米', 'type': 'direct'},
    'vivo': {'url': 'https://app.diandian.com/rank/line-4-0-0-75-0-3-0', 'name': 'vivo', 'type': 'direct'},
    'oppo': {'url': 'https://app.diandian.com/rank/line-5-0-0-75-0-3-0', 'name': 'OPPO', 'type': 'direct'},
    'meizu': {'url': 'https://app.diandian.com/rank/line-6-0-0-75-0-3-0', 'name': '魅族', 'type': 'direct'},
    'tencent': {'url': 'https://app.diandian.com/rank/line-7-0-0-75-0-3-0', 'name': '应用宝', 'type': 'direct'},
    'baidu': {'url': 'https://app.diandian.com/rank/line-8-0-0-75-0-3-0', 'name': '百度', 'type': 'direct'},
    'qihoo360': {'url': 'https://app.diandian.com/rank/line-9-0-0-75-0-3-0', 'name': '360', 'type': 'direct'},
    'honor': {'url': 'https://app.diandian.com/rank/line-17-0-0-75-0-3-0', 'name': '荣耀', 'type': 'direct'},
    'harmony': {'url': 'https://app.diandian.com/rank/line-9999-0-0-75-0-3-0', 'name': '鸿蒙', 'type': 'direct'},
    'wandoujia': {'url': 'https://app.diandian.com/rank/line-10-0-0-75-0-3-0', 'name': '豌豆荚', 'type': 'direct'},
    # TapTap
    'taptap': {'url': 'https://app.diandian.com/rank/line-4-0-0-0-3-0', 'name': 'TapTap', 'type': 'direct'},
}


def load_dingtalk_config():
    """加载钉钉配置"""
    config_path = CONFIG_DIR / "dingtalk.yaml"
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    return {}


async def get_dingtalk_access_token(client_id: str, client_secret: str) -> str:
    """获取钉钉 access_token"""
    url = "https://oapi.dingtalk.com/gettoken"
    params = {"appkey": client_id, "appsecret": client_secret}
    
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(url, params=params)
        result = response.json()
        if result.get('errcode') == 0:
            return result.get('access_token', '')
    return ""


async def upload_file_to_dingtalk(file_path: str, access_token: str) -> str:
    """上传文件到钉钉"""
    upload_url = "https://oapi.dingtalk.com/media/upload"
    async with httpx.AsyncClient(timeout=30) as client:
        with open(file_path, 'rb') as f:
            files = {'media': f}
            params = {'access_token': access_token, 'type': 'file'}
            response = await client.post(upload_url, params=params, files=files)
            result = response.json()
            if result.get('errcode') == 0:
                return result.get('media_id', '')
    return ""


async def send_file_to_dingtalk_chat(media_id: str, chat_id: str, access_token: str) -> bool:
    """发送文件到钉钉群"""
    send_url = "https://oapi.dingtalk.com/chat/send"
    data = {"chatid": chat_id, "sender_id": "system", "msgtype": "file", "file": {"media_id": media_id}}
    params = {"access_token": access_token}
    
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(send_url, params=params, json=data)
        result = response.json()
        return result.get('errcode') == 0


async def send_markdown_to_dingtalk(title: str, text: str, webhook: str) -> bool:
    """发送 Markdown 消息到钉钉机器人"""
    headers = {"Content-Type": "application/json"}
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": title,
            "text": text
        }
    }
    
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(webhook, headers=headers, json=data)
        result = response.json()
        return result.get('errcode') == 0


def validate_excel_file(file_path: Path, platform_name: str, is_offline: bool = False) -> bool:
    """
    验证 Excel 文件内容是否匹配当前渠道
    
    Args:
        file_path: Excel 文件路径
        platform_name: 平台名称
        is_offline: 是否下架榜单
    
    Returns:
        bool: 文件是否有效
    """
    if pd is None:
        return True  # 如果没有 pandas，跳过验证
    
    try:
        # 读取第一个 sheet 的前 3 行
        df = pd.read_excel(file_path, sheet_name=0, nrows=3)
        
        # 检查整个文件内容是否包含平台名称（包括列名）
        file_content = df.to_string().lower()
        columns_str = ' '.join([str(col).lower() for col in df.columns])
        full_content = file_content + ' ' + columns_str
        
        # 下架榜单检查"下架"字样，上架榜单检查平台名称
        if is_offline:
            if '下架' in file_content:
                print(f"   ✅ 文件内容验证通过：包含\"下架\"")
                return True
            else:
                print(f"   ❌ 文件内容不匹配：不包含\"下架\"")
                return False
        else:
            if platform_name.lower() in full_content:
                print(f"   ✅ 文件内容验证通过：包含\"{platform_name}\"")
                return True
            else:
                print(f"   ❌ 文件内容不匹配：不包含\"{platform_name}\"")
                return False
    except Exception as e:
        print(f"   ⚠️ 验证 Excel 失败：{e}")
        return True  # 验证失败时不阻止流程
    
    return True


def parse_excel_data(file_path: Path, is_offline: bool = False):
    """解析 Excel 文件，返回统计信息和 TOP20"""
    if pd is None:
        return None, None
    
    try:
        # 读取第一个 sheet
        df = pd.read_excel(file_path, sheet_name=0)
        
        # 获取列名（第一行是列名）
        if len(df) > 0:
            # 第一列是序号，第二列是应用 ID，第三列是应用名称，第四列是开发者，
            # 第五列是上架类型，第七列是价格，第八列是分类
            data_rows = df.iloc[1:]  # 跳过列名行
            
            if len(data_rows) > 0:
                total = len(data_rows)
                
                if is_offline:
                    # 下架榜单统计
                    if 4 < len(data_rows.columns):
                        offline_apps = data_rows[data_rows.iloc[:, 4] == '下架']
                        recovered_apps = data_rows[data_rows.iloc[:, 4] == '重新上架']
                    else:
                        offline_apps = data_rows
                        recovered_apps = []
                    
                    offline_count = len(offline_apps)
                    recovered_count = len(recovered_apps)
                    
                    stats = {
                        'total': total,
                        'new': offline_count,  # 下架数量
                        'recovered': recovered_count  # 重新上架数量
                    }
                else:
                    # 上架榜单统计
                    if 4 < len(data_rows.columns):
                        new_apps = data_rows[data_rows.iloc[:, 4] == '新上架']
                        recovered_apps = data_rows[data_rows.iloc[:, 4] == '恢复上架']
                    else:
                        new_apps = data_rows
                        recovered_apps = []
                    
                    total = len(data_rows)
                    new_count = len(new_apps)
                    recovered_count = len(recovered_apps)
                    
                    stats = {
                        'total': total,
                        'new': new_count,
                        'recovered': recovered_count
                    }
                
                # 获取 TOP20
                top20 = []
                for i in range(min(20, len(data_rows))):
                    row = data_rows.iloc[i]
                    app_name = row.iloc[2] if 2 < len(row) else 'Unknown'
                    category = row.iloc[7] if 7 < len(row) else 'Unknown'
                    top20.append({'name': app_name, 'category': category})
                
                return stats, top20
    except Exception as e:
        print(f"解析 Excel 失败：{e}")
    
    return None, None


def generate_markdown_message(stats: dict, top20: list, platform_name: str, filename: str, is_offline: bool = False) -> tuple:
    """生成 Markdown 消息"""
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    if is_offline:
        title = f"📊 点点数据 - 下架监控 ({date_str})"
        monitor_type = "下架"
        data_type = "下架"
    else:
        title = f"📊 点点数据 - 上架监控 ({date_str})"
        monitor_type = "上架"
        data_type = "新上架"
    
    # 构建消息文本
    text = f"""## 📊 点点数据 - {monitor_type}监控

**📅 数据日期**: {date_str}
**📱 平台**: {platform_name}
**📈 类型**: {monitor_type}监控

---

### 📊 数据统计
"""
    
    # 上架榜单显示详细统计，下架榜单显示下架和重新上架
    if is_offline:
        text += f"""- **下架**: {stats.get('new', 0)} 个
- **重新上架**: {stats.get('recovered', 0)} 个
- **总计**: {stats.get('total', 0)} 个
"""
    else:
        text += f"""- **{data_type}**: {stats.get('new', 0)} 个
- **恢复上架**: {stats.get('recovered', 0)} 个
- **总计**: {stats.get('total', 0)} 个
"""
    
    text += f"""
---

### 🔥 TOP 20 {data_type}

"""
    
    # 添加 TOP20 列表
    for i, app in enumerate(top20, 1):
        text += f"{i}. **{app['name']}** ({app['category']})\n"
    
    text += f"\n---\n\n📄 完整数据：`{filename}`"
    
    return title, text


async def main():
    """连接已运行的浏览器并获取数据"""
    parser = argparse.ArgumentParser(description='点点数据上架/下架榜单获取')
    parser.add_argument('--platform', type=str, default='appstore_cn',
                       help='平台名称 (appstore_cn, huawei, xiaomi, vivo, oppo, etc.)')
    parser.add_argument('--offline', action='store_true',
                       help='获取下架榜单（默认获取上架榜单）')
    parser.add_argument('--force', action='store_true',
                       help='强制重新获取，即使当天文件已存在')
    args = parser.parse_args()
    
    platform = args.platform
    if platform not in PLATFORM_MAP:
        print(f"❌ 未知平台：{platform}")
        print(f"可用平台：{', '.join(PLATFORM_MAP.keys())}")
        return False
    
    platform_info = PLATFORM_MAP[platform]
    platform_name = platform_info['name']
    
    # 生成 URL（上架榜或下架榜）
    if args.offline:
        # 检查平台映射表是否有专门的下架榜 URL
        offline_platform_key = platform + '_offline'
        if offline_platform_key in PLATFORM_MAP:
            platform_url = PLATFORM_MAP[offline_platform_key]['url']
        else:
            # 下架榜：将 URL 中的第二个参数从 0 改为 1
            # 上架榜：line-2-0-0-75-0-3-0
            # 下架榜：line-2-1-0-75-0-3-0
            base_url = platform_info['url']
            parts = base_url.split('/')
            url_path = parts[-1].split('-')
            if len(url_path) >= 3:
                url_path[2] = '1'  # 下架榜标记（第二个参数，索引 2）
                platform_url = '/'.join(parts[:-1] + ['-'.join(url_path)])
            else:
                platform_url = base_url
        list_type = '下架'
    else:
        platform_url = platform_info['url']
        list_type = '上架'
    
    # 检查当天文件是否已存在
    date_str = datetime.now().strftime('%Y%m%d')
    if args.offline:
        existing_filename = f"{platform}_offline_apps_{date_str}.xlsx"
    else:
        existing_filename = f"{platform}_new_apps_{date_str}.xlsx"
    existing_path = REPORTS_DIR / existing_filename
    
    if existing_path.exists():
        print("=" * 60)
        print(f"📊 点点数据 - {platform_name} {list_type}榜单获取")
        print("=" * 60)
        print(f"\n⚠️ 检测到当天文件已存在：{existing_filename}")
        print(f"📁 文件路径：{existing_path}")
        print(f"\n💡 如需重新获取，请添加 --force 参数")
        
        # 检查是否有 --force 参数
        if not args.force:
            print("\n✅ 使用已有文件，跳过获取")
            return True
    
    print("=" * 60)
    print(f"📊 点点数据 - {platform_name} {list_type}榜单获取")
    print("=" * 60)
    
    dingtalk_config = load_dingtalk_config()
    dingtalk = dingtalk_config.get('dingtalk', {})
    
    async with async_playwright() as p:
        # 优先尝试连接已有浏览器（CDP 端口 9222）
        print("\n🚀 启动浏览器...")
        browser = None
        context = None
        
        # 尝试连接已有浏览器
        try:
            browser = await p.chromium.connect_over_cdp('http://127.0.0.1:9222')
            print("   ✅ 连接到已有浏览器 (CDP 端口 9222)")
            if len(browser.contexts) > 0:
                context = browser.contexts[0]
                print("   ✅ 使用已有浏览器 context")
            else:
                context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
                print("   ✅ 创建新 context")
        except Exception as e:
            # 连接失败，启动新浏览器
            print(f"   ⚠️  连接已有浏览器失败: {e}")
            print("   启动新浏览器...")
            browser = await p.chromium.launch(
                headless=False,
                args=[
                    '--start-maximized',
                    '--disable-extensions',
                    '--disable-gpu',
                    '--no-first-run',
                    '--no-default-browser-check'
                ]
            )
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080}
            )
            print("   ✅ 新浏览器启动完成")
        
        # 加载之前保存的 Cookie
        config_path = CONFIG_DIR / "diandian.yaml"
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f) or {}
            cookie_str = config.get('cookie', '')
            if cookie_str:
                print("   🍪 加载已保存的 Cookie...")
                # 解析 Cookie 字符串
                import re
                cookies = []
                for part in cookie_str.split(';'):
                    part = part.strip()
                    if not part:
                        continue
                    name_value = part.split('=', 1)
                    if len(name_value) == 2:
                        cookies.append({
                            'name': name_value[0].strip(),
                            'value': name_value[1].strip(),
                            'domain': '.diandian.com',
                            'path': '/'
                        })
                if cookies:
                    await context.add_cookies(cookies)
                    print(f"   ✅ 已加载 {len(cookies)} 个 Cookie")
        
        try:
            # Step 0: 检查登录状态
            print(f"\n📖 Step 0: 检查登录状态...")
            page = None
            if len(context.pages) > 0:
                # 使用第一个已有页面
                for candidate in context.pages:
                    try:
                        # 测试页面是否可用
                        title = await candidate.title()
                        page = candidate
                        print(f"   ✅ 使用已有页面 (title: {title[:30]})")
                        break
                    except Exception as e:
                        # 页面已关闭，跳过
                        continue
            if page is None:
                page = await context.new_page()
                print("   ✅ 创建新页面")
                await asyncio.sleep(1)  # 等待页面初始化
            await page.goto('https://app.diandian.com/', wait_until='networkidle', timeout=120000)
            await asyncio.sleep(3)
            
            page_text = await page.text_content('body')
            if '退出登录' not in page_text and ('登录' in page_text and '注册' in page_text):
                login_btn = page.locator('text=登录').first
                if await login_btn.count() > 0:
                    print("   ❌ 检测到未登录状态，开始自动登录...")
                    
                    # 加载账号密码
                    credentials_path = CONFIG_DIR / "credentials.yaml"
                    if credentials_path.exists():
                        with open(credentials_path, 'r', encoding='utf-8') as f:
                            credentials = yaml.safe_load(f)
                        
                        username = credentials.get('diandian', {}).get('username', '')
                        password = credentials.get('diandian', {}).get('password', '')
                        
                        if username and password:
                            print("   📖 点击登录...")
                            await login_btn.click()
                            await asyncio.sleep(5)  # 增加等待时间让弹窗加载
                            
                            print("   📖 选择邮箱登录...")
                            # 页面已经跳转到登录页，邮箱标签
                            email_btn = page.locator('text=邮箱').first
                            if await email_btn.count() > 0:
                                await email_btn.click()
                                await asyncio.sleep(5)  # 增加等待时间让输入框加载
                                
                                print("   📖 输入账号密码...")
                                await asyncio.sleep(2)  # 额外等待确保输入框可交互
                                # 多种选择器尝试
                                email_input = page.locator('input[placeholder="请输入邮箱"], input[placeholder*="邮箱"], input[type="email"]').first
                                password_input = page.locator('input[placeholder="请输入密码"], input[placeholder*="密码"], input[type="password"]').first
                                
                                if await email_input.count() > 0:
                                    await email_input.fill(username)
                                    await password_input.fill(password)
                                    await asyncio.sleep(1)
                                    
                                    print("   📖 提交登录...")
                                    submit_btn = page.locator('button:has-text("登录")').first
                                    if await submit_btn.count() > 0:
                                        await submit_btn.click()
                                        await asyncio.sleep(5)
                                        
                                        # 检查是否登录成功
                                        new_text = await page.text_content('body')
                                        if '登录' not in new_text:
                                            print("   ✅ 登录成功")
                                            
                                            # 保存 Cookie
                                            cookies = await context.cookies()
                                            cookie_str = '; '.join([f"{c['name']}={c['value']}" for c in cookies])
                                            
                                            config_path = CONFIG_DIR / "diandian.yaml"
                                            config = {}
                                            if config_path.exists():
                                                with open(config_path, 'r', encoding='utf-8') as f:
                                                    config = yaml.safe_load(f) or {}
                                            
                                            config['cookie'] = cookie_str
                                            config['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M')
                                            
                                            with open(config_path, 'w', encoding='utf-8') as f:
                                                yaml.dump(config, f, allow_unicode=True)
                                            
                                            print("   ✅ Cookie 已保存")
                                        else:
                                            print("   ❌ 登录失败")
                                            await browser.close()
                                            return False
                                    else:
                                        print("   ❌ 未找到登录提交按钮")
                                        await browser.close()
                                        return False
                                else:
                                    print("   ❌ 未找到邮箱输入框")
                                    await browser.close()
                                    return False
                            else:
                                print("   ❌ 未找到邮箱登录选项")
                                await browser.close()
                                return False
                        else:
                            print("   ❌ 账号密码为空，请配置 credentials.yaml")
                            await browser.close()
                            return False
                    else:
                        print("   ❌ 未找到 credentials.yaml 配置文件")
                        await browser.close()
                        return False
            # 重新获取 page（可能已经导航）
            # 重新获取 page（可能已经导航）
            page = context.pages[0] if context.pages else await context.new_page()
            
            # Step 1: 导航到监控页面
            print(f"\n📖 Step 1: 访问{platform_name}{list_type}监控页面...")
            
            # 访问目标 URL
            print(f"   📍 访问：{platform_url}")
            print(f"   📋 榜单类型：{list_type}")
            
            # 直接导航到目标 URL
            await page.goto(platform_url, wait_until='networkidle', timeout=120000)
            await asyncio.sleep(60)  # 等待更长时间让数据加载（修改为 60 秒）
            
            # 验证页面是否正确，等待标题出现
            for i in range(10):
                page_title = await page.title()
                if page_title:
                    break
                await asyncio.sleep(2)
            
            # 验证页面是否正确
            page_title = await page.title()
            print(f"   📄 页面标题：{page_title}")
            
            # 检查页面标题是否包含平台名称（忽略大小写）
            if platform_name.lower() not in page_title.lower():
                print(f"   ❌ 页面标题不匹配！预期包含\"{platform_name}\"，实际：{page_title}")
                print(f"   ⚠️ 停止获取，避免获取错误数据")
                await browser.close()
                return False
            
            print(f"   ✅ 页面标题验证通过")
            
            # 截图
            await page.screenshot(path=str(REPORTS_DIR / f'debug_{platform}_page.png'), full_page=True)
            print("   📸 截图已保存")
            
            # 滚动到底部/顶部，确保所有元素加载
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(5)
            await page.evaluate("window.scrollTo(0, 0)")
            await asyncio.sleep(5)
            
            # 检查导出按钮是否存在
            export_btn = page.locator('.dd-export-btn').first
            if await export_btn.count() > 0:
                print("   ✅ 导出按钮存在")
            else:
                print("   ❌ 导出按钮不存在，可能需要更长时间加载")
                await asyncio.sleep(60)  # 再等待 60 秒（修改为 60 秒）
                # 再次尝试滚动
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await asyncio.sleep(3)
                await page.evaluate("window.scrollTo(0, 0)")
                await asyncio.sleep(3)
            
            print("   ✅ 页面已加载")
            
            # 截图
            await page.screenshot(path=str(REPORTS_DIR / f'debug_{platform}_page.png'), full_page=True)
            print("   📸 截图已保存")
            
            # Step 2: 点击"导出数据"
            print(f"\n📖 Step 2: 点击'导出数据'按钮...")
            export_btn = page.locator('.dd-export-btn').first
            if await export_btn.count() > 0:
                await export_btn.click()
                print("   ✅ 已点击'导出数据'")
                # 等待导出文件生成
                print("   ⏳ 等待导出文件生成...")
                await asyncio.sleep(5)
            else:
                print("   ❌ 未找到'导出数据'按钮")
                return False
            
            # Step 3: 点击弹窗中的"下载"按钮
            print("\n📖 Step 3: 点击弹窗中的'下载'按钮...")
            
            # 预期文件名（点点数据生成的文件名）
            date_str = datetime.now().strftime('%Y%m%d')
            # 点点数据默认文件名格式：平台_中国区_类型_日期.xlsx
            if args.offline:
                expected_filename = f"{platform_info['name']}_中国区_下架监控_{date_str}.xlsx"
            else:
                expected_filename = f"{platform_info['name']}_中国区_上架监控_{date_str}.xlsx"
            
            download_btn = page.locator('span.download.dd-pointer').first
            if await download_btn.count() > 0:
                await download_btn.click()
                print("   ✅ 已点击'下载'")
                print("   ⏳ 等待下载完成...")
                # 截图导出弹窗状态
                await page.screenshot(path=str(REPORTS_DIR / f'debug_{platform}_download_popup.png'), full_page=True)
                print("   📸 下载弹窗截图已保存")
                await asyncio.sleep(15)  # 等待下载完成（增加到 15 秒）
                
                # 检查下载目录（Chrome 默认下载到 ~/Downloads）
                download_dir = Path.home() / "Downloads"
                downloaded_file = download_dir / expected_filename
                
                if not downloaded_file.exists():
                    # 尝试其他可能的文件名格式（不带中国区）
                    alt_filename = f"{platform_info['name']}_{'下架' if args.offline else '上架'}监控_{date_str}.xlsx"
                    downloaded_file = download_dir / alt_filename
                
                if downloaded_file.exists():
                    downloaded_file_size = downloaded_file.stat().st_size
                    print(f"   📥 文件已下载：{downloaded_file} ({downloaded_file_size} bytes)")
                    
                    # 验证文件内容是否匹配当前渠道
                    print("   🔍 验证文件内容...")
                    file_valid = validate_excel_file(downloaded_file, platform_name, args.offline)
                else:
                    print(f"   ❌ 未找到下载文件：{expected_filename}")
                    print(f"      在目录：{download_dir}")
                    await browser.close()
                    return False
            else:
                print("   ❌ 未找到下载按钮")
                await browser.close()
                return False
            
            if not file_valid:
                print(f"   ⚠️ 文件内容不匹配{platform_name}，可能是上一次导出的数据")
                print("   ⏳ 等待 2 秒后重新下载...")
                await asyncio.sleep(2)
                # 删除已下载的错误文件
                if downloaded_file.exists():
                    downloaded_file.unlink()
                # 重新点击下载按钮
                await download_btn.click()
                await asyncio.sleep(10)
                # 再次验证
                file_valid = validate_excel_file(downloaded_file, platform_name, args.offline)
                if not file_valid:
                    print(f"   ❌ 文件内容仍然不匹配，跳过发送")
                    await browser.close()
                    return False
            
            # 复制文件到 reports 目录（只保留日期，不保留时分秒）
            date_str = datetime.now().strftime('%Y%m%d')
            if args.offline:
                new_filename = f"{platform}_offline_apps_{date_str}.xlsx"
            else:
                new_filename = f"{platform}_new_apps_{date_str}.xlsx"
            new_path = REPORTS_DIR / new_filename
            
            # 如果文件已存在，先删除
            if new_path.exists():
                new_path.unlink()
                print(f"   🗑️ 已删除旧文件：{new_filename}")
            
            # 复制文件（保留原文件在下载目录）
            import shutil
            shutil.copy2(downloaded_file, new_path)
            print(f"   💾 文件已保存：{new_path.name} (已验证)")
                    
            # Step 4: 发送钉钉
            print("\n📖 Step 4: 发送钉钉...")
            if dingtalk.get('client_id') and dingtalk.get('chat_id'):
                access_token = await get_dingtalk_access_token(
                    dingtalk['client_id'],
                    dingtalk['client_secret']
                )
                
                if access_token:
                    # 解析 Excel 数据
                    stats, top20 = parse_excel_data(new_path, args.offline)
                    
                    if stats and top20:
                        # 生成 Markdown 消息
                        title, markdown_text = generate_markdown_message(
                            stats, top20, platform_name, new_filename, args.offline
                        )
                        
                        # 发送 Markdown 消息
                        webhook = dingtalk.get('webhook', '')
                        if webhook:
                            print("   📤 发送 Markdown 通知...")
                            await send_markdown_to_dingtalk(title, markdown_text, webhook)
                            print("   ✅ Markdown 通知已发送")
                            
                            # 上传并发送文件
                            print("   📤 上传文件...")
                            media_id = await upload_file_to_dingtalk(str(new_path), access_token)
                            if media_id:
                                print("   📤 发送文件到群聊...")
                                success = await send_file_to_dingtalk_chat(
                                    media_id,
                                    dingtalk['chat_id'],
                                    access_token
                                )
                                if success:
                                    print("   ✅ 文件已发送到钉钉群")
                    
                    print("\n" + "=" * 60)
                    print("✅ 任务完成！")
                    print("=" * 60)
                    print("\n💡 浏览器保持打开状态，可继续执行其他任务")
                    return True
                else:
                    print("   ❌ 未找到'下载'按钮")
                    return False
            
        except Exception as e:
            print(f"\n❌ 错误：{e}")
            import traceback
            traceback.print_exc()
            return False
        
        finally:
            # 不关闭浏览器，只关闭连接
            await browser.close()
            print("\n✅ 已断开连接，浏览器保持运行")


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
