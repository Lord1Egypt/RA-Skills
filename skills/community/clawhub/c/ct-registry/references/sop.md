# ct-registry 操作 SOP / Operating SOP

> 适用范围：跨源检索**临床试验注册库**并归一化为统一竞争格局报告。
> 档位：B（普通输入 + 对外公开检索，零保密数据）。
> 红线：默认仅 PREVIEW；真实联网检索必须显式加 `--run`。

---

## 1. 适用场景

- 想回答「某药物 / 疾病领域**有哪些试验被注册、在研、已完成**？」——分期、状态、申办方、入组人数、国家。
- 需要**竞争格局（landscape）**：谁在做什么、做到哪一期、哪家申办方主导。
- 与 `ct-literature` 互补：本技能**只取注册库结构化元数据，绝不取论文全文/摘要、不总结研究发现**。

## 2. 前置条件

- Python 3（脚本用 `sys.executable`，不需额外依赖；CT.gov 走 `urllib`）。
- 联网（CT.gov 直连公开 API，无密钥）。
- 可选 China CDE：经统一端点 `ct-search.coze.site/run`（WHO ICTRP 与中国 CDE 共用一枚长期有效 token，落盘 `config/ictrp.dat`，经 `search_ictrp.py --store-token` 存储）。旧版独立 CDE 端点已归档至本地 `CDE/` 目录（token 落盘 `CDE/cde.dat`），并于 **2026-08-12 正式退役**；`--cde-legacy` 现为无操作警告并自动回退统一端点，不随包发布。不配置则跳过 CDE，仅 CT.gov。
- 可选 PubChem 富集：需能访问 pubchem.ncbi.nlm.nih.gov（无密钥）。

## 3. 命令示例（从使用到产出）

### 3.1 先 PREVIEW（不联网，确认参数）
```bash
python scripts/ct_registry.py --cond "non-small cell lung cancer" --intr osimertinib --max 50
# 输出：[ct_registry][PREVIEW] add --run to execute network requests.
```

### 3.2 真实检索（加 --run）
```bash
python scripts/ct_registry.py --cond "non-small cell lung cancer" --intr osimertinib --max 50 --run --out-dir ./out
```

### 3.3 仅按药物名检索（--drug 现同时作为 CT.gov 干预词）
```bash
python scripts/ct_registry.py --drug osimertinib --max 50 --run --out-dir ./out
# 说明：--drug 既驱动 CT.gov 干预检索，也用于可选 PubChem 富集。
```

### 3.4 加入中国 CDE 跨源合并（关键字中英文切换 + 确认门 + 静默降级）

`ct_registry.py` 会根据目标源**自动切换关键字语言**，你只需输入一个主检索词。切换分两阶段：

1. **术语优先**：先查 `ct-base/references/term_map.json`（~190 条）与内置 `_EXTRA` 兜底表，命中即用。
2. **未命中需确认（仅国外源）**：若 **CT.gov / PubChem** 的关键字不在术语表且语种不对，
   运行会**中止**并打印建议英文译文——绝不用中文去搜 CT.gov 而悄悄漏检。确认方式：
   - 直接把参数改成英文重写；或
   - 重跑并加 `--confirm-cond` / `--confirm-intr` / `--confirm-drug` 传入确认译文。
   - （仅已知安全的自动化可加 `--auto-confirm` 跳过确认、直接用原文。）

**CDE（国内）静默降级（默认开启，2026-08-11 更新）**：CDE 同时接受中英文，若关键字可派生出 (zh, en) 一对，
技能先用**中文**检索 CDE；若中文返回 0 条且存在有效英文译文，则**自动用英文再查一次**并合并去重（按 `registry_id`），
覆盖以任一种语言登记的试验。这取代了此前默认的中英并行双检（总是同时发两个 HTTP），在覆盖任一种语言登记试验的前提下，
HTTP 调用数约减半。加 `--no-cde-bilingual` 可关闭（退化成单次检索）。

```bash
# 中文主词：CT.gov 自动翻英文；CDE 自动用中文（中文 0 条时静默降级到英文）
python scripts/ct_registry.py --cond "非小细胞肺癌" --with-cde --run --out-dir ./out
# 英文主词：CT.gov 原样；CDE 关键词自动派生中文「非小细胞肺癌」（中文 0 条时静默降级到英文）
python scripts/ct_registry.py --cond "NSCLC" --with-cde --run --out-dir ./out
# 词不在术语表 -> CT.gov 中止等待确认：
python scripts/ct_registry.py --cond "某中文疾病名不在术语表" --with-cde --run --out-dir ./out
#   -> 打印建议英文 + [ABORT]；确认后重跑：
python scripts/ct_registry.py --cond "某中文疾病名不在术语表" --with-cde --run --out-dir ./out \
    --confirm-cond "confirmed english term"
# 仍可用显式 --cde-keyword 覆盖自动派生（同样走静默降级）
python scripts/ct_registry.py --cond "NSCLC" --with-cde --cde-keyword "奥希替尼" --run --out-dir ./out
```

### 3.5 附加 PubChem 靶点富集
```bash
python scripts/ct_registry.py --cond "NSCLC" --drug osimertinib --with-pubchem --run --out-dir ./out
```

