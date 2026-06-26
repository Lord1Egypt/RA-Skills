#!/usr/bin/env python3
"""
cd2flac - Convert CD audio archives (RAR/WAV+CUE) into organized FLAC files.

Usage:
    python3 cd2flac.py <directory> [options]

Features:
    - Extract RAR archives containing WAV+CUE pairs
    - Split WAV files into individual FLAC tracks using CUE sheets
    - Handle GBK-encoded CUE files (common for Chinese releases)
    - Organize multi-CD albums into CD1/, CD2/ subdirectories
    - Preserve cover art and metadata files
    - Clean up WAV and CUE after successful conversion

Options:
    --dry-run     Preview what would be done without making changes
    --keep-wav    Keep original WAV files after conversion
    --keep-cue    Keep CUE files after conversion
    --keep-rar    Keep RAR archives after extraction (default: keep)
    --threads N   Number of parallel conversions (default: 1)
"""

import os
import subprocess
import sys
import shutil
import re
import argparse
import tempfile
from pathlib import Path

# Optional: lyric injection
_lyric_module = None
def _get_lyric_module():
    global _lyric_module
    if _lyric_module is None:
        try:
            from scripts import lyric as _lyric_module
        except ImportError:
            try:
                import lyric as _lyric_module
            except ImportError:
                _lyric_module = False
    return _lyric_module if _lyric_module else None


