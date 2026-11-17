import argparse
import json
import os
import re
from datetime import datetime
from playwright.sync_api import sync_playwright

JS = r"""
({minFont}) => {
  const vw = document.documentElement.clientWidth;
  const out = {overflowX: document.documentElement.scrollWidth > vw + 1,
               scrollWidth: document.documentElement.scrollWidth, viewport: vw,
               offscreen: [], clipped: [], smallTargets: [], smallVisible: [], smallText: [], truncated: [], brokenImages: []};
  const label = el => {
    const t = (el.innerText || el.getAttribute('aria-label') || el.alt || '').trim().slice(0, 40);
    return el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') +
      (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/).slice(0,2).join('.') : '') +
      (t ? ' "' + t + '"' : '');
  };
  // skip what nobody can see: elements under a zero-opacity ancestor (labels faded out of frame) and 1px screen-reader-only text
  const visible = el => { const r = el.getBoundingClientRect();
    return r.width > 1 && r.height > 1 && el.checkVisibility({checkOpacity: true, checkVisibilityCSS: true}); };
  // each shadow layer reaches out blur + spread ± offset on each side; inset and fully transparent shadows do not count
  const shadowPad = sh => {
    const pad = {l: 0, t: 0, r: 0, b: 0};
    if (!sh || sh === 'none') return pad;
    for (const layer of sh.split(/,(?![^(]*\))/)) {
      if (/inset/.test(layer)) continue;
      const color = layer.match(/rgba?\([^)]*\)/);
      if (color && /rgba\([^)]*,\s*0\)$/.test(color[0])) continue;
      const [x = 0, y = 0, blur = 0, spread = 0] = (layer.replace(/rgba?\([^)]*\)/, '').match(/-?\d+(\.\d+)?px/g) || []).map(parseFloat);
      pad.l = Math.max(pad.l, blur + spread - x); pad.r = Math.max(pad.r, blur + spread + x);
      pad.t = Math.max(pad.t, blur + spread - y); pad.b = Math.max(pad.b, blur + spread + y);
    }
    return pad;
  };
  // hit area: the element plus absolutely positioned ::before / ::after (a common way to enlarge tap targets)
  const hitBox = (el, r) => {
    let w = r.width, h = r.height;
    if (getComputedStyle(el).position === 'static') return {w, h};
    for (const p of ['::before', '::after']) {
      const ps = getComputedStyle(el, p);
      if (ps.content === 'none' || ps.content === 'normal' || ps.position !== 'absolute' || ps.pointerEvents === 'none') continue;
      const v = k => ps[k] === 'auto' ? null : parseFloat(ps[k]);
      const pw = v('left') !== null && v('right') !== null ? r.width - v('left') - v('right') : parseFloat(ps.width) || 0;
      const ph = v('top') !== null && v('bottom') !== null ? r.height - v('top') - v('bottom') : parseFloat(ps.height) || 0;
      w = Math.max(w, pw); h = Math.max(h, ph);
    }
    return {w, h};
  };
  const all = [...document.querySelectorAll('body *')].filter(visible);
  for (const el of all) {
    const r = el.getBoundingClientRect();
    let fixed = false;
    for (let q = el; q; q = q.parentElement) if (getComputedStyle(q).position === 'fixed') fixed = true;
    if (r.right > vw + 1 && !fixed) {
      // marquee and carousel items clipped by an ancestor's overflow are hidden on purpose, skip them
      let clippedByAncestor = false, q = el.parentElement;
      while (q && q !== document.body) {
        const qs = getComputedStyle(q);
        if (qs.overflowX !== 'visible' || qs.overflow !== 'visible') { clippedByAncestor = true; break; }
        q = q.parentElement;
      }
      if (!clippedByAncestor) out.offscreen.push({el: label(el), right: Math.round(r.right)});
    }
    const s = getComputedStyle(el);
    // outline and shadow extent
    const pad = shadowPad(s.boxShadow);
    if (s.outlineStyle !== 'none') {
      const o = parseFloat(s.outlineWidth) + parseFloat(s.outlineOffset || 0);
      for (const k of ['l', 't', 'r', 'b']) pad[k] = Math.max(pad[k], o);
    }
    const anyPad = Math.max(pad.l, pad.t, pad.r, pad.b) > 0;
    if (anyPad || parseFloat(s.borderTopWidth) > 0) {
      let p = el.parentElement;
      while (p && p !== document.body) {
        const ps = getComputedStyle(p);
        if (ps.overflow !== 'visible' || ps.overflowX !== 'visible' || ps.overflowY !== 'visible') {
          const pr = p.getBoundingClientRect();
          // over: how many pixels the worst side sticks out of the clip box, to judge whether it is visible
          const over = Math.max(pr.left - (r.left - pad.l), (r.right + pad.r) - pr.right, pr.top - (r.top - pad.t), (r.bottom + pad.b) - pr.bottom);
          if (over > 0.5) {
            // content in scroll containers overflows by design; only report what looks sliced at the edge
            const inScroller = /auto|scroll/.test(ps.overflow + ps.overflowX + ps.overflowY);
            // kind: box when the element itself crosses the edge (intentionally cropped images too), shadow when only its outline or shadow does
            const boxOut = r.left < pr.left - 0.5 || r.right > pr.right + 0.5 || r.top < pr.top - 0.5 || r.bottom > pr.bottom + 0.5;
            if (!inScroller || anyPad) out.clipped.push({el: label(el), by: label(p), over: Math.round(over), kind: boxOut ? 'box' : 'shadow'});
          }
          break;
        }
        p = p.parentElement;
      }
    }
    const clickable = el.matches('a[href],button,input:not([type=hidden]),select,textarea,[role=button],[onclick],[tabindex]:not([tabindex="-1"])');
    // hit area (incl. pseudo-elements) under 44 goes to smallTargets; visible size under 44 with a big enough hit area goes to smallVisible (watch this one on scaled canvases)
    if (vw < 768 && clickable && (r.width < 44 || r.height < 44)) {
      const hit = hitBox(el, r);
      const item = {el: label(el), w: Math.round(r.width), h: Math.round(r.height), hitW: Math.round(hit.w), hitH: Math.round(hit.h)};
      (hit.w < 44 || hit.h < 44 ? out.smallTargets : out.smallVisible).push(item);
    }
    // rendered font size: CSS size times ancestor transform scale (scaled canvases and demo frames look big in CSS but tiny on screen)
    if (minFont > 0 && [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) && el.offsetHeight > 0) {
      const px = parseFloat(s.fontSize) * r.height / el.offsetHeight;
      if (px < minFont) out.smallText.push({el: label(el), px: Math.round(px * 10) / 10});
    }
    if ((s.overflow !== 'visible' || s.textOverflow === 'ellipsis') && el.scrollWidth > el.clientWidth + 1 && el.children.length === 0 && el.innerText)
      out.truncated.push({el: label(el)});
  }
  for (const img of document.images) if (img.complete && img.naturalWidth === 0 && visible(img)) out.brokenImages.push(img.currentSrc || img.src);
  out.smallText.sort((a, b) => a.px - b.px);
  for (const k of ['offscreen','clipped','smallTargets','smallVisible','smallText','truncated']) out[k] = out[k].slice(0, 40);
  return out;
}
"""

