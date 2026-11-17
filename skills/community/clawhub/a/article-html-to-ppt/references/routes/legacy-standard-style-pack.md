# Style-Pack Authoring Guide (Legacy Standard Workflow)

> 本文描述的是 Standard/工程路线的旧 style-pack 工作流，不是当前 V4 Template
> 模型主导组件编排。正式 Template 路线以
> [v4-template-route.md](v4-template-route.md) 为准：模型负责内容理解、页面设计和组件
> 组合，引擎负责模板证据、严格执行与门禁。这里的 style pack 仅用于兼容旧工程入口。

## 核心思路：设计感 = 可提取的 token

v4 引擎读一个 `styles/<pack>.json`（v3 style-contract v2.0 格式），其中：

- `colors` —— 主色/强调色/背景/表面/文字色/图表系列色
- `typography` —— 正文字体 / 编辑字体 / 字号体系 / 字重
- `grid`、`spacing`、`shape_tokens`、`card_tokens`、`table_tokens`、
  `chart_tokens`、`diagram_tokens`、`footer_tokens` …… —— 引擎自己的布局/组件 token

**用户的设计感**主要落在 `colors` + `typography`；**引擎的工程能力**落在其余 token。
提取器把前者从用户的 PPTX 里读出来，后者继承自内置包，保证可渲染、可 QA。

## 一键提取：从你的 PPTX 生成自己的 style pack

```bash
# 1. 从你自己的 deck（品牌模板 / 客户 deck / 过往优秀作品）提取
python3 scripts/template_from_pptx.py \
  --pptx my-brand-deck.pptx \
  --style-id my-brand \
  --display-name "My Brand" \
  --output styles/my-brand.json

# 2. 校验（对比度 / CJK 字体 / schema）
python3 -m engine style-validate --style styles/my-brand.json
# 期望 {"status": "pass", "findings": []}

# 3. 用它编译任意文档
python3 -m engine compile \
  --source doc:markdown:source.md \
  --style styles/my-brand.json \
  --output-dir out/
```

提取器会做：

- **配色**：统计所有 shape 的文字色 / 填充色 / 线条色 / 页面背景 → 映射到
  `primary / accent / background / surface_1 / surface_2 / text_primary /
  text_secondary / border / data_series`
- **字体**：统计所有文字 run 的字体 → `font_primary` / `font_editorial`，
  并自动附加 CJK 兜底字体（避免中文被操作系统随意替换）
- **继承**：grid / spacing / 组件 token 从基底包（默认 `consulting-light`）继承，
  保证引擎能确定性地布局

> 白色文字会被正确识别为"深色卡片上的反白"，不会误当成正文色。
> 提取器把来源 PPTX 记录在 `extensions.template_from_pptx` 里，pack 可审计。

## 手工微调（可选）

提取的配色/字体可能不完全等于你的意图，可以直接编辑生成的 `styles/<pack>.json`：

```jsonc
{
  "style_id": "my-brand",
  "display_name": "My Brand",
  "colors": {
    "primary": "#0A2233",        // 你的品牌主色
    "accent": "#2C4A6E",         // 强调色
    "background": "#FBFBF8",     // 页面背景
    "text_primary": "#2A2E35",
    "text_secondary": "#7C7669",
    "data_series": ["#0A2233", "#2C4A6E", "#4E7358", "#A66A2C"]
  },
  "typography": {
    "font_primary": ["Aptos", "PingFang SC", "Noto Sans CJK SC"],
    "font_editorial": ["Georgia", "PingFang SC"]
  }
}
```

改完再跑一次 `style-validate`，不通过就继续调（校验会明确报对比度/字体问题）。

## 在 SKILL 协议里的位置

编译命令已支持 `--style <任意路径>`（SKILL.md Step 4），所以提取出的 pack 直接可用，
无需改引擎。推荐工作流：

1. 用户给出自己的 PPTX / 说出品牌色 + 字体
2. Agent 运行 `template_from_pptx.py` 生成 pack（或直接让用户提供配色/字体手写 pack）
3. `style-validate` 通过后，用 `--style` 编译文档
4. 交付 deck，说明这是"长在用户模板里的"

## 后续（P10 已完成）

图表/图解的**配色、字体、风格**已并入 style pack——用户改一个 token，全 deck 图表同步换肤，依然不用写任何图表代码。

并且引擎现在可以**自动推断图表**（P10）：slide 有 ≥2 个 metric 块或数值表格时，引擎自动生成 chart 并渲染（comparison→combo、sequence→line、默认 column），模型/用户都不需要写 chart 结构。数据系列色取自 style pack 的 `data_series`，也就是用户模板的配色。

```bash
# 不需要写任何 chart 结构，引擎自动推断并渲染图表
python3 -m engine compile --source doc:markdown:source.md \
  --style styles/my-brand.json --output-dir out/
```
