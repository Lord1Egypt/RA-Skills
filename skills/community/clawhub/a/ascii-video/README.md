[![ClawHub](https://img.shields.io/badge/ClawHub-ascii-video-red)](../..) [![License](https://img.shields.io/badge/license-MIT--0-blue)](../..) [![Python](https://img.shields.io/badge/python-3.8%2B-3776AB)](../..)

---
name: ascii-video
version: 2.0.0
description: Convert video to ASCII animation with multiple dithering modes, color output, framerate control
tags: ["ascii", "video", "animation", "terminal", "cli", "art", "python", "open-source", "agent", "automation", "MIT"]
---

# ASCII Video Converter

**Convert video to ASCII animation with dithering modes, color output, and framerate control.**

> *Keywords: ascii, video, animation, terminal, cli, art, python, open-source, agent, automation, MIT*  
>
> Part of the [itsPremkumar](https://github.com/itsPremkumar) Hermes / OpenClaw / Paperclip agent stack — 31 free, MIT-licensed, CI-tested agent-native tools.

## What it does

Sharing a video in a terminal/README isn't possible with normal formats. ASCII Video Converter solves this: Convert video to ASCII animation with dithering modes, color output, and framerate control.

**Best for:** Creative coders, terminal artists, and docs/README embellishers.

## Features

- **Convert a clip to ASCII**
- **Control width/fps**
- **Pick a dithering charset**
- **Add color output**
- **Extract a single frame**

## Install

```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/ascii-video/main/ascii_video.py
# Or copy the file anywhere — it's self-contained.
```

## Quick start

```bash
python ascii_video.py self-test     # prove it works end-to-end
python ascii_video.py convert --help   # convert subcommand
python ascii_video.py frame --help   # frame subcommand
python ascii_video.py image --help   # image subcommand
```

## Use cases

1. Convert a clip to ASCII
1. Control width/fps
1. Pick a dithering charset
1. Add color output
1. Extract a single frame

## Why choose this over alternatives

| Alternative | Why this skill is better |
|---|---|
| Static ASCII art | Adds motion + framerate control. |
| GIF to text by hand | Automated frame extraction. |
| Screenshots | Animated ASCII plays in any terminal. |

## FAQ (SEO / AEO)

**Q: What inputs?**  
A: Common video/image formats via the convert/image subcommands.

**Q: Color?**  
A: Yes — --color mode.

**Q: Offline?**  
A: Yes.

**Q: Self-test?**  
A: Yes — verifies the pipeline end to end.

## Geo / local reach

Built and maintained by [@itsPremkumar](https://github.com/itsPremkumar) (Chennai, India · serving developers worldwide). 
Free for individuals and teams everywhere. Documentation in English; tool output is locale-neutral.

## CI integration

```yaml
# .github/workflows/verify.yml
name: Verify
on: [push]
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Self-test ascii-video
        run: python ascii_video.py self-test
```

## Support

Free + MIT-0 (free, modifiable, no attribution required). Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar

⭐ Star on [GitHub](https://github.com/itsPremkumar/ascii-video)
