#!/usr/bin/env python3
"""
Improved Aesthetic Predictor - Fast Scoring Script
Uses CLIP + MLP model for content-level aesthetic scoring.
Model path: Set via MODEL_DIR environment variable, or default to F:/software/skill/aesthetic-scorer/models/improved-aesthetic-predictor
Base Weight: 45% (dynamic, adjustable 45%-70% based on NIMA score consensus)
"""

import os
import sys
import json
import argparse
import numpy as np
import torch
import torch.nn as nn
from PIL import Image

# ── Model location ─────────────────────────────────────────────────────────────
# Override via environment variable: set AESTHETIC_SCORER_MODEL_DIR
_DEFAULT_MODEL_DIR = r"F:\software\skill\aesthetic-scorer\models\improved-aesthetic-predictor"
MODEL_DIR = os.environ.get("AESTHETIC_SCORER_MODEL_DIR", _DEFAULT_MODEL_DIR)
# Best available weight file (linearMSE variant)
DEFAULT_WEIGHT = os.path.join(MODEL_DIR, "sac+logos+ava1-l14-linearMSE.pth")


# ── MLP architecture (must match training) ─────────────────────────────────────
class MLP(nn.Module):
    def __init__(self, input_size=768):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_size, 1024),
            nn.Dropout(0.2),
            nn.Linear(1024, 128),
            nn.Dropout(0.2),
            nn.Linear(128, 64),
            nn.Dropout(0.1),
            nn.Linear(64, 16),
            nn.Linear(16, 1),
        )

    def forward(self, x):
        return self.layers(x)


def normalized(a, axis=-1, order=2):
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2 == 0] = 1
    return a / np.expand_dims(l2, axis)


def load_model(model_path=None):
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # ── Load CLIP via transformers (force offline mode to use local cache) ──────
    import os as _os
    import logging
    _os.environ["TRANSFORMERS_OFFLINE"] = "1"   # use cached weights only
    _os.environ["HF_DATASETS_OFFLINE"] = "1"
    logging.getLogger("transformers").setLevel(logging.ERROR)

    try:
        from transformers import CLIPModel, CLIPProcessor
        clip_model = CLIPModel.from_pretrained(
            "openai/clip-vit-large-patch14",
            ignore_mismatched_sizes=True,
            local_files_only=True,
        ).to(device)
        clip_processor = CLIPProcessor.from_pretrained(
            "openai/clip-vit-large-patch14",
            local_files_only=True,
        )
        clip_model.train(mode=False)
    except Exception as e:
        print(f"Error: Could not load CLIP model via transformers.\n{e}")
        sys.exit(1)

    # ── Load MLP weights ───────────────────────────────────────────────────────
    weight_path = model_path or DEFAULT_WEIGHT
    if not os.path.exists(weight_path):
        print(f"Error: Weight file not found: {weight_path}")
        sys.exit(1)

    mlp = MLP(768)
    state = torch.load(weight_path, map_location=device, weights_only=True)
    mlp.load_state_dict(state)
    mlp = mlp.to(device)
    mlp.train(mode=False)

    return mlp, clip_model, clip_processor, device


def predict_aesthetic(image_path, model_path=None):
    """
    Predict aesthetic score using Improved Aesthetic Predictor.
    Returns dict with 'score' key (0-10 scale).
    """
    if not os.path.exists(image_path):
        print(f"Error: Image not found: {image_path}")
        return None

    mlp, clip_model, clip_processor, device = load_model(model_path)

    pil_image = Image.open(image_path).convert("RGB")

    with torch.no_grad():
        inputs = clip_processor(images=pil_image, return_tensors="pt").to(device)
        feat_out = clip_model.get_image_features(**inputs)
        # transformers ≥5.x may return BaseModelOutputWithPooling; extract tensor
        if hasattr(feat_out, "pooler_output"):
            image_features = feat_out.pooler_output
        elif hasattr(feat_out, "last_hidden_state"):
            image_features = feat_out.last_hidden_state[:, 0, :]
        elif isinstance(feat_out, torch.Tensor):
            image_features = feat_out
        else:
            # Try to get the first element (common for dataclass outputs)
            image_features = feat_out[0] if hasattr(feat_out, '__getitem__') else feat_out
        im_emb = normalized(image_features.cpu().detach().numpy())
        score_tensor = mlp(torch.from_numpy(im_emb).to(device).float())
        raw_score = float(score_tensor.item())

    # Improved Aesthetic Predictor outputs roughly 1-10; clamp to be safe
    score = max(0.0, min(10.0, raw_score))

    return {
        "model": "improved-aesthetic-predictor",
        "score": score,
        "image_path": image_path,
        "image_size": list(pil_image.size),
    }


def main():
    parser = argparse.ArgumentParser(description="Improved Aesthetic Predictor scoring")
    parser.add_argument("image_path", type=str, help="Path to the image file")
    parser.add_argument("--model", type=str, default=None, help="Custom .pth weight path")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    result = predict_aesthetic(args.image_path, args.model)
    if result is None:
        sys.exit(1)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"\n{'='*60}")
        print("AESTHETIC SCORE (Improved Predictor)")
        print(f"{'='*60}")
        print(f"Score  : {result['score']:.2f}/10")
        print(f"Image  : {result['image_path']}")
        print(f"Size   : {result['image_size'][0]}x{result['image_size'][1]}")
        print(f"Weight : {DEFAULT_WEIGHT}")
        print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
