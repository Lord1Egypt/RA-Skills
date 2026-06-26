#!/usr/bin/env python3
"""ASCII Vision — Convert images to ASCII art for visual analysis without vision APIs.

Usage:
  ffmpeg -y -i <img> -vf "scale=W:<height>,format=gray" -frames:v 1 -f rawvideo pipe: \
    | python3 ascii_viewer.py [options]

  For auto-height (ffmpeg scale=W:-1), omit --height; height is detected from data.
  For manual height (ffmpeg scale=W:H), pass --height H.

Options:
  --width W        ASCII width in columns (default: 60)
  --height H       ASCII height in rows; auto-detected from data if omitted
  --chars MAP      Characters from dark to light (default: ' .:-=+*#%@')
  --invert         Reverse the character map (light → dark)
  --stats          Show brightness statistics
  --edges          Edge detection via pixel gradient threshold (requires --stats)

Examples:
  ffmpeg -y -i img.jpg -vf "scale=60:-1,format=gray" -frames:v 1 -f rawvideo pipe: \\
    | python3 ascii_viewer.py

  ffmpeg -y -i img.jpg -vf "scale=80:-1,format=gray" -frames:v 1 -f rawvideo pipe: \\
    | python3 ascii_viewer.py --width 80 --stats --edges
"""
import sys

def main():
    w = 60
    h = None  # auto-detect
    chars = ' .:-=+*#%@'
    show_stats = False
    show_edges = False

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == '--width' and i + 1 < len(args):
            w = int(args[i + 1]); i += 2
        elif args[i] == '--height' and i + 1 < len(args):
            h = int(args[i + 1]); i += 2
        elif args[i] == '--chars' and i + 1 < len(args):
            chars = args[i + 1]; i += 2
        elif args[i] == '--invert':
            chars = chars[::-1]; i += 1
        elif args[i] == '--stats':
            show_stats = True; i += 1
        elif args[i] == '--edges':
            show_edges = True; i += 1
        else:
            i += 1

    data = sys.stdin.buffer.read()

    # Auto-detect height from pixel data when not specified
    if h is None:
        h = len(data) // w
        if len(data) % w != 0:
            # Data doesn't divide evenly; use what we have
            pass

    expected = w * h if h else len(data)
    vals = list(data[:expected])
    n_chars = len(chars)

    # Generate ASCII
    for y in range(h or 0):
        line_chars = []
        for x in range(w):
            idx = y * w + x
            if idx < len(vals):
                v = vals[idx]
                c = chars[min(v * n_chars // 256, n_chars - 1)]
                line_chars.append(c)
        print(''.join(line_chars))

    # Statistics
    if show_stats and vals:
        avg = sum(vals) / len(vals)
        bright = sum(1 for v in vals if v > 180)
        dark = sum(1 for v in vals if v < 60)
        print(f'\n--- Stats (w={w}, h={h}) ---')
        print(f'brightness_avg={avg:.0f}/255')
        print(f'bright_pixels={bright}')
        print(f'dark_pixels={dark}')
        print(f'unique_levels={len(set(vals))}')

        if show_edges:
            edges = sum(
                1 for i in range(1, len(vals))
                if abs(vals[i] - vals[i - 1]) > 40
            )
            print(f'edges_detected={edges}/{len(vals)}')

if __name__ == '__main__':
    main()
