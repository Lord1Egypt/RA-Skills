"""Draw the demo video from a recording and encode it (demo_record.py makes the recording).

Every frame of the video is put together here: the part of the page the camera looks at, what is
marked on it, the cursor, the band of chapters above and the caption below. None of this is in the
recorded page itself, so captions and marks can be changed in the timeline and drawn again without
recording again.

    PY=~/.cache/auto-demo-recording/venv/bin/python
    $PY demo_render.py --work path/to/work --check                      # only checks the timeline, in numbers
    $PY demo_render.py --work path/to/work --out dist/演示.mp4            # draws, encodes, and compares the file with what was drawn
    $PY demo_render.py --work path/to/work --start 60 --end 90 --out /tmp/part.mp4
"""
from __future__ import annotations

import argparse
import bisect
import json
import math
import os
import shutil
import subprocess
import sys
import time
from functools import lru_cache
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
FPS = 60                         # the camera, the cursor and what is marked move this smoothly; the page itself is recorded at up to about 27 pictures a second
TOP, BOTTOM = 48, 102            # the band of chapters above the page, the band of captions below it
APP_H = H - TOP - BOTTOM         # the page as recorded fills what is between them
S = 2                            # what the video adds is drawn this many times larger and scaled down: smooth edges
INK, MUTED, LINE, BAND = (23, 26, 33), (108, 116, 131), (215, 219, 226), (238, 241, 246)
WHITE = (255, 255, 255)
ACCENT, SOFT = (47, 111, 237), (224, 234, 255)   # the chapter that is on, and those that are done: LOOK['accent'] in the story file
NOTE = (238, 92, 24)             # the colour of everything the video adds to the page; choose one the app itself does not use: LOOK['note']
FAST = '快进'                     # what the band says while waiting is played fast: LOOK['fast']
FADE = 0.18
NO_BREAK_BEFORE, NO_BREAK_AFTER, PAUSES = '，。、；：！？”’）》」…,.;:!?)', '“‘（《「(', '，。；：！？,.;:!?'
FONT_FOLDERS = ['/usr/share/fonts/opentype/noto', '/usr/share/fonts/noto-cjk', '/usr/share/fonts/google-noto-cjk', '/usr/share/fonts/opentype/noto-cjk',
                '/usr/share/fonts/truetype/noto', '/usr/local/share/fonts', '~/.local/share/fonts', '~/.fonts', '/System/Library/Fonts', '/Library/Fonts', '~/Library/Fonts',
                'C:/Windows/Fonts', '~/AppData/Local/Microsoft/Windows/Fonts']
FONT_NAMES = ['NotoSansCJK-{}.ttc', 'NotoSansCJKsc-{}.otf', 'NotoSansSC-{}.otf', 'NotoSansSC-{}.ttf', 'SourceHanSansSC-{}.otf', 'SourceHanSansCN-{}.otf']
# when neither Noto nor Source Han is installed: the Chinese faces the system itself has (Windows: Microsoft YaHei; macOS: PingFang SC, Hiragino)
PLATFORM_FONTS = {'Bold': ['msyhbd.ttc', 'Dengb.ttf', 'simhei.ttf', 'PingFang.ttc', 'Hiragino Sans GB.ttc', 'STHeiti Medium.ttc'],
                  'Medium': ['msyh.ttc', 'Deng.ttf', 'simhei.ttf', 'PingFang.ttc', 'Hiragino Sans GB.ttc', 'STHeiti Light.ttc'],
                  'Regular': ['msyh.ttc', 'Deng.ttf', 'simsun.ttc', 'PingFang.ttc', 'Hiragino Sans GB.ttc', 'STHeiti Light.ttc']}


# ---------- letters ----------
@lru_cache(maxsize=None)
def font_file(weight):
    """The file of the font in one of the weights Bold, Medium, Regular: (file, number of the face in it, name of the face).

    DEMO_FONT_BOLD, DEMO_FONT_MEDIUM, DEMO_FONT_REGULAR name a file (file#3 for a face in a collection); else Noto Sans CJK SC
    or Source Han Sans from the usual folders; else the system's own Chinese face (Microsoft YaHei, PingFang SC, Hiragino);
    else whatever the system gives for Chinese text of that weight."""
    named = os.environ.get(f'DEMO_FONT_{weight.upper()}')
    if named:
        path, _, index = named.partition('#')
        return path, int(index or 0), ImageFont.truetype(path, 20, index=int(index or 0)).getname()[0]
    for folder in FONT_FOLDERS:
        for name in FONT_NAMES + PLATFORM_FONTS[weight]:
            platform = name in PLATFORM_FONTS[weight]
            path = Path(folder).expanduser() / (name if platform else name.format(weight))
            for index in range(12 if path.is_file() else 0):
                try:
                    family = ImageFont.truetype(str(path), 20, index=index).getname()[0]
                except OSError:
                    break
                if platform:  # the system's face: its first one is the one wanted (PingFang SC is the first Chinese face in PingFang.ttc)
                    return str(path), index, family
                if path.suffix != '.ttc' or family.endswith((' SC', ' CN')):
                    return str(path), index, family
    if shutil.which('fc-match'):
        found = subprocess.run(['fc-match', '-f', '%{file}|%{index}|%{family}', f'sans-serif:lang=zh-cn:weight={ {"Bold": 200, "Medium": 100, "Regular": 80}[weight] }'],
                               capture_output=True, text=True).stdout.split('|')
        if len(found) == 3 and Path(found[0]).is_file():
            return found[0], int(found[1] or 0), found[2]
    raise SystemExit(f'找不到 {weight} 字重的字体：装 Noto Sans CJK，或用环境变量 DEMO_FONT_{weight.upper()} 指到字体文件')


