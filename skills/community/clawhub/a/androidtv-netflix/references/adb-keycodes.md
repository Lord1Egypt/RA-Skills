# ADB Keycode Reference

Common keycodes for controlling Android TV via `adb shell input keyevent <code>`.

## Navigation

| Key | Code | Description |
|-----|------|-------------|
| D-pad Up | 19 | Navigate up |
| D-pad Down | 20 | Navigate down |
| D-pad Left | 21 | Navigate left |
| D-pad Right | 22 | Navigate right |
| D-pad Center | 23 | Select / confirm |
| Back | 4 | Go back |
| Home | 3 | Go to home screen |
| Enter | 66 | Confirm input |

## Media

| Key | Code | Description |
|-----|------|-------------|
| Play/Pause | 85 | Toggle play/pause |
| Play | 126 | Start playback |
| Pause | 127 | Pause playback |
| Stop | 86 | Stop playback |
| Fast Forward | 90 | Fast forward |
| Rewind | 89 | Rewind |
| Next | 87 | Next track |
| Previous | 88 | Previous track |

## Volume

| Key | Code | Description |
|-----|------|-------------|
| Volume Up | 24 | Increase volume |
| Volume Down | 25 | Decrease volume |
| Mute | 164 | Toggle mute |

## Power & System

| Key | Code | Description |
|-----|------|-------------|
| Power | 26 | Power on/off |
| Sleep | 223 | Put device to sleep |
| Wake Up | 224 | Wake device |
| Menu | 82 | Open menu |
| Search | 84 | Open search |

## Text Input

Use `adb shell input text "hello"` for typing text directly.
