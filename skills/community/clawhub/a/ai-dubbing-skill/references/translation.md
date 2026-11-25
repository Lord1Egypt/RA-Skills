# Translating for a dub

For every language in the job's `translations`, `captions.py` writes
`work/<id>/translate.<lang>.json`, one entry per subtitle cue of the original:

```json
{"from": "en", "to": "es", "cues": [
  {"i": 1, "start": 0.0, "end": 5.16, "source": "I think one of the ways to describe it for both Doug and I is that we're hopeful", "text": ""}
]}
```

You fill every `text`, then run `captions.py` again. The same text is spoken by the voice and
shown as the captions, so a dub and its captions always say the same thing.

A dub is translated for the ear and the clock, not the page:

- **Meaning, in the words a native speaker would say out loud.** Not word for word. Spoken
  filler ("you know", "kind of") can go; the point can't.
- **The same length in time.** The voice must finish a line in about the time the speaker took.
  Spanish, Portuguese, French and German usually run 15 to 30 % longer than English, so aim for
  fewer words than the source. `dub.py` speeds a line up to `max_speed` (1.15x by default) and lists
  any line that still doesn't fit, with how much shorter it must be. Shorten those cues and run
  `captions.py` and `dub.py` again; only changed lines are spoken again.
- **Readable as captions too.** `captions.py` warns when a cue reads faster than about 20
  characters per second (fewer for Chinese, Japanese and Korean). Shortening for the dub usually
  fixes this as well.
- **Keep names, brands and numbers.** Convert units only when the audience uses others
  (17,500 mph = 28,000 km/h).
- **Each cue stands on its own.** A sentence can run over two cues, but a cue must not end in the
  middle of a word or a name. The voice speaks the cues of one sentence as one line.
- Don't change `i`, `start` or `end`. If the original changes later (new fixes), the script asks
  you to delete the file and translate the fresh template.
- Have a native speaker listen before posting to a large audience in a language the user can't
  speak. Say this once, plainly; don't claim the dub is perfect.

`emphasis` (optional): words to colour in the captions, as in fixes.json.

Scripts: right-to-left captions (Arabic, Hebrew, Persian, Urdu) need `pip install arabic-reshaper
python-bidi`; Chinese, Japanese and Korean use a system font or download a Noto font once; Hindi,
Bengali, Tamil, Thai and other scripts that need text shaping need Pillow with libraqm
(`check_setup.py` says whether this computer has it).