ANALYTICS = re.compile(r'google-analytics|googletagmanager|/g/collect|/ga/|doubleclick|segment\.io|hotjar|plausible|clarity\.ms|facebook\.net', re.I)

KEEP_HEADINGS = r"""
({keep, maxLines}) => {
  const vw = document.documentElement.clientWidth, vh = document.documentElement.clientHeight;
  const visible = el => {
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0 && el.checkVisibility({checkOpacity: true, checkVisibilityCSS: true});
  };
  const label = el => el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') +
    (typeof el.className === 'string' && el.className.trim() ? '.' + el.className.trim().split(/\s+/).slice(0,2).join('.') : '');
  // line count: group text fragments by vertical position, within half a line height counts as one line (works for per-letter inline-block headings too)
  const headings = [...document.querySelectorAll('h1,h2')].filter(visible).map(el => {
    const s = getComputedStyle(el);
    const lh = s.lineHeight === 'normal' ? parseFloat(s.fontSize) * 1.2 : parseFloat(s.lineHeight);
    const range = document.createRange(); range.selectNodeContents(el);
    const mids = [...range.getClientRects()].filter(r => r.width && r.height).map(r => r.top + r.height / 2).sort((a, b) => a - b);
    let lines = 0, last = -Infinity;
    for (const m of mids) if (m - last > lh / 2) { lines++; last = m; }
    return {tag: el.tagName.toLowerCase(), text: el.innerText.trim().slice(0,40), lines};
  });
  const results = keep.map(({name, selector}) => {
    const el = [...document.querySelectorAll(selector)].find(visible);
    if (!el) return {name, selector, top: null, bottom: null, height: vh, keepMissing: true, notInFirstScreen: false, keepCovered: []};
    const r = el.getBoundingClientRect();
    const points = [[r.x+r.width/2,r.y+r.height/2],[r.left+1,r.top+1],[r.right-1,r.top+1],[r.left+1,r.bottom-1],[r.right-1,r.bottom-1]];
    const covers = [];
    for (const [x,y] of points) {
      if (x < 0 || x >= vw || y < 0 || y >= vh) continue;
      let hit = document.elementFromPoint(x,y);
      // when a fixed or sticky overlay covers it, report the outermost overlay (cookie banner, bottom bar), not a small element inside it
      for (let q = hit; q && q !== document.body; q = q.parentElement) if (/fixed|sticky/.test(getComputedStyle(q).position)) hit = q;
      // hitting the element's own ancestor means the corner is outside a rounded edge, not covered; children of one overlay are reported once as that overlay
      if (!hit || hit === el || el.contains(hit) || hit.contains(el)) continue;
      const i = covers.findIndex(c => c.el.contains(hit) || hit.contains(c.el));
      if (i < 0) covers.push({el: hit, x, y});
      else if (hit.contains(covers[i].el)) covers[i].el = hit;
    }
    return {name, selector, top: r.top, bottom: r.bottom, height: vh,
      keepMissing: false, notInFirstScreen: r.bottom > vh || r.top < 0, keepCovered: covers.map(c => ({by: label(c.el), x: c.x, y: c.y}))};
  });
  return {headings, keep: results, h1TooManyLines: maxLines > 0 ? headings.filter(h => h.tag === 'h1' && h.lines > maxLines) : []};
}
"""


