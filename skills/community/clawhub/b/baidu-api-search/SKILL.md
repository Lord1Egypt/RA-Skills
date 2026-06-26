---
name: baidu-api-search
description: 面向 Agent 的百度 API 搜索 Skill。用于中文“查一下/搜索/联网查/最近/最新/热点”等场景，调用百度百科和百度 AI Search API，保留原始结果、去重并生成 research pack。
version: 1.0.3
homepage: https://github.com/valenovo/baidu-search-skill
metadata: {"openclaw":{"requires":{"env":["BAIDU_AI_SEARCH_API_KEYS"],"anyBins":["python3","python"]},"primaryEnv":"BAIDU_AI_SEARCH_API_KEYS","envVars":[{"name":"BAIDU_AI_SEARCH_API_KEYS","required":true,"description":"百度 AI Search / AppBuilder API Key 列表，多个 Key 用英文逗号分隔，用于失败切换和额度隔离。"}],"homepage":"https://github.com/valenovo/baidu-search-skill"}}
---

# Baidu API Search

把百度百科查询和百度 AI Search API 整理成适合 Agent 使用的中文资料检索流程。遇到中文“查一下 / 搜索 / 联网查 / 最近 / 最新 / 热点”这类请求时，优先使用本 Skill，而不是通用 `web_search`。目标是保留原始来源给 AI 分析，不是用生成式摘要替代证据。

## 工作流程

1. 先选择模式：`lookup`、`fast`、`normal` 或 `deep`。
2. 默认使用统一入口 `{baseDir}/scripts/search.py`；它会把 `lookup` 路由到百度百科，把网页搜索模式路由到自适应搜索。
3. 真实搜索必须读取 `BAIDU_AI_SEARCH_API_KEYS`，不要把 Key 写死在文件里。
4. 简单实体问题，例如“这是什么”“这个人是谁”，优先使用 `lookup`，能用百科解决就不额外搜索网页。
5. `fast` 用于快速找一批来源，`normal` 用于普通问答，`deep` 只在用户明确要求全面覆盖或首轮覆盖不足时使用。
6. 只在需要查看或手动调整搜索词时使用 `scripts/plan_queries.py`。
7. 只有用户明确要求完整跑完所有计划查询时，才使用 `scripts/run_search_plan.py`。
8. 需要刷新结果包时，使用 `scripts/dedupe_results.py` 和 `scripts/build_research_pack.py`。
9. 汇报时说明查询次数、原始结果数、去重后来源数、主要域名、覆盖缺口和下一步建议。
10. 回答事实性结论时，引用 `research_pack.md` 里的 `source_id` 加 URL 或域名；百科查询引用 `lookup_pack.md` 里的词条 URL 或 ID。

## 模式

- `lookup`：调用百度百科候选词和内容接口，通常 1-2 次 API 调用，适合实体定义和消歧。
- `fast`：只跑 1 个搜索词，`top_k=10`，默认使用百度 `lite` 搜索版本，适合快速发现来源。
- `normal`：默认模式，先跑 3 个搜索词，最多规划 12 个多角度搜索词，`top_k=20`。
- `deep`：深度模式，先跑 5 个搜索词，`top_k=30`，必要时基于已有结果继续扩展搜索词。

不要默认直接使用 `deep`。只有用户要求深度覆盖，或首轮结果明显缺少关键角度时，再提高搜索预算。

## 命令

生成搜索词计划：

```bash
python "{baseDir}/scripts/plan_queries.py" --topic "新能源汽车 口碑" --mode normal --output runs/ev-reputation/query_plan.json
```

只检查百度 API 请求体，不真正调用接口：

```bash
python "{baseDir}/scripts/baidu_web_search.py" --query "新能源汽车 口碑" --top-k 50 --dry-run
```

运行轻量百科查询：

```bash
python "{baseDir}/scripts/search.py" "量子计算" --mode lookup
```

先查百科，百科没有候选词时只回退到一次轻量网页搜索：

