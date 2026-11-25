# Amber phone task demo

From the Amber project root, run:

```bash
node demo/first-call-demo.js
```

Follow a repair-shop inquiry from the original OpenClaw prompt through recipient and objective approval, a short call excerpt, and the pickup instructions. The walkthrough uses fictional dialogue and works without credentials, OpenClaw, or a running bridge.

## Setup wizard recording

This directory contains demo recordings of the interactive setup wizard.

## Live Demo

**🎬 [Watch on asciinema.org](https://asciinema.org/a/l1nOHktunybwAheQ)** - Interactive player with copyable text and adjustable playback speed.

## What the Demo Shows

The demo wizard guides users through:

1. **Twilio Configuration**
   - Account SID validation (must start with "AC")
   - Mock credential-validation UX only in the demo recording (the real runtime wizard does live verification)
   - Phone number format validation (E.164)

2. **OpenAI Configuration**
   - Mock API-key-validation UX only in the demo recording (the real runtime wizard does live verification)
   - Project ID and webhook secret (required for OpenAI Realtime)
   - Voice selection (alloy/echo/fable/onyx/nova/shimmer)

3. **Server Setup**
   - Port configuration
   - Automatic ngrok detection and tunnel discovery
   - Public URL configuration

4. **Optional Integrations**
   - OpenClaw gateway (brain-in-loop features)
   - Assistant personalization (name, operator info)
   - Call screening customization

5. **Post-Setup**
   - Automatic dependency installation
   - TypeScript build
   - Clear next steps with webhook URL

## Demo Flow

> Important: `demo-wizard.js` is a playback/demo artifact. It does **not** call Twilio or OpenAI and must not be described as a real validator. The real interactive validator is `runtime/setup-wizard.js` via `npm run setup`.

The demo uses these example values (not real credentials):
- **Twilio SID:** AC1234567890abcdef1234567890abcd
- **Phone:** +15551234567
- **OpenAI Key:** paste-your-openai-api-key
- **OpenAI Project ID:** proj_demo1234567890abcdef
- **OpenAI Webhook Secret:** paste-your-openai-webhook-secret
- **Assistant:** Amber
- **Operator:** John Smith
- **Organization:** Acme Corp
