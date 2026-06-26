---
name: ai-usage-audit
author: Junjie Liu / Philosophie AI
version: 1.0.0
description: Monthly AI usage retrospective and insights — pulls your recent conversation history, analyzes usage patterns across multiple dimensions, and generates a polished HTML report with an actionable improvement checklist. Trigger when the user says "AI usage audit", "usage review", "review my chats", "monthly retrospective", "analyze my conversations", "how have I been using AI", "月度回顾", "使用审计", "AI 使用回顾". Also trigger when the user wants to understand their AI usage efficiency, discover inefficiency patterns, or optimize human-AI collaboration. Even casual phrases like "what have I been doing lately" (referring to AI conversations) or "let's do a retro" should trigger this skill. Note: this skill requires an AI product with memory or chat history features (e.g. Claude Pro with memory).
---

# AI Usage Audit — Monthly Retrospective & Insights

## Purpose

Turn your AI conversation history into a mirror: see what you're actually using AI for, where you're efficient, where you're wasting time, and where collaboration friction is highest. It's essentially a Sprint Retro applied to human-AI collaboration — a data-driven approach to continuously improving how you work with AI.

## When to Trigger

- User says "AI usage audit", "usage review", "monthly retrospective", "review my chats"
- User says "analyze my conversations", "how have I been using AI"
- User says "月度回顾", "使用审计", "AI 使用回顾", "分析我的对话"
- User wants to understand their AI usage efficiency or patterns
- User says "what have I been doing lately" or "let's do a retro" (referring to AI conversations)

## Prerequisites

This skill depends on `recent_chats` and `conversation_search` tools to pull conversation history. If these tools are unavailable, inform the user that this skill only works with AI products that have conversation history features.

## Language Configuration

**Default**: Match the user's language (detect from their message).

If the user specifies a language preference (e.g. "in English", "用中文", "en français"), use that language for the entire report. The HTML report, all analysis text, section headers, and the improvement checklist should all be in the chosen language.

Technical terms, tool names, and conversation titles may remain in their original language regardless of the report language.

## Data Collection Phase

Thorough data collection is the foundation of analysis quality. Don't start writing after pulling just one page — the more comprehensive the data, the more valuable the insights.

### Step 1: Determine Analysis Window

Default: past 30 days. If the user specifies a different time range, follow their request.

Calculate the time window: today minus 30 days (or the user-specified number of days) to get the `after` parameter.

### Step 2: Pull Conversation Records

Use `recent_chats` tool multiple times, n=20 each time, paginate with the `before` parameter until the entire time window is covered or approximately 5 rounds have been pulled.

For each conversation, record:
- Conversation title/topic (inferred from chat snippet)
- Update timestamp
- Approximate content category (for later analysis)

If the user is inside a Project, only conversations within that Project will be retrieved; if outside a Project, only non-Project conversations are available. Inform the user of this scope limitation.

### Step 3: Supplementary Search (Optional)

If high-frequency topics from recent_chats need more context, use `conversation_search` with relevant keywords to dig deeper.

## Analysis Framework

Analyze collected conversation data across five dimensions. Every dimension must be backed by specific evidence (conversation titles or content references) — no abstract conclusions without support.

### Dimension 1: Theme Clustering — "What am I using AI for?"

Categorize all conversations by topic. Typical categories include but are not limited to:
- Content creation (writing, copywriting, translation)
- Programming & technical (code, debugging, architecture)
- Research & learning (concept exploration, information synthesis)
- Decision-making & analysis (strategy, comparison, evaluation)
- File processing (documents, spreadsheets, presentations)
- Casual & exploratory (conversations without clear goals)

Output the conversation count and percentage for each category. Identify the "center of gravity" — the 2-3 areas where time and energy are most concentrated.

### Dimension 2: Pattern Detection — "Are there inefficiency patterns?"

Look for these signals:
- **Repeated questions**: Same or similar questions appearing across different conversations (knowledge not being retained)
- **Abandoned threads**: Tasks started but never completed (unclear goals or priority confusion)
- **Over-exploration**: Circling the same topic without converging on action (information consumption, not production)
- **Tool mismatch**: Using AI for things that could be solved faster with other tools
- **Context rebuilding**: Repeatedly providing background because conversations weren't continued in the same thread

For each identified pattern, provide specific conversations as evidence.

### Dimension 3: Value Output — "Which conversations actually produced something?"

Distinguish two types of conversations:
- **High-value output**: Produced concrete, usable deliverables (documents, code, presentations), made decisions, formed actionable plans
- **Low-efficiency consumption**: Primarily information intake, not converted into action or output

Estimate the proportion of high-value output conversations. Consumption isn't inherently bad — the goal is to make the ratio visible so the user can judge whether it's healthy.

### Dimension 4: Collaboration Friction — "Where does human-AI collaboration break down?"

Look for these friction signals:
- **Excessive revision**: Same output revised 3+ times (initial requirements were unclear)
- **Clarification loops**: Extensive back-and-forth to clarify what the user actually wants
- **Wrong tool choice**: Used an inappropriate tool or approach, then switched
- **Expectation gap**: User expressed dissatisfaction or started a new conversation for the same task

For each friction point, analyze root cause: was it a user-side issue (unclear requirements, unrealistic expectations) or an AI-side limitation (capability boundary, tool limitation)?

### Dimension 5: Highlights — "When was collaboration at its best?"

Identify 2-3 "best practice" moments:
- Conversations with the highest collaboration efficiency
- Conversations with the best output quality
- Most creative uses of AI

