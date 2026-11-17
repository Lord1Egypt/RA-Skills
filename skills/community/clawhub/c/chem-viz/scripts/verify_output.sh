#!/usr/bin/env bash
# chem-viz Level 1 语法验证脚本
# 用法: bash verify_output.sh <生成的HTML文件>
# 检查: HTML结构完整性 / JavaScript括号平衡 / 测试API暴露 / 常见陷阱
set -u

FILE="${1:-}"
if [ -z "$FILE" ] || [ ! -f "$FILE" ]; then
  echo "❌ 用法: verify_output.sh <HTML文件>  （文件不存在: $FILE）"
  exit 1
fi

PASS=0; FAIL=0
check() { # $1=描述 $2=是否通过(0/1)
  if [ "$2" -eq 0 ]; then echo "  ✅ $1"; PASS=$((PASS+1)); else echo "  ❌ $1"; FAIL=$((FAIL+1)); fi
}

echo "── chem-viz Level 1 语法验证: $(basename "$FILE") ──"

# 1. HTML结构
grep -qi "<html" "$FILE";            check "包含<html>标签" $?
grep -qi "</html>" "$FILE";          check "包含</html>闭合标签" $?
grep -qi "<canvas\|<svg\|jxgbox\|JXG" "$FILE"; check "包含可视化载体(canvas/svg/JSXGraph)" $?

# 2. JavaScript括号平衡（粗检：{} 数量一致）
O=$(grep -o "{" "$FILE" | wc -l | tr -d ' ')
C=$(grep -o "}" "$FILE" | wc -l | tr -d ' ')
[ "$O" = "$C" ]; check "花括号平衡 (开$O = 闭$C)" $?

# 3. 测试API（chem-viz规范必须暴露）
grep -q "__CHEMVIZ_STATE" "$FILE";   check "暴露测试API __CHEMVIZ_STATE" $?

# 4. 常见陷阱
if grep -q "cdn.3dmol.org\|importmap" "$FILE"; then
  grep -q "file://" "$FILE" && { :; }
  echo "  ⚠️  使用了3Dmol.org CDN或importmap——file://协议下可能CORS失败，建议改纯Canvas2D"
else
  echo "  ✅ 未使用高风险CDN（file://协议安全）"
fi

# 5. 中文界面
grep -q "探索\|拖\|点击\|演示" "$FILE"; check "包含中文交互提示" $?

echo "── 结果: 通过$PASS / 失败$FAIL ──"
[ "$FAIL" -eq 0 ] && echo "✅ Level 1 通过，可进入Level 2功能验证" && exit 0
echo "❌ Level 1 未通过，修复后重试"
exit 1
