# Audit Evolution 装机测试清单

用于 SkillHunt 发布前，让 Windows 和 macOS/Linux 用户验证安装、hook、run record 和短指令入口。

## Windows PowerShell

在 `audit-evolution` 仓库目录运行：

```powershell
$target = "$env:TEMP\audit-evolution-test"
Remove-Item -LiteralPath $target -Recurse -Force -ErrorAction SilentlyContinue
powershell -ExecutionPolicy Bypass -File .\scripts\install-audit-evolution.ps1 -TargetWorkspace $target -Agent codex -Force
powershell -ExecutionPolicy Bypass -File "$target\.audit-evolution\hooks\invoke-audit-evolution-hook.ps1" -WorkspacePath $target -EventType benchmark_completed -Summary "安装测试：刚完成一次本地评测，需要审计并准备下一轮进化"
Get-Content -LiteralPath "$target\.audit-evolution\run-records\latest.md" -Encoding UTF8 -TotalCount 40
```

通过标准：

- `$target\skills\audit-evolution\SKILL.md` 存在。
- `$target\AGENTS.md` 包含 `Audit Evolution Auto-Use`。
- `$target\.audit-evolution\run-records\latest.md` 存在。
- 复制给 Agent 的短指令 `进化` 会路由到 Audit Evolution。

## macOS / Linux

在 `audit-evolution` 仓库目录运行：

```bash
target="$(mktemp -d)"
bash ./scripts/install-audit-evolution.sh --target "$target" --agent openclaw --force
bash "$target/.audit-evolution/hooks/invoke-audit-evolution-hook.sh" --workspace "$target" --event benchmark_completed --summary "安装测试：刚完成一次本地评测，需要审计并准备下一轮进化"
sed -n '1,40p' "$target/.audit-evolution/run-records/latest.md"
```

通过标准：

- `$target/skills/audit-evolution/SKILL.md` 存在。
- `$target/AGENTS.md` 包含 `Audit Evolution Auto-Use`。
- `$target/.audit-evolution/run-records/latest.md` 存在。
- 复制给 Agent 的短指令 `进化` 会路由到 Audit Evolution。

## 反馈模板

```text
系统：
Agent：
安装是否成功：
hook 是否生成 latest.md：
Agent 回复“进化”后的行为变化：
评分建议：
问题截图或报错：
```
