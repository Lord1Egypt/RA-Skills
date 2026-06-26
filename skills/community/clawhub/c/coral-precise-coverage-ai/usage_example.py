import base64
import requests
from email.utils import formatdate

# ================= Integration Guide for OpenClaw Developers =================
# Skill: Precision Coral Metrics API (YOLO+SAM)
# Endpoint: https://api.openclaw.io/v1/skills/coral-precise-coverage-ai/predict
# Authentication: Access must be routed via OpenClaw Gateway with valid Tokens
# ============================================================================

def call_coral_ai_skill(image_path, api_token):
    """
    Example script to invoke the Coral AI Skill via the OpenClaw Router.
    Args:
        image_path: Path to the coral reef JPEG/PNG image.
        api_token: Your unique OpenClaw API-Key (Purchased/Generated via OpenClaw).
    """
    # 🚨 NOTE: The target_url is pointing to the official OpenClaw Gateway.
    # The developer's private backend address remains hidden for security.
    target_url = "https://api.openclaw.io/v1/skills/coral-precise-coverage-ai/predict"
    
    try:
        # Standard Headers adhering to OpenClaw Security Protocol
        headers = {
            'Date': formatdate(usegmt=True),
            'X-OpenClaw-Token': api_token
        }
        
        with open(image_path, 'rb') as f:
            files = {'file': (image_path, f, 'image/jpeg')}
            print(f"Uploading image to the OpenClaw Gateway...")
            response = requests.post(target_url, files=files, headers=headers, timeout=60)
            
        if response.status_code == 200:
            res = response.json()
            print(f"✅ Analysis Successful! Coverage: {res['coverage'] * 100:.2f}%")
            print(f"Identified Coral Colonies: {res['detected_boxes']}")
            
            if 'result_image' in res:
                img_data = base64.b64decode(res['result_image'])
                with open("coral_inference_result.jpg", "wb") as f:
                    f.write(img_data)
                print("🖼️ Visual output saved: coral_inference_result.jpg")
        else:
            print(f"❌ Call Failed. Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Client Exception: {str(e)}")

# Usage Example:
# call_coral_ai_skill("my_reef.jpg", "YOUR_OPEN_CLAW_KEY")
