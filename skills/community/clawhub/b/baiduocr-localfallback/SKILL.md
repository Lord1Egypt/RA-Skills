# BaiduOCR-LocalFallback

> **Disclaimer**:
> 1. This project is not an official Baidu product and has no affiliation with Baidu. This project only provides a wrapper for Baidu OCR API; users must apply for a Baidu Cloud account and comply with Baidu's terms of service.
> 2. This project is 99% AI-generated. The AI's owner has no programming background. Please evaluate the project's feasibility before use.


**115+ Baidu OCR API interfaces with EasyOCR local fallback — auto-switches to local recognition when the network is unstable.**

## Features

- ✅ **115+ OCR APIs** - General, ID cards, receipts, documents, education, and more
- ✅ **Local fallback** - Integrates EasyOCR; auto-switches when Baidu OCR is unavailable
- ✅ **Image preprocessing** - Auto compresses and converts to fit the 4MB limit
- ✅ **Token caching** - access_token cached for 25 days
- ✅ **Auto retry** - Retries 3 times on network fluctuations
- ✅ **Multiple config methods** - Environment variables, config file, or interactive setup

## Installation

### One-click install

```bash
bash <(curl -s https://raw.githubusercontent.com/xx235300/BaiduOCR-LocalFallback/main/install.sh)
```

### Manual install

```bash
# 1. Clone the repo
git clone https://github.com/xx235300/BaiduOCR-LocalFallback.git
cd BaiduOCR-LocalFallback

# 2. Install dependencies
pip3 install -r requirements.txt

# 3. Configure API credentials
python3 scripts/ocr.py --configure
```

## Quick Start

```python
from scripts.ocr import OCR

ocr = OCR()

# General text recognition
result = ocr.recognize(image="/path/to/image.jpg", api="general_basic")

# ID card recognition
result = ocr.recognize(image="/path/to/idcard.jpg", api="idcard", id_card_side="front")

# Handwriting (local fallback)
result = ocr.recognize(image="/path/to/handwriting.jpg", api="handwriting")
```

## Supported APIs

### General Text
| API | Description |
|-----|-------------|
| `general` | General text (with location) |
| `general_basic` | General text (basic) |
| `accurate` | High-accuracy (with location) |
| `accurate_basic` | High-accuracy (basic) |

### ID & Cards
| API | Description |
|-----|-------------|
| `idcard` | ID card |
| `bankcard` | Bank card |
| `passport` | Passport |
| `business_license` | Business license |

### Receipts
| API | Description |
|-----|-------------|
| `receipt` | General receipt |
| `vat_invoice` | VAT invoice |
| `taxi_receipt` | Taxi receipt |
| `train_ticket` | Train ticket |
| `invoice` | Invoice |

### Handwriting / Documents
| API | Description |
|-----|-------------|
| `handwriting` | Handwriting recognition |
| `table` | Table recognition |
| `formula` | Formula recognition |

### More APIs (115+)
Run `python3 scripts/ocr.py --show-apis` for the full list.

## Configuration

### Method 1: Interactive
```bash
python3 scripts/ocr.py --configure
```

### Method 2: Environment variables (recommended for security)
```bash
export BAIDU_OCR_API_KEY="<your_api_key>"
export BAIDU_OCR_SECRET_KEY="<your_secret_key>"
```

### Method 3: Config file
```bash
mkdir -p ~/.openclaw/skills/BaiduOCR-LocalFallback
cat > ~/.openclaw/skills/BaiduOCR-LocalFallback/config.json << 'EOF'
{
  "api_key": "<your_api_key>",
  "secret_key": "<your_secret_key>"
}
EOF
chmod 600 ~/.openclaw/skills/BaiduOCR-LocalFallback/config.json
```

## Response Format

```json
{
  "words_result": [
    {"words": "Recognized text", "location": {"vertices": [{"x": 0, "y": 0}, ...]}}
  ],
  "words_result_num": 1,
  "fallback_info": {  // only present when using local fallback
    "engine": "EasyOCR",
    "message": "Baidu OCR unavailable, using local EasyOCR"
  }
}
```

## Error Handling

```python
from scripts.ocr import OCR
from scripts.baidu_client import BaiduOCRError

ocr = OCR()
try:
    result = ocr.recognize(image="/path/to/image.jpg")
except BaiduOCRError as e:
    print(f"Baidu OCR error: {e.error_code} - {e.error_msg}")
except Exception as e:
    print(f"Other error: {e}")
```

## FAQ

### Q: I have no coding experience, what should I do if an error occurs during use?

Just send the cloud document link to the AI and let it troubleshoot and find a solution on its own.
Sample prompt:
```
Please troubleshoot and resolve the issue according to the skill usage documentation.
Skill Usage Documentation: https://my.feishu.cn/docx/Gjy0djSado5YqVxzO6ecYbOmn4g?from=from_copylink
```

### Q: How to get Baidu OCR API credentials?

1. Go to [Baidu Cloud Console](https://console.bce.baidu.com/)
2. Search "OCR" or "文字识别"
3. Create an app and enable the OCR services you need
4. Get API Key and Secret Key from "My Apps"

### Q: "Baidu OCR call failed" but no auto-switch to local fallback?

Check if fallback is disabled:
```python
ocr = OCR(use_fallback=False)  # Fallback disabled
```

### Q: EasyOCR initialization is slow?

First run requires downloading models (~100MB). Pre-initialize:
```python
from scripts.local_ocr import local_ocr
local_ocr._init_reader()  # Warm up
```

### Q: How to handle Base64 images?

```python
import base64

# Read image and convert to Base64
with open("image.jpg", "rb") as f:
    img_base64 = base64.b64encode(f.read()).decode()

result = ocr.recognize(image=img_base64, api="general_basic")
```

### Q: How to specify output format?

```python
# Table - returns Excel
result = ocr.recognize(image="table.jpg", api="table", request_type="excel")

# Table - returns JSON
result = ocr.recognize(image="table.jpg", api="table", request_type="json")
```

### Q: Web image recognition failed?

Web images must be publicly accessible. Ensure:
1. Image URL is publicly reachable
2. Firewall allows outbound 80/443
3. Try downloading locally first

### Q: How to disable SSL certificate verification (dev only)?

```python
import os
os.environ['REQUESTS_CA_BUNDLE'] = '/path/to/ca-bundle.crt'
```

## Performance Tips

- First-time EasyOCR requires downloading models (~100MB), please be patient
- Recommended image size under 2MB for best performance
- Large images are auto-compressed and scaled
- access_token is auto-cached and refreshed

## Related Documents
[Baidu Cloud Documentation Center](https://cloud.baidu.com/doc/OCR/s/Ck3h7y2ia)

## License

MIT © 2026 xx235300

