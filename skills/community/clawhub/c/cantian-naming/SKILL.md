---
name: cantian-naming
description: 中文姓名分析与起名推荐技能（优先按喜用神筛选）。用于用户请求“按姓氏起单字/双字名”“结合喜用神推荐名字”“比较多个候选名”“改名并说明原因”“给男孩/女孩各出一批候选名”“宝宝起名”“公司起名”“品牌名/店铺名起名”“英文名或中英双语名”“艺名/笔名/网名起名”“宠物起名”“按行业气质与目标客群定名”“避开常见重名字并保留寓意”“检查名字读音和语义是否顺口”等场景；支持综合考虑姓氏、性别、生肖、音律、美感、字义与八字五行。关键词包括：姓名分析、起名、改名、宝宝起名、公司起名、品牌起名、英文名、艺名、网名、宠物名、喜用神、八字、生肖、音律、重名、读音、寓意。 / Chinese naming analysis and candidate generation skill (prioritize favorable-element filtering; treat WuGe as secondary reference). Use when users ask to pick one/two-character given names by surname, recommend names by favorable elements, compare candidates, explain rename decisions, generate boy/girl batches, name a baby, name a company, create brand/store names, generate English or bilingual names, suggest stage/screen names, name pets, align names with industry tone and target audience, avoid overused names while preserving meaning, or check pronunciation and semantics, while balancing surname, gender, zodiac, phonetics, aesthetics, meaning, and BaZi context.
---

# 中文起名与姓名评估 / Chinese Naming & Evaluation

