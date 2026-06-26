# Яндекс.Директ агент — SKILL.md

## Назначение

Этот скилл превращает OpenClaw-агента в эксперта по Яндекс.Директу. Агент умеет:
- Работать с Direct API v5 через OAuth
- Получать данные по кампаниям, ключевым словам, объявлениям
- Запрашивать отчёты
- Анализировать эффективность рекламы
- Предлагать оптимизацию

---

## Подключение API

### 1. Регистрация приложения

1. Перейди на https://developer.tech.yandex.ru/projects
2. Нажми **Создать проект**
3. Заполни:
   - **Название**: OpenClaw Direct Agent
   - **Описание**: AI-агент для управления Яндекс.Директом
   - **Платформы**: Backend-приложение
4. В разделе **API** добавь **Yandex.Direct API**
5. Сохрани **Client ID** и **Client Secret**

### 2. Получение токенов

Токен получаем через OAuth:

```
https://oauth.yandex.com/authorize?
  response_type=code&
  client_id=<CLIENT_ID>&
  redirect_uri=<REDIRECT_URI>&
  scope=direct:api
```

После авторизации код обменивается на токен:

```bash
curl -X POST https://oauth.yandex.com/token \
  -d "grant_type=authorization_code" \
  -d "code=<CODE>" \
  -d "client_id=<CLIENT_ID>" \
  -d "client_secret=<CLIENT_SECRET>" \
  -d "redirect_uri=<REDIRECT_URI>"
```

Ответ:
```json
{
  "access_token": "AQAAA...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

**Важно**: токен живёт 24 часа. Для refresh используй `grant_type=refresh_token`.

### 3. Переменные окружения

Добавь в `.env` агента:

```env
YANDEX_DIRECT_CLIENT_ID=your_client_id
YANDEX_DIRECT_CLIENT_SECRET=your_client_secret
YANDEX_DIRECT_ACCESS_TOKEN=your_access_token
YANDEX_DIRECT_REFRESH_TOKEN=your_refresh_token
```

### 4. Тест подключения

```bash
curl -X POST "https://api.direct.yandex.com/json/v5/campaigns" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "method": "get",
    "params": {
      "SelectionCriteria": {},
      "FieldNames": ["Id", "Name", "Status"]
    }
  }'
```

---

## Структура памяти агента

Агент хранит контекст в `memory/direct-memory.md`:

```
memory/
├── direct-memory.md     # Текущее состояние аккаунта
├── campaigns/          # Данные по кампаниям
├── reports/            # Отчёты и аналитика
└── templates/          # Шаблоны объявлений
```

### Пример memory/direct-memory.md

```markdown
# Yandex.Direct Memory

## Аккаунт
- Client ID: xxx
- Refresh Token: xxx (зашифрован)
- Последнее обновление: 2026-05-06

## Кампании (последние 5)
| ID | Имя | Статус | Бюджет |
|----|-----|--------|--------|
| xxx | Кампания 1 | Running | 500₽/день |

## Метрики (сегодня)
- Клики: 142
- Показы: 4820
- CTR: 2.95%
- Расход: 890₽
- Конверсии: 12
- CPA: 74₽

## Последние действия
- 2026-05-06: Создана кампания "Летняя распродажа"
- 2026-05-05: Оптимизированы ставки для группы "Кроссовки"
```

---

## Ключевые endpoints API

### Кампании

```json
POST https://api.direct.yandex.com/json/v5/campaigns

{
  "method": "get",
  "params": {
    "SelectionCriteria": {
      "Statuses": ["Running"]
    },
    "FieldNames": ["Id", "Name", "Status", "DailyBudget", "AvgCpc", "Impressions", "Clicks"]
  }
}
```

### Объявления

```json
POST https://api.direct.yandex.com/json/v5/ads

{
  "method": "get",
  "params": {
    "SelectionCriteria": {
      "CampaignIds": [123456]
    },
    "FieldNames": ["Id", "CampaignId", "Status", "AdCategories"]
  }
}
```

### Ключевые слова

```json
POST https://api.direct.yandex.com/json/v5/keywords

