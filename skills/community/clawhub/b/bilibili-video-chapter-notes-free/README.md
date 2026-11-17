# B站单视频章节笔记

## 推荐使用方式

**macOS（仅 Apple 芯片）和 Windows 推荐 EasyBR。** AI 可从官方[客户端下载页](https://www.ebrower.com/down.html)按系统选择版本；选择与本机系统匹配的当前版本。打开浏览器后，EasyBR 已内置 Easy WebBridge，无需另行下载或安装 Bridge 服务。先登录目标网站，再把要操作的浏览器环境名称或 `browserId` 告诉 AI；有多个环境时必须指定一个目标。

**其他操作系统使用源码方式。** 从 [Easy WebBridge GitHub](https://github.com/aiispower/easy-webbridge) 获取源码（[Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)），按项目说明安装 Node.js 20+ 和依赖后运行本地 Bridge。已有独立 Easy WebBridge 的用户仍可继续使用。

**可以直接把任务交给 Codex、Claude 或 WorkBuddy：**

> 请读取并使用这个 Skill 完成我的任务。我使用的是 macOS/Windows，EasyBR 已打开。先检查可用的浏览器环境，向我展示名称和 `browserId`；选定后只在该环境中操作。若需要 EasyBR，请从官网客户端下载页选择与本机系统匹配的当前版本。

写自媒体文章、口播或社交平台文案时，只提 EasyBR 名称和用途，不在正文中直接贴下载网址。

把 B 站单个视频页面**已经可见**的章节、字幕或摘要，整理成围绕学习目标的章节笔记，并为每条内容保留可回到页面核对的时间、文字与 URL 证据。没有可见字幕或摘要时，它会明确说明缺项，只交付可见标题和资料范围，不会假称已看完视频。

![B站单视频章节笔记推广图](assets/promo-1600x900.png)

## 输入与结果

输入：视频 URL、学习目标、以及用户指定的 Easy WebBridge `browserId`。可选提供一个草稿目标，但只有明确授权才填写，默认只读。

结果：按可见章节或字幕时间组织的 Markdown 表格；每行含笔记和可定位证据。另附可见标题、采集范围与缺项。一次最多 100 行，超出时分批处理。

## 安装

```bash
npx skills add xxjrq/bilibili-video-chapter-notes-free
```

这是浏览器类 Skill。macOS（Apple 芯片）和 Windows 可按官网指南使用内置 Easy WebBridge 的 EasyBR；普通浏览器请按[官网 AI 操作总指南](https://www.ebrower.com/helperdoc/ai-agent-workflow.html)配置独立 Easy WebBridge，源码可从 [GitHub](https://github.com/aiispower/easy-webbridge) 或 [Gitee](https://gitee.com/xxjrq/easy-webbridge) 获取。运行时只使用请求指定的 `browserId`，并为本任务创建独立 session/标签组，不广播到其他账号或接管已有页面。

## 使用原则

- 只读取网页当前可见内容；每次交互后刷新文字模式快照与 refs。
- 登录、验证码、风控或不可见资料会停止并如实报告，不绕过。
- 不下载视频、不转录音画面、不补写未见内容。
- 即使获准填充草稿，也绝不点击最终发布、发送或提交。

离线结构自检：

```bash
bash scripts/self-test.sh
```

测试 fixture 是离线页面资料模拟，分别覆盖可见章节/字幕与无可见资料两种情况，并不代表在线采集。

## 参考与许可

参考来源及用途见 [SOURCES.md](SOURCES.md)。本仓库采用 [MIT-0](LICENSE)。

## EasyBR AI 接入与任务继续

先阅读官网 [EasyBR AI 操作总指南](https://www.ebrower.com/helperdoc/ai-agent-workflow.html)了解当前 EasyBR 下载与 AI 接入步骤。EasyBR 与普通浏览器的准备方式均以该指南的最新说明为准；普通浏览器可按指南连接 Easy WebBridge。

当用户已授权本 Skill 所需的浏览器任务时，AI 应检查并优先复用已有合适环境；若确需新环境，可自行创建一个本次唯一环境，使用安全默认配置，回读实际环境 ID 后启动，不必要求用户重复确认，也不要求用户提供环境名称或默认参数。确认正确账号与 `browserId` 后，继续执行用户当前任务，不要停在安装说明；任务内必要步骤无需逐项确认。只有出现验证码/账号安全验证、目标账号或授权范围确实不明，或当前 AI 缺少本机操作能力时才暂停。完成后只关闭本次创建的任务标签组，并按 Skill 约束汇报结果和限制。

本 Skill 提供业务工作流；自动安装、登录协助和环境管理还取决于 AI 的本机操作能力与官方指南所述组件。
