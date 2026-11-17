# ct-literature 批量检索 — 规格与格式规范（Batch Retrieval Spec）

> 入口：`python scripts/batch.py <spec_file> [--run] [--out-dir DIR] [--lint] [--max-total N] [--resume] [--force] [--concurrency N] [--pack]`
> 通用引擎：`scripts/batch_lib.py`（自包含，无 ct-base 运行时依赖）。
> 本技能适配器：`scripts/batch.py`（仅声明 `ADAPTER` 字段→CLI flag 映射）。

## 1. 这是什么

把"一批检索主题"放进一个文档，批量依次跑 ct-literature，每个主题产出独立子目录的报告，最后聚合为一张总览。

- **默认 SAFE PREVIEW（dry-run）**：不传 `--run` 只打印执行计划（每条将执行的完整命令 + 输出目录），**不联网**。
- 传 `--run` 才真正联网检索。
- 每个 entry 写入独立 `out_dir/<id>/` 子目录，避免固定文件名互相覆盖。
- 单条失败不影响整批（记 `error` + 写 `batch_errors.log` 并继续）。

## 2. 调用方式

```bash
# 1) 先 dry-run 看计划（强烈建议）
python scripts/batch.py references/examples/batch_lung_ia2.txt

# 2) 确认无误后真正执行
python scripts/batch.py references/examples/batch_lung_ia2.txt --run --out-dir ./batch_out

# 3) 仅校验格式（不执行、不联网）
python scripts/batch.py my_spec.txt --lint

# 4) 配额封顶 / 断点续跑
python scripts/batch.py big_spec.txt --run --max-total 50
python scripts/batch.py big_spec.txt --run --resume     # 跳过已完成的 entry
```

常用参数：

| 参数 | 含义 |
|---|---|
| `spec_file` | 检索关键词文档（行列表 `.txt` 或 YAML `.yaml`） |
| `--run` | 执行检索（联网）；缺省=只打印计划 |
| `--out-dir` | 结果根目录，默认 `./batch_out`，每 entry 一个子目录 |
| `--lint` | 仅校验规格，不执行、不联网 |
| `--max-total N` | 最多执行前 N 个有效 entry（配额封顶） |
| `--force` | 忽略配额预警强制执行 |
| `--resume` | 跳过已完成（存在 `.done` 标记）的 entry，支持断点续跑 |
| `--delay SEC` | 每条 entry 之间间隔秒数（限流友好；并发模式下不适用） |
| `--timeout SEC` | 单 entry 超时（默认 1800） |
| `--concurrency N` | entry 级并发数（默认 1 顺序执行；子进程层并发） |
| `--pack` | 打包模式：多 entry 合成一次 Coze 调用（见 §6） |
| `--pack-size N` | 每包 entry 数（默认 8） |
| `--pack-retries N` | 单包发送失败重试次数（默认 1） |
| `--pack-fallback auto\|strict` | 包失败时回退逐 entry（默认）或中止 |
| `--progress` | `human`（默认）或 `json` |

## 3. 格式 A：行列表（**默认主路径**，零格式负担）

一行一查询；`#` 开头为注释，空行忽略。

```
# 肺癌 IA 期文献批量检索
stage IA2 lung adenocarcinoma prognosis
acinar predominant adenocarcinoma | review_type=systematic year_from=2020
adjuvant immunotherapy early-stage NSCLC | safety=true depth=deep
osimertinib adjuvant NSCLC | review_type=systematic year_from=2018 max=30 concepts="intervention:osimertinib;outcome:disease-free survival"
recent NSCLC biomarker | recent_months=6 with_guidelines=true
```

语法规则：

- **主体**：`|` 之前整段文本即检索主题（映射到 `topic`）。
- **附加参数**：`|` 之后为 `key=value` 对，空格分隔；含空格的值用双引号包裹（如 `"intervention:osimertinib;outcome:disease-free survival"`）。
- **布尔开关**：`safety=true`/`safety=false`；`with_europepmc=false` 会展开为 `--no-with-europepmc`。
- **结构化概念 `concepts`**：`;` 分隔多项，`:` 或 `=` 作 TYPE/VALUE 分隔，例如
  `concepts="intervention:osimertinib;outcome:disease-free survival"` →
  两条 `--concept intervention=osimertinib` 与 `--concept outcome=disease-free survival`。
