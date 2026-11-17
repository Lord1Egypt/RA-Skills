# BMW K1200RS Repair Assistant

BMW K1200RS Repair Assistant on professionaalne ClawHub/Codex skill AI-juhitud mootorratta remondiloogika jaoks. See aitab assistendil tegutseda ettevaatliku töökoja abilisena BMW K1200RS diagnostikas, hoolduse planeerimises, remondimanuaali kontrollimises ja tööjärgses verifitseerimises.

Repo ei sisalda BMW remondimanuaali. Kasutaja peab tehase protseduuride, momentide, elektriskeemide, kulumispiiride ja ametlike spetsifikatsioonide jaoks lisama või viitama enda legaalselt hangitud BMW Repair Manual PDF-ile.

## Funktsioonid

- BMW K1200RS sümptomite struktureeritud kogumine ja täpsustavad küsimused.
- Ohutus-esmane diagnostikavoog elektri, kütuse, süüte, jahutuse, pidurite, ABS-i, jõuülekande, vedrustuse ja juhtseadmete jaoks.
- Remondimanuaalile toetuv töö planeerimine ilma autoriõigusega kaitstud manuaalisisu reprodutseerimata.
- Tõenäoliste põhjuste järjestamine koos praktiliste kontrollide ja verifitseerimissammudega.
- Selged piirid ohutuskriitilise töö, teekõlblikkuse ja professionaalse mehaaniku kaasamise jaoks.

## Paigaldus

Paigalda skill ClawHubist:

```bash
clawhub install bmw-k1200rs-repair-assistant
```

Või paigalda lokaalsest checkout'ist:

```bash
clawhub install ./bmw-k1200rs-repair-assistant
```

## Kasutamine

Näidispäringud:

```text
Use BMW K1200RS Repair Assistant. My 2002 K1200RS cranks but will not start after winter storage.
```

```text
Use BMW K1200RS Repair Assistant. I have the BMW Repair Manual PDF open to the ABS bleeding section; help me build a safe checklist from this excerpt.
```

```text
Use BMW K1200RS Repair Assistant. The bike surges at steady throttle around 3,000 RPM. Ask me for the details needed to diagnose it.
```

Tehasespetsifikatsioonide puhul kleebi lühike asjakohane väljavõte või anna lehekülje/peatüki märge enda legaalselt hangitud BMW Repair Manual PDF-ist. Assistent saab seejärel aidata infot tõlgendada ja muuta selle ohutuks tööchecklist'iks.

## Piirangud

- Ei sisalda BMW tehase remondimanuaali, autoriõigusega kaitstud skeeme, momenditabeleid, elektriskeeme ega hooldusgraafikuid.
- Ei asenda kvalifitseeritud mootorrattamehaanikut.
- Ei kinnita, et remont on ohutu või sõiduk teekõlblik.
- Ei tohi kasutada ohutussüsteemide, heitmesüsteemide, immobilaiseri, seadusenõuete või ülevaatusreeglite eiramiseks.
- Nõuab, et kasutaja kontrolliks ametlikud väärtused ja protseduurid enda legaalselt hangitud BMW Repair Manual PDF-ist.

## Märkus BMW Repair Manual PDF-i kohta

Kasutaja peab lisama või viitama enda legaalselt hangitud BMW Repair Manual PDF-ile väljaspool seda repot. Ära commiti PDF-i, kopeeritud peatükke, skaneeritud lehti, elektriskeeme ega BMW omanduslikke tabeleid sellesse reposse.

## Litsents

MIT. Vaata [LICENSE](LICENSE).
