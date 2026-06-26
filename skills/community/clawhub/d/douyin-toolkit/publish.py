#!/usr/bin/env python3
"""
douyin-publisher — 抖音视频发布工具

用法:
  # 首次使用（需要扫码登录一次）
  python3 publish.py --start-browser   # 启动Chrome（浏览器窗口出现后扫码登录）
  
  # 发布视频（登录态有效的情况）
  python3 publish.py --video xxx.mp4 --title "标题"
  
  # 连续发布多条，不关浏览器
  python3 publish.py --video xxx.mp4 --title "标题" --keep-alive
  
  # 如需验证码，收到后传入
  python3 publish.py --code 验证码
  
  # 自定义验证码等待超时（秒，默认120）
  python3 publish.py --video xxx.mp4 --title "标题" --code-timeout 300

说明:
  - 登录一次后，chrome_profile 保存登录态，后续自动登录
  - 不是每次都需要短信验证码，有时直接发布成功
  - 默认发布完关闭浏览器（--keep-alive 可保留）
  - VNC 只用于首次登录或排查问题，日常发布无需开启
"""
import sys, json, time, os, argparse, subprocess
from pathlib import Path

BASE_DIR = Path(__file__).parent
SCREENSHOTS = BASE_DIR / "screenshots"
USER_DATA_DIR = BASE_DIR / "chrome_profile"
CHROME_PATH = Path(os.path.expanduser(
    "~/.cache/ms-playwright/chromium-1223/chrome-linux64/chrome"
))
DEBUG_PORT = 9222
CDP_URL = f"http://127.0.0.1:{DEBUG_PORT}"
CODE_FILE = BASE_DIR / ".sms_code.txt"
STATE_FILE = BASE_DIR / ".publish_state.json"

for d in [SCREENSHOTS, USER_DATA_DIR]:
    d.mkdir(exist_ok=True)

from playwright.sync_api import sync_playwright


