#!/usr/bin/env python3
"""
Vision analysis module for screen-vision skill.
Sends screenshots to AI vision API and returns structured action instructions.
"""

import base64
import json
import sys
import os

# Prompt template for screen analysis
SCREEN_ANALYSIS_PROMPT = """You are a computer screen analyst. Analyze this screenshot and help complete the user's task.

## Current Task
{task}

## Step History
{history}

## Instructions
1. Describe what you see on the screen
2. Determine the next action to complete the task
3. Return ONLY a JSON response in this exact format:

```json
{{
  "screen_description": "Brief description of current screen state",
  "task_progress": "What has been done so far",
  "next_action": {{
    "type": "click|type|key|scroll|drag|wait|done|failed",
    "x": 0,
    "y": 0,
    "text": "",
    "button": "left|right",
    "direction": "up|down",
    "amount": 300,
    "reason": "Why this action"
  }},
  "confidence": 0.0-1.0
}}
```

## Action Types
- **click**: Click at (x, y). Include x, y, button.
- **type**: Type text. Include text field.
- **key**: Press a key. Include text field (e.g. "Return", "Tab", "Escape").
- **scroll**: Scroll. Include direction and amount.
- **drag**: Drag. Include x1, y1, x2, y2.
- **wait**: Wait for screen to update. No other fields needed.
- **done**: Task is complete. No other fields needed.
- **failed**: Cannot complete task. Include reason in text field.

Be precise with coordinates. The screen resolution is {resolution}.
If the task is already complete, return type "done".
If you cannot proceed, return type "failed" with explanation.
"""


def encode_image(image_path):
    """Encode image file to base64."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def call_vision_api(image_path, task, history="", resolution="1024x768",
                    provider_config=None):
    """
    Call vision API with screenshot and task context.
    
    Args:
        image_path: Path to screenshot
        task: Current task description
        history: Previous actions taken
        resolution: Screen resolution string
        provider_config: Dict with provider settings
    
    Returns:
        dict: Parsed action from AI response
    """
    if provider_config is None:
        provider_config = get_default_config()
    
    # Validate config before encoding image to avoid unnecessary I/O
    base_url = provider_config.get("baseUrl", "")
    api_key = provider_config.get("apiKey", "")

    if not base_url or not api_key or not provider_config.get("model"):
        missing = []
        if not base_url:
            missing.append("baseUrl")
        if not api_key:
            missing.append("apiKey")
        if not provider_config.get("model"):
            missing.append("model")
        return {"error": f"Vision API not configured. Missing: {', '.join(missing)}. Please set config.json or environment variables. See references/API_CONFIG.md for help."}

    prompt = SCREEN_ANALYSIS_PROMPT.format(
        task=task,
        history=history or "No actions taken yet.",
        resolution=resolution
    )
    
    img_b64 = encode_image(image_path)
    
    payload = {
        "model": provider_config.get("model", ""),
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/png;base64,{img_b64}"
                }}
            ]
        }],
        "max_tokens": 1500
    }
    
    import urllib.request
    import urllib.error
    
    url = f"{base_url}/chat/completions"
    data = json.dumps(payload).encode()
    
    headers = {
        "Content-Type": "application/json",
    }
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    req = urllib.request.Request(url, data=data, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode())
            content = result["choices"][0]["message"]["content"]
            return parse_action(content)
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()[:500]
        return {"error": f"API Error {e.code}: {error_body}"}
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}


def parse_action(content):
    """Parse AI response content to extract action JSON."""
    # Try to find JSON in response
    import re
    
    # Look for JSON block
    json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass
    
    # Try to find raw JSON
    json_match = re.search(r'\{[^{}]*\}', content, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except json.JSONDecodeError:
            pass
    
    # Return as description-only response
    return {
        "screen_description": content,
        "next_action": {
            "type": "done",
            "reason": "Could not parse structured action from AI response"
        },
        "confidence": 0.3
    }


def get_default_config():
    """Get default vision provider config from environment or config file."""
    # Try environment variables first
    api_key = os.environ.get("SV_VISION_API_KEY", "")
    base_url = os.environ.get("SV_VISION_BASE_URL", "")
    model = os.environ.get("SV_VISION_MODEL", "")

    if api_key or base_url or model:
        return {
            "provider": os.environ.get("SV_VISION_PROVIDER", ""),
            "baseUrl": base_url,
            "apiKey": api_key,
            "model": model
        }
    
    # Try config file
    config_paths = [
        os.path.expanduser("~/.openclaw/workspace/skills/screen-vision/config.json"),
        "/etc/screen-vision/config.json"
    ]
    
    for path in config_paths:
        if os.path.exists(path):
            try:
                with open(path) as f:
                    config = json.load(f)
                return config.get("vision", config)
            except:
                pass
    
    return {
        "provider": "",
        "baseUrl": "",
        "apiKey": "",
        "model": ""
    }


if __name__ == "__main__":
    # CLI usage for testing
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True, help="Screenshot path")
    parser.add_argument("--task", required=True, help="Task description")
    parser.add_argument("--history", default="", help="Action history")
    parser.add_argument("--resolution", default="1024x768")
    args = parser.parse_args()
    
    result = call_vision_api(
        args.image, args.task, args.history, args.resolution
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
