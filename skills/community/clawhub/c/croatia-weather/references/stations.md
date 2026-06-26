# DHMZ Station Cross-Reference

Station names differ between DHMZ feeds. Use this table to pick the correct name for each command.

> **Source of truth for feed URLs and XML structure:**
> https://meteo.hr/proizvodi.php?section=podaci&param=xml_korisnici
> If feeds stop working or station names change, check this page first.

---

## Home Station

The home station is configurable via environment variables. See the SKILL.md or README for details.

Default: **Zagreb-Grič** (current conditions) / **Zagreb_Maksimir** (forecasts).

---

## Major Cities — Cross-Reference

| City | `current` | `forecast`/`forecast3` | `climate` | Notes |
|---|---|---|---|---|
| **Zagreb** | Zagreb-Grič, Zagreb-Maksimir | Zagreb_Maksimir | zagreb_gric, zagreb_maksimir | Two stations |
| **Split** | Split-Marjan, Split-aerodrom | Split | split_marjan | |
| **Rijeka** | Rijeka | Rijeka | rijeka | |
| **Dubrovnik** | Dubrovnik | Dubrovnik | dubrovnik | |
| **Osijek** | RC Osijek-Čepin | Osijek | osijek | |
| **Zadar** | Zadar | Zadar | zadar | |
| **Šibenik** | Šibenik | Sibenik | sibenik | Accent difference |
| **Varaždin** | Varaždin | Varazdin | varazdin | Accent difference |
| **Karlovac** | Karlovac | Karlovac | karlovac | |
| **Pula** | Pula-aerodrom | Pula | — | No climate data |
| **Slavonski Brod** | Slavonski Brod | Slavonski_Brod | slavonski_brod | |
| **Gospić** | Gospić | Gospic | gospic | Accent difference |
| **Knin** | Knin | Knin | knin | |
| **Sisak** | Sisak | Sisak | sisak | |
| **Bjelovar** | Bjelovar | Bjelovar | bjelovar | |
| **Križevci** | Križevci | Krizevci | krizevci | |
| **Ogulin** | Ogulin | Ogulin | ogulin | |
| **Senj** | Senj | Senj | senj | |
| **Hvar** | Hvar | Hvar | hvar | |
| **Mali Lošinj** | — | Mali_Losinj | mali_losinj | Not in current |
| **Pazin** | Pazin | Pazin | pazin | |
| **Makarska** | Makarska | Makarska | — | |
| **Zavižan** | Zavižan | Zavizan | zavizan | Mountain station |

---

## Regions → Stations

### Istočna Hrvatska (Eastern)
Osijek (RC Osijek-Čepin), Vukovar-Grabovo, Slavonski Brod, Požega, Kutjevo, Virovitica, Beli Manastir, Đakovo, Vinkovci, Ilok, Našice, Slatina, RC Gradište, RC Gorice

### Središnja Hrvatska (Central)
Zagreb (Grič + Maksimir), Varaždin, Krapina, Križevci, Bjelovar, Sisak, Karlovac, Daruvar, RC Bilogora, Štrigova, Koprivnica, Čakovec, Glina, Pokupsko, Novska

### Gorska Hrvatska (Mountain)
Gospić, Ogulin, Zavižan, Parg-Čabar, Crni Lug - NP Risnjak, RC Puntijarka, Otočac, Ličko Lešće, Delnice, Udbina, Slunj, NP Plitvička jezera

### Sjeverni Jadran (Northern Adriatic)
Rijeka, Senj, Crikvenica, Mali Lošinj, Opatija, Malinska, Rab, Krk, Pag, Most Krk, Hreljin, Maslenica

### Istra
Pazin, Pula-aerodrom, Poreč, Rovinj, Bosiljevo

### Dalmacija
Split (Marjan + aerodrom), Dubrovnik, Zadar, Šibenik, Knin, Hvar, Makarska, Komiža, Lastovo, Ploče, Korčula, Sinj, Imotski, Metković, Nin, Cavtat, Orebić, Vela Luka, Palagruža

---

## River Stations (19 gauges)

| Gauge | River | Basin |
|---|---|---|
| Donji Miholjac | Drava | Drava |
| Batina | Dunav | Dunav |
| Vukovar | Dunav | Dunav |
| Ilok most | Dunav | Dunav |
| Bregana-remont | Bregana | Sava |
| Samobor | Gradna | Sava |
| Bračak | Krapina | Sava |
| Luketići | Korana | Sava |
| Jarče Polje | Donja Dobra | Sava |
| Zamost 2 | Čabranka | Kvarner |
| Kozjak most | Kozjak jezero | Plitvice |
| Portonski most | Mirna | Istra |
| Izvor Rječine | Rječina | Kvarner |
| Prevjes | Zrmanja | Zadar |
| Krupa | Krupa | Zadar |
| Roški slap | Krka | Šibenik |
| Nacionalni park | Krka | Šibenik |
| Dusina | Matica Vrgorska | Dalmacija |
| Metković | Neretva | Dalmacija |

---

## Climate Cities (23 available)

bjelovar, dubrovnik, gospic, hvar, karlovac, knin, krizevci, mali_losinj, ogulin, osijek, parg, pazin, rijeka, senj, sisak, slavonski_brod, split_marjan, sibenik, varazdin, zadar, zagreb_gric, zagreb_maksimir, zavizan

Data spans **1899–2024** (125+ years) for most stations.

---

## Sea Temperature Stations (Adriatic)

Božava, Crikvenica, Dubrovnik, Hvar, Komiža, Mali Lošinj, Malinska, Mljet (Malo jezero, Veliko jezero, otvoreno more), Opatija, Pula, Rab, Rovinj-Sv.Ivan, Split, Šibenik, Zadar

---

## Notes

- The `dhmz.py` script uses **fuzzy matching** — typing "Zagreb" will match "Zagreb-Grič" in current, "Zagreb_Maksimir" in forecast
- Forecast feeds use underscores (`Slavonski_Brod`), current feeds use spaces/dashes (`Slavonski Brod`)
- Some stations only appear in certain feeds (e.g., lighthouses `Porer`, `Sv. Ivan`, `Veli Rat` only in current)
- Climate feed uses lowercase without accents (`gospic` not `Gospić`)
