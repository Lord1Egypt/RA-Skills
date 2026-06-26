# Microsoft Tech Community – Kategorien

Die RSS-URLs folgen dem Pattern:
```
https://techcommunity.microsoft.com/plugins/custom/microsoft/microsoft/page_news_rss?category=<CATEGORY>
```

## Verifizierte Kategorien (Stand 2026-06-07)

| Kategorie | URL | Themen |
|---|---|---|
| BusinessCentral | `category=BusinessCentral` | BC, AL, ERP |
| MicrosoftFabric | `category=MicrosoftFabric` | Fabric, Data, Synapse-Nachfolger |
| PowerBI | `category=PowerBI` | Power BI, DAX, Berichte |
| AzureDataFactory | `category=AzureDataFactory` | ADF, ETL, Data Integration |
| Azure | `category=Azure` | Allgemein Azure |
| AI | `category=AI` | Azure AI, Cognitive Services |
| MicrosoftCopilot | `category=MicrosoftCopilot` | Copilot-News |

## Eine Kategorie testen

```bash
curl -s "https://techcommunity.microsoft.com/plugins/custom/microsoft/microsoft/page_news_rss?category=BusinessCentral" | head -30
```

Wenn `<rss>` und `<item>`-Tags zurückkommen, passt der Kategoriename.

## Vollständige Liste?

Die offizielle Liste ist schwer zu finden (dynamisch generiert).
Workaround: Besuche `https://techcommunity.microsoft.com/category/<...>/posts` und schau in der URL.