@lru_cache(maxsize=None)
def font(weight, size):
    path, index, _ = font_file(weight)
    return ImageFont.truetype(path, size, index=index)


def missing_glyphs(text):
    """Characters the font has no drawing for: they come out as the same empty box as a character nobody has."""
    face = font('Medium', 32)
    blank = bytes(face.getmask(chr(0xF0000)))
    return sorted({ch for ch in text if not ch.isspace() and bytes(face.getmask(ch)) == blank})


def in_words(text):
    """Written with spaces between words (English), not in Chinese characters."""
    wide = sum(1 for ch in text if 0x2E80 <= ord(ch) <= 0x9FFF or 0xF900 <= ord(ch) <= 0xFAFF or 0xFF00 <= ord(ch) <= 0xFFEF)
    return 2 * wide < len(text.replace(' ', ''))


def wrap(text, limit=1240):
    """A caption in one line, or in two: broken after a comma or a full stop where that can be. Chinese breaks between
    characters, never inside a number or a Latin word; text written in words breaks between words."""
    words = in_words(text)
    for size in (33, 31, 29, 27):
        face = font('Medium', size)
        if face.getlength(text) <= limit:
            return [text], size
        fits = []
        for at in range(2, len(text) - 1):
            before, after = text[at - 1], text[at]
            if words:
                if after != ' ' or before == ' ':
                    continue
                parts = text[:at], text[at + 1:]
            elif after in NO_BREAK_BEFORE or before in NO_BREAK_AFTER or ' ' in (before, after) or (before.isascii() and after.isascii()):
                continue
            else:
                parts = text[:at], text[at:]
            left, right = face.getlength(parts[0]), face.getlength(parts[1])
            if left <= limit and right <= limit:
                fits.append((abs(left - right), parts))
        for after_pause in (True, False):
            best = min((fit for fit in fits if (fit[1][0][-1] in PAUSES) == after_pause), default=None)
            if best:
                return list(best[1]), size
    raise SystemExit(f'字幕太长，两行放不下：{text}')


def ease(p):
    return p * p * (3 - 2 * p)


def mix(a, b, p):
    return [x + (y - x) * p for x, y in zip(a, b)]


def colour(text):
    return tuple(int(text.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))


class Pen:
    """Draws on a picture S times as large as asked for; picture() gives it at the size asked for, with smooth edges."""

    def __init__(self, size, colour):
        self.image = Image.new('RGBA' if len(colour) == 4 else 'RGB', (size[0] * S, size[1] * S), colour)
        self.draw = ImageDraw.Draw(self.image)

    def box(self, x0, y0, x1, y1, radius=0, fill=None, outline=None, width=0):
        self.draw.rounded_rectangle([x0 * S, y0 * S, max(x0, x1) * S, max(y0, y1) * S], radius * S, fill=fill, outline=outline, width=width * S)

    def ring(self, x, y, r, fill=None, outline=None, width=0):
        self.draw.ellipse([(x - r) * S, (y - r) * S, (x + r) * S, (y + r) * S], fill=fill, outline=outline, width=width * S)

    def line(self, points, fill, width):
        self.draw.line([(x * S, y * S) for x, y in points], fill=fill, width=width * S, joint='curve')

    def shape(self, points, fill):
        self.draw.polygon([(x * S, y * S) for x, y in points], fill=fill)

    def text(self, x, y, text, weight, size, fill, anchor='lm'):
        self.draw.text((x * S, y * S), text, font=font(weight, size * S), fill=fill, anchor=anchor)

    def picture(self):
        return self.image.reduce(S)


def width_of(text, weight, size):
    return int(font(weight, size).getlength(text)) + 1


