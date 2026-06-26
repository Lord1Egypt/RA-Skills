#!/usr/bin/env python3
"""
点点数据上架监控导出 - 最终版本
支持自动登录、选择渠道、导出数据、发送钉钉通知
"""

import asyncio
import yaml
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright
import sys
import os

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from notifiers.dingtalk import DingTalkNotifier

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('DiandianExport')


def load_credentials() -> dict:
    """加载账号凭证"""
    cred_path = Path(__file__).parent.parent / "config" / "credentials.yaml"
    if not cred_path.exists():
        raise FileNotFoundError(f"凭证文件不存在：{cred_path}")
    
    with open(cred_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


async def login_if_needed(page, username: str, password: str) -> bool:
    """检查登录状态，未登录则自动登录"""
    logger.info("📖 检查登录状态...")
    
    # 检查是否已登录
    page_content = await page.content()
    is_logged = '退出' in page_content or '账号设置' in page_content
    
    if is_logged:
        logger.info("✅ 已登录状态")
        return True
    
    logger.info("⚠️ 未登录，开始登录流程...")
    
    try:
        # Step 1: 点击右上角的"登录/注册"
        logger.info("📖 Step 1: 点击右上角的'登录/注册'...")
        login_btn = await page.wait_for_selector('text="登录/注册"', timeout=10000)
        await login_btn.click()
        await asyncio.sleep(2)
        logger.info("✅ 已点击登录/注册按钮")
        
        # Step 2: 点击"邮箱"选项
        logger.info("📖 Step 2: 点击'邮箱'选项...")
        email_selectors = ['text="邮箱"', 'div:has-text("邮箱")']
        clicked = False
        for selector in email_selectors:
            try:
                email_els = await page.query_selector_all(selector)
                for el in email_els:
                    el_text = await el.inner_text()
                    if '邮箱' in el_text and 'Google' not in el_text:
                        await el.click()
                        clicked = True
                        break
                if clicked:
                    break
            except Exception as e:
                logger.debug(f"选择器 {selector} 失败：{e}")
        
        if not clicked:
            logger.error("❌ 未找到邮箱选项")
            return False
        
        await asyncio.sleep(2)
        
        # Step 3: 输入账号密码
        logger.info("📖 Step 3: 输入账号密码...")
        username_input = await page.wait_for_selector('input[placeholder="请输入邮箱"]', timeout=5000)
        password_input = await page.wait_for_selector('input[placeholder="请输入密码"]', timeout=5000)
        
        await username_input.fill(username)
        await asyncio.sleep(0.5)
        await password_input.fill(password)
        await asyncio.sleep(0.5)
        logger.info("✅ 已输入账号密码")
        
        # Step 4: 点击登录按钮
        logger.info("📖 Step 4: 点击登录按钮...")
        submit_btn = await page.wait_for_selector('button:has-text("登录")', timeout=5000)
        await submit_btn.click()
        await asyncio.sleep(5)
        logger.info("✅ 已点击登录按钮")
        
        # 验证登录成功
        page_content = await page.content()
        is_logged = '退出' in page_content or '账号设置' in page_content
        
        if is_logged:
            logger.info("✅ 登录成功")
            return True
        else:
            logger.error("❌ 登录失败")
            return False
            
    except Exception as e:
        logger.error(f"❌ 登录异常：{e}")
        import traceback
        traceback.print_exc()
        return False


async def export_monitor_data(channel: str = "华为", send_to_dingtalk: bool = True, timeout: int = 300):
    """
    导出上架监控数据
    
    Args:
        channel: 商店渠道（华为/小米/应用宝等）
        send_to_dingtalk: 是否发送到钉钉
        timeout: 超时时间（秒），默认 5 分钟
    """
    logger.info(f"📱 开始导出 {channel} 渠道上架监控数据...")
    logger.info(f"📤 发送到钉钉：{'是' if send_to_dingtalk else '否'}")
    logger.info(f"⏱️  超时时间：{timeout}秒")
    
    start_time = datetime.now()
    
    async with async_playwright() as p:
        # 启动浏览器
        user_data_dir = Path(__file__).parent.parent / ".browser_data" / "diandian"
        user_data_dir.mkdir(parents=True, exist_ok=True)
        
        # 配置下载目录
        download_dir = Path.home() / "Downloads"
        
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
            await asyncio.sleep(3)
            
            # 检查是否超时
            if (datetime.now() - start_time).total_seconds() > timeout:
                logger.error(f"❌ 执行超时（{timeout}秒）")
                await context.close()
                return False
            
            # Step 2: 检查登录状态，未登录则自动登录
            creds = load_credentials()
            diandian = creds.get('diandian_backup', {})
            username = diandian.get('username', '')
            password = diandian.get('password', '')
            
            if not username or not password:
                logger.error("❌ 账号密码未配置")
                await context.close()
                return False
            
            login_success = await login_if_needed(page, username, password)
            if not login_success:
                logger.error("❌ 登录失败")
                await context.close()
                return False
            
            # Step 3: 点击顶部"市场情报"按钮，弹出市场趋势弹窗
            logger.info("📖 Step 3: 点击'市场情报'按钮...")
            market_intel_btn = await page.wait_for_selector('text="市场情报"', timeout=10000)
            await market_intel_btn.click()
            await asyncio.sleep(3)  # 等待弹窗完全展开
            logger.info("✅ 已点击市场情报，弹出市场趋势弹窗")
            
            # Step 4: 在市场趋势弹窗中点击"上架监控"卡片
            logger.info("📖 Step 4: 点击'上架监控'卡片...")
            try:
                # 等待弹窗完全展开
                await asyncio.sleep(2)
                
                # 查找包含"上架监控"文本的卡片并点击
                result = await page.evaluate('''() => {
                    const allDivs = document.querySelectorAll('div');
                    for (const div of allDivs) {
                        const text = div.textContent;
                        // 查找包含"上架监控"的卡片（确保不是其他文本的一部分）
                        if (text.includes('上架监控') && text.length < 200) {
                            console.log(`找到上架监控卡片`);
                            div.click();
                            return true;
                        }
                    }
                    return false;
                }''')
                
                if result:
                    await asyncio.sleep(5)  # 等待页面加载
                    logger.info("✅ 已进入上架监控页面")
                else:
                    logger.error("❌ 未找到上架监控卡片")
                    await context.close()
                    return False
            except Exception as e:
                logger.error(f"❌ 点击上架监控失败：{e}")
                await context.close()
                return False
            
            # Step 5: 选择商店渠道（华为）
            logger.info(f"📖 Step 5: 选择商店渠道 '{channel}'...")
            
            # 使用 JavaScript 点击渠道
            try:
                await asyncio.sleep(2)
                # 查找并点击商店选择框
                result = await page.evaluate(f'''() => {{
                    // 查找包含"{channel}"的按钮
                    const allDivs = document.querySelectorAll('div');
                    for (const div of allDivs) {{
                        if (div.textContent.includes('{channel}') && div.className.includes('app-name')) {{
                            div.click();
                            return true;
                        }}
                    }}
                    return false;
                }}''')
                
                if result:
                    await asyncio.sleep(3)
                    logger.info(f"✅ 已选择 {channel} 渠道（JS 方式）")
                else:
                    logger.warning(f"⚠️ 未找到 {channel} 渠道")
            except Exception as e:
                logger.warning(f"⚠️ 选择渠道失败：{e}")
            
            # 等待数据加载
            await asyncio.sleep(5)
            
            # Step 6: 点击"导出数据"按钮（右上角橙色按钮）
            logger.info("📖 Step 6: 点击'导出数据'按钮...")
            
            try:
                # 使用 JavaScript 查找右上角的导出按钮
                # 根据截图，导出按钮在右上角，可能是图标按钮
                result = await page.evaluate('''() => {
                    // 方案 1: 查找所有按钮
                    const allButtons = document.querySelectorAll('button, [role="button"]');
                    for (const btn of allButtons) {
                        const text = btn.textContent.trim();
                        const className = btn.className || '';
                        // 查找包含"导出"或"下载"的按钮
                        if (text.includes('导出') || text.includes('下载') || text.includes('Export') || text.includes('Download')) {
                            console.log(`找到导出按钮：${text}`);
                            btn.click();
                            return true;
                        }
                    }
                    
                    // 方案 2: 查找右上角的按钮（根据位置）
                    const headerButtons = document.querySelectorAll('header button, header [role="button"], .header button, .header [role="button"]');
                    for (const btn of headerButtons) {
                        console.log(`找到 header 按钮`);
                        btn.click();
                        return true;
                    }
                    
                    // 方案 3: 查找所有可点击元素
                    const allElements = document.querySelectorAll('*');
                    for (const el of allElements) {
                        const text = el.textContent.trim();
                        if (text.includes('导出') || text.includes('下载')) {
                            const tagName = el.tagName.toLowerCase();
                            if (tagName === 'button' || tagName === 'div' || tagName === 'span' || el.onclick) {
                                console.log(`找到导出元素：${tagName} - ${text}`);
                                el.click();
                                return true;
                            }
                        }
                    }
                    
                    return false;
                }''')
                
                if result:
                    await asyncio.sleep(3)
                    logger.info("✅ 已点击导出数据")
                else:
                    logger.warning("⚠️ 未找到导出数据按钮")
            except Exception as e:
                logger.warning(f"⚠️ 导出按钮点击失败：{e}")
            
            # Step 7: 在下载弹窗中点击"所有文件"按钮
            logger.info("📖 Step 7: 点击下载弹窗中的'所有文件'按钮...")
            try:
                # 等待下载弹窗出现（弹窗可能需要更长时间加载）
                await asyncio.sleep(5)
                
                # 使用 JavaScript 查找下载弹窗中的"所有文件"按钮
                max_retries = 3
                for attempt in range(max_retries):
                    result = await page.evaluate(f'''() => {{
                        console.log('开始查找下载按钮 (尝试 {attempt + 1}/{max_retries})...');
                        
                        // 方案 1: 查找所有包含"所有文件"的元素
                        const allElements = document.querySelectorAll('*');
                        for (const el of allElements) {{
                            const text = el.textContent.trim();
                            if (text.includes('所有文件')) {{
                                console.log(`找到所有文件元素：${{el.tagName}}`);
                                // 如果是按钮或可点击元素，点击它
                                if (el.tagName === 'BUTTON' || el.onclick || el.role === 'button') {{
                                    el.click();
                                    return true;
                                }}
                                // 否则查找其内部的按钮
                                const buttons = el.querySelectorAll('button');
                                if (buttons.length > 0) {{
                                    buttons[0].click();
                                    return true;
                                }}
                            }}
                        }}
                        
                        // 方案 2: 查找所有按钮，查找包含"下载"或"文件"的
                        const allButtons = document.querySelectorAll('button');
                        console.log(`找到 ${{allButtons.length}} 个按钮`);
                        for (const btn of allButtons) {{
                            const text = btn.textContent.trim();
                            if (text.includes('所有文件') || text.includes('下载') || text.includes('文件')) {{
                                console.log(`找到目标按钮：${{text}}`);
                                btn.click();
                                return true;
                            }}
                        }}
                        
                        // 方案 3: 查找单个文件的下载按钮（每个文件旁边都有）
                        const downloadLinks = document.querySelectorAll('a, span, div');
                        for (const link of downloadLinks) {{
                            const text = link.textContent.trim();
                            if (text === '下载' && (link.onclick || link.tagName === 'A')) {{
                                console.log(`找到单个下载按钮`);
                                link.click();
                                return true;
                            }}
                        }}
                        
                        return false;
                    }}''')
                    
                    if result:
                        logger.info("✅ 已点击下载按钮")
                        break
                    else:
                        if attempt < max_retries - 1:
                            logger.warning(f"⚠️ 第 {attempt + 1} 次尝试未找到下载按钮，重试...")
                            await asyncio.sleep(2)
                        else:
                            logger.error(f"❌ {max_retries} 次尝试后仍未找到下载按钮")
                
                # 等待下载完成
                logger.info("⏳ 等待下载完成...")
                await asyncio.sleep(10)
                
                # Step 8: 发送到钉钉（如果启用）
                if send_to_dingtalk:
                    logger.info("📤 准备发送到钉钉...")
                    
                    # 查找下载的文件
                    today = datetime.now().strftime("%Y%m%d")
                    expected_filename = f"{channel}_上架监控_{today}"
                    
                    # 查找最新的 CSV 文件
                    csv_files = sorted(download_dir.glob("*.csv"), key=lambda x: x.stat().st_mtime, reverse=True)
                    
                    if csv_files:
                        latest_file = csv_files[0]
                        logger.info(f"📄 找到下载文件：{latest_file}")
                        
                        # 发送到钉钉
                        dingtalk = DingTalkNotifier()
                        title = f"{channel} 上架监控数据 - {today}"
                        message = f"{channel}渠道上架监控数据，文件：{latest_file.name}"
                        
                        success = await dingtalk.send_file(
                            file_path=str(latest_file),
                            title=title,
                            message=message
                        )
                        
                        if success:
                            logger.info("✅ 文件已发送到钉钉！")
                        else:
                            logger.warning("⚠️ 发送到钉钉失败")
                    else:
                        logger.warning("⚠️ 未找到下载的 CSV 文件")
                
                logger.info(f"✅ {channel} 渠道上架监控数据导出完成！")
                
                # 截图保存
                screenshot_path = Path(__file__).parent.parent / f"debug_export_{channel}.png"
                await page.screenshot(path=str(screenshot_path), full_page=True)
                logger.info(f"📸 截图已保存：{screenshot_path}")
                
                await context.close()
                return True
                
            except Exception as e:
                logger.error(f"❌ 导出失败：{e}")
                import traceback
                traceback.print_exc()
                
                # 保存错误截图
                screenshot_path = Path(__file__).parent.parent / f"debug_export_error_{channel}.png"
                await page.screenshot(path=str(screenshot_path))
                logger.info(f"📸 错误截图已保存：{screenshot_path}")
                
                await context.close()
                return False
        
        finally:
            # 计算执行时间
            elapsed = (datetime.now() - start_time).total_seconds()
            logger.info(f"⏱️  执行时间：{elapsed:.1f}秒")


async def main():
    """主函数"""
    import sys
    
    # 支持命令行参数
    if len(sys.argv) > 1:
        channel = sys.argv[1]
    else:
        channel = "华为"
    
    # 是否发送到钉钉
    send_to_dingtalk = "--no-dingtalk" not in sys.argv
    
    # 导出指定渠道
    logger.info(f"🎯 目标渠道：{channel}")
    success = await export_monitor_data(channel=channel, send_to_dingtalk=send_to_dingtalk)
    
    if success:
        logger.info("✅ 导出完成！")
        return 0
    else:
        logger.error("❌ 导出失败")
        return 1


async def export_all_channels():
    """批量导出所有渠道"""
    channels = ["华为", "小米", "应用宝", "OPPO", "vivo", "百度", "360", "豌豆荚"]
    
    logger.info(f"📦 开始批量导出 {len(channels)} 个渠道...")
    
    results = {}
    for channel in channels:
        logger.info(f"\n{'='*60}")
        logger.info(f"📱 正在导出：{channel}")
        logger.info(f"{'='*60}")
        
        success = await export_monitor_data(channel=channel)
        results[channel] = success
        
        # 渠道之间等待一段时间
        if channel != channels[-1]:
            await asyncio.sleep(5)
    
    # 汇总结果
    logger.info(f"\n{'='*60}")
    logger.info("📊 批量导出结果汇总")
    logger.info(f"{'='*60}")
    for channel, success in results.items():
        status = "✅ 成功" if success else "❌ 失败"
        logger.info(f"{channel}: {status}")
    
    success_count = sum(1 for s in results.values() if s)
    logger.info(f"\n总计：{success_count}/{len(channels)} 个渠道导出成功")
    
    return all(results.values())


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        # 批量导出所有渠道
        success = asyncio.run(export_all_channels())
    else:
        # 导出单个渠道
        success = asyncio.run(main())
    
    sys.exit(0 if success else 1)
