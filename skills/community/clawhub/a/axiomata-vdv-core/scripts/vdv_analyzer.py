#!/usr/bin/env python3
"""
VDV Analyzer v1.0 — Vision de Vérité: Core Analysis Script
Universal, impersonal truth-seeking engine.

Usage:
    python3 vdv_analyzer.py --input "<text>" --mode quick
    python3 vdv_analyzer.py --input "<text>" --mode compress
    python3 vdv_analyzer.py --input "<file>" --mode density
    python3 vdv_analyzer.py --verify-phi
    python3 vdv_analyzer.py --store "<result>"
"""

import sys
import json
import argparse
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path

# ─────────────────────────────────────────────────────────────
# PHI CONSTANT — Golden Ratio for stability validation
# ─────────────────────────────────────────────────────────────
PHI = 1.618033988749895


@dataclass
class VDVResult:
    trigger: str
    silence: str
    tensions: List[str]
    attractor: str
    reinforcement: Dict
    phi_score: float


def detect_trigger(text: str) -> Tuple[bool, str]:
    """Detect if VDV should be triggered."""
    triggers = {
        "contradiction": ["mais", "however", "却", "然而", "矛盾", "yet", "but"],
        "entropy": ["complex", "unclear", "confusing", "复杂", "不清楚"],
        "non_dits": ["should", "must", "hidden", "应该", "必须"],
        "resistance": ["cannot", "unable", "block", "不能", "无法"]
    }
    
    detected = []
    text_lower = text.lower()
    
    for trigger_type, keywords in triggers.items():
        for kw in keywords:
            if kw in text_lower:
                detected.append(trigger_type)
                break
    
    if detected:
        return True, f"Triggers: {', '.join(set(detected))}"
    return False, "No clear trigger"


