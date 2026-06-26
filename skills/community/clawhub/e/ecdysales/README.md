# Ecdysales Lite 🏷️

Add watermarks, logos, and price stickers to product photos. One command, done.

## Install

```bash
./scripts/setup.sh --install
```

Requires: ImageMagick 6+, `bc`

## Use

```bash
# Process a photo
./scripts/run.sh photo.jpg '$299'

# Latest received image
./scripts/run.sh --latest '$299'

# Skip layers
./scripts/run.sh photo.jpg '$299' --sticker-only
./scripts/run.sh photo.jpg '$299' --no-logo
./scripts/run.sh photo.jpg '$299' --no-watermark

# Batch
./scripts/run.sh --batch ./photos prices.txt
```

⚠️ Use single quotes around prices: `'$299'` not `"$299"`

## Files

```
├── SKILL.md              # AI agent instructions
├── HOWTO.md              # Full documentation
├── POSTMORTEM.md         # Build notes & lessons learned
├── scripts/
│   ├── run.sh            # Entry point
│   ├── make-product.sh   # ImageMagick processor
│   └── setup.sh          # Dependency checker
├── assets/
│   ├── watermark-pattern.png
│   └── logo.png
└── config/
    ├── sticker-config.json
    ├── watermark-config.json
    └── logo-config.json
```

→ Full docs: [HOWTO.md](HOWTO.md)
