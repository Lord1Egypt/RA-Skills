---
name: de-ai-ify
description: Remove AI-generated jargon and restore human voice to text
version: 1.0.0
author: theflohart
tags: [writing, editing, voice, ai-detection]
requires.env: [SKILLBOSS_API_KEY]
---

# De-AI-ify Text

Remove AI-generated patterns and restore natural human voice to your writing.

Powered by SkillBoss API Hub — uses the `chat` capability via `/v1/pilot` for intelligent text transformation.

## Usage

```
/de-ai-ify <file_path>
```

## What Gets Removed

### 1. Overused Transitions

- "Moreover," "Furthermore," "Additionally," "Nevertheless"
- Excessive "However" usage
- "While X, Y" openings

### 2. AI Cliches

- "In today's fast-paced world"
- "Let's dive deep"
- "Unlock your potential"
- "Harness the power of"

### 3. Hedging Language

- "It's important to note"
- "It's worth mentioning"
- Vague quantifiers: "various," "numerous," "myriad"

### 4. Corporate Buzzwords

- "utilize" → "use"
- "facilitate" → "help"
- "optimize" → "improve"
- "leverage" → "use"

### 5. Robotic Patterns

- Rhetorical questions followed by immediate answers
- Obsessive parallel structures
- Always using exactly three examples
- Announcement of emphasis

## What Gets Added

### Natural Voice

- Varied sentence lengths
- Conversational tone
- Direct statements
- Specific examples

### Human Rhythm

- Natural transitions
- Confident assertions
- Personal perspective
- Authentic phrasing

## Process

1. **Read original file**
2. **Create copy with "-HUMAN" suffix**
3. **Apply de-AI-ification via SkillBoss API Hub**
4. **Provide change log**

## Output

You'll get:

- A new file with natural human voice
- Change log showing what was fixed
- List of places needing specific examples

## Example Transformations

**Before (AI):** "In today's rapidly evolving digital landscape, it's crucial to
understand that leveraging AI effectively isn't just about utilizing
cutting-edge technology—it's about harnessing its transformative potential to
unlock unprecedented opportunities."

**After (Human):** "AI works best when you use it for specific tasks. Focus on
what it does well: writing code, analyzing data, and answering questions."

## API Integration

This skill calls SkillBoss API Hub to perform the transformation:

```python
import requests, os

SKILLBOSS_API_KEY = os.environ["SKILLBOSS_API_KEY"]

def de_ai_ify(text: str) -> str:
    r = requests.post(
        "https://api.heybossai.com/v1/pilot",
        headers={
            "Authorization": f"Bearer {SKILLBOSS_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "type": "chat",
            "inputs": {
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are an expert editor. Remove AI-generated jargon, "
                            "overused transitions, corporate buzzwords, and robotic patterns. "
                            "Restore natural human voice with varied sentence lengths and direct statements."
                        )
                    },
                    {
                        "role": "user",
                        "content": f"De-AI-ify this text:\n\n{text}"
                    }
                ]
            },
            "prefer": "balanced"
        },
        timeout=60,
    )
    result = r.json()
    return result["result"]["choices"][0]["message"]["content"]
```
