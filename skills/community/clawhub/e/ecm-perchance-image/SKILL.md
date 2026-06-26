# ecm-perchance-image.py

## Description
A Web Browser skill that sends text prompts to Perchance.org and displays the resulting images.

## Usage

### In OpenClaw:
1. Open the skill folder: `C:\Users\evstr\.openclaw\workspace\skills\ecm-perchance-image`
2. Run: `openclaw run --cwd=skills/ecm-perchance-image/`
3. Enter your prompt and click "Generate Image"
4. View generated images in the web browser

## API Endpoint
https://perchance.org/new-image-gen-by-rs118

## API Parameters
- **prompt**: text string (required) - Type a detailed prompt here...
- **orientation**: string, optional, default: "landscape" - Options: landscape, portrait, square

## Current Status
✅ Enhanced with error handling
✅ Multiple image generation support
✅ Progress indicators
✅ User-friendly error messages
✅ Terminal support for OpenClaw

## Notes
- Perchance.org API may have rate limits
- Try different prompt parameters to find what works best
- You can customize orientation (portrait, square, landscape)

