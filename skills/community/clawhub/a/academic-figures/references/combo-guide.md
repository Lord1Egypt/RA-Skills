# 多图型组合应用指南（Combo Guide）

> **何时读我**：多图型组合成一张 figure 或一篇论文全套图。
> **最短路径**：按场景抄组合配方。
> **回 INDEX**：SKILL.md「文件索引与 30 秒路由」。

> 期刊 Figure 1 = Panel A+B+C 的组织方法：何时用 `composite` 单命令拼版，
> 何时用 `--pipeline` 多文件批产，以及两者混用的工程细节。

## 一、三条路线怎么选

| 路线 | 适用 | 产物 |
|---|---|---|
| `composite`（单命令多面板） | 同页 A+B+C 面板，一张图统一导出 | 单个 PDF/PNG/TIFF |
| `--pipeline`（YAML/JSON 批产） | 每张图独立文件、独立格式/DPI，或需要 `.batch-report.json` 核对 | 多个独立文件+批产报告 |
| 混用 | pipeline 里某一 figure 的 type 写 `composite`，面板图进批产流 | 报告统一管理 |

判断口诀：**审稿人把 ABC 当一张图读 → composite；期刊要求分图上传 → pipeline。**

## 二、composite 拼版要点（面板级）

```json
{"layout": [2, 2],
 "panel_labels": true,
 "panels": [
   {"type": "bar",  "data": {...}, "title": "基线特征",   "pos": [0, 0]},
   {"type": "box",  "data": {...}, "title": "主要终点",   "pos": [0, 1]},
   {"type": "km",   "data": {...}, "title": "无进展生存", "pos": [1, 0], "span": [1, 2]}
 ]}
```

- `layout` [行, 列] 定网格；每面板 `pos` 定位（0 基）；
- `span: [跨行, 跨列]`（v4.3）拼大面板，占位重叠会被前置拦截（报错不出废图）；
- `panel_labels: true` 自动加粗 A/B/C 角标（v4.1，行序优先），传数组（如 `["I","II"]`）自定义；
- 面板类型可以是**除 composite/diagram/upset 外**的任意注册图型（自管图型内部自建坐标轴，不可作面板，v4.7 起前置拦截）；
- 每面板自带 title；全局标题用 CLI `--title`。

## 三、pipeline 批产要点（文件级）

```yaml
defaults: {theme: okabe-ito, dpi: 600, format: [tiff, pdf]}
figures:
  - {type: bar,        data: fig1a.json, out: fig1a}
  - {type: violin,     data: fig1b.json, out: fig1b}
  - {type: km,         data: fig2.json,  out: fig2, format: [pdf]}
```

- `defaults` 管全局风格（主题/DPI/格式），单图可覆盖；
- YAML 需 `pip install pyyaml`；不想装依赖就写等价 JSON；
- 结束后生成 `.batch-report.json`：逐图成功/失败/耗时，审稿返修时逐条核对。

## 四、组合图的一致性纪律（审稿人视角）

1. **主题统一**：多面板/多文件全部用同一个 `--theme`（或 pipeline defaults），禁止各面板各配色；
2. **尺寸统一**：投稿套 `--journal <名>` 锁定栏宽（如 nature 双栏 183mm），composite 天然同页同宽；pipeline 靠同一 journal 预设对齐；
3. **语义色跨图一致**：对照组永远同一色、处理组永远同一色（规则见 `color-guide.md` §五）；
4. **字号统一**：`--journal` 预设锁字号；自由尺寸用 `--font-size` 全局指定；
5. **面板内不可嵌套自管图型**（composite/diagram/upset）：需要四层结构时拆两张图。

## 五、典型组合配方

**临床 RCT 论文 Figure 1**（composite 单图）：
A 基线比较 bar + B 主要终点 box/violin + C 亚组 forest —— 三面板 `layout: [1, 3]`。

**组学论文 Figure 2**（composite 单图 + 独立 upset）：
A volcano 差异表达 + B cluster_heatmap 聚类热图拼 `layout: [1, 2]`；upset 多平台基因集交集（≥5 集合）**单独出图**（自管图型不进面板，见上「不可嵌套」），作为 Figure 2(b) 或用 `--pipeline` 与 composite 一起批产。

**系统综述 Figure 1**（独立图）：PRISMA 流程图单独出（数字自洽校验不过会拒绝出图），不与数据图拼版。

**多中心年度报告**（pipeline 批产）：各中心一张 km，`defaults` 锁主题与 600dpi，报告单核对 N 张产物。

投稿前一键体检：`--pub-ready` = 自动 `--verify`（像素级重叠检测）+ 色盲安全提醒 + 多格式导出。
