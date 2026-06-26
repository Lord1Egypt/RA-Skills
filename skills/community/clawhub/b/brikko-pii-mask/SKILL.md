---
name: brikko-pii-mask
version: 0.1.0
description: |
  Маскирует персональные данные (ФИО, ИНН, СНИЛС, ОГРН, ОГРНИП, паспорт,
  телефон, email, банковский счёт) в тексте перед отправкой в LLM, и
  восстанавливает плейсхолдеры в ответе. Понимает русские склонения и
  валидирует ID по checksum-алгоритмам ФНС. Compatible с любой LLM
  (Claude, GPT, Gemini, локальные) — skill сам разговаривает с
  api.brikko.ru поверх HTTPS.

  Используется когда:
  — в тексте задачи есть персональные данные клиентов
  — компания работает по 152-ФЗ и не может отправлять реальные ПД в OpenAI/Anthropic
  — нужно сохранить контекст «что клиент Иванов сказал» без раскрытия личности

homepage: https://brikko.ru
repository: https://github.com/brikkoAI/brikko-pii-skill
authors:
  - Brikko Team <hello@brikko.ru>
tags:
  - pii
  - privacy
  - russian
  - 152-fz
  - compliance
  - anonymize

requires:
  env:
    - BRIKKO_API_KEY      # получить на https://brikko.ru → /app/keys
  binaries:
    - python3             # >= 3.10

compatibility:
  - claude-code
  - openclaw
  - codex

scripts:
  mask: scripts/mask.py
  restore: scripts/restore.py
---

# Brikko PII Mask — Skill для защиты персональных данных

Этот skill добавляет твоему агенту возможность безопасно работать с
персональными данными клиентов: маскирует ПД в тексте перед отправкой
в LLM и восстанавливает в ответе.

## Когда использовать

**Используй этот skill когда:**

1. Пользователь дал тебе текст с персональными данными (ФИО, ИНН, СНИЛС,
   ОГРН, ОГРНИП, паспорт РФ, телефон, email, банковский счёт)
2. Тебе нужно отправить этот текст в LLM (Claude/GPT/Gemini), чтобы
   получить ответ
3. Пользователь работает в РФ под 152-ФЗ и не имеет права передавать
   реальные ПД в OpenAI/Anthropic

**Не используй когда:**

- Текст явно публичный (новости, документация, открытые данные)
- ПД нет в тексте (skill сам определит и вернёт `count=0`)
- Пользователь явно сказал «отправь как есть, ПД не критичны»

## Как использовать

### Workflow

```
1. mask:    plaintext → masked text + mapping_id (хранится 1 час)
2. LLM:     masked text → answer (там тоже плейсхолдеры)
3. restore: answer + mapping_id → восстановленный ответ
4. отдать пользователю восстановленный ответ
```

### Шаг 1 — маскировать вход

```bash
python3 scripts/mask.py
# stdin: текст с ПД
# stdout: JSON {"masked_text", "mapping_id", "count", "audit"}
```

Пример:

```python
import json, subprocess
text = "Клиент Иванов Иван Иванович, ИНН 7707083893, тел +7 999 123 45 67"
result = json.loads(subprocess.check_output(
    ["python3", "scripts/mask.py"],
    input=text, text=True
))
# result["masked_text"] → "Клиент <NAME_1>, ИНН <INN_1>, тел <PHONE_1>"
# result["mapping_id"]  → "abc123..."
# result["count"]       → 3
```

### Шаг 2 — отправить замаскированный текст в LLM

Любой провайдер: Claude API, OpenAI API, локальная модель — без разницы.
Текст уже без ПД. Сохрани `mapping_id` для шага 3.

### Шаг 3 — восстановить плейсхолдеры в ответе

```bash
python3 scripts/restore.py --mapping-id abc123...
# stdin: ответ от LLM (с плейсхолдерами)
# stdout: текст с реальными ПД
```

