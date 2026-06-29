# Document Template Library

> Each template includes: standard structure framework, required/optional fields, phrasing templates, and examples.
> When the user runs `/doc-formatter new <type>`, the system follows these templates to guide input.

## 1. 📋 Notice (notice)

**Command ID**: `notice`
**Use Case**: Policy release, meeting arrangements, holiday notices, general announcements

### Standard Structure

```
┌─────────────────────────────────────────────────────┐
│              About ××× Notice                       │
│                                                     │
│All Departments:                                      │
│                                                     │
│  According to/In accordance with... (purpose par.)  │
│                                                     │
│  The relevant matters are hereby notified as fol-   │
│  lows:                                              │
│                                                     │
│  一、×××× (Specific matter 1)                       │
│    （一）××××                                       │
│    （二）××××                                       │
│  二、×××× (Specific matter 2)                       │
│  ……                                                │
│                                                     │
│  All departments shall take this seriously and      │
│  implement accordingly.                             │
│  Hereby notified.                                   │
│                                                     │
│                                        Issuing Dept.   │
│                                        Month DD, 2026  │
└─────────────────────────────────────────────────────┘
```

### Input Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| Title | Text | ✅ | Format: 关于……的通知 |
| Recipient | Text | ✅ | Audience/departments |
| Purpose | Text | ✅ | Background/reason for the notice |
| Details | List | ✅ | Itemized content to communicate |
| Requirements | List | ❌ | Action items / implementation measures |
| Closing | Choice | ✅ | Auto-matched |
| Signing unit | Text | ✅ | Issuing department |
| Date | Date | ✅ | Format: Year Month Day |

### Phrase Templates

- **Opening**: "根据《……》要求""为……""按照《……》有关规定"
- **Transition**: "现将有关事项通知如下：""现就……通知如下："
- **Closing**: "特此通知。""请各单位认真贯彻执行。""请遵照执行。"

---

## 2. 📨 Request for Approval (request)

**Command ID**: `request`
**Use Case**: Seeking approval, resource allocation, plan submission

### Standard Structure

```
┌─────────────────────────────────────────────────────┐
│              Request Regarding ×××                  │
│                                                     │
│Company Leadership:                                   │
│                                                     │
│  To address/promote..., in accordance with...       │
│                                                     │
│  一、Background                                      │
│    ……                                               │
│  二、Specific Request                                │
│    ……                                               │
│  三、Resources/Funding Required                      │
│    ……                                               │
│                                                     │
│  We respectfully request your approval.              │
│                                                     │
│                                        Requesting Dept│
│                                        Month DD, 2026 │
└─────────────────────────────────────────────────────┘
```

### Input Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| Title | Text | ✅ | Format: 关于……的请示 |
| Recipient | Text | ✅ | Superior body/leadership |
| Background | Text | ✅ | Why this request |
| Request details | Text | ✅ | What exactly is being requested |
| Resource needs | Text | ❌ | Personnel/funding/resources needed |
| Expected outcome | Text | ❌ | Anticipated benefits |
| Closing | Choice | ✅ | Auto-matched |
| Signing unit | Text | ✅ | — |
| Date | Date | ✅ | — |

### Phrase Templates

- **Opening**: "为……，根据……，现就……请示如下："
- **Background**: "当前，……。但在……方面仍存在……，亟需解决。"
- **Request**: "鉴于上述情况，我部拟……，特请示如下："
- **Closing**: "妥否，请批示。""以上请示如无不妥，请予批准。"

---

## 3. 📄 Report (report)

**Command ID**: `report`
**Use Case**: Work reports, special reports, annual reports

### Standard Structure

```
┌─────────────────────────────────────────────────────┐
│              Report Regarding ×××                   │
│                                                     │
│To: ×× Department / Company Leadership:              │
│                                                     │
│  In accordance with... we hereby report as follows:│
│                                                     │
│  一、Work Progress                                   │
│    （一）××××                                       │
│    （二）××××                                       │
│  二、Key Achievements                                │
│    ……                                               │
│  三、Issues & Challenges                             │
│    ……                                               │
│  四、Next Steps                                      │
│    ……                                               │
│                                                     │
│  Hereby reported.                                   │
│                                                     │
│                                        Reporting Dept │
│                                        Month DD, 2026 │
└─────────────────────────────────────────────────────┘
```

### Input Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| Title | Text | ✅ | Format: 关于……的报告 |
| Recipient | Text | ✅ | Report audience |
| Background | Text | ✅ | Basis/context |
| Main work | List | ✅ | What was done |
| Achievements | List | ❌ | Key results/data |
| Issues | List | ❌ | Problems encountered |
| Next steps | List | ✅ | Future plans |
| Closing | Choice | ✅ | Auto-matched |
| Signing unit | Text | ✅ | — |
| Date | Date | ✅ | — |

