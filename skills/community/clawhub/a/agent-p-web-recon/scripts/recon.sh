#!/bin/bash
# Web Recon 侦察脚本
# 用法：./recon.sh <target-url> [--passive|--active]

set -e

TARGET=$1
MODE=${2:---passive}

if [ -z "$TARGET" ]; then
    echo "用法：./recon.sh <target-url> [--passive|--active]"
    echo "  --passive  仅被动收集（安全）"
    echo "  --active   包含主动探测（需授权）"
    exit 1
fi

# 提取域名
DOMAIN=$(echo $TARGET | sed -E 's|https?://||' | cut -d'/' -f1)

echo "🔍 Web Recon - 目标：$TARGET"
echo "模式：$MODE"
echo "================================"

# 创建报告目录
REPORT_DIR="recon_report_$(date +%Y%m%d_%H%M%S)"
mkdir -p $REPORT_DIR

# ========== 被动收集（安全）==========
echo ""
echo "📡 阶段 1: 被动收集..."

# 1. 检查 Wayback Machine
echo "[*] 检查 Wayback Machine 快照..."
curl -s "http://web.archive.org/cdx/search/cdx?url=$TARGET&output=json" | head -20 > $REPORT_DIR/wayback_urls.txt
echo "  ✓ Wayback URLs: $REPORT_DIR/wayback_urls.txt"

# 2. 检查 Google Cache（需要手动访问）
echo "[*] Google Cache 链接:"
echo "  https://webcache.googleusercontent.com/search?q=cache:$TARGET"

# 3. 搜索引擎查询
echo "[*] 生成搜索引擎查询链接:"
echo "  site:$DOMAIN" > $REPORT_DIR/search_queries.txt
echo "  site:$DOMAIN inurl:admin" >> $REPORT_DIR/search_queries.txt
echo "  site:$DOMAIN filetype:pdf" >> $REPORT_DIR/search_queries.txt
echo "  site:$DOMAIN ext:json|xml|rss" >> $REPORT_DIR/search_queries.txt
echo "  ✓ 查询列表：$REPORT_DIR/search_queries.txt"

# 4. 检查 robots.txt
echo "[*] 检查 robots.txt..."
curl -s "$TARGET/robots.txt" > $REPORT_DIR/robots.txt 2>/dev/null || echo "  未找到 robots.txt"
if [ -s $REPORT_DIR/robots.txt ]; then
    echo "  ✓ robots.txt: $REPORT_DIR/robots.txt"
    # 提取禁止路径
    grep -E "^Disallow:" $REPORT_DIR/robots.txt | sed 's/Disallow: //' > $REPORT_DIR/disallowed_paths.txt
    echo "  ✓ 禁止路径：$REPORT_DIR/disallowed_paths.txt"
fi

# 5. 检查常见 RSS/Feed
echo "[*] 检查 RSS/Atom 订阅..."
for path in "/rss" "/rss.xml" "/feed" "/atom.xml" "/blog/rss"; do
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$TARGET$path")
    if [ "$STATUS" = "200" ]; then
        echo "  ✓ 发现 Feed: $path"
        curl -s "$TARGET$path" > "$REPORT_DIR/feed$(echo $path | tr '/' '_').xml"
    fi
done

# ========== 主动探测（需授权）==========
if [ "$MODE" = "--active" ]; then
    echo ""
    echo "⚠️  阶段 2: 主动探测（需授权）..."
    echo "确认你已获得书面授权？(y/n)"
    read -r CONFIRM
    if [ "$CONFIRM" != "y" ]; then
        echo "已取消主动探测"
        exit 0
    fi

    # 1. 探测常见 API 端点
    echo "[*] 探测 API 端点..."
    API_PATHS=("/api" "/api/v1" "/api/v2" "/graphql" "/api/posts" "/api/users" "/api/feed")
    for path in "${API_PATHS[@]}"; do
        STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$TARGET$path")
        if [ "$STATUS" = "200" ] || [ "$STATUS" = "401" ] || [ "$STATUS" = "403" ]; then
            echo "  [$STATUS] $path"
            echo "$path - $STATUS" >> $REPORT_DIR/api_endpoints.txt
        fi
    done

    # 2. 爬虫模拟测试
    echo "[*] 测试爬虫权限..."
    NORMAL_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$TARGET")
    BOT_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -A "Googlebot/2.1" "$TARGET")
    echo "  正常 User-Agent: $NORMAL_RESPONSE"
    echo "  Googlebot User-Agent: $BOT_RESPONSE"
    if [ "$NORMAL_RESPONSE" != "$BOT_RESPONSE" ]; then
        echo "  ⚠️  检测到不同响应 - 可能存在爬虫特殊权限"
    fi

    # 3. 目录扫描（如果安装了 dirsearch）
    if command -v dirsearch &> /dev/null; then
        echo "[*] 启动目录扫描..."
        dirsearch -u "$TARGET" -e php,html,js,json -o $REPORT_DIR/dirsearch.txt --quiet
        echo "  ✓ 扫描结果：$REPORT_DIR/dirsearch.txt"
    else
        echo "  ⚠️  dirsearch 未安装，跳过目录扫描"
        echo "  安装：pip install dirsearch"
    fi
fi

# ========== 生成报告 ==========
echo ""
echo "================================"
echo "📊 报告已生成：$REPORT_DIR/"
echo ""
echo "下一步:"
echo "1. 查看搜索引擎查询：cat $REPORT_DIR/search_queries.txt"
echo "2. 访问 Wayback Machine: https://web.archive.org/web/*/$TARGET"
echo "3. 检查发现的 Feed 文件"
echo ""
echo "⚠️  合规提醒：仅将结果用于合法用途"
