---
name: "ContextSlim Context Window Profiler & Optimizer"
description: "See exactly what's eating your context window. Analyzes prompts, conversations, and system instructions to show where every token goes. Actionable compression suggestions. All local."
author: "@TheShadowRose"
version: "1.0.1"
tags: ["context-window", "optimization", "tokens", "profiler", "cost-reduction", "analysis"]
license: "MIT"
---

# ContextSlim Context Window Profiler & Optimizer

See exactly what's eating your context window. Analyzes prompts, conversations, and system instructions to show where every token goes. Actionable compression suggestions. All local.

---

**Stop guessing why your AI forgot something. See exactly what's eating your context window.**

ContextSlim analyzes your prompts, conversations, and system instructions to show you where every token goes. Get actionable compression suggestions and visual breakdowns — all without sending anything to external APIs.

---

## The Problem

You're talking to an AI and suddenly it forgets critical information. Or your carefully crafted system prompt keeps getting cut off. Why? Because context windows aren't infinite, and most people have no idea how much space they're actually using.

Token counting is confusing. Different providers use different models. You don't want to install heavyweight tokenizer libraries just to get a ballpark estimate. And even if you could count tokens, you still don't know *where* they're being wasted.

## What ContextSlim Does

### 1. **Token Estimation** (`context_slim.py`)
Estimates token usage using word-based heuristics. No external dependencies, no API calls, no tokenizer libraries. Accurate within 10-15% for most English text.

- Provider-specific estimation (OpenAI, Anthropic, Google, or generic)
- Per-section breakdown (system prompt vs. user messages vs. tool definitions)
- Real context limits for major models (GPT-4: 128k, Claude: 200k, etc.)
- Truncation risk assessment (none/low/medium/high/critical)
- "Why did it forget?" diagnostic mode

### 2. **Compression Suggestions** (`context_compress.py`)
Analyzes your text and tells you exactly what you can cut, tighten, or simplify.

- Finds redundant phrases ("in order to" → "to")
- Identifies verbose language ("has the ability to" → "can")
- Detects excessive examples (5 examples → suggest 2-3)
- Spots formatting inefficiencies (excessive newlines, long separator lines)
- Flags repetitive instructions
- Estimates tokens saved per suggestion
- Confidence ratings (high/medium/low)

### 3. **Visual Reports** (`context_report.py`)
Generates beautiful HTML reports with CSS-based bar charts (zero JavaScript).

- Token usage breakdown by section
- Color-coded utilization meters
- Before/after compression comparisons
- Risk indicators (green → red)
- Works offline, mobile-friendly

---

## Quick Start

```bash
# Analyze a text file
python3 context_slim.py my_prompt.txt

# Get compression suggestions
python3 context_compress.py my_prompt.txt

# Generate full HTML report with suggestions
python3 context_report.py my_prompt.txt --compress --output report.html
```

### Basic Usage

```bash
# Analyze for a specific provider
python3 context_slim.py --provider anthropic --model claude-3-opus prompt.txt

# Get high-confidence suggestions only
python3 context_compress.py --min-confidence high prompt.txt

# Read from stdin
cat system_prompt.txt | python3 context_slim.py

# JSON output for scripting
python3 context_slim.py --output json prompt.txt > analysis.json
```

### Analyze Conversations

ContextSlim understands conversation JSON format:

```json
[
  {"role": "system", "content": "You are a helpful assistant..."},
  {"role": "user", "content": "Tell me about..."},
  {"role": "assistant", "content": "Sure! Here's..."}
]
```

```bash
python3 context_slim.py conversation.json
```

---

## Use Cases

### 1. **Prompt Engineering**
Before you deploy that 10,000-word system prompt, see how much space it actually takes. Find what you can cut without losing functionality.

### 2. **Debugging "Forgetting" Issues**
AI stopped following your instructions? See if your prompt is getting truncated. ContextSlim shows you exactly where the cutoff happens.

### 3. **Cost Optimization**
Tokens = money. Compress your prompts, reduce costs. See exactly how many tokens each compression saves.

### 4. **Multi-Provider Workflows**
Switching between GPT-4 (128k) and Claude (200k)? See how your prompts fit in each context window.

### 5. **Agent System Optimization**
Running an AI agent with tons of tools and memory? Profile which components are eating the most tokens.

### 6. **Team Standardization**
Enforce context budgets across your team. "System prompts must be under 5k tokens" — now you can actually measure it.

---

## How It Works

### Token Estimation Strategy

ContextSlim uses word-based heuristics instead of external tokenizers:

- **GPT models:** ~0.75 tokens per word
- **Claude models:** ~0.80 tokens per word
- **Generic average:** ~0.77 tokens per word

Plus adjustments for:
- Newlines (add ~0.3 tokens each)
- Code blocks (add ~2 tokens per block marker)
- Special formatting

