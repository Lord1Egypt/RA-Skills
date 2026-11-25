# Example: two NASA clips dubbed into Spanish and Brazilian Portuguese

Two short clips of retired NASA astronaut Bob Behnken talking about designing the SpaceX Crew
Dragon, dubbed into Spanish and Brazilian Portuguese with the free Kokoro voices, captioned in the
same words, cut to 9:16 for TikTok, Reels and Shorts, with a posting plan for four accounts.

What the skill did, in order:

1. `transcribe.py dub.json`: local faster-whisper ("small"), with `vocab` hints. Raw result:
   [`work/names/transcript.txt`](work/names/transcript.txt).
2. Proofreading: the agent read every line and wrote [`work/crew/fixes.json`](work/crew/fixes.json)
   (punctuation, which decides where a sentence ends and so how the voice phrases it) and chose the
   words to stress in the captions.
3. `captions.py`: subtitle files and translation templates. The agent translated each cue for the
   ear: in [`translate.es.json`](work/names/translate.es.json) "cursing our names" became "no
   maldigan nuestros nombres", and spoken filler ("kind of") was dropped so each line
   fits the time the speaker took.
4. Voices: the free male Kokoro voices `em_alex` (Spanish) and `pm_alex` (Brazilian Portuguese),
   to match the speaker. `voices.py sample dub.json es` lets you hear every free voice say your first
   line before you pick.
5. `dub.py`: spoke every line, fitted it to its slot and mixed it over the original, which stays
   quietly underneath (`"background": "voiceover"`). The report,
   [`work/names/dub.es.json`](work/names/dub.es.json), lists each line's time, slot and speed: every
   line fit between 0.9x and 1.0x, so none had to be shortened.
6. `render.py --preview`: the review sheets ([`review-names.jpg`](dubbed/names/review-names.jpg)),
   then `render.py`: four videos with the dubbed sound and matching captions
   ([`names.vertical.es.mp4`](dubbed/names/names.vertical.es.mp4)).
7. `post_plan.py post.json`: [`plan.md`](plan.md) and one WoopSocial request per post in
   [`requests/posts/`](requests/posts/). Every dubbed post is marked as AI-generated content for
   TikTok and Instagram, and the plan lists the "Altered or synthetic content" answer to give in
   YouTube Studio. The accounts are placeholders, so the plan lists them as not connected.

The soundtracks (`work/<id>/dub.<lang>.wav`) are left out of this folder to keep the repo small.
Make them again from this folder, with the free voices installed:

```
python3 ../../scripts/dub.py dub.json
python3 ../../scripts/render.py dub.json --preview
```

The source footage and the voices are credited in [CREDITS](CREDITS.md).
