---
name: apple-music-play
description: Play Apple Music songs on macOS using clawtunes, including streaming catalog tracks via a practical keyboard-navigation workaround after opening the song in Music. Use when the user asks to play a song, artist, album, playlist, or mood in Apple Music and normal AppleScript/library playback is not enough. Works with the Mac Apple Music app plus online catalog search/play. Aliases: clawtunes-play.
---

# Clawtunes Play

Use `clawtunes` as the first choice for Apple Music control on this Mac.

## Workflow

1. For library items, try direct playback first.
2. For songs likely not in the library, search the Apple Music catalog and open the selected result in Music.
3. For catalog playback, prefer the wrapper script that tries the best-known keyboard sequence automatically:
   - `Tab` + `Tab` + `Enter`
   - fallback: `Tab` + `Enter`
   - fallback: `Shift-Tab` + `Enter`
4. Check whether playback actually changed to the requested song.
5. If playback did not switch, say so plainly.

## Commands

- Direct library-style play:
  - `clawtunes_play --song "<song>"`
- Catalog play wrapper:
  - `catalog_play "<query>"`
- Status only:
  - `clawtunes_play --status`
- Experimental step-by-step catalog workflow:
  - `catalog_play_experiment "<query>" --index 1 --strategy tab-tab-enter`


## Requirements

This skill assumes these local tools are available on macOS:
- `clawtunes`
- `python3`
- `osascript`
- `open`

It also needs macOS Accessibility / Automation permission so `System Events` can send keyboard input to Music.

## Install / Use

- Keep repo in `skills/clawtunes-play`
- Commands: `clawtunes_play`, `catalog_play`, `catalog_play_experiment`
- For catalog playback, use the wrapper script in `scripts/catalog_play_wrapper.sh`

## Notes

- `clawtunes play song` targets library playback.
- `clawtunes catalog search` opens the streaming result in Music, but Music may not autoplay unless the UI focus lands correctly.
- The current best-known workaround is keyboard navigation after opening the result.
- This is macOS UI-state dependent; it is usable, but not a guaranteed Apple primitive.
