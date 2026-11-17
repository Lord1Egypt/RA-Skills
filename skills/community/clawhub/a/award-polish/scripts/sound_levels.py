import argparse
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

from layout_check import context_options, execute_step

# Sound evidence for reviewers: they cannot hear anything in a headless browser and will judge "no audio feedback" from screenshots alone.
# This script taps the WebAudio output with a level probe (injected only into the test browser, the site code is untouched),
# runs a steps file and records the peak level during each step (0 silent, 1 full scale), plus which files <audio>/<video> played.
# The steps file is a JSON array, one action per item with a label and an optional listen (ms to listen after the step, default 700):
#   {"label": "press start", "click": "#start"} / {"fill": "#name", "value": "Kiki"} / {"press": "Enter"}
#   {"js": "localStorage.setItem('mute','1')"} / {"wait_for": "#result"} / {"wait": 500} (these two only wait and are not measured)
# Usage: python3 sound_levels.py <url> --steps steps.json --out levels.json [--phone] [--fake-mic]
PROBE = """
(() => {
  const orig = AudioNode.prototype.connect;
  window.__peak = 0; window.__media = [];
  AudioNode.prototype.connect = function (dest, ...rest) {
    const r = orig.call(this, dest, ...rest);
    if (dest instanceof AudioDestinationNode && !this.__probed) {
      this.__probed = true;
      const an = this.context.createAnalyser(), mute = this.context.createGain();
      an.fftSize = 2048; mute.gain.value = 0;
      orig.call(this, an); orig.call(an, mute); orig.call(mute, this.context.destination);
      const buf = new Float32Array(an.fftSize);
      setInterval(() => { an.getFloatTimeDomainData(buf); for (const v of buf) window.__peak = Math.max(window.__peak, Math.abs(v)); }, 15);
    }
    return r;
  };
  const play = HTMLMediaElement.prototype.play;
  HTMLMediaElement.prototype.play = function () { window.__media.push(this.currentSrc || this.src); return play.call(this); };
})();
"""


def main():
    ap = argparse.ArgumentParser(description='Run steps on a page and record the peak audio level and media playback of each step.')
    ap.add_argument('url')
    ap.add_argument('--steps', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--phone', action='store_true', help='use a 375x812 phone viewport')
    ap.add_argument('--fake-mic', action='store_true', help='give the browser a fake microphone with permission granted (for "speak into the mic" features)')
    ap.add_argument('--settle', type=int, default=1000)
    a = ap.parse_args()
    steps = json.loads(Path(a.steps).read_text(encoding='utf-8'))
    args = ['--autoplay-policy=no-user-gesture-required']
    if a.fake_mic:
        args += ['--use-fake-device-for-media-stream', '--use-fake-ui-for-media-stream']
    rows, errors = [], []
    with sync_playwright() as p:
        browser = p.chromium.launch(args=args)
        ctx = browser.new_context(**context_options(375 if a.phone else 1440))
        if a.fake_mic:
            ctx.grant_permissions(['microphone'], origin='/'.join(a.url.split('/')[:3]))
        page = ctx.new_page()
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
        page.add_init_script(PROBE)
        page.goto(a.url, wait_until='load')
        page.wait_for_timeout(a.settle)
        for step in steps:
            if 'wait_for' in step or 'wait' in step:
                execute_step(page, step)
                continue
            page.evaluate('window.__peak = 0; window.__media = []')
            execute_step(page, step)
            page.wait_for_timeout(step.get('listen', 700))
            peak, media = page.evaluate('[window.__peak, window.__media]')
            row = {'label': step.get('label') or json.dumps(step, ensure_ascii=False), 'peak': round(peak, 3), 'media': media}
            rows.append(row)
            print(f"{row['label']}: level {row['peak']:.3f}" + (f"  media {', '.join(media)}" if media else ''))
        browser.close()
    Path(a.out).write_text(json.dumps({'url': a.url, 'steps': rows, 'errors': errors}, ensure_ascii=False, indent=2), encoding='utf-8')
    silent = [r['label'] for r in rows if r['peak'] < 0.01 and not r['media']]
    print('Silent steps: ' + (', '.join(silent) if silent else 'none'))
    print('errors:', errors)


if __name__ == '__main__':
    main()
