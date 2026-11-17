# AgentLens Social Connector

AgentLens Social Connector 是 AgentLens 官方发布的 Skill，可以让你的 AI agent 通过 AgentLens API 读取公开社交平台链接，再完成内容总结；当你的 AI agent 具备相应能力时，进一步解读图片/视频，并把整理稿保存进可用的知识库目的地。

把来自小红书、抖音、Bilibili、微博、微信公众号、微信视频号、TikTok、Instagram、X/Twitter、Reddit、YouTube 等平台的链接发给 agent 后，agent 会通过 AgentLens API 获取可读内容，再按你的要求总结、提取要点、尝试解读图片/视频，或在目标可用时保存到知识库。

## 为什么需要这个 Skill

AI agent 只要拿到内容，通常就能很好地做总结和分析。真正麻烦的是“拿到内容”这一步：社交平台经常有登录墙、页面结构变化、反爬策略、图片/视频混排，以及不稳定的字段格式。

AgentLens API 把这些差异收敛成一个统一接口：

- 一个 API 覆盖 20+ 个社交平台，以下按类别列出具体平台
- 不需要用户提供社交账号 cookie 或登录态
- 可返回正文、说明文案、来源信息、图片/视频等媒体文件 URL，以及部分平台可用的字幕/转写
- 面向 agent 工作流设计，不只是把 API 字段原样丢给用户

这个 Skill 在 API 调用之外补上完整操作路径：解释返回结果，在需要时尝试理解图片或视频，并在当前 agent 环境支持时，把整理后的内容保存到用户指定的知识库。

## 平台覆盖

AgentLens API 面向 20+ 个主流社交、视频、社区和创作者平台提供公开内容读取能力，包括：

- **短视频与视频平台**：抖音、Bilibili、快手、西瓜视频、微信视频号、TikTok、YouTube
- **社交网络与创作者帖子**：小红书、微博、微信公众号、Instagram、X/Twitter、Facebook、Threads、LinkedIn、Bluesky、Snapchat、Pinterest、Lemon8
- **社区与讨论内容**：知乎、Reddit
- **直播平台**：Twitch、Kick

> 实际可读取范围取决于内容是否公开和平台限制。AgentLens API 读取的是公开帖子/内容本身；不读取私密或登录后内容、评论区、完整时间线，也不读取 X/Reddit 对话串。

## 你可以怎么用

安装后，可以直接这样说：

```text
帮我读一下这条小红书笔记，并总结重点。
总结这个抖音视频在讲什么。
这个微博帖子主要说了什么？
帮我读取这个微信公众号文章，并保存到知识库。
看一下这个 Instagram 帖子的图片，帮我总结产品细节。
用 AgentLens 读取这个 X 链接。
总结这个 TikTok 视频，并提取可执行要点。
```

agent 会按文档尝试执行：

1. 识别社交 URL。
2. 读取本 Skill 和当前请求所需的 reference。
3. 加载 `AGENT_LENS_API_KEY`。
4. 调用本包 AgentLens API reference 中声明的 endpoint。
5. 整理 AgentLens API 返回字段。
6. 根据你的请求进行总结、解读返回的媒体文件，或在所需能力可用时保存到知识库。

Skill 中包含请求前检查，要求 agent 使用文档里的 endpoint 和参数，不凭记忆拼接 API 地址，也不在未经你同意时用其他来源替代原始链接。

## 安装

从发布该 Skill 的仓库或 marketplace 页面安装：

```text
安装 AgentLens Social Connector Skill: https://clawhub.ai/inkad-code/skills/agentlens-social-connector
```

如果你的 AI agent 支持从 GitHub 安装 Skill，可以指向本仓库。

> **自动识别说明：** 你的 AI agent 加载本 Skill 后，会按这里的流程读取内容；但仅完成安装，不代表每个 AI agent 都会自动识别并使用本 Skill 处理每一条社交链接。如果没有自动使用，直接说：“用 AgentLens Social Connector 读取这个链接。”

## 更新

本 Skill 使用发布日期作为版本号，例如 `2026.07.23`。首次安装或首次配置时，如果有已批准的记忆或配置机制，AI agent 会记录安装来源；后续按该来源以低频方式检查是否有新版本：默认最多每 7 天检查一次，或在你询问是否有更新时检查。安装来源可以是 GitHub release、ClawHub、SkillHub，或你批准的其他来源页面。

如果发现新版本，agent 应在低打扰场景提醒你，并在升级或重新安装前征求确认。未经你确认，agent 不应改写 Skill 文件、安装包或技能市场状态。

## API Key

在这里创建 AgentLens API key：

