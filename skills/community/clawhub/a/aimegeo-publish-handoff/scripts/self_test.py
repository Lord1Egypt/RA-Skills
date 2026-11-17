#!/usr/bin/env python3
"""Business tests using disposable local packs, with no external services."""

import copy
from datetime import datetime, timedelta, timezone
from itertools import permutations
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "handoff.py"
LEDGER = "发布交接包.json"


class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="publish-handoff-test-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.input = self.base / "input"
        shutil.copytree(ROOT / "examples" / "input", self.input)
        self.plan_path = self.input / "plan.json"
        self.plan = json.loads(self.plan_path.read_text())
        self.pack = self.base / "pack"
        self.tick = datetime.now(timezone.utc)

    def call(self, *args, error=None, cli=CLI):
        result = subprocess.run([sys.executable, str(cli), *map(str, args)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2 if error else 0, result.stdout + result.stderr)
        data = json.loads(result.stderr if error else result.stdout)
        if error:
            self.assertEqual(data["error"], error, data)
        return data

    def prepare(self, plan=None):
        if plan is not None:
            self.plan_path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
        return self.call("prepare", "--input", self.plan_path, "--out", self.pack)

    def ledger(self):
        return json.loads((self.pack / LEDGER).read_text())

    def target(self, platform="csdn"):
        return next(t for t in self.ledger()["targets"] if t["platform"] == platform)

    def receipt(self, status, mode="observed", **extra):
        t = self.target()
        self.tick = max(self.tick + timedelta(microseconds=1), datetime.now(timezone.utc))
        r = {"receipt_id": "test-" + str(self.tick.timestamp()), "platform": t["platform"],
             "account_id": t["account_id"], "draft_sha256": self.ledger()["draft"]["sha256"],
             "mode": mode, "observed_at": self.tick.isoformat(),
             "source": "合成测试输入，非真实平台记录", "evidence": "测试中的原生管理页回读记录"}
        if status:
            r["status"] = status
        if status in {"submitted", "under_review", "public"}:
            r["native_id"] = "fixture-native-7"
        if status == "pre_filled":
            r["checks"] = {"account": True, "title": True, "body": True, "assets": True}
        r.update(extra)
        return r

    def record(self, receipt, error=None):
        p = self.base / "receipt.json"
        p.write_text(json.dumps(receipt, ensure_ascii=False), encoding="utf-8")
        return self.call("record", "--pack", self.pack, "--receipt", p, error=error)

    def grant(self, **extra):
        t = self.target()
        auth = {**t["authorization"], "action": "submit", "reference": "合成测试：当前账号当前稿允许一次投稿"}
        auth.update(extra)
        path = self.base / "authorization.json"
        path.write_text(json.dumps(auth, ensure_ascii=False), encoding="utf-8")
        return path

    def begin(self, error=None, auth=True):
        args = ["intent", "--pack", self.pack, "--target", self.target()["id"]]
        if auth:
            args += ["--authorization", self.grant()]
        return self.call(*args, error=error)

    def recovery_history(self):
        target = self.plan["targets"][1]
        common = {"platform": target["platform"], "account_id": target["account_id"],
                  "draft_sha256": target["authorization"]["draft_sha256"], "mode": "observed",
                  "source": "离线合成历史，非真实发布记录", "evidence": "合成回读字段，仅用于状态回归"}
        return [
            {**common, "receipt_id": "history-unknown", "status": "unknown",
             "observed_at": "2026-10-19T16:00:00+08:00"},
            {**common, "receipt_id": "history-absent", "status": "failed", "submission_absent": True,
             "observed_at": "2026-10-19T08:01:00Z"},
            {**common, "receipt_id": "history-prefill", "status": "pre_filled",
             "observed_at": "2026-10-19T03:02:00-05:00",
             "checks": {"account": True, "title": True, "body": True, "assets": True}},
        ]

    def test_history_six_permutations_import_in_real_time_order(self):
        history = self.recovery_history()
        expected = [r["receipt_id"] for r in history]
        ledgers = []
        for index, order in enumerate(permutations(history)):
            with self.subTest(order=[r["receipt_id"] for r in order]):
                self.pack = self.base / ("permutation-" + str(index))
                self.prepare({**self.plan, "existing_receipts": list(order)})
                target = self.target()
                self.assertEqual(target["state"], "pre_filled")
                self.assertEqual([r["receipt_id"] for r in target["receipts"]], expected)
                self.assertEqual(target["current_receipt"], history[-1])
                ledgers.append((self.pack / LEDGER).read_bytes())
        self.assertTrue(all(ledger == ledgers[0] for ledger in ledgers))

    def test_reordered_history_reuses_pack_and_preserves_appended_acceptance(self):
        history = self.recovery_history()
        self.prepare({**self.plan, "existing_receipts": history})
        self.record(self.receipt("submitted"))
        protected = [self.pack / name for name in (LEDGER, "回执状态表.md", "平台稿件及素材清单.md")]
        before = {p: p.read_bytes() for p in protected}
        for order in permutations(history):
            self.assertTrue(self.prepare({**self.plan, "existing_receipts": list(order)})["reused"])
            self.assertEqual({p: p.read_bytes() for p in protected}, before)
        self.begin(error="ALREADY_ACCEPTED")

    def test_history_dict_time_and_native_id_errors_never_write_pack(self):
        history = self.recovery_history()
        invalid = [(value, "INVALID_FIELD") for value in (None, [], 123, True, "receipt")]
        invalid += [({**history[0], "observed_at": value}, "INVALID_TIME")
                    for value in (None, [], {}, 123, True, "2026-10-19", "not-time")]
        invalid += [({**history[0], "native_id": value}, "INVALID_FIELD")
                    for value in (123, True, [], {}, " ")]
        invalid += [({**history[0], "unexpected": "untrusted"}, "UNKNOWN_FIELD")]
        for index, (receipt, error) in enumerate(invalid):
            with self.subTest(receipt=receipt):
                path = self.input / ("invalid-history-" + str(index) + ".json")
                path.write_text(json.dumps({**self.plan, "existing_receipts": [receipt, *history[1:]]}), encoding="utf-8")
                self.call("prepare", "--input", path, "--out", self.pack, error=error)
                self.assertFalse(self.pack.exists())
                self.assertEqual(list(self.base.glob(".handoff-build-*")), [])
        self.prepare({**self.plan, "existing_receipts": history})
        before = (self.pack / LEDGER).read_bytes()
        for receipt, error in invalid:
            path = self.input / "invalid-existing-pack.json"
            path.write_text(json.dumps({**self.plan, "existing_receipts": [receipt, *history[1:]]}), encoding="utf-8")
            self.call("prepare", "--input", path, "--out", self.pack, error=error)
            self.assertEqual((self.pack / LEDGER).read_bytes(), before)

    def test_equal_history_times_keep_explicit_order_without_recovery_rank(self):
        history = self.recovery_history()
        unknown, prefill = history[0], {**history[2], "observed_at": history[0]["observed_at"]}
        self.prepare({**self.plan, "existing_receipts": [unknown, prefill]})
        self.assertEqual(self.target()["state"], "pre_filled")
        self.assertEqual([r["receipt_id"] for r in self.target()["receipts"]],
                         [unknown["receipt_id"], prefill["receipt_id"]])
        self.begin(error="READBACK_REQUIRED")
        self.pack = self.base / "reverse-equal-times"
        self.prepare({**self.plan, "existing_receipts": [prefill, unknown]})
        self.assertEqual(self.target()["state"], "unknown")
        self.assertEqual([r["receipt_id"] for r in self.target()["receipts"]],
                         [prefill["receipt_id"], unknown["receipt_id"]])
        self.begin(error="READBACK_REQUIRED")

    def test_export_import_late_unresolved_facts_preserves_display_and_action_guards(self):
        for state in ("unknown", "failed"):
            with self.subTest(state=state):
                self.pack = self.base / ("original-late-" + state)
                self.prepare(self.plan)
                origin = datetime.now(timezone.utc) - timedelta(minutes=30)
                self.record(self.receipt("pre_filled", observed_at=(origin + timedelta(minutes=10)).isoformat()))
                self.record(self.receipt(state, observed_at=(origin + timedelta(minutes=5)).isoformat()))
                old = copy.deepcopy(self.target())
                history = self.exported_history_plan()
                self.pack = self.base / ("imported-late-" + state)
                self.prepare(history)
                new = self.target()
                for key in ("state", "state_at", "current_receipt", "intents", "authorization", "authorization_history"):
                    self.assertEqual(new[key], old[key], key)
                self.assertEqual({r["receipt_id"]: r for r in new["receipts"]},
                                 {r["receipt_id"]: r for r in old["receipts"]})
                before = (self.pack / LEDGER).read_bytes()
                self.begin(error="READBACK_REQUIRED")
                self.record(self.receipt("pre_filled"), error="READBACK_REQUIRED")
                self.assertEqual((self.pack / LEDGER).read_bytes(), before)

    def test_export_import_late_unknown_keeps_actual_intent_identity(self):
        self.prepare()
        self.record(self.receipt("pre_filled"))
        first = self.begin()
        self.record(self.receipt("unknown", observed_at=(datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()))
        old = copy.deepcopy(self.target())
        history = self.exported_history_plan()
        self.pack = self.base / "late-unknown-with-intent-imported"
        self.prepare(history)
        self.assertEqual(self.target()["intents"], old["intents"])
        self.assertEqual(self.target()["current_receipt"], old["current_receipt"])
        self.assertEqual(self.target()["state"], old["state"])
        self.assertEqual(self.target()["intents"][0]["id"], first["intent_id"])
        self.begin(error="READBACK_REQUIRED")

    def test_export_import_late_acceptance_preserves_permanent_protection(self):
        self.prepare()
        self.record(self.receipt("pre_filled"))
        self.record(self.receipt("submitted", observed_at=(datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()))
        old = copy.deepcopy(self.target())
        history = self.exported_history_plan()
        self.pack = self.base / "late-acceptance-imported"
        self.prepare(history)
        self.assertEqual(self.target()["state"], old["state"])
        self.assertEqual(self.target()["current_receipt"], old["current_receipt"])
        self.assertEqual(self.target()["intents"], [])
        self.begin(error="ALREADY_ACCEPTED")

    def test_manual_pack_preserves_body_assets_and_review(self):
        original = (self.input / "tutorial.md").read_bytes()
        self.prepare()
        self.assertEqual(len(self.ledger()["targets"]), 2)
        for t in self.ledger()["targets"]:
            d = self.pack / "targets" / t["id"]
            self.assertEqual((d / "body.md").read_bytes(), original)
            self.assertEqual((d / "assets/cache-checklist.csv").read_bytes(), (self.input / "assets/cache-checklist.csv").read_bytes())
            meta = json.loads((d / "metadata.json").read_text())
            self.assertEqual(meta["account_id"], t["account_id"])
            self.assertEqual(meta["fields"], t["fields"])
        self.assertEqual(self.target("zhihu")["state"], "under_review")
        self.assertEqual(self.target()["state"], "ready")
        self.assertEqual((self.input / "tutorial.md").read_bytes(), original)
        self.assertTrue(original.endswith(b"\n"))

    def test_repeated_prepare_preserves_appended_history(self):
        self.prepare()
        self.record(self.receipt("submitted"))
        saved = (self.pack / LEDGER).read_bytes()
        self.assertTrue(self.prepare()["reused"])
        self.assertEqual((self.pack / LEDGER).read_bytes(), saved)

    def test_duplicate_target_collapses_and_distinct_account_remains(self):
        p = copy.deepcopy(self.plan)
        p["targets"].append(copy.deepcopy(p["targets"][1]))
        other = copy.deepcopy(p["targets"][1])
        other["account_id"] = "another-csdn-account"
        other["authorization"]["account_id"] = other["account_id"]
        p["targets"].append(other)
        self.prepare(p)
        self.assertEqual(len(self.ledger()["targets"]), 3)

    def test_title_change_cannot_bypass_same_draft_dedup(self):
        p = copy.deepcopy(self.plan)
        other = copy.deepcopy(p["targets"][1])
        other["title"] = "换个标题仍是同稿"
        p["targets"].append(other)
        self.plan_path.write_text(json.dumps(p))
        self.call("prepare", "--input", self.plan_path, "--out", self.pack, error="DUPLICATE_TARGET_CONFLICT")
        self.assertFalse(self.pack.exists())

    def test_review_never_retries(self):
        self.prepare()
        self.call("intent", "--pack", self.pack, "--target", self.target("zhihu")["id"], error="ALREADY_ACCEPTED")
        self.assertEqual(self.target("zhihu")["state"], "under_review")

    def test_submission_requires_observed_prefill_and_scoped_authorization(self):
        self.prepare()
        self.begin(error="READBACK_REQUIRED")
        self.record(self.receipt("pre_filled", mode="user_report"))
        self.begin(error="READBACK_REQUIRED")
        self.record(self.receipt("pre_filled"))
        self.begin(error="SUBMIT_NOT_AUTHORIZED", auth=False)
        result = self.begin()
        self.assertEqual(result["state"], "unknown")
        self.assertEqual(len(self.target()["intents"]), 1)
        self.begin(error="READBACK_REQUIRED")
        self.assertEqual(len(self.target()["intents"]), 1)

    def test_prefill_must_verify_all_fields(self):
        self.prepare()
        r = self.receipt("pre_filled")
        r["checks"]["body"] = False
        self.record(r, error="PREFILL_NOT_VERIFIED")
        self.assertEqual(self.target()["state"], "ready")
        r["checks"]["body"] = 1
        self.record(r, error="PREFILL_NOT_VERIFIED")

    def test_wrong_scope_and_expired_authorization_stop_intent(self):
        self.prepare()
        self.record(self.receipt("pre_filled"))
        for extra, error in [({"account_id": "someone-else"}, "AUTHORIZATION_SCOPE"),
                             ({"valid_until": "2000-01-01T00:00:00Z"}, "AUTHORIZATION_EXPIRED")]:
            self.call("intent", "--pack", self.pack, "--target", self.target()["id"],
                      "--authorization", self.grant(**extra), error=error)
        self.assertEqual(self.target()["intents"], [])

    def test_simulated_unrun_and_query_failure_do_not_change_unknown(self):
        self.prepare()
        self.record(self.receipt("pre_filled"))
        self.begin()
        self.record(self.receipt("public", mode="simulated", public_url="https://example.invalid/demo"))
        self.record(self.receipt(None, mode="not_run"))
        self.record(self.receipt(None, mode="query_failed"))
        self.assertEqual(self.target()["state"], "unknown")
        self.assertEqual([r["mode"] for r in self.target()["receipts"][-3:]], ["simulated", "not_run", "query_failed"])
        self.begin(error="READBACK_REQUIRED")
        self.record(self.receipt("public", mode="query_failed"), error="INVALID_RECEIPT")

    def test_query_failed_does_not_replace_accepted_state(self):
        self.prepare()
        self.record(self.receipt("under_review"))
        self.record(self.receipt(None, mode="query_failed"))
        self.assertEqual(self.target()["state"], "under_review")
        self.begin(error="ALREADY_ACCEPTED")

    def test_zero_submission_proof_bound_to_latest_intent_allows_repair(self):
        self.prepare()
        self.record(self.receipt("pre_filled"))
        first = self.begin()
        self.record(self.receipt("failed", submission_absent=True), error="INTENT_MISMATCH")
        self.record(self.receipt("failed", submission_absent=True, intent_id=first["intent_id"]))
        self.begin(error="READBACK_REQUIRED")
        self.record(self.receipt("pre_filled"))
        second = self.begin(auth=False)  # Saved authorization remains scoped; do not ask again.
        self.assertNotEqual(first["intent_id"], second["intent_id"])
        self.assertEqual(len(self.target()["intents"]), 2)
        self.record(self.receipt("failed", submission_absent=True, intent_id=first["intent_id"]), error="INTENT_MISMATCH")

    def test_failure_without_zero_submission_evidence_never_retries(self):
        self.prepare()
        self.record(self.receipt("failed"))
        self.record(self.receipt("pre_filled"), error="READBACK_REQUIRED")
        self.begin(error="READBACK_REQUIRED")

    def test_accepted_then_rejected_still_never_retries(self):
        self.prepare()
        self.record(self.receipt("submitted"))
        self.record(self.receipt("failed", evidence="合成记录：审核未通过"))
        self.begin(error="ALREADY_ACCEPTED")
        self.record(self.receipt("failed", submission_absent=True), error="ACCEPTED_PROTECTED")

    def test_public_needs_native_id_real_url_and_verified_flag(self):
        self.prepare()
        self.record(self.receipt("public"), error="INVALID_URL")
        self.record(self.receipt("public", public_url="https://example.invalid/demo"), error="PUBLIC_NOT_VERIFIED")
        self.record(self.receipt("public", public_url="javascript:alert(1)", public_verified=True), error="INVALID_URL")
        self.record(self.receipt("public", public_url="https://example.invalid/demo", public_verified=True))
        self.assertEqual(self.target()["state"], "public")
        self.record(self.receipt("unknown"), error="PUBLIC_PROTECTED")
        self.begin(error="ALREADY_ACCEPTED")

    def test_public_user_report_is_history_without_losing_verified_link(self):
        self.prepare()
        verified = self.receipt("public", public_url="https://example.invalid/verified", public_verified=True)
        self.record(verified)
        before = self.target()
        for extra in ({}, {"public_url": "https://example.invalid/unverified", "public_verified": True}):
            reported = self.receipt("public", mode="user_report", **extra)
            result = self.record(reported)
            self.assertFalse(result["applied"])
            self.assertEqual(self.target()["current_receipt"], verified)
            self.assertEqual(self.target()["state_at"], before["state_at"])
            self.assertEqual(self.target()["receipts"][-1], reported)
            self.assertTrue(self.record(reported)["duplicate"])
        report = (self.pack / "回执状态表.md").read_text()
        row = next(line for line in report.splitlines() if line.startswith("| CSDN /"))
        self.assertIn("已公开（回读记录）", row)
        self.assertIn("https://example.invalid/verified", row)
        self.assertNotIn("未取得公开链接", row)
        newer_verified = self.receipt("public", public_url="https://example.invalid/new-verified", public_verified=True)
        self.record(newer_verified)
        self.assertEqual(self.target()["current_receipt"], newer_verified)
        self.begin(error="ALREADY_ACCEPTED")

    def exported_history_plan(self):
        old = self.ledger()
        return {**self.plan,
                "existing_intents": [copy.deepcopy(i) for t in old["targets"] for i in t["intents"]],
                "existing_receipts": [copy.deepcopy(r) for t in old["targets"] for r in t["receipts"]]}

    def test_import_actual_intents_and_zero_receipts_preserves_scope_and_no_new_grant(self):
        self.prepare()
        self.record(self.receipt("pre_filled"))
        old_intent = self.begin()
        self.record(self.receipt("failed", submission_absent=True, intent_id=old_intent["intent_id"]))
        self.record(self.receipt("pre_filled"))
        history = self.exported_history_plan()
        self.pack = self.base / "imported"
        self.prepare(history)
        self.assertEqual(self.target()["intents"], history["existing_intents"])
        self.assertEqual(self.target()["state"], "pre_filled")
        self.assertEqual(self.target()["authorization"]["action"], "prepare")
        self.begin(auth=False, error="SUBMIT_NOT_AUTHORIZED")
        fresh = self.begin()
        self.assertNotEqual(fresh["intent_id"], old_intent["intent_id"])
        self.begin(error="READBACK_REQUIRED")

    def test_import_unresolved_intent_without_receipt_stays_unknown(self):
        self.prepare()
        self.record(self.receipt("pre_filled"))
        self.begin()
        history = self.exported_history_plan()
        self.pack = self.base / "imported"
        self.prepare(history)
        self.assertEqual(self.target()["state"], "unknown")
        self.begin(error="READBACK_REQUIRED")
        self.record(self.receipt("pre_filled"), error="READBACK_REQUIRED")

    def sequential_intent_history(self):
        target = self.plan["targets"][1]
        auth = {**target["authorization"], "action": "submit", "reference": "合成旧台账授权，不授权真实投稿"}
        first = {"id": "historical-A", "created_at": "2026-10-18T08:00:00Z",
                 "draft_sha256": auth["draft_sha256"], "authorization": auth}
        second = {**first, "id": "historical-B", "created_at": "2026-10-18T08:02:00Z"}
        zero = {"receipt_id": "historical-A-zero", "platform": target["platform"], "account_id": target["account_id"],
                "draft_sha256": auth["draft_sha256"], "mode": "observed", "status": "failed",
                "observed_at": "2026-10-18T08:01:00Z", "intent_id": first["id"], "submission_absent": True,
                "source": "合成历史回归", "evidence": "合成零提交证明，未访问任何平台"}
        return first, second, zero

    def test_overlapping_history_rejected_even_if_only_second_intent_has_zero_proof(self):
        first, second, zero = self.sequential_intent_history()
        zero = {**zero, "receipt_id": "B-zero", "intent_id": second["id"], "observed_at": "2026-10-18T08:03:00Z"}
        prefill = {**zero, "receipt_id": "B-prefill", "status": "pre_filled", "observed_at": "2026-10-18T08:04:00Z",
                   "checks": {"account": True, "title": True, "body": True, "assets": True}}
        prefill.pop("submission_absent")
        plan = {**self.plan, "existing_intents": [first, second], "existing_receipts": [zero, prefill]}
        self.plan_path.write_text(json.dumps(plan), encoding="utf-8")
        self.call("prepare", "--input", self.plan_path, "--out", self.pack, error="OVERLAPPING_INTENTS")
        self.assertFalse(self.pack.exists())
        self.assertEqual(list(self.base.glob(".handoff-build-*")), [])
        self.prepare(self.plan)
        before = (self.pack / LEDGER).read_bytes()
        self.plan_path.write_text(json.dumps(plan), encoding="utf-8")
        self.call("prepare", "--input", self.plan_path, "--out", self.pack, error="OVERLAPPING_INTENTS")
        self.assertEqual((self.pack / LEDGER).read_bytes(), before)

    def test_prior_zero_proof_admits_second_intent_but_preserves_its_protection(self):
        first, second, zero = self.sequential_intent_history()
        self.prepare({**self.plan, "existing_intents": [second, first], "existing_receipts": [zero]})
        self.assertEqual([i["id"] for i in self.target()["intents"]], [first["id"], second["id"]])
        self.assertEqual(self.target()["state"], "unknown")
        self.begin(error="READBACK_REQUIRED")
        self.record(self.receipt("pre_filled"), error="READBACK_REQUIRED")
        self.record(self.receipt("failed", submission_absent=True, intent_id=second["id"]))
        self.record(self.receipt("pre_filled"))
        current = self.begin()
        self.assertNotIn(current["intent_id"], (first["id"], second["id"]))
        self.assertEqual(len(self.target()["intents"]), 3)
        self.begin(error="READBACK_REQUIRED")

    def test_ambiguous_or_untrusted_zero_cannot_admit_second_history_intent(self):
        first, second, zero = self.sequential_intent_history()
        variants = [{**zero, "observed_at": second["created_at"]},
                    {**zero, "mode": "user_report"},
                    {**zero, "intent_id": second["id"]},
                    {**zero, "submission_absent": False}]
        for index, receipt in enumerate(variants):
            with self.subTest(receipt=receipt):
                self.pack = self.base / ("rejected-overlap-" + str(index))
                self.plan_path.write_text(json.dumps({**self.plan, "existing_intents": [first, second],
                                                     "existing_receipts": [receipt]}), encoding="utf-8")
                self.call("prepare", "--input", self.plan_path, "--out", self.pack, error="OVERLAPPING_INTENTS")
                self.assertFalse(self.pack.exists())

    def test_import_backdated_receipt_keeps_later_actual_intent_unresolved(self):
        self.prepare()
        self.record(self.receipt("pre_filled"))
        old_intent = self.begin()
        before_intent = (datetime.now(timezone.utc) - timedelta(minutes=1)).isoformat()
        self.record(self.receipt("failed", observed_at=before_intent, submission_absent=True,
                                 intent_id=old_intent["intent_id"]))
        history = self.exported_history_plan()
        self.pack = self.base / "imported"
        self.prepare(history)
        self.assertEqual(self.target()["state"], "unknown")
        self.assertEqual(self.target()["intents"], history["existing_intents"])
        self.begin(error="READBACK_REQUIRED")

    def test_bundled_history_import_has_no_current_submit_authorization(self):
        history = json.loads((self.input / "history-plan.json").read_text())
        self.prepare(history)
        self.assertEqual(self.target()["state"], "pre_filled")
        self.assertEqual(self.target()["intents"], history["existing_intents"])
        self.begin(auth=False, error="SUBMIT_NOT_AUTHORIZED")
        self.assertEqual(self.target("zhihu")["state"], "under_review")

    def test_import_submitted_receipt_with_intent_keeps_permanent_protection(self):
        self.prepare()
        self.record(self.receipt("pre_filled"))
        old_intent = self.begin()
        self.record(self.receipt("submitted", intent_id=old_intent["intent_id"]))
        history = self.exported_history_plan()
        self.pack = self.base / "imported"
        self.prepare(history)
        self.assertEqual(self.target()["state"], "submitted")
        self.begin(error="ALREADY_ACCEPTED")
        self.record(self.receipt("failed", submission_absent=True,
                                 intent_id=old_intent["intent_id"]), error="ACCEPTED_PROTECTED")

    def test_reordered_intent_history_reuses_without_dropping_appended_receipts(self):
        self.prepare()
        self.record(self.receipt("pre_filled"))
        first = self.begin()
        self.record(self.receipt("failed", submission_absent=True, intent_id=first["intent_id"]))
        self.record(self.receipt("pre_filled"))
        self.begin()
        history = self.exported_history_plan()
        self.pack = self.base / "imported"
        self.prepare(history)
        self.record(self.receipt("submitted"))
        before = (self.pack / LEDGER).read_bytes()
        history["existing_intents"].reverse()
        history["existing_receipts"].reverse()
        self.assertTrue(self.prepare(history)["reused"])
        self.assertEqual((self.pack / LEDGER).read_bytes(), before)
        self.begin(error="ALREADY_ACCEPTED")

    def test_invalid_intent_import_never_creates_pack(self):
        self.prepare()
        self.record(self.receipt("pre_filled"))
        old_intent = self.begin()
        self.record(self.receipt("failed", submission_absent=True, intent_id=old_intent["intent_id"]))
        history = self.exported_history_plan()
        original = history["existing_intents"][0]
        cases = [(None, "INVALID_FIELD"), ({**original, "id": []}, "INVALID_FIELD"),
                 ({**original, "created_at": {}}, "INVALID_TIME"),
                 ({**original, "draft_sha256": "wrong"}, "VERSION_MISMATCH"),
                 ({**original, "authorization": None}, "INVALID_FIELD"),
                 ({**original, "authorization": {**original["authorization"], "account_id": "someone-else"}}, "UNKNOWN_TARGET"),
                 ({**original, "authorization": {**original["authorization"], "draft_sha256": "wrong"}}, "AUTHORIZATION_SCOPE"),
                 ({**original, "authorization": {**original["authorization"], "action": "prepare"}}, "SUBMIT_NOT_AUTHORIZED"),
                 ({**original, "authorization": {**original["authorization"], "valid_until": "2000-01-01T00:00:00Z"}}, "AUTHORIZATION_EXPIRED"),
                 ({**original, "unexpected": True}, "UNKNOWN_FIELD")]
        for index, (entry, error) in enumerate(cases):
            with self.subTest(entry=entry):
                self.pack = self.base / ("invalid-import-" + str(index))
                self.plan_path.write_text(json.dumps({**history, "existing_intents": [entry]}))
                self.call("prepare", "--input", self.plan_path, "--out", self.pack, error=error)
                self.assertFalse(self.pack.exists())
        self.pack = self.base / "missing-import"
        self.plan_path.write_text(json.dumps({**history, "existing_intents": []}))
        self.call("prepare", "--input", self.plan_path, "--out", self.pack, error="INTENT_MISMATCH")
        self.assertFalse(self.pack.exists())
        self.pack = self.base / "conflicting-import"
        conflict = {**original, "created_at": "2001-01-01T00:00:00Z"}
        self.plan_path.write_text(json.dumps({**history, "existing_intents": [original, conflict]}))
        self.call("prepare", "--input", self.plan_path, "--out", self.pack, error="INTENT_CONFLICT")
        self.assertFalse(self.pack.exists())

    def test_invalid_optional_native_id_never_changes_pack(self):
        for status in ("unknown", "failed", "pre_filled"):
            with self.subTest(status=status):
                self.pack = self.base / status
                self.prepare()
                files = [self.pack / name for name in (LEDGER, "回执状态表.md", "平台稿件及素材清单.md")]
                before = {p: p.read_bytes() for p in files}
                self.record(self.receipt(status, native_id=123), error="INVALID_FIELD")
                self.assertEqual({p: p.read_bytes() for p in files}, before)
                result = self.call("report", "--pack", self.pack)
                self.assertEqual([t["state"] for t in result["targets"]], ["under_review", "ready"])
                self.assertEqual({p: p.read_bytes() for p in files}, before)

    def test_native_id_validation_covers_every_mode_state_and_type(self):
        self.prepare()
        before = (self.pack / LEDGER).read_bytes()
        for mode in ("observed", "user_report", "simulated", "not_run", "query_failed"):
            statuses = (None,) if mode in {"not_run", "query_failed"} else (
                "pre_filled", "submitted", "under_review", "public", "unknown", "failed")
            for status in statuses:
                with self.subTest(mode=mode, status=status):
                    r = self.receipt(status, mode=mode, native_id=123)
                    if status == "public":
                        r.update(public_url="https://example.invalid/demo", public_verified=True)
                    self.record(r, error="INVALID_FIELD")
                    self.assertEqual((self.pack / LEDGER).read_bytes(), before)
        for value in (0, True, False, 1.5, [], ["native-1"], {}, {"id": 123}, "", " \t"):
            with self.subTest(native_id=value):
                self.record(self.receipt("unknown", native_id=value), error="INVALID_FIELD")
                self.assertEqual((self.pack / LEDGER).read_bytes(), before)
        self.call("report", "--pack", self.pack)

    def test_optional_native_id_preserves_valid_values_and_required_ids(self):
        for status in ("pre_filled", "failed", "unknown"):
            for index, extra in enumerate(({}, {"native_id": None}, {"native_id": "00123"})):
                with self.subTest(status=status, extra=extra):
                    self.pack = self.base / (status + "-" + str(index))
                    self.prepare()
                    r = self.receipt(status, **extra)
                    self.assertEqual(self.record(r)["state"], status)
                    self.assertEqual(self.target()["current_receipt"], r)
                    self.assertEqual(self.target()["receipts"], [r])
                    result = self.call("report", "--pack", self.pack)
                    self.assertEqual(result["targets"][1]["state"], status)
                    expected_id = extra.get("native_id") or "无原生 ID"
                    self.assertIn(expected_id + " / 未取得公开链接", (self.pack / "回执状态表.md").read_text())
        before = (self.pack / LEDGER).read_bytes()
        for mode in ("observed", "user_report"):
            for status in ("submitted", "under_review", "public"):
                for absent in (True, False):
                    with self.subTest(mode=mode, status=status, absent=absent):
                        r = self.receipt(status, mode=mode, native_id=None)
                        if absent:
                            r.pop("native_id")
                        self.record(r, error="INVALID_FIELD")
                        self.assertEqual((self.pack / LEDGER).read_bytes(), before)

    def test_prepare_rejects_invalid_optional_native_id_without_output(self):
        for status in ("unknown", "failed", "pre_filled"):
            with self.subTest(status=status):
                p = copy.deepcopy(self.plan)
                r = p["existing_receipts"][0]
                r.update(status=status, native_id=123)
                if status == "pre_filled":
                    r["checks"] = {"account": True, "title": True, "body": True, "assets": True}
                self.plan_path.write_text(json.dumps(p, ensure_ascii=False), encoding="utf-8")
                self.call("prepare", "--input", self.plan_path, "--out", self.pack, error="INVALID_FIELD")
                self.assertFalse(self.pack.exists())
                self.assertEqual(list(self.base.glob(".handoff-build-*")), [])

    def test_receipt_idempotent_and_conflict_never_overwrites(self):
        self.prepare()
        r = self.receipt("submitted")
        self.record(r)
        saved = (self.pack / LEDGER).read_bytes()
        self.assertTrue(self.record(r)["duplicate"])
        self.assertEqual((self.pack / LEDGER).read_bytes(), saved)
        self.record({**r, "evidence": "不同内容"}, error="RECEIPT_CONFLICT")
        self.assertEqual((self.pack / LEDGER).read_bytes(), saved)

    def test_wrong_account_or_version_never_leaks_into_another_target(self):
        self.prepare()
        self.record(self.receipt("submitted", draft_sha256="0" * 64), error="VERSION_MISMATCH")
        self.record(self.receipt("submitted", account_id="unrelated"), error="UNKNOWN_TARGET")
        self.assertEqual(self.target()["state"], "ready")

    def test_stale_status_does_not_regress_but_historic_acceptance_protects(self):
        self.prepare()
        self.record(self.receipt("pre_filled"))
        self.record(self.receipt("submitted", observed_at="2020-01-01T00:00:00Z"))
        self.assertEqual(self.target()["state"], "pre_filled")
        self.begin(error="ALREADY_ACCEPTED")

    def late_history(self):
        origin = datetime.now(timezone.utc) - timedelta(minutes=30)
        self.record(self.receipt("pre_filled", observed_at=(origin + timedelta(minutes=10)).isoformat()))
        self.record(self.receipt("unknown", observed_at=(origin + timedelta(minutes=5)).isoformat()))
        self.assertEqual(self.target()["state"], "pre_filled")
        return origin

    def test_late_unknown_blocks_valid_authorization_and_fresh_prefill(self):
        self.prepare()
        self.late_history()
        before = (self.pack / LEDGER).read_bytes()
        self.begin(error="READBACK_REQUIRED")
        self.assertEqual((self.pack / LEDGER).read_bytes(), before)
        self.record(self.receipt("pre_filled"), error="READBACK_REQUIRED")
        self.assertEqual((self.pack / LEDGER).read_bytes(), before)
        report = self.call("report", "--pack", self.pack)
        target = next(t for t in report["targets"] if t["platform"] == "csdn")
        self.assertIn("先回读", target["next_action"])
        self.assertEqual(self.target()["intents"], [])

    def test_late_observed_zero_proof_between_unknown_and_prefill_restores_intent(self):
        self.prepare()
        origin = self.late_history()
        self.record(self.receipt("failed", submission_absent=True,
            observed_at=(origin + timedelta(minutes=7)).isoformat()))
        self.assertEqual(self.target()["state"], "pre_filled")
        self.begin()
        self.assertEqual(len(self.target()["intents"]), 1)
        self.begin(error="READBACK_REQUIRED")

    def test_backdated_zero_proof_cannot_clear_actual_later_intent(self):
        self.prepare()
        origin = self.late_history()
        self.record(self.receipt("failed", submission_absent=True,
            observed_at=(origin + timedelta(minutes=7)).isoformat()))
        first = self.begin()
        self.record(self.receipt("failed", submission_absent=True, intent_id=first["intent_id"],
            observed_at=(origin + timedelta(minutes=8)).isoformat()))
        self.begin(error="READBACK_REQUIRED")
        self.record(self.receipt("pre_filled"), error="READBACK_REQUIRED")
        self.assertEqual(len(self.target()["intents"]), 1)
        self.record(self.receipt("failed", submission_absent=True), error="INTENT_MISMATCH")
        self.record(self.receipt("failed", submission_absent=True, intent_id=first["intent_id"]))
        self.record(self.receipt("pre_filled"))
        self.begin(auth=False)
        self.assertEqual(len(self.target()["intents"]), 2)

    def test_untrusted_late_failure_or_simulation_cannot_clear_unknown(self):
        self.prepare()
        origin = self.late_history()
        for mode in ("user_report", "simulated"):
            self.record(self.receipt("failed", mode=mode, submission_absent=True,
                observed_at=(origin + timedelta(minutes=7)).isoformat()))
            self.begin(error="READBACK_REQUIRED")
        self.record(self.receipt("failed", observed_at=(origin + timedelta(minutes=8)).isoformat()))
        self.begin(error="READBACK_REQUIRED")
        self.assertEqual(self.target()["intents"], [])

    def test_late_unknown_after_prior_zero_proof_requires_newer_zero_proof(self):
        self.prepare()
        origin = self.late_history()
        self.record(self.receipt("failed", submission_absent=True,
            observed_at=(origin + timedelta(minutes=7)).isoformat()))
        self.record(self.receipt("unknown", observed_at=(origin + timedelta(minutes=9)).isoformat()))
        self.begin(error="READBACK_REQUIRED")
        self.record(self.receipt("failed", submission_absent=True,
            observed_at=(origin + timedelta(minutes=9, seconds=30)).isoformat()))
        self.begin()
        self.assertEqual(len(self.target()["intents"]), 1)

    def test_late_unknown_in_another_account_does_not_block_this_target(self):
        self.prepare()
        origin = datetime.now(timezone.utc) - timedelta(minutes=30)
        self.record(self.receipt("pre_filled"))
        self.record(self.receipt("unknown", platform="zhihu", account_id="example-zhihu-editor",
            observed_at=origin.isoformat()))
        self.begin()
        self.assertEqual(len(self.target()["intents"]), 1)
        self.call("intent", "--pack", self.pack, "--target", self.target("zhihu")["id"], error="ALREADY_ACCEPTED")

    def test_late_old_attempt_is_not_cleared_by_another_attempt_zero_proof(self):
        for index, (state, bound) in enumerate((("unknown", True), ("unknown", False), ("failed", True), ("failed", False))):
            with self.subTest(state=state, bound=bound):
                self.pack = self.base / ("separate-obligations-" + str(index))
                self.prepare(self.plan)
                self.record(self.receipt("pre_filled"))
                first = self.begin()
                zero = self.receipt("failed", submission_absent=True, intent_id=first["intent_id"])
                self.record(zero)
                self.record(self.receipt("pre_filled"))
                second = self.begin()
                start = datetime.fromisoformat(zero["observed_at"])
                end = datetime.fromisoformat(self.target()["intents"][-1]["created_at"])
                extra = {"intent_id": first["intent_id"]} if bound else {}
                self.record(self.receipt(state, observed_at=(start + (end - start) / 2).isoformat(), **extra))
                self.record(self.receipt("failed", submission_absent=True, intent_id=second["intent_id"]))
                self.begin(error="READBACK_REQUIRED")
                self.record(self.receipt("pre_filled"), error="READBACK_REQUIRED")
                old = copy.deepcopy(self.target())
                history = self.exported_history_plan()
                self.pack = self.base / ("restored-separate-obligations-" + str(index))
                self.prepare(history)
                self.assertEqual(self.target()["intents"], old["intents"])
                self.assertEqual({r["receipt_id"]: r for r in self.target()["receipts"]},
                                 {r["receipt_id"]: r for r in old["receipts"]})
                self.begin(error="READBACK_REQUIRED")
                self.record(self.receipt("failed", submission_absent=True, intent_id=first["intent_id"]))
                self.record(self.receipt("pre_filled"))
                third = self.begin()
                self.assertNotIn(third["intent_id"], (first["intent_id"], second["intent_id"]))
                self.begin(error="READBACK_REQUIRED")

    def test_unscoped_late_uncertainty_needs_its_own_zero_proof(self):
        self.prepare()
        self.record(self.receipt("pre_filled"))
        first = self.begin()
        self.record(self.receipt("unknown", observed_at=(datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()))
        self.record(self.receipt("failed", submission_absent=True, intent_id=first["intent_id"]))
        self.begin(error="READBACK_REQUIRED")
        self.record(self.receipt("pre_filled"), error="READBACK_REQUIRED")
        self.record(self.receipt("failed", submission_absent=True))
        self.record(self.receipt("pre_filled"))
        self.begin()
        self.begin(error="READBACK_REQUIRED")

    def test_history_replay_keeps_verified_public_over_later_lower_states(self):
        self.prepare(self.plan)
        for index, state in enumerate(("unknown", "failed", "pre_filled", "public")):
            with self.subTest(state=state):
                verified = self.receipt("public", observed_at="2026-10-18T10:00:00Z",
                    public_url="https://example.invalid/known-verified", public_verified=True)
                later = self.receipt(state, observed_at="2026-10-18T11:00:00Z",
                                     mode="user_report" if state == "public" else "observed")
                self.pack = self.base / ("public-protected-replay-" + str(index))
                self.prepare({**self.plan, "existing_receipts": [later, verified]})
                self.assertEqual(self.target()["state"], "public")
                self.assertEqual(self.target()["current_receipt"], verified)
                self.assertEqual(self.target()["receipts"], [verified, later])
                self.begin(error="ALREADY_ACCEPTED")
                self.record(self.receipt("unknown"), error="PUBLIC_PROTECTED")
                self.call("report", "--pack", self.pack)
                self.assertIn(verified["public_url"], (self.pack / "回执状态表.md").read_text())
                newer = self.receipt("public", public_url="https://example.invalid/newer-verified", public_verified=True)
                self.record(newer)
                self.assertEqual(self.target()["current_receipt"], newer)

    def test_changed_body_asset_or_metadata_blocks_all_next_actions(self):
        self.prepare()
        base = self.pack / "targets" / self.target()["id"]
        for file in [base / "body.md", base / "metadata.json", base / "assets/cache-checklist.csv", self.pack / "source/body.md"]:
            data = file.read_bytes()
            file.write_bytes(data + b"changed")
            self.call("report", "--pack", self.pack, error="CONTENT_CHANGED")
            file.write_bytes(data)

    def test_changed_plan_cannot_reset_ledger(self):
        self.prepare()
        before = (self.pack / LEDGER).read_bytes()
        p = copy.deepcopy(self.plan)
        p["draft"]["version"] = "v2"
        self.plan_path.write_text(json.dumps(p))
        self.call("prepare", "--input", self.plan_path, "--out", self.pack, error="PLAN_CHANGED")
        self.assertEqual((self.pack / LEDGER).read_bytes(), before)

    def test_missing_asset_empty_targets_and_unsafe_paths_leave_no_pack(self):
        for mutate, error in [
            (lambda p: p["assets"][0].update(file="assets/missing.csv"), "MISSING_FILE"),
            (lambda p: p.update(targets=[]), "EMPTY_TARGETS"),
            (lambda p: p["draft"].update(body_file="../outside.md"), "UNSAFE_PATH"),
            (lambda p: p["assets"][0].update(file="assets/../../outside.csv"), "UNSAFE_PATH")]:
            p = copy.deepcopy(self.plan)
            mutate(p)
            self.plan_path.write_text(json.dumps(p))
            self.call("prepare", "--input", self.plan_path, "--out", self.pack, error=error)
            self.assertFalse(self.pack.exists())

    def test_symlink_escape_is_not_read(self):
        outside = self.base / "outside.csv"
        outside.write_text("not-an-input")
        asset = self.input / "assets/cache-checklist.csv"
        asset.unlink()
        try:
            asset.symlink_to(outside)
        except (OSError, NotImplementedError):
            self.skipTest("此文件系统不支持符号链接")
        self.call("prepare", "--input", self.plan_path, "--out", self.pack, error="UNSAFE_PATH")

    def test_pack_and_script_work_after_relocation(self):
        self.prepare()
        moved = self.base / "moved" / "bundle"
        moved.parent.mkdir()
        shutil.move(self.pack, moved)
        isolated_script = self.base / "isolated.py"
        isolated_script.write_bytes(CLI.read_bytes())
        result = self.call("report", "--pack", moved, cli=isolated_script)
        self.assertEqual([t["state"] for t in result["targets"]], ["under_review", "ready"])

    def test_concurrent_intents_have_one_winner(self):
        self.prepare()
        self.record(self.receipt("pre_filled"))
        args = [sys.executable, str(CLI), "intent", "--pack", str(self.pack), "--target", self.target()["id"],
                "--authorization", str(self.grant())]
        processes = [subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for _ in range(2)]
        results = [(p, p.communicate(timeout=20)) for p in processes]
        self.assertEqual(sorted(p.returncode for p, _ in results), [0, 2], results)
        self.assertEqual(len(self.target()["intents"]), 1)
        self.assertEqual(self.target()["state"], "unknown")

    def test_lock_is_not_silently_removed(self):
        self.prepare()
        path = self.pack / ".handoff.lock"
        path.write_text("synthetic-owner")
        self.call("report", "--pack", self.pack, error="PACK_BUSY")
        self.assertEqual(path.read_text(), "synthetic-owner")

    def test_failure_example_keeps_unknown_and_blocks_submission(self):
        self.prepare()
        result = self.call("record", "--pack", self.pack, "--receipt", ROOT / "examples/failure/unknown-receipt.json")
        self.assertEqual(result["state"], "unknown")
        self.begin(error="READBACK_REQUIRED")

    def test_empty_body_invalid_utf8_and_duplicate_json_fields_fail(self):
        for body, error in [(b" \n", "EMPTY_BODY"), (b"\xff", "INVALID_INPUT_OR_IO")]:
            (self.input / "tutorial.md").write_bytes(body)
            self.call("prepare", "--input", self.plan_path, "--out", self.pack, error=error)
            self.assertFalse(self.pack.exists())
        self.plan_path.write_text('{"schema_version":1,"schema_version":2}')
        self.call("prepare", "--input", self.plan_path, "--out", self.pack, error="DUPLICATE_JSON_KEY")


if __name__ == "__main__":
    unittest.main(verbosity=2)
