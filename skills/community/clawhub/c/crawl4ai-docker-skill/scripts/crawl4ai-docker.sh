#!/bin/bash

# Crawl4AI Docker API 调用脚本
# 用于方便地调用 Docker 部署的 Crawl4AI 服务

CRAWL4AI_URL="http://localhost:11235"

# 函数：健康检查
health_check() {
    echo "🔍 检查 Crawl4AI 服务状态..."
    curl -s "$CRAWL4AI_URL/health" | jq .
}

# 函数：基础网页抓取
crawl_url() {
    local url="$1"
    local strategy="${2:-markdown}"
    
    echo "🌐 抓取网页: $url"
    curl -s -X POST "$CRAWL4AI_URL/crawl" \
        -H "Content-Type: application/json" \
        -d "{\
            \"urls\": [\"$url\"],\n            \"extraction_strategy\": \"$strategy\"\n        }" | jq .
}

# 函数：LLM 智能提取
crawl_with_llm() {
    local url="$1"
    local instruction="$2"
    local provider="${3:-openrouter/free}"
    local max_tokens="${4:-1000}"
    
    echo "🤖 LLM 智能提取: $url"
    echo "指令: $instruction"
    
    curl -s -X POST "$CRAWL4AI_URL/crawl" \
        -H "Content-Type: application/json" \
        -d "{\
            \"urls\": [\"$url\"],\n            \"extraction_strategy\": {\n                \"type\": \"llm\",\n                \"provider\": \"$provider\",\n                \"instruction\": \"$instruction\",\n                \"max_tokens\": $max_tokens\n            }\n        }" | jq .
}

# 函数：网页截图
screenshot() {
    local url="$1"
    
    echo "📸 生成网页截图: $url"
    curl -s -X POST "$CRAWL4AI_URL/screenshot" \
        -H "Content-Type: application/json" \
        -d "{\
            \"url\": \"$url\",\n            \"options\": {\n                \"full_page\": true,\n                \"quality\": 80\n            }\n        }" | jq .
}

# 函数：监控信息
monitor_health() {
    echo "📊 系统健康状态:"
    curl -s "$CRAWL4AI_URL/monitor/health" | jq .
}

monitor_browsers() {
    echo "🌐 浏览器池状态:"
    curl -s "$CRAWL4AI_URL/monitor/browsers" | jq .
}

# 主函数
main() {
    case "$1" in
        "health")
            health_check
            ;;
        "crawl")
            if [ -z "$2" ]; then
                echo "用法: $0 crawl <URL> [strategy]"
                echo "策略选项: markdown, llm"
                exit 1
            fi
            crawl_url "$2" "$3"
            ;;
        "llm")
            if [ -z "$2" ] || [ -z "$3" ]; then
                echo "用法: $0 llm <URL> <instruction> [provider] [max_tokens]"
                echo "示例: $0 llm https://example.com '总结主要内容' openrouter/free 1000"
                exit 1
            fi
            crawl_with_llm "$2" "$3" "$4" "$5"
            ;;
        "screenshot")
            if [ -z "$2" ]; then
                echo "用法: $0 screenshot <URL>"
                exit 1
            fi
            screenshot "$2"
            ;;
        "monitor")
            case "$2" in
                "health")
                    monitor_health
                    ;;
                "browsers")
                    monitor_browsers
                    ;;
                *)
                    monitor_health
                    echo ""
                    monitor_browsers
                    ;;
            esac
            ;;
        *)
            echo "Crawl4AI Docker API 调用脚本"
            echo ""
            echo "用法: $0 <command> [options]"
            echo ""
            echo "命令:"
            echo "  health                    - 服务健康检查"
            echo "  crawl <URL> [strategy]    - 基础网页抓取"
            echo "  llm <URL> <instruction>   - LLM 智能提取"
            echo "  screenshot <URL>          - 网页截图"
            echo "  monitor [health|browsers] - 监控信息"
            echo ""
            echo "示例:"
            echo "  $0 health"
            echo "  $0 crawl https://example.com"
            echo "  $0 llm https://example.com '总结主要内容'"
            echo "  $0 monitor"
            ;;
    esac
}

# 执行主函数
main "$@"