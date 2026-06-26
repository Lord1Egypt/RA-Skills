---
name: ai-orchestrator
description: Launch DeepSeek AI via Puppeteer browser automation with CDP interceptor for full API responses, persistent daemon for fast startup, health checks, graceful shutdown, and PM2 management. Production-ready.
---

# AI Orchestrator — Полный мануал оператора

**Для кого:** ИИ-агенты и операторы. **Статус:** Production-ready, v3.5 (2026-04-03)

## 1. Назначение

Надёжный доступ к DeepSeek AI через Puppeteer:
- **CDP-перехватчик API** — полные ответы без ожидания DOM
- **Persistent демон (PM2)** — подключение за ~35ms (vs ~15s холодный старт)
- **Health check** — auto-restart каждые 5 минут (`daemon-healthcheck.js`)
- **Graceful shutdown** — SIGTERM/SIGINT → корректное закрытие
- **Session persistence** (`--session`) — контекст между запросами
- **Fallback DOM extraction** — если CDP недоступен
- **Continue automation** — автоклик «Продолжить» до 30 раз + fallback через composer
- **Diagnostics** — crash-артфакты, трассировка фаз, метрики памяти
- **Smart rate limit** — экспоненциальный backoff при 429

**Free tier лимит (проверено 2026-04-03):** ~13 000 символов на ответ. Кнопка «Продолжить» может появиться — автоматический клик. Для длинных ответов: разбивай запрос на части через `--session`.

## 2. Быстрый старт

```bash
# Простой запрос
ask-deepseek.sh "Вопрос?"

# Сессия (контекст сохраняется)
ask-deepseek.sh "Вопрос 1" --session work
ask-deepseek.sh "Вопрос 2" --session work   # тот же чат
ask-deepseek.sh --session work --end-session # закрыть

# Демон (быстро, ~35ms)
ask-deepseek.sh "Вопрос" --daemon

# Пайп-поддержка
cat code.py | ask-deepseek.sh "Найди баги"      # pipe
ask-deepseek.sh <<'EOF'                          # heredoc
Длинный
мультитайн промпт
EOF

# Тест без отправки
./ask-deepseek.sh --dry-run
./ask-deepseek.sh "test" --daemon --dry-run
```

### Все флаги
`--session NAME` | `--search` | `--think` | `--new-chat` | `--end-session` | `--daemon` | `--visible` | `--wait` | `--close` | `--debug` | `--verbose` | `--dry-run` | `-h`

## 3. Архитектура

```
ask-deepseek.sh (wrapper: парсит флаги, stdin, дата)
  └─ ask-puppeteer.js (ядро ~1600 строк)
       ├─ setupDeepSeekInterceptor() — CDP Network API перехват
       ├─ sendPrompt() — отправка через DOM events + Enter
       ├─ waitForAnswer() — основной цикл: CDP → DOM polling → idle timeout
       ├─ extractBestText() — извлечение последнего текста со страницы
       ├─ extractAnswerFromDOM() — полный ответ из DOM
       ├─ handleContinueButton() — кнопка «Продолжить» + fallback через composer
       ├─ ensureBrowser(session, diag) — 3 попытки: демон → сессия → новый
       └─ ask(q) — главная функция + диагностика
  ├─ diagnostics.js (единый: trace + metrics + counters)
  ├─ deepseek-daemon.js (PM2: постоянный Chrome headless)
  ├─ daemon-healthcheck.js (PM2 cron: каждые 5 мин + авто-ресарт)
  └─ auth-check.js (DOM-проверка авторизации, score-based)
```

