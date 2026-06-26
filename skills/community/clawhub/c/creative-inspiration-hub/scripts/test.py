#!/usr/bin/env python3
"""Creative Inspiration Hub - Full Test Script"""
import sys
import json
sys.path.insert(0, '.')

from handler import handle_request


def assert_contract(name, result):
    assert result.get("success") is True, f"{name}: success flag missing"
    assert result.get("sessionId", "").startswith("session_"), f"{name}: sessionId missing"
    metadata = result.get("metadata", {})
    assert metadata.get("model") == "cih-v1.2", f"{name}: model version mismatch"
    assert metadata.get("engine") == "local-rule-based", f"{name}: engine metadata missing"

    if name == "idea-generation":
        ideas = result.get("ideas", [])
        assert len(ideas) >= 3, "idea-generation: expected at least 3 ideas"
        for idea in ideas:
            assert "evaluation" in idea and "overall" in idea["evaluation"], "idea missing evaluation"
            assert "implementation" in idea and "first_step" in idea["implementation"], "idea missing implementation first step"
    elif name == "cross-domain":
        combos = result.get("combinations", [])
        assert combos and combos[0]["inspirations"]["conceptPairs"], "cross-domain missing concept pairs"
    elif name == "inspiration-trigger":
        assert len(result.get("triggers", [])) >= 5, "expected 5 trigger words"
    elif name == "evaluation":
        scores = result.get("evaluation", {}).get("scores", {})
        assert {"novelty", "feasibility", "value", "originality", "overall"} <= set(scores), "evaluation score dimensions missing"
    elif name == "mindmap":
        mindmap = result.get("mindmap", {})
        assert mindmap.get("structure", {}).get("nodeCount", 0) >= 3, "mindmap node count too small"


def test_all_branches():
    print("=== Creative Inspiration Hub Full Test ===\n")
    
    tests = [
        ("idea-generation", {"type": "idea-generation", "theme": "智能家居", "domains": ["technology", "design"]}),
        ("cross-domain", {"type": "cross-domain", "domainA": "technology", "domainB": "biology"}),
        ("inspiration-trigger", {"type": "inspiration-trigger", "keywords": ["创新", "突破"]}),
        ("evaluation", {"type": "evaluation", "ideaToEvaluate": "基于AI的推荐系统"}),
        ("mindmap", {"type": "mindmap", "coreConcept": "创新", "relatedThoughts": ["想法1", "想法2"]})
    ]
    
    results = []
    for name, req in tests:
        try:
            result = handle_request(req)
            assert_contract(name, result)
            status = "PASS"
            print(f"{name}: {status}")
            results.append((name, status))
        except Exception as e:
            print(f"{name}: ERROR - {e}")
            results.append((name, "ERROR"))
    
    print(f"\n=== Summary: {sum(1 for _, s in results if s == 'PASS')}/{len(results)} passed ===")
    return all(s == "PASS" for _, s in results)

if __name__ == "__main__":
    success = test_all_branches()
    sys.exit(0 if success else 1)
