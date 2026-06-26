---
name: amazon-paapi
description: Official Amazon PA API for product info, prices, and reviews
version: 1.0.0
author: unknown
tags: [amazon, api, ecommerce, products, pricing, pa-api]
created: 2026-05-16
updated: 2026-05-16
---

# Amazon Product Advertising API (PA API) Skill

## Description
Offizielle Amazon API für Produktinformationen, Preise und Bewertungen.

## Commands

### Produktinformationen abrufen
```bash
ama-api B0BQXKDZGK
```

### ASIN zum Tracker hinzufügen
```bash
ama B0BQXKDZGK
```

### Alle Produkte anzeigen
```bash
ama --list
```

## Setup

### 1. Amazon Associates Konto erstellen
- Website: https://affiliate-program.amazon.de/
- Kostenlos registrieren
- Website/App angeben (kann auch ein Blog/Social Media sein)

### 2. PA API Zugriff aktivieren
- Im Associates Dashboard: "Tools" → "Product Advertising API"
- Credentials generieren
- Access Key + Secret Key kopieren

### 3. Credentials speichern
```bash
echo 'AMAZON_ACCESS_KEY=AKIA...' >> ~/.env
echo 'AMAZON_SECRET_KEY=...' >> ~/.env
echo 'AMAZON_PARTNER_TAG=deinname-21' >> ~/.env
```

## Limits
- **1 Request/Sec** (throttled)
- **8640 Requests/Tag** (mit Verdienst)
- **1 Request/5 Sec** (ohne Verdienst)

## Output Beispiel
```
✅ Produkt gefunden!
Titel: Samsung The Frame 55 Zoll QLED 4K
Preis: €1.199,00
Bewertung: 4.5 von 5 Sternen
URL: https://www.amazon.de/dp/B0BQXKDZGK
```

## Notes
- API ist kostenlos
- Braucht aktives Associates Konto
- Bei Inaktivität (keine Verkäufe 180 Tage) kann API deaktiviert werden
