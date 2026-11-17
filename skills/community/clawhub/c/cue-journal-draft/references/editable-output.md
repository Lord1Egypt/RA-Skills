# 可编辑版本（docx / md）

> `build_draft.py` 出的 HTML/PDF 是**版面稿**，mm 级定位，给设计师与印刷看。
> `export_editable.py` 出的 Word / Markdown 是**文字稿**，给编辑改稿、给领导批注、
> 给 LLM 再加工。**同一份 `content.json` 是唯一事实来源**，两个版本只是它的两种投影。

## 1. 为什么必须要两份

| | `draft.html` / `draft.pdf` | `draft.docx` | `draft.md` |
|---|---|---|---|
| 看什么 | 版面：每块在第几毫米、什么颜色多大字 | 文字：能不能改、要不要删 | 结构：diff、团队协作、喂给模型 |
| 给谁 | 设计师 / 印刷 / 报批的终稿 | 编辑改稿、领导批注、外部撰稿人 | 你自己（版本对比、让 LLM 润色单篇） |
| 定位 | **绝对定位**（mm） | **流式**（来自 StyleSpec 的页边距=版心网格） | 无 |
| 能否改 | 改它就是改代码 | 直接改，再回填 | 改完手写回 json |
| 每页 section | — | 每页一个 Word 分节，页边距=该页所用网格；A / B 两套网格自动切换 | — |
| 缺点 | 编辑不会改 | **不是版面**：Word 里的断页不等于成品页码 | 丢失全部版式 |

一句话给 user：**Word 版是用来改文字的，不是用来看版面的**。
若你企图让 docx 保持 mm 定位，Word 会把它变成一堆互相打架的文本框，
编辑一动就散——这是所有「让 Word 精准排版」尝试的结局。

## 2. 导出

```bash
python3 <skill>/scripts/export_editable.py \
    --spec stylespec.json --content content.json --out out/
# 只要 Markdown（零依赖）：  --only md
# 去掉 ‖标记‖ 段落：        --no-marks   （导出后就不可回填了）
# 去掉首页交付说明：        --no-intro
```

产物：`out/draft.docx` + `out/draft.md`。

docx 里做对了的几件事（都是从 StyleSpec 来的，没有硬编码）：

- **页面尺寸** = spec 的 canvas；**页边距** = 该页所用网格的 `left_mm / right_mm`，
  所以 Word 里每行字数和成品接近 —— 编辑写多写少能马上看出来。
- **每页一个分节**：A 网格页（窄）与 B 网格页（宽）各自一套页边距，互不干扰。
- **字族/字号/行距/主色**来自 spec（`families[0]` / `body_size_pt` / `leading` / `palette.roles`），
  并把同样的字族写进 `w:eastAsia`——只设 ascii/hAnsi 的话中文会掉回宋体。
- **页眉**放 `running_text`（该页有就放，封面/分隔页/编委会不放）。
- **图**：能找到文件就按版心宽插入；找不到就在原位留
  `[ 待图 ] <图说> ── 建议 172mm 宽 · ≥300dpi` 的占位，
  不吃掉隐含的「这里缺一张图」信息。
- **背景图不插**：整版底图放进 Word 只会变成一张碍事的浮动图片；改为留一行标记说明。

## 3. ‖标记‖：让 Word 稿还能机读

每一页开头有一行灰色小字：

```
‖页 06‖ 栏目 · 港澳地区法规动态 ‖{"i":5,"template":"unit_list","grid":"A","folio":"02","meta":{...}}‖
```

图位前面另有一行：

```
‖图位‖ {"kind":"figure","index":7,"src":"images/gen/fig_1.png"}
```

它们用样式 `JD mark`（7.5pt 灰）承载，`import_docx.py` 靠它认页认结构，
**编辑可以整段删掉**（删了文档仍可读，只是回填时少了一份 metadata，
此时一定带 `--base` 才能救回来）。

## 4. 回填

```bash
python3 <skill>/scripts/import_docx.py \
    --docx out/draft.docx --base content.json --out content.edited.json
python3 <skill>/scripts/build_draft.py --spec stylespec.json \
    --content content.edited.json --out out2/
```

脚本会打一份**改动清单**（哪个 fields / units[i] / blocks[i] 从什么改成了什么），
直接贴进 `review.md` 给裁判：Word 里到底改了哪些字，不用人工比对。

**能回**
- 全部文字：正文、标题、名录、目录、联系方式、图说、`folio` 页码、
  编辑新写的段落（按上下文落在所属栏目/文章里）、删掉的单元。
- 图位原路径：`src` 由 ‖图位‖ 标记携带。

**回不来，靠 `--base` 兜**
- 毫米定位（`x_mm` / `top_mm` / `folio_y_mm` 等）、背景图本体、
   Word 里替换上去的新图片、批注/修订/脚注。
