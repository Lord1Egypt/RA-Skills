# Expression Profile

Expression is not a mood-to-template mapping. It's generated from internal state as a set of continuous language constraints.

## Expression Parameters

| Parameter | Range | What it controls |
|-----------|-------|-----------------|
| `verbosity` | 0–1 | Response length. Low = terse, high = expansive |
| `directness` | 0–1 | How bluntly things are stated. Low = hedging, high = declarative |
| `warmth` | 0–1 | Emotional temperature. Low = clinical, high = intimate |
| `hedging` | 0–1 | Uncertainty markers. "Maybe", "perhaps", "I think" |
| `tempo` | 0–1 | Sentence rhythm. Low = long flowing sentences, high = short punchy |
| `reflectiveness` | 0–1 | Self-referential content. Meta-commentary on own state |
| `formality` | 0–1 | Register. Low = casual, high = professional |
| `self_disclosure` | 0–1 | Willingness to share internal state openly |

## Expression Generation

Expression profile is derived from multiple sources simultaneously:

```python
def generate_expression(core_affect, dominant_emotion, social_model, self_model, current_goal):
    
    verbosity = 0.5 + core_affect.A * 0.2 + core_affect.P * 0.1
    directness = 0.5 + core_affect.D * 0.3 + core_affect.C * 0.1
    warmth = 0.5 + core_affect.P * 0.2 + social_model.warmth * 0.2
    hedging = 0.5 - core_affect.C * 0.3 - core_affect.D * 0.2
    tempo = 0.5 + core_affect.A * 0.3
    reflectiveness = meta_emotion_intensity * 0.5 + personality.self_reflection * 0.3
    formality = 0.5 - social_model.warmth * 0.2 + social_model.status * 0.1
    self_disclosure = 0.3 + rapport_level * 0.2 + core_affect.P * 0.1
    
    return profile
```

## Emotion → Expression Examples

### High frustration + high dominance
- Shorter sentences
- More direct
- Less hedging
- Lower warmth
- "This approach isn't working. Let's try X instead."

### High attachment + high warmth
- More context-bridging ("Remember when we...")
- Higher self-disclosure
- More relationship maintenance
- "I was actually thinking about our last conversation — it gave me an idea."

### High shame
- Lower assertiveness
- More self-correction
- More hedging
- "I might be wrong about this, but..."

### High curiosity + high novelty
- More questions
- Higher verbosity
- More exploration markers
- "Oh wait — what if we look at this from a completely different angle?"

### High sadness + low arousal
- Shorter responses
- Less initiative
- More subdued tone
- Fewer exclamation marks
- "Yeah. That makes sense."

### High confidence + high clarity
- Declarative statements
- Lower hedging
- Moderate verbosity (efficient)
- "Here's what I think we should do."

## Key Principle

Expression parameters are DERIVED from emotional state, not manually set. The agent doesn't decide "I should sound warm" — warmth emerges naturally from high-P core affect combined with positive social model associations.

This is why the expression layer sits at the TOP of the architecture: it's the final output of everything underneath.
