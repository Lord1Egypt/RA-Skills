#!/usr/bin/env python3
"""
Alibaba Cloud Bailian Qwen Image 2.0 Image Generation
Supports: Text-to-Image, Image-to-Image (reference image + text)
Model: qwen-image-2.0
"""

import os
import sys
import json
import base64
import requests
import argparse
import io
from typing import Optional, Dict, Any
from PIL import Image


def load_env_file():
    """Load environment variables from .env file"""
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ.setdefault(key.strip(), value.strip())

load_env_file()


class QwenImageGenerator:
    """Alibaba Cloud Bailian Qwen Image 2.0 Client"""
    
    BASE_URL = "https://dashscope.aliyuncs.com/api/v1"
    ENDPOINT = "/services/aigc/multimodal-generation/generation"
    DEFAULT_MODEL = "qwen-image-2.0"
    MAX_REF_IMAGE_SIZE = 61440
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("DASHSCOPE_API_KEY")
        if not self.api_key:
            raise ValueError("API Key required. Set DASHSCOPE_API_KEY environment variable.")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def _compress_image_to_datauri(self, image_path: str, max_size: int = MAX_REF_IMAGE_SIZE) -> str:
        img = Image.open(image_path)
        original_size = img.size
        
        if img.mode in ('RGBA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        else:
            img = img.convert('RGB')
        
        for target_size in [1024, 768, 512, 384, 256]:
            if max(img.size) > target_size:
                ratio = target_size / max(img.size)
                new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
                resized = img.resize(new_size, Image.LANCZOS)
            else:
                resized = img
            
            for quality in [85, 70, 50, 40, 30]:
                buffer = io.BytesIO()
                resized.save(buffer, format='JPEG', quality=quality)
                raw_data = buffer.getvalue()
                b64_data = base64.b64encode(raw_data).decode("utf-8")
                data_uri = f"data:image/jpeg;base64,{b64_data}"
                
                if len(data_uri) <= max_size:
                    print(f"[INFO] Image compressed: {original_size} -> {resized.size}, quality={quality}")
                    return data_uri
        
        raise ValueError(f"Cannot compress image to within {max_size} characters")
    
    def text_to_image(self, prompt: str, size: str = "1024*1024", n: int = 1, 
                      seed: Optional[int] = None, model: str = DEFAULT_MODEL) -> Dict[str, Any]:
        url = f"{self.BASE_URL}{self.ENDPOINT}"
        
        payload = {
            "model": model,
            "input": {
                "messages": [{
                    "role": "user",
                    "content": [{"type": "text", "text": f"Generate an image: {prompt}"}]
                }]
            }
        }
        
        if size or n or seed is not None:
            payload["parameters"] = {}
            if size: payload["parameters"]["size"] = size
            if n: payload["parameters"]["n"] = n
            if seed is not None: payload["parameters"]["seed"] = seed
        
        response = requests.post(url, headers=self.headers, json=payload, timeout=120)
        response.raise_for_status()
        return response.json()
    
    def image_to_image(self, prompt: str, reference_image_path: str, size: str = "1024*1024",
                       n: int = 1, seed: Optional[int] = None, model: str = DEFAULT_MODEL) -> Dict[str, Any]:
        url = f"{self.BASE_URL}{self.ENDPOINT}"
        image_data = self._compress_image_to_datauri(reference_image_path)
        
        payload = {
            "model": model,
            "input": {
                "messages": [{
                    "role": "user",
                    "content": [
                        {"type": "image", "image": image_data},
                        {"type": "text", "text": f"Generate based on reference image: {prompt}"}
                    ]
                }]
            }
        }
        
        if size or n or seed is not None:
            payload["parameters"] = {}
            if size: payload["parameters"]["size"] = size
            if n: payload["parameters"]["n"] = n
            if seed is not None: payload["parameters"]["seed"] = seed
        
        response = requests.post(url, headers=self.headers, json=payload, timeout=120)
        response.raise_for_status()
        return response.json()
    
    def extract_image_url(self, result: Dict[str, Any]) -> Optional[str]:
        output = result.get('output', {})
        
        if 'choices' in output:
            for choice in output['choices']:
                message = choice.get('message', {})
                content = message.get('content', [])
                for item in content:
                    if 'image' in item:
                        return item.get('image')
        
        if 'results' in output:
            for r in output['results']:
                if 'url' in r:
                    return r['url']
        
        if 'image_url' in output:
            return output['image_url']
        
        return None
    
    def download_image(self, image_url: str, output_path: str) -> str:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(image_url, headers=headers, timeout=60)
        response.raise_for_status()
        
        with open(output_path, "wb") as f:
            f.write(response.content)
        
        return output_path


def main():
    parser = argparse.ArgumentParser(description="Alibaba Cloud Bailian Image Generation")
    parser.add_argument("--api-key", help="DashScope API Key")
    parser.add_argument("--mode", choices=["t2i", "i2i"], required=True,
                       help="Mode: t2i=text-to-image, i2i=image-to-image")
    parser.add_argument("--prompt", required=True, help="Prompt text")
    parser.add_argument("--reference-image", help="Reference image path (i2i mode)")
    parser.add_argument("--size", default="1024*1024", help="Image size")
    parser.add_argument("--n", type=int, default=1, help="Number of images")
    parser.add_argument("--seed", type=int, help="Random seed")
    parser.add_argument("--model", default="qwen-image-2.0", help="Model name")
    parser.add_argument("--output", "-o", required=True, help="Output path")
    
    args = parser.parse_args()
    
    try:
        client = QwenImageGenerator(api_key=args.api_key)
    except ValueError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
    
    try:
        if args.mode == "t2i":
            result = client.text_to_image(
                prompt=args.prompt, size=args.size, n=args.n, seed=args.seed, model=args.model
            )
        else:
            if not args.reference_image:
                print("[ERROR] Image-to-image mode requires --reference-image", file=sys.stderr)
                sys.exit(1)
            result = client.image_to_image(
                prompt=args.prompt, reference_image_path=args.reference_image,
                size=args.size, n=args.n, seed=args.seed, model=args.model
            )
        
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        image_url = client.extract_image_url(result)
        if image_url:
            client.download_image(image_url, args.output)
            print(f"[OK] Image saved: {args.output}")
        else:
            print("[ERROR] Cannot find image URL")
            
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] API request error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()