---
name: comfyui
description: Use when you need to automate ComfyUI tasks. This skill provides instructions and scripts for installing ComfyUI, parsing API-format workflow JSON files, checking and downloading missing models, and executing workflows. Use this for requests like "run this comfyui workflow", "set up comfyui", or "generate an image using this json".
---

# ComfyUI Automation Skill

This skill provides a reliable, standardized workflow for interacting with ComfyUI. It is specifically designed to be easily executed by automated agents.

## 1. Environment Setup & Verification

ComfyUI should be installed in the primary workspace. **Never** install directly using root `pip` to avoid OS conflicts (PEP 668); always use a virtual environment (`venv`).

**Check if installed:**
```bash
ls /root/.openclaw/workspace/ComfyUI/venv/bin/activate
```

**If missing, install:**
```bash
cd /root/.openclaw/workspace
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 2. Workflow Format

ComfyUI workflows must be in **API Format** (a flat JSON dictionary where keys are stringified Node IDs).
If the user provides a standard UI format JSON (which contains `links`, `pos`, `groups` arrays), kindly request the API Format or use an appropriate converter.

## 3. Checking and Downloading Missing Models

Workflows will fail if the required weights (UNet, Checkpoints, VAE, LoRA, CLIP) are missing from the `ComfyUI/models/` subdirectories. 
To avoid redownloading large files, **always check if the file exists first**.

Use the provided script to scan the workflow JSON for model requirements and check them against the local directory:
```bash
python3 scripts/analyze_models.py /path/to/workflow_api.json /root/.openclaw/workspace/ComfyUI
```

**Downloading:**
If models are missing, formulate a download script. Always use `wget -nc` (no clobber) or `-c` (continue) to prevent overwriting or duplicate downloads. Example:
```bash
cd /root/.openclaw/workspace/ComfyUI/models/checkpoints
wget -nc https://huggingface.co/path/to/model.safetensors
```

## 4. Execution via API

Do not try to run ComfyUI workflows by modifying the UI state. Instead:
1. Ensure the ComfyUI server is running locally (usually port `8188`).
2. Write a lightweight Python wrapper that loads the API JSON, alters necessary parameters (like Prompts or Seeds), and posts it to the API.

**Example Python Wrapper:**
```python
import json, urllib.request, random

# 1. Load the template
with open("workflow_api.json", "r") as f:
    workflow = json.load(f)

# 2. Inject user variables (Identify the correct Node IDs beforehand)
# workflow["27"]["inputs"]["text"] = "A beautiful sunset..."
# workflow["3"]["inputs"]["seed"] = random.randint(1, 9999999)

# 3. Submit to API
payload = json.dumps({"prompt": workflow}).encode('utf-8')
req = urllib.request.Request("http://127.0.0.1:8188/prompt", data=payload)
req.add_header('Content-Type', 'application/json')
res = json.loads(urllib.request.urlopen(req).read())
print(f"Prompt queued with ID: {res['prompt_id']}")
```

## 5. Error Handling & Reporting

- **Missing Nodes:** If the API returns an error about a missing class/node, locate the corresponding Custom Node repository, clone it into `ComfyUI/custom_nodes/`, and `pip install -r requirements.txt` inside its folder using the `venv`.
- **OOM (Out of Memory):** If the GPU runs out of VRAM, suggest adding optimization arguments like `--lowvram` to the ComfyUI startup command.
- **Reporting:** Always report the explicit failure reason to the user, including which node failed and what is missing.