# Delivery Notes

## WhatsApp

- Prefer PNG for reliable delivery.
- For sticker-like behavior, generate 512x512 output and send the PNG without caption.
- Keep WEBP as an optional artifact until native sticker upload is verified.

## Native sticker caveat

Current OpenClaw WhatsApp outbound behavior sends generated files as media/image, not verified native custom sticker upload. Use sticker-like image delivery unless the WhatsApp outbound layer is patched to send `{ sticker: mediaBuffer }` payloads.
