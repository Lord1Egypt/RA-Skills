---
name: flow-image-gen
description: Generate the storyboard images for a short-form video job. Walks the image_prompts[] array from a job's input.json, calls Google's Gemini image model to render each prompt as a PNG, and saves files into the job's images/ folder using the filenames specified by the timeline. Up to 4 images in parallel. Use whenever the orchestrator hands off image generation.
metadata: {"openclaw":{"requires":{"env":["GEMINI_API_KEY"],"bins":["curl","jq","base64"]},"primaryEnv":"GEMINI_API_KEY"}}
---

# flow-image-gen

Generate all storyboard images for one short-form video job using Google's
Gemini image model. Self-contained — one `curl` per image, no external services
beyond the Gemini API.

## Inputs

A job folder path, e.g. `examples/demo-job/`. Inside it, `input.json` with:

- `image_prompts[]` — array with `id`, `prompt`, optional `negative_prompt`
- `timeline[]` — used to map each prompt `id` to its output filename (`.image`)
- `resolution` — like "1080x1920" — used to derive aspect ratio
- `image_style` — object with `consistency_anchor` and `color_grade` (both appended to every prompt) for visual consistency across the set

`image_style` is read from `input.json` and merged into each prompt automatically.

## Quick run

The bundled runner implements the whole loop (parallelism, retries, skip-existing,
PNG size check). Run it as one invocation:

```bash
JOB=examples/demo-job bash skills/flow-image-gen/scripts/gen_images.sh
```

Tune concurrency with `IMAGE_GEN_PARALLEL` (default 4). The steps below document
exactly what that script does, in case you want to drive it by hand.

## Stage gate (status.json)

This skill reads and writes `<job_folder>/status.json` to support idempotent re-runs.

### Gate check — run BEFORE any other step

```bash
STATUS_FILE="$JOB/status.json"

# Initialize if absent (one-time, first skill to run)
if [ ! -f "$STATUS_FILE" ]; then
  jq -n '{
    schema_version: 1,
    stages: {images: "pending", voiceover: "pending", render: "pending"},
    artifacts: {images_completed: 0, voiceover_duration_ms: null, output_path: null},
    errors: []
  }' > "$STATUS_FILE"
fi

STAGE_STATUS=$(jq -r '.stages.images // "pending"' "$STATUS_FILE")
if [ "$STAGE_STATUS" = "done" ]; then
  echo "Skipped (images stage already done)"
  exit 0
elif [ "$STAGE_STATUS" = "failed" ]; then
  echo "FAILED: images stage previously failed. Check status.json. Exiting." >&2
  exit 1
fi

# Mark running
jq '.stages.images = "running"' "$STATUS_FILE" > "${STATUS_FILE}.tmp" && mv "${STATUS_FILE}.tmp" "$STATUS_FILE"
```

### On success — write done + artifact count

```bash
IMAGES_COUNT=$(ls -1 "$JOB/images/"*.png 2>/dev/null | wc -l)
jq --argjson count "$IMAGES_COUNT" \
  '.stages.images = "done" | .artifacts.images_completed = $count' \
  "$STATUS_FILE" > "${STATUS_FILE}.tmp" && mv "${STATUS_FILE}.tmp" "$STATUS_FILE"
```

### On any failure — write failed + error

```bash
jq --arg msg "<short error description>" \
  '.stages.images = "failed" | .errors += [{"stage": "images", "message": $msg, "time": (now | strftime("%Y-%m-%dT%H:%M:%SZ"))}]' \
  "$STATUS_FILE" > "${STATUS_FILE}.tmp" && mv "${STATUS_FILE}.tmp" "$STATUS_FILE"
```

## Provider details

- Endpoint: `https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent`
- Auth: header `x-goog-api-key: $GEMINI_API_KEY` (NOT `Authorization: Bearer` — Google rejects that with `ACCESS_TOKEN_TYPE_UNSUPPORTED`)
- Response shape: base64-encoded PNG inside `candidates[0].content.parts[].inlineData.data`
- Cost: ~$0.067 per image at 1K resolution

