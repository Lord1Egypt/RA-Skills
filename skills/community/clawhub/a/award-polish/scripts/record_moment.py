import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageStat
from playwright.sync_api import sync_playwright

from layout_check import execute_step
from side_by_side import font


INIT = r"""
(() => {
  const nativeRAF = window.requestAnimationFrame.bind(window);
  const nativeCancelRAF = window.cancelAnimationFrame.bind(window);
  const label = el => el ? el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') +
    (typeof el.className === 'string' && el.className.trim() ? '.' + el.className.trim().split(/\s+/).slice(0,2).join('.') : '') : '?';
  const state = {active: false, entries: new Map(), origin: 0, handle: null};
  state.collect = () => {
    if (!state.active) return;
    for (const animation of document.getAnimations()) {
      if (animation.timeline !== document.timeline || state.entries.has(animation)) continue;
      const effect = animation.effect, timing = effect.getTiming();
      const keyframes = effect.getKeyframes();
      const easings = [...new Set(keyframes.slice(0,-1).map(frame => frame.easing))];
      const start = performance.now() - state.origin;
      const initial = Number(animation.currentTime || 0);
      const record = {el: effect.pseudoElement || label(effect.target), type: animation.constructor.name,
        name: animation.animationName || animation.transitionProperty || '', duration: timing.duration,
        delay: timing.delay, easing: timing.easing !== 'linear' ? timing.easing : (easings.join(', ') || timing.easing),
        iterations: Number.isFinite(timing.iterations) ? timing.iterations : 'Infinity', appeared_ms: start};
      state.entries.set(animation, {initial, start, record});
      animation.pause();
    }
  };
  state.watch = () => {
    if (!state.active) return;
    state.collect();
    state.handle = nativeRAF(state.watch);
  };
  state.begin = () => {
    state.entries.clear(); state.origin = performance.now(); state.active = true;
    state.collect(); state.handle = nativeRAF(state.watch);
  };
  state.seek = t => {
    state.collect();
    for (const [animation, entry] of state.entries) animation.currentTime = entry.initial + t - entry.start;
  };
  state.end = () => {
    state.active = false; nativeCancelRAF(state.handle);
    const records = [...state.entries.values()].map(e => e.record);
    for (const animation of state.entries.keys()) animation.play();
    state.entries.clear(); return records;
  };
  state.paint = () => new Promise(resolve => nativeRAF(() => nativeRAF(resolve)));
  window.__moment = state;
})();
"""


def raw_action(page, step, target, center):
    if 'click' in step:
        page.mouse.click(*center)
    elif 'hover' in step:
        page.mouse.move(*center)
    elif 'fill' in step:
        target.evaluate("el => {el.focus(); el.value = ''; el.dispatchEvent(new Event('input', {bubbles:true}));}")
        page.keyboard.type(step['value'])
    elif 'press' in step:
        page.keyboard.press(step['press'])
    elif 'scroll' in step:
        page.mouse.wheel(0, step['scroll'])
    elif 'wait' not in step:
        raise ValueError(f'Unknown step: {step}')


