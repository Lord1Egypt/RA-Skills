# Voices

Each translated language gets one voice, set in the job file:

```json
"voices": {"es": "kokoro:em_alex", "pt-BR": "kokoro:pm_alex", "de": "piper:de_DE-thorsten-high",
           "ja": "elevenlabs:<voice ID>"}
```

A language without a voice uses the first free one listed for it. `python3 <skill>/scripts/voices.py
list` prints every language and voice; `voices.py sample dub.json es` makes each free voice say the
first translated line of the first video (`dubbed/voice-samples/`), so the user picks by listening.

## Free voices, on the user's computer

Nothing is sent anywhere, there is no per-minute cost, and the files download once to the user's
cache folder (not the project and not the skill folder).

| Engine | Install | Languages | Licence |
|---|---|---|---|
| Kokoro (kokoro-onnx) | `pip install kokoro-onnx soundfile` | English (US, UK), Spanish, French, Italian, Portuguese (Brazil), Hindi | Apache-2.0 model; about 120 MB once |
| Piper | `pip install piper-tts` | German, Dutch, Polish, Russian, Ukrainian, Czech, Danish, Finnish, Hungarian, Romanian, Greek, Persian, Norwegian, Swedish, Vietnamese | per voice, listed by `voices.py list`; 60 to 120 MB per voice |

Only Piper voices whose licence allows commercial use are listed (CC0, CC BY 4.0, Apache-2.0).
Voices under a non-commercial or share-alike licence, or with no stated licence, are left out on
purpose, even when they sound good. The Vietnamese voice is CC BY 4.0: credit "VAIS-1000 dataset"
in the post or the video description.

Both run on an ordinary laptop CPU: a 30-second clip takes well under a minute per language.

What they can't do: they are stock voices, not the speaker's voice, and Kokoro's Japanese and
Chinese are not good enough to post, so those languages are left out of the free route.

## The user's own ElevenLabs key

`elevenlabs:<voice ID>` with `ELEVENLABS_API_KEY` set. Use it for:

- languages the free voices don't speak (Japanese, Chinese, Korean, Turkish, Arabic, Indonesian and
  the rest of ElevenLabs' list);
- the user's own voice: they make a voice clone of themselves in their ElevenLabs account and give
  you its voice ID. Only ever their own voice, or a voice they have the speaker's written consent
  for. Never clone or imitate anyone else.

The translated text is sent to ElevenLabs and uses the user's credits (about one credit per
character with `eleven_multilingual_v2`, half with `eleven_flash_v2_5`; set it with
`"dub": {"model": "eleven_flash_v2_5"}`). `dub.py` prints the character count and stops; ask the user,
then run it again with `--confirm-cost`. Lines are cached, so a rerun only pays for lines that changed.

## Matching the speaker

- Pick a voice of the same apparent gender and age as the speaker; ask if it isn't obvious.
- One voice per language for a whole series, so a channel sounds the same every week.
- The voice is never presented as the speaker's own unless it is their own clone.
