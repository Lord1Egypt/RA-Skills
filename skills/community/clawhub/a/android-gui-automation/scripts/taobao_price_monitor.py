---
name: android-gui-automation
description: Android GUI automation for Hermes Agent (Termux). Automate mobile apps (Taobao, WeChat, etc.) via uiautomator2 or Tasker/MacroDroid — take screenshots, click, swipe, extract text, monitor prices, schedule tasks. Use when: user mentions Android phone automation, mobile app control, Taobao price tracking, app scraping, phone task scheduling, or running GUI automation from Termux. Supports: uiautomator2 (no-root), Tasker/MacroDroid (root), ADB, cron scheduling, and Telegram/WeChat price alerts.
emoji: "📱"
---

# Android GUI Automation

让 Hermes Agent (Termux) 通过 uiautomator2 或 Tasker/MacroDroid 控制 Android APP，实现截图、点击、滑动、文本识别、比价监控、定时提醒等自动化操作。

## 核心功能

- 📸 截取屏幕并识别文字/元素
- 👆 模拟点击、滑动、输入
- 🔍 搜索商品、比价、监控价格
- ⏰ 定时任务 + 异常时推送通知
- 📱 支持淘宝、微信、京东等主流 APP

## 架构概览

```
Hermes Agent (Termux)
  │
  ├── 方案A: uiautomator2（无 Root，推荐）
  │     └── Python 脚本直接控制
  │
  └── 方案B: Tasker/MacroDroid（需 Root/自动化工具）
        └── Hermes → HTTP Intent → Tasker → 执行
```

---

## 方案A：uiautomator2（无 Root）

### 安装依赖

```bash
# Termux 里执行
pkg install python python-pip
pip install uiautomator2 pillow requests schedule

# 初始化（连接手机，需先开启 USB 调试）
python -m uiautomator2 init
```

### 连接方式

```python
import uiautomator2 as u2

# USB 连接（需 ADB）
d = u2.connect('<手机IP>:5555')  # 例: 192.168.1.100:5555

# 无线连接（同一 WiFi）
d = u2.connect()  # 自动发现
```

### 基础操作

```python
import uiautomator2 as u2

d = u2.connect()

# 截图保存
d.screenshot("screen.png")

# 点击坐标
d.click(500, 800)

# 文字点击（找"搜索"按钮并点击）
d(text="搜索").click()

# 滑动屏幕
d.swipe(500, 1000, 500, 300)  # 上滑
d.swipe(500, 1000, 200, 1000)  # 左滑

# 输入文字
d.set_fastinput_ime(True)
d.send_keys("iPhone 16")

# 等待元素出现
d(text="搜索").wait(timeout=10.0)
d.implicitly_wait(10)

# 读取屏幕文字
d.dump_xml()  # 获取 UI 层次结构
```

### 淘宝比价实战脚本

```python
#!/usr/bin/env python3
"""
taobao_price_monitor.py
淘宝商品价格监控 — 定时搜索、比价、通知
"""

import uiautomator2 as u2
import time
import json
import os
from datetime import datetime

DEVICE = os.environ.get("ANDROID_DEVICE", "auto")  # 自动发现或指定 IP
PRODUCT_KEYWORD = os.environ.get("PRODUCT", "iPhone 16 256GB")
TARGET_PRICE = float(os.environ.get("TARGET_PRICE", "6000"))  # 目标价格
CHECK_INTERVAL = 3600 * 6  # 每6小时检查一次
PRICE_HISTORY_FILE = "price_history.json"

d = u2.connect(DEVICE if DEVICE != "auto" else None)

def load_history():
    if os.path.exists(PRICE_HISTORY_FILE):
        with open(PRICE_HISTORY_FILE) as f:
            return json.load(f)
    return {}

def save_history(history):
    with open(PRICE_HISTORY_FILE, "w") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def open_taobao():
    """启动淘宝APP"""
    d.app_stop("com.taobao.taobao")
    d.app_start("com.taobao.taobao")
    time.sleep(3)
    d(text="搜索").wait(timeout=10)

def search_product(keyword):
    """搜索商品"""
    d(text="搜索").click()
    time.sleep(1)
    d.set_fastinput_ime(True)
    d.send_keys(keyword)
    time.sleep(1)
    d(text="搜索", className="android.widget.Button").click()
    time.sleep(4)  # 等待结果加载

def get_first_price():
    """读取第一个商品的价格"""
    try:
        # 淘宝价格通常在商品卡片下方
        price_elem = d.xpath(
            '//android.widget.TextView[contains(@text,"¥")]'
        ).first
        if price_elem:
            price_text = price_elem.get_text()
            # 提取数字
            import re
            price = re.findall(r'[\d.]+', price_text)
            if price:
                return float(price[0])
    except Exception as e:
        print(f"读取价格失败: {e}")
    return None

def check_price():
    """执行一次价格检查"""
    print(f"[{datetime.now()}] 开始检查: {PRODUCT_KEYWORD}")
    
    open_taobao()
    search_product(PRODUCT_KEYWORD)
    
    price = get_first_price()
    if price is None:
        print("无法获取价格")
        return None
    
    print(f"当前价格: ¥{price}")
    
    history = load_history()
    if PRODUCT_KEYWORD not in history:
        history[PRODUCT_KEYWORD] = []
    
    history[PRODUCT_KEYWORD].append({
        "time": datetime.now().isoformat(),
        "price": price
    })
    save_history(history)
    
    # 检查是否值得提醒
    prices = [p["price"] for p in history[PRODUCT_KEYWORD]]
    lowest = min(prices)
    current = price
    is_lowest = (current <= lowest and len(prices) > 1)
    is_below_target = current <= TARGET_PRICE
    
    if is_lowest or is_below_target:
        msg = f"🔔 *{PRODUCT_KEYWORD}*\n当前价格: ¥{current}\n历史最低: ¥{lowest}\n目标价: ¥{TARGET_PRICE}"
        if is_lowest:
            msg += "\n✨ 创历史新低！"
        if is_below_target:
            msg += "\n✅ 已到目标价！"
        send_notify(msg)
    
    return price

def send_notify(message):
    """发送通知 — 对接 Hermes 的 notify 端点"""
    import requests
    try:
        # 对接 Telegram Bot（需要配置 TG_BOT_TOKEN 和 CHAT_ID）
        bot_token = os.environ.get("TG_BOT_TOKEN")
        chat_id = os.environ.get("TG_CHAT_ID")
        if bot_token and chat_id:
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            requests.post(url, data={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"})
    except Exception as e:
        print(f"通知发送失败: {e}")

if __name__ == "__main__":
    import schedule
    check_price()  # 立即执行一次
    
    # 定时循环
    while True:
        schedule.run_pending()
        time.sleep(60)
