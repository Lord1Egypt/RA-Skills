#!/usr/bin/env python3
"""
ExpertPack EK Ratio Evaluator

Measures the Esoteric Knowledge (EK) ratio of an ExpertPack by blind-probing
frontier LLMs with questions derived from the pack's propositions.

Usage:
    python3 eval-ek.py <pack-path> [--models model1,model2] [--sample N] [--output FILE]

Example:
    python3 eval-ek.py packs/home-assistant --models gpt-4.1-mini,claude-sonnet-4-6,gemini-2.0-flash
    python3 eval-ek.py packs/blender-3d --sample 50 --output eval-ek-blender.yaml
"""

import argparse
import json
import os
import re
import sys
import time
import yaml
import requests
from pathlib import Path
from datetime import datetime, timezone

# --- Configuration ---

DEFAULT_MODELS = [
    "openai/gpt-4.1-mini",
    "anthropic/claude-sonnet-4-6",
    "google/gemini-2.0-flash-001",
]

# OpenRouter API
OPENROUTER_BASE = "https://openrouter.ai/api/v1/chat/completions"

def get_api_key():
    """Resolve OpenRouter API key from OpenClaw auth profiles or environment."""
    # Check environment first
    key = os.environ.get("OPENROUTER_API_KEY")
    if key:
        return key
    
    # Check OpenClaw auth profiles
    auth_path = Path.home() / ".openclaw" / "agents" / "main" / "agent" / "auth-profiles.json"
    if auth_path.exists():
        with open(auth_path) as f:
            data = json.load(f)
        key = data.get("profiles", {}).get("openrouter:default", {}).get("key", "")
        if key:
            return key
    
    # Check OpenClaw models.json
    models_path = Path.home() / ".openclaw" / "agents" / "main" / "agent" / "models.json"
    if models_path.exists():
        with open(models_path) as f:
            data = json.load(f)
        key = data.get("providers", {}).get("openrouter", {}).get("apiKey", "")
        if key:
            return key
    
    print("ERROR: No OpenRouter API key found. Set OPENROUTER_API_KEY or configure via openclaw.", file=sys.stderr)
    sys.exit(1)


# --- Proposition Extraction ---

def find_proposition_files(pack_path: Path) -> list[Path]:
    """Find all proposition files in the pack (handles flat and composite packs)."""
    files = []
    for p in sorted(pack_path.rglob("propositions/*.md")):
        if p.name.startswith("_"):
            continue
        files.append(p)
    return files


def parse_propositions(filepath: Path) -> list[dict]:
    """Parse a propositions file into individual atomic statements with source context."""
    propositions = []
    current_source = None
    section_name = filepath.stem  # e.g., "concepts", "workflows"
    
    with open(filepath) as f:
        for line in f:
            line = line.rstrip()
            
            # Track source file headers (### filename.md)
            if line.startswith("### "):
                current_source = line[4:].strip()
                continue
            
            # Extract bullet-point propositions
            if line.startswith("- ") and len(line) > 10:
                prop_text = line[2:].strip()
                propositions.append({
                    "text": prop_text,
                    "source_file": current_source,
                    "section": section_name,
                    "prop_file": str(filepath),
                })
    
    return propositions


def extract_all_propositions(pack_path: Path) -> list[dict]:
    """Extract all propositions from the pack."""
    all_props = []
    for pf in find_proposition_files(pack_path):
        props = parse_propositions(pf)
        all_props.extend(props)
    return all_props


# --- Question Generation ---

def proposition_to_question(proposition: str) -> str:
    """Convert an atomic proposition into a natural probe question.
    
    Uses simple heuristic transformations. The question should be answerable
    if and only if the model has this specific knowledge.
    """
    # Strip trailing periods
    prop = proposition.rstrip(".")
    
    # For propositions that state a specific value/number, ask for that value
    # For propositions that describe behavior, ask about the behavior
    # Generic transformation: "Is it true that {proposition}? If so, explain the specifics."
    # Better: rephrase as an open question
    
    # Simple but effective: ask the model to explain the topic
    # The question should NOT contain the answer
    
    # Extract the subject (rough heuristic: first noun phrase before a verb)
    # For now, use a template that works well empirically
    return f"Regarding the following topic, what can you tell me? Be specific with details, numbers, and technical specifics if you know them: {prop[:80]}..."


def generate_targeted_question(api_key: str, proposition: str) -> str:
    """Generate a targeted question using an LLM that tests the specific fact WITHOUT revealing it.
    
    The question should be natural, specific enough to have one right answer,
    but must NOT contain the answer itself.
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://expertpack.ai",
        "X-Title": "ExpertPack EK Question Generator",
    }
    
    payload = {
        "model": "openai/gpt-4.1-mini",
        "messages": [{
            "role": "user",
            "content": f"""Convert this factual statement into a question that tests whether someone knows this specific fact.

