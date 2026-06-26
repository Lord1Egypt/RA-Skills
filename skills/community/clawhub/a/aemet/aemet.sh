#!/bin/bash
set -e

# Configuración
API_KEY_FILE="$HOME/.openclaw/credentials/aemet-api-key.txt"
BASE_URL="https://opendata.aemet.es/opendata/api"
CACHE_DIR="$HOME/.openclaw/cache/aemet"
mkdir -p "$CACHE_DIR"

# Colores para niveles de alerta
GREEN="🟢"
YELLOW="🟡"
ORANGE="🟠"
RED="🔴"

# Cargar API key
if [[ ! -f "$API_KEY_FILE" ]]; then
    echo "❌ Error: No se encontró la API key de AEMET"
    echo "Guarda tu API key en: $API_KEY_FILE"
    echo "Regístrate en: https://opendata.aemet.es/centrodedescargas/altaUsuario"
    exit 1
fi
API_KEY=$(cat "$API_KEY_FILE" | tr -d '[:space:]')

# Función para hacer peticiones con retry y cache
aemet_request() {
    local endpoint="$1"
    local url="${BASE_URL}${endpoint}?api_key=${API_KEY}"
    
    # Cache por 5 minutos
    local cache_file="${CACHE_DIR}/$(echo "$endpoint" | md5sum | cut -d' ' -f1)"
    if [[ -f "$cache_file" ]] && [[ $(find "$cache_file" -mmin -5) ]]; then
        cat "$cache_file"
        return
    fi
    
    # Intentar hasta 3 veces con backoff
    local attempt=0
    local max_attempts=3
    local delay=2
    
    while [[ $attempt -lt $max_attempts ]]; do
        attempt=$((attempt + 1))
        
        # Primera petición para obtener URL de datos
        local response=$(curl -s --max-time 30 "$url")
        local status=$(echo "$response" | jq -r '.estado // .status' 2>/dev/null)
        
        if [[ "$status" != "200" ]]; then
            if [[ "$status" == "429" ]]; then
                echo "⚠️  Rate limit excedido. Esperando ${delay}s..." >&2
                sleep $delay
                delay=$((delay * 2))
                continue
            else
                echo "❌ Error en la API ($status): $response" >&2
                return 1
            fi
        fi
        
        # Obtener URL de datos
        local data_url=$(echo "$response" | jq -r '.datos')
        
        # Segunda petición para obtener datos reales
        local data=$(curl -s --max-time 30 "$data_url")
        echo "$data" | tee "$cache_file"
        return 0
    done
    
    echo "❌ Máximo de reintentos alcanzado" >&2
    return 1
}

# Función para obtener código de área
get_area_code() {
    local area="$1"
    case "$(echo "$area" | tr '[:upper:]' '[:lower:]')" in
        "andalucia"|"andalucía") echo "1" ;;
        "aragon"|"aragón") echo "2" ;;
        "asturias") echo "3" ;;
        "baleares") echo "4" ;;
        "canarias") echo "5" ;;
        "cantabria") echo "6" ;;
        "castilla-la mancha"|"castilla la mancha") echo "7" ;;
        "castilla y leon"|"castilla y león") echo "8" ;;
        "cataluna"|"cataluña") echo "9" ;;
        "valencia"|"comunidad valenciana") echo "10" ;;
        "extremadura") echo "11" ;;
        "galicia") echo "12" ;;
        "madrid") echo "72" ;;
        "murcia") echo "13" ;;
        "navarra") echo "15" ;;
        "pais vasco"|"país vasco") echo "16" ;;
        "rioja"|"la rioja") echo "17" ;;
        "ceuta") echo "18" ;;
        "melilla") echo "19" ;;
        *) 
            if [[ "$area" =~ ^[0-9]+$ ]] && [[ "$area" -ge 1 ]] && [[ "$area" -le 19 ]] || [[ "$area" == "72" ]]; then
                echo "$area"
            else
                echo "❌ Área no válida: $area" >&2
                return 1
            fi
            ;;
    esac
}

# Función para obtener código de municipio
get_municipio_code() {
    local query="$1"
    
    if [[ -z "$query" ]]; then
        echo "❌ Consulta vacía" >&2
        return 1
    fi
    
    # Cache de municipios (24 horas)
    local municipios_cache="${CACHE_DIR}/municipios.json"
    if [[ ! -f "$municipios_cache" ]] || [[ $(find "$municipios_cache" -mtime +0) ]]; then
        echo "📥 Actualizando lista de municipios..." >&2
        aemet_request "/maestro/municipios" > "$municipios_cache" || return 1
    fi
    
    # Buscar por código postal
    if [[ "$query" =~ ^[0-9]{5}$ ]]; then
        local result=$(jq -r ".[] | select(.codigoPostal == \"$query\") | \"\(.id):\(.nombre):\(.provincia)\"" "$municipios_cache" 2>/dev/null | head -1)
        if [[ -n "$result" ]]; then
            echo "$result" | cut -d':' -f1
            return
        fi
    fi
    
    # Buscar por nombre
    local result=$(jq -r ".[] | select(.nombre | test(\"$query\"; \"i\")) | \"\(.id):\(.nombre):\(.provincia)\"" "$municipios_cache" 2>/dev/null | head -1)
    if [[ -n "$result" ]]; then
        echo "$result" | cut -d':' -f1
        return
    fi
    
    echo "❌ No se encontró el municipio: $query" >&2
    return 1
}