Analyze what these highlights have in common — under what conditions does collaboration work best?

## Output: HTML Report

Generate a polished HTML file, save to `/mnt/user-data/outputs/` and present with `present_files`.

### Report Structure

```
┌──────────────────────────────────────────────┐
│  HEADER                                       │
│  - "AI Usage Audit" + time range              │
│  - Total conversations / coverage / date       │
│  - One-sentence summary (overall profile)      │
└──────────────────────────────────────────────┘

§1  Data Overview
    - Total conversation count, time distribution (which days/weeks most active)
    - Topic distribution bar (pure CSS, no JS chart libraries)
    - Top keywords from the period

§2  Theme Clustering Analysis
    - Each category with conversation count and representative conversations
    - "Center of gravity" analysis
    - 🔍 Insight: Does your AI usage align with your core goals?

§3  Patterns & Efficiency
    - Identified inefficiency patterns (each with specific evidence)
    - Efficiency visualization using "traffic light" notation:
      🟢 Efficient / 🟡 Optimizable / 🔴 Needs change
    - 💡 Improvement suggestions (per pattern)

§4  Value Output Assessment
    - High-value vs. low-efficiency consumption ratio
    - Representative high-value conversations (brief description of output)
    - 📊 ROI assessment: time invested vs. actual output

§5  Collaboration Friction Points
    - Friction type statistics
    - Top 3 friction scenarios with root cause analysis
    - 🔧 Solutions (specific improvement methods per friction point)

§6  Highlights & Best Practices
    - 2-3 highlight moments
    - Common traits behind these highlights
    - ✨ Practices worth replicating

§7  Next Month Improvement Checklist
    - Based on all analysis above, generate 3-5 specific, actionable improvements
    - Each item format: What to do + Why + How to measure
    - Presented in checkbox style for easy tracking
    - This is the most important actionable section — no empty platitudes

§8  One-Paragraph Summary
    - 2-3 sentences for overall closure
    - Tone: like a coach who knows your work giving a monthly debrief
    - Not a repetition of prior sections — distill one core insight
```

### Section Usage Principles

- **Always write**: §1, §2, §3, §7, §8 (core skeleton)
- **Recommended**: §4, §6 (most audits will have content for these)
- **As needed**: §5 (only when clear friction is found)
- If data is too sparse (fewer than 10 conversations), switch to a compact version: §1 + §3 + §7 + §8

## Visual Design

The HTML report follows a clean, modern editorial design:

### Overall Style
- Light background (#faf9f6 warm white), high readability
- Serif font for headings (Newsreader), sans-serif for body (Inter for English, Noto Sans SC for Chinese, or appropriate font for other languages)
- Maximum width 820px, centered layout
- Comfortable spacing with breathing room between sections

### Key Components
- **Data cards**: White background, rounded corners, key numbers
- **Proportion bars**: Pure CSS horizontal bars for topic distribution
- **Traffic light labels**: 🟢🟡🔴 + text descriptions
- **Insight boxes**: Colored left border + light background (blue=insight, green=highlight, orange=suggestion, red=warning)
- **Checklist cards**: Checkbox-styled cards, each item actionable
- **Conversation references**: Gray background quote blocks with conversation title and timestamp

### Color System
- Each theme cluster category gets a distinct color (from a fixed palette)
- High-value = green tones, low-efficiency = orange tones, friction = red tones, highlights = blue tones

### Google Fonts
```html
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@300;400;500;600;700&family=Noto+Sans+SC:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

## Writing Style

### Tone
- Like a personal coach giving a monthly debrief — someone who knows your work
- Warm but not sentimental, data-driven but not cold
- Direct about problems but not judgmental — the goal is improvement, not evaluation
- Humor is fine; flippancy is not

### Format
- Use prose, not lists (except for the Checklist section)
- Use color highlights for key insights
- Every analysis point backed by evidence (conversation references)
- Summary paragraphs limited to 2-3 sentences — no rambling

### Language
- Write in the language determined by the Language Configuration section
- Tool names and technical terms stay in English regardless
- Conversation titles quoted as-is in their original language

## Quality Checklist

Before delivery, verify:
- [ ] Pulled enough conversation records (at least 3 pagination rounds or full time window)?
- [ ] Theme clustering backed by concrete data (not gut-feel categorization)?
- [ ] Each inefficiency pattern supported by specific conversations as evidence?
- [ ] Improvement checklist specific enough ("what + why + how to measure" all present)?
- [ ] One-paragraph summary distills a core insight (not repeating prior sections)?
- [ ] HTML report saved to outputs directory and presented with present_files?
- [ ] If fewer than 10 conversations, switched to compact version?

## What This Skill is NOT

- ❌ Not a token consumption tracker (doesn't count specific token usage)
- ❌ Not a full transcript dump (doesn't list every conversation verbatim)
- ❌ Not an AI product review (doesn't evaluate the AI's capabilities)
- ❌ Not a privacy audit (doesn't analyze sensitive information exposure)
- ✅ It's a personal retrospective to help you **see how you use AI and continuously improve your workflow**

## Credits

Built by **Junjie Liu / Philosophie AI**

- GitHub: [github.com/jjliu6](https://github.com/jjliu6)
- LinkedIn: [linkedin.com/in/junjieliu](https://linkedin.com/in/junjieliu/)
- Website: [philosophie.ai](https://philosophie.ai)

Part of the [ClawHub](https://github.com/jjliu6) skill collection.
