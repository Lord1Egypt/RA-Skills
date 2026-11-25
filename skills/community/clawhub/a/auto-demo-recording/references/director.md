# Writing a story

A story is a Python file. `demo_record.py` imports it, starts the app, and calls `story(d)`. The `d` object
(the director) both drives the page and writes the timeline that `demo_render.py` draws later. This document
is the complete API and the rules behind it.

Start from `story_template.py` and `examples/selftest/story.py`.

## The file contract

```python
TITLE = 'My App'                       # upper-left of the top band
SUBTITLE = 'Feature tour'              # grey text next to it (optional)
CHAPTERS = ['Overview', 'Task', 'Done']  # 2–5 short names; needed if you call d.chapter()
VIEW = (1280, 620)                     # page size in CSS px; width/height must be 64:31
DENSITY = 2.5                          # device scale; VIEW width × DENSITY < 4096
PORT = 8791                            # throwaway instance's port
LANGUAGE = 'en'                        # the captions' language, and so the narration's: zh en ja ko de fr es it pt ru
LOCALE = 'zh-CN'                       # the page's locale (default 'zh-CN')
LOOK = {'accent': '#2f6fed', 'note': '#ee5c18', 'fast': '快进'}   # `fast` in the band's language
VOICE = {...}                          # narration: engine, speaker, ...; see narration.md and engines.md
READING = 5.5                          # units a second a caption is given; default: the language's own (5.5 字/s zh, 3.8 /s en)

def launch(work, port): ...            # or set URL = 'http://...'
def guard(d): ...                      # optional, before recording starts
async def story(d): ...                # required
```

`VIEW` shapes: 1280×620, 1536×744, 1600×775, 1920×930. Other shapes are rejected with the ratio error.
`DENSITY` above about 3 makes each recorded frame larger without adding visible detail; 2–2.5 is normal.

`LANGUAGE` decides how a caption's reading time is computed and how `demo_voice.py` reads it; it also goes into
`timeline.json`, so the narration is in the same language as the captions without being told again. If it is left
out, it is taken from `LOCALE`, else guessed from the title and chapter names. The captions themselves must be
written in that language.

If both `URL` and `launch` exist, `launch` wins. If neither exists, recording stops.

## `launch(work, port)`

Return a dict:

| Key | Meaning |
| --- | --- |
| `command` | argv list to start a **separate** instance; optional for an already-static page |
| `cwd` | working directory of that command |
| `env` | extra environment variables, merged over the current environment |
| `url` | page to open (required) |
| `ready` | URL polled until it answers; default `url` |
| `timeout` | seconds to wait for `ready`; default 60 |
| `wipe` | paths under `work` removed before recording, e.g. `['data']` |

The recorder refuses to start if `PORT` is already listening. It writes the command's output to
`work/server.log`, starts it in its own process group, and stops the whole group afterwards.

**Isolation is the point.** Give the instance its own database/uploads/cache under `work`, and list them in
`wipe` so every take starts from the same state. Do not use the user's live service, real customer data or a
production API. If the app cannot run separately, stop and ask.

`work` is created before launch. Paths in `wipe` must resolve inside `work`; anything else is refused.

## `guard(d)`

Runs after the page loads and before the screencast starts. Use it to fail fast when the app is not in the
state the story expects:

```python
async def guard(d):
    if await d.page.locator('#items li').count() != 12:
        raise SystemExit('page is not in its initial state')
```

## Time

Every frame and timeline event carries its time in the **finished video**, which is not wall time:

| Call | Meaning |
| --- | --- |
| `await d.wait(seconds)` | real time the app needs; always actually waits |
| `await d.pause(seconds)` | time the viewer needs; in `--quick` it only moves the video clock |
| `await d.read()` | keep the current caption until it has been readable long enough |
| `await d.say(text)` | wait for the previous caption, then show and narrate `text` |
| `await d.hush()` | end the current caption (no text) |
| `d.chapter(index)` | start chapter `index` (0-based) in the top band and on the page |
| `await d.card(lines, seconds)` | full-frame card; the video stands still under it for `seconds` |
| `async with d.fast(speed):` | what happens inside is played `speed` × faster in the video |
| `await d.until(done, speed=4, limit=60, every=0.3, settle=0.4, what='…')` | poll an async predicate; the wait is played fast; raises after `limit` seconds |

