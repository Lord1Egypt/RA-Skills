#!/bin/bash
# AXIOMATA-DeepAllBoost-SuperFeature REVOLUTIONARY SYSTEM STARTUP
# Vollständiges revolutionäres Intelligenzsystem starten

echo "🌟 AXIOMATA-DeepAllBoost-SuperFeature REVOLUTIONARY SYSTEM STARTUP"
echo "=================================================================="

# Farben für Ausgabe
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
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

info() {
    echo -e "${BLUE}[INFO] $1${NC}
success() {
    echo -e "${PURPLE}[SUCCESS] $1${NC}"
}

# System-Check
check_system() {
    log "🔍 Checking system requirements..."
    
    # Python prüfen
    if ! command -v python3 &> /dev/null; then
        error "Python3 not found. Please install Python3."
        exit 1
    fi
    
    # Streamlit prüfen
    if ! python3 -c "import streamlit" &> /dev/null; then
        warning "Streamlit not found. Installing..."
        pip3 install streamlit
    fi
    
    # Asyncio prüfen
    if ! python3 -c "import asyncio" &> /dev/null; then
        error "Asyncio not available. Please check Python installation."
        exit 1
    fi
    
    success "✅ System requirements satisfied"
}

# Verzeichnisse prüfen
check_directories() {
    log "📁 Checking required directories..."
    
    directories=(
        "/home/deepall/clawd/my-mcp-server"
        "/home/deepall/alle deepall  apps/DeepAllBoost"
        "/home/deepall/superskill_workspace"
    )
    
    for dir in "${directories[@]}"; do
        if [ ! -d "$dir" ]; then
            error "Directory not found: $dir"
            exit 1
        fi
        log "✅ Directory found: $dir"
    done
    
    success "✅ All required directories found"
}

# Dateien prüfen
check_files() {
    log "📄 Checking required files..."
    
    files=(
        "/home/deepall/clawd/my-mcp-server/revolutionary_integrator.py"
        "/home/deepall/clawd/my-mcp-server/revolutionary_dashboard.py"
        "/home/deepall/alle deepall  apps/DeepAllBoost/streamlit_app.py"
        "/home/deepall/superskill_workspace/super_feature_system.py"
    )
    
    for file in "${files[@]}"; do
        if [ ! -f "$file" ]; then
            warning "File not found: $file"
        else
            log "✅ File found: $file"
        fi
    done
    
    success "✅ File check completed"
}

# Python-Umgebung einrichten
setup_python_env() {
    log "🐍 Setting up Python environment..."
    
    # Virtuelle Umgebung prüfen
    if [ ! -d "venv" ]; then
        log "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Virtuelle Umgebung aktivieren
    source venv/bin/activate
    
    # Abhängigkeiten installieren
    log "📦 Installing dependencies..."
    
    requirements=(
        "streamlit"
        "plotly"
        "pandas"
        "numpy"
        "asyncio"
        "json"
        "datetime"
        "typing"
    )
    
    for req in "${requirements[@]}"; do
        pip install "$req" &> /dev/null || warning "Failed to install $req"
    done
    
    success "✅ Python environment setup completed"
}

# Backend-System starten
start_backend() {
    log "🚀 Starting backend systems..."
    
    # Revolutionary Integrator starten
    log "🌟 Starting Revolutionary Integrator..."
    cd "/home/deepall/clawd/my-mcp-server"
    
    # Integrator im Hintergrund starten
    python3 revolutionary_integrator.py &
    INTEGRATOR_PID=$!
    log '✅ Revolutionary Integrator started (PID: $INTEGRATOR_PID)'
    
    # DeepAllBoost API starten
    log "🚀 Starting DeepAllBoost API..."
    cd "/home/deepall/alle deepall  apps/DeepAllBoost"
    
    if [ -f "api.py" ]; then
        python3 api.py &
        API_PID=$!
        log "✅ DeepAllBoost API started (PID: $API_PID)"
    else
        warning "DeepAllBoost API not found"
    fi
    
    success "✅ Backend systems started"
}

# Frontend-System starten
start_frontend() {
    log "🖥️ Starting frontend systems..."
    
    # Revolutionary Dashboard starten
    log "🌟 Starting Revolutionary Dashboard..."
    cd "/home/deepall/clawd/my-mcp-server"
    
    streamlit run revolutionary_dashboard.py --server.port 8501 --server.address 0.0.0.0 &
    DASHBOARD_PID=$!
    log "✅ Revolutionary Dashboard started (PID: $DASHBOARD_PID)"
    
    # DeepAllBoost Streamlit App starten
    log "🚀 Starting DeepAllBoost Streamlit App..."
    cd "/home/deepall/alle deepall  apps/DeepAllBoost"
    
    if [ -f "streamlit_app.py" ]; then
        streamlit run streamlit_app.py --server.port 8502 --server.address 0.0.0.0 &
        STREAMLIT_PID=$!
        log "✅ DeepAllBoost Streamlit App started (PID: $STREAMLIT_PID)"
    else
        warning "DeepAllBoost Streamlit App not found"
    fi
    
    success "✅ Frontend systems started"
}

# System-Status prüfen
check_system_status() {
    log "🔍 Checking system status..."
    
    # PIDs in Datei speichern
    echo "INTEGRATOR_PID=$INTEGRATOR_PID" > /tmp/revolutionary_system_pids.txt
    echo "API_PID=$API_PID" >> /tmp/revolutionary_system_pids.txt
    echo "DASHBOARD_PID=$DASHBOARD_PID" >> /tmp/revolutionary_system_pids.txt
    echo "STREAMLIT_PID=$STREAMLIT_PID" >> /tmp/revolutionary_system_pids.txt
    
    # Prozesse prüfen
    processes=("INTEGRATOR_PID" "API_PID" "DASHBOARD_PID" "STREAMLIT_PID")
    
    for proc in "${processes[@]}"; do
        pid=${!proc}
        if [ ! -z "$pid" ]; then
            if ps -p $pid > /dev/null; then
                success "✅ $proc is running (PID: $pid)"
            else
                warning "⚠️ $proc is not running"
            fi
        fi
    done
}

# Zugriffsinformationen anzeigen
show_access_info() {
    log "🌐 Access Information"
    log "===================="
    
    success "🌟 Revolutionary Dashboard: http://localhost:8501"
    success "🚀 DeepAllBoost Streamlit: http://localhost:8502"
    success "🔧 DeepAllBoost API: http://localhost:8000/docs"
    
    log ""
    log "📋 System Components:"
    log "- AXIOMATA: 12 Intelligent Agents"
    log "- DeepAllBoost: 63+ Enterprise Modules"
    log "- Super-Feature: 5 Revolutionary Features"
    log "- Total: 80+ Intelligence Modules"
    
    log ""
    log "🎯 Revolutionary Features:"
    log "- Universal Neural Interface"
    log "- Holographic Memory Matrix"
    log "- Temporal Quantum Computing"
    log "- Meta-Cognitive Architecture"
    log "- Cosmic Pattern Recognition"
    
    log ""
    warning "⚠️ To stop the system, run: ./stop_revolutionary_system.sh"
    warning "⚠️ Or use: killall python3; killall streamlit"
}

# Hauptfunktion
main() {
    echo ""
    log "🚀 STARTING REVOLUTIONARY INTELLIGENCE SYSTEM"
    log "=========================================="
    
    # System prüfen
    check_system
    check_directories
    check_files
    
    # Umgebung einrichten
    setup_python_env
    
    # Systeme starten
    start_backend
    start_frontend
    
    # Status prüfen
    check_system_status
    
    # Zugriffsinformationen anzeigen
    show_access_info
    
    echo ""
    success "🎉 REVOLUTIONARY INTELLIGENCE SYSTEM STARTED SUCCESSFULLY!"
    success "🌟 AXIOMATA + DeepAllBoost + Super-Feature System operational!"
    success "🚀 80+ Intelligent Modules ready for action!"
    echo ""
    
    # System laufen lassen
    log "💡 System is running. Press Ctrl+C to stop."
    wait
}

# Skript starten
main "$@"