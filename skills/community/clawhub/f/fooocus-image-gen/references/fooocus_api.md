# Fooocus Gradio API Reference

Fooocus exposes a Gradio API that can be accessed programmatically.

## Base URL

```
http://localhost:7865
```

## Endpoints

### GET /api/info

Returns information about available API functions.

**Response:**
```json
{
  "fn_index": 13,
  "fn_name": "generate",
  "inputs": [...],
  "outputs": [...]
}
```

### POST /api/predict

Main generation endpoint.

**Request:**
```json
{
  "fn_index": 13,
  "data": [
    "prompt",           // string: Positive prompt
    "negative_prompt",  // string: Negative prompt
    ["style1"],         // array: Selected styles
    "Quality",          // string: Performance setting
    1024,               // int: Width
    1024,               // int: Height
    1,                  // int: Number of images
    -1,                 // int: Seed (-1 for random)
    2.0,                // float: Sharpness
    4.0,                // float: Guidance scale
    "dpmpp_2m_sde_gpu", // string: Sampler
    "karras",           // string: Scheduler
    "",                 // string: Override model
    null,               // string: Input image (base64)
    null,               // string: Input mask (base64)
    false,              // bool: Advanced parameters
    null,               // float: Refiner switch at
    null                // string: Refiner model
  ]
}
```

**Response:**
```json
{
  "data": [
    "data:image/png;base64,....",  // Generated image
    "...",                         // Metadata
    "..."                          // Additional info
  ]
}
```

## Function Indices

Note: Function indices may vary by Fooocus version. Use `/api/info` to discover.

Common indices (v2.x):
- `13`: Main text-to-image generation
- `65`: Vary (Subtle)
- `66`: Vary (Strong)
- `67`: Upscale
- `68`: Inpaint
- `69`: Outpaint

## Authentication

By default, Fooocus does not require authentication for local access.

To enable authentication, start with:
```bash
python entry_with_update.py --share
```

Or set Gradio auth:
```bash
python entry_with_update.py --gradio-auth username:password
```

## Python Client Example

```python
import requests
import json
import base64

def generate_image(prompt, host="localhost", port=7865):
    url = f"http://{host}:{port}/api/predict"
    
    payload = {
        "fn_index": 13,
        "data": [
            prompt,           # prompt
            "",               # negative prompt
            ["Fooocus V2"],   # styles
            "Quality",        # performance
            1024, 1024,       # width, height
            1,                # num images
            -1,               # seed
            2.0,              # sharpness
            4.0,              # guidance
            "dpmpp_2m_sde_gpu", # sampler
            "karras",         # scheduler
            "",               # override model
            None,             # input image
            None,             # input mask
            False,            # advanced
            None,             # refiner switch
            None              # refiner model
        ]
    }
    
    response = requests.post(url, json=payload)
    result = response.json()
    
    # Extract image
    image_data = result["data"][0]
    if image_data.startswith("data:image"):
        image_data = image_data.split(",")[1]
    
    # Save
    with open("output.png", "wb") as f:
        f.write(base64.b64decode(image_data))
    
    return "output.png"

# Usage
generate_image("a beautiful sunset over mountains")
```

## JavaScript/Node.js Example

```javascript
const axios = require('axios');
const fs = require('fs');

async function generateImage(prompt) {
  const response = await axios.post('http://localhost:7865/api/predict', {
    fn_index: 13,
    data: [
      prompt,           // prompt
      "",               // negative prompt
      ["Fooocus V2"],   // styles
      "Quality",        // performance
      1024, 1024,       // width, height
      1,                // num images
      -1,               // seed
      2.0,              // sharpness
      4.0,              // guidance
      "dpmpp_2m_sde_gpu", // sampler
      "karras",         // scheduler
      "",               // override model
      null,             // input image
      null,             // input mask
      false,            // advanced
      null,             // refiner switch
      null              // refiner model
    ]
  });
  
  const imageData = response.data.data[0];
  const base64Data = imageData.replace(/^data:image\/png;base64,/, '');
  fs.writeFileSync('output.png', base64Data, 'base64');
  
  return 'output.png';
}

// Usage
generateImage("a beautiful sunset over mountains");
```

## cURL Example

```bash
# Generate image
curl -X POST http://localhost:7865/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "fn_index": 13,
    "data": [
      "a beautiful sunset",
      "",
      ["Fooocus V2"],
      "Quality",
      1024, 1024,
      1, -1, 2.0, 4.0,
      "dpmpp_2m_sde_gpu",
      "karras",
      "", null, null,
      false, null, null
    ]
  }'
```

## Error Handling

Common errors:

### Connection Refused
```
Error: Cannot connect to Fooocus
```
**Solution:** Start Fooocus first: `python entry_with_update.py`

### Out of Memory
```
RuntimeError: CUDA out of memory
```
**Solution:** Reduce image size or use `--always-low-vram` flag

### Model Not Found
```
FileNotFoundError: checkpoint not found
```
**Solution:** Models download automatically on first run, or use `--preset` to switch

## Queue System

Fooocus uses Gradio's queue system. For multiple concurrent requests:

1. Enable queue: `--enable-queue` (default in recent versions)
2. Adjust concurrency: `--concurrency-count 2`
3. Check queue status via WebSocket at `ws://localhost:7865/queue/join`

## Advanced Usage

### Custom Model

```python
payload = {
    "fn_index": 13,
    "data": [
        "prompt",
        "",
        [],
        "Quality",
        1024, 1024,
        1, -1, 2.0, 4.0,
        "dpmpp_2m_sde_gpu",
        "karras",
        "custom_model.safetensors",  // Override model
        None, None,
        False, None, None
    ]
}
```

### Image-to-Image

```python
import base64

# Read input image
with open("input.png", "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode()

payload = {
    "fn_index": 13,
    "data": [
        "prompt describing transformation",
        "",
        ["Fooocus V2"],
        "Quality",
        1024, 1024,
        1, -1, 2.0, 4.0,
        "dpmpp_2m_sde_gpu",
        "karras",
        "",
        f"data:image/png;base64,{img_b64}",  // Input image
        None,
        False, None, None
    ]
}
```

### Inpainting

```python
# Read both image and mask
with open("image.png", "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode()
with open("mask.png", "rb") as f:
    mask_b64 = base64.b64encode(f.read()).decode()

payload = {
    "fn_index": 68,  // Inpaint function
    "data": [
        f"data:image/png;base64,{img_b64}",
        f"data:image/png;base64,{mask_b64}",
        "prompt for inpainted area",
        "",
        ["Fooocus V2"],
        "Quality",
        2.0, 4.0,
        "dpmpp_2m_sde_gpu",
        "karras"
    ]
}
```

## Rate Limiting

No built-in rate limiting for local usage. For public deployments:

```bash
# Limit requests
python entry_with_update.py --max-file-size 10
```

## WebSocket Events

Connect to `ws://localhost:7865/queue/join` for real-time updates:

```javascript
const ws = new WebSocket('ws://localhost:7865/queue/join');

ws.onopen = () => {
  ws.send(JSON.stringify({
    fn_index: 13,
    data: [...]
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.msg === 'process_completed') {
    console.log('Generation complete!');
  }
};
```
