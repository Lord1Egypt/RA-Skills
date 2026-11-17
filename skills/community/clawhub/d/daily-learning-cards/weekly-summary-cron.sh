#!/bin/bash

# 一周学习汇总定时任务
# 时间：每周一 11:00
# 功能：生成上一周的完整学习汇总报告

TIMEOUT_DURATION=120

echo "$(date): 一周学习汇总任务启动"

# 获取上周的年份和周数（周一执行时生成上周一到上周日的数据）
YEAR=$(date -d "last week" +%Y)
WEEK=$(date -d "last week" +%V)

# 计算上周一到上周日的日期
START_DATE=$(date -d "last monday" +%Y-%m-%d)    # 上周一
END_DATE=$(date -d "last sunday" +%Y-%m-%d)      # 上周日

echo "处理日期范围: $START_DATE 到 $END_DATE"
echo "年份: $YEAR, 周数: $WEEK"

# 目录配置
SUMMARY_DIR="/home/admin/.openclaw/workspace/memory/learning-summaries"
CARDS_DIR="/home/admin/.openclaw/workspace/memory/learning-cards"
MEMORY_FEISHU="/home/admin/.openclaw/workspace/memory/feishu"
MEMORY_WEBUI="/home/admin/.openclaw/workspace/memory/webui"

# 生成汇总文件名（使用上周日的日期）
SUMMARY_FILE="$SUMMARY_DIR/${END_DATE}-elon-report.md"

# 初始化统计数据
TOTAL_DAYS=0
TOTAL_TOPICS=0
TOTAL_PITFALLS=0
TOTAL_CONCEPTS=0
TOTAL_QUOTES=0

# 收集上周的学习卡片
declare -a WEEK_CARDS
declare -a ALL_TOPICS
declare -a ALL_PITFALLS
declare -a ALL_CONCEPTS
declare -a ALL_QUOTES

# 扫描上周每一天
for i in {0..6}; do
    DAY_DATE=$(date -d "$START_DATE +${i}day" +%Y-%m-%d)
    
    # 检查学习卡片
    if [ -f "$CARDS_DIR/${DAY_DATE}.md" ]; then
        TOTAL_DAYS=$((TOTAL_DAYS + 1))
        WEEK_CARDS+=("$DAY_DATE")
        echo "找到学习卡片: $DAY_DATE"
        
        # 提取主题数
        topics=$(grep -c "^### [0-9]\\.\\|^## 📚 卡片" "$CARDS_DIR/${DAY_DATE}.md" 2>/dev/null || echo "0")
        TOTAL_TOPICS=$((TOTAL_TOPICS + ${topics:-0}))
        
        # 提取踩坑数（从表格中统计）
        pitfalls=$(grep -c "^| [0-9] |" "$CARDS_DIR/${DAY_DATE}.md" 2>/dev/null || echo "0")
        TOTAL_PITFALLS=$((TOTAL_PITFALLS + ${pitfalls:-0}))
        
        # 提取新概念数（从表格中统计）
        concepts=$(grep -c "^| .* | .* |" "$CARDS_DIR/${DAY_DATE}.md" 2>/dev/null | head -1 || echo "0")
        TOTAL_CONCEPTS=$((TOTAL_CONCEPTS + ${concepts:-0}))
        
        # 提取金句
        quotes=$(grep -E "^>.*" "$CARDS_DIR/${DAY_DATE}.md" 2>/dev/null | head -5)
        if [ -n "$quotes" ]; then
            ALL_QUOTES+=("$quotes")
        fi
    fi
done

echo "统计结果: $TOTAL_DAYS 天, $TOTAL_TOPICS 个主题, $TOTAL_PITFALLS 个踩坑, $TOTAL_CONCEPTS 个新概念"

# 生成汇总报告
timeout $TIMEOUT_DURATION bash -c "
cat > '$SUMMARY_FILE' << EOF
# ${YEAR}年第${WEEK}周学习汇总报告
生成日期：$(date +%Y-%m-%d)
数据周期：${START_DATE} 至 ${END_DATE}

## 【本周概览】
- 📅 学习天数：${TOTAL_DAYS} / 7 天
- 📚 主题数：${TOTAL_TOPICS} 个
- ⚠️ 踩坑数：${TOTAL_PITFALLS} 个
- 🧠 新概念：${TOTAL_CONCEPTS} 个

