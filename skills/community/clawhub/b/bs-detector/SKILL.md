---
name: bs-detector
description: Detects key claims in long messages and summarizes the real point. Uses NLP to find what someone is actually saying vs. what they want you to believe.
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      bins: [python3]
    always: false
---

# BS Detector — Find the Real Point

Detects claims, identifies fluff, and extracts the actionable truth from long messages.

## Usage

```bash
python3 detect.py --input message.txt
python3 detect.py --text "Your long slack message here..."
```

## Features

- Claim extraction from long text
- Fluff detection (filler, buzzwords, corporate speak)
- Core point summarization
- Sentiment analysis
- Key numbers and facts highlighted

## Example

Input: Long corporate email
Output: "Core message: Deadline is Friday. Key ask: Approval by EOD Thursday."