- **技能切换（跨技能，v1 不支持）**：`@ct-safety` 之类行切换其后行的技能上下文；v1 仅 `ct-literature` 有效，其它技能会被标 `skipped`。

支持的字段即下方 YAML 表的同一套（见 §4 表）。

## 4. 格式 B：YAML（可选高级格式）

适用于多字段 / 嵌套 `concepts` / 程序化生成场景。引擎先合并 `defaults`（entry 覆盖 default），再逐条校验。

```yaml
version: 1
skill: ct-literature
defaults:
  year_from: 2015
  max: 30
entries:
  - id: lung_adeno_ia2          # 稳定 id → 子目录名 + manifest 键；缺省自动 slug
    label: "IA2 肺腺癌 预后"      # 报告用人类可读标签（可选）
    topic: "stage IA2 lung adenocarcinoma prognosis"
    review_type: systematic
    year_from: 2020             # 覆盖 default 的 2015
  - id: acinar_vs_lepidic
    topic: "acinar predominant adenocarcinoma versus lepidic"
    safety: true
  - id: immuno
    topic: "adjuvant immunotherapy early-stage NSCLC"
    depth: deep
    concepts:                   # 列表；每项为 {TYPE: VALUE}
      - intervention: pembrolizumab
      - outcome: disease-free survival
```

**元数据字段（批量层，所有技能通用）**：`id`（必填且 `[a-z0-9_]`、缺省自动 slug）、`label`、`skill`、`enabled`（默认 true，false=跳过）。其余字段为技能专属（下表）。

**ct-literature 字段表（行列表 / YAML 通用）**：

| 字段 | CLI flag | 类型 | 说明 |
|---|---|---|---|
| `topic` | `--topic` | 值（必填） | 检索主题 |
| `review_type` | `--review-type` | 值 | systematic / scoping / … |
| `year_from` / `year_to` | `--year-from` / `--year-to` | 值 | 年份边界 |
| `max` | `--max` | 值 | 每源最大条数 |
| `sources` | `--sources` | 值 | 如 `OpenAlex,EuropePMC` |
| `depth` | `--depth` | 值 | quick / standard / deep |
| `keywords` | `--keywords` | 值 | 逗号分隔关键词 |
| `verify` | `--verify` | 值 | all / top / background |
| `only_type` | `--only-type` | 值 | 文献类型过滤 |
| `date_from` / `date_to` | `--date-from` / `--date-to` | 值 | 月级日期窗口 YYYY-MM-DD |
| `recent_months` | `--recent-months` | 值 | 最近 N 月 |
| `concepts` | `--concept`（可重复） | 结构概念 | `TYPE=VALUE`，多条 |
| `safety` | `--safety` | 开关 | 安全/CSM 分轨 |
| `cochrane` | `--cochrane` | 开关 | Cochrane CDSR |
| `snowball` | `--snowball` | 开关 | 引用网络扩展 |
| `with_arxiv` | `--with-arxiv` | 开关 | 启用 arXiv |
| `with_semantic_scholar` | `--with-semantic-scholar` | 开关 | 启用 S2 |
| `include_reviews` | `--include-reviews` / `--no-include-reviews` | 布尔可选 | 默认开 |
| `with_europepmc` | `--with-europepmc` / `--no-with-europepmc` | 布尔可选 | 默认开 |
| `with_biorxiv` / `with_medrxiv` / `with_guidelines` | 同上 | 布尔可选 | 默认开（前两者）/ 可选 |
| `with_pubmed` | `--with-pubmed` | 开关 | v1.7.0 NCBI E-utilities 独立车道（默认关） |
| `pubmed_fallback` | `--pubmed-fallback` / `--no-pubmed-fallback` | 布尔可选 | Europe PMC 故障自动补位，默认开 |
| `verify_dois` | `--verify-dois` | 开关 | DOI 专项审计（需 `--run`，逐条联网） |
| `original_only` | `--original-only` | 开关 | 只要原创研究（doc-type 反向甄别） |
| `online` / `offline` / `local` | 同名 flag | 开关 | 检索通道控制 |

> 新增/调整字段：编辑 `scripts/batch.py` 的 `ADAPTER["fields"]` 即可，无需改引擎。

## 5. 输出布局