def run_cmd(cmd, cwd=None, timeout=7200, capture=True):
    """Run a command, return (returncode, stdout, stderr)."""
    kwargs = dict(cwd=cwd, timeout=timeout)
    if capture:
        kwargs.update(stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        kwargs.update(stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        result = subprocess.run(cmd, **kwargs)
    except subprocess.TimeoutExpired:
        return -1, "", "TIMEOUT"
    if capture:
        out = result.stdout.decode('utf-8', 'replace').strip()
        err = result.stderr.decode('utf-8', 'replace').strip()
    else:
        out, err = "", ""
    return result.returncode, out, err


def has_tool(name):
    """Check if a system tool is available."""
    return shutil.which(name) is not None


def check_dependencies():
    """Verify all required tools are installed."""
    required = {'unrar': 'unrar', 'shnsplit': 'shntool',
                'cuebreakpoints': 'cuetools', 'flac': 'flac'}
    missing = []
    for cmd, pkg in required.items():
        if not has_tool(cmd):
            missing.append(f"{cmd} (install: sudo apt install {pkg})")
    if missing:
        print("❌ Missing dependencies:")
        for m in missing:
            print(f"   {m}")
        print("\nInstall them with:")
        print("   sudo apt-get install -y unrar cuetools shntool flac")
        return False
    return True


def safe_filename(s):
    """Clean a string for use as a filename."""
    replacements = {
        '/': '／', '\\': '＼', ':': '：', '"': "'",
        '?': '？', '*': '＊', '<': '＜', '>': '＞',
        '|': '｜', '\n': ' ', '\r': '',
    }
    for old, new in replacements.items():
        s = s.replace(old, new)
    return s.strip()


def get_rar_files(directory):
    """Get sorted list of RAR files in directory."""
    return sorted([f for f in os.listdir(directory)
                   if f.endswith('.rar') and os.path.isfile(os.path.join(directory, f))])


def find_wav_cue_pairs(directory):
    """Find all WAV+CUE pairs in directory tree. Returns [(wav_path, cue_path)]. """
    pairs = []
    for root, dirs, files in os.walk(directory):
        # Skip [原始文件] and CD subdirectories - they don't have WAV
        dirs[:] = [d for d in dirs if d not in ('[原始文件]', 'CD1', 'CD2', 'CD3')]
        wavs = {}
        cues = {}
        for f in files:
            if f.lower().endswith('.wav'):
                base = os.path.splitext(f)[0]
                wavs[base] = os.path.join(root, f)
            elif f.lower().endswith('.cue'):
                base = os.path.splitext(f)[0]
                cues[base] = os.path.join(root, f)
        for base in wavs:
            if base in cues:
                pairs.append((wavs[base], cues[base]))
            else:
                print(f"  ⚠️  WAV without matching CUE: {os.path.basename(wavs[base])}")
    return pairs


def read_cue_text(cue_path):
    """Read CUE file, trying multiple encodings. Returns text."""
    with open(cue_path, 'rb') as f:
        raw = f.read()
    for enc in ('gbk', 'gb18030', 'utf-8', 'latin-1'):
        try:
            return raw.decode(enc)
        except (UnicodeDecodeError, UnicodeError):
            continue
    return raw.decode('utf-8', 'replace')


def parse_cue_tracks(cue_text):
    """Parse CUE text, return list of (track_number, title) in order."""
    tracks = []
    cur_track = None
    for line in cue_text.split('\n'):
        m = re.search(r'TRACK\s+(\d+)\s+AUDIO', line, re.IGNORECASE)
        if m:
            cur_track = int(m.group(1))
            continue
        m = re.search(r'TITLE\s+"(.+)"', line)
        if m and cur_track is not None:
            tracks.append((cur_track, m.group(1)))
    return tracks


def count_cds(tracks_list):
    """Determine number of CDs from track list (detect repeated track 01)."""
    count = 0
    for tn, title in tracks_list:
        if tn == 1:
            count += 1
    return max(count, 1)


def get_multi_cd_groups(tracks_list, num_cds):
    """Split track list into per-CD groups."""
    groups = []
    current = []
    for tn, title in tracks_list:
        if tn == 1 and current:
            groups.append(current)
            current = []
        current.append((tn, title))
    if current:
        groups.append(current)
    # Pad to expected count
    while len(groups) < num_cds:
        groups.append([])
    return groups


def extract_rar(directory, rar_name, dry_run=False):
    """Extract a RAR file into the directory. Returns True on success."""
    rar_path = os.path.join(directory, rar_name)
    dir_name = os.path.splitext(rar_name)[0]
    target = os.path.join(directory, dir_name)

    if os.path.isdir(target):
        existing_flacs = len([f for r, d, files in os.walk(target)
                              for f in files if f.endswith('.flac')])
        if existing_flacs > 0:
            print(f"  ℹ️  Already has {existing_flacs} FLACs, skipping extraction")
            return True

    print(f"  🔓 Extracting {rar_name}...")
    if dry_run:
        return True
    rc, out, err = run_cmd(["unrar", "x", "-y", rar_path], cwd=directory, capture=False)
    if rc not in (0, 1):
        print(f"  ❌ Extraction failed (rc={rc})")
        return False
    print(f"  ✅ Extracted")
    return True


def extract_rar_cue_contents(directory, rar_name):
    """Get all CUE file contents from a RAR archive, decoded as GBK."""
    rar_path = os.path.join(directory, rar_name)
    rc, out, err = run_cmd(["unrar", "p", rar_path, "*.cue"], cwd=directory, timeout=60)
    if rc not in (0, 1):
        return None
    for enc in ('gbk', 'gb18030'):
        try:
            return out.encode('latin-1').decode(enc) if isinstance(out, str) else out
        except:
            pass
    return out


def process_single_cd(wav_path, cue_path, output_dir, dry_run=False):
    """Process one CD: split WAV by CUE into FLAC tracks."""
    wav_name = os.path.basename(wav_path)
    print(f"  🎵 {wav_name}", flush=True)

    # Read CUE and get correct track names
    cue_text = read_cue_text(cue_path)
    correct_titles = dict(parse_cue_tracks(cue_text))

    if not correct_titles:
        print(f"  ⚠️  No tracks found in CUE file")
        return False

    print(f"     {len(correct_titles)} tracks in CUE", flush=True)

    if dry_run:
        return True

    # Split WAV into FLAC tracks in output directory
    rc, out, err = run_cmd(
        ["shnsplit", "-f", cue_path, "-o", "flac", "-t", "%n - %t", wav_path],
        cwd=output_dir, capture=False
    )

    if rc not in (0, 1):
        print(f"  ❌ Split failed (rc={rc})")
        return False

    # Move any FLACs that ended up in parent directory
    parent = os.path.dirname(output_dir)
    for f in os.listdir(parent):
        if f.endswith('.flac') and os.path.isfile(os.path.join(parent, f)):
            shutil.move(os.path.join(parent, f), os.path.join(output_dir, f))

    # Rename garbled FLACs using correct titles
    flacs = sorted([f for f in os.listdir(output_dir) if f.endswith('.flac')])
    renamed = 0
    for f in flacs:
        m = re.match(r'(\d+)\s*-\s*(.+)\.flac', f)
        if not m:
            continue
        tn = int(m.group(1))
        if tn in correct_titles:
            correct = correct_titles[tn]
            new_name = f"{tn:02d} - {safe_filename(correct)}.flac"
            if new_name != f:
                if os.path.exists(os.path.join(output_dir, new_name)):
                    os.remove(os.path.join(output_dir, f))
                else:
                    os.rename(os.path.join(output_dir, f),
                              os.path.join(output_dir, new_name))
                    renamed += 1

    final = len([f for f in os.listdir(output_dir) if f.endswith('.flac')])
    if renamed:
        print(f"     Fixed {renamed} garbled filenames, {final} total", flush=True)
    else:
        print(f"     ✅ {final} FLACs", flush=True)
    return True


def process_album(directory, rar_name, args):
    """Process one RAR archive (one album)."""
    rar_path = os.path.join(directory, rar_name)
    album_name = os.path.splitext(rar_name)[0]
    album_dir = os.path.join(directory, album_name)

    print(f"\n{'='*60}")
    print(f"📦 {rar_name}")

    # Step 1: Extract RAR
    if not extract_rar(directory, rar_name, args.dry_run):
        return False

    # Step 2: Find WAV+CUE pairs (from both fresh extraction and remaining)
    pairs = find_wav_cue_pairs(album_dir)
    if not pairs:
        # Check if already has FLACs
        flacs = [f for r, d, files in os.walk(album_dir)
                 for f in files if f.endswith('.flac')]
        if flacs:
            print(f"  ✅ Already processed: {len(flacs)} FLACs")
        else:
            print(f"  ℹ️  No WAV+CUE pairs found")
        return True

    print(f"  Found {len(pairs)} WAV+CUE pair(s)")

    # Step 3: Determine if multi-CD
    multi_cd = len(pairs) > 1

    if multi_cd:
        # Process each CD into its own subdirectory
        for i, (wav, cue) in enumerate(pairs, 1):
            cd_dir = os.path.join(album_dir, f"CD{i}")
            os.makedirs(cd_dir, exist_ok=True)
            ok = process_single_cd(wav, cue, cd_dir, args.dry_run)
            if ok and not args.dry_run:
                # Clean up this CD's WAV+CUE
                if not args.keep_wav and os.path.isfile(wav):
                    os.remove(wav)
                if not args.keep_cue and os.path.isfile(cue):
                    os.remove(cue)
    else:
        # Single CD - process in album root
        wav, cue = pairs[0]
        ok = process_single_cd(wav, cue, album_dir, args.dry_run)
        if ok and not args.dry_run:
            if not args.keep_wav and os.path.isfile(wav):
                os.remove(wav)
            if not args.keep_cue and os.path.isfile(cue):
                os.remove(cue)

    # Step 4: Clean up RAR if requested
    if args.delete_rar and not args.dry_run and os.path.isfile(rar_path):
        os.remove(rar_path)
        print(f"  🗑️  Deleted RAR: {rar_name}")

    # Step 5: Inject lyrics if requested
    if args.lyrics and not args.dry_run:
        lyric_mod = _get_lyric_module()
        if lyric_mod:
            print(f"\n  🎤 Fetching lyrics...")
            for root, dirs, files in os.walk(album_dir):
                for f in sorted(files):
                    if f.endswith('.flac'):
                        fp = os.path.join(root, f)
                        try:
                            from mutagen.flac import FLAC
                            audio = FLAC(fp)
                            title = audio.get('title', [''])[0]
                            artist = audio.get('artist', [''])[0]
                            if not title:
                                m = re.match(r'\d+\s*-\s*(.+)\.flac', f)
                                if m:
                                    title = m.group(1).strip()
                            lrc, src, tlrc = lyric_mod.get_lyrics(title, artist, flac_path=fp)
                            if lrc:
                                lyric_mod.inject_to_flac(fp, lrc, tlrc)
                                lc = len([l for l in lrc.split('\n') if l.strip()])
                                print(f"    ✅ [{src}] {f} - {lc}行")
                            else:
                                print(f"    ❌ {f} - 未找到歌词")
                        except Exception as e:
                            print(f"    ⚠️ {f} - {e}")

    # Summary
    total_flacs = len([f for r, d, files in os.walk(album_dir)
                       for f in files if f.endswith('.flac')])
    print(f"  📊 Result: {total_flacs} FLACs")
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Convert CD audio archives (RAR/WAV+CUE) into FLAC files.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s /path/to/album/dir
  %(prog)s /path/to/album/dir --dry-run
  %(prog)s /path/to/album/dir --keep-wav --delete-rar
  %(prog)s /path/to/multi/album/root
        """)
    parser.add_argument('directory', help='Directory containing .rar or .wav/.cue files')
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview what would be done without making changes')
    parser.add_argument('--keep-wav', action='store_true',
                        help='Keep original WAV files after conversion')
    parser.add_argument('--keep-cue', action='store_true',
                        help='Keep CUE files after conversion')
    parser.add_argument('--delete-rar', action='store_true',
                        help='Delete RAR archives after successful extraction')
    parser.add_argument('--recursive', '-r', action='store_true',
                        help='Process subdirectories as separate albums')
    parser.add_argument('--lyrics', action='store_true',
                        help='Auto-fetch synced lyrics from Netease/Kugou and inject into FLAC')
    parser.add_argument('--lyrics-only', action='store_true',
                        help='Only inject lyrics into existing FLACs, skip conversion')

    args = parser.parse_args()

    # Check dependencies
    if not check_dependencies():
        sys.exit(1)

    directory = os.path.abspath(args.directory)
    if not os.path.isdir(directory):
        print(f"❌ Directory not found: {directory}")
        sys.exit(1)

    if args.dry_run:
        print("🔍 DRY RUN - no changes will be made\n")

    # ── Lyrics-only mode: inject into existing FLACs ──
    if args.lyrics_only:
        print("🎵 Lyrics-only mode: injecting lyrics into existing FLACs...\n")
        lyric_mod = _get_lyric_module()
        if lyric_mod:
            lyric_mod.process_directory(directory, dry_run=args.dry_run)
        else:
            print("❌ Lyric module not available (needs pycryptodome + mutagen)")
        return

    if args.recursive:
        # Process each subdirectory
        albums = sorted([d for d in os.listdir(directory)
                         if os.path.isdir(os.path.join(directory, d))])
        for album in albums:
            album_path = os.path.join(directory, album)
            process_album(album_path, None, args)
    else:
        # Process RAR files and leftover WAV+CUE in this directory
        rars = get_rar_files(directory)
        if rars:
            print(f"📀 Found {len(rars)} album archive(s) in {directory}")
            success = 0
            for rar in rars:
                if process_album(directory, rar, args):
                    success += 1
            print(f"\n{'='*60}")
            print(f"✅ Done: {success}/{len(rars)} albums processed successfully")
        else:
            # No RARs - process any existing WAV+CUE pairs directly
            pairs = find_wav_cue_pairs(directory)
            if pairs:
                print(f"🎵 Found {len(pairs)} WAV+CUE pair(s)")
                # Determine if multi-CD
                if len(pairs) > 1:
                    for i, (wav, cue) in enumerate(pairs, 1):
                        cd_dir = os.path.join(directory, f"CD{i}")
                        os.makedirs(cd_dir, exist_ok=True)
                        process_single_cd(wav, cue, cd_dir, args.dry_run)
                        if not args.dry_run:
                            if not args.keep_wav:
                                os.remove(wav)
                            if not args.keep_cue:
                                os.remove(cue)
                else:
                    wav, cue = pairs[0]
                    process_single_cd(wav, cue, directory, args.dry_run)
                    if not args.dry_run:
                        if not args.keep_wav:
                            os.remove(wav)
                        if not args.keep_cue:
                            os.remove(cue)
                print(f"\n✅ Processing complete")
            else:
                print(f"ℹ️  No RAR archives or WAV+CUE pairs found in {directory}")


if __name__ == "__main__":
    main()
