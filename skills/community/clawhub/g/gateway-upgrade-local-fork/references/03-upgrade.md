# 03 Upgrade（跑升级 + 合并 user env）

**目的**：升级 binary + 合并 user 自定义 env 到新 service unit。

**关键警告**：升级包会**重置 service unit**，user 自定义 env 全部丢失。**必须**手动合并回来。

## 步骤

### 1. 跑升级脚本

升级方式取决于 OpenClaw 提供方式：

```bash
# 方式 A: packaged installer (推荐)
# (跑 OpenClaw 自带的 install.sh 或 upgrade)

# 方式 B: git pull (源码升级)
cd $HOME/openclaw-local
git fetch origin
git checkout v2026.X.Y
npm install  # 重装依赖
npm run build  # 重新编译

# 方式 C: 直接换 binary 目录
# (OpenClaw 提供 tarball / deb 包)
```

### 2. 升级完成后立即 diff env

```bash
# diff 完整 service unit 跟升级前 .bak
diff ~/.config/systemd/user/openclaw-gateway.service.bak.<old-ver> \
     ~/.config/systemd/user/openclaw-gateway.service
```

### 3. 手动合并 user env（关键！）

```bash
# 跑 scripts/diff-env.sh 看丢失的
bash ~/.openclaw/workspace-main/skills/gateway-upgrade-local-fork/scripts/diff-env.sh

# 手动追加 user 自定义 env 到 service unit
SERVICE=~/.config/systemd/user/openclaw-gateway.service

# 按 4.21 时代 user 加过的顺序追加
grep -q "^Environment=CUDA_HOME=" $SERVICE || \
    sed -i '/^Environment=HF_ENDPOINT=/a Environment=CUDA_HOME=/usr/local/cuda' $SERVICE

grep -q "^Environment=LD_LIBRARY_PATH=" $SERVICE || \
    sed -i '/^Environment=CUDA_HOME=/a Environment=LD_LIBRARY_PATH=/usr/lib/wsl/lib:/usr/local/cuda/lib64:$LD_LIBRARY_PATH' $SERVICE

grep -q "^Environment=NVIDIA_DRIVER_CAPABILITIES=" $SERVICE || \
    sed -i '/^Environment=LD_LIBRARY_PATH=/a Environment=NVIDIA_DRIVER_CAPABILITIES=compute,utility' $SERVICE

grep -q "^Environment=QMD_EMBED_MODEL=" $SERVICE || \
    sed -i '/^Environment=NVIDIA_DRIVER_CAPABILITIES=/a Environment=QMD_EMBED_MODEL=hf:Qwen/Qwen3-Embedding-0.6B-GGUF/Qwen3-Embedding-0.6B-Q8_0.gguf' $SERVICE
```

**注意**：升级时 4.27/4.21 时代 user 加的 env（LD_LIBRARY_PATH / QMD_EMBED_MODEL / HF_ENDPOINT）**可能已经被升级包重置**。**逐个检查 + 重新加**。

### 4. 修 service unit Description + version 一致

```bash
# 实际 binary 版本
NEW_VER=$(node -e "console.log(require('\$HOME/openclaw-local/package.json').version)" 2>/dev/null)

# 修 Description 跟 binary 一致
sed -i "s|Description=OpenClaw Gateway (v.*)|Description=OpenClaw Gateway (v${NEW_VER}-local)|" \
    ~/.config/systemd/user/openclaw-gateway.service

# 修 OPENCLAW_SERVICE_VERSION
sed -i "s|Environment=OPENCLAW_SERVICE_VERSION=.*|Environment=OPENCLAW_SERVICE_VERSION=${NEW_VER}-local|" \
    ~/.config/systemd/user/openclaw-gateway.service
```

### 5. 检查 qmd 大版本

**不是每次都重装 qmd**。判断标准：
- 小版本升级（如 5.28.0 → 5.28.1）：**不动 qmd**
- 大版本升级（如 5.27 → 5.28）且 qmd 跳大版本：考虑升级 qmd

```bash
qmd --version
# 撞 better-sqlite3 ^12 ABI mismatch 报错
# → 升级到 qmd 2.5.3+（修了 pnpm-global + Bun 路由 ABI bug）

# 升级 qmd（仅在需要时）
npm install -g @tobilu/qmd@latest

# 重要：升级 qmd 后必须重编 better-sqlite3 native binding
cd $(npm root -g)/@tobilu/qmd
npm rebuild better-sqlite3
```

### 6. daemon-reload + 硬重启 service

```bash
# ⚠️ 必须硬重启 (systemctl restart)，不是 SIGUSR1 软重启
# 软重启不会重新读 service env
systemctl --user daemon-reload
systemctl --user restart openclaw-gateway.service
```

### 7. 验证新 env 生效

```bash
# 等 5s 让 service 完全启动
sleep 5

NEW_PID=$(systemctl --user show -p MainPID openclaw-gateway.service | cut -d= -f2)
echo "New PID: $NEW_PID"
echo ""
echo "=== Service env (验证) ==="
for env in CUDA_HOME LD_LIBRARY_PATH NVIDIA_DRIVER_CAPABILITIES QMD_EMBED_MODEL HF_ENDPOINT; do
    val=$(cat /proc/$NEW_PID/environ 2>/dev/null | tr '\0' '\n' | grep "^$env=")
    if [ -n "$val" ]; then
        echo "  ✓ $env"
    else
        echo "  ✗ $env MISSING"
    fi
done
```

## 主观判断点

- **升级后 service 跑得不对要不要立刻回滚？** —— 一般**等 5-10min** 让 boot update 跑完，看是不是 lazy init 卡住。如果 10min 后还跑不起来，再回滚
- **qmd 升级还是降级？** —— **升**。2.0.x 有 ABI bug，2.5.3 修了 + 加 fingerprint 机制
- **qmd model 选 Qwen3 还是 embeddinggemma？** —— **Qwen3**（中文质量好）+ 有 GPU 加速
- **plugin SDK 升级不兼容？** —— 看 OpenClaw 升级包 CHANGELOG，破坏性变更列得很清楚

## 升级后立即跑

```bash
# 验证 GPU 加速
qmd doctor | grep -E "device|GPU"
# 应该报 "device probe: GPU cuda; NVIDIA GeForce RTX 3080" (或你的 GPU 型号)

# 验证 fingerprint
qmd doctor | grep -E "fingerprint|freshness"
# 应该报 "embedding freshness: all active documents match current fingerprint"
```
