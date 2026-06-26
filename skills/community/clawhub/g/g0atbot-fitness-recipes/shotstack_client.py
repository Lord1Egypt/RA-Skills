"""
Shotstack Video Assembly Client
Assembles images + audio into TikTok-ready videos.
"""

import os
import requests
import time
from pathlib import Path

SHOTSTACK_API_KEY = os.getenv("SHOTSTACK_API_KEY", "")
SHOTSTACK_URL = "https://api.shotstack.io/v1"


def create_video_timeline(
    image_path: str,
    audio_path: str,
    duration: float = 30.0
) -> dict:
    """
    Create a Shotstack timeline for video assembly.
    
    Args:
        image_path: Path to the background image
        audio_path: Path to the voiceover audio
        duration: Video duration in seconds
    
    Returns:
        Shotstack timeline JSON
    """
    return {
        "timeline": {
            "fonts": [
                {"src": "https://shotstack-assets.s3.amazonaws.com/fonts/roboto/Roboto-Bold.ttf"}
            ],
            "tracks": [
                {
                    "type": "video",
                    "clips": [
                        {
                            "asset": {
                                "type": "image",
                                "src": f"file://{image_path}"
                            },
                            "start": 0,
                            "length": duration,
                            "fit": "cover",
                            "position": {"x": 0, "y": 0}
                        }
                    ]
                },
                {
                    "type": "audio",
                    "clips": [
                        {
                            "asset": {
                                "type": "audio",
                                "src": f"file://{audio_path}"
                            },
                            "start": 0,
                            "length": duration,
                            "volume": 1.0
                        }
                    ]
                },
                {
                    "type": "text",
                    "clips": [
                        {
                            "asset": {
                                "type": "text",
                                "text": "HIGH PROTEIN",
                                "style": "roboto",
                                "color": "#ffffff",
                                "size": 48,
                                "background": "#ff4757"
                            },
                            "start": 0,
                            "length": 5,
                            "position": {"x": 0.5, "y": 0.1}
                        },
                        {
                            "asset": {
                                "type": "text",
                                "text": "SAVE FOR LATER",
                                "style": "roboto",
                                "color": "#ffffff",
                                "size": 36,
                                "background": "#2ed573"
                            },
                            "start": duration - 5,
                            "length": 5,
                            "position": {"x": 0.5, "y": 0.9}
                        }
                    ]
                }
            ]
        },
        "output": {
            "format": "mp4",
            "resolution": "1080x1920",  # 9:16 TikTok format
            "fps": 30
        }
    }


def render_video(
    timeline: dict,
    output_path: str = None
) -> str:
    """
    Render video using Shotstack API.
    
    Args:
        timeline: Shotstack timeline JSON
        output_path: Where to save the rendered video
    
    Returns:
        Path to the rendered video
    """
    if not SHOTSTACK_API_KEY:
        print("⚠️  SHOTSTACK_API_KEY not set")
        return ""
    
    headers = {
        "x-api-key": SHOTSTACK_API_KEY,
        "Content-Type": "application/json"
    }
    
    print("🎬 Rendering video...")
    
    try:
        # Submit render job
        response = requests.post(
            f"{SHOTSTACK_URL}/render",
            json=timeline,
            headers=headers
        )
        response.raise_for_status()
        data = response.json()
        
        render_id = data["response"]["id"]
        print(f"📦 Render started: {render_id}")
        
        # Poll for completion
        while True:
            status_response = requests.get(
                f"{SHOTSTACK_URL}/render/{render_id}",
                headers=headers
            )
            status_data = status_response.json()
            status = status_data["response"]["status"]
            
            if status == "done":
                video_url = status_data["response"]["url"]
                print(f"✅ Render complete: {video_url}")
                
                # Download video
                if output_path is None:
                    output_dir = Path.home() / "clawd/bots/fitness-recipes-ai/output/videos"
                    output_dir.mkdir(parents=True, exist_ok=True)
                    output_path = str(output_dir / f"video_{render_id}.mp4")
                
                video_response = requests.get(video_url)
                with open(output_path, "wb") as f:
                    f.write(video_response.content)
                
                print(f"💾 Saved: {output_path}")
                return output_path
                
            elif status == "failed":
                print("❌ Render failed")
                return ""
            
            time.sleep(5)
            
    except Exception as e:
        print(f"❌ Error rendering video: {e}")
        return ""


def assemble_video(
    image_path: str,
    audio_path: str,
    recipe_name: str = "",
    duration: float = 30.0
) -> str:
    """
    Complete video assembly pipeline.
    
    Args:
        image_path: Path to food image
        audio_path: Path to voiceover
        recipe_name: Name for output file
        duration: Video duration
    
    Returns:
        Path to final video
    """
    timeline = create_video_timeline(image_path, audio_path, duration)
    
    output_dir = Path.home() / "clawd/bots/fitness-recipes-ai/output/videos"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = str(output_dir / f"{recipe_name.replace(' ', '_')}.mp4")
    
    return render_video(timeline, output_path)


def create_short_form_video(
    image_path: str,
    audio_path: str
) -> str:
    """
    Create a short-form video (15 seconds) for TikTok.
    """
    return assemble_video(image_path, audio_path, duration=15.0)


if __name__ == "__main__":
    # Test with placeholders
    import sys
    
    image_path = sys.argv[1] if len(sys.argv) > 1 else ""
    audio_path = sys.argv[2] if len(sys.argv) > 2 else ""
    
    if image_path and audio_path:
        video = assemble_video(image_path, audio_path, "test_recipe")
        print(f"🎉 Generated: {video}")
    else:
        print("Usage: python shotstack_client.py <image_path> <audio_path>")
