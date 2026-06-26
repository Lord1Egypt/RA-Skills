# Speaker mapping reference

This skill treats speaker naming as a first-class workflow rather than a cosmetic afterthought.

## Three ways to get useful speaker names

## 1. Generic diarisation only
Enable speaker diarisation during transcription:

```bash
node {baseDir}/assemblyai.mjs transcribe ./meeting.mp3 --speaker-labels
```

This produces generic labels such as `A`, `B`, or `Speaker A`.

Use this when:

- you only need separation, not identity
- you are not sure who the speakers are yet
- you want to name them later

## 2. Manual speaker mapping
Provide your own display names or channel names:

```bash
node {baseDir}/assemblyai.mjs format ./transcript.json   --speaker-map @assets/speaker-map.example.json
```

Accepted shapes:

### JSON object
```json
{
  "A": "Host",
  "B": "Guest",
  "channel:0": "Agent",
  "channel:1": "Customer"
}
```

### Rich JSON object
```json
{
  "A": { "display": "Host", "source": "manual" },
  "B": { "display": "Guest", "source": "manual" }
}
```

### Simple text / CSV-style
```text
A=Host
B=Guest
channel:0=Agent
channel:1=Customer
```

## 3. AssemblyAI speaker identification
Use Speech Understanding to map diarised speakers to names or roles.

### Known values
```bash
node {baseDir}/assemblyai.mjs understand TRANSCRIPT_ID   --speaker-type role   --known-speakers "agent,customer"
```

### Rich speaker profiles
```bash
node {baseDir}/assemblyai.mjs understand TRANSCRIPT_ID   --speaker-type name   --speaker-profiles @assets/speaker-profiles-name.example.json
```

Use known values when you only know the final labels.
Use rich profiles when descriptions help disambiguate similar speakers.

## Precedence

When rendering outputs, the skill applies speaker names in this order:

1. manual `--speaker-map`
2. AssemblyAI speaker identification mapping
3. fallback generic label

That means you can:

- let AssemblyAI do the first pass
- override only the mistakes manually
- keep stable speaker names across rerenders

## Channel vs diarisation

### Prefer `--multichannel` when:
- the recording is a call with clean left/right separation
- each channel already corresponds to one participant

### Prefer `--speaker-labels` when:
- the recording is a single mixed channel
- the speakers overlap or change within one channel
- you want speaker turns rather than channel IDs

You can still use a manual `channel:0` / `channel:1` map when multichannel is the right tool.

## Why this matters for downstream agents

A plain transcript often loses who said what.
This skill preserves speaker-aware structure in both:

- Markdown
- agent JSON

That makes later summarisation, action-item extraction, and role-specific analysis much more reliable.
