---

## name: can-dbc-matrix

description: Parse and analyze CAN DBC matrix JSON files exported by canmatrix. Use when working with CAN bus databases, DBC files, CAN messages, signals, ECUs, or when the user provides a canmatrix-exported JSON file for analysis, decoding, or signal lookup.

# CAN DBC Matrix JSON Parser

Parse CAN database JSON files exported by the Python `canmatrix` library. The input is always a JSON file produced by `canconvert` with `--jsonExportAll` (full export mode).

## Quick Reference: JSON Top-Level Keys


| Key              | Type   | Content                        |
| ---------------- | ------ | ------------------------------ |
| `messages`       | array  | CAN frames with nested signals |
| `ecus`           | object | ECU name → comment mapping     |
| `attributes`     | object | Global DB attributes           |
| `value_tables`   | object | Named value enumerations       |
| `signal_defines` | array  | Signal attribute definitions   |
| `frame_defines`  | array  | Frame attribute definitions    |
| `global_defines` | array  | Global attribute definitions   |
| `baudrate`       | number | CAN bus baudrate               |
| `fd_baudrate`    | number | CAN FD baudrate                |


## Core Workflow

1. **Load** the JSON with `json.load()`
2. **Navigate** using the structure documented in [json-schema.md](json-schema.md)
3. **Process** messages and signals as needed

## Common Tasks

### List All Messages

```python
import json

with open("can_db.json", encoding="utf-8") as f:
    db = json.load(f)

for msg in db["messages"]:
    print(f"0x{msg['id']:03X} {msg['name']}  DLC={msg['length']}  "
          f"cycle={msg.get('cycle_time', 'N/A')}ms  TX={msg.get('transmitters', [])}")
```

### Find a Signal by Name

```python
def find_signal(db, signal_name):
    for msg in db["messages"]:
        for sig in msg["signals"]:
            if sig["name"] == signal_name:
                return msg, sig
    return None, None

msg, sig = find_signal(db, "VehicleSpeed")
```

### Decode a Raw CAN Frame

```python
def decode_frame(db, arb_id, data_bytes):
    """Decode raw CAN data bytes into physical signal values."""
    msg = next((m for m in db["messages"] if m["id"] == arb_id), None)
    if not msg:
        return None

    results = {}
    for sig in msg["signals"]:
        raw = extract_raw_value(data_bytes, sig)
        physical = raw * float(sig["factor"]) + float(sig["offset"])

        # Value table lookup
        val_str = sig.get("values", {}).get(str(int(raw)))
        results[sig["name"]] = {
            "raw": raw,
            "physical": physical,
            "unit": sig.get("unit", ""),
            "enum": val_str,
        }
    return results


def extract_raw_value(data_bytes, sig):
    """Extract raw integer from CAN data bytes for one signal."""
    start_bit = sig["start_bit"]
    bit_length = sig["bit_length"]
    is_big_endian = sig.get("is_big_endian", False)
    is_signed = sig.get("is_signed", False)

    bits = ''.join(f'{b:08b}' for b in data_bytes)

    if is_big_endian:
        byte_pos = start_bit // 8
        bit_in_byte = start_bit % 8
        collected = []
        pos = byte_pos * 8 + (7 - bit_in_byte)
        for _ in range(bit_length):
            if 0 <= pos < len(bits):
                collected.append(bits[pos])
            curr_byte = pos // 8
            curr_bit = pos % 8
            if curr_bit == 0:
                pos = (curr_byte + 1) * 8 + 7
            else:
                pos -= 1
        raw = int(''.join(collected), 2)
    else:
        raw = 0
        for i in range(bit_length):
            byte_num = (start_bit + i) // 8
            bit_num = (start_bit + i) % 8
            if byte_num < len(data_bytes):
                if data_bytes[byte_num] & (1 << bit_num):
                    raw |= (1 << i)

    if is_signed and raw >= (1 << (bit_length - 1)):
        raw -= (1 << bit_length)
    return raw
```

### Physical Value Formula

```
physical = raw_value * factor + offset
raw_value = (physical - offset) / factor
```

Signal range: `[min, max]` in physical units.

### Generate Message/Signal Summary Table

```python
def summarize(db):
    rows = []
    for msg in db["messages"]:
        for sig in msg["signals"]:
            rows.append({
                "Message": f"0x{msg['id']:03X} {msg['name']}",
                "Signal": sig["name"],
                "Start": sig["start_bit"],
                "Len": sig["bit_length"],
                "Factor": sig["factor"],
                "Offset": sig["offset"],
                "Unit": sig.get("unit", ""),
                "Min": sig.get("min", ""),
                "Max": sig.get("max", ""),
                "Endian": "BE" if sig.get("is_big_endian") else "LE",
            })
    return rows
```

### Filter by ECU (Transmitter/Receiver)

```python
def messages_by_tx(db, ecu_name):
    return [m for m in db["messages"] if ecu_name in m.get("transmitters", [])]

def signals_received_by(db, ecu_name):
    results = []
    for msg in db["messages"]:
        for sig in msg["signals"]:
            if ecu_name in sig.get("receivers", []):
                results.append((msg, sig))
    return results
```

## Important Notes

- Message `id` is a decimal integer. Convert with `hex(id)` for display.
- `is_extended_frame`: True = 29-bit CAN ID, False = 11-bit standard ID.
- `is_fd`: True = CAN FD frame (up to 64 bytes), False = Classic CAN (up to 8 bytes).
- `factor`/`offset` may be strings or floats depending on export settings. Always cast to `float()`.
- `values` dict maps raw integer (as string key) → enum label string.
- Motorola (big-endian) bit numbering: canmatrix exports in "lsb" format by default.
- `cycle_time` is in milliseconds. 0 or absent means event-triggered.

## DBC to JSON Conversion

Use canmatrix's built-in CLI tool:

```bash
pip install canmatrix
canconvert input.dbc output.json --jsonExportAll
```

Other supported input formats: `.arxml`, `.kcd`, `.dbf`, `.xls(x)`, `.sym`, `.ldf`.

See [json-schema.md](json-schema.md) for the complete JSON structure reference.