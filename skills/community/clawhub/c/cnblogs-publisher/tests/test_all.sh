#!/bin/bash
# 测试所有功能

export CNBLOGS_BLOG_URL="https://rpc.cnblogs.com/metaweblog/sueyyyy"
export CNBLOGS_USERNAME="suyang320"
export CNBLOGS_TOKEN="03989364193E50C002FD667C5F016FC00423F010502BC4958DC3EA953527806A"

cd /Users/su/.openclaw/workspace/skills/cnblogs-publisher

echo "========================================"
echo "1. 获取博客信息"
echo "========================================"
python3 scripts/get_blog_info.py 2>&1 | head -15

echo ""
echo "========================================"
echo "2. 获取文章列表（最近3篇）"
echo "========================================"
python3 scripts/list_drafts.py 2>&1 | head -20

echo ""
echo "========================================"
echo "3. 获取单篇文章（ID: 19718794）"
echo "========================================"
python3 scripts/get_post.py 19718794 2>&1 | head -15

echo ""
echo "========================================"
echo "4. 更新草稿（ID: 19718794）"
echo "========================================"
python3 scripts/update_draft.py 19718794 test_article.md "OpenClaw,测试,更新" 2>&1

echo ""
echo "========================================"
echo "5. 再次获取文章（验证更新）"
echo "========================================"
python3 scripts/get_post.py 19718794 2>&1 | head -10

echo ""
echo "========================================"
echo "测试完成！"
echo "========================================"
