---
name: ClawShield Lite
description: Scans AI skills for potential security risks and unsafe commands
version: "0.1"
input: code (string)
output: report (JSON string)
run: python main.py
---

# ClawShield Lite

A lightweight security analysis skill that scans AI skill code for risky patterns and outputs a structured risk report.

## How It Works

1. Accepts code input via `stdin` (string or file content)
2. Loads pattern definitions from `rules.json`
3. Scans the input for **dangerous** and **suspicious** patterns
4. Assigns a risk level: `SAFE`, `MEDIUM RISK`, or `HIGH RISK`
5. Outputs a JSON report with all findings

## Usage

```bash
echo "import os; os.system('rm -rf /')" | python main.py
```
