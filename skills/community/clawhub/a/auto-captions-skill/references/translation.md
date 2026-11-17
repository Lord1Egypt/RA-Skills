# Translations

For every language in the job's `translations`, `captions.py` writes
`work/<id>/translate.<lang>.json`, one entry per subtitle cue of the original:

```json
{"from": "en", "to": "es", "cues": [
  {"i": 1, "start": 0.0, "end": 1.36, "source": "We won't have a lot of time to talk,", "text": ""}
]}
```

Fill every `text`, then run `captions.py` again. It writes the SRT/VTT/transcript for that
language, and `render.py` makes the captioned videos.

How to translate captions well:

- Meaning, not word for word, in the words a native speaker would say out loud.
- About as long as the source. A cue on screen for 2 seconds can't hold twice the words; the
  script warns when a translation reads faster than about 20 characters per second (fewer for
  Chinese, Japanese and Korean). Shorten those.
- Keep names and brands. Convert units when the audience uses others (17,500 mph = 28,000 km/h)
  and say so in the cue only if the speaker's number matters.
- Don't change `i`, `start` or `end`. If the original changes later (new fixes), the script asks
  you to delete the file and translate the fresh template.
- Have a native speaker check before posting to a large audience in a language the user can't read.

Word-by-word highlight needs the time of every spoken word, which a translation doesn't have, so
translated versions show whole chunks without the moving highlight.

Scripts: right-to-left (Arabic, Hebrew, Persian, Urdu) needs `pip install arabic-reshaper
python-bidi`; Chinese, Japanese and Korean use a system font or download a Noto font once;
Hindi, Bengali, Tamil, Thai and other scripts that need text shaping need Pillow with libraqm
(`check_setup.py` says whether this computer has it). Without it, use the SRT and the platform's
own captions for that language.
