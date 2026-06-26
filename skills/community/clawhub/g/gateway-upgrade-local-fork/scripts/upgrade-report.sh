#!/bin/bash
# upgrade-report.sh - 输出升级报告模板
# 用法: bash upgrade-report.sh <old-ver> <new-ver>

OLD_VER=${1:-?}
NEW_VER=${2:-?}

PID=$(systemctl --user show -p MainPID openclaw-gateway.service | cut -d= -f2)

cat <<EOF
# OpenClaw 升级报告 $OLD_VER → $NEW_VER

## 时间
$(date '+%Y-%m-%d %H:%M:%S %Z')

## 改动

### Binary
- 旧路径: 看 .bak service unit ExecStart
- 新路径: $(grep '^ExecStart=' ~/.config/systemd/user/openclaw-gateway.service | head -1)

### Service
- 旧 .bak: ~/.config/systemd/user/openclaw-gateway.service.bak.$OLD_VER
- 新: ~/.config/systemd/user/openclaw-gateway.service
- Description: $(grep '^Description=' ~/.config/systemd/user/openclaw-gateway.service | head -1)
- OPENCLAW_SERVICE_VERSION: $(grep '^Environment=OPENCLAW_SERVICE_VERSION=' ~/.config/systemd/user/openclaw-gateway.service | head -1)

### Env 保留
$(for env in CUDA_HOME LD_LIBRARY_PATH NVIDIA_DRIVER_CAPABILITIES QMD_EMBED_MODEL HF_ENDPOINT; do
    if grep -q "^Environment=$env=" ~/.config/systemd/user/openclaw-gateway.service; then
        val=$(grep "^Environment=$env=" ~/.config/systemd/user/openclaw-gateway.service | head -1 | cut -d= -f2-)
        echo "- ✓ $env=$val"
    else
        echo "- ✗ $env MISSING"
    fi
done)

### qmd (如果升级了)
- 旧: 看 /tmp/npm-global-pre-upgrade-*.txt
- 新: $(qmd --version 2>&1)

## 健康检查

EOF

# 实际跑 qmd doctor 填报告
echo "### qmd doctor"
qmd doctor 2>&1 | head -30

echo ""
echo "### GPU 状态"
/usr/lib/wsl/lib/nvidia-smi 2>&1 | grep -E "GeForce|MiB /" | head -3

echo ""
echo "### per agent qmd db"
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
echo "- 有 vectors: $done / 33"
echo "- 总 vectors: $total_v"

cat <<EOF

## 备份位置
- service: ~/.config/systemd/user/openclaw-gateway.service.bak.$OLD_VER
- per agent dbs: ~/.openclaw/agents/*/qmd/xdg-cache/qmd/index.sqlite.bak.<ts>
- binary (如果备了): ~/openclaw-local.bak.<ts>

## 升级后测试
- [ ] memory_search 工具 5-20s 返结果
- [ ] qmd doctor 报 GPU cuda
- [ ] per agent rebuild 31+ / 33
- [ ] 0 个 ECONNRESET / batch timeout
EOF
