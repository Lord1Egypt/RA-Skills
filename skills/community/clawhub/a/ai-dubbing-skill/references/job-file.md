# The job file (dub.json)

One JSON file describes the whole job. Paths are relative to the job file's folder.

```json
{
  "videos": [
    {"file": "clips/names.mp4", "id": "names"},
    {"file": "clips/crew.mp4", "id": "crew", "focus_x": 0.52}
  ],
  "language": "en",
  "vocab": ["Bob Behnken", "Dragon", "SpaceX"],
  "translations": ["es", "pt-BR"],
  "voices": {"es": "kokoro:em_alex", "pt-BR": "kokoro:pm_alex"},
  "dub": {"background": "voiceover", "max_speed": 1.15, "original_volume": 0.18},
  "post_to": ["TIKTOK", "INSTAGRAM", "YOUTUBE"],
  "outputs": [
    {"id": "vertical", "style": "pop", "canvas": "9:16", "fit": "crop", "languages": ["es", "pt-BR"],
     "style_overrides": {"max_width": 0.72}},
    {"id": "youtube", "style": "clean", "canvas": "source", "languages": ["es"]}
  ],
  "work": "work",
  "out": "dubbed"
}
```

## Dubbing

- `translations`: the languages to dub into. `captions.py` writes a translation template per video
  and language (`references/translation.md`).
- `voices`: one voice per language, `engine:voice` (`references/voices.md`). Left out, a language
  gets the first free voice listed for it.
- `dub.background`: what plays under the new voice.
  - `voiceover` (default): the original sound, turned down to `original_volume` (0.18, about
    -15 dB) wherever anyone speaks and left as it was in between. Music and sound effects stay;
    the original voice is faintly audible under the dub, as in a documentary voice-over.
  - `separate`: the original voice removed with demucs (`pip install demucs`, about 2 GB with
    PyTorch; slow on a laptop, roughly the video's length or more), so only music and sound stay
    under the dub. Best for videos with music under the speech.
  - `none`: the dubbed voice only.
- `dub.max_speed` (1.0 to 1.3, default 1.15): how much faster than normal a line may be spoken to
  fit. Above about 1.15 speech starts to sound rushed; shorten the translation instead.
- `dub.model`: the ElevenLabs model (`eleven_multilingual_v2` default, `eleven_flash_v2_5`,
  `eleven_turbo_v2_5`, `eleven_v3`). Only for `elevenlabs:` voices.

## videos

- `file` (required): the video. `id`: a short name used in file names (default: the file name).
- `subtitles`: an existing .srt or .vtt to use instead of transcribing (an .srt or .vtt with the
  same name next to the video is found automatically). Word times inside each cue are estimated,
  so word-highlight styles turn the highlight off for it.
- `language`: when this video's language differs from the job's. With a subtitle file, set it unless
  the text is in a non-Latin script (Japanese, Chinese, Korean, Arabic, Hebrew, Thai, Hindi, Russian
  and Greek are recognised); otherwise English is assumed.
- `focus_x` (0 to 1) and `position` (0.05 to 0.95): this video's crop and caption height, over the output's.
  `position` can also be one per output, for example `{"youtube": 0.7}` to lift the captions above a
  name title in the 16:9 version only.

## Job settings

- `language`: the spoken language (en, es, pt, de, ja...). Leave it out to let the engine detect it;
  set it for short clips, which are easy to misdetect.
- `vocab`: names, brands and terms. They are passed to the transcriber as hints and used by
  `fix.py --report` to spot near-misses.
- `post_to`: where the videos will go (platform names as in `posting.md`). Only Step 6 reads it;
  the scripts ignore it.
- `work`, `out`: folders (default `work` and `dubbed`).
- `font_file`: a .ttf/.otf for every output (a brand font, or a font for a script the bundled fonts lack).
- `preset`: x264 speed (`veryfast` default; `medium` gives slightly smaller files and takes longer).

## outputs

Each output is one version of every video:

- `id` (required, unique): used in file names (`<id>.<output>.<lang>.mp4`).
- `style`: a preset name (`references/styles.md`) or a path to your own style .json.
- `style_overrides`: any style setting, for this output only (colours, size, position, words...).
- `canvas`: `source` (keep the shape, at most 1920 px on the long side), `9:16`, `4:5`, `1:1`, `16:9`.
- `fit`: when the shape changes: `crop` (fills the frame; set `focus_x` so the speaker stays in),
  `blur` (the whole frame on a blurred copy of itself: wide shots, screen recordings, two people)
  or `pad` (black bars).
- `position`: caption height, 0.05 (top) to 0.95 (bottom). Left out, it comes from the style
  (`clean` sits higher on 9:16, clear of the apps' text), and with `fit: blur` or `pad` the
  captions sit just under the picture.
- `languages`: which languages to make (default: the spoken one, with the original sound, plus every
  dubbed language). Usually only the dubbed ones: the original video already exists.
- `sounds`: true to burn sound tags (`[laughter]`) from fixes.json too; they are always in the SRT.
- `font_file`: a font for this output only.
