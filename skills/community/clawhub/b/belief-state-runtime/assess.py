# -*- coding: utf-8 -*-
"""
personalized by belief-state-runtime.skill configurator
2026-06-01
"""

# belief-state-runtime (c) 2026 hqzzdsda — MIT License
# https://github.com/hqzzdsda/belief-state-runtime

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
belief-assessor skill — Self-contained epistemic reasoning engine.

No external dependencies. LLM function injected by agent.

Usage:
    from assess import assess_claim, assess_incremental, get_skill_definition

    result = assess_claim("claim", evidence="evidence", llm_func=my_llm)
"""

import math
import re
import json
from typing import Optional, Callable, Dict, List

# ── LLM function type ──────────────────────────────────────────

LLMFunc = Callable[[list, float, int], str]
"""
LLM call signature:
  messages: [{"role": "user", "content": "..."}]
  temperature: float
  max_tokens: int
  -> str (LLM response text)
"""

# ── Feature definitions ──────────────────────────────────────────

LLM_FEATURES = {
    "direct_support":     "Does the evidence directly support the claim?",
    "new_info":           "Does the evidence provide new information not previously mentioned?",
    "logical_consistent": "Is the evidence logically consistent with previously known information?",
    "direct_refute":      "Does the evidence explicitly refute the claim?",
    "limitation":         "Does the evidence point out limitations or exceptions?",
    "error_outdated":     "Does the evidence reveal that the claim contains errors or outdated info?",
}

# ── Result dataclass ──────────────────────────────────────────

class FeatureResult:
    __slots__ = [
        'source_reliability', 'evidence_density', 'temporal_freshness',
        'provenance_quality', 'quality_factor', 'features', 'support_score',
        'refute_score', 'raw_confidence', 'final_confidence', 'state',
        'direct_refute', 'limitation',
    ]

    def __init__(self):
        self.source_reliability = 0.5
        self.evidence_density = 0.0
        self.temporal_freshness = 0.5
        self.provenance_quality = 0.2
        self.quality_factor = 0.5
        self.features = {}
        self.support_score = 0.0
        self.refute_score = 0.0
        self.raw_confidence = 0.5
        self.final_confidence = 0.5
        self.state = "UNCERTAIN"
        self.direct_refute = False
        self.limitation = False


# ── Core engine ──────────────────────────────────────────

class FeatureExtractor:
    """
    Universal Belief Update Engine v1.

    Rule layer (4 continuous signals) + LLM layer (6 boolean features) -> confidence + state
    """

    def __init__(self, llm_func: LLMFunc):
        if llm_func is None:
            raise ValueError("llm_func is required. Pass your agent's LLM call function.")
        self.llm_func = llm_func

    def extract(
        self,
        claim: str,
        evidence: str,
        previous_confidence: Optional[float] = None,
        alpha: float = 0.5,
    ) -> FeatureResult:
        result = FeatureResult()

        # Layer 1: Rule layer
        self._extract_rule_signals(evidence, result)

        # Layer 2: LLM layer
        self._extract_llm_features(claim, evidence, result)

        # Quality factor Q
        result.quality_factor = (
            0.4 * result.source_reliability +
            0.3 * result.evidence_density +
            0.2 * result.temporal_freshness +
            0.1 * result.provenance_quality
        )

        # Support and refute scores
        f = result.features
        result.support_score = (
            (1.0 if f.get("direct_support") else 0.0) +
            (0.5 if f.get("new_info") else 0.0) +
            (0.3 if f.get("logical_consistent") else 0.0)
        ) / 1.8

        result.refute_score = (
            (1.0 if f.get("direct_refute") else 0.0) +
            (0.6 if f.get("error_outdated") else 0.0)
        ) / 1.6

        result.direct_refute = f.get("direct_refute", False)
        result.limitation = f.get("limitation", False)

        # Raw confidence
        semantic = result.support_score * (1 - result.refute_score)
        raw_conf = 0.6 * semantic + 0.4 * result.quality_factor
        if result.limitation:
            raw_conf *= 0.85
        result.raw_confidence = min(1.0, max(0.0, raw_conf))

        # Contradiction override
        if result.direct_refute:
            result.state = "CONTESTED"
            result.final_confidence = min(result.raw_confidence, 0.6)
            return result

        # Incremental update
        result.final_confidence = self._incremental_update(
            result.raw_confidence, previous_confidence, alpha,
        )

        # State determination
        result.state = self._determine_state(result.final_confidence)
        return result

    # ── Rule layer ──────────────────────────────────────────

    def _extract_rule_signals(self, evidence: str, result: FeatureResult):
        if not evidence:
            result.source_reliability = 0.4
            result.evidence_density = 0.0
            result.temporal_freshness = 0.7
            result.provenance_quality = 0.5
            return

        text = evidence.lower()

        # Source reliability
        domains = re.findall(r'https?://([^\s/]+)', evidence)
        if domains:
            scores = [self._domain_score(d) for d in domains]
            result.source_reliability = sum(scores) / len(scores)
        else:
            result.source_reliability = self._keyword_reliability(text)

        # Evidence density
        segments = re.split(r'\n\n|(?<=[.。])\s+', evidence)
        segments = [s.strip() for s in segments if len(s.strip()) > 20]
        result.evidence_density = min(1.0, 0.3 + len(segments) * 0.2)

        # Temporal freshness
        years = re.findall(r'\b((?:19|20)\d{2})\b', evidence)
        if years:
            latest = max(int(y) for y in years)
            age = 2026 - latest
            result.temporal_freshness = round(1.0 / (1.0 + age), 4)
        else:
            result.temporal_freshness = 0.7

        # Provenance quality
        unique_tlds = set()
        for d in domains:
            parts = d.split(".")
            tld = ".".join(parts[-2:]) if len(parts) >= 2 else d
            unique_tlds.add(tld)
        result.provenance_quality = min(1.0, 0.4 + len(unique_tlds) * 0.2) if unique_tlds else 0.5

    def _domain_score(self, domain: str) -> float:
        domain = domain.lower()
        for pattern, score in [
            ("gov", 0.9),
            ("edu", 0.9),
            ("who.int", 0.9),
            ("pubmed.ncbi", 0.9),
            ("nature.com", 0.9),
            ("science.org", 0.9),
            ("reuters.com", 0.7),
            ("bbc.com", 0.7),
            ("apnews.com", 0.7),
            ("nytimes.com", 0.7),
            ("theguardian.com", 0.7),
            ("arxiv.org", 0.6),
            ("wikipedia.org", 0.5),
            ("twitter.com", 0.3),
            ("x.com", 0.3),
            ("reddit.com", 0.3)
        ]:
            if pattern in domain:
                return score
        if domain.endswith(".gov") or domain.endswith(".edu"):
            return 0.9
        if domain.endswith(".org"):
            return 0.6
        return 0.5

    def _keyword_reliability(self, text: str) -> float:
        for keywords, score in [
            (["official", "government", "who", "nih", "fda", "央行", "官方", "政府"], 0.9),
            (["research", "study", "journal", "nature", "science", "研究", "论文", "期刊"], 0.8),
            (["report", "survey", "statistics", "报告", "白皮书", "调查", "统计"], 0.7),
            (["news", "reported", "新闻", "报道", "媒体"], 0.6),
            (["forum", "social media", "twitter", "论坛", "社交媒体", "网友"], 0.3),
        ]:
            if any(w in text for w in keywords):
                return score
        return 0.6

    # ── LLM layer ──────────────────────────────────────────

    def _extract_llm_features(self, claim: str, evidence: str, result: FeatureResult):
        prompt = f"""You are a fact verification assistant. Based on the following [Claim] and [New Evidence], answer 6 judgments. Output only a JSON object, no other text.

