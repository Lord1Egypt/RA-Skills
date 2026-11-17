# 范例：区域观察类双月刊（专业服务）

> **本目录已脱敏**：机构名、刊物名、自然人姓名、客户与项目名称、源文件名**全部替换为虚构合成实体**；
> 保留的是**实测的版式参数**（网格 / 字号 / 色板 / 坐标 / 字数分布）与抽取结构。
> 因此它演示的是**方法**，不是任何一家机构的真实刊物。
>
> 本目录是 `journal-draft` 的 **+learn 阶段示范输出**：一份样刊的 StyleSpec 与其背后的人工补全分析。
> 用它来校准「机器提取」与「人工提炼」的分工：`stylespec.{json,md}` 是脚本自动产出，下面两份是必须在脚本之上补的东西。

## 它是怎么跑出来的

两条通道都要跑，产出合并到同一份 `stylespec.json`：

```bash
# 1) 几何层（本地 PyMuPDF，零成本）：页 / 网格 / 字色 / 图片槽位
python ~/.workbuddy/skills/journal-draft/scripts/extract_style.py \
  "<你的样刊>.pdf" --out ./qiming-regional-sample
#   → stylespec.json + stylespec.md

# 2) 语义层（omni-reader MCP）：parse→save_result→read_outline 拿到富文本 Markdown
python ~/.workbuddy/skills/journal-draft/scripts/enrich_from_omni.py \
  --md "<OMNI_EXPORT>/result_xxx.md" --outline outline.json \
  --geo ./qiming-regional-sample/stylespec.json --out ./qiming-regional-sample
#   → semantic.json + unit-patterns.draft.md + stylespec.merged.json

# 3) 再由人/agent 在脚本之上补 ⇒ unit-patterns.md + 本文件的「版式地图」与「调性」
```

实测：91 页 text 档约 6.4 credits，产出约 163 KB Markdown / 55 个标题 / 4 栏目 20 目录条目。
（额度随官方调整，以实际账单为准；如需 `layout`/`grounded` 高保真档而当前档位未下发，
会返回 `DETAIL_CAPABILITIES_UNAVAILABLE`，这是**能力档位**问题、不可重试，退回 text 档即可，见 `references/omni-channel.md`。）

样例规格：A4 210×297mm，91 页，四类栏目，四个章节各有满版分隔页。

## 一、版式地图（脚本提错、必须人工纠正的部分）

脚本把 91 页聚成 19 个模板，噪声很大。**正确版式地图只有两种正文网格 + 六种<｜hy_place▁holder▁no▁813｜>页**，其余全是同一模板因末行长短被误拆：

| 模板 | 真实身份 | 版面网格 | 说明 |
|---|---|---|---|
| 封面 | 单页 | 满版底图 | 期号 + 年月 + 年份大字压图左下 |
| 引言页 | 单页 | 右栏 x243–521pt | 第三方评价引语，品牌色大字 |
| 编辑部页 | 单页 | 满版底图 + 右栏白字 | 名单 / 责编 / 邮箱 |
| 目录 | 2 页 | 左 90pt、页码右 492pt | CONTENTS + 编号 + 条目 + 页码右对齐 |
| **网格 A（栏目页）** | 法规动态 / 业绩 / 新闻 | **左 87–90pt → 右 498pt（版心 144mm）** | 顶部可有通栏 Banner |
| **网格 B（文章页）** | 深度文章正文 | **左 54pt → 右 541pt（版心 172mm）** | 顶部必有 175×78mm 主图 |
| 分隔页 | 每节 1 张 | 满版满出血图 | 四个栏目各一张 |
| 封底 | 1 页 | 满版图 + 分栏联系块 | 各办公室电话/传真/邮箱 |

关键收获：**同一本刊物里存在两套版心**。 scripts 不会告诉你「A 用于栏目、B 用于文章」，这个 mapping 只能由人判读，写进 StyleSpec 后机器才不会乱。

## 二、脚本读得准、可直接采信的部分

- 主色 `#A10F34`（占非黑文字约 7%）、正文黑 `#000000`、次级灰 `#7F7F7F`、深色块 `#3E3E3E`
- 字族只有三档：`PingFangSC-Regular` / `PingFangSC-Semibold` / `TrebuchetMS-Bold`（英文与数字）
- 字号序列：27 / 21.5 / 18 / 15.5 / 14.1 / 12 / 10.4 / 9.9 / 9.5 / 7.5 pt；正文锁定 **10.4pt，行距 22–23.3pt（约 2.1–2.2 倍）**
- 通页固定件：页眉刊名（右对齐，9.9pt，主色）、logo 图（x10.8mm / y9.0mm，55.1×6.8mm）、页码（灰 10.4pt）
- 「阅读原文」CTA：`+learn` 自动识别为跨页高频短语（×30），逐条固定收尾

## 三、页数配比（+plan 阶段按此配平）

| 栏目 | 印刷页码 | 页数 | 占比 |
|---|---|---|---|
| 封面 / 引言 / 编辑部 / 目录 | 1–5（封面区） | 6 | 7% |
| 01 法规动态 | 2–18 | 17 | 19% |
| 02 深度文章（6 篇） | 19–62 | 44 | 50% |
| 03 业绩快讯（约 6 则） | 63–79 | 17 | 19% |
| 04 新闻（约 3 则） | 80–85 | 6 | 7% |

**深度文章吃掉一半篇幅**，这是专业服务类刊物的典型结构：观点内容是主菜，动态只是配菜。做新一期大纲时先用这个配比兜底。

## 四、这份样例教会 checklist 什么

1. 标题前那条红色竖线是**装饰件**（约 1.6×8.2mm），不是项目符号；在 `image_slots` 里应该标 `role=decoration`，别让 AI 学着在每行前画个点。
2. 每条动态都严格遵循「日期+发文主体 → 要点 → 影响评价 → CTA」四段式。正因为它是可枚举的槽位结构，新条目才能被批量生成；遇到没有固定节律的栏目，就必须放慢到人工撰写。
3. 免责声明不是通用件：只有涉及基金 / 证券 / 产品收益率的内容才带「重要提示：投资涉及风险…」。这类条件触发的固定件，要在 StyleSpec 里写成 `condition` 字段，而不是无脑全刊套用。
