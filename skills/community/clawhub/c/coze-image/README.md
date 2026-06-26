# Coze Image Skill for OpenClaw

Generate images from text prompts using the Coze AI platform.

## Installation

### Via ClawHub (Recommended)

```bash
# Install ClawHub CLI if not already installed
npm install -g clawhub

# Install the skill
clawhub install coze-image

# Or sync to latest version
clawhub sync coze-image
```

### Manual Installation

Copy the skill folder to your OpenClaw skills directory:

```bash
# Windows
cp -r coze-image %APPDATA%\npm\node_modules\openclaw\skills\

# macOS/Linux
cp -r coze-image ~/.openclaw/skills/
```

## Configuration

Set the following environment variables in your OpenClaw configuration:

```bash
openclaw config set IMAGE_API_TOKEN your_coze_api_token
```

Optional configuration:

```bash
openclaw config set IMAGE_API_URL https://6fj9k4p9x3.coze.site/stream_run
openclaw config set IMAGE_API_PROJECT_ID 7621854258107039796
openclaw config set IMAGE_API_SESSION_ID mT8SQeCGgTMZNBsJEiRuN
openclaw config set IMAGE_API_TIMEOUT 60
```

## Usage

Once installed, you can generate images by simply asking:

```
Generate a picture of a cute cat playing on grass
```

Or use the skill directly:

```python
from coze_image_skill import run

result = run({
    "text": "a beautiful sunset over the ocean",
    "api_token": "your_token"  # Optional if env var is set
})

# Result contains Base64-encoded image
print(result["image"])  # data:image/jpeg;base64,...
```

## Features

- Text-to-image generation via Coze AI
- Automatic Base64 encoding for inline preview
- Support for custom Coze projects
- Graceful error handling
- Debug mode for troubleshooting

## Requirements

- Python 3.8+
- `requests` library
- Coze API access token

## License

MIT License

## Support

For issues or questions, please visit the ClawHub repository or OpenClaw community.
