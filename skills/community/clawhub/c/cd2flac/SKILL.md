---
name: cd2flac
description: |
  Convert CD audio archives (RAR files containing WAV+CUE pairs) into organized
  FLAC files. Handles RAR extraction, CUE-based track splitting, GBK encoding
  fix for Chinese filenames, multi-CD album organization, and auto-fetch synced
  lyrics from Netease Cloud Music (with Kugou fallback). Use whenever someone
  needs to extract and convert CD-quality audio archives (WAV+CUE in RAR/7z/ZIP)
  to per-track FLAC files. Also handles direct WAV+CUE pairs without archives.
---

# CD to FLAC Converter

Tool to extract CD audio from RAR archives and convert WAV+CUE pairs into
individual FLAC tracks with correct names and synced lyrics.

## Requirements

- **System packages**: `unrar`, `cuetools`, `shntool`, `flac`
- Install: `sudo apt-get install -y unrar cuetools shntool flac`

## Python dependencies

- `mutagen` (FLAC tag handling)
- `pycryptodome` (Netease API encryption)
- Install: `pip3 install mutagen pycryptodome`

## Usage

```bash
python3 skills/cd2flac/scripts/cd2flac.py <directory> [options]
```

### Basic — process RAR archives in a directory

```bash
python3 skills/cd2flac/scripts/cd2flac.py "/path/to/albums/"
```

### With synced lyrics (Netease + Kugou)

```bash
python3 skills/cd2flac/scripts/cd2flac.py "/path/to/albums/" --lyrics
```

### Inject lyrics into already converted FLACs (no conversion)

```bash
python3 skills/cd2flac/scripts/cd2flac.py "/path/to/albums/" --lyrics-only
```

### Standalone lyric injector (for any FLAC directory)

```bash
python3 skills/cd2flac/scripts/lyric.py "/path/to/album/"
python3 skills/cd2flac/scripts/lyric.py "/path/to/track.flac"
```

### Dry run — preview without changes

```bash
python3 skills/cd2flac/scripts/cd2flac.py "/path/to/albums/" --dry-run
```

### Keep WAV/CUE, delete RAR after extraction

```bash
python3 skills/cd2flac/scripts/cd2flac.py "/path/" --keep-wav --delete-rar
```

### Process subdirectories recursively

```bash
python3 skills/cd2flac/scripts/cd2flac.py "/path/" --recursive --lyrics
```

### Process already-extracted WAV+CUE pairs (no RAR)

```bash
python3 skills/cd2flac/scripts/cd2flac.py "/path/to/album_with_wav/"
```

## What It Does

1. **Extract**: Unpacks RAR archives in the target directory
2. **Parse CUE**: Reads CUE sheets in GBK/GB18030/UTF-8 encoding, extracts track titles
3. **Split**: Uses `shnsplit` to split each WAV into individual FLAC tracks
4. **Fix names**: Renames garbled tracks (CUE files in Chinese encodings produce mojibake filenames) using correct track titles from the CUE sheet
5. **Organize**: Multi-CD albums get `CD1/`, `CD2/`, etc. subdirectories
6. **Lyrics**: Auto-fetch synced lyrics from Netease Cloud Music (primary) and Kugou (fallback), inject as FLAC LYRICS tag with translation support
7. **Clean up**: Deletes original WAV and CUE files (optional: keep them)

## Lyric Injection

Lyrics are fetched using the same strategy as ESLyric:
- **Primary**: Netease Cloud Music via linuxapi (AES-ECB encryption, no login needed)
- **Fallback**: Kugou Music

Synced LRC is embedded as Vorbis comment `LYRICS` tag. If Netease provides
translation lyrics, they go in `LYRICS_TRANSLATIONS` tag.

## Common Scenarios

### Chinese album with garbled filenames

The script auto-detects and fixes GBK→UTF-8 mojibake in track names by
comparing the actual filename bytes against the CUE sheet's GBK-encoded titles.

### Multi-CD albums

If a directory contains multiple WAV+CUE pairs, they are treated as separate
discs and placed into `CD1/`, `CD2/`, etc. subdirectories.

### Already extracted albums

If the RAR is already extracted but not yet converted, the script detects the
WAV+CUE pairs and processes them directly.

### Add lyrics to an existing FLAC library

```bash
find /path/to/music -name "*.flac" -exec dirname {} \; | sort -u | \
  xargs -I{} python3 skills/cd2flac/scripts/lyric.py "{}"
```
