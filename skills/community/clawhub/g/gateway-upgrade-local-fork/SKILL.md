---
name: gateway-upgrade-local-fork
version: 0.3.0
description: "OpenClaw 网关服务本地 fork 升级 skill。覆盖 backup → upgrade → env-merge → verify 全流程。专门处理 OpenClaw systemd service 升级时丢失 user 自定义环境变量（CUDA / LD_LIBRARY_PATH / QMD_EMBED_MODEL）的问题，跑 qmd doctor 检查 RTX 30/40 系 GPU 加速状态，串行重建 per-agent qmd 索引避免 batch embed lock 争用。No data forwarded; all operations are local service+db manipulation only."
metadata: {"openclaw":{"emoji":"⬆️","requires":{"anyBins":["systemctl","sqlite3","node"]}}}
---

# OpenClaw Upgrade

升级 OpenClaw 主程序端到端 skill。**大方向按 5 阶段跑**：

1. **Pre-flight** — 体检当前状态，建立 baseline
2. **Backup** — 完整回滚点
3. **Upgrade** — 跑升级 + 合并 user env
4. **Post-flight** — diff env，确认没漏
5. **Verify** — 健康检查 + 修复

详细流程 → 各自 references 文档。

| 阶段 | 文档 | 关键点 |
|------|------|--------|
| 0. Pre-flight | [references/01-preflight.md](./references/01-preflight.md) | service unit .bak + qmd doctor baseline + GPU 状态 |
| 1. Backup | [references/02-backup.md](./references/02-backup.md) | binary + service + dbs（**核心**：env 备份）|
| 2. Upgrade | [references/03-upgrade.md](./references/03-upgrade.md) | 跑升级 + **手动合并 user env**（关键）|
| 3. Post-flight | [references/04-postflight.md](./references/04-postflight.md) | diff env 找丢失的 + Description 跟 version 一致 |
| 4. Verify | [references/05-verify.md](./references/05-verify.md) | qmd doctor + memory_search + per agent serial rebuild |
| 紧急回滚 | [references/06-rollback.md](./references/06-rollback.md) | 完全跑不起来的回滚步骤 |
| 注意事项 | [references/80-notes.md](./references/80-notes.md) | 一些容易踩的点（不是 silent failure 之王） |

## 辅助脚本

| 脚本 | 用途 |
|------|------|
| `scripts/backup-env.sh` | 一键备份 service unit + binary + per agent dbs |
| `scripts/diff-env.sh` | diff 当前 service 跟 .bak，列丢失的 user env |
| `scripts/qmd-rebuild-serial.sh` | **串行**重建 per agent qmd index（不并发）|
| `scripts/upgrade-report.sh` | 输出升级报告模板 |

## 核心原则（记住这 5 条就够了）

1. **先备份再动手** — 任何升级前必须有可回滚点
2. **env 是最容易丢的** — service unit 升级时**不保留** user 自定义 env
3. **service 跟 user shell GPU 资源不同** — LD_LIBRARY_PATH / CUDA_HOME 必须显式设
4. **per agent rebuild 不要并发** — 抢 batch embed lock + GPU = timeout 砍
5. **大版本升级前看 changelog** — qmd 跳 0.1.x → 2.0 / 2.5 是 silent ABI mismatch 高发期

## 触发场景

- user 喊"升级 OpenClaw" / "5.28 → 6.0" / "升级 5.28"
- 5.28 service 跑得不对劲（memory_search 报错 / agent timeout）
- qmd 报错 ABI mismatch / Dimension mismatch / `better_sqlite3.node` 找不到
- service unit 升级后 user 自定义 env 丢失
- `nvidia-smi` 找不到但实际 GPU 在（WSL2 误判）
