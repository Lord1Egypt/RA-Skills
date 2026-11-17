# Omni Reader 语义层通道

> 几何层（`extract_style.py`）看的是「这一页长什么样」，语义层看的是「这一本刊由什么组成」。
> 两者不可互相替代：几何层认不出栏目边界，语义层丢掉全部图片。

## 一、为什么样例学习必须跑两遍

| | 几何层 `extract_style.py` | 语义层 Omni + `enrich_from_omni.py` |
|---|---|---|
| 输入样例 | 本地 PDF（PyMuPDF 直接读） | 同一个 PDF，走 Omni 解析 |
| 拿到 | 页边距、版心、网格、字族字号、色板、图片矩形与占比、物理页 vs 印刷页 offset | 目录/栏目树、单元边界、文章总分层级、题头日期+作者、重复出现的段落型条目、页眉/CTA 频次、术语与法规名录 |
| 拿不到 | 栏目与文章边界、谁是谁的章节 | 图片、装饰件、颜色、网格、印张几何 |
| 成本 | 0 | 按页计费（见 §四） |
| 结论 | **必须两者都有**，缺一边就补到合成版 `stylespec.json` 上 | |

图片归属永远以几何层的 `image_slots` 为准。富文本层即使保留了 `<table>`、列表、标题树，也不会保留任何图。

## 二、调用顺序（唯一正确写法）

```
1) parse(source=<样例绝对路径>, detail="text", result_delivery="artifact")
   - 本地文件传路径，不要 file://，不要 base64 注入
   - 大刊一定加 result_delivery="artifact"，否则结果内联截断
2) processing -> 存 operation_id -> get_parse_status(wait_ms=20000) 轮询到 completed
   - 丢了 operation_id 不要重新提交（重复计费），先查 Bridge 缓存
3) read_outline(result_id)        # 标题树；块钱不贵，建议跑
4) save_result(result_id)         # 落盘完整 Markdown -> 拿到 <OMNI_EXPORT>/result_xxx.md
5) enrich_from_omni.py --md <落盘md> --outline <outline.json> --geo <stylespec.json> --out <dir>
```

`parse` 是唯一首调；`read_outline` / `read_result` / `save_result` 都是续调用。
多个样例源可以并发 `parse`，但各自 operation 要分开保管。

## 三、能力档位与排错

服务端 `GET /api/omni-reader/capabilities/v2` 会给出本账号可用的 direct profile，实测存在两档：

| profile | detail | 额外能力 |
|---|---|---|
| `omni.direct_text_billing.v1` | `text` | 仅 Markdown（保标题/列表/表格） |
| `omni.direct_grounding_billing.v1` | `grounded`, `layout` | `omni.result_bundle.v1` + `omni.grounding.v1`，带 grounding/layout sidecar |

本机 Bridge（当时现值）实测**只被下发 text 档**，所以 `detail="layout"` 会返回：

```
DETAIL_CAPABILITIES_UNAVAILABLE  retryable=false  billed=false
```

处置：**不要重试**，也不要告诉用户「账号不支持」。这是「当前未给本账号下发该能力」，退回 text 档 + 几何层补偿；需要高保真档时由服务运营方开通。

其它常见错误见 `cue-omni-reader` 技能：
- `UNSUPPORTED_DETAIL` — 请求的 detail 不存在
- `BRIDGE_UPGRADE_REQUIRED` — 升到最新发布版再试一次
- `OMNI_NOT_ENTITLED` / 403 — 账户额度或授权问题

### 没有 Omni 怎么办（退路，不是失败）

`SKILL.md` 的 `+learn` 说「两个通道都必须跑」，指的是**有语义层时的质量基准**，
不是开工前置条件。但**「不是前置条件」≠「默认可选」**：遇到下表情况时，
**先按 [`cue-onboarding.md`](cue-onboarding.md) §二 给一次开通指引**（注册 → 取 `CUE_API_KEY` →
装 Bridge / 连 MCP，含新账号注册即送 500 积分、每日 +10 积分），用户不要或确实装不了，
再走退路。**不要卡在这里，也不要替用户去申请账号或代填 key**：