# Función para mostrar alertas
show_alertas() {
    local area="$1"
    local filter_level="$2"
    local area_code=$(get_area_code "$area")
    
    if [[ -z "$area_code" ]]; then
        return 1
    fi
    
    echo "🌤️ Consultando alertas para área $area (código: $area_code)..."
    
    local data=$(aemet_request "/avisos_cap/ultimoelaborado/area/$area_code")
    if [[ -z "$data" ]]; then
        echo "❌ No se pudieron obtener alertas"
        return 1
    fi
    
    # Parsear XML con xmllint si está disponible
    local temp_file=$(mktemp)
    echo "$data" > "$temp_file"
    
    echo "📊 Alertas AEMET - $area (área $area_code)"
    echo "───────────────────────────────"
    
    if command -v xmllint &> /dev/null; then
        local alert_count=$(xmllint --xpath 'count(//alert)' "$temp_file" 2>/dev/null || echo "0")
        
        if [[ "$alert_count" -eq "0" ]]; then
            echo "✅ No hay alertas activas"
            rm "$temp_file"
            return
        fi
        
        local has_filtered=false
        
        for i in $(seq 1 "$alert_count"); do
            local event=$(xmllint --xpath "string((//alert)[$i]//event[1])" "$temp_file" 2>/dev/null || echo "")
            local level=$(xmllint --xpath "string((//alert)[$i]//parameter[valueName='AEMET-Meteoalerta nivel']/value)" "$temp_file" 2>/dev/null || echo "")
            local onset=$(xmllint --xpath "string((//alert)[$i]//onset)" "$temp_file" 2>/dev/null || echo "")
            local expires=$(xmllint --xpath "string((//alert)[$i]//expires)" "$temp_file" 2>/dev/null || echo "")
            
            level=$(echo "$level" | tr '[:upper:]' '[:lower:]')
            
            # Filtrar por nivel
            if [[ -n "$filter_level" ]]; then
                local filter_match=false
                IFS=',' read -ra levels <<< "$filter_level"
                for lvl in "${levels[@]}"; do
                    if [[ "$level" == "$lvl" ]]; then
                        filter_match=true
                        break
                    fi
                done
                if [[ "$filter_match" == false ]]; then
                    continue
                fi
            fi
            
            has_filtered=true
            
            # Icono según nivel
            local icon=""
            case "$level" in
                "verde") icon="$GREEN" ;;
                "amarilla"|"amarillo") icon="$YELLOW" ;;
                "naranja") icon="$ORANGE" ;;
                "roja"|"rojo") icon="$RED" ;;
                *) icon="⚪" ;;
            esac
            
            echo "$icon Nivel: ${level^}"
            echo "📅 Fecha: $(echo "$onset" | cut -d'T' -f1 2>/dev/null || echo "N/A")"
            echo "🌡️ Fenómeno: $event"
            echo "⏰ Inicio: $(echo "$onset" | sed 's/T/ /' | cut -d'+' -f1 2>/dev/null || echo "N/A")"
            echo "⏰ Fin: $(echo "$expires" | sed 's/T/ /' | cut -d'+' -f1 2>/dev/null || echo "N/A")"
            echo "───────────────────────────────"
        done
        
        if [[ "$has_filtered" == false ]] && [[ -n "$filter_level" ]]; then
            echo "ℹ️  No hay alertas de nivel: $filter_level"
        fi
    else
        echo "ℹ️  Instala xmllint (libxml2-utils) para ver detalles completos"
        echo "📄 Datos XML disponibles:"
        echo "$data" | head -5
    fi
    
    rm "$temp_file"
}

