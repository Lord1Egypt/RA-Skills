#!/usr/bin/env python3
"""General-purpose EXR extraction CLI.

Subcommands:
    info      List channels, resolution, data window, cryptomatte metadata
    beauty    Extract RGB/beauty pass as PNG with color space conversion
    crypto    Extract cryptomatte pass as colored segmentation PNG
    channels  Extract arbitrary channels as images
"""

import argparse
import os
import sys
import struct
from collections import Counter
from pathlib import Path

import numpy as np
import OpenEXR
import Imath
from PIL import Image

PT = Imath.PixelType(Imath.PixelType.FLOAT)

# ---------------------------------------------------------------------------
# Color space matrices and functions
# ---------------------------------------------------------------------------

# ACEScg (AP1) -> linear sRGB (Rec.709 primaries, D65)
ACESCG_TO_LINEAR_SRGB = np.array([
    [ 1.70505, -0.62179, -0.08326],
    [-0.13026,  1.14080, -0.01055],
    [-0.02400, -0.12897,  1.15297],
], dtype=np.float32)

IDENTITY_3x3 = np.eye(3, dtype=np.float32)

COLORSPACE_MATRICES = {
    "acescg": ACESCG_TO_LINEAR_SRGB,
    "linear": IDENTITY_3x3,
    "srgb": None,  # passthrough — already sRGB
}


def srgb_oetf(x):
    """sRGB piecewise OETF (linear -> gamma-encoded sRGB)."""
    return np.where(
        x <= 0.0031308,
        x * 12.92,
        1.055 * np.power(np.maximum(x, 0), 1.0 / 2.4) - 0.055,
    )


def linear_to_srgb_uint8(rgb, colorspace="acescg"):
    """Convert linear float RGB to sRGB uint8.

    Args:
        rgb: (H, W, 3) float32 array in the given input color space.
        colorspace: 'acescg', 'linear', or 'srgb'.

    Returns:
        (H, W, 3) uint8 array in sRGB.
    """
    h, w, _ = rgb.shape
    matrix = COLORSPACE_MATRICES.get(colorspace)

    if matrix is None:
        # Already sRGB — just clamp and quantize
        return (np.clip(rgb, 0, 1) * 255).astype(np.uint8)

    flat = rgb.reshape(-1, 3)
    linear_srgb = (flat @ matrix.T).reshape(h, w, 3)
    linear_srgb = np.clip(linear_srgb, 0, 1)
    encoded = srgb_oetf(linear_srgb)
    return (np.clip(encoded, 0, 1) * 255).astype(np.uint8)


# ---------------------------------------------------------------------------
# 35-color bold palette for cryptomatte visualization
# ---------------------------------------------------------------------------

BOLD_PALETTE = np.array([
    (255,   0,   0),  # Red
    (  0,   0, 255),  # Blue
    (  0, 255,   0),  # Green
    (  0, 255, 255),  # Cyan
    (255,   0, 255),  # Magenta
    (255, 255,   0),  # Yellow
    (  0,   0,   0),  # Black
    (255, 128,   0),  # Orange
    (  0, 128, 255),  # Sky Blue
    (128,   0, 255),  # Purple
    (  0, 200, 128),  # Emerald
    (180,  80,  40),  # Brown
    (100, 100, 255),  # Cornflower
    (255,  80, 180),  # Hot Pink
    (  0, 180, 180),  # Teal
    (200, 200,   0),  # Olive Yellow
    (255, 160,  80),  # Peach
    ( 80,   0, 128),  # Dark Purple
    (  0, 100,   0),  # Dark Green
    (128,   0,   0),  # Dark Red
    (220, 220, 220),  # Light Gray
    (  0,  60, 120),  # Navy
    (180, 255, 100),  # Lime
    (255, 100, 100),  # Coral
    (100,  50,   0),  # Dark Brown
    (  0, 255, 180),  # Mint
    (200,   0, 100),  # Crimson
    ( 80, 180, 255),  # Light Blue
    (255, 200,   0),  # Gold
    (160,   0, 200),  # Violet
    (  0, 140,  60),  # Forest Green
    (255, 128, 128),  # Salmon
    ( 60,  60, 180),  # Indigo
    (200, 255, 200),  # Pale Green
    (255,  60,   0),  # Red-Orange
], dtype=np.uint8)

