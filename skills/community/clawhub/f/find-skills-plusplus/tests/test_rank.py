from findskills import (
    compute_composite,
    derive_reputation,
    merge_candidates,
    normalize_key,
)


def test_normalize_key_strips_variants():
    assert normalize_key("React-Performance") == normalize_key("react performance")
    assert normalize_key("pdf-skill") == normalize_key("pdf")
    assert normalize_key("My_Skill") == "myskill"


def test_derive_reputation():
    assert derive_reputation({"official_source": True}) == 1.0
    assert derive_reputation({"source": "workbuddy-builtin"}) == 0.9
    assert derive_reputation({"homepage": "https://x"}) == 0.9
    assert derive_reputation({}) == 0.6
    assert derive_reputation({"reputation": 0.42}) == 0.42


def test_composite_official():
    c = {"score": 1.0, "downloads": 0, "updated": None, "official_source": True}
    # base = 0.5*1 + 0.3*0.3 + 0.2*0.5 = 0.5+0.09+0.1 = 0.69; *1.0
    assert abs(compute_composite(c) - 0.69) < 1e-6


def test_merge_dedup_merges_sources():
    lists = [
        ("registry", [{"name": "PDF", "slug": "pdf", "updated": 100, "official_source": False}]),
        ("skillhub", [{"name": "pdf", "slug": "pdf", "updated": 200, "official_source": False}]),
    ]
    merged = merge_candidates(lists)
    assert len(merged) == 1
    key = next(iter(merged))
    assert set(merged[key]["sources"]) == {"registry", "skillhub"}
    assert merged[key]["updated"] == 200  # 取更近


def test_merge_no_false_dedup():
    lists = [
        ("a", [{"name": "pdf", "slug": "pdf"}]),
        ("b", [{"name": "pptx", "slug": "pptx"}]),
    ]
    assert len(merge_candidates(lists)) == 2
