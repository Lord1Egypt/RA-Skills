#!/bin/bash
#
# 🛡️ agent-defender 研发管理脚本
# =================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESEARCH_DAEMON="$SCRIPT_DIR/research_daemon.py"
SYNC_SCRIPT="$SCRIPT_DIR/sync_from_lingshun.py"
PID_FILE="$SCRIPT_DIR/.defender_research.pid"
STATE_FILE="$SCRIPT_DIR/.defender_research_state.json"
LOG_DIR="$SCRIPT_DIR/logs"
LOG_FILE="$LOG_DIR/defender_research.log"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印函数
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 检查是否运行
check_running() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            return 0  # 正在运行
        else
            rm -f "$PID_FILE"  # 清理旧 PID 文件
            return 1  # 未运行
        fi
    fi
    return 1  # 未运行
}

# 启动守护进程
start() {
    print_info "启动 agent-defender 研发守护进程..."
    
    if check_running; then
        print_warning "守护进程已在运行 (PID: $PID)"
        return 1
    fi
    
    # 创建日志目录
    mkdir -p "$LOG_DIR"
    
    # 启动后台进程
    nohup python3 "$RESEARCH_DAEMON" > "$LOG_FILE" 2>&1 &
    PID=$!
    
    # 保存 PID
    echo $PID > "$PID_FILE"
    
    sleep 2
    
    if ps -p $PID > /dev/null 2>&1; then
        print_success "守护进程已启动 (PID: $PID)"
        print_info "日志文件：$LOG_FILE"
        return 0
    else
        print_error "启动失败"
        rm -f "$PID_FILE"
        return 1
    fi
}

# 停止守护进程
stop() {
    print_info "停止守护进程..."
    
    if ! check_running; then
        print_warning "守护进程未运行"
        return 0
    fi
    
    PID=$(cat "$PID_FILE")
    
    # 发送 SIGTERM
    kill -TERM $PID 2>/dev/null
    
    # 等待进程退出
    for i in {1..10}; do
        if ! ps -p $PID > /dev/null 2>&1; then
            print_success "守护进程已停止"
            rm -f "$PID_FILE"
            return 0
        fi
        sleep 1
    done
    
    # 如果还没退出，强制停止
    print_warning "发送 SIGKILL..."
    kill -9 $PID 2>/dev/null
    rm -f "$PID_FILE"
    print_success "守护进程已强制停止"
    return 0
}

# 重启守护进程
restart() {
    stop
    sleep 2
    start
}

# 查看状态
status() {
    if check_running; then
        PID=$(cat "$PID_FILE")
        UPTIME=$(ps -p $PID -o etime= 2>/dev/null | tr -d ' ')
        
        echo -e "${GREEN}✅ agent-defender 研发系统正在运行${NC}"
        echo ""
        echo "  PID:     $PID"
        echo "  运行时长：$UPTIME"
        echo "  日志：   $LOG_FILE"
        
        # 显示状态
        if [ -f "$STATE_FILE" ]; then
            echo ""
            echo "📊 状态:"
            python3 -c "
import json
with open('$STATE_FILE', 'r') as f:
    state = json.load(f)
print(f\"  轮次：{state.get('round', 0)}\")
print(f\"  规则数：{state.get('total_rules', 0)}\")
print(f\"  测试数：{state.get('total_tests', 0)}\")
print(f\"  质量评分：{state.get('quality_score', 0)}/100\")
"
        fi
        
        return 0
    else
        echo -e "${YELLOW}⚠️  agent-defender 研发系统未运行${NC}"
        return 1
    fi
}

# 查看日志
logs() {
    LINES=${2:-50}
    
    if [ ! -f "$LOG_FILE" ]; then
        print_warning "日志文件不存在"
        return 1
    fi
    
    echo -e "${BLUE}📄 最近 $LINES 行日志:${NC}"
    echo ""
    tail -n $LINES "$LOG_FILE"
}

# 实时跟踪日志
follow() {
    if [ ! -f "$LOG_FILE" ]; then
        print_warning "日志文件不存在"
        return 1
    fi
    
    print_info "实时跟踪日志 (Ctrl+C 停止)..."
    echo ""
    tail -f "$LOG_FILE"
}

# 手动运行一轮
run_once() {
    print_info "手动运行一轮研发..."
    python3 "$RESEARCH_DAEMON" --run-once
}

# 同步灵顺 V5 规则
sync() {
    print_info "从灵顺 V5 同步规则..."
    python3 "$SYNC_SCRIPT"
}

# 清理
clean() {
    print_info "清理临时文件..."
    rm -f "$PID_FILE"
    rm -f "$STATE_FILE"
    print_success "清理完成"
}

# 帮助信息
help() {
    echo "🛡️  agent-defender 研发管理脚本"
    echo ""
    echo "用法：$0 <命令> [参数]"
    echo ""
    echo "命令:"
    echo "  start       启动守护进程"
    echo "  stop        停止守护进程"
    echo "  restart     重启守护进程"
    echo "  status      查看状态"
    echo "  logs [n]    查看日志 (默认 50 行)"
    echo "  follow      实时跟踪日志"
    echo "  run-once    手动运行一轮"
    echo "  sync        从灵顺 V5 同步规则"
    echo "  clean       清理临时文件"
    echo "  help        显示帮助"
    echo ""
    echo "示例:"
    echo "  $0 start          # 启动守护进程"
    echo "  $0 status         # 查看状态"
    echo "  $0 logs 100       # 查看最近 100 行日志"
    echo "  $0 follow         # 实时跟踪日志"
    echo "  $0 sync           # 同步灵顺 V5 规则"
}

# 主函数
case "${1:-help}" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    status)
        status
        ;;
    logs)
        logs "$@"
        ;;
    follow)
        follow
        ;;
    run-once)
        run_once
        ;;
    sync)
        sync
        ;;
    clean)
        clean
        ;;
    help|--help|-h)
        help
        ;;
    *)
        print_error "未知命令：$1"
        echo ""
        help
        exit 1
        ;;
esac