def _ensure_chrome():
    """确保Chrome正在运行，没有则启动（使用xvfb）"""
    try:
        import urllib.request
        urllib.request.urlopen(f"http://127.0.0.1:{DEBUG_PORT}/json/version", timeout=2)
        return True  # 已在运行
    except:
        pass
    
    subprocess.Popen(
        [str(CHROME_PATH), f"--remote-debugging-port={DEBUG_PORT}",
         f"--user-data-dir={str(USER_DATA_DIR)}",
         "--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage",
         "https://creator.douyin.com/"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        env={**os.environ, "DISPLAY": ":99"}
    )
    # 等Chrome启动
    for _ in range(20):
        time.sleep(1)
        try:
            import urllib.request
            urllib.request.urlopen(f"http://127.0.0.1:{DEBUG_PORT}/json/version", timeout=1)
            return True
        except:
            pass
    return False


def _stop_chrome():
    """关闭Chrome"""
    try:
        subprocess.run(["pkill", "-f", "chrome.*9222"], timeout=5,
                       capture_output=True)
    except:
        pass


def _check_login(page):
    """检查当前页面是否有扫码登录覆盖层"""
    body_text = page.evaluate('document.body.innerText')
    if '扫码登录' in body_text and '登录' in body_text and '抖音' in body_text:
        return False
    return True


def _save_error_screenshot(page, label):
    """出错时自动截图"""
    ts = time.strftime("%Y%m%d_%H%M%S")
    path = str(SCREENSHOTS / f"error_{label}_{ts}.png")
    try:
        page.screenshot(path=path)
        print(f"📸 截图已保存: {path}")
    except:
        pass


def start_browser():
    """启动Chrome+VNC（用于首次登录或排查问题）"""
    if _ensure_chrome():
        print("✅ Chrome已在运行，端口 {DEBUG_PORT}")
        return
    
    subprocess.Popen(
        [str(CHROME_PATH), f"--remote-debugging-port={DEBUG_PORT}",
         f"--user-data-dir={str(USER_DATA_DIR)}",
         "--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage",
         "https://creator.douyin.com/"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        env={**os.environ, "DISPLAY": ":1"}
    )
    time.sleep(8)
    
    try:
        import urllib.request
        urllib.request.urlopen(f"http://127.0.0.1:{DEBUG_PORT}/json/version", timeout=2)
        print("✅ Chrome已启动（端口9222），在浏览器中打开 http://localhost:9222 或 VNC 扫码登录")
    except:
        print("❌ Chrome启动失败")


def publish(video_path, title="", description="", keep_alive=False, code_timeout=120):
    """发布视频到抖音"""
    if not _ensure_chrome():
        print("❌ Chrome启动失败")
        _save_error_screenshot(None, "chrome_fail")
        return
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(CDP_URL)
            ctx = browser.contexts[0]
            page = ctx.new_page()
            
            # 1. 去上传页面
            print("📄 正在打开上传页面...")
            page.goto("https://creator.douyin.com/creator-micro/content/upload", timeout=30000)
            time.sleep(5)
            
            # 1a. 登录态预检：检查页面上是否有"扫码登录"
            if not _check_login(page):
                _save_error_screenshot(page, "need_login")
                print("❌ 需要扫码登录，请运行 python3 publish.py --start-browser")
                print("   登录成功后重新运行发布命令")
                return
            
            # 1b. 如果页面 URL 含 login 也是未登录
            if 'login' in page.url.lower():
                _save_error_screenshot(page, "redirect_login")
                print("❌ 被重定向到登录页，登录态已过期")
                print("   请运行 python3 publish.py --start-browser 重新扫码登录")
                return
            
            print("✅ 已登录，开始上传...")
            
            # 2. 放弃残留草稿（如果有）
            body_text = page.evaluate('document.body.innerText')
            if '继续编辑' in body_text:
                try:
                    # 找到"放弃"文字并点击
                    page.evaluate('''() => {
                        const all = document.querySelectorAll('span, button, div');
                        for (const el of all) {
                            if (el.innerText.trim() === '放弃') { 
                                el.click(); 
                                return true;
                            }
                        }
                        return false;
                    }''')
                    time.sleep(2)
                    print("🗑️ 已放弃上一个草稿")
                except:
                    pass
            
            # 3. 上传视频
            file_input = page.locator('input[type="file"]')
            if file_input.count() == 0:
                _save_error_screenshot(page, "no_file_input")
                print("❌ 找不到文件上传入口，页面可能未正确加载")
                return
            
            file_input.first.set_input_files(str(video_path))
            print("📤 视频上传中...")
            
            upload_ok = False
            for i in range(60):
                time.sleep(3)
                text = page.evaluate('document.body.innerText')
                # 上传完成后页面会显示"作品描述"或"高清发布"
                if '作品描述' in text or ('基础信息' in text and '发布' in text):
                    upload_ok = True
                    print(f"✅ 上传完成（约 {i*3 + 3}s）")
                    break
            if not upload_ok:
                _save_error_screenshot(page, "upload_timeout")
                print("⚠️ 上传超时，请检查网络")
                return
            
            # 4. 填写标题
            if title:
                title_input = page.locator('input[placeholder*="标题"]')
                if title_input.count() > 0:
                    title_input.first.click()
                    title_input.first.fill('')
                    time.sleep(0.5)
                    title_input.first.fill(title)
                    print(f"📝 标题已填写: {title}")
                else:
                    # 备选：填第一个 text 输入框
                    text_inputs = page.locator('input[type="text"]')
                    if text_inputs.count() > 0:
                        text_inputs.first.click()
                        text_inputs.first.fill('')
                        time.sleep(0.5)
                        text_inputs.first.fill(title)
                        print(f"📝 标题已填写（备选方式）: {title}")
            
            if description:
                desc_area = page.locator('div[contenteditable="true"]')
                if desc_area.count() > 0:
                    desc_area.first.fill(description)
                    print("📝 描述已填写")
            
            # 5. 尝试发布：先点"高清发布"，再备选点"发布"
            print("📢 点击发布...")
            page.evaluate("""
                document.querySelectorAll('button').forEach(b => {
                    if (b.innerText.trim() === '高清发布') b.click();
                });
            """)
            time.sleep(5)
            
            # 如果高清发布没反应（页面没变），试试"发布"按钮
            current_text = page.evaluate('document.body.innerText')
            if '作品描述' in current_text and '高清发布' in current_text:
                # 高清发布没成功，试"发布"按钮
                page.evaluate("""
                    document.querySelectorAll('button').forEach(b => {
                        if (b.innerText.trim() === '发布') b.click();
                    });
                """)
                time.sleep(5)
            
            # 检查是否进到发布状态
            text = page.evaluate('document.body.innerText')
            if '上传中' in text or '发布中' in text or '上传' in text:
                print("⏳ 开始发布流程...")
            elif '作品描述' in text:
                # 发布按钮没生效，JS 点击备用
                page.evaluate("""
                    const btns = document.querySelectorAll('button');
                    for (const b of btns) {
                        const t = b.innerText.trim();
                        if (t === '高清发布' || t === '发布') {
                            b.dispatchEvent(new MouseEvent('click', {bubbles: true}));
                            break;
                        }
                    }
                """)
                time.sleep(5)
            
            # 6. 检查是否需要短信验证
            verify_present = page.evaluate('() => !!document.querySelector("#uc-second-verify, .second-verify-mask")')
            if verify_present or '验证码' in page.evaluate('document.body.innerText'):
                print("\n🔐 短信验证码已发送到手机")
                
                with open(STATE_FILE, 'w') as f:
                    json.dump({"waiting_code": True}, f)
                
                # 点"获取验证码"发短信
                page.evaluate('''() => {
                    const el = document.querySelector(".uc-ui-input_right");
                    if (el) el.click();
                }''')
                time.sleep(2)
                
                CODE_FILE.unlink(missing_ok=True)
                code_received = False
                for _ in range(code_timeout):
                    if CODE_FILE.exists():
                        code = CODE_FILE.read_text().strip()
                        CODE_FILE.unlink(missing_ok=True)
                        # 填入验证码
                        code_input = page.locator('input[type="number"]')
                        if code_input.count() > 0:
                            code_input.first.fill(code)
                        else:
                            page.locator('input[placeholder*="验证码"]').first.fill(code)
                        time.sleep(1)
                        # 点击"验证"按钮
                        page.evaluate('''() => {
                            const btns = document.querySelectorAll('.uc-ui-button, button');
                            for (const b of btns) {
                                if (b.innerText.trim() === '验证') {
                                    if (!b.classList.contains('disabled')) {
                                        b.click();
                                        return true;
                                    }
                                }
                            }
                            return false;
                        }''')
                        time.sleep(8)
                        print("✅ 验证完成")
                        code_received = True
                        break
                    time.sleep(1)
                
                STATE_FILE.unlink(missing_ok=True)
                if not code_received:
                    print(f"⚠️ 验证码等待超时（{code_timeout}秒）")
                    _save_error_screenshot(page, "code_timeout")
                    return
            
            # 7. 确认发布结果
            print("⏳ 等待发布完成...")
            publish_ok = False
            for i in range(40):
                time.sleep(5)
                text = page.evaluate('document.body.innerText')
                
                if '发布成功' in text:
                    publish_ok = True
                    print("🎉 发布成功！")
                    _save_error_screenshot(page, "success")
                    break
                elif '上传中' not in text and '发布中' not in text:
                    # 上传/发布结束了
                    break
            
            if not publish_ok:
                # 管理页确认
                page.goto("https://creator.douyin.com/creator-micro/content/manage", timeout=30000)
                time.sleep(8)
                text = page.evaluate('document.body.innerText')
                _save_error_screenshot(page, "check_result")
                
                if title and title in text:
                    print("🎉 发布成功！")
                elif 'login' in page.url.lower():
                    print("❌ 登录失效")
                    _save_error_screenshot(page, "login_fail")
                else:
                    print("✅ 发布完成")
    except Exception as e:
        print(f"❌ 发布过程出错: {e}")
        # 尝试截图
        try:
            _save_error_screenshot(page, "exception")
        except:
            pass
    finally:
        if not keep_alive:
            _stop_chrome()
        else:
            print("💚 Chrome 保持运行（--keep-alive），可继续下一条发布")


def send_code(code):
    """发送验证码到等待中的进程"""
    if not STATE_FILE.exists():
        print("❌ 没有等待验证码的进程")
        return
    
    state = json.loads(STATE_FILE.read_text())
    if state.get("waiting_code"):
        CODE_FILE.write_text(code)
        print("✅ 验证码已投递")
    else:
        print("❌ 进程不在等待状态")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="抖音视频发布工具")
    parser.add_argument("--start-browser", action="store_true",
                        help="启动Chrome（首次扫码登录用）")
    parser.add_argument("--video", help="视频文件路径")
    parser.add_argument("--title", default="", help="视频标题")
    parser.add_argument("--description", default="", help="视频描述")
    parser.add_argument("--code", help="短信验证码")
    parser.add_argument("--keep-alive", action="store_true",
                        help="发布完成后保持Chrome运行，不关浏览器")
    parser.add_argument("--code-timeout", type=int, default=120,
                        help="短信验证码等待超时（秒），默认120")
    
    args = parser.parse_args()
    
    if args.start_browser:
        start_browser()
    elif args.code:
        send_code(args.code)
    elif args.video:
        if not Path(args.video).exists():
            print(f"❌ 文件不存在: {args.video}")
            sys.exit(1)
        publish(args.video, args.title, args.description,
                keep_alive=args.keep_alive, code_timeout=args.code_timeout)
    else:
        print("抖音视频发布工具")
        print("  首次登录:  python3 publish.py --start-browser")
        print("  发布视频:  python3 publish.py --video xxx.mp4 --title '标题'")
        print("  连续发布:  python3 publish.py --video xxx.mp4 --title '标题' --keep-alive")
        print("  传入验证:  python3 publish.py --code 验证码")
        print("  超时设置:  python3 publish.py --video xxx.mp4 --code-timeout 300")