`d.say` computes the caption's reading time from its length in the story's language (Mandarin by characters and
spoken syllables, English and the other spaced languages by syllables and words via `demo_text.reading_time`). If the next action comes before that time, the caption is simply
replaced early; call `await d.read()` before moving on when the viewer needs the full time.

`d.until` calls `done()` every `every` seconds. `done` is an async function:
`await d.until(result.is_visible, speed=4, what='result')`. `settle` is extra time after the condition is
true, and a snapshot is taken so the final state is recorded.

## Page and elements

`d.page` is the Playwright `Page`; use it for anything the director does not cover (`locator`, `evaluate`,
`expect_download`, …).

| Call | Meaning |
| --- | --- |
| `await d.box(target)` | `[x, y, width, height]` of a locator (or return a rect passed in) |
| `await d.lines(locator)` | line boxes of every match inside the visible page |
| `await d.words(locator, 'some words')` | boxes of that text inside an element (scrolls an inner scroller if needed) |

## Camera

Coordinates are CSS pixels of the page, not of the 1920×1080 frame.

```python
await d.zoom(form, most=1.6, pad=40)     # move in on one or more targets
await d.zoom()                            # back to the whole page
```

- `most` is the maximum magnification (the camera never gets closer than `1 / most` of the page width).
- `pad` is extra page pixels around the target.
- `d` in `zoom(..., d=0.7)` is the move duration in video seconds.
- Several targets: `await d.zoom(a, b, c)` frames their union.
- The camera keeps the page's 64:31 shape, so a very tall target still shows its surroundings.
- If a target is wider/taller than the page, the check reports that part of it is outside the camera.

## Marks, notes and chips

```python
mark = d.mark([await d.box(result)], 'The result', place='right', expect='#ffffff')
await d.read()
d.clear(mark)                              # marks stay until cleared or the video ends
```

`d.mark(rects, label=None, kind='outline', place='above', pin=False, expect=None)`

| Argument | Meaning |
| --- | --- |
| `rects` | list of `[x, y, w, h]`; usually `[await d.box(locator)]` or `await d.words(...)` |
| `label` | short text on a chip next to the mark |
| `kind` | `outline` (default), `mark` (thin line, for words), `spot` (dim everything else) |
| `place` | `above`, `above-center`, `above-right`, `below`, `below-center`, `below-right`, `right`, `left`, `in-top-right`, `in-right`, `in-bottom-right` |
| `pin` | keep the requested place instead of moving to an emptier one |
| `expect` | `#rrggbb` the region should contain; the check fails if less than 30 % matches |

Labels are placed where the page is empty; `place` is a preference, not a guarantee. `left`/`right` labels may
be nudged further out. Labels and boxes fade in/out over 0.18 s. A mark shorter than 0.8 s is flagged by the check.

`spot` dims the rest of the page, so use it for a single important passage, not several at once.

```python
d.note('Elsewhere: the browser download folder', ['The exported file is saved here'])
d.chip('Downloaded: report.txt')           # lower-right, 3 s by default
```

`note` is for effects that happen outside the page (downloads, OS dialogs, files on disk); it stays until
cleared. `chip` is a short lower-right sign that disappears by itself.

`await d.flash(locator, seconds=2.2, most=1.7, pad=60, expect='#1d2230')` stands still on something that
appears only briefly (a toast), zooms in, outlines it, and returns. Use `expect` to prove the right thing was
caught.

## Hands