Claim: {claim}
New Evidence: {evidence[:1500]}

Judgment criteria:
1. direct_support: Does the evidence directly support the claim?
2. new_info: Does the evidence provide new information not previously mentioned?
3. logical_consistent: Is the evidence logically consistent with previously known information?
4. direct_refute: Does the evidence explicitly refute the claim?
5. limitation: Does the evidence point out limitations or exceptions?
6. error_outdated: Does the evidence reveal that the claim contains errors or outdated info?

Output format:
{{"direct_support": true/false, "new_info": true/false, "logical_consistent": true/false, "direct_refute": true/false, "limitation": true/false, "error_outdated": false}}"""

        features = {fid: False for fid in LLM_FEATURES}

        try:
            response = self.llm_func([{"role": "user", "content": prompt}], 0.05, 256)
            features = self._parse_features(response)
        except Exception as e:
            print(f"[WARN] LLM feature extraction failed: {e}")

        result.features = features

    def _parse_features(self, response: str) -> Dict[str, bool]:
        features = {fid: False for fid in LLM_FEATURES}

        try:
            json_match = re.search(r'\{[^{}]+\}', response)
            if json_match:
                data = json.loads(json_match.group())
                for fid in LLM_FEATURES:
                    val = data.get(fid)
                    if isinstance(val, bool):
                        features[fid] = val
                    elif isinstance(val, str):
                        features[fid] = val.lower() in ("true", "yes", "1")
                    elif isinstance(val, (int, float)):
                        features[fid] = bool(val)
                return features
        except (json.JSONDecodeError, AttributeError):
            pass

        # Fallback: regex
        for fid in LLM_FEATURES:
            pattern = re.compile(rf'"{fid}"\s*:\s*(true|false)', re.IGNORECASE)
            match = pattern.search(response)
            if match:
                features[fid] = match.group(1).lower() == "true"
            else:
                pattern2 = re.compile(rf'{fid}\s*[:=]\s*(true|false)', re.IGNORECASE)
                match2 = pattern2.search(response)
                if match2:
                    features[fid] = match2.group(1).lower() == "true"

        return features

    # ── Incremental update ──────────────────────────────────────────

    def _incremental_update(
        self, raw_conf: float, old_conf: Optional[float], alpha: float,
    ) -> float:
        if old_conf is None:
            return raw_conf
        delta = raw_conf - old_conf
        if delta > 0.1:
            return alpha * raw_conf + (1 - alpha) * old_conf
        elif delta < -0.1:
            return min(old_conf, raw_conf)
        else:
            return (old_conf + raw_conf) / 2.0

    def _determine_state(self, confidence: float) -> str:
        if confidence >= 0.65:
            return "VERIFIED"
        elif confidence <= 0.25:
            return "UNCERTAIN"
        else:
            return "CONTESTED"


# ── Public API ──────────────────────────────────────────

_extractors = {}

def _get_extractor(llm_func: LLMFunc) -> FeatureExtractor:
    key = id(llm_func)
    if key not in _extractors:
        _extractors[key] = FeatureExtractor(llm_func=llm_func)
    return _extractors[key]


def assess_claim(
    claim: str,
    evidence: str = "",
    previous_confidence: float = None,
    llm_func: LLMFunc = None,
) -> dict:
    """
    Evaluate the trustworthiness of a claim.

    Args:
        claim: The claim to evaluate
        evidence: Evidence text (optional)
        previous_confidence: Previous confidence for incremental update (optional)
        llm_func: LLM call function (required)
                  Signature: (messages: list[dict], temperature: float, max_tokens: int) -> str

    Returns:
        dict with state, confidence, features, summary
    """
    if llm_func is None:
        raise ValueError("llm_func is required. Pass your agent's LLM call function.")

    ext = _get_extractor(llm_func)
    result = ext.extract(claim, evidence, previous_confidence=previous_confidence)

    return {
        "state": result.state,
        "confidence": result.final_confidence,
        "confidence_range": [
            max(0.0, result.final_confidence - 0.15),
            min(1.0, result.final_confidence + 0.15),
        ],
        "quality_factor": round(result.quality_factor, 3),
        "support_score": round(result.support_score, 3),
        "refute_score": round(result.refute_score, 3),
        "features": result.features,
        "direct_refute": result.direct_refute,
        "limitation": result.limitation,
        "summary": _generate_summary(result),
    }


def assess_incremental(
    claim: str,
    evidence_stages: list,
    llm_func: LLMFunc = None,
) -> list:
    """
    Incremental evaluation: add evidence stage by stage.

    Args:
        claim: The claim to evaluate
        evidence_stages: List of evidence texts, added sequentially
        llm_func: LLM call function (required)

    Returns:
        List of results, one per stage
    """
    if llm_func is None:
        raise ValueError("llm_func is required.")

    ext = _get_extractor(llm_func)
    results = []
    prev_conf = None

    for i, evidence in enumerate(evidence_stages):
        result = ext.extract(claim, evidence, previous_confidence=prev_conf)
        entry = {
            "step": i + 1,
            "evidence_preview": evidence[:100],
            "state": result.state,
            "confidence": result.final_confidence,
            "support_score": round(result.support_score, 3),
            "refute_score": round(result.refute_score, 3),
            "quality_factor": round(result.quality_factor, 3),
            "features": {k: v for k, v in result.features.items() if v},
            "delta": round(result.final_confidence - prev_conf, 3) if prev_conf is not None else 0.0,
        }
        results.append(entry)
        prev_conf = result.final_confidence

    return results


# ── AI-Friendly Interface ──────────────────────────────────────────

def get_assessment_prompt(claim: str, evidence: str = "") -> str:
    """
    Return the prompt that should be answered by the AI agent.
    
    Use this when the agent itself will act as the LLM:
    1. Call get_assessment_prompt(claim, evidence)
    2. AI agent (you) answers the prompt by providing 6 boolean judgments
    3. Pass the AI's response to assess_claim_with_response()
    
    Returns:
        str: The prompt text the AI agent should answer
    """
    return f"""You are a fact verification assistant. Based on the following [Claim] and [New Evidence], answer 6 judgments. Output only a JSON object, no other text.

