"""The skill's own test: a small page that needs nothing, and a story that uses every kind of thing the director can do.

Run it to see that recording, drawing and narrating work on this machine before writing a story for
a real app, and read it as the shortest example of a story file:

    PY=~/.cache/auto-demo-recording/venv/bin/python; S=~/.claude/skills/autoDemoRecordingSkill
    $PY $S/scripts/demo_record.py --story $S/examples/selftest/story.py --work /tmp/demo-selftest
    $PY $S/scripts/demo_render.py --work /tmp/demo-selftest --check
    $PY $S/scripts/demo_render.py --work /tmp/demo-selftest --out /tmp/demo-selftest/selftest.mp4
    $PY $S/scripts/demo_voice.py  --work /tmp/demo-selftest
"""
from __future__ import annotations

import sys
from pathlib import Path

TITLE = '待办清单'                     # the name in the band above the page
SUBTITLE = '技能自检'                  # in grey next to it
CHAPTERS = ['添加与勾选', '筛选与查找', '小结与导出']
LANGUAGE = 'zh'                        # the captions, and with them the narration: 普通话. story-en.py is the English one.
PORT = 8793
PAGE = Path(__file__).resolve().parent / 'page'

# Narration: left empty, the first engine that can speak here is taken (Qwen on the GPU, then Kokoro on the CPU,
# then a remote service with a key). Write it down to keep the video reproducible, e.g.
# VOICE = {'engine': 'kokoro', 'speaker': 'zf_062'} or {'engine': 'openai', 'speaker': 'marin'}
VOICE = {}


def launch(work, port):
    """How the throwaway instance is started. A real app also gets its own data here: env={...: work / 'data'} and wipe=['data']."""
    return {'command': [sys.executable, '-m', 'http.server', str(port), '--bind', '127.0.0.1', '--directory', PAGE],
            'url': f'http://127.0.0.1:{port}/index.html'}


async def guard(d):
    """Before anything is recorded: is this the instance that was meant, and in the state the story starts from?"""
    if await d.page.locator('#items li').count() != 12:
        raise SystemExit('页面不是初始状态：清单应当正好有 12 项')


async def story(d):
    page = d.page
    items, choice, summary = page.locator('#items li'), page.locator('#filter'), page.locator('#summary')

    # ---- opening: a card, then the page as a whole
    await d.card(['待办清单', '添加 · 勾选 · 筛选 · 小结', '技能自检用的示例页面'], 2.6)
    d.cursor()
    await d.say('这是一个很小的待办清单页面，用来检查录制、渲染和配音整条流程。')
    pages = d.mark([await d.box(page.locator('.tabs'))], '两个页面', place='below')
    await d.read()
    d.clear(pages)

    # ---- 1: typing, a numbered step for each click, a message that is there for a moment only
    d.chapter(0)
    await d.say('先添加一项：在输入框里写上要做的事。')
    await d.zoom(page.locator('#add-form'), most=1.6, pad=40)
    await d.click(page.locator('#new-text'), '写下要做的事')
    await d.type(page.locator('#new-text'), '整理演示视频的字幕', 110)
    await d.click(page.locator('#add'), '添加')
    await d.zoom()
    await d.flash(page.locator('.toast').last, 2.0, expect='#1d2230')
    await d.say('新加的一项排在清单最前面，可以随时勾选完成。')
    await d.zoom(items.first, most=1.7, pad=70)
    added = d.mark([await d.box(items.first)], '刚添加的一项', place='right')
    await d.read()
    d.clear(added)
    await d.click(items.first.locator('input'), '勾选完成')
    d.facts['添加后'] = await page.locator('#counts').inner_text()   # what the page really showed: captions that state results are written from this
    await d.zoom()

    # ---- 2: a drop-down list, a list that scrolls by itself, words in a text
    d.chapter(1)
    await d.say('清单可以按完成情况筛选。')
    await d.choose(choice, '未完成', '只看未完成')
    await d.wait(1.4)
    await d.choose(choice, '全部')
    await d.say('清单很长时，它在自己的框里滚动；最后一项也能直接找到。')
    await d.reveal(items.last)
    last = d.mark([await d.box(items.last)], '清单的最后一项', place='right')
    await d.read()
    d.clear(last)
    guide = page.locator('#guide')
    await d.say('页面下方是使用说明，写明数据只保存在本机浏览器里。')
    await d.bring(guide, 120)
    await d.zoom(guide, most=1.5, pad=30)
    quoted = d.mark(await d.words(guide, '只保存在本机浏览器里'), '说明里的原话', kind='mark')
    await d.read()
    d.clear(quoted)
    await d.zoom()

    # ---- 3: a wait that is played fast, the passage lit up, a download, something that happens off the page
    d.chapter(2)
    await d.scroll(0, 500)
    await d.say('第二个页面生成小结；这一步要等几秒，画面已快进。')
    await d.click(page.locator('.tab[data-view="summary"]'), '小结')
    await d.click(page.locator('#summarize'), '生成小结')
    await d.until(summary.is_visible, speed=4, limit=60, what='小结出来')
    d.facts['小结'] = await summary.inner_text()
    await d.zoom(summary, most=1.6, pad=60)
    point = d.mark([await d.box(summary.locator('mark'))], '接下来该做的事', kind='spot', expect='#fff3c4')
    await d.say('小结给出总数和完成数，接下来该做的一项已经标出。')
    await d.read()
    d.clear(point)
    await d.zoom()
    async with page.expect_download() as download:
        await d.click(page.locator('#export'), '导出')
    d.chip('已下载：' + (await download.value).suggested_filename)
    saved = d.note('画面外：浏览器的下载目录', ['导出的文本文件保存在这里'])
    await d.say('小结可以导出成文本文件。')
    await d.read()
    d.clear(saved)
    await d.hush()
    await d.card(['添加 · 勾选 · 筛选 · 小结', '自检演示到此结束'], 3.0)
