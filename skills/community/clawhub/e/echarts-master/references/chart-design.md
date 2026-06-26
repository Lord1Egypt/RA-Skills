# ECharts 图表设计指南

专业的图表设计参考，包含配色方案、字体配置、最佳实践。

---

## 目录

1. [配色方案](#配色方案)
2. [字体配置](#字体配置)
3. [图表类型详解](#图表类型详解)
4. [配置模板](#配置模板)
5. [最佳实践](#最佳实践)

---

## 配色方案

### 1. Default（ECharts 默认）

```javascript
const defaultColors = [
  '#5470c6', '#91cc75', '#fac858', '#ee6666', 
  '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc'
];
```

**适用场景**: 通用场景，安全选择

---

### 2. Professional（商务专业）

```javascript
const professionalColors = [
  '#2c3e50', '#3498db', '#1abc9c', '#e74c3c', 
  '#f39c12', '#9b59b6', '#16a085', '#c0392b', '#2980b9'
];
```

**适用场景**: 商务报告、正式演示、企业数据

---

### 3. Vibrant（鲜艳活泼）

```javascript
const vibrantColors = [
  '#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', 
  '#ffeaa7', '#dfe6e9', '#fd79a8', '#a29bfe', '#00b894'
];
```

**适用场景**: 互联网产品、年轻用户、创意展示

---

### 4. Monochrome（单色渐变）

```javascript
const monochromeColors = [
  '#08306b', '#08519c', '#2171b5', '#4292c6', 
  '#6baed6', '#9ecae1', '#c6dbef', '#deebf7', '#f7fbff'
];
```

**适用场景**: 单一数据系列、热力图、渐变效果

---

### 5. Colorblind-Friendly（色盲友好）

```javascript
const colorblindColors = [
  '#0173b2', '#de8f05', '#029e73', '#d55e00', 
  '#cc78bc', '#009e60', '#ba3ac5', '#fd3c06', '#8c8c8c'
];
```

**适用场景**: 公共报告、无障碍设计、国际化产品

---

### 6. Dark Theme（深色主题）

```javascript
const darkColors = [
  '#37a2da', '#32c5e9', '#67e0e3', '#9fe6b8', 
  '#ffdb5c', '#ff9f7f', '#fb7293', '#e7bcf3', '#8378ea'
];
```

**适用场景**: 深色模式、夜间展示、科技感界面

---

## 字体配置

### 中文字体栈

```javascript
const fontFamily = '-apple-system, "PingFang SC", "Microsoft YaHei", "Helvetica Neue", Arial, sans-serif';
```

### 字号规范

| 元素 | 字号 | 字重 |
|------|------|------|
| 主标题 | 18-22px | bold |
| 副标题 | 14-16px | normal |
| 轴标签 | 12-14px | normal |
| 图例 | 12-14px | normal |
| Tooltip | 12-14px | normal |

---

## 图表类型详解

### 折线图 (Line)

**适用**: 时间序列、趋势分析

```javascript
{
  xAxis: { type: 'category', data: dates },
  yAxis: { type: 'value' },
  series: [{
    type: 'line',
    data: values,
    smooth: true,        // 平滑曲线
    areaStyle: {},       // 填充区域（可选）
    lineStyle: { width: 3 }
  }]
}
```

---

### 柱状图 (Bar)

**适用**: 分类对比、排名展示

```javascript
{
  xAxis: { type: 'category', data: categories },
  yAxis: { type: 'value' },
  series: [{
    type: 'bar',
    data: values,
    barWidth: '60%',
    itemStyle: {
      borderRadius: [4, 4, 0, 0]
    }
  }]
}
```

---

### 饼图/环形图 (Pie)

**适用**: 占比分析、构成展示

```javascript
{
  series: [{
    type: 'pie',
    radius: ['40%', '70%'],  // 环形图
    // radius: '70%',         // 饼图
    data: pieData,
    label: {
      formatter: '{b}: {d}%'
    }
  }]
}
```

---

### 散点图 (Scatter)

**适用**: 关系分析、分布展示

```javascript
{
  xAxis: { type: 'value', name: 'X 轴' },
  yAxis: { type: 'value', name: 'Y 轴' },
  series: [{
    type: 'scatter',
    data: scatterData,
    symbolSize: 10
  }]
}
```

---

### 雷达图 (Radar)

**适用**: 多维对比、能力评估

```javascript
{
  radar: {
    indicator: radarIndicators,
    radius: '65%'
  },
  series: [{
    type: 'radar',
    data: radarData,
    areaStyle: {}
  }]
}
```

---

### 仪表盘 (Gauge)

**适用**: 指标展示、进度显示

```javascript
{
  series: [{
    type: 'gauge',
    progress: { show: true },
    detail: { valueAnimation: true },
    data: gaugeData
  }]
}
```

---

## 配置模板

### 基础配置模板

```javascript
const baseOption = {
  title: {
    text: '图表标题',
    left: 'center',
    textStyle: { fontSize: 18, fontWeight: 'bold' }
  },
  tooltip: {
    trigger: 'axis',
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    borderColor: '#ddd',
    borderWidth: 1,
    textStyle: { color: '#333' }
  },
  legend: {
    data: ['系列 1', '系列 2'],
    top: '10%',
    textStyle: { fontSize: 12 }
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    top: '20%',
    containLabel: true
  },
  color: ['#5470c6', '#91cc75', '#fac858', '#ee6666']
};
```

---

### 响应式配置

```javascript
const responsiveOption = {
  ...baseOption,
  responsive: true,
  media: [
    {
      query: { maxWidth: 768 },
      option: {
        title: { textStyle: { fontSize: 16 } },
        legend: { top: '8%' },
        grid: { top: '18%' }
      }
    }
  ]
};
```

---

## 最佳实践

### ✅ DO

1. **清晰的标题**: 标题应说明图表展示的核心信息
2. **合理的轴范围**: 避免数据压缩或过度留白
3. **一致的配色**: 同一报告中相同含义使用相同颜色
4. **必要的标签**: 轴标签、单位、图例缺一不可
5. **适当的留白**: grid 配置确保标签不被截断
6. **交互友好**: 启用 tooltip、legend 点击筛选

### ❌ DON'T

1. **避免 3D 效果**: 3D 图表难以准确读取数据
2. **避免过多颜色**: 单图表颜色不超过 8 种
3. **避免饼图切片过多**: 超过 7 项考虑其他图表
4. **避免双 Y 轴混淆**: 双 Y 轴需清晰标注
5. **避免默认配色滥用**: 根据场景选择配色方案
6. **避免信息过载**: 一个图表传达一个核心信息

---

### 数据可视化原则

1. **准确性优先**: 图表应准确反映数据，不误导
2. **简洁明了**: 去除不必要的装饰元素
3. **层次分明**: 重要信息突出，次要信息弱化
4. **一致性**: 同类图表保持相同风格
5. **可访问性**: 考虑色盲用户，提供文字说明

---

## 快速参考

### 图表选择决策树

```
数据类型？
├─ 时间序列 → 折线图/面积图
├─ 分类对比 → 柱状图/条形图
├─ 占比构成 → 饼图/环形图/堆叠图
├─ 分布情况 → 直方图/箱线图
├─ 关系分析 → 散点图/气泡图
├─ 地理数据 → 地图
├─ 多维数据 → 雷达图/平行坐标
└─ 单一指标 → 仪表盘/数字卡片
```

### 常用配置速查

| 配置项 | 常用值 | 说明 |
|--------|--------|------|
| smooth | true/false | 折线平滑 |
| stack | '总量' | 堆叠显示 |
| radius | '70%' / ['40%', '70%'] | 饼图半径 |
| barWidth | '60%' | 柱状图宽度 |
| symbolSize | 10 | 散点大小 |
