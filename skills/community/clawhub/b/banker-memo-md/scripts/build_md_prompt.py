#!/usr/bin/env python3
"""Parameterise the banker-memo-md prompt template for a CN listed company.

Usage:
    python3 build_md_prompt.py <ts_code> <name_cn> <industry> <raw_data_dir> <output_dir>

Outputs the full prompt to stdout."""
from __future__ import annotations
import glob, pathlib, sys


def main() -> int:
    if len(sys.argv) != 6:
        sys.exit("usage: build_md_prompt.py <ts_code> <name_cn> <industry> "
                 "<raw_dir> <out_dir>")
    ts_code, name_cn, industry, raw_dir, out_dir = sys.argv[1:6]

    tmpl = (pathlib.Path(__file__).resolve().parent.parent /
            "references" / "banker_memo_md_prompt.md").read_text(encoding="utf-8")

    files = sorted(glob.glob(f"{raw_dir}/*.json"))
    file_list = "\n".join(f"- `{pathlib.Path(f).name}`" for f in files) or \
                "(raw-data/ is empty — run cn-client-investigation Phase 3.5 first)"
    uscc = next((pathlib.Path(f).stem.split("-primematrix-")[0]
                 for f in files if "primematrix" in pathlib.Path(f).name), "N/A")

    out = (tmpl
        .replace("{ts_code}", ts_code)
        .replace("{name_cn}", name_cn)
        .replace("{industry}", industry)
        .replace("{raw_dir}", raw_dir)
        .replace("{out_dir}", out_dir)
        .replace("{file_list}", file_list)
        .replace("{uscc}", uscc))
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
