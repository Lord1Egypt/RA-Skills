# Pet Schema Notes (field reference)

Frequently-used **query response fields** and **set* inputs** for commands listed in [SKILL.md](../SKILL.md).

## Queries: common response fields

Returned fields live under `data.resp.body.data` (exact nesting may vary by envelope).

### `getPetState`

- **bindTs**: binding day timestamp
- **character**: persona (`gentle`, `happy_sunshine`, `clingy`, `sensitive`, `irritable`)
- **characterValue**: persona score (0–10)
- **nextCharacter** / **nextCharacterRequiredValue** / **lastCharacterChangeTs**: progression fields (may be absent on older firmware)

### `getVolume`

- **total**, **volume**: step counts
- **isAuto**: `1`/`true` = auto volume

### `getMicro` / `getCamera`

- **enable**: `0` off, `1` on

---

## Settings: `set*` inputs

Recommended unified names (gateway accepts `pet_*` aliases and camelCase variants).

| cmd | Input | Maps to |
|-----|-------|---------|
| `setMicro` / `setCamera` | `pet_enable` | `enable` |
| `setWakeTimeout` | `pet_timeout_seconds` | `timeout` |
| `setNickname` | `pet_wake_word` | `nickname` |
| `setPetGender` | `pet_gender` | `value` |
| `setVolume` | `pet_total`, `pet_volume`, `pet_auto` | `total` / `volume` / `isAuto` |

Boolean inputs: `0/1`, `true/false`, `on/off`.
