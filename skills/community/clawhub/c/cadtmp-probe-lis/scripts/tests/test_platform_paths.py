#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests for scripts/platform_paths.py（win / darwin / linux 三种模拟输入）。

说明
----
- 纯 stdlib + unittest，不需要外部后端或联网；
- 通过 ``platform_hint`` 显式模拟三平台，用临时目录 + 环境变量注入机器目录；
- 不物理创建 /usr/bin、/Applications 等系统目录。
"""

from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SKILL_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILL_DIR / "scripts"))

import platform_paths as pp  # noqa: E402


def _write_file(path: Path, exec_bit: bool = True) -> Path:
    """创建可被『发现』的模拟可执行文件。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("#!/bin/sh\necho ok\n", encoding="utf-8")
    if exec_bit and os.name != "nt":
        path.chmod(0o755)
    return path


class HomeCodexTest(unittest.TestCase):
    """home_codex() 三平台目录根。"""

    def test_darwin_uses_home(self):
        with tempfile.TemporaryDirectory(prefix="cad-pp-") as td, mock.patch.dict(
            os.environ, {"HOME": td, "USERPROFILE": "/fake/profile"}
        ):
            self.assertEqual(pp.home_codex("darwin"), Path(td) / ".codex")

    def test_linux_uses_home(self):
        with tempfile.TemporaryDirectory(prefix="cad-pp-") as td, mock.patch.dict(
            os.environ, {"HOME": td, "USERPROFILE": "/fake/profile"}
        ):
            self.assertEqual(pp.home_codex("linux"), Path(td) / ".codex")

    def test_win_uses_userprofile(self):
        with tempfile.TemporaryDirectory(prefix="cad-pp-") as td, mock.patch.dict(
            os.environ, {"HOME": "/fake/home", "USERPROFILE": td}
        ):
            self.assertEqual(pp.home_codex("win"), Path(td) / ".codex")


class KnownDirsTest(unittest.TestCase):
    """平台表本身必须覆盖设计里约定的常见目录。"""

    def test_dwg2dxf_win_has_no_table_and_oda_hint(self):
        self.assertEqual(pp.known_dirs("dwg2dxf", "win"), [])
        self.assertIn("ODAFileConverter", pp.tool_hint("dwg2dxf", "win"))
        self.assertEqual(pp.tool_hint("dwg2dxf", "darwin"), "")

    def test_dwg2dxf_darwin_linux_common_paths(self):
        darwin = pp.known_dirs("dwg2dxf", "darwin")
        self.assertIn(Path("/opt/homebrew/bin"), darwin)
        linux = pp.known_dirs("dwg2dxf", "linux")
        self.assertIn("/usr/bin", [p.as_posix() for p in linux])
        self.assertIn("/usr/local/bin", [p.as_posix() for p in linux])

    def test_oda_linux_contains_opt(self):
        self.assertTrue(any(d.as_posix().startswith("/opt") for d in pp.known_dirs("ODAFileConverter", "linux")))

    def test_oda_win_contains_program_files_and_localappdata(self):
        with mock.patch.dict(os.environ, {
            "ProgramFiles": "C:/Program Files",
            "LOCALAPPDATA": "C:/Users/t/AppData/Local",
            "USERPROFILE": "C:/Users/t",
        }):
            joined = "\n".join(sorted(d.as_posix() for d in pp.known_dirs("ODAFileConverter", "win")))
        self.assertIn("C:/Program Files", joined)
        self.assertIn("C:/Users/t/AppData/Local", joined)

    def test_pdftoppm_linux_uses_usr_bin(self):
        self.assertIn(Path("/usr/bin"), pp.known_dirs("pdftoppm", "linux"))

    def test_pdf_venv_uses_bin_for_darwin(self):
        dirs = pp.known_dirs("pdf-inspector-python", "darwin")
        self.assertTrue(all(d.as_posix().endswith("/.venv/bin") for d in dirs))

    def test_pdf_venv_uses_scripts_for_win(self):
        with mock.patch.dict(os.environ, {"USERPROFILE": "C:/Users/t"}):
            dirs = pp.known_dirs("pdf-inspector-python", "win")
        self.assertTrue(all(d.as_posix().endswith("/.venv/Scripts") for d in dirs))

    def test_no_hardcoded_users_or_local_venv_bin(self):
        source = Path(__file__).resolve().parents[1] / "platform_paths.py"
        text = source.read_text(encoding="utf-8")
        self.assertNotIn("/Users", text)
        self.assertNotIn(".venv/bin", text)


