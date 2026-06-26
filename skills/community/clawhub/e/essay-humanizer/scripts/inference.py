#!/usr/bin/env python3
"""
Humanize an AI-drafted essay using fine-tuned Qwen + MLX LoRA.
System prompt encodes 24 weighted patterns from data/analysis/weights.json.

Clawhub layout:
  <skill-root>/scripts/inference.py   <- this file
  <skill-root>/assets/adapters/       <- LoRA .safetensors
  <skill-root>/data/analysis/weights.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

SKILL_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ADAPTER = SKILL_ROOT / "assets" / "adapters"
DEFAULT_MODEL = "Qwen/Qwen3-8B-MLX-4bit"

_model = None
_tokenizer = None


def load_weights() -> Dict:
    for name in ("weights.json", "weights_default.json"):
        p = SKILL_ROOT / "data" / "analysis" / name
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
    return {"patterns": [], "syntactic_profile": {}}


def build_system_instruction(data: Dict[str, Any]) -> str:
    patterns = sorted(
        data.get("patterns", []),
        key=lambda x: -float(x.get("weight", 0) or 0),
    )
    lines: List[str] = [
        "You rewrite AI-drafted academic/argumentative essays so they read as natural human student writing.",
        "Preserve the author's argument, structure, and any citations; do not invent sources.",
        "Remove chatty sign-offs and collaborative phrases. No markdown headings unless the input uses them.",
        "Prioritize fixing these AI-style issues (highest weight first):",
    ]
    if patterns:
        for p in patterns[:24]:
            lines.append(
                f"- {p.get('id', '?')}: {p.get('name', '')} (weight {float(p.get('weight', 0)):.3f})"
            )
    else:
        lines.append(
            "(Weights file empty — apply general de-AIfication: cut puffery, AI vocab, false ranges, em-dash spam, lists-as-crutch, collaborative register.)"
        )
    syn = data.get("syntactic_profile", {})
    if syn.get("mdd_variance_ratio_human_over_ai"):
        lines.append(
            f"Vary sentence complexity naturally; human reference variance ratio versus AI ~ {syn.get('mdd_variance_ratio_human_over_ai')}. "
            "Do not flatten every sentence to short, equally tidy clauses."
        )
    lines.append("Output only the rewritten essay body, plain text.")
    return "\n".join(lines)


def strip_latex_markers(text: str) -> str:
    if not text:
        return text
    out = re.sub(r"\$\$(.*?)\$\$", r"\1", text, flags=re.DOTALL)
    out = re.sub(r"\\\[(.*?)\\\]", r"\1", out, flags=re.DOTALL)
    out = re.sub(r"\\\((.*?)\\\)", r"\1", out, flags=re.DOTALL)
    out = re.sub(r"\$([^$\n]+)\$", r"\1", out)
    return out


def _ensure_adapters_decoded() -> None:
    """Auto-decode base64 JSON adapter on first use (Clawhub ships text only)."""
    binary = DEFAULT_ADAPTER / "adapters.safetensors"
    encoded = DEFAULT_ADAPTER / "adapters.safetensors.json"
    if binary.exists() or not encoded.exists():
        return
    import base64
    with open(encoded, "r", encoding="utf-8") as f:
        obj = json.load(f)
    binary.write_bytes(base64.b64decode(obj["data"]))


def load_model(base_model: str, adapter_path: Optional[str]):
    global _model, _tokenizer
    if _model is not None:
        return _model, _tokenizer

    _ensure_adapters_decoded()
    from mlx_lm import load

    ap = Path(str(adapter_path or DEFAULT_ADAPTER))
    has_adapters = ap.is_dir() and any(ap.glob("*.safetensors"))
    if has_adapters:
        _model, _tokenizer = load(base_model, adapter_path=str(ap))
    else:
        _model, _tokenizer = load(base_model)
    return _model, _tokenizer


def humanize(
    essay: str,
    max_tokens: int = 2048,
    base_model: str = DEFAULT_MODEL,
    adapter_path: Optional[str] = None,
) -> str:
    from mlx_lm import generate

    data = load_weights()
    sys_msg = build_system_instruction(data)
    model, tokenizer = load_model(base_model, adapter_path)
    messages = [
        {"role": "system", "content": sys_msg},
        {"role": "user", "content": f"Rewrite this essay:\n\n{essay.strip()}"},
    ]
    prompt = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True, tokenize=False
    )
    raw = generate(model, tokenizer, prompt=prompt, max_tokens=max_tokens)
    return strip_latex_markers(raw)


def main():
    ap = argparse.ArgumentParser(description="Humanize an AI-drafted essay (MLX + LoRA).")
    ap.add_argument("text", nargs="?", help="Essay text (or use --file)")
    ap.add_argument("--file", type=str)
    ap.add_argument("--max-tokens", type=int, default=2048)
    ap.add_argument("--base-model", type=str, default=DEFAULT_MODEL)
    ap.add_argument("--adapter-path", type=str, default=str(DEFAULT_ADAPTER))
    args = ap.parse_args()

    if args.file:
        essay = Path(args.file).read_text(encoding="utf-8")
    elif args.text:
        essay = args.text
    else:
        ap.print_help()
        sys.exit(1)

    print(
        humanize(
            essay,
            max_tokens=args.max_tokens,
            base_model=args.base_model,
            adapter_path=args.adapter_path,
        )
    )


if __name__ == "__main__":
    main()
