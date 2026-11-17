#!/usr/bin/env python3
"""Регрессионные тесты разрезателя (без внешних зависимостей).

Покрывают в том числе дефекты, найденные независимым аудитом 24.09.2026:
  A  — мелкий хвост разделов не должен пробивать --budget;
  A2 — фильтр «что резать» считается в символах, а не в байтах;
  B  — два раздела с ОДИНАКОВЫМ заголовком дают два файла и две строки указателя;
  C  — --verify-only возвращает ненулевой код при потере и при отсутствии бэкапов.

Запуск:  python3 scripts/test_split_skills.py
Пишет только в свою песочницу (/tmp) и удаляет её за собой.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "split_skills.py"
PY = sys.executable


def run(*args, **kw):
    return subprocess.run([PY, str(SCRIPT), *map(str, args)], capture_output=True,
                          text=True, **kw)


def mk_skill(root: Path, name: str, body: str) -> Path:
    d = root / "demo" / name
    d.mkdir(parents=True, exist_ok=True)
    (d / "SKILL.md").write_text(body, encoding="utf-8")
    return d


def check(label: str, cond: bool, detail: str = "") -> bool:
    print(f"  {'✓' if cond else '✗'} {label}{(' — ' + detail) if detail else ''}")
    return cond


def main() -> int:
    ok = True
    with tempfile.TemporaryDirectory(prefix="split-test-") as tmp:
        root = Path(tmp) / "root"
        bak = Path(tmp) / "bak"

        # --- A: хвост не пробивает бюджет (граница) ---
        h2 = "".join(f"## Section {i}\n" + "y" * 110 + "\n" for i in range(167))
        d = mk_skill(root, "boundary", f"---\nname: boundary\n---\n\nintro\n{h2}")
        r = run("--root", root, d, "--apply", "--backup-dir", bak)
        txt = (d / "SKILL.md").read_text(encoding="utf-8")
        ok &= check("A: после --apply файл ≤ бюджета либо честный skip",
                    len(txt) <= 20000 or "в бюджете" in r.stdout,
                    f"{len(txt)} симв")

        # --- B: одинаковые заголовки → два файла и две строки указателя ---
        shutil.rmtree(root, ignore_errors=True)
        body = ("---\nname: dup\n---\n\n# Dup\n\n## Duplicate Title\n" + "a" * 3000 +
                "\n## Duplicate Title\n" + "b" * 3000 +
                "\n## Different\n" + "c" * 3000 + "\n")
        d = mk_skill(root, "dup", body)
        r = run("--root", root, d, "--apply", "--backup-dir", bak, "--chunk", "3000",
                "--budget", "1000")
        refs = sorted(p.name for p in (d / "references").glob("*.md"))
        toc = (d / "SKILL.md").read_text(encoding="utf-8").count("references/")
        ok &= check("B: одинаковые заголовки не схлопнулись", len(refs) >= 2 and toc >= 2,
                    f"файлов {len(refs)}, строк указателя {toc}")

        # --- C1: --verify-only без бэкапов → ненулевой код ---
        r = run("--root", root, "--verify-only", "--backup-dir", Path(tmp) / "no-backups")
        ok &= check("C1: пустой каталог бэкапов → exit≠0", r.returncode != 0,
                    f"exit={r.returncode}")

        # --- C2: потеря файла ловится и даёт ненулевой код ---
        victim = sorted((d / "references").glob("*.md"))[0]
        victim.write_text("подменено", encoding="utf-8")
        r = run("--root", root, "--verify-only", "--backup-dir", bak)
        ok &= check("C2: потеря заголовков → exit≠0 и слово ПОТЕРЯНО",
                    r.returncode != 0 and "ПОТЕРЯНО" in r.stdout,
                    f"exit={r.returncode}")

        # --- A2: скилл у границы бюджета в байтах, но меньше в символах ---
        shutil.rmtree(root, ignore_errors=True)
        d = mk_skill(root, "cyr", "---\nname: cyr\n---\n\n" + "## Ы\n" + "ы" * 6000 + "\n")
        chars = len((d / "SKILL.md").read_text(encoding="utf-8"))
        r = run("--root", root)          # сухой прогон: цель задана неявно, через --root
        ok &= check("A2: граница считается в символах",
                    ("cyr" in r.stdout) == (chars > 20000), f"{chars} симв")

    print("\nИТОГ:", "все тесты пройдены" if ok else "ЕСТЬ ПАДЕНИЯ")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
