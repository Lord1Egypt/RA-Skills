# Basecamp access policy

An access policy limits which endpoints Basecamp connections may call through Maton. Basecamp doesn't offer a choice of OAuth scopes, so an access policy is the way to narrow a connection. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/basecamp#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Basecamp: its 386 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create basecamp --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "account"},
    {"method": "GET", "path": "account.json"},
    {"method": "GET", "path": "buckets/{id}/recordings/{id}/backlinks"},
    {"method": "GET", "path": "buckets/{id}/recordings/{id}/backlinks.json"},
    {"method": "GET", "path": "recordings/{id}/backlinks"},
    {"method": "GET", "path": "recordings/{id}/backlinks.json"},
    {"method": "GET", "path": "boosts/{id}"},
    {"method": "GET", "path": "buckets/{id}/boosts/{id}"},
    {"method": "GET", "path": "buckets/{id}/recordings/{id}/boosts"},
    {"method": "GET", "path": "buckets/{id}/recordings/{id}/boosts.json"},
    {"method": "GET", "path": "buckets/{id}/recordings/{id}/events/{id}/boosts"},
    {"method": "GET", "path": "buckets/{id}/recordings/{id}/events/{id}/boosts.json"},
    {"method": "GET", "path": "recordings/{id}/boosts"},
    {"method": "GET", "path": "recordings/{id}/boosts.json"},
    {"method": "GET", "path": "recordings/{id}/events/{id}/boosts"},
    {"method": "GET", "path": "recordings/{id}/events/{id}/boosts.json"},
    {"method": "GET", "path": "buckets/{id}/calendars/{id}"},
    {"method": "GET", "path": "calendars/{id}"},
    {"method": "GET", "path": "buckets/{id}/chats"},
    {"method": "GET", "path": "buckets/{id}/chats.json"},
    {"method": "GET", "path": "buckets/{id}/chats/{id}"},
    {"method": "GET", "path": "buckets/{id}/chats/{id}/lines"},
    {"method": "GET", "path": "buckets/{id}/chats/{id}/lines.json"},
    {"method": "GET", "path": "buckets/{id}/chats/{id}/lines/{id}"},
    {"method": "GET", "path": "buckets/{id}/chats/{id}/uploads"},
    {"method": "GET", "path": "buckets/{id}/chats/{id}/uploads.json"},
    {"method": "GET", "path": "chats"},
    {"method": "GET", "path": "chats.json"},
    {"method": "GET", "path": "chats/{id}"},
    {"method": "GET", "path": "chats/{id}/lines"},
    {"method": "GET", "path": "chats/{id}/lines.json"},
    {"method": "GET", "path": "chats/{id}/lines/{id}"},
    {"method": "GET", "path": "chats/{id}/uploads"},
    {"method": "GET", "path": "chats/{id}/uploads.json"},
    {"method": "GET", "path": "buckets/{id}/card_tables/cards/{id}"},
    {"method": "GET", "path": "buckets/{id}/card_tables/lists/{id}/cards"},
    {"method": "GET", "path": "buckets/{id}/card_tables/lists/{id}/cards.json"},
    {"method": "GET", "path": "card_tables/cards/{id}"},
    {"method": "GET", "path": "card_tables/lists/{id}/cards"},
    {"method": "GET", "path": "card_tables/lists/{id}/cards.json"},
    {"method": "GET", "path": "buckets/{id}/card_tables/columns/{id}"},
    {"method": "GET", "path": "card_tables/columns/{id}"},
    {"method": "GET", "path": "template_library/card_tables"},
    {"method": "GET", "path": "template_library/card_tables.json"},
    {"method": "GET", "path": "buckets/{id}/card_tables/{id}"},
    {"method": "GET", "path": "card_tables/{id}"},
    {"method": "GET", "path": "buckets/{id}/client/approvals"},
    {"method": "GET", "path": "buckets/{id}/client/approvals.json"},
    {"method": "GET", "path": "buckets/{id}/client/approvals/{id}"},
    {"method": "GET", "path": "client/approvals"},
    {"method": "GET", "path": "client/approvals.json"},
    {"method": "GET", "path": "client/approvals/{id}"},
    {"method": "GET", "path": "buckets/{id}/client/correspondences"},
    {"method": "GET", "path": "buckets/{id}/client/correspondences.json"},
    {"method": "GET", "path": "buckets/{id}/client/correspondences/{id}"},
    {"method": "GET", "path": "client/correspondences"},
    {"method": "GET", "path": "client/correspondences.json"},
    {"method": "GET", "path": "client/correspondences/{id}"},
    {"method": "GET", "path": "buckets/{id}/client/recordings/{id}/replies"},
    {"method": "GET", "path": "buckets/{id}/client/recordings/{id}/replies.json"},
    {"method": "GET", "path": "buckets/{id}/client/recordings/{id}/replies/{id}"},
    {"method": "GET", "path": "client/recordings/{id}/replies"},
    {"method": "GET", "path": "client/recordings/{id}/replies.json"},
    {"method": "GET", "path": "client/recordings/{id}/replies/{id}"},
    {"method": "GET", "path": "buckets/{id}/cloud_files/{id}"},
    {"method": "GET", "path": "cloud_files/{id}"},
    {"method": "GET", "path": "buckets/{id}/comments/{id}"},
    {"method": "GET", "path": "buckets/{id}/recordings/{id}/comments"},
    {"method": "GET", "path": "buckets/{id}/recordings/{id}/comments.json"},
    {"method": "GET", "path": "comments/{id}"},
    {"method": "GET", "path": "recordings/{id}/comments"},
    {"method": "GET", "path": "recordings/{id}/comments.json"},
    {"method": "GET", "path": "buckets/{id}/documents/{id}"},
    {"method": "GET", "path": "buckets/{id}/vaults/{id}/documents"},
    {"method": "GET", "path": "buckets/{id}/vaults/{id}/documents.json"},
    {"method": "GET", "path": "documents/{id}"},
    {"method": "GET", "path": "vaults/{id}/documents"},
    {"method": "GET", "path": "vaults/{id}/documents.json"},
    {"method": "GET", "path": "my/drafts"},
    {"method": "GET", "path": "my/drafts.json"},
    {"method": "GET", "path": "embeds/{id}"},
    {"method": "GET", "path": "buckets/{id}/events"},
    {"method": "GET", "path": "buckets/{id}/events.json"},
    {"method": "GET", "path": "buckets/{id}/inbox"},
    {"method": "GET", "path": "buckets/{id}/inbox.json"},
    {"method": "GET", "path": "events"},
    {"method": "GET", "path": "events.json"},
    {"method": "GET", "path": "inbox"},
    {"method": "GET", "path": "inbox.json"},
    {"method": "GET", "path": "buckets/{id}/recordings/{id}/events"},
    {"method": "GET", "path": "buckets/{id}/recordings/{id}/events.json"},
    {"method": "GET", "path": "recordings/{id}/events"},
    {"method": "GET", "path": "recordings/{id}/events.json"},
    {"method": "GET", "path": "buckets/{id}/cards/completed"},
    {"method": "GET", "path": "buckets/{id}/cards/completed.json"},
    {"method": "GET", "path": "buckets/{id}/cards/no_due_date"},
    {"method": "GET", "path": "buckets/{id}/cards/no_due_date.json"},
    {"method": "GET", "path": "buckets/{id}/cards/not_now"},
    {"method": "GET", "path": "buckets/{id}/cards/not_now.json"},
    {"method": "GET", "path": "buckets/{id}/cards/open"},
    {"method": "GET", "path": "buckets/{id}/cards/open.json"},
    {"method": "GET", "path": "buckets/{id}/cards/overdue"},
    {"method": "GET", "path": "buckets/{id}/cards/overdue.json"},
    {"method": "GET", "path": "buckets/{id}/cards/unassigned"},
    {"method": "GET", "path": "buckets/{id}/cards/unassigned.json"},
    {"method": "GET", "path": "buckets/{id}/checkins"},
    {"method": "GET", "path": "buckets/{id}/checkins.json"},
    {"method": "GET", "path": "buckets/{id}/comments"},
    {"method": "GET", "path": "buckets/{id}/comments.json"},
    {"method": "GET", "path": "buckets/{id}/files"},
    {"method": "GET", "path": "buckets/{id}/files.json"},
    {"method": "GET", "path": "buckets/{id}/forwards"},
    {"method": "GET", "path": "buckets/{id}/forwards.json"},
    {"method": "GET", "path": "buckets/{id}/messages"},
    {"method": "GET", "path": "buckets/{id}/messages.json"},
    {"method": "GET", "path": "buckets/{id}/todos/completed"},
    {"method": "GET", "path": "buckets/{id}/todos/completed.json"},
    {"method": "GET", "path": "buckets/{id}/todos/no_due_date"},
    {"method": "GET", "path": "buckets/{id}/todos/no_due_date.json"},
    {"method": "GET", "path": "buckets/{id}/todos/open"},
    {"method": "GET", "path": "buckets/{id}/todos/open.json"},
    {"method": "GET", "path": "buckets/{id}/todos/overdue"},
    {"method": "GET", "path": "buckets/{id}/todos/overdue.json"},
    {"method": "GET", "path": "buckets/{id}/todos/unassigned"},
    {"method": "GET", "path": "buckets/{id}/todos/unassigned.json"},
    {"method": "GET", "path": "cards/completed"},
    {"method": "GET", "path": "cards/completed.json"},
    {"method": "GET", "path": "cards/no_due_date"},
    {"method": "GET", "path": "cards/no_due_date.json"},
    {"method": "GET", "path": "cards/not_now"},
    {"method": "GET", "path": "cards/not_now.json"},
    {"method": "GET", "path": "cards/open"},
    {"method": "GET", "path": "cards/open.json"},
    {"method": "GET", "path": "cards/overdue"},
    {"method": "GET", "path": "cards/overdue.json"},
    {"method": "GET", "path": "cards/unassigned"},
    {"method": "GET", "path": "cards/unassigned.json"},
    {"method": "GET", "path": "checkins"},
    {"method": "GET", "path": "checkins.json"},
    {"method": "GET", "path": "comments"},
    {"method": "GET", "path": "comments.json"},
    {"method": "GET", "path": "files"},
    {"method": "GET", "path": "files.json"},
    {"method": "GET", "path": "forwards"},
    {"method": "GET", "path": "forwards.json"},
    {"method": "GET", "path": "messages"},
    {"method": "GET", "path": "messages.json"},
    {"method": "GET", "path": "todos/completed"},
    {"method": "GET", "path": "todos/completed.json"},
    {"method": "GET", "path": "todos/no_due_date"},
    {"method": "GET", "path": "todos/no_due_date.json"},
    {"method": "GET", "path": "todos/open"},
    {"method": "GET", "path": "todos/open.json"},
    {"method": "GET", "path": "todos/overdue"},
    {"method": "GET", "path": "todos/overdue.json"},
    {"method": "GET", "path": "todos/unassigned"},
    {"method": "GET", "path": "todos/unassigned.json"},
    {"method": "GET", "path": "buckets/{id}/dock/doors"},
    {"method": "GET", "path": "buckets/{id}/dock/doors.json"},
    {"method": "GET", "path": "buckets/{id}/dock/doors/{id}"},
    {"method": "GET", "path": "dock/doors"},
    {"method": "GET", "path": "dock/doors.json"},
    {"method": "GET", "path": "dock/doors/{id}"},
    {"method": "GET", "path": "projects/recordings"},
    {"method": "GET", "path": "projects/recordings.json"},
    {"method": "GET", "path": "buckets/{id}/stacks"},
    {"method": "GET", "path": "buckets/{id}/stacks.json"},
    {"method": "GET", "path": "buckets/{id}/stacks/{id}"},
    {"method": "GET", "path": "stacks"},
    {"method": "GET", "path": "stacks.json"},
    {"method": "GET", "path": "stacks/{id}"},
    {"method": "GET", "path": "buckets/{id}/inbox_forwards/{id}"},
    {"method": "GET", "path": "buckets/{id}/inboxes/{id}/inbox_forwards"},
    {"method": "GET", "path": "buckets/{id}/inboxes/{id}/inbox_forwards.json"},
    {"method": "GET", "path": "inbox_forwards/{id}"},
    {"method": "GET", "path": "inboxes/{id}/inbox_forwards"},
    {"method": "GET", "path": "inboxes/{id}/inbox_forwards.json"},
    {"method": "GET", "path": "buckets/{id}/gauge_needles/{id}"},
    {"method": "GET", "path": "gauge_needles/{id}"},
    {"method": "GET", "path": "projects/{id}/gauge/needles"},
    {"method": "GET", "path": "projects/{id}/gauge/needles.json"},
    {"method": "GET", "path": "projects/{id}/gauge/needles/{id}"},
    {"method": "GET", "path": "reports/gauges"},
    {"method": "GET", "path": "reports/gauges.json"},
    {"method": "GET", "path": "buckets/{id}/google_documents/{id}"},
    {"method": "GET", "path": "google_documents/{id}"},
    {"method": "GET", "path": "buckets/{id}/todosets/{id}/hill"},
    {"method": "GET", "path": "buckets/{id}/todosets/{id}/hill.json"},
    {"method": "GET", "path": "buckets/{id}/todosets/{id}/hills/versions"},
    {"method": "GET", "path": "buckets/{id}/todosets/{id}/hills/versions.json"},
    {"method": "GET", "path": "buckets/{id}/todosets/{id}/hills/versions/{id}"},
    {"method": "GET", "path": "todosets/{id}/hill"},
    {"method": "GET", "path": "todosets/{id}/hill.json"},
    {"method": "GET", "path": "todosets/{id}/hills/versions"},
    {"method": "GET", "path": "todosets/{id}/hills/versions.json"},
    {"method": "GET", "path": "todosets/{id}/hills/versions/{id}"},
    {"method": "GET", "path": "buckets/{id}/inbox_forwards/{id}/replies"},
    {"method": "GET", "path": "buckets/{id}/inbox_forwards/{id}/replies.json"},
    {"method": "GET", "path": "buckets/{id}/inbox_forwards/{id}/replies/{id}"},
    {"method": "GET", "path": "inbox_forwards/{id}/replies"},
    {"method": "GET", "path": "inbox_forwards/{id}/replies.json"},
    {"method": "GET", "path": "inbox_forwards/{id}/replies/{id}"},
    {"method": "GET", "path": "buckets/{id}/inboxes/{id}"},
    {"method": "GET", "path": "inboxes/{id}"},
    {"method": "GET", "path": "lineup/markers"},
    {"method": "GET", "path": "lineup/markers.json"},
    {"method": "GET", "path": "buckets/{id}/message_boards/{id}"},
    {"method": "GET", "path": "message_boards/{id}"},
    {"method": "GET", "path": "buckets/{id}/categories"},
    {"method": "GET", "path": "buckets/{id}/categories.json"},
    {"method": "GET", "path": "buckets/{id}/categories/{id}"},
    {"method": "GET", "path": "categories"},
    {"method": "GET", "path": "categories.json"},
    {"method": "GET", "path": "categories/{id}"},
    {"method": "GET", "path": "buckets/{id}/message_boards/{id}/messages"},
    {"method": "GET", "path": "buckets/{id}/message_boards/{id}/messages.json"},
    {"method": "GET", "path": "buckets/{id}/messages/{id}"},
    {"method": "GET", "path": "message_boards/{id}/messages"},
    {"method": "GET", "path": "message_boards/{id}/messages.json"},
    {"method": "GET", "path": "messages/{id}"},
    {"method": "GET", "path": "my/assignments"},
    {"method": "GET", "path": "my/assignments.json"},
    {"method": "GET", "path": "my/assignments/completed"},
    {"method": "GET", "path": "my/assignments/completed.json"},
    {"method": "GET", "path": "my/assignments/due"},
    {"method": "GET", "path": "my/assignments/due.json"},
    {"method": "GET", "path": "buckets/{id}/recordings/{id}/bookmark"},
    {"method": "GET", "path": "buckets/{id}/recordings/{id}/bookmark.json"},
    {"method": "GET", "path": "my/bookmarks"},
    {"method": "GET", "path": "my/bookmarks.json"},
    {"method": "GET", "path": "recordings/{id}/bookmark"},
    {"method": "GET", "path": "recordings/{id}/bookmark.json"},
    {"method": "GET", "path": "my/notes"},
    {"method": "GET", "path": "my/notes.json"},
    {"method": "GET", "path": "my/readings"},
    {"method": "GET", "path": "my/readings.json"},
    {"method": "GET", "path": "my/readings/bubble_ups"},
    {"method": "GET", "path": "my/readings/bubble_ups.json"},
    {"method": "GET", "path": "people/{id}/out_of_office"},
    {"method": "GET", "path": "people/{id}/out_of_office.json"},
    {"method": "GET", "path": "circles/people"},
    {"method": "GET", "path": "circles/people.json"},
    {"method": "GET", "path": "my/preferences"},
    {"method": "GET", "path": "my/preferences.json"},
    {"method": "GET", "path": "my/profile"},
    {"method": "GET", "path": "my/profile.json"},
    {"method": "GET", "path": "people"},
    {"method": "GET", "path": "people.json"},
    {"method": "GET", "path": "people/{id}"},
    {"method": "GET", "path": "projects/{id}/people"},
    {"method": "GET", "path": "projects/{id}/people.json"},
    {"method": "GET", "path": "circles"},
    {"method": "GET", "path": "circles.json"},
    {"method": "GET", "path": "circles/{id}"},
    {"method": "GET", "path": "my/recent_projects"},
    {"method": "GET", "path": "my/recent_projects.json"},
    {"method": "GET", "path": "projects"},
    {"method": "GET", "path": "projects.json"},
    {"method": "GET", "path": "projects/{id}"},
    {"method": "GET", "path": "projects/{id}/logo"},
    {"method": "GET", "path": "projects/{id}/logo.json"},
    {"method": "GET", "path": "projects/{id}/wallpaper"},
    {"method": "GET", "path": "projects/{id}/wallpaper.json"},
    {"method": "GET", "path": "buckets/{id}/question_answers/{id}"},
    {"method": "GET", "path": "buckets/{id}/questions/{id}/answers"},
    {"method": "GET", "path": "buckets/{id}/questions/{id}/answers.json"},
    {"method": "GET", "path": "buckets/{id}/questions/{id}/answers/by"},
    {"method": "GET", "path": "buckets/{id}/questions/{id}/answers/by.json"},
    {"method": "GET", "path": "buckets/{id}/questions/{id}/answers/by/{id}"},
    {"method": "GET", "path": "question_answers/{id}"},
    {"method": "GET", "path": "questions/{id}/answers"},
    {"method": "GET", "path": "questions/{id}/answers.json"},
    {"method": "GET", "path": "questions/{id}/answers/by"},
    {"method": "GET", "path": "questions/{id}/answers/by.json"},
    {"method": "GET", "path": "questions/{id}/answers/by/{id}"},
    {"method": "GET", "path": "my/question_reminders"},
    {"method": "GET", "path": "my/question_reminders.json"},
    {"method": "GET", "path": "buckets/{id}/questionnaires/{id}"},
    {"method": "GET", "path": "questionnaires/{id}"},
    {"method": "GET", "path": "buckets/{id}/questionnaires/{id}/questions"},
    {"method": "GET", "path": "buckets/{id}/questionnaires/{id}/questions.json"},
    {"method": "GET", "path": "buckets/{id}/questions/{id}"},
    {"method": "GET", "path": "questionnaires/{id}/questions"},
    {"method": "GET", "path": "questionnaires/{id}/questions.json"},
    {"method": "GET", "path": "questions/{id}"},
    {"method": "GET", "path": "buckets/{id}/filings/{id}"},
    {"method": "GET", "path": "buckets/{id}/recordings/{id}"},
    {"method": "GET", "path": "filings/{id}"},
    {"method": "GET", "path": "recordings/{id}"},
    {"method": "GET", "path": "reports/schedules/upcoming"},
    {"method": "GET", "path": "reports/schedules/upcoming.json"},
    {"method": "GET", "path": "reports/todos/assigned"},
    {"method": "GET", "path": "reports/todos/assigned.json"},
    {"method": "GET", "path": "reports/todos/assigned/{id}"},
    {"method": "GET", "path": "reports/todos/overdue"},
    {"method": "GET", "path": "reports/todos/overdue.json"},
    {"method": "GET", "path": "buckets/{id}/schedule_entries/{id}"},
    {"method": "GET", "path": "buckets/{id}/schedules/{id}/entries"},
    {"method": "GET", "path": "buckets/{id}/schedules/{id}/entries.json"},
    {"method": "GET", "path": "schedule_entries/{id}"},
    {"method": "GET", "path": "schedules/{id}/entries"},
    {"method": "GET", "path": "schedules/{id}/entries.json"},
    {"method": "GET", "path": "buckets/{id}/schedules/{id}"},
    {"method": "GET", "path": "schedules/{id}"},
    {"method": "GET", "path": "search"},
    {"method": "GET", "path": "search.json"},
    {"method": "GET", "path": "searches/metadata"},
    {"method": "GET", "path": "searches/metadata.json"},
    {"method": "GET", "path": "buckets/{id}/recordings/{id}/subscription"},
    {"method": "GET", "path": "buckets/{id}/recordings/{id}/subscription.json"},
    {"method": "GET", "path": "recordings/{id}/subscription"},
    {"method": "GET", "path": "recordings/{id}/subscription.json"},
    {"method": "GET", "path": "buckets/{id}/recordings/{id}/subtasks"},
    {"method": "GET", "path": "buckets/{id}/recordings/{id}/subtasks.json"},
    {"method": "GET", "path": "buckets/{id}/subtasks/{id}"},
    {"method": "GET", "path": "recordings/{id}/subtasks"},
    {"method": "GET", "path": "recordings/{id}/subtasks.json"},
    {"method": "GET", "path": "subtasks/{id}"},
    {"method": "GET", "path": "templates"},
    {"method": "GET", "path": "templates.json"},
    {"method": "GET", "path": "templates/{id}"},
    {"method": "GET", "path": "templates/{id}/project_constructions/{id}"},
    {"method": "GET", "path": "buckets/{id}/recordings/{id}/templatifications/{id}"},
    {"method": "GET", "path": "recordings/{id}/templatifications/{id}"},
    {"method": "GET", "path": "projects/{id}/timeline"},
    {"method": "GET", "path": "projects/{id}/timeline.json"},
    {"method": "GET", "path": "reports/progress"},
    {"method": "GET", "path": "reports/progress.json"},
    {"method": "GET", "path": "reports/users/progress/{id}"},
    {"method": "GET", "path": "buckets/{id}/recordings/{id}/timesheet"},
    {"method": "GET", "path": "buckets/{id}/recordings/{id}/timesheet.json"},
    {"method": "GET", "path": "buckets/{id}/timesheet_entries/{id}"},
    {"method": "GET", "path": "projects/{id}/recordings/{id}/timesheet"},
    {"method": "GET", "path": "projects/{id}/recordings/{id}/timesheet.json"},
    {"method": "GET", "path": "projects/{id}/timesheet"},
    {"method": "GET", "path": "projects/{id}/timesheet.json"},
    {"method": "GET", "path": "recordings/{id}/timesheet"},
    {"method": "GET", "path": "recordings/{id}/timesheet.json"},
    {"method": "GET", "path": "reports/timesheet"},
    {"method": "GET", "path": "reports/timesheet.json"},
    {"method": "GET", "path": "timesheet_entries/{id}"},
    {"method": "GET", "path": "buckets/{id}/todolists/{id}"},
    {"method": "GET", "path": "buckets/{id}/todolists/{id}/groups"},
    {"method": "GET", "path": "buckets/{id}/todolists/{id}/groups.json"},
    {"method": "GET", "path": "todolists/{id}"},
    {"method": "GET", "path": "todolists/{id}/groups"},
    {"method": "GET", "path": "todolists/{id}/groups.json"},
    {"method": "GET", "path": "template_library/copies/{id}"},
    {"method": "GET", "path": "template_library/todolists"},
    {"method": "GET", "path": "template_library/todolists.json"},
    {"method": "GET", "path": "buckets/{id}/todosets/{id}/todolists"},
    {"method": "GET", "path": "buckets/{id}/todosets/{id}/todolists.json"},
    {"method": "GET", "path": "todosets/{id}/todolists"},
    {"method": "GET", "path": "todosets/{id}/todolists.json"},
    {"method": "GET", "path": "buckets/{id}/todosets/{id}"},
    {"method": "GET", "path": "todosets/{id}"},
    {"method": "GET", "path": "buckets/{id}/todolists/{id}/todos"},
    {"method": "GET", "path": "buckets/{id}/todolists/{id}/todos.json"},
    {"method": "GET", "path": "buckets/{id}/todos/{id}"},
    {"method": "GET", "path": "todolists/{id}/todos"},
    {"method": "GET", "path": "todolists/{id}/todos.json"},
    {"method": "GET", "path": "todos/{id}"},
    {"method": "GET", "path": "buckets/{id}/dock/tools/{id}"},
    {"method": "GET", "path": "dock/tools/{id}"},
    {"method": "GET", "path": "buckets/{id}/uploads/{id}"},
    {"method": "GET", "path": "buckets/{id}/uploads/{id}/versions"},
    {"method": "GET", "path": "buckets/{id}/uploads/{id}/versions.json"},
    {"method": "GET", "path": "buckets/{id}/vaults/{id}/uploads"},
    {"method": "GET", "path": "buckets/{id}/vaults/{id}/uploads.json"},
    {"method": "GET", "path": "uploads/{id}"},
    {"method": "GET", "path": "uploads/{id}/versions"},
    {"method": "GET", "path": "uploads/{id}/versions.json"},
    {"method": "GET", "path": "vaults/{id}/uploads"},
    {"method": "GET", "path": "vaults/{id}/uploads.json"},
    {"method": "GET", "path": "buckets/{id}/vaults/{id}"},
    {"method": "GET", "path": "buckets/{id}/vaults/{id}/vaults"},
    {"method": "GET", "path": "buckets/{id}/vaults/{id}/vaults.json"},
    {"method": "GET", "path": "vaults/{id}"},
    {"method": "GET", "path": "vaults/{id}/vaults"},
    {"method": "GET", "path": "vaults/{id}/vaults.json"},
    {"method": "GET", "path": "buckets/{id}/webhooks"},
    {"method": "GET", "path": "buckets/{id}/webhooks.json"},
    {"method": "GET", "path": "buckets/{id}/webhooks/{id}"},
    {"method": "GET", "path": "webhooks"},
    {"method": "GET", "path": "webhooks.json"},
    {"method": "GET", "path": "webhooks/{id}"}
  ],
  "deny": []
}
```

## Endpoints

The Basecamp endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | account | read | account | Get account. |
| GET | account.json | read | account | Get account. |
| PUT | account/logo | write | account | Update account logo. |
| DELETE | account/logo | write | account | Remove account logo. |
| PUT | account/logo.json | write | account | Update account logo. |
| DELETE | account/logo.json | write | account | Remove account logo. |
| PUT | account/name | write | account | Update account name. |
| PUT | account/name.json | write | account | Update account name. |
| POST | attachments | write | attachments | Create an attachment. |
| POST | attachments.json | write | attachments | Create an attachment. |
| GET | buckets/{id}/recordings/{id}/backlinks | read | backlinks | Legacy project-scoped routes. |
| GET | buckets/{id}/recordings/{id}/backlinks.json | read | backlinks | Legacy project-scoped routes. |
| GET | recordings/{id}/backlinks | read | backlinks | Legacy project-scoped routes. |
| GET | recordings/{id}/backlinks.json | read | backlinks | Legacy project-scoped routes. |
| GET | boosts/{id} | read | boosts | Get a boost. |
| PUT | boosts/{id} | write | boosts | Update a boost. |
| DELETE | boosts/{id} | write | boosts | Destroy a boost. |
| GET | buckets/{id}/boosts/{id} | read | boosts | Get a boost. |
| PUT | buckets/{id}/boosts/{id} | write | boosts | Update a boost. |
| DELETE | buckets/{id}/boosts/{id} | write | boosts | Destroy a boost. |
| GET | buckets/{id}/recordings/{id}/boosts | read | boosts | Legacy project-scoped routes. |
| POST | buckets/{id}/recordings/{id}/boosts | write | boosts | Legacy project-scoped routes. |
| GET | buckets/{id}/recordings/{id}/boosts.json | read | boosts | Legacy project-scoped routes. |
| POST | buckets/{id}/recordings/{id}/boosts.json | write | boosts | Legacy project-scoped routes. |
| GET | buckets/{id}/recordings/{id}/events/{id}/boosts | read | boosts | Get boosts. |
| POST | buckets/{id}/recordings/{id}/events/{id}/boosts | write | boosts | Create a boost. |
| GET | buckets/{id}/recordings/{id}/events/{id}/boosts.json | read | boosts | Get boosts. |
| POST | buckets/{id}/recordings/{id}/events/{id}/boosts.json | write | boosts | Create a boost. |
| GET | recordings/{id}/boosts | read | boosts | Legacy project-scoped routes. |
| POST | recordings/{id}/boosts | write | boosts | Legacy project-scoped routes. |
| GET | recordings/{id}/boosts.json | read | boosts | Legacy project-scoped routes. |
| POST | recordings/{id}/boosts.json | write | boosts | Legacy project-scoped routes. |
| GET | recordings/{id}/events/{id}/boosts | read | boosts | Get boosts. |
| POST | recordings/{id}/events/{id}/boosts | write | boosts | Create a boost. |
| GET | recordings/{id}/events/{id}/boosts.json | read | boosts | Get boosts. |
| POST | recordings/{id}/events/{id}/boosts.json | write | boosts | Create a boost. |
| GET | buckets/{id}/calendars/{id} | read | calendars | Get a calendar. |
| PUT | buckets/{id}/calendars/{id} | write | calendars | Update a calendar. |
| GET | calendars/{id} | read | calendars | Get a calendar. |
| PUT | calendars/{id} | write | calendars | Update a calendar. |
| GET | buckets/{id}/chats | read | campfires | Get Campfires. |
| GET | buckets/{id}/chats.json | read | campfires | Get Campfires. |
| GET | buckets/{id}/chats/{id} | read | campfires | Legacy project-scoped routes. |
| GET | buckets/{id}/chats/{id}/lines | read | campfires | Legacy project-scoped routes. |
| POST | buckets/{id}/chats/{id}/lines | write | campfires | Legacy project-scoped routes. |
| GET | buckets/{id}/chats/{id}/lines.json | read | campfires | Legacy project-scoped routes. |
| POST | buckets/{id}/chats/{id}/lines.json | write | campfires | Legacy project-scoped routes. |
| GET | buckets/{id}/chats/{id}/lines/{id} | read | campfires | Legacy project-scoped routes. |
| PUT | buckets/{id}/chats/{id}/lines/{id} | write | campfires | Legacy project-scoped routes. |
| DELETE | buckets/{id}/chats/{id}/lines/{id} | write | campfires | Legacy project-scoped routes. |
| GET | buckets/{id}/chats/{id}/uploads | read | campfires | Legacy project-scoped routes. |
| POST | buckets/{id}/chats/{id}/uploads | write | campfires | Legacy project-scoped routes. |
| GET | buckets/{id}/chats/{id}/uploads.json | read | campfires | Legacy project-scoped routes. |
| POST | buckets/{id}/chats/{id}/uploads.json | write | campfires | Legacy project-scoped routes. |
| GET | chats | read | campfires | Get Campfires. |
| GET | chats.json | read | campfires | Get Campfires. |
| GET | chats/{id} | read | campfires | Legacy project-scoped routes. |
| GET | chats/{id}/lines | read | campfires | Legacy project-scoped routes. |
| POST | chats/{id}/lines | write | campfires | Legacy project-scoped routes. |
| GET | chats/{id}/lines.json | read | campfires | Legacy project-scoped routes. |
| POST | chats/{id}/lines.json | write | campfires | Legacy project-scoped routes. |
| GET | chats/{id}/lines/{id} | read | campfires | Legacy project-scoped routes. |
| PUT | chats/{id}/lines/{id} | write | campfires | Legacy project-scoped routes. |
| DELETE | chats/{id}/lines/{id} | write | campfires | Legacy project-scoped routes. |
| GET | chats/{id}/uploads | read | campfires | Legacy project-scoped routes. |
| POST | chats/{id}/uploads | write | campfires | Legacy project-scoped routes. |
| GET | chats/{id}/uploads.json | read | campfires | Legacy project-scoped routes. |
| POST | chats/{id}/uploads.json | write | campfires | Legacy project-scoped routes. |
| GET | buckets/{id}/card_tables/cards/{id} | read | card table cards | Legacy project-scoped routes. |
| PUT | buckets/{id}/card_tables/cards/{id} | write | card table cards | Legacy project-scoped routes. |
| POST | buckets/{id}/card_tables/cards/{id}/moves | write | card table cards | Legacy project-scoped routes. |
| POST | buckets/{id}/card_tables/cards/{id}/moves.json | write | card table cards | Legacy project-scoped routes. |
| GET | buckets/{id}/card_tables/lists/{id}/cards | read | card table cards | Legacy project-scoped routes. |
| POST | buckets/{id}/card_tables/lists/{id}/cards | write | card table cards | Legacy project-scoped routes. |
| GET | buckets/{id}/card_tables/lists/{id}/cards.json | read | card table cards | Legacy project-scoped routes. |
| POST | buckets/{id}/card_tables/lists/{id}/cards.json | write | card table cards | Legacy project-scoped routes. |
| GET | card_tables/cards/{id} | read | card table cards | Legacy project-scoped routes. |
| PUT | card_tables/cards/{id} | write | card table cards | Legacy project-scoped routes. |
| POST | card_tables/cards/{id}/moves | write | card table cards | Legacy project-scoped routes. |
| POST | card_tables/cards/{id}/moves.json | write | card table cards | Legacy project-scoped routes. |
| GET | card_tables/lists/{id}/cards | read | card table cards | Legacy project-scoped routes. |
| POST | card_tables/lists/{id}/cards | write | card table cards | Legacy project-scoped routes. |
| GET | card_tables/lists/{id}/cards.json | read | card table cards | Legacy project-scoped routes. |
| POST | card_tables/lists/{id}/cards.json | write | card table cards | Legacy project-scoped routes. |
| GET | buckets/{id}/card_tables/columns/{id} | read | card table columns | Legacy project-scoped routes. |
| PUT | buckets/{id}/card_tables/columns/{id} | write | card table columns | Legacy project-scoped routes. |
| PUT | buckets/{id}/card_tables/columns/{id}/color | write | card table columns | Legacy project-scoped routes. |
| PUT | buckets/{id}/card_tables/columns/{id}/color.json | write | card table columns | Legacy project-scoped routes. |
| POST | buckets/{id}/card_tables/columns/{id}/on_hold | write | card table columns | Legacy project-scoped routes. |
| DELETE | buckets/{id}/card_tables/columns/{id}/on_hold | write | card table columns | Legacy project-scoped routes. |
| POST | buckets/{id}/card_tables/columns/{id}/on_hold.json | write | card table columns | Legacy project-scoped routes. |
| DELETE | buckets/{id}/card_tables/columns/{id}/on_hold.json | write | card table columns | Legacy project-scoped routes. |
| POST | buckets/{id}/card_tables/lists/{id}/subscription | write | card table columns | Legacy project-scoped routes. |
| DELETE | buckets/{id}/card_tables/lists/{id}/subscription | write | card table columns | Legacy project-scoped routes. |
| POST | buckets/{id}/card_tables/lists/{id}/subscription.json | write | card table columns | Legacy project-scoped routes. |
| DELETE | buckets/{id}/card_tables/lists/{id}/subscription.json | write | card table columns | Legacy project-scoped routes. |
| POST | buckets/{id}/card_tables/{id}/columns | write | card table columns | Legacy project-scoped routes. |
| POST | buckets/{id}/card_tables/{id}/columns.json | write | card table columns | Legacy project-scoped routes. |
| POST | buckets/{id}/card_tables/{id}/moves | write | card table columns | Legacy project-scoped routes. |
| POST | buckets/{id}/card_tables/{id}/moves.json | write | card table columns | Legacy project-scoped routes. |
| GET | card_tables/columns/{id} | read | card table columns | Legacy project-scoped routes. |
| PUT | card_tables/columns/{id} | write | card table columns | Legacy project-scoped routes. |
| PUT | card_tables/columns/{id}/color | write | card table columns | Legacy project-scoped routes. |
| PUT | card_tables/columns/{id}/color.json | write | card table columns | Legacy project-scoped routes. |
| POST | card_tables/columns/{id}/on_hold | write | card table columns | Legacy project-scoped routes. |
| DELETE | card_tables/columns/{id}/on_hold | write | card table columns | Legacy project-scoped routes. |
| POST | card_tables/columns/{id}/on_hold.json | write | card table columns | Legacy project-scoped routes. |
| DELETE | card_tables/columns/{id}/on_hold.json | write | card table columns | Legacy project-scoped routes. |
| POST | card_tables/lists/{id}/subscription | write | card table columns | Legacy project-scoped routes. |
| DELETE | card_tables/lists/{id}/subscription | write | card table columns | Legacy project-scoped routes. |
| POST | card_tables/lists/{id}/subscription.json | write | card table columns | Legacy project-scoped routes. |
| DELETE | card_tables/lists/{id}/subscription.json | write | card table columns | Legacy project-scoped routes. |
| POST | card_tables/{id}/columns | write | card table columns | Legacy project-scoped routes. |
| POST | card_tables/{id}/columns.json | write | card table columns | Legacy project-scoped routes. |
| POST | card_tables/{id}/moves | write | card table columns | Legacy project-scoped routes. |
| POST | card_tables/{id}/moves.json | write | card table columns | Legacy project-scoped routes. |
| POST | buckets/{id}/card_tables/cards/{id}/positions | write | card table steps | Legacy project-scoped routes. |
| POST | buckets/{id}/card_tables/cards/{id}/positions.json | write | card table steps | Legacy project-scoped routes. |
| POST | buckets/{id}/card_tables/cards/{id}/steps | write | card table steps | Legacy project-scoped routes. |
| POST | buckets/{id}/card_tables/cards/{id}/steps.json | write | card table steps | Legacy project-scoped routes. |
| PUT | buckets/{id}/card_tables/steps/{id} | write | card table steps | Legacy project-scoped routes. |
| PUT | buckets/{id}/card_tables/steps/{id}/completions | write | card table steps | Legacy project-scoped routes. |
| PUT | buckets/{id}/card_tables/steps/{id}/completions.json | write | card table steps | Legacy project-scoped routes. |
| POST | card_tables/cards/{id}/positions | write | card table steps | Legacy project-scoped routes. |
| POST | card_tables/cards/{id}/positions.json | write | card table steps | Legacy project-scoped routes. |
| POST | card_tables/cards/{id}/steps | write | card table steps | Legacy project-scoped routes. |
| POST | card_tables/cards/{id}/steps.json | write | card table steps | Legacy project-scoped routes. |
| PUT | card_tables/steps/{id} | write | card table steps | Legacy project-scoped routes. |
| PUT | card_tables/steps/{id}/completions | write | card table steps | Legacy project-scoped routes. |
| PUT | card_tables/steps/{id}/completions.json | write | card table steps | Legacy project-scoped routes. |
| GET | template_library/card_tables | read | card table templates | Get the card table templates. |
| POST | template_library/card_tables | write | card table templates | Create a card table template. |
| GET | template_library/card_tables.json | read | card table templates | Get the card table templates. |
| POST | template_library/card_tables.json | write | card table templates | Create a card table template. |
| POST | template_library/copies | write | card table templates | Create a card table from a template. |
| POST | template_library/copies.json | write | card table templates | Create a card table from a template. |
| PUT | buckets/{id}/card_tables/wormholes/{id} | write | card table wormholes | Update a wormhole. |
| DELETE | buckets/{id}/card_tables/wormholes/{id} | write | card table wormholes | Delete a wormhole. |
| POST | buckets/{id}/card_tables/{id}/wormholes | write | card table wormholes | Create a wormhole. |
| POST | buckets/{id}/card_tables/{id}/wormholes.json | write | card table wormholes | Create a wormhole. |
| PUT | card_tables/wormholes/{id} | write | card table wormholes | Update a wormhole. |
| DELETE | card_tables/wormholes/{id} | write | card table wormholes | Delete a wormhole. |
| POST | card_tables/{id}/wormholes | write | card table wormholes | Create a wormhole. |
| POST | card_tables/{id}/wormholes.json | write | card table wormholes | Create a wormhole. |
| GET | buckets/{id}/card_tables/{id} | read | card tables | Legacy project-scoped routes. |
| GET | card_tables/{id} | read | card tables | Legacy project-scoped routes. |
| GET | buckets/{id}/chats/{id}/integrations | write | chatbots | Get chatbots. Kept out of read: returns lines_url, which carries the chatbot key. |
| POST | buckets/{id}/chats/{id}/integrations | write | chatbots | Create a chatbot. |
| GET | buckets/{id}/chats/{id}/integrations.json | write | chatbots | Get chatbots. Kept out of read: returns lines_url, which carries the chatbot key. |
| POST | buckets/{id}/chats/{id}/integrations.json | write | chatbots | Create a chatbot. |
| GET | buckets/{id}/chats/{id}/integrations/{id} | write | chatbots | Get a chatbot. Kept out of read: returns lines_url, which carries the chatbot key. |
| PUT | buckets/{id}/chats/{id}/integrations/{id} | write | chatbots | Update a chatbot. |
| DELETE | buckets/{id}/chats/{id}/integrations/{id} | write | chatbots | Destroy a chatbot. |
| GET | chats/{id}/integrations | write | chatbots | Get chatbots. Kept out of read: returns lines_url, which carries the chatbot key. |
| POST | chats/{id}/integrations | write | chatbots | Create a chatbot. |
| GET | chats/{id}/integrations.json | write | chatbots | Get chatbots. Kept out of read: returns lines_url, which carries the chatbot key. |
| POST | chats/{id}/integrations.json | write | chatbots | Create a chatbot. |
| GET | chats/{id}/integrations/{id} | write | chatbots | Get a chatbot. Kept out of read: returns lines_url, which carries the chatbot key. |
| PUT | chats/{id}/integrations/{id} | write | chatbots | Update a chatbot. |
| DELETE | chats/{id}/integrations/{id} | write | chatbots | Destroy a chatbot. |
| POST | integrations/{id}/buckets/{id}/chats/{id}/lines | write | chatbots | Create a line. |
| POST | integrations/{id}/buckets/{id}/chats/{id}/lines.json | write | chatbots | Create a line. |
| GET | buckets/{id}/client/approvals | read | client approvals | Get client approvals. |
| GET | buckets/{id}/client/approvals.json | read | client approvals | Get client approvals. |
| GET | buckets/{id}/client/approvals/{id} | read | client approvals | Legacy project-scoped routes. |
| GET | client/approvals | read | client approvals | Get client approvals. |
| GET | client/approvals.json | read | client approvals | Get client approvals. |
| GET | client/approvals/{id} | read | client approvals | Legacy project-scoped routes. |
| GET | buckets/{id}/client/correspondences | read | client correspondences | Get client correspondences. |
| GET | buckets/{id}/client/correspondences.json | read | client correspondences | Get client correspondences. |
| GET | buckets/{id}/client/correspondences/{id} | read | client correspondences | Legacy project-scoped routes. |
| GET | client/correspondences | read | client correspondences | Get client correspondences. |
| GET | client/correspondences.json | read | client correspondences | Get client correspondences. |
| GET | client/correspondences/{id} | read | client correspondences | Legacy project-scoped routes. |
| GET | buckets/{id}/client/recordings/{id}/replies | read | client replies | Get client replies. |
| GET | buckets/{id}/client/recordings/{id}/replies.json | read | client replies | Get client replies. |
| GET | buckets/{id}/client/recordings/{id}/replies/{id} | read | client replies | Get a client reply. |
| GET | client/recordings/{id}/replies | read | client replies | Get client replies. |
| GET | client/recordings/{id}/replies.json | read | client replies | Get client replies. |
| GET | client/recordings/{id}/replies/{id} | read | client replies | Get a client reply. |
| PUT | buckets/{id}/recordings/{id}/client_visibility | write | client visibility | Legacy project-scoped routes. |
| PUT | buckets/{id}/recordings/{id}/client_visibility.json | write | client visibility | Legacy project-scoped routes. |
| PUT | recordings/{id}/client_visibility | write | client visibility | Legacy project-scoped routes. |
| PUT | recordings/{id}/client_visibility.json | write | client visibility | Legacy project-scoped routes. |
| GET | buckets/{id}/cloud_files/{id} | read | cloud files | Get a cloud file. |
| PUT | buckets/{id}/cloud_files/{id} | write | cloud files | Update a cloud file. |
| POST | buckets/{id}/vaults/{id}/cloud_files | write | cloud files | Create a cloud file. |
| POST | buckets/{id}/vaults/{id}/cloud_files.json | write | cloud files | Create a cloud file. |
| GET | cloud_files/{id} | read | cloud files | Get a cloud file. |
| PUT | cloud_files/{id} | write | cloud files | Update a cloud file. |
| POST | vaults/{id}/cloud_files | write | cloud files | Create a cloud file. |
| POST | vaults/{id}/cloud_files.json | write | cloud files | Create a cloud file. |
| GET | buckets/{id}/comments/{id} | read | comments | Legacy project-scoped routes. |
| PUT | buckets/{id}/comments/{id} | write | comments | Legacy project-scoped routes. |
| GET | buckets/{id}/recordings/{id}/comments | read | comments | Legacy project-scoped routes. |
| POST | buckets/{id}/recordings/{id}/comments | write | comments | Legacy project-scoped routes. |
| GET | buckets/{id}/recordings/{id}/comments.json | read | comments | Legacy project-scoped routes. |
| POST | buckets/{id}/recordings/{id}/comments.json | write | comments | Legacy project-scoped routes. |
| GET | comments/{id} | read | comments | Legacy project-scoped routes. |
| PUT | comments/{id} | write | comments | Legacy project-scoped routes. |
| GET | recordings/{id}/comments | read | comments | Legacy project-scoped routes. |
| POST | recordings/{id}/comments | write | comments | Legacy project-scoped routes. |
| GET | recordings/{id}/comments.json | read | comments | Legacy project-scoped routes. |
| POST | recordings/{id}/comments.json | write | comments | Legacy project-scoped routes. |
| GET | buckets/{id}/documents/{id} | read | documents | Legacy project-scoped routes. |
| PUT | buckets/{id}/documents/{id} | write | documents | Legacy project-scoped routes. |
| GET | buckets/{id}/vaults/{id}/documents | read | documents | Legacy project-scoped routes. |
| POST | buckets/{id}/vaults/{id}/documents | write | documents | Legacy project-scoped routes. |
| GET | buckets/{id}/vaults/{id}/documents.json | read | documents | Legacy project-scoped routes. |
| POST | buckets/{id}/vaults/{id}/documents.json | write | documents | Legacy project-scoped routes. |
| GET | documents/{id} | read | documents | Legacy project-scoped routes. |
| PUT | documents/{id} | write | documents | Legacy project-scoped routes. |
| GET | vaults/{id}/documents | read | documents | Legacy project-scoped routes. |
| POST | vaults/{id}/documents | write | documents | Legacy project-scoped routes. |
| GET | vaults/{id}/documents.json | read | documents | Legacy project-scoped routes. |
| POST | vaults/{id}/documents.json | write | documents | Legacy project-scoped routes. |
| GET | my/drafts | read | drafts | Get my drafts. |
| GET | my/drafts.json | read | drafts | Get my drafts. |
| POST | embeds | write | embeds | Create an embed. |
| POST | embeds.json | write | embeds | Create an embed. |
| GET | embeds/{id} | read | embeds | Get an embed. |
| GET | buckets/{id}/events | read | event feed | Poll events. |
| GET | buckets/{id}/events.json | read | event feed | Poll events. |
| POST | buckets/{id}/events/stream_ticket | write | event feed | Create a stream ticket. |
| POST | buckets/{id}/events/stream_ticket.json | write | event feed | Create a stream ticket. |
| GET | buckets/{id}/inbox | read | event feed | Poll the inbox. |
| GET | buckets/{id}/inbox.json | read | event feed | Poll the inbox. |
| GET | events | read | event feed | Poll events. |
| GET | events.json | read | event feed | Poll events. |
| POST | events/stream_ticket | write | event feed | Create a stream ticket. |
| POST | events/stream_ticket.json | write | event feed | Create a stream ticket. |
| GET | inbox | read | event feed | Poll the inbox. |
| GET | inbox.json | read | event feed | Poll the inbox. |
| GET | buckets/{id}/recordings/{id}/events | read | events | Legacy project-scoped routes. |
| GET | buckets/{id}/recordings/{id}/events.json | read | events | Legacy project-scoped routes. |
| GET | recordings/{id}/events | read | events | Legacy project-scoped routes. |
| GET | recordings/{id}/events.json | read | events | Legacy project-scoped routes. |
| GET | buckets/{id}/cards/completed | read | everything | Get cards by filter. |
| GET | buckets/{id}/cards/completed.json | read | everything | Get cards by filter. |
| GET | buckets/{id}/cards/no_due_date | read | everything | Get cards by filter. |
| GET | buckets/{id}/cards/no_due_date.json | read | everything | Get cards by filter. |
| GET | buckets/{id}/cards/not_now | read | everything | Get cards by filter. |
| GET | buckets/{id}/cards/not_now.json | read | everything | Get cards by filter. |
| GET | buckets/{id}/cards/open | read | everything | Get cards by filter. |
| GET | buckets/{id}/cards/open.json | read | everything | Get cards by filter. |
| GET | buckets/{id}/cards/overdue | read | everything | Get overdue cards. |
| GET | buckets/{id}/cards/overdue.json | read | everything | Get overdue cards. |
| GET | buckets/{id}/cards/unassigned | read | everything | Get cards by filter. |
| GET | buckets/{id}/cards/unassigned.json | read | everything | Get cards by filter. |
| GET | buckets/{id}/checkins | read | everything | List check-ins. |
| GET | buckets/{id}/checkins.json | read | everything | List check-ins. |
| GET | buckets/{id}/comments | read | everything | List comments. |
| GET | buckets/{id}/comments.json | read | everything | List comments. |
| GET | buckets/{id}/files | read | everything | List files. |
| GET | buckets/{id}/files.json | read | everything | List files. |
| GET | buckets/{id}/forwards | read | everything | List forwards. |
| GET | buckets/{id}/forwards.json | read | everything | List forwards. |
| GET | buckets/{id}/messages | read | everything | List messages. |
| GET | buckets/{id}/messages.json | read | everything | List messages. |
| GET | buckets/{id}/todos/completed | read | everything | Get to-dos by filter. |
| GET | buckets/{id}/todos/completed.json | read | everything | Get to-dos by filter. |
| GET | buckets/{id}/todos/no_due_date | read | everything | Get to-dos by filter. |
| GET | buckets/{id}/todos/no_due_date.json | read | everything | Get to-dos by filter. |
| GET | buckets/{id}/todos/open | read | everything | Get to-dos by filter. |
| GET | buckets/{id}/todos/open.json | read | everything | Get to-dos by filter. |
| GET | buckets/{id}/todos/overdue | read | everything | Get overdue to-dos. |
| GET | buckets/{id}/todos/overdue.json | read | everything | Get overdue to-dos. |
| GET | buckets/{id}/todos/unassigned | read | everything | Get to-dos by filter. |
| GET | buckets/{id}/todos/unassigned.json | read | everything | Get to-dos by filter. |
| GET | cards/completed | read | everything | Get cards by filter. |
| GET | cards/completed.json | read | everything | Get cards by filter. |
| GET | cards/no_due_date | read | everything | Get cards by filter. |
| GET | cards/no_due_date.json | read | everything | Get cards by filter. |
| GET | cards/not_now | read | everything | Get cards by filter. |
| GET | cards/not_now.json | read | everything | Get cards by filter. |
| GET | cards/open | read | everything | Get cards by filter. |
| GET | cards/open.json | read | everything | Get cards by filter. |
| GET | cards/overdue | read | everything | Get overdue cards. |
| GET | cards/overdue.json | read | everything | Get overdue cards. |
| GET | cards/unassigned | read | everything | Get cards by filter. |
| GET | cards/unassigned.json | read | everything | Get cards by filter. |
| GET | checkins | read | everything | List check-ins. |
| GET | checkins.json | read | everything | List check-ins. |
| GET | comments | read | everything | List comments. |
| GET | comments.json | read | everything | List comments. |
| GET | files | read | everything | List files. |
| GET | files.json | read | everything | List files. |
| GET | forwards | read | everything | List forwards. |
| GET | forwards.json | read | everything | List forwards. |
| GET | messages | read | everything | List messages. |
| GET | messages.json | read | everything | List messages. |
| GET | todos/completed | read | everything | Get to-dos by filter. |
| GET | todos/completed.json | read | everything | Get to-dos by filter. |
| GET | todos/no_due_date | read | everything | Get to-dos by filter. |
| GET | todos/no_due_date.json | read | everything | Get to-dos by filter. |
| GET | todos/open | read | everything | Get to-dos by filter. |
| GET | todos/open.json | read | everything | Get to-dos by filter. |
| GET | todos/overdue | read | everything | Get overdue to-dos. |
| GET | todos/overdue.json | read | everything | Get overdue to-dos. |
| GET | todos/unassigned | read | everything | Get to-dos by filter. |
| GET | todos/unassigned.json | read | everything | Get to-dos by filter. |
| GET | buckets/{id}/dock/doors | read | external links | Get external links in a project. |
| POST | buckets/{id}/dock/doors | write | external links | Create an external link. |
| GET | buckets/{id}/dock/doors.json | read | external links | Get external links in a project. |
| POST | buckets/{id}/dock/doors.json | write | external links | Create an external link. |
| GET | buckets/{id}/dock/doors/{id} | read | external links | Get an external link. |
| PUT | buckets/{id}/dock/doors/{id} | write | external links | Update an external link. |
| DELETE | buckets/{id}/dock/doors/{id} | write | external links | Trash an external link. |
| GET | dock/doors | read | external links | Get external links in a project. |
| POST | dock/doors | write | external links | Create an external link. |
| GET | dock/doors.json | read | external links | Get external links in a project. |
| POST | dock/doors.json | write | external links | Create an external link. |
| GET | dock/doors/{id} | read | external links | Get an external link. |
| PUT | dock/doors/{id} | write | external links | Update an external link. |
| DELETE | dock/doors/{id} | write | external links | Trash an external link. |
| GET | projects/recordings | read | external links | List external links across projects. |
| GET | projects/recordings.json | read | external links | List external links across projects. |
| GET | buckets/{id}/stacks | read | folders | Get folders. |
| POST | buckets/{id}/stacks | write | folders | Create a folder. |
| GET | buckets/{id}/stacks.json | read | folders | Get folders. |
| POST | buckets/{id}/stacks.json | write | folders | Create a folder. |
| GET | buckets/{id}/stacks/{id} | read | folders | Get a folder. |
| PUT | buckets/{id}/stacks/{id} | write | folders | Update a folder. |
| DELETE | buckets/{id}/stacks/{id} | write | folders | Delete a folder. |
| GET | stacks | read | folders | Get folders. |
| POST | stacks | write | folders | Create a folder. |
| GET | stacks.json | read | folders | Get folders. |
| POST | stacks.json | write | folders | Create a folder. |
| GET | stacks/{id} | read | folders | Get a folder. |
| PUT | stacks/{id} | write | folders | Update a folder. |
| DELETE | stacks/{id} | write | folders | Delete a folder. |
| GET | buckets/{id}/inbox_forwards/{id} | read | forwards | Legacy project-scoped routes. |
| GET | buckets/{id}/inboxes/{id}/inbox_forwards | read | forwards | Legacy project-scoped routes. |
| GET | buckets/{id}/inboxes/{id}/inbox_forwards.json | read | forwards | Legacy project-scoped routes. |
| GET | inbox_forwards/{id} | read | forwards | Legacy project-scoped routes. |
| GET | inboxes/{id}/inbox_forwards | read | forwards | Legacy project-scoped routes. |
| GET | inboxes/{id}/inbox_forwards.json | read | forwards | Legacy project-scoped routes. |
| GET | buckets/{id}/gauge_needles/{id} | read | gauges | Get a gauge needle. |
| PUT | buckets/{id}/gauge_needles/{id} | write | gauges | Update a gauge needle. |
| DELETE | buckets/{id}/gauge_needles/{id} | write | gauges | Destroy a gauge needle. |
| GET | gauge_needles/{id} | read | gauges | Get a gauge needle. |
| PUT | gauge_needles/{id} | write | gauges | Update a gauge needle. |
| DELETE | gauge_needles/{id} | write | gauges | Destroy a gauge needle. |
| PUT | projects/{id}/gauge | write | gauges | Toggle a gauge. |
| PUT | projects/{id}/gauge.json | write | gauges | Toggle a gauge. |
| GET | projects/{id}/gauge/needles | read | gauges | Get gauge needles. |
| POST | projects/{id}/gauge/needles | write | gauges | Create a gauge needle. |
| GET | projects/{id}/gauge/needles.json | read | gauges | Get gauge needles. |
| POST | projects/{id}/gauge/needles.json | write | gauges | Create a gauge needle. |
| GET | projects/{id}/gauge/needles/{id} | read | gauges | Legacy project-scoped routes. |
| PUT | projects/{id}/gauge/needles/{id} | write | gauges | Legacy project-scoped routes. |
| DELETE | projects/{id}/gauge/needles/{id} | write | gauges | Legacy project-scoped routes. |
| GET | reports/gauges | read | gauges | Get gauges. |
| GET | reports/gauges.json | read | gauges | Get gauges. |
| GET | buckets/{id}/google_documents/{id} | read | google documents | Get a Google document. |
| PUT | buckets/{id}/google_documents/{id} | write | google documents | Update a Google document. |
| POST | buckets/{id}/vaults/{id}/google_documents | write | google documents | Create a Google document. |
| POST | buckets/{id}/vaults/{id}/google_documents.json | write | google documents | Create a Google document. |
| GET | google_documents/{id} | read | google documents | Get a Google document. |
| PUT | google_documents/{id} | write | google documents | Update a Google document. |
| POST | vaults/{id}/google_documents | write | google documents | Create a Google document. |
| POST | vaults/{id}/google_documents.json | write | google documents | Create a Google document. |
| GET | buckets/{id}/todosets/{id}/hill | read | hill charts | Get hill chart. |
| GET | buckets/{id}/todosets/{id}/hill.json | read | hill charts | Get hill chart. |
| PUT | buckets/{id}/todosets/{id}/hills/settings | write | hill charts | Update hill chart settings. |
| PUT | buckets/{id}/todosets/{id}/hills/settings.json | write | hill charts | Update hill chart settings. |
| GET | buckets/{id}/todosets/{id}/hills/versions | read | hill charts | Get hill chart progress updates. |
| POST | buckets/{id}/todosets/{id}/hills/versions | write | hill charts | Create a hill chart progress update. |
| GET | buckets/{id}/todosets/{id}/hills/versions.json | read | hill charts | Get hill chart progress updates. |
| POST | buckets/{id}/todosets/{id}/hills/versions.json | write | hill charts | Create a hill chart progress update. |
| GET | buckets/{id}/todosets/{id}/hills/versions/{id} | read | hill charts | Get a hill chart progress update. |
| GET | todosets/{id}/hill | read | hill charts | Get hill chart. |
| GET | todosets/{id}/hill.json | read | hill charts | Get hill chart. |
| PUT | todosets/{id}/hills/settings | write | hill charts | Update hill chart settings. |
| PUT | todosets/{id}/hills/settings.json | write | hill charts | Update hill chart settings. |
| GET | todosets/{id}/hills/versions | read | hill charts | Get hill chart progress updates. |
| POST | todosets/{id}/hills/versions | write | hill charts | Create a hill chart progress update. |
| GET | todosets/{id}/hills/versions.json | read | hill charts | Get hill chart progress updates. |
| POST | todosets/{id}/hills/versions.json | write | hill charts | Create a hill chart progress update. |
| GET | todosets/{id}/hills/versions/{id} | read | hill charts | Get a hill chart progress update. |
| GET | buckets/{id}/inbox_forwards/{id}/replies | read | inbox replies | Legacy project-scoped routes. |
| GET | buckets/{id}/inbox_forwards/{id}/replies.json | read | inbox replies | Legacy project-scoped routes. |
| GET | buckets/{id}/inbox_forwards/{id}/replies/{id} | read | inbox replies | Legacy project-scoped routes. |
| GET | inbox_forwards/{id}/replies | read | inbox replies | Legacy project-scoped routes. |
| GET | inbox_forwards/{id}/replies.json | read | inbox replies | Legacy project-scoped routes. |
| GET | inbox_forwards/{id}/replies/{id} | read | inbox replies | Legacy project-scoped routes. |
| GET | buckets/{id}/inboxes/{id} | read | inboxes | Legacy project-scoped routes. |
| GET | inboxes/{id} | read | inboxes | Legacy project-scoped routes. |
| GET | lineup/markers | read | lineup markers | List markers. |
| POST | lineup/markers | write | lineup markers | Create a marker. |
| GET | lineup/markers.json | read | lineup markers | List markers. |
| POST | lineup/markers.json | write | lineup markers | Create a marker. |
| PUT | lineup/markers/{id} | write | lineup markers | Update a marker. |
| DELETE | lineup/markers/{id} | write | lineup markers | Destroy a marker. |
| GET | buckets/{id}/message_boards/{id} | read | message boards | Legacy project-scoped routes. |
| GET | message_boards/{id} | read | message boards | Legacy project-scoped routes. |
| GET | buckets/{id}/categories | read | message types | Get message types. |
| POST | buckets/{id}/categories | write | message types | Create a message type. |
| GET | buckets/{id}/categories.json | read | message types | Get message types. |
| POST | buckets/{id}/categories.json | write | message types | Create a message type. |
| GET | buckets/{id}/categories/{id} | read | message types | Get a message type. |
| PUT | buckets/{id}/categories/{id} | write | message types | Update a message type. |
| DELETE | buckets/{id}/categories/{id} | write | message types | Destroy a message type. |
| GET | categories | read | message types | Get message types. |
| POST | categories | write | message types | Create a message type. |
| GET | categories.json | read | message types | Get message types. |
| POST | categories.json | write | message types | Create a message type. |
| GET | categories/{id} | read | message types | Get a message type. |
| PUT | categories/{id} | write | message types | Update a message type. |
| DELETE | categories/{id} | write | message types | Destroy a message type. |
| GET | buckets/{id}/message_boards/{id}/messages | read | messages | Legacy project-scoped routes. |
| POST | buckets/{id}/message_boards/{id}/messages | write | messages | Legacy project-scoped routes. |
| GET | buckets/{id}/message_boards/{id}/messages.json | read | messages | Legacy project-scoped routes. |
| POST | buckets/{id}/message_boards/{id}/messages.json | write | messages | Legacy project-scoped routes. |
| GET | buckets/{id}/messages/{id} | read | messages | Legacy project-scoped routes. |
| PUT | buckets/{id}/messages/{id} | write | messages | Legacy project-scoped routes. |
| POST | buckets/{id}/recordings/{id}/pin | write | messages | Legacy project-scoped routes. |
| DELETE | buckets/{id}/recordings/{id}/pin | write | messages | Legacy project-scoped routes. |
| POST | buckets/{id}/recordings/{id}/pin.json | write | messages | Legacy project-scoped routes. |
| DELETE | buckets/{id}/recordings/{id}/pin.json | write | messages | Legacy project-scoped routes. |
| GET | message_boards/{id}/messages | read | messages | Legacy project-scoped routes. |
| POST | message_boards/{id}/messages | write | messages | Legacy project-scoped routes. |
| GET | message_boards/{id}/messages.json | read | messages | Legacy project-scoped routes. |
| POST | message_boards/{id}/messages.json | write | messages | Legacy project-scoped routes. |
| GET | messages/{id} | read | messages | Legacy project-scoped routes. |
| PUT | messages/{id} | write | messages | Legacy project-scoped routes. |
| POST | recordings/{id}/pin | write | messages | Legacy project-scoped routes. |
| DELETE | recordings/{id}/pin | write | messages | Legacy project-scoped routes. |
| POST | recordings/{id}/pin.json | write | messages | Legacy project-scoped routes. |
| DELETE | recordings/{id}/pin.json | write | messages | Legacy project-scoped routes. |
| GET | my/assignments | read | my assignments | Get assignments. |
| GET | my/assignments.json | read | my assignments | Get assignments. |
| GET | my/assignments/completed | read | my assignments | Get completed assignments. |
| GET | my/assignments/completed.json | read | my assignments | Get completed assignments. |
| GET | my/assignments/due | read | my assignments | Get due assignments. |
| GET | my/assignments/due.json | read | my assignments | Get due assignments. |
| POST | my/priorities | write | my assignments | Prioritize an assignment. |
| POST | my/priorities.json | write | my assignments | Prioritize an assignment. |
| DELETE | my/priorities/{id} | write | my assignments | Deprioritize an assignment. |
| POST | my/priority_moves | write | my assignments | Reorder Up Next. |
| POST | my/priority_moves.json | write | my assignments | Reorder Up Next. |
| GET | buckets/{id}/recordings/{id}/bookmark | read | my bookmarks | Get a bookmark. |
| POST | buckets/{id}/recordings/{id}/bookmark | write | my bookmarks | Create a bookmark. |
| DELETE | buckets/{id}/recordings/{id}/bookmark | write | my bookmarks | Delete a bookmark. |
| GET | buckets/{id}/recordings/{id}/bookmark.json | read | my bookmarks | Get a bookmark. |
| POST | buckets/{id}/recordings/{id}/bookmark.json | write | my bookmarks | Create a bookmark. |
| DELETE | buckets/{id}/recordings/{id}/bookmark.json | write | my bookmarks | Delete a bookmark. |
| GET | my/bookmarks | read | my bookmarks | Get bookmarks. |
| GET | my/bookmarks.json | read | my bookmarks | Get bookmarks. |
| GET | recordings/{id}/bookmark | read | my bookmarks | Get a bookmark. |
| POST | recordings/{id}/bookmark | write | my bookmarks | Create a bookmark. |
| DELETE | recordings/{id}/bookmark | write | my bookmarks | Delete a bookmark. |
| GET | recordings/{id}/bookmark.json | read | my bookmarks | Get a bookmark. |
| POST | recordings/{id}/bookmark.json | write | my bookmarks | Create a bookmark. |
| DELETE | recordings/{id}/bookmark.json | write | my bookmarks | Delete a bookmark. |
| GET | my/notes | read | my notes | Get the note. |
| PUT | my/notes | write | my notes | Update the note. |
| GET | my/notes.json | read | my notes | Get the note. |
| PUT | my/notes.json | write | my notes | Update the note. |
| GET | my/readings | read | my notifications | Get notifications. |
| GET | my/readings.json | read | my notifications | Get notifications. |
| GET | my/readings/bubble_ups | read | my notifications | Get bubble-ups. |
| GET | my/readings/bubble_ups.json | read | my notifications | Get bubble-ups. |
| PUT | my/unreads | write | my notifications | Mark as read. |
| PUT | my/unreads.json | write | my notifications | Mark as read. |
| GET | people/{id}/out_of_office | read | out of office | Get out of office. |
| POST | people/{id}/out_of_office | write | out of office | Enable out of office. |
| DELETE | people/{id}/out_of_office | write | out of office | Disable out of office. |
| GET | people/{id}/out_of_office.json | read | out of office | Get out of office. |
| POST | people/{id}/out_of_office.json | write | out of office | Enable out of office. |
| DELETE | people/{id}/out_of_office.json | write | out of office | Disable out of office. |
| POST | account/enrollments/people | write | people | Enroll people. |
| POST | account/enrollments/people.json | write | people | Enroll people. |
| POST | admissions | write | people | Join a project. |
| POST | admissions.json | write | people | Join a project. |
| POST | buckets/{id}/admissions | write | people | Join a project. |
| POST | buckets/{id}/admissions.json | write | people | Join a project. |
| GET | circles/people | read | people | Get pingable people. |
| GET | circles/people.json | read | people | Get pingable people. |
| GET | my/preferences | read | people | Get my preferences. |
| PUT | my/preferences | write | people | Update my preferences. |
| GET | my/preferences.json | read | people | Get my preferences. |
| PUT | my/preferences.json | write | people | Update my preferences. |
| GET | my/profile | read | people | Get my personal info. |
| PUT | my/profile | write | people | Update my personal info. |
| GET | my/profile.json | read | people | Get my personal info. |
| PUT | my/profile.json | write | people | Update my personal info. |
| GET | people | read | people | Get all people. |
| GET | people.json | read | people | Get all people. |
| GET | people/{id} | read | people | Get person. |
| POST | projects/{id}/client_enablement | write | people | Enable or disable clients on a project. |
| DELETE | projects/{id}/client_enablement | write | people | Enable or disable clients on a project. |
| POST | projects/{id}/client_enablement.json | write | people | Enable or disable clients on a project. |
| DELETE | projects/{id}/client_enablement.json | write | people | Enable or disable clients on a project. |
| GET | projects/{id}/people | read | people | Get people on a project. |
| GET | projects/{id}/people.json | read | people | Get people on a project. |
| PUT | projects/{id}/people/client_users | write | people | Add and remove clients on a project. |
| PUT | projects/{id}/people/client_users.json | write | people | Add and remove clients on a project. |
| PUT | projects/{id}/people/users | write | people | Update who can access a project. |
| PUT | projects/{id}/people/users.json | write | people | Update who can access a project. |
| GET | circles | read | pings | Get Pings. |
| POST | circles | write | pings | Create a Ping. |
| GET | circles.json | read | pings | Get Pings. |
| POST | circles.json | write | pings | Create a Ping. |
| GET | circles/{id} | read | pings | Get a Ping. |
| GET | my/recent_projects | read | projects | Get recent projects. |
| GET | my/recent_projects.json | read | projects | Get recent projects. |
| GET | projects | read | projects | Get all projects. |
| POST | projects | write | projects | Create a project. |
| GET | projects.json | read | projects | Get all projects. |
| POST | projects.json | write | projects | Create a project. |
| GET | projects/{id} | read | projects | Get a project. |
| PUT | projects/{id} | write | projects | Update a project. |
| DELETE | projects/{id} | write | projects | Trash a project. |
| GET | projects/{id}/logo | read | projects | Get project logo. |
| PUT | projects/{id}/logo | write | projects | Update project logo. |
| DELETE | projects/{id}/logo | write | projects | Remove project logo. |
| GET | projects/{id}/logo.json | read | projects | Get project logo. |
| PUT | projects/{id}/logo.json | write | projects | Update project logo. |
| DELETE | projects/{id}/logo.json | write | projects | Remove project logo. |
| POST | projects/{id}/recent_visit | write | projects | Record a project visit. |
| POST | projects/{id}/recent_visit.json | write | projects | Record a project visit. |
| PUT | projects/{id}/status/active | write | projects | Unarchive a project. |
| PUT | projects/{id}/status/active.json | write | projects | Unarchive a project. |
| PUT | projects/{id}/status/archived | write | projects | Archive a project. |
| PUT | projects/{id}/status/archived.json | write | projects | Archive a project. |
| GET | projects/{id}/wallpaper | read | projects | Get project wallpaper. |
| PUT | projects/{id}/wallpaper | write | projects | Update project wallpaper. |
| DELETE | projects/{id}/wallpaper | write | projects | Remove project wallpaper. |
| GET | projects/{id}/wallpaper.json | read | projects | Get project wallpaper. |
| PUT | projects/{id}/wallpaper.json | write | projects | Update project wallpaper. |
| DELETE | projects/{id}/wallpaper.json | write | projects | Remove project wallpaper. |
| GET | buckets/{id}/question_answers/{id} | read | question answers | Legacy project-scoped routes. |
| PUT | buckets/{id}/question_answers/{id} | write | question answers | Legacy project-scoped routes. |
| GET | buckets/{id}/questions/{id}/answers | read | question answers | Legacy project-scoped routes. |
| POST | buckets/{id}/questions/{id}/answers | write | question answers | Legacy project-scoped routes. |
| GET | buckets/{id}/questions/{id}/answers.json | read | question answers | Legacy project-scoped routes. |
| POST | buckets/{id}/questions/{id}/answers.json | write | question answers | Legacy project-scoped routes. |
| GET | buckets/{id}/questions/{id}/answers/by | read | question answers | Legacy project-scoped routes. |
| GET | buckets/{id}/questions/{id}/answers/by.json | read | question answers | Legacy project-scoped routes. |
| GET | buckets/{id}/questions/{id}/answers/by/{id} | read | question answers | Legacy project-scoped routes. |
| GET | question_answers/{id} | read | question answers | Legacy project-scoped routes. |
| PUT | question_answers/{id} | write | question answers | Legacy project-scoped routes. |
| GET | questions/{id}/answers | read | question answers | Legacy project-scoped routes. |
| POST | questions/{id}/answers | write | question answers | Legacy project-scoped routes. |
| GET | questions/{id}/answers.json | read | question answers | Legacy project-scoped routes. |
| POST | questions/{id}/answers.json | write | question answers | Legacy project-scoped routes. |
| GET | questions/{id}/answers/by | read | question answers | Legacy project-scoped routes. |
| GET | questions/{id}/answers/by.json | read | question answers | Legacy project-scoped routes. |
| GET | questions/{id}/answers/by/{id} | read | question answers | Legacy project-scoped routes. |
| GET | my/question_reminders | read | question reminders | Get question reminders. |
| GET | my/question_reminders.json | read | question reminders | Get question reminders. |
| GET | buckets/{id}/questionnaires/{id} | read | questionnaires | Legacy project-scoped routes. |
| GET | questionnaires/{id} | read | questionnaires | Legacy project-scoped routes. |
| GET | buckets/{id}/questionnaires/{id}/questions | read | questions | Legacy project-scoped routes. |
| POST | buckets/{id}/questionnaires/{id}/questions | write | questions | Legacy project-scoped routes. |
| GET | buckets/{id}/questionnaires/{id}/questions.json | read | questions | Legacy project-scoped routes. |
| POST | buckets/{id}/questionnaires/{id}/questions.json | write | questions | Legacy project-scoped routes. |
| GET | buckets/{id}/questions/{id} | read | questions | Legacy project-scoped routes. |
| PUT | buckets/{id}/questions/{id} | write | questions | Legacy project-scoped routes. |
| PUT | buckets/{id}/questions/{id}/notification_settings | write | questions | Legacy project-scoped routes. |
| PUT | buckets/{id}/questions/{id}/notification_settings.json | write | questions | Legacy project-scoped routes. |
| POST | buckets/{id}/questions/{id}/pause | write | questions | Legacy project-scoped routes. |
| DELETE | buckets/{id}/questions/{id}/pause | write | questions | Legacy project-scoped routes. |
| POST | buckets/{id}/questions/{id}/pause.json | write | questions | Legacy project-scoped routes. |
| DELETE | buckets/{id}/questions/{id}/pause.json | write | questions | Legacy project-scoped routes. |
| GET | questionnaires/{id}/questions | read | questions | Legacy project-scoped routes. |
| POST | questionnaires/{id}/questions | write | questions | Legacy project-scoped routes. |
| GET | questionnaires/{id}/questions.json | read | questions | Legacy project-scoped routes. |
| POST | questionnaires/{id}/questions.json | write | questions | Legacy project-scoped routes. |
| GET | questions/{id} | read | questions | Legacy project-scoped routes. |
| PUT | questions/{id} | write | questions | Legacy project-scoped routes. |
| PUT | questions/{id}/notification_settings | write | questions | Legacy project-scoped routes. |
| PUT | questions/{id}/notification_settings.json | write | questions | Legacy project-scoped routes. |
| POST | questions/{id}/pause | write | questions | Legacy project-scoped routes. |
| DELETE | questions/{id}/pause | write | questions | Legacy project-scoped routes. |
| POST | questions/{id}/pause.json | write | questions | Legacy project-scoped routes. |
| DELETE | questions/{id}/pause.json | write | questions | Legacy project-scoped routes. |
| GET | buckets/{id}/filings/{id} | read | recordings | Get a filing. |
| GET | buckets/{id}/recordings/{id} | read | recordings | Legacy project-scoped routes. |
| POST | buckets/{id}/recordings/{id}/copies | write | recordings | Legacy project-scoped routes. |
| POST | buckets/{id}/recordings/{id}/copies.json | write | recordings | Legacy project-scoped routes. |
| POST | buckets/{id}/recordings/{id}/moves | write | recordings | Legacy project-scoped routes. |
| POST | buckets/{id}/recordings/{id}/moves.json | write | recordings | Legacy project-scoped routes. |
| PUT | buckets/{id}/recordings/{id}/status/active | write | recordings | Legacy project-scoped routes. |
| PUT | buckets/{id}/recordings/{id}/status/active.json | write | recordings | Legacy project-scoped routes. |
| PUT | buckets/{id}/recordings/{id}/status/archived | write | recordings | Legacy project-scoped routes. |
| PUT | buckets/{id}/recordings/{id}/status/archived.json | write | recordings | Legacy project-scoped routes. |
| PUT | buckets/{id}/recordings/{id}/status/trashed | write | recordings | Legacy project-scoped routes. |
| PUT | buckets/{id}/recordings/{id}/status/trashed.json | write | recordings | Legacy project-scoped routes. |
| GET | filings/{id} | read | recordings | Get a filing. |
| GET | recordings/{id} | read | recordings | Legacy project-scoped routes. |
| POST | recordings/{id}/copies | write | recordings | Legacy project-scoped routes. |
| POST | recordings/{id}/copies.json | write | recordings | Legacy project-scoped routes. |
| POST | recordings/{id}/moves | write | recordings | Legacy project-scoped routes. |
| POST | recordings/{id}/moves.json | write | recordings | Legacy project-scoped routes. |
| PUT | recordings/{id}/status/active | write | recordings | Legacy project-scoped routes. |
| PUT | recordings/{id}/status/active.json | write | recordings | Legacy project-scoped routes. |
| PUT | recordings/{id}/status/archived | write | recordings | Legacy project-scoped routes. |
| PUT | recordings/{id}/status/archived.json | write | recordings | Legacy project-scoped routes. |
| PUT | recordings/{id}/status/trashed | write | recordings | Legacy project-scoped routes. |
| PUT | recordings/{id}/status/trashed.json | write | recordings | Legacy project-scoped routes. |
| GET | reports/schedules/upcoming | read | reports | Get upcoming schedule. |
| GET | reports/schedules/upcoming.json | read | reports | Get upcoming schedule. |
| GET | reports/todos/assigned | read | reports | Get to-do assignments. |
| GET | reports/todos/assigned.json | read | reports | Get to-do assignments. |
| GET | reports/todos/assigned/{id} | read | reports | Get to-do assignments for a person. |
| GET | reports/todos/overdue | read | reports | Get overdue to-dos. |
| GET | reports/todos/overdue.json | read | reports | Get overdue to-dos. |
| GET | buckets/{id}/schedule_entries/{id} | read | schedule entries | Legacy project-scoped routes. |
| PUT | buckets/{id}/schedule_entries/{id} | write | schedule entries | Legacy project-scoped routes. |
| GET | buckets/{id}/schedules/{id}/entries | read | schedule entries | Legacy project-scoped routes. |
| POST | buckets/{id}/schedules/{id}/entries | write | schedule entries | Legacy project-scoped routes. |
| GET | buckets/{id}/schedules/{id}/entries.json | read | schedule entries | Legacy project-scoped routes. |
| POST | buckets/{id}/schedules/{id}/entries.json | write | schedule entries | Legacy project-scoped routes. |
| GET | schedule_entries/{id} | read | schedule entries | Legacy project-scoped routes. |
| PUT | schedule_entries/{id} | write | schedule entries | Legacy project-scoped routes. |
| GET | schedules/{id}/entries | read | schedule entries | Legacy project-scoped routes. |
| POST | schedules/{id}/entries | write | schedule entries | Legacy project-scoped routes. |
| GET | schedules/{id}/entries.json | read | schedule entries | Legacy project-scoped routes. |
| POST | schedules/{id}/entries.json | write | schedule entries | Legacy project-scoped routes. |
| GET | buckets/{id}/schedules/{id} | read | schedules | Legacy project-scoped routes. |
| PUT | buckets/{id}/schedules/{id} | write | schedules | Legacy project-scoped routes. |
| GET | schedules/{id} | read | schedules | Legacy project-scoped routes. |
| PUT | schedules/{id} | write | schedules | Legacy project-scoped routes. |
| GET | search | read | search | Search recordings. |
| GET | search.json | read | search | Search recordings. |
| GET | searches/metadata | read | search | Get search metadata. |
| GET | searches/metadata.json | read | search | Get search metadata. |
| POST | buckets/{id}/recordings/{id}/spotlight | write | spotlights | Legacy project-scoped routes. |
| DELETE | buckets/{id}/recordings/{id}/spotlight | write | spotlights | Legacy project-scoped routes. |
| POST | buckets/{id}/recordings/{id}/spotlight.json | write | spotlights | Legacy project-scoped routes. |
| DELETE | buckets/{id}/recordings/{id}/spotlight.json | write | spotlights | Legacy project-scoped routes. |
| POST | recordings/{id}/spotlight | write | spotlights | Legacy project-scoped routes. |
| DELETE | recordings/{id}/spotlight | write | spotlights | Legacy project-scoped routes. |
| POST | recordings/{id}/spotlight.json | write | spotlights | Legacy project-scoped routes. |
| DELETE | recordings/{id}/spotlight.json | write | spotlights | Legacy project-scoped routes. |
| GET | buckets/{id}/recordings/{id}/subscription | read | subscriptions | Legacy project-scoped routes. |
| POST | buckets/{id}/recordings/{id}/subscription | write | subscriptions | Legacy project-scoped routes. |
| PUT | buckets/{id}/recordings/{id}/subscription | write | subscriptions | Legacy project-scoped routes. |
| DELETE | buckets/{id}/recordings/{id}/subscription | write | subscriptions | Legacy project-scoped routes. |
| GET | buckets/{id}/recordings/{id}/subscription.json | read | subscriptions | Legacy project-scoped routes. |
| POST | buckets/{id}/recordings/{id}/subscription.json | write | subscriptions | Legacy project-scoped routes. |
| PUT | buckets/{id}/recordings/{id}/subscription.json | write | subscriptions | Legacy project-scoped routes. |
| DELETE | buckets/{id}/recordings/{id}/subscription.json | write | subscriptions | Legacy project-scoped routes. |
| GET | recordings/{id}/subscription | read | subscriptions | Legacy project-scoped routes. |
| POST | recordings/{id}/subscription | write | subscriptions | Legacy project-scoped routes. |
| PUT | recordings/{id}/subscription | write | subscriptions | Legacy project-scoped routes. |
| DELETE | recordings/{id}/subscription | write | subscriptions | Legacy project-scoped routes. |
| GET | recordings/{id}/subscription.json | read | subscriptions | Legacy project-scoped routes. |
| POST | recordings/{id}/subscription.json | write | subscriptions | Legacy project-scoped routes. |
| PUT | recordings/{id}/subscription.json | write | subscriptions | Legacy project-scoped routes. |
| DELETE | recordings/{id}/subscription.json | write | subscriptions | Legacy project-scoped routes. |
| GET | buckets/{id}/recordings/{id}/subtasks | read | subtasks | Get a recording's subtasks. |
| POST | buckets/{id}/recordings/{id}/subtasks | write | subtasks | Create a subtask. |
| GET | buckets/{id}/recordings/{id}/subtasks.json | read | subtasks | Get a recording's subtasks. |
| POST | buckets/{id}/recordings/{id}/subtasks.json | write | subtasks | Create a subtask. |
| GET | buckets/{id}/subtasks/{id} | read | subtasks | Get a subtask. |
| PUT | buckets/{id}/subtasks/{id} | write | subtasks | Update a subtask. |
| DELETE | buckets/{id}/subtasks/{id} | write | subtasks | Delete a subtask. |
| POST | buckets/{id}/subtasks/{id}/completion | write | subtasks | Complete a subtask. |
| DELETE | buckets/{id}/subtasks/{id}/completion | write | subtasks | Uncomplete a subtask. |
| POST | buckets/{id}/subtasks/{id}/completion.json | write | subtasks | Complete a subtask. |
| DELETE | buckets/{id}/subtasks/{id}/completion.json | write | subtasks | Uncomplete a subtask. |
| PUT | buckets/{id}/subtasks/{id}/position | write | subtasks | Reposition a subtask. |
| PUT | buckets/{id}/subtasks/{id}/position.json | write | subtasks | Reposition a subtask. |
| GET | recordings/{id}/subtasks | read | subtasks | Get a recording's subtasks. |
| POST | recordings/{id}/subtasks | write | subtasks | Create a subtask. |
| GET | recordings/{id}/subtasks.json | read | subtasks | Get a recording's subtasks. |
| POST | recordings/{id}/subtasks.json | write | subtasks | Create a subtask. |
| GET | subtasks/{id} | read | subtasks | Get a subtask. |
| PUT | subtasks/{id} | write | subtasks | Update a subtask. |
| DELETE | subtasks/{id} | write | subtasks | Delete a subtask. |
| POST | subtasks/{id}/completion | write | subtasks | Complete a subtask. |
| DELETE | subtasks/{id}/completion | write | subtasks | Uncomplete a subtask. |
| POST | subtasks/{id}/completion.json | write | subtasks | Complete a subtask. |
| DELETE | subtasks/{id}/completion.json | write | subtasks | Uncomplete a subtask. |
| PUT | subtasks/{id}/position | write | subtasks | Reposition a subtask. |
| PUT | subtasks/{id}/position.json | write | subtasks | Reposition a subtask. |
| GET | templates | read | templates | Get Templates. |
| POST | templates | write | templates | Create a Template. |
| GET | templates.json | read | templates | Get Templates. |
| POST | templates.json | write | templates | Create a Template. |
| GET | templates/{id} | read | templates | Get a Template. |
| PUT | templates/{id} | write | templates | Update a Template. |
| DELETE | templates/{id} | write | templates | Trash a Template. |
| POST | templates/{id}/project_constructions | write | templates | Create a Project Construction. |
| POST | templates/{id}/project_constructions.json | write | templates | Create a Project Construction. |
| GET | templates/{id}/project_constructions/{id} | read | templates | Get a Project Construction. |
| POST | buckets/{id}/recordings/{id}/templatifications | write | templatifications | Templatify a to-do list or card table. |
| POST | buckets/{id}/recordings/{id}/templatifications.json | write | templatifications | Templatify a to-do list or card table. |
| GET | buckets/{id}/recordings/{id}/templatifications/{id} | read | templatifications | Get a templatification. |
| POST | recordings/{id}/templatifications | write | templatifications | Templatify a to-do list or card table. |
| POST | recordings/{id}/templatifications.json | write | templatifications | Templatify a to-do list or card table. |
| GET | recordings/{id}/templatifications/{id} | read | templatifications | Get a templatification. |
| GET | projects/{id}/timeline | read | timeline | Get project timeline. |
| GET | projects/{id}/timeline.json | read | timeline | Get project timeline. |
| GET | reports/progress | read | timeline | Get timeline. |
| GET | reports/progress.json | read | timeline | Get timeline. |
| GET | reports/users/progress/{id} | read | timeline | Get person's timeline. |
| GET | buckets/{id}/recordings/{id}/timesheet | read | timesheets | Get timesheet for a recording. |
| GET | buckets/{id}/recordings/{id}/timesheet.json | read | timesheets | Get timesheet for a recording. |
| POST | buckets/{id}/recordings/{id}/timesheet/entries | write | timesheets | Create a timesheet entry. |
| POST | buckets/{id}/recordings/{id}/timesheet/entries.json | write | timesheets | Create a timesheet entry. |
| GET | buckets/{id}/timesheet_entries/{id} | read | timesheets | Get a timesheet entry. |
| PUT | buckets/{id}/timesheet_entries/{id} | write | timesheets | Update a timesheet entry. |
| DELETE | buckets/{id}/timesheet_entries/{id} | write | timesheets | Delete a timesheet entry. |
| GET | projects/{id}/recordings/{id}/timesheet | read | timesheets | Legacy project-scoped routes. |
| GET | projects/{id}/recordings/{id}/timesheet.json | read | timesheets | Legacy project-scoped routes. |
| POST | projects/{id}/recordings/{id}/timesheet/entries | write | timesheets | Legacy project-scoped routes. |
| POST | projects/{id}/recordings/{id}/timesheet/entries.json | write | timesheets | Legacy project-scoped routes. |
| GET | projects/{id}/timesheet | read | timesheets | Get timesheet for a project. |
| GET | projects/{id}/timesheet.json | read | timesheets | Get timesheet for a project. |
| GET | recordings/{id}/timesheet | read | timesheets | Get timesheet for a recording. |
| GET | recordings/{id}/timesheet.json | read | timesheets | Get timesheet for a recording. |
| POST | recordings/{id}/timesheet/entries | write | timesheets | Create a timesheet entry. |
| POST | recordings/{id}/timesheet/entries.json | write | timesheets | Create a timesheet entry. |
| GET | reports/timesheet | read | timesheets | Get timesheet report. |
| GET | reports/timesheet.json | read | timesheets | Get timesheet report. |
| GET | timesheet_entries/{id} | read | timesheets | Get a timesheet entry. |
| PUT | timesheet_entries/{id} | write | timesheets | Update a timesheet entry. |
| DELETE | timesheet_entries/{id} | write | timesheets | Delete a timesheet entry. |
| PUT | buckets/{id}/todolists/groups/{id}/position | write | to-do list groups | Legacy project-scoped routes. |
| PUT | buckets/{id}/todolists/groups/{id}/position.json | write | to-do list groups | Legacy project-scoped routes. |
| GET | buckets/{id}/todolists/{id} | read | to-do list groups | Legacy project-scoped routes. |
| GET | buckets/{id}/todolists/{id}/groups | read | to-do list groups | Legacy project-scoped routes. |
| POST | buckets/{id}/todolists/{id}/groups | write | to-do list groups | Legacy project-scoped routes. |
| GET | buckets/{id}/todolists/{id}/groups.json | read | to-do list groups | Legacy project-scoped routes. |
| POST | buckets/{id}/todolists/{id}/groups.json | write | to-do list groups | Legacy project-scoped routes. |
| PUT | todolists/groups/{id}/position | write | to-do list groups | Legacy project-scoped routes. |
| PUT | todolists/groups/{id}/position.json | write | to-do list groups | Legacy project-scoped routes. |
| GET | todolists/{id} | read | to-do list groups | Legacy project-scoped routes. |
| GET | todolists/{id}/groups | read | to-do list groups | Legacy project-scoped routes. |
| POST | todolists/{id}/groups | write | to-do list groups | Legacy project-scoped routes. |
| GET | todolists/{id}/groups.json | read | to-do list groups | Legacy project-scoped routes. |
| POST | todolists/{id}/groups.json | write | to-do list groups | Legacy project-scoped routes. |
| GET | template_library/copies/{id} | read | to-do list templates | Get a template copy. |
| GET | template_library/todolists | read | to-do list templates | Get the template library. |
| POST | template_library/todolists | write | to-do list templates | Create a to-do list template. |
| GET | template_library/todolists.json | read | to-do list templates | Get the template library. |
| POST | template_library/todolists.json | write | to-do list templates | Create a to-do list template. |
| PUT | buckets/{id}/todolists/{id} | write | to-do lists | Legacy project-scoped routes. |
| PUT | buckets/{id}/todosets/todolists/{id}/position | write | to-do lists | Legacy project-scoped routes. |
| PUT | buckets/{id}/todosets/todolists/{id}/position.json | write | to-do lists | Legacy project-scoped routes. |
| GET | buckets/{id}/todosets/{id}/todolists | read | to-do lists | Legacy project-scoped routes. |
| POST | buckets/{id}/todosets/{id}/todolists | write | to-do lists | Legacy project-scoped routes. |
| GET | buckets/{id}/todosets/{id}/todolists.json | read | to-do lists | Legacy project-scoped routes. |
| POST | buckets/{id}/todosets/{id}/todolists.json | write | to-do lists | Legacy project-scoped routes. |
| PUT | todolists/{id} | write | to-do lists | Legacy project-scoped routes. |
| PUT | todosets/todolists/{id}/position | write | to-do lists | Legacy project-scoped routes. |
| PUT | todosets/todolists/{id}/position.json | write | to-do lists | Legacy project-scoped routes. |
| GET | todosets/{id}/todolists | read | to-do lists | Legacy project-scoped routes. |
| POST | todosets/{id}/todolists | write | to-do lists | Legacy project-scoped routes. |
| GET | todosets/{id}/todolists.json | read | to-do lists | Legacy project-scoped routes. |
| POST | todosets/{id}/todolists.json | write | to-do lists | Legacy project-scoped routes. |
| GET | buckets/{id}/todosets/{id} | read | to-do sets | Legacy project-scoped routes. |
| GET | todosets/{id} | read | to-do sets | Legacy project-scoped routes. |
| GET | buckets/{id}/todolists/{id}/todos | read | to-dos | Legacy project-scoped routes. |
| POST | buckets/{id}/todolists/{id}/todos | write | to-dos | Legacy project-scoped routes. |
| GET | buckets/{id}/todolists/{id}/todos.json | read | to-dos | Legacy project-scoped routes. |
| POST | buckets/{id}/todolists/{id}/todos.json | write | to-dos | Legacy project-scoped routes. |
| GET | buckets/{id}/todos/{id} | read | to-dos | Legacy project-scoped routes. |
| PUT | buckets/{id}/todos/{id} | write | to-dos | Legacy project-scoped routes. |
| POST | buckets/{id}/todos/{id}/completion | write | to-dos | Legacy project-scoped routes. |
| DELETE | buckets/{id}/todos/{id}/completion | write | to-dos | Legacy project-scoped routes. |
| POST | buckets/{id}/todos/{id}/completion.json | write | to-dos | Legacy project-scoped routes. |
| DELETE | buckets/{id}/todos/{id}/completion.json | write | to-dos | Legacy project-scoped routes. |
| PUT | buckets/{id}/todos/{id}/position | write | to-dos | Legacy project-scoped routes. |
| PUT | buckets/{id}/todos/{id}/position.json | write | to-dos | Legacy project-scoped routes. |
| POST | buckets/{id}/todosets/{id}/todos | write | to-dos | Create a to-do. |
| POST | buckets/{id}/todosets/{id}/todos.json | write | to-dos | Create a to-do. |
| GET | todolists/{id}/todos | read | to-dos | Legacy project-scoped routes. |
| POST | todolists/{id}/todos | write | to-dos | Legacy project-scoped routes. |
| GET | todolists/{id}/todos.json | read | to-dos | Legacy project-scoped routes. |
| POST | todolists/{id}/todos.json | write | to-dos | Legacy project-scoped routes. |
| GET | todos/{id} | read | to-dos | Legacy project-scoped routes. |
| PUT | todos/{id} | write | to-dos | Legacy project-scoped routes. |
| POST | todos/{id}/completion | write | to-dos | Legacy project-scoped routes. |
| DELETE | todos/{id}/completion | write | to-dos | Legacy project-scoped routes. |
| POST | todos/{id}/completion.json | write | to-dos | Legacy project-scoped routes. |
| DELETE | todos/{id}/completion.json | write | to-dos | Legacy project-scoped routes. |
| PUT | todos/{id}/position | write | to-dos | Legacy project-scoped routes. |
| PUT | todos/{id}/position.json | write | to-dos | Legacy project-scoped routes. |
| POST | todosets/{id}/todos | write | to-dos | Create a to-do. |
| POST | todosets/{id}/todos.json | write | to-dos | Create a to-do. |
| POST | buckets/{id}/dock/tools | write | tools | Create a tool. |
| POST | buckets/{id}/dock/tools.json | write | tools | Create a tool. |
| GET | buckets/{id}/dock/tools/{id} | read | tools | Legacy project-scoped routes. |
| PUT | buckets/{id}/dock/tools/{id} | write | tools | Legacy project-scoped routes. |
| DELETE | buckets/{id}/dock/tools/{id} | write | tools | Legacy project-scoped routes. |
| POST | buckets/{id}/recordings/{id}/position | write | tools | Enable a tool. |
| PUT | buckets/{id}/recordings/{id}/position | write | tools | Reposition a tool. |
| DELETE | buckets/{id}/recordings/{id}/position | write | tools | Disable a tool. |
| POST | buckets/{id}/recordings/{id}/position.json | write | tools | Enable a tool. |
| PUT | buckets/{id}/recordings/{id}/position.json | write | tools | Reposition a tool. |
| DELETE | buckets/{id}/recordings/{id}/position.json | write | tools | Disable a tool. |
| POST | dock/tools | write | tools | Create a tool. |
| POST | dock/tools.json | write | tools | Create a tool. |
| GET | dock/tools/{id} | read | tools | Legacy project-scoped routes. |
| PUT | dock/tools/{id} | write | tools | Legacy project-scoped routes. |
| DELETE | dock/tools/{id} | write | tools | Legacy project-scoped routes. |
| POST | recordings/{id}/position | write | tools | Enable a tool. |
| PUT | recordings/{id}/position | write | tools | Reposition a tool. |
| DELETE | recordings/{id}/position | write | tools | Disable a tool. |
| POST | recordings/{id}/position.json | write | tools | Enable a tool. |
| PUT | recordings/{id}/position.json | write | tools | Reposition a tool. |
| DELETE | recordings/{id}/position.json | write | tools | Disable a tool. |
| GET | buckets/{id}/uploads/{id} | read | uploads | Legacy project-scoped routes. |
| PUT | buckets/{id}/uploads/{id} | write | uploads | Legacy project-scoped routes. |
| GET | buckets/{id}/uploads/{id}/versions | read | uploads | Legacy project-scoped routes. |
| POST | buckets/{id}/uploads/{id}/versions | write | uploads | Legacy project-scoped routes. |
| GET | buckets/{id}/uploads/{id}/versions.json | read | uploads | Legacy project-scoped routes. |
| POST | buckets/{id}/uploads/{id}/versions.json | write | uploads | Legacy project-scoped routes. |
| GET | buckets/{id}/vaults/{id}/uploads | read | uploads | Legacy project-scoped routes. |
| POST | buckets/{id}/vaults/{id}/uploads | write | uploads | Legacy project-scoped routes. |
| GET | buckets/{id}/vaults/{id}/uploads.json | read | uploads | Legacy project-scoped routes. |
| POST | buckets/{id}/vaults/{id}/uploads.json | write | uploads | Legacy project-scoped routes. |
| GET | uploads/{id} | read | uploads | Legacy project-scoped routes. |
| PUT | uploads/{id} | write | uploads | Legacy project-scoped routes. |
| GET | uploads/{id}/versions | read | uploads | Legacy project-scoped routes. |
| POST | uploads/{id}/versions | write | uploads | Legacy project-scoped routes. |
| GET | uploads/{id}/versions.json | read | uploads | Legacy project-scoped routes. |
| POST | uploads/{id}/versions.json | write | uploads | Legacy project-scoped routes. |
| GET | vaults/{id}/uploads | read | uploads | Legacy project-scoped routes. |
| POST | vaults/{id}/uploads | write | uploads | Legacy project-scoped routes. |
| GET | vaults/{id}/uploads.json | read | uploads | Legacy project-scoped routes. |
| POST | vaults/{id}/uploads.json | write | uploads | Legacy project-scoped routes. |
| POST | buckets/{id}/recordings/{id}/filing | write | vaults | Legacy project-scoped routes. |
| POST | buckets/{id}/recordings/{id}/filing.json | write | vaults | Legacy project-scoped routes. |
| GET | buckets/{id}/vaults/{id} | read | vaults | Legacy project-scoped routes. |
| PUT | buckets/{id}/vaults/{id} | write | vaults | Legacy project-scoped routes. |
| GET | buckets/{id}/vaults/{id}/vaults | read | vaults | Legacy project-scoped routes. |
| POST | buckets/{id}/vaults/{id}/vaults | write | vaults | Legacy project-scoped routes. |
| GET | buckets/{id}/vaults/{id}/vaults.json | read | vaults | Legacy project-scoped routes. |
| POST | buckets/{id}/vaults/{id}/vaults.json | write | vaults | Legacy project-scoped routes. |
| PUT | buckets/{id}/vaults/{id}/view_preference | write | vaults | Legacy project-scoped routes. |
| PUT | buckets/{id}/vaults/{id}/view_preference.json | write | vaults | Legacy project-scoped routes. |
| POST | recordings/{id}/filing | write | vaults | Legacy project-scoped routes. |
| POST | recordings/{id}/filing.json | write | vaults | Legacy project-scoped routes. |
| GET | vaults/{id} | read | vaults | Legacy project-scoped routes. |
| PUT | vaults/{id} | write | vaults | Legacy project-scoped routes. |
| GET | vaults/{id}/vaults | read | vaults | Legacy project-scoped routes. |
| POST | vaults/{id}/vaults | write | vaults | Legacy project-scoped routes. |
| GET | vaults/{id}/vaults.json | read | vaults | Legacy project-scoped routes. |
| POST | vaults/{id}/vaults.json | write | vaults | Legacy project-scoped routes. |
| PUT | vaults/{id}/view_preference | write | vaults | Legacy project-scoped routes. |
| PUT | vaults/{id}/view_preference.json | write | vaults | Legacy project-scoped routes. |
| GET | buckets/{id}/webhooks | read | webhooks | Get webhooks. |
| POST | buckets/{id}/webhooks | write | webhooks | Create a webhook. |
| GET | buckets/{id}/webhooks.json | read | webhooks | Get webhooks. |
| POST | buckets/{id}/webhooks.json | write | webhooks | Create a webhook. |
| GET | buckets/{id}/webhooks/{id} | read | webhooks | Legacy project-scoped routes. |
| PUT | buckets/{id}/webhooks/{id} | write | webhooks | Legacy project-scoped routes. |
| DELETE | buckets/{id}/webhooks/{id} | write | webhooks | Legacy project-scoped routes. |
| GET | webhooks | read | webhooks | Get webhooks. |
| POST | webhooks | write | webhooks | Create a webhook. |
| GET | webhooks.json | read | webhooks | Get webhooks. |
| POST | webhooks.json | write | webhooks | Create a webhook. |
| GET | webhooks/{id} | read | webhooks | Legacy project-scoped routes. |
| PUT | webhooks/{id} | write | webhooks | Legacy project-scoped routes. |
| DELETE | webhooks/{id} | write | webhooks | Legacy project-scoped routes. |
