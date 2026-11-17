# bii-blackrock-note

把 **BII 范式的个股研判简报**（A4 横向 · 封面 + 9 正册 + 12 增补册 · 左文字栏 + 右图表栏）
整体重定向为 **贝莱德智库（BlackRock Investment Institute）风格**，一条龙产出 `pptx + pdf + html`。

**内容零改动 · 只换视觉体系。** 七门体检中的门 5 用「可见文本词元多重集比对」把这条从口号变成判据。

## 为什么不是「画得好看」而是「判据」

一次真实实跑暴露了三类必踩坑，本技能把它们固化成了规则：

1. **装饰件会撑爆版式** —— 源稿 22 页刚好卡在纸高 793.7px。
   `display:inline-block` 胶囊标签会因*行盒*机制单页 +7px；页脚改两行 +4.5px。
   → 规则：**装饰件必须零净增量**（`block + width:fit-content`；页脚编号绝对定位）。
2. **品牌化会牺牲系列可区分性** —— 7 槽分类色若强行并成品牌五色，箱线图 4 个系列肉眼难分。
   → 规则：品牌识别由「黑 + 黄 + 结构装饰」承担，分类色只需收敛压暗、保留独立色相。
3. **白名单会掩盖注入事故** —— 写死的白名单只会误报，不会报真错。
   → 规则：白名单从 DOM **反推**本次真正注入了什么。

## 安装

```bash
cp -r bii-blackrock-note ~/.workbuddy/skills/
```

## 用法

```bash
bash ~/.workbuddy/skills/bii-blackrock-note/scripts/pipeline.sh \
  <源 BII.html> <输出目录>
```

## 依赖

- `bii-equity-note`（产出源 HTML）
- `html-to-pdf-cdp`（CDP 出 PDF）
- poppler（`pdfinfo/pdftotext/pdftoppm`）
- python-pptx + Pillow

## 发布（维护者用）

本技能**不自带发布脚本**——维护者工具不属于分发载荷。用通用发布器：

```bash
export GITHUB_TOKEN=ghp_xxx
bash ~/.workbuddy/skills/skill-publish-clawhub-github/scripts/publish_skill.sh \
  --dir ~/.workbuddy/skills/bii-blackrock-note --slug bii-blackrock-note \
  --name "BII 简报 × 贝莱德智库风格（pptx+pdf+html 三格式）" \
  --version <新版本号> --gh-repo bii-blackrock-note --go
```

| 渠道 | 标识 |
|---|---|
| ClawHub | [`bii-blackrock-note`](https://clawhub.ai/yjkj999999/skills/bii-blackrock-note) |
| GitHub | [`yjkj999999/bii-blackrock-note`](https://github.com/yjkj999999/bii-blackrock-note) |

## 版本谱系

| 版本 | 说明 |
|---|---|
| **1.1.0** | 全要素研读贝莱德《2026Q4 全球投资展望》（21 页，MKTG0926-M-5961218-EXP0927）：实测色板扩 14 色（深黄 `#FEDC00`/浅紫 `#9E79D9`/桃橙阶/鲑鱼带 `#FFB5A1`/轴灰 `#808080` 等）、14 组 28 形态图表范式库、6 个 opt-in 品牌组件（估计区/状态徽章/观点量尺/2×2 象限/三栏映射/分位带）。零净增量与内容零改动纪律不变。研读全文：`docs/br2026q4_design_study.md` |
| **1.0.2** | 把维护者发布脚本移出技能目录。原因：分发载荷里的远端写操作工具会让每个安装者被 ClawHub 安全审计判为 `Review`，且本地副本领先于已发布版本时会把**旧修订**当新版发出去 |
| **1.0.1** | 首个公开发布版。**取代并退休 `brand-pdf-deck-replica`**：把后者的视觉体系与三格式交付管线并进 BII 内容引擎 |
| — | ~~`brand-pdf-deck-replica@1.0.1`~~ 已 hide 下架（`clawhub unhide` 可回滚）。其「外部品牌 PDF 复刻 + 图表数值反解」能力不属本技能职责范围 |

两份并存会造成技能路由歧义：同一个「做成贝莱德智库风格」的意图会命中两个互相覆盖的技能。故只保留本技能。

## 许可

MIT-0 · Copyright (c) 2026 王东杰 (Wang Dong Jie) · yjkj999999
