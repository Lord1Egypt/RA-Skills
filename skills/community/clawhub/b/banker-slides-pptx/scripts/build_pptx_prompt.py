#!/usr/bin/env python3
"""Parameterise the banker-slides-pptx prompt for a company whose analysis.md
is already written by the banker-memo-md skill.

Usage:
    python3 build_pptx_prompt.py <deliverable_dir> <ts_code> <name_cn> <name_en>
"""
from __future__ import annotations
import pathlib, sys


def main() -> int:
    if len(sys.argv) != 5:
        sys.exit("usage: build_pptx_prompt.py <deliverable> <ts_code> <name_cn> <name_en>")
    d, ts_code, name_cn, name_en = sys.argv[1:5]
    dp = pathlib.Path(d).resolve()
    analysis_md = dp / "analysis.md"
    provenance_md = dp / "data-provenance.md"
    if not analysis_md.exists() or not provenance_md.exists():
        sys.exit(f"pre-flight failed: need both {analysis_md} and {provenance_md} "
                 "(run banker-memo-md first)")

    tmpl = (pathlib.Path(__file__).resolve().parent.parent /
            "references" / "banker_slides_prompt.md").read_text(encoding="utf-8")

    out = (tmpl
        .replace("{ts_code}", ts_code)
        .replace("{name_cn}", name_cn)
        .replace("{name_en}", name_en)
        .replace("{deliverable_dir}", str(dp))
        .replace("{analysis_md}", str(analysis_md))
        .replace("{provenance_md}", str(provenance_md)))

    # Include the actual analysis.md + provenance.md content inline so the
    # agent can extract the numbers without needing filesystem reads during
    # its turn. This keeps the prompt self-contained.
    print(out)
    print("\n---\n## Inline `analysis.md` content (已写好，供你提取数字)\n")
    print("```markdown")
    print(analysis_md.read_text(encoding="utf-8"))
    print("```\n")
    print("## Inline `data-provenance.md` content\n")
    print("```markdown")
    print(provenance_md.read_text(encoding="utf-8"))
    print("```\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
