import json
import sys
import os
import re

def analyze_workflow(json_path, comfy_dir):
    try:
        with open(json_path, "r") as f:
            workflow = json.load(f)
    except Exception as e:
        print(f"Error reading JSON: {e}")
        sys.exit(1)

    # Common model loaders and their target directories
    loaders = {
        "UNETLoader": "diffusion_models",
        "CheckpointLoaderSimple": "checkpoints",
        "VAELoader": "vae",
        "CLIPLoader": "text_encoders",
        "LoraLoader": "loras",
        "ControlNetLoader": "controlnet"
    }

    missing_models = []

    # Iterate through the API-format JSON
    for node_id, node_data in workflow.items():
        class_type = node_data.get("class_type")
        if class_type in loaders:
            target_dir = loaders[class_type]
            
            # The model filename is usually in the inputs dictionary
            inputs = node_data.get("inputs", {})
            
            # Find the filename (could be named ckpt_name, vae_name, lora_name, unet_name, etc.)
            model_filename = None
            for key, val in inputs.items():
                if isinstance(val, str) and (val.endswith(".safetensors") or val.endswith(".ckpt") or val.endswith(".pt")):
                    model_filename = val
                    break
            
            if model_filename:
                # Resolve the absolute path
                model_path = os.path.join(comfy_dir, "models", target_dir, model_filename)
                
                if not os.path.exists(model_path):
                    missing_models.append((class_type, model_filename, target_dir))

    if missing_models:
        print("MISSING MODELS DETECTED:")
        for mt, fname, tdir in missing_models:
            print(f"  - [{mt}] requires '{fname}' in 'models/{tdir}/'")
        print("\nPlease download the missing models using wget -nc before running the workflow.")
        sys.exit(2)
    else:
        print("All required models are present.")
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 analyze_models.py <workflow_api.json> <comfyui_base_dir>")
        sys.exit(1)
    
    json_file = sys.argv[1]
    comfy_base = sys.argv[2]
    analyze_workflow(json_file, comfy_base)