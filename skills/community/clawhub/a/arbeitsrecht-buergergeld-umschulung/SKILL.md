---
name: arbeitsrecht-buergergeld-umschulung
description: |
  Deutschsprachiger KI-Assistent für deutsches Arbeitsrecht, Bürgergeld (SGB II/XII) und berufliche Umschulung.
  Hilft bei Jobcenter-Konflikten (Widerspruch, Sanktionen, Fristen), Bildungsgutschein/AVGS-Anspruch (§81 SGB III),
  Umschulungsvoraussetzungen und Bürgergeld-Rechten. Referenziert konkrete Paragraphen (SGB II, III, X, ArbGG),
  BSG/LSG-Urteile und aktuelle Gesetzesstände. Erstellt handlungsorientierte Musterschreiben und Eskalationspfade
  (VdK, SoVD, Fachanwälte). Trennt klar zwischen gesichertem Recht, Jobcenter-Praxis und persönlicher Einschätzung.
  Use when: Jobcenter-Konflikt, Widerspruch, Sanktion, Bürgergeld-Antrag, Umschulung, Bildungsgutschein, AVGS,
  §81 SGB III, SGB II, SGB III, SGB X, ArbGG, Sozialgericht, Widerspruchsfrist, Eingliederungsvereinbarung,
  Maßnahmen, Berufsausbildung, Förderung, Rechtsbehelf, Untätigkeitsklage, Untätigkeit, Verzögerung, Nachforderung.
---

# Arbeitsrecht, Bürgergeld & Umschulung

## Wann diese Skill verwenden

- Nutzer fragt nach Rechten gegenüber dem Jobcenter (Bürgergeld, Sanktionen, Maßnahmen)
- Konflikte mit dem Jobcenter: Widerspruch, Klage, Fristen, Eingliederungsvereinbarung
- Fragen zu Bildungsgutschein (AVGS), §81 SGB III, Umschulungsvoraussetzungen
- Bedarf an Musterschreiben (Widerspruch, Antrag, Beschwerde)
- Unklarheit über gesetzliche Grundlagen (SGB II, III, X, ArbGG)
- Suche nach BSG/LSG-Urteilen oder Eskalationspfaden (VdK, SoVD, Anwälte)
- **Bürgergeld-Antrag nach Umzug** bei kommunalem Jobcenter mit Verzögerungen (>6 Wochen)
- **Untätigkeit des Jobcenters** - Entscheidung ausstehend, Antragsbearbeitung stockt
- **Wiederholte Nachforderungen** von Unterlagen als Verfahrenstaktik

## Wann diese Skill NICHT verwenden

- Allgemeine Karriereberatung ohne rechtlichen Bezug
- Steuerrechtliche Fragen (nicht SGB-bezogen)
- Unternehmensgründungsberatung ohne Fördermittelbezug
- Internationales Arbeitsrecht (außerhalb deutscher Jurisdiktion)

## Benötigte Eingaben vom Nutzer

- Konkrete Situation oder Fragestellung
- Betroffene Paragraphen oder Bescheide (falls bekannt)
- Zeitliche Fristen (Widerspruchsfrist: 1 Monat nach Bescheid)
- Art des Konflikts (Sanktion, Ablehnung, Eingliederungsvereinbarung)
- Gewünschter Ausgang (Widerspruch, Klage, Einigung)

## Workflow

### 1. Situation analysieren

- Frage des Nutzers in rechtliche Kategorien einordnen (SGB II, III, X, ArbGG)
- Relevante Paragraphen identifizieren und zitieren
- Fristen prüfen (Widerspruchsfrist: 1 Monat nach Bescheid gem. §84 SGG)
- **Bei Untätigkeit/Verzögerung:** Verzögerungsdauer feststellen
  - <6 Wochen: Fristsetzung, Eskalation
  - 4-6 Wochen: Dienstaufsicht, Nachforderungs-Abwehr
  - 3 Monate: Untätigkeitsklage ankündigen
  - 6 Monate: Untätigkeitsklage (§88 SGG)
  - Akute Not (Wohnungsverlust, Mittellosigkeit): §86b SGG sofort

### 2. Rechtsgrundlagen recherchieren

- Gesetze: `references/gesetze.md` für Paragraphen-Referenz
- Urteile: `references/urteile.md` für BSG/LSG-Entscheidungen
- Quellen: gesetze-im-internet.de, bmas.de, BSG-Datenbank

**Relevante Paragraphen bei Untätigkeit:**
| Paragraph | Thema | Einsetzbar nach |
|-----------|-------|-----------------|
| §86b SGG | Einstweiliger Rechtsschutz | **Sofort** bei akuter Notlage |
| §42 SGB I | Vorschuss/ Vorausleistung | Sofort bei dringendem Bedarf |
| §24 SGB X | Amtsermittlung | Gegen übermäßige Nachforderungen |
| §17 SGB X | Grundsatz der Untersuchung | Von Amts wegen zu ermitteln |
| §88 SGG | Untätigkeitsklage | **6 Monate** bei Antrag |

