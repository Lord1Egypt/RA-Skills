# API Reference Notes

These notes describe the default support surface exposed by the skill.

## Covered Surface

The bundled CLI maps every documented endpoint from the provided Dida365 OpenAPI spec:

### OAuth

- `GET /oauth/authorize`
- `POST /oauth/token`

### Project

- `GET /open/v1/project`
- `GET /open/v1/project/{projectId}`
- `GET /open/v1/project/{projectId}/data`
- `POST /open/v1/project`
- `POST /open/v1/project/{projectId}`
- `DELETE /open/v1/project/{projectId}`

### Task

- `GET /open/v1/project/{projectId}/task/{taskId}`
- `POST /open/v1/task`
- `POST /open/v1/task/{taskId}`
- `POST /open/v1/project/{projectId}/task/{taskId}/complete`
- `DELETE /open/v1/project/{projectId}/task/{taskId}`
- `POST /open/v1/task/move`
- `POST /open/v1/task/completed`
- `POST /open/v1/task/filter`

## CLI Payload Rules

- `project create` and `project update` accept first-class scalar flags for `name`, `color`, `sortOrder`, `viewMode`, and `kind`.
- `task create` and `task update` accept first-class scalar flags for:
  - `title`
  - `content`
  - `desc`
  - `kind`
  - `isAllDay`
  - `startDate`
  - `dueDate`
  - `timeZone`
  - `repeatFlag`
  - `priority`
  - `sortOrder`
- `task create` and `task update` accept JSON arrays via:
  - `--reminders-json`
  - `--tags-json`
  - `--items-json`
- `task move` accepts either:
  - a single operation from `--from-project-*`, `--to-project-*`, and `--task-id`
  - a full JSON array via `--json` or `--json-file`
- `task completed` and `task filter` accept either:
  - repeated `--project-id` and `--project-name`
  - first-class date flags such as `--start-date` and `--end-date`
  - a full JSON object via `--json` or `--json-file`
- `task filter` also accepts first-class filter flags for:
  - `--priority-json`
  - `--tag-json`
  - `--status-json`

## Exact-Match Project Resolution

The CLI resolves `--project-name` by calling `GET /open/v1/project` and matching `name` exactly.

- No fuzzy match
- No prefix match
- No task-title lookup
- Multiple matches are treated as an error

## Documented Quirks Preserved By The CLI

- `task update` requires both the path `taskId` and body fields `id` and `projectId`.
- Real testing showed `task update` behaves like patch semantics: sending only `title` preserved previously stored `content`, `desc`, `priority`, `repeatFlag`, and `reminders` in the tested cases.
- Real testing showed `project update` behaves like patch semantics: sending only `name` preserved previously stored `color`, `viewMode`, and `kind` in the tested cases.
- The docs show `tags` in task responses but do not document task tag mutation fields. Real testing showed stable create/update behavior for tag arrays, so the CLI exposes `--tags-json` for task writes.
- Task-level `kind` writes are undocumented in the official text. Real testing showed stable `TEXT` and `NOTE` writes, so the CLI exposes `--kind` for those values but still does not expose gray-area direct `CHECKLIST` writes.
- Real tag-filter testing showed `task filter` uses any-match / OR semantics for `tag`, not all-match semantics.
- Real testing showed `task completed` can operate account-wide when `projectIds` is omitted.
- Real testing showed unfiltered `task filter` responses are capped at 200 rows for this endpoint on the tested account.
- Real testing showed `task delete` behaves like soft delete in normal projects: the task left project views and appeared in the app trash, but could still be read through `task get` immediately after deletion.
- Real testing showed inbox delete behavior depends on the project id form. Using the literal alias `inbox` was unreliable; using the concrete inbox project id behaved more like soft delete to trash.
- Real testing showed move behavior for inbox tasks should still be treated as unreliable.
- Columns are returned by project data reads, but no column CRUD endpoints are documented. The CLI keeps columns read-only.

## Date Format

The documented date-time format is:

`yyyy-MM-dd'T'HH:mm:ssZ`

Example:

`2019-11-13T03:00:00+0000`

Use that format for:

- `startDate`
- `dueDate`
- `completedTime`
- completed-task query date filters
- task-filter query date filters

Observed date/time rules confirmed in real API and app testing:

