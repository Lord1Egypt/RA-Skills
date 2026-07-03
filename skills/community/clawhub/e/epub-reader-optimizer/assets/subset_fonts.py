"""subset_fonts.py
从 EPUB 的 xhtml 章节中收集实际用到的字符，将 TTF 字体子集化后转成 WOFF2 嵌入。

依赖：pip install fonttools brotli

用法：
    python subset_fonts.py <epub_OEBPS_dir>

会在 OEBPS_DIR/Fonts 下产出 LXGWWenKai.woff2 和 LXGWWenKaiMono.woff2。
前提：OEBPS_DIR/Fonts 下已有完整版的 LXGWWenKaiLite-Regular.ttf 和 LXGWWenKaiMonoLite-Regular.ttf。
"""
import re
import sys
from pathlib import Path
from fontTools.subset import Subsetter, Options
from fontTools.ttLib import TTFont


def collect_chars(oebps_dir: Path) -> set:
    chars = set()
    for xhtml in (oebps_dir / "Text").glob("*.xhtml"):
        txt = re.sub(r"<[^>]+>", " ", xhtml.read_text(encoding="utf-8"))
        chars.update(txt)
    # 兜底：ASCII 可见字符(空格到 ~)
    chars.update(chr(c) for c in range(0x20, 0x7F))
    # CJK 标点
    chars.update(chr(c) for c in range(0x3000, 0x3040))
    # 全角 ASCII
    chars.update(chr(c) for c in range(0xFF00, 0xFFF0))
    return chars


def subset_ttf_to_woff2(ttf_path: Path, out_path: Path, char_set: set) -> None:
    font = TTFont(str(ttf_path))
    opts = Options()
    opts.flavor = "woff2"
    opts.desubroutinize = True
    opts.layout_features = ["*"]
    opts.name_IDs = ["*"]
    opts.notdef_outline = True
    opts.recommended_glyphs = True
    sub = Subsetter(options=opts)
    sub.populate(text="".join(sorted(char_set)))
    sub.subset(font)
    font.flavor = "woff2"
    font.save(str(out_path))
    before = ttf_path.stat().st_size
    after = out_path.stat().st_size
    print(f"  ✅ {ttf_path.name} ({before:,} → {after:,} bytes, {before/after:.1f}×)")


def main(oebps_dir: Path) -> None:
    if not oebps_dir.is_dir():
        raise SystemExit(f"目录不存在：{oebps_dir}")

    chars = collect_chars(oebps_dir)
    print(f"📊 共收集 {len(chars)} 个唯一字符")

    fonts_dir = oebps_dir / "Fonts"
    fonts_dir.mkdir(parents=True, exist_ok=True)

    mapping = [
        ("LXGWWenKaiLite-Regular.ttf", "LXGWWenKai.woff2"),
        ("LXGWWenKaiMonoLite-Regular.ttf", "LXGWWenKaiMono.woff2"),
    ]

    for src_name, out_name in mapping:
        src = fonts_dir / src_name
        out = fonts_dir / out_name
        if not src.exists():
            print(f"  ⚠️  跳过，未找到 {src_name}")
            continue
        subset_ttf_to_woff2(src, out, chars)
        src.unlink()  # 删除源 TTF，EPUB 只带 WOFF2

    print(f"\n完成。子集中字体在：{fonts_dir}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法：python subset_fonts.py <epub_OEBPS_dir>")
        sys.exit(1)
    main(Path(sys.argv[1]))
