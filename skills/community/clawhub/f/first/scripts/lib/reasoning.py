#!/usr/bin/env python3
import re

STOPWORDS = {
    "the","a","an","and","or","but","if","to","of","in","on","for","with","at","by",
    "is","are","was","were","be","been","being","this","that","these","those",
    "i","you","we","they","he","she","it","my","your","our","their",
    "should","would","could","really","just","because","says","say","everyone","all",
    "what","why","how","when","where","who","need","needs","want","wants","future",
    "build","make","using","use","used","into","from","about","than","then","there",
    "have","has","had","do","does","did","can","may","might","must"
}

QUESTION_HINTS = [
    ("should i", "Decide whether this is worth doing."),
    ("should we", "Decide whether this is worth doing as a team or business."),
    ("how do i", "Find the most fundamental path to achieve the desired result."),
    ("how can i", "Find the most fundamental path to achieve the desired result."),
    ("why", "Understand the true drivers and causes behind the problem."),
    ("what", "Clarify the structure, components, and decision criteria of the problem.")
]

HEURISTICS = [
    "Distinguish objective from method.",
    "Separate user value from implementation choice.",
    "Test necessity before optimization.",
    "Identify the true bottleneck before redesigning the system.",
    "Reduce the problem to constraints, incentives, resources, and tradeoffs."
]

ANTI_PATTERNS = [
    ("everyone", "Assuming common behavior is evidence of correctness."),
    ("best", "Treating one best practice as universally correct."),
    ("agent", "Confusing tools with user value."),
    ("ai", "Confusing technology choice with actual user outcome."),
    ("trend", "Repeating category hype instead of testing objective reality."),
    ("future", "Confusing category momentum with current necessity.")
]

DOMAIN_MAP = {
    "product": ["user value", "retention", "adoption", "problem-solution fit"],
    "business": ["demand", "distribution", "pricing", "unit economics"],
    "startup": ["demand", "speed", "distribution", "cash runway"],
    "content": ["audience", "hook", "retention", "repeatability"],
    "marketing": ["distribution", "message-market fit", "CAC", "conversion"],
    "sales": ["pain", "trust", "objection handling", "conversion"],
    "agent": ["user value", "task fit", "reliability", "automation payoff"],
    "ai": ["user value", "task fit", "cost", "reliability"]
}

def clean_title(problem, limit=64):
    text = re.sub(r'\s+', ' ', problem.strip())
    text = re.sub(r'[?!.]+$', '', text)
    if len(text) <= limit:
        return text
    return text[:limit-3].rstrip() + "..."

def extract_keywords(text, limit=8):
    words = re.findall(r"[A-Za-z][A-Za-z0-9\-_']+", text.lower())
    seen = []
    for w in words:
        if w in STOPWORDS or len(w) <= 2:
            continue
        if w not in seen:
            seen.append(w)
    mapped = []
    for w in seen:
        mapped.append(w)
        if w in DOMAIN_MAP:
            for extra in DOMAIN_MAP[w]:
                if extra not in mapped:
                    mapped.append(extra)
    deduped = []
    for item in mapped:
        if item not in deduped:
            deduped.append(item)
    return deduped[:limit]

def infer_goal(problem):
    lower = problem.lower().strip()
    for prefix, goal in QUESTION_HINTS:
        if lower.startswith(prefix):
            return goal
    return "Clarify the real objective and rebuild a better solution from fundamentals."

def infer_assumptions(problem):
    assumptions = []
    lower = problem.lower()

    if "must" in lower:
        assumptions.append("Something in the current framing is being treated as mandatory when it may only be conventional.")
    if "everyone" in lower or "all " in lower:
        assumptions.append("Common behavior is being treated as evidence of correctness.")
    if "ai" in lower or "agent" in lower or "automation" in lower:
        assumptions.append("A technology choice may be getting confused with the actual user value.")
    if "need" in lower:
        assumptions.append("A perceived requirement may actually be a preference, habit, or inherited default.")
    if "best" in lower:
        assumptions.append("There may be an assumption that one universal best practice exists across contexts.")
    if "future" in lower or "trend" in lower:
        assumptions.append("Momentum or hype may be getting confused with actual necessity.")

    if not assumptions:
        assumptions = [
            "The current framing may contain inherited assumptions from analogy or convention.",
            "The default solution may be overvalued relative to the true objective.",
            "The visible problem may be a symptom rather than the root issue."
        ]
    return assumptions[:6]

