> 📢 News  
Laiye ADP Global Invoice Extraction · Free for Limited Time，Spots are limited, available on a first-come, first-served basis. [Learn more about: ADP Global Invoice Extraction Free Skill](../adp-global-invoice-extraction-free/SKILL.md)
---

# 🚀 Laiye ADP Global Document Intelligent Extraction · Fast
Developed by the ADP Intelligent Document Processing team of Laiye Technology. Tailored for **global cross-border finance, automation, system integration and high-concurrency production scenarios**, it delivers low-latency, high-throughput, full-format and multi-language intelligent extraction for invoices, bills and receipts. It fully supports structured standard documents, unstructured overseas purchase invoices and receipts. Whether it is electronic PDFs, scanned copies or images, **each page can be parsed and output as standardized JSON structured data in as fast as 5 seconds**. It supports enterprise-level batch processing and 7×24 stable service, empowering end-to-end workflow automation, intelligent reconciliation and data warehousing.

## ⭐ Core Advantages of High-Speed Edition

⚡ Ultra-fast Processing: Each page is parsed within 5 seconds. It supports large-scale concurrent calls to meet high-intensity processing requirements in production environments.  
✅ Enterprise-grade High-throughput Architecture: Low-latency response and stable processing for massive files.  
🌐 Multi-language Support: Recognizes invoices and receipts in English, Japanese, Korean, German, French, Thai and hundreds of other languages.  
📄 Full-format Compatibility: Adapts to VAT invoices worldwide, tax documents from Southeast Asia, unstructured receipts and mixed-format vouchers.  
🎯 Over 99% Extraction Accuracy: Accurately extracts key fields and greatly reduces costs for manual verification, translation and data entry.  
🤖 Continuous AI Optimization: The model keeps iterating and improving based on business data, and supports customized adaptation for enterprises.  

## 📌 Application Scenarios
| User Group | Usage Scenarios |
| ---- | ---- |
| Enterprise Finance & Shared Service Center | Batch processing of multi-language documents for automated bookkeeping, settlement and reconciliation. |
| System Integrators | API integration with up to 10 concurrent requests and low latency, complying with production-level SLA requirements. |
| Developers & Technical Teams | Integrate high-performance ADP API to build stable and efficient automated document processing workflows. |


## Install

```bash
# npm (recommended)
npm install -g @laiye-adp/agentic-doc-parse-and-extract-cli

# Linux / macOS
curl -fsSL https://raw.githubusercontent.com/laiye-ai/adp-cli/main/scripts/adp-init.sh | bash

# Windows (PowerShell)
irm https://raw.githubusercontent.com/laiye-ai/adp-cli/main/scripts/adp-init.ps1 | iex
```

