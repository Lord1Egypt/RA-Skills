"""Record a demo of a web app: drive it in a headless browser and keep what the screen showed.

What is shown, in which order and with which captions, is a story file written for the app (see
story_template.py and references/director.md). A throwaway instance of the app is started for the
recording, on its own data and its own port, so nothing of a running service is touched. The page is
recorded as it is; what the video adds to it (where the camera looks, what is marked, captions, the
cursor, the chapters) is written to a timeline, and demo_render.py draws it. Every frame and every
entry of the timeline carries its time in the finished video: waiting can be played fast there, and
a moment can be stood still on.

    PY=~/.cache/auto-demo-recording/venv/bin/python
    $PY demo_record.py --story path/to/story.py --work path/to/work --quick   # a trial: only the app itself is waited for
    $PY demo_record.py --story path/to/story.py --work path/to/work           # the recording
"""
from __future__ import annotations

import argparse
import asyncio
import base64
import contextlib
import importlib.util
import json
import math
import os
import shutil
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import urlsplit

import httpx
from playwright.async_api import async_playwright

import demo_text
from demo_common import WINDOWS, browsers, where

SHAPE = 1920 / 930   # the page's shape, width to height: what the picture has between its two bands (demo_render.py)

SCROLL_PAGE = """([top, ms]) => new Promise(done => {
  const from = scrollY, t0 = performance.now();
  const tick = now => { const p = Math.min(1, (now - t0) / ms); scrollTo(0, from + (top - from) * (p * p * (3 - 2 * p))); p < 1 ? requestAnimationFrame(tick) : done(); };
  requestAnimationFrame(tick); })"""
SCROLL_ELEMENT = """(el, [top, ms]) => new Promise(done => {
  const from = el.scrollTop, to = top < 0 ? el.scrollHeight - el.clientHeight : top, t0 = performance.now();
  const tick = now => { const p = Math.min(1, (now - t0) / ms); el.scrollTop = from + (to - from) * (p * p * (3 - 2 * p)); p < 1 ? requestAnimationFrame(tick) : done(); };
  requestAnimationFrame(tick); })"""
REVEAL = """(el, [bottom, ms]) => new Promise(done => {
  let box = el.parentElement;
  for (; box && box !== document.body && box !== document.documentElement; box = box.parentElement) {
    const flow = getComputedStyle(box).overflowY;
    if ((flow === 'auto' || flow === 'scroll') && box.scrollHeight > box.clientHeight + 1) break; }
  if (!box || box === document.body || box === document.documentElement) return done(false);
  const frame = box.getBoundingClientRect(), r = el.getBoundingClientRect(), low = Math.min(frame.bottom, bottom) - 6, from = box.scrollTop;
  const to = Math.max(0, r.top < frame.top ? from - (frame.top - r.top) : r.bottom > low ? from + (r.bottom - low) : from), t0 = performance.now();
  if (Math.abs(to - from) <= 1) return done(false);
  const tick = now => { const p = Math.min(1, (now - t0) / ms); box.scrollTop = from + (to - from) * (p * p * (3 - 2 * p)); p < 1 ? requestAnimationFrame(tick) : done(true); };
  requestAnimationFrame(tick); })"""
LINE_BOXES = "els => els.flatMap(el => [...el.getClientRects()].map(r => [r.x, r.y, r.width, r.height]))"
WORD_BOXES = """(el, words) => { const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT); let node;
  while ((node = walker.nextNode())) { const at = node.data.indexOf(words); if (at < 0) continue;
    const range = document.createRange(); range.setStart(node, at); range.setEnd(node, at + words.length);
    const box = el.getBoundingClientRect(), found = range.getBoundingClientRect();
    if (found.top < box.top || found.bottom > box.bottom) el.scrollTop += found.top - box.top - (box.height - found.height) / 2;
    return [...range.getClientRects()].map(r => [r.x, r.y, r.width, r.height]); }
  return []; }"""
