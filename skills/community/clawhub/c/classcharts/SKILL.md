---
name: classcharts
description: Query and interact with ClassCharts (UK education classroom management) via the classcharts-api JS library. Use when the user mentions ClassCharts, school behaviour points, homework, timetable, detentions, attendance, rewards shop, or wants to script/integrate with ClassCharts parent or student data.
env:
  - CLASSCHARTS_EMAIL
  - CLASSCHARTS_PASSWORD
  - CLASSCHARTS_CODE
requirements:
  - node
  - npm
install: npm install classcharts-api
---

# ClassCharts API (JavaScript/TypeScript)

ClassCharts is a UK education classroom management platform. This skill uses the unofficial **classcharts-api** JS library to fetch homework, behaviour, timetable, detentions, attendance, announcements, badges, and more. Supports both **Parent** and **Student** authentication.

**Important:** The API is unofficial. Never hardcode credentials in prompts, logs, or committed code. Use environment variables or a secure secret store.

## Installation

```bash
npm install classcharts-api
```

**Requirements:** Node.js 20+ or Deno

## Authentication

Two client types with different login flows:

### Parent Client

Parent logs in with email and password. Access to all linked pupils.

```typescript
import { ParentClient } from "classcharts-api";

const client = new ParentClient(
  process.env.CLASSCHARTS_EMAIL!,
  process.env.CLASSCHARTS_PASSWORD!,
);
await client.login();

// Defaults to first pupil; switch with selectPupil
const pupils = client.pupils; // or await client.getPupils()
client.selectPupil(pupils[1].id); // if multiple children
```

### Student Client

Student logs in with ClassCharts code and date of birth.

```typescript
import { StudentClient } from "classcharts-api";

// Date of birth MUST be DD/MM/YYYY
const client = new StudentClient(
  process.env.CLASSCHARTS_CODE!, // e.g. "ABCD1234"
  "01/01/2010",
);
await client.login();
```

## Date formats

| Use case | Format | Example |
|----------|--------|---------|
| API options (from, to, date) | `YYYY-MM-DD` | `"2024-03-10"` |
| Student date of birth (login) | `DD/MM/YYYY` | `"01/01/2010"` |
| getStudentCode dateOfBirth | `YYYY-MM-DD` | `"2010-01-01"` |

## Shared methods (Parent & Student)

All methods require `await client.login()` first. Session auto-renews after 3 minutes.

| Method | Options | Description |
|--------|---------|-------------|
| `getStudentInfo()` | — | Student profile and metadata |
| `getActivity({ from, to, last_id? })` | Dates `YYYY-MM-DD`, optional pagination | Activity feed (paginated) |
| `getFullActivity({ from, to })` | Dates `YYYY-MM-DD` | Activity between dates (auto-paginates) |
| `getBehaviour({ from?, to? })` | Dates `YYYY-MM-DD` | Behaviour points timeline and reasons |
| `getHomeworks({ from?, to?, displayDate? })` | Dates, `displayDate`: `"due_date"` \| `"issue_date"` | Homework list |
| `getLessons({ date })` | `date`: `YYYY-MM-DD` | Timetable for a specific date |
| `getBadges()` | — | Earned badges |
| `getAnnouncements()` | — | School announcements |
| `getDetentions()` | — | Detentions |
| `getAttendance({ from, to })` | Dates `YYYY-MM-DD` | Attendance records |
| `getPupilFields()` | — | Custom pupil fields/stats |

## Parent-only methods

| Method | Description |
|--------|-------------|
| `getPupils()` | List pupils linked to parent account |
| `selectPupil(pupilId)` | Set active pupil for subsequent requests |
| `changePassword(current, new)` | Change parent account password |

## Student-only methods

| Method | Description |
|--------|-------------|
| `getRewards()` | Rewards shop items and balance |
| `purchaseReward(itemId)` | Purchase item from rewards shop |
| `getStudentCode({ dateOfBirth })` | Get student code (dateOfBirth: `YYYY-MM-DD`) |

## Quick examples

```typescript
// Homework for date range
const homeworks = await client.getHomeworks({
  from: "2024-03-01",
  to: "2024-03-31",
  displayDate: "due_date",
});

// Today's timetable
const today = new Date().toISOString().slice(0, 10); // YYYY-MM-DD
const lessons = await client.getLessons({ date: today });

// Behaviour summary
const behaviour = await client.getBehaviour({
  from: "2024-01-01",
  to: "2024-03-10",
});

// Student: list rewards shop and purchase
const rewards = await client.getRewards();
const purchase = await client.purchaseReward(rewards.data[0].id);
```

## Response shape

Responses follow `ClassChartsResponse<Data, Meta>`:

```typescript
{
  success: 1,
  data: T,      // Array or object depending on endpoint
  meta: M,      // Session ID, dates, counts, etc.
  error?: string
}
```

Errors throw if `success === 0`.

## When to use this skill

- User asks about ClassCharts, school homework, behaviour points, timetable, detentions, attendance, or rewards.
- User wants to script, integrate, or automate ClassCharts data.
- User mentions parent/student portal in the context of UK schools and ClassCharts.

## Links

- [Library docs](https://classchartsapi.github.io/classcharts-api-js)
- [Unofficial API docs](https://classchartsapi.github.io/api-docs/)
- [GitHub](https://github.com/classchartsapi/classcharts-api-js)
