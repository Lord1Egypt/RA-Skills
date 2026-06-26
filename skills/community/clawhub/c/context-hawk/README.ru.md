# 🦅 Context-Hawk

> **Страж памяти контекста AI** — Перестаньте терять нить, начните помнить, что важно.

*Дайте любому AI-агенту память, которая действительно работает — через сессии, темы и время.*

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-2026.3%2B-brightgreen)](https://github.com/openclaw/openclaw)
[![ClawHub](https://img.shields.io/badge/ClawHub-context--hawk-blue)](https://clawhub.com)

**English** | [中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Italiano](README.it.md) | [Русский](README.ru.md) | [Português (Brasil)](README.pt-BR.md)

---

## Что он делает

Большинство AI-агентов страдают от **амнезии** — каждая новая сессия начинается с нуля. Context-Hawk решает эту проблему с помощью системы управления памятью production-уровня, которая автоматически захватывает важное, даёт шуму угаснуть и вспоминает нужное в нужный момент.

**Без Context-Hawk:**
> "Я уже говорил тебе — я предпочитаю краткие ответы!"
> (следующая сессия, агент снова забывает)

**С Context-Hawk:**
> (применяет ваши коммуникационные предпочтения из сессии 1)
> ✅ Каждый раз доставляет краткий, прямой ответ

---

## ❌ Without vs ✅ With Context-Hawk (TODO: translate)

| Scenario | ❌ Without Context-Hawk | ✅ With Context-Hawk |
|----------|------------------------|---------------------|
| **New session starts** | Blank — knows nothing about you | ✅ Injects relevant memories automatically |
| **User repeats a preference** | "I told you before..." | Remembers from day 1 |
| **Long task runs for days** | Restart = start over | Task state persists via `hawk resume` |
| **Context gets large** | Token bill skyrockets | 5 compression strategies keep it lean |
| **Duplicate info** | Same fact stored 10 times | SimHash dedup — stored once |
| **Memory recall** | All similar, redundant injection | MMR diverse recall — no repetition |
| **Memory management** | Everything piles up forever | 4-tier decay — noise fades, signal stays |
| **Self-improvement** | Repeats the same mistakes | importance + access_count tracking → smart promotion |
| **Multi-agent team** | Each agent starts fresh | Shared memory via LanceDB |

---

## ✨ 12 основных функций

---

## ✨ 12 основных функций

| # | Функция | Описание |
|---|---------|-------|
| 1 | **Сохранение состояния задачи** | `hawk resume` — сохраняет состояние, продолжает после перезапуска |
| 2 | **4-уровневая память** | Working → Short → Long → Archive с затуханием Вейбулла |
| 3 | **Структурированный JSON** | Оценка важности (0-10), категория, уровень, слои L0/L1/L2 |
| 4 | **Оценка важности AI** | Автоматически оценивает воспоминания, отбрасывает малозначимое |
| 5 | **5 стратегий внедрения** | A(высокая важность) / B(по задаче) / C(недавнее) / D(Top5) / E(полное) |
| 6 | **5 стратегий сжатия** | summarize / extract / delete / promote / archive |
| 7 | **Самоанализ** | Проверяет ясность задачи, недостающую информацию, обнаружение циклов |
| 8 | **Векторный поиск LanceDB** | Опционально — гибридный vector + BM25 поиск |
| 9 | **Чистый memory fallback** | Работает без LanceDB, персистенция через JSONL |
| 10 | **Автодедупликация** | Автоматически объединяет повторяющиеся воспоминания |
| 11 | **MMR Recall** | Maximal Marginal Relevance — diverse recall, no repetition |
| 12 | **6-Category Extraction** | LLM-powered: fact / preference / decision / entity / task / other |

---

## 🚀 Быстрая установка

```bash
# Установка в одну строку (рекомендуется)
bash <(curl -fsSL https://raw.githubusercontent.com/relunctance/context-hawk/master/install.sh)

# Или напрямую через pip
pip install context-hawk

# Со всеми функциями (включая sentence-transformers)
pip install "context-hawk[all]"
```

---

## 📦 Память состояния задачи (самая ценная функция)

Даже после перезапуска, отключения питания или смены сессии Context-Hawk продолжает точно с того места, где остановился.

```json
// memory/.hawk/task_state.jsonl
{
  "task_id": "task_20260329_001",
  "description": "Завершить документацию API",
  "status": "in_progress",
  "progress": 65,
  "next_steps": ["Проверить шаблон архитектуры", "Доложить пользователю"],
  "outputs": ["SKILL.md", "constitution.md"],
  "constraints": ["Покрытие должно достичь 98%", "API должны быть версионированы"],
  "resumed_count": 3
}
```

```bash
hawk task "Завершить документацию"  # Создать задачу
hawk task --step 1 done          # Отметить шаг выполненным
hawk resume                         # Продолжить после перезапуска ← КЛЮЧЕВОЕ!
```

---

## 🧠 Структурированная память

```json
{
  "id": "mem_20260329_001",
  "type": "task|knowledge|conversation|document|preference|decision",
  "content": "Полное исходное содержимое",
  "summary": "Краткое изложение в одну строку",
  "importance": 0.85,
  "tier": "working|short|long|archive",
  "created_at": "2026-03-29T00:00:00+08:00",
  "access_count": 3,
  "decay_score": 0.92
}
```

### Оценка важности

| Оценка | Тип | Действие |
|-------|------|---------|
| 0.9-1.0 | Решения/правила/ошибки | Постоянно, slowest decay |
| 0.7-0.9 | Задачи/предпочтения/знания | Долгосрочная память |
| 0.4-0.7 | Диалог/обсуждение | Краткосрочное, decay to archive |
| 0.0-0.4 | Чат/приветствия | **Отбросить, никогда не сохранять** |

---

## 🎯 5 стратегий внедрения контекста

| Стратегия | Триггер | Экономия |
|----------|---------|---------|
| **A: Высокая важность** | `важность ≥ 0.7` | 60-70% |
| **B: По задаче** | scope совпадает | 30-40% ← по умолчанию |
| **C: Недавнее** | последние 10 оборотов | 50% |
| **D: Top5 напоминание** | top 5 по `access_count` | 70% |
| **E: Полное** | без фильтра | 100% |

---

## 🗜️ 5 стратегий сжатия

`summarize` · `extract` · `delete` · `promote` · `archive`

---

## 🔔 4-уровневая система оповещений

| Уровень | Порог | Действие |
|-------|-------|---------|
| ✅ Нормальный | < 60% | Тихий |
| 🟡 Наблюдение | 60-79% | Предложить сжатие |
| 🔴 Критический | 80-94% | Приостановить автозапись, форсировать предложение |
| 🚨 Опасность | ≥ 95% | Заблокировать записи, обязательное сжатие |

---

## 🚀 Быстрый старт

```bash
# Установить плагин LanceDB (рекомендуется)
openclaw plugins install memory-lancedb-pro@beta

# Активировать навык
openclaw skills install ./context-hawk.skill

# Инициализировать
hawk init

# Основные команды
hawk task "Моя задача"    # Создать задачу
hawk resume             # Продолжить последнюю задачу ← ОЧЕНЬ ВАЖНО
hawk status            # Показать использование контекста
hawk compress          # Сжать память
hawk strategy B        # Переключить в режим по задаче
hawk introspect         # Отчёт самоанализа
```

---

## Автотриггер: каждые N оборотов

Каждые **10 оборотов** (по умолчанию, настраивается), Context-Hawk автоматически:

1. Проверяет уровень контекста
2. Оценивает важность воспоминаний
3. Сообщает статус пользователю
4. Предлагает сжатие при необходимости

```bash
# Конфигурация (memory/.hawk/config.json)
{
  "auto_check_rounds": 10,          # проверять каждые N оборотов
  "keep_recent": 5,                 # сохранять последние N оборотов
  "auto_compress_threshold": 70      # сжимать когда > 70%
}
```

---

## Структура файлов

```
context-hawk/
├── SKILL.md
├── README.md
├── LICENSE
├── scripts/
│   └── hawk               # Python CLI-утилита
└── references/
    ├── memory-system.md           # 4-уровневая архитектура
    ├── structured-memory.md      # Формат памяти и важность
    ├── task-state.md           # Сохранение состояния задачи
    ├── injection-strategies.md  # 5 стратегий внедрения
    ├── compression-strategies.md # 5 стратегий сжатия
    ├── alerting.md             # Система оповещений
    ├── self-introspection.md   # Самоанализ
    ├── lancedb-integration.md  # Интеграция LanceDB
    └── cli.md                  # CLI-справочник
```

---

## Технические характеристики

| | |
|---|---|
| **Персистенция** | Локальные JSONL-файлы, без базы данных |
| **Векторный поиск** | LanceDB (опционально) + sentence-transformers локальное встраивание, автофоллбэк на файлы |
| **Поиск** | BM25 + ANN векторный поиск + RRF фьюжн |
| **Провайдеры Embedding** | Ollama / sentence-transformers / Jina AI / Minimax / OpenAI |
| **Cross-Agent** | Универсальный, без бизнес-логики, работает с любым AI-агентом |
| **Нулевая конфигурация** | Работает из коробки (режим BM25-only) |
| **Python** | 3.12+ |

---

## Лицензия

MIT — свободное использование, модификация и распространение.