- For non-all-day tasks, `startDate == dueDate` behaves like a point-in-time task.
- For non-all-day tasks, `dueDate > startDate` behaves like a time-range task.
- For multi-day all-day tasks, the API uses `dueDate` as an exclusive upper bound: the stored `dueDate` is the local midnight immediately after the visible end date.
- The API may normalize returned timestamps to UTC while preserving `timeZone`.
- Non-documented date formats such as `2026-03-20 23:00:00` may be silently ignored instead of rejected. Use the documented format exactly.
- The CLI validates task and task-query date strings locally against the documented format to avoid silent API drops.
- For `task completed` queries, real boundary testing showed the `completedTime` window is inclusive on both ends.

## Confirmed `repeatFlag` Patterns

The following `repeatFlag` values were confirmed by reading tasks created in the official Dida365 client and by writing the same values back through the API.
This list intentionally includes only patterns whose meaning is directly expressed by the stored `repeatFlag`.

### Standard RRULE Patterns

- Every day: `RRULE:FREQ=DAILY;INTERVAL=1`
- Every 2 days: `RRULE:FREQ=DAILY;INTERVAL=2`
- Weekdays: `RRULE:FREQ=WEEKLY;INTERVAL=1;BYDAY=MO,TU,WE,TH,FR`
- Every week on one day: `RRULE:FREQ=WEEKLY;INTERVAL=1;BYDAY=MO`
- Weekly on selected weekdays: `RRULE:FREQ=WEEKLY;WKST=MO;INTERVAL=1;BYDAY=TU,WE,TH`
- Every 2 weeks on selected weekdays: `RRULE:FREQ=WEEKLY;WKST=MO;INTERVAL=2;BYDAY=MO,TH,SA`
- Weekends: `RRULE:FREQ=WEEKLY;INTERVAL=1;BYDAY=SU,SA`
- Every 3 weeks: `RRULE:FREQ=WEEKLY;WKST=MO;INTERVAL=3;BYDAY=MO`
- Every month on the same day: `RRULE:FREQ=MONTHLY;INTERVAL=1;BYMONTHDAY=16`
- Every month on the last day: `RRULE:FREQ=MONTHLY;INTERVAL=1;BYMONTHDAY=-1`
- Every month on the first Monday: `RRULE:FREQ=MONTHLY;INTERVAL=1;BYDAY=MO;BYSETPOS=1`
- Every 4 months: `RRULE:FREQ=MONTHLY;INTERVAL=4;BYMONTHDAY=16`
- Every year on the same month/day: `RRULE:FREQ=YEARLY;INTERVAL=1;BYMONTH=3;BYMONTHDAY=16`
- Every 5 years: `RRULE:FREQ=YEARLY;INTERVAL=5;BYMONTH=3;BYMONTHDAY=16`

### Dida365 Extensions On RRULE

- Legal workdays: `RRULE:FREQ=DAILY;INTERVAL=1;TT_SKIP=HOLIDAY,WEEKEND`
- Official holidays: `RRULE:FREQ=DAILY;INTERVAL=1;TT_SKIP=OFFICIAL_WORKDAY`
- Every 3 days, skip holidays: `RRULE:FREQ=DAILY;INTERVAL=3;TT_SKIP=HOLIDAY`
- Every 3 days, skip weekends and holidays: `RRULE:FREQ=DAILY;INTERVAL=3;TT_SKIP=WEEKEND,HOLIDAY`

### ERULE Patterns

- Forgetting curve: `ERULE:NAME=FORGETTINGCURVE;CYCLE=0`
- Custom calendar dates: `ERULE:NAME=CUSTOM;BYDATE=20260319,20260320,20260328,20260331`

### Lunar Patterns

- Lunar monthly: `LUNAR:FREQ=MONTHLY;INTERVAL=1;BYMONTHDAY=28`
- Lunar yearly: `LUNAR:FREQ=YEARLY;INTERVAL=1;BYMONTH=1;BYMONTHDAY=28`

### Usage Notes

- `repeatFlag` is not limited to plain RFC-style `RRULE` values. Dida365 also returns and accepts `ERULE`, `LUNAR`, and `TT_SKIP`-extended rules.
- Some values encode the current task date, such as `BYMONTHDAY=16` or `BYMONTH=3;BYMONTHDAY=16`. When creating a new rule, adjust those date parts to match the task's intended schedule.
- The CLI preserves `--repeat-flag ""`, so an empty string can be used to clear a stored recurrence value.
- Real undated-task testing showed `repeatFlag` can be silently cleared instead of preserved. For reliable recurrence writes, use `repeatFlag` only on tasks that already have `startDate` and `dueDate`.
- The list above is based on confirmed round-trips. If a UI label implies extra semantics that are not visible in the stored `repeatFlag`, do not infer more than the literal rule string expresses.

