# OpenRouter OCR Skill

## Overview

This skill provides OCR (Optical Character Recognition) functionality using models available via OpenRouter. It uses the OpenAI Python library to communicate with OpenRouter's API, specifically designed for models like Baidu's Qianfan OCR.

## Quick Start

When you need to extract text from an image:

1. **Ensure prerequisites**: 
   - Python 3.x installed
   - Required packages: `openai`, `requests` (install via `pip install openai requests`)
   - Place your OpenRouter API key in the file: `C:\Users\Administrator\.openclaw\secrets\openrouter.env`
     (format: `OPENROUTER_API_KEY=your_key_here`)

2. **Call the OCR script** with an image URL or local file path:
   ```bash
   python ocr.py <image_input> [prompt]
   ```
   - `image_input`: Either a URL or a local file path to the image
   - `prompt`: Optional text prompt for the OCR (default: "OCR提取图片所有文字")

3. **Get result**: The script prints the extracted text to stdout.

## Usage Examples

### Basic Usage with Default Prompt
```bash
python ocr.py "https://example.com/image.jpg"
```

### Custom Prompt
```bash
python ocr.py "https://example.com/image.jpg" "请识别图片中的所有文字"
```

### Local Image File
```bash
python ocr.py "C:\path\to\image.jpg"
```

## How It Works

The skill uses the OpenAI client configured with:
- Base URL: `https://openrouter.ai/api/v1`
- Model: `baidu/qianfan-ocr-fast:free` (configurable via environment variable)
- API Key: Read from `OPENROUTER_API_KEY` environment variable

It sends a multimodal request containing:
1. A text prompt (default: "OCR提取图片所有文字")
2. The image (encoded as base64 if local, or passed directly if URL)

The model returns the extracted text which is printed to console.

## Environment Variables

- `OPENROUTER_API_KEY`: **Required** - Your OpenRouter API key
- `OCR_MODEL`: Optional - Model to use (default: `baidu/qianfan-ocr-fast:free`)
- `OCR_BASE_URL`: Optional - OpenRouter base URL (default: `https://openrouter.ai/api/v1`)

## Installation

1. Create the skill directory: `mkdir -p skills/openrouter-ocr`
2. Save the `ocr.py` script in this directory
3. Install dependencies: `pip install openai requests`
4. Set your OpenRouter API key: 
   ```bash
   setx OPENROUTER_API_KEY "your_api_key_here"
   ```
   (Restart terminal after setting)

## Notes

- The skill works with both HTTP/HTTPS URLs and local file paths
- For local files, the image is read and base64-encoded before sending
- Error handling includes network issues, invalid API keys, and model errors
- The default model is Baidu's Qianfan OCR fast version (free tier)
- You can change the model by setting the `OCR_MODEL` environment variable
- Response time depends on image size and model speed

## Troubleshooting

- **API Key Error**: Ensure `OPENROUTER_API_KEY` is set correctly
- **Module Not Found**: Install required packages with `pip install openai requests`
- **Image Access**: Verify the image URL is accessible or local path exists
- **Model Not Available**: Check if the specified model is available on OpenRouter

## Example Output

```
✅ OCR 识别结果：
------------------------------------------------------------
这是识别出的文本内容
...
------------------------------------------------------------
```

## Security Note

Never commit your API key to version control. Keep it secure in environment variables.