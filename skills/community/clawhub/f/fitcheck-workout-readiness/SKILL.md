---
name: emocity-biometric-scan
version: "1.5.1"
description: "Face scan from the browser camera in 60 seconds: stress, a heart-rate estimate, mood, micro-expressions, eye contact, genuine smile, composure and, with the microphone on, voice tension, and the result comes back to the agent by itself after the user taps Send to my agent, no copy-paste. Use when the user explicitly asks for a face scan, a stress or heart-rate check from the camera, a before-and-after comparison, a challenge with friends or the deception challenge game. Optional: analyse a photo or clip the user hands over through the EmoPulse API with their own RapidAPI key from the environment; that file is uploaded. Not a medical device. Built on EmoPulse, a patented on-device perception architecture."
argument-hint: 'fitcheck scan me, fitcheck before and after, fitcheck challenge my friends, fitcheck deception challenge, fitcheck check my stress, fitcheck read this video, fitcheck analyse this photo with my key, fitcheck pre-workout check, fitcheck post-workout check, fitcheck before my call, fitcheck two-minute reset'
allowed-tools: Bash
homepage: https://emo.city?utm_source=clawhub&utm_medium=skill
author: emopulse
license: MIT-0
user-invocable: true
metadata:
  openclaw:
    emoji: "🧠"
    homepage: "https://emo.city?utm_source=clawhub&utm_medium=skill"
    envVars:
      - name: EMOPULSE_RAPIDAPI_KEY
        required: false
        description: "The user's own RapidAPI key for EmoPulse Face Analysis. Only for the optional photo or clip analysis; the browser scan needs no key."
    tags:
      - fitness
      - workout
      - health
      - game
      - party-game
---

# FitCheck Face Scan: Stress, Heart Rate & Mood Challenge

Sixty seconds on camera and you see what your face is broadcasting right now: stress, a heart-rate estimate, mood, micro-expressions, eye contact, genuine smile and composure, plus voice tension if the microphone is on. Scan before and after, compare the two, or turn it into a challenge with friends. It runs in the browser at emo.city, nothing to install.

## Cost

The first scan is free, no signup. More scans need an emo.city account on a paid plan, from $4.99 a month: https://emo.city/pricing?utm_source=clawhub&utm_medium=skill

## When to use

- The user asks for FitCheck by name, a face scan, or a stress or heart-rate check from the camera.
- Before and after something: a workout, a hard call, a date, a meditation.
- A game with friends: who stays the calmest, or the deception challenge.
- A video they want read moment by moment.
- A photo or clip they hand over and want analysed with their own RapidAPI key.

## When not to use

- To scan someone who has not agreed to it.
- For medical questions. Not a medical device.

## Try saying

- "FitCheck, scan me before my workout."
- "Before and after: scan me now and again after the call."
- "Challenge my friends: who stays the calmest?"
- "Let's play the deception challenge."
- "Check my stress."
- "Read this video with FitCheck."
- "FitCheck pre-workout check."
- "FitCheck post-workout check."
- "FitCheck before my call."
- "FitCheck two-minute reset."

## Play modes

- **Before and after.** Scan, do the thing, scan again. The agent returns both results and what changed.
- **Challenge your friends.** Each player gets their own agent link (one code per player), scans and taps SEND_TO_AGENT; anyone on the CHALLENGE link pastes COPY_TEXT instead. The agent keeps the scoreboard.
- **Deception challenge.** One asks, one answers, the live meters do the talking: DECEPTION, STRESS, MICRO_EXPR, EYE_CONTACT, AUTHENTIC, from OPEN to HELD BACK. The app's own line: for fun, not a real lie detector.
- **Check a video.** UPLOAD a clip, for example your own take before you post it, and get a moment-by-moment read with the tense spots flagged.

## Presets

- **Pre-workout / post-workout.** Scan right before training and within 10 minutes after. Return context "workout".
- **Before a call.** Scan 5 minutes before an important call and right after. Return context "call".
- **Two-minute reset.** Scan, breathe slowly for two minutes, scan again. Return context "reset".

For a single scan, add "session_note": "lighter" when the stress reading is high (over about 60), "as planned" between 30 and 60, "go for it" under about 30. It is a casual note about how the face looks today, not advice and not a medical reading.

```
{"context": "workout", "before": {...}, "after": {...}, "change": {...}, "session_note": "as planned"}
```

## Workflow

The scan result comes back to you without the user copying anything. Each scan gets its own one-time code.

1. Make a random one-time code (32 hex characters). Keep it in this conversation only; never write it to a file.

   ```
   CODE=$(openssl rand -hex 16 2>/dev/null || python3 -c "import secrets; print(secrets.token_hex(16))")
   ```

2. Give the user the link with that code: `https://emo.city/?agent=<CODE>&utm_source=clawhub&utm_medium=skill` (Chrome or Edge). The page takes the code out of the address bar and keeps it for that tab only.
3. Mode: LIVE (camera, up to 2 minutes), UPLOAD (photo or video; a single photo gives no heart rate) or CHALLENGE (the link for friends). Before and after, the presets and challenges need two or more scans, and one is free: say so before the first scan and link https://emo.city/pricing?utm_source=clawhub&utm_medium=skill for the rest.
4. Tell them: when the scan ends, tap **SEND_TO_AGENT** under the readings. Nothing is sent to you until they tap it.
5. Wait for the result. Check every 5 seconds for up to 5 minutes:

   ```
   for i in $(seq 1 60); do
     R=$(curl -s --max-time 10 "https://api.emo.city/api/v1/agent-result/$CODE")
     case "$R" in *'"waiting"'*) sleep 5 ;; *) echo "$R"; break ;; esac
   done
   ```

   `{"status": "ready", "result": {...}}` carries the JSON below, already parsed. It can be read once; after that the same code answers `waiting` again. `{"status": "waiting"}` means the user has not tapped yet.
