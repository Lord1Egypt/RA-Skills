# Canmatrix JSON Schema Reference

## Default Mode (`canconvert in.dbc out.json`)

### Top-Level

```json
{ "messages": [ ... ] }
```

### Message Object (default)

```json
{
  "name": "VCU_Status",
  "id": 291,
  "is_extended_frame": false,
  "is_fd": false,
  "signals": [ ... ]
}
```


| Field               | Type   | Description               |
| ------------------- | ------ | ------------------------- |
| `name`              | string | Frame name                |
| `id`                | int    | Arbitration ID (decimal)  |
| `is_extended_frame` | bool   | True = 29-bit extended ID |
| `is_fd`             | bool   | True = CAN FD frame       |
| `signals`           | array  | Signal definitions        |


### Signal Object (default)

```json
{
  "name": "VehicleSpeed",
  "start_bit": 8,
  "bit_length": 16,
  "factor": "0.01",
  "offset": "0",
  "is_big_endian": false,
  "is_signed": false,
  "is_float": false,
  "is_ascii": false
}
```


| Field           | Type         | Description                |
| --------------- | ------------ | -------------------------- |
| `name`          | string       | Signal name                |
| `start_bit`     | int          | Start bit (LSB numbering)  |
| `bit_length`    | int          | Width in bits              |
| `factor`        | string/float | Scale factor               |
| `offset`        | string/float | Offset                     |
| `is_big_endian` | bool         | True = Motorola byte order |
| `is_signed`     | bool         | Signed integer             |
| `is_float`      | bool         | IEEE 754 float             |
| `is_ascii`      | bool         | ASCII string signal        |


---

## Full Mode (`canconvert in.dbc out.json --jsonExportAll`)

Adds the following top-level keys alongside `messages`:

```json
{
  "messages": [ ... ],
  "ecus": { "VCU": "Vehicle Control Unit", "BMS": null },
  "attributes": { ... },
  "value_tables": { "OnOff": { "0": "Off", "1": "On" } },
  "env_vars": { ... },
  "baudrate": 500000,
  "fd_baudrate": 2000000,
  "signal_defines": [ ... ],
  "frame_defines": [ ... ],
  "global_defines": [ ... ],
  "env_defines": [ ... ],
  "ecu_defines": [ ... ]
}
```

### Message Object (full) — additional fields

```json
{
  "name": "VCU_Status",
  "id": 291,
  "is_extended_frame": false,
  "is_fd": false,
  "length": 8,
  "comment": "VCU periodic status",
  "cycle_time": 100,
  "transmitters": ["VCU"],
  "is_j1939": false,
  "is_complex_multiplexed": false,
  "mux_names": {},
  "header_id": null,
  "pdu_name": "",
  "attributes": { "GenMsgCycleTime": 100, "GenMsgSendType": "Cyclic" },
  "signals": [ ... ]
}
```


| Field                    | Type        | Description                   |
| ------------------------ | ----------- | ----------------------------- |
| `length`                 | int         | DLC in bytes                  |
| `comment`                | string/null | Message description           |
| `cycle_time`             | int         | Cycle time in ms (0 = event)  |
| `transmitters`           | string[]    | Sending ECU/node names        |
| `is_j1939`               | bool        | J1939 protocol frame          |
| `is_complex_multiplexed` | bool        | Complex multiplexing          |
| `mux_names`              | object      | Multiplexer name mapping      |
| `attributes`             | object      | Frame-level custom attributes |


### Signal Object (full) — additional fields

```json
{
  "name": "VehicleSpeed",
  "start_bit": 8,
  "bit_length": 16,
  "factor": "0.01",
  "offset": "0",
  "min": "0",
  "max": "655.35",
  "is_big_endian": false,
  "is_signed": false,
  "is_float": false,
  "is_ascii": false,
  "unit": "km/h",
  "comment": "Vehicle speed",
  "comments": {},
  "attributes": { "GenSigStartValue": 0 },
  "initial_value": "0",
  "values": { "0": "Off", "1": "On" },
  "is_multiplexer": false,
  "mux_value": null,
  "multiplex": null,
  "muxer_for_signal": null,
  "mux_val_grp": [],
  "receivers": ["BMS", "EPS"]
}
```


| Field            | Type         | Description                               |
| ---------------- | ------------ | ----------------------------------------- |
| `min`            | string/float | Minimum physical value                    |
| `max`            | string/float | Maximum physical value                    |
| `unit`           | string       | Physical unit                             |
| `comment`        | string/null  | Signal description                        |
| `comments`       | object       | Per-language comments                     |
| `attributes`     | object       | Signal-level custom attributes            |
| `initial_value`  | string/float | Default value                             |
| `values`         | object       | Value table: `{ "raw_int_str": "label" }` |
| `is_multiplexer` | bool         | Mux selector signal                       |
| `mux_value`      | int/null     | Mux selector value                        |
| `receivers`      | string[]     | Receiving ECU/node names                  |


### Define Object

Entries in `signal_defines`, `frame_defines`, `global_defines`, etc.:

```json
{ "name": "GenSigStartValue", "define": "INT 0 65535", "default": "0", "type": "INT" }
```

---

## Bit Numbering

Canmatrix JSON uses **LSB bit numbering** (default `jsonMotorolaBitFormat=lsb`):

- **Little-endian (Intel):** `start_bit` is the LSB position in vector bit numbering.
- **Big-endian (Motorola):** `start_bit` is also in LSB format.

### Vector Bit Numbering Layout (8-byte frame)

```
Byte:   0        1        2        3        4        5        6        7
Bit:  7..0    15..8    23..16   31..24   39..32   47..40   55..48   63..56
```

## Multiplexing

- Simple: one signal has `is_multiplexer: true`, others have `multiplex: "mux_value"`.
- Complex: `is_complex_multiplexed: true` on the frame, with `mux_names`, `muxer_for_signal`, and `mux_val_grp` on signals.

