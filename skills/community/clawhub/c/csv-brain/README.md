# CSVBrain — Natural Language Data Queries

Load a CSV file. Ask questions in plain English. Get answers.

## Quick Start

```javascript
const { CSVBrain } = require('./src/csv-brain');
const brain = new CSVBrain();
await brain.load('sales-data.csv');

const answer = await brain.ask('What was our best selling month?');
const trend = await brain.ask('Show me the revenue trend for Q3');
const top = await brain.ask('Which product has the highest margin?');
```

## What It Does

1. **Parses** your CSV/Excel file (auto-detects headers, types, delimiters)
2. **Profiles** the data (column types, ranges, distributions, missing values)
3. **Translates** your question into a data operation
4. **Returns** the answer in plain English with supporting numbers

## Supported Questions

| Type | Example |
|------|---------|
| Aggregation | "What's the total revenue?" |
| Filtering | "Show sales over $1000" |
| Ranking | "Top 5 customers by spend" |
| Trends | "How did sales change month over month?" |
| Comparison | "Compare Q1 vs Q2 performance" |
| Distribution | "What's the average order size?" |

## Features

- **Auto-detect** column types (dates, numbers, categories, text)
- **Large file support** — streams data, doesn't load everything into memory
- **Multiple formats** — CSV, TSV, Excel (.xlsx), JSON arrays
- **Export** — save query results as new CSV files
---

## ⚠️ Disclaimer

This software is provided "AS IS", without warranty of any kind, express or implied.

**USE AT YOUR OWN RISK.**

- The author(s) are NOT liable for any damages, losses, or consequences arising from 
  the use or misuse of this software — including but not limited to financial loss, 
  data loss, security breaches, business interruption, or any indirect/consequential damages.
- This software does NOT constitute financial, legal, trading, or professional advice.
- Users are solely responsible for evaluating whether this software is suitable for 
  their use case, environment, and risk tolerance.
- No guarantee is made regarding accuracy, reliability, completeness, or fitness 
  for any particular purpose.
- The author(s) are not responsible for how third parties use, modify, or distribute 
  this software after purchase.

By downloading, installing, or using this software, you acknowledge that you have read 
this disclaimer and agree to use the software entirely at your own risk.


**DATA DISCLAIMER:** This software processes and stores data locally on your system. 
The author(s) are not responsible for data loss, corruption, or unauthorized access 
resulting from software bugs, system failures, or user error. Always maintain 
independent backups of important data. This software does not transmit data externally 
unless explicitly configured by the user.

---

## Support & Links

| | |
|---|---|
| 🐛 **Bug Reports** | TheShadowyRose@proton.me |
| ☕ **Ko-fi** | [ko-fi.com/theshadowrose](https://ko-fi.com/theshadowrose) |
| 🛒 **Gumroad** | [shadowyrose.gumroad.com](https://shadowyrose.gumroad.com) |
| 🐦 **Twitter** | [@TheShadowyRose](https://twitter.com/TheShadowyRose) |
| 🐙 **GitHub** | [github.com/TheShadowRose](https://github.com/TheShadowRose) |
| 🧠 **PromptBase** | [promptbase.com/profile/shadowrose](https://promptbase.com/profile/shadowrose) |

*Built with [OpenClaw](https://github.com/openclaw/openclaw) — thank you for making this possible.*

---

🛠️ **Need something custom?** Custom OpenClaw agents & skills starting at $500. If you can describe it, I can build it. → [Hire me on Fiverr](https://www.fiverr.com/s/jjmlZ0v)
