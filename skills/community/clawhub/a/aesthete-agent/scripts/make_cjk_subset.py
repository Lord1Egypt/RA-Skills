#!/usr/bin/env python3
"""make_cjk_subset.py — build a tiny woff2 subset of a CJK serif font for page titles.

Why: CJK system serif fonts (SimSun/Songti SC) have no bold weight, so Chinese
headlines cannot carry the visual weight their Latin counterparts get from
Georgia 800. The fix is a real heavy weight from Source Han Serif / Noto Serif SC
(OFL-1.1, free to embed), subsetted down to just the headline characters.

Measured with fonttools 4.62: full Noto Serif CJK SC Bold = 24.3MB;
a ~190-character page-title subset = 67KB woff2 (99.7% smaller).

Optional dependency (like Pillow for image extraction):
    pip install fonttools brotli

Usage:
    python make_cjk_subset.py --text "标题文字" --out cjk-title.woff2
    python make_cjk_subset.py --text-file chars.txt --weight Heavy --out title.woff2
    python make_cjk_subset.py --text "..." --css  # also print the @font-face block
"""
import argparse
import sys
from pathlib import Path

# Source Han Serif release assets (Adobe, OFL-1.1). Weight name -> file name
# in https://github.com/adobe-fonts/source-han-serif/releases (SubsetOTF/CN/)
SOURCE_HAN_SERIF_CN = {
    "Bold": "SourceHanSerifCN-Bold.otf",
    "Heavy": "SourceHanSerifCN-Heavy.otf",
    "SemiBold": "SourceHanSerifCN-SemiBold.otf",
    "Medium": "SourceHanSerifCN-Medium.otf",
    "Regular": "SourceHanSerifCN-Regular.otf",
}
DOWNLOAD_URL = ("https://github.com/adobe-fonts/source-han-serif/releases/download/"
                "2.003R/09_SourceHanSerifCN.zip")
# 命名对照:Adobe 思源宋最重字重叫 Heavy;Google/Noto 侧同源字重叫 Black(≈900)。
# 文档/下载链接互指时注意别名——Noto CJK 没有 "Heavy" 这个字重名。

DEFAULT_PUNCT = "，。：；！？·—｜、（）「」『』“”‘’…"


def build(text, weight, font_path, out_path):
    try:
        from fontTools import subset
    except ImportError:
        print("ERROR: fonttools not installed. Run: pip install fonttools brotli",
              file=sys.stderr)
        return 2

    chars = sorted(set(text))
    css_ready = out_path.endswith(".woff2")
    argv = [
        str(font_path),
        "--text=" + "".join(chars),
        "--flavor=woff2" if css_ready else "",
        "--output-file=" + str(out_path),
        "--layout-features=*",
        "--no-hinting",
    ]
    subset.main([a for a in argv if a])
    size = Path(out_path).stat().st_size
    print(f"subset: {len(chars)} chars -> {out_path} ({size/1024:.1f} KB)")
    return 0


def font_face_css(out_path, weight, family="CJK Serif Title"):
    return (f'@font-face{{\n  font-family:"{family}";\n'
            f'  src:url("{out_path}") format("woff2");\n'
            f'  font-display:swap; font-weight:{weight};\n}}')


def main():
    ap = argparse.ArgumentParser(description="CJK title-font subset builder")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--text", help="headline text (all chars join the subset)")
    src.add_argument("--text-file", help="file whose characters join the subset")
    ap.add_argument("--weight", default="Bold", choices=sorted(SOURCE_HAN_SERIF_CN),
                    help="source weight (default Bold; Heavy=900 for hero titles)")
    ap.add_argument("--font", help="local font file (default: download Source Han Serif CN)")
    ap.add_argument("--out", default="cjk-title.woff2")
    ap.add_argument("--css", action="store_true", help="also print the @font-face block")
    a = ap.parse_args()

    try:
        from fontTools import subset  # noqa: F401
        import brotli  # noqa: F401
    except ImportError:
        print("ERROR: requires fonttools + brotli. Run: pip install fonttools brotli",
              file=sys.stderr)
        return 2

    text = Path(a.text_file).read_text(encoding="utf-8") if a.text_file else a.text
    text += DEFAULT_PUNCT

    font = Path(a.font) if a.font else Path(f"SourceHanSerifCN-{a.weight}.otf")
    if not font.exists():
        print(f"Font file not found: {font}\n"
              f"Download {a.weight} from:\n  {DOWNLOAD_URL}\n"
              f"(unzip SubsetOTF/CN/{SOURCE_HAN_SERIF_CN[a.weight]}, then pass --font)",
              file=sys.stderr)
        return 1

    rc = build(text, a.weight, font, a.out)
    if rc == 0 and a.css:
        print(font_face_css(a.out, {"Bold": 700, "Heavy": 900, "SemiBold": 600,
                                    "Medium": 500, "Regular": 400}[a.weight]))
    return rc


if __name__ == "__main__":
    sys.exit(main())
