---
name: dosbox
description: Launch, configure, and troubleshoot DOSBox-X first, with fallback to classic DOSBox, for DOS games and software. Use when working with classic DOS programs, mounting folders or ISO/CD images, generating launch commands, auto-generating reusable .conf files, fixing sound/input/fullscreen issues, editing dosbox config files, or preparing a shareable setup for old games and abandonware.
---

# DOSBox

Use this skill to get a DOS program running with the least drama possible.

Prefer **DOSBox-X** when available. Fall back to classic **DOSBox** only when DOSBox-X is missing or the user explicitly wants stock DOSBox behavior.

## Quick approach

1. Detect available emulators with `scripts/resolve_dosbox.py`.
2. Prefer **DOSBox-X** for:
   - ISO/CD-heavy installs
   - awkward installers
   - hardware and config edge cases
   - reusable setups that should be easier to tweak later
3. Identify what the user has:
   - a game/app folder
   - a floppy/ISO/CD image
   - an installer
   - an existing config file
4. Build a reproducible launch command or config instead of relying on vague manual steps.
5. If the program fails, troubleshoot in this order:
   - wrong mount / wrong drive letter
   - wrong startup executable
   - graphics/output mode
   - sound setup
   - CPU cycles / speed sensitivity
   - input or fullscreen settings

## Core workflows

### Launch a DOS app from a folder

Prefer mounting the containing folder as `C:`.

Typical command pattern:

```powershell
<dosbox-binary> -c "mount c <path-to-folder>" -c "c:" -c "dir" -c "<program.exe>"
```

Rules:
- Quote Windows paths carefully.
- Mount the parent folder that contains the DOS files.
- If the executable is unknown, inspect with `dir` first.
- If there is a setup utility (`SETUP.EXE`, `INSTALL.EXE`), run that before the main game when sound/video must be configured.

### Launch from CD / ISO media

Prefer DOSBox-X for image handling.

Typical pattern:

```powershell
<dosbox-binary> -c "imgmount d <image-file> -t iso" -c "d:" -c "dir"
```

If the game needs both a writable hard drive and CD:

```powershell
<dosbox-binary> -c "mount c <game-or-install-folder>" -c "imgmount d <image-file> -t iso" -c "c:"
```

### Install a DOS game

Use a dedicated writable game folder.

Recommended flow:
1. Create a clean install directory.
2. Mount it as `C:`.
3. Mount install media as `D:` if needed.
4. Run `INSTALL`, `SETUP`, or vendor-specific installer.
5. After install, create a reusable launch command or config file.

### Generate a reusable config file

Prefer a config file when the user wants a stable, repeatable setup.

Use `scripts/make_dosbox_conf.py` to generate a starter `.conf` file with:
- detected emulator path
- mount commands
- optional ISO mounting
- optional auto-run executable
- sensible defaults for fullscreen, output, cycles, and Sound Blaster

Examples:

```powershell
python scripts/make_dosbox_conf.py --game-path "C:\Games\DOOM" --exe DOOM.EXE --conf "C:\Games\DOOM\doom.conf"
python scripts/make_dosbox_conf.py --game-path "C:\Games\Install" --iso "C:\Images\GAME.iso" --exe INSTALL.EXE --conf "C:\Games\Install\install.conf"
```

Inspect the generated file before claiming it is final; some games need renderer, cycles, or audio tweaks.

### Use an existing config file

If a config already exists, inspect it before changing anything.

Typical launch forms:

```powershell
<dosbox-binary> -conf <config-file>
```

or:

```powershell
<dosbox-binary> -userconf
```

Only edit config values that solve the current problem. Avoid broad random tweaks.

## Troubleshooting checklist

### Program does not start

Check:
- mounted the correct folder
- using the correct drive letter
- executable name is correct
- files are not nested one level deeper than expected
- the program expects to be started from its own directory

Useful in-emulator commands:

```text
mount
c:
dir
cd <subdir>
```

### "This program requires MSCDEX/CD-ROM"

Mount optical media properly:

```powershell
imgmount d <image-file> -t iso
```

If using a host folder as a CD source, prefer DOSBox-X when possible and ensure the game really supports folder-based installation.

### Sound does not work

Run the game's setup program first.

Common working values for many DOS titles:
- Sound Blaster 16
- Port `220`
- IRQ `7`
- DMA `1`

If the game offers autodetect, still verify what it selected.

### Too fast or too slow

Adjust cycles.

Examples:

```text
cycles auto
cycles max
cycles fixed 12000
```

For old timing-sensitive games, prefer a fixed value and iterate.

### Fullscreen / black screen / renderer issues

Try changing output mode in config:
- `output=opengl`
- `output=texture`
- `output=ddraw`
- `output=surface`

Prefer changing one setting at a time.

### Keyboard / mouse problems

Check:
- whether mouse capture is active
- whether the game expects keyboard-only input
- whether key layout issues come from host locale differences

## Command generation rules

When writing commands for the user or a script:
- Prefer a single launch command with chained `-c` directives for quick tests.
- Prefer a config file for repeatable setups.
- Use absolute paths on Windows.
- Do not assume DOSBox is on PATH; detect common executable names or ask for the install path.
- If both DOSBox and DOSBox-X exist, prefer DOSBox-X for ISO/CD-heavy setups and advanced compatibility.
- If the task is shareable or repeatable, generate a `.conf` file and keep commands in `[autoexec]`.

## ClawHub publishing notes

This skill is meant to be portable.
- Do not hardcode one machine's install path as a requirement.
- Treat DOSBox-X as preferred, not mandatory.
- Use helper scripts to detect executables and generate commands/configs.
- Keep claims conservative: the generated config is a good starting point, not a guaranteed universal fix.

## Bundled resources

### scripts/resolve_dosbox.py

Use this helper to detect likely DOSBox executables and emit example commands for folder or ISO launches.

Example:

```powershell
python scripts/resolve_dosbox.py --game-path "C:\Games\DOOM"
python scripts/resolve_dosbox.py --game-path "C:\Games\Install" --iso "C:\Images\GAME.iso"
```

### scripts/make_dosbox_conf.py

Use this helper to generate a reusable `.conf` file for DOSBox-X or DOSBox.

### references/troubleshooting.md

Read this when the task is mainly diagnosis rather than simple launching.
