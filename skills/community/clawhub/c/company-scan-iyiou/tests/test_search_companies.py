"""
TDD test suite for search_companies.py

Tests cover:
- Parameter construction from CLI args
- Pagination logic
- Response parsing
- Edge cases (no results, API error, etc.)
"""

import json
import sys
import tempfile
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import MagicMock, call, patch

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import search_companies as sc


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _make_page(items, total=25, page_no=1, page_size=10):
    """Build a fake API response envelope."""
    return {
        "code": 200,
        "message": "success",
        "data": {
            "total": total,
            "pageNo": page_no,
            "pageSize": page_size,
            "records": items,
        },
    }


def _make_company(i=1):
    return {
        "comId": f"COM{i:04d}",
        "briefName": f"示例公司{i}",
        "fullName": f"示例公司{i}有限公司",
        "briefIntro": f"这是第{i}家示例企业的一句话简介",
        "industryName": "生物医药",
        "latestInvestRoundStr": "B轮",
        "latestInvestorStr": "红杉资本,高瓴资本",
        "latestInvestTime": "2024-03-01",
        "marketValuationRmb": 500000,
        "province": "上海",
        "url": f"https://data.iyiou.com/company/{i}",
    }


# ---------------------------------------------------------------------------
# 1. Parameter builder tests
# ---------------------------------------------------------------------------

class TestBuildParams(unittest.TestCase):

    def test_minimal_concepts_only(self):
        params = sc.build_params(concepts=["生物医药"], page_no=1, page_size=10)
        self.assertEqual(params["concepts"], ["生物医药"])
        self.assertEqual(params["pageNo"], 1)
        self.assertEqual(params["pageSize"], 10)
        # default country = 44 (China mainland)
        self.assertEqual(params["country"], 44)

    def test_full_params(self):
        params = sc.build_params(
            concepts=["脑机接口", "BCI"],
            min_invest_round="B轮",
            max_invest_round="Pre-IPO",
            min_invest_amount_wan=10000,
            latest_invest_after="2024-01-01",
            provinces=["上海", "浙江"],
            cities=None,
            country=44,
            established_after=None,
            established_before=None,
            page_no=2,
            page_size=20,
        )
        self.assertEqual(params["minInvestRound"], "B轮")
        self.assertEqual(params["maxInvestRound"], "Pre-IPO")
        self.assertEqual(params["minInvestAmountWan"], 10000)
        self.assertEqual(params["latestInvestAfter"], "2024-01-01")
        self.assertEqual(params["provinces"], ["上海", "浙江"])
        self.assertEqual(params["pageNo"], 2)

    def test_none_values_excluded(self):
        """None params should not appear in the payload."""
        params = sc.build_params(concepts=["AI"], page_no=1, page_size=10,
                                  min_invest_round=None, cities=None)
        self.assertNotIn("minInvestRound", params)
        self.assertNotIn("cities", params)

    def test_city_overrides_province_for_precision(self):
        """When cities are given, provinces may also be present (both allowed)."""
        params = sc.build_params(concepts=["AI"], cities=["合肥"], page_no=1, page_size=10)
        self.assertIn("cities", params)

    def test_keyword_param(self):
        params = sc.build_params(keyword="宁德时代", page_no=1, page_size=10)
        self.assertEqual(params["keyword"], "宁德时代")


# ---------------------------------------------------------------------------
# 2. Pagination logic tests
# ---------------------------------------------------------------------------

