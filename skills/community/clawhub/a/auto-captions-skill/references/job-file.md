# The job file (captions.json)

One JSON file describes the whole job. Paths are relative to the job file's folder.

```json
{
  "videos": [
    {"file": "clips/intro.mp4", "id": "intro"},
    {"file": "clips/speed.mp4", "id": "speed", "focus_x": 0.57, "position": 0.6},
    {"file": "clips/talk.mp4", "subtitles": "clips/talk.en.srt", "language": "en"}
  ],
  "language": "en",
  "vocab": ["Nichole Ayers", "ISS", "ham radio"],
  "translations": ["es", "pt-BR"],
  "post_to": ["TIKTOK", "INSTAGRAM", "YOUTUBE"],
  "outputs": [
    {"id": "vertical", "style": "pop", "canvas": "9:16", "fit": "crop", "focus_x": 0.5},
    {"id": "square", "style": "highlight", "canvas": "1:1", "fit": "blur",
     "style_overrides": {"active_box": {"color": "#0EA5E9", "radius": 18, "pad": [16, 6], "text": "#FFFFFF"}}},
    {"id": "youtube", "style": "clean", "canvas": "source", "languages": ["en"], "sounds": true}
  ],
  "work": "work",
  "out": "captioned",
  "font_file": null,
  "preset": "veryfast"
}
```

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
- `translations`: caption languages to add. `captions.py` writes a template per video and language.
- `post_to`: where the videos will go (platform names as in `posting.md`). Only Step 6 reads it;
  the scripts ignore it.
- `work`, `out`: folders (default `work` and `captioned`).
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
- `languages`: which caption languages to make (default: the spoken one plus every finished translation).
- `sounds`: true to burn sound tags (`[laughter]`) from fixes.json too; they are always in the SRT.
- `font_file`: a font for this output only.
