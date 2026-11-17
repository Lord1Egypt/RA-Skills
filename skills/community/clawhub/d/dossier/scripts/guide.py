#!/usr/bin/env python3
"""Инструкция навыка dossier — без сети и без записи на диск.

    guide.py             КАРТА РАБОТЫ: шаги с готовыми вызовами и главные правила
                         (коротко — так она переживает сжатие контекста)
    guide.py status      где я: что уже найдено, есть ли досье, чем кончилась
                         проверка и какой следующий шаг (после сжатия контекста)
    guide.py full        полная методика — тот же текст, что SKILL.md
    guide.py flow        порядок вызовов скриптов
    guide.py playbook    поисковый справочник: слои, готовые запросы, стоп-условия
    guide.py checklist   stop-gate перед сдачей досье

Почему по умолчанию коротко. В установке с малым контекстом движок сжимает
историю задачи, когда она перерастает порог, и от каждого старого ответа
инструмента оставляет пересказ его первых 2,5 тыс. знаков. Полный текст
навыка (≈85 тыс. знаков) сам запускал это сжатие на третьем ходу, и дальше
агент работал по пересказу начала инструкции. Поэтому карта — короткая, а
правила каждого шага печатает тот скрипт, который этот шаг выполняет: они
всегда свежие, когда нужны.
"""
from __future__ import annotations

import json
import pathlib
import sys
import time

sys.dont_write_bytecode = True

ROOT = pathlib.Path(__file__).resolve().parent.parent

CARD = """КАРТА РАБОТЫ dossier — 8 шагов. Каждый скрипт сам печатает правила своего шага и следующий вызов.
Вызовы — skill_exec(skill="dossier", script=…, args=[…]).

1. Поиск, волна 1 — личность:  search.py  ["--wave1", "<Имя Фамилия>", "--org", "<организация>", "--latin", "<Name Surname>"]
2. Поиск, волны 2–4 одним вызовом:  search.py  ["--deep", "<Имя Фамилия>", "--org", "…", "--latin", "…"]
3. Пробелы — свои вопросы, до 8 за вызов, имя в каждом:  search.py  ["<Имя>: вопрос 1", "<Имя>: вопрос 2", …]
4. Бриф — всё найденное одним блоком, с номерами источников и правилами записи:  search.py  ["--brief", "<Имя Фамилия>"]
5. Сразу по брифу — dossier.json одним write_file(root="task_drive", path="dossier.json").
6. Проверка формы и фактов одним вызовом:  verify_facts.py  ["dossier.json"]
   Отказ — исправить ВСЕ пункты одним write_file и вызвать снова (подтверждённое в кэше).
7. Сборка:  render_dossier.py  ["dossier.json", "Досье — <Фамилия Имя> — <ГГГГ-ММ-ДД>.docx"]
8. send_file(<путь из шага 7>) и тем же ходом — блок «ТЕКСТ ДЛЯ ЧАТА» как есть, без правок
   и без приписок (строку «Собрано» не дополнять — модели в ней нет намеренно).

Главное:
• Ищите ТОЛЬКО через search.py — это Perplexity Sonar. Встроенный поиск агента (gigasearch,
  web_search) здесь другой движок; источники из него сборка не примет. Упал вызов — повторите тот же.
• Пишите по брифу, не по памяти и не по прошлым досье из этого чата — они не образец.
• Факт — с номером источника [n]; вывод — в «Анализ» с пометкой «[Анализ]». Числа — только из
  источника дословно (поле figures). Семья, здоровье, утраты — ни в одном разделе.
• Место работы — «последнее известное, по состоянию на <дата>». Возраст, если выведен, — «около».
• Разделы — в полную силу лимитов (Одним абзацем 3–4 предложения; Чем известен 3–4 пункта;
  Темы 4–5 пунктов): тонкие разделы — главный дефект прошлых досье.
• Есть в запросе или памяти, для кого досье (организация и роль владельца) или повод встречи —
  запишите в owner_context / meeting_context: темы строятся на их стыке с опытом человека.
• Страницы целиком (browse_page) — только чтобы разрешить конкретное противоречие, не больше 2–3:
  Sonar их уже прочитал, а лишний текст вытесняет из контекста найденное.
• Потеряли нить после сжатия контекста — guide.py status: он скажет, что сделано и что дальше.
• Несколько человек в задаче — отдельный файл на каждого: dossier_<фамилия латиницей>.json.

Полная методика (если нужна): guide.py full. Поисковый справочник: guide.py playbook."""

