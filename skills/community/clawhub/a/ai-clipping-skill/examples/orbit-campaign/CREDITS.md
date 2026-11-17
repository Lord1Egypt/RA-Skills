# Credits

Footage courtesy of NASA. This project is not endorsed by NASA, and neither NASA nor astronaut Bob
Behnken endorses, sponsors or appears in an ad for anything shown here.

The three clips in `clips/` are cut from "Bob Behnken discusses training and development in SpaceX
Crew Dragon" (NASA, Johnson Space Center, jsc2020m000132, 9:02):
https://images.nasa.gov/details/jsc2020m000132_Bob_Behnken_discusses_training_and_development_in_SpaceX_Crew_Dragon

| Clip | Source time |
|---|---|
| `clips/clip-01.mp4` | 8:08.6 to 8:39.7 |
| `clips/clip-02.mp4` | 3:33.0 to 3:54.4 |
| `clips/clip-03.mp4` | 1:10.9 to 1:40.0 |

They were made by `make_clips.py` from NASA's medium-size download, transcribed on a laptop with
faster-whisper (`transcribe.py --engine local`), cropped to 9:16 and scaled to 540x960 to keep this
repo small. The JPEG images in `clips/` (`clips/*-cover.jpg`, the first frame of each clip, and
`clips/contact-sheet.jpg`) and `long-to-clips.jpg` (one frame of the interview at 5:00 plus a frame
of each clip) are frames of that footage, and `../showcase.png` is a screenshot of `plan.html`. The
source video itself is not in this repo; download it from the link above to run the example.

NASA material is generally not subject to copyright in the United States (NASA media usage
guidelines: https://www.nasa.gov/nasa-brand-center/images-and-media/).

"Example Orbit", its campaign, the brief, the accounts (`@example.clipper`, `@example.orbit` and
the others), every id, link and number in this folder are made up for the example. No real
campaign, brand, marketplace listing or post is shown. The clips are not ads: the line at the top
of each one reads "EXAMPLE ONLY: not a real ad" and the watermark reads "EXAMPLE ONLY". Everything
else here was made by this skill's scripts and the agent running it.