def infer_truths(problem):
    keywords = extract_keywords(problem)
    truths = [
        "A good solution must satisfy the real objective, not merely match convention.",
        "Constraints, incentives, and tradeoffs matter more than slogans or surface-level best practices.",
        "A method or tool is only valuable if it changes outcomes.",
        "The strongest solution usually comes from clarifying the bottleneck before expanding the design."
    ]
    if keywords:
        truths.append("The problem likely depends on a few high-leverage variables: " + ", ".join(keywords[:6]) + ".")
    return truths[:6]

def infer_components(problem):
    keywords = extract_keywords(problem)
    base = ["objective", "constraints", "resources", "incentives", "tradeoffs", "bottleneck"]
    for k in keywords:
        if k not in base:
            base.append(k)
    return base[:10]

def infer_constraints(problem):
    constraints = [
        "Limited time, attention, or execution capacity may restrict the solution space.",
        "Real user behavior may differ from what people say they want.",
        "Existing incentives may reward the current approach even if it is suboptimal."
    ]
    lower = problem.lower()
    if "budget" in lower or "cost" in lower or "price" in lower:
        constraints.append("Economic constraints are likely central to the decision.")
    if "team" in lower or "hire" in lower:
        constraints.append("Team capability and coordination may be a real limiting factor.")
    return constraints[:6]

def detect_anti_patterns(problem):
    lower = problem.lower()
    hits = []
    for token, warning in ANTI_PATTERNS:
        if token in lower and warning not in hits:
            hits.append(warning)
    if not hits:
        hits.append("No obvious anti-pattern dominates yet; verify the framing before expanding the solution.")
    return hits[:5]

def select_heuristics(problem):
    lower = problem.lower()
    chosen = ["Distinguish objective from method.", "Test necessity before optimization."]
    if "ai" in lower or "agent" in lower or "automation" in lower:
        chosen.append("Separate user value from implementation choice.")
    chosen.append("Identify the true bottleneck before redesigning the system.")
    return list(dict.fromkeys(chosen))[:5]

def infer_rebuilt_solution(problem):
    keywords = extract_keywords(problem)
    s = [
        "Restate the problem in terms of the actual objective rather than the default approach.",
        "Test whether each major assumption is necessary, optional, or false.",
        "Design around the smallest set of truths and constraints that must hold.",
        "Identify the bottleneck that most determines success before expanding scope."
    ]
    if keywords:
        s.append("Prioritize decisions around the highest-leverage variables: " + ", ".join(keywords[:4]) + ".")
    return s[:6]

def infer_next_actions(problem):
    return [
        "Write down the real goal in one sentence.",
        "List the top 3 assumptions currently shaping the decision.",
        "Identify which assumption, if false, would most change the answer.",
        "Define the real bottleneck in concrete terms.",
        "Choose one small test that validates the rebuilt solution."
    ]

def infer_pattern_candidate(case):
    assumptions = case.get("assumptions", [])
    anti_patterns = case.get("anti_patterns", [])
    problem = case.get("problem", "").lower()

    if any("technology choice" in a.lower() for a in assumptions):
        return "Do not confuse technology choice with user value."
    if any("common behavior" in a.lower() for a in assumptions):
        return "Treat consensus as a clue, not as proof."
    if "agent" in problem or "ai" in problem:
        return "Evaluate tools by outcome improvement, not by category hype."
    if anti_patterns:
        return "Clarify the bottleneck before expanding the solution space."
    return "Restate the objective before optimizing the method."

def promotion_status(case):
    overall = float(case.get("score", {}).get("overall", 0))
    candidate = (case.get("reusable_pattern_candidate") or "").strip()
    if overall >= 9.0 and candidate:
        return "promoted"
    if overall >= 8.0 and candidate:
        return "candidate"
    return "none"

def compute_score(case):
    assumptions = len(case.get("assumptions", []))
    truths = len(case.get("truths", []))
    rebuilt = len(case.get("rebuilt_solution", []))
    actions = len(case.get("next_actions", []))
    anti_patterns = len(case.get("anti_patterns", []))
    heuristics = len(case.get("heuristics_used", []))

    assumption_coverage = min(10, 5 + assumptions)
    truth_quality = min(10, 4 + truths + min(1, anti_patterns))
    solution_clarity = min(10, 4 + rebuilt + min(1, heuristics))
    actionability = min(10, 4 + actions)
    overall = round((assumption_coverage + truth_quality + solution_clarity + actionability) / 4, 1)

    return {
        "assumption_coverage": assumption_coverage,
        "truth_quality": truth_quality,
        "solution_clarity": solution_clarity,
        "actionability": actionability,
        "overall": overall
    }
