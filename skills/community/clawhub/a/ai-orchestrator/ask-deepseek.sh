#!/bin/bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TODAY=$(date '+%Y-%m-%d %H:%M %Z')

SEARCH_MODE=false
THINK_MODE=false
SESSION_NAME="${DEEPSEEK_SESSION:-}"
USE_DAEMON=false
DRY_RUN=false
VISIBLE=false
WAIT_FOR_AUTH=false
CLOSE_BROWSER=false
DEBUG_MODE=false
VERBOSE_MODE=false
FORCE_STDIN=false
START_NEW_CHAT=false
END_SESSION=false
QUESTION=""
STDIN_TEXT=""

SESSION_ARGS=()
PUPPETEER_ARGS=()

if [[ -n "$SESSION_NAME" ]]; then
  SESSION_ARGS=(--session "$SESSION_NAME")
fi

while [[ $# -gt 0 ]]; do
  case "$1" in
    --search) SEARCH_MODE=true; shift ;;
    --think) THINK_MODE=true; shift ;;
    --session)
      SESSION_NAME="$2"
      SESSION_ARGS=(--session "$2")
      shift 2
      ;;
    --new-chat) START_NEW_CHAT=true; shift ;;
    --end-session) END_SESSION=true; shift ;;
    --daemon) USE_DAEMON=true; shift ;;
    --visible) VISIBLE=true; shift ;;
    --wait) WAIT_FOR_AUTH=true; shift ;;
    --dry-run) DRY_RUN=true; shift ;;
    --close) CLOSE_BROWSER=true; shift ;;
    --debug) DEBUG_MODE=true; shift ;;
    --verbose) VERBOSE_MODE=true; shift ;;
    --stdin) FORCE_STDIN=true; shift ;;
    --help|-h)
      cat <<'EOF'
ask-deepseek.sh — универсальный wrapper (Puppeteer с демоном)

Использование:
  ask-deepseek.sh "вопрос"                    — одиночный запрос
  ask-deepseek.sh --session work "вопрос"     — сессия
  ask-deepseek.sh --session work "ещё вопрос" — продолжение сессии
  ask-deepseek.sh --session work --new-chat "вопрос" — новый чат в сессии
  ask-deepseek.sh --session work --end-session    — завершить сессию
  ask-deepseek.sh --search "запрос"           — поиск в интернете
  ask-deepseek.sh --daemon                    — использовать демон (быстрее)
  cat file.txt | ask-deepseek.sh "проанализируй"   — argv + stdin
  ask-deepseek.sh --stdin < file.txt          — читать промпт из stdin явно

Флаги:
  --session NAME   Имя сессии
  --search         Включить веб-поиск
  --think          Включить глубокое мышление (DeepThink)
  --new-chat       Начать новый чат в сессии
  --end-session    Завершить сессию
  --daemon         Использовать фоновый Chrome (ускоряет запросы)
  --visible        Открыть видимый браузер (если нужна авторизация)
  --wait           Ждать ручной авторизации (с --visible)
  --dry-run        Проверить auth + composer без реального вопроса
  --stdin          Явно читать тело промпта из stdin
  --close          Закрыть браузер после ответа (без демона)
  --debug          Включить отладку
  --verbose        Подробный лог
  -h, --help       Показать эту справку

stdin / heredoc:
  Если stdin подключён не к терминалу, wrapper автоматически читает его.
  Если одновременно передан текст аргументом, итоговый промпт будет:
  <аргументы> + пустая строка + <stdin>

Демон:
  Запуск демона:   pm2 start deepseek-daemon.js --name deepseek-daemon --no-autorestart
  Останов:         pm2 stop deepseek-daemon
  Автозапуск:      pm2 save && pm2 startup systemd -u $USER --hp $HOME
EOF
      exit 0
      ;;
    --)
      shift
      while [[ $# -gt 0 ]]; do
        QUESTION="${QUESTION:+$QUESTION }$1"
        shift
      done
      ;;
    -*)
      echo "Неизвестный флаг: $1. Запусти --help"
      exit 1
      ;;
    *)
      QUESTION="${QUESTION:+$QUESTION }$1"
      shift
      ;;
  esac
done

if [[ "$FORCE_STDIN" = true ]]; then
  if [[ -t 0 ]]; then
    echo "Ошибка: --stdin указан, но stdin не передан" >&2
    exit 1
  fi
  STDIN_TEXT=$(cat)
elif [[ ! -t 0 ]]; then
  STDIN_TEXT=$(cat)
fi

if [[ -n "$STDIN_TEXT" ]]; then
  if [[ -n "$QUESTION" ]]; then
    QUESTION="${QUESTION}"$'\n\n'"${STDIN_TEXT}"
  else
    QUESTION="$STDIN_TEXT"
  fi
fi

