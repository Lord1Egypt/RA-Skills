# YouTube-Channel-ID finden

RSS-Feeds für YouTube-Kanäle brauchen die 24-stellige Channel-ID (`UC...`).
Diese steht **nicht** im @-Handle. So findest du sie:

## Methode 1: Über die Kanal-Seite

1. Öffne `https://www.youtube.com/@<handle>` (z.B. `@msdyn365`)
2. Drücke `Ctrl+U` (Quelltext anzeigen)
3. Suche nach `"externalId":"UC..."` (Strg+F)
4. Die 24-stellige ID ist der Treffer

## Methode 2: Über ein Video

1. Öffne irgendein Video des Kanals
2. Klicke auf den Kanal-Namen unter dem Video
3. Folge Methode 1 ab Schritt 2

## Methode 3: API (schneller, braucht API-Key)

```bash
# Über die YouTube Data API
curl "https://www.googleapis.com/youtube/v3/channels?part=id&forUsername=msdyn365&key=YOUR_KEY"
```

## RSS-URL-Format

Sobald du die ID hast:

```
https://www.youtube.com/feeds/videos.xml?channel_id=UCxxxxxxxxxxxxxxxxxxxxxx
```

## Test

```bash
# Prüfe ob der Feed liefert
curl -s "https://www.youtube.com/feeds/videos.xml?channel_id=UC..." | head -50
```

Wenn du `<feed>` und `<entry>`-Tags siehst, passt es.

## Empfohlene Kanäle für BC / Fabric / Power BI

| Thema | Kanal | Wie finden |
|---|---|---|
| BC / Dynamics 365 | Suche nach "Microsoft Dynamics 365" | youtube.com/@MicrosoftDynamics365 |
| Microsoft Fabric | Suche nach "Microsoft Fabric" | youtube.com/@MicrosoftFabric |
| Power BI | Suche nach "Microsoft Power BI" | youtube.com/@MSPowerBI |
| AL-Entwicklung | Suche nach "waldo" oder "berndly" | BC-Community-Kanäle |

> **Tipp:** Du musst die Kanal-IDs nicht selbst rausfinden — `feeds-digest --discover-youtube "msdyn365"` (geplant für Phase 4) wird das per API übernehmen.
