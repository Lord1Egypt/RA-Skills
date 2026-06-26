#!/bin/bash
# 点点数据每日自动获取脚本
# 功能：获取所有 12 个渠道的上架榜和下架榜，并发送到钉钉
# 规则：
# - 每个平台请求之间等待 3 分钟，避免触发频率限制
# - 连续 2 次失败 → 立即停止，通知用户（防止 IP 被封）

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
VENV_PYTHON="$SKILL_DIR/venv/bin/python"
LOG_FILE="$SKILL_DIR/logs/daily_fetch_$(date +%Y%m%d).log"
FAIL_COUNT=0
MAX_FAILURES=2

# 确保日志目录存在
mkdir -p "$SKILL_DIR/logs"

echo "========================================" | tee -a "$LOG_FILE"
echo "📊 点点数据每日自动获取" | tee -a "$LOG_FILE"
echo "开始时间：$(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$LOG_FILE"
echo "规则：每个平台间隔 3 分钟，连续 $MAX_FAILURES 次失败停止" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"

# 1. 启动浏览器（如果未运行）
echo "" | tee -a "$LOG_FILE"
echo "📖 Step 1: 启动浏览器..." | tee -a "$LOG_FILE"
if ! pgrep -f "chrome.*9222" > /dev/null; then
    echo "   📌 浏览器未运行，启动中..." | tee -a "$LOG_FILE"
    bash "$SCRIPT_DIR/keep_browser_alive.sh" >> "$LOG_FILE" 2>&1
    sleep 5
    echo "   ✅ 浏览器已启动" | tee -a "$LOG_FILE"
else
    echo "   ✅ 浏览器已在运行" | tee -a "$LOG_FILE"
fi

# 2. 定义平台列表
PLATFORMS=(
    "appstore"
    "huawei"
    "xiaomi"
    "vivo"
    "oppo"
    "meizu"
    "tencent"
    "baidu"
    "qihoo360"
    "honor"
    "harmony"
    "wandoujia"
)

# 函数：处理单个平台，处理失败计数
# 规则：只有登录失败（IP封禁/连接失败）才会增加计数
# 单个平台获取失败但登录正常，不增加连续失败计数
process_platform() {
    local platform="$1"
    local extra_args="$2"
    
    echo "   📊 获取 $platform $extra_args..." | tee -a "$LOG_FILE"
    if $VENV_PYTHON "$SCRIPT_DIR/diandian_connect.py" --platform "$platform" $extra_args --force >> "$LOG_FILE" 2>&1; then
        echo "   ✅ $platform $extra_args 获取成功" | tee -a "$LOG_FILE"
        FAIL_COUNT=0  # 重置失败计数
        return 0
    else
        echo "   ❌ $platform $extra_args 获取失败" | tee -a "$LOG_FILE"
        # 检查是否是 IP 封禁/登录失败
        if grep -q "访问被禁止\|403\|登录失败\|未找到邮箱" "$LOG_FILE"; then
            FAIL_COUNT=$((FAIL_COUNT + 1))
            echo "   ⚠️ 检测到登录/访问失败，连续失败计数: $FAIL_COUNT" | tee -a "$LOG_FILE"
        else
            # 单个平台数据获取失败，但登录正常，不增加连续失败计数
            FAIL_COUNT=0
            echo "   ⚠️ 单次获取失败（登录正常），不增加连续失败计数" | tee -a "$LOG_FILE"
        fi
        return 1
    fi
}

# 3. 获取上架榜单
echo "" | tee -a "$LOG_FILE"
echo "📖 Step 2: 获取上架榜单..." | tee -a "$LOG_FILE"
for platform in "${PLATFORMS[@]}"; do
    # 检查失败计数
    if [ "$FAIL_COUNT" -ge "$MAX_FAILURES" ]; then
        echo "⛔ 连续 $MAX_FAILURES 次获取失败，停止执行，请检查 IP 是否被封禁" | tee -a "$LOG_FILE"
        # 发送钉钉通知
        if [ -f "$SCRIPT_DIR/dingtalk-notify.sh" ]; then
            bash "$SCRIPT_DIR/dingtalk-notify.sh" "⛔ 点点数据每日获取停止，连续 $MAX_FAILURES 次失败。可能 IP 被点点数据封禁，请检查。"
        fi
        exit 1
    fi
    
    # 处理平台
    process_platform "$platform" ""
    
    # 等待 3 分钟（如果不是最后一个）
    if [ "$platform" != "${PLATFORMS[-1]}" ]; then
        echo "   ⏳ 等待 3 分钟 (${FAIL_COUNT} failures)..." | tee -a "$LOG_FILE"
        sleep 180
    fi
done

# 重置失败计数（上架和下架分开算）
FAIL_COUNT=0

# 4. 获取下架榜单
echo "" | tee -a "$LOG_FILE"
echo "📖 Step 3: 获取下架榜单..." | tee -a "$LOG_FILE"
for platform in "${PLATFORMS[@]}"; do
    # 检查失败计数
    if [ "$FAIL_COUNT" -ge "$MAX_FAILURES" ]; then
        echo "⛔ 连续 $MAX_FAILURES 次获取失败，停止执行，请检查 IP 是否被封禁" | tee -a "$LOG_FILE"
        # 发送钉钉通知
        if [ -f "$SCRIPT_DIR/dingtalk-notify.sh" ]; then
            bash "$SCRIPT_DIR/dingtalk-notify.sh" "⛔ 点点数据每日获取停止，连续 $MAX_FAILURES 次失败。可能 IP 被点点数据封禁，请检查。"
        fi
        exit 1
    fi
    
    # 处理平台
    process_platform "$platform" "--offline"
    
    # 等待 3 分钟（如果不是最后一个）
    if [ "$platform" != "${PLATFORMS[-1]}" ]; then
        echo "   ⏳ 等待 3 分钟 (${FAIL_COUNT} failures)..." | tee -a "$LOG_FILE"
        sleep 180
    fi
done

# 5. 完成
echo "" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "✅ 任务完成！" | tee -a "$LOG_FILE"
echo "结束时间：$(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"

# 6. 保持浏览器运行（不关闭）
echo "" | tee -a "$LOG_FILE"
echo "💡 浏览器保持运行状态，供下次使用" | tee -a "$LOG_FILE"
