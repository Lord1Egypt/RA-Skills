---
name: Abfallkalender RV
description: Lade den Abfallkalender fuer den Landkreis Ravensburg ueber die offizielle Athos-Webseite herunter. Verwende diesen Skill, wenn du fuer Orte wie Ravensburg, Weingarten, Wangen im Allgaeu usw. anhand von Ort, Strasse und Hausnummer einen PDF- oder ICS-Abfallkalender holen sollst.
---

# Abfallkalender Landkreis Ravensburg

Lade Abfuhrtermine von der offiziellen Webseite des Landkreises Ravensburg herunter.
Bevorzuge `ICS`, weil ein KI-Agent das strukturierte Kalenderformat in der Regel besser weiterverarbeiten kann als ein PDF.

## Cache-Regel

- Bevorzuge fuer Agenten immer `ICS`.
- Verwende nur einen Cache, der zur exakt gleichen Adresse gehoert: gleicher Ort, gleiche Strasse, gleiche Hausnummer, gleicher Hausnummerzusatz.
- Wenn die gecachte `ICS` aelter als 7 Tage ist, ziehe immer eine frische Datei.
- Wenn bereits eine `ICS` zu einer anderen Adresse vorliegt, zaehlt sie nicht als Cache und darf nicht wiederverwendet werden.
- Fuer einen erzwungenen Frischzug `--no-cache` verwenden.

## Verwendung

```bash
# ICS herunterladen
# Das ist der bevorzugte Standardfall.
python3 ~/.openclaw/workspace/skills/abfallkalender-rv/scripts/download_waste_calendar.py \
  --city Ravensburg \
  --street Marienplatz \
  --house-number 26 \
  --format ics

# PDF herunterladen
python3 ~/.openclaw/workspace/skills/abfallkalender-rv/scripts/download_waste_calendar.py \
  --city Ravensburg \
  --street Marienplatz \
  --house-number 26 \
  --format pdf

# Zielpfad selbst setzen
python3 ~/.openclaw/workspace/skills/abfallkalender-rv/scripts/download_waste_calendar.py \
  --city Ravensburg \
  --street Marienplatz \
  --house-number 26 \
  --format ics \
  --output /tmp/abfall-ravensburg-marienplatz-26.ics
```

## Verhalten

- Das Script laeuft den echten Mehrschritt-Flow der Webseite durch.
- Es aktualisiert zuerst den Ort (`CITYCHANGED`), damit die korrekten Strassen geladen werden.
- Wenn die Seite eine separate Hausnummernauswahl liefert, waehlt das Script die passende Option aus.
- Bei unbekanntem Ort oder unbekannter Strasse bricht es mit einer klaren Fehlermeldung und Vorschlaegen ab.
- Es fuehrt einen adressgebundenen Cache unter `~/.cache/abfallkalender-rv`.
- Eine gecachte Datei wird nur wiederverwendet, wenn Adresse und Format exakt passen und die Datei nicht aelter als 7 Tage ist.
- Standardmaessig speichert es die Datei im aktuellen Verzeichnis unter dem vom Server gelieferten Dateinamen.

## Hinweise

- Verwende Orts- und Strassennamen moeglichst in der offiziellen Schreibweise der Webseite.
- Unterstuetzte Formate sind `ics` und `pdf`.
- `ics` ist das bevorzugte Format. `pdf` nur verwenden, wenn wirklich eine visuelle Kalenderansicht gebraucht wird.
- Fuer Tests oder harte Frischabfragen kann `--no-cache` genutzt werden.
- Der Skill ist rein lesend und laedt nur die Kalenderdatei herunter.
