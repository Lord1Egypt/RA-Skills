---
name: Barcelona
slug: barcelona
version: 1.0.0
description: Navigate Barcelona as visitor, resident, tech worker, student, or entrepreneur with neighborhoods, transport, costs, safety, and local insights.
metadata: {"clawdbot":{"emoji":"🏖️","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

## When to Use

User asks about Barcelona for any purpose: visiting, moving, working, studying, or starting a business. Agent provides practical guidance with current data.

## Quick Reference

| Topic | File |
|-------|------|
| **Visitors** | |
| Attractions (must-see vs skip) | `visitor-attractions.md` |
| Itineraries (1/3/7 days) | `visitor-itineraries.md` |
| Where to stay | `visitor-lodging.md` |
| Tips & day trips | `visitor-tips.md` |
| **Neighborhoods** | |
| Quick comparison | `neighborhoods-index.md` |
| Central (Gòtic, Raval, Born) | `neighborhoods-central.md` |
| Uptown (Eixample, Gràcia) | `neighborhoods-uptown.md` |
| Beach (Barceloneta, Poblenou) | `neighborhoods-beach.md` |
| Outer (Sant Andreu, Horta) | `neighborhoods-outer.md` |
| Choosing guide | `neighborhoods-choosing.md` |
| **Food** | |
| Overview & restaurants | `food-overview.md` |
| Traditional Catalan | `food-traditional.md` |
| Markets | `food-markets.md` |
| Best areas | `food-areas.md` |
| Dietary & tips | `food-practical.md` |
| **Practical** | |
| Moving & settling | `resident.md` |
| Transport | `transport.md` |
| Cost of living | `cost.md` |
| Safety | `safety.md` |
| Weather | `climate.md` |
| Local services | `local.md` |
| **Career** | |
| Tech industry | `tech.md` |
| Students | `student.md` |
| Startups | `startup.md` |

## Core Rules

### 1. Identify User Context First
- **Role**: Tourist, resident, tech worker, student, entrepreneur
- **Timeline**: Short visit, planning to move, already there
- Load relevant auxiliary file for details

### 2. Safety Context
Barcelona is generally safe but has Europe's highest pickpocketing rate. Main concerns:
- Pickpocketing (Las Ramblas, metro, beaches, Barri Gòtic)
- Phone snatching (tourists with phones visible)
- Apartment scams (online rentals)
- Beach theft (leaving belongings unattended)
See `safety.md` for area-specific guidance.

### 3. Weather Expectations
- Mediterranean climate — mild winters, hot summers
- Summer: Hot (28-32°C) with humidity
- Winter: Mild (10-15°C), rarely below 5°C
- Best months: May-June, September-October
- Beach season: June-September (water warm enough)

### 4. Current Data (Feb 2026)

| Item | Range |
|------|-------|
| 1BR rent | €1,200-1,800 (central), €900-1,400 (outer) |
| Senior SWE salary | €50K-80K total comp |
| Student budget | €1,000-1,400/month |
| T-usual (monthly pass) | €22.80 (Zone 1) |

### 5. Tourist Traps
- Skip: Las Ramblas restaurants (overpriced), Barceloneta beachfront restaurants
- Do: El Born neighborhood, Gràcia's Plaça del Sol, Poblenou
- Watch: Pickpockets everywhere in Ciutat Vella
- Free: Park Güell free zone, beaches, Bunkers del Carmel sunset

### 6. Transit Over Driving
- Metro + bus + FGC covers everything
- T-Casual (10 trips) for visitors
- Bicing for residents
- ZBE (Low Emission Zone) makes driving complicated

### 7. Neighborhood Matching

| Profile | Best Areas |
|---------|------------|
| Young professionals | Gràcia, Poblenou, Sant Antoni |
| Families | Sarrià, Les Corts, Horta |
| Budget-conscious | Sant Andreu, Nou Barris, Sants |
| Tech workers | Poblenou (22@), Eixample, Gràcia |
| Beach lifestyle | Barceloneta, Poblenou, Vila Olímpica |

## Language Context

### Catalan vs Spanish (Castellano)

Barcelona is bilingual. Understanding this is essential:

| Situation | Language Used |
|-----------|---------------|
| Street signs | Catalan |
| Official documents | Catalan (with Spanish option) |
| Daily conversation | Both (depends on person) |
| Service industry | Spanish common, Catalan appreciated |
| Schools | Catalan primary |
| Business | Both, leaning Spanish in multinationals |

**Practical advice:**
- Speaking Spanish is fine — most locals are bilingual
- Learning basic Catalan phrases = appreciated and shows respect
- Locals will switch to Spanish if you're struggling
- Don't assume political opinions based on language preference
- Catalonia has strong regional identity — be aware but neutral

### Basic Catalan Phrases

| Catalan | Spanish | English |
|---------|---------|---------|
| Bon dia | Buenos días | Good morning |
| Gràcies | Gracias | Thank you |
| Si us plau | Por favor | Please |
| Adéu | Adiós | Goodbye |
| Quant costa? | ¿Cuánto cuesta? | How much? |

## Barcelona-Specific Traps

- **Las Ramblas dining** — Tourist trap central. Walk into side streets.
- **Barceloneta beachfront** — Overpriced, mediocre. Walk to Poblenou.
- **"Free" walking tours** — Pressure to tip €15-20.
- **Sagrada Família without booking** — 2+ hour queues. Book online.
- **Airport taxi** — Should be ~€40-45. Insist on meter.
- **Pickpockets** — Worst in Europe for tourists. Stay vigilant.
- **Fake accommodation** — Never pay before seeing. Use official platforms.
- **Beach belongings** — Never leave unattended. Thefts very common.
- **Assuming everyone speaks English** — Start with "Perdona" or "Hola".