Or download a prebuilt binary from [GitHub Releases](https://github.com/laiye-ai/adp-cli/releases).

## Configure

Get an API key at [https://adp-global.laiye.com/](https://adp-global.laiye.com/?utm_source=clawhub) (new users get 100 free credits per month).

```bash
adp config set --api-key <your-api-key>
adp config set --api-base-url https://adp-global.laiye.com
adp config get
```

## Quick Examples

```bash
# List available apps
adp app-id list

# Parse a local document
adp parse local ./invoice.pdf --app-id <app-id>

# Extract key fields
adp extract local ./invoice.pdf --app-id <app-id>

# Parse a directory in async mode
adp parse local ./documents/ --app-id <app-id> --async

# Process a remote URL
adp extract url https://example.com/file.pdf --app-id <app-id>

# Query an async task
adp parse query <task-id>

# Two-phase async (submit + query separately, resumable)
adp extract local ./documents/ --app-id <app-id> --async --no-wait --export tasks.json
adp extract query --watch --file tasks.json

# Auto retry on failure (up to 2 retries)
adp parse local ./documents/ --app-id <app-id> --retry 2

# Check remaining credits
adp credit
```

## Commands

> AI agents should call `adp schema` for the machine-readable, authoritative command spec. The table below is a human-friendly summary.

| Command | Description |
|---|---|
| `adp version` | Print version |
| `adp config set` | Set API key / base URL |
| `adp config get` | Show current config |
| `adp config clear` | Clear config |
| `adp app-id list` | List available apps |
| `adp app-id cache` | Read app list from local cache |
| `adp parse local <path>` | Parse local file/directory |
| `adp parse url <url>` | Parse remote file (URL list file supported) |
| `adp parse base64 <data>` | Parse Base64-encoded content |
| `adp parse query <task-id...>` | Query async parse tasks (supports multiple IDs or `--file`) |
| `adp extract local <path>` | Extract from local file/directory |
| `adp extract url <url>` | Extract from remote file |
| `adp extract base64 <data>` | Extract from Base64-encoded content |
| `adp extract query <task-id...>` | Query async extract tasks (supports multiple IDs or `--file`) |
| `adp custom-app create` | Create a custom extraction app |
| `adp custom-app update` | Update custom app config |
| `adp custom-app get-config` | Show app config |
| `adp custom-app delete` | Delete a custom app |
| `adp custom-app delete-version` | Delete a specific config version |
| `adp custom-app ai-generate` | AI-recommend extraction fields |
| `adp credit` | Show remaining credits |
| `adp schema` | Output command schema (for AI agents) |

## Flags

| Flag | Description |
|---|---|
| `--json` | Output JSON |
| `--quiet` | Quiet mode, output result only |
| `--lang <en\|zh>` | Interface language |
| `--app-id` | App ID (required for parse / extract) |
| `--async` | Async mode |
| `--no-wait` | Submit tasks only, do not wait for results (use with `--async`) |
| `--export <path>` | Export result to file (single file) or directory (batch) |
| `--timeout <seconds>` | Timeout (default 900s) |
| `--concurrency <n>` | Concurrent workers (free: max 1, paid: max 2) |
| `--retry <n>` | Retries for retryable errors (default 0) |
| `--file <path>` | Read task IDs from JSON file (output of `--no-wait`, query only) |

## Async Workflow

For large files or batch jobs, submit with `--async` and the CLI returns a `task-id`. Poll for results with `parse query` / `extract query`:

```bash
adp parse local ./big.pdf --app-id <app-id> --async
# returns a task-id

adp parse query <task-id>
```

### Two-Phase Async (`--no-wait`)

By default, `--async` submits and polls until completion — ideal for AI agents. For resumable workflows, use two-phase mode:

**Phase 1: Submit tasks**

```bash
adp extract local ./documents/ --app-id <app-id> --async --no-wait --export tasks.json
```

Output is a JSON array with task IDs:

```json
[
  {"path": "invoice.pdf", "task_id": "task_abc123"},
  {"path": "contract.pdf", "task_id": "task_def456"}
]
```

**Phase 2: Query results**

```bash
adp extract query --watch --file tasks.json
adp extract query --watch --file tasks.json --export ./results/
```

Even if the CLI crashes mid-way, task IDs in `tasks.json` are preserved — resume anytime with `query --file`.

## Batch Processing

When processing multiple files/URLs, the CLI writes each result to a separate file:

```
adp_results_20250417_153020/
├── _summary.json              # Summary (total, success, failed, per-file status)
├── invoice_01.pdf.json        # Successful result
├── contract_02.docx.json
└── report_03.pdf.error.json   # Error details
```

- `--export <dir>` — specify output directory
- Without `--export` — auto-creates `adp_results_<timestamp>/`
- Single file — outputs to stdout or the `--export` file path

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | All success |
| `1` | All failed / system error |
| `2` | Parameter error |
| `3` | Resource not found |
| `4` | Permission denied |
| `5` | Conflict |
| `6` | Partial failure (some tasks failed in batch) |

## Environment Variables

| Variable | Description |
|---|---|
| `ADP_API_KEY` | API key (overrides config file) |
| `ADP_API_BASE_URL` | Service URL |
| `ADP_LANG` | Interface language (`en` / `zh`) |
| `ADP_LOG_LEVEL` | Log level (`debug` / `info` / `warn` / `error`) |

## Config Storage

- Config dir: `~/.adp/`
- Config file: `~/.adp/config.json`
- Encrypted API key: `~/.adp/key.enc` (AES-256-GCM)
- App cache: `~/.adp/app_cache.json`
- Version check cache: `~/.adp/version_check.json` (refreshed every 24h)

## 📜 License

We adopt a combined model of open-source tools + paid services: the CLI tool is completely free and open-source, making it easy for everyone to quickly integrate; while the core ADP intelligent parsing capability is a Public Cloud commercial service, billed based on actual usage, aiming to provide users with a highly accurate and stable document processing experience.

- **CLI Tool**: Open source under the MIT License, freely available for use, modification, and distribution
- **ADP Service**: AI document processing service based on Public Cloud, billed by usage, Billing Rules

Free Quota: New users can receive **100 free credits** per month after registration, allowing them to experience full functionality

## 🛠️ Support & Contact
- **CLI User Guide:** [ADP CLI User Guide](https://laiye-tech.feishu.cn/wiki/YIaawiK2DimisZk5KfDc8a8cnLh)
- **API Documentation:** [Open API User Guide](https://laiye-tech.feishu.cn/wiki/S1t2wYR04ivndKkMDxxcp2SFnKd)
- **ADP Product Manual:** [Public Cloud Manual](https://laiye-tech.feishu.cn/wiki/OfexwgVUQiOpEek4kO7c7NEJnAe)
- **Issue Tracker:** [GitHub Issues](https://github.com/Laiye-ADP/adp-skills/issues)
- **Email:** global_product@laiye.com
- **Website:** [Laiye ADP](https://laiye.com/en/product/adp-platform)
