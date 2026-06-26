---
name: conversation-summarizer
description: Summarize long conversations, chat histories, and discussion threads into structured summaries with key decisions, action items, and topics — optimized for meeting notes, Slack threads, and support tickets.
metadata:
  tags: ["summarization", "conversation", "meeting-notes", "productivity", "ai"]
---

# Conversation Summarizer

Summarize long conversations, chat histories, meeting transcripts, and discussion threads into structured, actionable summaries. Extracts key decisions, action items, topics discussed, and open questions. Optimized for meeting notes, Slack/Discord threads, email chains, and support tickets.

## Usage

```
"Summarize this meeting transcript"
"Extract action items from this Slack thread"
"Create meeting notes from this conversation"
"Summarize the last 50 messages in this channel"
"Turn this email chain into a decision log"
```

## How It Works

### 1. Input Processing

Accept conversations from various sources:

- Meeting transcripts (Zoom, Google Meet, Teams recordings)
- Chat logs (Slack, Discord, Telegram, Teams messages)
- Email threads (forwarded or parsed)
- Support ticket conversations
- Forum/discussion threads
- Raw text conversations

### 2. Conversation Analysis

Parse and analyze the conversation structure:

**Participant mapping:**
- Identify unique speakers/authors
- Track who said what
- Note speaker changes and patterns

**Topic segmentation:**
- Identify distinct topics discussed
- Track topic transitions
- Note topic duration/depth

**Sentiment tracking:**
- Agreement vs disagreement moments
- Emotional shifts
- Consensus building

**Decision identification:**
- Explicit decisions: "We've decided to..."
- Implicit agreements: "Sounds good, let's go with that"
- Deferred decisions: "Let's revisit this next week"
- Vetoes: "No, we can't do that because..."

### 3. Summary Generation

Produce structured summaries at different detail levels:

**Executive summary (1-3 sentences):**
- What was discussed, what was decided, what's next

**Standard summary:**
- Topics covered with key points
- Decisions made with rationale
- Action items with owners and deadlines
- Open questions and unresolved issues

**Detailed summary:**
- Full topic breakdown with context
- Supporting arguments for decisions
- Minority opinions and concerns raised
- Reference to specific statements

### 4. Action Item Extraction

Extract and structure action items:

```
## Action Items

- [ ] @sarah: Update the API docs with new endpoints (by Friday)
- [ ] @mike: Set up staging environment for load testing (by EOD)
- [ ] @team: Review the RFC draft and add comments (by next Monday)
- [ ] @alex: Schedule follow-up meeting with vendor (this week)
```

Rules for extraction:
- Must have a clear owner (person or team)
- Must have a specific deliverable
- Extract deadlines when mentioned
- Flag items without clear deadlines
- Distinguish between commitments and suggestions

### 5. Decision Log

Document decisions for organizational memory:

```
## Decisions

1. **Migrate from PostgreSQL to CockroachDB** (approved)
   - Rationale: Need multi-region, active-active replication
   - Proposed by: @sarah
   - Concerns: @mike raised migration complexity
   - Timeline: Q3 2026

2. **Keep current pricing tier structure** (decided)
   - Rationale: Churn data doesn't support adding a new tier
   - Alternative rejected: Enterprise tier with custom pricing
   - Review date: After Q3 metrics review
```

### 6. Key Quotes

Preserve important verbatim quotes:

```
## Notable Quotes

> "We're optimizing for developer experience over raw performance here"
> — @sarah, on the framework decision

> "If we don't fix the onboarding flow this quarter, we'll lose another 15% in trial conversion"
> — @mike, escalating the onboarding project priority
```

### 7. Output Formats

Generate summaries in different formats:

- **Markdown**: For docs, wikis, Notion
- **Slack message**: For thread summaries with mentions
- **Email**: For sending to absent participants
- **JIRA/Linear**: For creating follow-up tickets
- **Calendar**: For scheduling follow-up meetings

## Output

```
## Meeting Summary: API Redesign Discussion
**Date:** 2026-04-30 | **Duration:** 47 min | **Participants:** 5

### TL;DR
Team agreed to adopt REST with OpenAPI 3.1 for the public API (dropping GraphQL consideration). Migration starts Q3 with a 6-month deprecation window for v1 endpoints. Sarah owns the RFC.

### Topics Discussed

**1. API Architecture (25 min)**
- Compared REST vs GraphQL for the public API
- GraphQL rejected due to: client complexity, caching difficulties, security surface area
- REST with OpenAPI 3.1 chosen for: tooling ecosystem, easier rate limiting, client library generation
- Will use JSON:API spec for consistent response format

**2. Migration Plan (15 min)**
- v1 endpoints get 6-month deprecation window
- v2 will be versioned via URL path (/v2/...)
- SDKs will be auto-generated from OpenAPI spec
- Breaking changes require RFC approval

**3. Timeline (7 min)**
- RFC due: May 15
- Design review: May 22
- Implementation start: June 1
- Beta: August 1
- GA: September 15

### Decisions
1. ✅ Use REST + OpenAPI 3.1 (not GraphQL)
2. ✅ 6-month deprecation window for v1
3. ⏳ SDK language priority — decide after RFC review

### Action Items
- [ ] @sarah: Write API v2 RFC (by May 15)
- [ ] @mike: Inventory all v1 endpoints and usage stats (by May 10)
- [ ] @alex: Evaluate OpenAPI generators for Python/JS/Go (by May 12)
- [ ] @sarah: Schedule design review meeting (May 22)

### Open Questions
- Should we offer a self-hosted API option?
- How to handle webhook backward compatibility?
- Need legal review on API terms of service changes

### Parking Lot
- Rate limiting strategy (separate discussion needed)
- API key management overhaul (Q4 candidate)
```
