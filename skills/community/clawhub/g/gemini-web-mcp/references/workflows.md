# Task Workflows

Load this reference only after the `gemini-web-mcp` Skill has selected the user's capability lane.

The current 0.2.x runtime has a low-token compatibility server plus narrow primary profiles. The dedicated `gemini-assist` MCP server (`gemini-mcp-assist`) now implements the assistance workflows below; `gemini-create` and `gemini-account` remain pending. All of them share the same services instead of duplicating business logic.

## 1. Ask Gemini for a Second Opinion

Use for critique, alternative reasoning, code review, design review, or comparing model opinions.

Current routes:

```text
compact: chat(message=..., model="flash"|"pro", thinking_level="standard"|"extended")
primary: gemini_chat(message=..., model=..., thinking_level=..., temporary=true)
```

Process:

1. Give Gemini the relevant context, not the entire unrelated conversation.
2. Ask a concrete question or request a concrete critique.
3. Separate Gemini's answer from the calling agent's own conclusion.
4. Resolve disagreements or present them explicitly.
5. Continue the user's task; do not stop at “Gemini said…”.

Dedicated tool (`gemini-mcp-assist`):

```text
gemini_ask
```

## 2. Quick Web Search

Use for current facts, documentation discovery, comparison, or a small number of sources.

On the compatibility servers, use `chat` or `gemini_chat` with an explicit request to search current sources and return source URLs. The dedicated `gemini-mcp-assist` server exposes the grounded facade `gemini_search` directly.

Only label the result as grounded when the response actually contains observed source URLs or equivalent structured source evidence.

`gemini_search` returns this shape:

```text
answer
sources[]
observed_at
grounding_state = grounded | answer_only | unavailable | failed
```

Escalate to Deep Research when:

- the question is broad or disputed;
- multiple source classes must be reconciled;
- the user wants a durable report;
- quick search returns no source evidence.

Target dedicated tool:

```text
gemini_search
```

## 3. Understand an Image

Use for screenshots, UI mockups, charts, diagrams, photos, game scenes, and visual errors.

Current routes:

```text
compact: chat(message=<task>, image_path=<path>)
primary: gemini_chat(message=<task>, image_paths=[...])
```

Process:

1. State what should be inspected or compared.
2. Preserve image identity when several images are involved.
3. Ask for evidence tied to visible regions rather than a generic description.
4. Return the analysis to the calling agent.
5. Continue the surrounding task, such as fixing code or revising a design.

Dedicated tool (`gemini-mcp-assist`):

```text
gemini_understand_image
```

## 4. Understand Files, URLs, and Mixed Inputs

Use for documents, source files, PDFs, web pages, images plus code, or multiple evidence types.

Current primary routes:

```text
gemini_upload_file
gemini_analyze_url
gemini_chat(image_paths=[...])
```

For mixed inputs, run the smallest bounded calls needed, preserve the source identity of every result, then synthesize the evidence in the calling agent.

Do not claim that a URL was fetched or a file was understood if the structured result only shows an accepted prompt without source or Artifact evidence.

Dedicated tool (`gemini-mcp-assist`):

```text
gemini_understand
```

Its typed input shape:

```json
{
  "task": "Compare the implementation with the design",
  "inputs": [
    {"id": "design", "kind": "image", "path": "..."},
    {"id": "spec", "kind": "file", "path": "..."},
    {"id": "live", "kind": "url", "url": "..."},
    {"id": "notes", "kind": "text", "text": "..."}
  ]
}
```

## 5. Deep Research

Use for multi-source investigation, market/technical research, long comparisons, or a report the agent will cite or reuse.

Current route:

```text
gemini_deep_research(
  query=...,
  wait_for_completion=false,
  retain_chat=true
)
```

Default behavior:

1. Start asynchronously.
2. Preserve every returned local and upstream identifier.
3. Return control to the calling agent immediately.
4. Poll or resume by the preserved handle when possible.
5. Retrieve and save a Markdown report when complete.
6. Read the report and use it in the user's requested output.

Do not restart the same research merely because the initial MCP wait ended.

Dedicated tool (`gemini-mcp-assist`):

```text
gemini_research
```

The dedicated tool starts the operation by default and returns an opaque `operation_id`.

## 6. Generate or Edit an Image

Current routes:

```text
compact: create(prompt=..., type="image", image_path=<optional reference>)
compact: edit(image_path=..., prompt=...)
primary: gemini_generate_media(... media_type="image")
```

Process:

1. Choose a destination appropriate to the user's task.
2. Generate or edit.
3. Verify the returned Artifact.
4. Use the Artifact in the next step.
5. Only expose technical metadata when it helps the user or another tool.

Target dedicated tools:

```text
gemini_generate_image
gemini_edit_image
```

## 7. Generate Video or Music

Current routes:

```text
compact: create(prompt=..., type="video"|"music")
primary: gemini_generate_media
primary: gemini_generate_music
```

Treat queued/running results as operations, not failures and not completed media.

Process:

1. Start the generation.
2. Preserve operation and upstream IDs.
3. Resume rather than duplicate.
4. Verify the final media Artifact.
5. Use or attach the file in the user's task.

Target dedicated tools:

```text
gemini_generate_video
gemini_generate_music
```

## 8. Explicit Account Work

Use only when the user asks to inspect or change Gemini account data.

Current compact routes:

```text
history(action=...)
account(action=...)
scheduled(action=...)
prompts(action=...)
cleanup(...)
```

Current narrow primary routes:

```text
GEMINI_TOOLS=history
GEMINI_TOOLS=history-organize
GEMINI_TOOLS=account-read
GEMINI_TOOLS=scheduled-admin
GEMINI_TOOLS=prompts
```

Target account tools:

```text
gemini_history
gemini_notebooks
gemini_scheduled
gemini_gems
gemini_prompts
gemini_account
gemini_cleanup
```

Use list/search/read before mutation. Preserve returned IDs. Claim mutation success only after authoritative read-back.