FACT: {proposition}

CRITICAL RULES:
- The question MUST NOT contain ANY numbers, timeframes, specific values, percentages, prices, or technical details from the fact
- The question should ask about the TOPIC, letting the respondent supply the specific details from memory
- Strip ALL specifics — the whole point is to see if they know the details without being told
- The question should be natural — like something a practitioner would ask
- The question should be specific enough that there's one correct answer
- Do NOT start with "What do you know about" or other vague openings

Reply with ONLY the question, nothing else."""
        }],
        "max_tokens": 80,
        "temperature": 0.3,
    }
    
    try:
        resp = requests.post(OPENROUTER_BASE, headers=headers, json=payload, timeout=15)
        resp.raise_for_status()
        question = resp.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        if question:
            return question
    except Exception:
        pass
    
    # Fallback: simple topic extraction
    words = proposition.split()
    topic = " ".join(words[:6])
    return f"What are the specific technical details about {topic}?"


# --- Blind Probing ---

def probe_model(api_key: str, model: str, question: str, max_retries: int = 3) -> dict:
    """Send a blind probe to a model via OpenRouter. Returns the response."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://expertpack.ai",
        "X-Title": "ExpertPack EK Evaluator",
    }
    
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are a knowledgeable technical assistant. Answer the question directly and specifically. If you don't know the answer or are unsure, say 'I don't know' rather than guessing. Be precise with numbers, settings, and technical details."
            },
            {
                "role": "user", 
                "content": question
            }
        ],
        "max_tokens": 300,
        "temperature": 0.1,  # Low temp for factual consistency
    }
    
    for attempt in range(max_retries):
        try:
            resp = requests.post(OPENROUTER_BASE, headers=headers, json=payload, timeout=30)
            
            if resp.status_code == 429:
                retry_after = int(resp.headers.get("Retry-After", 5))
                print(f"  Rate limited, waiting {retry_after}s...", file=sys.stderr)
                time.sleep(retry_after)
                continue
            
            resp.raise_for_status()
            data = resp.json()
            
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            usage = data.get("usage", {})
            
            return {
                "content": content,
                "input_tokens": usage.get("prompt_tokens", 0),
                "output_tokens": usage.get("completion_tokens", 0),
                "model": model,
            }
        
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            return {"content": "", "error": "timeout", "model": model}
        
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            return {"content": "", "error": str(e), "model": model}
    
    return {"content": "", "error": "max retries exceeded", "model": model}


# --- Scoring ---

