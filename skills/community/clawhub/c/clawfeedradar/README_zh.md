# clawfeedradar 技能（ClawHub/OpenClaw）

`clawfeedradar` 是一个基于
[clawsqlite](https://github.com/ernestyu/clawsqlite) 兴趣簇的**个人读报雷达**
Skill。

它封装了上游 `clawfeedradar` Python 包，通过 JSON API 暴露给
OpenClaw Agent，用于：

- 针对单一来源（HN/RSS 等）跑一轮读报雷达；
- 根据 `sources.json` 对多来源批量跑雷达；
- 查看打分结果与生成的 RSS/XML/JSON 文件路径。

Skill 本身不 vendor 上游代码，也不 git clone 仓库——所有逻辑都在
`clawfeedradar` PyPI 包里，通过 `python -m clawfeedradar.cli ...`
调用。

> 如果你要修改雷达的算法或 CLI 行为，请直接在上游仓库里开发；
> 这个 Skill 面向的是 OpenClaw 的 Agent/调度层。

---

## 1. 前置条件

使用本 Skill 前，你应该已经有：

1. **一个带兴趣簇的 clawsqlite 知识库**

   - 通过 `clawsqlite-knowledge` Skill 或直接用 `clawsqlite` CLI：
     - 入库你的文章/笔记；
     - 配置好 Embedding（`EMBEDDING_*` + `CLAWSQLITE_VEC_DIM`）；
     - 跑一次 `clawsqlite knowledge build-interest-clusters` 构建兴趣簇。

2. **一套可用的 clawfeedradar CLI 配置**

   - 上游仓库：<https://github.com/ernestyu/clawfeedradar>
   - 推荐先阅读：
     - `README.md` / `README_zh.md`
     - `docs/SPEC_en.md` / `docs/SPEC_zh.md`
   - 在 clawfeedradar 仓库里配置 `.env`：
     - 知识库路径：`CLAWSQLITE_ROOT` / `CLAWSQLITE_DB`
     - Embedding：`EMBEDDING_*` / `CLAWSQLITE_VEC_DIM`
     - 抓全文：`CLAWFEEDRADAR_SCRAPE_CMD` / worker 数
     - 打分参数：兴趣/时间/人气等权重
     - 小 LLM 参数：摘要 + 中英对照（可选）
     - 输出目录与可选的 git 发布配置

当你能在 CLI 里执行：

```bash
cd ~/.openclaw/workspace/clawfeedradar
python -m clawfeedradar.cli run ...
```

并正常生成 feed 时，这个 Skill 就可以复用那套配置。

---

## 2. 安装

### 2.1 安装 Skill 壳

在 OpenClaw workspace 中执行：

```bash
openclaw skills install clawfeedradar
```

会在当前 workspace 下创建：

```text
~/.openclaw/workspace/skills/clawfeedradar
```

包含：

- `SKILL.md`
- `manifest.yaml`
- `bootstrap_deps.sh`
- `run_clawfeedradar.py`
- `README.md` / `README_zh.md`
- `ENV_EXAMPLE.md`

### 2.2 安装 / 升级 Python 包

`manifest.yaml` 中的 install hook 会在安装时执行
`bootstrap_deps.sh`，完成：

- 使用 `pip` 安装 `clawfeedradar` 包；
- 如基础 venv 只读，则退回安装到
  `skills/clawfeedradar/.venv` 前缀；
- 安装成功后打印 `NEXT:` 提示，说明包安装位置以及运行时将
  加入 `PYTHONPATH` 的 `site-packages` 路径。

正常情况下你不需要手动执行这个脚本；`openclaw skills install`
/ `update` 会自动跑 install hooks。

---

## 3. 运行入口与 JSON API

运行入口是 `run_clawfeedradar.py`，流程：

1. 从 stdin 读取 JSON payload；
2. 根据 `action` 字段选择 handler；
3. 构造一条 `python -m clawfeedradar.cli ...` 命令；
4. 必要时为该进程注入 workspace 本地 `site-packages` 到
   `PYTHONPATH`；
5. 执行并解析 stdout 为 JSON，规范化结果返回给调用方。

返回 JSON 至少包含：

- `ok: true|false`；
- 成功时 `data: ...`，失败时 `error` / `exit_code` / `stdout`
  / `stderr`；
- `next: [...]`：底层 CLI 输出的 `NEXT:` 提示；
- `error_kind`：对错误类型做粗分类（例如缺少 embedding /
  scraper / git 等）。

具体的 CLI 选项和行为请参考上游 clawfeedradar 仓库文档；本 Skill
只是一个薄薄的 JSON 封装。

---

## 4. 支持的 actions

### 4.1 `run_once`

针对单一来源（如 BBC Tech RSS）跑一轮雷达。

**Payload 示例：**

```json
{
  "action": "run_once",
  "source_url": "https://feeds.bbci.co.uk/news/technology/rss.xml",
  "max_source_items": 30,
  "max_items": 12,
  "score_threshold": 0.4,
  "source_lang": "en",
  "target_lang": "zh",
  "enable_preview": true,
  "preview_words": 512,
  "root": "/home/node/.openclaw/workspace/knowledge_data"
}
```

字段与 CLI 参数的对应关系（简化）：

- `source_url` → `--url`
- `max_source_items` → `--max-source-items`
- `max_items` → `--max-items`
- `score_threshold` → `--score-threshold`
- `source_lang` / `target_lang` → `--source-lang` / `--target-lang`
- `enable_preview` → 是否传递 `--no-preview`
- `preview_words` → `--preview-words`
- `root` → 知识库 `--root`（覆盖 `CLAWSQLITE_ROOT`）

返回 JSON 与 CLI 的 `--json` 输出一致，包括：

- 抓取到多少候选；
- 通过打分阈值的有多少；
- 输出的 XML/JSON 文件路径；
- 每条文章的打分与兴趣簇匹配信息等。

### 4.2 `schedule_from_sources_json`

根据 `sources.json` 配置，对多来源批量跑雷达。

**Payload 示例：**

```json
{
  "action": "schedule_from_sources_json",
  "sources_file": "/home/node/.openclaw/workspace/clawfeedradar/sources.json",
  "root": "/home/node/.openclaw/workspace/knowledge_data"
}
```

`sources_file` 的格式与上游 README/SPEC 中描述的一致，每个 source
可以配置：

- URL；
- 每源 `max_source_items` / `max_items`；
- 打分参数覆盖；
- 语言与预览策略等。

本 Skill 会对各个 source 依次执行 CLI，并汇总结果返回。

---

## 5. 环境变量配置

本 Skill 自身不直接读取 `.env`，而是依赖 clawfeedradar 与
clawsqlite 的配置文件。推荐在 OpenClaw 的 Agent 或宿主机环境中
统一配置这些变量。

主要环境变量（详见 `ENV_EXAMPLE.md`）：

- 知识库：`CLAWSQLITE_ROOT` / `CLAWSQLITE_DB`
- Embedding：`EMBEDDING_BASE_URL` / `EMBEDDING_MODEL` /
  `EMBEDDING_API_KEY` / `CLAWSQLITE_VEC_DIM`
- 兴趣簇：`CLAWSQLITE_INTEREST_*`（聚类算法、PCA、簇大小等）
- 抓全文：`CLAWFEEDRADAR_SCRAPE_CMD` / `CLAWFEEDRADAR_SCRAPE_WORKERS`
- LLM：`SMALL_LLM_*` / `CLAWFEEDRADAR_LLM_*`（context、预览长度、节流、语言等）
- 打分：`CLAWFEEDRADAR_INTEREST_SIGMOID_K` / `CLAWFEEDRADAR_W_RECENCY` /
  `CLAWFEEDRADAR_W_POPULARITY` /
  `CLAWFEEDRADAR_RECENCY_HALF_LIFE_DAYS`
- 输出与发布：`CLAWFEEDRADAR_OUTPUT_DIR` /
  `CLAWFEEDRADAR_PUBLISH_GIT_REPO` /
  `CLAWFEEDRADAR_PUBLISH_GIT_BRANCH` /
  `CLAWFEEDRADAR_PUBLISH_GIT_PATH`

---

## 6. 安全注意事项

- 本 Skill 不修改 clawsqlite DB 的 schema，也不会写入 `articles` 等
  表，只会读 embedding 与兴趣簇相关表；
- 所有外部网络请求（RSS 源抓取、全文、LLM、git push）都在
  clawfeedradar CLI 内完成，可通过日志完整审计；
- 如果你希望限制允许的来源或完全禁用发布功能，请在 Agent 配置
  层（env/sources.json 路径）进行约束。

关于 pipeline 细节、打分公式及调参建议，请参考上游仓库中的
`docs/SPEC_en.md` / `docs/SPEC_zh.md` 文档。