# API Reference for AI Agents

Quick reference for programmatic usage.

---

## Primary Interface

### Auto-Generate (Recommended)

```bash
node scripts/auto-generate.js <name> <story> \
  --aspect 9:16 \
  --duration 60 \
  --quality-check \
  --auto-retry \
  --json
```

**Returns JSON:**

```json
{
  "status": "success" | "failed",
  "projectId": "string",
  "completedSteps": ["array"],
  "error": "string (if failed)",
  "totalTimeSeconds": number
}
```

**Time:** 25-40 minutes

---

## Secondary Interface (Manual Steps)

### 1. Create Project

```bash
node scripts/giggle-api.js create-project <name> --aspect 9:16
```

Returns: `Project ID: <id>`

### 2. Generate Script

```bash
node scripts/giggle-api.js generate-script <project_id> <story> --duration 60
```

Time: 10-30s

### 3. Generate Characters

```bash
node scripts/giggle-api.js generate-characters <project_id>
```

Time: 1-2min

### 4. Generate Storyboard

```bash
node scripts/giggle-api.js generate-storyboard <project_id>
```

Time: 30s-1min
⚠️ Polling may show "pending" but check `project-status` to verify

### 5. Generate Images

```bash
node scripts/giggle-api.js generate-images <project_id>
```

Time: 2-4min (for ~12 shots)

### 6. Generate Videos

```bash
node scripts/giggle-api.js generate-videos <project_id>
```

Time: 15-30min (for ~12 shots)
⚠️ Use default model (wan25), don't specify --model

### 7. Export

```bash
node scripts/giggle-api.js export <project_id>
```

Time: 5-10min

---

## Quality Control

### Run QC

```bash
node scripts/quality-check.js <project_id> --json
```

Returns:

```json
{
  "average_score": number,
  "passed": boolean,
  "shots": [...]
}
```

### Retry Failed Shots

```bash
# Auto retry based on QC report
node scripts/giggle-api.js retry-low-score <project_id> --threshold 80

# Manual retry single shot
node scripts/giggle-api.js retry-video <project_id> <shot_id>

# Retry all failed
node scripts/giggle-api.js retry-all-failed <project_id>
```

---

## Cost Estimation

```bash
node scripts/estimate-cost.js <project_id> --json true
```

Returns:

```json
{
  "costs": {
    "script": 1,
    "characters": 4,
    "images": 60,
    "videos": 1056,
    "export": 5,
    "total": 1126,
    "totalUSD": 11.26
  },
  "shotCount": 12,
  "charCount": 2
}
```

**Note:** 1 credit = $0.01 USD

---

## Status Checks

### Project Status

```bash
node scripts/giggle-api.js project-status <project_id>
```

Shows: shots, images, videos completion status

### Video Status

```bash
node scripts/giggle-api.js video-status <project_id>
```

Shows: completed, generating, pending, failed counts

### List Projects

```bash
node scripts/giggle-api.js list-projects
```

---

## Error Codes

| Code                          | Meaning                     | Recovery                                |
| ----------------------------- | --------------------------- | --------------------------------------- |
| `SCRIPT_GENERATION_TIMEOUT`   | Script took >60s            | Retry                                   |
| `CHARACTER_GENERATION_FAILED` | Character generation failed | Retry or regenerate                     |
| `STORYBOARD_TIMEOUT`          | Storyboard polling timeout  | Check `project-status`, may be complete |
| `VIDEO_GENERATION_FAILED`     | Video failed                | Retry with same or different model      |
| `QUALITY_CHECK_FAILED`        | Score < threshold           | Retry low-score shots                   |
| `EXPORT_FAILED`               | Export failed               | Retry export                            |

**All errors:** Check `project-status` and `video-status` to diagnose

---

## Decision Tree

```
User asks for short drama
  ↓
Estimate cost
  ↓
Cost acceptable? ──No──> Stop
  ↓ Yes
Run auto-generate --json
  ↓
Poll every 5 minutes
  ↓
Status = "success"? ──No──> Report error, check last step
  ↓ Yes
Retrieve video URL from API
  ↓
Done
```

---

## Best Practices

1. **Always use `--json` flag** for programmatic parsing
2. **Use `auto-generate`** unless you need fine control
3. **Enable `--quality-check --auto-retry`** for production
4. **Estimate cost first** before generation
5. **Don't specify `--model`** for videos (use default wan25)
6. **Poll `video-status` every 30s** during video generation
7. **Set max 3 retry iterations** (cost/benefit balance)

---

## Example Workflow

```javascript
// 1. Estimate cost
const estimate = JSON.parse(execSync("node scripts/estimate-cost.js <project_id> --json true"));
if (estimate.costs.totalUSD > budget) return "Too expensive";

// 2. Generate
const result = JSON.parse(execSync('node scripts/auto-generate.js "Title" "Story" --json'));

// 3. Check result
if (result.status === "failed") {
  return `Failed at ${result.currentStep}: ${result.error}`;
}

// 4. Success
return `Video ready: project_id = ${result.projectId}`;
```

---

## Gotchas

1. **Storyboard polling** may timeout but storyboard is actually complete → check `project-status`
2. **Video models** - only use default, other names cause 500 error
3. **Quality check** requires Anthropic API key (separate cost)
4. **Export progress** shows 1000%+ (API returns raw value, not percentage)
5. **Credits** - 1 credit = $0.01, typical 12-shot drama costs $10-15

---

## Support

- Full docs: `SKILL.md`
- QC & Retry: `references/QUALITY-AND-RETRY.md`
- Setup: `SETUP.md`
- Tested workflow: `references/TESTED-WORKFLOW.md`
