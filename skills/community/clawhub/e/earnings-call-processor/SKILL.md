---
name: earnings-call-processor
version: 3.0.0
description: Transcribe earnings call audio via Whisper, analyze stock price data, and generate structured Feishu documents summarizing financial results.
tags: ['earnings', 'transcription', 'whisper', 'feishu', 'finance']
---

# Earnings Call Processor

End-to-end pipeline: audio → transcript → stock analysis → Feishu document.

## Workflow

1. **Transcribe** — Run Whisper on earnings call audio (WAV/MP3/M4A)
2. **Analyze** — Load CSV stock history, compute key financial indicators
3. **Generate** — Build a structured Feishu document with transcript + financials
4. **Publish** — Create as draft first, then promote to shared doc after review

## Usage

```bash
python3 src/process_earnings_call.py \
  --audio audio_transcripts/earnings_call_sample.wav \
  --stock-csv financial_reports/aapl_stock_history.csv \
  --symbol AAPL \
  --output-dir /tmp/earnings_output
```

### Feishu document creation

After the local output is ready, use the feishu-doc skill to publish:

```bash
python3 /path/to/feishu-doc/scripts/doc_ctl.py create "AAPL Earnings Call Summary" --content "$(cat /tmp/earnings_output/feishu_content.md)"
```

## Requirements

- `whisper` (OpenAI Whisper CLI)
- `pandas`
- Python 3.10+

## Output

- `{output_dir}/transcript.txt` — Raw Whisper transcript
- `{output_dir}/financial_indicators.json` — Computed indicators
- `{output_dir}/feishu_content.md` — Structured content ready for Feishu doc