FLOW = """Порядок работы dossier (вызовы — через skill_exec):

1. search.py  ["--wave1", "<Имя Фамилия>", "--org", "<организация>", "--latin", "<Name Surname>"]
   → личность закреплена двумя признаками; тёзки отсеяны.
2. search.py  ["--deep", "<Имя Фамилия>", "--org", "…", "--latin", "…"]   (волны 2–4, 24 вопроса)
3. search.py  ["<Имя>: вопрос 1", …]   (до 8 за вызов; незакрытые якоря, новые работодатели, сделки)
   search.py  ["--log", "<Имя Фамилия>"]   (счётчик)
4. search.py  ["--brief", "<Имя Фамилия>"]   → бриф: ответы Sonar с едиными номерами источников
   и правила записи JSON. Формат с лимитами целиком — render_dossier.py ["--schema"].
5. write_file(root="task_drive", path="dossier.json", …) — сразу после брифа, одним вызовом.
6. verify_facts.py  ["dossier.json"]   → сначала форма (объём, числа, ссылки, частное), потом
   каждое утверждение через Sonar. Отказ — исправить всё одним write_file и снова.
   «СБОЙ» или «проверка не завершена» — повторить тот же вызов без правок.
   Превышен объём — render_dossier.py ["--fit", "dossier.json"] срежет необязательное сам.
7. render_dossier.py  ["dossier.json", "Досье — <Фамилия Имя> — <ГГГГ-ММ-ДД>.docx"]
8. send_file(<путь из шага 7>) и тем же ходом — «ТЕКСТ ДЛЯ ЧАТА» как есть.

Вместо «dossier.json» можно передавать абсолютный путь из ответа write_file.
Потеряли нить — guide.py status."""


def skill_body(path: pathlib.Path) -> str:
    """Текст SKILL.md без шапки-манифеста: шапка — для движка, не для работы."""
    text = path.read_text(encoding="utf-8")
    if text.startswith("---"):
        parts = text.split("\n---", 1)
        if len(parts) == 2:
            text = parts[1].split("\n", 1)[1] if "\n" in parts[1] else ""
    return text.strip()


def section_of(path: pathlib.Path, heading: str) -> str:
    """Раздел markdown-файла от заголовка до следующего заголовка того же уровня."""
    lines = path.read_text(encoding="utf-8").splitlines()
    level = len(heading) - len(heading.lstrip("#"))
    out, inside = [], False
    for line in lines:
        if line.strip().startswith(heading):
            inside = True
        elif inside and line.startswith("#" * level + " ") and not line.startswith("#" * (level + 1)):
            break
        if inside:
            out.append(line)
    return "\n".join(out).strip()


