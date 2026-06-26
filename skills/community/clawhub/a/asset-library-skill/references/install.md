# Install

在首次安装、首次接入 AutoClaw/OpenClaw、缺少 key、缺少 MCP 注册、或 `caixu-skill` 无法确认环境已就绪时，先读这份文件。

目标不是手改零散配置，而是让 agent 用一套确定步骤把材序技能包装好、验活，再回到业务 skill。

## 什么时候必须先做安装

满足任一条件时，不要直接路由到 phase skill，先完成安装：

- 当前机器还没跑过 `pnpm install`
- 还没跑 `pnpm build`
- `openclaw` 或 `mcporter` 不可用
- AutoClaw profile 还没 onboard
- 不确定 `caixu-skill` 和默认 MVP phase skills 是否已挂到 AutoClaw
- 不确定两个 MCP 是否已注册
- 缺少下列任一关键 key 或 runtime config

## 必备环境

至少具备：

1. Node.js `24.x`
2. `pnpm` `10.x`
3. `openclaw`
4. `mcporter`
5. 一个可写的 SQLite 路径

可选但推荐：

1. `tmux`
2. 一个固定的演示目录
3. 如需高级可选扩展，再准备一个评委模式提交页地址

## 必填 key 与 config

最小可用配置：

- `CAIXU_AGENT_MODEL=glm-4.6`
- `CAIXU_AGENT_API_KEY`
- `CAIXU_ZHIPU_PARSER_API_KEY`
- `CAIXU_ZHIPU_OCR_API_KEY`
- `CAIXU_ZHIPU_VLM_API_KEY`
- `CAIXU_SQLITE_PATH`

只有在要跑提交演示时才强依赖：

- `CAIXU_JUDGE_DEMO_URL`

通常推荐同时保留：

- `CAIXU_PARSE_MODE=auto`
- `CAIXU_ZHIPU_PARSER_MODE=lite`
- `CAIXU_ZHIPU_OCR_ENABLED=false` 或 `true`
- `CAIXU_CLI_PROGRESS=true`
- `CAIXU_CLI_HEARTBEAT_MS=5000`

如果要启用可选的本地语义检索增强，额外建议配置：

- `CAIXU_EMBEDDING_MODEL=Xenova/paraphrase-multilingual-MiniLM-L12-v2`
- `CAIXU_EMBEDDING_CACHE_DIR`
- `CAIXU_EMBEDDING_TIMEOUT_MS=120000`

说明：

- 默认检索由 `FTS + agent_tags` 组成
- 本地 embedding 与向量召回是可选增强，首次启用时会在本地下载 embedding 模型，CPU 可跑，但首次耗时会更长
- 如果本地 embedding 初始化失败，默认查询仍应保持可用
- 旧库不会自动获得语义索引；首次启用后需要对目标库执行一次 `reindex_library_search`

## 推荐安装路径

先在仓库根目录执行：

```bash
pnpm install
pnpm test
pnpm typecheck
pnpm build
```

然后用 AutoClaw 向导完成真实安装：

```bash
pnpm autoclaw:setup -- \
  --agent-api-key YOUR_GLM46_KEY \
  --agent-model glm-4.6 \
  --zhipu-parser-api-key YOUR_PARSER_KEY \
  --zhipu-ocr-api-key YOUR_OCR_KEY \
  --zhipu-vlm-api-key YOUR_GLM46V_KEY \
  --sqlite-path /ABS/PATH/caixu.sqlite
```

如果 AutoClaw profile 不在默认 `~/.openclaw-autoclaw`，加：

```bash
--autoclaw-home /ABS/PATH/.openclaw-autoclaw
```

## 安装后的验活

优先执行：

```bash
pnpm autoclaw:doctor
```

然后至少确认：

```bash
openclaw --profile autoclaw skills check
mcporter list --json
```

如果只是要先确认仓库链路，不急着进 AutoClaw，可先跑：

```bash
pnpm smoke:agent
```

如果要启用可选语义检索增强，再至少补做一次旧库索引回填：

```bash
mcporter call caixu-data-mcp.reindex_library_search \
  --args '{"library_id":"YOUR_LIBRARY_ID"}' \
  --output json
```

然后再用自然语言查询进行验活，例如“找可用于暑期实习申请的证明材料”“查语言证书和成绩单”。

## 首次安装时 agent 的行为约束

- 发现 profile 未 onboard 时，优先提示并引导运行 `openclaw --profile autoclaw onboard`
- 优先使用 `pnpm autoclaw:setup`，不要手写 `mcpServers` 片段
- 缺 key 时，明确报出具体变量名，不要模糊说“少了配置”
- 安装完成前，不要继续路由到 `ingest-materials`、`build-asset-library` 等 phase skill
- 安装完成后，再回到用户原始目标，重新判断应该进入哪个 phase skill

## 首次安装失败时怎么处理

- `openclaw` 不存在：先安装或修正 PATH
- `mcporter` 不存在：先安装或修正 PATH
- `pnpm build` 失败：先修编译问题，不继续向导
- doctor 失败：优先重跑 `pnpm autoclaw:setup`，不要先手工改 JSON
- 只有 `submit-demo` 相关配置缺失：这是高级可选扩展；如果当前不需要提交演示，可先继续个人资产库主线
- 可选语义检索结果异常或不可用：先检查 embedding 环境变量、模型缓存目录与 `reindex_library_search` 是否已经完成
