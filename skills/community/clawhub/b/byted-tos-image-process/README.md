# Bytedance TOS Image Process Skill

This skill enables an agent to perform basic image processing tasks on files stored in Bytedance's TOS (TeraObjectStore) by directly using the Volcengine TOS Python SDK.

## Overview

The skill allows an agent to perform various image processing operations by constructing a `process` string and passing it to the TOS SDK. Key capabilities include:

1.  **Get Image Information**: Retrieve metadata like format, size, and EXIF info (`image/info`).
2.  **Format Conversion**: Convert images between formats like JPG, PNG, and WebP (`image/format`).
3.  **Resizing**: Scale images with various modes (`image/resize`).
4.  **Watermarking**: Apply text or image watermarks (`image/watermark`).
5.  **Blind Watermarking**: Embed or extract blind watermarks (`image/blindwatermark`).
6.  **Generic Processing**: A general-purpose entry point to support any other `image/...` operations available in TOS.

All operations support saving the output locally or persisting it back to a TOS bucket.

## Skill Structure

```
byted-tos-image-process/
├── SKILL.md              # Main skill file with quick start and core operations
├── README.md             # This file: detailed setup and environment guide
├── REFERENCE.md          # Complete parameter reference for each operation
├── WORKFLOWS.md          # Common end-to-end workflow examples
├── scripts/              # Executable Python scripts demonstrating each core capability
│   ├── image_info.py         # Script to get image information
│   ├── image_format.py       # Script for format conversion
│   ├── image_resize.py       # Script for resizing
│   ├── image_watermark.py    # Script for visible watermarks
│   ├── image_blindwatermark.py # Script for blind watermarks
│   └── image_process.py      # Generic script for any image process string
├── requirements.txt      # Python dependencies for the scripts
```

## Setup and Configuration

### Requirements
- Python 3.7+
- `tos` Python SDK

### Installation

Install the necessary Python library:
```bash
pip install tos
```

### Environment Variables

All scripts rely on environment variables for configuration.

| Variable                 | Description                                                  | Example                                    |
| ------------------------ | ------------------------------------------------------------ | ------------------------------------------ |
| `TOS_ACCESS_KEY`         | Your Access Key ID for TOS authentication.                   | `AKL...`                                   |
| `TOS_SECRET_KEY`         | Your Secret Access Key for TOS authentication.               | `your-secret-key`                          |
| `TOS_SECURITY_TOKEN`     | (Optional) The session token for temporary STS credentials.  | `STS...`                                   |
| `TOS_ENDPOINT`           | The full URL of the TOS service endpoint.                    | `https://tos-cn-beijing.volces.com`        |
| `TOS_REGION`             | The region of the TOS service.                               | `cn-beijing`                               |
| `TOS_BUCKET`             | The name of the bucket where the target image is stored.     | `my-image-assets`                          |
| `TOS_OBJECT_KEY`         | The full path (key) of the image file within the bucket.     | `input/photos/landscape.jpg`               |
| `MAX_OBJECT_SIZE`        | (Optional) Safeguard for local file size, in bytes.          | `262144` (default)                         |
| `TOS_SAVEAS_BUCKET`      | (Optional) The default bucket to save processed results into.| `my-processed-images`                      |
| `TOS_SAVEAS_OBJECT_PREFIX`| (Optional) A prefix for the object key when saving results.  | `output/resized/`                          |

**Security Note**: For production environments, use short-lived STS (Security Token Service) credentials. The SDK automatically uses `TOS_SECURITY_TOKEN` if present.

## Quick Start

### 1. Set Environment Variables

```bash
# --- Required ---
export TOS_ACCESS_KEY="YOUR_AK"
export TOS_SECRET_KEY="YOUR_SK"
export TOS_ENDPOINT="https://tos-cn-beijing.volces.com"
export TOS_REGION="cn-beijing"
export TOS_BUCKET="your-image-bucket"
export TOS_OBJECT_KEY="path/to/your/image.jpg"
```

### 2. Run Example Scripts

The `scripts/` directory contains ready-to-run examples.

**Get Image Info:**
```bash
python3 scripts/image_info.py
```

**Convert Image to WebP with Quality 80:**
```bash
python3 scripts/image_format.py --f webp --q 80 --output converted.webp
```

**Resize Image to 500px Width:**
```bash
python3 scripts/image_resize.py --w 500 --output resized.jpg
```

**Add a Text Watermark and Save back to TOS:**
```bash
# Parameters `type`, `text`, `size` etc., are passed via --kv
# The keys and values must match TOS API documentation for image watermarks.
# NOTE: Text for watermarks must be Base64-encoded.
TEXT_B64=$(echo -n "© My Brand" | base64)

python3 scripts/image_watermark.py \
  --kv type=1 \
  --kv text=${TEXT_B64} \
  --kv fill=I0ZGRkZGRg== \
  --kv size=40 \
  --kv p=9 \
  --saveas-bucket "your-output-bucket" \
  --saveas-object "watermarked/image.jpg"
```

**Use the Generic Processor:**
This script allows you to pass any valid process string.
```bash
python3 scripts/image_process.py \
  --process "image/resize,w_300,h_300,m_fill" \
  --output "filled_300x300.jpg"
```

## Note on Parameters

The specific key-value pairs for image processing (`format`, `resize`, `watermark`, etc.) are defined by the TOS service. **This skill's scripts provide common arguments (`--w`, `--h`, `--f`, etc.) for convenience, but all other parameters must be passed using the `--kv key=value` syntax.** Always refer to the official Volcengine TOS documentation for the most up-to-date and complete list of parameters for each image processing operation.