def status(name: str = "") -> int:
    """Где я: поиск, бриф, файл досье, итог проверки — и следующий шаг."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import search  # noqa: E402
    import verify_facts as vf  # noqa: E402

    recs = search.read_research()
    if not name:
        persons = [r.get("person") for r in recs if r.get("person")]
        name = persons[-1].split(" / ")[0] if persons else ""
    mine = search.read_research(name) if name else []
    waves: dict = {}
    for r in mine:
        waves[r.get("wave") or "custom"] = waves.get(r.get("wave") or "custom", 0) + 1
    print(f"Человек: {name or 'не найден в журнале поиска (12 ч)'}")
    if name:
        parts = ", ".join(f"{search.GROUP_TITLES.get(k, k)} — {v}" for k, v in waves.items()) or "нет"
        print(f"Ответов Sonar про него за 12 ч: {len(mine)} ({parts}).")

    files = []
    now = time.time()
    for root in vf.task_drive_roots():
        try:
            for p in root.glob("*/*.json"):
                if now - p.stat().st_mtime < 6 * 3600:
                    files.append(p)
        except OSError:
            continue
    dossiers = []
    for p in sorted(files, key=lambda x: x.stat().st_mtime, reverse=True)[:12]:
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(d, dict) and d.get("name") and ("summary" in d or "who" in d):
            dossiers.append((p, d))
    if dossiers:
        for p, d in dossiers[:3]:
            print(f"Файл досье: {p} — «{d.get('name')}», изменён {time.strftime('%H:%M', time.localtime(p.stat().st_mtime))}")
    else:
        print("Файла досье в каталогах задач за 6 ч нет.")

    st = {}
    try:
        st = json.loads((vf.work_dir() / vf.STATUS_NAME).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        pass
    if st and now - float(st.get("ts") or 0) < 6 * 3600:
        print(f"Последняя проверка фактов ({time.strftime('%H:%M', time.localtime(float(st.get('ts'))))}): "
              f"{st.get('status')} — {st.get('detail')}")
        for item in (st.get("failing") or [])[:12]:
            print(f"  [{item.get('status')}] «{str(item.get('text'))[:100]}»"
                  + (f" — Sonar: {item.get('why')}" if item.get("why") else ""))
    else:
        st = {}

    print()
    if not mine:
        print('Дальше: search.py ["--wave1", "<Имя Фамилия>", "--org", "…", "--latin", "…"]')
    elif "wave2" not in waves and "wave4" not in waves:
        print(f'Дальше: search.py ["--deep", "{name}", "--org", "…", "--latin", "…"]')
    elif not dossiers:
        print(f'Дальше: search.py ["--brief", "{name}"] и сразу dossier.json одним write_file по брифу.')
    elif st.get("status") == "ok":
        print('Дальше: render_dossier.py ["dossier.json", "Досье — <Фамилия Имя> — <ГГГГ-ММ-ДД>.docx"], '
              'затем send_file и «ТЕКСТ ДЛЯ ЧАТА» как есть.')
    elif st.get("status") == "claims_failed":
        print("Дальше: исправить перечисленное одним write_file (текст досье — read_file того файла), "
              "затем verify_facts.py снова.")
        print(f'Нужны данные для правки — search.py ["--brief", "{name}"] вернёт найденное.')
    else:
        print('Дальше: verify_facts.py ["dossier.json"] (сначала проверит форму, потом факты).')
    return 0


def main() -> int:
    topic = (sys.argv[1] if len(sys.argv) > 1 else "").strip().lower().lstrip("-")
    skill_md = ROOT / "SKILL.md"
    try:
        if topic == "flow":
            print(FLOW)
            return 0
        if topic == "status":
            return status(" ".join(sys.argv[2:]).strip())
        if topic == "playbook":
            print((ROOT / "references" / "search-playbook.md").read_text(encoding="utf-8"))
            return 0
        if topic == "checklist":
            text = section_of(skill_md, "## Stop-gate")
            print(text or "[!] Раздел Stop-gate не найден в SKILL.md")
            return 0 if text else 1
        if topic in ("full", "all", "skill", "instruction"):
            print(CARD)
            print("\n" + "=" * 30 + " SKILL.md " + "=" * 30 + "\n")
            print(skill_body(skill_md))
            return 0
        # Без аргумента и с любым другим — карта. Ошибка на незнакомый аргумент
        # стоила ход и выглядела в журнале как сбой навыка.
        if topic and topic not in ("help", "h", "card"):
            print(f"[i] Раздела «{topic}» нет — печатаю карту. Разделы: status, full, flow, playbook, checklist.\n")
        print(CARD)
        return 0
    except OSError as exc:
        print(f"[!] Не удалось прочитать файл навыка: {exc}")
        print(f"    Каталог навыка: {ROOT}")
        print("    Похоже, навык установлен в нестандартной раскладке — сообщите владельцу.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
