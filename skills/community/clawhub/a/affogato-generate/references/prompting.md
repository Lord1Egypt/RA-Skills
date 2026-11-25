# Prompting notes for Affogato models

## Images
- Subject first, then setting, then style, lens and lighting. One idea per
  sentence; no bag of adjectives.
- Name the medium ("35 mm photo", "flat vector illustration", "oil painting")
  and the framing ("close-up portrait", "wide establishing shot").
- Aspect ratio, size and number of images are parameters, not prompt text —
  read `model <id>` for the exact enum values.
- Editing models (`image-editing` feature): source image in the slot,
  prompt describes the change only ("make the jacket red, keep everything
  else").
- Character consistency: models with `supports_characters` accept a
  `character_id` from the user's Affogato characters.

## Video
- Describe one continuous shot: subject, action, camera move, setting,
  mood. Explicit camera language works ("slow dolly in", "static camera",
  "handheld").
- Keep the action simple for 5–10 s clips. Image-to-video: the image fixes
  the composition; the prompt describes motion only.
- Duration, resolution and audio are priced parameters; quote with
  `estimate` before generating. Renders take 1–5 minutes: use `--wait`.

## Audio
- Text-to-speech rows take `text` (priced per 1,000 characters) and a
  `voice` value; `model <id>` lists the voices as an enum where the model
  has fixed voices.
- Music/SFX rows take `prompt` plus `duration`.

## Costs
- Prices are credits (the user's plan credits). Typical: a fast image
  1–5 credits, a flagship image 20–40, 5 s of video 100–500, a minute of
  speech 10–30. Always quote; never assume.
