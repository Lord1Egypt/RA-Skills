# German Semiconductor Terminology (Deutsch)

Lexicon for searching Bundesanzeiger filings, regional press (Saxony/Bavaria semiconductor clusters), and German-language industry forums.

## Critical Translation Traps

These terms are mistranslated by Google Translate in semiconductor context:

| German | Correct meaning | Google Translate gives |
|---|---|---|
| Ausbeute | Yield (manufacturing) | "Loot" / "haul" |
| Abscheidung | Deposition (CVD/PVD) | "Separation" / "precipitation" |
| Scheibe | Wafer | "Disc" / "slice" (note: "Wafer" loanword dominates in modern German) |
| Aufschleudern | Spin coating | "Flinging on" |
| Speicher | Memory (RAM/storage) | "Attic" / "granary" |
| Baustein | Component / IC | "Building stone" |
| Gehäuse | Package (IC packaging) | "Housing" / "enclosure" |
| Leistungshalbleiter | Power semiconductor | "Performance semiconductor" |
| Dotierung | Doping (of silicon) | "Endowment" / "allocation" |
| Ladungsträger | Charge carrier | "Load carrier" / "cargo carrier" |
| Anschluss | Pin / terminal / pad | "Connection" (too vague) |
| Entwurf | Design (chip design) | "Draft" / "sketch" |

## Bundesanzeiger Filing Search

German HGB filings have NO equivalent of DART's 주요 거래처 or EDINET's 主要仕入先. There is no mandatory supplier disclosure section. The two standardized top-level documents are:

| Document | English | Legal basis |
|---|---|---|
| **Lagebericht** | Management report | §289 HGB |
| **Anhang** | Notes to financial statements | §§284-285 HGB |

Supplier information, when disclosed at all, appears as risk factors or procurement discussion within the Lagebericht. Search for these keywords inside the full text:

| Keyword | English | Where it appears |
|---|---|---|
| Beschaffung | Procurement | Lagebericht body text |
| Beschaffungsrisiken | Procurement risks | Risiko- und Chancenbericht subsection |
| Zulieferer / Lieferanten | Suppliers | Lagebericht, Anhang |
| Rohstoffe | Raw materials | Lagebericht |
| Abhängigkeit | Dependency | Risiko- und Chancenbericht |
| Lieferkette | Supply chain | Lagebericht |
| Aufgliederung der Umsatzerlöse | Revenue breakdown (by activity) | Anhang (§285 Nr. 4, large companies only) |
| Risiko- und Chancenbericht | Risk and opportunities report | Lagebericht subsection (DRS 20) |
| Grundlagen des Unternehmens | Company fundamentals | Lagebericht subsection (DRS 20) |

## Search Query Patterns

```
# Who supplies X to Company Y?
{Y} Lieferant {material}
{Y} Zulieferer Halbleiter

# Regional semiconductor cluster news
Halbleiter Sachsen / Halbleiter Dresden
Silicon Saxony {company}
Chipfabrik Dresden / Chipfabrik Magdeburg

# New fab / expansion announcements
{company} Halbleiterwerk Erweiterung
{company} neue Fertigung
Förderbescheid Halbleiter (government subsidy approvals)

# Supply chain tracking
Lieferkette Halbleiter
{material} Beschaffung {company}

# Supplier qualification
{company} Qualifizierung {customer}
{company} Lieferkette {customer}
```

## Key Press Sources

| Source | URL | Coverage |
|---|---|---|
| Elektroniknet.de | elektroniknet.de/halbleiter/ | Dedicated semiconductor section, freely accessible |
| Handelsblatt | handelsblatt.com/themen/chiphersteller | Business press, sometimes has supplier intel |
| Silicon Saxony | silicon-saxony.de | Cluster association news, podcast, event archives |
| Sächsische Zeitung | saechsische.de | Dresden/Saxony semiconductor cluster |
| Markt&Technik | markt-technik.de | Leading electronics weekly (paywalled) |

## Key Filing Sources

| Source | URL | What it covers |
|---|---|---|
| Bundesanzeiger | bundesanzeiger.de | Annual reports (Jahresabschluss) for German GmbH/AG |
| Unternehmensregister | unternehmensregister.de | Consolidated portal (Bundesanzeiger + Handelsregister) |
