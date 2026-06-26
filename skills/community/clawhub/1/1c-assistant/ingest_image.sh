#!/bin/bash
# ingest_image.sh — загрузка изображения в базу знаний через OCR
# Использование:
#   ingest_image.sh <путь_к_файлу_или_URL> <коллекция> <название> [chat_id]
#   ingest_image.sh /path/to/screenshot.png kb_devops "Nginx конфиг пример"
#   ingest_image.sh https://example.com/img.png kb_python "FastAPI схема"

set -e

IMAGE_INPUT="${1}"
COLLECTION="${2:-kb_devops}"
TITLE="${3:-Без названия}"
CHAT_ID="${4:-1360549978}"

INGEST_WEBHOOK="https://n8nwint.ru/webhook/1c-ingest"
SERVE_DIR="/home/alexandr/.openclaw/media/kb-images"
SERVE_URL_BASE="http://192.168.0.66:3033/files"
TEMP_DIR=$(mktemp -d)

cleanup() { rm -rf "$TEMP_DIR"; }
trap cleanup EXIT

echo "[ingest_image] Входной файл: $IMAGE_INPUT"
echo "[ingest_image] Коллекция: $COLLECTION | Название: $TITLE"

# === 1. Получить изображение ===
if echo "$IMAGE_INPUT" | grep -qE '^https?://'; then
    echo "[ingest_image] Скачиваем изображение..."
    IMAGE_FILE="$TEMP_DIR/image.png"
    curl -sL "$IMAGE_INPUT" -o "$IMAGE_FILE"
else
    IMAGE_FILE="$IMAGE_INPUT"
fi

if [ ! -f "$IMAGE_FILE" ]; then
    echo "[ingest_image] ERROR: файл не найден: $IMAGE_FILE"
    exit 1
fi

# === 2. Копировать в постоянное хранилище для раздачи ===
mkdir -p "$SERVE_DIR"
FILENAME="kb_$(date +%s)_$(basename "$IMAGE_FILE" | tr ' ' '_')"
cp "$IMAGE_FILE" "$SERVE_DIR/$FILENAME"
IMAGE_URL="$SERVE_URL_BASE/$FILENAME"
echo "[ingest_image] Изображение доступно: $IMAGE_URL"

# === 3. OCR через tesseract ===
echo "[ingest_image] Запускаем OCR..."
OCR_OUTPUT="$TEMP_DIR/ocr_result"
tesseract "$IMAGE_FILE" "$OCR_OUTPUT" -l rus+eng --psm 3 quiet 2>/dev/null || \
tesseract "$IMAGE_FILE" "$OCR_OUTPUT" -l eng --psm 3 quiet 2>/dev/null || true

OCR_TEXT=""
if [ -f "${OCR_OUTPUT}.txt" ]; then
    OCR_TEXT=$(cat "${OCR_OUTPUT}.txt" | tr -d '\r' | sed '/^[[:space:]]*$/d')
fi

if [ -z "$OCR_TEXT" ]; then
    OCR_TEXT="[Изображение без текста: $TITLE]"
    echo "[ingest_image] OCR: текст не найден, используем описание"
else
    echo "[ingest_image] OCR: извлечено $(echo "$OCR_TEXT" | wc -c) символов"
fi

# Добавляем метаданные к тексту для лучшего поиска
FULL_TEXT="## $TITLE

$OCR_TEXT

[Изображение: $IMAGE_URL]"

# === 4. Отправить в wf21 ===
echo "[ingest_image] Отправляем в базу знаний..."
PAYLOAD=$(python3 -c "
import json, sys
text = sys.argv[1]
print(json.dumps({
    'type': 'image',
    'collection': '$COLLECTION',
    'title': '$TITLE',
    'text': text,
    'image_url': '$IMAGE_URL',
    'chat_id': '$CHAT_ID',
    'version_1c': 'n/a'
}))
" "$FULL_TEXT")

RESULT=$(curl -s -X POST "$INGEST_WEBHOOK" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD")

echo "[ingest_image] Результат wf21: $RESULT"
echo "[ingest_image] Готово! Изображение '$TITLE' загружено в $COLLECTION"
echo "[ingest_image] URL: $IMAGE_URL"