class Timeline:
    def __init__(self, work: Path):
        global ACCENT, SOFT, NOTE, FAST
        data = json.loads((work / 'timeline.json').read_text(encoding='utf-8'))
        self.work, self.view, self.density, self.duration = work, data['view'], data['density'], data['duration']
        self.title, self.subtitle, self.trial = data.get('title', ''), data.get('subtitle', ''), bool((data.get('recorded') or {}).get('quick'))
        look = data.get('look') or {}
        ACCENT, NOTE, FAST = colour(look.get('accent', '#2f6fed')), colour(look.get('note', '#ee5c18')), look.get('fast', FAST)
        SOFT = tuple(round(v + (255 - v) * 0.85) for v in ACCENT)
        self.chapters, self.frames, self.facts = data['chapters'], data['frames'], data.get('facts') or {}
        self.frame_times = [frame[0] for frame in self.frames]
        events = data['events']
        for event in events:
            if 'end' in event and event['end'] is None:
                event['end'] = self.duration
        kind = lambda name: sorted((e for e in events if e['type'] == name), key=lambda e: e['t'])
        self.captions, self.chapter_marks, self.boxes, self.steps = kind('caption'), kind('chapter'), kind('box'), kind('step')
        self.clicks, self.cards, self.notes, self.chips = kind('click'), kind('card'), kind('note'), kind('chip')
        self.caption_times, self.chapter_times = [e['t'] for e in self.captions], [e['t'] for e in self.chapter_marks]
        for card in self.cards:  # the first card is there from the first frame on, the last one stays to the last
            card['opens'], card['closes'] = card['t'] < 0.5, card['end'] > self.duration - 0.5
            card['t'], card['end'] = 0.0 if card['opens'] else card['t'], self.duration + 1 if card['closes'] else card['end']
        self.camera_moves = self._moves(kind('camera'), 'rect', [0, 0, *self.view])
        self.cursor_moves = self._moves(kind('cursor'), 'to', None)
        clock = data['clock'] + [[self.duration, 1]]
        self.fast = [(start, end, round(1 / rate)) for (start, rate), (end, _) in zip(clock, clock[1:]) if 0 < rate < 1 and end - start > 0.5]
        counts = {}
        for step in self.steps:  # steps are counted within their chapter
            chapter = bisect.bisect_right(self.chapter_times, step['t'])
            counts[chapter] = step['n'] = counts.get(chapter, 0) + 1

    def _moves(self, events, key, start):
        moves = []
        for event in events:
            origin = self._value(moves, event['t'], start)
            moves.append((event['t'], event.get('d', 0), origin if origin is not None else event[key], event[key]))
        return moves

    @staticmethod
    def _value(moves, t, start):
        value = start
        for begin, d, origin, target in moves:
            if t < begin:
                break
            value = target if d <= 0 or t >= begin + d else mix(origin, target, ease((t - begin) / d))
        return value

    def camera(self, t):
        return self._value(self.camera_moves, t, [0, 0, *self.view])

    def settled(self, event):
        """A moment at which this is shown and the camera stands still."""
        t = event['t'] + 0.1
        while t < event['end'] - 0.5:
            if self.camera(t) == self.camera(t + 0.4):
                return t + 0.2
            t += 0.2
        return (event['t'] + event['end']) / 2

    def frame_index(self, t):
        return max(0, bisect.bisect_right(self.frame_times, t) - 1)

    def cursor(self, t):
        return self._value(self.cursor_moves, t, None)

    def caption(self, t):
        index = bisect.bisect_right(self.caption_times, t) - 1
        return self.captions[index]['text'] if index >= 0 else ''

    def chapter(self, t):
        index = bisect.bisect_right(self.chapter_times, t) - 1
        return self.chapter_marks[index]['index'] if index >= 0 else None

    @staticmethod
    def shown(event, t, fade=FADE):
        """How much of something is there at this time: fading in at its start and out at its end."""
        if not event['t'] <= t < event['end']:
            return 0.0
        return round(min(1.0, (t - event['t']) / fade + 0.05, (event['end'] - t) / fade + 0.05), 2)

    def card(self, card, t):
        if not card['t'] <= t < card['end']:
            return 0.0
        return round(min(1.0, 1.0 if card['opens'] else (t - card['t']) / 0.35 + 0.05, 1.0 if card['closes'] else (card['end'] - t) / 0.35 + 0.05), 2)

    def texts(self):
        out = [e['text'] for e in self.captions] + [e['label'] or '' for e in self.boxes] + [e['text'] for e in self.steps + self.chips]
        for event in self.cards + self.notes:
            out += event['lines'] + [event.get('title', '')]
        return out + self.chapters + [self.title, self.subtitle, FAST + ' ×']


# ---------- what is drawn over the page ----------
def on_screen(rect, cam):
    scale = W / cam[2]
    return [(rect[0] - cam[0]) * scale, (rect[1] - cam[1]) * scale, rect[2] * scale, rect[3] * scale]


def chip_size(text):
    return width_of(text, 'Bold', 24) + 26, 40


PLACES = ('above', 'above-center', 'above-right', 'below', 'below-center', 'below-right', 'right', 'left', 'in-top-right', 'in-right', 'in-bottom-right')


def union(rects):
    left, top = min(r[0] for r in rects), min(r[1] for r in rects)
    return [left, top, max(r[0] + r[2] for r in rects) - left, max(r[1] + r[3] for r in rects) - top]


def overlap(a, b):
    return a[0] < b[0] + b[2] and b[0] < a[0] + a[2] and a[1] < b[1] + b[3] and b[1] < a[1] + a[3]


def label_at(box, text, place, nudge=0):
    """Where the label of a marked box goes for one of the PLACES: left, top, width, height in the picture. `nudge` moves it further out to the side."""
    x, y, w, h = box
    cw, ch = chip_size(text)
    if place == 'right':
        return x + w + 18 + nudge, y + h / 2 - ch / 2, cw, ch
    if place == 'left':
        return x - cw - 18 - nudge, y + h / 2 - ch / 2, cw, ch
    if place.startswith('in-'):
        return x + w - cw - 12, {'in-top-right': y + 12, 'in-right': y + h / 2 - ch / 2, 'in-bottom-right': y + h - ch - 12}[place], cw, ch
    left = x + w / 2 - cw / 2 if place.endswith('center') else x + w - cw + 7 if place.endswith('right') else x - 7
    return left, (y - ch - 14 if place.startswith('above') else y + h + 14), cw, ch


def place_label(box, text, place, nudge=0):
    left, top, cw, ch = label_at(box, text, place, nudge)
    return round(min(max(left, 6), W - cw - 6)), round(min(max(top, 6), APP_H - ch - 6))


def part_of(picture, rect, density):
    x0, y0 = max(0, round(rect[0] * density)), max(0, round(rect[1] * density))
    return picture[y0:max(y0, round((rect[1] + rect[3]) * density)), x0:max(x0, round((rect[0] + rect[2]) * density))]


def ink(picture, rect, density):
    """How much is drawn in a part of the page: the share of its pixels that lie on an edge. Text gives a lot, an empty surface nothing."""
    part = part_of(picture, rect, density)
    if part.shape[0] < 3 or part.shape[1] < 3:
        return 1.0
    return float((np.abs(cv2.Laplacian(cv2.cvtColor(part, cv2.COLOR_BGR2GRAY), cv2.CV_16S, ksize=3)) > 24).mean())


