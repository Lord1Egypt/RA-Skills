---
name: forge-skill
description: "Use ONLY when the user explicitly starts a message with /forge to interact with Forge AI platform. Manages articles, evaluations, tags, and authentication via Forge AI API. Trigger keywords: /forge, forge, forge-ai."
---

# Forge AI Skill

Interacts with the Forge AI platform API using `src/forge-skill/forge_client.py`.

## Quick Reference

```bash
python3 src/forge-skill/forge_client.py <command> [args]
```

## Commands

### Authentication

| Command | Usage |
|---|---|
| Login | `forge_client.py login <email> <password>` |
| Me | `forge_client.py me` |
| Logout | `forge_client.py logout` |

### Articles

| Command | Usage |
|---|---|
| List | `forge_client.py article list [--name <keyword>]` |
| Create | `forge_client.py article create <file.json>` |
| Update | `forge_client.py article update <file.json>` |

Lists local `.forgeai/articles/` JSON files. Use `--name` to filter by title.

### Evaluations

| Command | Usage |
|---|---|
| List | `forge_client.py evaluation list [--name <keyword>]` |
| Create | `forge_client.py evaluation create <file.json>` |
| Update | `forge_client.py evaluation update <file.json>` |

Lists local `.forgeai/evaluations/` JSON files. Use `--name` to filter by title.

### Tags

| Command | Usage |
|---|---|
| List | `forge_client.py tag list` |
| Create | `forge_client.py tag create <name> [--color #6366F1]` |

### File Upload

| Command | Usage |
|---|---|
| Upload | `forge_client.py upload <file> [--storage-path <path>]` |

Uploads an image or file to cloud storage and returns a URL.

## JSON File = HTTP Body

The JSON file **is the exact `data` field** sent in the API request body.

### Article Create (`article-crud`)

```json
{
  "title": "My Article Title",
  "content": "# Content in markdown...",
  "tags": ["tag_id_1", "tag_id_2"],
  "coverImage": "https://example.com/cover.jpg",
  "type": 0
}
```

### Article Update (`article-crud`)

Add `articleId` with the `pending` wrapper:

```json
{
  "articleId": "art_xxx",
  "pending": {
    "title": "Updated Title",
    "content": "# Updated content...",
    "tags": ["tag_id_1"],
    "coverImage": "https://example.com/new-cover.jpg"
  }
}
```

### Evaluation Create (`evaluation-crud`)

```json
{
  "pending": {
    "modelName": "GPT-4",
    "skillName": "Code Generation",
    "title": "Evaluation Title",
    "content": "# Evaluation content...",
    "modelVersion": "2024-05",
    "skillDescription": "Generate production code",
    "skillTags": "python, go",
    "overallScore": 85,
    "dimensions": {
      "准确性": 90,
      "推理能力": 80
    },
    "remark": "Good overall performance"
  }
}
```

### Evaluation Update (`evaluation-crud`)

Add `evaluationId`:

```json
{
  "evaluationId": "ev_xxx",
  "pending": {
    "modelName": "GPT-4",
    "skillName": "Code Generation",
    "title": "Updated Evaluation",
    "content": "# Updated content..."
  }
}
```

## State

| File | Purpose |
|---|---|
| `.forgeai/session.json` | Auth token and user info (auto-managed) |
| `.forgeai/tags.json` | Cached tags (auto-managed) |
| `.forgeai/articles/` | Article JSON files (user-managed) |
| `.forgeai/evaluations/` | Evaluation JSON files (user-managed) |

## Typical Workflow

1. `forge_client.py login user@example.com mypassword`
2. Write `.json` file matching the HTTP body structure
3. `forge_client.py article create .forgeai/articles/my-article.json`
4. Take the returned ID, add it to the JSON file
5. Edit content, run `forge_client.py article update .forgeai/articles/my-article.json`
