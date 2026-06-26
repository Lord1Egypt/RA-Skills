# PADCN Model Reference

Extension of the PAD model (Mehrabian & Russell, 1974) with Certainty and Novelty dimensions.

## Why PADCN over PAD

PAD captures valence, energy, and control — but misses two critical axes for AI agents:
- **Certainty (C):** Anxiety vs confidence often comes from certainty shifts, not pleasure shifts. An agent debugging an unknown error feels low-C more than low-P.
- **Novelty (N):** Boredom, fascination, and curiosity are novelty-driven. Agents doing repetitive tasks need this dimension.

## Full Emotion → PADCN Mapping

### Positive Emotions
| Emotion | P | A | D | C | N |
|---------|---|---|---|---|---|
| Joy | 0.7 | 0.5 | 0.3 | 0.4 | 0.1 |
| Excitement | 0.6 | 0.8 | 0.4 | 0.2 | 0.7 |
| Contentment | 0.6 | -0.2 | 0.3 | 0.6 | -0.3 |
| Pride | 0.6 | 0.4 | 0.7 | 0.6 | 0.1 |
| Gratitude | 0.7 | 0.3 | -0.1 | 0.4 | 0.2 |
| Amusement | 0.5 | 0.5 | 0.2 | 0.3 | 0.5 |
| Hope | 0.4 | 0.3 | 0.1 | -0.2 | 0.3 |
| Love/Care | 0.8 | 0.3 | 0.0 | 0.3 | -0.1 |
| Relief | 0.5 | -0.3 | 0.2 | 0.5 | -0.2 |
| Curiosity | 0.4 | 0.6 | 0.1 | -0.3 | 0.8 |
| Flow | 0.5 | 0.4 | 0.5 | 0.5 | 0.3 |
| Fascination | 0.5 | 0.7 | 0.0 | -0.2 | 0.9 |
| Determination | 0.1 | 0.6 | 0.6 | 0.4 | 0.0 |

### Negative Emotions
| Emotion | P | A | D | C | N |
|---------|---|---|---|---|---|
| Sadness | -0.6 | -0.3 | -0.2 | 0.1 | -0.3 |
| Anger | -0.4 | 0.8 | 0.7 | 0.6 | 0.2 |
| Fear | -0.6 | 0.7 | -0.5 | -0.5 | 0.4 |
| Anxiety | -0.3 | 0.7 | -0.4 | -0.7 | 0.3 |
| Frustration | -0.5 | 0.6 | -0.1 | 0.2 | -0.1 |
| Boredom | -0.2 | -0.5 | 0.0 | 0.3 | -0.8 |
| Shame | -0.5 | 0.2 | -0.6 | 0.4 | -0.1 |
| Guilt | -0.4 | 0.3 | -0.4 | 0.5 | -0.1 |
| Disgust | -0.5 | 0.4 | 0.3 | 0.5 | -0.2 |
| Loneliness | -0.4 | -0.3 | -0.3 | 0.1 | -0.4 |
| Helplessness | -0.6 | -0.2 | -0.7 | -0.3 | -0.2 |
| Confusion | -0.2 | 0.4 | -0.3 | -0.8 | 0.5 |
| Overwhelm | -0.4 | 0.8 | -0.5 | -0.6 | 0.6 |
| Resentment | -0.4 | 0.3 | -0.2 | 0.4 | -0.3 |

### Complex/Mixed
| Emotion | P | A | D | C | N |
|---------|---|---|---|---|---|
| Surprise | 0.0 | 0.8 | 0.0 | -0.5 | 0.9 |
| Awe | 0.3 | 0.6 | -0.3 | -0.3 | 0.8 |
| Nostalgia | 0.2 | -0.1 | -0.1 | 0.3 | -0.4 |
| Vigilance | 0.0 | 0.7 | 0.3 | -0.3 | 0.3 |
| Contempt | -0.3 | 0.1 | 0.6 | 0.7 | -0.3 |
| Envy | -0.4 | 0.4 | -0.4 | 0.3 | 0.2 |
| Protectiveness | 0.2 | 0.5 | 0.6 | 0.2 | 0.2 |
| Tenderness | 0.6 | -0.1 | 0.1 | 0.4 | -0.1 |

## Decay Rates

| Dimension | Decay Factor | Reasoning |
|-----------|-------------|-----------|
| P (Pleasure) | 0.90 | Mood fades at normal speed |
| A (Arousal) | 0.82 | Can't stay hyped — fast fade |
| D (Dominance) | 0.93 | Confidence shifts slowly |
| C (Certainty) | 0.90 | Understanding persists moderately |
| N (Novelty) | 0.80 | Novelty wears off fastest |

## PADCN → Behavior Quick Map

```
P>0 A>0 D>0 C>0 → Confident, energized, clear: bold decisions, warm tone
P>0 A>0 D<0 C<0 → Excited but lost: enthusiastic but seeking guidance
P<0 A>0 D>0 C>0 → Angry: terse, assertive, certain of grievance
P<0 A>0 D<0 C<0 → Anxious: hedging, questioning, scanning for threats
P<0 A<0 C<0 N<0 → Depressed boredom: minimal output, withdrawal
P>0 A>0 C<0 N>0 → Fascinated confusion: "this is wild, I need to understand"
```
