#!/bin/bash
# /1c-help — отправляет справку по 1С ассистенту в Telegram

CHAT_ID="${1:-1360549978}"
BOT_URL="http://192.168.0.66:3033/send-telegram"
QDRANT="http://192.168.0.200:6333"
QDRANT_KEY="zkpDII8FaBpzpRke8uWWcOEJDGXxKNsn"

# Получить counts коллекций
get_count() {
  curl -s --max-time 5 "$QDRANT/collections/$1" \
    -H "api-key: $QDRANT_KEY" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('result',{}).get('points_count',0))" 2>/dev/null || echo "?"
}

CODE=$(get_count kb_1c_code)
ADMIN=$(get_count kb_1c_admin)
BUH=$(get_count kb_1c_buh)
ZUP=$(get_count kb_1c_zup)
FORMS=$(get_count kb_1c_forms)
ERP=$(get_count kb_1c_erp)

MSG="🤖 *1С Ассистент — Справка*

*Задать вопрос:*
Просто напиши вопрос — Кузя ответит автоматически.

Примеры:
• как написать запрос к регистру накопления?
• как начислить зарплату в ЗУП?
• как настроить права на справочник?
• как сделать печатную форму?

*База знаний (документов):*
📦 \`kb_1c_code\` — BSL код, диагностики: *${CODE}*
🔐 \`kb_1c_admin\` — Права, роли: *${ADMIN}*
📊 \`kb_1c_buh\` — Бухгалтерия, НДС: *${BUH}*
👥 \`kb_1c_zup\` — ЗУП, зарплата, НДФЛ: *${ZUP}*
🖨 \`kb_1c_forms\` — Печатные формы: *${FORMS}*
🏭 \`kb_1c_erp\` — ERP, общее: *${ERP}*

*Загрузить документ:*
— Текст: скажи Кузе «добавь в базу 1С [коллекция]: текст»
— URL: «загрузи в kb_1c_code из URL: https://...»
— PDF: «загрузи PDF /path/file.pdf в kb_1c_buh»

*Ответ на вопросы приходит в Telegram ~30-60 сек*"

curl -s -X POST "$BOT_URL" \
  -H "Content-Type: application/json" \
  -d "$(python3 -c "
import json, sys
print(json.dumps({'chat_id': '$CHAT_ID', 'text': sys.stdin.read()}))
" <<< "$MSG")"
