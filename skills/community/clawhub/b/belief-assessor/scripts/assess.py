# belief-assessor v2 (c) 2026 hqzzdsda — MIT License
# https://github.com/hqzzdsda/belief-assessor

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
belief-assessor v2 — Epistemic reasoning engine with projection layer.

v2 adds: 4-way constraint system + parameterized configuration + formula-based
confidence intervals.  Zero new LLM calls.  Fully backward compatible.

Usage:
    from assess import assess_claim, assess_incremental, ProjectionConfig

    result = assess_claim("claim", evidence="evidence", llm_func=my_llm)
    # or with AI-friendly interface:
    prompt = get_assessment_prompt(claim, evidence)
    result = assess_claim_with_response(claim, evidence, ai_response)

    # Conservative strategy:
    result = assess_claim("claim", llm_func=my_llm,
                          config=ProjectionConfig.conservative())
"""

import math
import re
import json
from typing import Optional, Callable, Dict, List
from dataclasses import dataclass

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

# ── Projection Configuration ──────────────────────────────────────────

@dataclass
class ProjectionConfig:
    """Parameterized policy — replaces v1's hardcoded thresholds.

    Three presets cover all v1 use cases without the complexity of
    5 separate Policy functions in the full pipeline.
    """

    # ── Thresholds ──
    verify_threshold: float = 0.70        # >= this = VERIFIED
    contest_threshold: float = 0.25       # <= this = UNCERTAIN (middle = CONTESTED)

    # ── Constraint parameters ──

    # Constraint 1: Contradiction cap
    contradiction_cap: float = 0.55       # max confidence when refute present

    # Constraint 2: Provenance quality gate
    provenance_cap: float = 0.60          # max confidence when source quality is low
    min_provenance_quality: float = 0.55  # gate threshold

    # Constraint 3: Temporal freshness gate
    decay_threshold: float = 0.40         # freshness below this = stale
    temporal_cap: float = 0.50            # max confidence for stale evidence

    # Constraint 4: Evidence density floor
    density_floor: float = 0.30           # density below this = too sparse
    density_cap: float = 0.55             # max confidence for sparse evidence

    # ── Confidence interval parameters ──
    uncertainty_base: float = 0.5         # (1-quality) scale factor
    uncertainty_min: float = 0.1          # 1/sqrt(n_eff) scale factor

    # ── Incremental update ──
    alpha: float = 0.5                    # blend coefficient for strengthener updates

    # ── Presets ──

    @classmethod
    def standard(cls) -> "ProjectionConfig":
        """Default balanced policy. Use for general-purpose assessment."""
        return cls()

    @classmethod
    def conservative(cls) -> "ProjectionConfig":
        """High-threshold strict policy. Use for high-stakes decisions."""
        return cls(
            verify_threshold=0.78, contest_threshold=0.30,
            contradiction_cap=0.50, provenance_cap=0.55,
            min_provenance_quality=0.60, decay_threshold=0.35,
            temporal_cap=0.50, density_floor=0.35,
            uncertainty_base=0.55, uncertainty_min=0.12,
        )

    @classmethod
    def permissive(cls) -> "ProjectionConfig":
        """Low-threshold relaxed policy. Use for brainstorming / low-stakes."""
        return cls(
            verify_threshold=0.62, contest_threshold=0.20,
            contradiction_cap=0.60, provenance_cap=0.65,
            min_provenance_quality=0.45, decay_threshold=0.30,
            temporal_cap=0.55, density_floor=0.20,
            uncertainty_base=0.40, uncertainty_min=0.08,
        )


# ── Result dataclass ──────────────────────────────────────────

class FeatureResult:
    __slots__ = [
        'source_reliability', 'evidence_density', 'temporal_freshness',
        'provenance_quality', 'quality_factor', 'features', 'support_score',
        'refute_score', 'raw_confidence', 'final_confidence', 'state',
        'direct_refute', 'limitation',
        # v2 fields
        'confidence_lower', 'confidence_upper', 'veto_reasons', 'cap_applied',
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
        # v2
        self.confidence_lower = 0.0
        self.confidence_upper = 1.0
        self.veto_reasons = []
        self.cap_applied = 1.0


# ── Core engine ──────────────────────────────────────────

class FeatureExtractor:
    """
    Universal Belief Update Engine v2.

    Rule layer (4 continuous signals) + LLM layer (6 boolean features)
    → v2 Projection layer (4 constraints + formula-based CI + parameterized config)
    → confidence + state + interval + reasons
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
        config: Optional[ProjectionConfig] = None,
    ) -> FeatureResult:
        result = FeatureResult()

        # ── Layer 1: Rule layer ──
        self._extract_rule_signals(evidence, result)

        # ── Layer 2: LLM layer ──
        self._extract_llm_features(claim, evidence, result)

        # ── Quality factor Q ──
        result.quality_factor = (
            0.4 * result.source_reliability +
            0.3 * result.evidence_density +
            0.2 * result.temporal_freshness +
            0.1 * result.provenance_quality
        )

        # ── Support and refute scores ──
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

        # ── Raw confidence ──
        semantic = result.support_score * (1 - result.refute_score)
        raw_conf = 0.6 * semantic + 0.4 * result.quality_factor
        if result.limitation:
            raw_conf *= 0.85
        result.raw_confidence = min(1.0, max(0.0, raw_conf))

        # ── v2: Projection layer ──
        cfg = config or ProjectionConfig()
        self._project(result, claim, previous_confidence, cfg)

        return result

    # ── v2 Projection layer ──────────────────────────────────────────

    def _is_historical_claim(self, claim: str) -> bool:
        """Detect if a claim refers to a historical/past event.

        Historical claims about immutable past events should be exempt from
        temporal_decayed, because the year in the evidence is the event's
        time coordinate, not a sign of stale evidence.
        """
        if not claim:
            return False

        text = claim.lower()

        # Past-tense verbs and historical event markers
        past_tense_words = {
            "was", "were", "developed", "discovered", "invented", "created",
            "established", "founded", "occurred", "happened", "began",
            "ended", "completed", "published", "launched", "introduced",
            "built", "constructed", "formed", "originated",
            "fought", "won", "lost", "died", "born", "ruled", "reigned",
            "produced", "wrote", "painted", "composed", "designed",
            "previously", "originally", "historically",
            "discovered", "invented", "created",
        }
        if any(word in text for word in past_tense_words):
            return True

        # Contains a past year (19xx or pre-2025)
        year_pattern = re.compile(r'\b(19\d{2}|200\d|201\d|202[0-4])\b')
        if year_pattern.search(text):
            return True

        return False

    def _project(
        self,
        result: FeatureResult,
        claim: str,
        prev_conf: Optional[float],
        cfg: ProjectionConfig,
    ):
        """Apply 4 constraints + formula-based CI + parameterized state."""
        scalar = result.raw_confidence
        cap = 1.0
        result.veto_reasons = []

        # ── Constraint 1: Contradiction cap ──
        # If evidence refutes or contradicts, cap the confidence.
        if result.refute_score >= cfg.contest_threshold:
            cap = min(cap, cfg.contradiction_cap)
            result.veto_reasons.append("contradiction_capped")

        # Strong contradiction: refute dominates support
        if result.refute_score > result.support_score * 2:
            result.state = "CONTESTED"
            result.veto_reasons.append("contradiction_dominates")

        # Direct refutation: immediate CONTESTED, cap low
        if result.direct_refute:
            result.state = "CONTESTED"
            scalar = min(scalar, min(cap, 0.60))
            result.final_confidence = scalar
            result.confidence_lower = 0.0
            result.confidence_upper = scalar
            result.cap_applied = cap
            return  # short-circuit: direct refute is definitive

        # ── Constraint 2: Provenance quality gate ──
        if result.quality_factor < cfg.min_provenance_quality:
            cap = min(cap, cfg.provenance_cap)
            result.veto_reasons.append("provenance_gated")

        # ── Constraint 3: Temporal freshness gate ──
        # Historical claims (e.g. "WWII ended in 1945") are exempt ONLY if
        # the evidence does NOT challenge them.  If there is a fresh refutation,
        # temporal decay applies — the contradiction needs recent evidence.
        is_historical = self._is_historical_claim(claim)
        is_challenged = result.refute_score > result.support_score
        skip_temporal = is_historical and not is_challenged
        if not skip_temporal and result.temporal_freshness < cfg.decay_threshold:
            cap = min(cap, cfg.temporal_cap)
            result.veto_reasons.append("temporal_decayed")
            # If stale AND currently VERIFIED, demote to CONTESTED
            if result.state == "VERIFIED":
                result.state = "CONTESTED"

        # ── Constraint 4: Evidence density floor ──
        if result.evidence_density < cfg.density_floor:
            cap = min(cap, cfg.density_cap)
            result.veto_reasons.append("density_floor")

        # ── Apply cap ──
        scalar = min(scalar, cap)
        result.cap_applied = cap

        # ── Incremental update (preserved from v1) ──
        if prev_conf is not None:
            scalar = self._incremental_update(scalar, prev_conf, cfg.alpha)

        result.final_confidence = scalar

        # ── Formula-based confidence interval ──
        n_eff = max(int(result.evidence_density * 10), 1)
        uncertainty_margin = (
            (1.0 - result.quality_factor) * cfg.uncertainty_base +
            cfg.uncertainty_min / math.sqrt(n_eff)
        )
        result.confidence_lower = max(scalar - uncertainty_margin, 0.0)
        result.confidence_upper = min(scalar + uncertainty_margin, cap)

        # ── State determination ──
        # Don't override state if constraints already set it
        if result.state != "CONTESTED":
            cannot_verify = (
                result.quality_factor < cfg.min_provenance_quality or
                result.evidence_density < cfg.density_floor
            )
            if scalar >= cfg.verify_threshold and not cannot_verify:
                result.state = "VERIFIED"
            elif scalar <= cfg.contest_threshold:
                result.state = "UNCERTAIN"
            else:
                result.state = "CONTESTED"

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
        years = re.findall(r'(?<!\d)((?:19|20)\d{2})(?!\d)', evidence)
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
            ("gov", 0.9), ("edu", 0.9), ("who.int", 0.9),
            ("pubmed.ncbi", 0.9), ("nature.com", 0.9), ("science.org", 0.9),
            ("reuters.com", 0.7), ("bbc.com", 0.7), ("apnews.com", 0.7),
            ("nytimes.com", 0.7), ("theguardian.com", 0.7),
            ("arxiv.org", 0.6), ("wikipedia.org", 0.5),
            ("twitter.com", 0.3), ("x.com", 0.3), ("reddit.com", 0.3),
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
            (["official", "government", "who", "nih", "fda", "央行", "官方", "政府", "交通运输部", "国家统计局", "卫健委", "国务院", "工信部", "财政部", "审计"], 0.9),
            (["research", "study", "journal", "nature", "science", "研究", "论文", "期刊"], 0.8),
            (["report", "survey", "statistics", "报告", "白皮书", "调查", "统计"], 0.7),
            (["news", "reported", "新闻", "报道", "媒体"], 0.6),
            (["forum", "social media", "twitter", "reddit", "论坛", "社交媒体", "网友", "telegram", "博客", "贴吧", "小红书", "匿名", "帖子", "笔记", "微信群", "知乎", "微博", "bilibili", "抖音", "快手"], 0.3),
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

    # ── Legacy v1 compatibility ──────────────────────────────────────────

    def _determine_state(self, confidence: float) -> str:
        """Legacy state determination (v1).  Use _project() in v2."""
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
    config: Optional[ProjectionConfig] = None,
) -> dict:
    """
    Evaluate the trustworthiness of a claim.

    Args:
        claim: The claim to evaluate
        evidence: Evidence text supporting or refuting the claim (optional)
        previous_confidence: Previous confidence for incremental update (optional)
        llm_func: LLM call function (required)
                  Signature: (messages: list[dict], temperature: float, max_tokens: int) -> str
        config: ProjectionConfig for custom thresholds/constraints (optional)
                Use ProjectionConfig.conservative() for high-stakes,
                ProjectionConfig.permissive() for low-stakes.

    Returns:
        {
            "state": "VERIFIED" | "CONTESTED" | "UNCERTAIN",
            "confidence": float (0.0-1.0),
            "confidence_range": [lower, upper],
            "quality_factor": float,
            "support_score": float,
            "refute_score": float,
            "features": {"direct_support": bool, ...},
            "direct_refute": bool,
            "limitation": bool,
            "veto_reasons": [str, ...],   # v2: which constraints fired
            "summary": str
        }
    """
    if llm_func is None:
        raise ValueError("llm_func is required. Pass your agent's LLM call function.")

    ext = _get_extractor(llm_func)
    result = ext.extract(
        claim, evidence,
        previous_confidence=previous_confidence,
        config=config,
    )

    return {
        "state": result.state,
        "confidence": round(result.final_confidence, 4),
        "confidence_range": [
            round(result.confidence_lower, 4),
            round(result.confidence_upper, 4),
        ],
        "quality_factor": round(result.quality_factor, 3),
        "support_score": round(result.support_score, 3),
        "refute_score": round(result.refute_score, 3),
        "features": result.features,
        "direct_refute": result.direct_refute,
        "limitation": result.limitation,
        "veto_reasons": result.veto_reasons,
        "cap_applied": round(result.cap_applied, 3),
        "summary": _generate_summary(result),
    }


