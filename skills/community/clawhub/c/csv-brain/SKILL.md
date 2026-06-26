---
name: "CSVBrain Natural Language Data Queries"
description: "Load CSV files and ask questions in plain English. AI-powered natural language queries via Anthropic, OpenAI, or local Ollama. No SQL required."
author: "@TheShadowRose"
version: "1.0.3"
tags: ["csv", "data-analysis", "natural-language", "ai", "query"]
license: "MIT"
env:
  ANTHROPIC_API_KEY: "Optional - for Anthropic/Claude models"
  OPENAI_API_KEY: "Optional - for OpenAI/GPT models"
  OLLAMA_HOST: "Optional - Ollama base URL, default http://localhost:11434"
---

# CSVBrain

**Version:** 1.0.3
**Author:** @TheShadowRose
**License:** MIT

## Description

Load CSV files and ask questions in plain English. AI-powered natural language queries via Anthropic, OpenAI, or local Ollama. No SQL required.

CSVBrain parses CSV files (comma, semicolon, or tab-delimited), profiles your data automatically, and lets you query it with structured filters or plain English questions powered by AI.

## Features

- **CSV Loading** — Parse CSV files with automatic delimiter detection (comma, semicolon, tab). Handles quoted fields and escaped quotes.
- **Data Profiling** — Instant statistics for every column: count, missing values, unique values, min/max/avg for numeric columns.
- **Structured Queries** — Filter, sort, limit, and aggregate your data programmatically.
- **Natural Language Ask** — Ask questions about your data in plain English. AI analyzes your dataset's structure, types, and statistics to give accurate answers with specific numbers.
- **Multi-Provider AI** — Route questions to Anthropic (Claude), OpenAI (GPT), or local Ollama models. Just change the model prefix.
- **Zero Dependencies** — Pure Node.js. No npm packages required. HTTP calls use built-in `https`/`http` modules.

## Installation

Copy `src/csv-brain.js` into your project.

```js
const { CSVBrain } = require('./src/csv-brain');
```

## Quick Start

```js
const { CSVBrain } = require('./src/csv-brain');

const brain = new CSVBrain();
const info = brain.load('sales.csv');
console.log(info);
// { rows: 1200, columns: 8, types: { month: 'text', revenue: 'number', ... } }

// Profile your data
const stats = brain.profile();
console.log(stats.revenue);
// { type: 'number', count: 1200, missing: 0, unique: 987, min: 12.5, max: 94200, avg: 8450.32 }

// Ask a question in plain English
const result = await brain.ask('What was our best month for revenue?');
console.log(result.answer);
// "Based on the data, March had the highest total revenue at $94,200."
console.log(result.model);
// "anthropic/claude-haiku-4-5"
```

## API

### `new CSVBrain(options?)`

Create a new instance.

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `model` | `string` | `"anthropic/claude-haiku-4-5"` | Default AI model for `ask()` |

```js
const brain = new CSVBrain({ model: 'openai/gpt-4o-mini' });
```

### `load(filePath, options?)`

Load a CSV file synchronously.

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `delimiter` | `string` | auto-detect | Force a specific delimiter |

**Returns:** `{ rows: number, columns: number, types: object }`

```js
const info = brain.load('data.csv');
const info2 = brain.load('data.tsv', { delimiter: '\t' });
```

### `profile()`

Get statistical profile of all columns.

**Returns:** Object keyed by column name, each with `type`, `count`, `missing`, `unique`, and (for numeric columns) `min`, `max`, `avg`.

```js
const stats = brain.profile();
console.log(stats);
```

### `query(options)`

Run a structured query against loaded data.

| Option | Type | Description |
|--------|------|-------------|
| `filter` | `{ column, operator, value }` | Filter rows. Operators: `>`, `<`, `>=`, `<=`, `=`, `contains` |
| `sort` | `{ column, order }` | Sort by column. Order: `"asc"` or `"desc"` |
| `limit` | `number` | Maximum rows to return |
| `aggregate` | `{ column }` | Return `count`, `sum`, `avg`, `min`, `max` for a numeric column |

```js
// Filter and sort
const topSales = brain.query({
  filter: { column: 'revenue', operator: '>', value: 10000 },
  sort: { column: 'revenue', order: 'desc' },
  limit: 10
});

// Aggregate
const totals = brain.query({
  aggregate: { column: 'revenue' }
});
console.log(totals);
// { count: 1200, sum: 10140384, avg: 8450.32, min: 12.5, max: 94200 }
```

### `async ask(question, options?)`

Ask a natural language question about your data. Requires an AI provider API key (or local Ollama).

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `model` | `string` | Instance default | AI model with provider prefix |
| `apiKey` | `string` | From environment | Override the API key |
| `ollamaHost` | `string` | `"http://localhost:11434"` | Ollama server URL |

**Returns:** `{ answer: string, data: any, query: object|null, model: string }`

```js
// Using Anthropic (default)
// Requires ANTHROPIC_API_KEY environment variable
const result = await brain.ask('Which product category has the highest average price?');
console.log(result.answer);
// "Electronics has the highest average price at $342.50, followed by Appliances at $289.00."

// Using OpenAI
// Requires OPENAI_API_KEY environment variable
const result2 = await brain.ask('How many orders were placed in Q4?', {
  model: 'openai/gpt-4o-mini'
});

// Using local Ollama (no API key needed)
const result3 = await brain.ask('Summarize the sales trends', {
  model: 'ollama/llama3'
});
```

## AI Provider Setup

### Anthropic (Claude)

Set your API key as an environment variable:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

Models: `anthropic/claude-haiku-4-5`, `anthropic/claude-sonnet-4-20250514`, etc.

### OpenAI (GPT)

```bash
export OPENAI_API_KEY="sk-..."
```

Models: `openai/gpt-4o-mini`, `openai/gpt-4o`, etc.

### Ollama (Local)

No API key required. Just run Ollama locally:

```bash
ollama serve
ollama pull llama3
```

Models: `ollama/llama3`, `ollama/mistral`, etc.

Optionally set a custom host:

```bash
export OLLAMA_HOST="http://192.168.1.100:11434"
```

## Error Handling

If the AI provider is unavailable, `ask()` returns a graceful error instead of throwing:

```js
const result = await brain.ask('What is the trend?');
if (result.answer.startsWith('AI unavailable:')) {
  console.log('Falling back to manual query...');
  const data = brain.query({ sort: { column: 'date', order: 'asc' } });
}
```

## Supported File Formats

- **CSV** — Comma-separated values (`.csv`)
- **TSV** — Tab-separated values (`.tsv`, `.txt`)
- **Semicolon-delimited** — Common in European locale exports

Delimiter is auto-detected from the first line, or can be specified manually.

> **Note:** Excel files (`.xlsx`, `.xls`) are **not** supported. Export your spreadsheet to CSV first.

## Limitations

- Files are loaded synchronously and fully into memory. Very large files (100MB+) may cause performance issues.
- AI answers depend on the quality and context window of the chosen model. Only column profiles and the first 5 sample rows are sent to the AI — not the entire dataset.
- No streaming support. The full AI response is returned at once.
- No built-in export functionality. Use `query()` results with your own file-writing logic.

## Disclaimer

CSVBrain is provided as-is under the MIT License. AI-generated answers may not always be accurate — always verify critical data analysis. API usage may incur costs from your AI provider.

## Support

- **Issues:** [github.com/TheShadowRose/CSVBrain/issues](https://github.com/TheShadowRose/CSVBrain/issues)
- **Author:** @TheShadowRose