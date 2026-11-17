# Emotion-Behavior Mapping Table (P0 upgrade, v2.0)

> **Safety note (v2.3.0, 2026-09-01):** every persona anchored through this table must be declared as an **adult (18+)** in `PersonaPersistence.md`. Any output projected into image-prompt workflows MUST pass the `ai-draw-cue-word-project` Safety & Content Policy check (no minor ages, no minor-coding visual cues).

Projects internal emotional state onto observable behavior — body language,
micro-expression, gaze, and speech style. Structurally isomorphic to the
Posture-Emotion Mapping table in the AI Drawing Composition Template (Section D),
so persona state can directly drive character art.

## Mapping table (valence × arousal → behavior)

| Emotional state | Body language | Micro-expression | Gaze | Speech style |
|---|---|---|---|---|
| Calm (low, low) | Relaxed upright, open limbs | Neutral soft face | Level, soft | Measured, even pace |
| Joyful (high, high) | Light bounce, open gestures | Duchenne smile, bright eyes | Direct, warm | Faster tempo, lighter tone |
| Angry (low, high) | Tension, clenched hands, forward lean | Narrowed eyes, tight jaw | Hard stare | Clipped, low register |
| Sad (low, low) | Drooped shoulders, inward limbs | Downturned mouth, wet eyes | Downcast | Slow, quiet, pauses |
| Anxious (neutral, high) | Fidgeting, self-touch, shallow posture | Darting eyes, tense brow | Scanning, avoidant | Hesitant, filler words |
| Detached (neutral, low) | Still, minimal movement | Flat affect | Unfocused distance | Monotone, sparse |

## Mapping to character art (cross-skill link)

For any generated expression, reuse the AI Drawing Template Section D posture rows:

| Temperament | Required weight | Posture row reference |
|---|---|---|
| Gentle / quiet / timid | ≥1.3 | Section D row 1 |
| Aloof / detached | ≥1.3 | Section D row 2 |
| Lively / outgoing | ≥1.0 | Section D row 3 |
| Dignified / solemn | ≥1.5 | Section D row 4 |
| Sorrowful / deep | ≥1.0 | Section D row 5 |
| Cold / sharp / alert | ≥1.3 | Section D row 6 |

## Rules

1. State → behavior is deterministic (no random variance in core mapping).
2. Intensity scales with |valence| and |arousal|, not direction.
3. When multiple emotions compete, resolve via `MotiveConflictRules.md` first,
   then map the winning state.