def share_of(picture, rect, density, colour):
    """The share of a part of the page that has this colour ('#rrggbb')."""
    part = part_of(picture, rect, density)
    wanted = np.array([int(colour[i:i + 2], 16) for i in (5, 3, 1)])
    return float((np.abs(part.astype(int) - wanted).max(axis=2) <= 14).mean()) if part.size else 0.0


def settle_labels(tl, painter):
    """Each label goes next to its box where the page is empty: to the place asked for if nothing is drawn there
    (further out to the side if something stands right next to the box), else to the emptiest of the other places."""
    placed = []
    for box in tl.boxes:
        if not box.get('label'):
            continue
        t = tl.settled(box)
        cam = tl.camera(t)
        scale, frame, wanted = W / cam[2], painter.page(tl.frame_index(t)), box.get('place') or 'above'
        fixed = box.get('pin') or box['kind'] == 'spot'
        on = on_screen(union(box['rects']), cam)
        taken = [rect for other in tl.boxes if other is not box and other['t'] < box['end'] and box['t'] < other['end'] for rect in other['rects']]
        taken += [rect for start, end, rect in placed if start < box['end'] and box['t'] < end]
        best = None
        for rank, place in enumerate([wanted] if fixed else [wanted] + [other for other in PLACES if other != wanted]):
            for nudge in ((0, 40, 80, 120, 160, 200, 240) if place in ('right', 'left') and not fixed else (0,)):
                left, top, cw, ch = label_at(on, box['label'], place, nudge)
                if fixed:
                    left, top = place_label(on, box['label'], place)
                elif left < 6 or top < 6 or left + cw > W - 6 or top + ch > APP_H - 6 or (place.startswith('in-') and (on[2] < cw + 80 or on[3] < ch + 24)):
                    continue
                rect = [cam[0] + left / scale, cam[1] + top / scale, cw / scale, ch / scale]
                drawn = ink(frame, rect, tl.density)
                score = drawn + 0.004 * rank + 0.00008 * nudge + (0.03 if place.startswith('in-') else 0) + (1 if any(overlap(rect, other) for other in taken) else 0)
                if best is None or score < best[0]:
                    best = (score, place, nudge, rect, drawn)
            if best and best[0] < 0.02:
                break
        if best is None:  # no place is free: the place asked for, kept inside the picture
            left, top = place_label(on, box['label'], wanted)
            rect = [cam[0] + left / scale, cam[1] + top / scale, *(v / scale for v in chip_size(box['label']))]
            best = (1, wanted, 0, rect, ink(frame, rect, tl.density))
        box['place'], box['nudge'], box['under'] = best[1], round(best[2] / scale, 1), round(best[4], 3)
        placed.append((box['t'], box['end'], best[3]))


def plan(tl: Timeline, t, cam):
    """Everything the video adds to the page at this time, as a list of things to draw, and where the cursor is. Equal lists give equal pictures."""
    marks = []
    boxes = [(box, tl.shown(box, t)) for box in tl.boxes if box['t'] <= t < box['end']]
    for box, a in boxes:
        if box['kind'] == 'spot':
            marks.append(('spot', tuple(round(v) for v in on_screen(box['rects'][0], cam)), a))
    for box, a in boxes:
        if box['kind'] != 'spot':
            marks += [(box['kind'], tuple(round(v) for v in on_screen(rect, cam)), a) for rect in box['rects']]
    for box, a in boxes:
        if box.get('label'):
            marks.append(('label', box['label'], *place_label(on_screen(union(box['rects']), cam), box['label'], box.get('place') or 'above', box.get('nudge', 0) * W / cam[2]), a))
    for step in tl.steps:
        a = tl.shown(step, t)
        if a > 0:
            x, y, w, h = on_screen(step['rect'], cam)
            marks.append(('step', step['n'], step['text'], round(x + w / 2), round(y), round(y + h), a))
    for click in tl.clicks:
        p = (t - click['t']) / 0.5
        if 0 <= p < 1:
            x, y, _, _ = on_screen([*click['at'], 0, 0], cam)
            marks.append(('ripple', round(x), round(y), round(10 + 34 * p), round(1 - p, 2)))
    for note in tl.notes:
        a = tl.shown(note, t)
        if a > 0:
            marks.append(('note', note['title'], tuple(note['lines']), a))
    for chip in tl.chips:
        a = tl.shown(chip, t)
        if a > 0:
            marks.append(('chip', chip['text'], a))
    for mark in tl.chapter_marks:
        a = tl.shown({'t': mark['t'], 'end': mark['t'] + 2.6}, t, 0.3)
        if a > 0:
            marks.append(('chapter', mark['index'] + 1, len(tl.chapters), tl.chapters[mark['index']], a))
    pointer = tl.cursor(t)
    if pointer:
        x, y, _, _ = on_screen([*pointer, 0, 0], cam)
        pointer = (round(x), round(y)) if -30 < x < W and -30 < y < APP_H else None
    return tuple(marks), pointer


