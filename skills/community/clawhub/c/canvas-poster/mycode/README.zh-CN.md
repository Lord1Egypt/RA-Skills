# canvas-poster

[English](./README.md)

声明式服务端海报/看板长图生成引擎，基于 [@napi-rs/canvas](https://github.com/nicknisi/napi-rs-canvas)。用简单的 JSON DSL 描述布局，直接输出 PNG —— 无需浏览器，无需 headless Chrome。

## 安装

```bash
npm install canvas-poster
```

## 快速开始

```js
const { buildPoster } = require('canvas-poster');

buildPoster({
  width: 800,
  header: { title: '📊 月度报告', subtitle: '2026年3月' },
  sections: [
    {
      type: 'kpi-cards',
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
        { name: '住宿费', value: 380700 },
        { name: '交通费', value: 290000 },
        { name: '餐饮费', value: 150000 },
      ],
    },
    {
      type: 'tips',
      title: '💡 管理建议',
      items: ['推行远程协作策略', '加强长期住宿管控'],
    },
  ],
  footer: '🦞 自动生成',
  output: './report.png',
});
```

## Section 类型

| 类型 | 说明 | 数据字段 |
|------|------|----------|
| `kpi-cards` | KPI 卡片组（2列网格） | `cards: [{label, value, color?, sub?}]` |
| `bar-chart` | 横向柱状图 | `bars: [{name, value, color?, pct?}]` |
| `pie-chart` | 饼图 + 图例 | `slices: [{name, value, pct?}]` |
| `line-chart` | 折线图（多线+图例） | `lines: [{name, data: number[], color?}]`, `xLabels?: string[]` |
| `area-chart` | 面积图 | `areas: [{name, data: number[], color?}]`, `xLabels?: string[]`, `opacity?: number` |
| `scatter-chart` | 散点图 | `points: [{x, y, color?}]`, `dotRadius?: number` |
| `table` | 数据表格 | `headers: string[], rows: string[][]` |
| `tips` | 建议/提示卡片 | `items: string[]` |
| `divider` | 分隔线 | 无需数据 |

所有 section 类型均支持 `title` 字段。

## API

### `buildPoster(config)`

返回 `{ canvas, width, height, buffer?, output? }`。

**Config 字段：**

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `width` | number | 800 | 画布宽度（像素） |
| `height` | number | 自动 | 画布高度（省略则自动计算） |
| `bg` | string | `'#0f172a'` | 背景色 |
| `header` | object | — | `{ title, subtitle?, bg?, bgEnd? }` |
| `sections` | array | `[]` | section 对象数组 |
| `footer` | string | — | 页脚文字 |
| `output` | string | — | 设置后自动写入 PNG 文件 |

### `buildDashboard(data, output)`

预置的数据看板模板（差旅/费用类）。详见 `templates/dashboard.js`。

## 作为 Claude Code Skill

本包同时可作为 [Claude Code](https://claude.ai/claude-code) Skill 使用。将其放在 `skills/canvas-poster` 目录下，当你要求 Claude「生成海报」「做看板」「生成长图」时会自动调用。

详见 [SKILL.md](./SKILL.md)。

## 字体支持

自动检测系统 CJK 字体：Windows（微软雅黑）、macOS（苹方）、Linux（文泉驿正黑）。也可将 `.ttc`/`.ttf` 字体文件放在 `lib/fonts/` 目录作为备选。

## 许可证

[MIT](./LICENSE)