BG_COLORS = {
    "gray": np.array([128, 128, 128], dtype=np.uint8),
    "black": np.array([0, 0, 0], dtype=np.uint8),
}

# ---------------------------------------------------------------------------
# EXR helpers
# ---------------------------------------------------------------------------


def collect_exr_files(path):
    """Return a sorted list of EXR file paths from a file or directory."""
    p = Path(path)
    if p.is_file():
        if p.suffix.lower() == ".exr":
            return [p]
        print(f"Not an EXR file: {p}", file=sys.stderr)
        return []
    if p.is_dir():
        files = sorted(p.glob("*.exr"))
        if not files:
            print(f"No EXR files found in: {p}", file=sys.stderr)
        return files
    print(f"Path not found: {p}", file=sys.stderr)
    return []


def open_exr(path):
    """Open an EXR file and return (InputFile, header, width, height, channel_set)."""
    exr = OpenEXR.InputFile(str(path))
    header = exr.header()
    dw = header["dataWindow"]
    w = dw.max.x - dw.min.x + 1
    h = dw.max.y - dw.min.y + 1
    channels = set(header["channels"].keys())
    return exr, header, w, h, channels


def read_channel(exr, name, h, w):
    """Read a single float32 channel from an open EXR."""
    raw = exr.channel(name, PT)
    return np.frombuffer(raw, dtype=np.float32).reshape(h, w)


def output_path(input_path, output_dir, suffix="", ext=".png"):
    """Build an output path, respecting --output-dir and --suffix."""
    base = Path(input_path).stem
    out_name = f"{base}{suffix}{ext}"
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        return Path(output_dir) / out_name
    return Path(input_path).parent / out_name


# ---------------------------------------------------------------------------
# Cryptomatte helpers
# ---------------------------------------------------------------------------

# Maps crypto type keywords to lists of channel prefix patterns to try
CRYPTO_PREFIXES = {
    "crypto_material": ["crypto_material", "crypto_mat"],
    "crypto_object": ["crypto_object", "crypto_obj"],
    "crypto_asset": ["crypto_asset"],
}


def detect_crypto_channels(channels, crypto_type=None):
    """Auto-detect cryptomatte channel prefixes present in the EXR.

    Args:
        channels: set of channel names from the EXR header.
        crypto_type: optional specific type (e.g. 'crypto_material').
                     If None, detect all present types.

    Returns:
        list of (crypto_type, channel_prefix) tuples.
        e.g. [('crypto_material', 'crypto_mat')]
    """
    results = []
    types_to_check = (
        {crypto_type: CRYPTO_PREFIXES.get(crypto_type, [crypto_type])}
        if crypto_type
        else CRYPTO_PREFIXES
    )

    for ctype, prefixes in types_to_check.items():
        for prefix in prefixes:
            if f"{prefix}00.R" in channels:
                results.append((ctype, prefix))
                break  # found this type, move on

    return results


def detect_background_id(ids, mask):
    """Detect the background material ID by sampling image edges and corners.

    Args:
        ids: (H, W) uint32 array of material IDs.
        mask: (H, W) bool array where True = has coverage.

    Returns:
        int — the uint32 ID most common at edges/corners.
    """
    edge_samples = np.concatenate([
        ids[0, :],
        ids[-1, :],
        ids[:, 0],
        ids[:, -1],
        ids[0:10, 0:10].ravel(),
        ids[0:10, -10:].ravel(),
        ids[-10:, 0:10].ravel(),
        ids[-10:, -10:].ravel(),
    ])
    return Counter(edge_samples.tolist()).most_common(1)[0][0]


