"""
ComfyUI Custom Nodes - Alibaba Cloud Bailian Qwen Image 2.0
Install: Copy this file and bailian_image_gen.py to ComfyUI/custom_nodes/
"""

import os
import sys
import torch
import numpy as np
from PIL import Image
import io

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

def load_env_file():
    """Load environment variables from .env file"""
    possible_paths = [
        os.path.join(current_dir, '.env'),
        os.path.join(os.path.dirname(current_dir), '.env'),
        os.path.join(os.path.dirname(os.path.dirname(current_dir)), '.env'),
    ]
    
    for env_path in possible_paths:
        if os.path.exists(env_path):
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        if key and value and key not in os.environ:
                            os.environ[key] = value
            print(f"[BailianNode] Loaded .env: {env_path}")
            return

load_env_file()

try:
    from bailian_image_gen import QwenImageGenerator
except ImportError as e:
    print(f"[BailianNode] Warning: Cannot import bailian_image_gen: {e}")
    QwenImageGenerator = None


class BailianText2Image:
    """Bailian Text-to-Image Node"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": "A cute orange cat, high quality"}),
                "size": (["1024*1024", "1024*768", "768*1024", "2048*2048"], {"default": "1024*1024"}),
            },
            "optional": {
                "seed": ("INT", {"default": -1, "min": -1, "max": 2147483647}),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "generate"
    CATEGORY = "Bailian"
    
    def generate(self, prompt, size, seed=-1):
        if QwenImageGenerator is None:
            raise RuntimeError("bailian_image_gen module not loaded")
        
        try:
            client = QwenImageGenerator()
        except ValueError as e:
            raise RuntimeError(f"API Key error: {e}")
        
        seed_val = None if seed == -1 else seed
        
        print(f"[BailianNode] Text-to-Image: prompt='{prompt[:50]}...', size={size}")
        
        result = client.text_to_image(prompt=prompt, size=size, seed=seed_val)
        
        image_url = client.extract_image_url(result)
        if not image_url:
            raise RuntimeError(f"Cannot get image URL: {result}")
        
        print(f"[BailianNode] Image URL: {image_url[:60]}...")
        
        import requests
        headers = {"Authorization": f"Bearer {client.api_key}"}
        img_response = requests.get(image_url, headers=headers, timeout=60)
        img_response.raise_for_status()
        
        pil_image = Image.open(io.BytesIO(img_response.content))
        pil_image = pil_image.convert("RGB")
        
        image_np = np.array(pil_image).astype(np.float32) / 255.0
        image_tensor = torch.from_numpy(image_np).unsqueeze(0)
        
        print(f"[BailianNode] Generated: {pil_image.size}")
        
        return (image_tensor,)


class BailianImage2Image:
    """Bailian Image-to-Image Node"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "prompt": ("STRING", {"multiline": True, "default": "Modern minimalist living room, warm lighting, high quality product photography"}),
                "size": (["1024*1024", "1024*768", "768*1024", "2048*2048"], {"default": "1024*1024"}),
            },
            "optional": {
                "seed": ("INT", {"default": -1, "min": -1, "max": 2147483647}),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "generate"
    CATEGORY = "Bailian"
    
    def generate(self, image, prompt, size, seed=-1):
        if QwenImageGenerator is None:
            raise RuntimeError("bailian_image_gen module not loaded")
        
        try:
            client = QwenImageGenerator()
        except ValueError as e:
            raise RuntimeError(f"API Key error: {e}")
        
        seed_val = None if seed == -1 else seed
        
        if isinstance(image, torch.Tensor):
            image_np = image[0].cpu().numpy()
            image_np = (image_np * 255).astype(np.uint8)
            pil_image = Image.fromarray(image_np)
        else:
            pil_image = image
        
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            pil_image.save(tmp.name)
            temp_path = tmp.name
        
        try:
            print(f"[BailianNode] Image-to-Image: prompt='{prompt[:50]}...', size={size}")
            
            result = client.image_to_image(
                prompt=prompt, reference_image_path=temp_path, size=size, seed=seed_val
            )
            
            image_url = client.extract_image_url(result)
            if not image_url:
                raise RuntimeError(f"Cannot get image URL: {result}")
            
            print(f"[BailianNode] Image URL: {image_url[:60]}...")
            
            import requests
            headers = {"Authorization": f"Bearer {client.api_key}"}
            img_response = requests.get(image_url, headers=headers, timeout=60)
            img_response.raise_for_status()
            
            output_image = Image.open(io.BytesIO(img_response.content))
            output_image = output_image.convert("RGB")
            
            image_np = np.array(output_image).astype(np.float32) / 255.0
            image_tensor = torch.from_numpy(image_np).unsqueeze(0)
            
            print(f"[BailianNode] Generated: {output_image.size}")
            
            return (image_tensor,)
            
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


NODE_CLASS_MAPPINGS = {
    "BailianText2Image": BailianText2Image,
    "BailianImage2Image": BailianImage2Image,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BailianText2Image": "Bailian Text-to-Image",
    "BailianImage2Image": "Bailian Image-to-Image",
}


print("="*60)
print("[BailianNode] Alibaba Cloud Bailian Qwen Image 2.0 Nodes Loaded")
print("[BailianNode] Available Nodes:")
print("  - BailianText2Image: Text-to-Image")
print("  - BailianImage2Image: Image-to-Image")
print("="*60)
print("[BailianNode] Please ensure DASHSCOPE_API_KEY is set in .env or environment")
print("="*60)
