# Tool Selection Notes

Use the first available backend that matches the requested output:

- `cwebp`: best default for `webp` output and aggressive size reduction
- `magick` or `convert`: best when format conversion or more flexible processing is needed
- `sips`: macOS-native fallback when no other compressor is installed

Recommended defaults:

- social upload or preview images: `webp` at quality `75-82`
- email or blog assets that need broad compatibility: `jpeg` at quality `80-85`
- repeated local optimization runs: write outputs into a separate `compressed/` directory to avoid double-compression
