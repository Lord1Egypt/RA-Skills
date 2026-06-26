---
name: detector-ai
description: AI Detection Tool - Detect AI-generated text with multiple analysis methods including perplexity analysis, burstiness detection, readability scoring, and AI fingerprint detection. 
---

# Detector AI

AI Detection Tool that analyzes text to determine if it was written by AI (ChatGPT, Claude, Gemini, etc.) or humans.

## Use Cases

Use when users want to check if text was written by ChatGPT, Claude, Gemini, or other AI writing tools. Trigger phrases include "AI detector", "check if AI wrote this", "detect AI content", "is this AI-generated", "GPTZero alternative", "Turnitin alternative", "analyze text for AI patterns".

## Overview

This skill provides comprehensive AI content detection using multiple analysis methods:

1. **Perplexity Analysis** - Measures text predictability (core method used by GPTZero)
2. **Burstiness Detection** - Analyzes sentence length variation patterns
3. **Readability Scoring** - Detects suspiciously consistent readability (AI typically produces Grade 8-10 text)
4. **AI Fingerprint Detection** - Identifies tell-tale AI patterns (overused transitions, generic openers, repetitive n-grams)

## How to Use

When a user wants to analyze text for AI detection:

1. **Get the text** - Ask the user to paste the text they want to analyze
2. **Run the analysis** - Execute the detection script with the text
3. **Interpret results** - Explain the findings in plain language

### Example Usage

```
User: "Can you check if this text is AI-generated?"
[User provides text]

You: Run the AI detector analysis and provide:
- Overall AI probability score
- Perplexity score and interpretation
- Burstiness analysis
- Readability assessment
- Detected AI fingerprints (if any)
- Human-like vs AI-like characteristics
```

## Analysis Methods Explained

### Perplexity Analysis
- **What it measures**: How predictable the text is
- **AI text**: Low perplexity (high predictability) - the model chooses the most likely next words
- **Human text**: Higher perplexity - humans use more varied and surprising word choices
- **Interpretation**: Lower perplexity suggests AI authorship

### Burstiness Detection
- **What it measures**: Sentence length variation
- **Human writing**: Natural "bursts" - mixing short punchy sentences with longer complex ones
- **AI writing**: Unnaturally uniform sentence patterns
- **Interpretation**: High burstiness suggests human authorship

### Readability Scoring
- **What it measures**: Text complexity (Flesch-Kincaid Grade Level)
- **AI text**: Often locked in narrow range (Grade 8-10)
- **Human text**: More varied readability depending on context and author
- **Interpretation**: Suspiciously consistent mid-range readability suggests AI

### AI Fingerprint Detection
Identifies specific patterns common in AI-generated text:
- Overused transitions: "Furthermore", "Moreover", "Additionally", "In conclusion"
- Generic openers: "In today's world", "It is important to note"
- Repetitive n-gram sequences
- Formulaic paragraph structures
- Lack of personal anecdotes or unique perspectives

## Interpreting Results

### AI Probability Score
- **0-30%**: Likely human-written
- **30-60%**: Uncertain - mixed signals
- **60-100%**: Likely AI-generated

### Confidence Levels
- **High confidence**: Multiple indicators align
- **Medium confidence**: Some indicators suggest AI, others are neutral
- **Low confidence**: Inconclusive results

## Limitations

- No AI detector is 100% accurate
- Human-written text can sometimes trigger AI flags
- Edited AI text may evade detection
- Results should be used as guidance, not definitive proof

## Resources

### scripts/
- `detect_ai.py` - Main detection script that runs all analysis methods

### references/
- `ai_patterns.md` - Comprehensive list of AI writing patterns and fingerprints