class FindToolExtraDirsTest(unittest.TestCase):
    """extra_dirs 在三种模拟平台上都能被找到。"""

    def _make(self, td: Path, name: str) -> Path:
        return _write_file(Path(td) / "bin" / name)

    def test_darwin_finds_via_extra_dir(self):
        with tempfile.TemporaryDirectory(prefix="cad-pp-") as td:
            fake = self._make(Path(td), "fake_tool_empty_name_1")
            got = pp.find_tool("fake_tool_empty_name_1", extra_dirs=[str(Path(td) / "bin")], platform_hint="darwin")
            self.assertEqual(got, str(fake))

    def test_linux_finds_via_extra_dir(self):
        with tempfile.TemporaryDirectory(prefix="cad-pp-") as td:
            fake = self._make(Path(td), "fake_tool_empty_name_2")
            got = pp.find_tool("fake_tool_empty_name_2", extra_dirs=[str(Path(td) / "bin")], platform_hint="linux")
            self.assertEqual(got, str(fake))


class FindToolWinTest(unittest.TestCase):
    """Windows：.exe 后缀、Program Files / LOCALAPPDATA / venv Scripts。"""

    def test_win_finds_exe_in_oda_dir_from_program_files(self):
        with tempfile.TemporaryDirectory(prefix="cad-pp-") as td:
            fake = _write_file(Path(td) / "ODAFileConverter" / "ODAFileConverter.exe")
            with mock.patch.dict(os.environ, {
                "ProgramFiles": str(td), "LOCALAPPDATA": str(td), "USERPROFILE": str(td)
            }):
                got = pp.find_tool("ODAFileConverter", platform_hint="win")
            self.assertEqual(got, str(fake))

    def test_win_finds_pdftoppm_exe_in_poppler_bin(self):
        with tempfile.TemporaryDirectory(prefix="cad-pp-") as td:
            fake = _write_file(Path(td) / "Programs" / "poppler" / "bin" / "pdftoppm.exe")
            with tempfile.TemporaryDirectory(prefix="cad-pp-path-") as pathd, mock.patch.dict(
                os.environ, {
                    "PATH": str(pathd), "LOCALAPPDATA": str(td),
                    "USERPROFILE": str(td), "ProgramFiles": str(td),
                }
            ):
                got = pp.find_tool("pdftoppm", platform_hint="win")
            self.assertEqual(got, str(fake))

    def test_win_finds_venv_python_in_scripts(self):
        with tempfile.TemporaryDirectory(prefix="cad-pp-") as td:
            fake = _write_file(Path(td) / ".codex" / "skills" / "pdf-inspector" / ".venv"
                               / "Scripts" / "python.exe")
            with mock.patch.dict(os.environ, {"USERPROFILE": str(td), "HOME": "/fake/home"}):
                got = pp.find_tool("pdf-inspector-python", platform_hint="win")
            self.assertEqual(got, str(fake))

    def test_win_missing_dwg2dxf_returns_none_with_hint(self):
        with tempfile.TemporaryDirectory(prefix="cad-pp-") as td, mock.patch.dict(
            os.environ, {"PATH": str(td), "USERPROFILE": str(td), "HOME": str(td)}
        ):
            got = pp.find_tool("dwg2dxf", platform_hint="win")
        self.assertIsNone(got)
        self.assertIn("ODA", pp.tool_hint("dwg2dxf", "win"))


