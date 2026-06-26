# flyai CLI Commands Reference

This file documents the exact flyai CLI syntax used by this skill.
Read this file in Steps 3–6 before constructing any flyai command.

## Installation

```bash
npm i -g @fly-ai/flyai-cli
```

## Command: search-flight

Search flights between two cities.

```bash
flyai search-flight \
  --origin "出发城市" \
  --destination "目的城市" \
  --dep-date YYYY-MM-DD \
  --back-date YYYY-MM-DD \
  --sort-type 3
```

**Key parameters:**

| Parameter            | Required | Description                                |
|----------------------|----------|--------------------------------------------|
| `--origin`           | Yes      | Departure city (Chinese name)              |
| `--destination`      | No       | Destination city (Chinese name)            |
| `--dep-date`         | No       | Departure date `YYYY-MM-DD`                |
| `--back-date`        | No       | Return date `YYYY-MM-DD`                   |
| `--dep-date-start/end`| No     | Departure date range                       |
| `--journey-type`     | No       | `1`=direct, `2`=connecting                 |
| `--max-price`        | No       | Max price in CNY                           |
| `--sort-type`        | No       | `3`=price low→high (recommended default)   |

**Response fields used in output:**

- `data.itemList[].adultPrice` — ticket price
- `data.itemList[].journeys[].segments[].depCityName` — departure city
- `data.itemList[].journeys[].segments[].arrCityName` — arrival city
- `data.itemList[].journeys[].segments[].depDateTime` — departure time
- `data.itemList[].journeys[].segments[].arrDateTime` — arrival time
- `data.itemList[].journeys[].segments[].duration` — flight duration
- `data.itemList[].journeys[].segments[].marketingTransportName` — airline
- `data.itemList[].journeys[].segments[].marketingTransportNo` — flight number
- `data.itemList[].journeys[].segments[].seatClassName` — cabin class
- `data.itemList[].jumpUrl` — booking link

---

## Command: search-hotel

Search hotels in a city, optionally near a POI.

```bash
flyai search-hotel \
  --dest-name "城市" \
  --poi-name "场馆/地标" \
  --check-in-date YYYY-MM-DD \
  --check-out-date YYYY-MM-DD \
  --sort distance_asc \
  --max-price 1500
```

**Key parameters:**

| Parameter            | Required | Description                                |
|----------------------|----------|--------------------------------------------|
| `--dest-name`        | Yes      | City name (Chinese)                        |
| `--poi-name`         | No       | Nearby POI to anchor search                |
| `--check-in-date`    | No       | Check-in date `YYYY-MM-DD`                 |
| `--check-out-date`   | No       | Check-out date `YYYY-MM-DD`                |
| `--sort`             | No       | `distance_asc`, `rate_desc`, `price_asc`   |
| `--max-price`        | No       | Max price per night in CNY                  |
| `--hotel-stars`      | No       | Star rating `1`–`5`, comma-separated       |

**Response fields used in output:**

- `name` — hotel name
- `address` — address
- `price` — price per night
- `score` / `scoreDesc` — rating
- `mainPic` — image URL (use `![hotel]({mainPic})`)
- `detailUrl` — booking link (use `[Book now]({detailUrl})`)
- `interestsPoi` — nearby POI description

---

## Command: keyword-search

Natural-language search across all travel categories.

```bash
flyai keyword-search --query "搜索关键词"
```

**Useful query patterns for this skill:**

| Intent               | Query example                              |
|----------------------|--------------------------------------------|
| Event tickets        | `"澳网门票 2026"`                            |
| Tennis experiences   | `"墨尔本 网球体验课"`                          |
| Visa info            | `"澳大利亚签证"`                              |
| Local SIM / WiFi     | `"澳大利亚电话卡"`                             |
| City tours           | `"巴黎一日游"`                                |

**Response fields used in output:**

- `data.itemList[].info.title` — item title
- `data.itemList[].info.price` — price
- `data.itemList[].info.picUrl` — image (use `![item]({picUrl})`)
- `data.itemList[].info.jumpUrl` — booking link (use `[Book now]({jumpUrl})`)
- `data.itemList[].info.tags[]` — tags

---

## Command: search-poi

Search attractions and points of interest.

```bash
flyai search-poi \
  --city-name "城市" \
  --category "类别" \
  --keyword "关键词"
```

**Key parameters:**

| Parameter   | Required | Description                                     |
|-------------|----------|-------------------------------------------------|
| `--city-name`| Yes     | City name (Chinese)                              |
| `--category` | No      | See category list below                          |
| `--keyword`  | No      | Attraction name keyword                          |
| `--poi-level`| No      | Rating level 1–5                                 |

**Commonly used categories for Grand Slam cities:**

- Nature: `自然风光`, `山湖田园`, `沙滩海岛`
- Culture: `人文古迹`, `古镇古村`, `历史古迹`, `园林花园`
- Entertainment: `主题乐园`, `动物园`, `海洋馆`
- Venues: `博物馆`, `地标建筑`, `演出赛事`
- Urban: `市集`, `城市观光`

**Response fields used in output:**

- `data.itemList[].name` — attraction name
- `data.itemList[].address` — address
- `data.itemList[].mainPic` — image URL
- `data.itemList[].jumpUrl` — booking link
- `data.itemList[].ticketInfo.price` — ticket price
