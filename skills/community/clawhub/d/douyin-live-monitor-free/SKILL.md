---
name: douyin-live-monitor-free
description: Monitor publicly visible Douyin live-room status through exactly one precisely selected or only online existing browser and produce timestamped snapshots. Report changes only while the requested task is actively running; this Skill has no background monitor or operating-system notification. Use when the user asks whether a Douyin creator is live, wants a bounded check of several rooms, track titles or public activity signals, or prepare a monitoring report without an API key.
---


## 推荐使用方式

**macOS（仅 Apple 芯片）和 Windows 推荐 EasyBR。** AI 可从官方[客户端下载页](https://www.ebrower.com/down.html)按系统选择版本；也可用 [GitHub Release 下载页](https://github.com/xxjrq/easybr/releases/tag/v1.7.8)作为下载渠道。打开浏览器后，EasyBR 已内置 Easy WebBridge，无需另行下载或安装 Bridge 服务。用户可指定名称或 `browserId`；未指定时仅在一个环境在线时自动使用，有多个环境时先选择目标。

**其他操作系统使用源码方式。** 从 [Easy WebBridge GitHub](https://github.com/aiispower/easy-webbridge) 获取源码（[Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)），按项目说明安装 Node.js 20+ 和依赖后运行本地 Bridge。已有独立 Easy WebBridge 的用户仍可继续使用。

**可以直接把任务交给 Codex、Claude 或 WorkBuddy：**

> 请读取并使用这个 Skill 完成我的任务。我使用的是 macOS/Windows，EasyBR 已打开。先列出在线浏览器环境；如果只有一个在线且我没有指定目标，就使用它；如果有多个，请展示名称和 `browserId` 并等我选择。若我指定浏览器名称或 `browserId`，只精确使用该环境；不可用时停止，不要切换。若 EasyBR 尚未下载，请从官方客户端下载页获取与本机系统匹配的版本。

写自媒体文章、口播或社交平台文案时，只提 EasyBR 名称和用途，不在正文中直接贴下载网址。
# 免费抖音直播间监控

在用户指定的有限时段内，按指定间隔读取抖音直播间公开页面状态，记录开播、下播、标题和页面可见信号。默认只读和记录，不自动互动、不发言、不录屏。本 Skill 没有常驻后台监控、系统通知或任务结束后的提醒功能；状态变化只能在本次任务运行期间回报。

## 输入

- 一个或多个抖音直播间链接或账号主页；只接受 HTTPS 的 `live.douyin.com` 房间链接或 `www.douyin.com/user/...` 主页链接，拒绝外站、本地地址和其他协议。
- 可选：检查间隔、持续时间、是否需要本次运行期间的状态变化回报、输出目录。未给持续时间时只做一次快照，不启动无期限轮询。
- 用户可指定浏览器显示名或 `browserId`，按完整值精确匹配。若未指定且恰好只有一个在线环境，可使用该环境；若有多个在线环境且目标不明确，先列出名称和 `browserId` 并等待用户选择。指定目标离线或不匹配时立即失败，绝不改用其他环境。监控多个账号时每个账号都必须明确指定唯一环境；同一浏览器内串行读取。

## 操作步骤

1. 列出在线浏览器。用户指定显示名或 `browserId` 时精确匹配该值；仅当用户未指定且恰好只有一个环境在线时才自动使用。多个在线环境且目标不明确时停止并请用户选择；指定环境离线或不匹配时立即失败，绝不改用其他账号或环境。
2. 为本任务创建 `douyin-live-monitor-free-<run-id>` 标签组，只在该组中打开页面；保留所有用户原有页面，不导航或关闭它们。
3. 确认目标页是公开直播/主页内容。遇到登录墙、验证码、风控、账号安全验证或无法确认页面状态时立即停止并返回 `needs_user_action`，不切换身份、不重试其他环境、不绕过限制。
4. 只读取公开页面可见信息：直播状态、标题、主播显示名和可见热度信号。不要读取或保存 Cookie、令牌、私信、后台分析、非公开数据或不相关个人信息。
5. 在用户指定的有限时段内按指定间隔轮询；多个房间串行处理。保存每次快照并计算状态变化（`started`、`still_live`、`ended`、`unavailable`）。
6. 运行期间在当前对话回报状态变化，并按需在用户指定目录生成 JSON/CSV/Markdown 结果。输出中的房间 URL 删除查询参数和片段，不记录浏览器凭据或请求头。
7. 页面不可访问或字段不可见时保留失败记录，不猜测在线人数。完成或失败后只关闭本次创建的标签组。

## 结果要求

每条快照至少包含 `room_url`、`creator_name`、`status`、`title`、`visible_metrics`、`collected_at`。报告明确检查间隔和最后一次成功读取时间。

## 失败处理

- 页面未加载：等待后重读一次；仍失败标记 `unavailable`。
- 登录、验证码、风控：停止并返回 `needs_user_action`，不绕过限制。
- 没有公开在线人数：记录为空，不以页面外数据补全。

## 隐私和提醒边界

- 用户指定名称或 `browserId` 时精确匹配；未指定时仅在唯一环境在线时使用。任何身份不匹配或不可用都停止，不自动挑选或切换账号。
- 本 Skill 复用浏览器现有登录态，但只读取公开页面字段；不得导出 Cookie、访问令牌、私信、账号后台或未公开数据。
- 输出仅包含用户要求的快照和汇总；房间链接剥除 query/hash。不得上传结果、发送消息或创建外部通知。
- 状态变化回报只在本次监控任务运行期间有效；任务结束后不会后台继续，也不会发桌面、邮件或手机通知。
- 该仓库没有可执行的常驻监控器；`scripts/self-test.mjs`只检查示例结构和 Skill 合约，不连接浏览器或采集真实直播数据。

## 运行前提

安装 <https://github.com/aiispower/easy-webbridge>；备用镜像 <https://gitee.com/xxjrq/easy-webbridge>。免费使用，不需要第三方 API Key。

## 自检

```bash
node scripts/self-test.mjs
```
