---
name: 1c-assistant
description: Используй когда пользователь пишет /1c или /1c-help (команды справки по 1С), или задаёт вопросы про 1С ERP, 1С Бухгалтерию, ЗУП, BSL программирование, права и роли пользователей 1С, запросы к регистрам, управляемые формы, конфигуратор, начисление зарплаты, НДФЛ, НДС, проводки, печатные формы. Всегда отвечай только на русском языке.
---

# Скилл: 1C AI Assistant

Отвечает на вопросы по 1С через локальный RAG (Qdrant + bge-m3 + qwen3:14b).

## Триггеры

**При `/1c` или `/1c-help` или "покажи состояние базы 1С"** — НЕМЕДЛЕННО выполнить:
```bash
bash /home/alexandr/.openclaw/workspace/1c-assistant/1c-help.sh 1360549978
```
Это всё. Больше ничего не делать, не генерировать текст. Скрипт сам отправит справку в Telegram.

Активировать при ключевых словах:
- **1С общее:** "1с", "1с erp", "1с бухгалтерия", "конфигуратор", "1с предприятие", "1с zup", "1с зуп"
- **Разработка:** "bsl", "встроенный язык", "запрос 1с", "схема данных", "регистр", "управляемые формы", "общий модуль"
- **Администрирование:** "права 1с", "роли 1с", "пользователи 1с", "рабочие места", "ограничение доступа"
- **Документы/Справочники:** "справочник", "документ 1с", "реквизит", "табличная часть"

## Определение коллекции по теме

| Тема | Коллекция |
|------|-----------|
| BSL код, синтаксис, диагностики, оптимизация | `kb_1c_code` |
| Права, роли, пользователи, администрирование | `kb_1c_admin` |
| Бухгалтерия, налоги, отчётность, счета | `kb_1c_buh` |
| ЗУП, кадры, зарплата, отпуска, больничные | `kb_1c_zup` |
| Печатные формы, шаблоны, макеты | `kb_1c_forms` |
| Всё остальное (ERP, НСИ, настройка) | `kb_1c_erp` |

## Алгоритм выполнения

### 1. Определить коллекцию из таблицы выше

### 2. Вызвать RAG Query webhook

```bash
QUESTION="<вопрос пользователя>"
COLLECTION="<коллекция из таблицы>"

curl -s -X POST https://n8nwint.ru/webhook/1c-rag-query \
  -H "Content-Type: application/json" \
  -d "$(jq -n \
    --arg question "$QUESTION" \
    --arg chat_id "1360549978" \
    --arg collection "$COLLECTION" \
    --arg model "qwen3:14b" \
    '{question: $question, chat_id: $chat_id, collection: $collection, model: $model}'
  )"
```

Ответ придёт в Telegram (30-60 сек). Сообщить пользователю: "Запрос отправлен, ответ придёт в Telegram."

### 3. Если нужен синхронный ответ (не через Telegram)

```bash
# Прямой запрос через Qdrant + Ollama
QUESTION="<вопрос>"
COLLECTION="<коллекция>"
QDRANT="http://192.168.0.200:6333"
OLLAMA="http://192.168.0.200:11434"
QDRANT_KEY="zkpDII8FaBpzpRke8uWWcOEJDGXxKNsn"

# 1. Получить embedding вопроса
VECTOR=$(curl -s -X POST "$OLLAMA/api/embeddings" \
  -H "Content-Type: application/json" \
  -d "{\"model\": \"bge-m3\", \"prompt\": \"$QUESTION\"}" | jq '.embedding')

# 2. Поиск в Qdrant
CONTEXT=$(curl -s -X POST "$QDRANT/collections/$COLLECTION/points/search" \
  -H "Content-Type: application/json" \
  -H "api-key: $QDRANT_KEY" \
  -d "{\"vector\": $VECTOR, \"limit\": 5, \"with_payload\": true}" \
  | jq -r '.result[] | .payload.text' | head -c 3000)

# 3. Ответ через Ollama
curl -s -X POST "$OLLAMA/api/generate" \
  -H "Content-Type: application/json" \
  -d "$(jq -n \
    --arg model "qwen3:14b" \
    --arg prompt "Ты старший специалист по 1С с 10+ годами опыта. Отвечай структурированно, на русском языке.\n\nКонтекст из базы знаний:\n$CONTEXT\n\nВопрос: $QUESTION\n\nОтвет:" \
    '{model: $model, prompt: $prompt, stream: false}'
  )" | jq -r '.response'
```