REACHABLE = """el => { const r = el.getBoundingClientRect(), hit = document.elementFromPoint(r.x + r.width / 2, r.y + r.height / 2);
  return Boolean(hit) && (hit === el || el.contains(hit) || hit.contains(el)); }"""


class Clock:
    """Time in the finished video against time on the wall.

    Waiting can be played fast (a rate below one) or left out (rate zero), and the video can stand
    still on a moment while the clock on the wall does not move at all.
    """

    def __init__(self):
        self.points = [[time.time(), 0.0, 1.0]]  # from this wall time on, video time runs on from this value at this rate

    def _point(self, wall):
        return next((point for point in reversed(self.points) if wall >= point[0]), self.points[0])

    def at(self, wall):
        start, video, rate = self._point(wall)
        return video + max(0.0, wall - start) * rate

    def rate_at(self, wall):
        return self._point(wall)[2]

    def now(self):
        return self.at(time.time())

    def rate(self, rate):
        wall = time.time()
        self.points.append([wall, self.at(wall), rate])

    def hold(self, seconds):
        wall = time.time()
        self.points.append([wall, self.at(wall) + seconds, self.points[-1][2]])


class Recorder:
    """Keeps the frames the browser shows and the timeline of what the video adds to them."""

    def __init__(self, cdp, folder, about):
        self.cdp, self.folder, self.about, self.clock = cdp, folder, about, Clock()
        self.frames, self.events, self.last_kept, self.lags, self.count = [], [], -1.0, [], 0
        folder.mkdir(parents=True)

    async def start(self):
        self.clock = Clock()  # the video begins now
        self.cdp.on('Page.screencastFrame', self._frame)
        await self.cdp.send('Page.startScreencast', {'format': 'jpeg', 'quality': 92, 'everyNthFrame': 1, 'maxWidth': 4096, 'maxHeight': 4096})
        await self.snap()

    async def stop(self):
        await self.snap()
        await self.cdp.send('Page.stopScreencast')

    def _frame(self, params):
        asyncio.ensure_future(self.cdp.send('Page.screencastFrameAck', {'sessionId': params['sessionId']}))
        now, shown = time.time(), params['metadata'].get('timestamp') or 0
        self.lags.append(now - shown)
        self._keep(shown if abs(now - shown) < 2 else now, params['data'])

    def _keep(self, wall, data, always=False):
        rate, video = self.clock.rate_at(wall), self.clock.at(wall)
        if not always and (rate == 0 or video - self.last_kept < (0.016 if rate >= 1 else 0.033)):
            return  # cut out, or more often than the video can show
        self.last_kept = max(self.last_kept, video)
        self.count += 1
        name = f'{self.count:06d}.jpg'
        (self.folder / name).write_bytes(base64.b64decode(data))
        self.frames.append([round(video, 4), name, wall])

    def leave_out(self, start, end):
        """Take the pictures shown between these two moments (time on the wall) out of the video. Returns how many."""
        before = len(self.frames)
        self.frames = [frame for frame in self.frames if not start <= frame[2] <= end]
        return before - len(self.frames)

    async def snap(self):
        """The page as it is right now. The browser sends frames only when something changes."""
        shot = await self.cdp.send('Page.captureScreenshot', {'format': 'jpeg', 'quality': 92})
        self._keep(time.time(), shot['data'], always=True)

    def add(self, what, t=None, **fields):
        event = {'type': what, 't': round(self.clock.now() if t is None else t, 4), **fields}
        self.events.append(event)
        return event

    def timeline(self, facts=None):
        return {**self.about, 'duration': round(self.clock.now(), 3), 'facts': facts or {},
                'clock': [[round(video, 4), rate] for _, video, rate in self.clock.points],
                'frames': sorted([frame[:2] for frame in self.frames], key=lambda frame: frame[0]), 'events': self.events}


def union(rects):
    left, top = min(r[0] for r in rects), min(r[1] for r in rects)
    return [left, top, max(r[0] + r[2] for r in rects) - left, max(r[1] + r[3] for r in rects) - top]


