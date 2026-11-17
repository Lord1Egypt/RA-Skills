# Agent Asset Federation / Agent Asset 联邦

English is normative; ZH-CN is paired. / 英文为规范文本；简体中文为配对译文。

## Registry / 注册表

Final Agent Asset indexes register in `SECOND_BRAIN_ASSET_REGISTRY`, or by default at `<state-root>/asset-index-registry.json`. The registry is runtime state and must not be stored in the installed Skill directory.
<!-- bilingual-compat: paired English translation appears immediately above. -->
ZH-CN: 最终 Agent Asset 索引注册到 `SECOND_BRAIN_ASSET_REGISTRY`，默认位置为 `<state-root>/asset-index-registry.json`。注册表属于运行时状态，不得存放在已安装的 Skill 目录中。

Each entry records the workspace root, manifest/index hashes, record count, and final-index readiness. Query routing skips entries when the workspace, manifest, index, record count, or final lifecycle state no longer matches registration.
<!-- bilingual-compat: paired English translation appears immediately above. -->
ZH-CN: 每个条目记录 workspace 根目录、manifest/index 哈希、记录数和最终索引就绪状态。当 workspace、manifest、index、记录数或最终生命周期状态与注册信息不再一致时，query routing 会跳过该条目。

`routine_update.py --source-mode asset-manifest` upserts a ready index automatically. Do not register candidate or review scopes.
<!-- bilingual-compat: paired English translation appears immediately above. -->
ZH-CN: `routine_update.py --source-mode asset-manifest` 会自动 upsert 已就绪索引；不要注册 candidate 或 review scope。

## Query Routing / 查询路由

`query_index.py` always queries the primary vault index. Its default `--asset-indexes auto` adds registered project indexes only when one of these is true:
<!-- bilingual-compat: paired English translation appears immediately above. -->
ZH-CN: `query_index.py` 始终查询主知识库索引。默认的 `--asset-indexes auto` 仅在以下任一条件成立时加入已注册项目索引：

- an explicit `--workspace` filter is given;
<!-- bilingual-compat: paired English translation appears immediately above. -->
- ZH-CN: 提供了显式 `--workspace` 过滤；
- the query has code/project intent;
<!-- bilingual-compat: paired English translation appears immediately above. -->
- ZH-CN: 查询具有代码或项目意图；
- a project title, path, or alias is a strong match;
<!-- bilingual-compat: paired English translation appears immediately above. -->
- ZH-CN: 项目标题、路径或 alias 强匹配；
- a bounded lexical probe has high query-term coverage in an asset index.
<!-- bilingual-compat: paired English translation appears immediately above. -->
- ZH-CN: 有界 lexical probe 在某个 asset index 中具有较高查询词覆盖率。

Use `--explain-routing` to inspect selected and skipped indexes. Use `--asset-indexes never` for primary-only retrieval and `--asset-indexes always` only for deliberate cross-index investigation.
<!-- bilingual-compat: paired English translation appears immediately above. -->
ZH-CN: 使用 `--explain-routing` 检查选中和跳过的索引；仅检索主索引时使用 `--asset-indexes never`，只有在明确进行跨索引调查时才使用 `--asset-indexes always`。

## Quality Gate / 质量门

A workspace may keep `.cleanup-extracted/retrieval-benchmark.json` with explicit strict queries. Run:
<!-- bilingual-compat: paired English translation appears immediately above. -->
ZH-CN: workspace 可通过 `.cleanup-extracted/retrieval-benchmark.json` 保存明确的严格查询。运行：

```bash
SKILL_DIR="/path/to/second-brain"
python3 "$SKILL_DIR/scripts/retrieval_quality.py" \
  --index <workspace>/.cleanup-extracted/second-brain-asset-index/documents.jsonl \
  --benchmark <workspace>/.cleanup-extracted/retrieval-benchmark.json \
  --out <workspace>/.cleanup-extracted/retrieval-quality-strict-top1.json
```

Strict cases require Top-1. Keep branch/version, artifact, module, or responsibility qualifiers when nearby projects are genuinely ambiguous.
<!-- bilingual-compat: paired English translation appears immediately above. -->
ZH-CN: 严格用例要求 Top-1。相邻项目确实有歧义时，保留 branch/version、artifact、module 或 responsibility 限定词。

## Optional Semantic Fallback / 可选语义 fallback

Semantic rerank is disabled unless the caller explicitly sets `SECOND_BRAIN_EMBEDDING_ENABLED=1` and supplies a dedicated API key, provider, and HTTPS base URL. It reranks only bounded lexical candidates and sends only the query plus indexed candidate `search_text`; it never uploads source-code bodies or full files.
<!-- bilingual-compat: paired English translation appears immediately above. -->
ZH-CN: 除非调用方显式设置 `SECOND_BRAIN_EMBEDDING_ENABLED=1` 并提供专用 API key、provider 和 HTTPS base URL，否则禁用 semantic rerank。它只重排有界 lexical candidates，只发送查询与候选索引的 `search_text`，绝不上传源代码正文或完整文件。

If no explicit provider is usable, report the capability gap and retain deterministic lexical results. Do not auto-download a local model and do not consume general-purpose provider credentials.
<!-- bilingual-compat: paired English translation appears immediately above. -->
ZH-CN: 如果没有可用的显式 provider，报告能力缺口并保留确定性的 lexical 结果；不要自动下载本地模型，也不要使用通用 provider 凭据。
