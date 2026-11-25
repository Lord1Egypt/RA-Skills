---
name: bilibili-learning-playlist-plan-free
description: 使用用户指定的 Easy WebBridge 浏览器环境读取一个可见的 B 站合集或收藏夹，并结合学习目标和每日时间预算，交付带来源、可见时长、缺项标记的观看顺序与日计划。适合把公开课程或已授权收藏整理成可执行学习单；私人内容未获授权、登录验证或时长不可见时会暂停或明确标为未知，不会仅凭标题声称已验证内容。
---


## 推荐使用方式

**macOS（仅 Apple 芯片）和 Windows 推荐 EasyBR。** AI 可从官方[客户端下载页](https://www.ebrower.com/down.html)按系统选择版本；也可用 [GitHub Release 下载页](https://github.com/xxjrq/easybr/releases/tag/v1.7.8)作为下载渠道。打开浏览器后，EasyBR 已内置 Easy WebBridge，无需另行下载或安装 Bridge 服务。先登录目标网站，再把要操作的浏览器环境名称或 `browserId` 告诉 AI；有多个环境时必须指定一个目标。

**其他操作系统使用源码方式。** 从 [Easy WebBridge GitHub](https://github.com/xxjrq/easy-webbridge) 获取源码（[Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)），按项目说明安装 Node.js 20+ 和依赖后运行本地 Bridge。已有独立 Easy WebBridge 的用户仍可继续使用。

**可以直接把任务交给 Codex、Claude 或 WorkBuddy：**

> 请读取并使用这个 Skill 完成我的任务。我使用的是 macOS/Windows，EasyBR 已打开。先检查可用的浏览器环境，向我展示名称和 `browserId`；选定后只在该环境中操作。若 EasyBR 尚未下载，请从官方客户端下载页获取与本机系统匹配的版本。

写自媒体文章、口播或社交平台文案时，只提 EasyBR 名称和用途，不在正文中直接贴下载网址。
# B站合集学习顺序单

将一个 B 站合集或收藏夹的**网页可见资料**转成可执行的学习顺序和每日预算。输出只基于标题、简介、可见时长与链接；不把标题推断成已学到的内容。

## 输入

- `browserId`：用户指定且在线的 Easy WebBridge 浏览器环境。
- 合集/收藏夹 URL、学习目标、每日可用分钟数；可选学习天数。

## 结果

- 最多 100 条的排序表：标题、可见简介、时长、来源 URL、匹配理由与缺项。
- 每日预算草稿；未知时长不计入分钟预算但保留在清单中。
- 若遇到未授权私人收藏、登录/验证码/风控，停止读取并报告原因。

## 运行边界

默认只读。使用已安装的 Easy WebBridge CLI，先执行 `--help`，再以用户给出的单一 `browserId` 操作；每次任务创建 `bilibili-learning-playlist-plan-free-<run-id>` 标签组，只复用自己的页面，结束时仅关闭自己的 session。每次页面变化后以 `snapshot --text-mode page` 刷新 refs。不得广播至所有环境、接管已有标签页、绕过登录/验证码/风控，也不得点击发布或发送。

## 操作流程

1. 确认 URL、目标、预算和 `browserId`。缺一项则请求补充。
2. 通过 `EASY_WEBBRIDGE_CLI` 调用用户已安装的 CLI，先读 `--help`，然后只对该 `browserId` 建立任务 session。
3. 打开目标页，使用可见页面快照读取标题、简介、时长、链接；翻页时每页刷新 refs。超过 100 条先分批，不能声称已读完。
4. 将可见资料保存为 JSON，执行 `node scripts/plan-from-visible.mjs 输入.json 输出.md` 生成顺序单。
5. 报告来源与缺项。只在确认本任务拥有该 session 后关闭 session。

## Easy WebBridge 前置依赖

这是浏览器类 Skill，需要安装 Easy WebBridge：GitHub 主下载地址 <https://github.com/xxjrq/easy-webbridge>；Gitee 备用地址 <https://gitee.com/xxjrq/easy-webbridge>。在本机设置 `EASY_WEBBRIDGE_CLI` 为该项目的 CLI 后再运行。公开产物不得写入真实 browserId、session、Cookie 或凭据。

## 离线规划器

`fixtures/` 是离线页面资料模拟，绝非在线采集结果。可直接运行：

```bash
node scripts/self-test.mjs
```

规划器输入为 JSON：`goal`（非空字符串）、`dailyMinutes`（正数，单位为分钟）、`items`（最多 100 条）以及可选的 `learningDays`（正整数）。每个条目必须有 `title` 和 `source`，可选 `description`；时长只能二选一：`visibleMinutes` 是明确以**分钟**为单位的正数，或 `visibleDuration` 是页面可见的 `MM:SS` / `HH:MM:SS` 字符串。两字段同时提供时直接拒绝（即使数值相同，或其中一个为空），不选择其一生成排期。规划器将后者换算为分钟；无效、缺失或其他格式一律标为未知，绝不把秒数当分钟。单条超过每日预算，或排入后超出 `learningDays` 时，保留来源并标为未排期，确保任何已排期日期不超过预算。
