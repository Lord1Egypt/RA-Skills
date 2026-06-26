# Large File Handling

Use this strategy for all session files. Batching keeps the Agent's context manageable and avoids compression issues.

## Step 1: Assess File Size

```bash
wc -l {session}.jsonl
```

| Line count | Strategy |
|-----------|----------|
| < 150 | Read whole file at once |
| 150 – 800 | Read in batches of 100–150 lines |
| > 800 | Preprocess with jq (extract text only), then batch |
| > 2000 | Preprocess + truncate to last 200 lines (last resort) |

## Step 2a: Small File — Read at Once

Use the Read tool on the full file. Parse all events and convert in one pass.

## Step 2b: Batched Reading

Read the file in chunks using line offsets. For each batch:

```bash
# Batch 1: lines 1–150
sed -n '1,150p' {session}.jsonl

# Batch 2: lines 151–300
sed -n '151,300p' {session}.jsonl

# ... continue until end of file
```

Or use the Read tool with `offset` and `limit` parameters.

For each batch, parse the JSON lines, extract content (see [platforms/openclaw.md](platforms/openclaw.md) — Message Content Block Extraction), and convert to clawpage markdown. Accumulate the output.

**Cross-batch tool call pairing**: A `toolCall` message and its matching `toolResult` may appear in different batches. Track unpaired toolCalls (by `id`) across batches. When a toolResult appears, match it to the buffered toolCall even if it was in a prior batch.

Write the accumulated output to `{projectDir}/chats/.tmp/{timestamp}.md` incrementally (or in one write at the end).

## Step 2c: jq Preprocessing (> 800 lines)

Strip binary content and extract text to a plain-text intermediate file, then batch over that.

```bash
jq -r '
  if .type == "session" then
    "[session] cwd=" + (.cwd // "")
  elif .type == "message" then
    "[message:" + .message.role + " ts=" + .timestamp + "]\n" +
    (.message.content[] |
      if .type == "text" then .text
      elif .type == "thinking" then "[thinking]\n" + (.thinking // "")
      elif .type == "toolCall" then "[toolCall id=" + (.id // "") + " name=" + (.name // "") + "]\n" + (.arguments | tostring)
      else ""
      end
    )
  elif .type == "model_change" then
    "[model_change] " + (.modelId // "") + " (" + (.provider // "") + ")"
  elif .type == "thinking_level_change" then
    "[thinking_level_change] " + (.thinkingLevel // "")
  elif .type == "compaction" then
    "[compaction] tokensBefore=" + (.tokensBefore | tostring)
  elif .type == "custom" then
    "[custom] " + (.customType // "custom")
  else empty end
' {session}.jsonl > {projectDir}/chats/.tmp/{name}-text.txt
```

Note: This strips images and binary data. Note in the output `description` that images were omitted.

## Step 3: Truncation (> 2000 lines, last resort)

If the preprocessed text is still too large:

```bash
tail -n 200 {projectDir}/chats/.tmp/{name}-text.txt > {projectDir}/chats/.tmp/{name}-truncated.txt
```

Note the truncation in the output `description` frontmatter field.

## Notes

- Do NOT modify or summarize content during preprocessing or batching — verbatim only
- If a toolCall and its toolResult span batch boundaries, resolve them in the final output
- Prefer full conversion (all events, all content) over truncation
