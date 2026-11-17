#!/usr/bin/env python3
"""split_skills.py — разрезает скиллы-монолиты: SKILL.md → SKILL.md + references/*.md.

Зачем: дамп скилла попадает в контекст агента ЦЕЛИКОМ и не сжимается. Скилл на 100 000
символов — это ~25 000 токенов в каждом запросе, где он загружен. Замерено: у одного
агента выводы инструментов дали 87 % объёма запроса, а тяжелейшие блоки — дампы скиллов
по 90–98 тыс. символов, повторяющиеся 2–10 раз за сессию. Разрез возвращает ~80 % контекста.

Что делает:
  * frontmatter, вступление и ведущие разделы H2 остаются в SKILL.md, пока суммарно ≤ бюджета;
  * остальные разделы переносятся ДОСЛОВНО, пачками по ~--chunk символов, в references/;
  * в SKILL.md добавляется указатель на созданные файлы;
  * после записи скрипт САМ проверяет, что ни один заголовок H2 не потерян.

Использование:
    SKILLS_DIR="$HOME/.hermes/skills"
    python3 split_skills.py --root "$SKILLS_DIR"                 # сухой прогон по всем
    python3 split_skills.py --root "$SKILLS_DIR" --apply         # записать
    python3 split_skills.py --root "$SKILLS_DIR" trading/foo --apply
    python3 split_skills.py --root . --verify-only                   # только проверка целостности

Код без внешних зависимостей (Python 3.9+). Всё, что пишется, — сами файлы скилла и бэкапы.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
import time
from pathlib import Path

TRANS = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "e", "ж": "zh", "з": "z",
    "и": "i", "й": "y", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o", "п": "p", "р": "r",
    "с": "s", "т": "t", "у": "u", "ф": "f", "х": "h", "ц": "c", "ч": "ch", "ш": "sh", "щ": "sch",
    "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya", " ": "-", "/": "-", "—": "-",
}


def slug(text: str, limit: int = 40) -> str:
    out = []
    for ch in text.lower():
        if ch in TRANS:
            out.append(TRANS[ch])
        elif ch.isascii() and (ch.isalnum() or ch in "-_"):
            out.append(ch)
        else:
            out.append("-")
    return re.sub(r"-{2,}", "-", "".join(out)).strip("-")[:limit] or "section"


def split_sections(text: str):
    """(вступление, [(заголовок H2, текст раздела)]). Код-фенсы не считаются заголовками."""
    intro, sections = [], []
    cur_head, cur_body, fence = None, [], False
    for ln in text.splitlines(keepends=True):
        if ln.lstrip().startswith("```"):
            fence = not fence
        if not fence and ln.startswith("## "):
            if cur_head is None:
                intro = cur_body
            else:
                sections.append((cur_head, "".join(cur_body)))
            cur_head, cur_body = ln.rstrip("\n")[3:].strip(), [ln]
        else:
            cur_body.append(ln)
    if cur_head is None:
        intro = cur_body
    else:
        sections.append((cur_head, "".join(cur_body)))
    return "".join(intro), sections


def headings(text: str) -> list[str]:
    return [h for h, _ in split_sections(text)[1]]


def plan(front: str, intro: str, sections, budget: int, chunk: int, min_tail: int):
    keep, move, size = [], [], len(front) + len(intro)
    for head, txt in sections:
        if size + len(txt) <= budget:
            keep.append((head, txt))
            size += len(txt)
        else:
            move.append((head, txt))
    chunks, cur, cur_len = [], [], 0
    for head, txt in move:
        if cur_len and cur_len + len(txt) > chunk:
            chunks.append(cur)
            cur, cur_len = [], 0
        cur.append((head, txt))
        cur_len += len(txt)
        if cur_len >= chunk:
            chunks.append(cur)
            cur, cur_len = [], 0
    if cur:
        # мелкий хвост возвращаем в SKILL.md ТОЛЬКО если он не пробивает бюджет
        # (дефект найден 24.09.2026: без проверки файл выходил за --budget)
        if cur_len < min_tail and size + cur_len <= budget:
            keep += cur
        else:
            chunks.append(cur)
    return keep, chunks


def process(skill_md: Path, args) -> dict:
    orig = skill_md.read_text(encoding="utf-8")
    front_m = re.match(r"^---\n.*?\n---\n", orig, re.S)
    front = front_m.group(0) if front_m else ""
    intro, sections = split_sections(orig[len(front):])
    if not sections:
        return {"skill": skill_md.parent.name, "skip": "нет разделов H2"}

    refs = skill_md.parent / "references"
    eff = args.budget
    keep: list = []
    files: list[tuple[str, str]] = []
    new_md = ""
    # Указатель в SKILL.md тоже занимает место. Поэтому подбираем бюджет так, чтобы
    # ИТОГОВЫЙ файл (разделы + указатель) не превышал --budget: если вылезли —
    # уменьшаем эффективный бюджет и переносим ещё один раздел (дефект A, 24.09.2026).
    for _ in range(12):
        keep, chunks = plan(front, intro, sections, eff, args.chunk, args.min_tail)
        if not chunks:
            break
        toc = ["\n## 📚 Справочники (грузятся по требованию)\n",
               "Полные разделы вынесены из SKILL.md, чтобы не занимать контекст. "
               "Читать по требованию: `references/<файл>`.\n"]
        files = []
        used_names: set[str] = set()
        for i, ch in enumerate(chunks, 1):
            base = slug(ch[0][0]) + (f"-{i}" if i > 1 else "")
            target, n = refs / f"{base}.md", 2
            body = "".join(t for _, t in ch)
            # уникальное имя внутри запуска: два раздела с ОДИНАКОВЫМ заголовком не должны
            # схлопнуться в один файл с одной строкой указателя (дефект B, 24.09.2026)
            while target.name in used_names or (target.exists()
                                                and target.read_text(encoding="utf-8") != body):
                target = refs / f"{base}-{n}.md"
                n += 1
            used_names.add(target.name)
            span = f"{ch[0][0][:40]} … {ch[-1][0][:40]}" if len(ch) > 1 else ch[0][0][:60]
            toc.append(f"* `references/{target.name}` — {span}\n")
            files.append((target.name, body))
        new_md = front + intro + "".join(t for _, t in keep) + "".join(toc)
        if len(new_md) <= args.budget or len(keep) <= 1:
            break
        eff -= max(200, len(new_md) - args.budget)

    if not files:
        return {"skill": skill_md.parent.name, "skip": f"в бюджете ({len(orig):,} симв)"}
    if len(new_md) > args.budget:
        print(f"  ⚠️ {skill_md.parent.name}: под бюджет не ушли ({len(new_md)} > {args.budget}) — "
              f"один раздел крупнее бюджета, режьте его вручную")

    result = {"skill": skill_md.parent.name, "before": len(orig), "after": len(new_md),
              "moved": sum(len(b) for _, b in files), "files": [n for n, _ in files]}

    if args.apply:
        args.backup_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(skill_md, args.backup_dir /
                     f"{skill_md.parent.name}.SKILL.md.bak-{time.strftime('%Y%m%d-%H%M%S')}")
        refs.mkdir(parents=True, exist_ok=True)
        for name, body in files:
            (refs / name).write_text(body, encoding="utf-8")
        skill_md.write_text(new_md, encoding="utf-8")
        result["verify"] = verify(skill_md.parent, headings(orig))
    return result


def verify(skill_dir: Path, must_have: list[str]) -> str:
    """Все заголовки исходника должны найтись в SKILL.md ∪ references."""
    blob = (skill_dir / "SKILL.md").read_text(encoding="utf-8") + "\n" + "\n".join(
        f.read_text(encoding="utf-8") for f in (skill_dir / "references").glob("*.md"))
    present = set(headings(blob))
    missing = [h for h in must_have if h not in present]
    return "OK: заголовков потеряно 0" if not missing else f"ПОТЕРЯНО {len(missing)}: {missing[:3]}"


def main() -> None:
    ap = argparse.ArgumentParser(description="Разрезать скиллы-монолиты на SKILL.md + references")
    ap.add_argument("targets", nargs="*", help="скиллы (путь к папке или к SKILL.md); пусто = все в --root")
    ap.add_argument("--root", default=".", help="каталог скиллов (по умолчанию текущий)")
    ap.add_argument("--budget", type=int, default=20000, help="потолок размера SKILL.md, символов")
    ap.add_argument("--chunk", type=int, default=38000, help="размер пачки для references, символов")
    ap.add_argument("--min-tail", type=int, default=4000, dest="min_tail",
                    help="хвост меньше этого остаётся в SKILL.md")
    ap.add_argument("--backup-dir", default=os.path.expanduser("~/.skill-split-backups"),
                    dest="backup_dir", help="куда класть бэкапы исходных SKILL.md")
    ap.add_argument("--apply", action="store_true", help="записать изменения (иначе сухой прогон)")
    ap.add_argument("--verify-only", action="store_true", dest="verify_only",
                    help="только проверить целостность (сравнить с бэкапами)")
    args = ap.parse_args()
    args.backup_dir = Path(args.backup_dir)

    root = Path(args.root).expanduser()
    if args.verify_only:
        baks = sorted(args.backup_dir.glob("*.SKILL.md.bak-*"))
        if not baks:
            print(f"нет бэкапов в {args.backup_dir} — проверять нечего. "
                  f"Укажите каталог бэкапов явно: --backup-dir <каталог>")
            sys.exit(2)                      # НЕ молчаливый «успех»
        bad = 0
        for bak in baks:
            name = bak.name.split(".SKILL.md.bak-")[0]
            dirs = [p.parent for p in root.rglob("SKILL.md") if p.parent.name == name]
            if not dirs:
                print(f"{name}: скилл не найден — ПОТЕРЯ")
                bad += 1
                continue
            res = verify(dirs[0], headings(bak.read_text(encoding="utf-8")))
            print(f"{name}: {res}")
            if "ПОТЕРЯНО" in res:
                bad += 1
        sys.exit(1 if bad else 0)             # гейт: ненулевой код при потере

    if args.targets:
        paths = []
        for t in args.targets:
            p = Path(t).expanduser()
            paths.append(p if p.is_absolute() else (root / p))
    else:
        # считаем в СИМВОЛАХ (len), как сам разрезатель: st_size — это байты,
        # из-за чего кириллический файл у границы бюджета проскакивал фильтр
        cand = []
        for p in root.rglob("SKILL.md"):
            try:
                if len(p.read_text(encoding="utf-8")) > args.budget:
                    cand.append(p)
            except OSError:
                continue
        paths = sorted(cand)
    if not paths:
        print(f"нечего резать: под {root} нет ни одного файла инструкции крупнее "
              f"{args.budget} символов — проверьте --root или укажите скилл явно\n")
        ap.print_help()
        sys.exit(0)

    print(f"{'скилл':34} {'было':>9} {'станет':>9} {'уедет':>9} {'файлов':>7}  проверка")
    tb = ta = 0
    for p in paths:
        if p.is_dir():
            p = p / "SKILL.md"
        if not p.exists():
            print(f"  {p}: не найден")
            continue
        r = process(p, args)
        if "skip" in r:
            print(f"{r['skill']:34} {'—':>9} {'—':>9} {'—':>9} {'—':>7}  {r['skip']}")
            continue
        tb += r["before"]
        ta += r["after"]
        print(f"{r['skill']:34} {r['before']:>9,} {r['after']:>9,} {r['moved']:>9,} "
              f"{len(r['files']):>7}  {r.get('verify', '')}")
    if tb:
        print(f"\nИТОГО: {tb:,} → {ta:,} символов на один дамп (−{100*(tb-ta)/tb:.0f} %)")
    print("[записано]" if args.apply else "[сухой прогон] добавьте --apply, чтобы записать")


if __name__ == "__main__":
    main()