def draw_marks(marks):
    """The list from plan() as a picture to lay over the page."""
    pen = Pen((W, APP_H), (0, 0, 0, 0))
    for item in marks:
        kind, a = item[0], item[-1]
        note, ink, white = (*NOTE, round(255 * a)), (*INK, round(255 * a)), (*WHITE, round(255 * a))
        if kind == 'spot':
            x, y, w, h = item[1]
            pen.box(0, 0, W, APP_H, fill=(12, 16, 24, round(122 * a)))
            pen.box(x - 8, y - 8, x + w + 8, y + h + 8, 14, fill=(0, 0, 0, 0))
            pen.box(x - 8, y - 8, x + w + 8, y + h + 8, 14, outline=note, width=4)
        elif kind == 'outline':
            x, y, w, h = item[1]
            pen.box(x - 12, y - 12, x + w + 12, y + h + 12, 16, outline=(*NOTE, round(64 * a)), width=5)
            pen.box(x - 7, y - 7, x + w + 7, y + h + 7, 11, outline=note, width=4)
        elif kind == 'mark':
            x, y, w, h = item[1]
            pen.box(x - 5, y - 4, x + w + 5, y + h + 4, 7, outline=note, width=3)
        elif kind == 'label':
            _, text, x, y, _ = item
            cw, ch = chip_size(text)
            pen.box(x, y, x + cw, y + ch, 9, fill=note)
            pen.text(x + 13, y + ch / 2 - 1, text, 'Bold', 24, white)
        elif kind == 'step':
            _, number, text, cx, top, bottom, _ = item
            width, height = width_of(text, 'Bold', 24) + 68, 44
            x = round(min(max(cx - width / 2, 6), W - width - 6))
            above = top - height - 22 >= 6
            y = top - height - 22 if above else min(bottom + 22, APP_H - height - 6)
            tip = min(max(cx, x + 26), x + width - 26)
            pen.shape([(tip - 10, y + height - 2), (tip + 10, y + height - 2), (tip, y + height + 11)] if above
                      else [(tip - 10, y + 2), (tip + 10, y + 2), (tip, y - 11)], ink)
            pen.box(x, y, x + width, y + height, height / 2, fill=ink)
            pen.ring(x + 22, y + 22, 16, fill=note)
            pen.text(x + 22, y + 21, str(number), 'Bold', 21, white, 'mm')
            pen.text(x + 48, y + 21, text, 'Bold', 24, white)
        elif kind == 'ripple':
            _, x, y, r, _ = item
            pen.ring(x, y, r, outline=(*NOTE, round(235 * a)), width=5)
        elif kind == 'note':
            _, title, lines, _ = item
            width = max(width_of(title, 'Bold', 26), *(width_of(line, 'Regular', 25) for line in lines)) + 76
            height = 62 + 40 * len(lines) + 22
            x, y = (W - width) // 2, 112
            pen.box(x + 2, y + 8, x + width + 2, y + height + 8, 20, fill=(16, 24, 40, round(52 * a)))
            pen.box(x, y, x + width, y + height, 20, fill=white)
            pen.box(x, y, x + width, y + height, 20, outline=note, width=3)
            pen.text(x + 38, y + 40, title, 'Bold', 26, note)
            for row, line in enumerate(lines):
                pen.text(x + 38, y + 84 + 40 * row, line, 'Regular', 25, ink)
        elif kind == 'chip':
            _, text, _ = item
            width = width_of(text, 'Medium', 24) + 82
            x, y = W - width - 28, APP_H - 46 - 26
            pen.box(x, y, x + width, y + 46, 23, fill=ink)
            pen.line([(x + 32, y + 12), (x + 32, y + 28)], white, 3)
            pen.line([(x + 24, y + 21), (x + 32, y + 29), (x + 40, y + 21)], white, 3)
            pen.line([(x + 22, y + 35), (x + 42, y + 35)], white, 3)
            pen.text(x + 58, y + 22, text, 'Medium', 24, white)
        elif kind == 'chapter':
            _, number, of, title, _ = item
            width = width_of(title, 'Bold', 30) + width_of(f'{number} / {of}', 'Medium', 20) + 118
            x, y = 28, APP_H - 60 - 26
            pen.box(x, y, x + width, y + 60, 30, fill=ink)
            pen.ring(x + 30, y + 30, 21, fill=note)
            pen.text(x + 30, y + 29, str(number), 'Bold', 26, white, 'mm')
            pen.text(x + 64, y + 29, title, 'Bold', 30, white)
            pen.text(x + width - 26, y + 30, f'{number} / {of}', 'Medium', 20, (190, 196, 208, round(255 * a)), 'rm')
    return pen.picture()


