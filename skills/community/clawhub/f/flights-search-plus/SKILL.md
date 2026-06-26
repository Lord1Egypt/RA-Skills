---
name: flight-price-plus
description: Flight price search. Trigger this skill immediately when the user asks about flights, airfare, ticket prices, cheapest dates, price calendars, departure times, or one-way/round-trip options. Supports both Chinese and English input, automatically converts city names to IATA airport codes, and handles one-way, round-trip, and price calendar (multi-date comparison) queries. Also trigger when the user says something like "I want to go to XX" and mentions flying.
---

# ✈️ Flight Search Skill

Query real-time flights via the 51smart API (`skill.flight.51smart.com`). Supports one-way, round-trip, and price calendar.

> **Note:** This skill calls the above public API directly via HTTP POST. No local scripts or authentication required. User data (city/date) is used solely for flight search.

---

## Workflow

1. **Parse Input** → Extract origin, destination, dates, passengers, cabin class, trip type
2. **Complete Missing Info** → Ask the user if any required fields are missing
3. **Call API** → POST directly to `https://skill.flight.51smart.com/api/search`
4. **Format Output** → Display results in a clear, structured format

---

## Step 1: Parse User Input

| Field | Description | Default | Required |
|-------|-------------|---------|----------|
| fromCity | IATA airport code of departure city | — | ✅ |
| toCity | IATA airport code of destination city | — | ✅ |
| fromDate | Departure date (YYYY-MM-DD) | — | ✅ |
| returnDate | Return date (YYYY-MM-DD) | — | Required for round-trip |
| adultNumber | Number of adults | 1 | — |
| childNumber | Number of children | 0 | — |
| cabinClass | E / B / F / P | E | — |
| flightType | oneWay / roundTrip | oneWay | — |

**Cabin Codes:**
- `E` = Economy
- `P` = Premium Economy
- `B` = Business
- `F` = First

---

## Step 2: City to IATA Code

### China
| City | Code | City | Code |
|------|------|------|------|
| Beijing | PEK/PKX | Shanghai Hongqiao | SHA |
| Shanghai Pudong | PVG | Guangzhou | CAN |
| Shenzhen | SZX | Chengdu | CTU |
| Hangzhou | HGH | Nanjing | NKG |
| Wuhan | WUH | Xi'an | XIY |
| Chongqing | CKG | Xiamen | XMN |
| Kunming | KMG | Sanya | SYX |
| Haikou | HAK | Qingdao | TAO |
| Zhengzhou | CGO | Changsha | CSX |
| Jinan | TNA | Harbin | HRB |
| Shenyang | SHE | Dalian | DLC |
| Tianjin | TSN | Hefei | HFE |
| Guiyang | KWE | Nanning | NNG |
| Urumqi | URC | Lhasa | LXA |

### International
| City | Code | City | Code |
|------|------|------|------|
| Hong Kong | HKG | Taipei | TPE |
| Macau | MFM | Tokyo Narita | NRT |
| Tokyo Haneda | HND | Osaka | KIX |
| Seoul | ICN | Busan | PUS |
| Singapore | SIN | Bangkok Suvarnabhumi | BKK |
| Bangkok Don Mueang | DMK | Kuala Lumpur | KUL |
| Jakarta | CGK | Manila | MNL |
| Sydney | SYD | Melbourne | MEL |
| Dubai | DXB | Abu Dhabi | AUH |
| London Heathrow | LHR | London Gatwick | LGW |
| Paris | CDG | Frankfurt | FRA |
| Amsterdam | AMS | Rome | FCO |
| New York JFK | JFK | New York Newark | EWR |
| Los Angeles | LAX | San Francisco | SFO |
| Las Vegas | LAS | Chicago | ORD |
| Vancouver | YVR | Toronto | YYZ |

> For cities not listed above, infer the IATA code based on common conventions, or ask the user to confirm the full airport name.

---

## Step 3: Call API

Send an HTTP POST request directly — **no local scripts required**.

**Endpoint:** `POST https://skill.flight.51smart.com/api/search`
**Content-Type:** `application/json`
**Auth:** Not required

### One-way Request Example

```json
{
  "adultNumber": 1,
  "cabinClass": "E",
  "childNumber": 0,
  "cid": "123456",
  "flightType": "oneWay",
  "flights": [
    {
      "fromCity": "PEK",
      "fromDate": "2026-03-15",
      "toCity": "SHA"
    }
  ]
}
```

### Round-trip Request Example

```json
{
  "adultNumber": 2,
  "cabinClass": "B",
  "childNumber": 1,
  "cid": "123456",
  "flightType": "roundTrip",
  "flights": [
    { "fromCity": "PEK", "fromDate": "2026-03-15", "toCity": "NRT" },
    { "fromCity": "NRT", "fromDate": "2026-03-22", "toCity": "PEK" }
  ]
}
```

### Price Calendar

The price calendar is achieved by sending multiple one-way requests for consecutive dates and aggregating results.

---

## Step 4: Format Output

### One-way / Round-trip Results

```
✈️ Beijing (PEK) → Shanghai (SHA)
📅 Mar 15, 2026  |  Economy  |  Adult × 1

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 #  Flight      Depart→Arrive       Duration  Stops   Price (USD)  Baggage
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 1  UA1597      22:38→00:06(+1)     1h28m     Nonstop $81.86       1PC/23KG
 2  CA1234      09:00→11:20         2h20m     Nonstop $95.00       1PC/23KG
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2 flights found
Lowest: $81.86 (before tax), incl. tax: $116.80
```

### Price Calendar Results

```
📅 Price Calendar
✈️ Shanghai (SHA) → Los Angeles (LAX)  |  Economy

Date            Lowest          Flights
─────────────────────────────────────
2026-04-01      $520.00 ⭐       8
2026-04-02      $490.00 🏆 Best  6
2026-04-03      $535.00          7
2026-04-04      $510.00          5
2026-04-05      $580.00          6
─────────────────────────────────────
Recommended date: 2026-04-02 ($490.00)
```

### Field Interpretation Rules

- **Total price incl. tax** = `price` + `tax` (adult fare)
- **Multiple passengers** = adult total × adultNumber + child total × childNumber
- **Stops** = number of segments - 1; show stopover city when `stopQuantity > 0`
- **Baggage** = `baggages[].pieces` + `baggages[].weight`; note "baggage not included" when `freeBaggage: false`
- **Limited seats** = show ⚠️ "Only X seats left" when `maxSeatsRemain ≤ 3`

---

## Key Response Fields

| Field | Description |
|-------|-------------|
| `status` | 0 = success |
| `message` | "SUCCESS" indicates normal response |
| `routings[]` | List of flight options |
| `routings[].prices[]` | Prices by passenger type (ADT = Adult, CHD = Child) |
| `routings[].segments[]` | Segment details (each stopover is a separate segment) |
| `routings[].rule.baggages[]` | Free baggage allowance |
| `routings[].rule.freeBaggage` | false = baggage must be purchased separately |
| `routings[].maxSeatsRemain` | Remaining seats |
| `passengerType` | ADT = Adult, CHD = Child |

---

## Error Handling

| Scenario | Action |
|----------|--------|
| `status != 0` or `message != "SUCCESS"` | Inform the user the query failed; suggest trying a different date |
| `routings` is an empty list | Notify that no flights are available for this route/date |
| Network timeout | Retry once; if it fails again, ask the user to try later |
| Unrecognized city code | Ask the user to confirm the full city or airport name |
| childNumber > adultNumber | Prompt: "Number of children cannot exceed the number of adults" |
