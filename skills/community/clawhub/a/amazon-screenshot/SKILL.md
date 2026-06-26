---
name: amazon-screenshot
description: 亚马逊 ASIN 页面截图工具。当用户提到"截图"、"asin截图"、"亚马逊截图"、"amazon screenshot"时触发。自动打开亚马逊ASIN详情页，支持人机校验自动点击，输出PNG截图并压缩为ZIP文档，最后通过MOSS邮箱发送到用户提供的飞书邮箱。
---

# Amazon Screenshot Skill

## 功能

截取亚马逊 ASIN 详情页图片，打包为 ZIP 压缩包，通过 MOSS 邮箱（moss@campsnail.com）发送到用户指定的邮箱。

## 核心规则

- 所有 ASIN 一次性截图，打包成 1 个 ZIP，发送 1 封邮件
- **发送完成后**：自动删除截图和 ZIP 文件，不占用服务器空间
- **邮箱限制**：只支持 `@campsnail.com` 域名邮箱，其他邮箱拒绝执行
- **并发限制**：脚本执行中时，新请求会提示"正在截图中，请等待"，避免同时执行

## 使用前提

用户需提供：
1. **ASIN 列表** - 要截图的亚马逊商品编码（单个或多个）
2. **收件邮箱** - 接收 ZIP 压缩包的邮箱地址（飞书邮箱）

## 使用示例

用户提供：
- ASIN：`B0GGD6242H B0GF7TF41C B0GF1MBLQT B0GF7TF41C B0GGD6242H B0GFMKRX3N B0FDKRSV72`
- 收件邮箱：`wangjunjie@campsnail.com`

→ 分两批执行（5+2），发送两封邮件

## 执行流程

1. 检查是否有其他实例在运行（有则提示等待）
2. 接收 ASIN 列表和收件邮箱
3. 所有 ASIN 一次性截图（每张间隔 2 秒）
4. 打包为 1 个 ZIP
5. 发送邮件
6. 删除截图文件和 ZIP

## 浏览器配置

- **模式**：有头模式（headless: false），在远程桌面的 Chrome 窗口中运行
- **DISPLAY 自动检测**：通过 Python 读取 X11 socket 属主自动获取当前活跃显示编号（默认 :10）
- **持久化登录状态**：使用独立 Profile 目录（`chrome_profile/`），保存 Cookie 和收货地址
- **反爬注入**：自动注入 Stealth 脚本，修补 navigator.webdriver 等自动化检测点

> 注意：运行截图时需要远程桌面 Chrome 窗口处于活跃状态（DISPLAY 检测依赖 X11）

## 并发说明

- 使用锁文件机制防止同时执行
- 执行中时新请求会收到提示，告知当前任务信息
- 任务完成或异常退出都会自动清理锁文件

## 行为约束

**主动通知**：任务全部完成后，必须在群里主动发送完成通知，告知用户邮件已发出、发了多少封、发送到哪个邮箱。不允许等用户来问再回复。

## 输出文件（临时）

- 截图：`skills/amazon-screenshot/outputs/<ASIN>_<时间戳>.png`
- ZIP 压缩包：`skills/amazon-screenshot/outputs/screenshots_<时间戳>.zip`

> 所有文件在邮件发送成功后自动删除

## 邮件主题

- 单批：`📦 亚马逊 ASIN 截图 - <时间戳>`
- 多批：`📦 亚马逊 ASIN 截图 (1/3) - <时间戳>`

## 脚本路径

`scripts/screenshot.js`