Claim: {claim}
New Evidence: {evidence[:1500] if evidence else "(No evidence provided)"}

Judgment criteria:
1. direct_support: Does the evidence directly support the claim?
2. new_info: Does the evidence provide new information not previously mentioned?
3. logical_consistent: Is the evidence logically consistent with previously known information?
4. direct_refute: Does the evidence explicitly refute the claim?
5. limitation: Does the evidence point out limitations or exceptions?
6. error_outdated: Does the evidence reveal that the claim contains errors or outdated info?

Output format:
{{"direct_support": true/false, "new_info": true/false, "logical_consistent": true/false, "direct_refute": true/false, "limitation": true/false, "error_outdated": false}}"""


def assess_claim_with_response(
    claim: str,
    evidence: str = "",
    llm_response: str = "",
    previous_confidence: float = None,
) -> dict:
    """
    Complete assessment using an AI agent's response.
    
    Use this when the AI agent has already answered the assessment prompt:
    1. Call get_assessment_prompt(claim, evidence) to get the prompt
    2. AI agent (you) answers the 6 boolean judgments
    3. Pass the AI's answer as llm_response here
    4. Returns the full assessment result
    
    Args:
        claim: The claim to evaluate
        evidence: Evidence text
        llm_response: The AI agent's JSON response to the assessment prompt
        previous_confidence: Previous confidence for incremental update
    
    Returns:
        dict with state, confidence, features, summary
    """
    # Parse the AI's response into features
    features = {fid: False for fid in LLM_FEATURES}
    
    if llm_response:
        try:
            json_match = re.search(r'\{[^{}]+\}', llm_response)
            if json_match:
                data = json.loads(json_match.group())
                for fid in LLM_FEATURES:
                    val = data.get(fid)
                    if isinstance(val, bool):
                        features[fid] = val
                    elif isinstance(val, str):
                        features[fid] = val.lower() in ("true", "yes", "1")
                    elif isinstance(val, (int, float)):
                        features[fid] = bool(val)
        except (json.JSONDecodeError, AttributeError):
            # Fallback: extract booleans from text
            for fid in LLM_FEATURES:
                pattern = re.compile(rf'"{fid}"\s*:\s*(true|false)', re.IGNORECASE)
                match = pattern.search(llm_response)
                if match:
                    features[fid] = match.group(1).lower() == "true"
    
    # Now run the full assessment using the parsed features
    return _compute_from_features(claim, evidence, features, previous_confidence)


def _compute_from_features(
    claim: str,
    evidence: str,
    features: Dict[str, bool],
    previous_confidence: Optional[float] = None,
    alpha: float = 0.5,
) -> dict:
    """Compute the full assessment result from pre-extracted features."""
    result = FeatureResult()
    
    # Layer 1: Rule layer
    extractor = FeatureExtractor(llm_func=lambda m, t, mt: "{}")
    extractor._extract_rule_signals(evidence, result)
    
    # Set features directly
    result.features = features
    result.direct_refute = features.get("direct_refute", False)
    result.limitation = features.get("limitation", False)
    
    # Quality factor Q
    result.quality_factor = (
        0.4 * result.source_reliability +
        0.3 * result.evidence_density +
        0.2 * result.temporal_freshness +
        0.1 * result.provenance_quality
    )
    
    # Support and refute scores
    f = result.features
    result.support_score = (
        (1.0 if f.get("direct_support") else 0.0) +
        (0.5 if f.get("new_info") else 0.0) +
        (0.3 if f.get("logical_consistent") else 0.0)
    ) / 1.8
    
    result.refute_score = (
        (1.0 if f.get("direct_refute") else 0.0) +
        (0.6 if f.get("error_outdated") else 0.0)
    ) / 1.6
    
    # Raw confidence
    semantic = result.support_score * (1 - result.refute_score)
    raw_conf = 0.6 * semantic + 0.4 * result.quality_factor
    if result.limitation:
        raw_conf *= 0.85
    result.raw_confidence = min(1.0, max(0.0, raw_conf))
    
    # Contradiction override
    if result.direct_refute:
        result.state = "CONTESTED"
        result.final_confidence = min(result.raw_confidence, 0.6)
    else:
        result.final_confidence = extractor._incremental_update(
            result.raw_confidence, previous_confidence, alpha,
        )
        result.state = extractor._determine_state(result.final_confidence)
    
    return {
        "state": result.state,
        "confidence": result.final_confidence,
        "confidence_range": [
            max(0.0, result.final_confidence - 0.15),
            min(1.0, result.final_confidence + 0.15),
        ],
        "quality_factor": round(result.quality_factor, 3),
        "support_score": round(result.support_score, 3),
        "refute_score": round(result.refute_score, 3),
        "features": result.features,
        "direct_refute": result.direct_refute,
        "limitation": result.limitation,
        "summary": _generate_summary(result),
    }


def get_skill_definition() -> dict:
    """Return skill definition for agent framework registration."""
    return {
        "name": "belief_assessor",
        "description": "Evaluate the trustworthiness of a claim based on evidence. Outputs structured belief state and calibrated confidence.",
        "parameters": {
            "claim": {
                "type": "string",
                "required": True,
                "description": "The claim to evaluate",
            },
            "evidence": {
                "type": "string",
                "required": False,
                "description": "Evidence text supporting or refuting the claim",
            },
        },
        "returns": {
            "state": "VERIFIED / CONTESTED / UNCERTAIN",
            "confidence": "0.0-1.0",
            "confidence_range": "[lower, upper]",
            "features": "6 boolean judgment bases",
            "summary": "One-sentence summary",
        },
    }


def _generate_summary(result) -> str:
    parts = []
    if result.direct_refute:
        parts.append("Evidence explicitly refutes the claim")
    elif result.state == "VERIFIED":
        if result.final_confidence >= 0.85:
            parts.append("Evidence strongly supports the claim")
        else:
            parts.append("Evidence supports the claim")
    elif result.state == "CONTESTED":
        if result.limitation:
            parts.append("Evidence supports but with limitations")
        else:
            parts.append("Evidence is disputed")
    else:
        parts.append("Insufficient evidence to judge")

    true_feats = [k for k, v in result.features.items() if v]
    if "new_info" in true_feats:
        parts.append("provides new information")
    if "error_outdated" in true_feats:
        parts.append("information may be outdated")

    return ", ".join(parts) if parts else "Unable to assess"
