#!/usr/bin/env python3
"""
Internalize a document into Gemma 2 2B using Doc-to-LoRA.

After internalization, the model can answer questions about the document
without the document being in the prompt.

Usage:
    python internalize.py --input document.txt --question "What is it about?"
    python internalize.py --text "Some text..." --question "Q1?,Q2?"
    python internalize.py --input doc.txt  # internalize only, print confirmation

Security note:
    This script uses torch.load with weights_only=False because D2L checkpoints
    contain Python config objects (AggregatorConfig, LoraConfig, HypernetConfig).
    Only load checkpoints from trusted sources (the official SakanaAI/doc-to-lora
    HuggingFace repository).
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

# Resolve repo root from skill location
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[3]  # .claude/skills/doc-to-lora/scripts -> repo root
os.chdir(REPO_ROOT)
sys.path.insert(0, str(REPO_ROOT / "src"))

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

import torch  # noqa: E402
from ctx_to_lora.model_loading import get_tokenizer  # noqa: E402
from ctx_to_lora.modeling.hypernet import ModulatedPretrainedModel  # noqa: E402


def load_model(checkpoint_path: str):
    """Load the D2L model with Mac-safe defaults.

    Note: weights_only=False is required because D2L checkpoints store
    Python config dataclasses (AggregatorConfig, LoraConfig, etc.)
    alongside model weights. This is safe when loading the official
    SakanaAI/doc-to-lora checkpoint.
    """
    if torch.cuda.is_available():
        device_map, dtype, flash = "cuda", torch.float16, True
    elif torch.backends.mps.is_available():
        device_map, dtype, flash = "mps", torch.float16, False
    else:
        device_map, dtype, flash = "cpu", torch.float32, False

    print(f"Device: {device_map} | dtype: {dtype}")

    # weights_only=False is needed: checkpoint contains config dataclasses
    # (AggregatorConfig, LoraConfig, HypernetConfig) not just tensors.
    # Only load from trusted sources.
    state_dict = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
    if device_map != "cuda":
        state_dict["ctx_encoder_args"].quantize_ctx_encoder = False
    else:
        try:
            import bitsandbytes  # noqa: F401
        except ImportError:
            state_dict["ctx_encoder_args"].quantize_ctx_encoder = False

    model = ModulatedPretrainedModel.from_state_dict(
        state_dict,
        train=False,
        use_sequence_packing=False,
        use_flash_attn=flash,
        base_model_kwargs={
            "device_map": device_map,
            "torch_dtype": dtype,
            "local_files_only": True,
        },
    )
    model.reset()
    model.eval()
    tokenizer = get_tokenizer(model.base_model.name_or_path)
    return model, tokenizer


def generate_answer(model, tokenizer, question: str, max_new_tokens: int = 256):
    """Generate an answer from the internalized model."""
    device = model.device
    messages = [{"role": "user", "content": question}]
    input_ids = tokenizer.apply_chat_template(
        messages, return_tensors="pt", add_generation_prompt=True
    ).to(device)
    with torch.no_grad():
        out = model.generate(
            input_ids=input_ids,
            max_new_tokens=max_new_tokens,
            do_sample=False,
        )
    return tokenizer.decode(out[0, input_ids.shape[1]:], skip_special_tokens=True)


def main():
    parser = argparse.ArgumentParser(description="Doc-to-LoRA: internalize & query")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--input", help="Path to a text file to internalize")
    source.add_argument("--text", help="Raw text to internalize")
    parser.add_argument(
        "--question", default=None,
        help="Question(s) to ask. Comma-separated for multiple.",
    )
    parser.add_argument(
        "--checkpoint",
        default="trained_d2l/gemma_demo/checkpoint-80000/pytorch_model.bin",
        help="Path to D2L checkpoint (only load from trusted sources)",
    )
    parser.add_argument("--max-tokens", type=int, default=256)
    parser.add_argument(
        "--output-json", default=None,
        help="Write results to JSON file (for programmatic use)",
    )
    args = parser.parse_args()

    # Load document
    if args.input:
        doc_text = Path(args.input).read_text()
        print(f"Document: {args.input} ({len(doc_text)} chars)")
    else:
        doc_text = args.text
        print(f"Document: inline text ({len(doc_text)} chars)")

    # Load model
    t0 = time.time()
    print("Loading D2L model...")
    model, tokenizer = load_model(args.checkpoint)
    print(f"Model loaded in {time.time() - t0:.1f}s")

    # Internalize
    t1 = time.time()
    print("Internalizing document...")
    model.internalize(doc_text)
    internalize_time = time.time() - t1
    print(f"Internalized in {internalize_time:.1f}s")

    # Query if questions provided
    if args.question:
        questions = [q.strip() for q in args.question.split(",")]
        results = []

        for q in questions:
            t2 = time.time()
            answer = generate_answer(model, tokenizer, q, args.max_tokens)
            elapsed = time.time() - t2
            results.append({"question": q, "answer": answer, "time_s": round(elapsed, 2)})
            print(f"\nQ: {q}")
            print(f"A: {answer}")
            print(f"   ({elapsed:.1f}s)")

        if args.output_json:
            output = {
                "document_chars": len(doc_text),
                "internalize_time_s": round(internalize_time, 2),
                "results": results,
            }
            Path(args.output_json).write_text(json.dumps(output, indent=2))
            print(f"\nResults written to {args.output_json}")
    else:
        print("\nDocument internalized. Pass --question to ask questions.")


if __name__ == "__main__":
    main()
