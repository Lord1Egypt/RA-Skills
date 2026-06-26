#!/bin/bash
#
# 百炼套餐用量查询（Browser Tool 版本）
# 使用 openclaw browser tool + evaluate 直接提取数据，无 cookie 依赖
#

set -e

BAILIAN_URL='https://bailian.console.aliyun.com/cn-beijing/?tab=coding-plan#/efm/detail'
TOOLS_PATH="$HOME/.openclaw/workspace/TOOLS.md"

# 从 TOOLS.md 读取账号密码
read_credentials() {
    ACCOUNT=$(grep '\*\*账号\*\*:' "$TOOLS_PATH" | head -1 | sed 's/.*账号\*\*: *//' | tr -d '\r')
    PASSWORD=$(grep '\*\*密码\*\*:' "$TOOLS_PATH" | head -1 | sed 's/.*密码\*\*: *//' | tr -d '\r')
    
    if [ -z "$ACCOUNT" ] || [ -z "$PASSWORD" ]; then
        echo "❌ 未在 TOOLS.md 中找到百炼账号信息"
        exit 1
    fi
    
    echo "$ACCOUNT|$PASSWORD"
}

# 输出报告
output_report() {
    local status="$1"
    local days_left="$2"
    local expire_date="$3"
    local auto_renew="$4"
    local last_stat="$5"
    local h5_usage="$6"
    local h5_reset="$7"
    local w1_usage="$8"
    local w1_reset="$9"
    local m1_usage="${10}"
    local m1_reset="${11}"
    local error="${12}"
    
    if [ -n "$error" ]; then
        echo "## 📊 百炼 Coding Plan 套餐详情"
        echo ""
        echo "查询失败：$error"
        return
    fi
    
    echo "## 📊 百炼 Coding Plan 套餐详情"
    echo ""
    echo "**套餐状态：** $status | 剩余 **$days_left 天**（$expire_date 到期）"
    echo "**自动续费：** $auto_renew"
    echo ""
    echo "**用量消耗：**"
    echo "- 最后统计时间：$last_stat"
    echo "- 近 5 小时：**$h5_usage**（$h5_reset **重置**）"
    echo "- 近一周：**$w1_usage**（$w1_reset **重置**）"
    echo "- 近一月：**$m1_usage**（$m1_reset **重置**）"
    echo ""
    echo "**可用模型：** 千问系列 / 智谱 / Kimi / MiniMax"
    
    # 用量分析
    echo ""
    echo "---"
    echo ""
    echo "### 💡 用量分析"
    
    # 提取百分比数字进行比较
    local h5_pct=$(echo "$h5_usage" | sed 's/%//g')
    local w1_pct=$(echo "$w1_usage" | sed 's/%//g')
    local m1_pct=$(echo "$m1_usage" | sed 's/%//g')
    
    if [ "$h5_pct" != "-" ] && [ "$w1_pct" != "-" ] && [ "$m1_pct" != "-" ]; then
        if [ "$h5_pct" -lt 90 ] && [ "$w1_pct" -lt 90 ] && [ "$m1_pct" -lt 90 ]; then
            echo "- ✅ 用量充足"
        elif [ "$h5_pct" -lt 95 ] && [ "$w1_pct" -lt 95 ] && [ "$m1_pct" -lt 95 ]; then
            echo "- ⚠️ 用量紧张"
        else
            echo "- ❌ 用量不足"
        fi
    fi
    
    if [ "$days_left" != "-" ] && [ "$days_left" -le 7 ] 2>/dev/null; then
        echo "- ⚠️ 套餐将在 $days_left 天后到期，请及时续费"
    fi
}

