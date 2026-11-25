# Denote Top Ads

Finde beliebte, aufstrebende und neu entdeckte Anzeigen für Spiele und Utility-Apps und wähle Motive für deinen nächsten Kampagnentest aus.

[EN](README.md) · [ZH](README.zh.md) · [JA](README.ja.md) · [KO](README.ko.md) · [ES](README.es.md) · [NL](README.nl.md) · DE · [FR](README.fr.md)

Denote erfasst und aktualisiert täglich Werbedaten zu Spielen und Utility-Apps. Jeder Erfassungslauf umfasst mehr als 60 Millionen Anzeigendatensätze. Die Ranglisten werden einmal pro Woche erstellt. Mit einem kostenlosen Konto erhältst du für die letzte abgeschlossene Woche drei Ranglisten für Spiele oder Apps mit jeweils bis zu zehn Anzeigen. [Denote Top Ads entdecken](https://denote.net/top-ads).

| Kostenlose Rangliste | Was du darin findest |
| --- | --- |
| Beliebte Anzeigen | Anzeigen, die in der vergangenen Woche besonders viel Aufmerksamkeit erhielten. |
| Aufsteiger | Anzeigen, deren Beliebtheit gegenüber der Vorwoche am stärksten zunahm. |
| Neue Anzeigen | Erstmals erfasste Anzeigen, sortiert nach ihrer anfänglichen Beliebtheit. |

## Deinen ersten Wochenüberblick abrufen

Führe diesen Befehl in deinem OpenClaw-Arbeitsbereich aus. Du benötigst Python 3.

```sh
git clone https://github.com/denote-developer/denote-top-ads.git skills/denote-top-ads
```

1. Öffne eine neue Sitzung und frage: „Welche Anzeigen kann ich mit Denote entdecken?“
2. [Kostenloses Denote-Konto erstellen](https://denote.net/user/register). Wenn du schon ein Konto hast, melde dich an. Erstelle einen Denote-API-Schlüssel mit der Berechtigung `top_ads:read` oder füge sie einem vorhandenen Schlüssel hinzu.
3. Speichere den Schlüssel in der Geheimnisverwaltung deines Agenten als `DENOTE_API_KEY`. Bitte ihn dann: „Zeig mir die App-Anzeigen der letzten Woche.“ Du erhältst alle drei Ranglisten. Ohne Kategorieangabe werden Spiele ausgewählt.

Im Chat erscheinen die ersten drei Anzeigen jeder Rangliste mit Medienlink und Laufzeit. Beliebte und neue Anzeigen zeigen den Wochenwert, Aufsteiger den Zuwachs und die Wachstumsrate. Der lokale Bericht am Ende der Antwort enthält alle Ergebnisse. Eine Karte öffnet das Video sowie Übersicht, Verlauf, ähnliche Anzeigen und Zielgruppe. Auch bei fehlenden Details führt die Schaltfläche zur passenden Rangliste im Denote-Arbeitsbereich.

## Eine Anzeige im Detail ansehen

Frage zum Beispiel: „Öffne den zweiten Platz der Aufsteiger.“ Mit Top Ads Pro oder Business kannst du verfügbare Daten zur Anzeigenleistung und Zielgruppe ansehen. Alle drei Wochenranglisten sind kostenlos.

## Produktansichten

[![Über die linke Seitenleiste lassen sich alle drei Wochenranglisten öffnen.](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/top-ads-navigation.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/top-ads-navigation.jpg)

*Über die linke Seitenleiste lassen sich alle drei Wochenranglisten öffnen.*

[![Beliebte Spieleanzeigen vom 9. bis 15. November 2026, sortiert nach ihrer Beliebtheit in dieser Woche.](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/trending-ads.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/trending-ads.jpg)

*Beliebte Spieleanzeigen vom 9. bis 15. November 2026, sortiert nach ihrer Beliebtheit in dieser Woche.*

[![Spieleanzeigen mit dem größten Zuwachs an Beliebtheit gegenüber der Vorwoche.](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/rising-ads.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/rising-ads.jpg)

*Spieleanzeigen mit dem größten Zuwachs an Beliebtheit gegenüber der Vorwoche.*

[![Neu erfasste Spieleanzeigen, sortiert nach ihrer anfänglichen Beliebtheit.](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/new-ads.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/new-ads.jpg)

*Neu erfasste Spieleanzeigen, sortiert nach ihrer anfänglichen Beliebtheit.*

[![Überblick zur Anzeige von Vita Mahjong mit Format und geschätzten Impressionen.](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/overview.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/overview.jpg)

*Überblick zur Anzeige von Vita Mahjong mit Format und geschätzten Impressionen.*

[![Täglicher Anzeigenwert von Vita Mahjong im Vergleich zu den Referenzlinien.](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/data-trend.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/data-trend.jpg)

*Täglicher Anzeigenwert von Vita Mahjong im Vergleich zu den Referenzlinien.*

[![Weitere Anzeigen mit demselben Motiv, den jeweiligen Werbetreibenden und der Laufzeit.](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/related-ads.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/related-ads.jpg)

*Weitere Anzeigen mit demselben Motiv, den jeweiligen Werbetreibenden und der Laufzeit.*

[![Reichweite von Vita Mahjong nach Land, Alter und Geschlecht.](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/audience.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/audience.jpg)

*Reichweite von Vita Mahjong nach Land, Alter und Geschlecht.*
