# B站简介资料链接索引

## 推荐使用方式

**macOS（仅 Apple 芯片）和 Windows 推荐 EasyBR。** AI 可从官方[客户端下载页](https://www.ebrower.com/down.html)按系统选择版本；选择与本机系统匹配的当前版本。打开浏览器后，EasyBR 已内置 Easy WebBridge，无需另行下载或安装 Bridge 服务。先登录目标网站，再把要操作的浏览器环境名称或 `browserId` 告诉 AI；有多个环境时必须指定一个目标。

**其他操作系统使用源码方式。** 从 [Easy WebBridge GitHub](https://github.com/aiispower/easy-webbridge) 获取源码（[Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)），按项目说明安装 Node.js 20+ 和依赖后运行本地 Bridge。已有独立 Easy WebBridge 的用户仍可继续使用。

**可以直接把任务交给 Codex、Claude 或 WorkBuddy：**

> 请读取并使用这个 Skill 完成我的任务。我使用的是 macOS/Windows，EasyBR 已打开。先检查可用的浏览器环境，向我展示名称和 `browserId`；选定后只在该环境中操作。若需要 EasyBR，请从官网客户端下载页选择与本机系统匹配的当前版本。

写自媒体文章、口播或社交平台文案时，只提 EasyBR 名称和用途，不在正文中直接贴下载网址。

把指定 B 站视频简介中作者公开的学习与工具资料，整理成可核对的链接清单。你提供 1–3 个视频 URL 和 `browserId`；Skill 交付每条链接的来源、可见用途、可访问状态，以及无法读取或打开时的原因，不会假称资料已经下载。

![B站简介资料链接索引推广图](assets/promo.png)

## 安装

```bash
npx skills add xxjrq/bilibili-description-source-index-free
```

这是浏览器 Skill。安装 [Easy WebBridge（GitHub）](https://github.com/aiispower/easy-webbridge)，或使用 [Gitee 备用地址](https://gitee.com/xxjrq/easy-webbridge)。运行时由用户提供 `browserId`；一项任务只管理自己的 session 和标签组，不接管已有页面。

## 输入与结果

输入：一个 Easy WebBridge `browserId`、1–3 个 B站视频 URL，以及可选的本地整理要求。

结果：JSON/表格草稿，包含 `source_video`、`url`、`purpose`、`access`、`evidence`，并在 `gaps` 中记录简介不可见、需登录或链接打不开等原因。默认只读；若授权填充草稿，也绝不点击最终发布或发送。

只处理网页可见内容。遇到登录、验证码或风控会停止并如实记录，不绕过限制。单次最多 100 行；更多内容需分批。

## 本地验证

```bash
node scripts/self-test.mjs
```

fixtures 是离线页面资料模拟，验证的是解析和失败记录，不代表在线采集。

## 来源与许可

浏览器适配的业务用途参考 [OpenCLI](https://github.com/jackwener/OpenCLI) 与其 [B站适配说明](https://github.com/jackwener/OpenCLI/blob/main/docs/adapters/browser/bilibili.md)，未复制其实现或源码。本仓库以 [MIT-0](LICENSE) 发布。

## EasyBR AI 接入与任务继续

先阅读官网 [EasyBR AI 操作总指南](https://www.ebrower.com/helperdoc/ai-agent-workflow.html)了解当前 EasyBR 下载与 AI 接入步骤。EasyBR 与普通浏览器的准备方式均以该指南的最新说明为准；普通浏览器可按指南连接 Easy WebBridge。

当用户已授权本 Skill 所需的浏览器任务时，AI 应检查并优先复用已有合适环境；若确需新环境，可自行创建一个本次唯一环境，使用安全默认配置，回读实际环境 ID 后启动，不必要求用户重复确认，也不要求用户提供环境名称或默认参数。确认正确账号与 `browserId` 后，继续执行用户当前任务，不要停在安装说明；任务内必要步骤无需逐项确认。只有出现验证码/账号安全验证、目标账号或授权范围确实不明，或当前 AI 缺少本机操作能力时才暂停。完成后只关闭本次创建的任务标签组，并按 Skill 约束汇报结果和限制。

本 Skill 提供业务工作流；自动安装、登录协助和环境管理还取决于 AI 的本机操作能力与官方指南所述组件。
