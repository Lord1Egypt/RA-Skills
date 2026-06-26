from __future__ import annotations

from pathlib import Path

from business_blueprint import render_png


def test_render_png_reports_skipped_when_cairosvg_is_missing(monkeypatch, tmp_path: Path) -> None:
    svg = tmp_path / "diagram.svg"
    svg.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10"></svg>', encoding="utf-8")

    monkeypatch.setattr(render_png, "_import_cairosvg", lambda: None)

    result = render_png.render_svg_to_png(svg)

    assert result.ok is False
    assert result.skipped is True
    assert result.reason == "cairosvg_unavailable"


def test_render_png_uses_cairosvg_when_available(monkeypatch, tmp_path: Path) -> None:
    svg = tmp_path / "diagram.svg"
    png = tmp_path / "diagram.png"
    svg.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10"></svg>', encoding="utf-8")

    class FakeCairoSvg:
        @staticmethod
        def svg2png(url: str, write_to: str, scale: float) -> None:
            assert url == str(svg)
            assert scale == 2
            Path(write_to).write_bytes(b"PNG")

    monkeypatch.setattr(render_png, "_import_cairosvg", lambda: FakeCairoSvg)

    result = render_png.render_svg_to_png(svg, png, scale=2)

    assert result.ok is True
    assert result.skipped is False
    assert result.png_path == png
    assert png.read_bytes() == b"PNG"
