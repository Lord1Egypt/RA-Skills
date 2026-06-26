# Finam Trade API — gRPC (FinamPy)

Библиотека-обёртка [FinamPy](https://github.com/cia76/FinamPy) для работы с [Finam Trade API](https://tradeapi.finam.ru) v2.13.0 из Python по протоколу gRPC.

---

## Установка

```bash
pip install git+https://github.com/cia76/FinamPy.git
```

При первом запуске передать токен явно (сохраняется в системное хранилище):

```python
import os
from FinamPy import FinamPy
fp_provider = FinamPy(os.environ["FINAM_API_KEY"])
```

Последующие вызовы — без токена:

```python
fp_provider = FinamPy()
```

---

## Подключение и базовое использование

```python
from FinamPy import FinamPy

fp_provider = FinamPy()

# Синхронный вызов метода — возвращает ответ или None при ошибке
response = fp_provider.call_function(stub.Method, RequestMessage(...))

# Закрыть канал перед выходом
fp_provider.close_channel()
```

**Свойства провайдера:**

| Свойство | Тип | Описание |
|---|---|---|
| `account_ids` | `list[str]` | Список ID торговых счетов |
| `tz_msk` | `tzinfo` | Часовой пояс МСК (UTC+3) |
| `min_history_date` | `datetime` | Минимальная дата истории баров |

---

## Форматы данных

### Символы

FinamPy использует два формата:

| Формат | Пример | Где используется |
|---|---|---|
| `{board}.{ticker}` (dataname) | `TQBR.SBER`, `SPBFUT.SiH5` | Человекочитаемый ввод |
| `{ticker}@{mic}` (symbol) | `SBER@MISX`, `Si@ROFX` | Все запросы к API |

Конвертация dataname → symbol:

```python
finam_board, ticker = fp_provider.dataname_to_finam_board_ticker('TQBR.SBER')
mic = fp_provider.get_mic(finam_board, ticker)
symbol = f'{ticker}@{mic}'  # → 'SBER@MISX'
```

**MIC-коды основных бирж:**

| MIC | Биржа |
|---|---|
| `MISX` | Московская биржа (акции) |
| `ROFX` | Московская биржа (фьючерсы) |
| `RUSX` | РТС |
| `XNGS` | NASDAQ/NGS |
| `XNYS` | NYSE |

### Таймфреймы

| FinamPy `tf` | Описание | Аналог REST |
|---|---|---|
| `M1` | 1 минута | `TIME_FRAME_M1` |
| `M5` | 5 минут | `TIME_FRAME_M5` |
| `M15` | 15 минут | `TIME_FRAME_M15` |
| `M30` | 30 минут | `TIME_FRAME_M30` |
| `H1` | 1 час | `TIME_FRAME_H1` |
| `H2` | 2 часа | `TIME_FRAME_H2` |
| `H4` | 4 часа | `TIME_FRAME_H4` |
| `D1` | День | `TIME_FRAME_D` |
| `W1` | Неделя | `TIME_FRAME_W` |
| `MN1` | Месяц | `TIME_FRAME_MN` |

Конвертация:

```python
finam_tf, tf_range, intraday = fp_provider.timeframe_to_finam_timeframe('D1')
# finam_tf   — константа для запроса к API
# tf_range   — timedelta максимального диапазона одного запроса
# intraday   — True для внутридневных таймфреймов
```

### Цены и объёмы (Decimal / nanos)

```python
from google.type.decimal_pb2 import Decimal

# Запись цены в запрос
price = Decimal(value='310.50')

# Чтение цены из ответа
price_float = float(response.price.value)

# Чтение денег из поля units + nanos
amount = round(cash.units + cash.nanos * 1e-9, 2)
```

### Временны́е метки (Timestamp)

```python
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp

# datetime → Timestamp
ts = Timestamp(seconds=int(datetime.timestamp(dt)))

# Timestamp → datetime (МСК)
dt = datetime.fromtimestamp(ts.seconds + ts.nanos / 1e9, fp_provider.tz_msk)
```

---

## Сервисы

| Стаб | Модуль | Операции |
|---|---|---|
| `fp_provider.assets_stub` | `assets_service_pb2` | Спецификация тикеров, время сервера |
| `fp_provider.accounts_stub` | `accounts_service_pb2` | Счета, позиции, баланс |
| `fp_provider.orders_stub` | `orders_service_pb2` | Заявки: просмотр, выставление, отмена |
| `fp_provider.marketdata_stub` | `marketdata_service_pb2` | Котировки, бары, стакан, сделки |

---

## AssetsService

### GetAsset — спецификация инструмента

```python
from FinamPy.grpc.assets_service_pb2 import GetAssetRequest, GetAssetResponse

si: GetAssetResponse = fp_provider.call_function(
    fp_provider.assets_stub.GetAsset,
    GetAssetRequest(symbol=symbol, account_id=fp_provider.account_ids[0])
)
```

**Запрос `GetAssetRequest`:**

| Поле | Тип | Описание |
|---|---|---|
| `symbol` | `string` | Инструмент в формате `ticker@mic` |
| `account_id` | `string` | ID торгового счёта |

**Ответ `GetAssetResponse`:**

| Поле | Тип | Описание |
|---|---|---|
| `ticker` | `string` | Тикер |
| `board` | `string` | Режим торгов (TQBR, SPBFUT, ...) |
| `name` | `string` | Полное название |
| `type` | `string` | Тип инструмента |
| `mic` | `string` | MIC-код биржи |
| `lot_size` | `Decimal` | Размер лота |
| `min_step` | `int` | Минимальный шаг цены (в единицах * 10^decimals) |
| `decimals` | `int` | Кол-во знаков после запятой |

Шаг цены в единицах: `si.min_step / (10 ** si.decimals)`

### Clock — время сервера

```python
from FinamPy.grpc.assets_service_pb2 import ClockRequest, ClockResponse

clock: ClockResponse = fp_provider.call_function(
    fp_provider.assets_stub.Clock, ClockRequest()
)
dt_server = datetime.fromtimestamp(clock.timestamp.seconds + clock.timestamp.nanos / 1e9, fp_provider.tz_msk)
```

---

## AccountsService

### GetAccount — информация по счёту

```python
from FinamPy.grpc.accounts_service_pb2 import GetAccountRequest, GetAccountResponse

account: GetAccountResponse = fp_provider.call_function(
    fp_provider.accounts_stub.GetAccount,
    GetAccountRequest(account_id=account_id)
)
if account is None:
    # Счёт не поддерживается в Finam Trade API
    ...
```

**Ответ `GetAccountResponse`:**

| Поле | Тип | Описание |
|---|---|---|
| `positions` | `list` | Открытые позиции (`symbol`, `quantity`, `average_price`, `current_price`) |
| `cash` | `list` | Свободные средства (`units`, `nanos`, `currency_code`) |
| `unrealized_profit` | `Decimal` | Нереализованная прибыль |
| `equity` | `Decimal` | Итого по счёту |

---

## OrdersService

### GetOrders — активные заявки

```python
from FinamPy.grpc.orders_service_pb2 import OrdersRequest, OrdersResponse, ORDER_STATUS_NEW

orders: OrdersResponse = fp_provider.call_function(
    fp_provider.orders_stub.GetOrders,
    OrdersRequest(account_id=account_id)
)
active = [o for o in orders.orders if o.status == ORDER_STATUS_NEW]
```

### PlaceOrder — выставить заявку

```python
from FinamPy.grpc.orders_service_pb2 import Order, OrderState, OrderType, StopCondition
import FinamPy.grpc.side_pb2 as side
from google.type.decimal_pb2 import Decimal

# Рыночная заявка
order_state: OrderState = fp_provider.call_function(
    fp_provider.orders_stub.PlaceOrder,
    Order(
        account_id=account_id,
        symbol=symbol,
        quantity=Decimal(value='10'),
        side=side.SIDE_BUY,
        type=OrderType.ORDER_TYPE_MARKET,
        client_order_id=str(int(datetime.now().timestamp()))
    )
)

# Лимитная заявка
order_state: OrderState = fp_provider.call_function(
    fp_provider.orders_stub.PlaceOrder,
    Order(
        account_id=account_id,
        symbol=symbol,
        quantity=Decimal(value='10'),
        side=side.SIDE_SELL,
        type=OrderType.ORDER_TYPE_LIMIT,
        limit_price=Decimal(value='310.50'),
        client_order_id=str(int(datetime.now().timestamp()))
    )
)

# Стоп заявка
order_state: OrderState = fp_provider.call_function(
    fp_provider.orders_stub.PlaceOrder,
    Order(
        account_id=account_id,
        symbol=symbol,
        quantity=Decimal(value='10'),
        side=side.SIDE_BUY,
        type=OrderType.ORDER_TYPE_STOP,
        stop_price=Decimal(value='315.00'),
        stop_condition=StopCondition.STOP_CONDITION_LAST_UP,
        client_order_id=str(int(datetime.now().timestamp()))
    )
)
```

**Поля `Order`:**

| Поле | Тип | Описание |
|---|---|---|
| `account_id` | `string` | ID торгового счёта |
| `symbol` | `string` | Инструмент `ticker@mic` |
| `quantity` | `Decimal` | Количество (в штуках) |
| `side` | `Side` | `SIDE_BUY` / `SIDE_SELL` |
| `type` | `OrderType` | `ORDER_TYPE_MARKET` / `ORDER_TYPE_LIMIT` / `ORDER_TYPE_STOP` |
| `limit_price` | `Decimal` | Цена для лимитной заявки |
| `stop_price` | `Decimal` | Цена для стоп заявки |
| `stop_condition` | `StopCondition` | `STOP_CONDITION_LAST_UP` / `STOP_CONDITION_LAST_DOWN` |
| `client_order_id` | `string` | Уникальный ID на стороне клиента |

**Ответ `OrderState`:**

| Поле | Тип | Описание |
|---|---|---|
| `order_id` | `string` | ID заявки на бирже |
| `exec_id` | `string` | ID исполнения (для рыночных) |
| `status` | `OrderStatus` | Статус заявки |

### CancelOrder — отменить заявку

```python
from FinamPy.grpc.orders_service_pb2 import CancelOrderRequest

order_state: OrderState = fp_provider.call_function(
    fp_provider.orders_stub.CancelOrder,
    CancelOrderRequest(account_id=account_id, order_id=order_id)
)
```

---

## MarketDataService

### LastQuote — последняя котировка

```python
from FinamPy.grpc.marketdata_service_pb2 import QuoteRequest, QuoteResponse

quote_response: QuoteResponse = fp_provider.call_function(
    fp_provider.marketdata_stub.LastQuote,
    QuoteRequest(symbol=symbol)
)
last_price = float(quote_response.quote.last.value)
```

### Bars — история баров

```python
from google.protobuf.timestamp_pb2 import Timestamp
from google.type.interval_pb2 import Interval
from FinamPy.grpc.marketdata_service_pb2 import BarsRequest, BarsResponse

finam_tf, tf_range, intraday = fp_provider.timeframe_to_finam_timeframe('D1')
start_dt = fp_provider.min_history_date

while start_dt <= datetime.now():
    end_dt = start_dt + tf_range
    bars_response: BarsResponse = fp_provider.call_function(
        fp_provider.marketdata_stub.Bars,
        BarsRequest(
            symbol=symbol,
            timeframe=finam_tf,
            interval=Interval(
                start_time=Timestamp(seconds=int(datetime.timestamp(start_dt))),
                end_time=Timestamp(seconds=int(datetime.timestamp(end_dt)))
            )
        )
    )
    for bar in bars_response.bars:
        dt_bar = datetime.fromtimestamp(bar.timestamp.seconds, fp_provider.tz_msk)
        # bar.open.value, bar.high.value, bar.low.value, bar.close.value, bar.volume.value
    start_dt = end_dt
```

**Поля бара `Bar`:** `timestamp`, `open`, `high`, `low`, `close`, `volume` — все цены типа `Decimal`.

---

## Подписки (стримы)

Подписки запускаются в отдельных потоках. Обработчики регистрируются через `.subscribe()` / `.unsubscribe()`.

### Котировки

```python
from threading import Thread
from FinamPy.grpc.marketdata_service_pb2 import SubscribeQuoteResponse

def on_quote(quote: SubscribeQuoteResponse):
    if quote.quote:
        print(quote.quote[0])

fp_provider.on_quote.subscribe(on_quote)
Thread(target=fp_provider.subscribe_quote_thread, args=((symbol,),)).start()

# Отмена
fp_provider.on_quote.unsubscribe(on_quote)
```

### Стакан

```python
from FinamPy.grpc.marketdata_service_pb2 import SubscribeOrderBookResponse

def on_order_book(ob: SubscribeOrderBookResponse):
    if ob.order_book:
        print(ob.order_book[0])

fp_provider.on_order_book.subscribe(on_order_book)
Thread(target=fp_provider.subscribe_order_book_thread, args=(symbol,)).start()
```

### Сделки (лента)

```python
from FinamPy.grpc.marketdata_service_pb2 import SubscribeLatestTradesResponse

def on_latest_trades(trades: SubscribeLatestTradesResponse):
    if trades.trades:
        print(trades.trades[0])

fp_provider.on_latest_trades.subscribe(on_latest_trades)
Thread(target=fp_provider.subscribe_latest_trades_thread, args=(symbol,)).start()
```

### Бары в реальном времени

```python
from FinamPy.grpc.marketdata_service_pb2 import TimeFrame, SubscribeBarsResponse, Bar

last_bar = None
dt_last_bar = None

def on_new_bar(bars: SubscribeBarsResponse, finam_timeframe: TimeFrame.ValueType):
    global last_bar, dt_last_bar
    for bar in bars.bars:
        dt_bar = datetime.fromtimestamp(bar.timestamp.seconds, fp_provider.tz_msk)
        if dt_last_bar is not None and dt_last_bar < dt_bar:
            # Закрылся предыдущий бар — можно обрабатывать last_bar
            print(f'{dt_last_bar} O:{last_bar.open.value} C:{last_bar.close.value}')
        last_bar = bar
        dt_last_bar = dt_bar

finam_tf, _, _ = fp_provider.timeframe_to_finam_timeframe('M1')
fp_provider.on_new_bar.subscribe(on_new_bar)
Thread(target=fp_provider.subscribe_bars_thread, args=(symbol, finam_tf)).start()
```

### Свои заявки и сделки

```python
fp_provider.on_order.subscribe(lambda order: print(f'Заявка: {order}'))
fp_provider.on_trade.subscribe(lambda trade: print(f'Сделка: {trade}'))
Thread(target=fp_provider.subscribe_orders_thread).start()
Thread(target=fp_provider.subscribe_trades_thread).start()
```

---

## Вспомогательные методы

| Метод | Возвращает | Описание |
|---|---|---|
| `dataname_to_finam_board_ticker(dataname)` | `(board, ticker)` | Разбивает `TQBR.SBER` на board и ticker |
| `get_mic(board, ticker)` | `str` | MIC-код биржи по board и ticker |
| `get_symbol_info(ticker, mic)` | `GetAssetResponse` | Спецификация инструмента |
| `timeframe_to_finam_timeframe(tf)` | `(finam_tf, tf_range, intraday)` | Конвертация строкового TF в константу API |
| `finam_timeframe_to_timeframe(finam_tf)` | `(tf, tf_range, intraday)` | Обратная конвертация |
| `call_function(stub_method, request)` | `Response \| None` | Синхронный вызов gRPC-метода |
| `close_channel()` | — | Закрыть gRPC-канал перед выходом |

---

## Обработка ошибок

`call_function` возвращает `None` при любой ошибке (недоступность, таймаут, неверные параметры). Всегда проверяйте результат:

```python
result = fp_provider.call_function(stub.Method, request)
if result is None:
    # Логировать или обработать ошибку
    ...
```

Ошибки и подробности логируются самой библиотекой в стандартный `logging`.

**Типичные причины `None`:**
- Истёк токен (библиотека переподключается автоматически, но первый запрос может упасть)
- Неверный `symbol` или `account_id`
- Счёт не поддерживается в Finam Trade API
- Превышен лимит запросов

---

## Особенности

- Из спецификации фьючерса невозможно определить, является ли он фьючерсом на сырьё
- Для дневных и выше таймфреймов (`intraday=False`) следует обрезать время у `datetime`: `dt_bar.date()`
- `subscribe_quote_thread` принимает **кортеж** символов: `args=((symbol,),)` — двойные скобки обязательны
- `client_order_id` должен быть уникальным; удобно использовать `str(int(datetime.now().timestamp()))`