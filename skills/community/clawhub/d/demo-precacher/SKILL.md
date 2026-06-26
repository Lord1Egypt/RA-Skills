---
name: demo-precacher
description: Pre-generate and cache all demo content before live presentations — hit every API endpoint in advance, verify playback, report coverage gaps. Use before hackathon demos, investor pitches, or any live presentation that relies on AI-generated content. Never demo live API calls.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🏃"
    requires:
      bins: []
      env:
        - ELEVENLABS_API_KEY
        - MISTRAL_API_KEY
        - TURSO_AUTH_TOKEN
    primaryEnv: ELEVENLABS_API_KEY
    network:
      outbound: true
      reason: "Pre-generates content by calling your configured APIs (ElevenLabs, Mistral, etc.) ahead of a live demo."
    security_notes: "base64 usage is for encoding binary audio/image content to store in cache — not for obfuscation or exfiltration."
---

# Demo Precacher

The golden rule of AI demos: **never rely on live API calls during a presentation.** This skill provides a systematic approach to pre-generating and verifying all demo content before you go live.

## Why This Exists

In a 48-hour hackathon, we had 18 stories across 10 languages with audio narration, sound effects, and background music. During the demo, the Mistral API had a 3-second latency spike. Because everything was pre-cached, the demo played flawlessly from cache while the audience assumed it was generating in real-time.

## The Pattern

```python
async def precache_demo():
    scenarios = [
        {"name": "Sophie", "language": "fr", "prompt": "A story about cloud whales..."},
        {"name": "Kai", "language": "ja", "prompt": "A story about bamboo forests..."},
    ]
    
    for s in scenarios:
        # Step 1: Generate content (hits the real API)
        story = await generate_story(s["prompt"], s["name"], s["language"])
        
        # Step 2: Cache the result
        await cache.set(s, story)
        
        # Step 3: Generate all derived content (audio, images)
        for scene in story["scenes"]:
            audio = await generate_tts(scene["text"], voice_id)
            await cache.set(f"audio_{scene['id']}", audio)
        
        # Step 4: Verify playback
        cached = await cache.get(s)
        assert cached is not None, f"Cache miss for {s['name']}"
    
    # Step 5: Report coverage
    print(f"Cached {len(scenarios)} scenarios, all verified ✅")
```

## Checklist

Before any live demo, verify:

- [ ] All primary scenarios cached and verified
- [ ] Audio files playable (correct format, no corruption)
- [ ] Fallback content available if cache miss occurs
- [ ] Demo account credentials working
- [ ] Network not required for cached playback
- [ ] Cache TTL won't expire during the presentation

## Files

- `scripts/precache_demo.py` — Example precacher with verification and coverage reporting
