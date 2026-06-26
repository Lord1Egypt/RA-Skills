---
name: chart-generator
description: 数据可视化图表生成器（支持 7 种图表类型）
metadata: {"clawdbot":{"emoji":"📊"}}
---

# Chart Generator - 图表生成器

使用 Python matplotlib 生成数据可视化图表，支持 **7 种图表类型**：折线图、柱状图、饼图、散点图、面积图、多系列对比图。

## 📊 支持的图表类型

| 类型 | Type 参数 | 说明 | 适用场景 |
|------|----------|------|----------|
| 📈 折线图 | `line` | 显示数据趋势 | 时间序列、趋势分析 |
| 📊 柱状图 | `bar` | 比较不同类别 | 分类数据对比 |
| 🥧 饼图 | `pie` | 显示占比分布 | 百分比、份额分析 |
| 🔵 散点图 | `scatter` | 显示数据点分布 | 相关性分析、分布图 |
| 🎨 面积图 | `area` | 强调数量变化 | 累积趋势、量变分析 |
| 📉 多系列折线图 | `multi-line` | 多组数据对比 | 多指标趋势对比 |
| 📊 多系列柱状图 | `bar-compare` | 多组数据并排对比 | 多维度分类对比 |

## 🚀 使用方法

### 方式 1：直接调用脚本

```bash
# 折线图（默认）
/home/thor/bin/conda run -n base python /home/thor/.openclaw/workspace/skills/chart-generator/chart_gen.py \
  --data "[2,4,3,7,8,8]" \
  --title "数据趋势" \
  --output "/tmp/chart.png"

# 柱状图
/home/thor/bin/conda run -n base python /home/thor/.openclaw/workspace/skills/chart-generator/chart_gen.py \
  --type bar \
  --data "[23,45,56,78,32]" \
  --title "销售对比"

# 饼图
/home/thor/bin/conda run -n base python /home/thor/.openclaw/workspace/skills/chart-generator/chart_gen.py \
  --type pie \
  --data "[30,25,20,15,10]" \
  --labels "['产品 A','产品 B','产品 C','产品 D','其他']" \
  --title "市场份额"

# 散点图
/home/thor/bin/conda run -n base python /home/thor/.openclaw/workspace/skills/chart-generator/chart_gen.py \
  --type scatter \
  --data-x "[1,2,3,4,5,6,7,8]" \
  --data-y "[2,4,3,7,8,8,6,9]" \
  --title "数据分布"

# 面积图
/home/thor/bin/conda run -n base python /home/thor/.openclaw/workspace/skills/chart-generator/chart_gen.py \
  --type area \
  --data "[2,4,3,7,8,8]" \
  --title "累积趋势"

# 多系列折线图
/home/thor/bin/conda run -n base python /home/thor/.openclaw/workspace/skills/chart-generator/chart_gen.py \
  --type multi-line \
  --datasets '{"2024 年":[23,45,56,78,32],"2025 年":[34,56,67,89,43]}' \
  --labels "['Q1','Q2','Q3','Q4','Q5']" \
  --title "年度对比"

# 多系列柱状图
/home/thor/bin/conda run -n base python /home/thor/.openclaw/workspace/skills/chart-generator/chart_gen.py \
  --type bar-compare \
  --datasets '{"北京":[23,45,56],"上海":[34,56,67],"广州":[30,50,60]}' \
  --labels "['一月','二月','三月']" \
  --title "城市销售对比"
```

### 方式 2：使用包装命令

```bash
# 简单折线图
chart-gen --data="[2,4,3,7,8,8]" --title="销售数据"

# 柱状图
chart-gen -t bar --data="[23,45,56,78,32]" --title="月度销售"

# 饼图
chart-gen -t pie --data="[30,25,20,15,10]" --labels="['A','B','C','D','E']" --title="占比分析"

# 散点图
chart-gen -t scatter --data-x="[1,2,3,4,5]" --data-y="[2,4,6,8,10]" --title="相关性"

# 面积图
chart-gen -t area --data="[5,10,15,20,25]" --title="增长趋势"

# 多系列对比
chart-gen -t multi-line --datasets='{"产品 A":[10,20,30],"产品 B":[15,25,35]}' --title="产品对比"

# 发送到 Telegram（自动清理临时文件）
chart-gen-send -t bar --data="[23,45,56,78,32]" --title="销售报表"
```

