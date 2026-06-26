---
name: dingtalk-gui-message
description: 通过 macOS GUI 自动化给钉钉联系人发消息。使用 peekaboo + screencapture + Swift Vision OCR + cliclick 实现全流程自动化。触发词：钉钉发消息、给XX发消息、钉钉GUI、dingtalk message。
---

# 钉钉 GUI 自动化发消息

通过 macOS 桌面 GUI 自动化，搜索钉钉联系人并发送消息。

## 前置条件

- macOS（arm64, Retina）
- 已安装钉钉桌面客户端（com.alibaba.DingTalkMac）
- 已安装工具：peekaboo, cliclick, swift
- 已授权：Screen Recording + Accessibility

## 用法

```bash
python3 scripts/send_message.py "联系人名" "消息内容"
```

## 登录处理

脚本自动检测钉钉是否需要登录：
- 已登录 → 直接执行
- 未登录 → 截取二维码，输出 `{"needs_login": true, "qr_code": "路径"}`
- exit code: 0=成功, 1=失败, 2=需要登录

## 技术方案（4/13 + 4/23 验证通过）

### 截图策略（关键！）

| 场景 | 工具 | 理由 |
|------|------|------|
| 登录检测 | `peekaboo image --app` | 只截钉钉窗口，避免误识别其他窗口文字 |
| OCR 导航 | `screencapture -x` | 全屏 Retina，能捕获 WebView 内容 |
| 二维码截图 | `screencapture -x` | 确保二维码可见 |

### 坐标换算（4/23 修正）

```
Retina 截图: 3024×1964 像素
逻辑分辨率: 1512×982
换算: 逻辑坐标 = 像素坐标 ÷ 2
```

### 双引擎 OCR

| 引擎 | 用途 |
|------|------|
| Swift Vision OCR | 文字精确坐标 → cliclick |
| qwen3.6-plus vision | 语义理解，确认操作结果 |

### 核心原则（踩坑总结）

1. **bundleId**: 始终用 `com.alibaba.DingTalkMac`
2. **中文输入**: 只用 `peekaboo paste --text --app bundleId`
3. **WebView 点击**: 用 `cliclick`，不用 `peekaboo click`
4. **搜索词**: 用名字前两个字，不用全名
5. **窗口激活**: `osascript activate` + `peekaboo focus` 双重保障

## 工具链

| 工具 | 用途 |
|------|------|
| peekaboo | paste 中文、hotkey、press、窗口截图 |
| screencapture | 全屏 Retina 截图（捕获 WebView） |
| Swift Vision | OCR + 像素坐标 |
| cliclick | 逻辑坐标点击 |
| qwen-vl-max | 截图语义分析 |