## Steps (what the runner does)

1. Confirm `GEMINI_API_KEY` is set. If empty, exit with error.

2. Read `<job_folder>/input.json`. Parse `image_prompts[]`, `timeline[]`, `resolution`, `image_style`.

3. Derive aspect ratio from `resolution`:
   - "1080x1920" → `"9:16"` (vertical Shorts)
   - "1920x1080" → `"16:9"` (landscape)
   - "1080x1080" → `"1:1"` (square)

4. Ensure `<job_folder>/images/` exists.

5. Extract `image_style.consistency_anchor` and `image_style.color_grade`. These two strings are appended to every prompt for visual consistency.

6. Build the work list: for each `image_prompts[i]`, the destination filename comes from the matching `timeline[].image` (matched by `id`, else positional, else `<id>.png`).

7. Generate the images — **up to 4 in parallel**, never sequentially one curl at a time (a 14-image job drops from ~4 min to ~1 min of waiting). Per image:

   a. Build the destination path: `$JOB/images/<filename>`.

   b. Skip if it already exists and is non-empty (supports re-runs after partial failure).

   c. Build the request body, merging the style anchor + color grade into the prompt:

```bash
      REQ_FILE=$(mktemp)
      FULL_PROMPT="${PROMPT}. ${STYLE_ANCHOR} Color grade: ${COLOR_GRADE}."
      jq -n --arg p "$FULL_PROMPT" --arg ar "$ASPECT_RATIO" '{
        contents: [{parts: [{text: $p}]}],
        generationConfig: {responseModalities: ["IMAGE"], imageConfig: {aspectRatio: $ar}}
      }' > "$REQ_FILE"
```

   d. Submit the request:

```bash
      RESP_FILE=$(mktemp)
      HTTP_CODE=$(curl -sS -X POST \
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent" \
        -H "x-goog-api-key: $GEMINI_API_KEY" \
        -H "Content-Type: application/json" \
        -d @"$REQ_FILE" -w "%{http_code}" -o "$RESP_FILE")
```

   e. Error check. If HTTP code is not 200, OR the response JSON has an `.error` key, report and retry once, then fail loudly.

   f. Decode the base64 image and write to disk:

```bash
      jq -r '.candidates[0].content.parts[] | select(.inlineData) | .inlineData.data' "$RESP_FILE" \
        | base64 -d > "$DEST"
```

   g. Verify the file is a valid PNG and non-trivially sized (>= 10 KB).

   h. Clean up temp files; print `OK $DEST`.

8. After the loop, print `Generated N/M images.` and exit non-zero if any image failed.

## Notes

- The `responseModalities: ["IMAGE"]` field is required. Without it, the same model returns a text description of the image instead of the image bytes.
- `negative_prompt` from `image_prompts[]` and `image_style.negative_prompt` are not used as a native negative parameter (this model doesn't support one). If exclusion matters, append them to the main prompt as natural language: "no text overlay, no watermark."
- Aspect ratio enum values the model accepts: `"1:1"`, `"3:4"`, `"4:3"`, `"9:16"`, `"16:9"`. Anything else 400s.
- Each image costs roughly $0.067 at 1K resolution. A 14-image Short costs ~$0.94 in API calls.
- If you see `ACCESS_TOKEN_TYPE_UNSUPPORTED`, the auth header is wrong (must be `x-goog-api-key`, not `Authorization: Bearer`).
- If you see `RESOURCE_EXHAUSTED` with `FreeTier` quotas, billing isn't active on the project that owns the key.

## Output

Per image: `OK <abs-path>` to stdout.
Final summary line: `Generated N/M images.`
On failure: `FAILED <path> (id=<n>): <reason>` to stderr, exit non-zero.