- `--base` 缺失时脚本会**明写警告**，不说假话。

所以：**回填必须带 `--base`**。

### 4.1 空转测试：没改稿时，回填结果必须与原文**逐字节一致**

这是回填链路上最值钱的一条验收动作，成本一条命令：

```bash
python3 <skill>/scripts/import_docx.py --docx out/draft.docx \
    --base content.json --out /tmp/rt.json
# 改动清单应显示「与原始 content.json 一致（未发现文字改动）」
```

**没改过 docx 就不可能有人类改动**，所以输出必须与原稿完全相同。只要报出改动，
就是回填链在丢东西——而这类丢失**不会报错**，只会静静少内容。实测（2026-09-17）
一次空转暴露了 5 处：

| 症状 | 真因 |
|---|---|
| 73 处「改动」，真改动被埋掉 | 行内加粗在 Word 里是 **run 属性不是字符**，`walk_text` 不回写 `**…**`；`<br>` 变真换行 |
| 目录页码整列消失 | toc 项只导出 `page`，而 issue-22 用的是 `ref` **锚点**（页码由渲染器解析）→ 回填成 `page: ""` |
| `meta` 整块不见 | 回填只写 `issue` + `pages`，把顶层的 `meta.freshness_exceptions` / `issue_date` / `window_months` 全丢了 → **时效豁免清单静默清空** |
| 单元的可选字段报「新增：」「被删除」 | `_units` 被 pop 后再 `base_fields.get("_units")` 取，恒为空 → `clean_unit` 的 base 永远是 `{}`，所有「照抄 base」的分支**都是死代码** |
| 空图位报「图片读取失败」并指向 content.json 目录 | `os.path.join(base, "")` 返回 base **目录**本身，而目录 `exists()` 为真 → 拿目录当图片嵌入 |

现在：`walk_text` 重建 `**`（只认 run 级加粗，标题样式不算）、toc 项按形态判
`page`/`ref`、顶层键整体继承、`clean_unit` 以 base 的键存在性为准、
空图位走 `[ 待图 ]` 占位。**两个样本（20 页 / 73 单元 / 310 块 / 6 图 / 4 组目录，
以及 5 页双栏玩具稿）回填后都与原文逐字节相等。**

改动清单也做了归一化：`<br>` / `**` / 空白差异不再算改动（`equivalent()`），
只报真正改了字的地方；顺带把「写法不同、内容等价」的字段回抄原文（`restore_equivalent()`），
免得编辑没碰过的字段被悄悄换写法。

**已知限界**：编辑在 Word 里把某个原本有值的可选字段（unit 的 `cta` / `image` / `meta`）
**清空**，无法表达为「删除」，回填会从 `--base` 恢复。要删字段就删到 content.json 里。

## 5. 踩过的坑

| 现象 | 原因 | 处理 |
|---|---|---|
| docx 里中文是宋体 | `python-docx` 的 `font.name` 只写 ascii/hAnsi | 脚本额外把同一字族写进 `w:eastAsia` |
| 白底上看不见字 | 编委会栏目在原刊里压在深色底图上，字色是白 | Word 版把 `JD names` / `JD meta` 改成深色（Word 里没有那张底图） |
| 每个名字占一行，改起来很难受 | 名录原样是一名一份 `<span>` | 导出时把人名用 ` / ` 连成一段，回填按 ` / ` 切回数组 |
| 「[分隔页，无正文]」被当成正文回填了 | 导出时给编辑的占位说明混进了 `fields.label` | 回填时丢弃以 `[` 开头的说明行 |
| 页码/期号在两版不一致 | 忘记同步改动 | 改动清单会列出，交付前必看 |
| `--base` 与 docx 页数不等 | Word 里增删了整页 | 脚本会报页数差并标出找不到对照的页 |
| 摘要回填后变成 note 块、与 `fields.abstract` 重复 | 摘要与 note 块共用 `JD note-block` 样式 | 摘要改用独立样式 `JD abstract`（v0.9.2） |
| 图注在回填后不见 | 占位路把图注拼在 `[ 待图 ]` 那行里，不是独立 `JD caption` 段 | 两条路都写独立 `JD caption` 段（v0.9.2） |
| `--base` 传了目录，抛 `PermissionError` 堆栈 | 目录也 `exists()` 为真 | 现在直接报「要的是原始 content.json 文件，不是目录」（v0.9.2） |

## 6. 交付组合建议

| 场景 | 给什么 |
|---|---|
| 领导审 / 外部撰稿人改 | `draft.docx`（带 --no-intro，留 ‖页 NN‖ 便于回指版面） |
| 设计师排版 | `draft.pdf` + `draft.html`（+ 原图目录） |
| 归档 / 下一期基线 | `content.json` + `draft.md` |
| 只做内部 update note | `draft.md` |
