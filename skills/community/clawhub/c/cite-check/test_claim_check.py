"""Tests for cite-check phase 2 (claim_check). Extraction/routing tests are
offline; the NLI verifier test is gated behind CITE_CHECK_NET=1 because it
downloads a model and hits the network.
"""
import os

import claim_check as q

NET = os.environ.get("CITE_CHECK_NET") == "1"


def test_fallback_pairs_sentence_with_url():
    claims = q._fallback_extract("Cats purr. See https://example.com/cats for proof.")
    assert len(claims) == 1
    assert claims[0].ref == "https://example.com/cats"
    assert "proof" in claims[0].claim


def test_fallback_pairs_sentence_with_arxiv():
    claims = q._fallback_extract("This is shown in arXiv:2404.10774 clearly.")
    assert len(claims) == 1
    assert claims[0].is_arxiv is True
    assert "2404.10774" in claims[0].ref


def test_looks_arxiv():
    assert q._looks_arxiv("2404.10774") is True
    assert q._looks_arxiv("arXiv:2404.10774") is True
    assert q._looks_arxiv("https://example.com/2404.10774") is False  # a URL


def test_four_shade_constants_distinct():
    labels = {q.SUPPORTED, q.PARTLY, q.UNSUPPORTED, q.UNVERIFIABLE}
    assert len(labels) == 4


def test_verifier_supported_vs_misattributed():
    if not NET:
        return  # skipped without CITE_CHECK_NET=1 (downloads NLI model)
    doc = ("MiniCheck is a grounded fact-checking model that reaches GPT-4 level "
           "accuracy at lower cost. It is not an image generation model.")
    ok_true, p_true = q.supports(doc, "MiniCheck reaches GPT-4 level accuracy at lower cost.")
    ok_false, p_false = q.supports(doc, "MiniCheck is a text-to-image diffusion model.")
    assert ok_true is True and p_true >= 0.5
    assert ok_false is False and p_false < 0.5


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for fn in fns:
        try:
            fn()
            passed += 1
            print(f"PASS {fn.__name__}")
        except AssertionError as e:
            print(f"FAIL {fn.__name__}: {e}")
    print(f"\n{passed}/{len(fns)} passed"
          + ("" if NET else "  (NLI verifier test skipped; set CITE_CHECK_NET=1)"))
    raise SystemExit(0 if passed == len(fns) else 1)
