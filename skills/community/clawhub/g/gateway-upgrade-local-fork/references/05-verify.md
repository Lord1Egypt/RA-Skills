# 05 Verify（健康检查）

**目的**：确认 memory_search 工具 + GPU 加速 + per agent 都正常。

## 步骤

### 1. service 状态

```bash
systemctl --user status openclaw-gateway.service
# 应该 active (running), 启动时间应该是刚才 restart 之后

PID=$(systemctl --user show -p MainPID openclaw-gateway.service | cut -d= -f2)
echo "PID: $PID"
# RSS 应该 1-3GB (启动后 + watch 5min interval 加载)
ps -o pid,rss,vsz,cmd -p $PID
```

### 2. 跑 qmd doctor

```bash
qmd doctor 2>&1 | tee /tmp/qmd-doctor-verify.txt
```

**必须**看到：
- `✓ SQLite runtime: 3.53.1` (或更新)
- `✓ better-sqlite3 package: 12.10.0` (或更新)
- `✓ sqlite-vec: v0.1.9` (或更新)
- `✓ device probe: GPU cuda; offloading enabled; devices: NVIDIA GeForce RTX 3080; VRAM ...GB free`
- `✓ embedding fingerprints: no vectors yet; current fingerprint <hash>` 或 `1 docs on current fingerprint`
- `✓ embedding vector sample: 1 sampled chunk reproduce stored vectors`

**如果 device probe 报 "running on CPU"** —— 升级时 LD_LIBRARY_PATH / NVIDIA_DRIVER_CAPABILITIES 没合并成功。回 [references/03-upgrade.md](./03-upgrade.md) 修。

### 3. GPU 实际在用

```bash
/usr/lib/wsl/lib/nvidia-smi 2>&1 | grep -E "MiB|GeForce"
# 应该有 NVIDIA GeForce RTX 3080 + VRAM total 10240MiB
# 跑 qmd embed 跑过的话 Memory-Usage 应该 ≥ 6-8GB
```

### 4. 测试 memory_search 工具（实跑一次）

```bash
# user 之前说"修复前别用 memory_search"，升级完成后用一次验证
# 在 OpenClaw 内部工具用一次（memory_search 之类）
```

期望：
- searchMs 应该在 5-20s（之前 ECONNRESET 5min+ timeout）
- 返回 1+ 个 result
- error 不应该是 batch timeout / Dimension mismatch

### 5. per agent qmd db 状态

```bash
echo "=== per agent qmd db 状态 ==="
done=0
total_v=0
for agent in $(ls -d ~/.openclaw/agents/*/ 2>/dev/null | xargs -n1 basename); do
    db="\$HOME/.openclaw/agents/$agent/qmd/xdg-cache/qmd/index.sqlite"
    if [ -f "$db" ]; then
        vectors=$(sqlite3 "$db" "SELECT COUNT(*) FROM content_vectors;" 2>/dev/null)
        total_v=$((total_v + vectors))
        if [ "$vectors" -gt "0" ] 2>/dev/null; then
            done=$((done + 1))
        fi
    fi
done
echo "有 vectors: $done / 33"
echo "总 vectors: $total_v"
```

### 6. 串行 rebuild 需要的 agent（**不并发**）

```bash
# 跑 scripts/qmd-rebuild-serial.sh
bash ~/.openclaw/workspace-main/skills/gateway-upgrade-local-fork/scripts/qmd-rebuild-serial.sh
```

**为什么串行**：
- 32 个并发 reindex 抢 batch embed lock + GPU 资源 = 14-15min timeout 砍
- 串行 30-50s/agent，32 个 16-20 min 跑完
- 串行 GPU 持续 7GB 利用率，并发反而 timeout 全部失败

**进度监控**：
```bash
# 看实时进度
tail -f /tmp/qmd-serial-reindex.log
```

### 7. 等 5-10min 让 watch 跑完

```bash
# watch 5min interval 5min 后跑下一次
# 跑完所有 agent embed 后, watch 5min 5min interval 还在跑
# 但 memory_search 应该已经能用了（不依赖所有 agent 完成）
```

## Verify 通过 checklist

- [ ] service active
- [ ] qmd doctor 报 GPU cuda
- [ ] memory_search 工具 5-20s 返结果
- [ ] per agent 32/33 有 vectors
- [ ] 0 个 qmd embed failed
- [ ] 0 个 ECONNRESET / batch timeout
- [ ] nvidia-smi 看 GPU 显存用了 ≥ 6GB (qmd embed 跑过)

## 不通过常见原因

| 症状 | 原因 | 修法 |
|------|------|------|
| qmd doctor 报 CPU | LD_LIBRARY_PATH 没合并 | 回 [03-upgrade.md](./03-upgrade.md) |
| memory_search 报 batch timeout | qmd.limits.timeoutMs 不够 / watch 5min 还在跑 | 等 5min + 调 timeout 120s → 600s |
| per agent 0 vectors | lazy init | 跑 [scripts/qmd-rebuild-serial.sh](./../scripts/qmd-rebuild-serial.sh) |
| 报 Dimension mismatch | 旧 db vec0 schema 跟新 model dim 不一致 | 删 db + 串行 rebuild |
| 报 ABI mismatch | better-sqlite3 native binding 没编译 | `cd $(npm root -g)/@tobilu/qmd && npm rebuild better-sqlite3` |
