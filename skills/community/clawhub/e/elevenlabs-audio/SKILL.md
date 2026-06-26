---
name: elevenlabs-audio
description: Create and manage voices, speech synthesis, audio projects, and conversational AI agents in ElevenLabs via the ElevenLabs API. Use this skill when users want to generate text-to-speech audio, manage voice libraries, create AI agents, or automate voice workflows.
---

# ElevenLabs

![ElevenLabs](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/elevenlabs.svg?v=2)

Access ElevenLabs via the ElevenLabs API with managed API key authentication. Manage voices, speech assets, audio projects, and voice workflow tasks from chat.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=elevenlabs-audio) for hosted connection flows and credentials so you do not need to configure ElevenLabs API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect ElevenLabs |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect ElevenLabs |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│   ElevenLabs     │
│   (User Chat)   │     │   (API Key)  │     │      API          │
└─────────────────┘     └──────────────┘     └──────────────────┘
          │                       │                       │
          │  1. Install Plugin    │                       │
          │  2. Pair Device       │                       │
          │  3. Connect ElevenLabs│                       │
          │                       │  4. Secure Proxy       │
          │                       │  5. API Requests        │
          │                       │                       │
          ▼                       ▼                       ▼
    ┌──────────┐           ┌──────────┐           ┌──────────┐
    │  SKILL   │           │ Dashboard│           │ ElevenLabs│
    │  File    │           │ Auth     │           │  Studio  │
    └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for ElevenLabs again."

## Quick Start

```bash
# List integrations
clawlink_list_integrations

# List ElevenLabs tools
clawlink_list_tools --integration elevenlabs

# Search for a specific tool
clawlink_search_tools --query "voice" --integration elevenlabs
```

## Authentication

All ElevenLabs tool calls are authenticated automatically by ClawLink using the user's connected ElevenLabs API credentials.

**No API key is required in chat.** ClawLink stores the API key securely and injects it into every ElevenLabs API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=elevenlabs and connect ElevenLabs.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `elevenlabs` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration elevenlabs
```

**Response:** Returns the live tool catalog for ElevenLabs.

### Reconnect

If ElevenLabs tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=elevenlabs
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration elevenlabs`

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm ElevenLabs is connected.
2. Call `clawlink_list_tools --integration elevenlabs` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `elevenlabs`.
5. If no ElevenLabs tools appear, direct the user to https://claw-link.dev/dashboard?add=elevenlabs.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                      │
│                                                             │
│  Example: List voices → Get details → Show results         │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  list → get → describe → preview → confirm → call           │
│                                                             │
│  Example: Describe tool → Preview changes → User approves   │
│           → Execute update                                  │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, search, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Tool Reference

### Voices

| Tool | Description | Mode |
|------|-------------|------|
| `elevenlabs_list_voices` | List all voices in the account | Read |
| `elevenlabs_get_voice` | Get voice details | Read |
| `elevenlabs_add_voice` | Add a custom voice by uploading audio | Write |
| `elevenlabs_edit_voice` | Update voice name, audio, or settings | Write |
| `elevenlabs_delete_voice` | Delete a custom voice | Write |
| `elevenlabs_get_audio_from_sample` | Get audio from a voice sample | Read |

### Text-to-Speech

| Tool | Description | Mode |
|------|-------------|------|
| `elevenlabs_text_to_speech` | Convert text to speech audio | Write |
| `elevenlabs_download_history_items` | Download generated audio | Read |
| `elevenlabs_delete_history_item` | Delete a history item | Write |

### Conversational AI (ConvAI)

| Tool | Description | Mode |
|------|-------------|------|
| `elevenlabs_create_conversational_agent` | Create a ConvAI agent | Write |
| `elevenlabs_get_convai_agents_summaries` | List ConvAI agents | Read |
| `elevenlabs_get_convai_agent` | Get agent configuration | Read |
| `elevenlabs_delete_convai_agent` | Delete an agent | Write |
| `elevenlabs_create_convai_knowledge_base` | Add knowledge base document | Write |

