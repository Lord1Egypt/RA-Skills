---
name: croatia-weather
description: "Swiss-army knife for Croatian weather — 27 commands covering current conditions, forecasts (7-day, 3-day, 3-hourly, regional, outlook), warnings (CAP, heat/cold wave), agriculture (soil temp, frost, agro bulletin, weekly agro data), maritime (Adriatic nautical, maritime forecast, sea temp), hydrology (river temps, river levels, precipitation, snow), environment (UV index, fire danger, biometeo), climate (125-year averages, annual precipitation), and European weather. All data from DHMZ (Državni hidrometeorološki zavod). Use when: (1) user asks about weather in Croatia or any Croatian city, (2) 'home' / 'my location' → configured home station, (3) any Croatian forecast, warnings, bura, UV, sea temp, snow, fire danger, river levels, soil temp, agriculture, sailing, maritime. For locations outside Croatia and Europe → use the standard weather skill."
metadata: {"openclaw":{"emoji":"🌦️","requires":{"bins":["python3"]}}}
---

# Croatia Weather — DHMZ Data

Fetches official weather data from **DHMZ** (Državni hidrometeorološki zavod) via their free XML feeds.
Data is licensed under [Open Licence (data.gov.hr)](https://data.gov.hr/open-licence-republic-croatia) — attribution: **Izvor: DHMZ**.

## Home Station (Configurable)

The default station is **Zagreb-Grič** (current) / **Zagreb_Maksimir** (forecast).
Customise via environment variables:

| Variable | Purpose | Default |
|---|---|---|
| `DHMZ_HOME_CURRENT` | Station for current conditions | `Zagreb-Grič` |
| `DHMZ_HOME_FORECAST` | Station for forecasts | `Zagreb_Maksimir` |
| `DHMZ_HOME_ALIASES` | Extra words that resolve to home (comma-separated) | _(empty)_ |

Any query mentioning "home", "my location", or "doma" uses the configured home station.

## CLI Tool

All commands go through a single Python script — no external dependencies (stdlib only).

```bash
python3 {baseDir}/scripts/dhmz.py <command> [options]
```

---

## Commands — Weather & Forecasts

### Current conditions

```bash
python3 {baseDir}/scripts/dhmz.py current                  # Home station
python3 {baseDir}/scripts/dhmz.py current Zagreb            # Fuzzy match → Zagreb-Grič
python3 {baseDir}/scripts/dhmz.py current --all             # All 50+ stations
```

Returns: temperature, humidity, pressure (with trend), wind direction/speed, weather description.

### 7-day forecast

```bash
python3 {baseDir}/scripts/dhmz.py forecast                  # Home station
python3 {baseDir}/scripts/dhmz.py forecast Split
```

Returns: daily min/max temperature, precipitation total, peak wind, weather symbol — for 7 days.

### 3-day 3-hourly forecast

```bash
python3 {baseDir}/scripts/dhmz.py forecast3                 # Home station
python3 {baseDir}/scripts/dhmz.py forecast3 Dubrovnik
```

Returns: 3-hourly breakdown for 3 days — temperature, precipitation, wind, weather per time slot.

### 3-day text outlook (with temperature/wind summary)

```bash
python3 {baseDir}/scripts/dhmz.py outlook
```

Returns: prose overview for next 3 days + Kopno/More temperature, wind, and warning level.

### Regional text forecast

```bash
python3 {baseDir}/scripts/dhmz.py regions
```

Returns: DHMZ prose forecast for 6 regions (Istočna, Središnja, Gorska, Sj. Jadran, Dalmacija, Istra).

### Temperature extremes (min/max)

```bash
python3 {baseDir}/scripts/dhmz.py temp-extremes             # All stations
python3 {baseDir}/scripts/dhmz.py temp-extremes Zagreb
```

### European weather

```bash
python3 {baseDir}/scripts/dhmz.py europe                    # All European capitals
python3 {baseDir}/scripts/dhmz.py europe Beograd            # Specific city
```

---

## Commands — Warnings & Health

### Weather warnings (CAP)

```bash
python3 {baseDir}/scripts/dhmz.py warnings
```

Returns: active warnings for today/tomorrow/day-after — severity color-coded (🟡🟠🔴), regions, description.

### Heat wave warnings (5-day)

```bash
python3 {baseDir}/scripts/dhmz.py heatwave
```

Returns: 5-day heat wave indicator per city (🟢 Green → 🔴 Red).

### Cold wave warnings (4-day)

```bash
python3 {baseDir}/scripts/dhmz.py coldwave
```

Returns: 4-day cold wave indicator per city.

### Biometeorological forecast

```bash
python3 {baseDir}/scripts/dhmz.py bio
```

Returns: 3-day biometeo outlook — human health impact + per-region severity.

---

## Commands — Agriculture & Land

### Ground frost indicator (5cm temperature)

```bash
python3 {baseDir}/scripts/dhmz.py frost                     # All stations
python3 {baseDir}/scripts/dhmz.py frost Zagreb
```

Returns: min temperature at 5cm above ground — critical for frost/agriculture. Flags 🥶 MRAZ when ≤0°C.

### Soil temperatures (5/10/20cm depths)

```bash
python3 {baseDir}/scripts/dhmz.py soil
```

Returns: soil temperature at 3 depths (07/14/21/00h readings) + soil state (smrznuto/vlažno/mokro/suho/snijeg).

### Agrometeorological bulletin

```bash
python3 {baseDir}/scripts/dhmz.py agro
```

Returns: comprehensive weekly agro analysis + 5-region forecast (Istočna, Središnja, Lika, Istra/Primorje, Dalmacija) + 3-day outlook. Includes temperature sums, soil temps, precipitation, plant protection advice.

### Weekly agro summary data

```bash
python3 {baseDir}/scripts/dhmz.py agro7
```

Returns: 7-day per-station data table — Tmax, Tmin, T5cm min, precipitation, humidity range, sunshine hours, soil temps at 5cm and 20cm.

---

## Commands — Water & Hydrology

### Precipitation

```bash
python3 {baseDir}/scripts/dhmz.py precip                    # All stations with rain
python3 {baseDir}/scripts/dhmz.py precip Zagreb
```

### Snow depth

```bash
python3 {baseDir}/scripts/dhmz.py snow
```

### River water temperatures

```bash
python3 {baseDir}/scripts/dhmz.py rivers
```

Returns: latest hourly temperature from 19 hydrological stations — Drava, Dunav, Sava basin, Krapina, Korana, Krka, Neretva, etc.

### Hydrological forecast (river levels)

```bash
python3 {baseDir}/scripts/dhmz.py hydro
```

Returns: river level status for Sava, Kupa, Dunav, Mura, Drava — with flood defense alert levels (pripremno stanje, redovne mjere, izvanredne mjere).

### Adriatic sea temperature

```bash
python3 {baseDir}/scripts/dhmz.py sea
```

---

## Commands — Maritime & Sailing

### Adriatic nautical forecast

```bash
python3 {baseDir}/scripts/dhmz.py adriatic
```

Returns: Maritime Meteorological Centre Split report — synoptic situation, warnings (knots, sea state), 12h + 12h forecast text.

### Maritime forecast for sailors

```bash
python3 {baseDir}/scripts/dhmz.py maritime
```

Returns: detailed 24h forecast split by North/Middle/South Adriatic + station observation table (wind, sea state, temperature, cloud cover, pressure).

---

## Commands — Environment

### UV index

```bash
python3 {baseDir}/scripts/dhmz.py uvi
```

Returns: hourly UV readings for all stations with risk level (🟢 low → 🟣 extreme).

### Forest fire danger index

```bash
python3 {baseDir}/scripts/dhmz.py fire
```

Returns: FWI-based fire danger for ~35 stations — temp, humidity, wind, precipitation, FWI score, danger level.

---

## Commands — Climate & History

### Historical monthly climate averages

```bash
python3 {baseDir}/scripts/dhmz.py climate zagreb_maksimir
python3 {baseDir}/scripts/dhmz.py climate dubrovnik
python3 {baseDir}/scripts/dhmz.py climate split_marjan
```

Available cities: bjelovar, dubrovnik, gospic, hvar, karlovac, knin, krizevci, mali_losinj, ogulin, osijek, parg, pazin, rijeka, senj, sisak, slavonski_brod, split_marjan, sibenik, varazdin, zadar, zagreb_gric, zagreb_maksimir, zavizan.

Returns: monthly mean temp, absolute max/min (with year), sunshine hours, precipitation, max snow depth, fog/frost/rain/snow days, ice/cold/warm/hot day counts.

### Annual precipitation by month

```bash
python3 {baseDir}/scripts/dhmz.py climate-rain 2025         # Specific year
python3 {baseDir}/scripts/dhmz.py climate-rain              # Previous year (default)
```

Available years: 2014–2026. Returns monthly rainfall totals per station.

---

## Commands — Utility

### List stations

```bash
python3 {baseDir}/scripts/dhmz.py stations
```

### Full overview (combined)

```bash
python3 {baseDir}/scripts/dhmz.py full                      # Home station
python3 {baseDir}/scripts/dhmz.py full Split
```

Combines: current + frost + warnings + 7-day forecast + regional forecast + biometeo + hydro.

---

## Station Matching

Fuzzy matching — exact names not required:

| User says | Matches |
|---|---|
| `home`, `doma`, `my` + configured aliases | Configured home station |
| `Zagreb` | Zagreb-Grič / Zagreb_Maksimir |
| `Split` | Split-Marjan / Split |
| `Dubrovnik` | Dubrovnik |
| `Rijeka` | Rijeka |
| Any partial name | Fuzzy: exact → contains → word match |

## Data Sources

All feeds are free under DHMZ Open Licence. Updated multiple times per day.

| Category | Feed | Content |
|---|---|---|
| **Current** | `vrijeme.hr/hrvatska_n.xml` | Live conditions (50+ stations) |
| **Current** | `vrijeme.hr/europa_n.xml` | European capitals weather |
| **Temp** | `vrijeme.hr/tx.xml` / `tn.xml` / `t5.xml` | Max/min/ground frost temps |
| **Precip** | `vrijeme.hr/oborina.xml` / `snijeg_n.xml` | Rainfall, snow depth |
| **Sea** | `vrijeme.hr/more_n.xml` | Adriatic sea temperature |
| **UV** | `vrijeme.hr/uvi.xml` | Hourly UV index |
| **Fire** | `vrijeme.hr/indeks.xml` | Forest fire danger (FWI) |
| **Rivers** | `vrijeme.hr/temp_vode.xml` | River water temperatures |
| **Soil** | `vrijeme.hr/agro_temp.xml` | Soil temps at 5/10/20cm |
| **Agro** | `klima.hr/agro_bilten.xml` / `agro7.xml` | Agro bulletin + 7-day data |
| **Warnings** | `meteo.hr/upozorenja/cap_hr_*.xml` | CAP alerts (3 days) |
| **Waves** | `prognoza.hr/toplinskival_5.xml` / `hladnival.xml` | Heat/cold wave indicators |
| **Forecast** | `prognoza.hr/prognoza_danas.xml` | Today's forecast |
| **Forecast** | `prognoza.hr/regije_danas.xml` | Regional text forecast |
| **Forecast** | `prognoza.hr/prognoza_izgledi.xml` | 3-day outlook |
| **Forecast** | `prognoza.hr/tri/3d_graf_i_simboli.xml` | 3-day 3-hourly meteogram |
| **Forecast** | `prognoza.hr/sedam/hrvatska/7d_meteogrami.xml` | 7-day meteogram |
| **Health** | `prognoza.hr/bio_novo.xml` | Biometeorological forecast |
| **Maritime** | `prognoza.hr/jadran_h.xml` / `pomorci.xml` | Adriatic nautical + maritime |
| **Hydro** | `hidro.hr/hidro_bilten.xml` | River levels + flood alerts |
| **Climate** | `klima.hr/k1/tablice/{city}.xml` | Monthly averages (125+ years) |
| **Climate** | `klima.hr/k2/{year}/oborina_{year}.xml` | Annual precipitation |

## Notes

- No API key needed — all feeds are public
- Zero external dependencies — Python 3 stdlib only
- Feed updates: current conditions ~hourly, forecasts ~twice daily (00:00/12:00 UTC)
- Wind format in forecasts: `NE2` = NE direction, strength 2 (1=slab, 2=umjeren, 3=jak, 4=olujni)
- Always attribute: **Izvor: DHMZ**
