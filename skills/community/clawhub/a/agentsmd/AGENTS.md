# agentsmd-skill

agentsmd Agent Skill 的源仓库：纯 Markdown 技能包（SKILL.md + references/ + assets/），无构建、无测试；技能包与 README 英文默认（中文参考译文收 docs/zh-CN/），协作文档（CHANGELOG/HANDOVER/运行记录）与 Release Notes 用简体中文，提交主题用英文 conventional commits，产出遵循 agents.md 开源规范。

## PR / Workflow Instructions

- 发版：SKILL.md frontmatter `version` 与 CHANGELOG 同步升版 → commit → push → `gh release create vX.Y.Z` 远程自动建 tag，勿 git tag + git push tag；Release Notes 取自 CHANGELOG 对应条目
- 发版推送后同步技能市场：ClawHub `clawhub skill publish`、LobeHub `lhm skill publish --identifier kelegele-agentsmd-skill`；skills.sh 随 GitHub 自动更新，勿手动投
- 文档语言：skill 包与 README 英文默认，中文版收 `docs/zh-CN/`（仅作参考译文，不随技能包发布）；SKILL.md frontmatter `description` 用双语（英文主句 + 中文触发短语），触发判据兼容中文
- 发布与改版保留引流位：SKILL.md「关于」、frontmatter `metadata.openclaw.homepage`、README 安装链接均指向 GitHub 仓库与 kelegele.com
- git push 偶发 `Connection was reset` / HTTP/2 framing 错误属瞬时故障：重试一次，仍败加 `-c http.version=HTTP/1.1`，勿判为网络不通

## Project-Specific Gotchas

- 改 SKILL.md 工作流/章节时，必须同步 README（特性列表、目录树）与 CHANGELOG，保持版本与内容三处一致
- 新增或修改数值门槛（行数、章节上限等）时，先核对与模板既有结构不自相矛盾（曾出现"章节 ≤6"与 6 个标准章节冲突）
- SKILL.md frontmatter 的 `description` 是触发判据，改动触发场景时须同步更新措辞
- 对外交付类指令（投稿／发布／提交／推送）落点不明时：先查环境变量（如 INBOX_REPO）与既有项目惯例，仍不明就问用户，不得默默降级为本地产出
- LobeHub 无新建技能网页入口（`/publish` 是 404）：新品等市场自动抓取（identifier 为 owner-repo 扁平化）后 `lhm skill claim` 认领，再 CLI 推版本
- ClawHub 条款：发布的技能一律 MIT-0（可商用、免署名），SKILL.md 勿写冲突许可条款

## 多 Agent 交接
- 开始时读取 HANDOVER.md 与对应任务记录，沿用原任务编号，登记负责人、目标和状态。
- 有进展、阻塞或用户新决定时更新任务记录；结束前补齐产物、证据、未完成项和下一步，在 HANDOVER.md 同步摘要和入口。
- 自动记录只反映会话状态。Agent 核对并填写业务结果；最终回复附记录路径，无法写入时标记「待同步」。