def clip(rect, bounds):
    """The part of `rect` that lies inside `bounds`."""
    left, top = max(rect[0], bounds[0]), max(rect[1], bounds[1])
    return [left, top, min(rect[0] + rect[2], bounds[0] + bounds[2]) - left, min(rect[1] + rect[3], bounds[1] + bounds[3]) - top]


def shot(rect, most, pad, view):
    """The part of the page the camera shows so that `rect` is in it: the page's own shape, never closer than `most` times."""
    x, y, w, h = rect[0] - pad, rect[1] - pad, rect[2] + 2 * pad, rect[3] + 2 * pad
    aspect = view[0] / view[1]
    width = min(view[0], max(w, h * aspect, view[0] / most))
    height = width / aspect
    left = min(max(x + w / 2 - width / 2, 0), view[0] - width)
    top = min(max(y + h / 2 - height / 2, 0), view[1] - height)
    return [round(left, 1), round(top, 1), round(width, 1), round(height, 1)]


def reading_time(text, a_second=None, say=None, tongue=None):
    """How long a caption is given before the next thing happens: long enough to be read, and to be read aloud (demo_text)."""
    return demo_text.reading_time(text, tongue, a_second, say)


class Director:
    """What a person recording the screen does with their hands and voice: point, click, type, scroll, zoom, mark, say."""

    union, clip = staticmethod(union), staticmethod(clip)

    def __init__(self, page, rec, api, work, url, view, quick=False):
        self.page, self.rec, self.api, self.work, self.url, self.view, self.quick = page, rec, api, work, url, tuple(view), quick
        self.pointer, self.camera, self.read_until, self.facts, self.tight = [round(view[0] * 0.727), round(view[1] * 0.532)], [0, 0, *view], 0.0, {}, []
        self.lowest = None  # when set (an async function): gives how far down the page may be scrolled at most
        self.tongue = 'zh'  # the language of the captions (LANGUAGE in the story file): how they are counted, and what says them
        self.reading = 5.5  # syllables a second a caption is given (READING in the story file; 5.5 characters a second for Mandarin)
        self.say_as = {}    # how the narration says what its rules get wrong (VOICE['say'] in the story file): such captions are given the time that takes

    @staticmethod
    def inside(rects, bounds):
        """Those of `rects` that lie inside `bounds`."""
        return [r for r in rects if r[0] >= bounds[0] - 1 and r[1] >= bounds[1] - 1 and r[0] + r[2] <= bounds[0] + bounds[2] + 1 and r[1] + r[3] <= bounds[1] + bounds[3] + 1]

    # ---- time
    async def wait(self, seconds):
        """Time the app needs: always waited for."""
        await self.page.wait_for_timeout(seconds * 1000)

    async def pause(self, seconds):
        """Time the viewer needs. The recording waits; a trial moves the video's clock on instead, so its timeline keeps its proportions."""
        if seconds <= 0:
            return
        if self.quick:
            self.rec.clock.hold(seconds)
        else:
            await self.wait(seconds)

    async def read(self):
        """Leave the caption on the screen long enough to be read."""
        await self.pause(self.read_until - self.rec.clock.now())

    async def say(self, text):
        await self.read()
        self.rec.add('caption', text=text)
        print(f'{self.rec.clock.now():7.1f}  {text}', flush=True)
        self.read_until = self.rec.clock.now() + reading_time(text, self.reading, self.say_as, self.tongue)

    async def hush(self):
        await self.read()
        self.rec.add('caption', text='')

    def chapter(self, index):
        self.rec.add('chapter', index=index)

    async def card(self, lines, seconds):
        """A card over the whole picture; the video stands still under it."""
        await self.rec.snap()
        now = self.rec.clock.now()
        self.rec.add('card', lines=lines, end=round(now + seconds, 4))
        self.rec.clock.hold(seconds)

    @contextlib.asynccontextmanager
    async def fast(self, speed):
        """What happens inside is played `speed` times faster in the video; the video says so while it does."""
        self.rec.clock.rate(1 / speed)
        try:
            yield
        finally:
            self.rec.clock.rate(1)
            await self.rec.snap()

    async def until(self, done, speed=1.0, limit=600, every=0.3, settle=0.4, what='要等的事'):
        """Wait until `done()` (an async function) gives something true, and give that back; the wait is played `speed` times faster."""
        async with self.fast(speed):
            for _ in range(int(limit / every)):
                found = await done()
                if found:
                    break
                await self.wait(every)
            else:
                raise RuntimeError(f'{limit} 秒内没有等到：{what}')
        if settle:
            await self.wait(settle)
            await self.rec.snap()
        return found

    # ---- where things are
    async def box(self, target):
        if isinstance(target, (list, tuple)):
            return list(target)
        found = await target.bounding_box()
        if not found:
            raise RuntimeError(f'看不到要操作的元素：{target}')
        return [found['x'], found['y'], found['width'], found['height']]

    async def lines(self, locator):
        """Every line box of every match that lies inside the page as shown."""
        boxes = await locator.evaluate_all(LINE_BOXES)
        return [b for b in boxes if b[2] > 1 and b[3] > 1 and b[1] >= 0 and b[1] + b[3] <= self.view[1] and b[0] >= 0 and b[0] + b[2] <= self.view[0]]

    async def words(self, locator, words):
        """The boxes of these words inside the element (scrolled into it, if the element scrolls)."""
        return await locator.evaluate(WORD_BOXES, words)

    # ---- the camera and what is marked
    async def zoom(self, *targets, most=1.8, pad=26, d=0.7):
        wanted = union([await self.box(target) for target in targets]) if targets else [0, 0, *self.view]
        self.camera = shot(wanted, most, pad, self.view)
        if clip(wanted, self.camera)[2:] != wanted[2:]:  # what was to be shown is larger than the page as shown, or partly outside it
            self.tight.append(f'{self.rec.clock.now():.1f}s 要看的区域 {[round(v) for v in wanted]} 超出镜头 {[round(v) for v in self.camera]}')
        self.rec.add('camera', rect=self.camera, d=d)
        await self.pause(d)

    def mark(self, rects, label=None, kind='outline', place='above', pin=False, expect=None):
        """Mark parts of the page until clear(). The label goes to `place` if the page is empty there, else where it is emptiest;
        `pin` keeps it at `place`. `expect` is the colour the page has there, which demo_render.py checks against the recorded picture."""
        edge = [9, 9, self.view[0] - 18, self.view[1] - 18]
        rects = [[round(v, 1) for v in clip(rect, edge)] for rect in rects]  # what reaches beyond the page as shown ends at its edge
        rects = [rect for rect in rects if rect[2] > 2 and rect[3] > 2]
        return self.rec.add('box', rects=rects, label=label, kind=kind, place=place, pin=pin, expect=expect, end=None) if rects else None

    def note(self, title, lines):
        """A card in the upper middle of the page, until clear(): for what happens where the page cannot show it."""
        return self.rec.add('note', title=title, lines=list(lines), end=None)

    def chip(self, text, seconds=3.0):
        """A small sign at the lower right, e.g. for a file that was downloaded."""
        return self.rec.add('chip', text=text, end=round(self.rec.clock.now() + seconds, 4))

    def clear(self, *marks):
        for event in marks:
            if event:
                event['end'] = round(self.rec.clock.now(), 4)

    async def flash(self, locator, seconds=2.2, most=1.7, pad=60, expect=None, timeout=20):
        """Stand still on something the page shows for a few seconds only (a toast), and move in on it."""
        await locator.wait_for(state='visible', timeout=timeout * 1000)
        await self.wait(0.35)
        await self.rec.snap()
        rect = await self.box(locator)
        now, back = self.rec.clock.now(), self.camera
        self.rec.add('camera', rect=shot(rect, most, pad, self.view), d=0.45)
        self.rec.add('box', t=round(now + 0.35, 4), rects=[[round(v, 1) for v in rect]], label=None, kind='outline', place='above', pin=False,
                     expect=expect, end=round(now + seconds - 0.45, 4))
        self.rec.add('camera', t=round(now + seconds - 0.45, 4), rect=back, d=0.45)
        self.rec.clock.hold(seconds)

    # ---- the hands
    def cursor(self):
        """Put the cursor into the picture where it stands (it is not drawn before it first appears or moves)."""
        self.rec.add('cursor', to=list(self.pointer), d=0)

    async def point(self, target):
        rect = await self.box(target)
        to = [rect[0] + rect[2] / 2, rect[1] + rect[3] / 2]
        d = min(0.9, max(0.35, math.dist(self.pointer, to) / 900))
        self.rec.add('cursor', to=[round(to[0], 1), round(to[1], 1)], d=d)
        await self.pause(d)
        await self.page.mouse.move(*to)
        self.pointer = to
        return rect

    async def click(self, target, step=None, after=0.4, press=True):
        rect = await self.box(target)
        if not isinstance(target, (list, tuple)) and not await target.evaluate(REACHABLE):
            raise RuntimeError(f'点不到这个元素（被挡住，或不在画面里）：{target}')
        callout = self.rec.add('step', text=step, rect=[round(v, 1) for v in rect], end=None) if step else None
        if callout:
            await self.pause(0.4)  # the step is named before it is done
        await self.point(rect)
        await self.wait(0.2)
        self.rec.add('click', at=[round(v, 1) for v in self.pointer])
        if press:
            await self.page.mouse.click(*self.pointer)
        await self.wait(after)
        if callout:
            callout['end'] = round(self.rec.clock.now() + 0.45, 4)

    async def choose(self, locator, label, step=None):
        """A drop-down list is not part of the page's picture: the cursor goes there, and the value changes."""
        await self.click(locator, step, after=0.15, press=False)
        await locator.select_option(label=label)
        await self.wait(0.5)

    async def type(self, locator, text, delay=90):
        await locator.press_sequentially(text, delay=0 if self.quick else delay)
        await self.wait(0.3)

    async def scroll(self, top, ms=700):
        if self.lowest:
            top = max(0, min(top, await self.lowest()))
        if abs(await self.page.evaluate('scrollY') - top) < 1:
            return
        await self.page.evaluate(SCROLL_PAGE, [top, 60 if self.quick else ms])
        await self.wait(0.2)

    async def bring(self, locator, top=150, ms=700):
        """Scroll the page until the element stands `top` pixels below its upper edge."""
        y = (await self.box(locator))[1]
        await self.scroll(max(0, await self.page.evaluate('scrollY') + y - top), ms)

    async def slide(self, locator, top, ms=600):
        """Scroll inside an element; a negative `top` means to its end."""
        await locator.evaluate(SCROLL_ELEMENT, [top, 60 if self.quick else ms])
        await self.wait(0.2)

    async def reveal(self, locator, ms=350):
        """Bring an entry of a list that scrolls by itself into the part of the list that is shown; the page moves only by what is then still hidden."""
        if await locator.evaluate(REVEAL, [self.view[1], 60 if self.quick else ms]):
            await self.wait(0.2)
        rect = await self.box(locator)
        below = rect[1] + rect[3] - (self.view[1] - 6)
        if below > 0:
            await self.scroll(await self.page.evaluate('scrollY') + below, ms)


