from __future__ import annotations

import re
from collections import Counter

TOKEN_RE = re.compile(r"[A-Za-zÅÄÖåäö0-9-]{3,}")
STOP_WORDS = {
    "the", "and", "for", "with", "that", "this", "from", "into", "over", "under",
    "have", "has", "had", "was", "were", "are", "but", "not", "you", "your",
    "että", "tämä", "nämä", "sitä", "niitä", "kun", "joka", "jotka", "sekä", "vain",
    "vielä", "myös", "mutta", "kuin", "ovat", "oli", "olla", "voidaan", "joten",
}


def simple_stem(token: str) -> str:
    token = token.lower()
    for suffix in (
        "ing", "ed", "es", "s", "ssa", "ssä", "sta", "stä", "lla", "llä", "lta", "ltä",
        "ksi", "tta", "ttä", "iin", "den", "jen", "nen", "n",
    ):
        if len(token) > len(suffix) + 2 and token.endswith(suffix):
            return token[: -len(suffix)]
    return token


def tokenize(text: str) -> list[str]:
    return [match.group(0).lower() for match in TOKEN_RE.finditer(text)]


def normalize_claim(text: str) -> tuple[str, list[str]]:
    # The first return value is a canonical, deduped string used for grouping/dedupe.
    # The second return value is the full ordered token multiset, which BM25 and
    # token-overlap scoring need so that repeated terms count more than once.
    clean_text = re.sub(r"\s+\[.*\]\s*$", "", text)
    tokens: list[str] = []
    for token in tokenize(clean_text):
        stemmed = simple_stem(token)
        if stemmed in STOP_WORDS:
            continue
        tokens.append(stemmed)
    canonical = " ".join(sorted(set(tokens)))
    return canonical, tokens


def jaccard_similarity(a: list[str], b: list[str]) -> float:
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 1.0
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def claims_match(text_a: str, text_b: str, threshold: float = 0.72) -> bool:
    _na, tokens_a = normalize_claim(text_a)
    _nb, tokens_b = normalize_claim(text_b)
    return jaccard_similarity(tokens_a, tokens_b) >= threshold


def token_counter(text: str) -> Counter[str]:
    _norm, tokens = normalize_claim(text)
    return Counter(tokens)
