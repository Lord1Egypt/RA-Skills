---
name: "AI Meeting Intelligence Expert"
description: "AI-powered meeting intelligence assistant — automatically transcribe, summarize, extract action items, generate follow-ups, and track decisions across your meeting lifecycle. Supports multi-language transcription, speaker identification, sentiment analysis, and integration with calendar/email tools. Built for project managers, executives, sales teams, and distributed teams who need to capture and act on meeting insights without manual note-taking. Keywords: meeting notes, meeting transcription, action items extraction, meeting summary, decision tracking, calendar integration, agenda preparation, meeting efficiency, AI meeting assistant, 会议纪要, 会议转录, 智能摘要, 行动项提取, 会议效率, 待办跟进, 决策追踪."
version: "1.0.0"
---

# AI Meeting Intelligence Expert

## Overview

Transform chaotic meetings into structured, actionable insights. This AI-powered meeting intelligence assistant handles the complete meeting lifecycle—from agenda preparation to decision tracking—freeing you to focus on what matters: the conversation itself.

## Triggers

- 中文触发词：`会议纪要`、`智能会议`、`会议分析`、`会议摘要`、`提取行动项`、`会议转录`、`开会被忘`
- English triggers: `meeting notes`, `meeting summary`, `transcribe meeting`, `action items`, `decision tracking`, `prepare meeting`, `meeting agenda`

## Features

### 1. Pre-Meeting Preparation
- Generate structured meeting agendas based on topic keywords
- Create attendee briefing documents from CRM/project data
- Suggest time allocations for each agenda item
- Provide historical context from past meeting notes

### 2. Real-Time Transcription Support
- Process live meeting notes and convert to timestamped transcript
- Identify and label different speakers
- Flag action items, decisions, and questions in real-time
- Highlight sentiment shifts during discussions

### 3. Post-Meeting Intelligence
- Generate comprehensive meeting summaries (30-second, 1-minute, 5-minute versions)
- Extract and format action items with owners and deadlines
- Create follow-up email drafts for stakeholders
- Update project trackers and task managers

### 4. Meeting Analytics
- Track meeting frequency, duration, and attendance
- Identify recurring discussion topics
- Measure action item completion rates
- Generate meeting ROI reports

## Workflow

### Basic Meeting Summary Workflow

```
1. INPUT: Meeting transcript/notes/raw text
   ↓
2. PROCESS: AI extracts key information
   - Speakers and roles
   - Topics discussed
   - Decisions made
   - Action items assigned
   - Questions raised
   ↓
3. OUTPUT: Structured meeting intelligence
   - Executive summary
   - Action item list
   - Decision log
   - Follow-up recommendations
```

### Full Meeting Lifecycle Workflow

```
Phase 1: Preparation
├── Receive meeting topic/context
├── Generate agenda template
├── Pull relevant background data
└── Prepare attendee briefings

Phase 2: During Meeting
├── Log notes in real-time
├── Mark key moments
├── Track time vs. agenda
└── Note unresolved items

Phase 3: Post-Meeting
├── Transcribe and clean up notes
├── Generate summary versions
├── Extract action items
├── Draft follow-ups
└── Update trackers

Phase 4: Follow-Through
├── Send summaries to attendees
├── Create task reminders
├── Track action item status
└── Flag overdue items
```

## Input Examples

### Example 1: Meeting Notes Input
```
Meeting: Q2 Product Planning
Date: 2026-05-15
Attendees: Sarah (PM), Mike (Eng), Lisa (Design), John (Sales)

Notes:
- Sarah opened with Q1 review, metrics looking good
- Mike mentioned technical blockers on API integration
- Lisa showed new mockups, everyone loved the dark mode
- John said enterprise clients are asking for SSO
- Decided to prioritize SSO for next sprint
- Mike will create technical spec by Friday
- Lisa to update mockups with SSO flows by next week
- Sarah to schedule follow-up with enterprise team
```

**Expected Output:**
```markdown
## Meeting Summary: Q2 Product Planning

### Quick Take (30 sec)
Q1 metrics positive. Team aligned on Q2 priorities: SSO feature for enterprise clients. Technical spec due Friday, mockups by next week.

### Decisions Made
1. Prioritize SSO implementation in next sprint
2. Enterprise team meeting to be scheduled

### Action Items
| Item | Owner | Due Date |
|------|-------|----------|
| Create technical spec for SSO | Mike | 2026-05-20 |
| Update mockups with SSO flows | Lisa | 2026-05-22 |
| Schedule enterprise team follow-up | Sarah | 2026-05-18 |

### Discussion Highlights
- Enterprise clients requesting SSO (high priority)
- Dark mode mockups well received
- API integration blockers acknowledged
```

