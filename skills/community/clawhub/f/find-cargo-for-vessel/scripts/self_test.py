from __future__ import annotations

import unittest

try:
    from .common import haversine_nm
    from .find_cargo import build_detail_action, infer_trade
    from .port_resolver import Port, PortResolver, parse_coordinates
    from .service import render_detail_page
    from .sol_cargo import parse_quantity_tons
except ImportError:
    from common import haversine_nm
    from find_cargo import build_detail_action, infer_trade
    from port_resolver import Port, PortResolver, parse_coordinates
    from service import render_detail_page
    from sol_cargo import parse_quantity_tons


class QuantityTests(unittest.TestCase):
    def test_single_and_scaled_quantities(self):
        self.assertEqual(parse_quantity_tons("3000吨")["min_tons"], 3000)
        self.assertEqual(parse_quantity_tons("12k")["min_tons"], 12000)
        self.assertEqual(parse_quantity_tons("5万吨")["min_tons"], 50000)

    def test_range_uses_minimum(self):
        result = parse_quantity_tons("10k-25k")
        self.assertEqual(result["min_tons"], 10000)
        self.assertEqual(result["max_tons"], 25000)
        compact = parse_quantity_tons("27-32000mts")
        self.assertEqual(compact["min_tons"], 27000)
        self.assertEqual(compact["max_tons"], 32000)

    def test_tolerance_and_manual_values(self):
        result = parse_quantity_tons("15000 ± 10% BDMT")
        self.assertEqual(result["min_tons"], 13500)
        self.assertEqual(result["max_tons"], 16500)
        self.assertEqual(
            parse_quantity_tons("5000方")["status"],
            "manual_confirmation",
        )
        self.assertEqual(
            parse_quantity_tons("详情如下")["status"],
            "manual_confirmation",
        )
        self.assertEqual(
            parse_quantity_tons("4")["status"],
            "manual_confirmation",
        )


class PortTests(unittest.TestCase):
    def setUp(self):
        self.shanghai = Port("CNSHG", "Shanghai Pt", "CN", 31.2, 121.5)
        self.zhoushan = Port("CNZOS", "Zhoushan", "CN", 30.0, 122.1)
        self.hong_kong = Port("HKHKG", "Hong Kong", "HK", 22.3, 114.2)
        self.resolver = PortResolver(
            [self.shanghai, self.zhoushan, self.hong_kong]
        )

    def test_locode_and_chinese_name(self):
        self.assertEqual(self.resolver.resolve("CNZOS").locode, "CNZOS")
        self.assertEqual(
            self.resolver.resolve("\u821f\u5c71\u6e2f").locode,
            "CNZOS",
        )

    def test_trade_inference(self):
        self.assertEqual(infer_trade(self.zhoushan, self.shanghai), "domestic")
        self.assertEqual(
            infer_trade(self.zhoushan, self.hong_kong),
            "international",
        )

    def test_coordinates_and_distance(self):
        self.assertEqual(parse_coordinates("3001N 12206E"), (30.016666666666666, 122.1))
        self.assertAlmostEqual(haversine_nm(30, 122, 30, 122), 0)


class DetailLinkTests(unittest.TestCase):
    def test_internal_detail_action(self):
        action = build_detail_action("akkejki", "https://shipping.example/api/")
        self.assertEqual(action["type"], "open_internal_detail")
        self.assertEqual(action["path"], "/cargo/akkejki/view")
        self.assertEqual(
            action["url"],
            "https://shipping.example/api/cargo/akkejki/view",
        )
        self.assertEqual(action["api_path"], "/cargo/akkejki")

    def test_detail_page_escapes_values_and_has_no_source_link(self):
        page = render_detail_page(
            {
                "cargo_id": "C100960",
                "cargo_name": "<script>alert(1)</script>",
                "contact_access": "empty_or_paid",
            }
        )
        self.assertIn("C100960", page)
        self.assertNotIn("<script>alert(1)</script>", page)
        self.assertNotIn("chartering.sol.com.cn", page)
        self.assertIn("需要付费查看", page)


if __name__ == "__main__":
    unittest.main(verbosity=2)
