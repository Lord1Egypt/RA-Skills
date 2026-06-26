---
name: "coding-plan-usage"
description: "Queries the remaining hours of Alibaba Cloud Coding Plan using a command-line tool. Invoke when user asks for Coding Plan usage."
---

# Coding Plan Usage Helper

用于查询阿里云 Coding Plan 余量的命令行工具。

## 何时使用

在以下场景主动调用：
- 用户希望“查询阿里云 Coding Plan余量”

## 执行流程

1. 直接运行 Python 脚本 `scripts/aliyun.py`
2. 若运行时报 `agent-browser` 不存在：先判断是否沙盒环境；仅真实环境缺失时安装依赖，否则提示用户：沙盒中找不到依赖是正常现象
3. 输出并解释结果

> 注意运行时的路径，切换到包含脚本的目录或使用完整路径执行。

## 如何运行

直接运行 Python 脚本 `scripts/aliyun.py`：

macOS / Linux:

```bash
python scripts/aliyun.py
```

Windows(PowerShell):

```powershell
python .\scripts\aliyun.py
```

如果命令存在，直接进入“输出解释规则”。

## 输出解释规则

- **未登录**：会自动打开阿里云首页并进入登录页，保存截图到当前目录`aliyu-login.png`，终端提示你扫码；扫码后再次运行即可。如果频道允许发送图片 你可以直接发给用户，否则可以帮用户打开图片。

截图完成后脚本会停止运行，当用户回复已经完成扫码登陆后，再次运行即可。

示例输出：

```text
Already logged in: false
Entered login page: true
请使用阿里云 App 扫码完成登录后，再次执行此程序以查询用量。
Login screenshot: /opt/coding-plan-usage/aliyu-login.png
Scan completed: false
```

- **已登录**：会自动进入 Coding Plan 页面并输出余量 JSON。

示例输出：

```json
{
  "hours5": {
    "usage": "0%",
    "resetTime": "2026-03-14 18:27:45"
  },
  "week": {
    "usage": "27%",
    "resetTime": "2026-03-16 00:00:00"
  },
  "month": {
    "usage": "15%",
    "resetTime": "2026-04-09 00:00:00"
  }
}
```

成功读取到用量后，程序会自动关闭浏览器会话。