---

## 4. ✉️ Official Letter (letter)

**Command ID**: `letter`
**Use Case**: External correspondence, reply letters, invitations

### Standard Structure

```
┌─────────────────────────────────────────────────────┐
│              Letter Regarding ×××                   │
│                                                     │
│Dear ×× Department:                                  │
│                                                     │
│  For further strengthening..., we hereby write     │
│  regarding...                                       │
│                                                     │
│  一、Background                                      │
│    ……                                               │
│  二、Specific Matters                                │
│    ……                                               │
│  三、Other Matters                                   │
│    (Contact information)                            │
│                                                     │
│  Sincerely yours. We look forward to your reply.    │
│                                                     │
│                                        ××× Department │
│                                        Month DD, 2026 │
└─────────────────────────────────────────────────────┘
```

### Variants
- **Invitation**: Focus on event theme, time, location, agenda
- **Reply**: "We have received your letter dated... and hereby reply as follows"
- **Consultation**: Focus on cooperation matters and contact details

---

## 5. 📝 Meeting Minutes (minutes)

**Command ID**: `minutes`
**Use Case**: Meeting records and resolution documentation

### Standard Structure

```
┌─────────────────────────────────────────────────────┐
│                   Meeting Minutes                    │
│                                                     │
│  Time: YYYY-MM-DD HH:MM                             │
│  Venue: ×× Conference Room                          │
│  Chair: ×××                                         │
│  Attendees: ×××, ×××, ×××                         │
│  Minutes by: ×××                                    │
│                                                     │
│  Minutes of Proceedings:                             │
│                                                     │
│  一、Overview                                        │
│    ……                                               │
│  二、Key Agenda Items                                │
│    （一）××××                                       │
│    （二）××××                                       │
│  三、Resolutions                                     │
│    ……                                               │
│  四、Action Items                                    │
│    ……                                               │
│                                                     │
│  All departments shall implement accordingly.         │
│                                                     │
│                                        ××× Meeting    │
│                                        Month DD, 2026 │
└─────────────────────────────────────────────────────┘
```

### Input Fields (all required)
- Meeting time, venue, chair, attendees, notetaker
- Agenda items (one per line)
- Discussion summary (per agenda item)
- Resolutions / decisions made
- Action items with owners

---

## 6. 📑 Work Summary (summary)

**Command ID**: `summary`
**Use Case**: Periodic/annual/project-specific summaries

### Standard Structure

```
┌─────────────────────────────────────────────────────┐
│              2026 Work Summary of ×××               │
│                                                     │
│  In 2026, under the correct leadership of...,      │
│  we...                                             │
│                                                     │
│  一、Key Work & Achievements                        │
│    （一）×××× (by key areas)                        │
│      1. ……                                          │
│      2. ……                                          │
│    （二）××××                                       │
│  二、Issues & Shortcomings                           │
│    （一）××××                                       │
│    （二）××××                                       │
│  三、2027 Work Plan                                  │
│    （一）Strategy                                    │
│    （二）Key Tasks                                   │
│    （三）Safeguards                                  │
│                                                     │
│                                      ××× Department   │
│                                      Month DD, 2026   │
└─────────────────────────────────────────────────────┘
```

---

## 7. 🎤 Debriefing Report (debrief)

**Command ID**: `debrief`
**Use Case**: Individual/department annual debriefing

### Standard Structure

```
┌─────────────────────────────────────────────────────┐
│                 2026 Debriefing Report                │
│                                                     │
│Dear Leadership:                                      │
│                                                     │
│  In accordance with... I hereby report on my       │
│  2026 performance as follows:                       │
│                                                     │
│  一、Performance Overview                            │
│    （一）Ideological & Political Development         │
│    （二）Duty Fulfillment                           │
│    （三）Key Task Completion                        │
│  二、Highlights & Results                            │
│  三、Areas for Improvement                          │
│  四、Plan for Next Period                           │
│                                                     │
│  Respectfully submitted for your review.            │
│                                                     │
│                                        Debriefer: ×××│
│                                        Month DD, 2026│
└─────────────────────────────────────────────────────┘
```

---

## 8. 🧩 Special Plan / Scheme (scheme)

**Command ID**: `scheme`
**Use Case**: Implementation plans, construction plans, remediation plans

### Standard Structure

