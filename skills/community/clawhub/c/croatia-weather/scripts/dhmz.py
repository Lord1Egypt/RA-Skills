#!/usr/bin/env python3
"""
DHMZ Weather CLI — Swiss-army knife for Croatian weather data.
Data: Državni hidrometeorološki zavod (DHMZ) — https://meteo.hr
Licensed under Open Licence (data.gov.hr). Attribution: Izvor: DHMZ

Configure your home station via environment variables:
  DHMZ_HOME_CURRENT  — station name for current conditions (default: Zagreb-Grič)
  DHMZ_HOME_FORECAST — station name for forecasts (default: Zagreb_Maksimir)
  DHMZ_HOME_ALIASES  — comma-separated extra aliases that resolve to home (optional)
"""

import os
import sys
import argparse
import xml.etree.ElementTree as ET
from urllib.request import urlopen, Request
from urllib.error import URLError
from collections import defaultdict
from datetime import datetime

FEEDS = {
    "current": "https://vrijeme.hr/hrvatska_n.xml",
    "current_reg": "https://vrijeme.hr/hrvatska1_n.xml",
    "europe": "https://vrijeme.hr/europa_n.xml",
    "tx": "https://vrijeme.hr/tx.xml",
    "tn": "https://vrijeme.hr/tn.xml",
    "t5": "https://vrijeme.hr/t5.xml",
    "sea": "https://vrijeme.hr/more_n.xml",
    "precip": "https://vrijeme.hr/oborina.xml",
    "snow": "https://vrijeme.hr/snijeg_n.xml",
    "uvi": "https://vrijeme.hr/uvi.xml",
    "fire": "https://vrijeme.hr/indeks.xml",
    "river": "https://vrijeme.hr/temp_vode.xml",
    "soil": "https://vrijeme.hr/agro_temp.xml",
    "agro": "https://klima.hr/agro_bilten.xml",
    "agro7": "https://klima.hr/agro7.xml",
    "warn_today": "https://meteo.hr/upozorenja/cap_hr_today.xml",
    "warn_tomorrow": "https://meteo.hr/upozorenja/cap_hr_tomorrow.xml",
    "warn_day3": "https://meteo.hr/upozorenja/cap_hr_day_after_tomorrow.xml",
    "fc_today": "https://prognoza.hr/prognoza_danas.xml",
    "fc_tomorrow": "https://prognoza.hr/prognoza_sutra.xml",
    "fc_regions": "https://prognoza.hr/regije_danas.xml",
    "fc_outlook": "https://prognoza.hr/prognoza_izgledi.xml",
    "fc_3d_detail": "https://prognoza.hr/tri/3d_graf_i_simboli.xml",
    "fc_7d": "https://prognoza.hr/sedam/hrvatska/7d_meteogrami.xml",
    "bio": "https://prognoza.hr/bio_novo.xml",
    "heat_wave": "https://prognoza.hr/toplinskival_5.xml",
    "cold_wave": "https://prognoza.hr/hladnival.xml",
    "adriatic": "https://prognoza.hr/jadran_h.xml",
    "maritime": "https://prognoza.hr/pomorci.xml",
    "hydro": "https://hidro.hr/hidro_bilten.xml",
}

WEATHER_SYMBOLS = {
    "1": "☀️ Vedro", "1n": "🌙 Vedro",
    "2": "🌤️ Pretežno vedro", "2n": "🌙 Pretežno vedro",
    "3": "⛅ Djelomično oblačno", "3n": "🌙 Djelomično oblačno",
    "4": "🌥️ Umjereno oblačno", "4n": "🌙 Umjereno oblačno",
    "5": "☁️ Pretežno oblačno", "5n": "🌙 Pretežno oblačno",
    "6": "☁️ Oblačno", "6n": "🌙 Oblačno",
    "7": "🌫️ Magla", "7n": "🌫️ Magla", "8": "🌫️ Sumaglica",
    "9": "🌧️ Kiša", "10": "🌧️ Pljusak", "11": "⛈️ Grmljavina",
    "12": "🌦️ Slaba kiša", "12n": "🌙 Slaba kiša",
    "13": "🌨️ Snijeg", "14": "🌨️ Susnježica", "15": "🌨️ Slab snijeg",
    "20": "🌤️ Vedro → oblačno", "21": "🌥️ Oblačno → vedro",
    "22": "🌦️ Nestabilno", "23": "⛈️ Grmljavinski pljuskovi",
    "24": "🌧️ Obilna kiša", "25": "🌧️ Kiša",
    "26": "🌧️ Kiša", "26n": "🌙 Kiša",
    "27": "🌦️ Slaba kiša", "27n": "🌙 Slaba kiša",
    "28": "🌧️ Umjerena kiša", "28n": "🌙 Umjerena kiša",
    "29": "🌧️ Jaka kiša",
    "30": "🌨️ Slab snijeg", "30n": "🌙 Slab snijeg",
    "31": "🌨️ Snijeg", "31n": "🌙 Snijeg", "32": "🌨️ Jak snijeg",
    "40": "🌨️ Susnježica", "40n": "🌙 Susnježica",
    "70": "🌨️ Snijeg", "71": "🌨️ Slab snijeg", "72": "🌨️ Jak snijeg",
}

HOME_STATION_CURRENT = os.environ.get("DHMZ_HOME_CURRENT", "Zagreb-Grič")
HOME_STATION_FORECAST = os.environ.get("DHMZ_HOME_FORECAST", "Zagreb_Maksimir")
_extra_aliases = os.environ.get("DHMZ_HOME_ALIASES", "")
HOME_ALIASES = {"home", "doma", "moj", "my"} | (
    {a.strip().lower() for a in _extra_aliases.split(",") if a.strip()} if _extra_aliases else set()
)

REGION_MAP = {
    "istocna": "Istočna Hrvatska",
    "sredisnja": "Središnja Hrvatska",
    "gorska": "Gorska Hrvatska",
    "sjjadran": "Sjeverni Jadran",
    "dalmacija": "Dalmacija",
    "istra": "Istra",
}

RIVER_STATIONS = [
    ("7012", "Donji Miholjac", "Drava"),
    ("7255", "Batina", "Dunav"),
    ("7052", "Vukovar", "Dunav"),
    ("7311", "Ilok most", "Dunav"),
    ("7266", "Bregana-remont", "Bregana"),
    ("7411", "Samobor", "Gradna"),
    ("5170", "Bračak", "Krapina"),
    ("5150", "Luketići", "Korana"),
    ("5224", "Jarče Polje", "Donja Dobra"),
    ("5070", "Zamost 2", "Čabranka"),
    ("6013", "Kozjak most", "Kozjak jezero"),
    ("6026", "Portonski most", "Mirna"),
    ("4196", "Izvor Rječine", "Rječina"),
    ("4109", "Prevjes", "Zrmanja"),
    ("4105", "Krupa", "Krupa"),
    ("4082", "Roški slap", "Krka"),
    ("3387", "Nacionalni park", "Krka"),
    ("3012", "Dusina", "Matica Vrgorska"),
    ("3194", "Metković", "Neretva"),
]