**Диагностический конвейер:**
```
ask()
 ──► new Diagnostics()           ← создаёт traceId, логирует фазы
 ──► diag.start('INIT')          ← фаза: проверка rate limit
 ──► diag.start('BROWSER_LAUNCH')← демон/сессия/новый браузер
 ──► diag.start('AUTH_CHECK')    ← requireAuth(), score 10 = OK
 ──► diag.start('COMPOSER_WAIT') ← ждём textarea
 ──► diag.start('PROMPT_SEND')   ← ввод промпта
 ──► diag.start('ANSWER_WAIT')   ← CDP signal → DOM polling → idle timeout
     └─► diag.start('CONTINUE')  ← кнопка «Продолжить» или fallback
 ──► diag.start('ANSWER_EXTRACT')← финальное извлечение
 ──► diag.printSummary()         ← метрики
 ──► diag.save()                 ← JSON + JSONL файлы в .diagnostics/
```

## 4. Ключевые файлы

| Файл | Роль |
|------|------|
| `ask-deepseek.sh` | CLI wrapper: флаги, stdin (pipe/heredoc), дата в промпте, --dry-run |
| `ask-puppeteer.js` | Ядро (~1600 строк). Браузер, CDP, extraction, continue, config |
| `diagnostics.js` | Единый модуль: trace фаз, метрики памяти, counters, JSON/JSONL output |
| `deepseek-daemon.js` | Запускает Chrome headless, пишет `.daemon-ws-endpoint` |
| `daemon-healthcheck.js` | Health check: connect → CDP → composer. Auto-restart через PM2 |
| `auth-check.js` | DOM-проверка авторизации, score-based |
| `.deepseek.json` | Конфиг: таймауты, пороги, логирование в файл |
| `.profile/` | Chrome user data dir (persist session, cookies) |
| `.sessions/` | Session JSON файлы |
| `.diagnostics/` | Trace JSONL, metrics JSON, crash screenshots |
| `.healthcheck.log` | Логи health check |

## 5. Конфигурация (`.deepseek.json`)

Все таймауты и пороги в одном файле. Изменения вступают в силу сразу.

```json
{
  "timeouts": {
    "browserLaunch": 30000,
    "answerWait": 600000,
    "composer": 10000,
    "navigation": 30000,
    "idleTimeout": 15000,
    "heartbeatInterval": 15000,
    "domErrorIdle": 25000
  },
  "thresholds": {
    "minResponseLength": 50,
    "maxContinueRounds": 30,
    "selectorCacheMax": 20
  },
  "diagnostics": { "enabled": true, "dir": ".diagnostics" },
  "logToFile": false,
  "logPath": ".logs/deepseek.log"
}
```

## 6. Диагностика

Каждый запрос генерирует в `.diagnostics/`:
- **`trace-<id>.jsonl`** — JSONL-лог фаз (start/succeed/fail)
- **`metrics-<id>.json`** — memory, timing, counts, completeness, platform info
- **`summary-<id>.json`** — краткий machine-readable итог прогона

Дополнительно:
- **`.logs/deepseek.log`** — сквозной файловый лог stdout/stderr событий (если `logToFile=true`)

При crash:
- **`.diagnostics/error-<ts>.png`** — скриншот страницы
- **`.diagnostics/error-<ts>.html`** — HTML страницы

**Trace ID** выводится в stdout: `🔖 Trace ID: tr-xxxxxxxx-xxxx`

## 7. Неисправности и Решения

### Quick Symptom Index
| Symptom | First action |
|---------|--------------|
| `Connection refused` / daemon dead | `pm2 restart deepseek-daemon && sleep 8` |
| Login/CAPTCHA/auth expired | `pm2 stop deepseek-daemon && rm -f .daemon-ws-endpoint && ./ask-deepseek.sh "auth" --visible --wait --dry-run && pm2 start deepseek-daemon` |
| Long answer cut off | switch to `--session` and split prompt into chunks |
| Composer timeout | run `./ask-deepseek.sh --dry-run` first |
| Chrome/profile weird state | `rm -f .profile/Singleton* && pm2 restart deepseek-daemon` |

## 7. Неисправности и Решения

### A. CAPTCHA / Сессия истекла
**Симптомы:** бесконечные попытки, в видимом браузере CAPTCHA или страница логина.

