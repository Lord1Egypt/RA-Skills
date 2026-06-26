#!/usr/bin/env python3
"""
Basic tests for agent-memory-tools.
Run: python3 scripts/tests.py
No pytest needed — uses unittest.
"""
from __future__ import annotations
import os, sys
# Cross-platform PATH setup
if sys.platform == "darwin":
    os.environ["PATH"] = "/opt/homebrew/bin:" + os.environ.get("HOME", "") + "/.bun/bin:" + os.environ.get("PATH", "")

import json, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from llm_client import load_config, _extract_json, cosine_sim


class TestConfig(unittest.TestCase):
    def test_load_config(self):
        cfg = load_config()
        self.assertIn("llm", cfg)
        self.assertIn("embeddings", cfg)
        self.assertIn("paths", cfg)
        self.assertIn("model", cfg["llm"])
        self.assertIn("baseUrl", cfg["llm"])
    
    def test_load_preset(self):
        cfg = load_config(preset="ollama")
        self.assertIn("11434", cfg["llm"]["baseUrl"])
    
    def test_load_script_override(self):
        cfg = load_config(script="multihop")
        # Should have a model set
        self.assertTrue(len(cfg["llm"]["model"]) > 0)
    
    def test_invalid_preset(self):
        cfg = load_config(preset="nonexistent")
        # Should still load without error
        self.assertIn("llm", cfg)


class TestJsonExtraction(unittest.TestCase):
    def test_plain_json(self):
        r = _extract_json('{"action": "answer", "confidence": 0.8}')
        self.assertEqual(r["action"], "answer")
    
    def test_json_in_code_block(self):
        r = _extract_json('```json\n{"key": "value"}\n```')
        self.assertEqual(r["key"], "value")
    
    def test_json_with_surrounding_text(self):
        r = _extract_json('Here is the result: {"status": "ok"} done.')
        self.assertEqual(r["status"], "ok")
    
    def test_gptoss_tags(self):
        text = '<|channel|>commentary to=repo_browser\n{"action": "refine"}'
        r = _extract_json(text)
        self.assertEqual(r["action"], "refine")
    
    def test_empty_string(self):
        r = _extract_json("")
        self.assertIsNone(r)
    
    def test_no_json(self):
        r = _extract_json("This is just plain text without any JSON.")
        self.assertIsNone(r)
    
    def test_array(self):
        r = _extract_json('[{"a": 1}, {"b": 2}]')
        self.assertEqual(len(r), 2)
    
    def test_thinking_tags_in_json(self):
        text = '<think>reasoning here</think>\n{"result": "done"}'
        r = _extract_json(text)
        self.assertEqual(r["result"], "done")


class TestCosineSim(unittest.TestCase):
    def test_identical(self):
        v = [1.0, 0.0, 1.0]
        self.assertAlmostEqual(cosine_sim(v, v), 1.0, places=5)
    
    def test_orthogonal(self):
        self.assertAlmostEqual(cosine_sim([1, 0], [0, 1]), 0.0, places=5)
    
    def test_opposite(self):
        self.assertAlmostEqual(cosine_sim([1, 0], [-1, 0]), -1.0, places=5)
    
    def test_empty(self):
        self.assertEqual(cosine_sim([], []), 0.0)


class TestExtractFacts(unittest.TestCase):
    def test_import(self):
        from extract_facts import EXTRACTION_PROMPT
        self.assertIn("durable", EXTRACTION_PROMPT)
    
    def test_categories(self):
        from extract_facts import EXTRACTION_PROMPT
        for cat in ["knowledge", "error", "timeline", "preference", "tool", "client", "hr"]:
            self.assertIn(cat, EXTRACTION_PROMPT)


class TestMultihopHelpers(unittest.TestCase):
    def test_enrich_empty_graph(self):
        from multihop_search import enrich_with_graph
        results = [{"filepath": "test.md", "text": "test"}]
        enriched = enrich_with_graph("test", results, {})
        self.assertEqual(len(enriched), 1)
    
    def test_enrich_dict_graph(self):
        from multihop_search import enrich_with_graph
        graph = {"entities": {"Sol": {"mentions": ["agents/sol.md", "MEMORY.md"], "relations": []}}}
        results = []
        enriched = enrich_with_graph("Sol", results, graph)
        self.assertGreater(len(enriched), 0)


class TestUnifiedRecall(unittest.TestCase):
    def test_import(self):
        from unified_recall import recall, merge_results, score_result, compute_recency
        self.assertTrue(callable(recall))
    
    def test_merge_dedup(self):
        from unified_recall import merge_results
        s1 = [{"filepath": "a.md", "text": "test", "source": "qmd", "score_raw": 0.5}]
        s2 = [{"filepath": "a.md", "text": "test", "source": "embed", "score_raw": 0.8, "semantic_sim": 0.8}]
        merged = merge_results([s1, s2])
        # Should merge into 1 result with 2 sources
        self.assertEqual(len(merged), 1)
        self.assertIn("qmd", merged[0]["sources"])
        self.assertIn("embed", merged[0]["sources"])
        self.assertEqual(merged[0]["score_raw"], 0.8)  # Best score kept
    
    def test_merge_convex_unique(self):
        from unified_recall import merge_results
        s1 = [{"filepath": "agentMemory:savoir", "text": "fact A", "source": "convex"}]
        s2 = [{"filepath": "agentMemory:savoir", "text": "fact B", "source": "convex"}]
        merged = merge_results([s1, s2])
        # Different facts = not merged
        self.assertEqual(len(merged), 2)
    
    def test_recency_recent(self):
        from unified_recall import compute_recency
        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")
        score = compute_recency(f"memory/{today}.md")
        self.assertGreater(score, 0.9)
    
    def test_recency_old(self):
        from unified_recall import compute_recency
        score = compute_recency("memory/2024-01-01.md")
        self.assertLess(score, 0.2)
    
    def test_recency_protected(self):
        from unified_recall import compute_recency
        score = compute_recency("bugs/old-bug.md")
        self.assertEqual(score, 0.7)  # Protected, no decay
    
    def test_score_result(self):
        from unified_recall import score_result
        cfg = load_config()
        r = {
            "filepath": "memory/2026-03-23.md",
            "sources": ["embed", "qmd"],
            "semantic_sim": 0.85,
            "score_raw": 0.7,
            "accessCount": 5,
            "centrality": 3,
        }
        score = score_result(r, cfg)
        self.assertGreater(score, 0.3)
        self.assertLess(score, 1.0)
    
    def test_multi_source_bonus(self):
        from unified_recall import score_result
        cfg = load_config()
        single = {"filepath": "test.md", "sources": ["qmd"], "score_raw": 0.5}
        multi = {"filepath": "test.md", "sources": ["qmd", "embed"], "score_raw": 0.5}
        s1 = score_result(single, cfg)
        s2 = score_result(multi, cfg)
        self.assertGreater(s2, s1)  # Multi-source should score higher


if __name__ == "__main__":
    unittest.main(verbosity=2)
