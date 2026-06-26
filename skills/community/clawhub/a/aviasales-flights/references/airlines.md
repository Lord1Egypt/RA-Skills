# Маппинг кодов авиакомпаний

## Российские авиакомпании

| Код IATA | Название |
|----------|----------|
| SU | Аэрофлот |
| S7 | S7 Airlines |
| DP | Победа |
| UT | ЮТэйр |
| U6 | Уральские авиалинии |
| 5N | Smartavia (Nordavia) |
| WZ | Red Wings |
| N4 | Nordwind |
| FV | Россия |
| IO | IrAero |
| GH | Глобус (дочка S7) |
| YC | ЯКСЭЙР (Yakutia Airlines) |
| R3 | Якутия |
| OV | SaratovAvia |
| 6W | Saratov Airlines |
| 7R | RusLine |
| A4 | Azimuth |

## Иностранные авиакомпании (часто летят из/в РФ)

| Код IATA | Название |
|----------|----------|
| TK | Turkish Airlines |
| PC | Pegasus Airlines |
| XQ | SunExpress |
| EK | Emirates |
| FZ | flydubai |
| QR | Qatar Airways |
| GF | Gulf Air |
| WY | Oman Air |
| ET | Ethiopian Airlines |
| MS | EgyptAir |
| SV | Saudia |
| KC | Air Astana |
| Z9 | Bek Air |
| LH | Lufthansa |
| AF | Air France |
| BA | British Airways |
| AY | Finnair |
| SK | SAS |
| LX | Swiss |
| OS | Austrian |
| KL | KLM |
| IB | Iberia |

## Примечание
Актуальный маппинг загружается автоматически с `https://api.travelpayouts.com/data/ru/airlines.json`
и кэшируется в `/tmp/airlines_cache.json` на 24 часа.
Данный файл служит справочным материалом и фоллбэком при недоступности API.