### Example 2: Action Item Extraction
**Input:** Raw meeting transcript or bullet points
**Output:** Structured action item list with:
- Task description
- Assigned owner
- Deadline (if mentioned)
- Priority level
- Related context

### Example 3: Meeting Agenda Generation
**Input:** "Quarterly planning meeting with engineering and product teams"
**Output:**
```markdown
## Q2 Planning Meeting Agenda

### Pre-Meeting (15 min)
- Review Q1 OKRs and completion status
- Prepare Q2 targets draft

### Agenda (60 min total)
1. Q1 Retrospective (15 min)
   - Wins to celebrate
   - Areas for improvement
   
2. Q2 Goal Setting (25 min)
   - Product roadmap alignment
   - Engineering capacity planning
   - Resource requirements
   
3. Team Updates (10 min)
   - Cross-functional dependencies
   - Blockers and risks
   
4. Wrap-Up (10 min)
   - Confirm decisions
   - Assign next steps
```

## Output Templates

### Template 1: Meeting Summary
```markdown
## [Meeting Title]

**Date:** [Date]
**Time:** [Start] - [End]
**Location:** [Room/Video Link]
**Attendees:** [Names and Roles]

### Executive Summary
[2-3 sentence overview]

### Agenda vs. Actual
| Topic | Planned | Actual |
|-------|---------|--------|
| ... | ... | ... |

### Key Decisions
1. [Decision 1]
2. [Decision 2]

### Action Items
- [ ] [Task] - @Owner - Due: [Date]
- [ ] [Task] - @Owner - Due: [Date]

### Open Questions
- [Question 1]
- [Question 2]

### Next Meeting
- Scheduled: [Date/Time]
- Focus: [Topics]
```

### Template 2: Follow-Up Email
```markdown
Subject: [Meeting Title] - Key Decisions & Your Action Items

Hi [Name],

Following up on today's [meeting name]. Here's a quick summary:

**What We Decided:**
- [Decision 1]
- [Decision 2]

**Your Next Steps:**
- [Action item 1] - by [date]
- [Action item 2] - by [date]

**Resources:**
- [Link to meeting notes]
- [Link to relevant documents]

Let me know if you have any questions!

Best,
[Your name]
```

## Integration Recommendations

| Use Case | Recommended Tools |
|----------|-------------------|
| Calendar sync | Google Calendar, Outlook |
| Note-taking | Notion, Obsidian, Evernote |
| Task management | Todoist, Asana, Linear, Jira |
| Video conferencing | Zoom, Google Meet, Teams |
| CRM sync | Salesforce, HubSpot |
| Email follow-ups | Gmail, Outlook |

## Best Practices

### For Meeting Organizers
1. Share agenda 24h before meeting
2. Designate a note-taker or use AI assistance
3. Start and end on time
4. Review and share summary within 2 hours

### For Action Item Tracking
1. Assign one clear owner per item
2. Set specific, achievable deadlines
3. Include context for why the task matters
4. Follow up within 48 hours of deadline

### For Meeting Efficiency
1. Default to 25 or 50-minute meetings
2. Include breaks for meetings over 90 minutes
3. Limit attendees to decision-makers and contributors
4. Record meetings (with consent) for accurate transcription

## Edge Cases & Troubleshooting

### Challenge: Incomplete Notes
**Solution:** Provide the AI with whatever you have—bullet points, partial transcripts, even voice memos. The assistant can work with fragmentary input and will clearly indicate confidence levels.

### Challenge: Multiple Meetings in One Day
**Solution:** Use the daily digest feature to get an overview of all meetings, cross-reference action items, and identify scheduling conflicts.

### Challenge: Unclear Action Item Ownership
**Solution:** When ambiguous, flag the item for clarification rather than assigning arbitrarily. Include a "Verify owner" tag.

### Challenge: Confidential Discussions
**Solution:** Emphasize that sensitive meetings should be handled locally. Provide a "sanitize" mode that removes sensitive names/companies while preserving structure.

## Version History

- **1.0.0** (2026-05-15): Initial release
  - Core meeting summary generation
  - Action item extraction
  - Decision tracking
  - Basic agenda generation
