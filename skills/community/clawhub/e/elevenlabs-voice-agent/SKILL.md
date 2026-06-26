---
name: elevenlabs-voice-agent
description: Build and manage ElevenLabs Conversational AI voice agents with Twilio phone integration. Use when creating AI phone agents (cold callers, appointment setters, customer service), configuring voice/LLM settings, connecting Twilio phone numbers, or debugging voice agent issues. Covers NEPQ sales framework, objection handling, and call qualification flows.
version: 1.0.0
---

# ElevenLabs Voice Agent

Build AI phone agents using ElevenLabs Conversational AI API + Twilio.

## Setup Flow

1. Create agent via ElevenLabs dashboard or API
2. Configure voice, TTS model, LLM, and system prompt
3. Purchase/connect Twilio phone number via ElevenLabs phone integration
4. Test and iterate on script, voice settings, turn-taking

## Optimal Voice Settings (Proven)

| Setting | Value | Why |
|---------|-------|-----|
| TTS Model | v3 conversational | Best quality for phone calls |
| Expressive mode | ON | Natural inflection |
| Stability | 0.45 | Natural variation without inconsistency |
| Similarity | 0.75 | Recognizable voice |
| Speed | 1.2x | Fast enough for cold calls (API max) |
| Streaming latency | 4 | Balance speed vs quality |
| Turn timeout | 2s | Don't wait too long for response |
| Eagerness | eager | Jump in naturally |
| Speculative turn | ON | Faster responses |
| Cascade timeout | 3s | Handle pauses |

## Recommended Voices

- **Alexandra** (`kdmDKE6EkgrWrrykO9Qt`): Pleasant female, great for cold calls
- **Hope** (`OYTbf65OHHFELVut7v2H`): Warm female backup

## LLM Choice

Use `gpt-4o-mini` for phone agents — speed is critical, latency kills calls.

## Key API Endpoints

```
POST https://api.elevenlabs.io/v1/convai/agents/create
PATCH https://api.elevenlabs.io/v1/convai/agents/{agent_id}
GET https://api.elevenlabs.io/v1/convai/agents/{agent_id}
POST https://api.elevenlabs.io/v1/convai/twilio/phone-numbers — Connect Twilio number
```

## Enable Phone Features

Enable these tools on the agent: `voicemail_detection`, `end_call`, `background_voice_detection`

## NEPQ Sales Framework

For appointment-setting agents, use Neuro-Emotional Persuasion Questioning:
- Permission-based opening ("Do you have a quick moment?")
- Question-led qualification (don't pitch, ask)
- Emotional connection questions before booking
- Soft close with specific time options

## Twilio Integration

1. Get Twilio Account SID + Auth Token
2. Use ElevenLabs API to create phone number connection
3. Phone number is provisioned automatically by ElevenLabs
4. Calls route: Twilio → ElevenLabs → AI agent

## Common Issues

- **Robotic voice**: Switch to v3 conversational model, enable expressive mode
- **Slow responses**: Use gpt-4o-mini, increase streaming latency optimization
- **Cuts off caller**: Increase turn timeout, reduce eagerness
- **Sounds scripted**: Add personality to system prompt, lower stability slightly
