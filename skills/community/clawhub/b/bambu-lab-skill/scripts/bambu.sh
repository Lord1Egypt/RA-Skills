#!/bin/bash

# Bambu Lab 3D-Drucker MQTT Control Script
# Unterstützt A1, P1P, X1 Modelle

# FALLBACK: Wenn mosquitto nicht installiert ist, nutze Python-Version
if ! command -v mosquitto_sub > /dev/null 2>&1; then
    # Prüfe ob Python-Version existiert
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    if [ -f "$SCRIPT_DIR/bambu.py" ]; then
        python3 "$SCRIPT_DIR/bambu.py" "$@"
        exit $?
    fi
fi

# Konfiguration
HOST="${BAMBU_HOST:-192.168.30.103}"
PORT="${BAMBU_PORT:-8883}"
SERIAL="${BAMBU_SERIAL:-03919A3A2200009}"
ACCESS_CODE="${BAMBU_ACCESS_CODE:-33576961}"
MODEL="${BAMBU_MODEL:-A1}"

# Topics
REPORT_TOPIC="device/${SERIAL}/report"
REQUEST_TOPIC="device/${SERIAL}/request"

# Temporäre Datei für MQTT Output
TEMP_FILE=$(mktemp)
trap "rm -f $TEMP_FILE" EXIT

# Hilfe anzeigen
show_help() {
    cat << 'EOF'
Bambu Lab 3D-Drucker Steuerung

Verwendung: bambu.sh <befehl> [optionen]

Status & Überwachung:
  status          - Vollständiger Status-Report
  progress        - Nur Druckfortschritt
  temps           - Temperaturen anzeigen
  watch           - Live-Überwachung (Strg+C zum Beenden)

Steuerung:
  pause           - Druck pausieren
  resume          - Druck fortsetzen
  stop            - Druck abbrechen
  light on|off    - Druckerlicht an/aus
  fans <0-15>    - Lüftergeschwindigkeit (0-15)

Benachrichtigungen:
  notify          - Überwachung mit Telegram-Benachrichtigung

Debug:
  raw             - Rohe MQTT-Nachrichten

Beispiele:
  bambu.sh status
  bambu.sh watch
  bambu.sh pause
  bambu.sh light on
EOF
}

# Prüfe ob mosquitto_sub/_pub verfügbar
 check_mqtt() {
    if ! command -v mosquitto_sub > /dev/null 2>&1; then
        echo "Fehler: mosquitto-clients nicht installiert"
        echo "Installiere mit: apt-get install mosquitto-clients"
        exit 1
    fi
}

# MQTT-Nachricht empfangen (einzeln)
receive_mqtt() {
    local timeout="${1:-5}"
    mosquitto_sub \
        -h "$HOST" \
        -p "$PORT" \
        -u "$SERIAL" \
        -P "$ACCESS_CODE" \
        -t "$REPORT_TOPIC" \
        --tls-version tlsv1.2 \
        -W "$timeout" \
        -C 1 2>/dev/null
}

# MQTT-Nachricht senden
send_mqtt() {
    local payload="$1"
    mosquitto_pub \
        -h "$HOST" \
        -p "$PORT" \
        -u "$SERIAL" \
        -P "$ACCESS_CODE" \
        -t "$REQUEST_TOPIC" \
        -m "$payload" \
        --tls-version tlsv1.2 2>/dev/null
}