**Решение:**
```bash
pm2 stop deepseek-daemon
rm -f .daemon-ws-endpoint
./ask-deepseek.sh "auth" --visible --wait --dry-run
pm2 start deepseek-daemon
```

**Важно:** видимый браузер не должен цепляться к скрытому daemon Chrome. Если нужен ручной логин — сначала останови daemon.

### B. Демон не отвечает / Connection refused
**Симптомы:** `Connection refused to ws://...`

**Решение:**
```bash
pm2 restart deepseek-daemon && sleep 8 && cat .daemon-ws-endpoint
```

### C. Lock файлы (Chrome already running)
**Симптомы:** `Cannot find module`, `.profile` lock.

**Решение:**
```bash
pkill -f "ai-orchestrator/.profile" && rm -f .profile/Singleton* && pm2 restart deepseek-daemon
```

### D. Ответ обрывается (INCOMPLETE_LIMIT_REACHED)
**Причина:** Free tier лимит ~13k символов на один ответ. Кнопка «Продолжить» появляется не всегда.

**Что делает навык:**
1. Ждёт кнопку «Продолжить» — если нашёл, кликает (до 30 раз)
2. Если кнопки нет, отправляет «Продолжи» через Enter в composer (fallback)
3. Если fallback не принёс текста → idle timeout 15 сек → возврат partial

**Решение для длинных ответов:**
```bash
# Разбей на части с --session
ask-deepseek.sh "Напиши руководство по Python: 1) структуры данных 2) ООП" --session guide
ask-deepseek.sh "Теперь паттерны проектирования" --session guide
ask-deepseek.sh "Теперь async, базы данных, REST API" --session guide
ask-deepseek.sh --session guide --end-session
```

### E. Fallback не работает (текст перезаписывается)
**Симптомы:** Fallback отправил «Продолжи», но текст уменьшился (Delta < 0).
**Причина:** DeepSeek иногда перезаписывает ответ вместо продолжения, особенно после idle timeout.
**Решение:** Это ограничение free tier. Используй `--session` и задавай запросы более короткими частями.

### F. PM2 не запускается / MODULE_NOT_FOUND
**Симптомы:** PM2 errored, модули не найдены после перемещения.

**Решение:**
```bash
pm2 delete deepseek-daemon
cd ~/.openclaw/workspace/skills/ai-orchestrator
pm2 start deepseek-daemon.js --name deepseek-daemon --no-autorestart
pm2 save
```

### G. Селекторы устарели (UI DeepSeek изменился)
**Симптомы:** `Timeout waiting for composer element`.

**Решение:**
```bash
ask-deepseek.sh "test" --visible
# В браузере: DevTools → проверка селекторов
# В коде: обновить COMPOSER и RESPONSE_SELECTORS в ask-puppeteer.js
```

### H. Rate limit / Smart Backoff
**Симптомы:** `Smart rate limit: backing off Xs (attempt #N)`.
**Причина:** Последовательные 429 ошибки от DeepSeek.
**Механизм:** Бэкoфф удваивается (5s → 10s → 20s → 40s). Сбрасывается при успехе.
**Решение:** Подождать. Навык делает это автоматически. Для избежания: пауза >5 сек между запросами.

## 8. Управление демоном через PM2

```bash
# Запуск
pm2 start deepseek-daemon.js --name deepseek-daemon --no-autorestart
pm2 save

# Управление
pm2 status deepseek-daemon
pm2 restart deepseek-daemon && sleep 8
pm2 stop deepseek-daemon
pm2 delete deepseek-daemon

# Логи
pm2 logs deepseek-daemon --lines 50 --nostream
tail -f .healthcheck.log
```

**PM2 auto-start при загрузке:**
```bash
pm2 startup       # создаёт init script
pm2 save          # сохраняет текущие процессы
```

## 9. Примечания к бенчмаркам

Для надёжных замеров:
- Используй `--daemon` (стабильное ~35ms подключение)
- Измеряй **сырой вывод** (stdout), не сводку subagents
- Файлы метрик: `.diagnostics/metrics-tr-<id>.json`
- Для повторных тестов: `pm2 flush && rm .diagnostics/metrics-*`

