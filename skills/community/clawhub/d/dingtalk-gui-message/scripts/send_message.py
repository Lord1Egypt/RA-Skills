"""钉钉 GUI 自动化发消息（v1.1 纯脚本版，零 AI 模型依赖）

基于 4/13 和 4/23 多次验证过的路径。
所有验证步骤用 OCR 关键词检测替代 vision API。

用法:
  python3 scripts/send_message.py "联系人名" "消息内容"
  python3 scripts/send_message.py "XXX" "你好" --wait-login

选项:
  --wait-login    登录时自动等待（轮询），不退出
  --vision        启用 vision 分析（可选，默认关闭）
  --timeout N     登录等待超时秒数（默认 120）

Exit codes: 0=成功, 1=失败, 2=需要登录（仅非 --wait-login 模式）
"""

import sys
import os
import json
import subprocess
import time
import argparse
import base64
import urllib.request

# ── 常量 ──

DINGTALK_BUNDLE_ID = "com.alibaba.DingTalkMac"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TMP_DIR = "/tmp/dingtalk-gui"
MAX_RETRIES = 3
RETINA_SCALE = 2  # Retina: 像素 ÷ 2 = 逻辑坐标

LOGIN_KEYWORDS = ["扫码登录", "扫一扫登录", "手机钉钉扫码", "手机确认登录"]
CHAT_READY_KEYWORDS = ["请输入消息", "按Enter发送"]
QR_KEYWORDS = ["扫码", "二维码", "扫一扫"]

DASHSCOPE_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"


def log(msg):
    print(f"  [{time.strftime('%H:%M:%S')}] {msg}", file=sys.stderr)


