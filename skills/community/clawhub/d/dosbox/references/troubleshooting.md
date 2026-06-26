# DOSBox troubleshooting reference

## Choose the emulator

Prefer **DOSBox-X** when:
- working with ISO/CD images
- dealing with awkward installers
- needing stronger hardware/config flexibility

Plain **DOSBox** is usually enough when:
- launching a simple folder-based game
- the user already has a working config
- you only need a minimal command

## Common executable names to inspect

If startup is unclear, look for:
- `GAME.EXE`
- `START.EXE`
- `PLAY.EXE`
- `RUN.EXE`
- `GO.BAT`
- `SETUP.EXE`
- `INSTALL.EXE`
- `CONFIG.EXE`

Check manuals or included text files if the folder is ambiguous.

## Practical config knobs

### Performance

```ini
[cpu]
core=auto
cputype=auto
cycles=auto
cycleup=500
cycledown=500
```

For unstable timing, switch to a fixed cycle count.

### Display

```ini
[render]
aspect=true
scaler=normal2x

[sdl]
fullscreen=false
output=opengl
```

If `opengl` misbehaves, try `texture`, `ddraw`, or `surface`.

### Sound

```ini
[sblaster]
sbtype=sb16
sbbase=220
irq=7
dma=1
hdma=5
mixer=true
```

Not every game needs all values, but these defaults are often a good baseline.

## Installation pattern

Use a structure like:

```text
C:\DOS\GAME\
C:\DOS\MEDIA\GAME.iso
C:\DOS\CONFIG\game.conf
```

This keeps installed files, media, and configs separate.

## Good agent behavior

- Prefer reproducible commands over generic advice.
- Inspect before editing configs.
- Explain only the settings being changed.
- Avoid claiming a renderer/sound tweak will definitely fix the issue.
- If the emulator is not installed, say so plainly and stop short of inventing paths.
