# 80 注意事项（一些容易踩的点）

**重要程度比 99-pitfalls 弱**。这些是日常升级会踩的点，不是 silent failure 之王。

## 1. service env 不继承 user shell

**症状**：
- `nvidia-smi` 看到 GPU 在用
- service 跑 qmd 报 "running on CPU" / Dimension mismatch
- 内存搜索工具超时

**原因**：
- systemd service 是独立 session，不读 `~/.bashrc`
- 升级时 service unit 会被覆盖
- 之前 user 加的 `LD_LIBRARY_PATH` / `CUDA_HOME` 丢失
- 4.21 时代 GPU 加速跑通是因为 service env 里有 CUDA 路径

**修法**：
- 升级后立刻 diff service unit 跟 .bak
- 手动追加 `LD_LIBRARY_PATH` / `CUDA_HOME` / `NVIDIA_DRIVER_CAPABILITIES` 等
- 详细看 [03-upgrade.md](./03-upgrade.md) 步骤 3

**预防**：
- 每次升级前备份 service unit（带版本号后缀）
- 升级后立刻跑 [04-postflight.md](./04-postflight.md) 体检

## 2. qmd 大版本跳级 + ABI mismatch

**症状**：
- `qmd query` / `qmd embed` 跑 5+ 分钟没结束
- `ls` / `search` 1s 跑通（不用 native）
- 报 `Could not locate the bindings file. Tried: ... better_sqlite3.node`

**原因**：
- qmd 0.1.x → 2.0.0 跳过了 1.x（2.0.0 major 重写）
- 2.0.0 引入 better-sqlite3 ^12.4.5（**Node 25 ABI**）
- OpenClaw 跑 Node 22 = **ABI mismatch**
- 默默降级到 pure JS 路径 = 5+ 分钟 hang

**修法**：
- 升级到 qmd 2.5.3+（修了 pnpm-global + Bun 路由 ABI bug）
- 升级后 `npm rebuild better-sqlite3` 重编 native binding

**预防**：
- 升级前看 qmd GitHub releases（https://github.com/tobi/qmd/releases）
- 看 CHANGELOG 找 ABI 改动
- 升级 qmd 后必须 rebuild better-sqlite3

## 3. per agent memory dbs 不是全局 db

**症状**：
- 清了 `~/.cache/qmd/index.sqlite` watch 还是 0 vectors
- 找不到 service 实际用的 db

**原因**：
- 期望路径是 per agent：`~/.openclaw/agents/<id>/qmd/xdg-cache/qmd/index.sqlite`
- **不是** `~/.cache/qmd/index.sqlite`（CLI 全局 db）
- 之前用 0.1.x 时代全局 db 习惯了

**修法**：
- per agent db 路径才对
- 全局 db 是 `qmd` CLI 用的，跟 service 无关
- rebuild 必须 per agent 跑

**预防**：
- 升级后跑 `find ~/.openclaw/agents/*/qmd/xdg-cache/qmd -name "index.sqlite"` 看实际 db 数量

## 4. concurrent reindex 必卡死

**症状**：
- 32 个并发 `openclaw memory index --force` 全部 timeout 120s
- `qmd embed failed: file lock timeout`
- 14-15 min 跑不完任何 agent

**原因**：
- 32 个并发 reindex 抢 batch embed lock
- 抢 GPU 资源
- 5min interval 调度堆积

**修法**：
- **串行**：`for agent in $agents; do openclaw memory index --force --agent $agent; done`
- 30-50s/agent，32 个 16-20 min 跑完

**预防**：
- 任何"资源紧张"操作（embed / reindex / sync 涉及 GPU + 锁）**默认串行**
- 想并发前先想清楚是不是会抢同一个 lock

## 5. qmd collection add conflict spam log

**症状**：
- log 里刷 `qmd collection add skipped for docs-<agent>`
- 看起来严重但不影响功能

**原因**：
- watch 跑 `qmd collection add --name docs-<agent>`
- qmd 内部 metadata 已经有 `docs-<agent>`（不同 name）
- 跳过但 collection 还在 db 里

**修法**：
- **不要修**！这是 WARN 不是 ERROR
- 多个 agent 都会触发
- 不影响 functionality

**预防**：
- 升级后看 log 时忽略这行

## 6. OPENCLAW_SERVICE_VERSION 跟 binary 不一致

**症状**：
- service unit 标 `v2026.4.27-local` 但 binary 是 5.28
- 排查时迷惑

**原因**：
- 升级包改了 service unit 但没更新 version

**修法**：
- 升级后改 `Description` + `OPENCLAW_SERVICE_VERSION` 跟 binary 实际版本一致
- 详细看 [03-upgrade.md](./03-upgrade.md) 步骤 4

**预防**：
- 升级完成前最后一步必做

## 7. qmd watch 5min interval 是 lazy init

**症状**：
- 升级后 watch 5min interval 不跑
- 等 10+ min 还没 sync / embed
- per agent db 都是 0 vectors

**原因**：
- watch 5min interval 只在 agent 第一次 `memory_search` 触发
- 不会在 service restart 后自动跑所有 agent

**修法**：
- 手动触发：`openclaw memory index --force --agent <id>` × 32
- 串行跑（[references/05-verify.md](./05-verify.md) 步骤 6）
- 32 个 16-20 min 跑完

**预防**：
- 升级脚本里包含"逐个 agent reindex"步骤
- 不要等 watch 5min 自然跑

## 8. 不要凭 `nvidia-smi` 找不到就判定 GPU 不在

**症状**：
- `nvidia-smi` command not found
- 误以为没 GPU
- 不查 LD_LIBRARY_PATH

**原因**：
- WSL2 下 nvidia-smi 实际路径在 `/usr/lib/wsl/lib/nvidia-smi`
- 不在默认 PATH 里
- 但**实际 GPU 一直在用**

**修法**：
- 用 `/usr/lib/wsl/lib/nvidia-smi` 跑
- 或者 `qmd doctor` 看 `device probe: GPU cuda`

**预防**：
- 升级前先 `/usr/lib/wsl/lib/nvidia-smi` 跑一下确认 GPU 实际状态
- 升级后 `qmd doctor` 是 GPU 真证据
