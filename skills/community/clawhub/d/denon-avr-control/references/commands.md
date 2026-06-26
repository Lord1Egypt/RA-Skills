# Denon AVR IP Control Notes

Use these command patterns for Denon/Marantz-style IP control when the receiver supports the classic protocol.

## Transport

- **TCP:** plain ASCII commands to port `23`, terminated with carriage return (`\r`)
- **HTTP:** `GET /goform/formiPhoneAppDirect.xml?<COMMAND>` on port `80`

Prefer TCP first. Use HTTP if telnet-style control is disabled or unavailable.

## Common commands

### Power

- `PWON`
- `PWSTANDBY`
- `PW?`

### Mute

- `MUON`
- `MUOFF`
- `MU?`

### Main volume

- `MVUP`
- `MVDOWN`
- `MV?`
- `MV35` → set volume to 35
- `MV355` → set volume to 35.5

### Input select

Common examples:

- `SITV`
- `SIBD`
- `SIGAME`
- `SINET`
- `SICD`
- `SIDVD`
- `SIAUX1`
- `SIAUX2`
- `SIBLUETOOTH`
- `SIPHONO`
- `SITUNER`
- `SISAT/CBL`
- `SI?`

Actual available inputs can vary by model and configuration.

### Sound mode

Examples:

- `MSSTEREO`
- `MSDIRECT`
- `MSPURE DIRECT`
- `MSMOVIE`
- `MSMUSIC`
- `MSGAME`
- `MSAUTO`
- `MSDOLBY AUDIO - DOLBY SURROUND`
- `MS?`

Sound mode strings vary more by model than power/volume/input commands. If a write fails, query first with `MS?` and then use `--raw` for model-specific values.

## Response shape

Many devices echo a state string like:

- `PWON`
- `MUOFF`
- `MV45`
- `SITV`

Some writes return no body on success, especially over HTTP.

## Practical workflow

1. Confirm reachability to the receiver host/IP.
2. Query state first with `PW?`, `MV?`, `SI?`, `MS?`.
3. Send one mutating command at a time.
4. If the model behaves differently, fall back to `--raw` with exact strings.
