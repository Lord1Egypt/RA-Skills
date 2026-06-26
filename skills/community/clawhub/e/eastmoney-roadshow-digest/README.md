# EastMoney Roadshow Digest (Transcript + Summary)｜东方财富路演纪要生成

> A reliability-first transcript & summary skill for public EastMoney roadshow replays.

Release package for **public EastMoney roadshow replay pages only**.

EastMoney Roadshow Digest (Transcript + Summary) is a reliability-first skill for turning public 东方财富路演回放页面 into structured transcript, clean transcript, summary, brief, and run report outputs.

本技能定位为：面向公开东方财富路演回放页的、以稳定性优先的纪要生成工具，可输出 transcript、clean transcript、summary、brief 与 run report。

## Scope
- Supports only public URLs like `https://roadshow.eastmoney.com/luyan/5149204`
- Validates URL before parsing
- Prefers subtitle discovery first
- Falls back to public replay media discovery + ASR
- Always writes `outputs/run_report.md`
- Writes `outputs/meta.json` whenever page parsing succeeds
- Does **not** require cookies, private credentials, or user-specific paths

## Outputs
- `outputs/meta.json`
- `outputs/transcript.md`
- `outputs/clean_transcript.md`
- `outputs/summary.md`
- `outputs/brief.md`
- `outputs/run_report.md`

## Files
- `SKILL.md` — bilingual skill instructions
- `manifest.json` — project manifest
- `main.py` — orchestration pipeline
- `providers/eastmoney.py` — URL validation, page parsing, subtitle/media discovery only
- `providers/asr.py` — audio extraction + speech-to-text only
- `outputs/` — runtime outputs (generated at runtime, not shipped in the release package)

## Dependencies
Python dependencies are declared in `requirements.txt`.

Runtime notes:
- `requests` is required
- `faster-whisper` is required for ASR
- `av` is required as a transitive runtime dependency for `faster-whisper`
- `ffmpeg` must be available on PATH for audio extraction / ASR fallback
- LLM capability is optional environment capability, not a required skill dependency

## Model + keys
Set the API key for a supported provider in the host environment. The skill will auto-detect the first available provider in this priority order:
- OpenAI: `OPENAI_API_KEY`
- Anthropic: `ANTHROPIC_API_KEY`
- Google: `GEMINI_API_KEY` (aliases: `GOOGLE_GENERATIVE_AI_API_KEY`, `GOOGLE_API_KEY`)
- xAI: `XAI_API_KEY`
- OpenRouter: `OPENROUTER_API_KEY`
- Moonshot/Kimi: `MOONSHOT_API_KEY` (alias: `KIMI_API_KEY`)

If no provider key is configured, the skill remains usable and automatically falls back to non-LLM rule-based outputs.

Install Python dependencies:
```bash
python3 -m pip install -r requirements.txt
```

Recommended explicit ASR dependency set for fresh environments:
```bash
python3 -m pip install requests>=2.31.0 faster-whisper>=1.1.0 av>=12.0.0
```

Install ffmpeg separately (examples):
- macOS: `brew install ffmpeg`
- Ubuntu/Debian: `sudo apt-get install ffmpeg`

## Run

### 唯一正确执行方式 / The only correct execution entry

This skill must be launched only through the documented standard entry below. Do **not** use `uv run`, alternate wrappers, or other Python launch paths.

```bash
EASTMONEY_ROADSHOW_ENTRY=python3-main python3 main.py --url https://roadshow.eastmoney.com/luyan/5149204
```

If the required entry marker is missing or the launcher deviates from this standard path, `main.py` will exit immediately with an error instead of running in a degraded or ambiguous environment.

## Notes
- If subtitle content is not publicly exposed, the workflow degrades to media discovery + ASR.
- If ASR dependencies are unavailable, the workflow still completes and explains the downgrade in `outputs/run_report.md`.
- If the runtime environment provides LLM capability, it is used automatically for higher-quality clean transcript / summary / brief generation.
- When LLM enhancement is enabled, transcript text or intermediate cleaned text may be sent to an external model provider for processing.
- If the runtime environment does not provide LLM capability, the skill automatically falls back to rule-based outputs and records the downgrade path in `outputs/run_report.md`.
- The skill does not require any specific LLM provider and does not bind to any single vendor.
- The skill is scoped to currently validated public replay pages and does not claim support for private rooms, logged-in experiences, or arbitrary video sources.
- 调试、验证、重跑一律使用同一标准入口：`EASTMONEY_ROADSHOW_ENTRY=python3-main python3 main.py --url ...`。
- 任何偏离该入口的调用都应视为无效执行，不得据此判断 skill 主链路是否异常。

## Changelog
### v0.1.0-release-candidate
- Reduced package contents to publish-safe runtime files only
- Aligned README / SKILL / manifest on a single standard execution entry
- Declared ASR runtime dependencies explicitly: faster-whisper / av / ffmpeg
- Added entry-guard expectations for consistent execution and validation