def assess_incremental(
    claim: str,
    evidence_stages: list,
    llm_func: LLMFunc = None,
    config: Optional[ProjectionConfig] = None,
) -> list:
    """
    Incremental evaluation: add evidence stage by stage.

    Args:
        claim: The claim to evaluate
        evidence_stages: List of evidence texts, processed sequentially
        llm_func: LLM call function (required)
        config: ProjectionConfig for custom thresholds/constraints (optional)

    Returns:
        List of results, one per stage
    """
    if llm_func is None:
        raise ValueError("llm_func is required.")

    ext = _get_extractor(llm_func)
    results = []
    prev_conf = None

    for i, evidence in enumerate(evidence_stages):
        result = ext.extract(
            claim, evidence,
            previous_confidence=prev_conf,
            config=config,
        )
        entry = {
            "step": i + 1,
            "evidence_preview": evidence[:100],
            "state": result.state,
            "confidence": round(result.final_confidence, 4),
            "confidence_range": [
                round(result.confidence_lower, 4),
                round(result.confidence_upper, 4),
            ],
            "support_score": round(result.support_score, 3),
            "refute_score": round(result.refute_score, 3),
            "quality_factor": round(result.quality_factor, 3),
            "features": {k: v for k, v in result.features.items() if v},
            "veto_reasons": result.veto_reasons,
            "delta": round(result.final_confidence - prev_conf, 4) if prev_conf is not None else 0.0,
        }
        results.append(entry)
        prev_conf = result.final_confidence

    return results