# Función para mostrar predicción
show_pronostico() {
    local municipio="$1"
    local tipo="${2:-diaria}"
    
    if [[ "$tipo" != "diaria" ]] && [[ "$tipo" != "horaria" ]]; then
        echo "❌ Tipo no válido: $tipo (usa 'diaria' o 'horaria')" >&2
        return 1
    fi
    
    echo "🌤️ Buscando municipio: $municipio..."
    
    local municipio_code=$(get_municipio_code "$municipio")
    if [[ -z "$municipio_code" ]]; then
        return 1
    fi
    
    echo "📊 Obteniendo predicción $tipo para municipio $municipio_code..."
    
    local endpoint=""
    case "$tipo" in
        "diaria") endpoint="/prediccion/especifica/municipio/diaria/$municipio_code" ;;
        "horaria") endpoint="/prediccion/especifica/municipio/horaria/$municipio_code" ;;
    esac
    
    local data=$(aemet_request "$endpoint")
    if [[ -z "$data" ]]; then
        echo "❌ No se pudo obtener la predicción"
        return 1
    fi
    
    echo "📈 Predicción $tipo"
    echo "───────────────────────────────"
    
    if echo "$data" | jq -e '.municipio' >/dev/null 2>&1; then
        local nombre=$(echo "$data" | jq -r '.municipio.nombre // "N/A"')
        local provincia=$(echo "$data" | jq -r '.municipio.provincia // "N/A"')
        echo "📍 Municipio: $nombre"
        echo "🏙️ Provincia: $provincia"
        
        if [[ "$tipo" == "diaria" ]] && echo "$data" | jq -e '.prediccion.dia' >/dev/null 2>&1; then
            echo ""
            echo "📅 Próximos días:"
            echo "$data" | jq -r '.prediccion.dia[0:3] | .[] | "  \(.fecha): \(.temperatura.maxima)°C / \(.temperatura.minima)°C"' 2>/dev/null || echo "  (Formato no esperado)"
        fi
    else
        echo "📊 Datos recibidos (instala jq para formato completo):"
        echo "$data" | head -3
    fi
}

# Función para buscar municipio
show_buscar() {
    local query="$1"
    
    if [[ -z "$query" ]]; then
        echo "❌ Consulta vacía" >&2
        return 1
    fi
    
    echo "🔍 Buscando municipio: $query..."
    
    local municipios_cache="${CACHE_DIR}/municipios.json"
    if [[ ! -f "$municipios_cache" ]] || [[ $(find "$municipios_cache" -mtime +0) ]]; then
        echo "📥 Actualizando lista de municipios..." >&2
        aemet_request "/maestro/municipios" > "$municipios_cache"
    fi
    
    local results
    if [[ "$query" =~ ^[0-9]{5}$ ]]; then
        results=$(jq -r ".[] | select(.codigoPostal == \"$query\") | \"📮 \(.codigoPostal) - \(.nombre) (\(.provincia)) - ID: \(.id)\"" "$municipios_cache" 2>/dev/null)
    else
        results=$(jq -r ".[] | select(.nombre | test(\"$query\"; \"i\")) | \"📍 \(.nombre) (\(.provincia)) - CP: \(.codigoPostal) - ID: \(.id)\"" "$municipios_cache" 2>/dev/null | head -10)
    fi
    
    if [[ -z "$results" ]]; then
        echo "❌ No se encontraron resultados"
        return 1
    fi
    
    echo "📋 Resultados:"
    echo "$results"
}

# Función de test
show_test() {
    echo "🧪 Probando conexión con AEMET..."
    response=$(curl -s --max-time 30 "${BASE_URL}/maestro/municipios?api_key=${API_KEY}")
    status=$(echo "$response" | jq -r '.estado // .status' 2>/dev/null || echo "error")
    if [[ "$status" == "200" ]]; then
        echo "✅ Conexión exitosa"
        return 0
    else
        echo "❌ Error en la conexión ($status)"
        return 1
    fi
}

# Main
case "${1:-}" in
    "alertas")
        area="${2:-madrid}"
        filter_level="${3:-}"
        show_alertas "$area" "$filter_level"
        ;;
    "pronóstico"|"pronostico")
        municipio="${2:-}"
        tipo="${3:-diaria}"
        if [[ -z "$municipio" ]]; then
            echo "❌ Uso: $0 pronóstico <municipio|código_postal> [diaria|horaria]"
            exit 1
        fi
        show_pronostico "$municipio" "$tipo"
        ;;
    "buscar")
        query="${2:-}"
        if [[ -z "$query" ]]; then
            echo "❌ Uso: $0 buscar <nombre|código_postal>"
            exit 1
        fi
        show_buscar "$query"
        ;;
    "test")
        show_test
        ;;
    *)
        echo "🌤️ AEMET Skill v1.0 - Consulta alertas meteorológicas"
        echo "───────────────────────────────"
        echo "Uso:"
        echo "  $0 alertas <área> [nivel]      - Alertas por área (ej: madrid)"
        echo "  $0 pronóstico <municipio>      - Predicción para municipio"
        echo "  $0 buscar <nombre|cp>          - Buscar municipio"
        echo "  $0 test                        - Probar conexión"
        echo ""
        echo "Ejemplos:"
        echo "  $0 alertas madrid"
        echo "  $0 alertas cataluña amarilla,naranja"
        echo "  $0 pronóstico 28001"
        echo "  $0 pronóstico \"Madrid\" --horaria"
        echo "  $0 buscar \"Barcelona\""
        echo ""
        echo "📝 Requisitos: curl, jq, libxml2-utils (xmllint)"
        echo "🔑 API key: ~/.openclaw/credentials/aemet-api-key.txt"
        exit 1
        ;;
esac