# Voice, Subtitles, and Lip-Sync

## Voice bible

For each character lock:

- voice ID or actor;
- age impression, pitch, pace, energy, accent, rasp, breath;
- emotional range and forbidden tones;
- pronunciation lexicon for names, brands, classical quotations, and dialect;
- catchphrase delivery;
- approved sample line.

Do not let each generation task invent a new voice. Use the same TTS voice or recorded actor across the season.

## Performance score

Each dialogue line should carry:

- objective: what the character wants from the listener;
- tactic: persuade, threaten, bargain, evade, comfort, test;
- beat change: where the line turns;
- emphasis word and subordinate clause;
- pause before or after the turn;
- breath, laugh, swallow, or silence;
- overlap or interruption intent.

Do not send a flat line to TTS and hope emotion appears. Direct the performance.

## Voice casting matrix

For every principal and recurring character lock:

- voice ID, age impression, pitch range, pace, timbre, accent;
- comic timing and dramatic ceiling;
- volume range;
- pronunciation lexicon;
- approved greeting, threat, joke, and emotional line;
- relationship-specific tone.

Keep a separate tone for narration, phone voice, off-screen voice, and memory/flashback.

## Audio-first timing

For dialogue scenes:

1. Lock the final script and pronunciation.
2. Generate or record dialogue.
3. Measure exact line durations and pauses.
4. Build the subtitle timing from the final audio.
5. Generate or select silent video.
6. Force-align mouth motion or use an image-to-video/lip-sync model.
7. Re-time cuts to the final audio.

For action-only scenes, generate ambience and SFX after picture lock.

## Dialogue timing pass

Before final subtitles:

1. read the scene aloud at performance pace;
2. cut lines that cannot fit the action;
3. mark pauses and overlaps;
4. check names and quotations against the pronunciation lexicon;
5. confirm every line has a speaker and story function;
6. lock the audio before final subtitle timing.

## Subtitle rules

- 1–2 lines maximum.
- 10–18 Chinese characters per line, depending on platform.
- Minimum display about 1.2 seconds; prefer 2–5 seconds.
- Do not split names, numbers, quotations, or fixed phrases across lines.
- Preserve punctuation only when it changes meaning.
- Keep captions inside the lower safe area.
- Use the same font, size, outline, and shadow across the season.
- Add speaker labels only when necessary.
- Provide an SRT and a burned-in master when requested.

## Lip-sync by coverage

- wide/master: mouth detail can be approximate;
- medium dialogue: sync visible consonants and jaw cadence;
- close-up: sync the full performance, including breath and micro-pauses;
- reaction shot: no speaking mouth unless the character is actually speaking;
- insert: no mouth movement;
- off-screen dialogue: preserve the voice perspective, do not animate visible lips.

Use J/L cuts to hide sync imperfections when appropriate, but never sacrifice story clarity.

## Lip-sync rules

- Prefer final audio as the timing authority.
- Keep mouth movement subtle for stylized characters; avoid photoreal teeth.
- Use shot-level sync, not whole-episode sync.
- Accepted drift target: generally under 80–100 ms for dialogue close-ups.
- Mute auto-generated dialogue if it conflicts with the approved voice.
- For off-screen dialogue, do not force visible lip movement.
- Re-check after trimming, retiming, or changing frame rate.

## Mixing checklist

- dialogue intelligible on phone speakers;
- music ducked under dialogue;
- cold-open and cliffhanger have a clear sound event;
- no abrupt cut in room tone or music;
- stereo output, consistent loudness;
- AI-generated audio labeled according to platform policy.

## Deliverable set

- final audio stems: dialogue, music, SFX;
- voice timeline CSV;
- subtitle SRT;
- burned-in subtitle master;
- lip-sync map with shot IDs and drift notes;
- pronunciation lexicon;
- music and SFX rights log.
