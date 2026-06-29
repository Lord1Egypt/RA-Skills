# 可视化代码示例

本文件提供常见资讯图表的代码模板，可直接复用或微调后通过 `show_widget` 渲染。

## 1. 模型评测柱状图

适用于对比多个模型在同一基准上的得分。

```html
<canvas id="benchmarkChart" width="680" height="400"></canvas>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
new Chart(document.getElementById('benchmarkChart'), {
  type: 'bar',
  data: {
    labels: ['GPT-4o', 'Claude 3.5', 'Gemini 2.5', 'Llama 4', 'Qwen 3'],
    datasets: [
      {
        label: 'MMLU',
        data: [88.7, 88.3, 90.0, 85.5, 87.2],
        backgroundColor: 'rgba(54, 162, 235, 0.8)'
      },
      {
        label: 'HumanEval',
        data: [90.2, 92.0, 88.5, 82.3, 89.1],
        backgroundColor: 'rgba(255, 99, 132, 0.8)'
      }
    ]
  },
  options: {
    responsive: false,
    plugins: { title: { display: true, text: '主流大模型评测得分对比' } },
    scales: { y: { beginAtZero: false, min: 70, max: 100 } }
  }
});
</script>
```

## 2. 融资趋势折线图

适用于展示 AI 领域融资规模的时间变化。

```html
<canvas id="fundingChart" width="680" height="400"></canvas>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
new Chart(document.getElementById('fundingChart'), {
  type: 'line',
  data: {
    labels: ['2024 Q1', 'Q2', 'Q3', 'Q4', '2025 Q1', 'Q2', 'Q3', 'Q4', '2026 Q1', 'Q2'],
    datasets: [{
      label: '全球 AI 融资（亿美元）',
      data: [120, 150, 180, 210, 190, 220, 250, 280, 300, 320],
      borderColor: 'rgba(75, 192, 192, 1)',
      backgroundColor: 'rgba(75, 192, 192, 0.2)',
      fill: true,
      tension: 0.3
    }]
  },
  options: {
    responsive: false,
    plugins: { title: { display: true, text: '全球 AI 领域融资趋势' } }
  }
});
</script>
```

## 3. 事件时间线 SVG

适用于按时间排列重大 AI 事件。

```svg
<svg viewBox="0 0 680 300" xmlns="http://www.w3.org/2000/svg">
  <!-- 时间线主干 -->
  <line x1="60" y1="150" x2="620" y2="150" stroke="#4A90D9" stroke-width="3"/>

  <!-- 事件节点 -->
  <circle cx="120" cy="150" r="8" fill="#4A90D9"/>
  <text x="120" y="130" font-size="12" text-anchor="middle" fill="#333">GPT-4o 发布</text>
  <text x="120" y="175" font-size="10" text-anchor="middle" fill="#666">2024.5</text>

  <circle cx="240" cy="150" r="8" fill="#4A90D9"/>
  <text x="240" y="130" font-size="12" text-anchor="middle" fill="#333">Claude 3.5 Sonnet</text>
  <text x="240" y="175" font-size="10" text-anchor="middle" fill="#666">2024.6</text>

  <circle cx="380" cy="150" r="8" fill="#E74C3C"/>
  <text x="380" y="130" font-size="12" text-anchor="middle" fill="#333">Gemini 2.5 Pro</text>
  <text x="380" y="175" font-size="10" text-anchor="middle" fill="#666">2025.3</text>

  <circle cx="520" cy="150" r="8" fill="#E74C3C"/>
  <text x="520" y="130" font-size="12" text-anchor="middle" fill="#333">Llama 4 发布</text>
  <text x="520" y="175" font-size="10" text-anchor="middle" fill="#666">2025.6</text>

  <circle cx="580" cy="150" r="8" fill="#27AE60"/>
  <text x="580" y="130" font-size="12" text-anchor="middle" fill="#333">Qwen 3</text>
  <text x="580" y="175" font-size="10" text-anchor="middle" fill="#666">2026.1</text>
</svg>
```

## 4. 市场份额环形图

适用于展示各模型/平台的市场占比。

```html
<canvas id="marketChart" width="680" height="400"></canvas>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
new Chart(document.getElementById('marketChart'), {
  type: 'doughnut',
  data: {
    labels: ['OpenAI', 'Anthropic', 'Google', 'Meta', '其他'],
    datasets: [{
      data: [45, 18, 15, 10, 12],
      backgroundColor: [
        'rgba(54, 162, 235, 0.8)',
        'rgba(255, 206, 86, 0.8)',
        'rgba(75, 192, 192, 0.8)',
        'rgba(153, 102, 255, 0.8)',
        'rgba(201, 203, 207, 0.8)'
      ]
    }]
  },
  options: {
    responsive: false,
    plugins: {
      title: { display: true, text: 'AI 大模型 API 市场份额分布（2026）' }
    }
  }
});
</script>
```

## 使用要点

- 所有图表通过 `show_widget` 渲染，无需写入文件
- 调用 `show_widget` 前必须先调用 `read_me`（modules: "chart"）加载设计规范
- Chart.js HTML 片段不需要 `<html>/<head>/<body>` 标签
- SVG 使用 `viewBox="0 0 680 N"` 格式，适配内联渲染
- 图表标题、标签使用中文，与简报正文语言一致
- 数据来源必须标注在文字说明中，图表本身不宜放过多注释文字
