"""
ElevenLabs TTS Client
Generates voiceovers for fitness recipe videos.
"""

import os
import requests
from pathlib import Path

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
ELEVENLABS_URL = "https://api.elevenlabs.io/v1/text-to-speech"


# Voice IDs for fitness content (energetic male voice)
VOICES = {
    "energetic_male": "21m00Tcm4TlvDq8ikWAM",  # Adam
    "calm_male": "AZnzlk1XvdvYsBnYFSwJ",     # Sam
    "deep_male": "nPczCjz82KWsc9L0j8Pt",      # Thomas
}


def generate_voiceover(
    text: str,
    voice_id: str = "21m00Tcm4TlvDq8ikWAM",
    output_path: str = None,
    stability: float = 0.5,
    similarity_boost: float = 0.75
) -> str:
    """
    Generate TTS voiceover using ElevenLabs.
    
    Args:
        text: Script to convert to speech
        voice_id: Voice ID to use
        output_path: Where to save the audio
        stability: Voice stability (0-1)
        similarity_boost: Voice similarity boost (0-1)
    
    Returns:
        Path to the generated audio file
    """
    if not ELEVENLABS_API_KEY:
        print("⚠️  ELEVENLABS_API_KEY not set - skipping TTS")
        return ""
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    
    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity_boost
        }
    }
    
    print(f"🎤 Generating voiceover ({len(text)} chars)...")
    
    try:
        response = requests.post(
            f"{ELEVENLABS_URL}/{voice_id}",
            json=payload,
            headers=headers
        )
        response.raise_for_status()
        
        if output_path is None:
            output_dir = Path.home() / "clawd/bots/fitness-recipes-ai/output/audio"
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = str(output_dir / f"{hash(text)}.mp3")
        
        with open(output_path, "wb") as f:
            f.write(response.content)
        
        print(f"✅ Saved: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"❌ Error generating voiceover: {e}")
        return ""


def create_recipe_script(recipe_name: str, calories: int, protein: int) -> str:
    """Create a recipe script for TTS."""
    return f"""
    This healthy {recipe_name} has only {calories} calories and {protein} grams of protein.
    
    Here's what makes it perfect for your fitness goals.
    
    First, it's high in protein to support muscle growth.
    Second, it's low in calories so you can stay lean.
    And third, it tastes amazing.
    
    Save this video for your next meal prep.
    Your body will thank you.
    """


def generate_recipe_voiceover(recipe_name: str, calories: int, protein: int) -> str:
    """Generate a complete recipe voiceover."""
    script = create_recipe_script(recipe_name, calories, protein)
    return generate_voiceover(script)


# Test voices
TEST_VOICES = {
    "adam": "21m00Tcm4TlvDq8ikWAM",  # Energetic, clear
    "sam": "AZnzlk1XvdvYsBnYFSwJ",   # Calm, steady
    "thomas": "nPczCjz82KWsc9L0j8Pt", # Deep, authoritative
}


if __name__ == "__main__":
    # Test generation
    test_script = "This protein-packed meal has 450 calories and 35 grams of protein."
    generate_voiceover(test_script)