6. Fallback: if 5 minutes pass, or the answer is anything other than `waiting` or `ready` (an error, no connection), or the user scans in the Google Play app, where the link code does not carry over (app link: https://play.google.com/store/apps/details?id=city.emo.www.twa&referrer=utm_source%3Dclawhub%26utm_medium%3Dskill ), ask them to tap COPY_TEXT and paste the summary into the chat, then parse it as shown below.
7. Reply with a short read and one light takeaway. For before-and-after and challenges, return the scoreboard. A second scan needs a new code and a new link, and an emo.city plan once the free scan is used, at https://emo.city/pricing?utm_source=clawhub&utm_medium=skill . Offer it once, then drop it.

## Result format

With SEND_TO_AGENT the `result` object already has the JSON keys below. The COPY_TEXT summary looks like this (numbers are an example):

```
EMOCITY SCAN REPORT
---
Emotion: neutral
Felt-vs-shown: 18%
Stress: 34%
Genuineness: 72%
Eye Contact: 81%
HR: 74bpm
HRV: 42ms
Voice Tension: 20%
Micro-Expressions: 3
Standout moments: 2
---
```

Turn it into:

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

`HR: N/A` becomes `null`, a missing HRV line becomes `null`, percentages are integers from 0 to 100.

**Before and after:** return `{"before": {...}, "after": {...}, "change": {"stress": -12, "heart_rate_bpm": -9, "eye_contact": 4}}` plus one sentence in plain words.

**Challenge:** return `{"players": [{"name": "Ana", "stress": 22, "eye_contact": 88, "genuineness": 80, "felt_vs_shown": 12}], "calmest": "Ana", "steadiest_eyes": "Ana", "most_genuine_smile": "Ana"}`. In the deception challenge the lowest `felt_vs_shown` wins. Keep scoreboards in the conversation; do not write them to files.

## Reading the numbers

- **Stress**: under about 30 relaxed, a good day to push; 30 to 60 some tension, keep it moderate; over about 60 tense, a good moment to slow down.
- **Heart-rate estimate**: from subtle colour changes in the face. `null` means the signal was too weak (light, movement); never report 0.
- **Mood**: the dominant expression. **Micro-expressions**: brief flickers the scan flagged.
- **Eye contact, genuineness, composure**: how steady, open and relaxed the face looked.
- Tendencies, not verdicts about a person. Game results are for fun.

## Optional: photo or clip analysis with the user's own RapidAPI key

The engine behind the scan is also a hosted API, EmoPulse Face Analysis: https://rapidapi.com/emocity/api/emopulse-face-analysis (free BASIC plan, 50 requests a month; every plan has a hard monthly limit, so a key cannot run up overage charges). Unlike the browser scan, this path uploads the file. Run it only when all three hold:

1. **Key from the environment.** Read `EMOPULSE_RAPIDAPI_KEY`, which the user sets in their own environment; suggest a dedicated key they can revoke. Never ask for the key in the chat, never print it, never write it to a file. If it is not set, send them to the RapidAPI page and stop.
2. **Their media, with consent.** Only a photo or clip they hand you, of themselves or of someone who knows and agreed. Never fetch a picture of a person from the web.
3. **Say it, then wait.** One line first: "This uploads the file to the EmoPulse API through RapidAPI." Run only after a yes.

The key goes to curl through standard input, so it never appears in command arguments:

```
printf 'X-RapidAPI-Key: %s\n' "$EMOPULSE_RAPIDAPI_KEY" | curl -s -X POST "https://emopulse-face-analysis.p.rapidapi.com/api/v1/analyze/image" \
  -H @- \
  -H "X-RapidAPI-Host: emopulse-face-analysis.p.rapidapi.com" \
  -F "file=@/path/to/photo.jpg"
```

Photo: JPG or PNG up to 10 MB, up to 4 faces. Clip: MP4 or MOV up to 100 MB to `/api/v1/analyze/video`, same command. The response has `faces_detected` and a `faces` list; map each face to the same JSON keys: `avg_stress` to `stress`, `dominant_emotion` to `mood`, `avg_eye_contact` to `eye_contact`, `avg_authenticity` to `genuineness`, `avg_deception` to `felt_vs_shown`, plus `micro_expressions` and `genuine_smiles`. The API does not return a heart rate; set `heart_rate_bpm` to `null`. If `faces_detected` is 0, say no face was found and stop.

## Data

The camera and microphone are processed in the browser and never uploaded. What leaves the device is anonymous usage analytics and the numbers of each scan, saved to the account for signed-in users and kept as anonymous scans without one, as the emo.city privacy policy describes. SEND_TO_AGENT sends only the summary numbers shown above, no video, no audio, no name: they wait on api.emo.city under the one-time code for up to 15 minutes and are deleted as soon as the agent reads them. The agent's only call is that GET with the code. The optional API path above uploads the one file the user chose.
