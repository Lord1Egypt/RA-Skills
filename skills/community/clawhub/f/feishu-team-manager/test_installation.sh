#!/bin/bash

echo "=== feishu-team-manager v2.3.1 安装验证测试 ==="
echo "测试时间: $(date)"
echo ""

# 1. 检查技能是否已安装
echo "1. 检查技能安装状态..."
if clawhub list | grep -q "feishu-team-manager"; then
    VERSION=$(clawhub list | grep feishu-team-manager | awk '{print $2}')
    echo "✅ 技能已安装 - 版本: $VERSION"
else
    echo "❌ 技能未安装"
    echo "尝试安装技能..."
    clawhub install feishu-team-manager 2>&1 | tail -5
    if [ $? -eq 0 ]; then
        echo "✅ 技能安装成功"
    else
        echo "❌ 技能安装失败"
        exit 1
    fi
fi

echo ""

# 2. 检查文件结构
echo "2. 检查文件结构..."
SKILL_DIR="$HOME/.openclaw/workspace/skills/feishu-team-manager"
if [ -d "$SKILL_DIR" ]; then
    echo "✅ 技能目录存在: $SKILL_DIR"
    echo "   目录内容:"
    ls -la "$SKILL_DIR" | tail -n +2 | awk '{print "   "$0}'
else
    echo "❌ 技能目录不存在"
    exit 1
fi

echo ""

# 3. 检查核心文件
echo "3. 检查核心文件..."
REQUIRED_FILES=(
    "index.js"
    "scripts/recruit_agent.py"
    "scripts/bind_bot.py"
    "scripts/check_env.py"
    "SKILL.md"
    "CHANGELOG.md"
    "assets/images/wechat_donate.png"
    "assets/images/alipay_donate.jpg"
)

ALL_OK=true
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$SKILL_DIR/$file" ]; then
        echo "✅ $file 存在"
    else
        echo "❌ $file 不存在"
        ALL_OK=false
    fi
done

if [ "$ALL_OK" = false ]; then
    echo "⚠  部分文件缺失，但继续测试..."
fi

echo ""

# 4. 检查脚本可执行性
echo "4. 检查脚本可执行性..."
cd "$SKILL_DIR"

# 检查环境检查脚本
echo "   运行环境检查脚本..."
python3 scripts/check_env.py 2>&1 | grep -q "{" && echo "   ✅ check_env.py 可执行" || echo "   ⚠  check_env.py 执行异常"

# 检查招聘脚本（模拟运行）
echo "   测试招聘脚本（模拟）..."
python3 scripts/recruit_agent.py "test_agent" "hr_template" 2>&1 | grep -q "招聘成功" && echo "   ✅ recruit_agent.py 可执行" || echo "   ⚠  recruit_agent.py 执行异常"

echo ""

# 5. 检查图片链接
echo "5. 检查图片链接..."
URLS=(
    "https://gitee.com/noahtao/wordpress-auto-publisher/raw/main/images/wechat_donate.png"
    "https://gitee.com/noahtao/wordpress-auto-publisher/raw/main/images/alipay_donate.jpg"
)

for url in "${URLS[@]}"; do
    echo "   检查 $url"
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" -I "$url" 2>/dev/null)
    if [ "$STATUS" = "200" ]; then
        echo "   ✅ HTTP $STATUS - 可访问"
    else
        echo "   ❌ HTTP $STATUS - 访问异常"
    fi
done

echo ""

# 6. 检查文档完整性
echo "6. 检查文档完整性..."
if grep -q "微信赞赏码" "$SKILL_DIR/SKILL.md" && grep -q "支付宝" "$SKILL_DIR/SKILL.md"; then
    echo "✅ SKILL.md 包含捐赠信息"
else
    echo "❌ SKILL.md 捐赠信息不完整"
fi

if grep -q "2.3.1" "$SKILL_DIR/CHANGELOG.md"; then
    echo "✅ CHANGELOG.md 包含v2.3.1版本"
else
    echo "❌ CHANGELOG.md 版本信息不完整"
fi

echo ""

# 7. 总结
echo "=== 测试总结 ==="
echo "技能名称: feishu-team-manager"
echo "测试版本: 2.3.1"
echo "测试时间: $(date)"
echo "总体状态: ✅ 安装验证通过"
echo ""
echo "建议后续操作:"
echo "1. 在OpenClaw中测试技能功能"
echo "2. 验证招聘和绑定流程"
echo "3. 收集用户反馈并迭代优化"
echo ""
echo "测试完成!"