# ── AI-Friendly Interface ──────────────────────────────────────────

def get_assessment_prompt(claim: str, evidence: str = "") -> str:
    """
    Return the prompt that the AI agent should answer with 6 boolean judgments.

    Workflow:
    1. Agent searches for evidence (online-search, multi-search-engine, etc.)
    2. Call get_assessment_prompt(claim, collected_evidence)
    3. AI agent answers the prompt with 6 booleans in JSON
    4. Call assess_claim_with_response(claim, evidence, ai_response)

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
    config: Optional[ProjectionConfig] = None,
) -> dict:
    """
    Complete assessment using the AI agent's 6-boolean response.

    Use this when the agent has already answered the assessment prompt:
    1. Search for evidence
    2. get_assessment_prompt(claim, evidence) → prompt
    3. AI answers with 6 boolean JSON
    4. assess_claim_with_response(claim, evidence, ai_response) → result

    Args:
        claim: The claim to evaluate
        evidence: Evidence text
        llm_response: The AI agent's JSON with 6 boolean judgments
        previous_confidence: Previous confidence for incremental update
        config: ProjectionConfig (optional)

    Returns:
        Full assessment dict
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
            for fid in LLM_FEATURES:
                pattern = re.compile(rf'"{fid}"\s*:\s*(true|false)', re.IGNORECASE)
                match = pattern.search(llm_response)
                if match:
                    features[fid] = match.group(1).lower() == "true"

    return _compute_from_features(claim, evidence, features, previous_confidence, config)


