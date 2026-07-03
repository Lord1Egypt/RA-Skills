"""build_epub.py
将一个目录打包为合规的 EPUB 文件。

用法：
    python build_epub.py <src_dir> <out.epub>

EPUB 规范要点：
- mimetype 必须是 zip 中第一个条目
- mimetype 必须 STORED（不压缩）、内容固定为 application/epub+zip
- 其他文件可 DEFLATE 压缩

注意：不要用 PowerShell 的 Compress-Archive，它生成的 zip 不满足上述要求。
"""
import os
import sys
import zipfile
from pathlib import Path


def build_epub(src_dir: Path, out_file: Path) -> None:
    """将 src_dir 打包为符合 EPUB 规范的 out_file。"""
    if not src_dir.is_dir():
        raise SystemExit(f"源目录不存在：{src_dir}")

    # 确保 mimetype 文件存在且内容正确
    mimetype_path = src_dir / "mimetype"
    mimetype_path.write_text("application/epub+zip", encoding="ascii")

    if out_file.exists():
        out_file.unlink()

    with zipfile.ZipFile(out_file, "w", zipfile.ZIP_DEFLATED) as zf:
        # 1) 第一个写入 mimetype，且 STORED（不压缩、不带 extra）
        zi = zipfile.ZipInfo("mimetype")
        zi.compress_type = zipfile.ZIP_STORED
        zi.external_attr = 0o644 << 16
        zf.writestr(zi, "application/epub+zip")

        # 2) 其余文件按 DEFLATE 压缩添加
        added = {"mimetype"}
        for root, _, files in os.walk(src_dir):
            for name in files:
                full = Path(root) / name
                rel = full.relative_to(src_dir).as_posix()
                if rel in added:
                    continue
                zf.write(full, rel, compress_type=zipfile.ZIP_DEFLATED)
                added.add(rel)

    # 3) 自检
    with zipfile.ZipFile(out_file) as z:
        names = z.namelist()
        assert names[0] == "mimetype", "mimetype 必须是 zip 中的第一个条目"
        assert z.getinfo("mimetype").compress_type == zipfile.ZIP_STORED, \
            "mimetype 必须未压缩（STORED）"
        assert z.read("mimetype") == b"application/epub+zip", \
            "mimetype 内容必须是 application/epub+zip"

    size_mb = out_file.stat().st_size / (1024 * 1024)
    print(f"已生成 EPUB：{out_file}")
    print(f"大小：{size_mb:.2f} MB，条目数：{len(names)}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法：python build_epub.py <src_dir> <out.epub>")
        sys.exit(1)
    build_epub(Path(sys.argv[1]), Path(sys.argv[2]))
