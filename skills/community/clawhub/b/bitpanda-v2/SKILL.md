# Bitpanda v2 - Skill per Gestione Portafoglio

Una skill semplice e affidabile per interagire con l'API Bitpanda. Restituisce dati grezzi senza aggregazioni automatiche, garantendo accuratezza e trasparenza.

## 🎯 Filosofia

**Meno "smart", più affidabile.** La versione precedente aveva bug di aggregazione che restituivano dati errati. Questa skill:
- ✅ Restituisce dati grezzi dall'API
- ✅ Gestione pagination corretta
- ✅ Error handling chiaro
- ❌ NO aggregazioni automatiche (l'utente elabora se vuole)

## 📋 Prerequisiti

### Software
- `curl` - per chiamate HTTP
- `jq` - per parsing JSON
- PowerShell o bash shell

### API Key Bitpanda

1. Vai su [Bitpanda Developer Portal](https://developers.bitpanda.com/)
2. Accedi con il tuo account Bitpanda
3. Naviga in "API Keys" o "Settings"
4. Crea una nuova API key (seleziona le permission necessarie)
5. Copia la chiave e salvala

### Configurazione Variabile d'Ambiente

**PowerShell:**
```powershell
$env:BITPANDA_API_KEY = "tua-api-key-qui"
# Per renderla permanente:
[System.Environment]::SetEnvironmentVariable("BITPANDA_API_KEY", "tua-api-key-qui", "User")
```

**Bash (Linux/Mac):**
```bash
export BITPANDA_API_KEY="tua-api-key-qui"
# Per renderla permanente, aggiungi a ~/.bashrc o ~/.zshrc:
echo 'export BITPANDA_API_KEY="tua-api-key-qui"' >> ~/.bashrc
```

## 🛠️ Comandi Disponibili

### `balances` - Wallet Crypto con Saldi > 0

Mostra tutti i wallet crypto/commodity/security con saldo maggiore di zero.

**Endpoint:** `/v1/asset-wallets` (filtrato per balance > 0)

**Esempio:**
```bash
bitpanda.sh balances
```

**Output:** JSON array con solo gli asset che possiedi in quantità significativa. Include:
- Cryptocoin (BTC, ETH, LTC, etc.)
- Commodity/Metals (XAU-Gold, XAG-Silver)
- Security/Stocks (AMD, ARM, QCOM, etc.)
- ETF e altri prodotti

---

### `data` - Portfolio Completo

Ottieni la struttura completa del tuo portfolio con tutti i wallet organizzati per categoria.

**Endpoint:** `/v1/asset-wallets` (risposta completa)

**Esempio:**
```bash
bitpanda.sh data
```

**Output:** JSON completo con:
- Tutti i wallet organizzati per tipo (cryptocoin, commodity, security, etc.)
- `last_user_action`: timestamp dell'ultima azione
- Struttura gerarchica completa del portfolio

**Nota:** Questo comando restituisce TUTTI i wallet (anche quelli con balance = 0), utile per vedere la struttura completa.

---

### `trades [--limit N]` - Storico Trade

Recupera lo storico dei tuoi trade. Supporta pagination automatica per trade vecchi.

**Esempi:**
```bash
# Ultimi 10 trade
bitpanda.sh trades --limit 10

# Tutti i trade (pagination automatica)
bitpanda.sh trades

# Limitato a 50 trade
bitpanda.sh trades --limit 50
```

**Output:** JSON con dettagli di ogni trade (data, tipo, asset, quantità, prezzo).

---

### `price <SYMBOL>` - Prezzo Singolo Asset

Ottieni il prezzo corrente di un singolo asset.

**Esempi:**
```bash
bitpanda.sh price BTC
bitpanda.sh price ETH
bitpanda.sh price EUR
```

**Output:** JSON con simbolo, prezzo attuale e timestamp.

---

### `prices` - Prezzi di Tutti gli Asset Posseduti

Recupera i prezzi correnti di tutti gli asset che possiedi nel tuo portafoglio.

**Esempio:**
```bash
bitpanda.sh prices
```

**Output:** JSON con lista di simboli e prezzi corrispondenti.

---

## 📚 API Reference

Base URL: `https://developer.bitpanda.com/`

### Endpoint Utilizzati (CORRETTI secondo docs ufficiali)

| Comando | Endpoint | Metodo | Note |
|---------|----------|--------|------|
| balances | `/v1/asset-wallets` | GET | Filtra solo balance > 0 |
| data | `/v1/asset-wallets` | GET | Risposta completa con tutte le categorie |
| trades | `/v1/trades` | GET | Cursor-based pagination |
| price | `/v1/ticker?symbol=...` | GET | Prezzo singolo asset |
| prices | `/v1/ticker` | GET | Prezzi di tutti gli asset disponibili |

**⚠️ Endpoint NON ESISTENTI (rimossi):**
- `/v1/balances` - Non esiste nella docs ufficiale!
- `/v1/data` - Non esiste nella docs ufficiale!

### Pagination

**Trades:** Usa `cursor` e `page_size` per paginazione.
```json
{
  "data": [...],
  "meta": {
    "total_count": 197,
    "next_cursor": "...",
    "page_size": 10
  }
}
```

**Asset Wallets:** Nessuna pagination - restituisce tutti i wallet in una sola chiamata.

## ⚠️ Errori Comuni e Troubleshooting

### 401 Unauthorized
**Causa:** API key invalida o mancante.
**Soluzione:** Verifica che `$env:BITPANDA_API_KEY` sia impostata correttamente.

### 429 Rate Limit
**Causa:** Troppe richieste in breve tempo.
**Soluzione:** Attendi qualche secondo e riprova. Bitpanda ha limiti di rate.

### Timeout
**Causa:** Connessione lenta o API non risponde.
**Soluzione:** Controlla la tua connessione internet, riprova dopo.

### jq Non Trovato
**Causa:** `jq` non installato sul sistema.
**Soluzione:** 
- Windows: Installa via Chocolatey (`choco install jq`) o scarica da [stedolan.github.io/jq](https://stedolan.github.io/jq/)
- Mac: `brew install jq`
- Linux: `sudo apt install jq` (Debian/Ubuntu)

### Output JSON Non Formattato
**Causa:** `jq` non funziona correttamente.
**Soluzione:** Testa con `echo '{}' | jq '.'`. Se non funziona, reinstalla jq.

## 🔧 Configurazione Avanzata

### Timeout Personalizzato
Modifica lo script per cambiare il timeout delle richieste:
```bash
# Nel file bitpanda.sh, cerca la riga con --max-time e modifica
curl ... --max-time 30 ...
```

### Verbose Mode
Per debug, aggiungi `-v` alle chiamate curl nello script.

## 📝 Note Importanti

- **NO Aggregazione:** Questa skill non fa calcoli o aggregazioni sui dati. Restituisce esattamente ciò che Bitpanda invia.
- **Pagination Obbligatoria:** Per `balances` e `trades`, la pagination è gestita automaticamente se necessario.
- **Dati Grezzi:** Se vuoi elaborare i dati (calcolare valori totali, ecc.), fallo dopo con jq o altri tool.

## 🚀 Esempi Pratici

### Valore Totale del Portafoglio
```bash
# Ottieni il portfolio completo e estrai il valore totale
bitpanda.sh data | jq '.total_value'
```

### Lista Asset con Quantità > 0
```bash
# Filtra solo gli asset che possiedi in quantità significativa
bitpanda.sh balances | jq '.[] | select(.available > 0) | {symbol, available}'
```

### Ultimo Trade
```bash
# Ottieni l'ultimo trade fatto
bitpanda.sh trades --limit 1 | jq '.trades[0]'
```

## 🆚 Differenze con bitpanda-official (vecchia versione)

| Caratteristica | bitpanda-official (vecchia) | bitpanda-v2 (nuova - MARZO 2026) |
|----------------|----------------------------|-----------------------------------|
| Endpoint balances/data | ❌ `/v1/balances`, `/v1/data` (NON ESISTENTI!) | ✅ `/v1/asset-wallets` (endpoint corretto) |
| Aggregazione dati | ✅ Automatica (buggy!) | ❌ NO - dati grezzi filtrati |
| Pagination trades | ⚠️ Parziale | ✅ Completa e corretta con cursor |
| Error handling | ⚠️ Limitato | ✅ Completo con messaggi chiari |
| Affidabilità | ❌ Dati errati (endpoint sbagliati) | ✅ Endpoint corretti secondo docs ufficiali |

**🔧 Aggiornamento Marzo 2026:** Corretti gli endpoint `balances` e `data` che usavano URL non esistenti nella API Bitpanda. Ora usano `/v1/asset-wallets` come specificato nella documentazione ufficiale.

## 📞 Supporto

Per problemi o domande:
1. Controlla la [documentazione ufficiale Bitpanda](https://developers.bitpanda.com/)
2. Verifica che l'API key sia valida
3. Testa le chiamate direttamente con curl per isolare il problema

---

**Filosofia BradiBot:** 🦥 Qualità > Velocità, Affidabilità > "Smart". Una skill semplice che funziona bene è meglio di una complessa che dà risultati errati! 💪