# 主流程
main() {
    echo "🔐 开始查询百炼套餐用量..."
    
    # 读取账号（从 TOOLS.md 安全读取，不在日志中显示）
    CREDS=$(read_credentials)
    ACCOUNT=$(echo "$CREDS" | cut -d'|' -f1)
    PASSWORD=$(echo "$CREDS" | cut -d'|' -f2)
    
    # 安全提示：凭证不在日志中输出
    
    # 1. 启动浏览器（如未运行）
    echo "🌐 启动浏览器..."
    openclaw browser start --timeout 10000 2>/dev/null || true
    sleep 2
    
    # 2. 打开页面
    echo "📄 打开百炼控制台..."
    openclaw browser open "$BAILIAN_URL" --timeout 30000 2>/dev/null
    sleep 5
    
    # 3. 获取快照，检查登录状态
    echo "  检查登录状态..."
    SNAPSHOT=$(openclaw browser snapshot --format aria --timeout 15000 2>/dev/null || echo "")
    
    # 检查是否已登录（查找邮箱、"主账号"、"退出登录"或"账号中心"）
    if echo "$SNAPSHOT" | grep -q "@qq\.com\|@.*\.com\|主账号\|退出登录\|账号中心"; then
        echo "  ✅ 已登录，跳过登录流程"
    else
        echo "  ⚠️ 未登录，开始登录流程..."
        
        # 找登录按钮并点击
        echo "  点击登录按钮..."
        openclaw browser click --text "登录" --timeout 10000 2>/dev/null || true
        sleep 2
        
        # 4. 再次快照，找账号密码框
        echo "  填写账号密码..."
        SNAPSHOT2=$(openclaw browser snapshot --format aria --timeout 15000 2>/dev/null || echo "")
        
        # 找第一个 textbox（账号）
        ACCOUNT_REF=$(echo "$SNAPSHOT2" | grep -o '"ref":"[^"]*"[^}]*"role":"textbox"' | head -1 | sed 's/.*"ref":"\([^"]*\)".*/\1/')
        
        if [ -n "$ACCOUNT_REF" ]; then
            echo "  填写账号 (ref: $ACCOUNT_REF)..."
            openclaw browser type "$ACCOUNT_REF" "$ACCOUNT" --timeout 5000 2>/dev/null || true
        else
            # 尝试用 fill
            openclaw browser fill --fields "[{\"text\":\"$ACCOUNT\"}]" --timeout 5000 2>/dev/null || true
        fi
        sleep 1
        
        # 找密码框（第二个 textbox）
        echo "  填写密码..."
        # 切换到密码框（Tab 键）
        openclaw browser press "Tab" --timeout 2000 2>/dev/null || true
        sleep 0.5
        openclaw browser type --text "$PASSWORD" --timeout 5000 2>/dev/null || true
        sleep 1
        
        # 5. 点击登录按钮
        echo "  提交登录..."
        openclaw browser click --text "立即登录" --timeout 10000 2>/dev/null || true
        
        # 等待登录完成
        echo "  等待登录完成..."
        sleep 8
        
        # 刷新页面
        echo "  刷新页面..."
        openclaw browser navigate "$BAILIAN_URL" --timeout 30000 2>/dev/null
        sleep 3
    fi
    
    # 6. 用 evaluate 提取数据
    echo "  提取数据..."
    
    # 使用 --json 获取完整响应，用 jq 提取 result 字段
    EVAL_RESPONSE=$(openclaw browser evaluate --fn "
        () => {
            const text = document.body.innerText;
            const status = text.includes('生效中') ? '✅ 生效中' : '-';
            const daysMatch = text.match(/剩余天数\s*(\d+)\s*天/);
            const daysLeft = daysMatch ? daysMatch[1] : '-';
            const expireMatch = text.match(/结束时间\s*(\d{4}-\d{2}-\d{2})/);
            const expireDate = expireMatch ? expireMatch[1] : '-';
            const autoRenew = text.includes('未开启') ? '❌ 未开启' : '✅ 已开启';
            const lastStatMatch = text.match(/最后统计时间\s*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})/);
            const lastStat = lastStatMatch ? lastStatMatch[1] : '-';
            const h5Match = text.match(/近\s*5\s*小时\s*用量[\s\S]{0,150}?(\d+)%/);
            const h5Usage = h5Match ? h5Match[1] + '%' : '-';
            const h5ResetMatch = text.match(/近\s*5\s*小时\s*用量[\s\S]{0,100}?(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s*重置/);
            const h5Reset = h5ResetMatch ? h5ResetMatch[1] : '-';
            const w1Match = text.match(/近一周用量[\s\S]{0,150}?(\d+)%/);
            const w1Usage = w1Match ? w1Match[1] + '%' : '-';
            const w1ResetMatch = text.match(/近一周用量[\s\S]{0,100}?(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s*重置/);
            const w1Reset = w1ResetMatch ? w1ResetMatch[1] : '-';
            const m1Match = text.match(/近一月用量[\s\S]{0,150}?(\d+)%/);
            const m1Usage = m1Match ? m1Match[1] + '%' : '-';
            const m1ResetMatch = text.match(/近一月用量[\s\S]{0,100}?(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s*重置/);
            const m1Reset = m1ResetMatch ? m1ResetMatch[1] : '-';
            const hasSubscription = text.includes('我的订阅');
            return JSON.stringify({status, daysLeft, expireDate, autoRenew, lastStat, h5Usage, h5Reset, w1Usage, w1Reset, m1Usage, m1Reset, hasSubscription});
        }
    " --json --timeout 15000 2>/dev/null)
    
    # 用 jq 提取 result 字段
    DATA=$(echo "$EVAL_RESPONSE" | jq -r '.result' 2>/dev/null || echo "")
    
    if [ -z "$DATA" ]; then
        output_report "" "" "" "" "" "" "" "" "" "" "" "数据提取失败"
        return 1
    fi
    
    # 检查是否有订阅信息
    HAS_SUB=$(echo "$DATA" | jq -r '.hasSubscription' 2>/dev/null || echo "false")
    if [ "$HAS_SUB" != "true" ]; then
        output_report "" "" "" "" "" "" "" "" "" "" "" "未找到订阅信息（可能登录失败）"
        return 1
    fi
    
    # 用 jq 提取各个字段
    STATUS=$(echo "$DATA" | jq -r '.status')
    DAYS_LEFT=$(echo "$DATA" | jq -r '.daysLeft')
    EXPIRE_DATE=$(echo "$DATA" | jq -r '.expireDate')
    AUTO_RENEW=$(echo "$DATA" | jq -r '.autoRenew')
    LAST_STAT=$(echo "$DATA" | jq -r '.lastStat')
    H5_USAGE=$(echo "$DATA" | jq -r '.h5Usage')
    H5_RESET=$(echo "$DATA" | jq -r '.h5Reset')
    W1_USAGE=$(echo "$DATA" | jq -r '.w1Usage')
    W1_RESET=$(echo "$DATA" | jq -r '.w1Reset')
    M1_USAGE=$(echo "$DATA" | jq -r '.m1Usage')
    M1_RESET=$(echo "$DATA" | jq -r '.m1Reset')
    
    # 输出报告
    output_report "$STATUS" "$DAYS_LEFT" "$EXPIRE_DATE" "$AUTO_RENEW" "$LAST_STAT" \
                  "$H5_USAGE" "$H5_RESET" "$W1_USAGE" "$W1_RESET" "$M1_USAGE" "$M1_RESET" ""
    
    echo ""
    echo "✅ 查询完成"
}

main "$@"
