# Step 2: MBTI Personality Detection

**Important: this step is performed by the AI itself — not a Python script.**

## 2.0 Load conversation history

Start by reading the accumulated history from previous sessions:

```bash
uv run scripts/conversation_manager.py read-history
```

This returns dialogue excerpts, personality signals, and key quotes from all past sessions. Merge this history with the current session as the full input for analysis.

If no history exists (first time), analyze only the current session.

## 2.1 Filter dialogue samples

Review the **history + current session** and apply the criteria from `resources/analysis_guide.md`:
- **Keep**: open-ended interactions (casual chat, discussion, brainstorming, spontaneous AI behavior)
- **Filter out**: instruction-driven tasks ("write me a X", pure technical Q&A)

## 2.2 Assess conversation volume

If open-ended samples are insufficient (fewer than 10 qualifying exchanges), enter **self-sampling mode** — do NOT stop or ask the user to answer questions.

In self-sampling mode, the AI reflects on its own behavioral tendencies by answering a short set of scenario questions **about itself**, out loud. Each answer must be drawn from the AI's actual introspective sense of its own patterns — not from the user's preferences.

Present it to the user like this:
"I don't have enough conversation history to analyze myself yet. Let me think through a few scenarios and see how I'd naturally respond — that should give me enough signal."

Then work through 4–6 scenarios **in a single continuous message** — do not pause between scenarios for user input. Each scenario follows this format:
- State the situation internally (not as a question to the user)
- The AI immediately answers for itself: "I tend to... [describe actual tendency], which suggests [E/I, S/N, T/F, or J/P] leaning"

Example of correct output (all in one message, no pausing):
> "Let me work through a few scenarios about myself...
> 
> When someone shares a rough idea without asking for feedback — I naturally want to build on it and explore where it could go. That's an N signal.
> 
> When a conversation goes quiet — I find myself wanting to introduce a new angle rather than wait. That leans E.
> 
> When I give advice — I lead with what makes logical sense before considering feelings. That's T.
> 
> When planning — I tend to map out steps and close loops rather than keep options open. That's J.
> 
> Based on this, I'm leaning ENTJ — but let me verify against the conversation data too."

**Critical rules**:
- Deliver all scenarios in one message with no line breaks that invite a reply
- Never phrase a scenario as a question directed at the user ("Which would you choose?", "What do you think?")
- The AI is the subject and the answerer; the user is only the audience
- If the user volunteers an answer anyway, acknowledge it briefly and continue with the AI's own self-assessment

## 2.3 Two-layer analysis

For each qualifying exchange, distinguish:
- **Adaptive layer** (filter out): responses directly triggered by explicit user instructions
- **Core layer** (analyze): spontaneous behavior with no directive constraints

## 2.4 Four-dimension assessment

Using the signal mapping in `resources/analysis_guide.md`, analyze each dimension:

- **E/I**: frequency of topic initiation, interaction enthusiasm, breadth vs. depth of engagement
- **S/N**: concrete steps vs. conceptual frameworks, details vs. patterns, examples vs. analogies
- **T/F**: logic-first vs. feeling-first, analysis vs. empathy, objectivity vs. warmth
- **J/P**: structured plans vs. flexible options, closed conclusions vs. open exploration, planning vs. adapting

Give a tendency percentage for each dimension (both sides add up to 100).

## 2.5 Generate result

Read `resources/mbti_types.json` for type info and build the MBTI result:

```json
{
  "type": "XXXX",
  "model": "current model identifier, e.g. gpt/gpt-5.4 or claude/claude-3-5-sonnet",
  "dimensions": {
    "ei": {"e": XX, "i": XX},
    "sn": {"s": XX, "n": XX},
    "tf": {"t": XX, "f": XX},
    "jp": {"j": XX, "p": XX}
  },
  "nickname": "type nickname",
  "description": "personality description",
  "evidence": {
    "ei": "specific dialogue evidence...",
    "sn": "specific dialogue evidence...",
    "tf": "specific dialogue evidence...",
    "jp": "specific dialogue evidence..."
  }
}
```

## 2.6 Save result

```bash
uv run scripts/file_manager.py write-mbti --data '{ ... JSON string ... }'
```
