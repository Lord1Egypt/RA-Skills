from __future__ import annotations

import unittest
from datetime import date
from unittest.mock import patch

from . import find_vessel as find_vessel_module
from .find_vessel import (
    build_detail_action,
    parse_loading_date,
    parse_open_date,
    search_vessels,
)
from .port_resolver import Port, infer_trade
from .service import render_detail_page
from .sol_tonnage import _parse_list_page, parse_capacity_tons


class CapacityTests(unittest.TestCase):
    def test_single_scaled_and_bare_values(self):
        self.assertEqual(parse_capacity_tons("5000吨")["max_tons"], 5000)
        self.assertEqual(parse_capacity_tons("DWCC26000")["max_tons"], 26000)
        self.assertEqual(parse_capacity_tons("1.2万吨")["max_tons"], 12000)
        self.assertEqual(parse_capacity_tons("498")["max_tons"], 498)

    def test_range_and_dimension(self):
        value = parse_capacity_tons("10000--50000T")
        self.assertEqual(value["min_tons"], 10000)
        self.assertEqual(value["max_tons"], 50000)
        self.assertEqual(
            parse_capacity_tons("76*22")["status"],
            "manual_confirmation",
        )
        self.assertEqual(
            parse_capacity_tons("14,619 / 13,411 M3")["status"],
            "manual_confirmation",
        )


class DateTests(unittest.TestCase):
    def test_loading_date(self):
        self.assertEqual(parse_loading_date("2026-07-25"), date(2026, 7, 25))
        self.assertEqual(parse_loading_date("2026年7月25日"), date(2026, 7, 25))

    def test_open_date_and_nearest_year(self):
        reference = date(2026, 12, 28)
        parsed = parse_open_date("1月3日", reference)
        self.assertEqual(parsed["date"], "2027-01-03")
        self.assertEqual(parsed["delta_days"], 6)
        self.assertEqual(
            parse_open_date("2026年6月底附近", reference)["status"],
            "manual_confirmation",
        )
        self.assertEqual(
            parse_open_date("3RD/JAN", reference)["date"],
            "2027-01-03",
        )

    def test_time_window_boundaries(self):
        reference = date(2026, 7, 25)
        self.assertEqual(parse_open_date("2026-07-18", reference)["delta_days"], -7)
        self.assertEqual(parse_open_date("2026-08-09", reference)["delta_days"], 15)


class ParsingTests(unittest.TestCase):
    def test_list_row(self):
        page = """
        <table><tr>
          <td></td><td><a href="open_msg.asp?solid=akalhbi">T101999</a></td>
          <td>测试公司</td><td>TBN</td><td>杂货船</td><td>3600载重吨</td>
          <td>大连</td><td>2026-07-30</td><td>7-25</td>
        </tr></table>
        """
        records, pages = _parse_list_page(page, "A")
        self.assertEqual(pages, 1)
        self.assertEqual(records[0]["vessel_id"], "T101999")
        self.assertEqual(records[0]["solid"], "akalhbi")


class TradeAndActionTests(unittest.TestCase):
    def test_trade(self):
        china = Port("CNDLC", "Dalian", "CN", 38.9, 121.6)
        shanghai = Port("CNSHG", "Shanghai", "CN", 31.2, 121.5)
        singapore = Port("SGSIN", "Singapore", "SG", 1.3, 103.8)
        self.assertEqual(infer_trade(china, shanghai), "domestic")
        self.assertEqual(infer_trade(china, singapore), "international")

    def test_internal_detail_action(self):
        action = build_detail_action("akalhbi", "https://shipping.example/api/")
        self.assertEqual(action["path"], "/vessel/akalhbi/view")
        self.assertEqual(
            action["url"],
            "https://shipping.example/api/vessel/akalhbi/view",
        )

    def test_detail_page_is_safe(self):
        page = render_detail_page(
            {
                "vessel_id": "T101999",
                "vessel_name": "<script>alert(1)</script>",
                "contact_access": "empty_or_paid",
            }
        )
        self.assertNotIn("<script>alert(1)</script>", page)
        self.assertNotIn("chartering.sol.com.cn", page)
        self.assertIn("需要付费查看", page)


class FakeResolver:
    load = Port("CNSWE", "Shanwei", "CN", 22.78, 115.35)
    discharge = Port("CNNTG", "Nantong", "CN", 32.02, 120.85)
    nearby = Port("CNSWE", "Shanwei", "CN", 22.78, 115.35)

    def resolve(self, value):
        return self.load if value == "汕尾" else self.discharge

    def resolve_field(self, value):
        return [] if value == "全国" else [self.nearby]


class MatchingTests(unittest.TestCase):
    def test_confirmed_and_manual_records_are_retained_and_ranked(self):
        records = [
            {
                "vessel_id": "T2",
                "company_name": "B",
                "vessel_name": "未知船",
                "vessel_type": "散货船",
                "capacity_raw": "76*22",
                "open_port_raw": "全国",
                "open_date_raw": "待定",
                "updated_date": "7-25",
                "solid": "bbb",
                "trade_code": "A",
            },
            {
                "vessel_id": "T1",
                "company_name": "A",
                "vessel_name": "确定船",
                "vessel_type": "散货船",
                "capacity_raw": "12000吨",
                "open_port_raw": "汕尾",
                "open_date_raw": "2026-07-30",
                "updated_date": "7-25",
                "solid": "aaa",
                "trade_code": "A",
            },
            {
                "vessel_id": "T3",
                "company_name": "C",
                "vessel_name": "小船",
                "vessel_type": "散货船",
                "capacity_raw": "5000吨",
                "open_port_raw": "汕尾",
                "open_date_raw": "2026-07-30",
                "updated_date": "7-25",
                "solid": "ccc",
                "trade_code": "A",
            },
        ]
        payload = {
            "records": records,
            "fetched_at": "2026-07-25T00:00:00+08:00",
            "cache_status": "fresh",
            "record_count": len(records),
        }
        with (
            patch.object(
                find_vessel_module,
                "PortResolver",
                return_value=FakeResolver(),
            ),
            patch.object(
                find_vessel_module,
                "get_tonnage_list",
                return_value=payload,
            ),
        ):
            result = search_vessels(
                "汕尾",
                "南通",
                "河沙",
                10000,
                "2026-07-25",
                sync_demand_record=False,
            )
        self.assertEqual([item["vessel_id"] for item in result["results"]], ["T1", "T2"])
        self.assertEqual(
            result["results"][1]["manual_confirmation_fields"],
            ["capacity", "open_date", "open_port"],
        )
        self.assertEqual(result["coverage"]["capacity_excluded_records"], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
