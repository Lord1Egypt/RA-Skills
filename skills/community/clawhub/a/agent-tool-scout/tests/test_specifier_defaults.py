"""Tests for specifier defaults — smart default values for specifier/document types."""

import tempfile
from pathlib import Path

import pytest

from clam.generator.applescript_gen import check_command_support, generate_wrapper
from clam.generator.specifier_defaults import DOCUMENT_DEFAULT, get_specifier_default
from clam.scanner.app_scanner import find_app
from clam.scanner.sdef_parser import parse_sdef


class TestSpecifierDefaults:
    def test_chrome_specifier_default(self):
        assert get_specifier_default("google-chrome", "specifier") == "active tab of window 1"

    def test_arc_specifier_default(self):
        assert get_specifier_default("arc", "specifier") == "active tab of window 1"

    def test_finder_specifier_default(self):
        assert get_specifier_default("finder", "specifier") is not None

    def test_document_default(self):
        assert get_specifier_default("keynote", "document") == DOCUMENT_DEFAULT

    def test_document_default_any_app(self):
        assert get_specifier_default("any-random-app", "document") == DOCUMENT_DEFAULT

    def test_no_default_for_unknown_type(self):
        assert get_specifier_default("google-chrome", "range") is None

    def test_no_default_for_unknown_app(self):
        assert get_specifier_default("unknown-app", "specifier") is None


@pytest.fixture(scope="module")
def chrome_sdef():
    app = find_app("google-chrome")
    if not app:
        pytest.skip("Google Chrome not installed")
    return parse_sdef(app.sdef_path, app.name)


@pytest.fixture(scope="module")
def keynote_sdef():
    app = find_app("keynote")
    if not app:
        pytest.skip("Keynote not installed")
    return parse_sdef(app.sdef_path, app.name)


class TestChromeSupport:
    def test_reload_is_supported(self, chrome_sdef):
        results = check_command_support(chrome_sdef, "google-chrome")
        reload = next(r for r in results if r["name"] == "reload")
        assert reload["supported"]

    def test_go_back_is_supported(self, chrome_sdef):
        results = check_command_support(chrome_sdef, "google-chrome")
        go_back = next(r for r in results if r["name"] == "go-back")
        assert go_back["supported"]

    def test_execute_is_supported(self, chrome_sdef):
        results = check_command_support(chrome_sdef, "google-chrome")
        execute = next(r for r in results if r["name"] == "execute")
        assert execute["supported"]

    def test_make_still_unsupported(self, chrome_sdef):
        """make has 'type' and 'record' params — still unsupported."""
        results = check_command_support(chrome_sdef, "google-chrome")
        make = next(r for r in results if r["name"] == "make")
        assert not make["supported"]

    def test_support_rate_improved(self, chrome_sdef):
        results = check_command_support(chrome_sdef, "google-chrome")
        supported = sum(1 for r in results if r["supported"])
        assert supported >= 15  # was 1, now at least 15


class TestKeynoteSupport:
    def test_stop_is_supported(self, keynote_sdef):
        results = check_command_support(keynote_sdef, "keynote")
        stop = next(r for r in results if r["name"] == "stop")
        assert stop["supported"]

    def test_slide_switcher_supported(self, keynote_sdef):
        results = check_command_support(keynote_sdef, "keynote")
        show = next(r for r in results if r["name"] == "show-slide-switcher")
        assert show["supported"]

    def test_support_rate_improved(self, keynote_sdef):
        results = check_command_support(keynote_sdef, "keynote")
        supported = sum(1 for r in results if r["supported"])
        assert supported >= 8  # was 2, now at least 8


class TestGeneratedCode:
    def test_chrome_reload_has_target_default(self, chrome_sdef):
        with tempfile.TemporaryDirectory() as tmpdir:
            generate_wrapper(chrome_sdef, Path(tmpdir))
            import glob
            cli_file = glob.glob(f"{tmpdir}/cli_*.py")[0]
            code = Path(cli_file).read_text()
            assert "active tab of window 1" in code

    def test_chrome_reload_target_is_optional(self, chrome_sdef):
        with tempfile.TemporaryDirectory() as tmpdir:
            generate_wrapper(chrome_sdef, Path(tmpdir))
            import glob
            cli_file = glob.glob(f"{tmpdir}/cli_*.py")[0]
            code = Path(cli_file).read_text()
            # Find reload command — target should be optional
            assert 'required=False' in code

    def test_keynote_stop_has_front_document(self, keynote_sdef):
        with tempfile.TemporaryDirectory() as tmpdir:
            generate_wrapper(keynote_sdef, Path(tmpdir))
            import glob
            cli_file = glob.glob(f"{tmpdir}/cli_*.py")[0]
            code = Path(cli_file).read_text()
            assert "front document" in code
