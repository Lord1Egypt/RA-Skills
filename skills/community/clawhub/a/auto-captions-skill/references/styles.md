# Caption styles

No platform publishes evidence that one caption style beats another; these presets cover the looks
most common in short-form video. Pick by the video and the account, then keep it consistent: a
recognisable style is part of an account's look. Show the user `styles.py`'s sheet on their own
video rather than describing styles.

| Preset | Looks like | Good for |
|---|---|---|
| `pop` | 1 to 3 words, heavy font, thick outline, spoken word yellow, keywords green | Default for TikTok, Reels, Shorts |
| `bold` | 1 or 2 big condensed uppercase words (a small word or a number goes with the next word), spoken word green | High-energy talking heads, hooks |
| `highlight` | up to 4 words, spoken word on a coloured pill | Brands (set the pill to the brand colour) |
| `reveal` | words appear as spoken, up to 2 lines | Explainers, calm voices |
| `lines` | two short lines, spoken word cyan | Fast talkers, longer clips |
| `clean` | sentence case on a soft dark band, 2 lines, low in the frame | YouTube, LinkedIn, podcasts, B2B, accessibility |
| `minimal` | small lowercase words, soft shadow | Lifestyle, aesthetic, voiceovers |
| `one-word` | one huge word at a time (a small word or a number goes with the next word) | Hooks and very short clips (tiring past 30 s) |

## Settings (in a style file or `style_overrides`)

- `font` (a bundled file: Poppins-ExtraBold.ttf, Poppins-Bold.ttf, Anton-Regular.ttf, Inter.ttf,
  or any .ttf/.otf path), `weight` (for Inter: Medium, SemiBold, Bold, Black).
- `size`: text size in pixels on a 1080-wide (or 1080-tall) frame; it scales with the output.
- `color`, `active` (spoken word), `keyword` (emphasis words), `stroke` (outline width),
  `stroke_color`, `shadow` (`{"dx":0,"dy":6,"alpha":0.45,"blur":3}`), `box` (a band behind each
  line: `{"color":"#000000","alpha":0.6,"radius":10,"pad":[18,6]}`), `active_box` (a pill behind
  the spoken word: `{"color":"#7C3AED","radius":18,"pad":[16,6],"text":"#FFFFFF"}`).
- `uppercase`, `lowercase`, `reveal` (words appear as spoken).
- `words` (most words on screen), `chars` (most characters per line), `lines` (1 to 3), `pause`
  (a silence longer than this, in seconds, starts a new caption), `min_show`.
- `position` (0.05 top to 0.95 bottom, the middle of the caption block), `position_tall` (the
  same, used on 9:16 instead), `max_width` (share of the frame width), `line_gap`.

Make a brand style: copy a preset to the user's project (`brand.json`), change colours and font,
and set `"style": "brand.json"`.

## Placement

No app publishes a safe zone for normal posts; the numbers around are ad specs and third-party
measurements, and the apps change their layouts. What holds across TikTok, Reels and Shorts: the
right edge has a column of buttons and the bottom fifth holds the account name and post text.
Captions centred, about 55 to 65% down the frame, clear both. The review sheet draws each app's
buttons on the frame so the user can see it. Move captions above a lower-third name title or a
slide's text, and below a face rather than over the mouth.

## Readability rules the scripts apply

- Chunks break at sentence ends, commas and pauses; they never end on a small word ("the", "of")
  and keep numbers with what follows ("9 or 10 minutes"), as long as that fits on the lines the
  style allows.
- Line breaks inside a caption come after punctuation, never after "the" or inside a name.
- Captions stay on screen through short pauses, then clear.
- A word wider than the frame at the style's size is reported; lower `size` for that output.
