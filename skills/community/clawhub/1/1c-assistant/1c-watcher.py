#!/usr/bin/env python3
"""
OpenClaw trajectory watcher для 1С ассистента.
- /1c → отправляет справку
- Вопрос про 1С → вызывает wf20 RAG Query (qwen3 не умеет bash)
"""
import os, json, time, subprocess, glob, datetime

SESSIONS_DIR  = "/home/alexandr/.openclaw/agents/main/sessions"
HELP_SCRIPT   = "/home/alexandr/.openclaw/workspace/1c-assistant/1c-help.sh"
CHAT_ID       = "1360549978"
STATE_FILE    = "/tmp/1c-watcher-state.json"
RAG_WEBHOOK   = "https://n8nwint.ru/webhook/1c-rag-query"
RAG_MODEL     = "qwen3:14b"
MCP_URL       = "http://127.0.0.1:3033"
OLLAMA_URL    = "http://192.168.0.200:11434"
N8N_GOOGLE_MCP = "https://n8nwint.ru/mcp/55c131e9-8408-4a71-8b3b-318c4264fd07"
MCPORTER      = "/home/alexandr/.npm-global/bin/mcporter"

KEYWORDS_CALENDAR = [
    "календарь", "calendar", "расписание", "встреча", "событие",
    "проверь календарь", "что сегодня", "план на день",
    "запись", "напоминание", "дедлайн", "schedule",
]

KEYWORDS_OLLAMA = [
    "статус олламы", "статус ollama", "ollama status",
    "список моделей", "какие модели", "модели ollama",
    "ollama работает", "перезапусти ollama", "ollama загружена",
]

KEYWORDS_SYSSTAT = [
    "сколько памяти", "свободно памяти", "free -h", "свободно места",
    "df -h", "нагрузка cpu", "load average", "сколько места на диске",
]

# Ключевые слова для определения 1С вопросов
KEYWORDS_1C = [
    "1с", "1c", "bsl", "встроенный язык",
    "регистр накопления", "регистр бухгалтерии", "регистр сведений",
    "справочник", "документ 1с", "конфигуратор",
    "управляемые формы", "управляемая форма",
    "роли 1с", "права 1с", "пользователи 1с",
    "запрос 1с", "скд", "схема компоновки",
    "бухгалтерия", "ндс", "ндфл", "зарплата", "зуп",
    "печатная форма", "макет", "табличный документ",
    "проведение", "проводки", "закрытие месяца",
    "начисление", "страховые взносы",
    "erp", "нси", "обмен данными",
]

KEYWORDS_PYTHON = [
    "python", "питон", "django", "fastapi", "flask", "aiohttp", "asyncio",
    "pydantic", "sqlalchemy", "pandas", "numpy", "pytest", "celery",
    "pip install", "requirements.txt", "venv", "poetry", "pyproject",
    "декоратор python", "генератор python", "lambda python",
    "async def", "await python", "тип данных python",
    "список python", "словарь python", "класс python",
]

KEYWORDS_DEVOPS = [
    "docker", "dockerfile", "docker-compose", "compose файл", "контейнер docker",
    "образ docker", "docker run", "docker build", "docker logs",
    "kubernetes", "k8s", "helm chart", "kubectl",
    "github actions", "woodpecker ci", "ci/cd pipeline",
    "nginx", "caddy", "reverse proxy",
    "ansible", "terraform", "wireguard",
    "systemctl", "journalctl", "systemd", "сервис linux",
    "ss -t", "ip addr", "iptables", "firewall",
    "df -h", "du -sh", "lsblk", "свободно диск",
]

# Коллекции по темам
COLLECTION_MAP = [
    (["bsl", "запрос", "скд", "код", "диагностик", "управляемые формы", "управляемая форма",
      "цикломатическ", "когнитивн", "транзакц", "встроенный язык"], "kb_1c_code"),
    (["права", "роли", "пользовател", "доступ", "разрешен"], "kb_1c_admin"),
    (["бухгалтер", "ндс", "счет", "проводк", "баланс", "налог", "закрытие месяца",
      "регистр бухгалтери"], "kb_1c_buh"),
    (["зарплат", "зуп", "ндфл", "страховые взносы", "начислен", "кадр", "сотрудник"], "kb_1c_zup"),
    (["печатная форма", "макет", "табличный документ", "скд", "схема компоновки"], "kb_1c_forms"),
    # Python / DevOps
    (["docker", "dockerfile", "compose", "контейнер docker", "образ docker",
      "kubernetes", "k8s", "helm", "kubectl", "github actions", "woodpecker",
      "nginx конфиг", "ansible", "terraform", "wireguard конфиг"], "kb_devops"),
    (["python", "питон", "django", "fastapi", "flask", "asyncio", "pydantic",
      "sqlalchemy", "pandas", "numpy", "pytest", "pip install", "venv", "poetry",
      "async def", "await python"], "kb_python"),
]

