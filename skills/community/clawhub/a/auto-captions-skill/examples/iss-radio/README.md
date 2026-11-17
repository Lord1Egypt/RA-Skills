# Example: two NASA clips, captioned in English and Spanish

Two short clips of NASA astronaut Nichole Ayers on the International Space Station, captioned for
TikTok, Reels and Shorts (9:16, `pop` style), for YouTube (16:9, `clean` style) and for LinkedIn
(4:5 on a blurred background, `clean` style, the captions under the picture),
with a Spanish version for a Spanish-language account and a posting plan for five accounts.

What the skill did, in order:

1. `transcribe.py captions.json`: local faster-whisper ("small"), with `vocab` hints. Raw result:
   [`work/speed/transcript.txt`](work/speed/transcript.txt). It missed the word "where" and
   dropped most commas, which decide where captions break.
2. Proofreading: the agent read every line and wrote [`work/intro/fixes.json`](work/intro/fixes.json)
   and [`work/speed/fixes.json`](work/speed/fixes.json): restored "where" and the punctuation, and
   chose the words to stress ("16 times", "17,500", "25 times", "9 or 10 minutes"). NASA's own
   subtitle file for this video spells her name "Nicole"; the captions here use "Nichole", as on
   NASA's name title in the video.
3. `captions.py`: subtitle files ([`speed.en.srt`](captioned/speed/speed.en.srt), `.vtt`, `.txt`) and a
   translation template the agent filled ([`translate.es.json`](work/speed/translate.es.json)). The
   speed is converted for the Spanish audience: 17,500 mph became 28 000 km/h. Where the Spanish
   would read faster than 20 characters a second, the agent shortened it ("No tendremos mucho
   tiempo,").
4. `styles.py --at 9.9`: all 8 styles on one frame ([`styles-speed.jpg`](captioned/styles-speed.jpg)).
5. `render.py --preview`: the review sheets with TikTok's, Reels' and Shorts' buttons drawn on
   ([`review-speed.jpg`](captioned/speed/review-speed.jpg)), then `render.py`: eight videos.
   Half-size copies are in [`previews/`](previews/).
6. `post_plan.py post.json`: [`plan.md`](plan.md) and one WoopSocial request per post in
   [`requests/captions/`](requests/captions/). The accounts are placeholders, so the plan lists them as not connected.

Run it yourself from this folder (the clips here are small copies, so the crops look softer):

```
python3 ../../scripts/transcribe.py captions.json --force
python3 ../../scripts/captions.py captions.json
python3 ../../scripts/render.py captions.json --preview
```
