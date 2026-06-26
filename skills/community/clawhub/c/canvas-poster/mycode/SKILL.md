---
name: canvas-poster
description: |
  服务端海报生成引擎。基于 @napi-rs/canvas，声明式生成数据看板、战报、对比图等长图海报。
  支持 KPI 卡片、柱状图、饼图、表格、建议卡片等 Section 类型。
  当用户提到"生成海报"、"做看板"、"长图"、"数据可视化图"、"生成图表"时使用。
  也供其他 Skill 作为依赖调用。
---

# canvas-poster

服务端长图海报生成引擎，基于 `@napi-rs/canvas`。

## 快速开始

```bash
cd skills/canvas-poster && npm install
node examples/demo.js /tmp/my-poster.png
```

## 核心用法：Section DSL

```js
const { buildPoster } = require('./lib/builder');

buildPoster({
  width: 800,
  header: {
    bg: '#1e40af',
    title: '📊 数据看板',
    subtitle: '2026年3月',
  },
  sections: [
    {
      type: 'kpi-cards',
      title: '📊 概览',
      cards: [
        { label: '总费用', value: '¥92.2万', color: 'red' },
        { label: '人数', value: '745人' },
        { label: '人均', value: '¥1,238' },
        { label: '达成率', value: '87.2%', color: 'green' },
      ],
    },
    {
      type: 'bar-chart',
      title: '💼 费用结构',
      bars: [
        { name: '住宿费', value: 380700, color: '#3b82f6' },
        { name: '交通费', value: 290000, color: '#22c55e' },
      ],
    },
    {
      type: 'pie-chart',
      title: '🗺️ 路线分布',
      slices: [
        { name: '北京→武汉', value: 180000 },
        { name: '北京→上海', value: 120000 },
      ],
    },
    {
      type: 'table',
      title: '⚠️ 异常分析',
      headers: ['部门', '异常金额', '占比'],
      rows: [
        ['AI应用中心', '¥64,121', '7.0%'],
      ],
    },
    {
      type: 'tips',
      title: '💡 管理建议',
      items: ['建议1', '建议2', '建议3'],
    },
  ],
  footer: '🦞 自动生成',
  output: '/tmp/poster.png',
});
```

## Section 类型

| 类型 | 说明 | 数据字段 |
|------|------|----------|
| `kpi-cards` | KPI 卡片组（2×N 网格） | `cards: [{label, value, color?, sub?}]` |
| `bar-chart` | 横向柱状图 | `bars: [{name, value, color?, pct?}]` |
| `pie-chart` | 饼图/环图 + 图例 | `slices: [{name, value, pct?}]`, `donut?: boolean\|number`, `center?: string` |
| `line-chart` | 折线图（多线+图例） | `lines: [{name, data: number[], color?}]`, `xLabels?: string[]`, `showDots?: boolean`, `showLegend?: boolean` |
| `area-chart` | 面积图 | `areas: [{name, data: number[], color?}]`, `xLabels?: string[]`, `opacity?: number`, `showDots?: boolean`, `showLegend?: boolean` |
| `scatter-chart` | 散点图 | `points: [{x, y, color?}]`, `dotRadius?: number` |
| `table` | 表格 | `headers: string[], rows: string[][]` |
| `tips` | 建议卡片（绿色框） | `items: string[]` |
| `divider` | 分隔线 | 无需数据 |

## 核心模块

- `lib/core.js` — 通用绘制工具（圆角矩形、饼图、柱状图、格式化）
- `lib/builder.js` — Section DSL → Canvas 构建器

## 发图到飞书

IM 图片上传有 ECONNRESET 问题，推荐方案：
1. 生成 PNG → 上传飞书云盘 → 开权限 → 发链接
2. 或嵌入飞书文档直接预览

```bash
node examples/demo.js /tmp/poster.png
```