SOIL_STATE = {"1": "smrznuto", "2": "vlažno", "3": "mokro", "4": "suho", "5": "snijeg"}

CLIMATE_CITIES = [
    "bjelovar", "dubrovnik", "gospic", "hvar", "karlovac", "knin",
    "krizevci", "mali_losinj", "ogulin", "osijek", "parg", "pazin",
    "rijeka", "senj", "sisak", "slavonski_brod", "split_marjan",
    "sibenik", "varazdin", "zadar", "zagreb_gric", "zagreb_maksimir", "zavizan",
]

AGRO_REGIONS = {
    "p_ih": "Istočna Hrvatska",
    "p_ssz": "Središnja i sjeverozapadna Hrvatska",
    "p_lg": "Lika i Gorski kotar",
    "p_ip": "Istra i Primorje",
    "p_da": "Dalmacija",
}

WAVE_COLORS = {"G": "🟢 Zeleno", "Y": "🟡 Žuto", "O": "🟠 Narančasto", "R": "🔴 Crveno", "W": "⚪ Bijelo"}


def fetch_xml(url):
    try:
        req = Request(url, headers={"User-Agent": "DHMZ-Weather-CLI/1.0"})
        with urlopen(req, timeout=15) as r:
            return ET.parse(r).getroot()
    except (URLError, ET.ParseError) as e:
        print(f"ERROR: Failed to fetch {url}: {e}", file=sys.stderr)
        sys.exit(1)


def match_station(name, candidates):
    """Fuzzy station match: exact → contains → case-insensitive contains."""
    norm = name.strip()
    norm_lower = norm.lower().replace("-", " ").replace("_", " ")
    if norm_lower in HOME_ALIASES:
        return None
    for c in candidates:
        if c == norm:
            return c
    for c in candidates:
        if norm_lower in c.lower().replace("-", " ").replace("_", " "):
            return c
    for c in candidates:
        cl = c.lower().replace("-", " ").replace("_", " ")
        if any(part in cl for part in norm_lower.split()):
            return c
    return None


def resolve_station(query, candidates, default):
    if not query or query.lower().strip() in HOME_ALIASES:
        return default
    found = match_station(query, candidates)
    if found:
        return found
    print(f"Station '{query}' not found. Available: {', '.join(sorted(candidates))}", file=sys.stderr)
    sys.exit(1)


# ── Original commands ──────────────────────────────────────

def cmd_current(args):
    """Current weather conditions from all DHMZ stations."""
    root = fetch_xml(FEEDS["current"])
    dt = root.find("DatumTermin")
    date_str = dt.find("Datum").text if dt is not None else "?"
    term_str = dt.find("Termin").text if dt is not None else "?"

    stations = {}
    for grad in root.findall("Grad"):
        name = grad.find("GradIme").text.strip()
        stations[name] = grad

    target = resolve_station(args.station, stations.keys(), HOME_STATION_CURRENT)
    grad = stations[target]
    pod = grad.find("Podatci")

    def txt(tag):
        el = pod.find(tag)
        return el.text.strip() if el is not None and el.text else "-"

    print(f"📍 {target} — DHMZ ({date_str} {term_str}:00 UTC)")
    print(f"🌡️  Temperatura:    {txt('Temp')}°C")
    print(f"💧 Vlaga:          {txt('Vlaga')}%")
    print(f"🔵 Tlak:           {txt('Tlak')} hPa (trend: {txt('TlakTend')})")
    print(f"💨 Vjetar:         {txt('VjetarSmjer')} {txt('VjetarBrzina')} m/s")
    print(f"🌤️  Vrijeme:        {txt('Vrijeme')}")

    if args.all:
        print(f"\n{'─'*60}")
        print(f"Sve postaje ({date_str} {term_str}:00 UTC):\n")
        print(f"{'Postaja':<30} {'°C':>5} {'Vlaga':>6} {'hPa':>7} {'Vjetar':>12} Opis")
        print(f"{'─'*30} {'─'*5} {'─'*6} {'─'*7} {'─'*12} {'─'*20}")
        for name in sorted(stations):
            g = stations[name]
            p = g.find("Podatci")
            def t(tag, _p=p):
                el = _p.find(tag)
                return el.text.strip() if el is not None and el.text else "-"
            wind = f"{t('VjetarSmjer')} {t('VjetarBrzina')}"
            print(f"{name:<30} {t('Temp'):>5} {t('Vlaga'):>5}% {t('Tlak'):>7} {wind:>12} {t('Vrijeme')}")


