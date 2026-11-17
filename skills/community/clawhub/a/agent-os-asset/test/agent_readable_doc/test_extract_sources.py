from __future__ import annotations

from pathlib import Path
import zipfile

import pytest

from support import load_skill_script


extract_sources = load_skill_script("extract_sources.py")

DOC_XML = b"""<?xml version="1.0" encoding="UTF-8"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body><w:p><w:r><w:t>Hello</w:t></w:r></w:p></w:body>
</w:document>
"""
PPT_XML = b"""<?xml version="1.0" encoding="UTF-8"?>
<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
       xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
  <p:cSld><a:t>Hello slide</a:t></p:cSld>
</p:sld>
"""


def write_docx(path: Path, members: dict[str, bytes]) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("word/document.xml", DOC_XML)
        for name, data in members.items():
            archive.writestr(name, data)


def write_pptx(path: Path, members: dict[str, bytes]) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("ppt/slides/slide1.xml", PPT_XML)
        for name, data in members.items():
            archive.writestr(name, data)


def test_html_parser_adds_default_image_width() -> None:
    parser = extract_sources.BodyHTMLParser()
    parser.feed('<article><img src="chart.png" alt="chart"></article>')

    assert "![chart|560](chart.png)" in parser.markdown()


@pytest.mark.parametrize("kind", ["parent", "percent-parent", "absolute", "symlink", "hidden", "sensitive", "not-image", "hardlink", "pii-directory", "remote", "oversized"])
def test_html_images_cannot_copy_unapproved_local_files(tmp_path: Path, kind: str) -> None:
    import os
    import shutil
    from unittest.mock import patch

    documents = tmp_path / "documents"
    documents.mkdir()
    outside = tmp_path / "outside.png"
    outside.write_bytes(b"PRIVATE_SENTINEL")
    source = documents / "note.html"
    if kind == "parent":
        src = "../outside.png"
    elif kind == "percent-parent":
        src = "%2e%2e/outside.png"
    elif kind == "remote":
        src = "https://example.invalid/tracking.png"
    elif kind == "absolute":
        src = str(outside)
    elif kind == "symlink":
        (documents / "alias.png").symlink_to(outside)
        src = "alias.png"
    elif kind == "hardlink":
        os.link(outside, documents / "alias.png")
        src = "alias.png"
    elif kind == "pii-directory":
        (documents / "PII").mkdir()
        (documents / "PII" / "chart.png").write_bytes(b"PRIVATE_SENTINEL")
        src = "PII/chart.png"
    elif kind == "oversized":
        src = "large.png"
        with (documents / src).open("wb") as stream:
            stream.truncate(16 * 1024 * 1024 + 1)
    else:
        src = {"hidden": ".private.png", "sensitive": "api-token.png", "not-image": "private.txt"}[kind]
        (documents / src).write_bytes(b"PRIVATE_SENTINEL")
    source.write_text(f'<article><img src="{src}"></article>')
    with patch.object(shutil, "copy2", wraps=shutil.copy2) as copy:
        result = extract_sources.extract_html(source, tmp_path / "normalized", tmp_path / "assets")
    assert result["assets"] == []
    copy.assert_not_called()
    assert result["warnings"]
    assert not (tmp_path / "assets").exists()
    assert "![" not in Path(result["normalized"]).read_text()


def test_html_images_preserve_safe_relative_companions(tmp_path: Path) -> None:
    image = tmp_path / "images" / "chart.png"
    image.parent.mkdir()
    image.write_bytes(b"synthetic-image")
    source = tmp_path / "note.html"
    source.write_text('<img src="images/chart.png">')
    result = extract_sources.extract_html(source, tmp_path / "normalized", tmp_path / "assets")
    assert len(result["assets"]) == 1
    assert Path(result["assets"][0]).read_bytes() == b"synthetic-image"


def test_shell_extraction_adds_bilingual_heading_and_warning(tmp_path: Path) -> None:
    source = tmp_path / "deploy.sh"
    source.write_text("echo hello\n", encoding="utf-8")

    result = extract_sources.extract_text_file(source, tmp_path / "normalized")

    normalized = Path(result["normalized"]).read_text(encoding="utf-8")
    assert "# Shell Script / Shell 脚本: deploy.sh" in normalized
    assert "Warning: no shebang was found in this script. / 警告：此脚本未发现 shebang。" in normalized


def test_docx_extraction_accepts_normal_office_archive(tmp_path: Path) -> None:
    source = tmp_path / "safe.docx"
    write_docx(source, {"word/media/chart.png": b"png"})

    result = extract_sources.extract_docx(source, tmp_path / "normalized", tmp_path / "assets")

    assert result["status"] == "ok"
    assert "Hello" in Path(result["normalized"]).read_text(encoding="utf-8")
    assert len(result["assets"]) == 1


@pytest.mark.parametrize(
    "member_name",
    ["../escape.txt", "word/media/../../escape.png", "word\\media\\..\\..\\escape.png", "/absolute.txt"],
)
def test_docx_rejects_zip_traversal_members(tmp_path: Path, member_name: str) -> None:
    source = tmp_path / "unsafe.docx"
    write_docx(source, {member_name: b"unsafe"})

    with pytest.raises(extract_sources.ExtractionError, match="unsafe archive member path"):
        extract_sources.extract_docx(source, tmp_path / "normalized", tmp_path / "assets")


def test_docx_rejects_xml_doctype_and_entities(tmp_path: Path) -> None:
    source = tmp_path / "entity.docx"
    xml = b"""<?xml version="1.0"?>
<!DOCTYPE w:document [<!ENTITY payload "unsafe">]>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body><w:p><w:r><w:t>&payload;</w:t></w:r></w:p></w:body>
</w:document>
"""
    with zipfile.ZipFile(source, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("word/document.xml", xml)

    with pytest.raises(extract_sources.ExtractionError, match="DTD or entity"):
        extract_sources.extract_docx(source, tmp_path / "normalized", tmp_path / "assets")


def test_docx_rejects_high_compression_ratio_member(tmp_path: Path) -> None:
    source = tmp_path / "bomb.docx"
    write_docx(source, {"word/media/bomb.bin": b"A" * 1_000_000})

    with pytest.raises(extract_sources.ExtractionError, match="compression ratio"):
        extract_sources.extract_docx(source, tmp_path / "normalized", tmp_path / "assets")


def test_docx_rejects_member_count_abuse(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    source = tmp_path / "many.docx"
    write_docx(source, {"word/media/one.bin": b"1", "word/media/two.bin": b"2"})
    monkeypatch.setattr(extract_sources, "MAX_ARCHIVE_MEMBERS", 2)

    with pytest.raises(extract_sources.ExtractionError, match="too many members"):
        extract_sources.extract_docx(source, tmp_path / "normalized", tmp_path / "assets")


def test_docx_wraps_invalid_zip_as_extraction_error(tmp_path: Path) -> None:
    source = tmp_path / "broken.docx"
    source.write_bytes(b"not a zip")

    with pytest.raises(extract_sources.ExtractionError, match="Invalid Office archive"):
        extract_sources.extract_docx(source, tmp_path / "normalized", tmp_path / "assets")


def test_pptx_uses_same_archive_path_guard(tmp_path: Path) -> None:
    source = tmp_path / "unsafe.pptx"
    write_pptx(source, {"ppt/media/../../escape.png": b"unsafe"})

    with pytest.raises(extract_sources.ExtractionError, match="unsafe archive member path"):
        extract_sources.extract_pptx(source, tmp_path / "normalized", tmp_path / "assets")
