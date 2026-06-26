# Conversation History Summarization — Design Spec

## 1. Overview

### 1.1 Background

The chat assistant agent serializes the full history message sequence on every turn and loads it in full as LLM input context on the next turn. As the number of turns grows, token usage grows linearly, causing:

1. **Rising LLM inference cost**: each request carries more tokens.
2. **Increased latency**: longer context means longer time-to-first-token and total inference time.
3. **Context window overflow risk**: when total messages approach the model's context window limit, truncation may occur.
4. **Storage pressure**: the serialized message payload keeps growing.

### 1.2 Goal

When the number of conversation turns exceeds **10** (configurable), automatically compress earlier history into a text summary, replacing the original message sequence.

### 1.3 Non-goals

- No changes to frontend display logic or message delivery protocol
- No modification to raw message storage
- No impact on other message streams

---

## 2. Architecture Analysis

### 2.1 Message flow overview

```
User request
  │
  ▼
Conversation entry (service layer)
  │
  ├─ Parse user message
  ├─ Build agent input
  │    ├─ Load history messages from storage
  │    ├─ Inject system messages
  │    └─ Append current user message
  ├─ Build agent context
  │
  ▼
Agent inference
  │
  ├─ Pre-chat middleware: update profile, sync tool messages
  ├─ LLM inference
  └─ Post-chat middleware: moderation, persist messages
```

---

## 3. Detailed Design

### 3.1 Approach

Introduce summarization logic that checks turn count before LLM inference and triggers compression when the threshold is exceeded.

### 3.2 Turn counting

Count the number of messages where `role == User`.

### 3.3 Summarization strategy

- **Retain the most recent K turns** (default K=5) in full — no compression
- **Compress the first N-K turns** into a summary text
- System-level messages are always retained and never compressed

### 3.4 Summary generation

Use a lightweight LLM to generate the summary:

```go
type SummaryConfig struct {
    TriggerThreshold   int    `json:"trigger_threshold"`
    RetainRecentRounds int    `json:"retain_recent_rounds"`
    SummaryModel       string `json:"summary_model"`
    SummaryMaxTokens   int    `json:"summary_max_tokens"`
    Enabled            bool   `json:"enabled"`
}
```

### 3.5 Message replacement

```
Before:
  [System(profile)] [System(env)] [User1] [Assist1] [Tool1] [Assist1']
  [User2] [Assist2] ... [User10] [Assist10] [User11(current)]

After:
  [System(profile)] [System(env)] [System(summary: first 6 turns compressed)]
  [User7] [Assist7] [Tool7] [Assist7'] ... [User11(current)]
```

---

## 4. Code Change Plan

### 4.1 New files

| Path | Description |
|------|-------------|
| `internal/summarizer/summarizer.go` | Core summarization logic |
| `internal/summarizer/config.go` | Config struct definition |
| `internal/summarizer/prompt.go` | Summarization prompt template |
| `internal/summarizer/summarizer_test.go` | Unit tests |

### 4.2 Modified files

| Path | Change |
|------|--------|
| `internal/middleware/before_chat.go` | Call summarization logic |
| `internal/context/model.go` | Add `SummaryVersion` field |

---

## 5. Core pseudocode

```go
func SummarizeHistoryIfNeeded(ctx context.Context, state *AgentState) error {
    config := GetSummaryConfig(ctx)
    if !config.Enabled { return nil }

    rounds := countUserRounds(state.Messages)
    if rounds <= config.TriggerThreshold { return nil }

    splitIndex := findSplitIndex(state.Messages, config.RetainRecentRounds)
    msgsToSummarize := extractNonSystemMessages(state.Messages[:splitIndex])

    summaryText, err := generateSummary(ctx, config, msgsToSummarize)
    if err != nil {
        log.Warn(ctx, "generate summary failed, skip: %v", err)
        return nil
    }

    summaryMsg := &Message{Role: System, Content: "[SUMMARY]" + summaryText}
    state.Messages = append(systemMsgs, summaryMsg, state.Messages[splitIndex:]...)
    return nil
}
```

---

## 6. Risk & Fallback

| Risk | Mitigation |
|------|------------|
| Summary loses critical context | Retain the most recent 5 turns in full |
| Summarization LLM call fails | Skip summarization on failure, use full history |
| Cache conflict | Invalidate cache after summarization |

---

## 7. Token usage estimate

| Turns | Without summary | With summary | Savings |
|-------|----------------|--------------|---------|
| 10    | ~6,500         | ~6,500       | 0%      |
| 15    | ~9,750         | ~4,250       | ~56%    |
| 20    | ~13,000        | ~4,250       | ~67%    |
| 30    | ~19,500        | ~4,250       | ~78%    |
