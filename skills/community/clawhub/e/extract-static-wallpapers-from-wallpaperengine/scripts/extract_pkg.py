#!/usr/bin/env python3
"""Extract Wallpaper Engine scene.pkg (PKGV0023 format) and embedded PNG textures.

Usage:
    python extract_pkg.py <scene.pkg> [output_dir]

If output_dir is omitted, a directory with _extracted suffix is created alongside the pkg.
"""

import struct
import os
import sys


def extract_pkg(pkg_path, out_dir):
    """Parse PKGV0023 and extract all entries plus embedded PNGs from .tex files."""
    with open(pkg_path, 'rb') as f:
        data = f.read()

    # --- Parse header ---
    num_entries = struct.unpack_from('<I', data, 0)[0]
    magic = data[4:12].decode('ascii')
    if not magic.startswith('PKGV00'):
        raise ValueError(f'Unknown magic: {magic}, expected PKGV00xx')
    header_val = struct.unpack_from('<I', data, 12)[0]
    print(f'Entries: {num_entries}, HeaderVal: {header_val}')

    # --- Parse entry metadata ---
    pos = 16
    entries = []
    for i in range(num_entries):
        name_len = struct.unpack_from('<I', data, pos)[0]; pos += 4
        name = data[pos:pos + name_len].decode('ascii', errors='replace'); pos += name_len
        # NO alignment padding after filename in PKGV0023
        offset = struct.unpack_from('<I', data, pos)[0]; pos += 4
        size = struct.unpack_from('<I', data, pos)[0]; pos += 4
        entries.append((name, offset, size))
        print(f'  [{i}] {name}  offset={offset}  size={size}  ({size / 1024:.1f} KB)')

    data_start = pos
    print(f'\nData section at file offset: {data_start}')

    # --- Extract all entry files ---
    os.makedirs(out_dir, exist_ok=True)
    tex_files = []

    for name, offset, size in entries:
        file_offset = data_start + offset
        file_data = data[file_offset:file_offset + size]

        out_path = os.path.join(out_dir, name)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, 'wb') as f:
            f.write(file_data)
        print(f'  Extracted: {name}')

        if name.endswith('.tex'):
            tex_files.append(out_path)

    # --- Extract embedded PNGs from .tex files ---
    for tex_path in tex_files:
        _extract_tex_pngs(tex_path, out_dir)

    print('\nDone.')


def _extract_tex_pngs(tex_path, out_dir):
    """Scan a .tex file for embedded PNG streams and extract them all."""
    with open(tex_path, 'rb') as f:
        data = f.read()

    png_sig = b'\x89PNG\r\n\x1a\n'
    png_count = 0

    idx = 0
    while True:
        idx = data.find(png_sig, idx)
        if idx < 0:
            break

        # Parse PNG chunks to find IEND
        pos = idx + 8  # after PNG signature
        while pos < len(data) - 12:
            chunk_len = struct.unpack_from('>I', data, pos)[0]
            chunk_type = data[pos + 4:pos + 8].decode('ascii', errors='replace')
            if chunk_type == 'IEND':
                pos += 12  # IEND: 4(len) + 4(type) + 0(data) + 4(crc)
                break
            pos += 12 + chunk_len

        png_data = data[idx:pos]
        w = int.from_bytes(png_data[16:20], 'big')
        h = int.from_bytes(png_data[20:24], 'big')

        png_count += 1
        if png_count == 1:
            fname = 'wallpaper.png'
        else:
            fname = f'wallpaper_{w}x{h}.png'

        out_path = os.path.join(out_dir, fname)
        with open(out_path, 'wb') as f:
            f.write(png_data)
        print(f'  PNG #{png_count}: {fname} ({w}x{h}, {len(png_data) / 1024:.1f} KB)')

        idx = pos

    if png_count == 0:
        print(f'  No PNGs found in: {os.path.basename(tex_path)}')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    pkg = sys.argv[1]
    if len(sys.argv) >= 3:
        out = sys.argv[2]
    else:
        base = os.path.splitext(pkg)[0]
        out = base + '_extracted'

    print(f'PKG: {pkg}')
    print(f'Output: {out}\n')
    extract_pkg(pkg, out)
