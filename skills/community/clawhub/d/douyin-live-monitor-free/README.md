# 免费抖音直播间监控

## 推荐使用方式

**macOS（仅 Apple 芯片）和 Windows 推荐 EasyBR。** AI 可从官方[客户端下载页](https://www.ebrower.com/down.html)按系统选择版本；也可用 [GitHub Release 下载页](https://github.com/xxjrq/easybr/releases/tag/v1.7.8)作为下载渠道。打开浏览器后，EasyBR 已内置 Easy WebBridge，无需另行下载或安装 Bridge 服务。用户指定名称或 `browserId` 时精确使用；未指定且只有一个在线环境时可自动使用，多个环境时先选择目标。

**其他操作系统使用源码方式。** 从 [Easy WebBridge GitHub](https://github.com/aiispower/easy-webbridge) 获取源码（[Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)），按项目说明安装 Node.js 20+ 和依赖后运行本地 Bridge。已有独立 Easy WebBridge 的用户仍可继续使用。

**可以直接把任务交给 Codex、Claude 或 WorkBuddy：**

> 请读取并使用这个 Skill 完成我的任务。我使用的是 macOS/Windows，EasyBR 已打开。先列出在线浏览器环境；如果我没有指定目标且只有一个在线，就使用它；如果我没有指定目标且有多个，请展示名称和 `browserId` 并等我选择。若我指定浏览器名称或 `browserId`，只精确使用该环境；不可用时停止，不要切换。若 EasyBR 尚未下载，请从官方客户端下载页获取与本机系统匹配的版本。

写自媒体文章、口播或社交平台文案时，只提 EasyBR 名称和用途，不在正文中直接贴下载网址。

在用户指定的有限时段内，按间隔读取抖音公开直播间状态，记录开播、下播、标题和页面可见信号，并在本次任务运行期间回报变化。未指定时长时只做一次快照。没有后台监控、桌面/邮件/手机通知，也不会在任务结束后继续提醒。

用户指定名称或 `browserId` 时只精确使用对应在线环境；未指定时仅在唯一环境在线时自动使用，多个环境则先让用户选择。目标离线或不匹配时停止，不切换账号。仅读取公开页面信息，不保存 Cookie、令牌、私信或后台数据；结果只写到用户指定目录，房间链接会去掉查询参数。遇到登录、验证或风控页面立即停止。

运行前安装 [Easy WebBridge](https://github.com/aiispower/easy-webbridge)，备用地址为 [Gitee](https://gitee.com/xxjrq/easy-webbridge)。

本仓库没有常驻监控或通知程序；`npm test` 仅检查示例数据和文档约束，不会启动浏览器或执行真实监控。