# Status formatieren anzeigen
show_status() {
    local json="$1"
    
    if [ -z "$json" ]; then
        echo "❌ Keine Verbindung zum Drucker möglich"
        echo "   Prüfe: Ist der Drucker im LAN-Mode?"
        return 1
    fi
    
    # Werte extrahieren
    local state=$(echo "$json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('print',{}).get('gcode_state','UNKNOWN'))" 2>/dev/null)
    local percent=$(echo "$json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('print',{}).get('mc_percent',0))" 2>/dev/null)
    local remaining=$(echo "$json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('print',{}).get('mc_remaining_time',0))" 2>/dev/null)
    local bed=$(echo "$json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('print',{}).get('bed_temper',0))" 2>/dev/null)
    local nozzle=$(echo "$json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('print',{}).get('nozzle_temper',0))" 2>/dev/null)
    local layer=$(echo "$json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('print',{}).get('layer_num',0))" 2>/dev/null)
    local total_layer=$(echo "$json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('print',{}).get('total_layer_num',0))" 2>/dev/null)
    local filename=$(echo "$json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('print',{}).get('filename','-'))" 2>/dev/null)
    local error=$(echo "$json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('print',{}).get('print_error',0))" 2>/dev/null)
    
    # Status übersetzen
    local status_text="$state"
    case "$state" in
        IDLE) status_text="🟡 Bereit" ;;
        RUNNING) status_text="🟢 Druckt" ;;
        PAUSE) status_text="⏸️  Pausiert" ;;
        FINISH) status_text="✅ Fertig" ;;
        FAILED) status_text="❌ Fehlgeschlagen" ;;
    esac
    
    # Restzeit formatieren
    local hours=$((remaining / 3600))
    local mins=$(((remaining % 3600) / 60))
    local time_str="${hours}h ${mins}min"
    
    echo "═══════════════════════════════════════"
    echo "    🖨️  Bambu Lab $MODEL Status"
    echo "═══════════════════════════════════════"
    echo "Status:    $status_text"
    echo "Datei:     $filename"
    echo "Fortschritt: $percent%"
    echo "Layer:     $layer / $total_layer"
    echo "Restzeit:  $time_str"
    echo "───────────────────────────────────────"
    echo "🌡️  Temperaturen:"
    echo "   Nozzle: ${nozzle}°C"
    echo "   Bett:   ${bed}°C"
    
    if [ "$error" != "0" ] && [ -n "$error" ]; then
        echo "───────────────────────────────────────"
        echo "⚠️  Fehler-Code: $error"
    fi
    echo "═══════════════════════════════════════"
}

# Nur Progress anzeigen
cmd_progress() {
    check_mqtt
    local json=$(receive_mqtt 5)
    local percent=$(echo "$json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('print',{}).get('mc_percent',0))" 2>/dev/null)
    local state=$(echo "$json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('print',{}).get('gcode_state','UNKNOWN'))" 2>/dev/null)
    
    echo "Druckfortschritt: $percent% ($state)"
}

# Temperaturen anzeigen
cmd_temps() {
    check_mqtt
    local json=$(receive_mqtt 5)
    local bed=$(echo "$json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('print',{}).get('bed_temper',0))" 2>/dev/null)
    local bed_target=$(echo "$json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('print',{}).get('bed_target_temper',0))" 2>/dev/null)
    local nozzle=$(echo "$json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('print',{}).get('nozzle_temper',0))" 2>/dev/null)
    local nozzle_target=$(echo "$json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('print',{}).get('nozzle_target_temper',0))" 2>/dev/null)
    local chamber=$(echo "$json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('print',{}).get('chamber_temper','-'))" 2>/dev/null)
    
    echo "🌡️  Temperaturen:"
    echo "   Nozzle: ${nozzle}°C / ${nozzle_target}°C (Ziel)"
    echo "   Bett:   ${bed}°C / ${bed_target}°C (Ziel)"
    [ "$chamber" != "-" ] && echo "   Kammer: ${chamber}°C"
}

# Vollständigen Status anzeigen
cmd_status() {
    check_mqtt
    echo "Verbinde mit $MODEL @ $HOST..."
    local json=$(receive_mqtt 5)
    show_status "$json"
}

# Live-Überwachung
cmd_watch() {
    check_mqtt
    echo "🔴 Live-Überwachung gestartet (Strg+C zum Beenden)..."
    echo ""
    
    while true; do
        local json=$(receive_mqtt 3)
        clear
        show_status "$json"
        echo ""
        echo "Aktualisiert: $(date '+%H:%M:%S')"
        echo "(Strg+C zum Beenden)"
    done
}

# Druck pausieren
cmd_pause() {
    check_mqtt
    echo "⏸️  Pausiere Druck..."
    send_mqtt '{"print": {"command": "pause"}}'
    sleep 1
    echo "✅ Pausiert"
}

# Druck fortsetzen
cmd_resume() {
    check_mqtt
    echo "▶️  Setze Druck fort..."
    send_mqtt '{"print": {"command": "resume"}}'
    sleep 1
    echo "✅ Fortgesetzt"
}

# Druck stoppen
cmd_stop() {
    check_mqtt
    read -p "❌ Druck wirklich abbrechen? (j/N) " confirm
    if [ "$confirm" = "j" ] || [ "$confirm" = "J" ]; then
        echo "Breche Druck ab..."
        send_mqtt '{"print": {"command": "stop"}}'
        echo "✅ Abgebrochen"
    else
        echo "Abbruch verworfen"
    fi
}

