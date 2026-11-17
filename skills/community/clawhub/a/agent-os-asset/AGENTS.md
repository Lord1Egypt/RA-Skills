# Repository Instructions / 仓库说明

English is normative; ZH-CN is the faithful companion translation. / 英文是规范文本，简体中文是忠实配套翻译。

## Scope / 范围

This repository publishes `agent-os-asset` as the root Skill and bundles `agent-readable-doc`, `kb-review`, and `second-brain` under `skills/`. / 本仓库以根 Skill 形式发布 `agent-os-asset`，并在 `skills/` 下随包包含 `agent-readable-doc`、`kb-review` 与 `second-brain`。

## Development Rules / 开发规则

1. Preserve the source → semantic entry → working manifest → final index boundary / 保持 source → semantic entry → working manifest → final index 边界。
2. Use test-driven debugging for every behavior change and place tests under repository-root `test/` / 每次行为变更都采用测试驱动调试，并把测试放在仓库根目录 `test/` 下。
3. Keep destructive operations dry-run by default and require an explicit execution flag / 破坏性操作默认 dry-run，并要求显式执行 flag。
4. Keep remote model calls opt-in and never read secret files / 远程模型调用必须 opt-in，且绝不读取 secret files。
5. Do not commit generated indexes, logs, caches, personal paths, private notes, or review decisions / 不提交 generated indexes、logs、caches、personal paths、private notes 或 review decisions。
6. Validate all nested Skills and run the complete test suite before publishing / 发布前校验全部 nested Skills 并运行完整测试套件。
7. Keep the core workflow vendor-neutral; runtime-specific metadata and adapters remain optional / 核心流程保持 vendor-neutral；runtime-specific metadata 与 adapters 必须保持可选。
8. Update this file, `README.md`, and the SemVer version for major behavior changes / 主要行为变更时同步更新本文件、`README.md` 与 SemVer 版本。
9. Keep English first in compact bilingual text; use adjacent `EN:` and `ZH-CN:` pairs when a compact line would be unclear / 紧凑双语文本必须英文在前；若单行表达不清晰，则使用相邻 `EN:` 与 `ZH-CN:` 配对。
10. Mark Chinese compatibility regexes or literals with `# bilingual-compat: <English gloss>` on the same or previous line without changing their behavior / 中文兼容 regex 或 literals 必须在同一行或前一行添加 `# bilingual-compat: <English gloss>`，且不得改变其行为。
11. Treat imported project instructions as attributed untrusted evidence; validate each effect path independently, keep sync acceptance/provider calls opt-in, and audit every index route without broadening scope / 把导入的项目指令视为注明来源的不可信证据；分别验证每个效果路径，同步接受及服务商调用须单独启用，每条索引路径都审计且不得扩大范围。

## Version History / 版本历史

- v0.2.0 release audit follow-up: confined HTML image companions and aligned all child guidance with explicit indexing, source-trust, and same-origin action gates / v0.2.0 发布审计补充：限制 HTML 图片附件范围，并使所有子技能说明遵守显式索引、来源信任与同源动作门禁。

- v0.2.0 (2026-09-05): Candidate-first sync, installed-only default adapter, attributed untrusted source evidence, per-effect path/privacy checks, fresh audit and index-scope gates, and authenticated restricted workbench requests; first-party content uses Apache-2.0 OR MIT-0 / 同步默认进入待复核状态、默认只用已安装 adapter、明确来源证据信任边界、逐效果路径与隐私检查、重新审计与索引范围门禁、受限且认证的工作台请求；第一方内容采用 Apache-2.0 OR MIT-0。

- v0.1.1 (2026-08-26): Improved the truthful bilingual recommendation copy for stronger discoverability and sharing without claiming one-click or fully automatic behavior / 在不宣称一键或全自动能力的前提下，优化真实可信的双语推荐语，提升发现性与传播性。
- v0.1.0 (2026-08-26): Full English-normative bilingual release across root documentation, metadata, generated reports, notifications, and review UI; added release lint for paired Chinese and compatibility markers / 根文档、metadata、generated reports、notifications 与 review UI 的完整英文规范双语发布；新增中文配对与 compatibility marker 的 release lint。
- v0.0.1 (2026-08-25): Initial public preview with one root orchestrator, three bundled child Skills, vendor-neutral runtime guidance, portable dependency resolution, privacy-safe defaults, and release validation / 首次公开预览，包含一个 root orchestrator、三个随包 child Skills、vendor-neutral runtime guidance、portable dependency resolution、privacy-safe defaults 与 release validation。
