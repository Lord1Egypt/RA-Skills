# FitCheck Face Scan: Stress, Heart Rate & Mood Challenge

**60 seconds on camera: stress, a heart-rate estimate, mood, micro-expressions, eye contact, genuine smile and composure, plus voice tension if the microphone is on. Scan before and after, challenge your friends, play the deception challenge, read any video. Tap Send to my agent and the result lands with your agent as clean JSON, no copy-paste; it keeps the score.**

Live at [emo.city](https://emo.city?utm_source=clawhub&utm_medium=skill) | Powered by [EmoPulse](https://www.emopulse.app)

## Install

```
openclaw skills install @gv66co/fitcheck-workout-readiness
```

Then say "fitcheck scan me". The scan runs in the browser at emo.city: no app, no account, the first scan is free.

## What you can do

| Ask your agent | What happens |
|---|---|
| "fitcheck scan me before my workout" | 60-second scan, a short read and one takeaway |
| "fitcheck before and after" | two scans, side by side, with what changed |
| "fitcheck challenge my friends" | one link for everyone, the agent keeps the scoreboard |
| "fitcheck deception challenge" | one asks, one answers, the meters decide (for fun) |
| "fitcheck read this video" | a moment-by-moment read with the tense spots flagged |
| "fitcheck pre-workout check" | a quick read and a casual note for today's session |
| "fitcheck analyse this photo with my key" | optional, through the EmoPulse API with your own RapidAPI key |

## What your agent gets back

```json
{
  "mood": "neutral",
  "stress": 34,
  "heart_rate_bpm": 74,
  "hrv_ms": 42,
  "eye_contact": 81,
  "genuineness": 72,
  "felt_vs_shown": 18,
  "voice_tension": 20,
  "micro_expressions": 3,
  "standout_moments": 2
}
```

Your agent gives you a link with a one-time code. After the scan you tap SEND_TO_AGENT and the agent picks up these numbers by itself (they wait up to 15 minutes and are deleted once read). COPY_TEXT still works as the manual way.

Before-and-after adds a `change` block; a challenge returns `players` and the winners (calmest, steadiest eyes, most genuine smile).

## Optional: the same engine as an API

[EmoPulse Face Analysis on RapidAPI](https://rapidapi.com/emocity/api/emopulse-face-analysis): one POST with a photo or clip, one JSON object per face (stress, expression mix, eye contact, micro-expression and genuine-smile counts). Free BASIC plan with a hard monthly limit. Set your own key as `EMOPULSE_RAPIDAPI_KEY`; the agent reads it from the environment, never from the chat, tells you before it uploads a file and waits for your yes. The API does not return a heart rate; that comes from the live browser scan.

## Data

The camera and microphone are processed in the browser and never uploaded; what is sent is anonymous usage analytics and the numbers of each scan (see the emo.city privacy policy). SEND_TO_AGENT passes only those summary numbers to your agent, once. Scan only people who agreed. Not a medical device.

## License

EmoPulse's on-device perception architecture is patented (1 patent granted, 2 pending).

The text of this skill is published on ClawHub under MIT-0. The emo.city app, the EmoPulse engine and the API are separate hosted services with their own terms: [emopulse.app/license](https://www.emopulse.app/license) and [emo.city/privacy](https://emo.city/privacy).
