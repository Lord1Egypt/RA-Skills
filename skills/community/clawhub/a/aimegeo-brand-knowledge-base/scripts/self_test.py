#!/usr/bin/env python3
"""Offline business tests; does not depend on icons, licensing files, or a host repo."""

import copy
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class KnowledgeBaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="brand-kb-test-")
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        self.inputs = self.work / "inputs"
        self.inputs.mkdir()
        shutil.copytree(ROOT / "examples" / "materials", self.inputs / "materials")
        for name in ("input.json", "update.json", "resolution.json", "failure-unsupported.json",
                     "project-split-input.json", "project-split-update.json", "project-split-resolution.json",
                     "failure-incomplete-project-split.json"):
            shutil.copyfile(ROOT / "examples" / name, self.inputs / name)
        self.output = self.work / "knowledge-base"
        self.payload = json.loads((self.inputs / "input.json").read_text(encoding="utf-8"))

    def run_build(self, name="input.json", success=True, output=None):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "knowledge_base.py"), "build",
             "--input", str(self.inputs / name), "--output", str(output or self.output)],
            cwd=self.work, capture_output=True, encoding="utf-8",
            env={"PYTHONIOENCODING": "utf-8"},
        )
        self.assertEqual(result.returncode, 0 if success else 2, result.stdout + result.stderr)
        data = json.loads(result.stdout if success else result.stderr)
        self.assertEqual(data["status"], "ok" if success else "error")
        return data

    def write_payload(self, payload, name="custom.json"):
        (self.inputs / name).write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return name

    def index(self):
        return json.loads((self.output / "知识索引.json").read_text(encoding="utf-8"))

    def snapshot(self):
        return {p.relative_to(self.output).as_posix(): p.read_bytes() for p in self.output.rglob("*") if p.is_file()}

    def test_full_local_delivery_matches_checked_example(self):
        result = self.run_build()
        self.assertEqual(result["stats"], {
            "source_count": 3, "record_count": 7, "fact_count": 6,
            "usable_fact_count": 6, "conflict_fact_count": 0, "pending_fact_count": 0,
            "superseded_fact_count": 0, "open_gap_count": 2,
        })
        index = self.index()
        self.assertEqual(len(index["documents"]), 5)
        self.assertEqual({doc["path"].split("/")[0] for doc in index["documents"]}, {"公司", "产品", "主题"})
        self.assertFalse(any(doc["category"] == "trust" for doc in index["documents"]))
        for fact in index["facts"]:
            body = (self.output / fact["document_path"]).read_text(encoding="utf-8")
            self.assertIn(fact["texts"][0], body)
            self.assertEqual(fact["project_ids"], ["content-demo"])
        for source in index["sources"]:
            self.assertEqual((self.output / source["snapshot_path"]).read_bytes(), (self.inputs / source["origin"]).read_bytes())
        expected_root = ROOT / "examples" / "expected"
        expected = {p.relative_to(expected_root).as_posix(): p.read_bytes() for p in expected_root.rglob("*") if p.is_file()}
        self.assertEqual(self.snapshot(), expected)

    def test_duplicate_fact_retains_both_source_locations(self):
        self.run_build()
        facts = [f for f in self.index()["facts"] if f["key"] == "delivery_formats"]
        self.assertEqual(len(facts), 1)
        self.assertEqual(set(facts[0]["record_ids"]), {"fact-export-intro", "fact-export-faq"})
        self.assertEqual({ref["source_id"] for ref in facts[0]["sources"]}, {"intro-v1", "faq-v1"})

    def test_repeat_import_is_byte_identical(self):
        self.run_build()
        before = self.snapshot()
        self.run_build()
        self.assertEqual(self.snapshot(), before)

    def test_update_conflict_and_explicit_replacement_preserve_history(self):
        self.run_build()
        manual = self.output / "团队补充.md"
        manual.write_text("用户手写的选题备注。", encoding="utf-8")
        old_sources = {p.name: p.read_bytes() for p in (self.output / "原始资料").iterdir()}
        result = self.run_build("update.json")
        self.assertEqual(result["stats"]["conflict_fact_count"], 2)
        self.assertEqual(result["stats"]["usable_fact_count"], 5)
        self.assertEqual(result["stats"]["record_count"], 8)
        self.assertEqual(manual.read_text(encoding="utf-8"), "用户手写的选题备注。")
        for name, raw in old_sources.items():
            self.assertEqual((self.output / "原始资料" / name).read_bytes(), raw)
        versions = [f for f in self.index()["facts"] if f["key"] == "delivery_formats"]
        self.assertTrue(all(f["status"] == "conflict" for f in versions))
        result = self.run_build("resolution.json")
        self.assertEqual(result["stats"]["conflict_fact_count"], 0)
        self.assertEqual(result["stats"]["usable_fact_count"], 6)
        versions = [f for f in self.index()["facts"] if f["key"] == "delivery_formats"]
        self.assertEqual([f["value"] for f in versions if f["status"] == "supported"], ["Markdown+JSON+CSV"])
        self.assertEqual(sum(f["status"] == "superseded" for f in versions), 2)
        self.assertEqual(len(self.index()["records"]), 9)
        self.assertEqual(len(self.index()["sources"]), 4)
        self.assertEqual(result["stats"]["open_gap_count"], 2)

    def test_unsupported_claim_fails_before_writing(self):
        error = self.run_build("failure-unsupported.json", success=False)
        self.assertEqual(error, json.loads((ROOT / "examples" / "failure-output.json").read_text(encoding="utf-8")))
        self.assertFalse(self.output.exists())

    def test_fabricated_quote_rejected(self):
        payload = copy.deepcopy(self.payload)
        payload["records"][0]["sources"][0]["quote"] = "不存在于资料中的奖项和业绩。"
        self.run_build(self.write_payload(payload), success=False)
        self.assertFalse(self.output.exists())

    def test_missing_source_is_not_treated_as_evidence(self):
        payload = copy.deepcopy(self.payload)
        payload["sources"][0]["path"] = "materials/absent.md"
        self.run_build(self.write_payload(payload), success=False)
        self.assertFalse(self.output.exists())

    def test_wrong_target_identity_keeps_existing_files(self):
        self.run_build()
        before = self.snapshot()
        payload = {"schema_version": 1, "kb": {"id": "different-kb", "name": self.payload["kb"]["name"]}, "as_of": "2026-10-20"}
        self.run_build(self.write_payload(payload), success=False)
        self.assertEqual(self.snapshot(), before)
        payload["kb"] = {"id": self.payload["kb"]["id"], "name": "同ID但错误名称"}
        self.run_build(self.write_payload(payload), success=False)
        self.assertEqual(self.snapshot(), before)

    def test_reusing_fact_id_cannot_overwrite_content(self):
        self.run_build()
        before = self.snapshot()
        payload = copy.deepcopy(self.payload)
        payload["records"][0]["text"] = "未经原记录声明的新说法。"
        self.run_build(self.write_payload(payload), success=False)
        self.assertEqual(self.snapshot(), before)

    def test_source_id_is_immutable_and_raw_copy_is_preserved(self):
        self.run_build()
        before = self.snapshot()
        source = self.inputs / "materials" / "product.md"
        source.write_text(source.read_text(encoding="utf-8") + "\n新版附注。\n", encoding="utf-8")
        self.run_build(success=False)
        self.assertEqual(self.snapshot(), before)

    def test_manually_edited_managed_document_is_not_overwritten(self):
        self.run_build()
        document = self.output / self.index()["documents"][0]["path"]
        document.write_text(document.read_text(encoding="utf-8") + "\n人工补充。\n", encoding="utf-8")
        before = self.snapshot()
        self.run_build("update.json", success=False)
        self.assertEqual(self.snapshot(), before)

    def test_unmanaged_file_collision_fails_before_partial_output(self):
        self.output.mkdir()
        (self.output / "知识库目录.md").write_text("已有独立目录", encoding="utf-8")
        before = self.snapshot()
        self.run_build(success=False)
        self.assertEqual(self.snapshot(), before)

    def test_project_scopes_do_not_cross_merge_or_conflict(self):
        payload = copy.deepcopy(self.payload)
        payload["projects"].append({"id": "other", "name": "独立试验项目"})
        for entity in payload["entities"]:
            entity["project_ids"].append("other")
        other = copy.deepcopy(payload["records"][2])
        other.update(id="fact-other", value="仅适用另一项目的约定", project_ids=["other"])
        payload["records"].append(other)
        self.run_build(self.write_payload(payload))
        facts = [f for f in self.index()["facts"] if f["key"] == "delivery_formats"]
        self.assertEqual(len(facts), 2)
        self.assertTrue(all(f["status"] == "supported" for f in facts))
        self.assertEqual({tuple(f["project_ids"]) for f in facts}, {("content-demo",), ("other",)})

    def direct_split_payload(self):
        payload = json.loads((self.inputs / "project-split-resolution.json").read_text(encoding="utf-8"))
        update = json.loads((self.inputs / "project-split-update.json").read_text(encoding="utf-8"))
        payload["sources"] = update["sources"]
        payload["records"][0]["supersedes"] = ["shared-v1"]
        return payload

    def test_project_split_restores_current_facts_and_preserves_history(self):
        self.run_build("project-split-input.json")
        result = self.run_build("project-split-update.json")
        self.assertEqual(result["stats"]["conflict_fact_count"], 2)
        self.assertEqual(result["stats"]["usable_fact_count"], 0)
        before = self.index()
        old_sources = {s["snapshot_path"]: (self.output / s["snapshot_path"]).read_bytes() for s in before["sources"]}
        result = self.run_build("project-split-resolution.json")
        self.assertEqual(result["stats"], {
            "source_count": 2, "record_count": 4, "fact_count": 4,
            "usable_fact_count": 2, "conflict_fact_count": 0, "pending_fact_count": 0,
            "superseded_fact_count": 2, "open_gap_count": 0,
        })
        index = self.index()
        current = {tuple(f["project_ids"]): f for f in index["facts"] if f["status"] == "supported"}
        self.assertEqual(set(current), {("project-a",), ("project-b",)})
        self.assertEqual(current[("project-a",)]["value"], "Markdown+JSON+CSV")
        self.assertEqual(current[("project-b",)]["value"], "Markdown+JSON")
        historical = {f["id"]: f for f in index["facts"] if f["status"] == "superseded"}
        self.assertEqual(set(historical), {"shared-v1", "a-update"})
        self.assertEqual(historical["shared-v1"]["project_ids"], ["project-a", "project-b"])
        self.assertEqual(historical["shared-v1"]["superseded_by"], ["a-current", "b-current"])
        for record in before["records"]:
            self.assertIn(record, index["records"])
        for relative, raw in old_sources.items():
            self.assertEqual((self.output / relative).read_bytes(), raw)
        for fact in current.values():
            self.assertFalse(fact["conflicts_with"])
            self.assertTrue(fact["sources"])
            body = (self.output / fact["document_path"]).read_text(encoding="utf-8")
            self.assertIn(fact["texts"][0], body)
        snapshot = self.snapshot()
        self.run_build("project-split-resolution.json")
        self.assertEqual(self.snapshot(), snapshot)
        replay = json.loads((self.inputs / "project-split-input.json").read_text(encoding="utf-8"))
        replay["as_of"] = index["as_of"]
        self.run_build(self.write_payload(replay))
        self.assertEqual(self.snapshot(), snapshot)
        next_a = copy.deepcopy(next(r for r in index["records"] if r["id"] == "a-current"))
        next_a.update(id="a-next", supersedes=["a-current"])
        followup = {"schema_version": 1, "kb": index["kb"], "as_of": "2026-10-22", "records": [next_a]}
        self.run_build(self.write_payload(followup))
        current_ids = {f["id"] for f in self.index()["facts"] if f["status"] == "supported"}
        self.assertEqual(current_ids, {"a-next", "b-current"})
        self.assertEqual(self.index()["stats"]["conflict_fact_count"], 0)

    def test_project_split_can_replace_shared_fact_in_one_import(self):
        self.run_build("project-split-input.json")
        self.run_build(self.write_payload(self.direct_split_payload()))
        facts = {f["id"]: f for f in self.index()["facts"]}
        self.assertEqual({rid: f["status"] for rid, f in facts.items()}, {
            "shared-v1": "superseded", "a-current": "supported", "b-current": "supported",
        })

    def test_incomplete_project_split_rejected_without_changing_existing_files(self):
        self.run_build("project-split-input.json")
        before = self.snapshot()
        error = self.run_build("failure-incomplete-project-split.json", success=False)
        self.assertEqual(error, {
            "status": "error",
            "message": "替代事实必须完整覆盖旧记录 shared-v1 的项目范围；尚缺项目：project-b；为未变更项目新增保留原值的替代记录",
        })
        self.assertEqual(self.snapshot(), before)

    def test_project_split_cannot_expand_or_move_target_scope(self):
        self.run_build("project-split-input.json")
        self.run_build("project-split-update.json")
        before = self.snapshot()
        for scope in (["project-b"], ["project-a", "project-b"]):
            with self.subTest(scope=scope):
                payload = self.direct_split_payload()
                replacement = payload["records"][0]
                replacement.update(id="invalid-scope", project_ids=scope, supersedes=["a-update"])
                payload["records"] = [replacement]
                error = self.run_build(self.write_payload(payload), success=False)
                self.assertEqual(error["message"], "替代事实的项目范围必须是旧记录 a-update 的项目范围子集")
                self.assertEqual(self.snapshot(), before)

    def test_project_split_does_not_hide_conflicting_successors(self):
        self.run_build("project-split-input.json")
        payload = self.direct_split_payload()
        old = copy.deepcopy(self.index()["records"][0])
        old.update(id="a-old-value", project_ids=["project-a"], supersedes=["shared-v1"])
        payload["records"].append(old)
        self.run_build(self.write_payload(payload))
        facts = {f["id"]: f for f in self.index()["facts"]}
        self.assertEqual(facts["shared-v1"]["status"], "superseded")
        self.assertEqual(facts["a-current"]["status"], "conflict")
        self.assertEqual(facts["a-old-value"]["status"], "conflict")
        self.assertEqual(facts["b-current"]["status"], "supported")

    def test_project_split_must_replace_all_original_duplicate_records(self):
        base = json.loads((self.inputs / "project-split-input.json").read_text(encoding="utf-8"))
        duplicate = copy.deepcopy(base["records"][0])
        duplicate["id"] = "shared-extra"
        base["records"].append(duplicate)
        self.run_build(self.write_payload(base))
        self.assertEqual(self.index()["facts"][0]["record_ids"], ["shared-extra", "shared-v1"])
        self.run_build(self.write_payload(self.direct_split_payload()))
        facts = {f["id"]: f for f in self.index()["facts"]}
        self.assertEqual(facts["shared-v1"]["status"], "superseded")
        self.assertEqual(facts["shared-extra"]["status"], "conflict")
        self.assertEqual(facts["a-current"]["status"], "conflict")
        self.assertEqual(facts["b-current"]["status"], "supported")

    def test_project_split_coverage_is_checked_for_each_target(self):
        base = json.loads((self.inputs / "project-split-input.json").read_text(encoding="utf-8"))
        duplicate = copy.deepcopy(base["records"][0])
        duplicate["id"] = "shared-extra"
        base["records"].append(duplicate)
        self.run_build(self.write_payload(base))
        before = self.snapshot()
        payload = self.direct_split_payload()
        payload["records"][1]["supersedes"] = ["shared-extra"]
        error = self.run_build(self.write_payload(payload), success=False)
        self.assertEqual(error["message"],
                         "替代事实必须完整覆盖旧记录 shared-extra 的项目范围；尚缺项目：project-a；为未变更项目新增保留原值的替代记录")
        self.assertEqual(self.snapshot(), before)

    def test_pending_project_split_cannot_replace_supported_history(self):
        self.run_build("project-split-input.json")
        before = self.snapshot()
        payload = self.direct_split_payload()
        payload["records"][0].update(status="pending", sources=[])
        error = self.run_build(self.write_payload(payload), success=False)
        self.assertEqual(error["message"], "只有有来源支持的新事实可以替代旧事实")
        self.assertEqual(self.snapshot(), before)

    def test_unknown_entity_or_project_rejected(self):
        for field, value in (("entity_id", "unknown-brand"), ("project_ids", ["unknown-project"])):
            with self.subTest(field=field):
                payload = copy.deepcopy(self.payload)
                payload["records"][0][field] = value
                self.run_build(self.write_payload(payload), success=False)
                self.assertFalse(self.output.exists())

    def test_source_path_cannot_escape_input_directory(self):
        payload = copy.deepcopy(self.payload)
        payload["sources"][0]["path"] = "../outside.md"
        self.run_build(self.write_payload(payload), success=False)
        self.assertFalse(self.output.exists())

    def test_source_symlink_is_not_followed(self):
        external = self.work / "outside.md"
        external.write_text("外部内容", encoding="utf-8")
        (self.inputs / "materials" / "linked.md").symlink_to(external)
        payload = copy.deepcopy(self.payload)
        payload["sources"][0]["path"] = "materials/linked.md"
        self.run_build(self.write_payload(payload), success=False)
        self.assertFalse(self.output.exists())

    def test_pending_claim_is_retained_but_never_usable(self):
        payload = json.loads((self.inputs / "failure-unsupported.json").read_text(encoding="utf-8"))
        payload["records"][0]["status"] = "pending"
        result = self.run_build(self.write_payload(payload))
        self.assertEqual(result["stats"]["pending_fact_count"], 1)
        self.assertEqual(result["stats"]["usable_fact_count"], 0)
        self.assertEqual(self.index()["facts"][0]["sources"], [])

    def test_supported_duplicate_does_not_promote_pending_text(self):
        payload = copy.deepcopy(self.payload)
        pending = copy.deepcopy(payload["records"][2])
        pending.update(id="fact-export-pending", status="pending", sources=[], text="关于相同交付格式的一段待核实补充。")
        payload["records"].append(pending)
        self.run_build(self.write_payload(payload))
        facts = [f for f in self.index()["facts"] if f["key"] == "delivery_formats"]
        self.assertEqual(len(facts), 2)
        self.assertEqual({f["status"] for f in facts}, {"supported", "pending"})
        usable = next(f for f in facts if f["status"] == "supported")
        self.assertNotIn(pending["text"], usable["texts"])
        self.assertNotIn(pending["id"], usable["record_ids"])

    def test_gap_resolution_requires_current_usable_evidence(self):
        payload = copy.deepcopy(self.payload)
        payload["gaps"] = [{
            "id": "gap-delivery", "entity_id": "product-a", "project_ids": ["content-demo"],
            "question": "交付格式是什么？", "reason": "确认当前交付格式。",
            "resolved_by": ["fact-export-intro", "fact-export-faq"],
        }]
        self.run_build(self.write_payload(payload))
        self.assertTrue(self.index()["gap_results"][0]["resolved"])
        self.run_build("update.json")
        self.assertFalse(self.index()["gap_results"][0]["resolved"])
        self.assertEqual(self.index()["stats"]["open_gap_count"], 1)

    def split_gap(self, resolved_by=()):
        return {"id": "gap-project-delivery", "entity_id": "product-a",
                "project_ids": ["project-a", "project-b"], "question": "A、B两个项目分别交付哪些格式？",
                "reason": "两个项目都需要当前交付依据。", "resolved_by": list(resolved_by)}

    def initialize_split_gap(self):
        base = json.loads((self.inputs / "project-split-input.json").read_text(encoding="utf-8"))
        base["gaps"] = [self.split_gap(["shared-v1"])]
        self.run_build(self.write_payload(base))
        self.run_build("project-split-update.json")

    def test_split_gap_is_closed_by_joint_project_coverage(self):
        self.initialize_split_gap()
        self.assertEqual(self.index()["stats"]["open_gap_count"], 1)
        payload = json.loads((self.inputs / "project-split-resolution.json").read_text(encoding="utf-8"))
        payload["gaps"] = [self.split_gap(["a-current", "b-current"])]
        result = self.run_build(self.write_payload(payload))
        self.assertEqual(result["stats"]["open_gap_count"], 0)
        self.assertEqual(self.index()["gap_results"], [{**self.split_gap(["a-current", "b-current"]), "resolved": True}])
        old = next(fact for fact in self.index()["facts"] if fact["id"] == "shared-v1")
        self.assertEqual(old["status"], "superseded")
        self.assertEqual(old["project_ids"], ["project-a", "project-b"])
        before = self.snapshot()
        self.run_build(self.write_payload(payload))
        self.assertEqual(self.snapshot(), before)

    def test_split_gap_only_one_project_fails_without_changing_library(self):
        self.initialize_split_gap()
        self.run_build("project-split-resolution.json")
        before = self.snapshot()
        payload = {"schema_version": 1, "kb": self.index()["kb"], "as_of": "2026-10-22",
                   "gaps": [self.split_gap(["a-current"])]}
        error = self.run_build(self.write_payload(payload), success=False)
        self.assertEqual(error["message"], "缺失项解决证据未完整覆盖项目：project-b")
        self.assertEqual(self.snapshot(), before)

    def test_split_gap_cannot_union_evidence_from_other_entity(self):
        self.initialize_split_gap()
        self.run_build("project-split-resolution.json")
        before = self.snapshot()
        other = copy.deepcopy(next(r for r in self.index()["records"] if r["id"] == "b-current"))
        other.update(id="other-b", entity_id="other-product", supersedes=[])
        payload = {"schema_version": 1, "kb": self.index()["kb"], "as_of": "2026-10-22",
                   "entities": [{"id": "other-product", "kind": "product", "name": "受控另一对象",
                                 "project_ids": ["project-a", "project-b"]}],
                   "records": [other], "gaps": [self.split_gap(["a-current", "other-b"])]}
        error = self.run_build(self.write_payload(payload), success=False)
        self.assertEqual(error["message"], "缺失项解决证据的对象或项目范围不匹配")
        self.assertEqual(self.snapshot(), before)

    def test_split_gap_does_not_count_superseded_shared_scope(self):
        self.initialize_split_gap()
        self.run_build("project-split-resolution.json")
        self.assertFalse(self.index()["gap_results"][0]["resolved"])
        payload = {"schema_version": 1, "kb": self.index()["kb"], "as_of": "2026-10-22",
                   "gaps": [self.split_gap(["a-current", "shared-v1"])]}
        self.run_build(self.write_payload(payload))
        self.assertFalse(self.index()["gap_results"][0]["resolved"])
        self.assertEqual(self.index()["stats"]["open_gap_count"], 1)

    def test_split_gap_pending_record_does_not_complete_current_coverage(self):
        self.initialize_split_gap()
        self.run_build("project-split-resolution.json")
        pending = copy.deepcopy(next(r for r in self.index()["records"] if r["id"] == "b-current"))
        pending.update(id="b-pending", status="pending", sources=[], supersedes=[])
        payload = {"schema_version": 1, "kb": self.index()["kb"], "as_of": "2026-10-22",
                   "records": [pending], "gaps": [self.split_gap(["a-current", "b-pending"])]}
        self.run_build(self.write_payload(payload))
        self.assertFalse(self.index()["gap_results"][0]["resolved"])
        payload = {"schema_version": 1, "kb": self.index()["kb"], "as_of": "2026-10-22",
                   "gaps": [self.split_gap(["a-current", "b-current"])]}
        self.run_build(self.write_payload(payload))
        self.assertTrue(self.index()["gap_results"][0]["resolved"])

    def test_empty_records_cannot_produce_folder_only_delivery(self):
        payload = copy.deepcopy(self.payload)
        payload["records"] = []
        self.run_build(self.write_payload(payload), success=False)
        self.assertFalse(self.output.exists())

    def test_replacement_cycles_rejected(self):
        payload = copy.deepcopy(self.payload)
        payload["records"][2]["supersedes"] = ["fact-export-faq"]
        payload["records"][3]["supersedes"] = ["fact-export-intro"]
        self.run_build(self.write_payload(payload), success=False)
        self.assertFalse(self.output.exists())

    def test_cross_entity_replacement_rejected(self):
        payload = copy.deepcopy(self.payload)
        payload["records"][2]["supersedes"] = ["fact-company"]
        self.run_build(self.write_payload(payload), success=False)
        self.assertFalse(self.output.exists())

    def test_stale_incremental_date_rejected(self):
        self.run_build()
        before = self.snapshot()
        payload = {"schema_version": 1, "kb": self.payload["kb"], "as_of": "2026-10-18"}
        self.run_build(self.write_payload(payload), success=False)
        self.assertEqual(self.snapshot(), before)


if __name__ == "__main__":
    unittest.main(verbosity=2)