class TestFetchAll(unittest.TestCase):

    @patch("search_companies.call_api")
    def test_single_page_result(self, mock_api):
        """Total <= page_size → only one API call."""
        companies = [_make_company(i) for i in range(5)]
        mock_api.return_value = _make_page(companies, total=5, page_no=1, page_size=10)
        result, total = sc.fetch_all(base_params={}, max_results=50, page_size=10)
        self.assertEqual(len(result), 5)
        self.assertEqual(total, 5)
        mock_api.assert_called_once()

    @patch("search_companies.call_api")
    def test_multi_page_fetches_all_up_to_total(self, mock_api):
        """Should paginate until total is reached."""
        page1 = [_make_company(i) for i in range(1, 11)]
        page2 = [_make_company(i) for i in range(11, 16)]
        mock_api.side_effect = [
            _make_page(page1, total=15, page_no=1, page_size=10),
            _make_page(page2, total=15, page_no=2, page_size=10),
        ]
        result, total = sc.fetch_all(base_params={}, max_results=50, page_size=10)
        self.assertEqual(len(result), 15)
        self.assertEqual(total, 15)
        self.assertEqual(mock_api.call_count, 2)

    @patch("search_companies.call_api")
    def test_max_results_cap(self, mock_api):
        """Never return more than max_results even if API has more."""
        pages = [[_make_company(i) for i in range(j, j + 10)] for j in range(0, 100, 10)]
        mock_api.side_effect = [
            _make_page(pages[i], total=200, page_no=i + 1, page_size=10)
            for i in range(5)  # only 5 pages should be fetched for max_results=50
        ]
        result, total = sc.fetch_all(base_params={}, max_results=50, page_size=10)
        self.assertLessEqual(len(result), 50)
        self.assertEqual(total, 200)  # real total preserved from API

    @patch("search_companies.call_api")
    def test_empty_result(self, mock_api):
        mock_api.return_value = _make_page([], total=0)
        result, total = sc.fetch_all(base_params={}, max_results=50, page_size=10)
        self.assertEqual(result, [])
        self.assertEqual(total, 0)

    @patch("search_companies.call_api")
    def test_api_error_raises(self, mock_api):
        mock_api.return_value = {"code": 500, "message": "Internal Server Error", "data": None}
        with self.assertRaises(sc.APIError):
            sc.fetch_all(base_params={}, max_results=50, page_size=10)


# ---------------------------------------------------------------------------
# 3. Markdown rendering tests
# ---------------------------------------------------------------------------

class TestRenderMarkdown(unittest.TestCase):

    def test_renders_all_fields(self):
        companies = [_make_company(1), _make_company(2)]
        md = sc.render_markdown(companies, total_found=2, query_summary="生物医药 / B轮 / 上海")
        # table header fields
        self.assertIn("企业简称", md)
        self.assertIn("企业全称", md)
        self.assertIn("一句话简介", md)
        self.assertIn("行业", md)
        self.assertIn("最新融资轮次", md)
        self.assertIn("最新投资方", md)
        self.assertIn("融资时间", md)
        self.assertIn("估值(万元)", md)
        self.assertIn("省份", md)
        self.assertIn("链接", md)
        # footer prompt
        self.assertIn("https://data.iyiou.com/company/comlist", md)

    def test_empty_companies_message(self):
        md = sc.render_markdown([], total_found=0, query_summary="脑机接口")
        self.assertIn("未找到", md)

    def test_truncation_notice_when_more_exist(self):
        """If total_found > len(companies), a 'more results' hint appears."""
        companies = [_make_company(i) for i in range(50)]
        md = sc.render_markdown(companies, total_found=200, query_summary="AI")
        self.assertIn("200", md)   # total number mentioned


# ---------------------------------------------------------------------------
# 4. CLI argument parsing tests
# ---------------------------------------------------------------------------

class TestCLI(unittest.TestCase):

    def test_parse_concepts_comma_separated(self):
        args = sc.parse_args(["--concepts", "生物医药,医疗器械"])
        self.assertEqual(args.concepts, ["生物医药", "医疗器械"])

    def test_parse_provinces_comma_separated(self):
        args = sc.parse_args(["--provinces", "上海,江苏,浙江"])
        self.assertEqual(args.provinces, ["上海", "江苏", "浙江"])

    def test_parse_max_results_default(self):
        args = sc.parse_args([])
        self.assertEqual(args.max_results, 50)

    def test_parse_min_invest_round(self):
        args = sc.parse_args(["--min-invest-round", "B轮"])
        self.assertEqual(args.min_invest_round, "B轮")

    def test_parse_output_file(self):
        args = sc.parse_args(["--output-file", "/tmp/out.md"])
        self.assertEqual(args.output_file, "/tmp/out.md")

    def test_parse_output_file_default_none(self):
        args = sc.parse_args([])
        self.assertIsNone(args.output_file)

    def test_parse_output_temp_flag(self):
        args = sc.parse_args(["--output-temp"])
        self.assertTrue(args.output_temp)

    def test_parse_output_temp_default_false(self):
        args = sc.parse_args([])
        self.assertFalse(args.output_temp)


