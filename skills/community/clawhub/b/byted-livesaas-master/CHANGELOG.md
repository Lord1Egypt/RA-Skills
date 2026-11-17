# Changelog

## 1.1.3

- 增加内外网 CLI 入口解析策略：公网 `bytedlive` 优先，不可用时自动降级到内网 `bytedlive-b`。
- Onboarding 安装流程增加公网包与内网包的顺序兜底，BOE / 测试环境命令也按同一策略重试。

## 1.1.2

- 明确 console-login 不通时必须保留 AK/SK 兼容路径，使用 `bytedlive openapi set-credentials` 本地隐藏输入并重新验证。

## 1.1.1

- 小补丁版本升级，保持 `VERSION`、`SKILL.md` frontmatter 与发布清单版本一致。

## 1.0.5

- `VERSION` 与 `SKILL.md` front-matter 版本对齐，修复埋点 `skillVersion` 不一致。
- 自测说明去掉对 Skill 包内不存在目录的硬编码路径，仅保留可执行的 `bytedlive control test` 说明。

## 1.0.4

- `control room list` 的 `--sort-order` 支持 `desc`/`asc` 等小写输入，CLI 自动规范为 OpenAPI 要求的 `Desc`/`Asc`。
- 自测说明与 `bytedlive control test` 对齐。

## 1.0.3

- 启动埋点脚本按 Skill 安装路径自动识别 Agent，避免硬编码 `--agent codex` 导致误报。
- SKILL 启动命令改为 `node tools/report_usage.js`（无需手动传 `--agent`）。

## 1.0.0

- 初始版本，提供控播 onboarding、凭证安全、命令路由、OpenAPI 兜底与错误恢复契约。