```
<out_dir>/
  batch_manifest.json   # 规格回显 + 每 entry {status, out_dir, cmd, returncode, elapsed_sec, n_results}
  batch_index.html      # 汇总表，链接到各 entry 的 lit_report.html
  batch_summary.md      # 人类可读摘要
  batch_errors.log      # 失败 entry 的 stderr（无失败则删除）
  <entry_id_1>/         # 该 entry 的全部原生产物（lit_report.html / .xlsx / .merged.json …）
  <entry_id_2>/
```

## 6. 配额与限流

- OpenAlex 免 key 仅 **100 次/天**（自 2026-02-13）。批量 N 条极易击穿。
- 引擎在 `--run` 前估算命中数；若预计 > 90 次且未加 `--force` / `--max-total`，**直接中止（exit 3）且不联网**。
- 执行默认**顺序**进行（限流友好）；`--delay` 可加间隔，`--max-total` 封顶。
- 长任务中断可用 `--resume` 续跑（已完成 entry 写入 `.done` 标记，跳过不重跑）。

## 6. Pack 模式（`--pack`，一次 Coze 调用打包多个 entry）

默认模式下每条 entry 是一次独立子进程调用，而单次 `ct_literature.py` 内部会向 Coze 发
**6 个源并行调用 + 1 条汇总留痕**——批量 N 条 ≈ N×7 次 Coze 调用。`--pack` 把这 N 条
打包成**每包一次**调用，由 Coze 端拆解逐条执行后批量返回。

```
翻译预处理（一次）  →  拆包（≤8 entry/包）  →  每包一次 POST（mode=batch_search）
→  Coze 端逐条执行、批量返回  →  按 entry id 拆回写 pack_payloads.json
→  --from-pack 子进程复用 ct_literature.py 全管线（合并/去重/报告）
```

- **翻译预处理一次完成**：全部 entry 的 topic/concepts 在引擎内统一翻英（本地词典 +
  联网兜底按唯一片段去重），随包下发英文检索式；子进程收到英文 topic 时翻译直接短路。
- **传输复用既有设施**：异步协议（`{accepted, run_id}` + 轮询 `/run/status/{id}`，
  绕过网关 60s 硬超时）+ 大结果集 S3 外置回拉。
- **源路由与非 pack 一致**：`semantic_scholar` 恒本地（私人 key 零传递）不进包；
  `openalex` 仅本机无 key 时进包（有 key 走本地 keyed pool，由 `--from-pack` 子进程
  按原路由执行）——覆盖度与常规模式完全相同。
- **失败隔离**：逐条 try/catch 在 Coze 端；单条/单包失败只回退受影响 entry
  （`--pack-fallback strict` 可改为中止）；`--from-pack` 子进程失败会自动用原命令
  （常规联网检索）重试一次。
- **审计更干净**：每包一条飞书汇总，取代 N 条。
- **端点未实现契约时自动回退**逐 entry 模式（响应分类：`results` → 支持；
  search 形态响应 / 400 schema 错 → 不支持）。
- dry-run 加 `--pack` 可预览打包计划（包划分、每包 queries 数、检索式），**零联网**。
- Coze 端契约（请求/响应/异步/S3/验收清单）→ [references/batch_search_contract.md](references/batch_search_contract.md)。

```bash
# 预览打包计划（不联网）
python scripts/batch.py my_spec.txt --pack
# 执行：20 条 → 3 包，每包一次 Coze 调用
python scripts/batch.py my_spec.txt --pack --run --out-dir ./batch_out
# 打包执行 + 后端子进程并发（本地合并/报告阶段）
python scripts/batch.py my_spec.txt --pack --run --concurrency 3
```

## 7. 范围与路线图

- **v1（已落地）**：仅 ct-literature 单技能；行列表为默认 + YAML 可选；默认 dry-run；不做 OA-PDF 批量下载。
- **v1.1（已落地，2026-10-20）**：`--concurrency N` entry 级并发（零外部依赖，墙时间 ÷N）。
- **v1.2（客户端已落地，2026-10-20）**：`--pack` 打包调用模式（翻译预处理一次完成 /
  异步轮询 / S3 回拉 / 逐条错误隔离 / 自动回退）。**Coze 端 `batch_search` 契约待实现**
  （见 references/batch_search_contract.md）；实现前 `--pack` 会自动回退逐 entry 模式，
  功能不受影响。
- **v2**：补 ct-safety / ct-registry 的 `ADAPTER`；支持跨技能多块文档；增加 CSV 格式。
- **v3（可选）**：OA-PDF 批量下载透传；更丰富的聚合视图。