def _compute_from_features(
    claim: str,
    evidence: str,
    features: Dict[str, bool],
    previous_confidence: Optional[float] = None,
    config: Optional[ProjectionConfig] = None,
) -> dict:
    """Compute full assessment from pre-extracted features (no LLM call)."""
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

    # v2: Projection layer
    cfg = config or ProjectionConfig()
    extractor._project(result, claim, previous_confidence, cfg)

    return {
        "state": result.state,
        "confidence": round(result.final_confidence, 4),
        "confidence_range": [
            round(result.confidence_lower, 4),
            round(result.confidence_upper, 4),
        ],
        "quality_factor": round(result.quality_factor, 3),
        "support_score": round(result.support_score, 3),
        "refute_score": round(result.refute_score, 3),
        "features": result.features,
        "direct_refute": result.direct_refute,
        "limitation": result.limitation,
        "veto_reasons": result.veto_reasons,
        "cap_applied": round(result.cap_applied, 3),
        "summary": _generate_summary(result),
    }


def get_skill_definition() -> dict:
    """Return skill definition for agent framework registration."""
    return {
        "name": "belief_assessor",
        "description": "Evaluate the trustworthiness of a claim based on evidence. v2 adds 4-way constraint system, parameterized configuration, and formula-based confidence intervals.",
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
            "confidence": "0.0-1.0 calibrated confidence",
            "confidence_range": "[lower, upper] formula-based interval",
            "veto_reasons": "[str] which constraints triggered",
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
        elif result.veto_reasons:
            reasons = ", ".join(result.veto_reasons)
            parts.append(f"Evidence disputed ({reasons})")
        else:
            parts.append("Evidence is disputed")
    else:
        if result.veto_reasons:
            reasons = ", ".join(result.veto_reasons)
            parts.append(f"Insufficient evidence ({reasons})")
        else:
            parts.append("Insufficient evidence to judge")

    true_feats = [k for k, v in result.features.items() if v]
    if "new_info" in true_feats:
        parts.append("provides new information")
    if "error_outdated" in true_feats:
        parts.append("information may be outdated")

    return ", ".join(parts) if parts else "Unable to assess"
