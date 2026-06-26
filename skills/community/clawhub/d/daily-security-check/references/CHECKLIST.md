# 每日安全巡检 — 检查清单

执行本 Skill 时，按以下项逐项检查（项目根目录为 OpenClaw 仓库根）。**报告输出路径**：`workspace/docs/security-audit/security-report-YYYY-MM-DD.md`。

## 1. 网关是否仍绑定到 loopback

- 查看项目根目录 `openclaw.json` 中 `gateway.bind` 是否为 `"loopback"`。
- 若为 `"0.0.0.0"` 或其它，视为异常并提醒。

## 2. 防火墙

- 在报告中提醒用户在本机确认：**系统设置 → 网络 → 防火墙 → 开启**，并设置为「阻止所有传入连接」。
- 本项无法自动检测，仅作提醒。

## 3. API 密钥是否在 .env

- 检查 `openclaw.json` 中是否仍有明文 `apiKey`、`token`、`appSecret`（即非 `${VAR}` 形式的敏感值）。
- 若存在明文凭证，列出位置并建议迁移到 `.env` 并用 `${VAR}` 引用。

## 4. SOUL.md 安全监控规则

确认项目内各 agent 的 SOUL.md 均包含「安全监控规则」章节（含 6 条规则）。路径示例（请按实际 agent 目录调整）：

- `workspace/SOUL.md`
- `agents/<agent-name>/workspace/SOUL.md`（如 news、content、finance、operation、program、product 等）

若有缺失，列出对应 agent 并提醒补全。

## 5. 异常认证失败

- 若可访问 OpenClaw 或系统近期日志，简要查看是否有认证失败、未授权访问等记录。
- 若无权限或无法判断，在报告中说明「需用户自行关注日志与登录异常」。

## 6. 身份与访问控制（扩展，参考 community-official-security-extras）

- **DM/群组**：`openclaw.json` 中各 channel 的 `dmPolicy` 应为 `"pairing"` 或 `"allowlist"`，`groupPolicy` 应为 `"allowlist"`（生产环境避免 `open`）。
- **Gateway Token**：`OPENCLAW_GATEWAY_TOKEN` 至少 32 字符，建议 64 字符（256 位）；建议每 30 天轮换。
- **控制 UI**：`gateway.controlUi.allowInsecureAuth` 与 `gateway.controlUi.dangerouslyDisableDeviceAuth` 均应为 `false`（或未显式启用）。

## 7. 工具与沙箱（扩展，参考 community-official-security-extras）

- **exec**：`openclaw.json` 中 `tools.exec.security` 应为 `"allowlist"` 或 `"deny"`，禁止 `"full"`；`tools.exec.ask` 建议 `"on-miss"`。
- **exec-approvals**：`exec-approvals.json` 的 `defaults.security` 应为 `"allowlist"` 或 `"deny"`；allowlist 条目需在 Control UI 或 CLI 中按需添加（可执行路径的 glob）。
- **沙箱**：若启用 Docker 沙箱，`agents.defaults.sandbox.mode` 建议为 `"non-main"`；`scope`/`workspaceAccess` 按需设置；容器内进程应以非 root 用户运行（如 `sandbox.docker.user`）。
- **运行身份**：Gateway 进程应以普通用户（非 root）运行；若用 systemd/LaunchDaemon 等方式托管，需显式配置运行用户。
- **工具策略**：建议定期审查 `tools.profile` 与 `tools.allow`/`tools.deny`，保持默认拒绝、显式放行。

## 8. 官方安全审计（执行命令）

- **执行**：在项目根目录运行（若使用非默认状态目录，请先设置环境变量 `OPENCLAW_STATE_DIR`）：
  ```bash
  openclaw security audit
  ```
- **纳入报告**：将输出中的 Summary（critical/warn/info 数量）及关键 WARN 要点写入报告；若有 critical 需明确标出并提醒立即处理。
- **权限收紧**：若需将会话日志与配置目录权限收紧为 700/600，可提醒用户执行 `openclaw security audit --fix`（同上需正确设置 `OPENCLAW_STATE_DIR`）。

## 9. OpenClaw 健康检查（doctor）

- **执行**：在项目根目录运行（若使用非默认状态目录，请先设置 `OPENCLAW_STATE_DIR`）；仅只读检查，不执行 `--fix`：
  ```bash
  openclaw doctor
  ```
- **纳入报告**：将输出中的 Summary 或关键结论（如是否有需修复项）写入报告；若有建议运行 `openclaw doctor --fix` 的提示，在报告中标出并提醒用户**在本地终端按需手动执行**，不在此技能内自动执行 `--fix`。
