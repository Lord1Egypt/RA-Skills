#!/bin/bash
# ============================================
# CI/CD 通知脚本
# 支持：飞书、钉钉、Slack、企业微信
# ============================================

set -e

# 配置
WEBHOOK_TYPE="${WEBHOOK_TYPE:-feishu}"  # feishu, dingtalk, slack, wecom
WEBHOOK_URL="${WEBHOOK_URL:-}"
STATUS="${1:-success}"  # success, failure, unstable
PROJECT_NAME="${PROJECT_NAME:-Unknown}"
VERSION="${VERSION:-latest}"
BUILD_URL="${BUILD_URL:-}"
BUILD_USER="${BUILD_USER:-Jenkins}"

# 检查必要参数
if [ -z "$WEBHOOK_URL" ]; then
    echo "错误: WEBHOOK_URL 未设置"
    exit 1
fi

# 根据状态设置图标和颜色
case "$STATUS" in
    success)
        ICON="✅"
        COLOR="green"
        TITLE="部署成功"
        ;;
    failure)
        ICON="❌"
        COLOR="red"
        TITLE="部署失败"
        ;;
    unstable)
        ICON="⚠️"
        COLOR="yellow"
        TITLE="部署不稳定"
        ;;
    *)
        ICON="ℹ️"
        COLOR="blue"
        TITLE="部署通知"
        ;;
esac

# 构建消息内容
MESSAGE="${ICON} ${TITLE}
项目：${PROJECT_NAME}
版本：${VERSION}
构建人：${BUILD_USER}
链接：${BUILD_URL}"

# 发送飞书通知
send_feishu() {
    local payload
    payload=$(cat <<EOF
{
    "msg_type": "interactive",
    "card": {
        "header": {
            "title": {
                "tag": "plain_text",
                "content": "${TITLE}"
            },
            "template": "${COLOR}"
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "**项目：** ${PROJECT_NAME}\n**版本：** ${VERSION}\n**构建人：** ${BUILD_USER}\n**时间：** $(date '+%Y-%m-%d %H:%M:%S')"
                }
            },
            {
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {
                            "tag": "plain_text",
                            "content": "查看详情"
                        },
                        "url": "${BUILD_URL}",
                        "type": "primary"
                    }
                ]
            }
        ]
    }
}
EOF
)
    curl -s -X POST "$WEBHOOK_URL" \
        -H "Content-Type: application/json" \
        -d "$payload"
}

# 发送钉钉通知
send_dingtalk() {
    local payload
    payload=$(cat <<EOF
{
    "msgtype": "markdown",
    "markdown": {
        "title": "${TITLE}",
        "text": "### ${ICON} ${TITLE}\n\n**项目：** ${PROJECT_NAME}\n\n**版本：** ${VERSION}\n\n**构建人：** ${BUILD_USER}\n\n**时间：** $(date '+%Y-%m-%d %H:%M:%S')\n\n[查看详情](${BUILD_URL})"
    }
}
EOF
)
    curl -s -X POST "$WEBHOOK_URL" \
        -H "Content-Type: application/json" \
        -d "$payload"
}

# 发送 Slack 通知
send_slack() {
    local payload
    payload=$(cat <<EOF
{
    "attachments": [
        {
            "color": "${COLOR}",
            "title": "${TITLE}",
            "fields": [
                {"title": "项目", "value": "${PROJECT_NAME}", "short": true},
                {"title": "版本", "value": "${VERSION}", "short": true},
                {"title": "构建人", "value": "${BUILD_USER}", "short": true},
                {"title": "时间", "value": "$(date '+%Y-%m-%d %H:%M:%S')", "short": true}
            ],
            "actions": [
                {
                    "type": "button",
                    "text": "查看详情",
                    "url": "${BUILD_URL}"
                }
            ]
        }
    ]
}
EOF
)
    curl -s -X POST "$WEBHOOK_URL" \
        -H "Content-Type: application/json" \
        -d "$payload"
}

# 发送企业微信通知
send_wecom() {
    local payload
    payload=$(cat <<EOF
{
    "msgtype": "markdown",
    "markdown": {
        "content": "${ICON} **${TITLE}**\n\n>项目：${PROJECT_NAME}\n>版本：${VERSION}\n>构建人：${BUILD_USER}\n>时间：$(date '+%Y-%m-%d %H:%M:%S')\n>[查看详情](${BUILD_URL})"
    }
}
EOF
)
    curl -s -X POST "$WEBHOOK_URL" \
        -H "Content-Type: application/json" \
        -d "$payload"
}

# 主函数
main() {
    echo "发送 ${WEBHOOK_TYPE} 通知..."
    
    case "$WEBHOOK_TYPE" in
        feishu)
            send_feishu
            ;;
        dingtalk)
            send_dingtalk
            ;;
        slack)
            send_slack
            ;;
        wecom)
            send_wecom
            ;;
        *)
            echo "错误: 不支持的 WEBHOOK_TYPE: ${WEBHOOK_TYPE}"
            exit 1
            ;;
    esac
    
    echo "通知发送完成"
}

main "$@"
