# 01 生成搜索查询

## 脚本

```bash
python3 scripts/build_queries.py --date {date} --window 3
```

## 作用

从 `config/profile.yaml` 读取用户画像（topics + keywords），自动生成两类搜索查询：

- **platform 查询**（纯关键词）：给 opencli 平台原生搜索用（微博/小红书/B站/Twitter/Reddit 等）
- **google 查询**（带 `after:YYYY-MM-DD`）：给 `opencli google search` 用

## 输入

- `config/profile.yaml` — 用户画像，关键词在 `topics[*].keywords.cn` 和 `topics[*].keywords.en`

## 输出

- `output/raw/{date}_queries.txt` — 自动保存（`--no-save` 可关闭）
- 同时输出到 stdout

## 输出格式

```
# 日报搜索查询（platform）— 2026-04-06（窗口 3 天）
# 共 90 条查询

## [high-cn] 大模型与模型能力演进
  大模型
  基础模型
  多模态模型
  大模型 基础模型

## [high-en] 大模型与模型能力演进
  large language model
  foundation model
  multimodal model

============================================================

# 日报搜索查询（google）— 2026-04-06（窗口 3 天）

## [high] 大模型与模型能力演进
  大模型与模型能力演进 after:2026-04-04
  large language model foundation model multimodal model after:2026-04-04
```

## 关键逻辑

1. 关键词按 cn/en 分组（支持新格式 `{cn: [], en: []}` 和旧格式扁平列表）
2. platform 查询不带日期，依靠平台自身排序 + 后续 filter_index.py 筛选
3. google 查询统一用 `after:YYYY-MM-DD`（不用中文日期，避免污染搜索词）
4. 按 priority 控制数量：high 全部关键词，medium 前 3 个，low 前 1 个
5. high topic 额外生成组合查询（如 `大模型 基础模型`、`OpenAI Anthropic`）

## 参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--date` | 今天 | 目标日期 YYYY-MM-DD |
| `--window` | 3 | 时间窗口天数 |
| `--type` | all | `all`/`platform`/`google` |
| `--json` | false | JSON 格式输出 |
| `--no-save` | false | 不保存到文件 |
