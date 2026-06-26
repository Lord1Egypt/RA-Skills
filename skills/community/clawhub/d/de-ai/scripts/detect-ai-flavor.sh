#!/bin/bash
# 检测文本AI味
# 用法: bash detect-ai-flavor.sh "文本内容" 或 pipe

input="${1:-$(cat /dev/stdin)}"

echo "📊 AI味检测报告"
echo "================"

score=0

# 检测点1：套路开头
if echo "$input" | grep -qiE "在当今|随着[^。]*的发展|众所周知|不得不说"; then
  echo "⚠️  套路开头 (+20分) - 避免'在当今/随着/众所周知'"
  score=$((score+20))
fi

# 检测点2：长连接词
if echo "$input" | grep -qiE "此外|值得注意的是|综上所述|总而言之|毋庸置疑"; then
  echo "⚠️  长连接词 (+15分) - 直接说事，不用过渡"
  score=$((score+15))
fi

# 检测点3：过度礼貌
if echo "$input" | grep -qiE "如果您方便|诚挚地|竭诚为您|很高兴为您"; then
  echo "⚠️  过度礼貌 (+15分) - 像真人一样说话"
  score=$((score+15))
fi

# 检测点4：模板结尾
if echo "$input" | grep -qiE "希望以上|对您有所帮助|如有任何问题|请随时联系"; then
  echo "⚠️  模板结尾 (+20分) - 自然收尾就行"
  score=$((score+20))
fi

# 检测点5：书面词
if echo "$input" | grep -qiE "获取|进行|共计|鉴于|予以|事宜|该[^的]"; then
  echo "⚠️  书面词 (+15分) - 试试口语化"
  score=$((score+15))
fi

# 检测点6：完美过渡
if echo "$input" | grep -qiE "首先|其次|再次|最后|第一|第二|第三"; then
  echo "ℹ️  结构词 (+10分) - 偶尔用可以，别每段都这样"
  score=$((score+10))
fi

if [ $score -eq 0 ]; then
  echo "✅ 看起来比较自然，AI味不重"
else
  echo ""
  echo "总分: $score 分"
  if [ $score -ge 50 ]; then echo "🔴 AI味很重，建议大幅修改"; fi
  if [ $score -ge 20 ] && [ $score -lt 50 ]; then echo "🟡 有些AI味，局部调整即可"; fi
  if [ $score -lt 20 ]; then echo "🟢 基本OK，小修小补"; fi
fi