## 10. Файлы и управление

**Не удалять:**
- `ask-puppeteer.js`, `deepseek-daemon.js`, `daemon-healthcheck.js`
- `diagnostics.js`, `auth-check.js`, `SKILL.md`, `ask-deepseek.sh`
- `.daemon-ws-endpoint`, `.profile/`, `.sessions/`, `package.json`

**Можно чистить:**
- Дампы диагностики: `rm -f .diagnostics/error-*.png .diagnostics/error-*.html`
- Логи PM2: `pm2 flush`
- Сессии: `rm -f .sessions/*.json`

## 11. Производительность (проверено 2026-04-03)

| Тест | Длина ответа | Время | Статус |
|------|-------------|-------|--------|
| Малый (3 предложения) | **309** символов | **16с** | ✅ |
| Средний (3 паттерна) | **5,713** символов | **51с** | ✅ |
| Длинный (руководство) | **13,053** символа | **59с** | ⚠️ Limit reached |

**Константы:**
- Daemon подключение: ~35ms
- Отправка промпта: <50ms
- Idle timeout: 15 сек без изменений текста
- DOM error timeout: 25 сек без успешного извлечения
- Smart rate limit: 5с базовый, удваивается при 429
- Пик памяти Node: 74–79 MB

## 12. Скрипты: детали

### `ask-deepseek.sh` — CLI wrapper
- Парсит флаги, добавляет дату, вызывает `ask-puppeteer.js`
- **stdin support**: `cat file \| ask-deepseek.sh "анализ"`, `ask-deepseek.sh --stdin < file.txt` или heredoc
- **argv + stdin merge**: если передан и аргумент, и stdin, wrapper собирает промпт как `<аргументы> + пустая строка + <stdin>`
- **--dry-run**: проверка auth + composer без отправки промпта
- Без `--daemon`: добавляет `--close` автоматически

### `ask-puppeteer.js` — ядро
Основные функции:
- `loadConfig()` — читает `.deepseek.json` с defaults
- `ensureBrowser(session, diag)` — 3 попытки: демон → сессия → новый + auto-recovery
- `setupDeepSeekInterceptor(page)` — CDP Network API перехват
- `sendPrompt(page, sel, prompt)` — отправка через DOM events + Enter
- `waitForAnswer(page, diag, ...)` — основной цикл (CDP signal → DOM polling → idle timeout)
- `handleContinueButton(page, text)` — поиск кнопки «Продолжить», fallback через composer
- `extractAnswerFromDOM(page, ...)` — парсинг DOM для ответа
- `extractBestText(page)` — последний текст со страницы (используется в continue)

### `diagnostics.js` — единый модуль диагностики
Заменяет `pipeline-trace.js` + `metrics-collector.js`:
- Trace фаз: start/succeed/fail/skip с таймаутами и метаданными
- Память: Node.js memory snapshots
- Counters: retry, continue, extraction attempts
- Output: JSONL (trace) + JSON (metrics) + JSON (summary) + stdout summary

### `deepseek-daemon.js` — демон PM2
- Запускает Chrome headless с `userDataDir: .profile/`
- Пишет `.daemon-ws-endpoint` для клиентов
- Graceful shutdown: SIGTERM → browser.close()

### `daemon-healthcheck.js` — health check
- Подключается к браузеру через wsEndpoint, проверяет composer
- 2 consecutive failure → `pm2 restart deepseek-daemon`
- Высокая память (>1.5GB) → рестарт
- Логи: `.healthcheck.log`

### `auth-check.js` — авторизация
- DOM-проверка по сигналам: presence of textarea, absence of login/CAPTCHA
- Score-based: 10 = OK, 0 = не авторизован

---

*История изменений в `.backup-cleanup/`. Конфигурация в `.deepseek.json`. Диагностика теперь единая через `diagnostics.js`.*
