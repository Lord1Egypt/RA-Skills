---
name: echarts-master
description: ECharts 图表大师。根据用户数据和业务上下文，自动设计并生成专业的 ECharts 可视化图表。使用场景：(1) 用户提供表格/JSON/CSV 数据需要可视化，(2) 用户说"帮我做个图"、"画个图表"，(3) 需要将查询结果可视化展示。
---

# ECharts Master - 图表生成专家

专业的 ECharts 可视化图表生成技能。自动分析数据结构，选择最佳图表类型，生成可交互的 HTML 图表。

## 核心能力

- **智能图表选择** - 根据数据类型和业务场景自动推荐最佳图表
- **本地化渲染** - 解决 ECharts CDN 被墙问题，使用本地资源
- **HTTP 服务管理** - 自动启动 8082 端口服务预览图表
- **专业配色方案** - 内置多套配色模板，符合数据可视化最佳实践

## 工作流

### 1. 数据接收与分析

接收用户提供的数据（表格/JSON/CSV），分析：
- 数据维度（1 维/2 维/多维）
- 数据类型（数值/分类/时间序列）
- 数据量级（少量/中等/大量）
- 业务场景（对比/趋势/分布/关系）

### 2. 图表类型选择

根据数据分析结果选择图表类型：

| 场景 | 推荐图表 | 数据要求 |
|------|----------|----------|
| 趋势分析 | 折线图、面积图 | 时间序列数据 |
| 对比分析 | 柱状图、条形图 | 分类数据 + 数值 |
| 占比分析 | 饼图、环形图、漏斗图 | 分类数据 + 百分比 |
| 分布分析 | 直方图、箱线图、散点图 | 连续数值数据 |
| 关系分析 | 散点图、气泡图、关系图 | 多维数据 |
| 地理数据 | 地图、热力地图 | 地理位置 + 数值 |
| 多维数据 | 雷达图、平行坐标 | 3+ 维度数据 |
| 仪表展示 | 仪表盘、 gauge 图 | 单值/多值指标 |

详细图表选择指南见 [references/chart-design.md](references/chart-design.md)

### 3. 生成 HTML 文件

使用模板生成完整的 HTML 文件：

```bash
# 读取模板
cp ~/.openclaw/skills/echarts-master/assets/echarts-base-template.html ./chart.html

# 或使用 Codex 直接生成完整 HTML
```

### 4. 启动 HTTP 服务预览

```bash
# 进入图表所在目录
cd /path/to/chart

# 启动 Python HTTP 服务（8082 端口）
python3 -m http.server 8082

# 或使用 node
npx http-server -p 8082
```

告知用户访问：`http://localhost:8082/chart.html`

## 输出格式规范

### HTML 文件结构

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>图表标题</title>
  <!-- 本地 ECharts -->
  <script src="./echarts.min.js"></script>
  <style>
    #main { width: 100%; height: 600px; }
  </style>
</head>
<body>
  <div id="main"></div>
  <script>
    var chart = echarts.init(document.getElementById('main'));
    var option = { /* 配置项 */ };
    chart.setOption(option);
  </script>
</body>
</html>
```

### 图表配置规范

- **标题**: 清晰描述图表内容
- **Tooltip**: 启用，显示详细数据
- **Legend**: 多系列时启用
- **Grid**: 合理边距，避免标签截断
- **X/Y 轴**: 明确标签、单位、刻度
- **颜色**: 使用配色模板，避免默认色

## 配色方案

使用 [references/chart-design.md](references/chart-design.md) 中的配色模板：

- **Default** - ECharts 默认配色（安全选择）
- **Professional** - 商务专业配色
- **Vibrant** - 鲜艳活泼配色
- **Monochrome** - 单色渐变配色
- **Colorblind-friendly** - 色盲友好配色

## 常见问题处理

### CDN 被墙问题

**不要使用** 在线 CDN 链接。必须：
1. 使用本地 `echarts.min.js` 文件
2. 或告知用户下载后本地打开

### 大数据量渲染

- 启用 `sampling: 'lttb'` 降采样
- 使用 `large: true` 优化模式
- 考虑分页或聚合展示

### 响应式适配

- 容器使用百分比宽度
- 监听 window.resize 事件
- 调用 `chart.resize()` 重绘

## 相关资源

- **配色模板**: [references/chart-design.md](references/chart-design.md)
- **HTML 模板**: [assets/echarts-base-template.html](assets/echarts-base-template.html)

## 使用示例

### 示例 1：销售趋势图

用户：`这是本月销售数据，帮我做个图`
```json
{"dates": ["1 日","5 日","10 日","15 日","20 日","25 日","30 日"], "sales": [12000, 15000, 18000, 22000, 19000, 25000, 28000]}
```

→ 生成折线图，展示趋势变化

### 示例 2：产品占比

用户：`画个饼图展示各产品占比`
```json
{"products": ["产品 A", "产品 B", "产品 C", "产品 D"], "values": [35, 25, 25, 15]}
```

→ 生成环形图，显示百分比

### 示例 3：多系列对比

用户：`对比三个部门的季度业绩`
```json
{"quarters": ["Q1", "Q2", "Q3", "Q4"], "dept1": [100, 120, 140, 160], "dept2": [80, 100, 110, 130], "dept3": [90, 110, 125, 145]}
```

→ 生成分组柱状图，多系列对比
