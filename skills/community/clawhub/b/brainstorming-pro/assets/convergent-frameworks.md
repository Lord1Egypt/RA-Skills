# Konvergente Frameworks — Ideen priorisieren und auswählen

**Use:** Nach divergenter Phase. Von Quantität zu Qualität.

---

## 1. Dot-Voting

**Use:** Schnelle demokratische Priorisierung

**Ablauf:**
1. Alle Ideen sichtbar aufhängen (Wall/Board)
2. Jede Person bekommt 3-5 Klebepunkte
3. Punkte verteilen (alle auf eine oder streuen)
4. Top 5-10 zählen

**Faustregel:**
- 100 Ideen → 5 Punkte pro Person
- 50 Ideen → 3 Punkte pro Person
- 20 Ideen → 2 Punkte pro Person

**Facilitation-Tip:**
- 5 Min still voten (keine Diskussion)
- "Vote on what excites you" nicht "what's safe"
- Nach Voting: Top 3 diskutieren

---

## 2. Impact / Effort Matrix

**Use:** ROI-basierte Priorisierung

**Achsen:**
- **Y-Achse:** Impact (Low → High)
- **X-Achse:** Effort (Low → High)

**Quadranten:**

```
        High Impact
            │
    Quick   │   Big Bets
    Wins    │   (High Impact, High Effort)
            │
────────────┼──────────── Effort
            │   Fill-Ins  │   Thankless
            │   (Low      │   Tasks
            │    Impact,  │   (Low
            │    Low      │    Impact,
            │    Effort)  │    High
            │             │    Effort)
            │
        Low Impact
```

**Priorisierung:**
1. **Quick Wins** zuerst (High Impact, Low Effort)
2. **Big Bets** planen (High Impact, High Effort)
3. **Fill-Ins** wenn Kapazität (Low Impact, Low Effort)
4. **Thankless** ignorieren (Low Impact, High Effort)

**Facilitation-Tip:**
- Jede Idee auf Post-it
- Gemeinsam einordnen (5-10 Min)
- Nur Quick Wins + Big Bets weiterverfolgen

---

## 3. Kano-Modell

**Use:** Kundenbedürfnisse priorisieren

**5 Kategorien:**

| Kategorie | Frage | Beispiel |
|-----------|-------|----------|
| **Basis** | Erwartet (nicht erwähnen) | Login, Datenschutz |
| **Performance** | Mehr ist besser | Speed, Features |
| **Excitement** | Überrascht positiv | Unanticipated delight |
| **Indifferent** | Kunde egal | Interner Prozeß |
| **Reverse** | Stört Kunde | Zu viel Feature |

**Survey-Frage:**
- **Funktional:** "Wie fühlst du wenn Feature X vorhanden?"
- **Dysfunktional:** "Wie fühlst du wenn Feature X fehlt?"

**Antworten:**
- Like, Expect, Neutral, Live-with, Dislike

**Auswertung:**
- Meist "Like" bei vorhanden → Excitement
- Meist "Dislike" bei fehlt → Basis
- Linear skaliert → Performance

---

## 4. MoSCoW-Methode

**Use:** Scope-Verhandlung mit Stakeholdern

**Prioritäten:**

| Level | Bedeutung | % Scope |
|-------|-----------|---------|
| **M**ust-Have | Nicht verhandelbar | 60% |
| **S**hould-Have | Verhandelbar wenn nötig | 20% |
| **C**ould-Have | Optional wenn Zeit | 20% |
| **W**on't-Have | Explizit nicht jetzt | 0% |

**Rules:**
- Must-Haves ≤ 60% (sonst alles ist P0)
- Should + Could = Buffer für Scope-Creep
- Won't-Haves dokumentieren (nicht vergessen)

**Facilitation-Tip:**
- Stakeholder müssen Must-Haves **verteidigen**
- "Warum ist das nicht verhandelbar?"
- Wenn alles P0 → Stakeholder eskalieren

---

## 5. RICE-Scoring

**Use:** Data-driven Priorisierung

**Formula:**
```
RICE Score = (Reach × Impact × Confidence) / Effort
```

**Komponenten:**

| Faktor | Frage | Scale |
|--------|-------|-------|
| **R**each | Wie viele betroffen? | 1-100 (Personen/Quartal) |
| **I**mpact | Wie stark? | 0.25-3 (Massive = 3) |
| **C**onfidence | Wie sicher? | 50%-100% (High = 100%) |
| **E**ffort | Wie aufwändig? | 1-10 (Person-Months) |

**Beispiel:**
```
Feature A:
- Reach: 50 Kunden/Quartal
- Impact: 2 (High)
- Confidence: 80%
- Effort: 3 Months

RICE = (50 × 2 × 0.8) / 3 = 26.7
```

