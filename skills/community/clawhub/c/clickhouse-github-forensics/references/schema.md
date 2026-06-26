# github_events Full Schema

Query to retrieve: `DESCRIBE github_events FORMAT PrettyCompact`

## All Columns

| Column | Type | Notes |
|--------|------|-------|
| `file_time` | DateTime | File ingestion time |
| `event_type` | Enum8 | See event types below |
| `actor_login` | LowCardinality(String) | GitHub username |
| `repo_name` | LowCardinality(String) | `owner/repo` format |
| `created_at` | DateTime | Event timestamp (primary for queries) |
| `updated_at` | DateTime | Last update time |
| `action` | Enum8 | Event-specific action |
| `comment_id` | UInt64 | Comment ID if applicable |
| `body` | String | Comment/PR/issue body text |
| `path` | String | File path for review comments |
| `position` | Int32 | Line position |
| `line` | Int32 | Line number |
| `ref` | LowCardinality(String) | Branch/tag reference |
| `ref_type` | Enum8 | branch/tag/repository/none/unknown |
| `creator_user_login` | LowCardinality(String) | Content creator |
| `number` | UInt32 | PR/issue number |
| `title` | String | PR/issue title |
| `labels` | Array(LowCardinality(String)) | Applied labels |
| `state` | Enum8 | open/closed/none |
| `locked` | UInt8 | Is locked |
| `assignee` | LowCardinality(String) | Assigned user |
| `assignees` | Array(LowCardinality(String)) | All assignees |
| `comments` | UInt32 | Comment count |
| `author_association` | Enum8 | NONE/CONTRIBUTOR/OWNER/COLLABORATOR/MEMBER/MANNEQUIN |
| `closed_at` | DateTime | When closed |
| `merged_at` | DateTime | When merged |
| `merge_commit_sha` | String | Merge commit SHA |
| `requested_reviewers` | Array(LowCardinality(String)) | Requested reviewers |
| `requested_teams` | Array(LowCardinality(String)) | Requested teams |

## Event Types (event_type Enum)

```
CommitCommentEvent = 1
CreateEvent = 2
DeleteEvent = 3
ForkEvent = 4
GollumEvent = 5
IssueCommentEvent = 6
IssuesEvent = 7
MemberEvent = 8
PublicEvent = 9
PullRequestEvent = 10
PullRequestReviewCommentEvent = 11
PushEvent = 12
ReleaseEvent = 13
SponsorshipEvent = 14
WatchEvent = 15
GistEvent = 16
FollowEvent = 17
DownloadEvent = 18
PullRequestReviewEvent = 19
ForkApplyEvent = 20
Event = 21
TeamAddEvent = 22
DiscussionEvent = 23
```

## Action Values (action Enum)

```
none = 0
created = 1
added = 2
edited = 3
deleted = 4
opened = 5
closed = 6
reopened = 7
assigned = 8
unassigned = 9
labeled = 10
unlabeled = 11
review_requested = 12
review_request_removed = 13
synchronize = 14
started = 15
published = 16
update = 17
create = 18
fork = 19
merged = 20
forked = 21
updated = 22
dismissed = 23
```

## ref_type Values

```
none = 0
branch = 1
tag = 2
repository = 3
unknown = 4
```

## author_association Values

```
NONE = 0
CONTRIBUTOR = 1
OWNER = 2
COLLABORATOR = 3
MEMBER = 4
MANNEQUIN = 5
```

## Data Statistics

As of 2026-03-20:
- **Total events:** ~10.5 billion
- **Freshness:** Near real-time (minutes behind)
- **History:** Back to 2011

Query to check:
```sql
SELECT max(created_at) as latest, count() as total FROM github_events
```