**Why not use real tokenizers?**  
They require heavyweight dependencies (transformers, tiktoken) and still vary between models. Word-based estimation is "good enough" for profiling and costs zero dependencies.

### Compression Detection

ContextSlim scans for:
- **Redundant phrases:** "in order to", "due to the fact that", etc.
- **Verbose constructions:** "is able to" → "can"
- **Excessive examples:** More than 3-4 examples in one list
- **Formatting bloat:** Too many newlines, overly long separators
- **Repetitive instructions:** Similar sentences that could be consolidated

Each suggestion includes:
- What to change
- Estimated tokens saved
- Confidence level (high/medium/low)

---

## Configuration

Copy `config_example.py` to `config.py` and customize:

```python
# Set default provider
PROVIDER = 'anthropic'
MODEL = 'claude-3-opus'

# Adjust truncation risk thresholds
TRUNCATION_THRESHOLDS = {
    'none': 50,
    'low': 70,
    'medium': 85,
    'high': 95,
    'critical': 100
}

# Control compression suggestions
MIN_CONFIDENCE = 'medium'
MAX_SUGGESTIONS_PER_CATEGORY = 5
```

See `config_example.py` for full options.

---

## Examples

### Example 1: System Prompt Analysis

```bash
$ python3 context_slim.py system_prompt.txt --provider openai --model gpt-4

=== ContextSlim Analysis ===
Provider: openai (limit: 128,000 tokens)
Total tokens: 8,432
Utilization: 6.59%
Truncation risk: NONE

Section breakdown:
  [file] 8,432 tokens (11,234 words)
```

### Example 2: Compression Suggestions

```bash
$ python3 context_compress.py system_prompt.txt --min-confidence high

=== ContextSlim Compression Analysis ===
Found 7 suggestions
Potential savings: 127 tokens

1. [REDUNDANCY] Replace "in order to" with "to"
   Confidence: high | Saves: ~3 tokens
   Original: ...in order to provide accurate responses...
   Suggested: ...to provide accurate responses...

2. [VERBOSITY] Simplify verbose phrase
   Confidence: high | Saves: ~5 tokens
   Original: ...has the ability to process...
   Suggested: ...can process...
```

### Example 3: Full HTML Report

```bash
$ python3 context_report.py conversation.json --compress --output report.html

✅ Report generated: report.html
```

Open `report.html` in a browser to see:
- Total tokens and utilization
- Visual breakdown by message
- All compression suggestions with before/after
- Color-coded risk indicators

---

## What's Included

| File | Purpose |
|------|---------|
| `context_slim.py` | Main analysis engine (CLI + library) |
| `context_compress.py` | Compression suggestion engine |
| `context_report.py` | HTML report generator |
| `config_example.py` | Configuration template |
| `README.md` | This file |
| `LIMITATIONS.md` | Honest limitations |
| `LICENSE` | MIT License |

---

## Requirements

- Python 3.7+
- **Zero external dependencies** (stdlib only)
- Works on Linux, macOS, Windows

---

## Python API

Use ContextSlim in your own scripts:

```python
from context_slim import ContextAnalyzer, TokenEstimator
from context_compress import CompressionAnalyzer
from context_report import ReportGenerator

# Analyze text
analyzer = ContextAnalyzer(provider='anthropic', model='claude-3-opus')
profile = analyzer.analyze_text("Your prompt here...")

print(f"Tokens: {profile.total_tokens}")
print(f"Risk: {profile.truncation_risk}")

# Get compression suggestions
compressor = CompressionAnalyzer(provider='anthropic')
suggestions = compressor.analyze("Your prompt here...")

print(f"Could save {compressor.estimate_total_savings(suggestions)} tokens")

# Generate HTML report
html = ReportGenerator.generate_profile_report(profile, suggestions)
with open('report.html', 'w') as f:
    f.write(html)
```

---

## quality-verified


---

## FAQ

**Q: How accurate is the token estimation?**  
A: Within 10-15% for English text. Good enough for profiling, not perfect. If you need exact counts, use the provider's official tokenizer.

**Q: Does it work for non-English text?**  
A: Estimation accuracy drops for non-English. Word-to-token ratios vary by language. You can adjust ratios in `config.py`.

**Q: Does it send my data anywhere?**  
A: **No.** Everything runs locally. Zero network calls, zero external APIs.

**Q: Can I use it for code?**  
A: Yes, but code has different token patterns than prose. Estimates may be less accurate for heavily formatted code.

**Q: What about multimodal contexts (images, audio)?**  
A: Text-only for now. See `LIMITATIONS.md`.

---

## License

MIT — See `LICENSE` file.

---

## Author

**Shadow Rose**

Built for AI users who want to understand and optimize their context windows without needing a PhD in tokenization.


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