def logical_silence(text: str) -> str:
    """Phase 2: Observe without judging."""
    sentences = re.split(r'[.!?\n]', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if len(sentences) <= 3:
        return "Simple structure — observe main claim"
    
    # Find non-obvious elements
    non_dits = []
    for sent in sentences:
        # Sentences with passive voice, should/must, hidden references
        if any(kw in sent.lower() for kw in ["should", "must", "hidden", "perhaps", "probably"]):
            non_dits.append(sent)
    
    if non_dits:
        return f"Possible non-dits detected: {'; '.join(non_dits[:3])}"
    return "No obvious non-dits — observe structure"


def map_tensions(text: str) -> List[str]:
    """Phase 3: Map resistance and tension points."""
    tensions = []
    
    # Look for contradictions
    if re.search(r'\b(mais|toutefois|ceppendant|however|but|yet)\b', text, re.IGNORECASE):
        tensions.append("Contradiction marker detected")
    
    # Look for forced logic (should/must = coercion markers)
    should_count = len(re.findall(r'\b(should|must|ought to|devrait|doit)\b', text, re.IGNORECASE))
    if should_count >= 3:
        tensions.append(f"High coercion density: {should_count} should/must patterns")
    
    # Look for complexity (nested clauses)
    comma_count = text.count(',')
    if comma_count >= 10:
        tensions.append(f"High complexity: {comma_count} commas")
    
    # Look for evasion patterns
    if re.search(r'il semble que|it seems that|appear to|似乎', text, re.IGNORECASE):
        tensions.append("Evasive language: 'seems/appears'")
    
    return tensions if tensions else ["No strong tensions detected"]


def localize_attractor(text: str) -> str:
    """Phase 4: Find invariant point via compression."""
    # Remove everything that can be removed
    sentences = re.split(r'[.!?\n]', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
    
    if not sentences:
        return "No substantial content to compress"
    
    # Score each sentence by "weight" (length, keyword density)
    scored = []
    for sent in sentences:
        score = len(sent)
        # Sentences with "truth" words get bonus
        if any(kw in sent.lower() for kw in ["true", "truth", "real", "essential", "核心", "真实"]):
            score += 20
        # Sentences with many conjunctions are less central
        if sent.lower().count(' and ') > 2:
            score -= 10
        scored.append((sent, score))
    
    # Sort by score, highest first
    scored.sort(key=lambda x: x[1], reverse=True)
    
    # Top candidate
    if scored:
        top = scored[0][0][:100]
        return f"Rigid point candidate: '{top}...' ({len(sentences)} sentences analyzed)"
    
    return "Could not determine attractor"


def compute_phi_score(text: str) -> float:
    """
    Compute phi-score: how close to golden ratio stability.
    Returns value between 0-1 where 1 = perfect phi alignment.
    """
    # Simplified: measure structure coherence vs chaos
    sentences = re.split(r'[.!?\n]', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if not sentences:
        return 0.0
    
    # Phi alignment: coherence score normalized
    coherence = min(len(sentences) / 5, 1.0)  # 5 sentences = optimal
    
    # Simplicity bonus
    avg_len = sum(len(s) for s in sentences) / len(sentences)
    simplicity = max(0, 1.0 - (avg_len / 200))  # 200 chars = neutral
    
    # Combined: coherence * 0.6 + simplicity * 0.4
    score = coherence * 0.6 + simplicity * 0.4
    
    return round(min(score, 1.0), 3)


def analyze_text(text: str, mode: str = "quick") -> Dict:
    """
    Full VDV analysis.
    
    Args:
        text: Input text or file path
        mode: quick | compress | density
    """
    trigger_detected, trigger_msg = detect_trigger(text)
    
    if mode == "quick":
        tensions = map_tensions(text)[:3]
        return {
            "mode": "quick",
            "trigger": trigger_msg,
            "attractor": localize_attractor(text),
            "phi_score": compute_phi_score(text)
        }
    
    elif mode == "compress":
        silence = logical_silence(text)
        tensions = map_tensions(text)
        attractor = localize_attractor(text)
        phi = compute_phi_score(text)
        
        return {
            "mode": "compress",
            "trigger": trigger_msg,
            "silence": silence,
            "tensions": tensions,
            "attractor": attractor,
            "phi_score": phi
        }
    
    else:  # density
        sentences = re.split(r'[.!?\n]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        word_count = sum(len(s.split()) for s in sentences)
        char_count = sum(len(s) for s in sentences)
        
        return {
            "mode": "density",
            "sentences": len(sentences),
            "words": word_count,
            "chars": char_count,
            "trigger": trigger_msg,
            "phi_score": compute_phi_score(text),
            "tension_density": len(map_tensions(text))
        }


def verify_phi() -> bool:
    """Verify phi constant."""
    computed = (1 + 5**0.5) / 2
    match = abs(computed - PHI) < 1e-12
    print(f"Phi verification: {PHI} {'✅' if match else '❌'}")
    print(f"Computed: {computed}")
    return match


def store_result(result: Dict, storage_dir: str = ".") -> str:
    """Store VDV result to local JSON."""
    storage_path = Path(storage_dir) / "vdv_results.json"
    
    results = []
    if storage_path.exists():
        with open(storage_path) as f:
            results = json.load(f)
    
    results.append({
        "timestamp": result.get("timestamp", ""),
        "result": result
    })
    
    with open(storage_path, "w") as f:
        json.dump(results[-100:], f, indent=2)  # Keep last 100
    
    return str(storage_path)


def main():
    parser = argparse.ArgumentParser(description="VDV Analyzer v1.0")
    parser.add_argument("--input", "-i", help="Text to analyze or @filepath")
    parser.add_argument("--mode", "-m", choices=["quick", "compress", "density"], 
                       default="compress", help="Analysis mode")
    parser.add_argument("--verify-phi", action="store_true", help="Verify phi constant")
    parser.add_argument("--store", "-s", help="Store result to file")
    parser.add_argument("--output-dir", "-o", default=".", help="Storage directory")
    
    args = parser.parse_args()
    
    if args.verify_phi:
        verify_phi()
        return 0
    
    if args.input:
        if args.input.startswith("@"):
            filepath = args.input[1:]
            try:
                with open(filepath) as f:
                    text = f.read()
            except FileNotFoundError:
                print(f"Error: File not found: {filepath}", file=sys.stderr)
                return 1
        else:
            text = args.input
        
        result = analyze_text(text, args.mode)
        result["timestamp"] = __import__("datetime").datetime.now().isoformat()
        
        if args.store:
            path = store_result(result, args.output_dir)
            print(f"Stored: {path}")
        else:
            print(json.dumps(result, indent=2))
        return 0
    
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())