---
name: data-synthesis
description: >-
  从 CSV 语料切块后，用同一套 LLM 接口依次生成问题与答案，输出 JSONL 训练数据。
  适用于文档/表格语料合成 QA、微调数据准备；支持 OpenAI 兼容网关与内网 Qwen 等服务。
---

# Data Synthesis

## 流程概览

**CSV 语料 → 按字符切块 → 每块生成问题列表 → 对每个问题基于该块生成答案 → 写出 JSONL。**  
不包含单独的小模型质量过滤环节。

| 阶段 | 说明 |
|------|------|
| 输入 | 带表头的 CSV，需有一列长文本可供切块 |
| 切块与遍历 | `scripts/synthesize_qa.py` |
| 问题生成 | 每个文本块调用一次 LLM |
| 答案生成 | 每个「块 + 问题」调用一次 LLM |
| 输出 | 每行一条 JSON（JSONL） |

## Agent 建议执行顺序

1. **准备**：运行 `scripts/parse_file.py`，确认列名、行数、文本列与内容预览。
2. **合成**：运行 `scripts/synthesize_qa.py`，得到 JSONL。
3. **模式**：未开启 API 时为 **dry-run**（不联网）；设置 `DATA_SYNTHESIS_USE_API=1` 后走真实推理。若网关需要鉴权，再配置 `OPENAI_API_KEY`。

## 脚本与依赖

| 脚本 | 作用 |
|------|------|
| `scripts/parse_file.py` | 校验 CSV，输出列名、行数、`detected_text_column`、文本预览 |
| `scripts/synthesize_qa.py` | 完整 QA 流水线；默认输出 `<输入文件名_stem>_qa.jsonl`，可用 `-o` 指定路径 |

仅依赖 Python 标准库。API 模式通过 `urllib` 调用 **OpenAI 兼容**的 `POST .../v1/chat/completions`（`OPENAI_BASE_URL` 可写成根路径 `.../v1`，也可写成完整 URL 直至 `.../chat/completions`）。

## 命令示例

```bash
# 1. 检查语料
python scripts/parse_file.py path/to/corpus.csv

# 2. 本地 dry-run（不写密钥、不调外网）
python scripts/synthesize_qa.py path/to/corpus.csv -o path/to/out.jsonl
```

**内网 Qwen 示例（与环境变量一致，推荐）：**

```bash
export DATA_SYNTHESIS_USE_API=1
export OPENAI_BASE_URL='http://xxx'
export DATA_SYNTHESIS_MODEL='xxx'
export DATA_SYNTHESIS_MAX_TOKENS=2000
export DATA_SYNTHESIS_TEMPERATURE=0.7

python scripts/synthesize_qa.py path/to/corpus.csv \
  --text-column text \
  --chunk-size 6000 \
  --chunk-overlap 200 \
  --sleep 0.3 \
  -o path/to/out.jsonl
```

**仅用命令行指定模型（与上面环境变量二选一即可）：**

```bash
python scripts/synthesize_qa.py path/to/corpus.csv \
  --text-column text \
  --model xxx \
  -o path/to/out.jsonl
```

常用参数：`--max-rows` 试跑前几行；`--sleep` 控制请求间隔。勿在已设置 `DATA_SYNTHESIS_MODEL` 时再传冲突的 `--model`。

## 输入格式

- CSV 第一行为表头。
- 文本列自动匹配：`text`、`content`、`body`、`正文`、`文本`；否则使用**第一列**。
- 手动指定：`--text-column 列名`。

## 输出格式

- **JSONL**：每行一个对象，主要字段包括 `chunk_id`、`row_index`、`chunk`、`question`、`answer`，以及 `source_fields`（除主文本列外、值非空的其它列）。
- 运行结束会在标准输出打印统计 JSON：`rows`、`chunks`、`questions_generated`、`qa_pairs_written`、`errors`。

## 能力与局限

**能力：** 适合从表格语料批量得到结构化 QA，便于后续清洗与训练；出题与作答共用同一模型与网关配置。

**局限：** 切块为**字符滑动窗口**，不是按段落语义切分；问题列表依赖模型返回可解析的 JSON，失败会记入 `errors`。
