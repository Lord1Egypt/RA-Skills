# 01 Pre-flight（升级前体检）

**目的**：建立基线，记录"现在好的状态是什么样"，升级后好对比。

## 检查清单

### 1. 备份 service unit（必须带版本后缀）

```bash
# 当前 service unit 在 ~/.config/systemd/user/openclaw-gateway.service
# 备份到 .bak.<old-version>
OLD_VER=$(node -e "console.log(require('\$HOME/openclaw-local/package.json').version)" 2>/dev/null)
cp ~/.config/systemd/user/openclaw-gateway.service{,.bak.\$OLD_VER}
```

### 2. 记录 baseline

```bash
echo "=== Service Description ==="
systemctl --user show openclaw-gateway.service -p Description
echo ""
echo "=== Service version env ==="
PID=$(systemctl --user show -p MainPID openclaw-gateway.service | cut -d= -f2)
cat /proc/$PID/environ 2>/dev/null | tr '\0' '\n' | grep -E "OPENCLAW_SERVICE_VERSION|OPENCLAW_SERVICE_MARKER"
echo ""
echo "=== Binary path ==="
cat /proc/$PID/cmdline 2>/dev/null | tr '\0' ' '
echo ""
echo "=== Binary version ==="
node -e "console.log(require('\$HOME/openclaw-local/package.json').version)"
```

### 3. 跑 qmd doctor baseline

```bash
# 2.5.0+ 才有 qmd doctor
qmd --version
qmd doctor 2>&1 | tee /tmp/qmd-doctor-pre-upgrade.txt
```

**重点记录**：
- SQLite runtime version
- better-sqlite3 package version
- sqlite-vec version
- **device probe**: GPU 还是 CPU
- embedding fingerprint
- embedding freshness

### 4. GPU 状态

```bash
# WSL2 下 nvidia-smi 实际位置可能在 /usr/lib/wsl/lib/nvidia-smi
which nvidia-smi 2>&1 || echo "(nvidia-smi not in PATH, try /usr/lib/wsl/lib/)"
/usr/lib/wsl/lib/nvidia-smi 2>&1 | head -20
```

**重点记录**：
- GPU 型号
- Driver Version
- CUDA Version
- VRAM 总数
- 当前使用率

### 5. per agent qmd db 状态

```bash
# 5.28 期望路径是 per agent，不是全局
for agent in $(ls -d ~/.openclaw/agents/*/ 2>/dev/null | xargs -n1 basename); do
    db="\$HOME/.openclaw/agents/$agent/qmd/xdg-cache/qmd/index.sqlite"
    if [ -f "$db" ]; then
        size=$(stat -c %s "$db")
        vectors=$(sqlite3 "$db" "SELECT COUNT(*) FROM content_vectors;" 2>/dev/null)
        echo "$agent: ${size}B, ${vectors} vectors"
    fi
done
```

### 6. 找出 user 自定义 env（关键！升级后必须合并回来）

```bash
# 对比当前 service 跟 user .bashrc / .profile 找 user 加的 env
echo "=== ~/.bashrc CUDA/QMD env ==="
grep -iE "cuda|ld_lib|qmd|hf|hfendpoint" ~/.bashrc 2>&1 | head -10
echo ""
echo "=== ~/.profile CUDA/QMD env ==="
grep -iE "cuda|ld_lib|qmd|hf|hfendpoint" ~/.profile 2>&1 | head -10
echo ""
echo "=== 当前 service unit env (找 user 加的非默认) ==="
grep "^Environment=" ~/.config/systemd/user/openclaw-gateway.service
```

**user 4.21 / 4.27 时代加过的 env 列表**（升级后必须合并回来）：
- `CUDA_HOME=/usr/local/cuda`
- `LD_LIBRARY_PATH=/usr/lib/wsl/lib:/usr/local/cuda/lib64:$LD_LIBRARY_PATH`
- `NVIDIA_DRIVER_CAPABILITIES=compute,utility`
- `QMD_EMBED_MODEL=hf:Qwen/Qwen3-Embedding-0.6B-GGUF/Qwen3-Embedding-0.6B-Q8_0.gguf`
- `HF_ENDPOINT=https://hf-mirror.com`

### 7. 列出 user 装过的 npm global packages

```bash
npm list -g --depth=0 > /tmp/npm-global-pre-upgrade-$(date +%Y%m%d).txt
```

特别关注：
- `@tobilu/qmd`（qmd 版本，跟 OpenClaw dist 兼容性极重要，**大版本升级时才需要重装**）
- 其他 user 手动装的 LLM provider / plugin SDK

## 体检报告模板

```markdown
# Pre-flight Report

## 时间
<timestamp>

## Baseline
- service Description: <description>
- binary version: <version>
- binary path: <path>

## Service env (user 自定义)
- CUDA_HOME: <value or MISSING>
- LD_LIBRARY_PATH: <value or MISSING>
- NVIDIA_DRIVER_CAPABILITIES: <value or MISSING>
- QMD_EMBED_MODEL: <value or MISSING>
- HF_ENDPOINT: <value or MISSING>

## GPU
- 型号: <model>
- Driver: <version>
- CUDA: <version>
- VRAM: <size>

## qmd doctor
- better-sqlite3: <version>
- sqlite-vec: <version>
- device probe: <GPU or CPU>

## per agent
- 33 agents, <N> have vectors, <M> need rebuild

## 备份位置
- service: ~/.config/systemd/user/openclaw-gateway.service.bak.<old-ver>
- npm global: /tmp/npm-global-pre-upgrade-<date>.txt
- qmd doctor: /tmp/qmd-doctor-pre-upgrade.txt
```
