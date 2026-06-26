# Continuance v1.3.0

This release adds a new meditation-audio capability to Continuance.

## New feature: soft spoken meditation audio

Continuance can now generate a local meditation-style audio track from the guidance text itself.

### What it does
- detects the language from the generated guidance text
- selects a soft Chinese or English voice accordingly
- slows the speaking pace for a calmer meditative cadence
- mixes in a light randomized ambient background beneath the speech
- outputs a ready-to-send mp3 for meditation-style delivery

## New bundled script
- `scripts/generate_meditation_audio.py`

## Intended experience
This is designed for:
- daily meditation
- quiet reflection
- contemplative spiritual guidance
- a softer voice-note style delivery that feels more like guided rest than ordinary narration

## Notes
- Background remains subtle and non-dramatic
- Voice stays dominant and clear
- Language follows the generated text automatically
