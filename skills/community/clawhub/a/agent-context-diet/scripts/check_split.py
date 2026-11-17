#!/usr/bin/env python3
"""Независимая сверка разреза: ни одна строка исходника не потерялась.

Заголовки — не единственное, что может потеряться: раздел мог переехать не целиком.
Скрипт сверяет **все непустые строки** исходного файла с суммой SKILL.md ∪ references/
и печатает, сколько строк и где потеряно.

Запуск:
    python3 check_split.py <бэкап SKILL.md> <каталог скилла>
    python3 check_split.py <бэкап SKILL.md> <каталог скилла> --quiet

Код возврата: 0 — всё на месте (или показана справка); 1 — есть потерянные строки;
2 — не найдены входные файлы.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def lines_of(path: Path) -> list[str]:
    return [ln for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Сверить, что после разреза скилла не потерялась ни одна строка.")
    ap.add_argument("source", nargs="?", help="бэкап исходного SKILL.md")
    ap.add_argument("skill_dir", nargs="?", help="каталог скилла (или путь к его SKILL.md)")
    ap.add_argument("--quiet", action="store_true", help="только код возврата, без вывода")
    args = ap.parse_args()

    if not args.source or not args.skill_dir:
        ap.print_help()
        return 0

    src = Path(args.source)
    skill_dir = Path(args.skill_dir)
    skill_md = skill_dir / "SKILL.md" if skill_dir.is_dir() else skill_dir
    if not src.exists() or not skill_md.exists():
        print(f"нет входных файлов: {src} / {skill_md}")
        return 2

    parts = [skill_md] + (sorted((skill_md.parent / "references").glob("*.md"))
                          if (skill_md.parent / "references").is_dir() else [])
    joined = "\n".join(p.read_text(encoding="utf-8") for p in parts)

    src_lines = lines_of(src)
    missing = [ln for ln in src_lines if ln not in joined]
    if not args.quiet:
        print(f"исходник: {src.name} ({len(src_lines):,} непустых строк)")
        print(f"частей: {len(parts)} (SKILL.md + references)")
        print(f"потеряно строк: {len(missing)}")
        for ln in missing[:5]:
            print(f"  – {ln[:100]}")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
