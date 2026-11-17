# Canvas API endpoints for curl

All 18 `canvas_*` MCP tools, transcribed from `src/tools/*.ts` in
`canvas-parent-mcp`. Every call needs:

```sh
-H "Authorization: Bearer $CANVAS_TOKEN"
-H "Accept: application/json+canvas-string-ids, application/json"
```

against `$CANVAS_BASE_URL` (per-institution, e.g.
`https://<district>.instructure.com`). Pipe every response through
`sed 's/^while(1);//'` before `jq` (Canvas's XSSI guard). List endpoints are
marked **paginated** — see the `Link`-header loop in `SKILL.md` for anything
you expect to run long; for a quick look just bump `per_page`.

`{userSegment}` below means `users/self`, or `users/<observeeId>` to read a
linked observee's data instead (get IDs from §2).

---

## 1. Profile

```sh
curl -s -H "Authorization: Bearer $CANVAS_TOKEN" -H "Accept: application/json+canvas-string-ids, application/json" \
  "$CANVAS_BASE_URL/api/v1/users/self/profile" | sed 's/^while(1);//' \
  | jq '{id, name, primary_email, login_id, locale, time_zone}'
```

## 2. Observees — students linked to your observer account

Empty array for a plain student token.

```sh
curl -s -H "Authorization: Bearer $CANVAS_TOKEN" -H "Accept: application/json+canvas-string-ids, application/json" \
  "$CANVAS_BASE_URL/api/v1/users/self/observees?include[]=avatar_url" | sed 's/^while(1);//' \
  | jq '.[] | {id, name}'
```

*(paginated)*

## 3. Courses — active, with grades

```sh
curl -s -H "Authorization: Bearer $CANVAS_TOKEN" -H "Accept: application/json+canvas-string-ids, application/json" \
  "$CANVAS_BASE_URL/api/v1/{userSegment}/courses?enrollment_state=active&state[]=available&include[]=total_scores&include[]=current_grading_period_scores&include[]=term" \
  | sed 's/^while(1);//' | jq '.[] | {id, name, total_scores}'
```

*(paginated)*

## 4. Single course — syllabus, teachers, term

```sh
curl -s -H "Authorization: Bearer $CANVAS_TOKEN" -H "Accept: application/json+canvas-string-ids, application/json" \
  "$CANVAS_BASE_URL/api/v1/courses/{courseId}?include[]=syllabus_body&include[]=teachers&include[]=term" \
  | sed 's/^while(1);//' | jq '{id, name, syllabus_body, teachers, term}'
```

## 5. Assignments — a course's assignment list, with your submission inline

`bucket` (optional): `past` `overdue` `undated` `ungraded` `unsubmitted`
`upcoming` `future`.

```sh
curl -s -H "Authorization: Bearer $CANVAS_TOKEN" -H "Accept: application/json+canvas-string-ids, application/json" \
  "$CANVAS_BASE_URL/api/v1/courses/{courseId}/assignments?include[]=submission&order_by=due_at&bucket=upcoming" \
  | sed 's/^while(1);//' | jq '.[] | {id, name, due_at, submission: .submission.workflow_state}'
```

*(paginated)*

## 6. Missing submissions — past-due, unsubmitted

For an observee, `course_ids[]` (repeat the param per ID) is required.

```sh
curl -s -H "Authorization: Bearer $CANVAS_TOKEN" -H "Accept: application/json+canvas-string-ids, application/json" \
  "$CANVAS_BASE_URL/api/v1/{userSegment}/missing_submissions?include[]=planner_overrides&include[]=course&filter[]=submittable&course_ids[]=123&course_ids[]=456" \
  | sed 's/^while(1);//' | jq '.[] | {id, name, due_at, course_id}'
```

*(paginated)*

## 7. Single submission — rubric + grader comments

`userId` defaults to `self`; pass a numeric Canvas user ID for an observee.

```sh
curl -s -H "Authorization: Bearer $CANVAS_TOKEN" -H "Accept: application/json+canvas-string-ids, application/json" \
  "$CANVAS_BASE_URL/api/v1/courses/{courseId}/assignments/{assignmentId}/submissions/self?include[]=submission_comments&include[]=rubric_assessment&include[]=assignment" \
  | sed 's/^while(1);//' | jq '{score, grade, submitted_at, submission_comments}'
```

## 8. Recent graded submissions in a course

`student_ids[]` defaults to `self`; `graded_since` defaults to 14 days ago
(ISO 8601, compute it yourself for curl — Canvas doesn't).

```sh
since=$(date -u -v-14d +%Y-%m-%dT%H:%M:%SZ)   # macOS date; use `date -u -d '14 days ago' ...` on GNU
curl -s -H "Authorization: Bearer $CANVAS_TOKEN" -H "Accept: application/json+canvas-string-ids, application/json" \
  "$CANVAS_BASE_URL/api/v1/courses/{courseId}/students/submissions?student_ids[]=self&workflow_state[]=graded&graded_since=$since&include[]=assignment&include[]=submission_comments" \
  | sed 's/^while(1);//' | jq '.[] | {assignment: .assignment.name, score, grade}'
```

*(paginated)*

## 9. Enrollments — per-course grades

```sh
curl -s -H "Authorization: Bearer $CANVAS_TOKEN" -H "Accept: application/json+canvas-string-ids, application/json" \
  "$CANVAS_BASE_URL/api/v1/{userSegment}/enrollments?state[]=active&type[]=StudentEnrollment&include[]=current_points&include[]=grades" \
  | sed 's/^while(1);//' | jq '.[] | {course_id, grades}'
```

*(paginated)*

## 10. Calendar events / assignments across contexts

`context_codes[]` looks like `course_123`, `user_456` (repeat the param per
code). `type` is `event` or `assignment`.

```sh
curl -s -H "Authorization: Bearer $CANVAS_TOKEN" -H "Accept: application/json+canvas-string-ids, application/json" \
  "$CANVAS_BASE_URL/api/v1/calendar_events?type=assignment&start_date=2026-07-01&end_date=2026-07-31&context_codes[]=course_123" \
  | sed 's/^while(1);//' | jq '.[] | {title, start_at}'
```

*(paginated)*

## 11. Upcoming events — Canvas's curated next-7-days view

```sh
curl -s -H "Authorization: Bearer $CANVAS_TOKEN" -H "Accept: application/json+canvas-string-ids, application/json" \
  "$CANVAS_BASE_URL/api/v1/users/self/upcoming_events" | sed 's/^while(1);//' | jq .
```

## 12. Planner items — assignments + announcements + notes + events

Omit `{observeeId}` (use `/api/v1/planner/items`) for yourself.

```sh
curl -s -H "Authorization: Bearer $CANVAS_TOKEN" -H "Accept: application/json+canvas-string-ids, application/json" \
  "$CANVAS_BASE_URL/api/v1/users/{observeeId}/planner/items?start_date=2026-07-01&end_date=2026-07-31" \
  | sed 's/^while(1);//' | jq '.[] | {plannable_type, plannable_date: .plannable_date}'
```

*(paginated; self variant: `$CANVAS_BASE_URL/api/v1/planner/items?...`)*

## 13. Announcements — across one or more courses

`context_codes[]` is **required** (e.g. `course_123`); defaults to
`active_only=true`.

```sh
curl -s -H "Authorization: Bearer $CANVAS_TOKEN" -H "Accept: application/json+canvas-string-ids, application/json" \
  "$CANVAS_BASE_URL/api/v1/announcements?context_codes[]=course_123&context_codes[]=course_456&active_only=true" \
  | sed 's/^while(1);//' | jq '.[] | {title, posted_at}'
```

*(paginated)*

## 14. Conversations (inbox) — list

`scope` (optional): `unread` `starred` `archived` `sent`. `filter[]` is an
array of context codes.

```sh
curl -s -H "Authorization: Bearer $CANVAS_TOKEN" -H "Accept: application/json+canvas-string-ids, application/json" \
  "$CANVAS_BASE_URL/api/v1/conversations?scope=unread&include[]=participant_avatars" \
  | sed 's/^while(1);//' | jq '.[] | {id, subject, last_message}'
```

*(paginated)*

## 15. Conversation detail — full thread

```sh
curl -s -H "Authorization: Bearer $CANVAS_TOKEN" -H "Accept: application/json+canvas-string-ids, application/json" \
  "$CANVAS_BASE_URL/api/v1/conversations/{id}?include[]=participant_avatars" \
  | sed 's/^while(1);//' | jq '.messages[] | {author_id, body, created_at}'
```

## 16. Discussion topics — a course's list

`only_announcements` defaults `false`; `order_by` (optional): `position`
`recent_activity` `title`.

```sh
curl -s -H "Authorization: Bearer $CANVAS_TOKEN" -H "Accept: application/json+canvas-string-ids, application/json" \
  "$CANVAS_BASE_URL/api/v1/courses/{courseId}/discussion_topics?only_announcements=false&order_by=recent_activity" \
  | sed 's/^while(1);//' | jq '.[] | {id, title, posted_at}'
```

*(paginated)*

## 17. Course files — metadata list

`search_term` and `content_types[]` are optional filters.

```sh
curl -s -H "Authorization: Bearer $CANVAS_TOKEN" -H "Accept: application/json+canvas-string-ids, application/json" \
  "$CANVAS_BASE_URL/api/v1/courses/{courseId}/files?search_term=syllabus" \
  | sed 's/^while(1);//' | jq '.[] | {id, display_name, url, "content-type"}'
```

*(paginated)*

## 18. Download a file

Use the absolute `url` field from §17 directly — it's already a
fully-qualified, Bearer-authable Canvas URL (no `/api/v1` prefix needed):

```sh
curl -sL -H "Authorization: Bearer $CANVAS_TOKEN" "$FILE_URL" -o /path/to/destination.pdf
```

`-L` follows Canvas's redirect to the actual file storage backend. The MCP's
`canvas_download_file` tool additionally only fetches `/files/` URLs on the
`CANVAS_BASE_URL` host, only writes inside `CANVAS_OUTPUT_DIR` (default
`~/Downloads`), refuses to overwrite an existing
destination unless told to and validates the parent directory exists —
replicate that yourself in a script if it matters (`[ -f dest ] && exit 1`,
`[ -d "$(dirname dest)" ] || exit 1`).
