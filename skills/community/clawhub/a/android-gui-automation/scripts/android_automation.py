#!/usr/bin/env python3
"""
android_automation.py
多平台 Android GUI 自动化 — 淘宝/拼多多/小红书/抖音/京东 比价+发帖
支持 Hermes Agent crontab 定时执行
"""

import uiautomator2 as u2
import time
import json
import os
import re
import schedule
import requests
from datetime import datetime

# ============ 配置区 ============
DEVICE_IP = os.environ.get("ANDROID_DEVICE", "auto")
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")
TG_CHAT_ID = os.environ.get("TG_CHAT_ID", "")
DEFAULT_APPS = ["taobao", "pinduoduo", "jd"]
# =================================

APP_PACKAGES = {
    "taobao":     "com.taobao.taobao",
    "jd":         "com.jingdong.app.mall",
    "pinduoduo":  "com.xunmeng.pinduoduo",
    "xiaohongshu":"com.xingin.xhs",
    "douyin":     "com.ss.android.ugc.aweme",
    "wechat":     "com.tencent.mm",
    "meituan":    "com.sankuai.meituan",
    "weibo":      "com.sina.weibo",
    "bilibili":   "tv.danmaku.bili",
}

d = None

def connect():
    global d
    d = u2.connect(DEVICE_IP if DEVICE_IP != "auto" else None)
    return d

def open_app(package_name):
    """启动 APP"""
    d.app_stop(package_name)
    d.app_start(package_name)
    time.sleep(3)

def screenshot(name="screen"):
    """截图"""
    path = f"/sdcard/{name}_{int(time.time())}.png"
    d.screenshot(path)
    return path

def get_screen_text():
    """获取屏幕文字"""
    return d.dump_xml()

def wait_and_click(text, timeout=10):
    """等待并点击文字元素"""
    if d(text=text, timeout=timeout).exists:
        d(text=text).click()
        return True
    return False

def input_text(text):
    """输入文字"""
    d.set_fastinput_ime(True)
    d.send_keys(text)
    d.set_fastinput_ime(False)

def swipe_up():
    d.swipe(540, 1800, 540, 600)
    time.sleep(1)

def press_back():
    d.press("back")

# ============ 淘宝 ============
def taobao_search(keyword):
    open_app(APP_PACKAGES["taobao"])
    wait_and_click("搜索")
    time.sleep(1)
    input_text(keyword)
    time.sleep(0.5)
    wait_and_click("搜索", timeout=5)
    time.sleep(3)

def taobao_get_price():
    """读取第一个商品价格"""
    try:
        xml = get_screen_text()
        matches = re.findall(r'¥([\d.]+)', xml)
        if matches:
            return float(matches[0])
    except Exception as e:
        print(f"读取淘宝价格失败: {e}")
    return None

# ============ 拼多多 ============
def pinduoduo_search(keyword):
    open_app(APP_PACKAGES["pinduoduo"])
    wait_and_click("搜索")
    time.sleep(1)
    input_text(keyword)
    time.sleep(0.5)
    wait_and_click("搜索", timeout=5)
    time.sleep(3)

def pinduoduo_get_price():
    """读取拼多多价格"""
    try:
        xml = get_screen_text()
        matches = re.findall(r'单独购买¥([\d.]+)', xml)
        if matches:
            return float(matches[0])
        matches2 = re.findall(r'¥([\d.]+)', xml)
        if matches2:
            return float(matches2[0])
    except Exception as e:
        print(f"读取拼多多价格失败: {e}")
    return None

# ============ 小红书 ============
def xiaohongshu_post(content, tag="AI"):
    """发小红书图文笔记"""
    open_app(APP_PACKAGES["xiaohongshu"])
    wait_and_click("发布")
    time.sleep(2)
    wait_and_click("选择照片")
    time.sleep(2)
    # 选第一张
    d.xpath('//android.widget.ImageView[@index="0"]').click()
    time.sleep(1)
    wait_and_click("完成")
    time.sleep(1)
    input_text(content)
    time.sleep(1)
    wait_and_click("添加话题")
    time.sleep(0.5)
    input_text(f"#{tag}")
    time.sleep(0.5)
    press_back()
    time.sleep(0.5)
    wait_and_click("发布")
    time.sleep(3)
    if d(text="发布成功").exists or d(text="笔记发布成功").exists:
        return True
    return False

def xiaohongshu_search(keyword):
    """小红书搜索"""
    open_app(APP_PACKAGES["xiaohongshu"])
    # 寻找搜索入口（首页有搜索框）
    if d(text="搜索").exists:
        d(text="搜索").click()
        time.sleep(1)
        input_text(keyword)
        time.sleep(0.5)
        press_back()
        time.sleep(2)

# ============ 抖音 ============
def douyin_search(keyword):
    """抖音搜索"""
    open_app(APP_PACKAGES["douyin"])
    time.sleep(3)
    # 首页点击搜索按钮
    if d(description="搜索").exists:
        d(description="搜索").click()
        time.sleep(2)
        input_text(keyword)
        time.sleep(0.5)
        press_back()
        time.sleep(3)

def douyin_post(video_path, title, hashtags):
    """发抖音视频（需完整视频路径）"""
    open_app(APP_PACKAGES["douyin"])
    d(description="加号").wait(timeout=5)
    d(description="加号").click()
    time.sleep(2)
    wait_and_click("上传视频")
    time.sleep(2)
    # 选择视频（实际需要文件选择器交互，较复杂）
    # 此处简化，实际使用需要根据具体文件选择界面调整
    wait_and_click("下一步")
    time.sleep(2)
    input_text(title)
    time.sleep(1)
    for tag in hashtags:
        input_text(f"#{tag} ")
    time.sleep(1)
    wait_and_click("发布")
    time.sleep(5)

