#!/bin/bash
# Bitpanda v2 - Script per gestione portafoglio
# Filosofia: Dati grezzi, affidabili, senza aggregazioni automatiche

set -e

# ============================================================================
# CONFIGURAZIONE
# ============================================================================

BASE_URL="https://api.bitpanda.com"
TIMEOUT=30
PAGE_SIZE=50

# ============================================================================
# FUNZIONI UTILITÀ
# ============================================================================

# Legge l'API key dall'ambiente o da parametro
get_api_key() {
    if [ -n "$BITPANDA_API_KEY" ]; then
        echo "$BITPANDA_API_KEY"
    elif [ -n "$1" ]; then
        echo "$1"
    else
        error_exit "API key non trovata. Imposta BITPANDA_API_KEY o passala come parametro."
    fi
}

# Gestione errori comuni
handle_error() {
    local http_code=$1
    local response=$2
    
    case $http_code in
        401)
            error_exit "Errore 401: API key invalida o non autorizzata. Verifica BITPANDA_API_KEY."
            ;;
        429)
            echo "⚠️ Errore 429: Rate limit raggiunto. Attendi qualche secondo e riprova." >&2
            sleep 5
            return 1
            ;;
        0|5*)
            error_exit "Errore di connessione o server ($http_code). Controlla la tua connessione internet."
            ;;
    esac
    
    if [ -n "$response" ]; then
        echo "Risposta errore: $response" | jq '.' 2>/dev/null || echo "$response"
    fi
}

# Uscita con messaggio di errore
error_exit() {
    echo "❌ $1" >&2
    exit 1
}

# Chiamata API base con error handling
api_call() {
    local endpoint=$1
    local params=${2:-""}
    local api_key=$(get_api_key "$3")
    
    local url="${BASE_URL}${endpoint}"
    if [ -n "$params" ]; then
        url="${url}?${params}"
    fi
    
    local response
    local http_code
    
    # Esegui la chiamata curl
    response=$(curl -s -w "\n%{http_code}" \
        --max-time $TIMEOUT \
        -H "X-Api-Key: ${api_key}" \
        -H "Content-Type: application/json" \
        "$url" 2>/dev/null) || {
        handle_error 0 ""
        return $?
    }
    
    # Estrai HTTP code e body
    http_code=$(echo "$response" | tail -n1)
    response=$(echo "$response" | sed '$d')
    
    # Gestisci errori
    if [ "$http_code" != "200" ]; then
        handle_error "$http_code" "$response"
        return $?
    fi
    
    echo "$response"
}

# ============================================================================
# COMANDI PRINCIPALI
# ============================================================================

# balances - Tutti i wallet con saldi > 0 (endpoint corretto: /v1/asset-wallets)
cmd_balances() {
    # Endpoint /v1/balances NON ESISTE nella docs ufficiale!
    # Usiamo /v1/asset-wallets che restituisce tutti i wallet organizzati per categoria
    
    local response=$(api_call "/v1/asset-wallets")
    
    # Estrai solo i wallet con balance > 0 da tutte le categorie
    echo "$response" | jq '[
        .data.attributes.cryptocoin.wallets[] | select(.balance | tonumber > 0),
        .data.attributes.commodity.metal.wallets[] | select(.balance | tonumber > 0),
        .data.attributes.security.stock.wallets[] | select(.balance | tonumber > 0),
        .data.attributes.security.etf.wallets[] | select(.balance | tonumber > 0),
        .data.attributes.etc.wallets[] | select(.balance | tonumber > 0),
        .data.attributes.fiat_earn.wallets[] | select(.balance | tonumber > 0)
    ]'
}

# data - Portfolio completo (endpoint corretto: /v1/asset-wallets)
cmd_data() {
    # Endpoint /v1/data NON ESISTE nella docs ufficiale!
    # Usiamo /v1/asset-wallets che include anche last_user_action e dati aggregati
    
    local response=$(api_call "/v1/asset-wallets")
    echo "$response" | jq '.'
}

# trades - Storico trade (con pagination)
cmd_trades() {
    local limit=${1:-50}
    local all_trades=()
    local cursor=""
    local first=true
    
    while true; do
        local params="limit=${limit}"
        if [ -n "$cursor" ]; then
            params="${params}&cursor=${cursor}"
        fi
        
        local response=$(api_call "/v1/trades" "$params")
        
        # Estrai trades e next_cursor
        local trades=$(echo "$response" | jq -c '.trades // []')
        cursor=$(echo "$response" | jq -r '.next_cursor // empty')
        
        if [ $first = true ]; then
            all_trades=($trades)
            first=false
        else
            all_trades+=($trades)
        fi
        
        # Se non c'è next_cursor, siamo alla fine
        if [ -z "$cursor" ]; then
            break
        fi
        
        # Evita loop infiniti: se abbiamo già molti trade, fermiamoci
        if [ ${#all_trades[@]} -gt 1000 ]; then
            echo "⚠️ Limitato a 1000 trade per evitare timeout." >&2
            break
        fi
    done
    
    # Unisci tutti i trade e formatta
    echo "[${all_trades[*]}]" | jq '.'
}

# price - Prezzo singolo asset
cmd_price() {
    local symbol=$1
    
    if [ -z "$symbol" ]; then
        error_exit "Specifica un simbolo (es. BTC, ETH, EUR)."
    fi
    
    local response=$(api_call "/v1/ticker" "symbol=${symbol}")
    
    # Filtra per il simbolo richiesto
    echo "$response" | jq ".[] | select(.symbol == \"${symbol}\")"
}

# prices - Prezzi di tutti gli asset posseduti
cmd_prices() {
    local response=$(api_call "/v1/ticker")
    echo "$response" | jq '.'
}

# ============================================================================
# HELP E USAGE
# ============================================================================

show_help() {
    cat << EOF
Bitpanda v2 - Gestione Portafoglio

Utilizzo: $0 <comando> [opzioni]

Comandi:
  balances              Tutti i wallet con saldi (con pagination)
  data                  Portfolio completo
  trades [--limit N]    Storico trade (default limit: 50)
  price <SYMBOL>        Prezzo singolo asset (es. BTC, ETH)
  prices                Prezzi di tutti gli asset

Opzioni:
  --help, -h            Mostra questo messaggio

Prerequisiti:
  - Imposta BITPANDA_API_KEY come variabile d'ambiente
  - Installa curl e jq

Esempi:
  $0 balances
  $0 trades --limit 10
  $0 price BTC
  $0 prices

Filosofia: Dati grezzi, affidabili, senza aggregazioni automatiche. 🦥💪
EOF
}

# ============================================================================
# MAIN
# ============================================================================

main() {
    if [ $# -eq 0 ]; then
        show_help
        exit 1
    fi
    
    local command=$1
    shift
    
    case $command in
        balances)
            cmd_balances
            ;;
        data)
            cmd_data
            ;;
        trades)
            local limit=50
            if [ -n "$1" ] && [[ "$1" == --limit* ]]; then
                limit=$(echo "$1" | sed 's/--limit=//')
            fi
            cmd_trades $limit
            ;;
        price)
            if [ -z "$1" ]; then
                error_exit "Specifica un simbolo per il prezzo."
            fi
            cmd_price "$1"
            ;;
        prices)
            cmd_prices
            ;;
        --help|-h|help)
            show_help
            ;;
        *)
            error_exit "Comando sconosciuto: $command. Usa --help per vedere i comandi disponibili."
            ;;
    esac
}

# Esegui main con tutti gli argomenti
main "$@"