def cmd_forecast(args):
    """7-day forecast from DHMZ meteograms."""
    root = fetch_xml(FEEDS["fc_7d"])
    izmjena = root.find("izmjena")
    update_info = izmjena.text.strip() if izmjena is not None else ""

    cities = {}
    for grad in root.findall("grad"):
        cities[grad.attrib.get("ime", "")] = grad

    target = resolve_station(args.city, cities.keys(), HOME_STATION_FORECAST)
    grad = cities[target]

    print(f"📍 {target.replace('_', ' ')} — 7-dnevna prognoza DHMZ")
    if update_info:
        print(f"   {update_info}")
    print()

    by_date = defaultdict(list)
    for d in grad.findall("dan"):
        by_date[d.attrib["datum"]].append(d)

    print(f"{'Dan':<14} {'Min':>4} {'Max':>4} {'Oborina':>8} {'Vjetar':>10} Vrijeme")
    print(f"{'─'*14} {'─'*4} {'─'*4} {'─'*8} {'─'*10} {'─'*25}")

    for datum in sorted(by_date.keys())[:7]:
        entries = by_date[datum]
        temps = [int(e.find("t_2m").text) for e in entries if e.find("t_2m") is not None]
        precip = sum(float(e.find("oborina").text) for e in entries if e.find("oborina") is not None)
        day_entries = [e for e in entries if int(e.attrib.get("sat", 0)) in (11, 14)]
        sym_entry = day_entries[0] if day_entries else entries[len(entries) // 2]
        sym = sym_entry.find("simbol").text if sym_entry.find("simbol") is not None else "-"
        desc = WEATHER_SYMBOLS.get(sym, sym)
        winds = [e.find("vjetar").text for e in entries if e.find("vjetar") is not None]
        peak_wind = max(winds, key=lambda w: int(w[-1]) if w and w[-1].isdigit() else 0) if winds else "-"
        dtj = entries[0].attrib.get("dtj", "")
        label = f"{dtj:<10} {datum[:5]}"
        rain_str = f"{precip:.1f}mm" if precip > 0 else "—"
        print(f"{label:<14} {min(temps):>3}° {max(temps):>3}° {rain_str:>8} {peak_wind:>10} {desc}")


def cmd_forecast3(args):
    """3-day detailed (3-hourly) forecast."""
    root = fetch_xml(FEEDS["fc_3d_detail"])
    izmjena = root.find("izmjena")
    update_info = izmjena.text.strip() if izmjena is not None else ""

    cities = {}
    for grad in root.findall("grad"):
        cities[grad.attrib.get("ime", "")] = grad

    target = resolve_station(args.city, cities.keys(), HOME_STATION_FORECAST)
    grad = cities[target]

    print(f"📍 {target.replace('_', ' ')} — 3-dnevna prognoza (trosatna) DHMZ")
    if update_info:
        print(f"   {update_info}")
    print()

    print(f"{'Datum':<14} {'Sat':>4} {'°C':>4} {'Oborina':>8} {'Vjetar':>8} Vrijeme")
    print(f"{'─'*14} {'─'*4} {'─'*4} {'─'*8} {'─'*8} {'─'*25}")

    prev_date = ""
    for d in grad.findall("dan"):
        datum = d.attrib.get("datum", "")[:10]
        sat = d.attrib.get("sat", "")
        dtj = d.attrib.get("dtj", "")
        temp = d.find("t_2m").text if d.find("t_2m") is not None else "-"
        sym = d.find("simbol").text if d.find("simbol") is not None else "-"
        wind = d.find("vjetar").text if d.find("vjetar") is not None else "-"
        rain = d.find("oborina").text if d.find("oborina") is not None else "0"
        desc = WEATHER_SYMBOLS.get(sym, sym)
        rain_str = f"{float(rain):.1f}mm" if float(rain) > 0 else "—"
        date_label = f"{dtj:<10} {datum[:5]}" if datum != prev_date else ""
        prev_date = datum
        print(f"{date_label:<14} {sat:>4}h {temp:>3}° {rain_str:>8} {wind:>8} {desc}")


def cmd_warnings(args):
    """Active DHMZ weather warnings (CAP format)."""
    feeds = [
        ("Danas", FEEDS["warn_today"]),
        ("Sutra", FEEDS["warn_tomorrow"]),
        ("Prekosutra", FEEDS["warn_day3"]),
    ]
    ns = {"cap": "urn:oasis:names:tc:emergency:cap:1.2"}
    found_any = False
    for label, url in feeds:
        try:
            root = fetch_xml(url)
        except SystemExit:
            continue
        infos = root.findall("cap:info", ns)
        en_infos = [i for i in infos if (i.find("cap:language", ns) is not None and i.find("cap:language", ns).text == "en")]
        if not en_infos:
            en_infos = infos

        seen = set()
        for info in en_infos:
            event = info.find("cap:event", ns)
            desc = info.find("cap:description", ns)
            severity = info.find("cap:severity", ns)
            area = info.find("cap:area", ns)
            area_desc = area.find("cap:areaDesc", ns) if area is not None else None

            event_t = event.text if event is not None else "?"
            desc_t = desc.text.strip() if desc is not None and desc.text else ""
            sev_t = severity.text if severity is not None else "?"
            area_t = area_desc.text if area_desc is not None else "?"

            key = f"{event_t}|{area_t}"
            if key in seen:
                continue
            seen.add(key)

            level_params = info.findall("cap:parameter", ns)
            color = ""
            for p in level_params:
                vn = p.find("cap:valueName", ns)
                if vn is not None and vn.text == "awareness_level":
                    val = p.find("cap:value", ns)
                    if val is not None:
                        parts = val.text.split(";")
                        if len(parts) >= 2:
                            color = parts[1].strip()

            icon = {"yellow": "🟡", "orange": "🟠", "red": "🔴"}.get(color, "⚠️")
            if not found_any:
                print("⚠️  DHMZ Upozorenja\n")
                found_any = True
            print(f"{icon} [{label}] {event_t} — {area_t} (severity: {sev_t})")
            if desc_t:
                print(f"   {desc_t}")
            print()

    if not found_any:
        print("✅ Nema aktivnih upozorenja.")


def cmd_regions(args):
    """Regional text forecast for today."""
    root = fetch_xml(FEEDS["fc_regions"])
    date_el = root.find("datum")
    date_str = date_el.text.strip() if date_el is not None else "?"
    print(f"📋 Regionalna prognoza — {date_str}\n")

    for tag, label in REGION_MAP.items():
        el = root.find(tag)
        if el is not None and el.text:
            print(f"📍 {label}")
            print(f"   {el.text.strip()}\n")


def cmd_precip(args):
    """Daily precipitation amounts."""
    root = fetch_xml(FEEDS["precip"])
    dt = root.find("datumtermin")
    date_str = dt.find("datum").text if dt is not None else "?"
    term_str = dt.find("termin").text if dt is not None else "?"

    stations = {}
    for grad in root.findall("grad"):
        name = grad.find("ime").text.strip()
        stations[name] = grad

    if args.station:
        target = resolve_station(args.station, stations.keys(), HOME_STATION_CURRENT.replace("RC ", ""))
        g = stations[target]
        amount = g.find("kolicina").text.strip() if g.find("kolicina") is not None else "-"
        print(f"🌧️ Oborina {target}: {amount} mm ({date_str} {term_str}:00 UTC)")
    else:
        print(f"🌧️ Dnevna oborina — {date_str} {term_str}:00 UTC\n")
        print(f"{'Postaja':<30} {'mm':>8}")
        print(f"{'─'*30} {'─'*8}")
        for name in sorted(stations):
            g = stations[name]
            amount = g.find("kolicina").text.strip() if g.find("kolicina") is not None else "-"
            if float(amount) > 0:
                print(f"{name:<30} {amount:>7} mm")


def cmd_temp_extremes(args):
    """Today's min/max temperature extremes."""
    root_tx = fetch_xml(FEEDS["tx"])
    root_tn = fetch_xml(FEEDS["tn"])

    dt_tx = root_tx.find("datumtermin")
    tx_date = dt_tx.find("datum").text if dt_tx is not None else "?"
    dt_tn = root_tn.find("datumtermin")
    tn_date = dt_tn.find("datum").text if dt_tn is not None else "?"

    tx_map = {g.find("ime").text.strip(): g.find("tempmax").text.strip() for g in root_tx.findall("grad")}
    tn_map = {g.find("ime").text.strip(): g.find("tempmin").text.strip() for g in root_tn.findall("grad")}
    all_names = sorted(set(tx_map) | set(tn_map))

    if args.station:
        target = resolve_station(args.station, all_names, HOME_STATION_FORECAST)
        print(f"🌡️ {target}: Tmin = {tn_map.get(target, '-')}°C ({tn_date}), Tmax = {tx_map.get(target, '-')}°C ({tx_date})")
    else:
        print(f"🌡️ Temperature — Tmin ({tn_date}) / Tmax ({tx_date})\n")
        print(f"{'Postaja':<30} {'Tmin':>7} {'Tmax':>7}")
        print(f"{'─'*30} {'─'*7} {'─'*7}")
        for name in all_names:
            print(f"{name:<30} {tn_map.get(name, '-'):>6}° {tx_map.get(name, '-'):>6}°")


def cmd_snow(args):
    """Snow depth at stations with snow cover."""
    root = fetch_xml(FEEDS["snow"])
    title = root.find("naslov")
    print(f"❄️  {title.text.strip() if title is not None else 'Visine snijega'}\n")
    print(f"{'Postaja':<30} {'Snijeg':>8} {'Novi':>8}")
    print(f"{'─'*30} {'─'*8} {'─'*8}")
    for grad in root.findall("grad"):
        name = grad.find("ime").text.strip()
        snow = grad.find("snijeg").text.strip() if grad.find("snijeg") is not None else "-"
        new_snow = grad.find("novi_snijeg").text.strip() if grad.find("novi_snijeg") is not None else "-"
        print(f"{name:<30} {snow:>6} cm {new_snow:>6} cm")
    if not root.findall("grad"):
        print("Nema snježnog pokrivača.")


def cmd_uvi(args):
    """UV index readings."""
    root = fetch_xml(FEEDS["uvi"])
    date_el = root.find("Datum")
    date_str = date_el.text.strip() if date_el is not None else "?"
    print(f"☀️  UV Indeks — {date_str}\n")

    rows = root.findall("Podatci")
    if not rows:
        print("Nema podataka.")
        return
    header = rows[0]
    terms = [t.text for t in header.findall("Termin")]
    print(f"{'Postaja':<25} {' '.join(f'{h:>5}h' for h in terms)}")
    print(f"{'─'*25} {'─'*((6)*len(terms))}")

    for row in rows[1:]:
        station_el = row.find("Postaja")
        station = station_el.text.strip() if station_el is not None else "?"
        vals = []
        for t in row.findall("Termin"):
            v = t.text.strip() if t is not None and t.text and t.text.strip() else "-"
            vals.append(v)
        max_val = max((float(v) for v in vals if v != "-"), default=0)
        level = "🟢 low" if max_val < 3 else "🟡 moderate" if max_val < 6 else "🟠 high" if max_val < 8 else "🔴 very high" if max_val < 11 else "🟣 extreme"
        print(f"{station:<25} {' '.join(f'{v:>5} ' for v in vals)} ({level})")


def cmd_sea(args):
    """Adriatic sea temperatures."""
    root = fetch_xml(FEEDS["sea"])
    date_el = root.find("Datum")
    date_str = date_el.text.strip() if date_el is not None else "?"
    print(f"🌊 Temperatura mora — {date_str}\n")

    rows = root.findall("Podatci")
    if not rows:
        print("Nema podataka.")
        return
    header = rows[0]
    terms = [t.text for t in header.findall("Termin")]
    print(f"{'Postaja':<25} {' '.join(f'{h:>5}h' for h in terms)}")
    print(f"{'─'*25} {'─'*((6)*len(terms))}")

    for row in rows[1:]:
        station_el = row.find("Postaja")
        station = station_el.text.strip() if station_el is not None else "?"
        vals = []
        for t in row.findall("Termin"):
            v = t.text.strip() if t is not None and t.text and t.text.strip() else "-"
            if v != "-":
                v = f"{v}°"
            vals.append(v)
        print(f"{station:<25} {' '.join(f'{v:>5} ' for v in vals)}")


def cmd_fire(args):
    """Forest fire danger index."""
    root = fetch_xml(FEEDS["fire"])
    date_el = root.find("datum")
    date_str = date_el.text.strip() if date_el is not None else "?"
    print(f"🔥 Indeks opasnosti od šumskih požara — {date_str}\n")
    print(f"{'Postaja':<20} {'°C':>5} {'Vlaga':>6} {'Vjetar':>7} {'Oborina':>8} {'FWI':>5} Opasnost")
    print(f"{'─'*20} {'─'*5} {'─'*6} {'─'*7} {'─'*8} {'─'*5} {'─'*12}")

    for p in root.findall("postaja"):
        def t(tag, _p=p):
            el = _p.find(tag)
            return el.text.strip() if el is not None and el.text else "-"
        icon = {"niska": "🟢", "umjerena": "🟡", "visoka": "🟠", "vrlo visoka": "🔴", "ekstremna": "🟣"}.get(t("indeks"), "⚪")
        print(f"{t('ime'):<20} {t('temperatura'):>5} {t('vlaga'):>5}% {t('vjetar'):>6} km/h {t('oborina'):>5} mm {t('fwi'):>5} {icon} {t('indeks')}")


def cmd_bio(args):
    """Biometeorological forecast."""
    root = fetch_xml(FEEDS["bio"])
    print("🧑‍⚕️ Biometeorološka prognoza\n")

    bio_levels = {"1": "🟢 Povoljno", "2": "🟡 Umjereno nepovoljno", "3": "🟠 Nepovoljno", "4": "🔴 Vrlo nepovoljno"}

    for pod in root.findall("Podaci"):
        date_el = pod.find("Datum")
        text_el = pod.find("Tekst")
        if date_el is None:
            continue
        print(f"📅 {date_el.text.strip()}")
        if text_el is not None and text_el.text:
            print(f"   {text_el.text.strip()}")
        regions = []
        for tag, label in [("istocna", "Istočna"), ("sredisnja", "Središnja"), ("gorska", "Gorska"), ("sjevernijadran", "Sj. Jadran"), ("juznijadran", "J. Jadran")]:
            el = pod.find(f"station[@name='{tag}']")
            if el is not None and el.text:
                level = bio_levels.get(el.text.strip(), el.text.strip())
                regions.append(f"   {label}: {level}")
        if regions:
            print("\n".join(regions))
        print()


def cmd_stations(args):
    """List all available station names for each feed type."""
    print("📡 DHMZ Postaje\n")
    print(f"Configured home: {HOME_STATION_CURRENT} (current) / {HOME_STATION_FORECAST} (forecast)\n")
    print("── Trenutno stanje (hrvatska_n.xml) ──")
    root = fetch_xml(FEEDS["current"])
    names = sorted(g.find("GradIme").text.strip() for g in root.findall("Grad"))
    for n in names:
        print(f"  {n}")

    print(f"\n── Prognoza 7d (7d_meteogrami.xml) ──")
    root = fetch_xml(FEEDS["fc_7d"])
    names = sorted(set(g.attrib.get("ime", "") for g in root.findall("grad")))
    for n in names:
        print(f"  {n.replace('_', ' ')}")

    print(f"\n── Klima (srednje mjesečne vrijednosti) ──")
    for c in CLIMATE_CITIES:
        print(f"  {c}")


# ── NEW: Frost (ground-level 5cm min temp) ─────────────────

def cmd_frost(args):
    """Min temperature at 5cm above ground — frost indicator."""
    root = fetch_xml(FEEDS["t5"])
    dt = root.find("datumtermin")
    date_str = dt.find("datum").text if dt is not None else "?"
    term_str = dt.find("termin").text if dt is not None else "?"

    stations = {}
    for grad in root.findall("grad"):
        name = grad.find("ime").text.strip()
        stations[name] = grad

    if args.station:
        target = resolve_station(args.station, stations.keys(), HOME_STATION_FORECAST)
        g = stations[target]
        temp = g.find("temp5").text.strip() if g.find("temp5") is not None else "-"
        frost = "🥶 MRAZ" if temp != "-" and float(temp) <= 0 else "✅ Bez mraza"
        print(f"🌱 {target}: T5cm = {temp}°C — {frost} ({date_str} {term_str}:00 UTC)")
    else:
        print(f"🌱 Minimalna temperatura na 5 cm — {date_str} {term_str}:00 UTC\n")
        print(f"{'Postaja':<35} {'T5cm':>6} Status")
        print(f"{'─'*35} {'─'*6} {'─'*12}")
        for name in sorted(stations):
            g = stations[name]
            temp = g.find("temp5").text.strip() if g.find("temp5") is not None else "-"
            frost = "🥶 MRAZ" if temp != "-" and float(temp) <= 0 else ""
            print(f"{name:<35} {temp:>5}° {frost}")


# ── NEW: Soil temperature ──────────────────────────────────

def cmd_soil(args):
    """Soil temperature at 5/10/20cm depths."""
    root = fetch_xml(FEEDS["soil"])
    date_el = root.find("datum")
    date_str = date_el.text.strip() if date_el is not None else "?"
    print(f"🌾 Temperatura tla — {date_str}\n")
    print(f"{'Postaja':<20} {'5cm (07/14/21/00)':>22} {'10cm (07/14/21/00)':>22} {'20cm (07/14/21/00)':>22} Stanje tla")
    print(f"{'─'*20} {'─'*22} {'─'*22} {'─'*22} {'─'*14}")

    for p in root.findall("postaja"):
        name_el = p.find("ime")
        name = name_el.text.strip() if name_el is not None else "?"

        def get_temps(tag):
            el = p.find(tag)
            if el is None:
                return "- / - / - / -"
            temps = [t.text.strip() if t.text else "-" for t in el.findall("tt")]
            while len(temps) < 4:
                temps.append("-")
            return " / ".join(f"{t:>4}" for t in temps)

        t5 = get_temps("temppet")
        t10 = get_temps("tempdeset")
        t20 = get_temps("tempdvadeset")

        stanje_el = p.find("stanjetla")
        if stanje_el is not None:
            states = [SOIL_STATE.get(s.text.strip(), s.text.strip()) for s in stanje_el.findall("stanje") if s.text]
            state_str = ", ".join(states)
        else:
            state_str = "-"

        print(f"{name:<20} {t5:>22} {t10:>22} {t20:>22} {state_str}")


# ── NEW: River temperatures ────────────────────────────────

def cmd_rivers(args):
    """River water temperatures from 19 hydrological stations."""
    root = fetch_xml(FEEDS["river"])
    print("🏞️  Temperature rijeka\n")
    print(f"{'Postaja':<20} {'Rijeka':<18} {'Zadnja':>8} {'Vrijeme':>22}")
    print(f"{'─'*20} {'─'*18} {'─'*8} {'─'*22}")

    timeseries = root.findall("timeseries")
    for i, ts in enumerate(timeseries):
        if i >= len(RIVER_STATIONS):
            break
        sid, station, river = RIVER_STATIONS[i]
        data = ts.find("data")
        if data is None:
            print(f"{station:<20} {river:<18} {'N/A':>8}")
            continue
        rows = data.findall("r")
        last_valid = None
        for r in reversed(rows):
            cols = r.findall("c")
            if len(cols) >= 2 and cols[1].text is not None:
                last_valid = cols
                break
        if last_valid:
            time_str = last_valid[0].text
            temp = last_valid[1].text
            if "T" in time_str:
                time_str = time_str.split("T")[0] + " " + time_str.split("T")[1][:5]
            print(f"{station:<20} {river:<18} {temp:>6}°C {time_str:>22}")
        else:
            print(f"{station:<20} {river:<18} {'N/A':>8}")


# ── NEW: Hydrological forecast ─────────────────────────────

def cmd_hydro(args):
    """Hydrological forecast — river levels and flood alerts."""
    root = fetch_xml(FEEDS["hydro"])
    date_el = root.find("period_prognoze")
    date_str = date_el.text.strip() if date_el is not None else "?"
    print(f"🌊 Hidrološka prognoza — {date_str}\n")

    pripremno = root.find("pripremno_stanje")
    if pripremno is not None and pripremno.text and pripremno.text.strip():
        print(f"⚠️  Pripremno stanje: {pripremno.text.strip()}\n")

    redovne = root.find("redovne_mjere")
    if redovne is not None and redovne.text and redovne.text.strip():
        print(f"🟠 Redovne mjere obrane: {redovne.text.strip()}\n")

    izvanredne = root.find("izvanredne_mjere")
    if izvanredne is not None and izvanredne.text and izvanredne.text.strip():
        print(f"🔴 Izvanredne mjere obrane: {izvanredne.text.strip()}\n")

    river_tags = [
        ("sava", "🏞️  Sava"), ("kupa", "🏞️  Kupa"), ("dunav", "🏞️  Dunav"),
        ("mura", "🏞️  Mura"), ("drava", "🏞️  Drava"),
    ]
    for tag, label in river_tags:
        el = root.find(tag)
        if el is not None and el.text and el.text.strip():
            print(f"{label}")
            print(f"   {el.text.strip()}\n")


# ── NEW: Agro bulletin ─────────────────────────────────────

def cmd_agro(args):
    """Agrometeorological bulletin — weekly analysis + regional forecasts."""
    root = fetch_xml(FEEDS["agro"])
    date_el = root.find("datum_upisa")
    date_str = date_el.text.strip() if date_el is not None else "?"
    print(f"🌾 Agrometeorološki bilten — {date_str}\n")

    upozorenje = root.find("upozorenje")
    if upozorenje is not None and upozorenje.text and upozorenje.text.strip():
        print(f"⚠️  Upozorenje: {upozorenje.text.strip()}\n")

    interval = root.find("interval_analize")
    stanje = root.find("stanje")
    if interval is not None and stanje is not None:
        print(f"📊 Analiza ({interval.text.strip()}):")
        print(f"   {stanje.text.strip()}\n")

    interval_p = root.find("interval_prognoze")
    if interval_p is not None:
        print(f"📋 Prognoza ({interval_p.text.strip()}):")
    for tag, label in AGRO_REGIONS.items():
        el = root.find(tag)
        if el is not None and el.text:
            print(f"\n   📍 {label}")
            print(f"   {el.text.strip()}")

    interval_i = root.find("interval_izgleda")
    if interval_i is not None:
        print(f"\n\n🔮 Izgledi ({interval_i.text.strip()}):")
    for tag, label in [("unutrasnjost", "Unutrašnjost"), ("jadran", "Jadran")]:
        el = root.find(tag)
        if el is not None and el.text:
            print(f"   {label}: {el.text.strip()}")
    print()


# ── NEW: Agro 7-day data ──────────────────────────────────

def cmd_agro7(args):
    """Weekly agrometeorological data per station."""
    root = fetch_xml(FEEDS["agro7"])
    title = root.find("Naslov")
    print(f"🌾 {title.text.strip() if title is not None else 'Agro podaci (7 dana)'}\n")

    pods = root.find("Podaci")
    if pods is None:
        print("Nema podataka.")
        return

    print(f"{'Postaja':<18} {'Tmax':>5} {'Tmin':>5} {'T5min':>6} {'Oborina':>8} {'VlagaMax':>9} {'VlagaMin':>9} {'Sunce':>6} {'T5cm':>12} {'T20cm':>12}")
    print(f"{'─'*18} {'─'*5} {'─'*5} {'─'*6} {'─'*8} {'─'*9} {'─'*9} {'─'*6} {'─'*12} {'─'*12}")

    for grad in pods.findall("Grad"):
        def t(tag, el=grad):
            e = el.find(tag)
            return e.text.strip() if e is not None and e.text else "-"
        print(f"{t('GradIme'):<18} {t('Tmax'):>5} {t('Tmin'):>5} {t('Tmin5'):>6} {t('Obor'):>7}mm {t('VlagaMax'):>8}% {t('VlagaMin'):>8}% {t('Sunce'):>5}h {t('Tna5Max'):>5}/{t('Tna5Min'):<5} {t('Tna20Max'):>5}/{t('Tna20Min'):<5}")


# ── NEW: Adriatic nautical forecast ────────────────────────

def cmd_adriatic(args):
    """Adriatic nautical forecast from DHMZ Maritime Centre."""
    root = fetch_xml(FEEDS["adriatic"])
    title = root.find("Naslov")
    print(f"⛵ {title.text.strip() if title is not None else 'Prognoza za Jadran'}\n")

    upozorenje = root.find("Upozorenje")
    if upozorenje is not None:
        naslov = upozorenje.find("Upozorenje_naslov")
        tekst = upozorenje.find("Upozorenje_tekst")
        if naslov is not None and tekst is not None and tekst.text:
            print(f"⚠️  {naslov.text.strip()}")
            print(f"   {tekst.text.strip()}\n")

    stanje = root.find("Stanje")
    if stanje is not None:
        naslov = stanje.find("Stanje_naslov")
        tekst = stanje.find("Stanje_tekst")
        if naslov is not None and tekst is not None and tekst.text:
            print(f"🌍 {naslov.text.strip()}")
            print(f"   {tekst.text.strip()}\n")

    for el in root:
        if el.tag == "Prognoza_naslov":
            print(f"📋 {el.text.strip()}")
        elif el.tag == "Prognoza_tekst" and el.text:
            print(f"   {el.text.strip()}\n")


# ── NEW: Maritime forecast ─────────────────────────────────

def cmd_maritime(args):
    """Detailed maritime forecast with regional breakdown and station table."""
    root = fetch_xml(FEEDS["maritime"])
    title = root.find("Naslov")
    print(f"🚢 {title.text.strip() if title is not None else 'Prognoza za pomorce'}\n")

    upozorenje = root.find("Upozorenje")
    if upozorenje is not None and upozorenje.text and upozorenje.text.strip():
        print(f"⚠️  Upozorenje: {upozorenje.text.strip()}\n")

    stanje = root.find("Stanje")
    if stanje is not None and stanje.text and stanje.text.strip():
        print(f"🌍 Stanje: {stanje.text.strip()}\n")

    zaglavlje = root.find("Prognoza_zaglavlje")
    if zaglavlje is not None and zaglavlje.text:
        print(f"📋 {zaglavlje.text.strip()}\n")

    for el in root:
        if el.tag == "Prognoza_naslov":
            print(f"   📍 {el.text.strip()}")
        elif el.tag == "Prognoza_tekst" and el.text:
            print(f"   {el.text.strip()}\n")

    tablica = root.find("Tablica")
    if tablica is not None:
        zag = tablica.find("Tablica_zaglavlje")
        if zag is not None and zag.text:
            print(f"\n📊 {zag.text.strip()}")
        print(f"{'Postaja':<18} {'Vjetar':>12} {'More':>5} {'T°C':>5} {'Oblačnost':>15} {'hPa':>6}")
        print(f"{'─'*18} {'─'*12} {'─'*5} {'─'*5} {'─'*15} {'─'*6}")
        for pod in tablica.findall("Podaci"):
            station = pod.find("Postaja")
            if station is None:
                continue
            terms = [t.text.strip() if t is not None and t.text and t.text.strip() else "-" for t in pod.findall("Termin")]
            while len(terms) < 5:
                terms.append("-")
            print(f"{station.text.strip():<18} {terms[0]:>12} {terms[1]:>5} {terms[2]:>5} {terms[3]:>15} {terms[4]:>6}")


# ── NEW: 3-day outlook text ────────────────────────────────

def cmd_outlook(args):
    """3-day text outlook with temperature/wind summary."""
    root = fetch_xml(FEEDS["fc_outlook"])
    meta = root.find("metadata")
    created = meta.find("creationtime").text if meta is not None and meta.find("creationtime") is not None else "?"
    print(f"🔮 Izgledi za 3 dana — {created}\n")

    section = root.find("section")
    if section is None:
        print("Nema podataka.")
        return

    for param in section:
        if param.tag == "param" and param.attrib.get("name") == "rh_text":
            print(f"📝 {param.attrib.get('value', '')}\n")

    sym_map = {"1": "☀️", "2": "🌤️", "3": "⛅", "4": "🌥️", "5": "☁️", "6": "☁️",
               "12": "🌦️", "26": "🌧️", "27": "🌦️", "28": "🌧️"}

    print(f"{'Područje':<14} {'Datum':>8} {'Min':>5} {'Max':>5} {'Vjetar':>7} {'⚠️':>3} Vrijeme")
    print(f"{'─'*14} {'─'*8} {'─'*5} {'─'*5} {'─'*7} {'─'*3} {'─'*10}")

    for station in section.findall("station"):
        name = station.attrib.get("name", "")
        area = name.split(":")[-1] if ":" in name else name
        params = {p.attrib["name"]: p.attrib["value"] for p in station.findall("param")}
        datum = params.get("datum", "")
        if len(datum) == 6:
            datum = f"{datum[:2]}.{datum[2:4]}."
        sym = sym_map.get(params.get("vrijeme", ""), params.get("vrijeme", ""))
        pozor_val = int(params.get("pozor", "0"))
        pozor = ["—", "🟡", "🟠", "🔴"][min(pozor_val, 3)]
        print(f"{area:<14} {datum:>8} {params.get('Tmn', '-'):>4}° {params.get('Tmx', '-'):>4}° {params.get('wind', '-'):>6} {pozor:>3} {sym}")


# ── NEW: Heat wave warnings ────────────────────────────────

def cmd_heatwave(args):
    """5-day heat wave danger indicator per city."""
    root = fetch_xml(FEEDS["heat_wave"])
    print("🌡️🔴 Upozorenje na toplinske valove\n")

    section = root.find("section")
    if section is None:
        print("Nema podataka.")
        return

    print(f"{'Grad':<18} {'Dan1':>6} {'Dan2':>6} {'Dan3':>6} {'Dan4':>6} {'Dan5':>6}")
    print(f"{'─'*18} {'─'*6} {'─'*6} {'─'*6} {'─'*6} {'─'*6}")

    for station in section.findall("station"):
        name = station.attrib.get("name", "")
        params = {p.attrib["name"]: p.attrib["value"] for p in station.findall("param")}
        days = [WAVE_COLORS.get(params.get(f"dan{i}", ""), params.get(f"dan{i}", "-")) for i in range(1, 6)]
        print(f"{name:<18} {'  '.join(f'{d:>6}' for d in days)}")


# ── NEW: Cold wave warnings ────────────────────────────────

def cmd_coldwave(args):
    """4-day cold wave danger indicator per city."""
    root = fetch_xml(FEEDS["cold_wave"])
    print("🌡️🔵 Upozorenje na hladne valove\n")

    section = root.find("section")
    if section is None:
        print("Nema podataka.")
        return

    print(f"{'Grad':<18} {'Dan1':>6} {'Dan2':>6} {'Dan3':>6} {'Dan4':>6}")
    print(f"{'─'*18} {'─'*6} {'─'*6} {'─'*6} {'─'*6}")

    for station in section.findall("station"):
        name = station.attrib.get("name", "")
        params = {p.attrib["name"]: p.attrib["value"] for p in station.findall("param")}
        days = [WAVE_COLORS.get(params.get(f"dan{i}", ""), params.get(f"dan{i}", "-")) for i in range(1, 5)]
        print(f"{name:<18} {'  '.join(f'{d:>6}' for d in days)}")


# ── NEW: Climate averages ──────────────────────────────────

def cmd_climate(args):
    """Historical monthly climate averages for a Croatian city."""
    home_climate = HOME_STATION_FORECAST.lower().replace(" ", "_").replace("-", "_")
    city = (args.city or home_climate).lower().replace(" ", "_").replace("-", "_")
    if city in HOME_ALIASES:
        city = home_climate
    if city not in CLIMATE_CITIES:
        print(f"City '{city}' not available. Choose from: {', '.join(CLIMATE_CITIES)}", file=sys.stderr)
        sys.exit(1)

    url = f"https://klima.hr/k1/tablice/{city}.xml"
    root = fetch_xml(url)

    station = root.find("postaja")
    interval = root.find("interval")
    print(f"📊 Klima — {station.text if station is not None else city} ({interval.text if interval is not None else '?'})\n")

    months_hr = ["Sij", "Velj", "Ožu", "Tra", "Svi", "Lip", "Srp", "Kol", "Ruj", "Lis", "Stu", "Pro"]

    print(f"{'Parametar':<30} {' '.join(f'{m:>6}' for m in months_hr)}")
    print(f"{'─'*30} {'─'*((7)*12)}")

    for pod in root.findall("podaci"):
        el = pod.find("el")
        if el is None or el.text is None:
            continue
        label = el.text.strip()
        if not label:
            continue
        vals = [mj.text.strip() if mj.text else "-" for mj in pod.findall("mj")]
        while len(vals) < 12:
            vals.append("-")
        print(f"{label:<30} {' '.join(f'{v:>6}' for v in vals)}")


# ── NEW: Annual precipitation ──────────────────────────────

def cmd_climate_rain(args):
    """Monthly precipitation totals per station for a given year."""
    year = args.year or str(datetime.now().year - 1)
    url = f"https://klima.hr/k2/{year}/oborina_{year}.xml"
    root = fetch_xml(url)

    year_el = root.find("godina")
    print(f"🌧️ Godišnja oborina — {year_el.text if year_el is not None else year}\n")

    months = ["Sij", "Velj", "Ožu", "Tra", "Svi", "Lip", "Srp", "Kol", "Ruj", "Lis", "Stu", "Pro", "Ukup"]
    print(f"{'Postaja':<22} {' '.join(f'{m:>6}' for m in months)}")
    print(f"{'─'*22} {'─'*((7)*13)}")

    month_tags = ["sijecanj", "veljaca", "ozujak", "travanj", "svibanj", "lipanj",
                  "srpanj", "kolovoz", "rujan", "listopad", "studeni", "prosinac", "ukupno"]

    for p in root.findall("postaja"):
        name_el = p.find("ime_postaje")
        name = name_el.text.strip() if name_el is not None else "?"
        vals = []
        for tag in month_tags:
            el = p.find(tag)
            v = el.text.strip().replace(",", ".") if el is not None and el.text else "-"
            vals.append(v)
        print(f"{name:<22} {' '.join(f'{v:>6}' for v in vals)}")


# ── NEW: Europe weather ────────────────────────────────────

def cmd_europe(args):
    """Current weather conditions for European capital cities."""
    root = fetch_xml(FEEDS["europe"])
    dt = root.find("DatumTermin")
    date_str = dt.find("Datum").text if dt is not None else "?"
    term_str = dt.find("Termin").text if dt is not None else "?"

    cities = {}
    for grad in root.findall("Grad"):
        name = grad.find("GradIme").text.strip()
        cities[name] = grad

    if args.city:
        query = args.city.strip()
        target = None
        for c in cities:
            if query.lower() in c.lower():
                target = c
                break
        if not target:
            print(f"City '{query}' not found. Available: {', '.join(sorted(cities))}", file=sys.stderr)
            sys.exit(1)
        grad = cities[target]
        pod = grad.find("Podatci")
        def txt(tag):
            el = pod.find(tag)
            return el.text.strip() if el is not None and el.text else "-"
        print(f"📍 {target} ({date_str} {term_str}:00 UTC)")
        print(f"🌡️  Temperatura:    {txt('Temp')}°C")
        print(f"💧 Vlaga:          {txt('Vlaga')}%")
        print(f"🔵 Tlak:           {txt('Tlak')} hPa")
        print(f"💨 Vjetar:         {txt('VjetarSmjer')} {txt('VjetarBrzina')} m/s")
        print(f"🌤️  Vrijeme:        {txt('Vrijeme')}")
    else:
        print(f"🌍 Europa — {date_str} {term_str}:00 UTC\n")
        print(f"{'Grad':<22} {'°C':>5} {'Vlaga':>6} {'hPa':>7} {'Vjetar':>10} Opis")
        print(f"{'─'*22} {'─'*5} {'─'*6} {'─'*7} {'─'*10} {'─'*20}")
        for name in sorted(cities):
            g = cities[name]
            p = g.find("Podatci")
            def t(tag, _p=p):
                el = _p.find(tag)
                return el.text.strip() if el is not None and el.text else "-"
            wind = f"{t('VjetarSmjer')} {t('VjetarBrzina')}"
            print(f"{name:<22} {t('Temp'):>5} {t('Vlaga'):>5}% {t('Tlak'):>7} {wind:>10} {t('Vrijeme')}")


# ── Updated full command ───────────────────────────────────

def cmd_full(args):
    """Comprehensive weather overview."""
    print("=" * 60)
    print("  DHMZ Vremenska slika — Potpuni pregled")
    print("=" * 60)
    print()

    cmd_current(argparse.Namespace(station=args.station, all=False))
    print()

    cmd_frost(argparse.Namespace(station=args.station))
    print()

    cmd_warnings(argparse.Namespace())
    print()

    print("─" * 60)
    cmd_forecast(argparse.Namespace(city=args.station))
    print()

    print("─" * 60)
    cmd_regions(argparse.Namespace())

    print("─" * 60)
    cmd_bio(argparse.Namespace())

    print("─" * 60)
    cmd_hydro(argparse.Namespace())

    print("─" * 60)
    print("Izvor: DHMZ (https://meteo.hr)")


# ── CLI ─────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="DHMZ Weather CLI — Croatian weather data from Državni hidrometeorološki zavod",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s current                     Current conditions (home station)
  %(prog)s current Zagreb              Current conditions in Zagreb
  %(prog)s current --all               All stations
  %(prog)s forecast                    7-day forecast (home station)
  %(prog)s forecast Split              7-day forecast for Split
  %(prog)s forecast3 Dubrovnik         3-day 3-hourly forecast
  %(prog)s warnings                    Active DHMZ weather warnings
  %(prog)s regions                     Regional text forecast
  %(prog)s outlook                     3-day text outlook with temp/wind
  %(prog)s precip                      Precipitation (stations with rain)
  %(prog)s temp-extremes               Min/max temperatures
  %(prog)s frost                       Ground frost indicator (5cm temp)
  %(prog)s snow                        Snow depth
  %(prog)s uvi                         UV index
  %(prog)s sea                         Adriatic sea temperatures
  %(prog)s fire                        Forest fire danger index
  %(prog)s bio                         Biometeorological forecast
  %(prog)s heatwave                    5-day heat wave indicator
  %(prog)s coldwave                    4-day cold wave indicator
  %(prog)s soil                        Soil temperatures (5/10/20cm)
  %(prog)s agro                        Agrometeorological bulletin
  %(prog)s agro7                       Weekly agro summary data
  %(prog)s rivers                      River water temperatures
  %(prog)s hydro                       Hydrological forecast (river levels)
  %(prog)s adriatic                    Adriatic nautical forecast
  %(prog)s maritime                    Maritime forecast for sailors
  %(prog)s climate zagreb_maksimir     Historical monthly averages
  %(prog)s climate-rain 2025           Annual precipitation by month
  %(prog)s europe                      European capital cities weather
  %(prog)s europe Beograd              Specific European city
  %(prog)s stations                    List all station names
  %(prog)s full                        Full overview

Configure home station: DHMZ_HOME_CURRENT / DHMZ_HOME_FORECAST env vars.
Data source: DHMZ — https://meteo.hr (Open Licence, data.gov.hr)
""",
    )
    sub = parser.add_subparsers(dest="command")

    p_cur = sub.add_parser("current", help="Current conditions")
    p_cur.add_argument("station", nargs="?", default=None)
    p_cur.add_argument("--all", "-a", action="store_true")

    p_fc7 = sub.add_parser("forecast", help="7-day forecast")
    p_fc7.add_argument("city", nargs="?", default=None)

    p_fc3 = sub.add_parser("forecast3", help="3-day 3-hourly forecast")
    p_fc3.add_argument("city", nargs="?", default=None)

    sub.add_parser("warnings", help="Active weather warnings (today/tomorrow/day3)")
    sub.add_parser("regions", help="Regional text forecast")
    sub.add_parser("outlook", help="3-day text outlook with temp/wind")

    p_prec = sub.add_parser("precip", help="Precipitation amounts")
    p_prec.add_argument("station", nargs="?", default=None)

    p_tx = sub.add_parser("temp-extremes", help="Min/max temperature extremes")
    p_tx.add_argument("station", nargs="?", default=None)

    p_frost = sub.add_parser("frost", help="Ground frost indicator (5cm temp)")
    p_frost.add_argument("station", nargs="?", default=None)

    sub.add_parser("snow", help="Snow depth")
    sub.add_parser("uvi", help="UV index")
    sub.add_parser("sea", help="Adriatic sea temperatures")
    sub.add_parser("fire", help="Forest fire danger index")
    sub.add_parser("bio", help="Biometeorological forecast")
    sub.add_parser("heatwave", help="5-day heat wave indicator")
    sub.add_parser("coldwave", help="4-day cold wave indicator")
    sub.add_parser("soil", help="Soil temperatures (5/10/20cm)")
    sub.add_parser("agro", help="Agrometeorological bulletin")
    sub.add_parser("agro7", help="Weekly agro summary data")
    sub.add_parser("rivers", help="River water temperatures")
    sub.add_parser("hydro", help="Hydrological forecast (river levels)")
    sub.add_parser("adriatic", help="Adriatic nautical forecast")
    sub.add_parser("maritime", help="Maritime forecast for sailors")

    p_clim = sub.add_parser("climate", help="Historical monthly climate averages")
    p_clim.add_argument("city", nargs="?", default=None)

    p_rain = sub.add_parser("climate-rain", help="Annual precipitation by month")
    p_rain.add_argument("year", nargs="?", default=None)

    p_eur = sub.add_parser("europe", help="European capital cities weather")
    p_eur.add_argument("city", nargs="?", default=None)

    sub.add_parser("stations", help="List available station names")

    p_full = sub.add_parser("full", help="Full weather overview")
    p_full.add_argument("station", nargs="?", default=None)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    dispatch = {
        "current": cmd_current, "forecast": cmd_forecast, "forecast3": cmd_forecast3,
        "warnings": cmd_warnings, "regions": cmd_regions, "outlook": cmd_outlook,
        "precip": cmd_precip, "temp-extremes": cmd_temp_extremes, "frost": cmd_frost,
        "snow": cmd_snow, "uvi": cmd_uvi, "sea": cmd_sea, "fire": cmd_fire,
        "bio": cmd_bio, "heatwave": cmd_heatwave, "coldwave": cmd_coldwave,
        "soil": cmd_soil, "agro": cmd_agro, "agro7": cmd_agro7,
        "rivers": cmd_rivers, "hydro": cmd_hydro,
        "adriatic": cmd_adriatic, "maritime": cmd_maritime,
        "climate": cmd_climate, "climate-rain": cmd_climate_rain,
        "europe": cmd_europe, "stations": cmd_stations, "full": cmd_full,
    }
    dispatch[args.command](args)


if __name__ == "__main__":
    main()
