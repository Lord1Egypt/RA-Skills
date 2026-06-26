# Pin Types Reference

> All curl examples below assume `CORKBOARD_TOKEN` is exported in your shell.
> See `references/setup.md` or `references/api.md#authentication` for how to
> obtain it.

## Shared Fields

Every pin includes:

```typescript
type PinType =
  | 'task'
  | 'note'
  | 'link'
  | 'event'
  | 'alert'
  | 'email'
  | 'opportunity'
  | 'briefing'
  | 'github'
  | 'idea'
  | 'tracking'
  | 'article'
  | 'twitter'
  | 'reddit'
  | 'youtube';

type PinStatus = 'active' | 'completed' | 'snoozed' | 'dismissed';

interface Pin {
  id: string;
  type: PinType;
  title: string;
  content?: string;
  status: PinStatus;
  createdAt: string;
  updatedAt: string;
  priority?: 1 | 2 | 3;
  url?: string;      // absolute http(s) URL only
  dueAt?: string;    // date string
}
```

Notes:
- Create requests require `type` and `title`.
- `priority` is optional and defaults to `2`.
- `url` and every nested URL field must be absolute `http(s)` URLs.
- Update requests accept the same specialized fields as create requests.

## Pin Types

| Type | Use for | Key fields |
|------|---------|------------|
| `task` | Action items (inline-editable via double-click on title) | `content`, `priority`, `dueAt` |
| `note` | Reference context (inline-editable via double-click on title) | `content` |
| `link` | External links | `url` |
| `event` | Time-sensitive reminders | `content`, `dueAt`, `priority` |
| `alert` | Urgent notices | `content`, usually `priority: 1` |
| `email` | Important email summaries | `emailFrom`, `emailId`, `emailDate`, `content` |
| `opportunity` | Follow-up opportunities | `emailFrom`, `emailId`, `priority`, `content` |
| `briefing` | Daily or situational briefings | `content` with limited formatting |
| `github` | Repo bookmarks | `repo`, `url`, `stars`, `forks`, `content` |
| `idea` | Idea incubator entries | `ideaVerdict`, `ideaScores`, `ideaCompetitors`, `ideaEffortEstimate`, `ideaResearchSummary` |
| `tracking` | Package tracking | `trackingNumber`, `trackingCarrier`, `trackingStatus`, `trackingEta`, `trackingUrl` |
| `article` | Article summaries | `articleData` |
| `twitter` | X/Twitter previews | `url`, `content` |
| `reddit` | Reddit previews | `url`, `content` |
| `youtube` | YouTube video cards | `url`, `youtubeData` |

## Specialized Shapes

### `email` and `opportunity`

These share the email-style metadata fields:

```typescript
emailFrom?: string;
emailDate?: string;
emailId?: string;
```

### `briefing`

`content` supports a safe, limited markdown-like format:
- `## Heading`
- `### Subheading`
- `**bold**`
- `- bullet`
- `---`

### `github`

```typescript
repo?: string;   // owner/repo
stars?: number;
forks?: number;
url?: string;
```

### `idea`

```typescript
ideaVerdict?: 'hot' | 'warm' | 'cold' | 'pass';
ideaScores?: {
  viability?: number;
  alignment?: number;
  effort?: number;
  competition?: number;
  marketSignal?: number;
};
ideaCompetitors?: number;
ideaEffortEstimate?: string;
ideaResearchSummary?: string;
```

### `tracking`

```typescript
trackingStatus?: 'pre-transit' | 'in-transit' | 'out-for-delivery' | 'delivered' | 'exception' | 'unknown';
trackingNumber?: string;
trackingCarrier?: string;
trackingLocation?: string;
trackingEta?: string;
trackingLastUpdate?: string;
trackingUrl?: string;
```

### `article`

```typescript
articleData?: {
  url: string;
  source: string;
  readTime?: string;
  tldr: string;
  bullets: string[];
  tags?: string[];
};
```

### `youtube`

```typescript
youtubeData?: {
  videoId: string;        // required — 11-char YouTube video ID
  thumbnailUrl: string;   // required — absolute http(s) URL
  channelTitle?: string;
  description?: string;
  publishedAt?: string;
  duration?: string;      // e.g. "12:44" or "1:02:30"
  embedUrl?: string;      // absolute http(s) URL
  sourceUrl?: string;     // absolute http(s) URL
};
```

Supported URL formats for the `url` field:
- `https://www.youtube.com/watch?v=<id>`
- `https://youtu.be/<id>`
- `https://www.youtube.com/shorts/<id>`
- `https://www.youtube.com/live/<id>`

## Examples

Task:
```bash
curl -X POST "$CORKBOARD_API/api/pins" \
  -H "Authorization: Bearer $CORKBOARD_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"type":"task","title":"Review PR","content":"Auth refactor complete","priority":1}'
```

Opportunity:
```bash
curl -X POST "$CORKBOARD_API/api/pins" \
  -H "Authorization: Bearer $CORKBOARD_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type":"opportunity",
    "title":"Wholesale inquiry from gallery",
    "content":"Reply with pricing sheet and lead times",
    "emailFrom":"buyer@example.com",
    "emailId":"gmail-message-id",
    "priority":2
  }'
```

Tracking:
```bash
curl -X POST "$CORKBOARD_API/api/pins" \
  -H "Authorization: Bearer $CORKBOARD_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type":"tracking",
    "title":"UPS package",
    "trackingNumber":"1Z999AA10123456784",
    "trackingCarrier":"UPS",
    "trackingStatus":"in-transit",
    "trackingEta":"2026-04-03T17:00:00Z"
  }'
```

Article:
```bash
curl -X POST "$CORKBOARD_API/api/pins" \
  -H "Authorization: Bearer $CORKBOARD_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type":"article",
    "title":"Local-first dashboards",
    "url":"https://example.com/local-first-dashboards",
    "articleData":{
      "url":"https://example.com/local-first-dashboards",
      "source":"Example Weekly",
      "tldr":"Practical notes on shipping local-first tools.",
      "bullets":["Sync matters less than resilience","Offline UX still wins"],
      "tags":["product","frontend"]
    }
  }'
```

YouTube:
```bash
curl -X POST "$CORKBOARD_API/api/pins" \
  -H "Authorization: Bearer $CORKBOARD_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type":"youtube",
    "title":"Demo video",
    "url":"https://www.youtube.com/watch?v=abc123xyz00",
    "youtubeData":{
      "videoId":"abc123xyz00",
      "thumbnailUrl":"https://i.ytimg.com/vi/abc123xyz00/hqdefault.jpg",
      "channelTitle":"Demo Channel",
      "duration":"12:44",
      "embedUrl":"https://www.youtube.com/embed/abc123xyz00",
      "sourceUrl":"https://www.youtube.com/watch?v=abc123xyz00"
    }
  }'
```