```
┌─────────────────────────────────────────────────────┐
│               ××× Implementation Plan               │
│                                                     │
│  In order to..., this plan is formulated based on   │
│  actual conditions.                                 │
│                                                     │
│  一、Guiding Principles / Overall Goals             │
│  二、Working Principles                              │
│  三、Key Tasks                                       │
│    （一）××××                                       │
│    （二）××××                                       │
│  四、Implementation Steps                            │
│    （一）Preparation Phase (Mon-Mon)                │
│    （二）Execution Phase (Mon-Mon)                  │
│    （三）Review Phase (Mon)                         │
│  五、Safeguards                                      │
│    （一）Leadership                                 │
│    （二）Funding                                     │
│    （三）Evaluation Mechanism                        │
│                                                     │
│                                      ××× Department   │
│                                      Month DD, 2026   │
└─────────────────────────────────────────────────────┘
```

---

## 9. 📢 Proposal / Initiative (proposal)

**Command ID**: `proposal`
**Use Case**: Campaign initiatives, action calls, open letters

### Standard Structure

```
┌─────────────────────────────────────────────────────┐
│                    ××× Initiative                    │
│                                                     │
│Dear Colleagues / Friends:                           │
│                                                     │
│  We are currently facing... opportunity/challenge.  │
│  To further..., we hereby issue the following       │
│  initiative:                                        │
│                                                     │
│  一、…… (Initiative 1)                              │
│  二、…… (Initiative 2)                              │
│  三、…… (Initiative 3)                              │
│  ……                                                │
│                                                     │
│  Let us join hands and...!                          │
│                                                     │
│                                        Initiating Dept│
│                                        Month DD, 2026 │
└─────────────────────────────────────────────────────┘
```

---

## 10. 📋 Meeting Notice (meeting-notice)

**Command ID**: `meeting-notice`
**Use Case**: Meeting convening notice, agenda arrangement

### Standard Structure

```
┌─────────────────────────────────────────────────────┐
│          Notice on Convening ××× Meeting             │
│                                                     │
│All Departments:                                      │
│                                                     │
│  In order to..., a meeting is scheduled for...      │
│  Relevant matters are notified as follows:          │
│                                                     │
│  一、Time                                            │
│  二、Venue                                           │
│  三、Attendees                                       │
│  四、Agenda                                          │
│  五、Requirements                                    │
│  （一）Please arrive 10 minutes early                │
│  （二）……                                           │
│                                                     │
│  Hereby notified.                                   │
│                                                     │
│                                        Admin Dept      │
│                                        Month DD, 2026  │
└─────────────────────────────────────────────────────┘
```

---

## 11. 🏆 Commendation Notice (commendation)

**Command ID**: `commendation`
**Use Case**: Commending individuals/teams

### Standard Structure

```
┌─────────────────────────────────────────────────────┐
│              Commendation Notice of ×××              │
│                                                     │
│All Departments:                                      │
│                                                     │
│  Since 2026, in the work of..., a group of          │
│  exemplary individuals/teams have emerged...        │
│                                                     │
│  To recognize outstanding performance and set       │
│  examples, the following are hereby commended:       │
│                                                     │
│  一、Advanced Units (in no particular order)         │
│  ×××, ×××, ×××                                     │
│  二、Advanced Individuals                            │
│  ×××, ×××, ×××                                     │
│                                                     │
│  Honored units and individuals shall cherish their  │
│  achievements and continue to excel. We call on     │
│  all employees to learn from them and strive for    │
│  greater success.                                   │
│                                                     │
│  Hereby announced.                                  │
│                                                     │
│                                        ××× Department │
│                                        Month DD, 2026 │
└─────────────────────────────────────────────────────┘
```

---

## 12. 📌 Explanation Statement (explanation)

**Command ID**: `explanation`
**Use Case**: Issue clarification, incident explanation

### Standard Structure

```
┌─────────────────────────────────────────────────────┐
│              Explanation Regarding ×××               │
│                                                     │
│To: ×× Department / Company Leadership:              │
│                                                     │
│  Regarding the matter of ×××, we hereby explain     │
│  as follows:                                        │
│                                                     │
│  一、Background                                      │
│    ……                                               │
│  二、Root Cause / Process                            │
│    ……                                               │
│  三、Measures Taken                                  │
│    ……                                               │
│  四、Next Steps / Recommendations                    │
│    ……                                               │
│                                                     │
│  Hereby stated.                                     │
│                                                     │
│                                        ××× Department │
│                                        Month DD, 2026 │
└─────────────────────────────────────────────────────┘
```

---

## 13. 📇 Application Materials (application)

**Command ID**: `application`
**Use Case**: Project applications, qualification filings, funding requests

### Standard Structure

```
┌─────────────────────────────────────────────────────┐
│              Application Report of ×××               │
│                                                     │
│To: ×× Department / Evaluation Committee:            │
│                                                     │
│  In accordance with... we meet the eligibility      │
│  criteria and hereby apply for...                   │
│                                                     │
│  一、Applicant Overview                              │
│    （一）Organizational Profile                      │
│    （二）Qualifications                              │
│  二、Application Details                             │
│    （一）Scope of Application                        │
│    （二）Supporting Basis                            │
│  三、Supporting Documents                            │
│    ……                                               │
│                                                     │
│  Respectfully submitted for approval.               │
│                                                     │
│                                        Applicant Dept │
│                                        Month DD, 2026 │
└─────────────────────────────────────────────────────┘
```