**Facilitation-Tip:**
- Jede Idee scoren (15 Min)
- Top 5 nach RICE priorisieren
- Confidence explizit machen (nicht raten)

---

## 6. Value vs. Complexity

**Use:** Executive-friendly Priorisierung

**Achsen:**
- **Y-Achse:** Business Value (Revenue, Retention, NPS)
- **X-Achse:** Complexity (Tech, Org, Compliance)

**Decision-Rules:**
1. **High Value, Low Complexity** → Sofort starten
2. **High Value, High Complexity** → Roadmap planen
3. **Low Value, Low Complexity** → Fill-Ins
4. **Low Value, High Complexity** → Streichen

**Facilitation-Tip:**
- Value quantifizieren (€, %, Score)
- Complexity multidimensional (Tech + Org + Risk)
- C-Level einladen für Value-Diskussion

---

## 7. 100-Dollar-Test

**Use:** Wenn demokratisches Voting blockt

**Ablauf:**
1. Jede Person bekommt imaginäre 100$
2. "Investiere" in Ideen (alle auf eine oder streuen)
3. Top 3 nach investiertem Kapital

**Psychologie:**
- "Investment" framing → ROI-Denken
- Knappheit (100$) → erzwungene Trade-offs
- Keine "halben" Votes (alles oder nichts)

**Facilitation-Tip:**
- 5 Min still investieren
- Nach Voting: "Warum hast du in X investiert?"
- Top 3 weiterverfolgen

---

## 8. Now / Next / Later

**Use:** Roadmap-Planning nach Brainstorming

**Horizonte:**

```
Now (4-6 Wochen)     Next (3-6 Monate)    Later (6-12+ Monate)
│                    │                    │
├─ Quick Wins        ├─ Big Bets          ├─ Excitement
├─ Basis-Must-Haves  ├─ Performance       ├─ When capacity
└─ 3-5 Items         ├─ 5-8 Items         └─ Backlog
```

**Decision-Rules:**
- **Now:** Nur was ≤ 6 Wochen lieferbar
- **Next:** Was Planung braucht aber klar ist
- **Later:** Alles andere (Review in 6 Monaten)

**Facilitation-Tip:**
- Jede Idee zuordnen (10 Min)
- Now-Scope ≤ 5 Items (Fokus erzwingen)
- Later explizit dokumentieren (nicht vergessen)

---

## 9. Weighted Scoring

**Use:** Multi-Stakeholder Priorisierung

**Steps:**
1. Kriterien definieren (5-7 max)
2. Gewichtung pro Kriterium (Summe = 100%)
3. Jede Idee pro Kriterium scoren (1-10)
4. Gewichteter Score = Σ (Kriterium × Gewichtung)

**Beispiel-Kriterien:**
- Business Value (30%)
- Technical Feasibility (20%)
- Customer Impact (25%)
- Strategic Fit (15%)
- Risk (10%)

**Berechnung:**
```
Idee A:
- Business Value: 8 × 0.30 = 2.4
- Feasibility: 6 × 0.20 = 1.2
- Customer: 9 × 0.25 = 2.25
- Strategic: 7 × 0.15 = 1.05
- Risk: 4 × 0.10 = 0.4

Total: 7.3 / 10
```

---

## 10. Decision-Matrix (Pugh)

**Use:** Wenn Baseline-Vergleich nötig

**Ablauf:**
1. Baseline definieren (Status-quo oder Competitor)
2. Kriterien definieren (5-7)
3. Jede Idee vs. Baseline: Better (+), Same (0), Worse (-)
4. Σ Score → Top Ideen

**Beispiel:**
```
Baseline: Current Checkout

Kriterien: Conversion, Speed, Support, Dev-Effort, Maintenance

Idee A: + + 0 - 0 = +2
Idee B: + + + - - = +1
Idee C: + + + + 0 = +4 ← Winner
```

---

## Auswahl-Decision-Tree

```
Stakeholder-Typ?
├── Demokratisch → Dot-Voting oder 100-Dollar-Test
├── Executive → Value vs. Complexity oder Now/Next/Later
├── Data-Driven → RICE oder Weighted Scoring
└── Customer-Focus → Kano oder Decision-Matrix

Zeit verfügbar?
├── <15 Min → Dot-Voting oder 100-Dollar-Test
├── 15-30 Min → Impact/Effort oder MoSCoW
└── 30-60 Min → RICE oder Weighted Scoring

Ideen-Anzahl?
├── 10-20 → Dot-Voting oder Impact/Effort
├── 20-50 → Kano oder MoSCoW
└── 50+ → RICE oder Weighted Scoring (top 20 first)
```

---

**Source:** Brainstorming-Skill P0-Assets  
**Integration:** Nach `divergent-techniques.md`, vor `framework-matrix.md`
