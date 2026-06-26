#!/bin/bash
# AXIOMATA-DeepAllBoost-SuperFeature REVOLUTIONARY SYSTEM STOP
# Vollständiges revolutionäres Intelligenzsystem stoppen

echo "🛑 AXIOMATA-DeepAllBoost-SuperFeature REVOLUTIONARY SYSTEM STOP"
echo "============================================================"

# Farben für Ausgabe
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Logging Funktion
log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

success() {
    echo -e "${PURPLE}[SUCCESS] $1${NC}"
}

# Prozesse stoppen
stop_processes() {
    log "🛑 Stopping revolutionary system processes..."
    
    # PIDs aus Datei laden
    if [ -f "/tmp/revolutionary_system_pids.txt" ]; then
        source /tmp/revolutionary_system_pids.txt
        
        # Einzelne Prozesse stoppen
        if [ ! -z "$INTEGRATOR_PID" ]; then
            if ps -p $INTEGRATOR_PID > /dev/null; then
                kill $INTEGRATOR_PID
                success "✅ Revolutionary Integrator stopped (PID: $INTEGRATOR_PID)"
            else
                warning "⚠️ Revolutionary Integrator not running"
            fi
        fi
        
        if [ ! -z "$API_PID" ]; then
            if ps -p $API_PID > /dev/null; then
                kill $API_PID
                success "✅ DeepAllBoost API stopped (PID: $API_PID)"
            else
                warning "⚠️ DeepAllBoost API not running"
            fi
        fi
        
        if [ ! -z "$DASHBOARD_PID" ]; then
            if ps -p $DASHBOARD_PID > /dev/null; then
                kill $DASHBOARD_PID
                success "✅ Revolutionary Dashboard stopped (PID: $DASHBOARD_PID)"
            else
                warning "⚠️ Revolutionary Dashboard not running"
            fi
        fi
        
        if [ ! -z "$STREAMLIT_PID" ]; then
            if ps -p $STREAMLIT_PID > /dev/null; then
                kill $STREAMLIT_PID
                success "✅ DeepAllBoost Streamlit stopped (PID: $STREAMLIT_PID)"
            else
                warning "⚠️ DeepAllBoost Streamlit not running"
            fi
        fi
        
        # PID-Datei löschen
        rm -f /tmp/revolutionary_system_pids.txt
    else
        warning "⚠️ No PID file found"
    fi
}

# Alle Python-Prozesse stoppen
stop_python_processes() {
    log "🐍 Stopping all Python processes..."
    
    # Python-Prozesse suchen und stoppen
    python_pids=$(pgrep -f "revolutionary_integrator.py|revolutionary_dashboard.py|streamlit_app.py|api.py")
    
    if [ ! -z "$python_pids" ]; then
        for pid in $python_pids; do
            if ps -p $pid > /dev/null; then
                kill $pid
                success "✅ Python process stopped (PID: $pid)"
            fi
        done
    else
        log "✅ No Python processes found"
    fi
}

# Alle Streamlit-Prozesse stoppen
stop_streamlit_processes() {
    log "🖥️ Stopping all Streamlit processes..."
    
    # Streamlit-Prozesse suchen und stoppen
    streamlit_pids=$(pgrep -f "streamlit")
    
    if [ ! -z "$streamlit_pids" ]; then
        for pid in $streamlit_pids; do
            if ps -p $pid > /dev/null; then
                kill $pid
                success "✅ Streamlit process stopped (PID: $pid)"
            fi
        done
    else
        log "✅ No Streamlit processes found"
    fi
}

# Ports prüfen und freigeben
check_ports() {
    log "🔍 Checking and releasing ports..."
    
    ports=(8000 8501 8502)
    
    for port in "${ports[@]}"; do
        # Port belegende Prozesse finden
        port_pids=$(lsof -ti :$port 2>/dev/null)
        
        if [ ! -z "$port_pids" ]; then
            for pid in $port_pids; do
                if ps -p $pid > /dev/null; then
                    kill $pid
                    success "✅ Port $port released (PID: $pid)"
                fi
            done
        else
            log "✅ Port $port is free"
        fi
    done
}

# System-Status prüfen
check_system_status() {
    log "🔍 Checking system status..."
    
    # Python-Prozesse prüfen
    python_count=$(pgrep -f "revolutionary_integrator.py|revolutionary_dashboard.py|streamlit_app.py|api.py" | wc -l)
    log "🐍 Python processes: $python_count"
    
    # Streamlit-Prozesse prüfen
    streamlit_count=$(pgrep -f "streamlit" | wc -l)
    log "🖥️ Streamlit processes: $streamlit_count"
    
    # Ports prüfen
    ports=(8000 8501 8502)
    for port in "${ports[@]}"; do
        if lsof -i :$port > /dev/null 2>&1; then
            warning "⚠️ Port $port is still in use"
        else
            success "✅ Port $port is free"
        fi
    done
}

# Hauptfunktion
main() {
    echo ""
    log "🛑 STOPPING REVOLUTIONARY INTELLIGENCE SYSTEM"
    log "=========================================="
    
    # Bestätigung anfordern
    echo -e "${YELLOW}Are you sure you want to stop the revolutionary system? (y/N)${NC}"
    read -r response
    if [[ ! "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        log "❌ Stop operation cancelled"
        exit 0
    fi
    
    # Prozesse stoppen
    stop_processes
    stop_python_processes
    stop_streamlit_processes
    
    # Ports freigeben
    check_ports
    
    # System-Status prüfen
    check_system_status
    
    echo ""
    success "🎉 REVOLUTIONARY INTELLIGENCE SYSTEM STOPPED SUCCESSFULLY!"
    success "🌟 All processes terminated and ports released"
    echo ""
}

# Skript starten
main "$@"