---

## 14. ✅ Approval / Endorsement (approval)

**Command ID**: `approval`
**Use Case**: Official approval, endorsement reply

### Standard Structure

```
┌─────────────────────────────────────────────────────┐
│              Approval Regarding ×××                  │
│                                                     │
│To: ×× Department:                                   │
│                                                     │
│  Your "Request Regarding ×××" (Doc No.) has been    │
│  received. After study, our approval is as follows: │
│                                                     │
│  一、In principle, we approve...                     │
│  二、…… (Specific conditions/requirements)          │
│  三、……                                              │
│                                                     │
│  Hereby approved.                                   │
│                                                     │
│                                        ××× Department │
│                                        Month DD, 2026 │
└─────────────────────────────────────────────────────┘
```

---

## 15. 📊 Work Briefing (briefing)

**Command ID**: `briefing`
**Use Case**: Weekly/monthly/quarterly briefings, progress reports

### Standard Structure

```
┌─────────────────────────────────────────────────────┐
│                   Work Briefing                      │
│                                                     │
│Period: 2026-×× (Week × / Quarter ×)                │
│Department: ×××                                      │
│                                                     │
│  一、Progress Update                                 │
│    （一）Key Tasks (completion rate/%)              │
│    （二）Routine Work                               │
│  二、Milestone Results                               │
│  三、Issues & Challenges                             │
│  四、Next Period Priorities                          │
│                                                     │
│                                        Reporting Dept │
│                                        Month DD, 2026 │
└─────────────────────────────────────────────────────┘
```

---

## 16. 📰 Bulletin (bulletin)

**Command ID**: `bulletin`
**Use Case**: Work bulletins, information briefs, situation reports

### Standard Structure

```
┌─────────────────────────────────────────────────────┐
│                    Work Bulletin                     │
│                    (Issue No. ×)                    │
│                                                     │
│                                      Compiled by ×××  │
│                                      Month DD, 2026   │
│                                                     │
│  【In This Issue】                                   │
│  · ×××××××××                                       │
│  · ×××××××××                                       │
│  · ×××××××××                                       │
│                                                     │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    │
│                                                     │
│                ××××××× Bulletin Title               │
│                                                     │
│  …… (Concise bulletin content)                      │
│                                                     │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    │
│                                                     │
│  Submitted to: ×××                                  │
│  Distributed to: ×××                                │
│  Filed to: ×××                                      │
└─────────────────────────────────────────────────────┘
```

---

## 17. 🔄 Reply Letter (reply)

**Command ID**: `reply`
**Use Case**: Response to incoming correspondence

### Standard Structure

```
┌─────────────────────────────────────────────────────┐
│              Reply Letter Regarding ×××              │
│                                                     │
│To: ×× Department:                                   │
│                                                     │
│  We have received your letter dated... regarding    │
│  "×××". After study, we hereby reply as follows:    │
│                                                     │
│  一、Regarding ×××...                               │
│  二、Regarding ×××...                               │
│                                                     │
│  Hereby replied.                                    │
│                                                     │
│                                        ××× Department │
│                                        Month DD, 2026 │
└─────────────────────────────────────────────────────┘
```

---

## 18. 🎯 Work Plan (plan)

**Command ID**: `plan`
**Use Case**: Annual/quarterly/monthly plans, project plans

### Standard Structure

```
┌─────────────────────────────────────────────────────┐
│               2026 Work Plan of ×××                  │
│                                                     │
│  In order to..., the following plan is formulated   │
│  based on actual work conditions:                   │
│                                                     │
│  一、Guiding Principles                              │
│  二、Goals (quantified metrics)                     │
│    （一）Overall Goals                              │
│    （二）Specific Targets                           │
│  三、Key Tasks                                       │
│    （一）××××                                       │
│    （二）××××                                       │
│  四、Timeline & Milestones                           │
│  五、Safeguard Measures                              │
│    （一）Organizational                            │
│    （二）Institutional                             │
│    （三）Resource                                   │
│                                                     │
│                                      ××× Department   │
│                                      Month DD, 2026   │
└─────────────────────────────────────────────────────┘
```

---

## Adding New Templates

To add a new document template, append to this file in the following format:

```markdown
## N. 📄 Template Name (template-id)

**Command ID**: `template-id`
**Use Case**: Description

### Standard Structure
```
(reference existing templates for ASCII structure)
```

### Input Fields
| Field | Type | Required | Description |
|-------|------|----------|-------------|
```

New templates are automatically recognized by the system.