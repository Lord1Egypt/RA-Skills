"""
fal.ai Image Generation Client
Generates food images for fitness recipes.
"""

import os
import requests
from pathlib import Path

FAL_API_KEY = os.getenv("FAL_API_KEY", "")
FAL_API_URL = "https://fal.run/fal-ai/flux"


def generate_food_image(prompt: str, output_path: str = None) -> str:
    """
    Generate a food image using fal.ai FLUX model.
    
    Args:
        prompt: Description of the food to generate
        output_path: Where to save the image
    
    Returns:
        Path to the generated image
    """
    if not FAL_API_KEY:
        print("⚠️  FAL_API_KEY not set - using placeholder")
        return generate_placeholder(prompt)
    
    headers = {
        "Authorization": f"Key {FAL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": f"Professional food photography, {prompt}, high quality, appetizing, studio lighting, clean background",
        "num_images": 1,
        "width": 720,
        "height": 1280,  # 9:16 vertical for TikTok
 format    }
    
    print(f"🎨 Generating: {prompt}")
    
    try:
        response = requests.post(FAL_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # Get image URL and download
        image_url = data["images"][0]["url"]
        image_response = requests.get(image_url)
        
        if output_path is None:
            output_dir = Path.home() / "clawd/bots/fitness-recipes-ai/output/images"
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"{hash(prompt)}.jpg"
        
        with open(output_path, "wb") as f:
            f.write(image_response.content)
        
        print(f"✅ Saved: {output_path}")
        return str(output_path)
        
    except Exception as e:
        print(f"❌ Error generating image: {e}")
        return generate_placeholder(prompt)


def generate_placeholder(prompt: str) -> str:
    """Generate a placeholder image for testing."""
    from PIL import Image, ImageDraw, ImageFont
    
    output_dir = Path.home() / "clawd/bots/fitness-recipes-ai/output/images"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"placeholder_{hash(prompt)}.jpg"
    
    # Create placeholder image
    img = Image.new('RGB', (720, 1280), color='#1a1a2e')
    draw = ImageDraw.Draw(img)
    
    # Add text
    text = prompt[:30] + "..." if len(prompt) > 30 else prompt
    draw.text((360, 640), text, fill='#ffffff', anchor='mm')
    
    img.save(output_path)
    print(f"📦 Placeholder: {output_path}")
    return str(output_path)


# Food-specific prompts
FOOD_PROMPTS = {
    "protein_shake": "Chocolate protein shake with banana, professional food photography",
    "chicken_meal": "Grilled chicken breast with vegetables, healthy meal prep",
    "smoothie_bowl": "Acai smoothie bowl with fruits and granola, top view",
    "avocado_toast": "Avocado toast with poached egg, sourdough bread",
    "protein_pancakes": "Protein pancakes with maple syrup and berries",
    "greek_yogurt": "Greek yogurt parfait with honey and walnuts",
    "salmon_dish": "Baked salmon with asparagus and lemon",
    "quinoa_salad": "Quinoa salad with vegetables and feta cheese",
    "turkey_stirfry": "Turkey stir fry with vegetables and rice",
    "overnight_oats": "Overnight oats with fruits and chia seeds",
}


if __name__ == "__main__":
    # Test generation
    for name, prompt in list(FOOD_PROMPTS.items())[:3]:
        generate_food_image(prompt)
