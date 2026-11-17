#!/usr/bin/env python3
"""Boundary tests for the offline package contract; no live parser or LLM evaluation."""
import argparse
import copy
import contextlib
import io
import importlib.util
import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

SPEC = importlib.util.spec_from_file_location("ontology", Path(__file__).with_name("ontology.py"))
o = importlib.util.module_from_spec(SPEC)
sys.modules['ontology'] = o
SPEC.loader.exec_module(o)
import experience as e
DEMO = Path(__file__).resolve().parent.parent / "assets" / "demo"


class Boundaries(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.inputs = self.root / "inputs"
        shutil.copytree(DEMO, self.inputs)
        self.a, _ = o.prepare_input(self.inputs / "r1.json")
        self.b, _ = o.prepare_input(self.inputs / "r2.json")

    def tearDown(self): self.temp.cleanup()

    def build(self):
        dest = self.root / "v1"
        o.write_package(self.a, o.roots_for(self.a, self.inputs), dest, {})
        return dest

    def merged(self):
        dest = self.build()
        base, run = o.load_package(dest)
        k, changes = o.merge(base, self.b)
        out = self.root / "v2"
        roots = dict(o.roots_for(base, dest), **o.roots_for(self.b, self.inputs))
        o.write_package(k, roots, out, changes, run["knowledge_sha256"], "update")
        return out

    def test_replay_no_duplicate_or_lost_history(self):
        out = self.merged(); k, _ = o.load_package(out)
        again, changes = o.merge(k, self.b)
        self.assertEqual(len(again["assertions"]), 5)
        self.assertEqual(changes["duplicate_assertions"], 3)
        self.assertEqual(len([a for a in again["assertions"] if a["concept_id"] == "relation:offers"]), 1)

    def test_restated_same_period_preserves_conflict(self):
        k, _ = o.load_package(self.merged())
        r = o.query(k, SimpleNamespace(entity=None, concept="metric:revenue", period="2025Q4", basis="IFRS", qualifiers=None))
        self.assertEqual(r["status"], "conflict")
        self.assertEqual({a["value"] for a in r["assertions"]}, {100, 105})

    def test_unspecified_basis_requires_scope(self):
        k, _ = o.load_package(self.merged())
        r = o.query(k, SimpleNamespace(entity=None, concept="metric:revenue", period="2026Q1", basis=None, qualifiers=None))
        self.assertEqual(r["status"], "needs_scope")

    def test_explicit_basis_selects_with_evidence(self):
        k, _ = o.load_package(self.merged())
        r = o.query(k, SimpleNamespace(entity=None, concept="metric:revenue", period="2026Q1", basis="IFRS", qualifiers="{}"))
        self.assertEqual(r["status"], "found")
        self.assertEqual(r["assertions"][0]["value"], 120)
        self.assertTrue(r["sources"])

    def test_changed_definition_reusing_id_rejected(self):
        self.b["definitions"][0]["description"] = "A silently different meaning"
        with self.assertRaises(o.Invalid): o.merge(self.a, self.b)

    def test_changed_source_reusing_id_rejected(self):
        other = copy.deepcopy(self.a); other["sources"][0]["sha256"] = "0" * 64
        with self.assertRaises(o.Invalid): o.merge(self.a, other)

    def test_retrieval_date_cannot_move_scope_backwards(self):
        self.b["scope"]["as_of"] = "2025-01-01"
        with self.assertRaises(o.Invalid): o.merge(self.a, self.b)

    def test_source_bytes_tampering_rejected(self):
        out = self.build(); k, _ = o.load_package(out)
        (out / k["sources"][0]["content_file"]).write_text("changed")
        with self.assertRaises(o.Invalid): o.load_package(out)

    def test_knowledge_tampering_rejected(self):
        out = self.build(); k = o.read_json(out / "knowledge.json")
        k["assertions"][0]["value"] = 999
        (out / "knowledge.json").write_text(json.dumps(k))
        with self.assertRaises(o.Invalid): o.load_package(out)

    def test_changes_tampering_rejected(self):
        out = self.build(); (out / "changes.json").write_text('{}')
        with self.assertRaises(o.Invalid): o.load_package(out)

    def test_bad_page_is_not_native_evidence(self):
        self.a["assertions"][0]["evidence"][0]["page"] = 2
        with self.assertRaises(o.Invalid): o.check_knowledge(self.a, self.inputs)

    def test_fake_native_provenance_rejected(self):
        self.a["sources"][0]["page_spans"][0]["basis"] = o.OMNI
        with self.assertRaises(o.Invalid): o.check_knowledge(self.a, self.inputs)

    def test_range_hash_mismatch_rejected(self):
        self.a["assertions"][0]["evidence"][0]["span_sha256"] = "0" * 64
        with self.assertRaises(o.Invalid): o.check_knowledge(self.a, self.inputs)

    def test_unicode_mid_character_range_rejected(self):
        s = self.a["sources"][0]; raw = '企业'.encode(); (self.inputs / s["content_file"]).write_bytes(raw)
        s["sha256"] = o.digest(raw); s["page_spans"][0]["end_utf8"] = len(raw)
        ev = self.a["assertions"][0]["evidence"][0]
        ev.update(start_utf8=1, end_utf8=3, span_sha256=o.digest(raw[1:3]))
        with self.assertRaises(UnicodeError): o.check_knowledge(self.a, self.inputs)

    def test_unknown_entity_relation_rejected(self):
        self.a["assertions"][1]["value"] = "org:unknown"
        with self.assertRaises(o.Invalid): o.check_knowledge(self.a, self.inputs)

    def test_unit_required(self):
        self.a["assertions"][0]["unit"] = ""
        with self.assertRaises(o.Invalid): o.check_knowledge(self.a, self.inputs)

    def test_injected_acceptance_rejected(self):
        j = o.read_json(self.inputs / "r1.json"); j["assertions"][0]["status"] = "accepted"
        p = self.inputs / "injected.json"; p.write_text(json.dumps(j))
        with self.assertRaises(o.Invalid): o.prepare_input(p)

    def test_claim_kind_defaults_to_reported(self):
        j = o.read_json(self.inputs / "r1.json")
        for a in j["assertions"]: a.pop("claim_kind", None)
        p = self.inputs / "noclaim.json"; p.write_text(json.dumps(j))
        k, _ = o.prepare_input(p)
        self.assertTrue(all(a["claim_kind"] == "reported" for a in k["assertions"]))

    def test_derived_value_cannot_masquerade_as_reported(self):
        self.a["assertions"][0]["claim_kind"] = "derived"
        with self.assertRaises(o.Invalid): o.check_knowledge(self.a, self.inputs)

    def test_traversal_rejected(self):
        with self.assertRaises(o.Invalid): o.local_file(self.inputs, "../outside.txt")

    def test_symlink_escape_rejected(self):
        external = self.root / "outside.txt"; external.write_text("private")
        (self.inputs / "link.txt").symlink_to(external)
        if not (self.inputs / "link.txt").is_symlink():
            # On Windows without symlink privilege, symlink_to silently copies the
            # target instead of creating a link, so no escape exists to reject.
            self.skipTest("platform cannot create file symlinks (silently copied)")
        with self.assertRaises(o.Invalid): o.local_file(self.inputs, "link.txt")

    def test_private_and_credential_urls_rejected(self):
        for url in ("http://127.0.0.1/a", "http://localhost/a", "http://service.internal/a", "https://u:p@example.org/a", "https://example.org/a?token=abc"):
            with self.subTest(url=url), self.assertRaises(o.Invalid): o.public_url(url)

    def test_existing_output_never_overwritten(self):
        out = self.build()
        with self.assertRaises(o.Invalid): o.write_package(self.a, o.roots_for(self.a, self.inputs), out, {})

    def test_missing_query_is_not_zero(self):
        r = o.query(self.a, SimpleNamespace(entity=None, concept="metric:none", period=None, basis=None, qualifiers=None))
        self.assertEqual(r["status"], "not_found"); self.assertEqual(r["assertions"], [])

    def test_duplicate_json_keys_rejected(self):
        p = self.root / "duplicate.json"; p.write_text('{"value":1,"value":2}')
        with self.assertRaises(o.Invalid): o.read_json(p)

    def test_okf_never_claims_human_verification(self):
        out = self.root / "okf"; o.export_okf(self.a, out)
        files = list(out.glob('concept-*.md')); self.assertEqual(len(files), 2)
        for f in files:
            s = f.read_text(); self.assertIn('status: draft', s); self.assertNotIn('\nverified:', s)

    def test_review_persists_across_duplicate_update(self):
        base = self.build(); k, _ = o.load_package(base)
        reviewed = self.root / 'reviewed'
        with contextlib.redirect_stdout(io.StringIO()):
            code = o.main(['review', str(base), '--assertion', k['assertions'][0]['id'], '--decision', 'rejected',
                           '--reviewer', 'synthetic-test-actor', '--note', 'Synthetic regression decision', '--out', str(reviewed)])
        self.assertEqual(code, 0)
        r, _ = o.load_package(reviewed); merged, changes = o.merge(r, self.a)
        self.assertEqual(merged['assertions'][0]['status'], 'rejected')
        self.assertEqual(changes['duplicate_assertions'], 2)
        self.assertEqual(len(merged['assertions'][0]['reviews']), 1)
        original, _ = o.load_package(base)
        self.assertEqual(original['assertions'][0]['status'], 'candidate')

    def test_feedback_excludes_source_and_claim_content(self):
        base = self.build(); out = self.root / 'feedback.json'
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(o.main(['feedback', str(base), '--out', str(out)]), 0)
        s = out.read_text()
        for value in ['example.org', 'Northstar', '100', 'demo-r1']:
            self.assertNotIn(value, s)

    def test_url_markup_characters_rejected(self):
        for value in ['https://example.org/a>bad', 'https://example.org/a\nnext', 'https://example.org/a space']:
            with self.subTest(value=value), self.assertRaises(o.Invalid): o.public_url(value)

    def test_numeric_spelling_is_support_not_conflict(self):
        incoming = copy.deepcopy(self.a)
        row = incoming['assertions'][0]
        original_id = row['id']
        row['value'] = float(row['value']); row['id'] = o.assertion_id(row)
        merged, changes = o.merge(self.a, incoming)
        self.assertEqual(o.conflict_ids(merged), [])
        self.assertEqual(changes['additional_support'], [row['id']])
        self.assertEqual(merged['assertions'][0]['id'], original_id)
        result = o.query(merged, SimpleNamespace(concept='metric:revenue', qualifiers=None))
        self.assertEqual(result['status'], 'found')
        self.assertEqual(len(result['assertions']), 2)

    def test_large_integer_differences_are_not_rounded_away(self):
        a = 10 ** 40
        self.assertNotEqual(o.value_key(a), o.value_key(a + 1))

    def test_unit_and_validity_scope_can_be_selected(self):
        a = self.a['assertions'][0]
        b = copy.deepcopy(a); b.update(unit='CNY', valid_from='2026-01-01', valid_to='2026-03-31')
        b['fact_id'] = o.fact_id(b); b['id'] = o.assertion_id(b)
        self.a['assertions'].append(b)
        broad = o.query(self.a, SimpleNamespace(concept='metric:revenue', qualifiers=None))
        self.assertEqual(broad['status'], 'needs_scope')
        self.assertEqual(len(broad['scopes']), 2)
        selected = o.query(self.a, SimpleNamespace(concept='metric:revenue', qualifiers=None,
                          unit='CNY', valid_from='2026-01-01', valid_to='2026-03-31'))
        self.assertEqual(selected['status'], 'found')
        self.assertEqual(selected['assertions'], [b])

    def test_fact_cli_selects_from_old_schema_package(self):
        base = self.build(); k, run = o.load_package(base)
        self.assertEqual(run['schema_version'], '0.1.0')
        self.assertEqual(run['skill_version'], o.VERSION)
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = o.main(['query', str(base), '--fact', k['assertions'][0]['fact_id']])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(stdout.getvalue())['status'], 'found')

    def test_boolean_qualifier_does_not_match_number(self):
        a = self.a['assertions'][0]; a['qualifiers'] = {'flag': True}
        a['fact_id'] = o.fact_id(a); a['id'] = o.assertion_id(a)
        result = o.query(self.a, SimpleNamespace(concept='metric:revenue', qualifiers='{"flag":1}'))
        self.assertEqual(result['status'], 'not_found')

    def test_query_rejects_ambiguous_json_and_invalid_dates(self):
        for value in ('{"flag":1,"flag":2}', '{"flag":NaN}'):
            with self.subTest(value=value), self.assertRaises(o.Invalid):
                o.query(self.a, SimpleNamespace(qualifiers=value))
        with self.assertRaises(o.Invalid):
            o.query(self.a, SimpleNamespace(qualifiers=None, valid_from='2026-99-01'))

    def test_malformed_assertions_return_structured_error(self):
        for bad in (None, {}, ['text'], [None]):
            k = o.read_json(self.inputs / 'r1.json'); k['assertions'] = bad
            p = self.inputs / 'malformed.json'; p.write_text(json.dumps(k))
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                code = o.main(['build', str(p), '--out', str(self.root / 'invalid')])
            self.assertEqual(code, 2)
            self.assertEqual(json.loads(stderr.getvalue())['status'], 'invalid')
            self.assertFalse((self.root / 'invalid').exists())

    def test_report_identifies_conflict_scope_and_escapes_source_text(self):
        k, changes = o.merge(self.a, self.b)
        changes['conflicts'] = o.conflict_ids(k)
        k['entities'][0]['name'] = '[external](https://example.org)'
        rendered = o.render(k, changes)
        self.assertIn('candidate / conflict', rendered)
        self.assertIn(changes['conflicts'][0], rendered)
        self.assertIn('| Validity |', rendered)
        self.assertNotIn('[external](https://example.org)', rendered)

    def test_quote_preparation_preserves_exact_evidence(self):
        target = self.root / 'prepared'
        e.prepare(self.inputs / 'quote-draft.json', target)
        k, _ = o.prepare_input(target / 'input.json')
        self.assertEqual(k['assertions'], self.a['assertions'])
        self.assertEqual(k['sources'][0]['sha256'], self.a['sources'][0]['sha256'])

    def quote_input(self, text, quote, occurrence=None):
        d = o.read_json(self.inputs / 'quote-draft.json')
        d['assertions'] = d['assertions'][:1]
        d['sources'][0]['page_spans'] = []
        (self.inputs/d['sources'][0]['content_file']).write_text(text, encoding='utf-8')
        d['assertions'][0]['evidence'] = [dict(source_id=d['sources'][0]['id'],role='value',quote=quote)]
        if occurrence is not None: d['assertions'][0]['evidence'][0]['occurrence'] = occurrence
        p=self.inputs/'draft.json';p.write_text(json.dumps(d,ensure_ascii=False),encoding='utf-8')
        return p

    def test_ambiguous_quote_fails_without_output(self):
        p=self.quote_input('收入 100。收入 100。','收入 100。')
        with self.assertRaises(o.Invalid): e.prepare(p,self.root/'prepared')
        self.assertFalse((self.root/'prepared').exists())

    def test_quote_occurrence_uses_utf8_byte_positions(self):
        p=self.quote_input('收入 100。收入 100。','收入 100。',2)
        e.prepare(p,self.root/'prepared')
        k,_=o.prepare_input(self.root/'prepared'/'input.json')
        self.assertEqual(k['assertions'][0]['evidence'][0]['start_utf8'],len('收入 100。'.encode()))

    def test_changed_quote_and_wrong_hash_are_rejected(self):
        p=self.quote_input('actual text','invented text')
        with self.assertRaises(o.Invalid): e.prepare(p,self.root/'bad')
        d=o.read_json(p);d['assertions'][0]['evidence'][0]['quote']='actual text';d['sources'][0]['sha256']='0'*64
        p.write_text(json.dumps(d))
        with self.assertRaises(o.Invalid): e.prepare(p,self.root/'bad')

    def test_quote_locator_cannot_override_derived_page(self):
        p=self.inputs/'quote-draft.json';d=o.read_json(p)
        d['assertions'][0]['evidence'][0]['page']=999;p.write_text(json.dumps(d))
        with self.assertRaises(o.Invalid): e.prepare(p,self.root/'bad')

    def test_brief_requires_preserved_baseline(self):
        current,_=o.merge(self.a,self.b)
        delta=e.changes_between(self.a,current)
        self.assertEqual(len(delta['new_conflict_ids']),1)
        self.assertEqual(delta['baseline_assertions_preserved'],2)
        current['assertions'].pop(0)
        with self.assertRaises(o.Invalid): e.changes_between(self.a,current)

    def test_evidence_previews_are_bounded_and_not_rewritten(self):
        previews=e.previews(self.a,self.inputs,limit=10)
        self.assertTrue(previews[0]['truncated'])
        ev=self.a['assertions'][0]['evidence'][0]
        raw=(self.inputs/self.a['sources'][0]['content_file']).read_bytes()
        self.assertEqual(previews[0]['excerpt'],raw[ev['start_utf8']:ev['end_utf8']].decode()[:10])

    def test_brief_html_keeps_hostile_content_as_data(self):
        k=copy.deepcopy(self.a);k['scope']['title']='</script><img src=x onerror=alert(1)>'
        d=e.payload(k,self.inputs)
        document=e.html_report(d)
        self.assertNotIn('</script><img',document)
        self.assertIn('\\u003c/script',document)
        self.assertNotIn('innerHTML',document)

    def test_one_command_demo_is_complete_and_offline(self):
        out=self.root/'demo';result=e.demo(out)
        self.assertEqual(result['api_calls'],0)
        self.assertTrue((out/'brief'/'brief.html').is_file())
        k,_=o.load_package(out/'v2');self.assertEqual(len(k['assertions']),5)
        with self.assertRaises(o.Invalid): e.demo(out)

    def test_query_evidence_cli_returns_source_excerpts(self):
        base=self.build();stdout=io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.assertEqual(o.main(['query',str(base),'--concept','metric:revenue','--with-evidence']),0)
        result=json.loads(stdout.getvalue())
        self.assertTrue(result['evidence_previews'][0]['excerpt'])
        self.assertIn('url',result['evidence_previews'][0])


