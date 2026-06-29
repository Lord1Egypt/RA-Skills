"""
🛠️ axiom-image-metadata-stripper — Image Metadata Remover
==========================================================

⚠️ LIMITATIONS CONNUES :
- JPEG/PNG seulement (pas WebP, AVIF, HEIC)
- Pas de ré-encodage (préserve la qualité d'origine)
- Pas de préservation sélective (tout ou rien)

SUPPRIME LES METADONNÉES D'IMAGE (EXIF, GPS, IPTC, XMP)
"""

import re
import struct
import sys


# JPEG markers
JPEG_SOI = b"\xff\xd8"  # Start of image
JPEG_EOI = b"\xff\xd9"  # End of image
JPEG_SOS = b"\xff\xda"  # Start of scan

# APP/COM markers we want to strip (metadata)
METADATA_MARKERS = {
    b"\xff\xe0": "APP0 (JFIF)",
    b"\xff\xe1": "APP1 (EXIF, XMP)",
    b"\xff\xe2": "APP2 (ICC)",
    b"\xff\xe3": "APP3",
    b"\xff\xe4": "APP4",
    b"\xff\xe5": "APP5",
    b"\xff\xe6": "APP6",
    b"\xff\xe7": "APP7",
    b"\xff\xe8": "APP8",
    b"\xff\xe9": "APP9",
    b"\xff\xea": "APP10",
    b"\xff\xeb": "APP11",
    b"\xff\xec": "APP12 (IPTC)",
    b"\xff\xed": "APP13 (Photoshop)",
    b"\xff\xee": "APP14 (Adobe)",
    b"\xff\xef": "APP15",
    b"\xff\xfe": "COM (Comment)",
}


def detect_format(data: bytes) -> str:
    """Detect image format from magic bytes."""
    if data[:3] == b"\xff\xd8\xff":
        return "jpeg"
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return "png"
    if data[:6] in (b"GIF87a", b"GIF89a"):
        return "gif"
    return "unknown"


def strip_jpeg(data: bytes) -> bytes:
    """
    Strip metadata from JPEG.

    Strategy: walk through markers, skip metadata APP/COM markers,
    keep everything else (DQT, DHT, SOF, SOS, image data).
    """
    if data[:2] != JPEG_SOI:
        raise ValueError("Not a JPEG (no SOI marker)")

    output = bytearray(JPEG_SOI)
    i = 2

    while i < len(data):
        if data[i] != 0xFF:
            # No more markers, just copy remaining
            output.extend(data[i:])
            break

        # Find next marker
        while i < len(data) and data[i] == 0xFF:
            i += 1
        if i >= len(data):
            break

        marker = bytes([0xFF, data[i]])
        i += 1

        # SOI/EOI/RST markers have no length
        if marker in (JPEG_SOI, JPEG_EOI) or (0xD0 <= data[i-1] <= 0xD7):
            output.extend(marker)
            continue

        if i + 1 >= len(data):
            break

        # Read segment length (2 bytes, big-endian, includes the 2 length bytes)
        length = struct.unpack(">H", data[i:i+2])[0]
        segment = data[i-2:i+length]

        if marker in METADATA_MARKERS:
            # Skip this metadata segment
            pass
        else:
            # Keep this segment
            output.extend(segment)

        i += length - 2  # -2 because we already consumed 2 bytes (length)

        if marker == JPEG_SOS:
            # Start of scan — copy remaining data
            output.extend(data[i:])
            break

    return bytes(output)


def strip_png(data: bytes) -> bytes:
    """
    Strip metadata from PNG.

    Strategy: keep only critical chunks (IHDR, PLTE, IDAT, IEND),
    skip ancillary chunks (tEXt, zTXt, iTXt, tIME, pHYs, etc.).
    """
    PNG_SIG = b"\x89PNG\r\n\x1a\n"
    if data[:8] != PNG_SIG:
        raise ValueError("Not a PNG")

    output = bytearray(data[:8])
    i = 8

    while i < len(data):
        if i + 8 > len(data):
            break
        length = struct.unpack(">I", data[i:i+4])[0]
        chunk_type = data[i+4:i+8]

        # Critical chunks (uppercase first letter) are kept
        # Ancillary chunks (lowercase first letter) are metadata — skip
        is_critical = chunk_type[:1].decode("ascii", errors="replace").isupper()

        if is_critical or chunk_type == b"IEND":
            # Keep this chunk
            chunk_data = data[i:i+12+length]
            output.extend(chunk_data)
            if chunk_type == b"IEND":
                break
        # else: skip ancillary chunk

        i += 12 + length  # 4 length + 4 type + data + 4 CRC

    return bytes(output)