MAX_ENTRY_AGE_SEC = 300  # игнорировать записи старше 5 минут (баг: новые сессии читают всю историю)

def is_recent_entry(entry):
    try:
        ts = entry.get("ts") or entry.get("timestamp") or entry.get("time")
        if not ts:
            return True
        if isinstance(ts, (int, float)):
            dt = datetime.datetime.fromtimestamp(ts / 1000, tz=datetime.timezone.utc)
        else:
            dt = datetime.datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
        age = (datetime.datetime.now(datetime.timezone.utc) - dt).total_seconds()
        return age < MAX_ENTRY_AGE_SEC
    except:
        return True

def load_state():
    try:
        return json.load(open(STATE_FILE))
    except:
        return {"processed": [], "file_sizes": {}}

def save_state(state):
    json.dump(state, open(STATE_FILE, "w"))

def get_trajectory_files():
    return glob.glob(f"{SESSIONS_DIR}/*.trajectory.jsonl")

def is_help_trigger(text):
    t = text.strip().lower()
    if t in {"/1c", "/1c-help", "/1с"} or t.startswith("/1c"):
        return True
    if "1с помощь" in t or "помощь 1с" in t:
        return True
    return False

ALL_KEYWORDS = KEYWORDS_1C + KEYWORDS_PYTHON + KEYWORDS_DEVOPS

def is_known_question(text):
    """Вопрос по 1С, Python или DevOps — нужна RAG."""
    t = text.strip().lower()
    if t.startswith("[openclaw") or t.startswith("heartbeat"):
        return False
    if len(t) < 10:
        return False
    for kw in ALL_KEYWORDS:
        if kw in t:
            return True
    return False

# Оставляем для обратной совместимости
def is_1c_question(text):
    return is_known_question(text)

def detect_collection(text):
    t = text.lower()
    for keywords, collection in COLLECTION_MAP:
        for kw in keywords:
            if kw in t:
                return collection
    return "kb_1c_erp"

def extract_last_user_text(entry):
    """Только последнее user сообщение (не вся история)."""
    try:
        if entry.get("type") != "prompt.submitted":
            return None
        data = entry.get("data", {})
        if not isinstance(data, dict):
            return None
        messages = data.get("messages", [])
        if not isinstance(messages, list):
            return None
        for msg in reversed(messages):
            if not isinstance(msg, dict) or msg.get("role") != "user":
                continue
            content = msg.get("content", "")
            if isinstance(content, str):
                return content
            elif isinstance(content, list):
                for c in reversed(content):
                    if isinstance(c, dict):
                        t = c.get("text", "") or c.get("content", "")
                        if t:
                            return t
    except:
        pass
    return None

def send_telegram(text):
    subprocess.run([
        "curl", "-s", "-X", "POST", f"{MCP_URL}/send-telegram",
        "-H", "Content-Type: application/json",
        "-d", json.dumps({"chat_id": CHAT_ID, "text": text})
    ], capture_output=True, timeout=10)

def send_help():
    print("[watcher] Sending /1c help card...", flush=True)
    subprocess.run(["bash", HELP_SCRIPT, CHAT_ID], timeout=30)
    print("[watcher] Help sent.", flush=True)

