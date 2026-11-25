---
name: bilibili-channel-update-digest-free
description: 使用用户指定的 Easy WebBridge 浏览器环境和UP主主页，读取最多10条当前可见视频，交付含标题、日期、主题、链接、来源与缺项的近期更新摘要草稿；适合一次性核对公开更新。未显示发布时间的条目留空并继续整理其余可见视频；登录、验证码或风控则停止，不编造投稿时间、播放数据或采集结果。
---


## 推荐使用方式

**macOS（仅 Apple 芯片）和 Windows 推荐 EasyBR。** AI 可从官方[客户端下载页](https://www.ebrower.com/down.html)按系统选择版本；也可用 [GitHub Release 下载页](https://github.com/xxjrq/easybr/releases/tag/v1.7.8)作为下载渠道。打开浏览器后，EasyBR 已内置 Easy WebBridge，无需另行下载或安装 Bridge 服务。先登录目标网站，再把要操作的浏览器环境名称或 `browserId` 告诉 AI；有多个环境时必须指定一个目标。

**其他操作系统使用源码方式。** 从 [Easy WebBridge GitHub](https://github.com/xxjrq/easy-webbridge) 获取源码（[Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)），按项目说明安装 Node.js 20+ 和依赖后运行本地 Bridge。已有独立 Easy WebBridge 的用户仍可继续使用。

**可以直接把任务交给 Codex、Claude 或 WorkBuddy：**

> 请读取并使用这个 Skill 完成我的任务。我使用的是 macOS/Windows，EasyBR 已打开。先检查可用的浏览器环境，向我展示名称和 `browserId`；选定后只在该环境中操作。若 EasyBR 尚未下载，请从官方客户端下载页获取与本机系统匹配的版本。

写自媒体文章、口播或社交平台文案时，只提 EasyBR 名称和用途，不在正文中直接贴下载网址。
# B站UP主近期更新摘要

把一个指定 UP 主主页中**当前可见**的最多 10 条视频，整理成可核对的更新摘要。输入是用户明确提供的 `browserId` 与主页 URL；结果是标题、日期、主题、链接、来源和缺项，而不是监控、私密运营分析或发布操作。

## 前置依赖

本 Skill 需要安装并连接 [Easy WebBridge](https://github.com/xxjrq/easy-webbridge)。GitHub 为主下载地址，Gitee 备用：[gitee.com/xxjrq/easy-webbridge](https://gitee.com/xxjrq/easy-webbridge)。在目标浏览器安装扩展并确认其已连接后，使用用户指定的单个 `browserId`；不要广播到其他账号环境。

运行前先阅读 CLI 帮助：

```bash
node /path/to/easy-webbridge/cli/easy-webbridge.mjs --help
```

`/path/to/easy-webbridge` 是用户本机安装目录，不应写入公开产物或输出。

## 执行流程

1. 确认用户给出单一 `browserId`、UP 主主页 URL，并说明只读取当前可见内容。
2. 创建仅属于本次工作的 session：`bilibili-channel-update-digest-free-<run-id>`；使用该 session 和简短分组标题新开首个标签页。后续只复用该 session。不得接管、登记或关闭已有页面。
3. 导航后使用 `snapshot <browserId> <tabId> --compact --visibility visible --text-mode page` 获取页面文字；页面变化、滚动或点击后及时重新快照，刷新 refs。只读取网页上可见资料。
4. 从当前可见视频卡片提取不超过 10 条：标题、页面显示的日期、可概括的主题、视频链接，以及该主页/卡片作为来源。日期未显示则为空；主题无法可靠判断则写“未能从可见标题判断”。不要推断投稿时间、播放数据或未显示资料。
5. 遇到登录页、验证码、风控或账号安全验证，立刻停止，不绕过；交付已读取项目和阻塞原因。默认只读。用户明确授权草稿填充时，最多填写草稿字段，绝不点击最终发布或发送。
6. 输出摘要后，关闭前核对 session 名称确为本次创建；只关闭该 session。

## 输出格式

```markdown
# UP主近期更新摘要

来源主页：<用户提供的URL>
采集范围：当前可见的 <n>/最多10 条视频
状态：完成｜部分完成（说明原因）

| # | 标题 | 日期 | 主题 | 链接 | 可见来源 |
|---|---|---|---|---|---|
| 1 | … | 2026-… 或留空 | … | https://www.bilibili.com/video/... | 主页当前可见视频卡片 |

缺项与限制：
- 未显示发布时间的条目已留空。
- 本摘要不包含未显示的播放数据或投稿时间。
```

离线结构验证运行 `node scripts/self-test.mjs`；fixtures 是离线页面资料模拟，绝不代表在线采集或账号测试。