## 【学习卡片清单】
EOF

# 添加每日学习卡片链接
for day in \"${WEEK_CARDS[@]}\"; do
    echo \"- [${day}](memory/learning-cards/${day}.md)\" >> '$SUMMARY_FILE'
done

cat >> '$SUMMARY_FILE' << EOF

## 【核心主题汇总】
EOF

# 提取所有核心主题
for day in \"${WEEK_CARDS[@]}\"; do
    echo \"### ${day}\" >> '$SUMMARY_FILE'
    grep -E \"^## 📚 卡片 [0-9]+\" \"$CARDS_DIR/${day}.md\" 2>/dev/null | sed 's/## /- /' >> '$SUMMARY_FILE'
    echo \"\" >> '$SUMMARY_FILE'
done

cat >> '$SUMMARY_FILE' << EOF

## 【踩坑汇总】
EOF

# 提取所有踩坑记录
for day in \"${WEEK_CARDS[@]}\"; do
    if grep -q \"### .*踩坑\" \"$CARDS_DIR/${day}.md\" 2>/dev/null; then
        echo \"### ${day}\" >> '$SUMMARY_FILE'
        awk '/### .*踩坑/,/^### |^## /{if (!/^### .*踩坑/ && !/^### / && !/^## /) print}' \"$CARDS_DIR/${day}.md\" 2>/dev/null | head -20 >> '$SUMMARY_FILE'
        echo \"\" >> '$SUMMARY_FILE'
    fi
done

cat >> '$SUMMARY_FILE' << EOF

## 【新概念速查】
EOF

# 提取所有新概念
for day in \"${WEEK_CARDS[@]}\"; do
    if grep -q \"### .*新概念\" \"$CARDS_DIR/${day}.md\" 2>/dev/null; then
        echo \"### ${day}\" >> '$SUMMARY_FILE'
        awk '/### .*新概念/,/^### |^## /{if (!/^### .*新概念/ && !/^### / && !/^## /) print}' \"$CARDS_DIR/${day}.md\" 2>/dev/null | head -20 >> '$SUMMARY_FILE'
        echo \"\" >> '$SUMMARY_FILE'
    fi
done

cat >> '$SUMMARY_FILE' << EOF

## 【金句摘录】
EOF

# 添加金句
for quote in \"${ALL_QUOTES[@]}\"; do
    echo \"${quote}\" >> '$SUMMARY_FILE'
    echo \"\" >> '$SUMMARY_FILE'
done

cat >> '$SUMMARY_FILE' << EOF

## 【亮点】🌟
- 本周学习天数：${TOTAL_DAYS}/7
- 新增主题：${TOTAL_TOPICS} 个
- 新增概念：${TOTAL_CONCEPTS} 个

## 【问题】⚠️
- 缺失学习卡片天数：$((7 - TOTAL_DAYS)) 天

## 【下周学习建议】P0/P1/P2 优先级
- P0：保持每日学习卡片生成
- P1：回顾本周踩坑记录，避免重复犯错
- P2：深入学习新概念，形成知识体系

## 【经理寄语】Elon 的话
> \"本周学习数据已汇总，建议重点关注踩坑记录和新概念，形成可复用的知识资产。\"

---
Generated on $(date)
EOF
"

echo "汇总报告已生成: $SUMMARY_FILE"

# 发送概要到飞书
FEISHU_TARGET="oc_961ed2e84e1c196a9598dc6414d92ea6"
SUMMARY_MSG="📊 ${YEAR}年第${WEEK}周学习汇总报告

📅 学习天数：${TOTAL_DAYS}/7天
📚 主题数：${TOTAL_TOPICS}个
⚠️ 踩坑数：${TOTAL_PITFALLS}个
🧠 新概念：${TOTAL_CONCEPTS}个

数据周期：${START_DATE} 至 ${END_DATE}
完整报告：${SUMMARY_FILE}"

openclaw message send --channel=feishu --target="${FEISHU_TARGET}" --message="${SUMMARY_MSG}" 2>&1
echo "✅ 飞书消息已发送到 ${FEISHU_TARGET}"

echo "$(date): 一周学习汇总任务完成"
