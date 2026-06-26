# Effects Guide

## Denoise Parameters
- `prop_decrease`: 0.0-1.0, how much noise to remove
- `stationary`: True for consistent noise (fan/hum), False for variable noise
- `noise_sample`: Usually first 0.5s of recording

## Speed/Pitch
- Speed > 1.0: Faster playback (chipmunk effect with naive method)
- Pitch +12 semitones: One octave up
- Pitch -12 semitones: One octave down

## Volume Normalization
- Peak (-1 dBFS): Prevents clipping
- RMS (-20 dBFS): Consistent perceived loudness
- LUFS: Broadcast standard (integrated loudness)
