# WorkBuddy 技能与专家

两类入口分别检查，不能仅改文件名互换。官方来源：[技能格式](https://open.workbuddy.cn/en/docs/skill)、[专家格式](https://open.workbuddy.cn/docs/expert)，核对日期 2026-11-06。

## 技能

扩展 frontmatter 必填且非空：`name`、`display_name`、`display_name_en`、`description`、`description_zh`、`description_en`、`version`、`author`。用 assets/workbuddy-market.json 格式提供市场字段，打包副本注入；源技能的 name 和 description 保留。

本项目兼容 profile 将 `SKILL.md` 放在 ZIP 根，资源使用“目录/文件”。最多两段路径来自 2026-10 的上传器反馈，并非官网对所有 ZIP 的普遍限制。它仅约束独立技能包，不能用于判断专家嵌入技能的深度。

深层资源需要专用适配副本：维护旧→新路径映射、检测重名，修改 Markdown、资源清单、动态加载器和脚本路径。不能盲目文本替换二进制或只移动文件。工具遇到深路径直接报错，避免静默改变行为。

## 单 Agent 专家

ZIP 根有 `.codebuddy-plugin/plugin.json`、`agents/<agentName>.md`、`avatars/`、README；技能路径在 plugin.json 中引用。专家版本独立于嵌入技能版本。

插件名称与 plugin 保持一致；agentName 对应实际 Agent 文件。Agent frontmatter 的名称、description、displayName、profession 与配置一致。运行权限由平台分配，不能自加 tools。依赖连接器仅在角色必须依靠它时声明，凭据不进包。

市场字段包括双语展示名、头衔、简介、标签和推荐提问。标签与问题各三条，默认问题与第一条相同。中文卡片简介按字段说明控制在 40–50 字符，长介绍放 README/独立文案。头像为 PNG/JPG、512×512、≤500KB；选择实际角色对应行业分类。

**专家头像交付限制（2026-11-13 用户确认）**：WorkBuddy 开放平台的专家头像不能手动上传，必须随专家压缩包交付。图片放在 ZIP 内，例如 `avatars/expert.png`，由 `.codebuddy-plugin/plugin.json` 的 `avatar` 指向该相对路径。不能只交付 PNG 或建议上传专家后在平台手动补头像；此限制仅针对专家入口，不据此推断独立技能头像的上传方式。

生成或更换头像后，先同步专家源码中的头像文件及配置，再重新打包；从实际 ZIP 读取配置和图片，确认引用存在、格式/尺寸/体积合规，并与用户选定新图的 SHA256 一致，避免误带旧机器人头像。单独 PNG 可作预览或备份，不能代替专家包内资源。

**上传器案例**：2026-11-05，`FastGPT 工作流与知识库专家` 因 17 字、上限 15 字被拒。改为 `FastGPT工作流专家`（12 字）；`N8N自动化工作流专家`（11 字）。默认同时检查两个语言的名称≤15，英文上限是本项目保守兼容措施，不将其表述为官网明确规定。名称中空格与拉丁字母也计数，不修改稳定机器标识来解决显示名错误。

工具生成单 Agent、自包含版本，不自动生成专家团或任意 MCP 配置。输入示例作者邮箱须改为真实发布者资料；头像由用户提供或另行制作，不能假造官方背书。上传后实际核对技能资源是否保留、专家能否读取内置入口、脚本和召唤是否成功。
