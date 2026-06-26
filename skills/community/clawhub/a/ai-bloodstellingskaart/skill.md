# AI Blootstellingskaart Nederland

Check de AI-impact op elk Nederlands beroep via een gratis API.

## Wat het doet

Deze skill geeft toegang tot de AI Blootstellingskaart: 103 Nederlandse beroepsgroepen (CBS BRC 2014) met AI-scores, prognose 2030, salaris, career advice en concrete AI-tools.

## API

**Alle beroepen ophalen:**
```
GET https://simondjanssen.nl/api/beroep
```

**Eén beroep opzoeken (fuzzy matching):**
```
GET https://simondjanssen.nl/api/beroep?naam=verpleegkundige
```

## Response voorbeeld

```json
{
  "name": "Verpleegkundigen MBO",
  "sector": "Zorg en welzijn",
  "ai_score": 2,
  "vulnerability": 3,
  "jobs": 192000,
  "salary": 36000,
  "forecast_2030": {
    "trend": "sterke groei",
    "range_low": 12,
    "range_high": 23,
    "risk_label": "Laag"
  },
  "career_advice": {
    "type": "veilig",
    "title": "Veilig beroep",
    "summary": "..."
  },
  "tools": ["Epic ECD", "Chipsoft HiX", "Woebot AI"],
  "source": "AI Blootstellingskaart — simondjanssen.nl/ai-kaart",
  "license": "CC BY 4.0"
}
```

## Voorbeeldvragen

- "Wat is de AI-impact op mijn beroep als verpleegkundige?"
- "Welke beroepen zijn het meest kwetsbaar voor AI?"
- "Wat is de prognose 2030 voor developers?"
- "Welk salaris hoort bij een administratief medewerker?"

## Data

- 103 CBS BRC 2014 beroepsgroepen
- 5,8 miljoen banen (~60% werkzame bevolking)
- AI-scores: LLM-schattingen, cross-gevalideerd met Felten et al., OECD, WEF
- Prognose 2030: momentum + AI-disruptie × NL-kwetsbaarheid

## Auteur

Simon Janssen — CTO bij HappyNurse, Advisory Board CIONET Nederland.

- Site: https://simondjanssen.nl
- Kaart: https://simondjanssen.nl/ai-kaart
- Methodologie: https://simondjanssen.nl/ai-kaart/methodologie
- LinkedIn: https://linkedin.com/in/simondjanssen

## Licentie

CC BY 4.0 — Vrij te gebruiken met bronvermelding.