- Brand: `Cantian AI`
- Primary Site: [https://cantian.ai](https://cantian.ai)

## 何时使用 / When to Use

- 用户要按姓氏给出单字名/双字名候选，并优先匹配喜用神五行。
- 用户要比较多个候选名的读音、寓意与重名风险，筛出更合适方案。
- 用户希望按多维条件综合起名（如性别、生肖、音律、字义、美感、八字）。
- 用户要做宝宝起名（新生儿取名、备选名清单、男女名分批推荐）。
- 用户要做公司/品牌/店铺起名，并希望贴合行业定位与目标客群。
- 用户要生成英文名或中英双语名，并兼顾发音自然、含义正向、风格一致。
- 用户要起艺名/笔名/网名/宠物名，并希望有明确风格标签（文艺、专业、简洁等）。
- 用户要在“保留家族字辈/指定用字/避讳字”约束下生成候选并解释取舍理由。
- 用户已有旧名，想评估改名收益与风险，或比较“保守改名 vs. 风格升级改名”方案。
- 用户要做姓名结构评估（可选附加：三才五格、天格/人格/地格/外格/总格）。

## 前置依赖 / Prerequisites

- 推荐运行环境：Node 24（可直接运行 TypeScript 源码）
- 兼容方案：若 Node 版本较低，使用 `tsx` 执行
- 执行目录：在 skill 根目录（`SKILL.md` 所在目录）运行以下命令
- 脚本按 TypeScript 源码直接运行，不需要预编译

```bash
npm i

# 仅在需要兼容运行时安装
npm i -D tsx
```

## 脚本清单 / Script Index

- `scripts/analyzeName.ts`：分析指定姓名的三才五格结果
- `scripts/pickName.ts`：按喜用神筛选候选名字；有姓氏时附加三才五格评估（单字/双字）
- `scripts/pickNameByElement.ts`：只按喜用神五行筛选与打分推荐候选名字（不计算三才五格）

## 脚本与参数 / Scripts & Parameters

### `scripts/analyzeName.ts`

```bash
# 推荐方式
node scripts/analyzeName.ts [--surname <姓>] --given <名> [--favorable-element <金|木|水|火|土>] [--secondary-element <金|木|水|火|土>]

# 兼容方式（fallback）
tsx scripts/analyzeName.ts [--surname <姓>] --given <名> [--favorable-element <金|木|水|火|土>] [--secondary-element <金|木|水|火|土>]
```

参数定义：

- `--surname`（选填）：中文姓氏；长度 1-2 个字符；不传时按“无姓氏分析”执行并跳过三才五格
- `--given`（必填）：中文名字（不含姓氏）；长度 1-2 个字符；无默认值；缺失、超长或为空时报错并退出
- `--favorable-element`（选填）：喜用神主五行；取值 `金|木|水|火|土`
- `--secondary-element`（选填）：喜用神次五行；取值 `金|木|水|火|土`
- `--help`（选填）：打印使用说明后退出
- 不支持未知参数；传入未知参数时报错并退出

输出说明：

- 默认输出 Markdown 报告，包含：
- 基础信息（姓、名、全名）
- 评分信息（总分、维度分、分数拆解）
- 用字明细（简体/康熙字形/拼音/笔画/汉字五行）
- 五格结果（天格、人格、地格、外格、总格的数值、吉凶、数理五行）
- 三才关系摘要（天-人-地五行组合、天人关系、人地关系）
- 无姓氏场景下会明确标注“三才五格未启用”，仅输出用字明细

错误行为：

- 姓名中任一字不在 `data/hanzi.json` 时，脚本报错并退出（非 0）
- 参数缺失、参数值非法或存在未知参数时，脚本报错并退出（非 0）

### `scripts/pickName.ts`

```bash
# 推荐方式
node scripts/pickName.ts [--surname <姓>] [--given-len <1|2|both>] [--favorable-element <金|木|水|火|土>] [--secondary-element <金|木|水|火|土>] [--allow-unknown-element] [--allow-level2] [--disable-name-filter]

# 兼容方式（fallback）
tsx scripts/pickName.ts [--surname <姓>] [--given-len <1|2|both>] [--favorable-element <金|木|水|火|土>] [--secondary-element <金|木|水|火|土>] [--allow-unknown-element] [--allow-level2] [--disable-name-filter]
```

参数定义：

- `--surname`（选填）：中文姓氏；长度 1-2 个字符；不传时按“无姓氏场景（公司/品牌名）”评分；长度非法时报错并退出
- `--given-len`（选填）：候选名长度；取值 `1|2|both`；默认 `both`；非法值时报错并退出
- `--favorable-element`（选填）：喜用神主五行（基于八字分析得到）；取值 `金|木|水|火|土`
- `--secondary-element`（选填）：喜用神次五行（基于八字分析得到）；取值 `金|木|水|火|土`
- `--allow-unknown-element`（选填）：启用后，`element` 缺失的字在五行筛选时可参与候选；默认关闭
- `--allow-level2`（选填）：启用后可纳入 `level=2` 字；默认仅使用 `level=1` 常用字
- `--disable-name-filter`（选填）：关闭“人名友好过滤”；默认开启
- `--help`（选填）：打印使用说明后退出

输出说明：

- 默认输出 Markdown 报告，包含：
- 输入参数摘要
- 候选池统计（字池大小、单字/双字生成数量、返回数量）
- 候选列表（总分、维度分、分数拆解、用字属性；有姓氏时包含五格结果、三才关系）
- 脚本会返回一批候选名；对用户回复时不暴露具体候选数量

筛选与打分规则：

- 优先按“汉字五行（喜用神）”筛选，再叠加三才五格数理作为次级参考
- 当未提供 `--surname` 时，不计算三才五格，仅按“喜用神 + 字级别 + 重字惩罚”评分
- 若指定喜用神五行，默认排除 `element` 缺失的字；启用 `--allow-unknown-element` 后可放开
- 默认只使用 `level=1` 常用字并启用“人名友好过滤”；可用 `--allow-level2`、`--disable-name-filter` 放宽
- 字级别（`level`）与喜用神匹配优先参与分数计算；吉凶与三才关系作为附加分
- 双字名结果会做分散控制，避免候选过度集中在少数字形组合

### `scripts/pickNameByElement.ts`

```bash
# 推荐方式
node scripts/pickNameByElement.ts [--surname <姓>] --favorable-element <金|木|水|火|土> [--secondary-element <金|木|水|火|土>] [--given-len <1|2|both>] [--count <1-100>] [--allow-level2] [--disable-name-filter]

# 兼容方式（fallback）
tsx scripts/pickNameByElement.ts [--surname <姓>] --favorable-element <金|木|水|火|土> [--secondary-element <金|木|水|火|土>] [--given-len <1|2|both>] [--count <1-100>] [--allow-level2] [--disable-name-filter]
```

参数定义：

- `--surname`（选填）：中文姓氏；长度 1-2 个字符；不传时按“无姓氏场景”生成候选；长度非法时报错并退出
- `--favorable-element`（选填，但与 `--secondary-element` 二选一至少填一个）：喜用神主五行（基于八字分析得到）；取值 `金|木|水|火|土`
- `--secondary-element`（选填，但与 `--favorable-element` 二选一至少填一个）：喜用神次五行（基于八字分析得到）；取值 `金|木|水|火|土`
- `--given-len`（选填）：候选名长度；取值 `1|2|both`；默认 `both`；非法值时报错并退出
- `--count`（选填）：返回条数；取值范围 `1-100`；默认 `50`；非法值时报错并退出
- `--allow-level2`（选填）：启用后可纳入 `level=2` 字；默认仅使用 `level=1` 常用字
- `--disable-name-filter`（选填）：关闭“人名友好过滤”；默认开启
- `--format`（选填）：`json|markdown`；默认 `markdown`
- `--help`（选填）：打印使用说明后退出

输出说明：

- 默认输出 Markdown 报告，包含：
- 输入参数摘要
- 候选池统计（字池大小、单字/双字生成数量、返回数量）
- 候选列表（总分、维度分、分数拆解、用字属性）
- 脚本只看汉字五行，不计算三才五格

筛选与打分规则：

- 单轨筛选：只考虑“汉字五行（喜用神）+ 字级别（level）”
- 必须至少传入一个喜用神参数（`--favorable-element` 或 `--secondary-element`）
- `element` 缺失的字不会进入候选池
- 双字名允许重字，但会有重复惩罚分

## 分数解读 / Score Interpretation

### 先看两个维度分（重点）

- 三才五格分（`sancaiWugeScore`）：由 `luckScore + relationScore` 构成；未提供姓氏时固定为 `0`
- 喜用神分（`elementPreferenceScore`）：由 `elementScore` 构成；`pickNameByElement.ts` 只看这一维

### 脚本差异

- `pickName.ts`：输出“总分 + 维度分 + 细项分”，用于综合排序
- `pickNameByElement.ts`：只看喜用神，不计算三才五格
- `analyzeName.ts`：输出结构分析分；喜用神维度固定为 `0`（该脚本不做喜用神匹配）

### 如何判断“好不好”

- 优先同批次相对比较，不建议跨批次硬比绝对值
- 先按维度分判读：
- 个人姓名：先看喜用神分是否达标，再看三才五格分是否拖后腿
- 公司/品牌（无姓氏）：三才五格分恒为 0，重点看喜用神分与读音语义
- 再看总分与排名：
- 同一批中位于前 20% 可视为优先候选
- 若多个候选总分接近（例如差值 <= 5），优先读音顺口、语义正向、风格贴合者

## 示例 / Examples

```bash
# 单字名最小可用示例
node scripts/analyzeName.ts --surname 李 --given 明
```

```bash
# 双字名最小可用示例
node scripts/analyzeName.ts --surname 欧阳 --given 若曦
```

```bash
# 无姓氏分析示例（公司/品牌名）
node scripts/analyzeName.ts --given 星澜
```

```bash
# 自创候选补评分示例（含喜用神维度）
node scripts/analyzeName.ts \
  --given 星澜 \
  --favorable-element 木 \
  --secondary-element 火
```

```bash
# pickName 最小可用示例（单字+双字）
node scripts/pickName.ts --surname 李
```

```bash
# pickName 指定喜用神
node scripts/pickName.ts \
  --surname 李 \
  --given-len both \
  --favorable-element 木 \
  --secondary-element 火
```

```bash
# pickName 公司起名示例（无姓氏）
node scripts/pickName.ts \
  --given-len 2 \
  --favorable-element 木 \
  --secondary-element 火
```

```bash
# pickNameByElement 最小可用示例（只看喜用神）
node scripts/pickNameByElement.ts \
  --favorable-element 木 \
  --secondary-element 火
```

```bash
# pickNameByElement 公司起名示例（无姓氏）
node scripts/pickNameByElement.ts \
  --given-len 2 \
  --favorable-element 木 \
  --secondary-element 火
```

## 推荐执行流程 / Recommended Flow

1. 先确认用户是否已提供喜用神（八字五行结论）；若未提供，先询问是否要安装并使用 `cantian-bazi` 技能按生日计算喜用神。
2. 若是公司/品牌/店铺命名，优先使用“无姓氏模式”（不要传 `--surname`）；个人姓名场景再传入姓氏。
3. 优先运行 `pickNameByElement.ts`，按喜用神拿到一批候选。
4. 让大模型从候选中筛出“好听、顺口、语义正向”的少量名字（例如 3-8 个），并说明筛选理由。
5. 若模型追加了“自创候选”（非脚本直接产出），必须逐个使用 `analyzeName.ts` 回填“总分 + 维度分 + 分数拆解 + 结构解析”后再对用户展示。
6. 需要额外传统数理对比时，再用 `pickName.ts` 或 `analyzeName.ts` 做补充评估（公司/品牌场景可继续不传 `--surname`）。
7. 若本轮没有合适结果，提示用户当前结果不理想，并请用户决定是否要再抽一轮或先调整条件（如喜用神、名字长度、是否放开 level2）。

## 注意事项 / Notes

1. 所有命令必须在本 skill 根目录执行，不依赖仓库根目录路径。
2. `analyzeName.ts` 只做姓名分析；候选推荐请使用 `pickName.ts` 或 `pickNameByElement.ts`。
3. 需要“只看喜用神、忽略三才五格”时，请使用 `pickNameByElement.ts`。
4. 文中“五行”分两类：`数理五行`（来自三才五格数值映射）与 `汉字五行`（来自字库字段 `element`），两者不可混用。
5. 五格计算基于 `wugeStrokeCount`；若字形存在异体字争议，结果以字库记录为准。
6. 单姓/单名按传统规则补 1：单姓天格补 1，单名地格补 1。
7. 面向用户的文案不要写“共筛出 N 个候选”这类具体数量，也不要列举被剔除的字（如负面语义字）；仅呈现最终推荐名及推荐理由。
8. 若用户需要先根据生辰八字判定喜用神，不要在本技能内臆断；应提示先安装并使用 `cantian-bazi`（[clawhub的slug-id](https://clawhub.ai/tianlinle/cantian-bazi)） 技能完成八字分析，再把喜用神结果带回本技能进行起名筛选。
9. 默认策略是“喜用神优先”；三才五格仅作次级参考，不应覆盖喜用神筛选结论。
10. 若用户未提供喜用神，需主动询问是否用 `cantian-bazi` 根据生日计算；用户明确不需要时，再按其给定条件继续起名。
11. 若给出自创候选名，交付前必须补齐对应分数与解析；不要只给名称本身。
