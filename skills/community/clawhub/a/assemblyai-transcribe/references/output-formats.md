# Output formats

This skill deliberately exposes multiple output shapes because different follow-on tasks benefit from different formats.

## 1. Markdown transcript (`--export markdown`)

Best for:

- another LLM or agent reading the transcript
- a human reviewing the result
- preserving speaker names and timestamps in a compact way

Structure:

- `# AssemblyAI Transcript`
- `## Metadata`
- `## Speaker Map` (when relevant)
- `## Transcript`
- optional sections for chapters, key phrases, topics, entities, sentiment, translations, custom formatting, and word-level timestamps

Design goals:

- stable headings
- compact metadata
- speaker-aware transcript lines
- easy skimming
- easy chunking by downstream agents

## 2. Agent JSON (`--export agent-json`)

Best for:

- scripts and deterministic downstream processing
- tools that need stable key names
- preserving merged speaker display names without re-implementing mapping logic

Top-level shape:

- `schema_version`
- `generated_at`
- `source`
- `transcript`
- `features`
- `speaker_map`
- `utterances`
- `words` (only when requested)
- `chapters`
- `highlights`
- `topics`
- `entities`
- `sentiment`
- `translated_texts`
- `speech_understanding`

Schema asset:

- `assets/transcript-agent-json-schema.json`

## 3. Raw JSON (`--export json`)

Best for:

- debugging exact AssemblyAI responses
- validating new API fields
- preserving the original response for later re-rendering

## 4. Bundle mode (`--bundle-dir`)

Best for:

- AI-agent pipelines
- multi-step workflows
- keeping several exports together without inventing filenames later

Bundle contents typically include:

- `*.transcript.md`
- `*.agent.json`
- `*.raw.json`
- `*.manifest.json`

With `--all-exports`, the bundle also includes:

- `*.paragraphs.txt`
- `*.sentences.txt`
- `*.srt`
- `*.vtt`

The manifest is especially useful because another agent can read a single JSON file and discover the rest.

## Speaker map precedence

When rendering Markdown or agent JSON, this skill resolves speaker display names in the following order:

1. manual speaker map (`--speaker-map`)
2. AssemblyAI speaker identification mapping
3. fallback label generated from the raw speaker/channel token

That means:

- AssemblyAI can generate an initial mapping
- you can later override just one or two speakers without redoing everything

## Why bundle mode is the default recommendation

Agents often do better when:

- the main transcript is in Markdown
- the canonical machine-readable copy is separate
- filenames are explicit
- a manifest tells them where everything lives

That is why the recommended default workflow is:

```bash
node {baseDir}/assemblyai.mjs transcribe INPUT --bundle-dir ./out --all-exports
```