def context_options(width, height=900, phone_height=812):
    mobile = width < 768
    return dict(viewport={'width': width, 'height': phone_height if mobile else height},
                device_scale_factor=2 if mobile else 1, is_mobile=mobile, has_touch=mobile)


def execute_step(page, step):
    if 'click' in step:
        page.locator(step['click']).filter(visible=True).first.click()
    elif 'hover' in step:
        page.locator(step['hover']).filter(visible=True).first.hover()
    elif 'fill' in step:
        page.locator(step['fill']).filter(visible=True).first.fill(step['value'])
    elif 'press' in step:
        page.keyboard.press(step['press'])
    elif 'scroll' in step:
        page.mouse.wheel(0, step['scroll'])
    elif 'js' in step:
        page.evaluate(step['js'])
    elif 'wait' in step:
        page.wait_for_timeout(step['wait'])
    elif 'wait_for' in step:
        page.wait_for_selector(step['wait_for'], timeout=step.get('timeout', 20000))
    else:
        raise ValueError(f'Unknown step: {step}')


def check_page(page, keep=None, max_h1_lines=2, min_font=12):
    result = page.evaluate(JS, {'minFont': min_font})
    result.update(page.evaluate(KEEP_HEADINGS, {'keep': keep or [], 'maxLines': max_h1_lines}))
    return result


