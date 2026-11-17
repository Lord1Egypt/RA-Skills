from __future__ import annotations

import unittest
from datetime import date
from unittest.mock import patch

from . import find_buyer as matcher
from .find_buyer import (
    _age_score,
    _capacity_score,
    parse_buyer_age,
    parse_capacity,
    parse_seller_age,
    search_buyers,
    vessel_type_score,
)
from .service import render_detail_page
from .sol_purchases import _parse_list_page


class ParsingTests(unittest.TestCase):
    def test_capacity_units_and_ranges(self):
        self.assertEqual(parse_capacity("5000吨")["unit"], "DWT")
        self.assertEqual(parse_capacity("3～5万DWT")["max"], 50000)
        self.assertEqual(parse_capacity("1200TEU")["unit"], "TEU")

    def test_seller_age_forms(self):
        self.assertEqual(parse_seller_age("8年")["age"], 8)
        self.assertEqual(parse_seller_age("2018年建造")["age"], date.today().year - 2018)
        self.assertTrue(parse_seller_age("新船")["is_new_ship"])

    def test_buyer_age_ranges(self):
        self.assertEqual(parse_buyer_age("不限")["status"], "unrestricted")
        self.assertEqual(parse_buyer_age("10-15年")["min"], 10)
        self.assertEqual(parse_buyer_age("新船")["max"], 0)

    def test_list_page_regular_and_featured_rows(self):
        html = """<table>
        <tr><td></td><td><a href="purchase_msg.asp?solid=abc">P12345</a></td><td>油船</td><td>4000～6000DWT</td><td>5-10年</td><td>中国旗</td><td>测试公司</td><td>有效</td><td>26-7-26</td></tr>
        <tr><td><a href="purchase_msg.asp?solid=def">P12346</a></td><td>油船</td><td>3000～7000DWT</td><td>不限</td><td>不限</td><td>有效</td><td>26-7-25</td></tr>
        </table>"""
        records, has_next = _parse_list_page(html)
        self.assertFalse(has_next)
        self.assertEqual([item["purchase_id"] for item in records], ["P12345", "P12346"])
        self.assertEqual(records[0]["company_name"], "测试公司")
        self.assertEqual(records[1]["company_name"], "")


class ScoreTests(unittest.TestCase):
    def test_type_scores(self):
        self.assertEqual(vessel_type_score("油船", "油船"), 35)
        self.assertEqual(vessel_type_score("油船", "化学品船"), 28)
        self.assertIsNone(vessel_type_score("油船", "散货船"))
        self.assertIsNone(vessel_type_score("油船", "其他船"))

    def test_capacity_interval_and_tolerance(self):
        seller = parse_capacity("5000DWT")
        self.assertEqual(_capacity_score(seller, parse_capacity("3000-7000DWT"))[0], 35)
        self.assertIsNotNone(_capacity_score(seller, parse_capacity("5500-6000DWT")))
        self.assertIsNone(_capacity_score(seller, parse_capacity("7000-8000DWT")))

    def test_new_ship_requires_zero_in_buyer_range(self):
        seller = parse_seller_age("新船")
        self.assertIsNotNone(_age_score(seller, parse_buyer_age("新船")))
        self.assertIsNone(_age_score(seller, parse_buyer_age("5-10年")))

    def test_detail_page_safe_without_membership(self):
        page = render_detail_page(
            {
                "purchase_id": "P1",
                "remarks": "<script>x</script>",
                "membership_type": "高级会员",
                "membership_points": "100",
                "contact_access": "empty_or_paid",
            }
        )
        self.assertNotIn("<script>x</script>", page)
        self.assertNotIn("sp.sol.com.cn", page)
        self.assertNotIn("会员类型", page)
        self.assertNotIn("会员积分", page)
        self.assertNotIn("高级会员", page)
        self.assertIn("需要付费查看", page)


class MatchingTests(unittest.TestCase):
    def test_filters_ranking_and_record_only_trade_scope(self):
        records = [
            {"purchase_id": "P1", "vessel_type": "油船", "capacity_raw": "4000～6000DWT", "age_range_raw": "5-10年", "flag": "中国旗", "company_name": "A", "status": "有效", "updated_date": "26-7-26", "solid": "aaa"},
            {"purchase_id": "P2", "vessel_type": "化学品船", "capacity_raw": "3000～7000DWT", "age_range_raw": "不限", "flag": "中国旗", "company_name": "B", "status": "有效", "updated_date": "26-7-25", "solid": "bbb"},
            {"purchase_id": "P3", "vessel_type": "散货船", "capacity_raw": "4000～6000DWT", "age_range_raw": "5-10年", "flag": "中国旗", "company_name": "C", "status": "有效", "updated_date": "26-7-25", "solid": "ccc"},
            {"purchase_id": "P4", "vessel_type": "油船", "capacity_raw": "4000～6000DWT", "age_range_raw": "5-10年", "flag": "中国旗", "company_name": "D", "status": "过期", "updated_date": "26-7-25", "solid": "ddd"},
            {"purchase_id": "P5", "vessel_type": "油船", "capacity_raw": "4000～6000DWT", "age_range_raw": "5-10年", "flag": "不限", "company_name": "E", "status": "有效", "updated_date": "26-7-25", "solid": "eee"},
        ]
        payload = {"records": records, "fetched_at": "now", "cache_status": "fresh", "record_count": 5, "page_count": 1, "truncated": False}
        detail = {"company_name": "测试公司", "contact_access": "visible", "membership_type": "高级会员"}
        with patch.object(matcher, "get_purchase_list", return_value=payload), patch.object(matcher, "get_purchase_detail", return_value=detail):
            result = search_buyers("油船", "5000DWT", "8年", flag="中国旗", trade_scope="内贸", sync_demand_record=False)
        self.assertEqual([item["purchase_id"] for item in result["results"]], ["P1", "P2"])
        self.assertGreater(result["results"][0]["match_score"], result["results"][1]["match_score"])
        self.assertEqual(result["coverage"]["status_excluded"], 1)
        self.assertEqual(result["coverage"]["flag_excluded"], 1)
        self.assertFalse(result["query"]["trade_scope_used_for_matching"])
        self.assertTrue(all("membership_type" not in item for item in result["results"]))
        self.assertEqual(result["demand_sync"]["status"], "disabled_for_validation")


if __name__ == "__main__":
    unittest.main(verbosity=2)
