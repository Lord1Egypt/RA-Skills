"""A starting point for a demo story. Copy this file next to your app and change everything marked TODO.

Run it with:

    PY=~/.cache/auto-demo-recording/venv/bin/python
    $PY scripts/demo_record.py --story story.py --work /tmp/demo-work --quick   # trial
    $PY scripts/demo_record.py --story story.py --work /tmp/demo-work           # real recording

The full director API is in references/director.md. Keep captions short: they are read aloud by
demo_voice.py, and each one gets only until the next caption to be said.

Before writing this file, ask the user: whether the video should have a narration at all, in which
language, and by which engine (see SKILL.md, step 0). The answers go into LANGUAGE and VOICE below,
so the video can be made again exactly as it was.
"""
from __future__ import annotations

import sys

# ---- the top band and the chapters ------------------------------------------------------------
TITLE = 'My App'                     # TODO: shown at the upper left of every frame
SUBTITLE = 'Feature tour'            # TODO: smaller grey text next to it
CHAPTERS = ['Overview', 'Main task', 'Results']   # TODO: 2–5 short names

# ---- the page ----------------------------------------------------------------------------------
VIEW = (1280, 620)                   # CSS px; width / height must be 64:31
DENSITY = 2.5                        # device scale; VIEW width × DENSITY must stay below 4096
PORT = 8791                          # the throwaway instance's port; must be free
LANGUAGE = 'en'                      # TODO: the language of the captions, which is also the language of the narration:
                                     # zh 普通话, en English, ja, ko, de, fr, es, it, pt, ru (demo_text.LANGUAGES)
LOCALE = 'en-US'                     # the page's locale; 'zh-CN' for a Chinese app

# Drawn by demo_render.py. `note` must be a colour the app itself does not use.
LOOK = {'accent': '#2f6fed', 'note': '#ee5c18', 'fast': 'Fast forward'}

# Narration; see references/narration.md and references/engines.md. Remove what you do not need.
VOICE = {
    # 'engine': 'kokoro',            # qwen (local GPU) | kokoro (local CPU) | openai | compatible | elevenlabs | dashscope
    # 'speaker': 'af_maple',         # the voice: a Qwen speaker, a Kokoro voice, or a remote voice id
    # 'model': 'gpt-4o-mini-tts',    # remote: the model id
    # 'pace': 4.0,                   # units a second (syllables for English, 字 for Mandarin)
    # 'say': {'WPS 365': 'W P S three sixty five'},   # fix how the narration reads a caption
}


# ---- how the throwaway instance starts ---------------------------------------------------------
def launch(work, port):
    """Start a separate instance with its own data, and return how to reach it.

    `work` is this recording's working folder. Put the instance's database, uploads and cache under it,
    and list what must be removed before each recording in `wipe`. Never point this at the user's live
    service or real data.

    Examples:

        # A Python web app
        return {
            'command': [sys.executable, '-m', 'myapp', '--port', str(port)],
            'url': f'http://127.0.0.1:{port}/',
            'cwd': '/path/to/app',
            'env': {'DATA_DIR': str(work / 'data'), 'DEBUG': '0'},
            'wipe': ['data'],
            'ready': f'http://127.0.0.1:{port}/health',
            'timeout': 90,
        }

        # A static page: no command needed
        return {'url': f'http://127.0.0.1:{port}/index.html'}
    """
    return {
        'command': [sys.executable, '-m', 'http.server', str(port), '--bind', '127.0.0.1',
                    '--directory', '/path/to/page'],                     # TODO
        'url': f'http://127.0.0.1:{port}/index.html',
    }


def guard(d):
    """Optional. Before anything is recorded, check this is the intended page and starting state."""
    # if await d.page.locator('.item').count() != 12:
    #     raise SystemExit('page is not in its initial state')
    pass


async def story(d):
    page = d.page

    # Opening card, then the page as a whole.
    await d.card([TITLE, SUBTITLE, 'A short line about what this shows'], 2.6)
    d.cursor()
    await d.say('This short demo shows how to …')
    overview = d.mark([await d.box(page.locator('header'))], 'Main navigation', place='below')
    await d.read()
    d.clear(overview)

    # Chapter 1: one task, with numbered steps and a zoomed-in camera.
    d.chapter(0)
    await d.say('First, open the form and enter a value.')
    await d.zoom(page.locator('form'), most=1.6, pad=40)
    await d.click(page.locator('input[name="q"]'), 'Enter a value')
    await d.type(page.locator('input[name="q"]'), 'example', 110)
    await d.click(page.locator('button[type="submit"]'), 'Search')
    await d.zoom()

    # A result that the page really shows. Captions that state results can also be built from d.facts.
    await d.say('The result appears below the form.')
    result = page.locator('.result')
    await d.until(result.is_visible, speed=4, limit=60, what='result')
    d.facts['result'] = await result.inner_text()
    box = d.mark([await d.box(result)], 'The result', place='right', expect='#ffffff')
    await d.read()
    d.clear(box)

    # Chapter 2: a longer wait, played fast, then the end.
    d.chapter(1)
    await d.say('A longer job reports its progress and finishes on its own.')
    await d.click(page.locator('#start'), 'Start the job')
    await d.until(page.locator('#done').is_visible, speed=6, limit=120, what='job to finish')
    await d.say('When it finishes, the page summarises the outcome.')
    await d.read()

    # Everything that is not cleared fades out when the video ends; the closing card stays.
    await d.hush()
    await d.card(['Thanks for watching', 'Back to the app whenever you like'], 3.0)
