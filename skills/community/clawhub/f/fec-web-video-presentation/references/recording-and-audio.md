# Recording And Audio

## Recording Modes

Manual mode:

- Click, Space, ArrowRight, or PageDown advances one step.
- ArrowLeft or PageUp goes back.
- Best when a human narrator is recording live.

Auto mode:

- Uses per-step durations from the project data.
- Best when narration audio is already aligned or when making a clean screen capture.

## Recording Checklist

- Browser console has no errors.
- Stage is centered and scaled without distortion.
- No horizontal or vertical scrollbars appear inside the capture frame.
- Controls are hidden unless hovered or focused.
- Current step persists only when helpful; reset it after changing chapter order or step count.
- Record a 10 second sample before doing the full take.

## Audio Policy

Audio is optional. A project may use:

- Existing narration files from the user.
- Host-native TTS or voiceover tools.
- A project-owned TTS pipeline.

Keep audio alignment provider-neutral. Store segment text and file paths in project data, but do not encode a vendor-specific API contract into the skill.