@lru_cache(maxsize=None)
def cursor_sprite():
    scale, big = 1.45, 4
    shape = [(0, 0), (0, 24), (6, 18.6), (10, 27.6), (13.6, 26), (9.8, 17.2), (17.6, 17.2)]
    image = Image.new('RGBA', (int(24 * scale * big), int(32 * scale * big)), (0, 0, 0, 0))
    points = [((x + 2) * scale * big, (y + 2) * scale * big) for x, y in shape]
    ImageDraw.Draw(image).polygon(points, fill=(20, 22, 28, 255), outline=(255, 255, 255, 255), width=int(1.6 * scale * big))
    return image.resize((image.width // big, image.height // big), Image.LANCZOS), round(2 * scale)


# ---------- the bands and the cards ----------
def chapter_strip(title, subtitle, chapters, current):
    """The chapters at the right of the upper band: [(text, width)], each with its name where there is room for that, else only the one that is on."""
    left = 30 + width_of(title, 'Bold', 22) + 14 + (width_of(subtitle, 'Regular', 18) if subtitle else 0) + 26 + width_of(f'{FAST} ×16', 'Bold', 19) + 58 + 30
    names = [f'{i + 1}  {name}' for i, name in enumerate(chapters)]
    if sum(width_of(name, 'Medium', 19) + 28 for name in names) + 6 * (len(names) - 1) > W - 26 - left:
        names = [name if i == current else str(i + 1) for i, name in enumerate(names)]
    widths = [width_of(name, 'Medium', 19) + 28 for name in names]
    return list(zip(names, widths)), W - 26 - sum(widths) - 6 * (len(widths) - 1) >= left


@lru_cache(maxsize=None)
def top_band(title, subtitle, chapters, current, fast):
    pen = Pen((W, TOP), BAND)
    pen.text(30, TOP / 2 - 1, title, 'Bold', 22, INK)
    x = 30 + width_of(title, 'Bold', 22) + 14
    if subtitle:
        pen.text(x, TOP / 2, subtitle, 'Regular', 18, MUTED)
        x += width_of(subtitle, 'Regular', 18)
    if fast:  # waiting that is played fast says so
        x += 26
        text = f'{FAST} ×{fast}'
        pen.box(x, 9, x + width_of(text, 'Bold', 19) + 58, TOP - 9, 15, fill=NOTE)
        for offset in (0, 12):
            pen.shape([(x + 15 + offset, 17), (x + 15 + offset, TOP - 17), (x + 26 + offset, TOP / 2)], WHITE)
        pen.text(x + 45, TOP / 2 - 1, text, 'Bold', 19, WHITE)
    strip, _ = chapter_strip(title, subtitle, chapters, current)
    x = W - 26 - sum(width for _, width in strip) - 6 * (len(strip) - 1)
    for i, (name, width) in enumerate(strip):
        here, done = current == i, current is not None and i < current
        if here or done:
            pen.box(x, 9, x + width, TOP - 9, 15, fill=ACCENT if here else SOFT)
        pen.text(x + 14, TOP / 2 - 1, name, 'Medium', 19, WHITE if here else ACCENT if done else MUTED)
        x += width + 6
    pen.box(0, TOP - 1, W, TOP, fill=LINE)
    return np.asarray(pen.picture())


@lru_cache(maxsize=64)
def bottom_band(text):
    pen = Pen((W, BOTTOM), WHITE)
    pen.box(0, 0, W, 1, fill=LINE)
    if text:
        lines, size = wrap(text)
        step = size + 11
        first = BOTTOM / 2 - step * (len(lines) - 1) / 2
        for row, line in enumerate(lines):
            pen.text(W / 2, first + row * step, line, 'Medium', size, INK, 'mm')
    return np.asarray(pen.picture())


@lru_cache(maxsize=None)
def card(lines):
    """A card over the whole picture: a short bar in the accent colour, a title, and lines below it (the last one smaller, when there are several)."""
    pen = Pen((W, H), WHITE)
    title, rest = lines[0], lines[1:]
    top = 540 - (150 + 76 * len(rest)) / 2
    pen.box(W / 2 - 38, top, W / 2 + 38, top + 8, 4, fill=ACCENT)
    size = next((size for size in (70, 62, 54, 46, 40) if width_of(title, 'Bold', size) <= W - 320), 40)
    pen.text(W / 2, top + 92, title, 'Bold', size, INK, 'mm')
    for row, line in enumerate(rest):
        last = row == len(rest) - 1 and len(rest) > 1
        pen.text(W / 2, top + 200 + row * 76, line, 'Regular', 26 if last else 38, MUTED if last else (74, 82, 97), 'mm')
    return np.asarray(pen.picture())


# ---------- putting the frames together ----------
class Painter:
    def __init__(self, tl: Timeline):
        self.tl, self.loaded, self.picture, self.key, self.bytes = tl, None, None, None, None
        self.layers, self.drawn = {}, 0
        settle_labels(tl, self)

    def page(self, index):
        if self.loaded != index:
            path = self.tl.work / 'frames' / self.tl.frames[index][1]
            self.picture = cv2.imdecode(np.fromfile(path, np.uint8), cv2.IMREAD_COLOR)
            if self.picture is None:
                raise SystemExit(f'读不出这一帧：{path}')
            self.loaded = index
        return self.picture

    def layer(self, marks):
        if marks not in self.layers:
            if len(self.layers) > 3:
                self.layers.pop(next(iter(self.layers)))
            self.layers[marks] = draw_marks(marks)
        return self.layers[marks]

    def frame(self, t):
        tl = self.tl
        cards = tuple((tuple(card['lines']), tl.card(card, t)) for card in tl.cards if card['t'] <= t < card['end'])
        if cards and cards[-1][1] >= 1:
            key = cards[-1]
        else:
            index = tl.frame_index(t)
            cam = tuple(round(v, 1) for v in tl.camera(t))
            caption, chapter = tl.caption(t), tl.chapter(t)
            fast = next((speed for start, end, speed in tl.fast if start <= t < end), 0)
            key = (index, cam, caption, chapter, fast, cards, plan(tl, t, cam))
        if key == self.key:
            return self.bytes
        self.key, self.drawn = key, self.drawn + 1
        if len(key) == 2:
            canvas = card(key[0])
        else:
            marks, pointer = key[-1]
            picture, d = self.page(index), tl.density
            x0, y0 = round(cam[0] * d), round(cam[1] * d)
            x1, y1 = min(picture.shape[1], round((cam[0] + cam[2]) * d)), min(picture.shape[0], round((cam[1] + cam[3]) * d))
            part = picture[y0:y1, x0:x1]
            if part.shape[1] != W or part.shape[0] != APP_H:
                part = cv2.resize(part, (W, APP_H), interpolation=cv2.INTER_AREA if part.shape[1] > W else cv2.INTER_CUBIC)
            app = Image.fromarray(cv2.cvtColor(part, cv2.COLOR_BGR2RGB))
            if marks:
                layer = self.layer(marks)
                app.paste(layer, (0, 0), layer)
            if pointer:
                sprite, offset = cursor_sprite()
                app.paste(sprite, (pointer[0] - offset, pointer[1] - offset), sprite)
            canvas = np.empty((H, W, 3), np.uint8)
            canvas[:TOP] = top_band(tl.title, tl.subtitle, tuple(tl.chapters), chapter, fast)
            canvas[TOP:TOP + APP_H] = np.asarray(app)
            canvas[TOP + APP_H:] = bottom_band(caption)
            for lines, a in cards:
                canvas = cv2.addWeighted(card(lines), a, canvas, 1 - a, 0)
        self.bytes = canvas.tobytes()
        return self.bytes


def check(tl: Timeline):
    """What can be told about the picture without looking at it. Returns a summary and the list of things that are off."""
    off = []
    painter = Painter(tl)
    for box in tl.boxes:  # is something drawn where a box is, and is it what the box was meant for
        t = tl.settled(box)
        frame = painter.page(tl.frame_index(t))
        if min(ink(frame, rect, tl.density) for rect in box['rects']) < 0.003:
            off.append(f'{t:.1f}s 标注框里是空的：{box.get("label")} {box["rects"][0]}')
        if box.get('expect'):
            box['match'] = round(min(share_of(frame, rect, tl.density, box['expect']) for rect in box['rects']), 2)
            if box['match'] < 0.3:
                off.append(f'{t:.1f}s 标注框里不是预想的内容（颜色 {box["expect"]} 只占 {box["match"]:.0%}）：{box.get("label")} {box["rects"][0]}')
        if box.get('under', 0) > 0.06 and not box.get('pin') and box['kind'] != 'spot':
            off.append(f'{t:.1f}s 标注文字压在页面内容上（{box["under"]:.0%}）：{box["label"]}，位置 {box["place"]}')
    missing = missing_glyphs(''.join(tl.texts()))
    if missing:
        off.append(f'字体里没有这些字符：{"".join(missing)}')
    if not chapter_strip(tl.title, tl.subtitle, tuple(tl.chapters), 0)[1]:
        off.append('章节太多或名字太长，顶上的章节条放不下')
    two_lines = sum(1 for caption in tl.captions if caption['text'] and len(wrap(caption['text'])[0]) > 1)
    share = lambda rect, cam: (max(0, min(rect[0] + rect[2], cam[0] + cam[2]) - max(rect[0], cam[0])) * max(0, min(rect[1] + rect[3], cam[1] + cam[3]) - max(rect[1], cam[1]))) / max(1e-6, rect[2] * rect[3])
    for box in tl.boxes:
        middle = (box['t'] + box['end']) / 2
        if box['end'] - box['t'] < 0.8:
            off.append(f'{box["t"]:.1f}s 标注只出现了 {box["end"] - box["t"]:.1f} 秒：{box.get("label")}')
        for rect in box['rects']:
            if rect[2] <= 0 or rect[3] <= 0:
                off.append(f'{box["t"]:.1f}s 标注框没有大小：{box.get("label")}')
            elif share(rect, tl.camera(middle)) < 0.9:
                off.append(f'{middle:.1f}s 标注框有一部分在画面外：{box.get("label")} {rect}，镜头 {[round(v) for v in tl.camera(middle)]}')
    for step in tl.steps:
        if share(step['rect'], tl.camera(step['end'] - 0.35)) < 0.9:
            off.append(f'{step["t"]:.1f}s 步骤“{step["text"]}”的目标不在画面里')
    for click in tl.clicks:
        if share([click['at'][0] - 1, click['at'][1] - 1, 2, 2], tl.camera(click['t'])) < 1:
            off.append(f'{click["t"]:.1f}s 点击的位置不在画面里')
    gaps = np.diff(tl.frame_times) if len(tl.frame_times) > 1 else np.array([0.0])
    summary = {'成片秒': tl.duration, '页面帧': len(tl.frames), '最长静止秒': round(float(gaps.max()), 1), '字幕': sum(1 for c in tl.captions if c['text']),
               '两行字幕': two_lines, '标注框': len(tl.boxes), '其中原文高亮': sum(1 for box in tl.boxes if box['kind'] == 'spot'), '步骤': len(tl.steps),
               '放大': sum(1 for move in tl.camera_moves if move[3][2] < tl.view[0] - 1), '最大放大倍数': round(max([tl.view[0] / move[3][2] for move in tl.camera_moves] or [1]), 2),
               '快进段': [(round(start, 1), round(end, 1), f'×{speed}') for start, end, speed in tl.fast],
               '章节起点秒': [round(mark['t'], 1) for mark in tl.chapter_marks]}
    return summary, off


ENCODE = ['-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
          '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-threads', '4']


def encode(tl: Timeline, out: Path, first, last):
    """Frames `first` up to `last` into a file without sound."""
    encoder = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', *ENCODE, '-g', str(3 * FPS), str(out)],
                               stdin=subprocess.PIPE)
    painter = Painter(tl)
    try:
        for number in range(first, last):
            encoder.stdin.write(painter.frame(number / FPS))
    finally:
        encoder.stdin.close()
        code = encoder.wait()
    if code:
        raise SystemExit(f'ffmpeg 退出码 {code}')
    return painter.drawn


def render(work: Path, out: Path, first, last, jobs):
    """The video is drawn in several parts at the same time; the parts are then joined and a silent track is added."""
    parts_folder = work / 'parts'
    shutil.rmtree(parts_folder, ignore_errors=True)
    parts_folder.mkdir(parents=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    jobs = max(1, min(jobs, (last - first) // 300))
    bounds = [first + round(i * (last - first) / jobs) for i in range(jobs + 1)]
    parts = [parts_folder / f'{i:02d}.mp4' for i in range(jobs)]
    workers = [subprocess.Popen([sys.executable, __file__, '--work', str(work), '--out', str(part), '--fps', str(FPS), '--frames', f'{a}:{b}'])
               for part, a, b in zip(parts, bounds, bounds[1:])]
    if any([worker.wait() for worker in workers]):
        raise SystemExit('有一段没有画成')
    (parts_folder / 'list.txt').write_text(''.join(f"file '{part.name}'\n" for part in parts), encoding='utf-8')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', 'list.txt',
                    '-f', 'lavfi', '-t', f'{(last - first) / FPS:.3f}', '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100',  # a silent track: some players and editors want one
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '64k', '-movflags', '+faststart', str(out)], cwd=parts_folder, check=True)
    shutil.rmtree(parts_folder, ignore_errors=True)


def compare(tl: Timeline, out: Path, first, last, samples=12):
    """The file against what was drawn, without looking at either: what the file says about itself, and how close some of
    its frames, read back, are to the same frames drawn again (in dB; the encoder's loss leaves 35 and more)."""
    probe = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=codec_name,pix_fmt,width,height,r_frame_rate,nb_frames,duration',
                                       '-of', 'json', str(out)], capture_output=True, text=True, check=True).stdout)['streams'][0]
    painter, close = Painter(tl), []
    for sample in range(samples):
        number = round((sample + 0.5) * (last - first) / samples)
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{max(0.0, (number - 0.25) / FPS):.5f}', '-i', str(out), '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                             capture_output=True).stdout
        if len(raw) != W * H * 3:
            close.append(0.0)
            continue
        drawn = np.frombuffer(painter.frame((first + number) / FPS), np.uint8).astype(np.float64)
        close.append(round(10 * math.log10(255 ** 2 / max(1e-9, float(((np.frombuffer(raw, np.uint8) - drawn) ** 2).mean()))), 1))
    facts = {'编码': probe.get('codec_name'), '像素格式': probe.get('pix_fmt'), '宽高': [probe.get('width'), probe.get('height')], '帧率': probe.get('r_frame_rate'),
             '帧数': int(probe.get('nb_frames') or 0), '时长秒': round(float(probe.get('duration') or 0), 3), '读回的画面与所画的接近程度dB': {'最低': min(close), '中位': sorted(close)[len(close) // 2]}}
    off = []
    if facts['帧数'] != last - first:
        off.append(f'文件有 {facts["帧数"]} 帧，画的是 {last - first} 帧')
    if facts['宽高'] != [W, H] or facts['编码'] != 'h264':
        off.append(f'文件不是 {W}×{H} 的 H.264')
    if min(close) < 32:
        off.append(f'读回的画面和所画的差得多（最低 {min(close)} dB）')
    return facts, off


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--work', type=Path, required=True, help='the working folder of the recording')
    parser.add_argument('--out', type=Path, help='the video file to write')
    parser.add_argument('--check', action='store_true', help='check the timeline and stop')
    parser.add_argument('--start', type=float, default=0.0, help='seconds; with --end, only this part of the video')
    parser.add_argument('--end', type=float, default=None)
    parser.add_argument('--jobs', type=int, default=6)
    parser.add_argument('--fps', type=int, default=FPS)
    parser.add_argument('--frames', help='first:last, one part of the video without sound (used by this script itself)')
    arguments = parser.parse_args()
    FPS = arguments.fps
    timeline = Timeline(arguments.work.resolve())
    if arguments.frames:
        encode(timeline, arguments.out, *(int(number) for number in arguments.frames.split(':')))
        raise SystemExit(0)
    if not arguments.check and not arguments.out:
        raise SystemExit('要写到哪个文件：--out；只检查时间线：--check')
    summary, problems = check(timeline)
    print(json.dumps(summary, ensure_ascii=False))
    if timeline.trial:
        print('注意： 这是试跑（--quick）的时间线：标注出现时间短、镜头没停稳一类的提示不算数，成片要用正式录制的')
    if arguments.check:
        for caption in timeline.captions:
            if caption['text']:
                print(f'{caption["t"]:7.1f}  ' + ' ／ '.join(wrap(caption['text'])[0]))
        for box in timeline.boxes:
            if box.get('label') or box.get('expect'):
                print(f'{box["t"]:7.1f}  {box["kind"]:7s} {box.get("label") or "":22s} 位置 {box.get("place"):16s} 文字下方 {box.get("under", "")!s:6s} 颜色相符 {box.get("match", "")}')
        print(json.dumps(timeline.facts, ensure_ascii=False))
    for problem in problems:
        print('注意：', problem)
    if not arguments.check:
        began = time.time()
        first = round(arguments.start * FPS)
        last = round(min(timeline.duration, arguments.end if arguments.end is not None else timeline.duration) * FPS)
        out = arguments.out.resolve()
        render(arguments.work.resolve(), out, first, last, arguments.jobs)
        facts, off = compare(timeline, out, first, last)
        print(json.dumps({'输出': str(out), '帧': last - first, '秒': round((last - first) / FPS, 1), '用时秒': round(time.time() - began), **facts}, ensure_ascii=False))
        for problem in off:
            print('注意：', problem)
        if first == 0 and arguments.end is None:  # the whole video: demo_voice.py takes this file as the one to narrate
            (arguments.work.resolve() / 'render.json').write_text(json.dumps({'out': str(out), 'fps': FPS, 'frames': last, 'problems': problems + off}, ensure_ascii=False, indent=1), encoding='utf-8')
