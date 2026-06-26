#!/bin/bash
# 自动客服应答虾 - 服务管理脚本
# 依赖：Python 3.8+, flask, transformers

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
SERVER_PID_FILE="/tmp/auto-customer-service.pid"
SERVER_LOG_FILE="/tmp/auto-customer-service.log"
SERVER_PORT="${CHATBOT_PORT:-5000}"

start() {
    if [ -f "$SERVER_PID_FILE" ] && kill -0 "$(cat "$SERVER_PID_FILE")" 2>/dev/null; then
        echo "客服机器人服务已在运行 (PID: $(cat "$SERVER_PID_FILE"))"
        return 0
    fi
    
    echo "启动客服机器人服务..."
    python3 -c "
import sys
sys.path.insert(0, '$SKILL_DIR')
from flask import Flask, request, jsonify
import json, os

app = Flask(__name__)

# 加载知识库
def load_faq():
    faq_path = os.path.join('$SKILL_DIR', 'references', 'faq-database.md')
    if os.path.exists(faq_path):
        with open(faq_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ''

faq_content = load_faq()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')
    # 简单关键词匹配（实际部署时替换为 NLP 模型）
    response = match_intent(message, faq_content)
    return jsonify({'reply': response, 'transfer_human': should_transfer(message)})

def match_intent(msg, faq):
    keywords = {
        '退货': '支持7天无理由退货，请在订单页面申请退货~',
        '库存': '请问您咨询的是哪个商品？可以发送商品名称，我帮您查询~',
        '发货': '付款后1-2个工作日内发货，请放心~',
        '密码': '忘记密码可在登录页点击「忘记密码」，通过手机号验证重置~',
        '发票': '可在订单详情页申请发票，3-5个工作日内开具~',
    }
    for kw, reply in keywords.items():
        if kw in msg:
            return reply
    return '您好，我是智能客服小虾！请问有什么可以帮助您的？如需人工服务请说「转人工」~'

def should_transfer(msg):
    transfer_keywords = ['人工', '转人工', '真人', '投诉', '骗人', '愤怒']
    return any(kw in msg for kw in transfer_keywords)

app.run(host='0.0.0.0', port=$SERVER_PORT)
" >> "$SERVER_LOG_FILE" 2>&1 &
    
    echo $! > "$SERVER_PID_FILE"
    sleep 1
    
    if kill -0 "$(cat "$SERVER_PID_FILE")" 2>/dev/null; then
        echo "✅ 客服机器人服务已启动 (PID: $(cat "$SERVER_PID_FILE"), Port: $SERVER_PORT)"
        echo "   API 地址: http://localhost:$SERVER_PORT/chat"
    else
        echo "❌ 服务启动失败，请查看日志: $SERVER_LOG_FILE"
        return 1
    fi
}

stop() {
    if [ -f "$SERVER_PID_FILE" ]; then
        PID=$(cat "$SERVER_PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            kill "$PID"
            rm -f "$SERVER_PID_FILE"
            echo "✅ 客服机器人服务已停止"
        else
            echo "服务未在运行"
            rm -f "$SERVER_PID_FILE"
        fi
    else
        echo "服务未在运行"
    fi
}

reload() {
    echo "重新加载知识库..."
    if [ -f "$SERVER_PID_FILE" ] && kill -0 "$(cat "$SERVER_PID_FILE")" 2>/dev/null; then
        kill -HUP "$(cat "$SERVER_PID_FILE")"
        echo "✅ 知识库已重新加载"
    else
        echo "❌ 服务未在运行，请先启动服务"
    fi
}

test_chat() {
    local message="$1"
    if [ -z "$message" ]; then
        echo "用法: $0 test \"您的问题\""
        return 1
    fi
    
    echo "测试问题: $message"
    response=$(curl -s -X POST "http://localhost:$SERVER_PORT/chat" \
        -H "Content-Type: application/json" \
        -d "{\"message\": \"$message\"}")
    
    if [ $? -eq 0 ]; then
        echo "回复: $(echo "$response" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('reply',''))")"
        echo "转人工: $(echo "$response" | python3 -c "import sys,json; d=json.load(sys.stdin); print('是' if d.get('transfer_human') else '否')")"
    else
        echo "❌ 请求失败，请确认服务已启动"
    fi
}

status() {
    if [ -f "$SERVER_PID_FILE" ] && kill -0 "$(cat "$SERVER_PID_FILE")" 2>/dev/null; then
        echo "✅ 服务运行中 (PID: $(cat "$SERVER_PID_FILE"), Port: $SERVER_PORT)"
    else
        echo "❌ 服务未运行"
    fi
}

case "$1" in
    start)   start ;;
    stop)    stop ;;
    reload)  reload ;;
    test)    test_chat "$2" ;;
    status)  status ;;
    restart) stop; sleep 1; start ;;
    *)
        echo "用法: $0 {start|stop|restart|reload|test|status}"
        echo ""
        echo "命令说明:"
        echo "  start          启动客服机器人服务"
        echo "  stop           停止服务"
        echo "  restart        重启服务"
        echo "  reload         重新加载知识库（不重启服务）"
        echo "  test \"问题\"    测试问答效果"
        echo "  status         查看服务状态"
        exit 1
        ;;
esac
