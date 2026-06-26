# LLM Gateway notes

Use the `llm` command when the user wants more than transcription:

- summaries
- action items
- structured JSON
- downstream reasoning
- extraction from a transcript that already exists

## Why this skill includes an `llm` command

AssemblyAI's older transcription summarisation fields are deprecated, and LeMUR is deprecated in favour of the LLM Gateway.

This skill therefore prepares transcript text and sends it to:

- `https://llm-gateway.assemblyai.com/v1/chat/completions`
- or the EU equivalent when configured

## Speaker-aware transcript formatting

The LLM Gateway only sees the text you send it.

For transcripts with speakers, this skill can convert the transcript into lines like:

```text
[00:00:00.000] Host: Welcome everyone
[00:00:04.200] Guest: Thanks for having me
```

That is the default `--input-format speaker-aware`.

Other options:

- `--input-format plain`
- `--input-format markdown`

## Structured outputs

When the next step is automated, prefer `--schema`.

Example:

```bash
node {baseDir}/assemblyai.mjs llm TRANSCRIPT_ID   --prompt @assets/example-prompt.txt   --schema @assets/llm-json-schema.example.json   --out ./summary.json
```

This is usually better than asking for free-form text and trying to parse it later.

## Raw request override

If you need a newer or more specialised LLM Gateway parameter, use:

```bash
node {baseDir}/assemblyai.mjs llm TRANSCRIPT_ID   --request @my-chat-body.json
```

The CLI then sends your request body as-is.

## Good default pattern for agents

1. generate transcript bundle
2. inspect agent JSON or Markdown
3. call `llm` with a schema if the next step is automated
4. keep the raw LLM response as a sidecar when debugging