### Projects& Chapters

| Tool | Description | Mode |
|------|-------------|------|
| `elevenlabs_list_projects` | List audio projects | Read |
| `elevenlabs_add_project` | Create a new project | Write |
| `elevenlabs_get_chapters` | Get chapters in a project | Read |
| `elevenlabs_convert_chapter` | Convert chapter to audio | Write |

### Dubbing

| Tool | Description | Mode |
|------|-------------|------|
| `elevenlabs_dub_a_video_or_an_audio_file` | Dub video/audio to another language | Write |
| `elevenlabs_get_dubbing_project_metadata` | Get dubbing project status | Read |
| `elevenlabs_delete_dubbing_project` | Delete a dubbing project | Write |

### Pronunciation Dictionaries

| Tool | Description | Mode |
|------|-------------|------|
| `elevenlabs_add_pronunciation_dictionary_from_rules` | Create pronunciation dictionary | Write |
| `elevenlabs_add_rules_to_the_pronunciation_dictionary` | Add rules to dictionary | Write |

## Code Examples

### List voices

```bash
clawlink_call_tool --tool "elevenlabs_list_voices" \
  --params '{}'
```

### Text to speech

```bash
clawlink_call_tool --tool "elevenlabs_text_to_speech" \
  --params '{
    "text": "Hello, this is a test of the ElevenLabs text to speech system.",
    "voice_id": "YOUR_VOICE_ID"
  }'
```

### Create a ConvAI agent

```bash
clawlink_call_tool --tool "elevenlabs_create_conversational_agent" \
  --params '{
    "name": "Customer Support Agent",
    "prompt": "You are a helpful customer support agent.",
    "voice_id": "YOUR_VOICE_ID"
  }'
```

### Add knowledge base document

```bash
clawlink_call_tool --tool "elevenlabs_create_convai_knowledge_base" \
  --params '{
    "agent_id": "YOUR_AGENT_ID",
    "url": "https://example.com/docs"
  }'
```

## Security & Permissions

- Access is scoped to the connected ElevenLabs account's voices, projects, and agents.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (deleting voices, agents, projects) are marked as high-impact and must be confirmed.
- ConvAI agent configurations may include sensitive business logic; confirm before modifications.
- Some features (dubbing, high-quality voices) may require premium subscription tiers.

## Notes

- Voice cloning requires clear audio samples without background noise.
- Audio generation may take time for longer texts; consider async patterns for large outputs.
- ConvAI agents require configuration of prompt, voice, and potentially knowledge base.
- Some API features are tier-dependent (free vs. paid plans).

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration elevenlabs`. |
| Missing connection | ElevenLabs is not connected. Direct the user to https://claw-link.dev/dashboard?add=elevenlabs. |
| `Voice not found` | The voice ID does not exist or is not accessible. |
| `Invalid API key` | The ElevenLabs API key is invalid. Reconnect the integration. |
| `Conversion pending` | Audio conversion is still processing. Poll for completion. |
| Write rejected | User did not confirm a write action. Always confirm before executing writes. |

### Troubleshooting: Tools Not Visible

1. Check that the ClawLink plugin is installed:
   ```bash
   openclaw plugins list
   ```
2. If the plugin is installed but tools are missing, tell the user to send `/new` as a standalone message to reload the catalog.
3. If a fresh chat does not help, run:
   ```bash
   openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
   openclaw gateway restart
   ```
4. After restart, tell the user to send `/new` again and retry.

### Troubleshooting: Invalid Tool Call

1. Ensure the integration slug is exactly `elevenlabs`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [ElevenLabs API Documentation](https://elevenlabs.io/docs/api-reference/overview)
- [ElevenLabs API Reference](https://elevenlabs.io/docs/api-reference)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=elevenlabs-audio
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=elevenlabs-audio)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
