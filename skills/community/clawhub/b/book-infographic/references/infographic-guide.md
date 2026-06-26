# 信息图编辑指南

## 目录
- [信息图结构说明](#信息图结构说明)
- [HTML 信息图编辑](#html-信息图编辑)
- [可视化库使用](#可视化库使用)
- [样式修改指南](#样式修改指南)
- [常见编辑场景](#常见编辑场景)

---

## 信息图结构说明

### 标准 HTML 信息图结构

```
infographic.html
├── <head>
│   ├── 元数据（标题、作者、描述）
│   ├── 样式表（<style> 或外部 CSS）
│   └── 可视化库（ECharts / D3.js / Chart.js）
├── <body>
│   ├── .header (书籍封面区)
│   ├── .overview (概览区)
│   ├── .concepts (核心概念区)
│   ├── .chapters (章节摘要区)
│   ├── .visualizations (数据可视化区)
│   └── .footer (页脚)
```

---

## HTML 信息图编辑

### 1. 修改标题和元数据

```html
<!-- 修改书籍信息 -->
<div class="header">
    <h1>《书名》</h1>
    <p class="meta">作者 | 出版年份 | 核心主题</p>
</div>
```

### 2. 修改内容文本

```html
<!-- 修改章节标题 -->
<h2 class="chapter-title">第1章 章节标题</h2>

<!-- 修改段落内容 -->
<p class="content">这里是新的内容文本...</p>
```

### 3. 修改颜色主题

```css
:root {
    --primary-color: #2196F3;    /* 主色调 */
    --secondary-color: #FFC107;  /* 辅助色 */
    --bg-color: #ffffff;         /* 背景色 */
    --text-color: #333333;       /* 文字色 */
}

/* 应用主题 */
body {
    background-color: var(--bg-color);
    color: var(--text-color);
}
```

---

## 可视化库使用

### ECharts（推荐）

ECharts 是百度开源的数据可视化库，支持丰富的图表类型。

#### 柱状图示例

```javascript
var chart = echarts.init(document.getElementById('chartContainer'));
var option = {
    title: { text: '章节字数统计' },
    tooltip: {},
    xAxis: {
        data: ['第1章', '第2章', '第3章', '第4章']
    },
    yAxis: {},
    series: [{
        name: '字数',
        type: 'bar',
        data: [3500, 4200, 2800, 5100],
        itemStyle: {
            color: '#2196F3'
        }
    }]
};
chart.setOption(option);
```

#### 饼图示例

```javascript
var option = {
    title: { text: '内容类型分布' },
    series: [{
        type: 'pie',
        radius: '50%',
        data: [
            { value: 40, name: '概念定义' },
            { value: 25, name: '案例分析' },
            { value: 20, name: '方法论' },
            { value: 15, name: '其他' }
        ]
    }]
};
```

#### 关系图示例

```javascript
var option = {
    title: { text: '知识图谱' },
    series: [{
        type: 'graph',
        layout: 'force',
        nodes: [
            { name: '核心概念A', x: 100, y: 100 },
            { name: '概念B', x: 200, y: 150 },
            { name: '概念C', x: 150, y: 200 }
        ],
        links: [
            { source: '核心概念A', target: '概念B' },
            { source: '核心概念A', target: '概念C' }
        ]
    }]
};
```

---

## 样式修改指南

### 全局样式调整

```css
/* 字体设置 */
body {
    font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
    font-size: 16px;
    line-height: 1.8;
}

/* 容器宽度 */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

/* 卡片样式 */
.card {
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    padding: 24px;
    margin-bottom: 20px;
}
```

### 响应式设计

```css
@media (max-width: 768px) {
    .container {
        padding: 12px;
    }
    
    .card {
        padding: 16px;
    }
    
    h1 { font-size: 24px; }
    h2 { font-size: 20px; }
}
```

### 动画效果

```css
.card {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 16px rgba(0,0,0,0.15);
}
```

---

## 常见编辑场景

### 场景 1：修改图表数据

1. 打开 HTML 文件找到对应的 `<script>` 标签
2. 找到 ECharts/Chart.js 的 `series.data` 部分
3. 修改数值数组

```javascript
// 修改前
data: [3500, 4200, 2800, 5100]

// 修改后
data: [4000, 3800, 3200, 4500]
```

### 场景 2：添加新图表

1. 在 HTML 中添加图表容器
```html
<div id="newChart" style="width: 100%; height: 400px;"></div>
```

2. 添加初始化代码
```javascript
var newChart = echarts.init(document.getElementById('newChart'));
newChart.setOption({
    // 图表配置
});
```

### 场景 3：调整布局

```css
/* 两列布局 */
.two-columns {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}

/* 三列布局 */
.three-columns {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
}
```

### 场景 4：更换配色方案

```css
/* 方案 A：科技蓝 */
:root {
    --primary: #1976D2;
    --secondary: #64B5F6;
    --accent: #FF5722;
}

/* 方案 B：自然绿 */
:root {
    --primary: #2E7D32;
    --secondary: #81C784;
    --accent: #FF8F00;
}

/* 方案 C：商务灰 */
:root {
    --primary: #455A64;
    --secondary: #90A4AE;
    --accent: #FF7043;
}
```

### 场景 5：导出为图片

使用 ECharts 的内置导出功能：

```javascript
// 获取图表实例
var chart = echarts.getInstanceByDom(document.getElementById('chart'));

// 导出为 PNG
var url = chart.getDataURL({
    pixelRatio: 2,
    backgroundColor: '#fff'
});

// 下载图片
var link = document.createElement('a');
link.download = 'infographic.png';
link.href = url;
link.click();
```

---

## 外部资源

- ECharts 官方文档：https://echarts.apache.org/zh/index.html
- Chart.js 官方文档：https://www.chartjs.org/docs/
- D3.js 官方文档：https://d3js.org/

---

## 编辑检查清单

- [ ] 所有文字内容已正确填写
- [ ] 图表数据准确无误
- [ ] 配色方案统一协调
- [ ] 布局在不同屏幕尺寸下正常显示
- [ ] 字体大小适中可读
- [ ] 导出的图片质量满足要求