# ---------------------------------------------------------------------------
# 5. Output file behavior tests
# ---------------------------------------------------------------------------

class TestOutputFile(unittest.TestCase):

    def _mock_api_side_effect(self, companies):
        """Return a side_effect list with a single page response."""
        return [_make_page(companies, total=len(companies))]

    @patch("search_companies.call_api")
    def test_output_file_writes_content(self, mock_api):
        """--output-file writes Markdown to the specified path."""
        companies = [_make_company(i) for i in range(3)]
        mock_api.side_effect = self._mock_api_side_effect(companies)

        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            sc.main.__module__  # ensure import is fine
            with patch("sys.argv", ["search_companies.py",
                                    "--concepts", "生物医药",
                                    "--output-file", tmp_path]):
                sc.main()

            content = Path(tmp_path).read_text(encoding="utf-8")
            self.assertIn("企业简称", content)
            self.assertIn("示例公司1", content)
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    @patch("search_companies.call_api")
    def test_output_file_stdout_is_short(self, mock_api):
        """When --output-file is used, stdout contains only a short confirmation."""
        companies = [_make_company(i) for i in range(3)]
        mock_api.side_effect = self._mock_api_side_effect(companies)

        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            with patch("sys.argv", ["search_companies.py",
                                    "--concepts", "生物医药",
                                    "--output-file", tmp_path]), \
                 patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                sc.main()

            stdout_text = mock_stdout.getvalue()
            lines = [l for l in stdout_text.strip().splitlines() if l]
            self.assertEqual(len(lines), 1, f"stdout should be 1 line, got: {stdout_text!r}")
            self.assertIn("✅", lines[0])
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    @patch("search_companies.call_api")
    def test_output_temp_uses_system_tempdir(self, mock_api):
        """--output-temp writes to tempfile.gettempdir(), works cross-platform."""
        import tempfile as _tempfile
        companies = [_make_company(i) for i in range(3)]
        mock_api.side_effect = self._mock_api_side_effect(companies)

        expected_path = Path(_tempfile.gettempdir()) / "company_scan_result.md"
        # ensure clean state
        if expected_path.exists():
            expected_path.unlink()

        with patch("sys.argv", ["search_companies.py",
                                "--concepts", "生物医药",
                                "--output-temp"]):
            sc.main()

        self.assertTrue(expected_path.exists())
        content = expected_path.read_text(encoding="utf-8")
        self.assertIn("企业简称", content)
        expected_path.unlink()

    @patch("search_companies.call_api")
    def test_output_temp_stdout_contains_path(self, mock_api):
        """--output-temp stdout confirmation message contains the actual file path."""
        import tempfile as _tempfile
        companies = [_make_company(i) for i in range(2)]
        mock_api.side_effect = self._mock_api_side_effect(companies)

        expected_path = str(Path(_tempfile.gettempdir()) / "company_scan_result.md")

        with patch("sys.argv", ["search_companies.py",
                                "--concepts", "生物医药",
                                "--output-temp"]), \
             patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            sc.main()

        stdout_text = mock_stdout.getvalue().strip()
        self.assertIn(expected_path, stdout_text)
        lines = [l for l in stdout_text.splitlines() if l]
        self.assertEqual(len(lines), 1)

        Path(expected_path).unlink(missing_ok=True)

    @patch("search_companies.call_api")
    def test_no_output_file_prints_to_stdout(self, mock_api):
        """Without --output-file, full Markdown is printed to stdout."""
        companies = [_make_company(i) for i in range(3)]
        mock_api.side_effect = self._mock_api_side_effect(companies)

        with patch("sys.argv", ["search_companies.py", "--concepts", "生物医药"]), \
             patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            sc.main()

        stdout_text = mock_stdout.getvalue()
        self.assertIn("企业简称", stdout_text)
        self.assertIn("示例公司1", stdout_text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