class FindToolPathPriorityTest(unittest.TestCase):
    """PATH 必须优先于平台表与 extra_dirs。"""

    def test_path_wins_over_extra_dir(self):
        # 模拟 darwin/linux 的 PATH 优先级：Windows runner 上无 POSIX 执行位且
        # PATHEXT 不强制无扩展名，因此把 _which_path 固定为 PATH 命中的那份，
        # 并 mock 掉执行位判定，只验证 PATH > extra_dirs。
        with tempfile.TemporaryDirectory(prefix="cad-pp-") as td:
            pathdir = Path(td) / "PATH_ONLY"
            pathdir.mkdir(parents=True, exist_ok=True)
            path_tool = _write_file(pathdir / "oda_prefer_path", exec_bit=True)
            # 同一工具名放 platform 表/extra 里的另一份，不应被选中
            extra_fake = _write_file(Path(td) / "extra" / "oda_prefer_path", exec_bit=True)
            with mock.patch.dict(os.environ, {
                "PATH": str(pathdir) + os.pathsep + os.environ.get("PATH", ""),
                "ProgramFiles": str(td),
                "LOCALAPPDATA": str(td),
                "USERPROFILE": str(td),
            }), mock.patch.object(pp, "_is_executable_file", return_value=True), \
                    mock.patch.object(pp, "_which_path", return_value=str(path_tool)):
                got = pp.find_tool("oda_prefer_path", extra_dirs=[str(Path(td) / "extra")], platform_hint="darwin")
            self.assertEqual(got, str(path_tool))
            self.assertNotEqual(got, str(extra_fake))

class OcrandPdfUnixTest(unittest.TestCase):
    """ocr_image / pdf-inspector venv 在 macOS/Linux 的 macOS/Linux 布局。"""

    def test_ocr_image_found_under_home_codex_bin_on_darwin(self):
        with tempfile.TemporaryDirectory(prefix="cad-pp-") as td:
            fake = _write_file(Path(td) / ".codex" / "bin" / "ocr_image")
            with mock.patch.dict(os.environ, {"HOME": str(td), "USERPROFILE": "/fake/profile"}):
                got = pp.find_tool("ocr_image", platform_hint="darwin")
            self.assertEqual(got, str(fake))

    def test_ocr_image_found_under_home_codex_bin_on_linux(self):
        with tempfile.TemporaryDirectory(prefix="cad-pp-") as td:
            fake = _write_file(Path(td) / ".codex" / "bin" / "ocr_image")
            with mock.patch.dict(os.environ, {"HOME": str(td), "USERPROFILE": "/fake/profile"}):
                got = pp.find_tool("ocr_image", platform_hint="linux")
            self.assertEqual(got, str(fake))

    def test_pdf_venv_python_darwin_bin(self):
        with tempfile.TemporaryDirectory(prefix="cad-pp-") as td:
            fake = _write_file(Path(td) / ".codex" / "skills" / "pdf-inspector" / ".venv"
                               / "bin" / "python")
            with mock.patch.dict(os.environ, {"HOME": str(td), "USERPROFILE": "/fake/profile"}):
                got = pp.find_tool("pdf-inspector-python", platform_hint="darwin")
            self.assertEqual(got, str(fake))

    def test_pdf_venv_python_linux_bin(self):
        with tempfile.TemporaryDirectory(prefix="cad-pp-") as td:
            fake = _write_file(Path(td) / ".codex" / "skills" / "pdf-inspector" / ".venv"
                               / "bin" / "python")
            with mock.patch.dict(os.environ, {"HOME": str(td), "USERPROFILE": "/fake/profile"}):
                got = pp.find_tool("pdf-inspector-python", platform_hint="linux")
            self.assertEqual(got, str(fake))


class PdfVenvEnvOverrideTest(unittest.TestCase):
    """PDF_INSPECTOR_ROOT / PDF_INSPECTOR_VENV 环境变量优先。"""

    def test_win_uses_env_venv_root(self):
        with tempfile.TemporaryDirectory(prefix="cad-pp-") as td, mock.patch.dict(
            os.environ, {"USERPROFILE": str(td), "HOME": "/fake/h"}
        ):
            root = Path(td) / "custom"
            fake = _write_file(root / ".venv" / "Scripts" / "python.exe")
            with mock.patch.dict(os.environ, {"PDF_INSPECTOR_ROOT": str(root)}):
                got = pp.find_tool("pdf-inspector-python", platform_hint="win")
            self.assertEqual(got, str(fake))


if __name__ == "__main__":
    unittest.main()
