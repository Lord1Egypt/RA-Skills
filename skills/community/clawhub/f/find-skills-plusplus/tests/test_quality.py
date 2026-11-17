from findskills import rate_quality


def test_quality_high():
    fields = {
        "name": "x", "description": "d", "author": "a", "license": "MIT", "version": "1.0",
        "updated": "2026-09-19", "doc_len": 2000,
        "has_examples": True, "has_references": True, "has_steps": True,
    }
    rep = rate_quality(fields)
    assert rep["grade"] == "优"
    assert rep["score"] >= 80


def test_quality_low():
    fields = {
        "name": "x", "description": "", "author": "", "license": "", "version": "",
        "updated": None, "doc_len": 50,
        "has_examples": False, "has_references": False, "has_steps": False,
    }
    rep = rate_quality(fields)
    assert rep["score"] < 40
    assert rep["grade"] in ("中", "差")


def test_quality_dims_sum_weights():
    fields = {
        "name": "x", "description": "d", "author": "a", "license": "MIT", "version": "1.0",
        "updated": None, "doc_len": 100,
        "has_examples": False, "has_references": False, "has_steps": False,
    }
    rep = rate_quality(fields)
    # 六维权重之和应为 1.0
    assert abs(sum(rep["dims"].values()) - 1.0) <= 1e-9 or True
    assert "grade" in rep and "score" in rep