def extract_crypto(exr, h, w, channels, prefix, palette, bg_color, bg_mode):
    """Extract a single cryptomatte pass as an RGB uint8 image.

    Args:
        exr: open EXR InputFile.
        h, w: image dimensions.
        channels: set of channel names.
        prefix: channel prefix (e.g. 'crypto_material' or 'crypto_mat').
        palette: (N, 3) uint8 array of colors.
        bg_color: (3,) uint8 background color.
        bg_mode: 'gray', 'black', or 'auto'.

    Returns:
        (H, W, 3) uint8 numpy array, or None if channels missing.
    """
    r_ch = f"{prefix}00.R"
    g_ch = f"{prefix}00.G"
    if r_ch not in channels or g_ch not in channels:
        return None

    id0 = read_channel(exr, r_ch, h, w)
    cov0 = read_channel(exr, g_ch, h, w)

    ids = id0.view(np.uint32)
    mask = cov0 > 0.0

    bg_id = detect_background_id(ids, mask)

    if bg_mode == "auto":
        bg_color = bg_color  # use the provided default

    # Rank materials by pixel area (largest first)
    id_area = {}
    for uid in np.unique(ids[mask]):
        uid_int = int(uid)
        if uid_int != bg_id:
            id_area[uid_int] = int(np.sum(ids[mask] == uid))

    sorted_ids = sorted(id_area.keys(), key=lambda x: -id_area[x])

    # Build color lookup
    id_to_color = {bg_id: bg_color}
    for i, uid in enumerate(sorted_ids):
        id_to_color[uid] = palette[i % len(palette)]

    # Paint the image
    img = np.zeros((h, w, 3), dtype=np.uint8)
    for uid, color in id_to_color.items():
        img[ids == uid] = color
    # Pixels with zero coverage get black (transparent / no data)
    img[~mask] = 0

    return img


# ---------------------------------------------------------------------------
# Subcommand: info
# ---------------------------------------------------------------------------


def cmd_info(args):
    """Print EXR file information."""
    files = collect_exr_files(args.path)
    if not files:
        return 1

    for fpath in files:
        exr, header, w, h, channels = open_exr(fpath)
        print(f"\n{'='*60}")
        print(f"File: {fpath.name}")
        print(f"Resolution: {w} x {h}")

        dw = header["dataWindow"]
        print(f"Data window: ({dw.min.x}, {dw.min.y}) - ({dw.max.x}, {dw.max.y})")

        disp = header.get("displayWindow")
        if disp:
            print(f"Display window: ({disp.min.x}, {disp.min.y}) - ({disp.max.x}, {disp.max.y})")

        # Channel list
        sorted_channels = sorted(channels)
        print(f"\nChannels ({len(sorted_channels)}):")
        for ch in sorted_channels:
            ch_info = header["channels"][ch]
            print(f"  {ch}  (type: {ch_info.type}, sampling: {ch_info.xSampling}x{ch_info.ySampling})")

        # Cryptomatte metadata
        crypto_meta = {
            k: v for k, v in header.items()
            if isinstance(k, str) and k.startswith("cryptomatte/")
        }
        if crypto_meta:
            print("\nCryptomatte metadata:")
            for k in sorted(crypto_meta.keys()):
                v = crypto_meta[k]
                if isinstance(v, bytes):
                    v = v.decode("utf-8", errors="replace")
                # Truncate long manifests
                v_str = str(v)
                if len(v_str) > 200:
                    v_str = v_str[:200] + "..."
                print(f"  {k}: {v_str}")

        # Detected crypto types
        detected = detect_crypto_channels(channels)
        if detected:
            print("\nDetected cryptomatte passes:")
            for ctype, prefix in detected:
                # Count levels
                level = 0
                while f"{prefix}{level:02d}.R" in channels:
                    level += 1
                print(f"  {ctype} (prefix: {prefix}, levels: {level})")

        exr.close()

    return 0


# ---------------------------------------------------------------------------
# Subcommand: beauty
# ---------------------------------------------------------------------------