```python
restored = subprocess.check_output(
    ["python3", "scripts/restore.py", "--mapping-id", result["mapping_id"]],
    input=llm_response, text=True
).strip()
# restored содержит реальные имена/ИНН/телефоны вместо <NAME_1>/<INN_1>/<PHONE_1>
```

## Конфигурация

Skill использует Brikko Gateway API (`https://api.brikko.ru/v1/anonymize`,
`/v1/restore`). Чтобы получить API-ключ:

1. Регистрация на [brikko.ru](https://brikko.ru) (бесплатно, 200 ₽
   welcome credit, для Studio-юзеров)
2. Создать ключ: brikko.ru → /app → «Создать API-ключ»
3. Экспортировать в окружение: `export BRIKKO_API_KEY=sk-brk-...`

**Тарифы:** анонимизация бесплатна в M2 (promo для adoption этого skill).
Только chat-completions через api.brikko.ru тарифицируются по обычным
ставкам провайдеров + 15% наценка Brikko.

**Self-hosted alternative:** установи Brikko Studio локально через
`npm install -g brikko-cli && brikko init` — skill автоматически
переключится на http://localhost:3737 если `BRIKKO_API_URL` указывает туда.

## Что детектируется

| Категория | Примеры | Checksum-валидация |
|---|---|---|
| `NAME` | Иванов / Иванову / Иванова (склонения) | — |
| `INN` | 7707083893 (10 цифр для юрлиц), 770708389300 (12 для физлиц) | ✓ алгоритм ФНС |
| `SNILS` | 123-456-789 01 | ✓ |
| `OGRN` | 1027700132195 (13 цифр) | ✓ |
| `OGRNIP` | 304500116000157 (15 цифр) | ✓ |
| `PASSPORT_RF` | 4509 123456 | regex |
| `PHONE_RF` | +7 999 123 45 67, 8(495)1234567 | regex |
| `EMAIL` | user@example.com | regex |
| `BANK_ACCOUNT_RF` | 40702810500000123456 (20 цифр) | ✓ контрольная цифра |
| `IPV4` | 192.168.1.1 | regex |

False-positive ratio < 1% за счёт checksum-валидации (без него случайные
10 цифр в тексте — например телефон без +7 или серийник детали — попадали
бы в категорию INN).

## Privacy & Audit

- Plaintext ПД **никогда** не покидают твою машину дальше
  api.brikko.ru (HTTPS, TLS 1.3, certs от Let's Encrypt)
- Mapping (плейсхолдер → оригинал) хранится в Redis на api.brikko.ru
  с TTL 1 час, после удаляется автоматически
- Audit-log Brikko содержит только категории и счётчики, **не plaintext** —
  «3 NAME, 1 INN, 2 PHONE» а не сами имена/номера
- При self-hosted Studio (Docker compose locally) — данные вообще не
  покидают локальную машину

## Failure modes

| Ошибка | Skill делает |
|---|---|
| Нет `BRIKKO_API_KEY` в env | exit 2, hint про регистрацию |
| api.brikko.ru недоступен | retry 3 раза, потом exit 1 с сетевым диагнозом |
| `mapping_id` истёк (>1 ч между mask и restore) | возвращает текст с плейсхолдерами как есть + warning |
| Текст > 1 MB | exit 2, hint разбить на чанки |

## Verify

```bash
# Установить skill в проект OpenClaw / Claude Code
# (детали — по выбранной экосистеме, см. README.md)

# Тест-запрос
echo "Клиент Иванов, ИНН 7707083893" | python3 scripts/mask.py
# Ожидаемый stdout: JSON с masked_text="Клиент <NAME_1>, ИНН <INN_1>"
```

## Поддержка

- Документация: https://brikko.ru/docs/skills/pii-mask
- Issues: https://github.com/brikkoAI/brikko-pii-skill/issues
- Email: hello@brikko.ru
- Telegram: [@brikko_ru](https://t.me/brikko_ru)