## Confirmed Reminder Patterns

The following reminder trigger values were confirmed through real API calls and Chinese-locale app checks.

- On time: `TRIGGER:PT0S`
- 5 minutes early: `TRIGGER:-PT5M`
- 30 minutes early: `TRIGGER:-PT30M`
- 1 hour early: `TRIGGER:-PT1H`
- 1 hour early: `TRIGGER:-PT60M`
- 1 day early: `TRIGGER:-PT1440M`
- All-day task, same day 9:00: `TRIGGER:P0DT9H0M0S`
- All-day task, same day 18:00: `TRIGGER:P0DT18H0M0S`

Usage notes:

- For multi-reminder tasks, app display order may differ from API array order.
- For all-day tasks with custom reminder times, the API stores offsets relative to the local-midnight boundary of the all-day task.
- `TRIGGER:-P1DT0H0M0S` is intentionally excluded from the stable list because real testing showed inconsistent app labeling.

## Intentionally Excluded Gray-Area Patterns

The skill intentionally does not expose the following pattern families as normal supported usage:

- Reminder `TRIGGER:-P1DT0H0M0S`
  - The API stored this value, but real Chinese-locale app checks labeled it as "2 days early" rather than "1 day early".
- Monthly weekday recurrence with `BYSETPOS != 1`
  - The API stored these rules and calendar placement was correct, but the app repeat label was wrong for tested values such as second, third, fourth, and last Monday.

## Definitions

### Enum Values

- Task priority: `0` none, `1` low, `3` medium, `5` high
- Task status: `0` normal, `2` completed
- Checklist item status: `0` normal, `1` completed
- Task kind: `TEXT`, `NOTE`, `CHECKLIST`
- Project kind: `TASK`, `NOTE`
- Project viewMode: `list`, `kanban`, `timeline`
- Project permission: `read`, `write`, `comment`

### ChecklistItem

- `id`: subtask identifier. In real update testing, checklist item ids were not stable across task updates; the API reassigned them after item edits.
- `title`: subtask title
- `status`: checklist item status, `0` normal or `1` completed
- `completedTime`: completion timestamp in the documented date format. In real testing this field was not stable for checklist items; completed status should be determined from `status`, not from `completedTime`.
- `isAllDay`: all-day flag
- `sortOrder`: subtask sort order
- `startDate`: start timestamp in the documented date format
- `timeZone`: timezone used for the start timestamp

### Task

- `id`: task identifier
- `projectId`: parent project identifier
- `title`: task title
- `content`: task content
- `desc`: checklist description text
- `isAllDay`: all-day flag
- `startDate`: start timestamp in the documented date format
- `dueDate`: due timestamp in the documented date format
- `completedTime`: completion timestamp in the documented date format
- `timeZone`: timezone used by the task timestamps
- `priority`: priority enum `0/1/3/5`
- `status`: task status enum `0/2`
- `repeatFlag`: recurrence rule, such as `RRULE:FREQ=DAILY;INTERVAL=1`
- `reminders`: reminder trigger strings
- `tags`: task tags returned in some actual responses. In real testing, tasks tagged in the official app were returned with tag arrays such as `["t1"]`
- `sortOrder`: task sort order
- `items`: checklist items for checklist tasks
- `kind`: task type enum `TEXT`, `NOTE`, or `CHECKLIST`
- `etag`: opaque revision token returned by the API
- `modifiedTime`: last-modified timestamp returned by the API

### Project

- `id`: project identifier
- `name`: project name
- `color`: project color, such as `#F18181`
- `sortOrder`: project sort order
- `closed`: whether the project is closed
- `groupId`: group identifier when the project belongs to a group
- `viewMode`: view enum `list`, `kanban`, or `timeline`
- `permission`: permission enum `read`, `write`, or `comment`
- `kind`: project type enum `TASK` or `NOTE`

### Column

- `id`: column identifier
- `projectId`: parent project identifier
- `name`: column name
- `sortOrder`: column sort order

### ProjectData

- `project`: project metadata. For inbox reads, this field may be omitted in actual responses.
- `tasks`: undone tasks under the project
- `columns`: columns under the project

## Response Handling

- Successful JSON responses are printed to stdout unchanged.
- Commands/endpoints that allow successful empty responses are normalized to:

```json
{
  "ok": true
}
```

- Commands that are expected to return JSON entities raise an error if the API returns an empty `200` response.

- Non-2xx responses are printed to stderr as structured JSON that includes:
  - error type
  - message
  - HTTP status
  - method
  - URL
  - parsed response body when available
