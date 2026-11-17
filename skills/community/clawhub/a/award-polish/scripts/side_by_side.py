import argparse
import platform
import re
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

from layout_check import context_options


def font(size, path=None):
    if path:
        return ImageFont.truetype(path, size)
    candidates = {
        # CJK fonts first so Chinese or Japanese labels render; Latin fonts cover machines without them
        'Darwin': ['/System/Library/Fonts/STHeiti Medium.ttc', '/System/Library/Fonts/Helvetica.ttc'],
        'Linux': ['/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
                  '/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc',
                  '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
                  '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'],
        'Windows': ['C:/Windows/Fonts/msyh.ttc', 'C:/Windows/Fonts/arial.ttf'],
    }.get(platform.system(), [])
    for candidate in candidates:
        if Path(candidate).is_file():
            return ImageFont.truetype(candidate, size)
    raise SystemExit('No usable font found; pass a font file with --font.')


def compose(paths, labels, out, cols=2, width=900, height=1600, font_path=None):
    f, gap, top = font(44, font_path), 24, 80
    rows = []
    for i in range(0, len(paths), cols):
        row = []
        for path in paths[i:i + cols]:
            with Image.open(path) as source:
                im = source.convert('RGB')
            im = im.resize((width, max(1, round(im.height * width / im.width))))
            row.append(im.crop((0, 0, width, min(im.height, height) if height else im.height)))
        rows.append(row)
    total_height = sum(top + max(x.height for x in row) + gap for row in rows)
    canvas = Image.new('RGB', (width * cols + gap * (cols + 1), total_height), (246, 245, 242))
    draw = ImageDraw.Draw(canvas)
    y = 0
    for row in rows:
        for j, im in enumerate(row):
            x = gap + j * (width + gap)
            draw.text((x, y + 16), labels[j], fill=(24, 24, 27), font=f)
            canvas.paste(im, (x, y + top))
        y += top + max(x.height for x in row) + gap
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out)
    return canvas.size


def main():
    ap = argparse.ArgumentParser(description='Stitch images into labelled columns, or screenshot the same pages and widths of several URLs (fresh context each) and stitch them.')
    ap.add_argument('images', nargs='*')
    ap.add_argument('--out', default='compare.png')
    ap.add_argument('--labels', help='comma-separated column labels')
    ap.add_argument('--cols', type=int, default=2, choices=(2, 3))
    ap.add_argument('--width', type=int, default=900, help='width of each column')
    ap.add_argument('--height', type=int, default=1600, help='height kept from each image, 0 keeps the full height')
    ap.add_argument('--font')
    ap.add_argument('--urls', nargs='+', metavar='label=url')
    ap.add_argument('--pages', nargs='+', default=['/'])
    ap.add_argument('--widths', default='1440,375')
    ap.add_argument('--settle', type=int, default=1500)
    ap.add_argument('--dismiss')
    ap.add_argument('--full', action='store_true')
    ap.add_argument('--clock', type=datetime.fromisoformat, help='freeze the page clock at this local time (e.g. 2026-11-09T12:30) when the columns change with the time of day')
    a = ap.parse_args()
    if a.width <= 0 or a.height < 0 or a.settle < 0:
        ap.error('width must be positive; height and settle must not be negative')
    font(28, a.font)
    if a.urls:
        if a.images or len(a.urls) not in (2, 3) or any('=' not in item for item in a.urls):
            ap.error('screenshot mode takes 2 or 3 label=url pairs and no images')
        sites = [item.split('=', 1) for item in a.urls]
        labels = a.labels.split(',') if a.labels else [label for label, _ in sites]
        if len(labels) != len(sites) or any(not label or not base for label, base in sites):
            ap.error('URLs and labels must not be empty; --labels must match the number of URLs')
        out = Path(a.out)
        out.mkdir(parents=True, exist_ok=True)
        shots = out / 'screenshots'
        shots.mkdir(exist_ok=True)
        comparisons = []
        with sync_playwright() as p:
            browser = p.chromium.launch()
            for path in a.pages:
                slug = re.sub(r'[^\w-]+', '-', path.strip('/')).strip('-') or 'home'
                for width in [int(w) for w in a.widths.split(',')]:
                    images = []
                    for index, (_, base) in enumerate(sites, 1):
                        context = browser.new_context(**context_options(width))
                        page = context.new_page()
                        if a.clock:
                            page.clock.set_fixed_time(a.clock)
                        page.goto(base.rstrip('/') + '/' + path.lstrip('/'), wait_until='load')
                        page.wait_for_timeout(a.settle)
                        if a.dismiss:
                            page.locator(a.dismiss).filter(visible=True).first.click()
                            page.wait_for_timeout(a.settle)
                        shot = shots / f'{slug}-{width}-{index}.png'
                        page.screenshot(path=str(shot), full_page=a.full)
                        images.append(shot)
                        context.close()
                    result = out / f'{slug}-{width}.png'
                    compose(images, labels, result, len(sites), a.width, 0 if a.full else a.height, a.font)
                    comparisons.append(result)
            browser.close()
        for result in comparisons:
            print(result)
    else:
        if not a.images or len(a.images) % a.cols:
            ap.error('the number of images must be a multiple of --cols')
        labels = a.labels.split(',') if a.labels else (['Before', 'After'] if a.cols == 2 else ['Version 1', 'Version 2', 'Version 3'])
        if len(labels) != a.cols:
            ap.error('--labels must match --cols')
        print('saved', a.out, compose(a.images, labels, a.out, a.cols, a.width, a.height, a.font))


if __name__ == '__main__':
    main()
