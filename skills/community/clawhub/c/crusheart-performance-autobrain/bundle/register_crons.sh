#!/bin/bash
# register_crons.sh — 注册所有定时任务
# 精简版：仅 2 个任务
# 01:00 统一维护（记忆维护已合并进来）
# 05:00 引擎初始化+版本检查

set -e

echo "🕐 注册定时任务..."

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"

# 读取配置获取 channel
CHANNEL=$(python3 -c "
import sys, json, os
sys.path.insert(0, '$WORKSPACE')
try:
    from scripts.read_config import get_primary_channel, get_channel_names
    ch = get_primary_channel()
    if not ch:
        names = get_channel_names()
        ch = names[0] if names else 'default'
except Exception:
    config_path = os.environ.get('OPENCLAW_CONFIG_DIR',
        os.path.join(os.environ.get('HOME', '/tmp'), '.openclaw', 'openclaw.json'))
    if os.path.exists(config_path):
        try:
            with open(config_path) as f:
                cfg = json.load(f)
            ch = cfg.get('channels', {}).get('primary', 'default')
        except:
            ch = 'default'
    else:
        ch = 'default'
print(ch)
")

echo "  默认 Channel: $CHANNEL"

if ! openclaw cron list > /dev/null 2>&1; then
    echo "  ⚠️  openclaw cron 不可用，请确保 Gateway 正在运行"
    echo "  手动执行命令参考："
    echo ""
    echo "  # 01:00 统一维护 + 记忆维护（扫描+归档+索引重建+技能扫描+自纠错链路）"
    echo "  openclaw cron add '0 1 * * *' --channel $CHANNEL --message 'daily maintenance: health, memory, cleanup, dreams, replay + memory scan, archive, index rebuild, skill scan, self-correction'"
    echo ""
    echo "  # 05:00 引擎初始化 + 版本检查"
    echo "  openclaw cron add '0 5 * * *' --channel $CHANNEL --message 'engine init + version check'"
    exit 1
fi

# 清理旧定时任务
echo "  清理旧定时任务..."
EXISTING=$(openclaw cron list 2>/dev/null | grep -oP 'id="[^"]+"' | sed 's/id="//;s/"//')
for id in $EXISTING; do
    openclaw cron rm "$id" 2>/dev/null || true
done

# 注册新任务 — 仅 2 个
echo ""
echo "  注册 [1/2]: 01:00 统一维护（含记忆维护）"
openclaw cron add "0 1 * * *" \
    --message "统一维护+记忆维护 | 健康巡检+记忆固化+系统清理+梦境扫描+ReplayBuffer蒸馏+执行复盘+记忆扫描/归档/索引重建+技能扫描+自纠错链路" \
    --channel "$CHANNEL"

echo "  注册 [2/2]: 05:00 引擎初始化 + 版本检查"
openclaw cron add "0 5 * * *" \
    --message "引擎重初始化 | init_engines.py --bootstrap + 新版本检查 version_check.py" \
    --channel "$CHANNEL"

echo ""
echo "✅ 定时任务注册完成（精简版，共 2 个）"
