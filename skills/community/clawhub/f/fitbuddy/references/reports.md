# 图表与报告

## 图表生成

调用 `scripts/chart.py` 生成图表，保存到 `fitbuddy-data/charts/` 目录。

### 体重趋势图
```bash
python scripts/chart.py weight-trend --data-dir fitbuddy-data --output fitbuddy-data/charts/weight-trend.png --days 30
```
- 折线图：X轴日期，Y轴体重(kg)
- 水平虚线：目标体重
- 最近一天标注数值

### 热量收支图
```bash
python scripts/chart.py calorie-balance --data-dir fitbuddy-data --output fitbuddy-data/charts/calorie-balance.png --days 14
```
- 柱状图：每日摄入热量 vs 消耗热量
- 水平虚线：每日热量目标

### 营养素占比饼图
```bash
python scripts/chart.py macro-pie --data-dir fitbuddy-data --output fitbuddy-data/charts/macro-pie.png --date YYYY-MM-DD
```
- 饼图：蛋白质/碳水/脂肪的热量占比
- 同时标注克数

## 报告

### 周报
用户说"看看这周报告"/"周报"时生成：

```bash
python scripts/chart.py weekly-report --data-dir fitbuddy-data --output fitbuddy-data/charts/weekly-report.png
```

文字模板（AI 根据数据填充）：
```
📊 本周健身报告（MM/DD - MM/DD）
━━━━━━━━━━━━━━━━━━━━━━
📏 体重: XXkg → XXkg (↓/↑ X.Xkg)
🔥 平均每日摄入: XXXX kcal
⚡ 平均每日消耗: XXXX kcal
💧 平均每日饮水: XXXXml
🏋️ 训练 X 次，消耗共 XXXX kcal

🌟 本周亮点:
- [最大进步的动作/数据]

💡 下周建议:
- [基于数据的建议]
━━━━━━━━━━━━━━━━━━━━━━
```

### 月报
类似周报，覆盖 30 天范围，增加趋势总结。

## 图表中文显示

chart.py 会自动尝试以下中文字体（按优先级）：
1. Microsoft YaHei（微软雅黑）
2. SimHei（黑体）
3. WenQuanYi Micro Hei（Linux常见）
4. PingFang SC（macOS）
5. 无中文字体时使用英文标签
