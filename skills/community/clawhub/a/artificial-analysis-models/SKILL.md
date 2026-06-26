---
name: artificial-analysis-models
description: "Fetch LLM benchmarks and pricing from Artificial Analysis API and sync to a Feishu Bitable table. Use when updating model specs, prices, benchmark scores, or building a model catalog in Feishu."
---

# Artificial Analysis 模型信息 → 飞书表格

从 [Artificial Analysis 免费 API](https://artificialanalysis.ai/api-reference) 拉取 LLM **价格、速度、评测分数**，整理到**飞书多维表格**，便于销售/售前查阅。

## 前置：API Key

1. 在 [Artificial Analysis Insights Platform](https://artificialanalysis.ai/) 注册并生成 API Key  
2. 任选一种配置方式：

```bash
# 方式 A：环境变量
export ARTIFICIAL_ANALYSIS_API_KEY="你的key"

# 方式 B：凭证文件（推荐）
mkdir -p ~/.openclaw/credentials
cat > ~/.openclaw/credentials/artificial-analysis.json <<'EOF'
{"api_key": "你的key"}
EOF
chmod 600 ~/.openclaw/credentials/artificial-analysis.json
```

免费 API 限额：**1000 次/天**；请缓存结果，不要每次对话都重复全量拉取。

## 工作流（在飞书调用本 skill 时执行）

### 1. 拉取 API 数据

```bash
node {SKILL_DIR}/scripts/fetch-llms.mjs
```

产出：`~/.openclaw/cache/artificial-analysis/llms-latest.json`

### 2. 生成多维表格记录

```bash
node {SKILL_DIR}/scripts/build-bitable-records.mjs
```

产出：

- `bitable-records.json` — `batch_create` / `batch_update` 用的 `records[]`
- `bitable-field-defs.json` — 建表字段定义

`{SKILL_DIR}` = 本 skill 目录。

### 3. 飞书多维表格（核心交付）

**不要**把 JSON 文件路径发给用户；交付物是**可打开的多维表格链接** + 简短说明。

#### 3.1 首次：创建表格

若无现成表格，复制 `bitable-config.example.json` 为 `bitable-config.json` 并留空 token，由 Agent 创建后写回。

1. `feishu_bitable_app.create`  
   - `name`: `AI 模型信息库（Artificial Analysis）`  
   - 可选 `folder_token`（用户指定文件夹时）

2. `feishu_bitable_app_table.create`  
   - `app_token`: 上一步返回  
   - `name`: `LLM 模型一览`  
   - `fields`: 读取 `bitable-field-defs.json`（类型见 [references/bitable-setup.md](references/bitable-setup.md)）

3. `feishu_bitable_app_table_record.list` — 若存在空行则 `batch_delete` 删掉默认空记录

4. `feishu_bitable_app_table_record.batch_create`  
   - `records`: 从 `bitable-records.json` 读取，**每批 ≤500 条**，多批串行并间隔 0.5–1 秒

5. 将 `app_token`、`table_id` 写入 `{SKILL_DIR}/bitable-config.json` 供下次更新

6. 给用户发多维表格链接（从 `feishu_bitable_app` 返回的 URL 或说明如何在工作台打开该 Base）

#### 3.2 后续：更新表格

若 `{SKILL_DIR}/bitable-config.json` 已有 `app_token` + `table_id`：

1. `feishu_bitable_app_table_record.list` 拉取现有记录（分页），建立 `模型ID → record_id` 映射  
2. 对比 `bitable-records.json`：  
   - 新 ID → 加入 `batch_create` 批次  
   - 已有 ID → 加入 `batch_update` 批次（带 `record_id`）  
3. 串行执行批量写入（遵守 500 条/批、勿并发写同一表）

### 4. 飞书私聊摘要（给销售同学）

发送示例（**无本地路径**）：

```text
已更新 AI 模型信息表（数据来源 Artificial Analysis，{N} 个模型）

要点：
• 智能指数最高：{模型名}（{分数}）
• 综合价格最低（Top3 中）：{模型名}（${价格}/1M tokens）
• 编程指数最高：{模型名}

📎 多维表格：{表格链接或打开方式}
数据说明：https://artificialanalysis.ai/
```

可根据 `llms-latest.json` 中 `intelligence_index`、`price_blended_3_1`、`coding_index` 排序生成 3–5 条要点。

## API 字段说明（LLM 端点）

| API 字段 | 表格列 |
| --- | --- |
| `evaluations.artificial_analysis_intelligence_index` | 智能指数 |
| `evaluations.artificial_analysis_coding_index` | 编程指数 |
| `evaluations.artificial_analysis_math_index` | 数学指数 |
| `evaluations.mmlu_pro` 等 | 转为 % 显示 |
| `pricing.price_1m_*` | 价格列（USD / 1M tokens） |
| `median_output_tokens_per_second` | 输出速度 |
| `id` | 模型ID（更新主键） |

完整 API 文档：[API Reference](https://artificialanalysis.ai/api-reference)

## 依赖工具

- `feishu_bitable_app` / `feishu_bitable_app_table` / `feishu_bitable_app_table_field` / `feishu_bitable_app_table_record`  
- 详见 skill `feishu-bitable`

## 禁止

- 不要把 `llms-latest.json`、`bitable-records.json` 路径当最终交付发给销售用户  
- 不要在没有 API Key 时假装拉取成功  
- 不要突破 1000 次/日限额频繁全量请求（应复用 `llms-latest.json` 除非用户明确要求刷新）

## 扩展（可选）

用户若需要 Text-to-Image / Video 等，可另调：

- `GET /api/v2/data/media/text-to-image`（`include_categories=true`）  
- 需单独建表；本 skill 默认仅 **LLM 文本模型** 端点。