# ============ 京东 ============
def jd_search(keyword):
    open_app(APP_PACKAGES["jd"])
    wait_and_click("搜索")
    time.sleep(1)
    input_text(keyword)
    press_back()  # 触发搜索
    time.sleep(3)

def jd_get_price():
    try:
        xml = get_screen_text()
        matches = re.findall(r'¥([\d.]+)', xml)
        if matches:
            return float(matches[0])
    except:
        pass
    return None

# ============ 多平台比价 ============
def compare_price(keyword, platforms=None):
    """多平台同时比价"""
    if platforms is None:
        platforms = ["taobao", "pinduoduo", "jd"]
    
    results = {}
    for platform in platforms:
        print(f"[{datetime.now()}] 检查 {platform}...")
        try:
            if platform == "taobao":
                taobao_search(keyword)
                price = taobao_get_price()
            elif platform == "pinduoduo":
                pinduoduo_search(keyword)
                price = pinduoduo_get_price()
            elif platform == "jd":
                jd_search(keyword)
                price = jd_get_price()
            else:
                continue
            results[platform] = price
        except Exception as e:
            results[platform] = f"错误: {e}"
        time.sleep(2)
    
    return results

# ============ 通知 ============
def notify(message):
    if TG_BOT_TOKEN and TG_CHAT_ID:
        url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
        try:
            requests.post(url, data={
                "chat_id": TG_CHAT_ID,
                "text": message,
                "parse_mode": "Markdown"
            }, timeout=10)
        except Exception as e:
            print(f"通知失败: {e}")

# ============ 价格监控 ============
PRICE_HISTORY_FILE = "price_history.json"

def load_history():
    if os.path.exists(PRICE_HISTORY_FILE):
        with open(PRICE_HISTORY_FILE) as f:
            return json.load(f)
    return {}

def save_history(history):
    with open(PRICE_HISTORY_FILE, "w") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def price_monitor(keyword, target_price=0):
    """定时比价主函数"""
    print(f"[{datetime.now()}] 开始监控: {keyword}")
    results = compare_price(keyword)
    
    history = load_history()
    if keyword not in history:
        history[keyword] = []
    
    for platform, price in results.items():
        if isinstance(price, float):
            history[keyword].append({
                "time": datetime.now().isoformat(),
                "platform": platform,
                "price": price
            })
    
    save_history(history)
    
    # 生成报告
    report = f"📊 *{keyword}* 价格监控\n"
    for platform, price in results.items():
        if isinstance(price, float):
            report += f"• {platform}: ¥{price}\n"
        else:
            report += f"• {platform}: {price}\n"
    
    # 检查是否创历史新低
    all_prices = [h["price"] for h in history[keyword] if isinstance(h["price"], (int, float))]
    if all_prices:
        lowest = min(all_prices)
        current = list(results.values())[0]
        if isinstance(current, float) and current <= lowest:
            report += f"\n✨ 创历史新低！¥{current}"
    
    if target_price > 0:
        first_price = next((p for p in results.values() if isinstance(p, float)), None)
        if first_price and first_price <= target_price:
            report += f"\n✅ 已到目标价 ¥{target_price}！"
    
    print(report)
    notify(report)
    return results

# ============ CLI 入口 ============
if __name__ == "__main__":
    import sys
    connect()
    
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    
    if cmd == "compare":
        keyword = sys.argv[2] if len(sys.argv) > 2 else "iPhone 16"
        print(compare_price(keyword))
    
    elif cmd == "monitor":
        keyword = sys.argv[2] if len(sys.argv) > 2 else "iPhone 16"
        target = float(sys.argv[3]) if len(sys.argv) > 3 else 0
        price_monitor(keyword, target)
    
    elif cmd == "post":
        # python3 android_automation.py post xiaohongshu "内容" "标签"
        platform = sys.argv[2]
        content = sys.argv[3] if len(sys.argv) > 3 else "Hello World"
        tag = sys.argv[4] if len(sys.argv) > 4 else "AI"
        if platform == "xiaohongshu":
            success = xiaohongshu_post(content, tag)
            print(f"发布{'成功' if success else '失败'}")
    
    elif cmd == "screenshot":
        path = screenshot()
        print(f"截图: {path}")
    
    elif cmd == "search":
        # python3 android_automation.py search taobao iPhone
        platform = sys.argv[2] if len(sys.argv) > 2 else "taobao"
        keyword = sys.argv[3] if len(sys.argv) > 3 else "iPhone"
        if platform == "taobao":
            taobao_search(keyword)
        elif platform == "pinduoduo":
            pinduoduo_search(keyword)
        elif platform == "jd":
            jd_search(keyword)
        elif platform == "xiaohongshu":
            xiaohongshu_search(keyword)
        elif platform == "douyin":
            douyin_search(keyword)
        print(f"已在 {platform} 搜索: {keyword}")
    
    else:
        print("用法:")
        print("  python3 android_automation.py compare <商品>     # 多平台比价")
        print("  python3 android_automation.py monitor <商品> [目标价]  # 定时监控")
        print("  python3 android_automation.py search <平台> <关键词>  # 搜索")
        print("  python3 android_automation.py post <平台> <内容> [标签]  # 发帖")
        print("  python3 android_automation.py screenshot         # 截图")
        print()
        print("平台: taobao / pinduoduo / jd / xiaohongshu / douyin")