def score_response_llm(api_key: str, proposition: str, response: str) -> str:
    """Score a model's response against the ground truth proposition using LLM-as-judge.
    
    Returns: 'ek' (esoteric), 'gk' (general knowledge), or 'partial'
    
    Uses a cheap, fast model as judge to determine whether the probed model
    demonstrated knowledge of the specific fact in the proposition.
    """
    # Quick checks before calling the judge
    resp_lower = response.lower().strip()
    
    # Explicit refusal / uncertainty → EK (no judge needed)
    refusal_signals = [
        "i don't know", "i'm not sure", "i don't have specific",
        "i'm not familiar", "not aware of", "cannot confirm",
        "i lack specific", "beyond my knowledge",
    ]
    for signal in refusal_signals:
        if signal in resp_lower:
            return "ek"
    
    # Empty or very short response → EK
    if len(resp_lower) < 20:
        return "ek"
    
    # Use LLM judge for nuanced scoring
    judge_prompt = f"""Judge whether this AI response demonstrates knowledge of a specific fact.

GROUND TRUTH: {proposition}

AI RESPONSE (given WITHOUT the ground truth above): {response[:500]}

Scoring — be strict:
- GK: Response contains the SAME specific details as the ground truth (matching numbers, names, technical specifics, mechanisms). All key distinguishing details must be present and correct. Merely discussing the same general topic area is NOT enough.
- EK: Response is wrong about the specifics, vague, generic, discusses a different aspect of the topic, or is missing the key details that make this fact unique. If the response covers the right topic but at a surface level without the ground truth's specific details, score EK.
- PARTIAL: Gets SOME specific details right but not all (e.g., correct mechanism but wrong values, or correct values but wrong context). Use sparingly.

Reply with ONLY one word: GK, EK, or PARTIAL"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://expertpack.ai",
        "X-Title": "ExpertPack EK Judge",
    }
    
    payload = {
        "model": "anthropic/claude-sonnet-4-6",  # Better judge than mini models
        "messages": [{"role": "user", "content": judge_prompt}],
        "max_tokens": 5,
        "temperature": 0.0,
    }
    
    try:
        resp = requests.post(OPENROUTER_BASE, headers=headers, json=payload, timeout=15)
        resp.raise_for_status()
        
        judge_answer = resp.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip().upper()
        
        if "GK" in judge_answer:
            return "gk"
        elif "EK" in judge_answer:
            return "ek"
        elif "PARTIAL" in judge_answer:
            return "partial"
        else:
            # Fallback: if judge gave unexpected output, default to partial
            return "partial"
    
    except Exception:
        # If judge fails, fall back to simple heuristic
        return "partial"


# --- Main Evaluation ---

def run_evaluation(pack_path: Path, models: list[str], sample_size: int = 0, api_key: str = "") -> dict:
    """Run the full EK evaluation on a pack."""
    
    print(f"\n{'='*60}")
    print(f"ExpertPack EK Ratio Evaluation")
    print(f"Pack: {pack_path}")
    print(f"Models: {', '.join(models)}")
    print(f"{'='*60}\n")
    
    # 1. Extract propositions
    print("Extracting propositions...")
    all_props = extract_all_propositions(pack_path)
    
    if not all_props:
        print("ERROR: No propositions found. Run the improvement pipeline first to generate propositions/.", file=sys.stderr)
        sys.exit(1)
    
    print(f"  Found {len(all_props)} propositions across {len(find_proposition_files(pack_path))} files")
    
    # 2. Sample if requested
    if sample_size and sample_size < len(all_props):
        import random
        random.seed(42)  # Reproducible sampling
        all_props = random.sample(all_props, sample_size)
        print(f"  Sampled {sample_size} propositions for evaluation")
    
    # 3. Probe each proposition against each model
    results = []
    total_probes = len(all_props) * len(models)
    probe_count = 0
    
    print(f"\nProbing {len(all_props)} propositions × {len(models)} models = {total_probes} API calls...")
    print(f"Estimated time: ~{total_probes * 2}s\n")
    
    for i, prop in enumerate(all_props):
        # Generate question (uses LLM to create a question that doesn't reveal the answer)
        time.sleep(0.5)
        question = generate_targeted_question(api_key, prop["text"])
        
        prop_result = {
            "proposition": prop["text"],
            "source_file": prop["source_file"],
            "section": prop["section"],
            "question": question,
            "model_scores": {},
            "final_classification": None,
        }
        
        any_model_knows = False
        all_ek = True
        
        for model in models:
            probe_count += 1
            progress = f"[{probe_count}/{total_probes}]"
            
            # Rate limiting: 1.5s between probes (probe + judge = 2 calls each)
            time.sleep(1.5)
            
            print(f"  {progress} Probing {model.split('/')[-1]}...", end=" ", flush=True)
            
            response = probe_model(api_key, model, question)
            
            if response.get("error"):
                print(f"ERROR: {response['error']}")
                score = "ek"  # Treat errors as EK (model couldn't answer)
            else:
                score = score_response_llm(api_key, prop["text"], response["content"])
                print(f"→ {score.upper()}")
            
            prop_result["model_scores"][model] = {
                "score": score,
                "response_excerpt": response.get("content", "")[:200],
                "tokens": response.get("input_tokens", 0) + response.get("output_tokens", 0),
            }
            
            if score == "gk":
                any_model_knows = True
                all_ek = False
            elif score == "partial":
                all_ek = False
        
        # Union rule: if ANY model knows it → GK; if all EK → EK; otherwise → Partial
        if any_model_knows:
            prop_result["final_classification"] = "gk"
        elif all_ek:
            prop_result["final_classification"] = "ek"
        else:
            prop_result["final_classification"] = "partial"
        
        results.append(prop_result)
        
        # Progress summary every 10 propositions
        if (i + 1) % 10 == 0:
            ek_so_far = sum(1 for r in results if r["final_classification"] == "ek")
            partial_so_far = sum(1 for r in results if r["final_classification"] == "partial")
            gk_so_far = sum(1 for r in results if r["final_classification"] == "gk")
            running_ratio = (ek_so_far + 0.5 * partial_so_far) / len(results)
            print(f"\n  --- Progress: {len(results)} props | EK={ek_so_far} Partial={partial_so_far} GK={gk_so_far} | Running EK ratio: {running_ratio:.2f} ---\n")
    
    # 4. Calculate aggregate metrics
    ek_count = sum(1 for r in results if r["final_classification"] == "ek")
    partial_count = sum(1 for r in results if r["final_classification"] == "partial")
    gk_count = sum(1 for r in results if r["final_classification"] == "gk")
    total = len(results)
    
    ek_ratio = (ek_count + 0.5 * partial_count) / total if total > 0 else 0
    
    # Per-section breakdown
    section_scores = {}
    for r in results:
        sec = r["section"]
        if sec not in section_scores:
            section_scores[sec] = {"ek": 0, "partial": 0, "gk": 0, "total": 0}
        section_scores[sec][r["final_classification"]] += 1
        section_scores[sec]["total"] += 1
    
    section_ratios = {}
    for sec, counts in section_scores.items():
        section_ratios[sec] = round(
            (counts["ek"] + 0.5 * counts["partial"]) / counts["total"], 2
        )
    
    # 5. Build output
    output = {
        "pack": str(pack_path),
        "measured": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "models": models,
        "propositions_total": total,
        "ek_count": ek_count,
        "partial_count": partial_count,
        "gk_count": gk_count,
        "ek_ratio": round(ek_ratio, 3),
        "by_section": dict(sorted(section_ratios.items(), key=lambda x: -x[1])),
        "interpretation": interpret_ratio(ek_ratio),
        "details": results,
    }
    
    # 6. Print summary
    print(f"\n{'='*60}")
    print(f"EK Analysis: {pack_path.name}")
    print(f"{'='*60}")
    print(f"Total propositions:  {total}")
    print(f"Esoteric (EK):       {ek_count} ({ek_count/total*100:.1f}%)")
    print(f"Partial:             {partial_count} ({partial_count/total*100:.1f}%)")
    print(f"General (GK):        {gk_count} ({gk_count/total*100:.1f}%)")
    print(f"{'─'*40}")
    print(f"EK Ratio:            {ek_ratio:.3f}")
    print(f"Interpretation:      {interpret_ratio(ek_ratio)}")
    print(f"\nHighest EK sections:")
    for sec, ratio in sorted(section_ratios.items(), key=lambda x: -x[1])[:5]:
        print(f"  {sec:30s} → {ratio:.2f}")
    print(f"\nLowest EK sections:")
    for sec, ratio in sorted(section_ratios.items(), key=lambda x: x[1])[:3]:
        print(f"  {sec:30s} → {ratio:.2f}")
    print(f"{'='*60}\n")
    
    return output


def interpret_ratio(ratio: float) -> str:
    if ratio >= 0.80:
        return "Exceptional — almost entirely esoteric"
    elif ratio >= 0.60:
        return "Strong — majority esoteric content"
    elif ratio >= 0.40:
        return "Mixed — significant general knowledge padding"
    elif ratio >= 0.20:
        return "Weak — most content already in model weights"
    else:
        return "Minimal value-add"


# --- CLI ---

def main():
    parser = argparse.ArgumentParser(
        description="Measure ExpertPack EK (Esoteric Knowledge) ratio via blind probing"
    )
    parser.add_argument("pack_path", type=Path, help="Path to the ExpertPack directory")
    parser.add_argument(
        "--models", type=str, default=",".join(DEFAULT_MODELS),
        help=f"Comma-separated OpenRouter model IDs (default: {','.join(DEFAULT_MODELS)})"
    )
    parser.add_argument(
        "--sample", type=int, default=0,
        help="Sample N propositions instead of testing all (0 = all)"
    )
    parser.add_argument(
        "--output", type=str, default="",
        help="Output YAML file path (default: eval/ek-ratio-{date}.yaml in pack)"
    )
    
    args = parser.parse_args()
    
    if not args.pack_path.exists():
        print(f"ERROR: Pack path does not exist: {args.pack_path}", file=sys.stderr)
        sys.exit(1)
    
    models = [m.strip() for m in args.models.split(",")]
    api_key = get_api_key()
    
    # Run evaluation
    output = run_evaluation(args.pack_path, models, args.sample, api_key)
    
    # Save results
    if args.output:
        out_path = Path(args.output)
    else:
        eval_dir = args.pack_path / "eval"
        eval_dir.mkdir(exist_ok=True)
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        out_path = eval_dir / f"ek-ratio-{date_str}.yaml"
    
    # Write without the full details for readability; details go in a separate section
    summary = {k: v for k, v in output.items() if k != "details"}
    
    with open(out_path, "w") as f:
        yaml.dump(summary, f, default_flow_style=False, sort_keys=False, width=120)
        f.write("\n# --- Per-proposition details ---\n")
        f.write("# details:\n")
        for d in output["details"]:
            f.write(f"#   - proposition: {d['proposition'][:80]}...\n")
            f.write(f"#     classification: {d['final_classification']}\n")
            for model, ms in d["model_scores"].items():
                f.write(f"#     {model.split('/')[-1]}: {ms['score']}\n")
    
    print(f"Results saved to: {out_path}")
    
    return output


if __name__ == "__main__":
    main()
