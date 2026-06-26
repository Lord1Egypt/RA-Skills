from __future__ import annotations

import unittest
from unittest.mock import patch

import digital_oracle.providers.yahoo as yahoo_provider
from digital_oracle.providers.yahoo import _YFinancePriceFetcher


class YFinancePriceFetcherImportTests(unittest.TestCase):
    def test_prefers_global_install_before_repo_local_deps(self) -> None:
        fake_yf = object()
        with patch.object(yahoo_provider.importlib, "import_module", return_value=fake_yf) as import_module:
            fetcher = _YFinancePriceFetcher()

        self.assertIs(fetcher._yf, fake_yf)
        import_module.assert_called_once_with("yfinance")

    def test_falls_back_to_repo_local_deps_when_global_import_missing(self) -> None:
        fake_yf = object()
        deps_path = "/tmp/digital-oracle/.deps"
        with patch.object(yahoo_provider.importlib, "import_module", side_effect=[ImportError(), fake_yf]) as import_module:
            with patch.object(yahoo_provider.os.path, "isdir", return_value=True):
                with patch.object(yahoo_provider.os.path, "abspath", return_value=f"{deps_path}/digital_oracle/providers/yahoo.py"):
                    with patch.object(yahoo_provider.sys, "path", []):
                        fetcher = _YFinancePriceFetcher()

        self.assertIs(fetcher._yf, fake_yf)
        self.assertEqual(import_module.call_count, 2)


if __name__ == "__main__":
    unittest.main()
