# Meeting Minutes Extractor — Reference Guide

## Purpose
Extract fully structured meeting minutes — action items, decisions, attendees, discussion points, risks, open questions — from notes, documents, transcripts, or audio files. Produce outputs ready for team distribution.

---

## Step 1 — Input Type Handling

| Input Type | Handling |
|---|---|
| Typed notes / Word doc | Read directly; detect sections by headers or blank lines |
| PDF meeting notes | Read full text; look for heading hierarchy |
| Image / screenshot of handwritten notes | Read visually; note any illegible passages as `[ILLEGIBLE]` |
| Audio file (.mp3, .m4a, .wav, .ogg, .flac) | Run audio_transcriber.py first (see SKILL.md Step 2) |
| Video transcript (.txt) | Read directly |
| SRT subtitle file | Strip sequence numbers and timestamps (pattern: `\d+\n\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}`) — keep spoken text only |
| Email chain | Extract meeting details from email body; identify confirmed attendees from recipients |
| Slack / Teams export | Parse by message timestamp and sender; group by topic |
| Calendar invite (.ics / event description) | Extract agenda, attendees, time, location |

### Audio Transcription Quality Flags
After transcription, note in output:
- `[INAUDIBLE]` — segment could not be transcribed
- `[CROSSTALK]` — multiple speakers talking simultaneously
- `[UNCLEAR: possible "word"]` — low-confidence transcription
- `[SPEAKER A / SPEAKER B]` — if speaker diarization not available, use generic labels

---

## Step 2 — Pre-Extraction: Meeting Context

Before extracting content, confirm or infer:

| Field | Source |
|---|---|
| Meeting type | Regular standup / Project review / Board meeting / 1:1 / Client call / All-hands / Interview |
| Formality level | Formal (board/legal) / Semi-formal (project team) / Informal (startup standup) |
| Language | If not English, note source language and translate key outputs |
| Confidentiality | Does the document contain any confidential or HR-sensitive content? Flag if so. |

---

## Step 3 — Meeting Overview Extraction

| Field | Value | Notes |
|---|---|---|
| Title / Subject | | From heading, subject line, or first sentence |
| Date | | Convert all formats to YYYY-MM-DD |
| Start time | | |
| End time | | |
| Duration | | If times given: calculate; if not, note [NOT RECORDED] |
| Location | | Physical address / Zoom / Teams / Google Meet / Phone |
| Meeting Link | | If present |
| Facilitator / Chair | | Person who ran the meeting |
| Note-taker / Scribe | | Person who wrote the notes |
| Quorum met? | | If formal meeting requiring quorum |
| Recording available? | | Yes / No / Unknown |

---

## Step 4 — Attendees

| Name | Role / Title | Department | Present | Late? | Left Early? |
|---|---|---|---|---|---|

Also extract:
- **Invited but absent**: note who was expected but didn't attend
- **Guests / external participants**: flag non-organization attendees
- **Proxy / substitute**: if someone attended on behalf of another

---

## Step 5 — Agenda vs. Actual Coverage

If an agenda was provided or referenced:
| # | Agenda Item | Covered? | Time Spent | Notes |
|---|---|---|---|---|

If no agenda was present, reconstruct the discussion flow as a de-facto agenda.

---

## Step 6 — Key Discussion Points

For each topic or agenda item, extract:

**[Topic / Agenda Item Name]**

| Element | Content |
|---|---|
| Summary | 2–4 sentence summary of what was discussed |
| Key facts / data shared | Metrics, numbers, status updates mentioned |
| Different viewpoints | If there was disagreement, note both sides |
| Concerns raised | Issues, blockers, risks mentioned |
| Context / background | Any background info shared to frame the discussion |

---

## Step 7 — Decisions Made

This section must be precise — every decision should be unambiguous.

| # | Decision | Made By | Rationale (if given) | Binding? | Reversible? |
|---|---|---|---|---|---|

