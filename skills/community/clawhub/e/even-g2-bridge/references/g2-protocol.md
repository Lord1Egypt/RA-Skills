# G2 Protocol Reference

## G2 "Add Agent" API Format

The Even Realities G2 app sends requests in OpenAI Chat Completions format:

```
POST {Agent URL}
Authorization: Bearer {Token}
Content-Type: application/json
User-Agent: Dart/3.8 (dart:io)

{
  "model": "openclaw",
  "messages": [
    {"role": "user", "content": "transcribed voice text"}
  ]
}
```

Expected response: standard OpenAI Chat Completion JSON.

## G2 Display Specs

- **Resolution**: 576 × 136 pixels
- **Color**: 1-bit monochrome (green laser projection)
- **Brightness**: up to 1200 nits
- **Usable text width**: ~488 pixels (~48 monospace characters)
- **Usable lines**: ~8 lines
- **Supports**: Plain text only
- **Does NOT support**: Images, markdown, clickable links

## Image Display (BLE only, not HTTP)

G2 can display 1-bit BMP images via BLE protocol (0x15 command), but this is
NOT available through the HTTP "Add Agent" API. Image display requires direct
BLE connection from a phone app.

## Even Hub SDK

Even Hub V0.0.7+ includes an OpenClaw integration pilot. The SDK provides
additional capabilities beyond the "Add Agent" HTTP API.

- SDK docs: https://evenhub.evenrealities.com/
- Community: https://discord.gg/arDkX3pr (Even Realities Discord)

## Key Resources

- Official Demo App: https://github.com/even-realities/EvenDemoApp
- BLE Protocol RE: https://github.com/i-soxi/even-g2-protocol
