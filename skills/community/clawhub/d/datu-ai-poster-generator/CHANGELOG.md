# 更新日志

## v1.1.9 (2026-05-19)

- 增加已有图片修改的强路由规则：改图、换字、替换 logo、保留版式、继续修图等请求必须走 AI 修图接口。
- 扩充 `manifest.json` 的修图触发词，提升小龙虾、飞书、微信等宿主对 AI 修图意图的命中率。
- 补充示例说明，避免宿主把待修改图片误当作内容素材重新生成。

## v1.1.8 (2026-05-14)

- 明确宿主/IM 工具收到用户提供的 Datu API Key 后，应保存为 `DATU_API_KEY` 持久凭据。
- 明确后续调用应自动注入 `X-API-Key`，不要反复要求用户重新提供 API Key。
- 在 `manifest.json` 中增加 `credentialPersistence` 元数据，便于 OpenClaw、ClawHub、飞书、微信等宿主正确实现凭据保存。

## v1.1.7 (2026-04-29)

- Cancel new 8K datu and edit requests; the skill now submits only `resolution=4k`.
- Add `9:21` ratio support alongside `9:16`.
- Note that AI edit now follows the server-side RunningHub G2 quality chain by default.

## v1.1.6 (2026-04-27)

- 新增发布脚本 `scripts.publish_skill_package`，可在每次技能更新后打包版本化 zip。
- 支持将技能 zip 上传到 `cdn.aimindschool.com` COS，发布者可将脚本输出的 CDN URL 私下发给下载受限用户。
- 保持 `/api/skill/version` 只做低频版本提醒，不把 CDN 包描述成可绕过 ClawHub 入口限流的公开安装入口。

## v1.1.5 (2026-04-27)

- 优化 ClawHub/OpenClaw 安全审查说明，明确 `DATU_API_KEY` 是必需凭证，`X-API-Key` 是请求头。
- 将“原始内容提交”表述调整为“上传前安全检查通过后的保真提交”，避免被理解为绕过确认的外发。
- 明确 `deep_research=true` 只能在用户明确选择或确认后启用。
- 补充发布信息中的外部 API、隐私政策、仓库和凭证元数据，减少 registry 元数据不一致导致的可疑提示。

## v1.1.4 (2026-04-27)

- 深度研究报告下载格式从 Markdown 改为 Word `.docx`，方便用户继续编辑。
- 明确下载报告应保留深度研究 API 原始报告内容，生图链路内部再整理简报。

## v1.1.3 (2026-04-27)

- 新增 `deep_research` 深度研究说明，明确会全网深度抓取并分析，通常额外需要 5-15 分钟。
- 明确深度研究额外消耗 5 积分，并会强制使用 `magic_wand=true`。
- 新增 `research_report_download_url` 与 `/api/tasks/{task_id}/research-report-link` 说明。
- 明确如果用户选择深度研究，最终结果不仅给出图片，也要给出 Markdown 深度研究报告文件。

## v1.1.2 (2026-04-23)

- 新增 GET /api/skill/version，用于技能低频检查最新版本。
- 新增技能侧“顺手提醒一句”的更新提示规则，不打断主流程。
## v1.1.1 (2026-04-23)

- 补充隐私与敏感数据规则，明确遇到明显敏感、受监管或含凭证内容时必须先提醒并获得明确批准。
- 在技能说明中更直白地标注这是对 `https://datu.digilifeform.com` 外部 API 的调用。
- 将表述统一为“不要压缩整理摘要总结用户信息，而是把用户给的原始信息直接交给大图技能”。

## v1.1.0 (2026-04-23)

- 新增 `magic_wand` 文档说明，明确大图生成支持“设计化 Prompt”与“原始 Prompt 直出”两种模式。
- 新增强约束：`magic_wand=true` 时禁止外层代理先做摘要、提炼或缩写，必须保留用户给出的原始信息。
- 新增 `9:16` 比例说明与示例。
- 更新大图与修图 API 示例，补齐当前真实字段。
- 明确 `magic_wand` 与修图 `magic_think` 的职责分离。
- 补充系统统一追加 4K 高清质量要求的说明。
- 同步 `4k` 默认高质量链路与自动回退说明。
- 修复多份中文文档乱码问题。

## v1.0.0 (2026-04-13)

- 首次发布技能包。
- 支持文本生成大图。
- 支持文件上传生成。
- 支持 AI 修图。
- 支持 `16:9` 与 `21:9`。
- 支持 `4k` 与 `8k`。