| 情况 | 现象 | 处置 |
|---|---|---|
| 未安装 / 未连接该 MCP | 工具根本不可见 | 走退路 |
| 未授权 | `OMNI_NOT_ENTITLED` / 403 | 走退路 |
| 额度不足 | 额度类错误 | 先问用户是否继续（按页计费）；不继续则走退路 |
| Bridge 版本过低 | `BRIDGE_UPGRADE_REQUIRED` | 提示用户升级；不升则走退路 |

**退路 = 几何层 + 人工补语义**：

1. `extract_style.py` 照常跑（本地、零成本）。几何层与图片槽位不受影响——
   **图片归属本来就只看几何层**。
2. 栏目树与单元边界从**样例的目录页**人工抄进 `stylespec.json` 的 `semantic` 段，
   至少补齐 `toc`（栏目 → 页 → 篇）与 `unit_metrics`。
3. 单元模板照 `assets/templates/unit-pattern.template.md` 手写 slot 结构，语料从样例正文摘 3 条。
4. 拿不到的是 `paragraph_units` 的切分正则（它靠语义层统计重复出现的段落型条目）——
   短条目型刊物会因此漏掉一整类内容。
   **交付时必须明说「本期语义层是人工补的」**，不要让用户以为跑的是完整通道。

## 四、成本

按处理单元（页）计费，金额只认服务端 `billing.credits_charged` 快照，**不要自行估算费率**。
实测基准：91 页双月刊，text 档 `credits_charged = 6.432`（≈0.0707/页）。

跑之前告诉用户预计费用；样本很大时先确认。同一份样例别重复提交——提交前先在 Bridge 缓存里找同名结果。

## 五、富文本层的三个坑（脚本已处理，改脚本前先读）

1. **标题层级不可信。** Omni 的 Markdown heading level 忽高忽低，正文里的二级栏目会被抬成一级。
   → 脚本改用**目录页（CONTENTS）作为权威锚点**：目录是本刊自我声明的结构，且每条带印刷页码。
   终止判据：目录里每个栏目编号只出现一次，正文各栏目页会重复这个编号，见到重复即停。
2. **散字：`spaced text`。** 加宽字距的标题会输出成「王 维 巍」。
   → `norm_space()` 只合并「汉字<空格>汉字」。汉字与数字之间的空格**必须保留**，否则目录条目「XXX 19」的页码会被吃掉。
3. **绝大多数可复用单元不在标题树里。** 法规动态、业绩快讯这类条目既无页码也无 markdown 标题，只是一段重复出现的段落。
   → `paragraph_units()` 按「相同 leading pattern + 相近篇幅 + 出现 ≥3 次」聚类，输出切分正则与字数分布。这是纯几何层永远发现不了的部分。

## 六、输出与置信度

```
semantic.json            # 完整语义层
unit-patterns.draft.md   # UnitPattern 草稿，直接拿去填规范值
stylespec.merged.json    # 几何层 + semantic 合成（给了 --geo 才有）
```

`section_tree.tree_confidence` 三档：

- `high` — 命中目录，栏目与单元边界可信
- `media` — 无目录、靠题头日期推断
- `low` — 既无目录也无日期，边界不可信，**必须人工划定**，不要拿去写稿

`header_metas[].authors_candidates` 由连写汉字串按 2/3 字切分得到，一律是候选，写稿前必须跟用户核对人名。

## 七、实测样本

`assets/examples/qiming-regional-sample/`（91 页双月刊）跑出的结果：

- 目录解析：4 个栏目 / 20 个条目，其中 9 条带印刷页码
- 目录内 6 篇深度观察文章：正文 2 854–6 848 字（中位 5 107）
- 段落型单元：日期导语式 34 条（81–392 字，中位 268）；地区前缀式 6 条
- 页眉「区域观察」×82；CTA「阅读原文」×34；分所名录固定件 15 条
- `capability_notes`: 富文本层无图片（`has_images_in_text=false`）、内含 1 个 HTML 表格