**Decision quality indicators:**
- Explicit decision: "We decided to…", "The board approved…", "It was agreed that…" → extract verbatim
- Implicit decision: Inferred from action items or discussion outcome → note as `[inferred from discussion]`
- Deferred decision: "We'll revisit this next week" → log in Open Questions section, not here

---

## Step 8 — Action Items (Most Important Section)

Extract every action item with maximum precision. This section must be thorough and unambiguous.

| # | Action Item | Owner | Due Date | Priority | Dependencies | Status |
|---|---|---|---|---|---|---|

**Rules for action item extraction:**
- Must contain an actionable verb: "Send", "Review", "Schedule", "Create", "Investigate", "Follow up on", "Prepare", "Confirm"
- Extract the EXACT person named as owner — not "the team" unless no individual is named
- If no owner stated: `[UNASSIGNED]`
- If no due date: `[NOT SET]`
- Priority inference:
  - "urgent", "by end of day", "EOD", "ASAP", "blocking" → **High**
  - "this week", "by Friday", "soon" → **Medium**
  - "whenever you can", "at some point", "low priority" → **Low**
  - No signal → **Medium** (default)
- Dependencies: note if action item is blocked by another item or external party

**Types of action items to capture:**
- Direct assignments: "John will send the report by Thursday"
- Follow-ups: "Sarah will follow up with the vendor"
- Investigations: "Someone needs to look into the billing discrepancy"
- Scheduling: "Set up a follow-up call with the client"
- Approvals: "Get sign-off from legal before proceeding"
- Communications: "Inform the wider team about the decision"
- Document creation: "Write up the technical spec"

---

## Step 9 — Open Questions / Parking Lot

| # | Question / Issue | Raised By | Context | Next Step | Assigned To |
|---|---|---|---|---|---|

---

## Step 10 — Risks & Issues Surfaced

| # | Risk / Issue | Severity | Raised By | Mitigation Discussed | Action Item # |
|---|---|---|---|---|---|

Severity: **Critical** / **High** / **Medium** / **Low**

---

## Step 11 — Next Meeting

| Field | Value |
|---|---|
| Date & Time | |
| Location / Link | |
| Confirmed Attendees | |
| Agenda Items Proposed | |
| Who is Scheduling | |

---

## Step 12 — Executive Summary

3–6 sentence plain-English summary covering:
1. What was the purpose of the meeting?
2. What were the major decisions?
3. What are the most critical action items (top 3)?
4. What is the key risk or blocker?
5. What is the immediate next step?

---

## Step 13 — Follow-up Email Draft (on request)

If the user asks, generate a follow-up email:

```
Subject: [Meeting Title] — Minutes & Action Items (YYYY-MM-DD)

Hi team,

Thanks for attending [meeting name] on [date]. Here's a summary of what we covered:

**Decisions:**
1. [decision]
2. [decision]

**Action Items:**
| Owner | Action | Due |
|---|---|---|
| [name] | [action] | [date] |

**Open Questions:**
- [question] — owner: [name]

Next meeting: [date, time, link]

Please reach out if anything needs clarification.

[Sender name]
```

---

## Language Handling
- If the source is in a non-English language, translate action items, decisions, and the summary to English. Note the original language.
- For mixed-language meetings (code-switching), translate non-English segments inline with `[translated: original text]`.
- Preserve proper nouns (names, project names, company names) in their original language.

---

## Confidentiality Rules
- If the meeting contains HR matters (performance, discipline, compensation), flag: "⚠ This meeting contains HR-sensitive content. Distribute on a need-to-know basis."
- If it contains M&A, financial projections, or legal matters, flag with appropriate sensitivity warning.
- Do not include personal health or personal life disclosures made incidentally in the minutes.

## Action Prompt
End with: "Would you like me to:
- Export action items as a task list (CSV or JSON)?
- Draft the follow-up email to send to the team?
- Compare with previous meeting minutes you share?
- Flag which action items are overdue based on today's date?
- Create a recurring meeting template from this structure?"
