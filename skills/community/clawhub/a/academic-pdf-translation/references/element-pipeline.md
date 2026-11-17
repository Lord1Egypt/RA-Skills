# 元素管线与交付前核查

这份文档讲 `academic_pdf_translation/` 这个包：各模块负责什么、数据怎么流、
交付前核查怎么用。它和 [architecture.md](architecture.md) 的分工是：
那份讲整个 Skill 的作业契约与文件格式，这份讲元素级的处理与核查。

## 包结构

```
academic_pdf_translation/
├── contracts/    共享定义：枚举、坐标、字体解析、作业迁移
├── analysis/     从原文得出元素清单，并把译文单元绑到元素上
├── planning/     按质量档位给每个元素定渲染策略，并备好降级链
├── render/       各内容类型的渲染器、版面块、页面合成、计划桥接
├── verify/       对产出 PDF 的核查：定位、对账、挑页、返修
├── delivery/     把生成、核查、返修串成一条线，给出交付结论
└── qa/           QA 判据：区域几何、文本信号、排版度量
```

### contracts —— 共享定义

| 模块 | 负责 |
| --- | --- |
| `enums.py` | 质量档位、路线、23 种元素类型 |
| `models.py` | `SourceElement`、坐标运算（`normalize_bbox` 等） |
| `fonts.py` | 跨平台字体发现与 ReportLab 真实探测 |
| `migration.py` | 旧作业升级到当前 schema |

### analysis —— 原文里有什么

`source_elements.build_inventory` 从 `source_structure.json` 得出元素清单；
`detectors/` 按类型识别图、表、公式、脚注、图题、文字角色、页眉页脚。
`unit_binding.bind_units` 把译文单元绑到元素上，结果写进
`unit_bindings.json`——按译文定位元素时以这份绑定为准。

### planning —— 每个元素怎么画

`render_plan.build_render_plan(inventory, quality_mode, forced_strategies=)`
给每个元素定策略，并由 `fallback_policy.build_chain` 备好三级降级链：

1. 按正常策略生成；
2. 保留原始元素区域（`preserve-element-region`）；
3. 保留整张原文页（`preserve-full-source-page`）。

`forced_strategies` 供内部返修使用，只许沿降级链往下，往回调会被拒绝并进
`plan.problems`。

### render —— 画

各内容类型一个渲染器，共同的规矩：

- 公式不重新输入，原样搬区域；
- 表格在网格、行列、数字映射、合并单元格、表题表注、粗体语义全部确定时
  才结构化重建，否则保留原表区域加中文翻译键，不压成段落；
- 位图不放大，低分辨率图给出警告；
- 文字角色只来自元素清单，不按字号或行长猜测标题。

`plan_bridge.py` 把渲染计划里定到保留级的元素翻成生成器认识的复杂内容
条目，并按图像 xref 把图级图题挂到条目上，保证图题与图同页。

### verify —— 核对产出的 PDF

| 模块 | 回答的问题 |
| --- | --- |
| `candidate_mapping.py` | 每个源元素落在候选哪一页 |
| `structural_audit.py` | 元素齐不齐、顺序对不对、图题是否同页 |
| `visual_review.py` | 哪几页值得人细看，看什么 |
| `repair.py` | 哪些能安全自动修，哪些交给复审 |

定位判据按证明力排序：图像字节哈希（位图）、像素指纹（保留区域）、
文字探针（文字元素）、文字锚点（矢量图）。绘图对象数量只作下界参考。

返修最多一轮（`MAX_REPAIR_ROUNDS = 1`），允许的动作只有降级与重排
（`preserve-element-region`、`preserve-full-source-page`、
`keep-caption-with-target`、`recompose-reading-order`）；
`lower-threshold`、`widen-whitelist`、`skip-check`、`drop-element`、
`relax-qa`、`mark-complete` 一律拒绝——返修改产出，不改判据。

### delivery —— 一个结论

`first_delivery.run_first_delivery` 把生成、核查、一次返修、再核查串成一条
线，只给三种结论：

| 结论 | 含义 | 退出码 |
| --- | --- | ---: |
| `delivered` | 核查全过 | 0 |
| `handover` | 剩余问题交给按档位安排的复审 | 2 |
| `blocked` | 返修引入回退，或生成失败 | 1 |

`complete` / `passed` / `delivered` 都是根据核查结果计算的只读属性。

### qa —— 判据的词汇表

`geometry.py` 答"这块东西落在页面哪里、占多大"；`text_signals.py` 是占位
符、拉丁散文、汉字、原文页标的正则；`typography.py` 量字号、行距、留白、
行宽。它们只量不判，阈值由调用方按档位决定。

## 数据流

```
source.pdf
  └─ analysis            → source_elements.json + unit_bindings.json
       └─ planning       → render_plan.json（含降级链）
            └─ plan_bridge → 并进 complex_content（派生视图，写回磁盘）
                 └─ build_candidate.py → candidate.pdf
                      └─ verify        → 映射 / 对账 / 视觉检查
                           └─ repair   → 重算渲染计划 → 重建（最多一轮）
                                └─ 再核查 → delivered / handover / blocked
```

### 派生视图与迁移

`complex_content.json` 与 `figure_inventory.json` 从此是**自动派生视图**，
不再手写：

- 生成器每次构建都会把渲染计划并进复杂内容并写回磁盘，戳上
  `derived_from.render_plan_sha256`；哈希对不上就是旧视图，不作数。
- `build_render_plan.py` 每次都同步写回程序派生的 `figure_inventory.json`。
- 旧作业首次用新版本构建时自动升级，无需手动迁移；带手写载荷的旧作业
  仍按旧规矩逐项校验（`validate_job.py` 按有无派生戳区分）。
- 元素级对账以 `source_elements.json` + `render_plan.json` +
  候选映射派生的 `candidate-elements.json` 为准（`verify/render_contract.py`），
  复杂条目数量只剩视图一致性的辅助角色。

## 命令用法

```bash
python3 scripts/deliver_first_candidate.py <作业目录>
```

| 参数 | 作用 |
| --- | --- |
| `--delivery-dir` | 证据写到哪里，默认 `<作业目录>/delivery` |
| `--page-budget` | 最多渲染几页给人细看，默认 6 |
| `--no-repair` | 只核查，不执行返修 |
| `--json` | 只输出 JSON |

前置：作业需要先有元素清单与单元绑定。

```bash
python3 scripts/analyze_source_elements.py <作业目录>
python3 scripts/bind_translation_units.py <作业目录>
```