### 方式 3：交给 AI 助手

直接描述需求即可：
- "帮我把数据 [2,4,3,7,8,8] 画成折线图"
- "生成一个饼图，数据是 [30,25,20,15,10]"
- "可视化这组数据：[10,20,15,25,30]，用柱状图"
- "对比 2024 和 2025 年的销售数据：2024 年 [23,45,56,78]，2025 年 [34,56,67,89]"

## 📋 参数说明

| 参数 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| `--data` | 单系列数据数组 | 单系列必填 | - |
| `--data-x` | 散点图 X 轴数据 | scatter 必填 | - |
| `--data-y` | 散点图 Y 轴数据 | scatter 必填 | - |
| `--datasets` | 多系列数据 JSON | 多系列必填 | - |
| `--labels` | X 轴标签 | 可选 | 自动生成 |
| `--type, -t` | 图表类型 | 可选 | line |
| `--title` | 图表标题 | 可选 | Data Chart |
| `--output` | 输出文件路径 | 可选 | /tmp/chart.png |
| `--width` | 图表宽度（英寸） | 可选 | 10 |
| `--height` | 图表高度（英寸） | 可选 | 6 |
| `--color` | 颜色（hex） | 可选 | #2196F3 |

## 🎨 图表类型详解

### 1️⃣ 折线图 (line)
```bash
chart-gen --data="[23,45,56,78,32,45,67]" --title="周销售趋势"
```
- 适合展示时间序列数据
- 自动填充渐变区域
- 标记数据点

### 2️⃣ 柱状图 (bar)
```bash
chart-gen -t bar --data="[23,45,56,78,32]" --labels="['周一','周二','周三','周四','周五']"
```
- 每个柱子上方显示数值
- 自动调整颜色
- 适合分类对比

### 3️⃣ 饼图 (pie)
```bash
chart-gen -t pie --data="[30,25,20,15,10]" --labels="['A','B','C','D','E']" --title="市场份额"
```
- 自动显示百分比
- 超过 10 项自动合并为"其他"
- 使用多彩配色方案

### 4️⃣ 散点图 (scatter)
```bash
chart-gen -t scatter --data-x="[1,2,3,4,5]" --data-y="[2,4,6,8,10]" --title="相关性分析"
```
- 显示数据点分布
- 自动标注点序号
- 适合相关性分析

### 5️⃣ 面积图 (area)
```bash
chart-gen -t area --data="[5,10,15,20,25]" --title="增长趋势"
```
- 强调数量变化的累积效果
- 半透明填充
- 适合展示总量变化

### 6️⃣ 多系列折线图 (multi-line)
```bash
chart-gen -t multi-line --datasets='{"2024 年":[23,45,56],"2025 年":[34,56,67]}' --title="年度对比"
```
- 自动分配不同颜色
- 显示图例
- 适合多指标趋势对比

### 7️⃣ 多系列柱状图 (bar-compare)
```bash
chart-gen -t bar-compare --datasets='{"北京":[23,45],"上海":[34,56]}' --labels="['Q1','Q2']"
```
- 并排显示多组数据
- 自动计算柱宽
- 适合多维度对比

## 🧹 自动清理

`chart-gen-send` 命令会在发送后自动删除临时文件，保持系统干净。

## 📦 依赖

- Python 3 (via conda)
- matplotlib
- pillow

## 💡 示例场景

```bash
# 销售周报
chart-gen-send --data="[230,450,560,780,320,450,670]" --title="周销售报表"

# 产品份额分析
chart-gen-send -t pie --data="[35,28,20,12,5]" --labels="['产品 A','产品 B','产品 C','产品 D','其他']" --title="产品份额"

# 季度对比
chart-gen-send -t multi-line --datasets='{"Q1":[100,120,150],"Q2":[130,140,160],"Q3":[150,170,190]}' --title="季度趋势"

# 城市销售对比
chart-gen-send -t bar-compare --datasets='{"北京":[230,340,450],"上海":[280,390,500],"广州":[200,300,400]}' --labels="['一月','二月','三月']" --title="城市对比"
```
