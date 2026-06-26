# EmmeStudio — Template Documenti

Specifiche di layout per ogni tipo di documento. Usare come riferimento quando si produce un nuovo documento.

---

## 1. Carta Intestata

**Template:** `BRAND/CARTA INTESTATA - PREVENTIVI/EmmeStudio_CartaIntestata.docx`

### Struttura

- **Header:** Logo EmmeStudio (variante primaria blu) posizionato in alto
- **Corpo:**
  - Titolo comunicazione: Georgia Bold 18pt (fallback per Ivar Soft Semibold)
  - Titolo paragrafo: Arial Bold 12pt (fallback per Open Sauce One Semibold)
  - Testo corpo: Arial Regular 10pt (fallback per Open Sauce One Regular)
- **Footer:** Dati studio (indirizzo, contatti, P.IVA)
- **Margini:** Standard Word (2.5cm circa su tutti i lati)

### Quando usarla

Comunicazioni generiche a clienti, lettere, note informative. NON per preventivi (usare i template specifici).

---

## 2. Preventivi

**Template disponibili:**

| Template | File | Caso d'uso |
|---|---|---|
| SRL + Startup + Gestione | `000000_Cliente_SRLStartupGestione.docx` | Offerta gestione contabilità SRL |
| Forfettario completo | `000000_Cliente_ForfettarioArtCommAperturaGestione.docx` | Apertura + gestione regime forfettario |
| Versamento CS | `000000_Cliente_SRL_VersamentoCS.docx` | Comunicazione versamento capitale sociale |

### Struttura comune preventivi

```
┌─────────────────────────────────────────┐
│  [LOGO EMMESTUDIO]            Header    │
├─────────────────────────────────────────┤
│                                         │
│  Titolo offerta (Georgia Bold 18pt)     │
│                                         │
│  Spett.le / Gentile,                    │
│  Bergamo, lì … [anno]                   │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │ TABELLA COMPETENZE               │  │
│  │ Voce              │ Importo      │  │
│  │ ...               │ € ...        │  │
│  │ Totale            │ € ...        │  │
│  └───────────────────────────────────┘  │
│                                         │
│  [Eventuali altre sezioni tabellari]    │
│                                         │
│  Clausola IVA esclusa                   │
│  Clausola validità 30 giorni            │
│                                         │
│  Firma per accettazione: ___________    │
│                                         │
├─────────────────────────────────────────┤
│  [FOOTER DATI STUDIO]                   │
└─────────────────────────────────────────┘
```

### Regole preventivi

- **Titolo:** Inizia sempre con "Offerta per..." (es. "Offerta per Gestione Contabilità SRL per anno 2026")
- **Destinatario:** "Spett.le [Ragione Sociale]" per aziende, "Gentile [Nome]," per persone fisiche
- **Data:** "Bergamo, lì [giorno mese] [anno]"
- **Tabelle competenze:**
  - Colonna sinistra: voce descrittiva
  - Colonna destra: importo (€ allineato a destra)
  - Riga totale in bold
  - Note con asterisco (*) sotto la tabella, font più piccolo
- **Prezzi:** Formato `€ 1.000,00` (separatore migliaia = punto, decimali = virgola)
- **Sezioni tipiche:** Competenze attivazione, Spese anticipate, Fatturazione elettronica, Costi di gestione
- **Sconti:** Mostrare sia il totale pieno che il totale scontato quando applicabile
- **Addebito mensile:** Quando presente, calcolare come totale annuo scontato / 12

### Font nei preventivi attuali

| Elemento | Font attuale | Font ufficiale (se disponibile) |
|---|---|---|
| Titolo offerta | Georgia Bold 18pt | Ivar Soft Semibold 18pt |
| Voci tabella | Arial Regular 8.5pt | Open Sauce One Regular 8.5pt |
| Voci bold | Arial Bold 8.5pt | Open Sauce One Semibold 8.5pt |
| Titolo sezione | Georgia Bold 16pt | Ivar Soft Semibold 16pt |
| Note asterisco | Poppins Regular 8.5pt | Open Sauce One Regular 8pt |

---

## 3. Presentazioni

**Template:** `BRAND/PPT/EmmeStudio_EsempioPresentazione.key` (Keynote)
**Esempio PDF:** `BRAND/PPT/EmmeStudio_EsempioPresentazione.pdf`

### 3 tipi di slide

#### Tipo A — Copertina / Chiusura (sfondo blu scuro #160C30)

```
┌─────────────────────────────────────────┐
│                                         │
│  Titolo grande                          │
│  (Ivar Soft Semibold, azzurro #77B3DD)  │
│  Occupa 2/3 superiori                   │
│                                         │
│  Sottotitolo                            │
│  (Open Sauce One, bianco)               │
│                                         │
│                                         │
│  [LOGO bianco]     Relatore | Data      │
└─────────────────────────────────────────┘
```

#### Tipo B — Divisoria sezione (sfondo azzurro #A5D3EC)

```
┌─────────────────────────────────────────┐
│                                         │
│                                         │
│                                         │
│  (3/4 superiori vuoti — design arioso)  │
│                                         │
│  01                                     │
│  Titolo sezione                         │
│  (Ivar Soft Semibold, blu scuro)        │
└─────────────────────────────────────────┘
```

#### Tipo C — Contenuto (sfondo bianco)

```
┌─────────────────────────────────────────┐
│                                         │
│  Titolo slide    │  Contenuto           │
│  (Ivar Soft      │  (Open Sauce One     │
│   Semibold,      │   Regular, corpo)    │
│   blu scuro)     │                      │
│   ~28% width     │  • Elenco puntato    │
│                  │  • Con bold per       │
│                  │    evidenziazione     │
│                  │                      │
│            © EmmeStudio [anno] | [pag]  │
└─────────────────────────────────────────┘
```

### Regole presentazioni

- **Formato:** 16:9 (widescreen)
- **Linea verticale:** Sottile (~1-2px), azzurro/grigio, separa titolo (28%) da contenuto (70%)
- **Indice:** Slide 2, numeri sezione (01, 02...) in azzurro, titoli in serif bold
- **Timeline/Roadmap:** Linea orizzontale con cerchi azzurri equidistanti
- **Evidenziazione:** Solo bold, mai colori diversi nel testo, mai sottolineato
- **Emoji/icone:** Uso molto parco (quasi assenti)
- **Margini:** ~6% laterali, ~8-10% superiore/inferiore
- **Interlinea titoli grandi:** 1.1-1.2 (compatta)
- **Interlinea corpo:** 1.5-1.6 (ariosa)