def main():
    ap = argparse.ArgumentParser(description='Full-page and per-screen screenshots at several widths; checks layout, whether key elements are in the first screen, heading line counts and states after interactions.')
    ap.add_argument('urls', nargs='*')
    ap.add_argument('--widths', default='375,768,1024,1280,1440')
    ap.add_argument('--height', type=int, default=900)
    ap.add_argument('--phone-height', type=int, default=812)
    ap.add_argument('--settle', type=int, default=800)
    ap.add_argument('--out', default='check-out')
    ap.add_argument('--slices', type=int, default=0)
    ap.add_argument('--forbid', default='', help='comma-separated strings that must not appear on the page')
    ap.add_argument('--keep', action='append', default=[], metavar='name=selector')
    ap.add_argument('--max-h1-lines', type=int, default=2)
    ap.add_argument('--states', help='JSON array of states, each with name, url, steps')
    ap.add_argument('--min-font', type=float, default=12, help='report smallText when the rendered font size is below this many pixels (report only, does not fail); 0 turns it off')
    ap.add_argument('--clock', type=datetime.fromisoformat, help='freeze the page clock at this local time (e.g. 2026-11-09T12:30) so greetings, opening hours and dates that change with the clock give the same screenshots and coordinates every run')
    a = ap.parse_args()
    widths = [int(x) for x in a.widths.split(',')]
    if not widths or min(widths) <= 0 or min(a.height, a.phone_height) <= 0 or min(a.settle, a.slices, a.max_h1_lines) < 0:
        ap.error('widths and heights must be positive; settle, slices and max-h1-lines must not be negative')
    states = json.load(open(a.states, encoding='utf-8')) if a.states else []
    if not a.urls and not states:
        ap.error('give URLs or --states')
    keep = []
    for item in a.keep:
        if '=' not in item:
            ap.error('--keep needs name=selector')
        name, selector = item.split('=', 1)
        if not name or not selector:
            ap.error('--keep name and selector must not be empty')
        keep.append(dict(name=name, selector=selector))
    os.makedirs(a.out, exist_ok=True)
    report = []
    cases = [(url, None, []) for url in a.urls] + [(s['url'], s['name'], s['steps']) for s in states]
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for w in widths:
            for index, (url, state, steps) in enumerate(cases, 1):
                ctx = browser.new_context(**context_options(w, a.height, a.phone_height))
                page = ctx.new_page()
                if a.clock:
                    page.clock.set_fixed_time(a.clock)
                errors, failed = [], []
                page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
                page.on('pageerror', lambda e: errors.append(str(e)))
                def on_failed(request):
                    if request.resource_type in ('document', 'script', 'stylesheet', 'image', 'font', 'media') and not ANALYTICS.search(request.url):
                        failed.append(request.url)
                page.on('requestfailed', on_failed)
                page.goto(url, wait_until='load')
                page.wait_for_timeout(a.settle)
                for step in steps:
                    execute_step(page, step)
                r = check_page(page, keep, a.max_h1_lines, a.min_font)
                r['forbidden'] = [x for x in a.forbid.split(',') if x and x in page.inner_text('body')]
                slug = re.sub(r'[^a-zA-Z0-9]+', '-', url.split('://')[-1]).strip('-')[:60] or 'page'
                state_slug = re.sub(r'[^\w-]+', '-', state or '', flags=re.UNICODE)
                slug += f'-{index}' + (f'-{state_slug}' if state else '')
                shot = os.path.join(a.out, f'{slug}-{w}.png')
                page.screenshot(path=shot, full_page=True)
                if a.slices:
                    height = page.viewport_size['height']
                    total = page.evaluate('document.documentElement.scrollHeight')
                    for i in range(min(a.slices, -(-total // height))):
                        page.evaluate('(y) => window.scrollTo(0,y)', i * height)
                        page.wait_for_timeout(a.settle)
                        page.screenshot(path=os.path.join(a.out, f'{slug}-{w}-screen{i+1:02d}.png'))
                r.update(url=url, width=w, state=state, screenshot=shot, consoleErrors=errors[:20], failedRequests=failed[:20])
                r['pass'] = not any(r[k] for k in ('overflowX','offscreen','clipped','truncated','brokenImages','forbidden','consoleErrors','failedRequests','h1TooManyLines')) and not any(k['keepMissing'] or k['notInFirstScreen'] or k['keepCovered'] for k in r['keep'])
                report.append(r)
                ctx.close()
        browser.close()
    path = os.path.join(a.out, 'report.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    for r in report:
        flags = [k for k in ('overflowX','offscreen','clipped','smallTargets','smallVisible','smallText','truncated','brokenImages','forbidden','consoleErrors','failedRequests','h1TooManyLines') if r.get(k)]
        flags += [k for k in ('keepMissing','notInFirstScreen','keepCovered') if any(x[k] for x in r['keep'])]
        small = f" smallest text {r['smallText'][0]['px']}px" if r.get('smallText') else ''
        print(f"{'PASS' if r['pass'] else 'FAIL'} {r['width']:>5} {r['url']} state: {r['state']} {' '.join(flags)}{small}")
    if keep:
        print('\nKey elements in the first screen')
        print('width | url / state | element | y range | screen height | result')
        for r in report:
            for k in r['keep']:
                bounds = 'not found' if k['keepMissing'] else f"{k['top']:.1f} to {k['bottom']:.1f}"
                status = ', '.join(key for key in ('keepMissing','notInFirstScreen','keepCovered') if k[key]) or 'OK'
                print(f"{r['width']} | {r['url']} / {r['state']} | {k['name']} | {bounds} | {k['height']} | {status}")
                for cover in k['keepCovered']:
                    print(f"  covered by: {cover['by']}")
    print('report:', path)


if __name__ == '__main__':
    main()

