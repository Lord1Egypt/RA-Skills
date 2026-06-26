# База знаний Кузи — Шпаргалка

## Коллекции

| Коллекция | Тема |
|-----------|------|
| `kb_1c_code` | BSL код, диагностики, запросы |
| `kb_1c_admin` | Права, роли, пользователи |
| `kb_1c_buh` | Бухгалтерия, НДС, проводки |
| `kb_1c_zup` | ЗУП, зарплата, НДФЛ |
| `kb_1c_forms` | Печатные формы, СКД |
| `kb_1c_erp` | ERP, НСИ, общая настройка |
| `kb_python` | Python, FastAPI, asyncio, декораторы |
| `kb_devops` | Docker, Nginx, Linux команды, systemd |

---

## Загрузка документов

### Текст напрямую
```bash
curl -s -X POST https://n8nwint.ru/webhook/1c-ingest \
  -H "Content-Type: application/json" \
  -d "$(python3 -c "import json; print(json.dumps({
    'type': 'text',
    'collection': 'kb_devops',
    'title': 'Название документа',
    'text': 'Текст для добавления в базу...',
    'chat_id': '1360549978',
    'version_1c': 'n/a'
  }))")"
```

### URL страницы (автоматически скачает и очистит HTML)
```bash
curl -s -X POST https://n8nwint.ru/webhook/1c-ingest \
  -H "Content-Type: application/json" \
  -d "$(python3 -c "import json; print(json.dumps({
    'type': 'url',
    'collection': 'kb_python',
    'title': 'FastAPI документация',
    'url': 'https://fastapi.tiangolo.com/tutorial/',
    'chat_id': '1360549978',
    'version_1c': 'n/a'
  }))")"
```

### PDF файл (OCR автоматически для сканов)
```bash
bash ~/.openclaw/workspace/1c-assistant/ingest_pdf.sh \
  "/path/to/file.pdf" \
  "kb_1c_buh" \
  "Название документа"

# PDF по URL
bash ~/.openclaw/workspace/1c-assistant/ingest_pdf.sh \
  "https://example.com/doc.pdf" \
  "kb_python" \
  "Название"
```

### Скриншот / Изображение (OCR + фото в Telegram)
```bash
bash ~/.openclaw/workspace/1c-assistant/ingest_image.sh \
  "/path/to/screenshot.png" \
  "kb_devops" \
  "Nginx конфиг — пример"

# Изображение по URL
bash ~/.openclaw/workspace/1c-assistant/ingest_image.sh \
  "https://example.com/screenshot.png" \
  "kb_python" \
  "FastAPI схема"
```
Что происходит:
1. OCR (tesseract rus+eng) → текст попадает в Qdrant
2. Изображение копируется → доступно по http://192.168.0.66:3033/files/
3. При RAG поиске → Telegram получает текстовый ответ + само фото

---

## Задать вопрос (прямой RAG запрос)

```bash
curl -s -X POST https://n8nwint.ru/webhook/1c-rag-query \
  -H "Content-Type: application/json" \
  -d "$(python3 -c "import json; print(json.dumps({
    'question': 'как написать запрос к регистру накопления?',
    'chat_id': '1360549978',
    'collection': 'kb_1c_code',
    'model': 'qwen3:14b'
  }))")"
```
Ответ придёт в Telegram через 30–90 сек.

---

## Проверка состояния коллекций

```bash
QDRANT="http://192.168.0.200:6333"
KEY="zkpDII8FaBpzpRke8uWWcOEJDGXxKNsn"
for coll in kb_1c_erp kb_1c_buh kb_1c_zup kb_1c_code kb_1c_admin kb_1c_forms kb_python kb_devops; do
  count=$(curl -s "$QDRANT/collections/$coll" -H "api-key: $KEY" \
    | python3 -c "import sys,json; print(json.load(sys.stdin).get('result',{}).get('points_count','?'))")
  echo "$coll: $count"
done
```

---

## Кузе в Telegram (команды голосом/текстом)

```
добавь скриншот /path/file.png в kb_devops как "Название"
загрузи PDF /docs/guide.pdf в kb_1c_buh
загрузи в kb_python из URL: https://docs.python.org/...
покажи состояние базы знаний
```

---

## Пути и сервисы

| Сервис | Адрес |
|--------|-------|
| Qdrant | http://192.168.0.200:6333 |
| Ollama | http://192.168.0.200:11434 |
| n8n | https://n8nwint.ru |
| MCP / Telegram proxy | http://192.168.0.66:3033 |
| Файловый сервер (изображения) | http://192.168.0.66:3033/files/ |

| Воркфлоу | ID | Назначение |
|----------|----|------------|
| RAG Query | ukODGfQwN2ShcLLJ | Поиск + ответ в Telegram |
| Ingest | Z3EO43BdXe7qKq0f | Загрузка документов |

| Сервис | Команда |
|--------|---------|
| Watcher (1C/Python/DevOps RAG) | `systemctl --user restart 1c-watcher` |
| OpenClaw | `systemctl --user restart openclaw-gateway` |