class VersionConsistency(unittest.TestCase):
    """M158 案①一致性锁:脚本 VERSION 常量必须==两份 SKILL frontmatter version(防漂)。

    M158 追加(4.1 发现,lead 转):本包中英两份 SKILL 各带 version 字段,单读一份
    测不到两文漂移——遍历 SKILL.md+SKILL.en.md,三者(脚本+两份)同号才放行。"""

    def test_script_version_equals_both_skill_frontmatter(self):
        root = Path(__file__).resolve().parent.parent
        for name in ("SKILL.md", "SKILL.en.md"):
            with self.subTest(skill=name):
                text = (root / name).read_text(encoding="utf-8")
                fm = re.search(r"^---\s*\n(.*?)\n---\n", text, re.DOTALL)
                self.assertIsNotNone(fm, f"{name} 缺 frontmatter 块")
                mv = re.search(r'^version:\s*"?([0-9][^"\n]*)"?\s*$', fm.group(1), re.MULTILINE)
                self.assertIsNotNone(mv, f"{name} frontmatter 缺 version 字段")
                self.assertEqual(o.VERSION, mv.group(1),
                                 f"ontology.py VERSION={o.VERSION} 与 {name} frontmatter {mv.group(1)} 漂号(M156 第6项/M158 追加)")