def load(path: Path):
    """The story file as a module; what stands next to it can be imported from it."""
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location('story', path)
    module = importlib.util.module_from_spec(spec)
    sys.modules['story'] = module
    spec.loader.exec_module(module)
    missing = [name for name in ('TITLE', 'CHAPTERS', 'story') if not hasattr(module, name)]
    if missing or not (hasattr(module, 'launch') or hasattr(module, 'URL')):
        raise SystemExit(f'故事文件里缺：{", ".join(missing) or "launch() 或 URL"}')
    return module


def listening(port):
    with contextlib.suppress(OSError), socket.create_connection(('127.0.0.1', port), timeout=0.5):
        return True
    return False


async def answering(api, address, seconds, server):
    """Wait until the app answers."""
    for _ in range(int(seconds / 0.5)):
        if server and server.poll() is not None:
            raise SystemExit('要录的服务一启动就退出了，见工作目录里的 server.log')
        with contextlib.suppress(httpx.HTTPError):
            if (await api.get(address)).status_code < 500:
                return
        await asyncio.sleep(0.5)
    raise SystemExit(f'{seconds} 秒内 {address} 没有应答，见工作目录里的 server.log')


def stop(server):
    """Stop the throwaway app and whatever it started."""
    if not server or server.poll() is not None:
        return
    if WINDOWS:  # no process groups to signal: the whole tree goes at once
        subprocess.run(['taskkill', '/F', '/T', '/PID', str(server.pid)], capture_output=True)
        with contextlib.suppress(subprocess.TimeoutExpired):
            server.wait(timeout=15)
        return
    with contextlib.suppress(ProcessLookupError):
        os.killpg(server.pid, signal.SIGTERM)  # it was started as the head of its own group: what it started goes with it
    try:
        server.wait(timeout=15)
    except subprocess.TimeoutExpired:
        with contextlib.suppress(ProcessLookupError):
            os.killpg(server.pid, signal.SIGKILL)


