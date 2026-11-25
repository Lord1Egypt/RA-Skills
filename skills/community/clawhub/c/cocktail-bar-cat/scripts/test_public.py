#!/usr/bin/env python3
"""公开分发的隐私、兼容和演示价格回归门禁；只读本地文件。"""
import ast
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parent.parent


def load(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


class PublicTests(unittest.TestCase):
    def test_business_records_are_empty(self):
        self.assertEqual(load("customers.json")["customers"], [])
        sales = load("sales.json")
        self.assertEqual(sales["daily"], [])
        self.assertTrue(all(value == 0 for value in sales["summary"].values()))
        inventory = load("inventory.json")
        self.assertEqual(inventory["inventory"], {})
        self.assertEqual(inventory["regular_customers"], {})
        cost = load("cost_history.json")
        self.assertEqual(cost["tracking_items"], [])
        self.assertEqual(cost["weekly_data"], [])
        supplier = load("suppliers.json")
        self.assertEqual(supplier["suppliers"], [])
        self.assertEqual(supplier["price_records"], [])
        self.assertEqual(load("menu.json")["menu"]["categories"], {})
        self.assertEqual(load("menu_real.json")["menu"]["categories"], {})
        self.assertEqual(load("gommone_products.json"), [])
        self.assertEqual(load("push_history.json")["pushed"], {})

    def test_empty_templates_reject_additional_private_fields(self):
        expected = {
            "customers.json": {"customers": []},
            "push_history.json": {"pushed": {}},
            "gommone_products.json": [],
            "sales.json": {"generated_at": None, "period": {}, "summary": {
                "total_days": 0, "total_orders": 0, "total_revenue": 0,
                "daily_avg_orders": 0, "daily_avg_revenue": 0}, "daily": []},
            "cost_history.json": {"generated_at": None, "period": {}, "tracking_items": [],
                                  "weekly_data": [], "trend_analysis": {}},
            "inventory.json": {"inventory": {}, "regular_customers": {}, "update_time": None,
                "price_source": "公开版空记录模板；价格演示见 prices.json，不代表采购记录", "price_update_date": None},
            "suppliers.json": {"suppliers": [], "price_records": [],
                "usage": "公开版空记录模板；由使用者自行建立供应商档案与价格记录"},
        }
        menu = {"menu": {"name": "公开版空酒单模板", "categories": {}},
                "notes": "不包含门店选单、定价或上架状态；请自行设置酒单"}
        expected.update({"menu.json": menu, "menu_real.json": menu})
        for name, data in expected.items():
            self.assertEqual(load(name), data, name)

    def test_business_metadata_does_not_claim_live_prices(self):
        for name in ("prices.json", "shopping.json", "inventory.json", "recipes.json"):
            text = (ROOT / name).read_text(encoding="utf-8")
            self.assertIn("演示", text, name)
            for marker in ("京东参考", "淘宝参考", "真实采购", "沿用采购价", "门店配方表"):
                self.assertNotIn(marker, text, name)

    def test_no_private_paths_or_credentials_in_distribution(self):
        patterns = (
            r"/Users/[A-Za-z0-9._-]+/", r"[A-Za-z]:\\Users\\",
            r"gh[pousr]_[A-Za-z0-9]{30,}", r"github_pat_[A-Za-z0-9_]{30,}",
            r"AKIA[0-9A-Z]{16}", r"sk-[A-Za-z0-9]{30,}",
            r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
        )
        for path in ROOT.rglob("*"):
            if not path.is_file() or (path.suffix not in (".json", ".md", ".py") and path.name != ".gitignore"):
                continue
            text = path.read_text(encoding="utf-8")
            for pattern in patterns:
                self.assertIsNone(re.search(pattern, text), path.relative_to(ROOT).as_posix())
        self.assertFalse((ROOT / "_skillhub_meta.json").exists())
        self.assertFalse((ROOT / "backup").exists())

    def test_recipe_business_fields_have_no_store_brand(self):
        for recipe in load("recipes.json")["recipes"]:
            self.assertFalse(recipe.get("menu"))
            self.assertNotIn("enabled", recipe)
            for ingredient in recipe["ingredients"]:
                self.assertNotIn("brand", ingredient)
            self.assertGreater(recipe["cost_estimate"], 0)
            expected = float((Decimal(str(recipe["cost_estimate"])) / Decimal("0.25")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
            prices = recipe["suggested_price"]
            prices = prices if isinstance(prices, list) else [prices]
            self.assertTrue(prices)
            for price in prices:
                self.assertGreater(price, recipe["cost_estimate"])
                self.assertAlmostEqual(price, expected, places=2, msg=recipe["name"])

    def test_demo_recipe_costs_recalculate(self):
        prices = load("prices.json")
        flat = {name: entry for category, rows in prices.items() if category != "notes"
                for name, entry in rows.items() if isinstance(entry, dict)}
        for recipe in load("recipes.json")["recipes"]:
            total = Decimal(0)
            for item in recipe["ingredients"]:
                name, unit, amount = item["name"], item["unit"], item["amount"]
                self.assertIn(name, flat)
                if isinstance(amount, (int, float)) or (isinstance(amount, str) and re.fullmatch(r"\d+(?:\.\d+)?", amount)):
                    quantity = Decimal(str(amount))
                elif amount is None or amount == "up":
                    quantity = Decimal(1)
                else:
                    self.fail("未声明的演示数量: " + recipe["name"] + "/" + name)
                factor = Decimal(1)
                if unit == "barspoon":
                    factor = Decimal(5)
                elif unit == "dash":
                    factor = Decimal("0.5")
                elif unit == "drop":
                    factor = Decimal("0.05")
                elif unit in ("topping", "fill"):
                    factor = Decimal("0.2" if name == "肉桂粉" else "3" if name == "茴香酒" else "60" if name == "香槟" else "100")
                elif unit == "个" and name in ("蛋白", "蛋清", "蛋黄"):
                    factor = Decimal(30)
                elif unit == "片":
                    factor = Decimal("0.2" if name in ("薄荷叶", "罗勒叶") else "2")
                elif unit not in ("ml", "g"):
                    factors = {"颗": "5", "个": "10", "块": "5", "根": "3", "转": "0.1", "边": "0.5", "杯": "150"}
                    factor = Decimal(factors[unit])
                total += quantity * factor * Decimal(str(flat[name]["price_per_unit"]))
            expected = float(total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
            self.assertAlmostEqual(recipe["cost_estimate"], expected, places=2, msg=recipe["name"])

    def test_demo_package_prices_are_consistent(self):
        for category, rows in load("prices.json").items():
            if category == "notes":
                continue
            for name, entry in rows.items():
                quantity = entry.get("volume_ml", entry.get("weight_g"))
                self.assertGreater(quantity, 0, name)
                self.assertAlmostEqual(entry["price"], quantity * entry["price_per_unit"], places=3, msg=name)
                if entry["unit"] == "ml":
                    self.assertEqual(entry["price_per_ml"], entry["price_per_unit"])

    def test_shopping_demo_prices_match_material_rates(self):
        prices = load("prices.json")
        flat = {name: entry for category, rows in prices.items() if category != "notes"
                for name, entry in rows.items()}
        aliases = {"卡莎萨": "卡莎萨", "查特绿": "查特绿"}
        shopping = load("shopping.json")
        for bottle in shopping["bottles"]:
            key = aliases.get(bottle["key"], bottle["key"])
            self.assertIn(key, flat)
            for option in [bottle] + ([bottle["small_size"]] if bottle.get("small_size") else []):
                capacity = re.search(r"(\d+(?:\.\d+)?)\s*ml", option["spec"])
                self.assertIsNotNone(capacity)
                expected = float((Decimal(capacity.group(1)) * Decimal(str(flat[key]["price_per_unit"]))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
                self.assertAlmostEqual(option["price"], expected, places=2, msg=bottle["key"])

    def test_demo_quantity_assumptions_are_explicit(self):
        manifest = load("public-data-manifest.json")
        assumptions = manifest["synthetic_prices"]["quantity_assumptions"]
        self.assertIn("1g/ml", assumptions["cross_unit_density"])
        self.assertEqual(assumptions["base_quantity_factors"]["dash"], 0.5)
        self.assertEqual(assumptions["base_quantity_factors"]["drop"], 0.05)
        self.assertIn("数值字符串", assumptions["numeric_amount"])
        self.assertEqual(manifest["recipe_preservation"]["sha256_before_and_after"],
                         "285af2c735adc8cbc2bc8a01d864a3e4caafdb3613a81c50f7a21fa25521e6e6")

    def test_frontmatter_description_and_references(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        front = text.split("---", 2)[1]
        self.assertRegex(front, r"(?m)^name: cocktail-bar-cat$")
        self.assertRegex(front, r"(?m)^version: [\"']?2\.7\.4")
        self.assertRegex(front, r"(?m)^agent_created: true$")
        description = re.search(r"(?ms)^description:\s*(.*?)(?=\n[A-Za-z_][A-Za-z0-9_-]*:|\Z)", front)
        self.assertIsNotNone(description)
        self.assertLessEqual(len(description.group(1).strip()), 1024)
        self.assertLess(len(text.splitlines()), 500)
        for reference in set(re.findall(r"references/[A-Za-z0-9_-]+\.md", text)):
            self.assertTrue((ROOT / reference).is_file(), reference)
        for path in ROOT.glob("*.json"):
            self.assertIn(path.name, text)

    def test_query_script_does_not_write_or_report(self):
        for name in ("history.py", "feedback.py", "inspire.py", "shop.py", "bars.py"):
            tree = ast.parse((ROOT / "scripts" / name).read_text(encoding="utf-8"))
            modules = {alias.name.split(".")[0] for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
            self.assertFalse(modules & {"requests", "urllib", "socket", "httpx", "aiohttp"}, name)
            attrs = {node.attr for node in ast.walk(tree) if isinstance(node, ast.Attribute)}
            self.assertFalse(attrs & {"write_text", "write_bytes", "unlink", "rename", "mkdir"}, name)

    def test_source_facts_preserved_while_expression_changes(self):
        # 原 v2.7.2 的证据事实投影；不把文字重新整理冒充原字节不变。
        pick = lambda row, keys: {key: row.get(key) for key in keys}
        history_data = load("cocktail_history.json")
        bar_data = load("bar_signatures.json")
        history_facts = {
            "sources": [pick(s, ("id", "author", "year", "edition", "kind", "url", "accessed", "verification")) for s in history_data["sources"]],
            "records": [{**pick(r, ("id", "name", "name_en", "family_id", "canonical_name")),
                "claims": [pick(c, ("status", "source_ids", "locator")) for c in r["claims"]],
                "versions": [pick(v, ("year", "source_id", "locator", "label")) for v in r.get("historical_versions", [])]}
                for r in history_data["records"]],
        }
        bar_facts = {
            "sources": [pick(s, ("id", "publisher", "date", "kind", "url")) for s in bar_data["sources"]],
            "bars": [pick(b, ("id", "name", "city", "region", "tier", "source_ids", "source_date", "last_verified", "freshness", "menu_status", "concept_only", "signature_count")) for b in bar_data["bars"]],
            "signatures": [{**pick(s, ("id", "name", "bar", "city", "classic_anchor", "source_ids", "menu_snapshot", "freshness", "status", "snapshot_source", "verified")),
                "ingredients": s["replica"]["ingredients"]} for s in bar_data["signatures"]],
        }
        for data, expected in ((history_facts, "81c9d753d0758ccaeb27629daa761f9aee025c4ee57ab2785e79ef42637bfc71"),
                               (bar_facts, "b40562123b5352e462890517aa59c378b7dd843b7264a9638f9e8ae7acb1093b")):
            self.assertEqual(hashlib.sha256(json.dumps(data, ensure_ascii=False, sort_keys=True).encode()).hexdigest(), expected)

    def test_no_distributed_third_party_excerpt_fields(self):
        data = load("cocktail_history.json")
        self.assertEqual(data["policy"]["distribution_profile"], "clawhub_mit0")
        for record in data["records"]:
            for claim in record["claims"]:
                self.assertNotIn("quote_en", claim)
                self.assertNotIn("quote_zh", claim)
                self.assertTrue(claim.get("evidence_record"))
            for version in record.get("historical_versions", []):
                self.assertNotIn("method_original", version)
                self.assertNotIn("method_zh", version)
                self.assertTrue(version.get("method_summary_zh"))
        bars = load("bar_signatures.json")
        self.assertEqual(bars["distribution_profile"], "clawhub_mit0")
        self.assertTrue(all("taste_note" not in bar for bar in bars["bars"]))
        text = json.dumps(bars, ensure_ascii=False)
        # 不将待排除的第三方原句抄入测试包；仅检查自有分类标签。
        self.assertNotIn("携程笔记原文", text)
        self.assertNotIn("taste_note", text)

    def test_no_residual_review_or_copy_expressions(self):
        bars = load("bar_signatures.json")
        text = json.dumps(bars, ensure_ascii=False)
        for marker in ("顾客评价里", "探店者称", "公开探店文把它列为", "被批评「",
                       "被作者列为", "最值得抄", "整套照搬", "可照搬的结构",
                       "骨架照搬", "好喝到连去两天", "羊城最爱酒吧"):
            self.assertNotIn(marker, text, marker)
        self.assertIn("骨架不变", text)
        self.assertEqual(bars["version"], "2.7.4")
        self.assertIn("v274_expression_cleanup", bars["expression_policy"])

    def test_mit0_license_and_isolated_profile(self):
        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("MIT No Attribution", license_text)
        self.assertIn("homleeliu-yishe", license_text)
        self.assertIn("Permission is hereby granted, free of charge", license_text)
        self.assertNotIn("The above copyright notice and this permission notice", license_text)
        manifest = load("public-data-manifest.json")
        self.assertEqual(manifest["distribution_profile"], "clawhub_mit0")
        self.assertEqual(manifest["license"], "MIT-0")
        self.assertFalse((ROOT / "icon.png").exists())

    def test_no_toxic_or_flame_serving_and_no_medical_claims(self):
        recipes = load("recipes.json")["recipes"]
        holidays = load("holidays.json")
        for marker in ("雄黄粉", "雄黄酒（改良版）"):
            self.assertNotIn(marker, json.dumps(holidays, ensure_ascii=False))
        for recipe in recipes:
            self.assertNotEqual(recipe["method"], "点燃")
            self.assertNotIn("治愈感冒", recipe.get("story", ""))
        self.assertIn("不点火", recipes[175]["method"])
        self.assertEqual(len(recipes), 177)

    def test_reorganized_knowledge_hashes_match_manifest(self):
        manifest = load("public-data-manifest.json")
        self.assertEqual(len(manifest["release_knowledge_hashes"]), 6)
        for name, record in manifest["release_knowledge_hashes"].items():
            self.assertEqual(hashlib.sha256((ROOT / name).read_bytes()).hexdigest(), record["sha256"], name)


if __name__ == "__main__":
    unittest.main(verbosity=2)
