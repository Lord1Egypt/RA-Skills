# 客户端适配矩阵

以下是 2026-11-06 文档核对结果，不代表本项目已在这些客户端完成导入测试。文件结构可以共用，发现路径、运行时和市场元数据不能据此推断相同。目录中的 `<name>` 指实际技能机器名。

| 目标 | 本工具 profile / 交付 | 发现或安装位置与核验 |
| --- | --- | --- |
| WorkBuddy 技能 | workbuddy，ZIP 根入口 | 使用技能上传入口；扩展元数据、资源两段路径兼容规则见 WorkBuddy 指南 |
| WorkBuddy 专家 | expert 命令 | 专家上传入口；单 Agent 配置并内置完整技能；不沿用独立技能的深度规则 |
| Trae | trae，ZIP 根入口 | 官方支持 SKILL.md 或含资源的 ZIP；项目目录 `.trae/skills/<name>`，上传后检查资源实际保留 |
| Codex | folder，标准目录包 | 当前官方文档为项目 `.agents/skills` 与用户 `~/.agents/skills`；已有宿主可能暴露不同有效目录，依据当前技能清单确认，避免同名多份 |
| Claude Code | folder | 项目 `.claude/skills/<name>` 或个人 `~/.claude/skills/<name>`；本地目录不等于云端/Cowork 已同步 |
| Cursor | folder | 项目 `.cursor/skills/<name>` 或 `.agents/skills/<name>`；用户目录与云端同步分别核验 |
| GitHub Copilot | folder | 项目 `.github/skills/<name>`，官方也支持兼容目录；IDE、CLI 与云端各自检查发现和权限 |
| Hermes | folder | 实际 home/profile 的 skills 根，常见 `~/.hermes/skills`；确认运行 Agent 使用的目录，再检查发现和新会话 |

仅选择实际要求的目标，不为了“多平台”复制多份内容完全相同且名字误导的包。folder 包可解压到上述已确认的 skills 根；不要形成 `<name>/<name>/SKILL.md` 双重目录。源码根入口包与文件夹包都可能正确，区别在用户选择的导入方式。

Codex 专属 `agents/openai.yaml` 用于 UI 与调用策略，不能假定其他平台读取。保留普通 SKILL.md 入口。默认允许隐式选择，除非用户明确要求更改。使用命令行、Shell、Python/Node、网络或桌面工具的技能必须说明环境要求；平台发现成功不等于脚本可运行。

本地、云端、SSH 和容器的路径与权限不同。别把非交互 shell 的默认 home 当成运行 Agent 的实际 profile；不打印完整环境变量来排查路径。没有浏览器时交付离线候选和实际待验证项，不自动重启服务。

新增其他平台时先核对官方入口、当前 schema 与实际导出/导入示例，补一条有日期的证据记录。未知平台不靠更换后缀假装支持；优先提供标准目录候选，明确发现和执行待验证。

官方资料：

- [Trae Skills](https://docs.trae.cn/ide_skills)
- [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code Skills](https://code.claude.com/docs/en/skills)
- [Cursor Skills](https://cursor.com/docs/skills)
- [GitHub Copilot Skills](https://docs.github.com/en/copilot/concepts/customizations/agent-skills)
- [Hermes Working with Skills](https://hermes-agent.nousresearch.com/docs/guides/work-with-skills)