# Licht steuern
cmd_light() {
    check_mqtt
    local mode="${1:-}"
    if [ -z "$mode" ]; then
        echo "Fehler: on oder off angeben"
        echo "Verwendung: light on|off"
        exit 1
    fi
    
    case "$mode" in
        on|1)
            echo "💡 Schalte Licht an..."
            send_mqtt '{"print": {"command": "ledctrl", "led_node": "chamber_light", "led_mode": "on"}}'
            ;;
        off|0)
            echo "🌑 Schalte Licht aus..."
            send_mqtt '{"print": {"command": "ledctrl", "led_node": "chamber_light", "led_mode": "off"}}'
            ;;
        *)
            echo "Fehler: on oder off angeben"
            exit 1
            ;;
    esac
    echo "✅ Fertig"
}

# Lüfter steuern
cmd_fans() {
    check_mqtt
    local speed="${1:-}"
    if [ -z "$speed" ]; then
        echo "Fehler: Geschwindigkeit (0-15) angeben"
        echo "Verwendung: fans <0-15>"
        exit 1
    fi
    
    # Konvertiere 0-15 zu 0-255
    local pwm=$((speed * 17))
    [ $pwm -gt 255 ] && pwm=255
    
    echo "🌪️  Setze Lüfter auf $speed (PWM: $pwm)..."
    send_mqtt "{\"print\": {\"command\": \"gcode_line\", \"param\": \"M106 S$pwm\"}}"
    echo "✅ Fertig"
}

# Rohe MQTT-Nachrichten
cmd_raw() {
    check_mqtt
    echo "🔴 Zeige rohe MQTT-Nachrichten (Strg+C zum Beenden)..."
    mosquitto_sub \
        -h "$HOST" \
        -p "$PORT" \
        -u "$SERIAL" \
        -P "$ACCESS_CODE" \
        -t "$REPORT_TOPIC" \
        --tls-version tlsv1.2 2>/dev/null | while read line; do
        echo "$line" | python3 -m json.tool 2>/dev/null || echo "$line"
    done
}

# Benachrichtigungs-Modus
cmd_notify() {
    check_mqtt
    echo "🔔 Starte Überwachung mit Benachrichtigungen..."
    
    local last_state=""
    
    while true; do
        local json=$(receive_mqtt 5)
        local state=$(echo "$json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('print',{}).get('gcode_state','UNKNOWN'))" 2>/dev/null)
        local percent=$(echo "$json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('print',{}).get('mc_percent',0))" 2>/dev/null)
        local error=$(echo "$json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('print',{}).get('print_error',0))" 2>/dev/null)
        local filename=$(echo "$json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('print',{}).get('filename','Unbekannt'))" 2>/dev/null)
        
        # Bei Status-Änderung benachrichtigen
        if [ "$state" != "$last_state" ]; then
            case "$state" in
                FINISH)
                    echo "✅ DRUCK FERTIG: $filename"
                    # Hier könnte Telegram-Integration kommen
                    ;;
                FAILED)
                    echo "❌ DRUCK FEHLGESCHLAGEN: $filename"
                    ;;
                PAUSE)
                    echo "⏸️  Druck pausiert: $filename"
                    ;;
                RUNNING)
                    echo "🟢 Druck gestartet/läuft: $filename ($percent%)"
                    ;;
            esac
            last_state="$state"
        fi
        
        # Bei Fehler sofort benachrichtigen
        if [ "$error" != "0" ] && [ -n "$error" ]; then
            echo "⚠️  FEHLER Code $error beim Drucken!"
        fi
        
        # Alle 10% Fortschritt melden
        if [ $((percent % 10)) -eq 0 ] && [ "$percent" != "0" ] && [ "$state" = "RUNNING" ]; then
            echo "📊 Fortschritt: $percent%"
        fi
        
        sleep 30
    done
}

# Hauptprogramm
main() {
    local cmd="${1:-status}"
    shift || true
    
    case "$cmd" in
        help|--help|-h)
            show_help
            ;;
        status)
            cmd_status
            ;;
        progress)
            cmd_progress
            ;;
        temps)
            cmd_temps
            ;;
        watch)
            cmd_watch
            ;;
        pause)
            cmd_pause
            ;;
        resume)
            cmd_resume
            ;;
        stop)
            cmd_stop
            ;;
        light)
            cmd_light "$@"
            ;;
        fans)
            cmd_fans "$@"
            ;;
        raw)
            cmd_raw
            ;;
        notify)
            cmd_notify
            ;;
        *)
            echo "Unbekannter Befehl: $cmd"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

main "$@"
