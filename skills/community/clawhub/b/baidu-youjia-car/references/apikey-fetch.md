# Baidu Youjia Car API Key Setup Guide (OpenClaw)

## BAIDU_API_KEY Not Configured

When the `BAIDU_API_KEY` environment variable is not set, follow these steps:

### 1. Get API Key
Visit: **https://console.bce.baidu.com/qianfan/ais/console/apiKey**

- Log in to your Baidu Cloud account
- Create an application or view existing API keys
- Copy your **API Key** (only API Key is needed, no Cookie required)

### 2. Configure OpenClaw
Edit the OpenClaw configuration file: `~/.openclaw/openclaw.json`

Add or merge the following structure:

```json
{
  "skills": {
    "entries": {
      "baidu-youjia-car": {
        "env": {
          "BAIDU_API_KEY": "your_actual_api_key_here"
        }
      }
    }
  }
}
```

Replace `"your_actual_api_key_here"` with your actual API key.

### 3. Verify Configuration
```bash
# Check JSON format
cat ~/.openclaw/openclaw.json | python -m json.tool
```

### 4. Restart OpenClaw
```bash
openclaw gateway restart
```

### 5. Test
```bash
cd ~/.openclaw/workspace/skills/baidu-youjia-car
python3 scripts/askprice.py '{"query":"奥迪A4L多少钱"}'
```

## API Details

- **Endpoint**: `https://qianfan.baidubce.com/v2/tools/clue/askprice`
- **Method**: GET
- **Authentication**: Bearer token in Authorization header
- **Parameters**:
  - `query` (required): 查询内容，必须包含车系名
  - `city` (optional): 城市名，默认北京

### Example Request
```bash
curl --location 'https://qianfan.baidubce.com/v2/tools/clue/askprice?query=奥迪A4L多少钱' \
  --header 'Authorization: Bearer your_api_key_here'
```

## Troubleshooting
- Ensure `~/.openclaw/openclaw.json` exists with correct JSON format
- Confirm API key is valid and the service is activated
- Check account balance on Baidu Cloud
- Restart OpenClaw after configuration changes
- Note: Cookie is NOT required, only the Authorization header with API Key

**Recommended**: Use OpenClaw configuration file for centralized management
