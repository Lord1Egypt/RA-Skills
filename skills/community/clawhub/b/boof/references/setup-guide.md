# Boof — Setup Guide

## Prerequisites

- **macOS** (Apple Silicon or Intel) or Linux
- **Python 3.10+** (3.11–3.13 recommended)
- **Java 11+** (required by opendataloader-pdf)
- **bun** (for QMD installation) — install from https://bun.sh

## Step 1: Install Java 11+

opendataloader-pdf uses a Java-based PDF engine under the hood. No GPU required.

```bash
# macOS via Homebrew (keg-only, doesn't conflict with system Java)
brew install openjdk

# Add to PATH (add this to ~/.zshrc or ~/.bash_profile)
export PATH="/opt/homebrew/opt/openjdk/bin:$PATH"

# Verify
java -version
# Should show: openjdk version "25.x.x" or similar
```

**Alternative:** Install from [Adoptium](https://adoptium.net/) if you prefer a GUI installer.

## Step 2: Install opendataloader-pdf

opendataloader-pdf runs fully locally. No API keys, no cloud, no GPU. Processes 100+ pages/sec in fast mode.

```bash
# Create isolated Python venv
python3 -m venv ~/.openclaw/tools/odl-env

# Install opendataloader-pdf
~/.openclaw/tools/odl-env/bin/pip install -U opendataloader-pdf

# Verify
~/.openclaw/tools/odl-env/bin/python3 -c "import opendataloader_pdf; print('OK')"
```

**Note:** No model downloads needed for standard mode — conversion is deterministic and rule-based.

## Step 3: Install QMD (Local RAG indexing + retrieval)

QMD provides local semantic search over markdown files using local GGUF models — no API keys, no cloud.

```bash
# Install via bun (NOT npm — the npm package is a placeholder)
bun install -g https://github.com/tobi/qmd

# Verify
~/.bun/bin/qmd status
```

**First run:** QMD downloads embedding and reranker models (~1–2GB total) on first query. One-time cost.

### Configure QMD for OpenClaw

If using with OpenClaw's memory system, set the QMD path in `~/.openclaw/openclaw.json`:

```json5
{
  memory: {
    backend: "qmd",
    qmd: {
      command: "~/.bun/bin/qmd",
      limits: {
        timeoutMs: 30000
      }
    }
  }
}
```

## Step 4: Install the Boof Skill

### For OpenClaw users:

```bash
clawhub install boof
```

### Standalone usage:

```bash
export ODL_ENV=~/.openclaw/tools/odl-env
export QMD_BIN=~/.bun/bin/qmd

./scripts/boof.sh /path/to/document.pdf
```

## Verify Everything Works

```bash
# Test with any PDF
bash ~/.openclaw/workspace/skills/boof/scripts/boof.sh ~/Downloads/some-paper.pdf

# Query the indexed content
~/.bun/bin/qmd query "what is the main finding?" -c some-paper
```

## Hybrid Mode (Complex Tables / Scanned PDFs / OCR)

For PDFs with complex borderless tables, scanned pages, or multi-language OCR, enable hybrid mode:

```bash
# Install hybrid extras
~/.openclaw/tools/odl-env/bin/pip install "opendataloader-pdf[hybrid]"

# Start the hybrid backend (in a separate terminal or background)
~/.openclaw/tools/odl-env/bin/opendataloader-pdf-hybrid --port 5002

# Use boof.sh with hybrid flag (set env var)
ODL_HYBRID=true bash boof.sh /path/to/complex.pdf
```

Hybrid mode accuracy: **0.90 overall, 0.93 table accuracy** vs. 0.72 in fast mode.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `java: command not found` | Run `export PATH="/opt/homebrew/opt/openjdk/bin:$PATH"` or install from Adoptium |
| `import opendataloader_pdf` fails | Reinstall: `~/.openclaw/tools/odl-env/bin/pip install -U opendataloader-pdf` |
| Output markdown is empty | Check Java version (`java -version` must be 11+) |
| `qmd: command not found` | Use full path: `~/.bun/bin/qmd`, or add `~/.bun/bin` to PATH |
| QMD queries timeout | Set `timeoutMs: 30000` — first run downloads models |
| `npm install -g qmd` installs wrong package | Must use: `bun install -g https://github.com/tobi/qmd` |

## Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| RAM | 4GB | 8GB+ |
| Disk | 2GB (QMD models only) | 5GB+ |
| CPU | Any (ARM or x86) | Any — no GPU needed |
| GPU | Not required | Not required |

**vs. previous Marker-based backend:** Marker required a GPU for best results and downloaded ~2GB of ML models. opendataloader-pdf is purely CPU-based, starts instantly, and produces cleaner structured output (proper Markdown tables vs. flat text).
