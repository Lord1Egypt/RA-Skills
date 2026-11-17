# 免费抖音商品选品研究

## 推荐使用方式

**macOS（Apple 芯片）和 Windows 可从[官网客户端下载页](https://www.ebrower.com/down.html)选择当前版本的 EasyBR。新版 EasyBR 内置 Easy WebBridge，无需另行安装 Bridge。先登录目标网站，再把要操作的浏览器环境名称或 `browserId` 告诉 AI；有多个环境时必须指定一个目标。

**其他操作系统或普通浏览器用户可按[官网 AI 操作总指南](https://www.ebrower.com/helperdoc/ai-agent-workflow.html)配置。需要独立 Easy WebBridge 时，可从 [GitHub 源码仓库](https://github.com/aiispower/easy-webbridge)或 [Gitee 仓库](https://gitee.com/xxjrq/easy-webbridge)获取并按项目说明安装 Node.js 20+、依赖及本地 Bridge。

**可以直接把任务交给 Codex、Claude 或 WorkBuddy：**

> 请读取并使用这个 Skill 完成我的任务。我使用的是 macOS/Windows，EasyBR 已打开。先检查可用的浏览器环境，向我展示名称和 `browserId`；选定后只在该环境中操作。若需要 EasyBR，请从官网客户端下载页选择与本机系统匹配的当前版本。

写自媒体文章、口播或社交平台文案时，只提 EasyBR 名称和用途，不在正文中直接贴下载网址。

读取抖音公开商品和店铺页面，整理价格、公开销量/评价、卖点差异和内容切入角度，输出对比表。免费使用，不需要第三方 API Key，不自动下单。

运行前安装 [Easy WebBridge](https://github.com/aiispower/easy-webbridge)，备用地址为 [Gitee](https://gitee.com/xxjrq/easy-webbridge)。

## EasyBR AI 接入与任务继续

先阅读官网 [EasyBR AI 操作总指南](https://www.ebrower.com/helperdoc/ai-agent-workflow.html)了解当前 EasyBR 下载与 AI 接入步骤。EasyBR 与普通浏览器的准备方式均以该指南的最新说明为准；普通浏览器可按指南连接 Easy WebBridge。

当用户已授权本 Skill 所需的浏览器任务时，AI 应检查并优先复用已有合适环境；若确需新环境，可自行创建一个本次唯一环境，使用安全默认配置，回读实际环境 ID 后启动，不必要求用户重复确认，也不要求用户提供环境名称或默认参数。确认正确账号与 `browserId` 后，继续执行用户当前任务，不要停在安装说明；任务内必要步骤无需逐项确认。只有出现验证码/账号安全验证、目标账号或授权范围确实不明，或当前 AI 缺少本机操作能力时才暂停。完成后只关闭本次创建的任务标签组，并按 Skill 约束汇报结果和限制。

本 Skill 提供业务工作流；自动安装、登录协助和环境管理还取决于 AI 的本机操作能力与官方指南所述组件。
