#!/usr/bin/env python3
"""
点点数据全渠道上架/下架榜完整导出 - 单次登录批量处理版本
解决重复登录问题，一次登录导出所有渠道
"""

import asyncio
import yaml
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright
import sys
import os
import shutil

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from notifiers.dingtalk import DingTalkNotifier

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('DiandianFullExport')


def load_credentials() -> dict:
    """加载账号凭证"""
    cred_path = Path(__file__).parent.parent / "config" / "credentials.yaml"
    if not cred_path.exists():
        raise FileNotFoundError(f"凭证文件不存在：{cred_path}")
    
    with open(cred_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


async def login(page, username: str, password: str) -> bool:
    """执行登录流程"""
    logger.info("🔐 开始登录流程...")
    
    try:
        # Step 1: 点击右上角的"登录/注册"
        logger.info("📖 Step 1: 点击右上角的'登录/注册'...")
        
        # 等待页面完全加载
        await asyncio.sleep(3)
        
        login_btn = await page.wait_for_selector('text="登录/注册"', timeout=15000)
        await login_btn.click()
        await asyncio.sleep(3)
        logger.info("✅ 已点击登录/注册按钮")
        
        # 截图
        screenshot_path = Path(__file__).parent.parent / "debug_full_login_1.png"
        await page.screenshot(path=str(screenshot_path))
        
        # Step 2: 点击"邮箱"选项 - 使用更精确的选择器
        logger.info("📖 Step 2: 点击'邮箱'选项...")
        await asyncio.sleep(2)
        
        # 多种方式查找邮箱选项
        email_found = False
        
        # 方法 1: 使用文本查找
        email_elements = await page.query_selector_all('text=邮箱')
        for el in email_elements:
            box = await el.bounding_box()
            if box:
                await el.click()
                email_found = True
                break
        
        if not email_found:
            # 方法 2: 使用 JavaScript 查找
            email_found = await page.evaluate("""() => {
                const elements = document.querySelectorAll('*');
                for (const el of elements) {
                    if (el.textContent && el.textContent.includes('邮箱') && 
                        !el.textContent.includes('Google') && 
                        !el.textContent.includes('短信')) {
                        el.click();
                        return true;
                    }
                }
                return false;
            }""")
        
        if not email_found:
            logger.error("❌ 未找到邮箱选项")
            return False
        
        await asyncio.sleep(3)
        logger.info("✅ 已点击邮箱选项")
        
        # 截图
        screenshot_path = Path(__file__).parent.parent / "debug_full_login_2.png"
        await page.screenshot(path=str(screenshot_path))
        
        # Step 3: 输入账号密码
        logger.info("📖 Step 3: 输入账号密码...")
        
        # 尝试多种选择器找到输入框
        username_input = None
        password_input = None
        
        selectors = [
            'input[placeholder*="邮箱"]',
            'input[type="text"]',
            'input[autocomplete="username"]',
        ]
        
        for selector in selectors:
            el = await page.query_selector(selector)
            if el:
                username_input = el
                break
        
        selectors = [
            'input[placeholder*="密码"]',
            'input[type="password"]',
            'input[autocomplete="password"]',
        ]
        
        for selector in selectors:
            el = await page.query_selector(selector)
            if el:
                password_input = el
                break
        
        if not username_input or not password_input:
            logger.error("❌ 未找到输入框")
            screenshot_path = Path(__file__).parent.parent / "debug_full_login_no_input.png"
            await page.screenshot(path=str(screenshot_path))
            return False
        
        await username_input.fill(username)
        await asyncio.sleep(0.5)
        await password_input.fill(password)
        await asyncio.sleep(0.5)
        logger.info("✅ 已输入账号密码")
        
        # Step 4: 点击登录按钮
        logger.info("📖 Step 4: 点击登录按钮...")
        
        login_clicked = False
        login_selectors = [
            'button:has-text("登录")',
            'button[type="submit"]',
            '[role="button"]:has-text("登录")',
        ]
        
        for selector in login_selectors:
            btn = await page.query_selector(selector)
            if btn:
                await btn.click()
                login_clicked = True
                break
        
        if not login_clicked:
            login_clicked = await page.evaluate("""() => {
                const buttons = document.querySelectorAll('button');
                for (const btn of buttons) {
                    if (btn.textContent.includes('登录')) {
                        btn.click();
                        return true;
                    }
                }
                return false;
            }""")
        
        if not login_clicked:
            logger.error("❌ 未找到登录按钮")
            return False
        
        await asyncio.sleep(8)
        logger.info("✅ 已点击登录按钮")
        
        # 截图
        screenshot_path = Path(__file__).parent.parent / "debug_full_login_3.png"
        await page.screenshot(path=str(screenshot_path))
        
        # Step 5: 验证登录成功
        page_content = await page.content()
        is_logged = '退出' in page_content or '账号设置' in page_content
        
        if is_logged:
            logger.info("✅ 登录成功！")
            return True
        else:
            logger.error("❌ 登录验证失败，可能需要验证码或人机验证")
            return False
            
    except Exception as e:
        logger.error(f"❌ 登录异常：{e}")
        import traceback
        traceback.print_exc()
        return False


async def export_channel(page, channel_name: str, download_dir: Path, monitor_type: str = "new") -> bool:
    """
    导出单个渠道的数据
    
    Args:
        page: Playwright 页面对象
        channel_name: 渠道名称（华为/小米/应用宝...）
        monitor_type: new=上架监控, offline=下架监控
        download_dir: 下载目录
    """
    monitor_text = "上架监控" if monitor_type == "new" else "下架监控"
    logger.info(f"\n📱 开始导出 {channel_name} - {monitor_text}...")
    
    try:
        # 如果还在主页，先导航到上架监控
        if monitor_type == "new":
            # 点击"市场情报"
            logger.info("📖 点击'市场情报'...")
            market_btn = await page.wait_for_selector('text="市场情报"', timeout=10000)
            await market_btn.click()
            await asyncio.sleep(3)
            
            # 点击"上架监控"卡片
            logger.info("📖 点击'上架监控'...")
            await page.evaluate('''() => {
                const allDivs = document.querySelectorAll('div');
                for (const div of allDivs) {
                    const text = div.textContent;
                    if (text && text.includes('上架监控') && text.length < 200) {
                        div.click();
                        return true;
                    }
                }
                return false;
            }''')
            await asyncio.sleep(5)
        else:
            # 点击"市场情报"
            logger.info("📖 点击'市场情报'...")
            market_btn = await page.wait_for_selector('text="市场情报"', timeout=10000)
            await market_btn.click()
            await asyncio.sleep(3)
            
            # 点击"下架监控"卡片
            logger.info("📖 点击'下架监控'...")
            await page.evaluate('''() => {
                const allDivs = document.querySelectorAll('div');
                for (const div of allDivs) {
                    const text = div.textContent;
                    if (text && text.includes('下架监控') && text.length < 200) {
                        div.click();
                        return true;
                    }
                }
                return false;
            }''')
            await asyncio.sleep(5)
        
        # 选择渠道
        logger.info(f"📖 选择渠道: {channel_name}...")
        selected = await page.evaluate(f'''() => {{
            const allDivs = document.querySelectorAll('div');
            for (const div of allDivs) {{
                if (div.textContent && div.textContent.includes('{channel_name}') && 
                    (div.className.includes('name') || div.className.includes('app'))) {{
                    div.click();
                    return true;
                }}
            }}
            return false;
        }}''')
        
        if selected:
            await asyncio.sleep(5)
            logger.info(f"✅ 已选择 {channel_name}")
        else:
            logger.warning(f"⚠️ 选择渠道 {channel_name} 可能失败")
        
        # 滚动加载
        for i in range(2):
            await page.evaluate("window.scrollBy(0, 800)")
            await asyncio.sleep(2)
        
        # 点击导出按钮
        logger.info("📖 点击'导出数据'...")
        await asyncio.sleep(2);
        exported = await page.evaluate('''() => {
            // 方法 1: 查找右上角的导出图标按钮（通常是固定位置）
            const header = document.querySelector('header') || document.querySelector('.header') || document.querySelector('[class*="header"]');
            if (header) {
                const buttons = header.querySelectorAll('button, [role="button"]');
                for (const btn of buttons) {
                    const text = btn.textContent.trim();
                    if (text.includes('导出') || text.includes('下载') || text.includes('⤓') || text.includes('↓')) {
                        btn.click();
                        return true;
                    }
                }
                // 如果是图标按钮，点击最后一个按钮
                const allBtns = header.querySelectorAll('button');
                if (allBtns.length > 0) {
                    allBtns[allBtns.length - 1].click();
                    return true;
                }
            }
            
            // 方法 2: 查找包含导出文字的按钮
            const allButtons = document.querySelectorAll('button, [role="button"]');
            for (const btn of allButtons) {
                const text = btn.textContent.trim();
                if (text.includes('导出') || text.includes('下载')) {
                    btn.click();
                    return true;
                }
            }
            
            // 方法 3: 查找右上角区域任何可点击元素
            const elements = document.querySelectorAll('*');
            for (const el of elements) {
                const rect = el.getBoundingClientRect();
                // 判断是否在右上角
                if (rect.right > window.innerWidth - 200 && rect.top < 100) {
                    const text = el.textContent.trim();
                    if (text.includes('导出') || text.includes('下载')) {
                        if (el.tagName === 'BUTTON' || el.onclick || getComputedStyle(el).cursor === 'pointer') {
                            el.click();
                            return true;
                        }
                    }
                }
            }
            
            // 方法 4: 在右上角区域随便找个按钮点击
            for (const el of elements) {
                const rect = el.getBoundingClientRect();
                if (rect.right > window.innerWidth - 200 && rect.top < 100) {
                    if (el.tagName === 'BUTTON' || el.onclick) {
                        el.click();
                        return true;
                    }
                }
            }
            
            return false;
        }''')
        
        if exported:
            await asyncio.sleep(5)
            logger.info("✅ 已点击导出按钮")
            
            # 点击"所有数据"下载
            downloaded = await page.evaluate('''() => {
                const allElements = document.querySelectorAll('*');
                for (const el of allElements) {
                    const text = el.textContent.trim();
                    if (text.includes('所有') && text.includes('文件') || 
                        text.includes('全部') && text.includes('导出') ||
                        text.includes('下载')) {
                        if (el.tagName === 'BUTTON' || el.onclick) {
                            el.click();
                            return true;
                        }
                    }
                }
                // 如果找不到，直接找下载按钮
                for (const el of allElements) {
                    if (el.textContent.trim() === '下载') {
                        el.click();
                        return true;
                    }
                }
                return false;
            }''')
            
            if downloaded:
                await asyncio.sleep(10)  # 等待下载完成
                logger.info(f"✅ {channel_name} - {monitor_text} 下载完成")
                return True
            else:
                logger.warning(f"⚠️ {channel_name} - {monitor_text} 下载按钮未找到")
                return False
        else:
            logger.warning(f"⚠️ {channel_name} - {monitor_text} 导出按钮未找到")
            return False
            
    except Exception as e:
        logger.error(f"❌ {channel_name} - {monitor_text} 导出失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def find_downloaded_files(download_dir: Path, after_time: datetime) -> list:
    """查找在指定时间之后下载的文件"""
    downloaded = []
    
    # 查找常见的导出文件格式
    patterns = ['*.xlsx', '*.csv', '*.xls']
    
    for pattern in patterns:
        for file in download_dir.glob(pattern):
            mtime = datetime.fromtimestamp(file.stat().st_mtime)
            if mtime > after_time:
                downloaded.append((file, mtime))
    
    # 按时间排序
    downloaded.sort(key=lambda x: x[1], reverse=True)
    return [f[0] for f in downloaded]


async def merge_and_send_to_dingtalk(files: list, today_str: str):
    """合并文件并发送到钉钉"""
    logger.info(f"\n📤 准备发送 {len(files)} 个文件到钉钉...")
    
    if not files:
        logger.warning("⚠️ 没有文件需要发送")
        return False
    
    dingtalk = DingTalkNotifier()
    
    # 如果只有一个文件，直接发送
    if len(files) == 1:
        file_path = files[0]
        title = f"点点数据 {today_str} 上架/下架榜"
        message = f"今日点点数据榜单\n文件: {file_path.name}"
        return await dingtalk.send_file(str(file_path), title, message)
    
    # 如果有多个文件，打包发送
    # 创建临时目录
    export_dir = Path(__file__).parent.parent / "reports" / "diandian_exports"
    export_dir.mkdir(parents=True, exist_ok=True)
    
    # 复制文件并重命名
    copied_files = []
    for src_file in files:
        # 判断类型（上架/下架）
        if "上架" in src_file.name or "新" in src_file.name or "上线" in src_file.name:
            suffix = "上架"
        elif "下架" in src_file.name or "下线" in src_file.name:
            suffix = "下架"
        else:
            suffix = "unknown"
        
        # 复制
        dest_name = f"点点数据_{suffix}_{src_file.name}"
        dest_file = export_dir / dest_name
        shutil.copy2(src_file, dest_file)
        copied_files.append(dest_file)
    
    # 创建 Excel 汇总文件（如果有多个文件需要合并，可以在这里添加合并逻辑）
    
    # 发送汇总文件
    # 这里我们找到最近导出的完整 Excel 文件
    excel_files = list(export_dir.glob(f"点点数据_上架下架榜_{today_str}.xlsx"))
    if excel_files:
        # 使用已合并的文件
        final_file = excel_files[0]
    else:
        # 创建汇总文件名
        final_file = export_dir / f"点点数据_上架下架榜_{today_str}.xlsx"
        # 如果只有一个文件复制过去
        if len(copied_files) == 1:
            shutil.copy2(copied_files[0], final_file)
        else:
            # 这里假设点点已经导出了完整的汇总文件
            # 如果需要合并多个 sheet，可以使用 openpyxl 来合并
            # 这里简化处理，使用最新下载的文件
            pass
    
    if final_file.exists():
        title = f"点点数据 {today_str} 全渠道上架/下架榜"
        message = f"今日（{today_str}）点点数据全渠道上架榜和下架榜已导出，请查看附件。"
        success = await dingtalk.send_file(str(final_file), title, message)
        logger.info(f"✅ 文件已发送到钉钉: {final_file}")
        return success
    else:
        logger.error("❌ 汇总文件不存在")
        return False


async def main():
    """主函数：单次登录，批量导出所有渠道"""
    start_time = datetime.now()
    today_str = start_time.strftime("%Y%m%d")
    logger.info(f"🚀 点点数据全渠道导出任务开始 - {today_str}")
    
    # 配置
    channels = [
        ("华为", "new"),
        ("华为", "offline"),
        ("小米", "new"), 
        ("小米", "offline"),
        ("应用宝", "new"),
        ("应用宝", "offline"),
        ("OPPO", "new"),
        ("OPPO", "offline"),
        ("vivo", "new"),
        ("vivo", "offline"),
        ("百度", "new"),
        ("百度", "offline"),
        ("360", "new"),
        ("360", "offline"),
        ("豌豆荚", "new"),
        ("豌豆荚", "offline"),
    ]
    
    # 下载目录
    download_dir = Path.home() / "Downloads"
    
    # 加载凭证 - 使用备份账号
    creds = load_credentials()
    diandian = creds.get('diandian_backup', {})
    username = diandian.get('username', '')
    password = diandian.get('password', '')
    
    if not username or not password:
        logger.error("❌ 账号密码未配置")
        return 1
    
    logger.info(f"🎯 使用账号: {username}")
    logger.info(f"📋 需要导出 {len(channels)} 个（渠道+类型）")
    
    async with async_playwright() as p:
        # 启动浏览器
        user_data_dir = Path(__file__).parent.parent / ".browser_data" / "diandian"
        user_data_dir.mkdir(parents=True, exist_ok=True)
        
        context = await p.chromium.launch_persistent_context(
            user_data_dir=str(user_data_dir),
            headless=False,
            channel='chrome',
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                f'--download-path={download_dir}'
            ]
        )
        
        page = context.pages[0] if context.pages else await context.new_page()
        await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        try:
            # Step 1: 访问主页
            logger.info("📖 Step 1: 访问点点数据主页...")
            await page.goto("https://app.diandian.com/", wait_until="domcontentloaded", timeout=60000)
            await asyncio.sleep(5)
            
            # Step 2: 检查是否已登录
            page_content = await page.content()
            is_logged = '退出' in page_content or '账号设置' in page_content
            
            if is_logged:
                logger.info("✅ 已处于登录状态，跳过登录")
            else:
                # 需要登录
                login_success = await login(page, username, password)
                if not login_success:
                    logger.error("❌ 登录失败，任务终止")
                    # 保存错误截图
                    screenshot_path = Path(__file__).parent.parent / f"debug_full_login_error.png"
                    await page.screenshot(path=str(screenshot_path))
                    await context.close()
                    return 1
            
            # 记录开始下载时间
            download_start_time = datetime.now()
            
            # Step 3: 批量导出
            results = {}
            for channel_name, monitor_type in channels:
                success = await export_channel(page, channel_name, download_dir, monitor_type)
                results[f"{channel_name}-{monitor_type}"] = success
                
                # 每个渠道后等待
                await asyncio.sleep(5)
                
                # 检查超时
                elapsed = (datetime.now() - start_time).total_seconds()
                if elapsed > 600:  # 10 分钟超时
                    logger.warning(f"⏱️  已执行 {elapsed:.1f} 秒，提前结束")
                    break
            
            # Step 4: 查找下载的文件并发送到钉钉
            await asyncio.sleep(10)  # 等待最后一个下载完成
            downloaded_files = find_downloaded_files(download_dir, download_start_time)
            
            logger.info(f"\n📊 导出结果汇总:")
            success_count = sum(1 for v in results.values() if v)
            total_count = len(results)
            logger.info(f"成功: {success_count}/{total_count}")
            
            for key, success in results.items():
                status = "✅" if success else "❌"
                logger.info(f"  {status} {key}")
            
            logger.info(f"\n📂 下载目录找到 {len(downloaded_files)} 个新文件")
            for f in downloaded_files[:5]:
                logger.info(f"  - {f.name}")
            if len(downloaded_files) > 5:
                logger.info(f"  ... 还有 {len(downloaded_files) - 5} 个")
            
            # 发送到钉钉
            if downloaded_files:
                success = await merge_and_send_to_dingtalk(downloaded_files, today_str)
                if success:
                    logger.info("✅ 所有文件已发送到钉钉！")
                else:
                    logger.error("❌ 发送到钉钉失败")
            else:
                logger.warning("⚠️ 没有找到新下载的文件")
            
            # 保存最终截图
            screenshot_path = Path(__file__).parent.parent / f"debug_full_export_final_{today_str}.png"
            await page.screenshot(path=str(screenshot_path), full_page=True)
            
            # 完成
            elapsed_total = (datetime.now() - start_time).total_seconds()
            logger.info(f"\n🏁 任务完成！总耗时: {elapsed_total:.1f} 秒")
            logger.info(f"成功: {success_count}/{total_count}")
            
            await context.close()
            
            # 返回成功码如果至少有一个成功
            return 0 if success_count > 0 else 1
            
        except Exception as e:
            logger.error(f"❌ 任务异常: {e}")
            import traceback
            traceback.print_exc()
            
            # 保存错误截图
            try:
                screenshot_path = Path(__file__).parent.parent / f"debug_full_export_error_{today_str}.png"
                await page.screenshot(path=str(screenshot_path))
            except:
                pass
            
            await context.close()
            return 1


if __name__ == "__main__":
    exit(asyncio.run(main()))
