---
name: eastmoney-roadshow-transcript-summary
description: EastMoney Roadshow Digest (Transcript + Summary)｜东方财富路演纪要生成. A reliability-first transcript & summary skill for public EastMoney roadshow replays, focused on validated public replay URLs and bounded transcript generation with summary outputs.
---

# EastMoney Roadshow Digest (Transcript + Summary)｜东方财富路演纪要生成

## Purpose | 用途

Create a clean, reliability-first workflow for **public EastMoney roadshow replay pages only**.

仅处理**公开可访问的东方财富路演回放页**，不依赖本地 cookie、私有接口凭据或用户路径，强调执行可控与结果留痕。
本发布包不包含本地 vendor、缓存、输出物或调试残留，目标是可在新环境中按统一入口运行。

## Input | 输入

- `url: string`
- Must match `https://roadshow.eastmoney.com/luyan/<id>`

## Output | 输出

Write these files under `outputs/`:
- `meta.json`
- `transcript.md`
- `clean_transcript.md`
- `summary.md`
- `brief.md`
- `run_report.md`

Page parsing succeeds → always write `meta.json`.
Any downstream failure or downgrade → still write `run_report.md`.

## Workflow | 工作流

1. Validate URL
2. Parse page and fetch public metadata
3. Prefer subtitle candidates if available
4. Discover replay media and run ASR fallback if needed
5. Clean transcript
6. Generate summary
7. Generate executive brief
8. Always write run report

## Role boundaries | 模块边界

- `providers/eastmoney.py`: validate URL, parse page, fetch public metadata, discover subtitle/media candidates only
- `providers/asr.py`: convert audio to text only
- `main.py`: orchestration, file writing, cleaning, summary generation, reporting

## Reliability notes | 可靠性说明

- If subtitle is absent, attempt media+ASR fallback
- If ASR dependencies are missing, degrade gracefully and explain in `run_report.md`
- If page parsing succeeds, still write `meta.json` even when downstream steps fail
- LLM capability is optional environment capability, not a required dependency of the skill package
- When LLM capability exists in the runtime, use it automatically for cleaner transcript / summary / brief generation
- When environment-provided LLM capability is available, transcript text or intermediate cleaned text may be sent to an external model service for processing
- When LLM capability does not exist, fall back automatically to rule-based outputs and explain the path in `run_report.md`
- Do not bind the skill description to any specific LLM vendor or provider
- Keep outputs deterministic and conservative; do not invent facts
- Keep `README.md`, `SKILL.md`, and `manifest.json` aligned on scope, inputs, outputs, and dependency expectations

## Practical guidance | 实操说明

- Use replay metadata from the public detail API
- Preserve source path in `meta.json`
- Prefer concise summaries grounded in extracted text
- If transcript quality is low, say so explicitly in `run_report.md`
- 唯一正确执行方式：`EASTMONEY_ROADSHOW_ENTRY=python3-main python3 main.py --url <roadshow_url>`
- 禁止使用 `uv run`、其他包装器、替代 Python 启动路径或任何未在 README / SKILL 明示的入口
- 调试、验证、重跑必须与正式执行使用同一标准入口；偏离入口的运行结果不得作为 skill 故障判断依据
- LLM 增强按环境中可用的 provider key 自动启用；若无 key，则自动降级到规则版输出

## Entry enforcement | 入口约束

`main.py` contains a startup self-check. If the execution entry does not match the documented standard path, it must fail fast and exit with a clear error instead of continuing in a potentially inconsistent environment.

## Dependencies | 依赖

- Python 3.9+
- `requests` required
- `faster-whisper` required for ASR
- `av` required as a runtime dependency for `faster-whisper`
- `ffmpeg` required on PATH for audio extraction / ASR fallback
- LLM capability is optional if the host runtime provides it; the skill remains usable without it

## Model + keys | 模型与密钥

按环境变量自动检测可用 provider，优先顺序如下：
- OpenAI: `OPENAI_API_KEY`
- Anthropic: `ANTHROPIC_API_KEY`
- Google: `GEMINI_API_KEY`（别名：`GOOGLE_GENERATIVE_AI_API_KEY`, `GOOGLE_API_KEY`）
- xAI: `XAI_API_KEY`
- OpenRouter: `OPENROUTER_API_KEY`
- Moonshot/Kimi: `MOONSHOT_API_KEY`（别名：`KIMI_API_KEY`）

若检测到可用 key，clean transcript / summary / brief 可启用外部模型增强；若未检测到，则自动降级为规则版输出。
- 启用增强时，transcript 或中间清洗文本可能发送至外部模型服务处理。

## Description | 描述

EastMoney Roadshow Digest (Transcript + Summary) is a reliability-first skill for turning public 东方财富路演回放页面 into structured transcript, clean transcript, summary, brief, and run report outputs.

本技能定位为：面向公开东方财富路演回放页的、以稳定性优先的纪要生成工具，可输出 transcript、clean transcript、summary、brief 与 run report。

## Validation standard | 验证标准

- 调试、验证、重跑、正式执行全部使用同一入口：`EASTMONEY_ROADSHOW_ENTRY=python3-main python3 main.py --url <roadshow_url>`
- 对发布包的任何验证结论，必须基于该标准入口；偏离入口的结果无效

## Non-goals | 非目标

- Do not handle private/live-only rooms
- Do not log in
- Do not require browser cookies
- Do not publish automatically