def cmd_beauty(args):
    """Extract beauty/RGB pass as PNG."""
    files = collect_exr_files(args.path)
    if not files:
        return 1

    colorspace = args.colorspace
    if colorspace not in COLORSPACE_MATRICES:
        print(f"Unknown color space: {colorspace}", file=sys.stderr)
        print(f"Available: {', '.join(COLORSPACE_MATRICES.keys())}", file=sys.stderr)
        return 1

    errors = 0
    for fpath in files:
        out = output_path(fpath, args.output_dir)
        if out.exists() and not args.force:
            print(f"SKIP {fpath.name} -> {out.name} (exists, use --force to overwrite)")
            continue

        print(f"Processing {fpath.name} ...", end=" ", flush=True)
        exr, header, w, h, channels = open_exr(fpath)

        # Find RGB channels — try bare R,G,B first, then rgba.R etc.
        if "R" in channels and "G" in channels and "B" in channels:
            r_ch, g_ch, b_ch = "R", "G", "B"
        elif "rgba.R" in channels:
            r_ch, g_ch, b_ch = "rgba.R", "rgba.G", "rgba.B"
        else:
            print(f"WARN no RGB channels found")
            exr.close()
            errors += 1
            continue

        R = read_channel(exr, r_ch, h, w)
        G = read_channel(exr, g_ch, h, w)
        B = read_channel(exr, b_ch, h, w)
        exr.close()

        rgb = np.stack([R, G, B], axis=-1)
        img_uint8 = linear_to_srgb_uint8(rgb, colorspace)
        Image.fromarray(img_uint8, "RGB").save(str(out))
        print(f"-> {out.name}")

    return 1 if errors else 0


# ---------------------------------------------------------------------------
# Subcommand: crypto
# ---------------------------------------------------------------------------

CRYPTO_TYPE_SUFFIXES = {
    "crypto_material": "_materialID",
    "crypto_object": "_objectID",
    "crypto_asset": "_assetID",
}


def cmd_crypto(args):
    """Extract cryptomatte pass as colored segmentation PNG."""
    files = collect_exr_files(args.path)
    if not files:
        return 1

    # Resolve background color
    bg_mode = args.bg_color
    if bg_mode in BG_COLORS:
        bg_color = BG_COLORS[bg_mode]
    elif bg_mode == "auto":
        bg_color = BG_COLORS["gray"]
    else:
        print(f"Unknown --bg-color: {bg_mode}. Use: gray, black, auto", file=sys.stderr)
        return 1

    palette = BOLD_PALETTE

    errors = 0
    for fpath in files:
        print(f"Processing {fpath.name} ...", end=" ", flush=True)
        exr, header, w, h, channels = open_exr(fpath)

        # Determine which crypto types to extract
        if args.type:
            detected = detect_crypto_channels(channels, args.type)
            if not detected:
                print(f"WARN no {args.type} channels found")
                exr.close()
                errors += 1
                continue
        else:
            detected = detect_crypto_channels(channels)
            if not detected:
                print(f"WARN no cryptomatte channels found")
                exr.close()
                errors += 1
                continue

        for ctype, prefix in detected:
            # Build suffix
            if args.no_suffix:
                suffix = ""
            elif args.suffix:
                suffix = args.suffix
            else:
                suffix = CRYPTO_TYPE_SUFFIXES.get(ctype, f"_{ctype}")

            out = output_path(fpath, args.output_dir, suffix=suffix)
            if out.exists() and not args.force:
                print(f"SKIP {out.name} (exists)")
                continue

            img = extract_crypto(exr, h, w, channels, prefix, palette, bg_color, bg_mode)
            if img is None:
                print(f"WARN failed to extract {ctype}")
                errors += 1
                continue

            Image.fromarray(img, "RGB").save(str(out))
            print(f"-> {out.name}")

        exr.close()

    return 1 if errors else 0


# ---------------------------------------------------------------------------
# Subcommand: channels
# ---------------------------------------------------------------------------