# End session
if [[ "$END_SESSION" = true ]]; then
  if [[ -n "$SESSION_NAME" ]]; then
    node "$SCRIPT_DIR/ask-puppeteer.js" "${SESSION_ARGS[@]}" --end-session 2>/dev/null || true
    rm -f "$SCRIPT_DIR/.sessions/${SESSION_NAME}.json"
    echo "Сессия '$SESSION_NAME' завершена"
  else
    echo "Ошибка: --end-session требует --session NAME" >&2
    exit 1
  fi
  exit 0
fi

if [[ -z "$QUESTION" && "$DRY_RUN" = true ]]; then
  QUESTION="dry-run"
fi

if [[ -z "$QUESTION" ]]; then
  echo "Ошибка: нужен вопрос. Запусти --help для справки"
  echo "  ask-deepseek.sh \"вопрос\""
  echo "  cat file.txt | ask-deepseek.sh \"проанализируй\""
  echo "  ask-deepseek.sh --stdin < file.txt"
  echo "  ask-deepseek.sh <<'EOF'"
  echo "  длинный текст"
  echo "  EOF"
  exit 1
fi

# Промпт с датой и режимами
FULL_PROMPT="[Дата: ${TODAY}]"
[[ "$SEARCH_MODE" = true ]] && FULL_PROMPT="$FULL_PROMPT [РЕЖИМ: ПОИСК В ИНТЕРНЕТЕ]"
[[ "$THINK_MODE" = true ]] && FULL_PROMPT="$FULL_PROMPT [РЕЖИМ: DEEP THINK]"
FULL_PROMPT="$FULL_PROMPT $QUESTION"

# Флаги для ask-puppeteer.js
[[ "$SEARCH_MODE" = true ]] && PUPPETEER_ARGS+=(--search)
[[ "$THINK_MODE" = true ]] && PUPPETEER_ARGS+=(--think)
[[ -n "$SESSION_NAME" ]] && PUPPETEER_ARGS+=("${SESSION_ARGS[@]}")
[[ "$START_NEW_CHAT" = true ]] && PUPPETEER_ARGS+=(--new-chat)
[[ "$USE_DAEMON" = true ]] && PUPPETEER_ARGS+=(--daemon)
[[ "$VISIBLE" = true ]] && PUPPETEER_ARGS+=(--visible)
[[ "$WAIT_FOR_AUTH" = true ]] && PUPPETEER_ARGS+=(--wait)
[[ "$DRY_RUN" = true ]] && PUPPETEER_ARGS+=(--dry-run)
[[ "$CLOSE_BROWSER" = true ]] && PUPPETEER_ARGS+=(--close)
[[ "$DEBUG_MODE" = true ]] && PUPPETEER_ARGS+=(--debug)
[[ "$VERBOSE_MODE" = true ]] && PUPPETEER_ARGS+=(--verbose)

PROMPT_FILE="$(mktemp)"
cleanup_prompt_file() {
  rm -f "$PROMPT_FILE"
}
trap cleanup_prompt_file EXIT
printf '%s' "$FULL_PROMPT" > "$PROMPT_FILE"

echo "📅 $TODAY"
[[ -n "$SESSION_NAME" ]] && echo "🔄 Сессия: $SESSION_NAME"
[[ "$SEARCH_MODE" = true ]] && echo "🔍 Поиск"
[[ "$THINK_MODE" = true ]] && echo "🧠 DeepThink"
[[ "$USE_DAEMON" = true ]] && echo "⚡ Режим демона (быстрый)"
echo ""

# Проверяем демон
if [[ "$USE_DAEMON" = true ]]; then
  if [[ ! -f "$SCRIPT_DIR/.daemon-ws-endpoint" ]]; then
    # Fallback: daemon session metadata may still be present during restart races.
    if [[ -f "$SCRIPT_DIR/.sessions/daemon.json" ]]; then
      daemon_ws=$(node -e 'try{const fs=require("fs");const p=process.argv[1];const j=JSON.parse(fs.readFileSync(p,"utf8"));if(j&&j.browserWSEndpoint)process.stdout.write(j.browserWSEndpoint)}catch(e){}' "$SCRIPT_DIR/.sessions/daemon.json")
      if [[ -n "$daemon_ws" ]]; then
        printf '%s' "$daemon_ws" > "$SCRIPT_DIR/.daemon-ws-endpoint"
      fi
    fi
  fi
  if [[ ! -f "$SCRIPT_DIR/.daemon-ws-endpoint" ]]; then
    echo "❌ Демон не запущен. Запусти: cd \"$SCRIPT_DIR\" && pm2 start deepseek-daemon.js --name deepseek-daemon --no-autorestart"
    exit 1
  fi
fi

# Запускаем puppeteer
if [[ "$USE_DAEMON" = true ]]; then
  node "$SCRIPT_DIR/ask-puppeteer.js" --file "$PROMPT_FILE" "${PUPPETEER_ARGS[@]}" 2>&1
else
  # Без демона — закрываем браузер после
  node "$SCRIPT_DIR/ask-puppeteer.js" --file "$PROMPT_FILE" "${PUPPETEER_ARGS[@]}" --close 2>&1
fi

EXIT_CODE=$?

exit $EXIT_CODE
