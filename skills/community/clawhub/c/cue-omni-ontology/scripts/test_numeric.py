"""Numeric pack tests (stdlib unittest): verbatim validation, schema, credit-causal ordering, normal events, views.
All figures below are SYNTHETIC round numbers chosen to keep the arithmetic relations; they are not any company's data."""
import contextlib, io, json, sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import numeric, ontology

ROW20 = "| 短期借款 | 3,000,000,000.00 | 2,000,000,000.00 |"
ROW19 = "| 短期借款 | 900,000,000.00 | 1,020,000,000.00 |"
P20 = {1: "封面", 5: ROW20 + "\n| 资产总计 | 20,000,000,000.00 | 18,000,000,000.00 |",
       9: "公司于 2020 年发生同一控制下企业合并，对上年数据进行了追溯调整。"}
P19 = {1: "封面", 4: ROW19}


def mk_sources(d):
    s = Path(d) / "src"; s.mkdir()
    for fy, P in ((2020, P20), (2019, P19)):
        (s / f"FY{fy}.pages.jsonl").write_text(
            "\n".join(json.dumps({"page": k, "text": v}, ensure_ascii=False) for k, v in P.items()) + "\n", encoding="utf-8")
    return s


def pt(fy, v, page, ex=None):
    return {"fy": fy, "value": v, "page": page, "table_id": f"FY{fy}:BS:p{page}", **({"excerpt": ex} if ex else {})}


def base_numeric():
    return {"company": "[本公司]", "fy": 2020, "fy_prev": 2019, "unit": "元",
            "scale": {"total_assets": 20000000000.00, "revenue": 8000000000.00, "total_assets_fy_prev_report": 8000000000.00},
            "deltas": [
                {"id": "d1", "item": "短期借款", "period": "latest", "scale_kind": "assets", "unit": "元",
                 "current": pt(2020, 3000000000.00, 5, ROW20), "prior": pt(2020, 2000000000.00, 5, ROW20),
                 "prior_as_originally_reported": pt(2019, 900000000.00, 4, ROW19),
                 "delta": 1000000000.00, "delta_pct": 50.0, "restated": True, "restatement_diff": 1100000000.00, "check_ids": ["c1"]},
                {"id": "d2", "item": "资产总计", "period": "latest", "scale_kind": "assets", "unit": "元",
                 "current": pt(2020, 20000000000.00, 5), "prior": pt(2020, 18000000000.00, 5), "delta": 2000000000.00,
                 "restated": False, "check_ids": []},
                {"id": "d3", "item": "短期借款", "period": "earlier", "scale_kind": "assets", "unit": "元",
                 "current": pt(2019, 900000000.00, 4), "prior": pt(2019, 1020000000.00, 4), "delta": -120000000.00, "check_ids": []}],
            "checks": [{"id": "c1", "check": "note_ties_to_statement", "item": "短期借款", "ok": False, "page": 5, "table_id": "x", "detail": {}}],
            "flags": [{"flag": "担保总额占净资产比例", "fy": 2020, "value_pct": 45.0, "page": 5, "table_id": "g"}],
            "restatements": [{"delta_id": "d1"}]}


def narrative():
    return {"items": [{"id": "n1", "fy": 2020, "page": 9, "type": "other", "quote": "同一控制下企业合并，对上年数据进行了追溯调整"}]}


def write(d, obj, name):
    p = Path(d) / name; p.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8"); return p


def causal_numeric():
    n = base_numeric()
    P = lambda fy, v, pg=5: pt(fy, v, pg)
    n["deltas"] += [
        {"id": "d4", "item": "应收账款", "period": "latest", "scale_kind": "assets", "unit": "元", "current": P(2020, 3000.0), "prior": P(2020, 2000.0), "delta": 1000.0, "check_ids": []},
        {"id": "d5", "item": "营业收入", "period": "latest", "scale_kind": "revenue", "unit": "元", "current": P(2020, 1000.0), "prior": P(2020, 1000.0), "delta": 0.0, "check_ids": []},
        {"id": "d6", "item": "净利润", "period": "latest", "scale_kind": "revenue", "unit": "元", "current": P(2020, -500.0), "prior": P(2020, 100.0), "delta": -600.0, "check_ids": []},
        {"id": "d7", "item": "长期借款-抵押借款", "period": "latest", "scale_kind": "assets", "unit": "元", "current": P(2020, 10.0), "prior": P(2020, 9.0),
         "prior_as_originally_reported": P(2019, 5.0, 4), "delta": 1.0, "restated": False, "restatement_class": "presentation_or_basis_change",
         "restatement_subclass": "net_vs_gross_current_portion", "check_ids": []}]
    n["scale"]["total_assets"] = 10000.0
    n["basis_changes"] = [{"delta_id": "d7", "item": "长期借款-抵押借款", "subclass": "net_vs_gross_current_portion"}]
    return n


class NumericPackTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(); self.d = self._tmp.name; self.src = mk_sources(self.d)
        self.pkg = Path(self.d) / "pkg"

    def tearDown(self):
        self._tmp.cleanup()

    def test_import_and_causal_rank(self):
        r = numeric.import_pack(write(self.d, base_numeric(), "n.json"), write(self.d, narrative(), "r.json"), self.src, self.pkg)
        self.assertEqual((r["deltas"], r["narrative"], r["failed_checks"]), (3, 1, 1))
        v = numeric.view(self.pkg, "deltas")
        self.assertEqual({x["id"]: x["causal_role"] for x in v["deltas"]}, {"d1": "driver", "d2": "context", "d3": "driver"})
        self.assertEqual(v["deltas"][-1]["id"], "d2")              # context after drivers
        top = [x for x in v["deltas"] if x["id"] == "d1"][0]
        self.assertEqual(top["prior_as_originally_reported"]["value"], 900000000.00)
        self.assertEqual(top["failed_check_ids"], ["c1"])
        self.assertNotIn("severity", top)

    def test_drivers_consequences_and_normal_events(self):
        numeric.import_pack(write(self.d, causal_numeric(), "n.json"), None, self.src, self.pkg)
        dr = numeric.view(self.pkg, "drivers")["drivers"]
        ar = [k for k in dr if k["indicator"].startswith("应收账款增速")][0]
        self.assertEqual((ar["strength"], ar["category"], ar["evidence"][0]["delta_id"]), (3, "collection", "d4"))
        cs = numeric.view(self.pkg, "consequences")["consequences"]
        self.assertEqual(cs[0]["delta_id"], "d6"); self.assertIn(ar["id"], cs[0]["linked_drivers"])
        nm = numeric.view(self.pkg, "normal")["normal_events"]
        self.assertEqual(nm[0]["kind"], "presentation_or_basis_change"); self.assertEqual(nm[0]["explains"][0]["delta_id"], "d7")
        pos = {x["id"]: i for i, x in enumerate(numeric.view(self.pkg, "deltas")["deltas"])}
        self.assertTrue(pos["d4"] < pos["d6"] < pos["d2"])         # driver < consequence < context
        self.assertEqual(numeric.view(self.pkg, "deltas", role="consequence")["total"], 1)

    def test_rejects_restated_basis_change(self):
        n = causal_numeric(); n["deltas"][-1]["restated"] = True
        with self.assertRaisesRegex(numeric.Invalid, "basis change"):
            numeric.import_pack(write(self.d, n, "n.json"), None, self.src, self.pkg)

    def test_rejects_non_verbatim_excerpt(self):
        n = base_numeric(); n["deltas"][0]["current"]["excerpt"] = "短期借款 30亿"
        with self.assertRaisesRegex(numeric.Invalid, "verbatim"):
            numeric.import_pack(write(self.d, n, "n.json"), None, self.src, self.pkg)

    def test_rejects_missing_page_or_table_and_bad_delta(self):
        for mut, msg in ((lambda n: n["deltas"][1]["prior"].update(page=77), "not in FY2020"),
                         (lambda n: n["deltas"][1]["prior"].pop("table_id"), "table_id"),
                         (lambda n: n["deltas"][1].update(delta=5.0), "current - prior"),
                         (lambda n: n["deltas"][1].pop("unit"), "unit"),
                         (lambda n: n["deltas"][1]["current"].update(value=True), "value must be a finite number")):
            with self.subTest(msg=msg):
                n = base_numeric(); mut(n)
                with self.assertRaisesRegex(numeric.Invalid, msg):
                    numeric.import_pack(write(self.d, n, "n.json"), None, self.src, Path(self.d) / f"pkg{msg[:3]}")

    def test_rejects_non_verbatim_quote(self):
        r = narrative(); r["items"][0]["quote"] = "公司进行了重述"
        with self.assertRaisesRegex(numeric.Invalid, "quote not verbatim"):
            numeric.import_pack(write(self.d, base_numeric(), "n.json"), write(self.d, r, "r.json"), self.src, self.pkg)

    def test_views_and_filters_and_cli(self):
        numeric.import_pack(write(self.d, base_numeric(), "n.json"), write(self.d, narrative(), "r.json"), self.src, self.pkg)
        self.assertEqual(numeric.view(self.pkg, "deltas", period="earlier")["total"], 1)
        self.assertEqual(numeric.view(self.pkg, "deltas", item="资产")["deltas"][0]["id"], "d2")
        self.assertEqual(numeric.view(self.pkg, "checks", failed_only=True)["total"], 1)
        sm = numeric.view(self.pkg, "overview")
        self.assertEqual(sm["counts"]["failed_checks"], 1); self.assertEqual(sm["flags"][0]["value_pct"], 45.0)
        # 45% >= 30% -> guarantee driver
        self.assertTrue(any(k["category"] == "guarantee_related" for k in numeric.view(self.pkg, "drivers")["drivers"]))
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.assertEqual(ontology.main(["numeric", str(self.pkg), "--view", "narrative"]), 0)
        self.assertEqual(json.loads(buf.getvalue())["total"], 1)

    def test_immutable_and_tamper_detected(self):
        numeric.import_pack(write(self.d, base_numeric(), "n.json"), None, self.src, self.pkg)
        with self.assertRaisesRegex(numeric.Invalid, "exists"):
            numeric.import_pack(write(self.d, base_numeric(), "n.json"), None, self.src, self.pkg)
        f = self.pkg / "numeric.json"; f.write_text(f.read_text(encoding="utf-8").replace("短期借款", "长期借款"), encoding="utf-8")
        with self.assertRaisesRegex(numeric.Invalid, "hash"):
            numeric.view(self.pkg, "summary")


if __name__ == "__main__":
    unittest.main(verbosity=1)