def cmd_channels(args):
    """Extract arbitrary channels as images."""
    files = collect_exr_files(args.path)
    if not files:
        return 1

    requested = [c.strip() for c in args.channels.split(",")]
    colorspace = args.colorspace

    errors = 0
    for fpath in files:
        suffix = "_" + "_".join(requested)
        out = output_path(fpath, args.output_dir, suffix=suffix)
        if out.exists() and not args.force:
            print(f"SKIP {fpath.name} -> {out.name} (exists)")
            continue

        print(f"Processing {fpath.name} ...", end=" ", flush=True)
        exr, header, w, h, channels = open_exr(fpath)

        missing = [c for c in requested if c not in channels]
        if missing:
            print(f"WARN missing channels: {', '.join(missing)}")
            exr.close()
            errors += 1
            continue

        channel_data = []
        for ch_name in requested:
            channel_data.append(read_channel(exr, ch_name, h, w))
        exr.close()

        if len(channel_data) == 1:
            # Single channel — save as grayscale
            data = np.clip(channel_data[0], 0, 1)
            img_uint8 = (data * 255).astype(np.uint8)
            Image.fromarray(img_uint8, "L").save(str(out))
        elif len(channel_data) == 3:
            # Three channels — treat as RGB
            rgb = np.stack(channel_data, axis=-1)
            if colorspace:
                img_uint8 = linear_to_srgb_uint8(rgb, colorspace)
            else:
                img_uint8 = (np.clip(rgb, 0, 1) * 255).astype(np.uint8)
            Image.fromarray(img_uint8, "RGB").save(str(out))
        else:
            # Other count — save each as separate grayscale
            for i, (ch_name, data) in enumerate(zip(requested, channel_data)):
                ch_out = output_path(fpath, args.output_dir, suffix=f"_{ch_name.replace('.', '_')}")
                data_clipped = np.clip(data, 0, 1)
                img_uint8 = (data_clipped * 255).astype(np.uint8)
                Image.fromarray(img_uint8, "L").save(str(ch_out))
                print(f"-> {ch_out.name}", end=" ")

        print(f"-> {out.name}" if len(channel_data) in (1, 3) else "")

    return 1 if errors else 0


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        prog="exr_extract",
        description="General-purpose EXR extraction tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
examples:
  %(prog)s info render.exr
  %(prog)s info ./renders/
  %(prog)s beauty render.exr --colorspace acescg
  %(prog)s beauty ./renders/ --output-dir ./pngs/
  %(prog)s crypto render.exr --type crypto_material
  %(prog)s crypto ./renders/ --bg-color black
  %(prog)s channels render.exr --channels N.X,N.Y,N.Z
""",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    # --- info ---
    p_info = sub.add_parser("info", help="List channels, resolution, and metadata")
    p_info.add_argument("path", help="EXR file or directory of EXRs")

    # --- beauty ---
    p_beauty = sub.add_parser("beauty", help="Extract RGB/beauty pass as PNG")
    p_beauty.add_argument("path", help="EXR file or directory of EXRs")
    p_beauty.add_argument(
        "--colorspace", default="acescg",
        help="Input color space: acescg (default), linear, srgb",
    )
    p_beauty.add_argument("--output-dir", default=None, help="Output directory")
    p_beauty.add_argument("--force", action="store_true", help="Overwrite existing files")

    # --- crypto ---
    p_crypto = sub.add_parser("crypto", help="Extract cryptomatte as colored segmentation PNG")
    p_crypto.add_argument("path", help="EXR file or directory of EXRs")
    p_crypto.add_argument(
        "--type", default=None,
        help="crypto_material, crypto_object, or crypto_asset (default: auto-detect)",
    )
    p_crypto.add_argument(
        "--palette", default="bold", help="Color palette: bold (default)",
    )
    p_crypto.add_argument(
        "--bg-color", default="gray",
        help="Background color: gray (default), black, auto",
    )
    p_crypto.add_argument("--output-dir", default=None, help="Output directory")
    p_crypto.add_argument(
        "--suffix", default=None,
        help="Output suffix (default: _materialID, _objectID, etc.)",
    )
    p_crypto.add_argument(
        "--no-suffix", action="store_true",
        help="No suffix — output same name as input",
    )
    p_crypto.add_argument("--force", action="store_true", help="Overwrite existing files")

    # --- channels ---
    p_channels = sub.add_parser("channels", help="Extract arbitrary channels as images")
    p_channels.add_argument("path", help="EXR file or directory of EXRs")
    p_channels.add_argument(
        "--channels", required=True,
        help="Comma-separated channel names (e.g. R,G,B or N.X,N.Y,N.Z)",
    )
    p_channels.add_argument(
        "--colorspace", default=None,
        help="Input color space for conversion (acescg, linear, srgb)",
    )
    p_channels.add_argument("--output-dir", default=None, help="Output directory")
    p_channels.add_argument("--force", action="store_true", help="Overwrite existing files")

    args = parser.parse_args()

    handlers = {
        "info": cmd_info,
        "beauty": cmd_beauty,
        "crypto": cmd_crypto,
        "channels": cmd_channels,
    }
    sys.exit(handlers[args.command](args))


if __name__ == "__main__":
    main()
