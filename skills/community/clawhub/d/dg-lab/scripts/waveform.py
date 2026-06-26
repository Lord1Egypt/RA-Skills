#!/usr/bin/env python3
"""DG-LAB V3 waveform generation and validation utilities.

SECURITY MANIFEST:
  Environment variables accessed: none
  External endpoints called: none
  Local files read: scripts/presets.json
  Local files written: none
"""

import json
import math
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent

FREQ_MIN = 10
FREQ_MAX = 240
FREQ_INPUT_MAX = 1000
INTENSITY_MIN = 0
INTENSITY_MAX = 100
HEX_ENTRY_LEN = 16  # 8 bytes = 16 hex chars
MS_PER_ENTRY = 100  # each entry represents 100ms
MAX_ENTRIES_PER_MESSAGE = 100  # APP limit


def freq_input_to_byte(value: int) -> int:
    """Convert user-friendly frequency (10-1000) to protocol byte (10-240).

    Uses the official DG-LAB conversion formula from V3 spec.
    """
    if value < 10:
        return 10
    if value <= 100:
        return value
    if value <= 600:
        return (value - 100) // 5 + 100
    if value <= 1000:
        return (value - 600) // 10 + 200
    return 10


def validate_freq(value: int) -> int:
    if not FREQ_MIN <= value <= FREQ_MAX:
        raise ValueError(f"Frequency {value} out of range [{FREQ_MIN}, {FREQ_MAX}]")
    return value


def validate_intensity(value: int) -> int:
    if not INTENSITY_MIN <= value <= INTENSITY_MAX:
        raise ValueError(f"Intensity {value} out of range [{INTENSITY_MIN}, {INTENSITY_MAX}]")
    return value


def encode_entry(freq: int, intensity: int) -> str:
    """Encode a single 100ms waveform entry to V3 HEX format.

    Each entry = 4 freq bytes + 4 intensity bytes (same value repeated 4x for 25ms granularity).
    """
    f = validate_freq(freq)
    i = validate_intensity(intensity)
    return f"{f:02X}" * 4 + f"{i:02X}" * 4


def decode_entry(hex_str: str) -> dict:
    """Decode a V3 HEX entry back to frequency and intensity values."""
    if len(hex_str) != HEX_ENTRY_LEN:
        raise ValueError(f"Entry must be {HEX_ENTRY_LEN} hex chars, got {len(hex_str)}")
    freqs = [int(hex_str[i:i+2], 16) for i in range(0, 8, 2)]
    intensities = [int(hex_str[i:i+2], 16) for i in range(8, 16, 2)]
    return {"freq": freqs, "intensity": intensities}


def validate_hex_data(data: list[str]) -> list[str]:
    """Validate a list of V3 HEX entries."""
    if not data:
        raise ValueError("Waveform data is empty")
    if len(data) > MAX_ENTRIES_PER_MESSAGE:
        raise ValueError(f"Too many entries: {len(data)} > {MAX_ENTRIES_PER_MESSAGE}")
    for i, entry in enumerate(data):
        if len(entry) != HEX_ENTRY_LEN:
            raise ValueError(f"Entry {i}: expected {HEX_ENTRY_LEN} hex chars, got {len(entry)}")
        try:
            decoded = decode_entry(entry)
            for f in decoded["freq"]:
                if f != 0:
                    validate_freq(f)
            for v in decoded["intensity"]:
                validate_intensity(v)
        except ValueError as e:
            raise ValueError(f"Entry {i} ({entry}): {e}") from e
    return data


def generate_constant(freq: int, intensity: int, duration_ms: int) -> list[str]:
    """Generate constant waveform (same freq + intensity throughout)."""
    count = max(1, duration_ms // MS_PER_ENTRY)
    entry = encode_entry(freq, intensity)
    return [entry] * count


def generate_ramp(freq: int, start_intensity: int, end_intensity: int,
                  duration_ms: int) -> list[str]:
    """Generate linear ramp from start to end intensity."""
    count = max(2, duration_ms // MS_PER_ENTRY)
    entries = []
    for i in range(count):
        t = i / (count - 1)
        intensity = round(start_intensity + (end_intensity - start_intensity) * t)
        entries.append(encode_entry(freq, intensity))
    return entries


def generate_sine(freq: int, max_intensity: int, period_ms: int,
                  duration_ms: int) -> list[str]:
    """Generate sine-wave intensity pattern."""
    count = max(1, duration_ms // MS_PER_ENTRY)
    period_entries = max(1, period_ms // MS_PER_ENTRY)
    entries = []
    for i in range(count):
        t = (i % period_entries) / period_entries
        intensity = round(max_intensity * (0.5 + 0.5 * math.sin(2 * math.pi * t - math.pi / 2)))
        entries.append(encode_entry(freq, intensity))
    return entries


def generate_pulse(freq: int, intensity: int, on_ms: int, off_ms: int,
                   duration_ms: int) -> list[str]:
    """Generate on/off pulse pattern."""
    on_count = max(1, on_ms // MS_PER_ENTRY)
    off_count = max(1, off_ms // MS_PER_ENTRY)
    cycle = on_count + off_count
    total = max(1, duration_ms // MS_PER_ENTRY)
    entries = []
    for i in range(total):
        pos = i % cycle
        if pos < on_count:
            entries.append(encode_entry(freq, intensity))
        else:
            entries.append(encode_entry(freq, 0))
    return entries


def load_presets() -> dict:
    """Load built-in waveform presets."""
    presets_path = SCRIPT_DIR / "presets.json"
    if not presets_path.exists():
        raise FileNotFoundError(f"Presets file not found: {presets_path}")
    with open(presets_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_preset(name: str) -> list[str]:
    """Get a preset waveform by name. Returns validated HEX data list."""
    presets = load_presets()
    if name not in presets:
        available = ", ".join(sorted(presets.keys()))
        raise ValueError(f"Unknown preset '{name}'. Available: {available}")
    return validate_hex_data(presets[name]["data"])


def list_presets() -> list[dict]:
    """List all available presets with metadata."""
    presets = load_presets()
    result = []
    for key, info in presets.items():
        result.append({
            "id": key,
            "name_zh": info.get("name_zh", key),
            "description": info.get("description", ""),
            "entries": len(info["data"]),
            "duration_ms": len(info["data"]) * MS_PER_ENTRY,
        })
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python waveform.py list                         - List all presets")
        print("  python waveform.py preset <name>                - Show preset data")
        print("  python waveform.py constant <freq> <int> <ms>   - Generate constant")
        print("  python waveform.py ramp <freq> <s> <e> <ms>     - Generate ramp")
        print("  python waveform.py validate <hex1> <hex2> ...   - Validate HEX data")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "list":
        for p in list_presets():
            print(f"  {p['id']:20s} ({p['name_zh']}) - {p['duration_ms']}ms - {p['description']}")
    elif cmd == "preset":
        name = sys.argv[2]
        data = get_preset(name)
        print(json.dumps(data))
    elif cmd == "constant":
        freq, intensity, ms = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
        print(json.dumps(generate_constant(freq, intensity, ms)))
    elif cmd == "ramp":
        freq, s, e, ms = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
        print(json.dumps(generate_ramp(freq, s, e, ms)))
    elif cmd == "validate":
        data = sys.argv[2:]
        try:
            validate_hex_data(data)
            print("OK: all entries valid")
        except ValueError as err:
            print(f"INVALID: {err}", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)
