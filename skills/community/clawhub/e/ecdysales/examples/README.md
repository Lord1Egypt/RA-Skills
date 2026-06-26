# Examples

Ready-to-use configs and batch files. Copy any of these to `config/` to use.

## Sticker configs

| File | Mode | Style |
|------|------|-------|
| `sticker-fixed.json` | Fixed | Gold, top-right, 48px — text wraps around price |
| `sticker-reactive.json` | Reactive | Gold, top-right, 20%×12.5% of image — same size regardless of price |
| `sticker-red-bold.json` | Fixed | Red, top-left, 64px white text — sale/promo style |

**Fixed mode** — sticker size depends on the price text. Good for consistent font size.

**Reactive mode** — sticker is always a fixed fraction of the image. Good for uniform look across different prices.

To use: copy to `config/`:
```bash
cp examples/sticker-reactive.json config/sticker-config.json
```

## Batch file

`prices.txt` — one image per line: `<filename> '<price>' [flags]`

Run with:
```bash
./scripts/run.sh --batch ./photos examples/prices.txt
```