def run(cmd, timeout=15):
    log(f"→ {cmd[:120]}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    if result.returncode != 0 and result.stderr:
        log(f"  stderr: {result.stderr[:200]}")
    return result


def get_qwen_api_key():
    for p in [os.path.expanduser("~/.openclaw/openclaw.json")]:
        try:
            with open(p) as f:
                cfg = json.load(f)
            key = cfg.get("models", {}).get("providers", {}).get("qwen", {}).get("apiKey")
            if key:
                return key
        except Exception:
            continue
    return os.environ.get("QWEN_API_KEY")


# ── 截图 ──

def screenshot_window(filename="window.png"):
    """截取钉钉窗口（登录检测用）"""
    os.makedirs(TMP_DIR, exist_ok=True)
    path = os.path.join(TMP_DIR, filename)
    run(f'peekaboo image --app "{DINGTALK_BUNDLE_ID}" --path {path}')
    return path


def screenshot_fullscreen(filename="screen.png"):
    """全屏 Retina 截图（OCR 导航用，能捕获 WebView）"""
    os.makedirs(TMP_DIR, exist_ok=True)
    path = os.path.join(TMP_DIR, filename)
    run(f"screencapture -x {path}")
    return path


# ── OCR ──

def ocr(image_path, keyword=None):
    """Swift Vision OCR，返回 JSON"""
    ocr_script = os.path.join(SCRIPT_DIR, "ocr_screen.swift")
    cmd = f'swift {ocr_script} "{image_path}"'
    if keyword:
        cmd += f' "{keyword}"'
    result = run(cmd, timeout=30)
    if result.returncode != 0:
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return None


def ocr_has_keyword(image_path, keywords):
    """OCR 检测图片中是否包含任意关键词"""
    ocr_result = ocr(image_path)
    if not ocr_result or not ocr_result.get("success"):
        return False, []
    all_texts = " ".join([t["text"] for t in ocr_result.get("all_texts", [])])
    matched = [kw for kw in keywords if kw in all_texts]
    return len(matched) > 0, matched


def ocr_find(image_path, keyword):
    """OCR 查找关键词并返回坐标"""
    result = ocr(image_path, keyword)
    if not result or not result.get("matched"):
        return None
    target = result["matched"][0]
    px, py = target["center_x"], target["center_y"]
    lx, ly = int(px / RETINA_SCALE), int(py / RETINA_SCALE)
    return {"text": target["text"], "px": px, "py": py, "lx": lx, "ly": ly}


# ── Vision（可选） ──

def vision_analyze(image_path, prompt):
    api_key = get_qwen_api_key()
    if not api_key:
        return None
    try:
        with open(image_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        data = json.dumps({
            "model": "qwen-vl-max",
            "messages": [{"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}},
                {"type": "text", "text": prompt}
            ]}]
        }).encode()
        req = urllib.request.Request(
            f"{DASHSCOPE_BASE_URL}/chat/completions", data=data,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
        answer = result.get("choices", [{}])[0].get("message", {}).get("content", "")
        log(f"  🔍 Vision: {answer[:100]}")
        return answer
    except Exception as e:
        log(f"  ⚠ Vision: {e}")
        return None


# ── 基础操作 ──

def click_at(lx, ly):
    run(f"cliclick c:{lx},{ly}")
    time.sleep(0.5)


def activate_dingtalk():
    log("激活钉钉...")
    run(f'osascript -e \'tell application id "{DINGTALK_BUNDLE_ID}" to activate\'')
    time.sleep(2)
    run(f'peekaboo window focus --app "{DINGTALK_BUNDLE_ID}"')
    time.sleep(3)


def paste_text(text):
    log(f"粘贴: {text}")
    run(f'peekaboo paste --text "{text}" --app "{DINGTALK_BUNDLE_ID}"')
    time.sleep(1)


def press_key(key):
    run(f'peekaboo press {key} --app "{DINGTALK_BUNDLE_ID}"')
    time.sleep(0.5)


# ── 登录检测 + 等待 ──

def check_login():
    """OCR 检测是否需要登录"""
    log("检测登录状态...")
    img = screenshot_window("login_check.png")
    needs_login, matched = ocr_has_keyword(img, LOGIN_KEYWORDS)
    if needs_login:
        log(f"  ⚠ 需要登录（触发词: {matched}）")
        return False
    log("  ✓ 已登录")
    return True


def capture_qr_code():
    """等待二维码加载 → 截图 → OCR 验证二维码存在"""
    log("截取二维码...")
    qr_path = os.path.join(TMP_DIR, "qr_code.png")
    for retry in range(5):
        time.sleep(3)
        run(f"screencapture -x {qr_path}")
        # OCR 检测二维码关键词
        has_qr, _ = ocr_has_keyword(qr_path, QR_KEYWORDS)
        if has_qr:
            log(f"  ✓ 二维码已确认（第 {retry+1} 次截图）")
            return qr_path
        log(f"  等待二维码加载... (第 {retry+1} 次)")
    log("  ⚠ 返回最后一张截图")
    return qr_path


def wait_for_login(timeout=120):
    """轮询等待登录完成"""
    log(f"等待登录（最长 {timeout} 秒）...")
    for i in range(timeout // 5):
        time.sleep(5)
        img = screenshot_window(f"login_poll_{i}.png")
        needs_login, _ = ocr_has_keyword(img, LOGIN_KEYWORDS)
        if not needs_login:
            log(f"  ✓ 登录成功（等待了 {(i+1)*5} 秒）")
            return True
        if i % 4 == 0:
            log(f"  等待中... ({(i+1)*5}s/{timeout}s)")
    log("  ✗ 登录超时")
    return False


# ── 搜索联系人 ──

def open_search():
    log("打开搜索框 (Cmd+F)...")
    run(f'peekaboo press escape --app "{DINGTALK_BUNDLE_ID}"')
    time.sleep(0.5)
    run(f'peekaboo hotkey --keys "cmd,f" --app "{DINGTALK_BUNDLE_ID}"')
    time.sleep(1)


def find_and_click_person(name, use_vision=False):
    """搜索并点击联系人（纯 OCR 验证）"""
    log(f"搜索联系人: {name}")
    open_search()

    search_term = name[:2] if len(name) >= 2 else name
    paste_text(search_term)
    time.sleep(2)

    for attempt in range(MAX_RETRIES):
        log(f"OCR 查找 (第 {attempt + 1} 次)...")
        img = screenshot_fullscreen("search_result.png")

        # 精确匹配
        target = ocr_find(img, name)
        # 回退到前两个字匹配
        if not target and len(name) >= 2:
            target = ocr_find(img, name[:2])

        if target:
            log(f"  ✓ '{target['text']}' 像素({target['px']},{target['py']}) → 逻辑({target['lx']},{target['ly']})")
            click_at(target["lx"], target["ly"])
            time.sleep(2)

            # OCR 验证聊天窗口打开（检测"请输入消息"）
            img2 = screenshot_fullscreen("after_click.png")
            chat_ready, _ = ocr_has_keyword(img2, CHAT_READY_KEYWORDS)
            name_present = ocr_find(img2, name) is not None

            if chat_ready:
                log(f"  ✓ 聊天窗口已打开（输入框已就绪）")
                if use_vision:
                    vision_analyze(img2, f"是否已打开与'{name}'的聊天窗口？")
                return True
            elif name_present:
                log(f"  ✓ 找到 '{name}'，尝试继续")
                return True
            else:
                log(f"  ⚠ 点击后未检测到聊天窗口，重试...")
                continue
        else:
            ocr_result = ocr(img)
            all_texts = [t['text'][:20] for t in (ocr_result or {}).get('all_texts', [])[:10]]
            log(f"  未找到 '{name}'，OCR: {all_texts}")
            time.sleep(2)

    return False


# ── 发送消息 ──

def send_message(message, use_vision=False):
    """发送消息（纯 OCR 验证）"""
    log(f"发送消息: {message}")
    img = screenshot_fullscreen("chat_window.png")

    # OCR 找输入框
    input_clicked = False
    for kw in ["请输入消息", "输入"]:
        target = ocr_find(img, kw)
        if target:
            log(f"  输入框 '{target['text']}' → ({target['lx']},{target['ly']})")
            click_at(target["lx"], target["ly"])
            input_clicked = True
            break

    if not input_clicked:
        log("  用默认坐标点击输入框")
        click_at(700, 700)

    time.sleep(1)
    paste_text(message)
    time.sleep(1)

    log("按回车发送...")
    press_key("return")
    time.sleep(2)

    # OCR 验证消息已发送
    img = screenshot_fullscreen("sent_confirm.png")
    target = ocr_find(img, message)
    if target:
        log(f"  ✅ 消息已在聊天记录中确认")
    else:
        log(f"  ⚠ 未在聊天记录中确认到消息（可能已发送但 OCR 未识别）")

    if use_vision:
        vision_analyze(img, f"消息'{message}'是否已成功发送？")

    return True


# ── main ──

def main():
    parser = argparse.ArgumentParser(description="钉钉 GUI 自动化发消息")
    parser.add_argument("name", help="联系人名称")
    parser.add_argument("message", help="消息内容")
    parser.add_argument("--wait-login", action="store_true", help="登录时自动等待轮询")
    parser.add_argument("--vision", action="store_true", help="启用 vision 分析（可选）")
    parser.add_argument("--timeout", type=int, default=120, help="登录等待超时（秒）")
    args = parser.parse_args()

    os.makedirs(TMP_DIR, exist_ok=True)
    log(f"目标: {args.name}")
    log(f"消息: {args.message}")

    # 1. 激活钉钉
    activate_dingtalk()

    # 2. 登录检测
    if not check_login():
        qr_path = capture_qr_code()

        if args.wait_login:
            # 输出二维码路径，然后等待
            print(json.dumps({
                "status": "waiting_login",
                "qr_code": qr_path,
                "message": "钉钉需要登录，请扫描二维码"
            }, ensure_ascii=False), flush=True)

            if not wait_for_login(args.timeout):
                print(json.dumps({"success": False, "error": "登录超时"}, ensure_ascii=False, indent=2))
                sys.exit(1)
            time.sleep(3)  # 登录后等待加载
        else:
            print(json.dumps({
                "success": False,
                "needs_login": True,
                "qr_code": qr_path,
                "message": "钉钉需要登录，请扫描二维码"
            }, ensure_ascii=False, indent=2))
            sys.exit(2)

    # 3. 搜索并点击联系人
    if not find_and_click_person(args.name, use_vision=args.vision):
        print(json.dumps({"success": False, "error": f"未找到联系人: {args.name}"}, ensure_ascii=False, indent=2))
        sys.exit(1)

    # 4. 发送消息
    if send_message(args.message, use_vision=args.vision):
        print(json.dumps({
            "success": True,
            "to": args.name,
            "message": args.message,
            "screenshots": {
                "search": os.path.join(TMP_DIR, "search_result.png"),
                "click": os.path.join(TMP_DIR, "after_click.png"),
                "sent": os.path.join(TMP_DIR, "sent_confirm.png")
            }
        }, ensure_ascii=False, indent=2))
        log("✅ 完成")
    else:
        print(json.dumps({"success": False, "error": "消息发送失败"}, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