| Call | Meaning |
| --- | --- |
| `d.cursor()` | make the cursor appear at its current position |
| `await d.point(target)` | move the cursor to a locator |
| `await d.click(target, 'Step text', after=0.4)` | move, click, show a numbered step above/below the target; `press=False` clicks nothing |
| `await d.choose(select_locator, 'Label', 'Step text')` | click a native `<select>` and choose an option |
| `await d.type(locator, 'text', delay=90)` | type like a person (per-character delay) |
| `await d.scroll(top, ms=700)` | scroll the page to a y offset |
| `await d.bring(locator, top=150, ms=700)` | scroll until the element is `top` px below the top edge |
| `await d.slide(locator, top, ms=600)` | scroll inside an element; a negative `top` means its end |
| `await d.reveal(locator, ms=350)` | bring a row of a self-scrolling list into view |

Clicks are rejected if `elementFromPoint` at the target's centre is not the element or its descendant/ancestor
(the element is covered or off-screen). Scroll or zoom first. Numbered steps are counted per chapter, so
starting a new chapter restarts at 1.

## Facts

`d.facts` is a dict of values read from the page during recording. It is written to `timeline.json` and printed
at the end. Use it to build captions that state real results instead of guessing:

```python
d.facts['counts'] = await page.locator('#counts').inner_text()
await d.say(f'After adding it, the page shows: {d.facts["counts"]}')
```

## Optional controls

| Attribute | Meaning |
| --- | --- |
| `d.lowest` | async function returning the lowest page scroll allowed; `scroll`/`bring` clamp to it |
| `d.reading` | reading speed (set from `READING`) |
| `d.say_as` | pronunciation overrides (set from `VOICE['say']`) |
| `d.quick` | true during `--quick` |

## Writing good captions

- One idea per caption, 10–35 Chinese characters or 6–18 English words.
- Say what the viewer should see, not what the click is mechanically doing.
- When a caption reports a result, read it from the page (`d.facts`) or write it after seeing the real result.
- Captions are the narration script. Avoid parentheses, symbols, URLs and code; if a number or acronym is
  read wrongly, add a `say` override in `VOICE` (see `narration.md`).
- The renderer wraps a caption into at most two lines at 33–27 px and stops with an error if it cannot fit.
- End the video with `await d.hush()` and a closing `card`; anything still marked fades out at the end.

## Patterns

**A transient message**

```python
await d.click(page.locator('#save'), 'Save')
await d.flash(page.locator('.toast').last, 2.0, expect='#1d2230')
```

**A slow job**

```python
await d.click(page.locator('#run'), 'Run')
await d.until(page.locator('#done').is_visible, speed=6, limit=120, what='job to finish')
await d.say('When it finishes, the page summarises the outcome.')
```

**A download happens outside the page**

```python
async with page.expect_download() as download:
    await d.click(page.locator('#export'), 'Export')
d.chip('Downloaded: ' + (await download.value).suggested_filename)
saved = d.note('Elsewhere: the browser download folder', ['The exported file is saved here'])
await d.read()
d.clear(saved)
```

**A self-scrolling list**

```python
await d.reveal(page.locator('#items li').last)
last = d.mark([await d.box(page.locator('#items li').last)], 'The last row', place='right')
await d.read()
d.clear(last)
```

**A modal or drop-down**

```python
await d.click(page.locator('#open-dialog'), 'Open')
await d.until(page.locator('.dialog').is_visible, speed=2, what='dialog')
await d.choose(page.locator('.dialog select'), 'All')
```

**A chapter change**

```python
d.chapter(1)
await d.say('The second page shows the results.')
```

## Rules and pitfalls

- **64:31 only.** `demo_record.py` stops if `VIEW` is off by more than 0.004.
- **Page width must match `VIEW`.** The recorder makes the window slightly wider for a scrollbar, but if the
  page's own width differs, recording stops; make the page responsive or change `VIEW`.
- **Wait for animations.** A screenshot taken mid-transition makes labels and camera positions drift.
- **Element visibility before `box`.** `bounding_box()` returns `None` for hidden elements; wait first.
- **No secrets on screen.** The frames are real screenshots; use demo accounts and sample data.
- **The timeline is editable.** Captions, marks and times live in `work/timeline.json`; you can adjust them and
  render again without re-recording, but the next recording overwrites the file. Prefer fixing the story.
- **`--quick` is not a finished video.** It skips viewer pauses; use it only to debug selectors and state.
