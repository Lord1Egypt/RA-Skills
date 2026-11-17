# financial-experts-said: графики и визуализация

Визуализация экспертных уровней из базы financial-experts-said (SQLite).

## Когда использовать
«Нарисуй уровни по IMOEX», «график по эксперту X», «покажи все тезисы», «интерактивный HTML».

## Which output? (два разных артефакта — не путать)

| Что нужно | Команда | Выход | Что внутри |
|---|---|---|---|
| **Свечи + уровни на графике** («нарисуй уровни», «график TradingView») | `chart/ticker_chart_html.py` | `levels-chart.html` | Интерактивные свечи (lightweight-charts, MOEX ISS/stooq) + линии уровней экспертов, фильтры, табы |
| **Реестр тезисов** («покажи все тезисы», «что говорил X») | `pipeline/dashboard.py` | `registry.html` | Таблица карточек: цитаты, источники, позиции, мини-графики уровней |

Не используйте имя `dashboard.html` для обоих выходов — это гарантированная путаница.

## Network disclosure

Generating or opening the interactive HTML dashboard requires network access:
it loads TradingView lightweight-charts from a CDN and fetches market data from
MOEX ISS. Opening the HTML can disclose metadata such as IP address, time, and
user agent to those services. State this before generating or opening the
dashboard and obtain user confirmation when network access has not already
been approved.

## Использование
Все команды строятся строго от `FES_ROOT` и `FES_DB` (никогда — относительно текущей директории):

```bash
# PNG-график
python3 "$FES_ROOT/chart/ticker_chart.py" --db "$FES_DB" --asset IMOEX --out chart.png

# Интерактивный HTML (свечи MOEX + уровни экспертов, фильтры, табы)
python3 "$FES_ROOT/chart/ticker_chart_html.py" --db "$FES_DB" --out levels-chart.html

# Реестр-дашборд (таблица тезисов + детализация + мини-графики уровней)
python3 "$FES_ROOT/pipeline/dashboard.py" --db "$FES_DB" --output registry.html
```
HTML-графика использует `lightweight-charts` с CDN — нужен интернет при открытии.

## Правила отображения
1. Свежая дата эксперта — сплошные линии, ранние — пунктир.
2. Фильтры «актив», «эксперт», «актив+эксперт»; мобильная вёрстка.
3. Дайджест до графика: последняя цена + 3 свежих тезиса.
4. Подписи уровней на правой шкале.
5. Табы «Графики»/«Покрытие»: у обеих панелей класс `tabpane`, активная — `tabpane active`; переключатель снимает `active` у всех `.tabpane`.

## Источники цен
- MOEX ISS `/candles` PRIMARY (interval=24), fallback `/history`; тикер из БД (assets.ticker).
- Словесные активы → мапы в скрипте (Золото→GLDRUB_TOM, Нефть→BRZ6, ОФЗ→RGBI и т.п.) как fallback.
- Золото: уровни в $/oz → пересчёт в ₽/г (уровень <10000 трактуем как $/oz), помечать «пересчёт».
- Нулевые свечи отбрасывать; пустые серии — «price empty», не «ok».
- Не котируются на MOEX: S&P 500, DXY, Moderna (stooq-fallback в PNG-скрипте).

## Обязательные проверки перед отправкой HTML
1. Embedded JSON валиден, `</script>`-guard стоит.
2. Даты через Date.parse, не строками.
3. Все вставки в DOM через esc().