class Patch024(unittest.TestCase):
    """0.3.0 (backtest fix, developed as unpublished dev-0.2.4): normalized quotes, enriched conflicts, catalog, strict query fields."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.inputs = self.root / "inputs"
        shutil.copytree(DEMO, self.inputs)

    def tearDown(self):
        self.temp.cleanup()

    def test_prepare_normalizes_table_pipes_but_keeps_verbatim_span(self):
        src = self.inputs / "demo-r1.txt"
        raw = src.read_text(encoding="utf-8")
        # Inject a markdown table line into a fresh source snapshot
        table = "金额 | 100 | 元\n其它"
        # Build minimal draft quoting without pipes; source has pipes
        content = "前言\n| 金额 | 100 | 元 |\n结语\n"
        snap = self.inputs / "table-src.txt"
        snap.write_text(content, encoding="utf-8")
        raw_b = content.encode("utf-8")
        draft = {
            "schema_version": o.SCHEMA_VERSION,
            "scope": {"title": "PipeQuote", "as_of": "2026-01-01"},
            "entities": [{"id": "org:subject", "type": "Organization", "name": "Subj"}],
            "definitions": [{"id": "metric:x", "kind": "metric", "value_type": "number",
                             "name": "X", "description": "x", "status": "candidate"}],
            "sources": [{
                "id": "source:t", "url": "https://example.com/t", "title": "t",
                "published_at": "2026-01-01", "accessed_at": "2026-01-02",
                "public_status": "synthetic", "parse_origin": "synthetic",
                "content_file": "table-src.txt", "sha256": o.digest(raw_b),
                "page_spans": [{"page": 1, "start_utf8": 0, "end_utf8": len(raw_b), "basis": "synthetic_page"}],
            }],
            "assertions": [{
                "entity_id": "org:subject", "concept_id": "metric:x", "value": 100,
                "unit": "CNY", "period": "2026Q1", "basis": "IFRS", "qualifiers": {},
                "evidence": [{"source_id": "source:t", "quote": "金额 100 元", "role": "value"}],
            }],
        }
        dp = self.inputs / "pipe-draft.json"
        dp.write_text(json.dumps(draft, ensure_ascii=False, indent=2), encoding="utf-8")
        out = self.root / "prepared-pipe"
        result = e.prepare(dp, out)
        self.assertEqual(result["status"], "prepared")
        self.assertGreaterEqual(result.get("quote_normalized_matches", 0), 1)
        k = o.read_json(out / "input.json")
        ev = k["assertions"][0]["evidence"][0]
        excerpt = raw_b[ev["start_utf8"]:ev["end_utf8"]].decode("utf-8")
        self.assertIn("|", excerpt)  # verbatim original keeps pipes
        self.assertEqual(ev["span_sha256"], o.digest(excerpt.encode("utf-8")))

    def test_conflict_details_marks_intra_report_vs_cross_period(self):
        a, _ = o.prepare_input(self.inputs / "r1.json")
        # Duplicate same fact key with different value, same source -> intra_report
        twin = copy.deepcopy(a["assertions"][0])
        twin["value"] = twin["value"] + 1 if isinstance(twin["value"], (int, float)) else "other"
        twin.pop("id", None); twin.pop("fact_id", None)
        twin["fact_id"] = o.fact_id(twin); twin["id"] = o.assertion_id(twin)
        a["assertions"].append(twin)
        details = o.conflict_details(a)
        self.assertTrue(details)
        self.assertEqual(details[0]["kind"], "intra_report")
        self.assertIn("old_value", details[0])
        self.assertIn("new_value", details[0])
        self.assertIn("severity", details[0])
        # Cross-period: use merged demo package
        dest = self.root / "v1"
        o.write_package(a, o.roots_for(a, self.inputs), dest, {})
        changes = o.read_json(dest / "changes.json")
        self.assertIsInstance(changes["conflicts"][0], dict)
        self.assertEqual(changes["conflicts"][0]["kind"], "intra_report")

    def test_catalog_lists_entities_and_changes(self):
        a, _ = o.prepare_input(self.inputs / "r1.json")
        dest = self.root / "v1"
        o.write_package(a, o.roots_for(a, self.inputs), dest, {"new_facts": [x["fact_id"] for x in a["assertions"]]})
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = o.main(["catalog", str(dest), "--kind", "all"])
        self.assertEqual(code, 0)
        data = json.loads(buf.getvalue())
        self.assertEqual(data["status"], "ok")
        self.assertTrue(data["entities"])
        self.assertTrue(data["definitions"])
        self.assertIn("conflicts", data["changes"])

    def test_query_args_json_rejects_unknown_field(self):
        a, _ = o.prepare_input(self.inputs / "r1.json")
        dest = self.root / "v1"
        o.write_package(a, o.roots_for(a, self.inputs), dest, {})
        buf = io.StringIO(); err = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(err):
            code = o.main(["query", str(dest), "--args-json", json.dumps({"concept": "metric:revenue", "bogus": 1})])
        self.assertEqual(code, 2)
        self.assertIn("unknown query fields", err.getvalue())

    def test_query_dict_rejects_unknown_field(self):
        a, _ = o.prepare_input(self.inputs / "r1.json")
        with self.assertRaises(o.Invalid):
            o.query(a, {"concept": "metric:revenue", "typo_field": "x"})

    def test_credit_risk_section_catalog_present(self):
        root = Path(__file__).resolve().parent.parent
        data = json.loads((root / "references" / "credit-risk-sections.json").read_text(encoding="utf-8"))
        ids = {s["id"] for s in data["sections"]}
        self.assertEqual(ids, {"audit_opinion", "mda", "guarantees", "borrowings",
                               "related_party", "litigation", "impairment", "going_concern"})
        self.assertTrue((root / "references" / "credit-risk-sections.md").exists())

class Patch025(unittest.TestCase):
    """0.3.0 (backtest fix, unpublished dev-0.2.5): cross_period only when disagreeing values come from different sources; severity order."""

    def _rows(self, spec):
        rows = []
        for i, (value, srcs) in enumerate(spec):
            rows.append({"id": f"assert:{i}", "value": value, "period": "2020-12-31",
                         "evidence": [{"source_id": s} for s in srcs]})
        return rows

    def test_two_values_same_report_plus_support_from_other_report_is_intra(self):
        k = {"sources": [{"id": "src:a"}, {"id": "src:b"}]}
        rows = self._rows([(80000000, ["src:a"]), (35000000, ["src:a"]), (80000000, ["src:b"])])
        self.assertEqual(o.conflict_kind(k, rows), "intra_report")

    def test_value_changed_between_reports_is_cross_period(self):
        k = {"sources": [{"id": "src:a"}, {"id": "src:b"}]}
        rows = self._rows([(640000000.0, ["src:a"]), (630000000.0, ["src:b"])])
        self.assertEqual(o.conflict_kind(k, rows), "cross_period")

    def test_severity_sort_high_medium_low(self):
        src = Path(o.__file__).read_text(encoding="utf-8")
        self.assertIn('rank = {"high": 0, "medium": 1, "low": 2}', src)


class Patch026(unittest.TestCase):
    """0.3.0 (backtest fix, unpublished dev-0.2.6): every conflict / new fact carries short verbatim excerpts (report, page, quote) from EvidenceSpans."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.inputs = self.root / "inputs"
        shutil.copytree(DEMO, self.inputs)
        self.a, _ = o.prepare_input(self.inputs / "r1.json")
        self.b, _ = o.prepare_input(self.inputs / "r2.json")

    def tearDown(self): self.temp.cleanup()

    def merged(self):
        dest = self.root / "v1"
        o.write_package(self.a, o.roots_for(self.a, self.inputs), dest, {})
        base, run = o.load_package(dest)
        k, changes = o.merge(base, self.b)
        out = self.root / "v2"
        roots = dict(o.roots_for(base, dest), **o.roots_for(self.b, self.inputs))
        o.write_package(k, roots, out, changes, run["knowledge_sha256"], "update")
        return out

    def _raw(self, pkg, source_id):
        k = o.read_json(pkg / "knowledge.json")
        s = [x for x in k["sources"] if x["id"] == source_id][0]
        return (pkg / s["content_file"]).read_bytes()

    def test_conflict_carries_verbatim_excerpts_for_both_sides(self):
        out = self.merged()
        ch = o.read_json(out / "changes.json")
        conflicts = [c for c in ch["conflicts"] if c["kind"] == "cross_period"]
        self.assertTrue(conflicts)
        c = conflicts[0]
        self.assertTrue(c["old_evidence"] and c["new_evidence"])
        self.assertNotEqual(c["old_evidence"][0]["source_id"], c["new_evidence"][0]["source_id"])
        for ev in c["old_evidence"] + c["new_evidence"]:
            raw = self._raw(out, ev["source_id"])
            full = raw[ev["start_utf8"]:ev["end_utf8"]].decode("utf-8")
            self.assertTrue(full.startswith(ev["quote"]))
            self.assertLessEqual(len(ev["quote"]), o.EXCERPT_CHARS)
            self.assertIn("report", ev); self.assertIn("page", ev)

    def test_new_facts_carry_excerpts_and_catalog_shows_them(self):
        out = self.merged()
        ch = o.read_json(out / "changes.json")
        self.assertEqual({d["fact_id"] for d in ch["new_fact_details"]}, set(ch["new_facts"]))
        for d in ch["new_fact_details"]:
            self.assertTrue(d["evidence"])
            for ev in d["evidence"] + d["prior_evidence"]:
                raw = self._raw(out, ev["source_id"])
                self.assertTrue(raw[ev["start_utf8"]:ev["end_utf8"]].decode("utf-8").startswith(ev["quote"]))
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.assertEqual(o.main(["catalog", str(out), "--kind", "changes"]), 0)
        data = json.loads(buf.getvalue())
        self.assertIn("new_fact_details", data["changes"])
        self.assertTrue(all("old_evidence" in c and "new_evidence" in c for c in data["changes"]["conflicts"]))

    def test_excerpt_truncation_flag(self):
        k = {"sources": [{"id": "s", "title": "t"}]}
        raw = ("甲" * 300).encode("utf-8")
        a = {"evidence": [{"source_id": "s", "page": 1, "start_utf8": 0, "end_utf8": len(raw)}]}
        ex = o.evidence_excerpts(k, a, {"s": raw})
        self.assertTrue(ex[0]["truncated"]); self.assertEqual(len(ex[0]["quote"]), o.EXCERPT_CHARS)