def parse_date_from_text(text):
    """Извлекает дату из текста. Возвращает строку YYYY-MM-DD или сегодня."""
    import re
    t = text.lower()
    now = datetime.datetime.now()
    year = now.year

    # dd.mm или dd.mm.yyyy
    m = re.search(r'(\d{1,2})\.(\d{1,2})(?:\.(\d{2,4}))?', t)
    if m:
        day, month = int(m.group(1)), int(m.group(2))
        yr = int(m.group(3)) if m.group(3) else year
        if yr < 100: yr += 2000
        try:
            return datetime.date(yr, month, day).strftime("%Y-%m-%d")
        except: pass

    # завтра / послезавтра / сегодня
    if "послезавтра" in t:
        return (now + datetime.timedelta(days=2)).strftime("%Y-%m-%d")
    if "завтра" in t:
        return (now + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    return now.strftime("%Y-%m-%d")

def mcporter_call(tool, **kwargs):
    args = [MCPORTER, "call", f"n8n-google.{tool}"]
    for k, v in kwargs.items():
        args.append(f"{k}={v}")
    r = subprocess.run(args, capture_output=True, text=True, timeout=20)
    return r.stdout.strip() or r.stderr.strip()

def handle_calendar(text):
    print(f"[watcher] Calendar request: '{text[:80]}'", flush=True)
    t = text.lower()
    date_str = parse_date_from_text(text)

    try:
        # Получить события на указанную дату
        output = mcporter_call("Get_many_events",
            Return_All="false",
            After=f"{date_str}T00:00:00",
            Before=f"{date_str}T23:59:59",
            Fields="", iCalUID="", Query="")

        if not output or output == "[]":
            send_telegram(f"📅 *Календарь на {date_str}:*\n\nСобытий нет.")
            return

        # Форматируем вывод
        try:
            events = json.loads(output)
            if not events:
                send_telegram(f"📅 *Календарь на {date_str}:*\n\nСобытий нет.")
                return
            lines = [f"📅 *Календарь на {date_str}:*\n"]
            for ev in events[:10]:
                summary = ev.get("summary", "Без названия")
                start = ev.get("start", {}).get("dateTime", ev.get("start", {}).get("date", ""))[:16]
                end = ev.get("end", {}).get("dateTime", ev.get("end", {}).get("date", ""))[:16]
                lines.append(f"• *{summary}*\n  {start} → {end}")
            msg = "\n".join(lines)
        except:
            msg = f"📅 *Календарь на {date_str}:*\n\n{output[:1200]}"

        send_telegram(msg)

        # Скопировать на другую дату если просят
        copy_match = None
        import re
        for kw in ["скопируй на", "copy to", "перенеси на", "создай на"]:
            if kw in t:
                rest = t.split(kw, 1)[1]
                copy_date = parse_date_from_text(rest)
                copy_match = copy_date
                break

        if copy_match and isinstance(json.loads(output), list):
            events_to_copy = json.loads(output)
            copied = 0
            for ev in events_to_copy[:5]:
                summary = ev.get("summary","Событие")
                start_orig = ev.get("start",{}).get("dateTime","")
                end_orig   = ev.get("end",{}).get("dateTime","")
                if start_orig:
                    start_time = start_orig[11:16]
                    end_time   = end_orig[11:16] if end_orig else "00:00"
                    new_start = f"{copy_match}T{start_time}:00"
                    new_end   = f"{copy_match}T{end_time}:00"
                    mcporter_call("Create_an_event",
                        Start=new_start, End=new_end,
                        Summary=f"{summary} (копия)",
                        Description="", Use_Default_Reminders="true")
                    copied += 1
            if copied:
                send_telegram(f"✅ Скопировано {copied} событий на {copy_match}")

        # Отправить на почту если просят
        if any(kw in t for kw in ["на почту", "email", "отправь", "mail"]):
            email_body = f"События на {date_str}:\n\n{output[:2000]}"
            subprocess.run([
                "curl", "-s", "-X", "POST", f"{MCP_URL}/send-report",
                "-H", "Content-Type: application/json",
                "-d", json.dumps({
                    "subject": f"Календарь на {date_str}",
                    "body": email_body,
                    "chat_id": CHAT_ID
                })
            ], capture_output=True, timeout=10)
            send_telegram(f"📧 Отчёт по календарю отправлен на почту")

    except Exception as e:
        send_telegram(f"❌ Ошибка календаря: {e}")
    print(f"[watcher] Calendar done.", flush=True)

def handle_ollama():
    print("[watcher] Ollama status request", flush=True)
    try:
        result = subprocess.run([
            "curl", "-s", f"{OLLAMA_URL}/api/tags"
        ], capture_output=True, text=True, timeout=10)
        data = json.loads(result.stdout)
        models = data.get("models", [])
        lines = ["🤖 *Ollama — модели:*\n"]
        for m in models:
            size_gb = m.get("size", 0) / (1024**3)
            lines.append(f"• `{m['name']}` — {size_gb:.1f}GB")
        send_telegram("\n".join(lines))
    except Exception as e:
        send_telegram(f"❌ Ollama недоступна: {e}")
    print("[watcher] Ollama status sent.", flush=True)

def handle_sysstat():
    print("[watcher] System stat request", flush=True)
    try:
        mem = subprocess.run(["free", "-h"], capture_output=True, text=True, timeout=5).stdout
        disk = subprocess.run(["df", "-h", "--output=target,size,used,avail,pcent", "/", "/home"],
                              capture_output=True, text=True, timeout=5).stdout
        load = subprocess.run(["uptime"], capture_output=True, text=True, timeout=5).stdout.strip()
        msg = f"💻 *Состояние системы:*\n\n*RAM:*\n```\n{mem.strip()}\n```\n\n*Диск:*\n```\n{disk.strip()}\n```\n\n*Нагрузка:* `{load}`"
        send_telegram(msg)
    except Exception as e:
        send_telegram(f"❌ Ошибка: {e}")
    print("[watcher] Sysstat sent.", flush=True)

def is_calendar_request(text):
    t = text.strip().lower()
    return any(kw in t for kw in KEYWORDS_CALENDAR)

def is_ollama_request(text):
    t = text.strip().lower()
    return any(kw in t for kw in KEYWORDS_OLLAMA)

def is_sysstat_request(text):
    t = text.strip().lower()
    return any(kw in t for kw in KEYWORDS_SYSSTAT)

def send_rag_query(question, collection):
    print(f"[watcher] RAG query → {collection}: {question[:60]}...", flush=True)
    result = subprocess.run([
        "curl", "-s", "-X", "POST", RAG_WEBHOOK,
        "-H", "Content-Type: application/json",
        "-d", json.dumps({
            "question": question,
            "chat_id": CHAT_ID,
            "collection": collection,
            "model": RAG_MODEL
        })
    ], capture_output=True, text=True, timeout=15)
    print(f"[watcher] RAG response: {result.stdout[:100]}", flush=True)

def scan_file(filepath, state):
    try:
        size = os.path.getsize(filepath)
        last_size = state["file_sizes"].get(filepath, 0)
        if size <= last_size:
            return None, None
        state["file_sizes"][filepath] = size

        with open(filepath, "rb") as f:
            f.seek(last_size)
            new_content = f.read().decode("utf-8", errors="ignore")

        for line in new_content.strip().split("\n"):
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
                if not is_recent_entry(entry):
                    continue
                run_id = entry.get("runId", entry.get("traceId", "unknown"))
                text = extract_last_user_text(entry)
                if not text:
                    continue

                key = f"{run_id}:{text[:50]}"
                if key in state["processed"]:
                    continue

                state["processed"].append(key)
                if len(state["processed"]) > 200:
                    state["processed"] = state["processed"][-100:]

                if is_help_trigger(text):
                    print(f"[watcher] /1c trigger: '{text[:50]}'", flush=True)
                    return "help", None
                elif is_calendar_request(text):
                    print(f"[watcher] Calendar trigger: '{text[:50]}'", flush=True)
                    return "calendar", text
                elif is_ollama_request(text):
                    print(f"[watcher] Ollama trigger: '{text[:50]}'", flush=True)
                    return "ollama", None
                elif is_sysstat_request(text):
                    print(f"[watcher] Sysstat trigger: '{text[:50]}'", flush=True)
                    return "sysstat", None
                elif is_known_question(text):
                    collection = detect_collection(text)
                    print(f"[watcher] RAG trigger [{collection}]: '{text[:60]}'", flush=True)
                    return "rag", (text, collection)

            except json.JSONDecodeError:
                pass
    except Exception as e:
        print(f"[watcher] Error scanning: {e}", flush=True)
    return None, None

def main():
    print("[watcher] Started. /1c help + 1C RAG proxy.", flush=True)
    state = load_state()

    for f in get_trajectory_files():
        if f not in state["file_sizes"]:
            state["file_sizes"][f] = os.path.getsize(f)
    save_state(state)
    print(f"[watcher] Tracking {len(state['file_sizes'])} files", flush=True)

    heartbeat = 0
    while True:
        action, payload = None, None
        for filepath in get_trajectory_files():
            a, p = scan_file(filepath, state)
            if a:
                action, payload = a, p
                break

        if action:
            save_state(state)
            time.sleep(2)
            if action == "help":
                send_help()
            elif action == "calendar":
                handle_calendar(payload or "")
            elif action == "ollama":
                handle_ollama()
            elif action == "sysstat":
                handle_sysstat()
            elif action == "rag":
                question, collection = payload
                send_rag_query(question, collection)
        else:
            save_state(state)
            heartbeat += 1
            if heartbeat % 100 == 0:
                print(f"[watcher] alive, files={len(state['file_sizes'])}", flush=True)

        time.sleep(3)

if __name__ == "__main__":
    main()
