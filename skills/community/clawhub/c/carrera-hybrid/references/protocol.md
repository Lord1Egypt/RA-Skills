# Carrera HYBRID BLE Protocol — Reverse Engineering Notes

## Discovery

- **App**: "Carrera Hybrid" by Carrera Toys GmbH (com.sturmkind.carrerahybrid)
- **Developer**: Sturmkind
- **BLE Name**: `HYBRID-<MAC>` (e.g. `HYBRID-XXXXXXXXXXXX`)
- **Address Type**: LE Random
- **Service**: Nordic UART Service (NUS)
  - TX (write to car): `6e400002-b5a3-f393-e0a9-e50e24dcca9e`
  - RX (notifications from car): `6e400003-b5a3-f393-e0a9-e50e24dcca9e`
- **DFU Service**: `0000fe59` (firmware update, not used)

## Packet Structure

20 bytes, sent every ~60ms:

```
Byte:  0    1    2    3    4    5    6      7       8    9    10   11   12   13   14     15   16   17   18   19
Value: BF   0F   00   08   28   00   [GAS]  [STEER] 86   00   72   00   02   FF   [LIGHT] 00   00   00   00   [CRC]
```

### Byte 6 — Gas/Throttle
- `0xDF` (223) = Idle / no throttle
- Forward: `0xE0` → `0xFF` → `0x00` → `0x11` (wraps around, 0x11 = maximum forward)
- Reverse: below `0xDF` (e.g. `0xDF - 40 = 0xB7`)
- Range: approximately ±50 from idle is practical

### Byte 7 — Steering
- `0x00` = Center (straight)
- `0x01` → `0x7F` = Right (0x7F = full right)
- `0x81` → `0xFF` = Left (0x81 = full left, 0xFF = slight left)
- Signed interpretation: positive = right, negative = left

### Byte 14 — Light
- `0x82` = Light ON (default)
- `0x80` = Light OFF
- Bit 1 controls the headlight

### Byte 19 — CRC-8 Checksum
- **Polynomial**: 0x31
- **Initial value**: 0xFF
- Computed over bytes 0-18

```python
def crc8(data):
    crc = 0xFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x80:
                crc = ((crc << 1) ^ 0x31) & 0xFF
            else:
                crc = (crc << 1) & 0xFF
    return crc
```

### Bytes 0-5, 8-13, 15-18 — Static
These bytes are constant in all observed captures:
`BF 0F 00 08 28 00 ... ... 86 00 72 00 02 FF ... 00 00 00 00`

Meaning unknown — possibly car configuration, channel ID, or firmware version identifiers.

## Car Telemetry (RX)

The car sends back 19-byte notification packets:
```
AF 01 9D 01 00 00 00 00 00 00 93 00 FF FF 7E 00 00 00 F7
```
- Starts with `0xAF`
- Content not fully decoded (likely battery, speed, gyro data)

## MITM Proxy Method

To decode the protocol of a new Sturmkind car:

1. Use `bless` to create a fake BLE peripheral with the car's name
2. Turn off the real car so the app connects to the fake
3. Log all write requests to the UART TX characteristic
4. Drive in the app: forward, back, left, right, light toggle
5. Analyze changing bytes to identify gas, steering, light fields
6. Verify CRC-8 with common polynomials (0x07, 0x31, 0x39, etc.)

## Calibration Data

At Gas=20, Steer=80 on smooth indoor surface:
- Full circle: ~7100ms
- ~19.7ms per degree
- Higher gas = faster circle, shorter time

## Discovered Via

BLE MITM proxy on Linux (Intel AX201 adapter, BlueZ, bleak + bless).
691 packets captured in first successful session. Protocol fully decoded from 54 unique packet variants.