### 3. Handlungsoptionen aufzeigen

- Sofortmaßnahmen (Widerspruch einlegen, Fristen wahren)
- Eskalationspfade (VdK, SoVD, Fachanwalt für Sozialrecht)
- Musterschreiben aus `assets/musterschreiben/` anpassen

**Eskalationsstufen bei Untätigkeit:**
| Stufe | Maßnahme | Zeitpunkt |
|-------|----------|-----------|
| 1 | Sachbearbeiter kontaktieren, Fristsetzung (14 Tage) | 0-2 Wochen |
| 2 | Teamleiter/Gruppenleiter einschalten | 2-4 Wochen |
| 3 | Dienstaufsichtsbeschwerde + §86b SGG prüfen (akute Not!) | 4-6 Wochen |
| 4 | Untätigkeitsklage ankündigen | 3 Monate |
| 5 | Untätigkeitsklage (§88 SGG) einreichen | 6 Monate |

### 4. Rechtliche Einordnung kommunizieren

**Drei-Kategorien-Trennung:**
1. **Gesichertes Recht:** Gesetzestext, bindende Urteile
2. **Jobcenter-Praxis:** Übliche Verfahrensweise, Ermessensspielraum
3. **Persönliche Einschätzung:** Bewertung der Erfolgsaussichten

### 5. Nächste Schritte definieren

- Konkrete Handlungsanweisung mit Fristen
- Musterschreiben bereitstellen
- Bei Bedarf: Übergabe an Fachanwalt oder Sozialverband

## Referenzdateien

| Datei | Wann lesen |
|-------|------------|
| [`references/gesetze.md`](references/gesetze.md) | Für Paragraphen-Referenz (SGB II, III, X, ArbGG) |
| [`references/urteile.md`](references/urteile.md) | Für BSG/LSG-Entscheidungen und Präzedenzfälle |
| [`references/eskalation.md`](references/eskalation.md) | Für VdK, SoVD, Anwaltskontakte, Beschwerdewege |

## Musterschreiben

| Datei | Verwendung |
|-------|------------|
| [`assets/musterschreiben/widerspruch-bescheid.md`](assets/musterschreiben/widerspruch-bescheid.md) | Widerspruch gegen Jobcenter-Bescheid |
| [`assets/musterschreiben/antrag-bildungsgutschein.md`](assets/musterschreiben/antrag-bildungsgutschein.md) | Antrag auf Bildungsgutschein/AVGS |
| [`assets/musterschreiben/widerspruch-sanktion.md`](assets/musterschreiben/widerspruch-sanktion.md) | Widerspruch gegen Sanktion (§31 SGB II) |
| [`assets/musterschreiben/fristsetzung-untaetigkeit.md`](assets/musterschreiben/fristsetzung-untaetigkeit.md) | Fristsetzung bei Antragsverzögerung |
| [`assets/musterschreiben/nachforderungs-abwehr.md`](assets/musterschreiben/nachforderungs-abwehr.md) | Antwort auf übermäßige Nachforderungen (§24 SGB X) |
| [`assets/musterschreiben/dienstaufsichtsbeschwerde.md`](assets/musterschreiben/dienstaufsichtsbeschwerde.md) | Beschwerde über Verfahrensverzögerung |
| [`assets/musterschreiben/eilantrag-86b-sGG.md`](assets/musterschreiben/eilantrag-86b-sGG.md) | Einstweiliger Rechtsschutz bei akuter Notlage |
| [`assets/musterschreiben/untaetigkeitsklage-88-sGG.md`](assets/musterschreiben/untaetigkeitsklage-88-sGG.md) | Untätigkeitsklage nach 6 Monaten |

## Beispiele

### Beispiel 1: Sanktion widersprechen

**Nutzer:** "Das Jobcenter hat mir eine Minderung von 30% wegen versäumten Termins gegeben. Was kann ich tun?"

**Antwort-Struktur:**
1. **Rechtsgrundlage:** §31 SGB II (Pflichtverletzungen), §31a SGB II (Minderungsbeträge)
2. **Frist:** Widerspruch innerhalb 1 Monat nach Bescheid (§84 SGG)
3. **Musterschreiben:** `assets/musterschreiben/widerspruch-sanktion.md`
4. **Eskalation:** Bei Ablehnung → Sozialgericht, VdK/SoVD-Unterstützung
5. **Trennung:** Gesichertes Recht (§31 SGB II) vs. Jobcenter-Praxis (Ermessen bei "wichtigem Grund")

### Beispiel 2: Bildungsgutschein beantragen

**Nutzer:** "Ich möchte eine Umschulung zur Fachinformatikerin machen. Wie bekomme ich einen Bildungsgutschein?"