def strip_metadata(input_path: str, output_path: str = None) -> dict:
    """
    Strip metadata from an image file.

    Returns dict with: input, output, original_size, stripped_size, format
    """
    with open(input_path, "rb") as f:
        data = f.read()

    fmt = detect_format(data)
    original_size = len(data)

    if fmt == "jpeg":
        stripped = strip_jpeg(data)
    elif fmt == "png":
        stripped = strip_png(data)
    else:
        raise ValueError(f"Unsupported format: {fmt}")

    if output_path is None:
        output_path = input_path + ".stripped"

    with open(output_path, "wb") as f:
        f.write(stripped)

    return {
        "input": input_path,
        "output": output_path,
        "format": fmt,
        "original_size": original_size,
        "stripped_size": len(stripped),
        "bytes_removed": original_size - len(stripped),
        "percent_removed": round(100 * (original_size - len(stripped)) / original_size, 2) if original_size > 0 else 0,
    }


def analyze(input_path: str) -> dict:
    """
    Analyze a JPEG/PNG for metadata chunks (without stripping).
    """
    with open(input_path, "rb") as f:
        data = f.read()

    fmt = detect_format(data)
    result = {
        "input": input_path,
        "format": fmt,
        "size": len(data),
        "metadata_chunks": [],
    }

    if fmt == "jpeg":
        i = 2
        while i < len(data) - 1:
            if data[i] != 0xFF:
                break
            while i < len(data) and data[i] == 0xFF:
                i += 1
            if i >= len(data):
                break
            marker = bytes([0xFF, data[i]])
            i += 1
            if marker in (JPEG_SOI, JPEG_EOI) or (0xD0 <= data[i-1] <= 0xD7):
                continue
            if i + 1 >= len(data):
                break
            length = struct.unpack(">H", data[i:i+2])[0]
            if marker in METADATA_MARKERS:
                result["metadata_chunks"].append({
                    "marker": marker.hex(),
                    "name": METADATA_MARKERS[marker],
                    "size": length,
                })
            i += length - 2
            if marker == JPEG_SOS:
                break

    elif fmt == "png":
        i = 8
        while i < len(data):
            if i + 8 > len(data):
                break
            length = struct.unpack(">I", data[i:i+4])[0]
            chunk_type = data[i+4:i+8].decode("ascii", errors="replace")
            is_critical = chunk_type[:1].decode("ascii", errors="replace").isupper()
            if not is_critical:
                result["metadata_chunks"].append({
                    "chunk_type": chunk_type,
                    "size": length,
                })
            i += 12 + length
            if chunk_type == "IEND":
                break

    return result


def main():
    import argparse
    parser = argparse.ArgumentParser(description="axiom-image-metadata-stripper ")
    parser.add_argument("file", help="Image file")
    parser.add_argument("-o", "--output", help="Output path (default: input + .stripped)")
    parser.add_argument("--analyze", action="store_true", help="Just analyze, don't strip")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    try:
        if args.analyze:
            result = analyze(args.file)
        else:
            result = strip_metadata(args.file, args.output)

        if args.json:
            import json
            print(json.dumps(result, indent=2))
        else:
            if args.analyze:
                print(f"Format: {result['format']}")
                print(f"Size: {result['size']} bytes")
                print(f"Metadata chunks: {len(result['metadata_chunks'])}")
                for chunk in result["metadata_chunks"]:
                    name = chunk.get("name") or chunk.get("chunk_type")
                    size = chunk.get("size")
                    print(f"  - {name}: {size} bytes")
            else:
                print(f"✅ Stripped: {result['output']}")
                print(f"   Format: {result['format']}")
                print(f"   Original: {result['original_size']} bytes")
                print(f"   Stripped: {result['stripped_size']} bytes")
                print(f"   Removed:  {result['bytes_removed']} bytes ({result['percent_removed']}%)")
        return 0
    except Exception as e:
        print(f"❌ Erreur : {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