async def browser_for(playwright, density):
    """The browser named in the settings; else the one Playwright brought, else one of the system."""
    named = where('chromium')
    choices = [str(named)] if named else [None] + browsers()
    failed = []
    for path in choices:
        try:
            return await playwright.chromium.launch(executable_path=path, headless=True, args=[
                '--no-sandbox', '--disable-dev-shm-usage', '--hide-scrollbars', f'--force-device-scale-factor={density}']), path or 'Playwright 自带的 Chromium'
        except Exception as error:
            failed.append(f'{path or "Playwright 自带的 Chromium"}：{str(error).splitlines()[0][:160]}')
    raise SystemExit('没有能用的 Chromium。\n' + '\n'.join(failed) + '\n运行 demo_env.py 看怎么装')


async def record(story_file: Path, work: Path, quick: bool):
    story = load(story_file)
    view, density, port = tuple(getattr(story, 'VIEW', (1280, 620))), float(getattr(story, 'DENSITY', 2.5)), int(getattr(story, 'PORT', 8791))
    tongue = demo_text.language(getattr(story, 'LANGUAGE', None)) or demo_text.language(getattr(story, 'LOCALE', 'zh-CN')) or demo_text.guess([story.TITLE, *getattr(story, 'CHAPTERS', [])])
    if abs(view[0] / view[1] - SHAPE) > 0.004:
        raise SystemExit(f'VIEW 的宽高比要是 64:31（如 1280×620、1536×744、1600×775、1920×930），现在是 {view[0]}×{view[1]}')
    if (view[0] + 40) * density > 4096:
        raise SystemExit(f'VIEW 的宽 × DENSITY 不能超过 4096，现在是 {view[0]} × {density}')
    plan = story.launch(work, port) if hasattr(story, 'launch') else {'url': story.URL}
    url = plan['url']
    for name in ['frames', *plan.get('wipe', [])]:  # what an earlier recording left in the working folder
        target = (work / name).resolve()
        if work not in target.parents:
            raise SystemExit(f'wipe 只能写工作目录里面的东西：{name}')
        shutil.rmtree(target) if target.is_dir() else target.unlink(missing_ok=True)
    work.mkdir(parents=True, exist_ok=True)
    served = url.startswith('http')
    api = httpx.AsyncClient(base_url='{0.scheme}://{0.netloc}'.format(urlsplit(url)), trust_env=False, timeout=60) if served else None
    server, errors = None, []
    try:
        if plan.get('command'):
            if listening(port):
                raise SystemExit(f'端口 {port} 上已经有服务在跑，它不是这次录制启动的。换一个端口（故事文件里的 PORT），不要去停别人的服务')
            with open(work / 'server.log', 'w', encoding='utf-8', errors='replace') as log:
                server = subprocess.Popen([str(part) for part in plan['command']], cwd=plan.get('cwd'), stdout=log, stderr=subprocess.STDOUT,
                                          env={**os.environ, **{key: str(value) for key, value in (plan.get('env') or {}).items()}},
                                          **({'creationflags': subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW} if WINDOWS else {'start_new_session': True}))
        if served:
            await answering(api, plan.get('ready') or url, plan.get('timeout', 60), server)
        async with async_playwright() as playwright:
            browser, used = await browser_for(playwright, density)
            context = await browser.new_context(viewport={'width': view[0], 'height': view[1]}, device_scale_factor=density,
                                                locale=getattr(story, 'LOCALE', 'zh-CN'), accept_downloads=True)
            page = await context.new_page()
            page.on('pageerror', lambda error: errors.append(str(error)))
            await page.goto(url, wait_until='load')
            with contextlib.suppress(Exception):
                await page.wait_for_load_state('networkidle', timeout=8000)
            wide = await page.evaluate('document.documentElement.getBoundingClientRect().width')
            gutter = round(view[0] - wide)
            if 0 < gutter <= 40:  # the page keeps this much free at the right for a scrollbar: the window is made that much wider, and the video never shows it
                await page.set_viewport_size({'width': view[0] + gutter, 'height': view[1]})
                wide = await page.evaluate('document.documentElement.getBoundingClientRect().width')
                if abs(wide - view[0]) > 0.5:
                    raise SystemExit(f'页面宽 {wide}，预想的是 {view[0]}，镜头会对不准')
            else:
                gutter = 0
            about = {'title': story.TITLE, 'subtitle': getattr(story, 'SUBTITLE', ''), 'look': getattr(story, 'LOOK', {}), 'voice': dict(getattr(story, 'VOICE', {}) or {}, language=tongue),
                     'language': tongue, 'view': list(view), 'density': density, 'chapters': list(story.CHAPTERS),
                     'recorded': {'story': str(story_file), 'quick': quick, 'browser': used, 'gutter': gutter, 'at': time.strftime('%Y-%m-%d %H:%M')}}
            rec = Recorder(await context.new_cdp_session(page), work / 'frames', about)
            director = Director(page, rec, api, work, url, view, quick)
            director.tongue, director.say_as = tongue, dict(getattr(story, 'VOICE', {}).get('say') or {})
            director.reading = float(story.READING) if hasattr(story, 'READING') else demo_text.LANGUAGES[tongue]['reading']
            try:
                if hasattr(story, 'guard'):
                    await story.guard(director)
                await rec.start()
                started = time.time()
                try:
                    await story.story(director)
                finally:
                    await rec.stop()
                    timeline = rec.timeline(director.facts)
                    (work / 'timeline.json').write_text(json.dumps(timeline, ensure_ascii=False), encoding='utf-8')
            finally:
                await browser.close()
        lags = sorted(rec.lags) or [0]
        print(json.dumps({'录制用时秒': round(time.time() - started), '成片秒': timeline['duration'], '帧': len(rec.frames), '时间线条目': len(rec.events), '浏览器': used,
                          '帧到达延迟秒': {'中位': round(lags[len(lags) // 2], 3), '最大': round(lags[-1], 3)}, '页面脚本报错': errors}, ensure_ascii=False))
        print(json.dumps(director.facts, ensure_ascii=False))
        for line in director.tight:
            print('镜头：', line)
    finally:
        if api:
            await api.aclose()
        stop(server)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--story', type=Path, required=True, help='the story file written for the app')
    parser.add_argument('--work', type=Path, required=True, help='working folder: frames, timeline, the throwaway data')
    parser.add_argument('--quick', action='store_true', help='a trial run: nothing is waited for but the app itself')
    arguments = parser.parse_args()
    asyncio.run(record(arguments.story.resolve(), arguments.work.resolve(), arguments.quick))
