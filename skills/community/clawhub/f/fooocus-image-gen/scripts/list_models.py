#!/usr/bin/env python3
"""
List available Fooocus models and presets.
"""

import os
import json
import argparse
from pathlib import Path

# Fooocus presets configuration
PRESETS = {
    "default": {
        "description": "Balanced settings for general purpose generation",
        "base_model": "juggernautXL_v8Rundiffusion.safetensors",
        "performance": "Quality",
        "styles": []
    },
    "anime": {
        "description": "Anime and cartoon style generation",
        "base_model": "animaPencilXL_v100.safetensors",
        "performance": "Quality",
        "styles": ["Anime"]
    },
    "realistic": {
        "description": "Photorealistic image generation",
        "base_model": "realisticStockPhoto_v20.safetensors",
        "performance": "Quality",
        "styles": ["Photographic"]
    },
    "lcm": {
        "description": "Fast generation with LCM (Latent Consistency Model)",
        "base_model": "juggernautXL_v8Rundiffusion.safetensors",
        "performance": "Speed",
        "styles": []
    },
    "lightning": {
        "description": "Very fast generation with Lightning model",
        "base_model": "juggernautXL_v8Rundiffusion.safetensors",
        "performance": "Extreme Speed",
        "styles": []
    },
    "playground_v2.5": {
        "description": "Artistic and creative image generation",
        "base_model": "playground-v2.5-1024px-aesthetic.safetensors",
        "performance": "Quality",
        "styles": []
    },
    "pony_v6": {
        "description": "Versatile style generation with Pony Diffusion",
        "base_model": "ponyDiffusionV6XL.safetensors",
        "performance": "Quality",
        "styles": []
    },
    "sai": {
        "description": "Professional, high-quality image generation",
        "base_model": "sd_xl_base_1.0.safetensors",
        "performance": "Quality",
        "styles": []
    }
}

# Common Fooocus model filenames
COMMON_MODELS = [
    "juggernautXL_v8Rundiffusion.safetensors",
    "animaPencilXL_v100.safetensors",
    "realisticStockPhoto_v20.safetensors",
    "playground-v2.5-1024px-aesthetic.safetensors",
    "ponyDiffusionV6XL.safetensors",
    "sd_xl_base_1.0.safetensors",
    "sd_xl_refiner_1.0.safetensors",
    "Anything-V5.0-pruned.safetensors",
    "Counterfeit-V3.0.safetensors",
    "DreamShaper_8.safetensors",
]

def find_fooocus_directory() -> Optional[Path]:
    """Try to find the Fooocus installation directory."""
    possible_paths = [
        Path.home() / "Fooocus",
        Path.home() / ".fooocus",
        Path("/opt/fooocus"),
        Path("C:/Fooocus"),
        Path("G:/Fooocus"),
    ]
    
    for path in possible_paths:
        if path.exists() and (path / "entry_with_update.py").exists():
            return path
    return None

def find_models_directory(fooocus_path: Path) -> Path:
    """Find the models directory within Fooocus installation."""
    models_path = fooocus_path / "models" / "checkpoints"
    if models_path.exists():
        return models_path
    return fooocus_path / "models"  # Fallback

def list_installed_models(models_path: Path) -> list:
    """List installed model files."""
    if not models_path.exists():
        return []
    
    model_files = []
    for ext in [".safetensors", ".ckpt", ".pt", ".pth"]:
        model_files.extend(models_path.glob(f"*{ext}"))
    
    return sorted([f.name for f in model_files if f.is_file()])

def list_available_presets() -> dict:
    """List available presets with descriptions."""
    return PRESETS

def check_model_availability(model_name: str, models_path: Path) -> bool:
    """Check if a specific model is available."""
    return (models_path / model_name).exists()

def print_model_info(models_path: Path, presets: dict):
    """Print information about available models and presets."""
    print("=" * 60)
    print("Fooocus Models and Presets")
    print("=" * 60)
    
    # Installed Models
    print("\n📦 Installed Models:")
    installed_models = list_installed_models(models_path)
    
    if installed_models:
        for model in installed_models:
            print(f"  ✓ {model}")
    else:
        print("  ✗ No models found. Fooocus will download default models on first run.")
        print("     Common models are usually placed in:")
        print(f"     {models_path}")
        
    # Common Models Reference
    print("\n🔧 Common Model Filenames:")
    for model in COMMON_MODELS:
        status = "✓" if check_model_availability(model, models_path) else "?"
        print(f"  {status} {model}")
    
    # Presets
    print("\n🎨 Available Presets:")
    for preset_name, preset_info in presets.items():
        print(f"  {preset_name}: {preset_info['description']}")
        print(f"    Base Model: {preset_info.get('base_model', 'default')}")
        print(f"    Performance: {preset_info.get('performance', 'default')}")
        if preset_info.get('styles'):
            print(f"    Styles: {', '.join(preset_info['styles'])}")
        print()
    
    print("=" * 60)
    print("Usage Tips:")
    print("- Use --preset flag with generate_image.py to apply styles")
    print("- Place custom models in the models/checkpoints directory")
    print("- Fooocus will download default models on first run")
    print("=" * 60)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="List available Fooocus models and presets",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--path", help="Path to Fooocus installation")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    
    # Find Fooocus directory
    fooocus_path = None
    if args.path:
        fooocus_path = Path(args.path)
        if not fooocus_path.exists():
            print(f"Error: Path not found: {args.path}")
            sys.exit(1)
    else:
        fooocus_path = find_fooocus_directory()
    
    if not fooocus_path:
        print("❌ Fooocus installation not found.")
        print("   Try specifying the path with --path")
        print("   Or run install_fooocus.py to install Fooocus.")
        sys.exit(1)
    
    print(f"Found Fooocus at: {fooocus_path}")
    
    # Find models directory
    models_path = find_models_directory(fooocus_path)
    print(f"Models directory: {models_path}")
    
    # List available items
    presets = list_available_presets()
    print_model_info(models_path, presets)
    
    # JSON output if requested
    if args.json:
        info = {
            "fooocus_path": str(fooocus_path),
            "models_path": str(models_path),
            "installed_models": list_installed_models(models_path),
            "presets": presets
        }
        print(json.dumps(info, indent=2))
    

def list_models_json(fooocus_path: str = None):
    """List models in JSON format for programmatic use."""
    if fooocus_path is None:
        fooocus_path = find_fooocus_directory()
        if not fooocus_path:
            return {"error": "Fooocus not found"}
    
    models_path = find_models_directory(fooocus_path)
    presets = list_available_presets()
    
    return {
        "fooocus_path": str(fooocus_path),
        "models_path": str(models_path),
        "installed_models": list_installed_models(models_path),
        "presets": presets
    }

if __name__ == "__main__":
    import sys
    main()
