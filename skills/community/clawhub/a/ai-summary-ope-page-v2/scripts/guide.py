# -*- coding: utf-8 -*-
"""guide.py — печатает редакторские справочники навыка.

Команды:
  guide.py summary      канон одностраничного резюме для руководителя
  guide.py translation  стандарт перевода: как писать по-русски без калек (для документов не на русском)
  guide.py humanize     проверка на человечность: финальная редактура (её же отдаёт build при humanize_required)
  guide.py factcheck    сверка фактов резюме с документом (её же отдаёт build при factcheck_required)
  guide.py             список разделов

Справочники лежат в references/ рядом со scripts/. Скрипт только читает их.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import _core as core  # noqa: E402

TOPICS = {
    "summary": ("summary_canon.md", "канон резюме: читатель, семь правил, структура, голос, стоп-слова, самопроверка"),
    "translation": ("translation_guide.md", "стандарт перевода: приёмы, кальки, модальность, числа, термины"),
    "humanize": ("humanize_guide.md", "проверка на человечность: финальная редактура резюме, один раз после вёрстки"),
    "factcheck": ("factcheck_guide.md", "сверка фактов: каждое утверждение резюме — с текстом документа, исправление ошибок"),
}


def main() -> None:
    core.setup_stdio()
    topic = sys.argv[1].strip().lower() if len(sys.argv) > 1 else ""
    if topic not in TOPICS:
        core.out({"ok": True, "topics": {k: v[1] for k, v in TOPICS.items()},
                  "usage": "guide.py summary | guide.py translation | guide.py humanize | guide.py factcheck"})
    path = Path(__file__).resolve().parent.parent / "references" / TOPICS[topic][0]
    if not path.is_file():
        core.fail("Справочник %s не найден в папке навыка." % TOPICS[topic][0],
                  "Проверьте, что папка references/ загружена вместе с навыком.")
    core.out({"ok": True, "topic": topic, "text": path.read_text(encoding="utf-8")})


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:
        core.fail("Внутренняя ошибка guide.py: %s: %s" % (type(e).__name__, e))