def contact_sheet(timeline, out, cols, font_path):
    f = font(20, font_path)
    images = []
    for ms, path in timeline:
        with Image.open(path) as source:
            im = source.convert('RGB')
        im = im.resize((360, max(1, round(im.height * 360 / im.width))))
        draw = ImageDraw.Draw(im)
        draw.rectangle((0, 0, 116, 30), fill='white')
        draw.text((6, 4), f'+{ms}ms', font=f, fill='black')
        images.append(im)
    height = images[0].height
    sheet = Image.new('RGB', (cols * 360, math.ceil(len(images) / cols) * height), '#d9d9d9')
    for i, im in enumerate(images):
        sheet.paste(im, ((i % cols) * 360, (i // cols) * height))
    sheet.save(out)


def estimate_motion(timeline):
    changes = []
    previous = None
    for ms, path in timeline:
        with Image.open(path) as source:
            im = source.convert('L')
        im = im.resize((400, max(1, round(im.height * 400 / im.width))))
        if previous is not None:
            difference = ImageChops.difference(im, previous[1]).point(lambda value: 255 if value > 6 else 0)
            fraction = ImageStat.Stat(difference).mean[0] / 255
            changes.append({'from_ms': previous[0], 'to_ms': ms, 'fraction': fraction, 'moving': fraction > 0.0005})
        previous = ms, im
    moving = [item for item in changes if item['moving']]
    start = moving[0]['from_ms'] if moving else None
    end = moving[-1]['to_ms'] if moving else None
    return {'start_ms': start, 'end_ms': end, 'moving_ms': end - start if moving else 0,
            'still_moving': bool(changes and changes[-1]['moving']), 'differences': changes}


def main():
    ap = argparse.ArgumentParser(description='Record a page interaction frame by frame: frames in a step sets how many milliseconds to record; a virtual clock advances JS and document.timeline animations exactly; writes contact sheets, animations.json and motion.json.')
    ap.add_argument('url')
    ap.add_argument('--steps', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--width', type=int, default=1440)
    ap.add_argument('--height', type=int, default=900)
    ap.add_argument('--phone', action='store_true')
    ap.add_argument('--every', type=int, default=40)
    ap.add_argument('--settle', type=int, default=800)
    ap.add_argument('--cols', type=int, default=4)
    ap.add_argument('--font')
    ap.add_argument('--frames', type=int, help='milliseconds to record for action steps that do not set frames')
    a = ap.parse_args()
    if min(a.every, a.cols, a.width, a.height) <= 0 or a.settle < 0 or (a.frames is not None and a.frames < 0):
        ap.error('every and cols must be positive; settle and frames must not be negative')
    font(20, a.font)
    steps = json.loads(Path(a.steps).read_text(encoding='utf-8'))
    out = Path(a.out)
    (out / 'frames').mkdir(parents=True, exist_ok=True)
    animations, motions = [], []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={'width': 375 if a.phone else a.width, 'height': 812 if a.phone else a.height},
                                      device_scale_factor=2 if a.phone else 1, is_mobile=a.phone, has_touch=a.phone)
        context.add_init_script(INIT)
        page = context.new_page()
        page.goto(a.url, wait_until='load')
        page.wait_for_timeout(a.settle)
        installed = False
        for index, step in enumerate(steps, 1):
            frames = step.get('frames', a.frames if any(k in step for k in ('click','hover','fill','press','scroll')) else None)
            if frames is None:
                execute_step(page, step)
                continue
            if frames < 0:
                raise ValueError('frames must not be negative')
            target, center = None, None
            action = next((key for key in ('click','hover','fill') if key in step), None)
            if action:
                target = page.locator(step[action]).filter(visible=True).first
                target.scroll_into_view_if_needed()
                box = target.bounding_box()
                center = (box['x'] + box['width']/2, box['y'] + box['height']/2)
            if not installed:
                page.clock.install()
                installed = True
            pause_ms = page.evaluate('Date.now() + 1000')
            page.clock.pause_at(datetime.fromtimestamp(pause_ms / 1000, timezone.utc))
            page.evaluate('window.__moment.begin()')
            raw_action(page, step, target, center)
            page.evaluate('window.__moment.paint()')
            times = list(range(0, frames + 1, a.every))
            if times[-1] != frames:
                times.append(frames)
            timeline = []
            previous = 0
            for ms in times:
                if ms:
                    page.clock.run_for(ms - previous)
                page.evaluate('window.__moment.paint()')
                page.evaluate('(t) => window.__moment.seek(t)', ms)
                path = out / 'frames' / f'{index:02d}-{ms:06d}.png'
                page.screenshot(path=str(path))
                timeline.append((ms, path))
                previous = ms
            records = page.evaluate('window.__moment.end()')
            for record in records:
                record.update(step=index, step_name=step.get('name'))
            animations.extend(records)
            page.clock.resume()
            page.wait_for_timeout(300)
            contact_sheet(timeline, out / f'contact-{index:02d}.png', a.cols, a.font)
            motion = estimate_motion(timeline)
            motion.update(step=index, name=step.get('name'), frames=len(timeline))
            motions.append(motion)
            long_animations = [r for r in records if isinstance(r['duration'], (int, float)) and r['duration'] > 500 and r['iterations'] != 'Infinity']
            print(f"Step {index} {step.get('name', '')}: {len(timeline)} frames, {len(records)} animations, picture moved for {motion['moving_ms']}ms, {len(long_animations)} non-looping animations over 500ms", flush=True)
            if motion['still_moving']:
                print('  Still moving in the last frame: frames is too short.', flush=True)
            for record in long_animations:
                print(' ', json.dumps(record, ensure_ascii=False))
        context.close()
        browser.close()
    (out / 'animations.json').write_text(json.dumps(animations, ensure_ascii=False, indent=2), encoding='utf-8')
    (out / 'motion.json').write_text(json.dumps(motions, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
