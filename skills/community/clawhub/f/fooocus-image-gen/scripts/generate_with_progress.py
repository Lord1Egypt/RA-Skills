#!/usr/bin/env python3
"""
Fooocus WebSocket Client with Real-time Progress
Provides live progress updates during image generation
"""

import os
import sys
import json
import time
import base64
import argparse
import asyncio
import websockets
import urllib.request
from pathlib import Path
from typing import Optional, Callable, Dict, Any

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 7865


class FooocusWebSocketClient:
    """WebSocket client for Fooocus with real-time progress"""
    
    def __init__(self, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT):
        self.host = host
        self.port = port
        self.ws_url = f"ws://{host}:{port}/queue/join"
        self.http_url = f"http://{host}:{port}"
        self.session_hash = None
        
    async def check_connection(self) -> bool:
        """Check if Fooocus is running"""
        try:
            req = urllib.request.Request(
                f"{self.http_url}/",
                method="HEAD",
                headers={"User-Agent": "Fooocus-WS-Client/1.0"}
            )
            with urllib.request.urlopen(req, timeout=5) as _:
                return True
        except:
            return False
    
    async def generate_with_progress(
        self,
        prompt: str,
        negative_prompt: str = "",
        width: int = 1024,
        height: int = 1024,
        steps: int = 30,
        cfg: float = 4.0,
        seed: int = -1,
        sharpness: float = 2.0,
        styles: Optional[list] = None,
        input_image: Optional[str] = None,
        input_mask: Optional[str] = None,
        preset: str = "default",
        on_progress: Optional[Callable[[Dict], None]] = None,
        on_complete: Optional[Callable[[str], None]] = None,
        on_error: Optional[Callable[[str], None]] = None
    ) -> Optional[str]:
        """
        Generate image with real-time progress updates via WebSocket
        
        Args:
            prompt: Generation prompt
            negative_prompt: Negative prompt
            width: Image width
            height: Image height
            steps: Number of sampling steps
            cfg: Guidance scale
            seed: Random seed (-1 for random)
            sharpness: Sharpness value
            styles: List of style names
            input_image: Base64 input image (optional)
            input_mask: Base64 input mask (optional)
            preset: Model preset
            on_progress: Callback for progress updates
            on_complete: Callback when generation completes
            on_error: Callback for errors
            
        Returns:
            Base64 image string or None if failed
        """
        import uuid
        
        self.session_hash = str(uuid.uuid4())
        
        if styles is None:
            styles = ["Fooocus V2"]
        
        try:
            async with websockets.connect(self.ws_url) as ws:
                # Send join message
                join_msg = {
                    "fn_index": 13,
                    "session_hash": self.session_hash
                }
                await ws.send(json.dumps(join_msg))
                
                # Wait for estimation
                while True:
                    msg = await ws.recv()
                    data = json.loads(msg)
                    
                    if data.get("msg") == "estimation":
                        # Server is estimating queue time
                        if on_progress:
                            on_progress({
                                "status": "estimating",
                                "queue_size": data.get("queue_size", 0),
                                "message": "Estimating wait time..."
                            })
                    
                    elif data.get("msg") == "send_data":
                        # Server ready for data
                        break
                
                # Send generation data
                generation_data = {
                    "fn_index": 13,
                    "data": [
                        prompt,
                        negative_prompt,
                        styles,
                        "Quality",
                        width,
                        height,
                        1,
                        seed,
                        sharpness,
                        cfg,
                        "dpmpp_2m_sde_gpu",
                        "karras",
                        "",
                        input_image,
                        input_mask,
                        False,
                        None,
                        None
                    ],
                    "session_hash": self.session_hash
                }
                await ws.send(json.dumps(generation_data))
                
                # Listen for progress
                current_step = 0
                total_steps = steps
                
                while True:
                    try:
                        msg = await asyncio.wait_for(ws.recv(), timeout=300)
                        data = json.loads(msg)
                        
                        msg_type = data.get("msg")
                        
                        if msg_type == "progress":
                            # Generation progress
                            progress_data = data.get("progress_data", {})
                            current = progress_data.get("index", 0)
                            total = progress_data.get("length", total_steps)
                            
                            progress_pct = (current / total * 100) if total > 0 else 0
                            
                            if on_progress:
                                on_progress({
                                    "status": "generating",
                                    "step": current,
                                    "total_steps": total,
                                    "progress_percent": round(progress_pct, 1),
                                    "message": f"Generating... Step {current}/{total} ({progress_pct:.1f}%)"
                                })
                        
                        elif msg_type == "process_completed":
                            # Generation complete
                            output = data.get("output", {})
                            
                            if "data" in output and len(output["data"]) > 0:
                                image_data = output["data"][0]
                                
                                if on_complete:
                                    on_complete(image_data)
                                
                                return image_data
                            else:
                                error_msg = "No image data in response"
                                if on_error:
                                    on_error(error_msg)
                                return None
                        
                        elif msg_type == "process_error":
                            # Generation error
                            error_msg = data.get("error", "Unknown error")
                            if on_error:
                                on_error(error_msg)
                            return None
                            
                    except asyncio.TimeoutError:
                        error_msg = "Generation timed out"
                        if on_error:
                            on_error(error_msg)
                        return None
                        
        except websockets.exceptions.ConnectionRefused:
            error_msg = f"Cannot connect to Fooocus at {self.host}:{self.port}. Is it running?"
            if on_error:
                on_error(error_msg)
            return None
        except Exception as e:
            error_msg = f"WebSocket error: {str(e)}"
            if on_error:
                on_error(error_msg)
            return None
    
    async def upscale_with_progress(
        self,
        image_path: str,
        scale: float = 2.0,
        on_progress: Optional[Callable[[Dict], None]] = None,
        on_complete: Optional[Callable[[str], None]] = None,
        on_error: Optional[Callable[[str], None]] = None
    ) -> Optional[str]:
        """Upscale image with progress updates"""
        import uuid
        
        self.session_hash = str(uuid.uuid4())
        
        # Read and encode image
        try:
            with open(image_path, "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode()
        except Exception as e:
            if on_error:
                on_error(f"Failed to read image: {e}")
            return None
        
        try:
            async with websockets.connect(self.ws_url) as ws:
                join_msg = {
                    "fn_index": 67,  # Upscale function
                    "session_hash": self.session_hash
                }
                await ws.send(json.dumps(join_msg))
                
                # Wait for send_data
                while True:
                    msg = await ws.recv()
                    data = json.loads(msg)
                    if data.get("msg") == "send_data":
                        break
                
                # Send upscale data
                upscale_data = {
                    "fn_index": 67,
                    "data": [
                        f"data:image/png;base64,{img_b64}",
                        scale,
                        f"{scale}x"
                    ],
                    "session_hash": self.session_hash
                }
                await ws.send(json.dumps(upscale_data))
                
                # Listen for completion
                while True:
                    msg = await ws.recv()
                    data = json.loads(msg)
                    
                    if data.get("msg") == "progress" and on_progress:
                        on_progress({
                            "status": "upscaling",
                            "message": "Upscaling in progress..."
                        })
                    
                    elif data.get("msg") == "process_completed":
                        output = data.get("output", {})
                        if "data" in output and len(output["data"]) > 0:
                            image_data = output["data"][0]
                            if on_complete:
                                on_complete(image_data)
                            return image_data
                        else:
                            if on_error:
                                on_error("No image data in response")
                            return None
                    
                    elif data.get("msg") == "process_error":
                        if on_error:
                            on_error(data.get("error", "Upscaling failed"))
                        return None
                        
        except Exception as e:
            if on_error:
                on_error(f"WebSocket error: {e}")
            return None


def print_progress(progress: Dict):
    """Default progress printer"""
    status = progress.get("status", "unknown")
    message = progress.get("message", "")
    
    if status == "generating":
        step = progress.get("step", 0)
        total = progress.get("total_steps", 1)
        pct = progress.get("progress_percent", 0)
        
        # Create progress bar
        bar_length = 30
        filled = int(bar_length * pct / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        print(f"\r[{bar}] {pct:.1f}% | {message}", end="", flush=True)
    else:
        print(f"\r{message}", end="", flush=True)


def save_base64_image(b64_data: str, output_path: str):
    """Save base64 image to file"""
    if "," in b64_data:
        b64_data = b64_data.split(",")[1]
    
    img_data = base64.b64decode(b64_data)
    with open(output_path, "wb") as f:
        f.write(img_data)
    return output_path


async def main():
    parser = argparse.ArgumentParser(
        description="Generate images with real-time progress feedback"
    )
    
    # Connection
    parser.add_argument("--host", default=DEFAULT_HOST, help="Fooocus host")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Fooocus port")
    
    # Generation parameters
    parser.add_argument("--prompt", "-p", required=True, help="Generation prompt")
    parser.add_argument("--negative", "-n", default="", help="Negative prompt")
    parser.add_argument("--width", type=int, default=1024, help="Image width")
    parser.add_argument("--height", type=int, default=1024, help="Image height")
    parser.add_argument("--steps", type=int, default=30, help="Sampling steps")
    parser.add_argument("--cfg", type=float, default=4.0, help="Guidance scale")
    parser.add_argument("--seed", type=int, default=-1, help="Random seed")
    parser.add_argument("--sharpness", type=float, default=2.0, help="Sharpness")
    parser.add_argument("--style", action="append", help="Style preset")
    
    # Input/Output
    parser.add_argument("--input", "-i", help="Input image path")
    parser.add_argument("--mask", "-m", help="Mask image path")
    parser.add_argument("--output", "-o", required=True, help="Output path")
    
    # Mode
    parser.add_argument("--mode", choices=["generate", "upscale"], default="generate")
    parser.add_argument("--scale", type=float, default=2.0, help="Upscale factor")
    
    # Display
    parser.add_argument("--no-progress", action="store_true", help="Disable progress bar")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # Create client
    client = FooocusWebSocketClient(args.host, args.port)
    
    # Check connection
    if not await client.check_connection():
        print(f"Error: Cannot connect to Fooocus at {args.host}:{args.port}")
        print("Make sure Fooocus is running:")
        print(f"  cd ~/Fooocus && python entry_with_update.py")
        sys.exit(1)
    
    if args.verbose:
        print(f"Connected to Fooocus at {args.host}:{args.port}")
    
    # Prepare callbacks
    if args.no_progress:
        on_progress = None
    else:
        on_progress = print_progress
    
    result = None
    
    def on_complete(image_data):
        nonlocal result
        result = image_data
        if not args.no_progress:
            print()  # New line after progress bar
        print(f"✓ Generation complete!")
    
    def on_error(error_msg):
        if not args.no_progress:
            print()  # New line after progress bar
        print(f"✗ Error: {error_msg}")
    
    # Execute generation
    if args.mode == "generate":
        # Prepare input images
        input_image = None
        input_mask = None
        
        if args.input:
            with open(args.input, "rb") as f:
                input_image = f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
        
        if args.mask:
            with open(args.mask, "rb") as f:
                input_mask = f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
        
        styles = args.style or ["Fooocus V2"]
        
        print(f"Generating: {args.prompt[:60]}...")
        
        result = await client.generate_with_progress(
            prompt=args.prompt,
            negative_prompt=args.negative,
            width=args.width,
            height=args.height,
            steps=args.steps,
            cfg=args.cfg,
            seed=args.seed,
            sharpness=args.sharpness,
            styles=styles,
            input_image=input_image,
            input_mask=input_mask,
            on_progress=on_progress,
            on_complete=on_complete,
            on_error=on_error
        )
    
    elif args.mode == "upscale":
        if not args.input:
            print("Error: --input required for upscaling")
            sys.exit(1)
        
        print(f"Upscaling: {args.input}")
        
        result = await client.upscale_with_progress(
            image_path=args.input,
            scale=args.scale,
            on_progress=on_progress,
            on_complete=on_complete,
            on_error=on_error
        )
    
    # Save result
    if result:
        save_base64_image(result, args.output)
        print(f"Saved to: {args.output}")
    else:
        print("Generation failed")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