## 4. 参数表

| 参数 | 默认值 | 说明 |
|---|---|---|
| `--cond` | — | 疾病/适应症条件（CT.gov `query.cond`） |
| `--intr` | — | 干预/药物（CT.gov `query.intr`） |
| `--drug` | — | **同时作为 CT.gov 干预检索词**；并驱动可选 `--with-pubchem` 富集 |
| `--sponsor` | — | 申办方筛选 |
| `--status` | — | 试验状态筛选（如 RECRUITING） |
| `--max` | `50` | 每源最大返回条数 |
| `--with-pubchem` | off | 附加 PubChem 靶点/化合物富集（需 `--drug`） |
| `--with-cde` | off | 附加中国 CDE 注册库（需 token；失败自动跳过） |
| `--cde-keyword` / `--cde-multi-keywords` | — | CDE 关键词（multi_keyword 为空格分隔 AND）；**可省略**——省略时自动从 `--cond`/`--drug` 派生中文版（并走静默降级） |
| `--cde-mode` | `search` | `search` / `combined` / `multi_keyword`（带结构化过滤或 combined 时自动退化为单语检索） |
| `--cde-indication` / `--cde-drugs-name` / `--cde-drugs-type` / `--cde-appliers` / `--cde-trial-status` | — | CDE 结构化过滤条件 |
| `--confirm-cond` / `--confirm-intr` / `--confirm-drug` / `--confirm-cde-keyword` | — | 已确认译文（英/中），**跳过术语确认门**直接用，避免 CT.gov 因未命中术语表中止 |
| `--auto-confirm` | off | 术语缺失时不中止、直接用原文（可能漏检）；仅已知安全的自动化使用 |
| `--no-cde-bilingual` | off | 关闭 CDE 静默降级（默认开启） |
| `--out-dir` | `./out` | 产出目录 |
| `--run` | off | **必加**才真正联网；否则仅 PREVIEW |

## 5. 产出文件（位于 `--out-dir`）

| 文件 | 说明 |
|---|---|
| `ctgov.json` | CT.gov 原始抓取 |
| `cde.json` | CDE 原始抓取（仅 `--with-cde` 且成功） |
| `normalized.json` | 跨源归一化统一 schema |
| `agg.json` | 聚合统计（分期/状态/申办方分布） |
| `agg_full.json` | 聚合全量 JSON（含明细） |
| `report.md` | **主产出**：人类可读竞争格局报告 |
| `pubchem.json` | PubChem 富集（仅 `--with-pubchem --drug`） |

## 6. 典型工作流

1. PREVIEW 确认 `--cond`/`--intr` 拼写 → 加 `--run` 出 `report.md`。
2. 需要中国数据 → 加 `--with-cde`（确认 token 已落盘）；失败会告警并继续 CT.gov。关键字语言自动切换：中文主词直接给 CDE（静默降级）、英文主词自动翻中文给 CDE（静默降级）。若 CT.gov 关键字不在术语表，运行会中止等待确认译文（见 §3.4 / §7）。
3. 需要化合物靶点 → 加 `--with-pubchem --drug <名>`。
4. 把 `report.md` 作为情报简报的「格局」维度，与 `ct-literature`(证据)、`ct-safety`(信号) 并列。

## 7. 排错

| 现象 | 原因 | 处理 |
|---|---|---|
| 仅 PREVIEW 无网络 | 未加 `--run` | 追加 `--run` |
| CDE 段告警 skipped | token 缺失 / 工作流失败 | 检查 `~/.workbuddy/skills/ct-registry/config/ictrp.dat`（统一端点，WHO/CDE 共用）；legacy 端点检查 `CDE/cde.dat`；或暂时去掉 `--with-cde` |
| 返回过多/无关 | 检索词过宽 | 同时给 `--cond` + `--intr`，或加 `--status` |
| `[ct_registry][CONFIRM] … [ABORT] 未确认, 已停止检索` | CT.gov/PubChem 关键字不在术语表且语种不对 | 运行已中止、未联网；用建议英文重写参数，或加 `--confirm-cond/--confirm-intr/--confirm-drug` 传入确认译文后重跑 |
| `[ct_registry][CONFIRM][CDE] …` | CDE 关键字不在术语表 | 非致命：CDE 同时支持中英文，仍直接用原文检索（双检也会尝试另一语言）；如需精确中文可加 `--confirm-cde-keyword` |
| `[ct_registry][bilingual] CDE 中英双检合并: zh N + en M -> K 条` | CDE 静默降级生效（中文 0 条时自动补发英文） | 正常信息；K 为去重后合并条数 |
| 想查「论文」却用本技能 | 用错技能 | 改用 `ct-literature` |

## 8. 本次修复记录

- **`--drug` 检索修复**：旧版 `--drug` 仅驱动 PubChem 富集，不带 CT.gov 检索词，导致 `ct_registry.py --drug X` 会拉取**未过滤的巨大全集** + PubChem。现 `--drug` 同时作为 CT.gov 干预词（与 `--intr` 等价 fallback），直接按药物名即可拿到真实试验。行为更稳健，且对 `ct-pipeline` 调用无副作用（其已传 `--cond`）。