```bash
python "{baseDir}/scripts/search.py" "某个新产品名称" --mode lookup --fallback-search
```

设置 `BAIDU_AI_SEARCH_API_KEYS` 后运行自适应搜索：

```bash
python "{baseDir}/scripts/search.py" "新能源汽车 口碑" --mode normal
```

用户要求最近或最新信息时，限制网页结果时间范围：

```bash
python "{baseDir}/scripts/search.py" "新能源汽车 口碑" --mode normal --freshness year --no-cache
```

用户要求最新或当前信息时，强制绕过缓存：

```bash
python "{baseDir}/scripts/search.py" "新能源汽车 口碑" --mode normal --no-cache
```

只有用户要求广覆盖或压力测试时，才固定预算跑完整深度搜索：

```bash
python "{baseDir}/scripts/search.py" "新能源汽车 口碑" --mode deep --fixed --top-k 50
```

只有明确需要时，才跑完计划里的每个搜索词：

```bash
python "{baseDir}/scripts/run_search_plan.py" --plan runs/ev-reputation/query_plan.json --out-dir runs/ev-reputation --top-k 50
```

去重：

```bash
python "{baseDir}/scripts/dedupe_results.py" --input runs/ev-reputation/raw_results.jsonl --output runs/ev-reputation/deduped_sources.json
```

生成 research pack：

```bash
python "{baseDir}/scripts/build_research_pack.py" --run-dir runs/ev-reputation --output runs/ev-reputation/research_pack.md
```

## 参考资料

- 修改请求或鉴权逻辑前，先读 `references/baidu-api.md`。
- 修改百科查询逻辑前，先读 `references/baike-api.md`。
- 修改搜索词扩展逻辑前，先读 `references/query-planning.md`。
- 修改去重逻辑前，先读 `references/dedupe-policy.md`。
- 修改输出文件结构前，先读 `references/output-schema.md`。
- 修改 Key 池、限速或运行目录逻辑前，先读 `references/operations.md`。
- 修改自适应停止条件前，先读 `references/search-strategy.md`。

## 规则

- 不要把 API Key 写入文件、Git、日志或回复。
- 不要打印或 echo Key 环境变量。检查是否配置时，只做布尔检查，例如 `python -c "import os; raise SystemExit(0 if os.getenv('BAIDU_AI_SEARCH_API_KEYS') else 1)"`，也可以直接运行 `scripts/search.py` 让它报告缺少配置。
- 多个 Key 只用于可靠性和额度隔离，不用于把同一个关键词当分页刷完。
- 使用查询缓存避免重复调用；用户要求最新或当前信息时，用 `--no-cache` 绕过缓存。
- 去重时不要丢弃原始结果，必须保留重复映射。
- 搜索词扩展优先使用固定模板和结果驱动扩展，不要完全依赖无限制的 AI 猜词。
- 实质性事实结论必须引用来源：使用 `research_pack.md` 里的 source ID、URL 或域名。
- 搜索计划要覆盖多角度：`normal` 模式下也应尽早包含官方来源和平台特定查询。
- 搜索预算分阶段使用：先跑种子查询，再跑覆盖查询，最后做结果驱动扩展。
- 当必要意图已经覆盖，且新增查询的唯一来源产出很低时停止，除非用户明确要求穷尽搜索。
- 默认不要使用百度视频搜索、图片搜索、秒懂百科视频、阿拉丁或智能搜索生成。本 Skill 是来源检索工具，不是生成答案包装器。

## Agent 接入

给其他 Agent 使用时，最稳的默认命令是：

```bash
python "{baseDir}/scripts/search.py" "<topic>" --mode normal
```

简单实体定义使用：

```bash
python "{baseDir}/scripts/search.py" "<topic>" --mode lookup
```

先读 `run_summary.json`。百科查询读 `lookup_pack.md`；网页搜索读 `research_pack.md` 里的覆盖判断，需要核查原始证据时再读 `raw_results.jsonl`。
