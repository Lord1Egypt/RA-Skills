# Amazon Product Advertising API (PA API) Skill

## Was ist das?
Die offizielle Amazon API für Produktinformationen, Preise, Bilder, Bewertungen.

## Voraussetzungen
1. Amazon Associates Konto (kostenlos)
2. Access Key + Secret Key
3. Partner Tag (Associates ID)

## Limits
- 1 Request/Sec (throttled)
- 8640 Requests/Tag (im Verdienstprogramm)
- 1 Request/5 Sec (ohne Verdienst)

## Kosten
Kostenlos, aber braucht Amazon Associates Konto.

## Setup
1. Bei https://affiliate-program.amazon.de/ anmelden
2. Zu "Produktwerbung-API" navigigieren
3. Credentials generieren
4. In `.env` speichern:
   ```
   AMAZON_ACCESS_KEY=AKIA...
   AMAZON_SECRET_KEY=...
   AMAZON_PARTNER_TAG=jensbuermann-21
   ```
