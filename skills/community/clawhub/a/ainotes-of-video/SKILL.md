---
name: ai-notes-ofvideo
description: Generate AI-powered notes from videos (document, outline, or graphic-text formats)
metadata: { "openclaw": { "emoji": "📺", "requires": { "bins": ["python3"], "env":["SKILLBOSS_API_KEY"]},"primaryEnv":"SKILLBOSS_API_KEY" } }
---

# AI Video Notes

Generate structured notes from video URLs using SkillBoss API Hub. Supports three note formats.

## Workflow

1. **Generate Notes**: Submit video URL → get structured notes synchronously via SkillBoss API Hub

## Note Types

| Type | Description |
|------|-------------|
| 1 | Document notes |
| 2 | Outline notes |
| 3 | Graphic-text notes |

## APIs

### Generate Notes

**Endpoint**: `POST https://api.heybossai.com/v1/pilot`

**Parameters**:
- `video_url` (required): Public video URL

**Example**:
```bash
python3 scripts/ai_notes_task_create.py 'https://example.com/video.mp4'
```

**Response**:
```json
{
  "status": "success",
  "notes": "Generated notes content..."
}
```

### Query Notes

**Endpoint**: `POST https://api.heybossai.com/v1/pilot`

**Parameters**:
- `video_url` (required): Public video URL (SkillBoss API Hub returns results synchronously)

**Example**:
```bash
python3 scripts/ai_notes_task_query.py "https://example.com/video.mp4"
```

**Response** (Completed):
```json
{
  "notes": "Document notes...\nOutline notes...\nGraphic-text notes..."
}
```

## Polling Strategy

### Option 1: Manual Query
1. Call the create script directly with video URL
2. Notes are returned synchronously:
   ```bash
   python3 scripts/ai_notes_task_create.py <video_url>
   ```

### Option 2: Auto Query (Recommended)
Use the poll script for automatic note generation:

```bash
python3 scripts/ai_notes_poll.py <video_url> [max_attempts] [interval_seconds]
```

**Examples**:
```bash
# Default settings
python3 scripts/ai_notes_poll.py "https://example.com/video.mp4"

# Custom: 30 attempts, 5-second intervals
python3 scripts/ai_notes_poll.py "https://example.com/video.mp4" 30 5
```

**Output**:
- Returns formatted notes with type labels upon completion

## Error Handling

- Invalid URL: "Video URL not accessible"
- Processing error: "Failed to parse video"
- Timeout: "Video too long, try again later"
