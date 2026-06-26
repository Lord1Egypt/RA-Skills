# clawsqlite-knowledge（ClawHub Skill）

`clawsqlite-knowledge` 是一个围绕
[clawsqlite](https://github.com/ernestyu/clawsqlite) **knowledge** CLI
封装的 ClawHub 技能。

它不是通用的 SQLite 工具，而是专门为 OpenClaw/ClawHub 场景做的
「日常知识库操作面板」：

- 从网页 URL 入库 → markdown + SQLite
- 把你的想法/随记/摘抄入库
- 在知识库里检索（FTS / hybrid / vec 自动退级）
- 按 id 查看某条记录
- 通过底层 `clawsqlite` CLI 做健康检查和清理（孤儿文件、备份、VACUUM）

具体的表结构、索引、Embedding、维护逻辑，都由 PyPI 包
`clawsqlite` 实现。`clawsqlite-knowledge` 只是一个薄薄的 JSON 封装，
让 Agent 调用更方便、更安全。

为了让环境更透明可检查，底层 CLI 提供了一个 `doctor` 子命令，用于
自检当前知识库配置（路径、vec0、embedding、小模型等）：

```bash
# 通过 PyPI 安装后
clawsqlite knowledge doctor --json

# 在源码目录下（未安装 wheel 时）
python -m clawsqlite_knowledge.cli doctor
```

建议在新环境首次配置 clawsqlite 时先跑一遍 `clawsqlite knowledge doctor`
看一下报告，再开始正常使用知识库和 Skill。

> 如果你需要完全控制 clawsqlite 的所有能力（包括 plumbing 命令、
> 自己的表、复杂流水线），应该直接使用 `clawsqlite` 包和 CLI，
> 而不是这个 Skill。

---

## 1. 与 clawsqlite 的关系

- **clawsqlite（PyPI / GitHub 仓库）**
  - 一个通用的 SQLite + 知识库 CLI/库；
  - 暴露多个一级命令：`clawsqlite knowledge|db|index|fs|embed`；
  - 适合在 shell 里直接用，也适合写脚本、做其它应用。

- **clawsqlite-knowledge（本 Skill）**
  - 代码目录：`clawhub-skills/clawsqlite-knowledge`；
  - 由 ClawHub 安装并运行；
  - 依赖 PyPI 上的 `clawsqlite>=1.0.2` 包（不 vendor 源码，不 git clone）；
  - 对外暴露一个小而精的 JSON API（并假定环境中可以运行
    `clawsqlite knowledge doctor` 做自检）：
    - `ingest_url`
    - `ingest_text`
    - `search`
    - `show`

你可以简单理解为：

- 需要 **全功能 CLI / 算法** → 用 `clawsqlite`；
- 需要 **给 Agent 用的知识库 Skill** → 用 `clawsqlite-knowledge`。

---

## 2. 安装与升级（两阶段）

在 ClawHub / OpenClaw 中，本 Skill 的安装/升级分为两步：

1. 安装 / 更新 **Skill 壳**（ClawHub 侧）
2. 安装 / 升级 **底层的 clawsqlite PyPI 包（v0.1.7+）**

### 2.1 第一步：安装 Skill 壳

在 OpenClaw 环境中，用 skills 子命令把 Skill 安装到当前 workspace：

```bash
openclaw skills install clawsqlite-knowledge
```

这一步会在本地创建类似这样的目录：

```text
~/.openclaw/workspace/skills/clawsqlite-knowledge
```

此时目录里只有 Skill 的元数据和辅助文件：

- `SKILL.md`
- `manifest.yaml`
- `bootstrap_deps.py`
- `run_clawknowledge.py`
- README / README_zh 等

> **重要：** 完成这一步后，只是把 Skill 壳拉到了 workspace，底层的
> `clawsqlite` CLI 可能还没有安装，或者版本还停留在旧的 0.1.x。第二步
> 会确保环境里存在 **`clawsqlite>=1.0.2`**。

### 2.2 第二步：安装/升级 `clawsqlite`（PyPI v0.1.4）

第二步由 `manifest.yaml` 里声明的引导脚本处理：

```yaml
install:
  - id: clawsqlite_knowledge_bootstrap
    kind: python
    label: Install clawsqlite from PyPI
    script: bootstrap_deps.py
```

脚本的核心逻辑（简化版）：

```python
requirement = "clawsqlite>=1.0.2"
cmd = [sys.executable, "-m", "pip", "install", requirement]
proc = subprocess.run(cmd)
if proc.returncode != 0:
    prefix = _workspace_prefix()
    subprocess.run([
        sys.executable,
        "-m",
        "pip",
        "install",
        requirement,
        f"--prefix={prefix}",
    ])
```

含义是：

- 优先尝试把 `clawsqlite>=1.0.2` 装到 Skill 运行时使用的默认 Python 环境；
- 如果该环境只读或 `pip install` 失败，则退回安装到 workspace 本地前缀：

  ```text
  <workspace>/skills/clawsqlite-knowledge/.clawsqlite-venv
  ```

- 在前缀安装成功后，脚本会打印一段 `NEXT:` 提示，说明：
  - 运行时会自动把该前缀里的 site-packages 目录加入 `PYTHONPATH`；
  - 这样 `python -m clawsqlite_cli` 在 Skill 里就能正常工作；
  - 如果你想在宿主机手动用 CLI，也可以复用这条 `PYTHONPATH`。

如果你想在安装 Skill 壳之后显式触发第二步，可以：

```bash
cd ~/.openclaw/workspace/skills/clawsqlite-knowledge
python bootstrap_deps.py
```

或在支持的环境中直接重跑一次安装命令，让 ClawHub 再次执行 install hooks：

```bash
openclaw skills install clawsqlite-knowledge
```

> **注意：** 这个 Skill **从不** vendor `clawsqlite` 源码，也不会 git clone
> 仓库。唯一的代码来源就是 `pip install "clawsqlite>=1.0.2"`。

### 2.3 `clawsqlite` CLI 实际装在哪里？

取决于你的环境：

- 如果 `pip install clawsqlite>=1.0.2` 能在基础 venv 中成功：
  - `clawsqlite` 可执行入口会出现在该 venv 的 `bin` 目录；
  - 模块 `clawsqlite_cli` 可直接通过 `python -m clawsqlite_cli` 调用。
- 如果走的是 workspace 前缀回退路径：

  ```text
  <workspace>/skills/clawsqlite-knowledge/.clawsqlite-venv/
  ```

  运行时会在执行 `run_clawknowledge.py` 之前，将前缀下的 site-packages
  加入 `PYTHONPATH`，这样同样可以通过 `python -m clawsqlite_cli` 调用。

如果你希望在宿主机上也直接使用 `clawsqlite` CLI，可以参考类似：

```bash
cd ~/.openclaw/workspace/skills/clawsqlite-knowledge
PYTHONPATH="$(python - << 'EOF'
from bootstrap_deps import _workspace_prefix, _site_packages
p = _workspace_prefix()
print(_site_packages(p))
EOF)"$PYTHONPATH" \
  python -m clawsqlite_cli knowledge --help
```

一般情况下，直接当 Skill 用（让 Agent 调用）就够了，不必关心这一步。

---

## 3. 运行约定

`run_clawknowledge.py` 的约定是：

- 从 stdin 读入一个 JSON 对象；
- 读取 `action` 字段，根据不同 action 调用不同 handler；
- 在内部执行：`python -m clawsqlite_cli knowledge ...`；
- 最后把结果 JSON 写回 stdout。

通用字段：

- `root`（可选）：知识库根目录覆盖；
- `action`：下文列出的几种之一。

返回格式统一为：

- 成功：`{"ok": true, "data": {...}}`；
- 失败：`{"ok": false, "error": "...", "exit_code": 1, "stdout": "...", "stderr": "..."}`；
- 若底层 CLI 输出 `NEXT:` 行，则解析为 `next` 数组；
- 失败时还会包含 `error_kind` 字段，粗略标记错误类型（例如
  `missing_scraper` / `missing_embedding` / `other`）。

---

## 4. 推荐的第一步：先跑一次 `doctor`

在一个全新的环境里启用这个 Skill 之前，强烈建议先用底层 CLI 跑一遍
自检命令，看看当前环境处于哪种能力模式：

```bash
clawsqlite knowledge doctor --json
```

报告会检查：

- CLAWSQLITE_ROOT / CLAWSQLITE_DB（路径是否存在）；
- sqlite-vec 扩展和向量表（vec0 / vec 索引是否可用）；
- Embedding 配置（EMBEDDING_* + CLAWSQLITE_VEC_DIM 是否完整）；
- 小模型配置（SMALL_LLM_* 三元组是否完整）；
- 当前整体属于哪种能力模式：
  - LLM + Embedding
  - LLM + 无 Embedding
  - 无 LLM + Embedding
  - 无 LLM + 无 Embedding（纯 FTS）

Agent 可以根据这份报告决定：

- 默认使用 `mode=fts` 还是 `mode=hybrid/vec`；
- 在能力缺失时是否向用户输出 NEXT 提示，指导补齐配置。

## 5. 支持的 actions

### 4.1 `ingest_url`

从 URL 入库一篇文章。

**Payload 示例：**

```json
{
  "action": "ingest_url",
  "url": "https://mp.weixin.qq.com/s/UzgKeQwWWoV4v884l_jcrg",
  "title": "微信文章: Ground Station 项目",
  "category": "web",
  "tags": "wechat,ground-station",
  "gen_provider": "openclaw",
  "root": "/home/node/.openclaw/workspace/knowledge_data"
}
```

说明：

- 真正的网页抓取由 `clawsqlite knowledge ingest --url ...` 调用的
  抓取脚本完成；
- 建议在环境中配置 `CLAWSQLITE_SCRAPE_CMD` 为 clawfetch Skill/CLI；
- `ingest_url` 只负责把 JSON 请求翻译成 CLI 调用，并返回 JSON 结果。

### 4.2 `ingest_text`

从一段文本/想法/摘抄入库，标记为本地来源。

**Payload 示例：**

```json
{
  "action": "ingest_text",
  "text": "今天想到一个关于网络抓取架构的想法……",
  "title": "网络抓取架构随记",
  "category": "idea",
  "tags": "crawler,architecture",
  "gen_provider": "openclaw",
  "root": "/home/node/.openclaw/workspace/knowledge_data"
}
```

适用场景：

- 突然想到的点子 / 设计想法；
- 书里/小说里的金句摘抄；
- 你和 Agent 对话时，让它“帮我记一下”。

底层 `clawsqlite knowledge ingest --text ...` 会：

- 从正文构造“长摘要”（约 800 字以内，按自然段边界软截断）；
- 用 jieba/启发式抽标签；
- 在 `clawsqlite>=1.0.2` 中，这套标签生成逻辑与查询侧关键词抽取共用
  同一条 TextRank + 语义向心流水线；
- 在配置了 Embedding 的情况下，为摘要打向量并写入 vec 表；
- 用拼音/ASCII 生成文件名，在 articles 目录下写入 markdown。

### 4.3 `search`

在知识库中检索，使用 `clawsqlite>=1.0.2` 提供的完整检索流水线：
`query_refine/query_tags + FTS/vec hybrid`。

底层调用的是 `clawsqlite knowledge search ... --json`，本 Skill 只负责
转发参数和返回结果。

高层行为：

- 查询会被拆成两部分：
  - `query_refine`：更适合检索的一句话（由 Small LLM 或启发式生成）；
  - `query_tags`：若干个关键词（数量由 `CLAWSQLITE_SEARCH_QUERY_TAG_MIN/MAX`
    控制）。
- 是否使用 Small LLM 和 Embedding，会决定内部的「能力模式」：
  - Mode1（有 LLM + 有 Embedding）：用 LLM 生成 query_refine/query_tags，
    打分时同时使用摘要/标签向量 + FTS + 标签字面匹配；
  - Mode2（有 LLM + 无 Embedding）：用 LLM 生成 query_refine/query_tags，
    打分时使用 FTS + 标签字面匹配；
  - Mode3（无 LLM + 有 Embedding）：用启发式生成 query_refine/query_tags，
    打分时使用摘要/标签向量 + FTS + 标签字面匹配；
  - Mode4（无 LLM + 无 Embedding）：启发式 query_refine/query_tags +
    FTS + 标签字面匹配。
- 在有 Embedding 的模式下，打分逻辑会：
  - 将摘要与标签分别 embed 到 vec0 表（`articles_vec`、`articles_tag_vec`）中；
  - 用 `1/(1+d)` + 以 0.5 为中心的 Logistic Sigmoid 归一化向量距离；
  - 将标签通道拆成“标签语义得分（tag vector）”和“标签字面得分（tag lexical）”，拆分比例由 `CLAWSQLITE_TAG_VEC_FRACTION` 控制；
  - 对标签字面得分应用可选的 log 压缩：`ln(1+αx)/ln(1+α)`，`α` 来自
    `CLAWSQLITE_TAG_FTS_LOG_ALPHA`（默认 5.0），防止一堆弱命中压制语义得分。
- 最终总分是 vec/fts/tag/priority/recency 多通道按权重线性组合，
  不同模式的默认权重由 `CLAWSQLITE_SCORE_WEIGHTS_MODE1..4` 控制
  （兼容旧的 `CLAWSQLITE_SCORE_WEIGHTS*`）。

更多细节可参考本目录的 `ENV_EXAMPLE.md` 与 clawsqlite 仓库的
README/README_zh。

**Payload 示例：**

```json
{
  "action": "search",
  "query": "网络爬虫 架构",
  "mode": "hybrid",
  "topk": 10,
  "category": "idea",
  "tag": "crawler",
  "include_deleted": false,
  "root": "/home/node/.openclaw/workspace/knowledge_data"
}
```

语义：

- `mode=hybrid`：
  - 如果 Embedding + vec 表可用 → 用向量 + FTS 混合检索；
  - 如果不可用 → 自动退化为 FTS；
- 支持按 `category` / `tag` / `since` / `priority` 等过滤；
- 返回结果里包含 `id` / `title` / `category` / `score` / `created_at` 等字段。

### 4.4 `show`

按 id 查看单条记录。

**Payload 示例：**

```json
{
  "action": "show",
  "id": 3,
  "full": true,
  "root": "/home/node/.openclaw/workspace/knowledge_data"
}
```

- `full=true` 时，会通过 `clawsqlite knowledge show --full` 返回正文内容；
- 适合在 Agent 侧拿到 id 之后，拉取完整上下文进行总结、重写等操作。

---

## 5. 错误处理与 NEXT 提示

底层 `clawsqlite` CLI 为 Agent 设计，所有错误都会带一条
`NEXT: ...` 导航提示，例如：

```text
ERROR: db not found at /path/to/db. Check --root/--db or .env configuration.
NEXT: set --root/--db (or CLAWSQLITE_ROOT/CLAWSQLITE_DB) to an existing knowledge_data directory, or run an ingest command first to initialize the DB.
```

`run_clawknowledge.py` 在 CLI 退出码非 0 时，会解析这些 `NEXT:` 行，
将其放入返回 JSON 的 `next` 数组，并设置 `error_kind` 字段，方便
上层 Agent 根据错误类型和 NEXT 做下一步动作。

---

## 6. 什么时候用 clawsqlite-knowledge，什么时候直接用 clawsqlite？

适合用 **clawsqlite-knowledge** 的场景：

- 在 ClawHub/OpenClaw 中，需要一个「个人知识库 Skill」给 Agent 调；
- 日常主要操作是：URL / 文本入库、搜索、按 id 查看记录。

适合直接用 **clawsqlite** 的场景：

- 需要对知识库的 schema/索引/Embedding 流程有完全掌控；
- 需要 plumbing 命令：
  - `clawsqlite db schema/exec/backup/vacuum`
  - `clawsqlite index check/rebuild`
  - `clawsqlite fs list-orphans/gc`
  - `clawsqlite embed column`
- 正在开发新的应用，而不是单一的个人知识库。

两者可以复用同一套数据根目录（`CLAWSQLITE_ROOT` / `CLAWSQLITE_DB` /
`CLAWSQLITE_ARTICLES_DIR`），方便你在 CLI 和 Skill 之间切换。

### 中文 FTS 退级：libsimple 缺失时的 jieba 模式

本 Skill 在分词与检索层面完全依赖底层 `clawsqlite` 的实现。当
`libsimple`（CJK tokenizer 扩展）无法加载时，可以通过
`CLAWSQLITE_FTS_JIEBA=auto|on|off` 启用 `jieba` 预分词模式：

- `auto`（默认）：仅当 `libsimple` 无法加载且环境中有 `jieba` 时启用；
- `on`：强制启用 jieba 预分词（即使 `libsimple` 可用）；
- `off`：禁用 jieba 预分词。

在 jieba 模式下，CJK 文本会先用 jieba 分词并用空格拼接后写入 FTS；
查询侧也使用同样的规则归一化，因此写入 / 重建 / 查询保持一致。
英文文本不受影响。

如果在已有数据库上切换该模式，建议执行：

```bash
clawsqlite knowledge reindex --rebuild --fts
```

让 FTS 索引按当前 tokenizer 配置（simple 或 jieba 退级）重建。
详细行为说明见 `clawsqlite` 仓库的 README/README_zh。

---

## 7. 升级说明（clawsqlite>=1.0.2）

- 本 Skill 依赖 `clawsqlite>=1.0.2`，更新时会通过 `bootstrap_deps.py` 安装新的 PyPI 版本。
- 在 OpenClaw 中，推荐的下发流程是：`openclaw skills update clawsqlite-knowledge`，如同时调整了 `CLAWSQLITE_FTS_JIEBA`，再执行一次 FTS 重建。

## 8. 兴趣簇与兴趣报告（通过底层 clawsqlite CLI）

本 Skill 的 JSON API 刻意保持很小（入库/检索/按 id 查看），但其底层
仍然是同一个 SQLite 数据库和 articles 目录。因此，你可以直接使用
`clawsqlite knowledge` 的兴趣簇与兴趣报告命令，在同一个知识库上做
更深入的分析。

典型用法：

```bash
# 基于现有 embedding 构建或刷新兴趣簇
clawsqlite knowledge build-interest-clusters \
  --db /path/to/knowledge.sqlite3 \
  --min-size 5 \
  --max-clusters 16

# 检查兴趣簇质量（簇半径 / 簇间距离 / PCA 图）
clawsqlite knowledge inspect-interest-clusters \
  --db /path/to/knowledge.sqlite3 \
  --vec-dim 1024

# 生成一份周度兴趣报告（Markdown + PNG，HTML/PDF 可选）
clawsqlite knowledge report-interest \
  --db /path/to/knowledge.sqlite3 \
  --days 7 \
  --vec-dim 1024 \
  --lang zh \
  --format html \
  --out-dir /path/to/reports
```

`report-interest` 会在 `--out-dir`（默认为当前目录下的 `./reports`）
下创建一个按时间窗口结束日期命名的目录，例如
`reports/20260331-report/`，其中至少包含：

- `report.md`  – 报告正文（窗口内新增文章数、涉及兴趣簇数、每日新增、
  按兴趣簇分布、簇心 PCA 图、升温/降温簇等）；
- `images/`    – PNG 图表（`daily_articles.png` / `cluster_distribution.png`
  / `interest_clusters_pca.png`）。

如果环境中安装了 `pandoc`，且未显式加 `--no-pdf`，CLI 会在生成
Markdown 后尝试：

```bash
pandoc report.md -o report.pdf
```

缺少 LaTeX 等依赖时，该步骤是“尽力而为”的：命令不会失败，只是目录中
可能没有 `report.pdf`。

当你传入 `--format html`，并且环境中有 `pandoc` 时，CLI 会在写出
`report.md` 后尝试执行等价于：

```bash
pandoc report.md -s -o report.html --mathjax --self-contained
```

成功时会额外生成一个 `report.html`，包含内联图片的自包含 HTML 报告。

需要注意的是：

- 本 Skill 本身只暴露入库/检索/查看的 JSON API；
- 兴趣簇构建与兴趣报告（`build-interest-clusters` /
  `inspect-interest-clusters` / `report-interest`）目前仅通过底层
  `clawsqlite` CLI 提供；
- Skill 与 CLI 复用同一个知识库根目录，因此你可以一边用 Skill 做
  日常 ingest/search，一边用 CLI 定期生成兴趣簇与周报。