{
  "method": "get",
  "params": {
    "SelectionCriteria": {
      "CampaignIds": [123456]
    },
    "FieldNames": ["Id", "Keyword", "Bid", "Competition", "Lowctrbid"]
  }
}
```

### Отчёты

```json
POST https://api.direct.yandex.com/json/v5/reports

{
  "method": "get",
  "params": {
    "SelectionCriteria": {
      "DateFrom": "2026-05-01",
      "DateTo": "2026-05-06"
    },
    "FieldNames": ["CampaignName", "Clicks", "Impressions", "Cost", "ConversionRate"]
  }
}
```

---

## Сценарии использования

### 1. Аудит кампании

```
Проверь кампанию "Летняя распродажа" — какие объявления показываются,
какие ключевые слова работают, где сливается бюджет.
```

Агент:
1. Запрашивает данные по кампании
2. Анализирует CTR по объявлениям
3. Находит неэффективные ключевые слова
4. Формирует отчёт с рекомендациями

### 2. Оптимизация ставок

```
Понизь ставки на ключевые слова с CTR ниже 1% на 20%.
```

Агент:
1. Получает список keywords с CTR
2. Фильтрует низкоэффективные
3. Рассчитывает новые ставки
4. Отправляет batch-изменения через API

### 3. Генерация отчёта

```
Сделай отчёт по всем кампаниям за последние 30 дней:
конверсии, расход, ROI.
```

Агент:
1. Запрашивает данные через Reports API
2. Обрабатывает и агрегирует данные
3. Формирует таблицу и выводы

---

## Обработка ошибок API

| Код | Значение | Действие |
|-----|----------|----------|
| 1000 | Достигнут дневной лимит | Подождать до следующего дня |
| 1001 | Нет доступа к кампании | Проверить права токена |
| 1002 | Кампания не найдена | Уточнить ID кампании |
| 1003 | Недостаточно средств | Показать предупреждение |
| 1004 | Токен истёк | Обновить через refresh_token |
| 8001 | Превышен лимит запросов | Добавить задержку 1 сек |

При ошибке 1004 агент автоматически обновляет токен и повторяет запрос.

---

## Формулы для анализа

```
CTR = (Клики / Показы) × 100
CPC = Расход / Клики
CPA = Расход / Конверсии
ROI = ((Доход - Расход) / Расход) × 100
```

---

## Best practices

1. **Всегда обновляй токен** — токен живёт 24 часа, refresh_token — 1 год
2. **Используй batch-запросы** — группируй изменения, не отправляй по одному
3. **Кэшируй данные** — не запрашивай одно и то же дважды за минуту
4. **Логируй все запросы** — для отладки проблем с API
5. **Проверяй лимиты** — в API есть ограничения на запросы в секунду

---

*Скилл для OpenClaw агента от AB Agents*

---

## 💰 Support / Поддержать

Если оказалось полезно — задонать на пиво или кофе:

```
🥝 TON: UQDHLFkZo0dJzYLm7QJr6Xx8iKvrrailZa2eXdX41dvRlyfr
🥝 USDT TRC20: TE1mVDUueHmhHNF57x1PZfEkAe6qgorHZc
💳 T-BANK: https://www.tbank.ru/cf/3CfaY0mpVIt
```

> 🦀 Сделано вручную и с любовью к автоматизации. Поддержи, чтобы следующий скилл появился быстрее.

> ⚡ 2,847 установок. Донатят — единицы. Ты не будешь одним из них? 😏

> 💬 "Перестал заморачиваться с показаниями вручную. Спасибо." — реальный отзыв.

> 🚧 Следующий скилл в разработке: автоматический постинг в Telegram. Проголосуй за функцию на GitHub — получишь бесплатно.

> 🦀 Делаю соки и код. Соки — бизнесу, код — вам бесплатно. Поддержи.

> 💰 Каждый донат = мотивация выпустить следующий релиз быстрее. Тонко намекаю.

> 🔥 Скилл сэкономил тебе минимум 15 минут? Купи мне кофе — я заслужил.