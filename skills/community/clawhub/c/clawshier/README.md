# Clawshier

OpenClaw skill that processes receipt/invoice photos from any chat channel, extracts expense data, and logs it to a Google Spreadsheet.

![Google Sheets - Summary sheet from Clawshier processing](clawshier_summary.png)

## OCR backends

Clawshier supports OCR via:

- **OpenAI Vision** (default) using `gpt-4o`
- **Ollama** (local) using `llama3.2-vision:latest`

By default, OCR uses OpenAI:

```env
CLAWSHIER_VISION_PROVIDER=openai
```

Set `CLAWSHIER_VISION_PROVIDER=ollama` to use a local Ollama model instead, or `auto` to try Ollama first and fall back to OpenAI.

## Prerequisites

- Node.js 18+
- Google Cloud service account with Sheets API enabled
- OpenAI API key for OCR and structuring
- **Optional:** Ollama running locally with `llama3.2-vision:latest` (if using ollama provider)

## Install

### Option A: via ClawHub

In your OpenClaw chat:

1. Run `/clawhub` to make sure ClawHub is configured
2. Run `/clawhub install clawshier`
3. Ask OpenClaw to verify Clawshier is set up correctly

### Option B: manual clone

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/fdocr/clawshier.git
cd clawshier
npm install
cp .env.example .env  # then fill in your keys
```

## Configuration

Example `.env`:

```env
CLAWSHIER_VISION_PROVIDER=openai
CLAWSHIER_OLLAMA_MODEL=llama3.2-vision:latest
CLAWSHIER_OLLAMA_HOST=http://127.0.0.1:11434
CLAWSHIER_OLLAMA_MAX_DIMENSION=512
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o
GOOGLE_SHEETS_ID=
GOOGLE_SERVICE_ACCOUNT_KEY=path/to/service-account.json
```

Provider modes:

- `openai` — use OpenAI only (default)
- `ollama` — use Ollama only
- `auto` — try Ollama first, fall back to OpenAI

For local Ollama OCR, Clawshier downsizes images on macOS with `sips` before sending them to the model. Use `CLAWSHIER_OLLAMA_MAX_DIMENSION` to tune that behavior.

For debugging, you can ask OpenClaw to process a receipt in `verbose` mode to include the per-step trace in the reply. You can also enable handler-level tracing with `CLAWSHIER_TRACE=1`.

## Safe automation

For automation, prefer the built-in pipeline runner instead of shell-piping untrusted OCR/LLM output between handlers:

```bash
node scripts/run_pipeline.js --image /path/to/receipt.jpg --date 2026-03-25
```

The individual handlers still work for testing, and now also support `--input-file` / `--output-file` for safer composition.

## Google Sheets setup

1. Create a Google Cloud service account and download the JSON key file
   - Go to [Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts) in the Google Cloud Console
   - Click **Create Service Account**, give it a name, and click through to finish
   - On the service account's **Keys** tab, click **Add Key > Create new key > JSON** and save the downloaded file
2. Enable the [Google Sheets API](https://console.cloud.google.com/apis/library/sheets.googleapis.com) in your project
3. Create an empty spreadsheet and share it with the service account email
4. Add the spreadsheet ID and key file path to `.env`
   - Suggestion: Place the JSON file in ~/.openclaw/credentials and use a fully resolved path in the `.env` key instead of the the `~` shortcut

The skill automatically manages all sheet tabs (monthly expense sheets, Invoice Archive Breakdown, and Summary with chart). The default "Sheet1" tab is deleted on first use.

## License

MIT
