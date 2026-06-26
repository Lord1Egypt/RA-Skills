# Clawtunes Play Install

## Requirements

This skill assumes these local tools are available on macOS:
- `clawtunes`
- `python3`
- `osascript`
- `open`

It also needs macOS Accessibility / Automation permission so `System Events` can send keyboard input to Music.

## Where it lives

Keep the repo in:
- `skills/clawtunes-play`

## Commands

- `clawtunes_play --song "<song>"`
- `catalog_play "<query>"`
- `catalog_play_experiment "<query>" --index 1 --strategy tab-tab-enter`

## Wrapper

Catalog playback uses:
- `scripts/catalog_play_wrapper.sh`

That wrapper resolves repo-relative paths and avoids hardcoded user-specific paths.
