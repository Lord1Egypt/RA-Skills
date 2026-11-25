"""The skill's own test, in English: the same small page (its own text is Chinese; the captions are what is spoken), a
story that uses every kind of thing the director can do, and the English narration path of demo_voice.py.

Run it to see that recording, drawing and narrating work in English on this machine:

    PY=~/.cache/auto-demo-recording/venv/bin/python; S=~/.claude/skills/autoDemoRecordingSkill
    $PY $S/scripts/demo_record.py --story $S/examples/selftest/story-en.py --work /tmp/demo-selftest-en
    $PY $S/scripts/demo_render.py --work /tmp/demo-selftest-en --check
    $PY $S/scripts/demo_render.py --work /tmp/demo-selftest-en --out /tmp/demo-selftest-en/selftest-en.mp4
    $PY $S/scripts/demo_voice.py  --work /tmp/demo-selftest-en
"""
from __future__ import annotations

import sys
from pathlib import Path

TITLE = 'To-Do List'                  # the name in the band above the page
SUBTITLE = 'Skill self-test'          # in grey next to it
CHAPTERS = ['Add and tick off', 'Filter and find', 'Summary and export']
LANGUAGE = 'en'                       # the captions, and with them the narration: English. story.py is the Mandarin one.
PORT = 8794
PAGE = Path(__file__).resolve().parent / 'page'

# Narration: left empty, the first engine that can speak here is taken. Kokoro (CPU) speaks English with af_maple,
# af_sol, bf_vale; Qwen with its own speakers; a remote service with a voice id.
VOICE = {}


def launch(work, port):
    """How the throwaway instance is started. A real app also gets its own data here: env={...: work / 'data'} and wipe=['data']."""
    return {'command': [sys.executable, '-m', 'http.server', str(port), '--bind', '127.0.0.1', '--directory', PAGE],
            'url': f'http://127.0.0.1:{port}/index.html'}


async def guard(d):
    """Before anything is recorded: is this the instance that was meant, and in the state the story starts from?"""
    if await d.page.locator('#items li').count() != 12:
        raise SystemExit('the page is not in its initial state: the list should have exactly 12 items')


async def story(d):
    page = d.page
    items, choice, summary = page.locator('#items li'), page.locator('#filter'), page.locator('#summary')

    # ---- opening: a card, then the page as a whole
    await d.card(['To-Do List', 'Add · tick off · filter · summary', 'The sample page of the skill self-test'], 2.6)
    d.cursor()
    await d.say('This is a small to-do page, used to check recording, rendering and narration.')
    pages = d.mark([await d.box(page.locator('.tabs'))], 'Two pages', place='below')
    await d.read()
    d.clear(pages)

    # ---- 1: typing, a numbered step for each click, a message that is there for a moment only
    d.chapter(0)
    await d.say('First, add an item: type what needs doing into the box.')
    await d.zoom(page.locator('#add-form'), most=1.6, pad=40)
    await d.click(page.locator('#new-text'), 'Type what to do')
    await d.type(page.locator('#new-text'), 'Polish the demo captions', 90)
    await d.click(page.locator('#add'), 'Add it')
    await d.zoom()
    await d.flash(page.locator('.toast').last, 2.0, expect='#1d2230')
    await d.say('The new item is first in the list, and can be ticked off any time.')
    await d.zoom(items.first, most=1.7, pad=70)
    added = d.mark([await d.box(items.first)], 'The item just added', place='right')
    await d.read()
    d.clear(added)
    await d.click(items.first.locator('input'), 'Tick it off')
    d.facts['counts'] = await page.locator('#counts').inner_text()   # what the page really showed: captions that state results are written from this
    await d.zoom()

    # ---- 2: a drop-down list, a list that scrolls by itself, words in a text
    d.chapter(1)
    await d.say('The list can be filtered by whether an item is done.')
    await d.choose(choice, '未完成', 'Only the open ones')
    await d.wait(1.4)
    await d.choose(choice, '全部')
    await d.say('A long list scrolls inside its own box, and the last item can be reached directly.')
    await d.reveal(items.last)
    last = d.mark([await d.box(items.last)], 'The last item of the list', place='right')
    await d.read()
    d.clear(last)
    guide = page.locator('#guide')
    await d.say('Below the page is a guide, which says the data stays in this browser.')
    await d.bring(guide, 120)
    await d.zoom(guide, most=1.5, pad=30)
    quoted = d.mark(await d.words(guide, '只保存在本机浏览器里'), 'The words of the guide', kind='mark')
    await d.read()
    d.clear(quoted)
    await d.zoom()

    # ---- 3: a wait that is played fast, the passage lit up, a download, something that happens off the page
    d.chapter(2)
    await d.scroll(0, 500)
    await d.say('The second page writes a summary; it takes a few seconds, played fast.')
    await d.click(page.locator('.tab[data-view="summary"]'), 'Summary')
    await d.click(page.locator('#summarize'), 'Write it')
    await d.until(summary.is_visible, speed=4, limit=60, what='the summary')
    d.facts['summary'] = await summary.inner_text()
    await d.zoom(summary, most=1.6, pad=60)
    point = d.mark([await d.box(summary.locator('mark'))], 'What to do next', kind='spot', expect='#fff3c4')
    await d.say('The summary gives the total and the number done, and the next thing to do is marked.')
    await d.read()
    d.clear(point)
    await d.zoom()
    async with page.expect_download() as download:
        await d.click(page.locator('#export'), 'Export')
    d.chip('Downloaded: ' + (await download.value).suggested_filename)
    saved = d.note('Off the page: the browser download folder', ['The exported text file is saved here'])
    await d.say('The summary can be exported as a text file.')
    await d.read()
    d.clear(saved)
    await d.hush()
    await d.card(['Add · tick off · filter · summary', 'The self-test ends here'], 3.0)
