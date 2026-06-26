# 04 Post-Flight（env diff 报告）

**目的**：明确知道升级丢了/改了啥，避免隐性回归。

## 步骤

### 1. 完整 diff service unit

```bash
# 升级前的 .bak 跟现在的对比
diff ~/.config/systemd/user/openclaw-gateway.service.bak.<old-ver> \
     ~/.config/systemd/user/openclaw-gateway.service
```

**重点看**：
- `Description=` 是否跟 binary 实际版本一致
- `ExecStart=` binary 路径是否对（升级可能从旧目录切到新目录）
- `OPENCLAW_SERVICE_VERSION=` 是否跟 binary 一致
- 哪些 user 加的 env 丢失

### 2. 关键 env 检查清单

```bash
SERVICE=~/.config/systemd/user/openclaw-gateway.service

echo "=== 关键 env 检查 (5 个常丢) ==="
for env in CUDA_HOME LD_LIBRARY_PATH NVIDIA_DRIVER_CAPABILITIES QMD_EMBED_MODEL HF_ENDPOINT; do
    if grep -q "^Environment=$env=" $SERVICE; then
        val=$(grep "^Environment=$env=" $SERVICE | head -1 | cut -d= -f2-)
        echo "  ✓ $env=$val"
    else
        echo "  ✗ $env MISSING"
    fi
done
```

### 3. 跑 qmd doctor 看升级后状态

```bash
qmd doctor 2>&1 | tee /tmp/qmd-doctor-post-upgrade.txt
```

**跟 pre-upgrade baseline 对比**：

```bash
diff /tmp/qmd-doctor-pre-upgrade.txt /tmp/qmd-doctor-post-upgrade.txt
```

**重点看**：
- device probe: 之前 CPU → 现在 GPU cuda ？
- better-sqlite3 version: 升级了吗？
- sqlite-vec version
- embedding fingerprint
- embedding freshness

### 4. 看 boot update 跑了没

```bash
tail -200 /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep -E "qmd manager initialized|qmd watcher ready"
```

应该看到每个 per agent 至少一次 `qmd manager initialized` 跟 `qmd watcher ready`。

### 5. 跑 env diff 脚本

```bash
bash ~/.openclaw/workspace-main/skills/gateway-upgrade-local-fork/scripts/diff-env.sh
```

会输出 user 关心的 env 是否都在 + 哪些被升级包改了。

## 体检报告

```markdown
# Post-flight Report

## 时间
<timestamp>

## service unit diff 摘要
- Description: <old> → <new>
- OPENCLAW_SERVICE_VERSION: <old> → <new>
- ExecStart: <old> → <new>
- <N> user env 保留, <M> 丢失

## user env 状态
- CUDA_HOME: ✓/✗
- LD_LIBRARY_PATH: ✓/✗
- NVIDIA_DRIVER_CAPABILITIES: ✓/✗
- QMD_EMBED_MODEL: ✓/✗
- HF_ENDPOINT: ✓/✗

## qmd doctor 状态
- better-sqlite3: <version>
- sqlite-vec: <version>
- device probe: GPU cuda or CPU
- fingerprint: <value>
- freshness: all match or pending

## 下一步
- 跑 references/05-verify.md
```