## Загрузка изображений и скриншотов

Когда пользователь просит добавить скриншот, фото, изображение:

```bash
# Изображение с сервера
bash /home/alexandr/.openclaw/workspace/1c-assistant/ingest_image.sh \
  "/path/to/screenshot.png" \
  "kb_devops" \
  "Название скриншота"

# Изображение по URL
bash /home/alexandr/.openclaw/workspace/1c-assistant/ingest_image.sh \
  "https://example.com/screenshot.png" \
  "kb_python" \
  "Название"
```

Что делает скрипт:
1. OCR через tesseract (rus+eng) — извлекает текст
2. Копирует в /tmp/mcp-serve/ — картинка становится доступна по URL
3. Отправляет в wf21 с `image_url` в payload
4. При RAG поиске — Telegram получит текстовый ответ + само фото

Коллекции для изображений: те же что для текста (kb_python, kb_devops, kb_1c_code и т.д.)

## Загрузка PDF документов

Когда пользователь просит загрузить PDF — спросить:
1. Путь к файлу на сервере ИЛИ URL к PDF
2. Коллекцию (из таблицы выше)
3. Название документа

Использовать универсальный скрипт (автоматически определяет скан и запускает OCR):

```bash
# PDF по пути на сервере
bash /tmp/1c-assistant/scripts/ingest_pdf.sh \
  "/home/alexandr/docs/guide.pdf" \
  "kb_1c_buh" \
  "Название документа"

# PDF по URL
bash /tmp/1c-assistant/scripts/ingest_pdf.sh \
  "https://example.com/doc.pdf" \
  "kb_1c_zup" \
  "Название документа"
```

Скрипт: текстовый PDF → pdftotext; скан → tesseract OCR (rus+eng). Уведомление придёт в Telegram.

## Загрузка новых документов (text/url)

```bash
# Добавить URL в базу знаний
curl -s -X POST https://n8nwint.ru/webhook/1c-ingest \
  -H "Content-Type: application/json" \
  -d "$(jq -n \
    --arg type "url" \
    --arg collection "<коллекция>" \
    --arg title "<название>" \
    --arg url "<url>" \
    --arg chat_id "1360549978" \
    --arg version_1c "8.3" \
    '{type: $type, collection: $collection, title: $title, url: $url, chat_id: $chat_id, version_1c: $version_1c}'
  )"

# Добавить текст напрямую
curl -s -X POST https://n8nwint.ru/webhook/1c-ingest \
  -H "Content-Type: application/json" \
  -d "$(jq -n \
    --arg type "text" \
    --arg collection "<коллекция>" \
    --arg title "<название>" \
    --arg text "<текст документа>" \
    --arg chat_id "1360549978" \
    --arg version_1c "8.3" \
    '{type: $type, collection: $collection, title: $title, text: $text, chat_id: $chat_id, version_1c: $version_1c}'
  )"
```

## Проверка состояния коллекций

```bash
QDRANT="http://192.168.0.200:6333"
QDRANT_KEY="zkpDII8FaBpzpRke8uWWcOEJDGXxKNsn"

for coll in kb_1c_erp kb_1c_buh kb_1c_zup kb_1c_code kb_1c_admin kb_1c_forms; do
  count=$(curl -s "$QDRANT/collections/$coll" \
    -H "api-key: $QDRANT_KEY" | jq '.result.points_count')
  echo "$coll: $count points"
done
```

## Эскалация

| Ситуация | Действие |
|----------|----------|
| score < 0.7 (нет контекста) | Попробовать kb_1c_erp как fallback |
| Все коллекции пустые | Ответить из знаний модели с пометкой "из общих знаний" |
| Вопрос про разработку конфигурации | Передать Codex скилл |
| Нужно добавить документацию | Использовать ingest webhook выше |