**Antwort-Struktur:**
1. **Rechtsgrundlage:** §81 SGB III (Bildungsgutschein), §77 ff. SGB III (Förderung der Berufsausbildung)
2. **Voraussetzungen:** Förderbedürftigkeit, Eignung, Notwendigkeit der Maßnahme
3. **Musterschreiben:** `assets/musterschreiben/antrag-bildungsgutschein.md`
4. **Eskalation:** Bei Ablehnung → Widerspruch, BSG-Urteile zur AVGS-Förderung
5. **Trennung:** Gesetzlicher Anspruch (§81 SGB III) vs. Jobcenter-Ermessen (Auswahl der Maßnahme)

### Beispiel 3: Untätigkeit bei Bürgergeld-Antrag (nach Umzug)

**Nutzer:** "Ich habe Probleme bei der Bürgergeld-Antragung nach meinem Umzug. Das kommunale Jobcenter fordert ständig Unterlagen nach und bummelt seit über 6 Wochen."

**Antwort-Struktur:**
1. **Verzögerungsdauer prüfen:** 6 Wochen festgestellt → Stufe 3 (Dienstaufsicht + §86b SGG prüfen)
2. **Akute Notlage prüfen:** Wenn Wohnungsverlust/Mittellosigkeit → §86b SGG sofort
3. **Rechtsgrundlagen:** §24 SGB X (Amtsermittlung), §17 SGB X (Von Amts wegen), §42 SGB I (Vorschuss)
4. **Musterschreiben:** `assets/musterschreiben/fristsetzung-untaetigkeit.md` + `assets/musterschreiben/nachforderungs-abwehr.md`
5. **Eskalation:** Dienstaufsichtsbeschwerde einreichen, bei akuter Not → Eilantrag (§86b SGG)
6. **Perspektive:** Untätigkeitsklage (§88 SGG) erst nach 6 Monaten möglich

## Quellen-Priorisierung

1. **Primärquellen:** gesetze-im-internet.de, bmas.de, BSG-Urteile
2. **Sekundärquellen:** Fachaufsätze, Sozialverbände (VdK, SoVD)
3. **Praxisquellen:** Foren (buergergeld.de, arbeitsrecht.de), Erfahrungsberichte

## Fristen-Übersicht

| Frist | Rechtsgrundlage | Hinweis |
|-------|-----------------|---------|
| Widerspruch gegen Bescheid | §84 SGG | 1 Monat nach Zustellung |
| Klage vor Sozialgericht | §92 SGG | 1 Monat nach Widerspruchsbescheid |
| Untätigkeitsklage (Antrag) | §88 SGG | Nach **6 Monaten** ohne Entscheidung |
| Untätigkeitsklage (Widerspruch) | §88 SGG | Nach **3 Monaten** ohne Entscheidung |
| Einstweiliger Rechtsschutz | §86b SGG | **Sofort** bei akuter Notlage (Wohnungsverlust, Mittellosigkeit) |
| Gehörsrüge | §142 SGG | Innerhalb 1 Jahres nach Rechtskraft |
| Vorschuss/Akkzessorische Leistung | §42 SGB I | Bei dringendem Bedarf, einkommensunabhängig |

## Troubleshooting

### Problem: Frist abgelaufen

- **Lösung:** Wiedereinsetzung in den vorigen Stand beantragen (§67 SGG)
- **Voraussetzung:** Glaubhaft machen, dass Frist ohne Verschäumen nicht versäumt wurde

### Problem: Jobcenter reagiert nicht (Untätigkeit)

**Nach Verzögerungsdauer unterscheiden:**

| Dauer | Lösung | Rechtsgrundlage |
|-------|--------|-----------------|
| 0-4 Wochen | Fristsetzung (14 Tage) | Allgemeines Verwaltungsrecht |
| 4-6 Wochen | Dienstaufsichtsbeschwerde + Nachforderungs-Abwehr | §24 SGB X, §17 SGB X |
| 3 Monate | Untätigkeitsklage ankündigen | §88 SGG (Vorbereitung) |
| 6 Monate | Untätigkeitsklage einreichen | §88 SGG |
| Akute Not | Eilantrag + Vorschuss | §86b SGG, §42 SGB I |

**Alternative:** Dienstaufsichtsbeschwerde (keine Frist, aber keine Rechtswirkung)

### Problem: Sanktion droht

- **Lösung:** Vorläufigen Rechtsschutz beantragen (§86b SGG)
- **Voraussetzung:** Eilbedürftigkeit, schwere finanzielle Beeinträchtigung

### Problem: Ständige Nachforderungen von Unterlagen

- **Lösung:** Nachforderungs-Abwehr-Schreiben (§24 SGB X - Amtsermittlung)
- **Rechtsgrundlage:** Jobcenter muss von Amts wegen ermitteln (§17 SGB X), nicht nur Nachforderungen stellen
- **Musterschreiben:** `assets/musterschreiben/nachforderungs-abwehr.md`

## Sicherheitshinweise

- **Keine Rechtsberatung:** Diese Skill ersetzt keine anwaltliche Beratung
- **Aktualität prüfen:** Gesetze und Urteile können sich ändern
- **Einzelfallprüfung:** Jeder Fall ist individuell zu bewerten
- **Dokumentation:** Alle Schritte und Fristen schriftlich festhalten