class OmniSource(unittest.TestCase):
    """0.3.0: saved Omni result -> exact content + page_spans (shapes as returned by @cueai/omni-reader-mcp 1.8.x;
    synthetic text and fake ids). No Bridge process, no network, no key."""

    PAGES = ["示例公司公告 第一页。\n累计逾期债务 12.34 亿元。", "第二页：新增诉讼 5 件，金额 0.67 亿元。", "Page three: 特此公告。"]

    def setUp(self):
        import hashlib
        import omni_source as om
        self.om, self.hashlib = om, hashlib
        self.temp = tempfile.TemporaryDirectory(); self.root = Path(self.temp.name)
        sep = "\n\n"
        self.content = sep.join(self.PAGES)
        segs, pos = [], 0
        for i, t in enumerate(self.PAGES, 1):
            n = len(t.encode("utf-8"))
            segs.append({"segment_id": f"segment_{i:06d}", "content_range_utf8": {"start": pos, "end": pos + n},
                         "grounding": {"availability": "available", "anchors": [
                             {"kind": "page", "basis": "source_pdf_page_1_based", "reliability": "reliable", "value": i}]}})
            pos += n + len(sep.encode("utf-8"))
        self.grounding = {"schema_version": "omni.grounding.v1", "detail": "grounded", "segments": segs,
                          "document": {"format": "pdf", "partial": False, "incomplete": [], "truncated": []}}
        self.meta = {"id": "src:omni-demo", "url": "https://example.org/omni-demo.pdf", "title": "Synthetic Omni result",
                     "published_at": None, "accessed_at": "2026-10-07", "public_status": "retrieved_public"}

    def tearDown(self):
        self.temp.cleanup()

    def digest(self, text):
        return "sha256:" + self.hashlib.sha256(text.encode("utf-8")).hexdigest()

    def response(self, storage="inline", content=None, grounding_as_text=False):
        content = self.content if content is None else content
        g = json.dumps(self.grounding, ensure_ascii=False) if grounding_as_text else self.grounding
        if storage == "inline":
            parts = {"content": {"part": "content", "digest": self.digest(self.content), "storage": {"kind": "inline", "text": content}},
                     "grounding": {"part": "grounding", "storage": {"kind": "inline", **({"text": g} if grounding_as_text else {"value": g})}}}
        else:
            parts = {"content": {"part": "content", "digest": self.digest(self.content), "storage": {"kind": "artifact", "next_cursor": "c:content:0"}},
                     "grounding": {"part": "grounding", "storage": {"kind": "artifact", "next_cursor": "c:grounding:0"}}}
        sc = {"status": "completed", "operation_id": "op_fake",
              "result": {"kind": "bundle", "result_id": "result_fake", "detail": "grounded",
                         "bundle_protocol_version": "omni.result_bundle.v1", "parts": parts},
              "billing": {"credits_charged": 0}}
        return {"jsonrpc": "2.0", "id": 3, "result": {"content": [{"type": "text", "text": json.dumps(sc, ensure_ascii=False)}],
                                                       "structuredContent": sc}}

    def save(self, obj, name="r.json"):
        p = self.root / name
        p.write_text(obj if isinstance(obj, str) else json.dumps(obj, ensure_ascii=False), encoding="utf-8")
        return p

    def test_inline_result_to_page_spans_prepare_and_build(self):
        r = self.om.build_source(self.save(self.response()), self.root / "src", self.meta, "omni_replay", fy=2026)
        self.assertEqual(r["pages"], [1, 2, 3])
        rec = json.loads(Path(r["source_record"]).read_text(encoding="utf-8"))
        raw = (self.root / "src" / rec["content_file"]).read_bytes()
        self.assertEqual(raw, self.content.encode("utf-8"))
        for span, text in zip(rec["page_spans"], self.PAGES):
            self.assertEqual(raw[span["start_utf8"]:span["end_utf8"]].decode("utf-8"), text)
            self.assertEqual(span["basis"], o.OMNI)
        lines = [json.loads(x) for x in (self.root / "src" / "FY2026.pages.jsonl").read_text(encoding="utf-8").splitlines()]
        self.assertEqual([x["text"] for x in lines], self.PAGES)
        draft = {"schema_version": o.SCHEMA_VERSION, "scope": {"title": "Omni replay", "as_of": "2026-10-07"},
                 "entities": [{"id": "org:demo", "type": "Organization", "name": "Demo (synthetic)"}],
                 "definitions": [{"id": "metric:overdue", "kind": "metric", "name": "Cumulative overdue debt",
                                  "description": "As explicitly reported.", "value_type": "number", "status": "candidate"}],
                 "sources": [rec],
                 "assertions": [{"entity_id": "org:demo", "concept_id": "metric:overdue", "value": 12.34, "period": "2026-09-28",
                                 "basis": "as_reported", "unit": "CNY_100m", "qualifiers": {}, "valid_from": None, "valid_to": None,
                                 "claim_kind": "reported", "evidence": [{"source_id": rec["id"], "role": "value_and_scope",
                                                                         "quote": "累计逾期债务 12.34 亿元。"}]}]}
        (self.root / "src" / "draft.json").write_text(json.dumps(draft, ensure_ascii=False), encoding="utf-8")
        e.prepare(self.root / "src" / "draft.json", self.root / "prep")
        out = self.root / "v1"
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(o.main(["build", str(self.root / "prep" / "input.json"), "--out", str(out)]), 0)
        k, _ = o.load_package(out)
        ev = k["assertions"][0]["evidence"][0]
        self.assertEqual((ev["page"], ev["locator_basis"]), (1, o.OMNI))

    def test_artifact_storage_is_read_back_and_digest_checked(self):
        content, grounding = self.content, json.dumps(self.grounding, ensure_ascii=False)
        calls = []

        class FakeBridge:
            def tool(self, name, args, timeout=0):
                calls.append(args)
                part, i = args["cursor"].split(":")[1], int(args["cursor"].split(":")[2])
                text = content if part == "content" else grounding
                chunks = [text[j:j + 7] for j in range(0, len(text), 7)]
                return {"status": "completed", "result": {"text": chunks[i],
                        "next_cursor": f"c:{part}:{i + 1}" if i + 1 < len(chunks) else None}}

        r = self.om.build_source(self.save(self.response("artifact")), self.root / "a", self.meta, bridge=FakeBridge())
        self.assertEqual(r["pages"], [1, 2, 3]); self.assertGreater(len(calls), 5)
        self.assertTrue(all(c["result_id"] == "result_fake" and c["max_bytes"] <= 65536 for c in calls))
        content = self.content[:-1]                       # truncated read -> digest mismatch -> nothing written
        with self.assertRaisesRegex(self.om.OmniError, "digest"):
            self.om.build_source(self.save(self.response("artifact"), "t.json"), self.root / "b", self.meta, bridge=FakeBridge())
        self.assertFalse((self.root / "b").exists())

        class Expired:
            def tool(self, name, args, timeout=0):
                return {"status": "failed", "error": {"code": "RESULT_EXPIRED", "billed": False}}
        with self.assertRaisesRegex(self.om.OmniError, "expired"):
            self.om.build_source(self.save(self.response("artifact"), "e.json"), self.root / "c", self.meta, bridge=Expired())

    def test_shapes_structured_content_compact_text_and_grounding_text(self):
        full = self.response(grounding_as_text=True)
        for name, obj in (("sc.json", full["result"]["structuredContent"]),
                          ("compact.json", {"content": full["result"]["content"]}),
                          ("full.json", full)):
            with self.subTest(shape=name):
                r = self.om.build_source(self.save(obj, name), self.root / name[:-5], self.meta)
                self.assertEqual(r["pages"], [1, 2, 3])

    def test_conservative_page_mapping(self):
        raw = "AAAA|BBBB|CCCC|DDDD|EEEE|FFFF"
        def seg(a, b, anchors):
            return {"content_range_utf8": {"start": a, "end": b}, "grounding": {"anchors": anchors}}
        src = lambda v: {"kind": "page", "basis": "source_pdf_page_1_based", "value": v}
        rendered = {"kind": "page", "basis": "rendered_pdf_page_1_based", "value": 9}
        g = {"segments": [seg(0, 4, [src(1)]), seg(5, 9, [src(1)]), seg(10, 14, [rendered]),
                          seg(15, 19, [src(2), src(3)]), seg(20, 24, [src(2)]), seg(25, 29, [src(1)])],
             "document": {"partial": True}}
        spans, warns = self.om.page_spans(raw, g)
        self.assertEqual([(s["page"], s["start_utf8"], s["end_utf8"]) for s in spans], [(1, 0, 9), (2, 20, 24)])
        joined = " ".join(warns)
        for word in ("rendered_page_only", "multi_page", "page_reappears", "partial"):
            self.assertIn(word, joined)

    def test_markdown_failures_and_overwrite_are_refused(self):
        md = self.save(self.content, "r.md")
        with self.assertRaisesRegex(self.om.OmniError, "structuredContent"):
            self.om.build_source(md, self.root / "m", self.meta)
        r = self.om.build_source(md, self.root / "m", self.meta, text_only=True)
        rec = json.loads(Path(r["source_record"]).read_text(encoding="utf-8"))
        self.assertEqual(rec["page_spans"], [])
        for code in ("SOURCE_ACCESS_DENIED", "DETAIL_CAPABILITIES_UNAVAILABLE"):
            bad = {"status": "failed", "error": {"code": code, "billed": False}}
            with self.assertRaisesRegex(self.om.OmniError, code):
                self.om.build_source(self.save(bad, code + ".json"), self.root / "f", self.meta)
        p = self.save(self.response(), "ok.json")
        self.om.build_source(p, self.root / "o", self.meta)
        with self.assertRaisesRegex(self.om.OmniError, "overwrite"):
            self.om.build_source(p, self.root / "o", self.meta)
        with self.assertRaisesRegex(self.om.OmniError, "parse_origin"):
            self.om.build_source(p, self.root / "o2", self.meta, parse_origin="synthetic")

    def test_cli_validates_metadata(self):
        p = self.save(self.response())
        base = ["omni-source", str(p), "--id", "src:cli", "--title", "t", "--accessed-at", "2026-10-07"]
        with contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(o.main(base + ["--url", "https://example.org/x.pdf", "--out", str(self.root / "cli")]), 0)
        self.assertEqual(json.loads(out.getvalue())["pages"], [1, 2, 3])
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(o.main(base + ["--url", "http://127.0.0.1/x.pdf", "--out", str(self.root / "cli2")]), 2)
        self.assertFalse((self.root / "cli2").exists())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    unittest.main(argv=[__file__], verbosity=2)
