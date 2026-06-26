#!/bin/bash
# Auto-Claw 一键优化安装脚本
# ⚠️ 以下是需要人类授权的部分

set -e

echo "╔══════════════════════════════════════════════════════╗"
echo "║  Auto-Claw 优化安装 — 待授权项                   ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# 已完成 ✅
echo "✅ 已完成（自主执行）："
echo "   • Yoast SEO 27.2 — 激活"
echo "   • WP Super Cache 3.0.3 — 激活"
echo "   • Redis Server — 已安装+运行"
echo "   • Redis Object Cache 2.7.0 — 激活（文件fallback）"
echo "   • Permalink结构优化 — /index.php/ 已移除"
echo "   • 主页Meta Description — 已设置"
echo "   • Schema.org JSON-LD — 已注入"
echo "   • A/B测试退出弹窗 — 已部署"
echo "   • 竞品监控mu-plugin — 已部署"
echo ""

# 待完成 🔒
echo "🔒 待授权（需人类操作）："
echo ""
echo "1. 【图片】上传 og:image (1200x630px) 到 WordPress 媒体库"
echo "   → 影响: Twitter/OG分享显示默认图片"
echo ""
echo "2. 【性能】安装 php8.2-redis 或 php-redis (需要服务器root)"
echo "   → 当前: Redis使用文件fallback，性能提升有限"
echo "   → 命令: apt install php-redis 或从源码编译"
echo ""
echo "3. 【SEO】安装 \"Yoast SEO\" 内置的 XML Sitemap 功能"
echo "   → 当前: sitemap功能在 wpseo 设置中 disabled"
echo "   → 解决: wpseo -> Search Appearance -> 启用 sitemap"
echo ""
echo "4. 【ClawhHub】发布技能包"
echo "   → 需访问 https://clawhub.ai 获取 token"
echo ""
echo "5. 【OpenAI API Key】激活 AI 内容生成"
echo "   → 当前: AI功能使用 mock 模式"
echo ""

echo "💡 回复 'approve' 或 '继续' 开始下一步"