[https://agentlensapi.io/](https://agentlensapi.io/?utm_source=clawhub&utm_content=social_connector_skill)

之后可以在 agent 提示时粘贴 key，或通过宿主的 secret / 环境变量设置 `AGENT_LENS_API_KEY`。不要把 key 粘贴进本 Skill 包、共享文档或代码仓库。

本 Skill 也支持用户确认后的本地配置：

```text
~/.agentlens/config.json
```

只有在你信任当前环境，并明确同意保存本地配置时，才建议把 key 写入本地。请通过宿主的安全凭据或本地配置流程设置 `agentLensApiKey` 的值；本包刻意不提供任何 key-value 示例。Skill 要求 agent 不打印完整 key，也不要把完整 key 写进聊天回复、运行日志或测试记录。

## 价格

本 Skill 使用 AgentLens API 读取社交内容。使用前需要 AgentLens 账号和 API key。按本版本发布时的官网公开信息，AgentLens API 价格如下：

| 套餐 | 月付价格 | 年付价格 | 每月 API 调用额度 |
| --- | ---: | ---: | ---: |
| Basic | $0 | $0 | 20 |
| Pro | $2.90/月 | $29.90/年 | 200 |
| Ultra | $5.90/月 | $59.90/年 | 500 |
| Mega | $9.90/月 | $99.90/年 | 1,000 |

价格、额度和套餐可用性可能变化，请以 AgentLens 官网最新价格为准：

[https://agentlensapi.io/](https://agentlensapi.io/?utm_source=clawhub&utm_content=social_connector_skill)

技能市场说明：本 Skill 本身不是付费 Skill，也不设置按 Skill 收费或付费门槛。AgentLens API 是否免费或收费，取决于用户自己的 AgentLens 套餐。

## 输出

典型回答会包含：

- 主要结论
- 关键要点
- 平台和作者/来源
- 如果 AgentLens API 返回字幕，则基于字幕/转写总结
- 对媒体主导内容，补充图片或视频解读；文字主导内容则按需处理媒体
- 如果你要求保存，则生成适合写入知识库的整理稿

除非你明确要求，否则 agent 不应暴露原始 JSON。

## 媒体与知识库

当 AgentLens API 返回图片、视频等媒体文件 URL 时，本 Skill 会指导 agent 使用当前环境的图片解读、音视频处理或转写能力。对小红书、抖音、TikTok、Instagram、Bilibili、视频号等媒体主导内容，图片/视频是内容本身的一部分，agent 应先尝试解读返回媒体文件再总结。如果当前环境无法读取或处理媒体文件，agent 需要明确说明限制，并基于正文、字幕、来源信息和媒体元数据做有限总结。对文字主导内容，agent 只在任务需要解读图片、做视频级总结或更深入解读媒体内容时下载对应媒体文件。媒体文件只在当前请求中临时使用。

当 AgentLens API 返回的视频没有字幕或转写数据时，agent 应先检查当前环境是否已经有可用的转写能力，例如平台原生工具、本地 Whisper 或已授权的语音转文字 API。只有这些路径都不可用时，才向你询问是否安装本地工具、配置 API，或改为只基于标题、说明文案和来源信息总结。

当你要求保存结果时，Skill 会先准备一份干净的整理稿，包含原始链接、平台、作者/来源、账号/Handle、标题、发布日期、获取日期、摘要、要点、转写说明、媒体解读和原文/正文。整理稿上方优先显示摘要和要点，原文放在偏下方，方便需要时查阅。

随后在目标写入工具或已批准的兜底路径可用时，agent 会写入你指定的目的地；如果目标不可用或写入失败，agent 应保留整理稿，并说明目标端错误或缺失能力。支持的目的地包括 Notion、Obsidian/本地 vault、ima、本地 Markdown/工作区文件，或当前 agent 环境提供的知识库工具。

对支持目录结构的目的地，如果用户没有现成约定，Skill 会建议按平台和账号分组。对于 Notion 和 Obsidian，agent 应先使用你当前环境已有/默认的写入工具；只有没有可用默认工具时，才使用本 Skill 的兜底辅助流程。用户要求把正文/原文与图片、视频、媒体文件或图文内容一起保存，属于明确的媒体文件保存请求，而不是纯文本保存。对 ima，必须使用单个 `media_type=20` HTML 文档，以 base64 内嵌所要求的图片；视频仅在下文的明确请求和大小限制条件满足时才允许内嵌。不得静默降级成 Markdown 或仅导入 URL。对 Notion，当前环境存在经验证的原生媒体 block 时才使用；否则必须说明限制，并在降级成仅链接/文本前取得用户同意。如果你需要长期保存原始媒体文件，agent 会先确认要保存哪些媒体，再下载所选媒体，并按目标知识库支持的方式上传或附加。

对于 ima，默认保存文本优先的整理稿，并写入图片或视频解读结论和媒体引用；不要把图片或视频批量上传成一堆没有索引关系的独立知识条目。如果你要求保留图文排版，优先生成单个内嵌 base64 图片的 HTML 文件。

对于 ima 中的视频，使用返回来源 URL 的 HTML 播放器只适合作为短期预览，因为平台视频链接可能过期。只有你明确要求保留视频字节时，AI agent 才能在确认最终文件符合 ima 当前 **10 MB 总上限**且可以上传后，创建一个内嵌 base64 视频的 `media_type=20` HTML 文件。该上限涵盖全部 HTML 正文，以及每个内嵌的 base64 图片或视频；可行时还应在 ima 内检查播放。OpenAPI 兜底流程尚无已验证的独立视频上传类型，因此这不代表能生成稳定的长期视频归档。

## 限制

本 Skill 用于通过 AgentLens API 读取公开社交内容。它不用于：

- 私密帖子或受保护账号
- 登录用户账号
- 读取评论区、完整回复串、X/Twitter 对话串或 Reddit 讨论串
- 管理、点赞、发帖、关注或发消息
- 绕过付费墙或访问控制
- 在没有当前请求或确认目的地的情况下自动保存每个链接

## Skill 结构

```text
agentlens-social-connector/
  SKILL.md
  README.md
  SKILL_cn.md
  README_cn.md
  references/
    agentlens-api.md
    media-workflows.md
    knowledge-base-workflows.md
    agentlens-api_cn.md
    media-workflows_cn.md
    knowledge-base-workflows_cn.md
```

本包包含英文运行/reference 文档及中文副本。`SKILL.md`、`README.md` 和 `references/*.md` 是英文文档；`SKILL_cn.md`、`README_cn.md` 和 `references/*_cn.md` 是中文文档。

`SKILL.md` 包含运行时行为；`references/agentlens-api.md` 说明 API 请求、响应、字段整理和错误处理；`references/media-workflows.md` 说明图片/视频解读和转写流程；`references/knowledge-base-workflows.md` 说明经用户确认后的保存流程。
