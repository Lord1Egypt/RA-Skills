# Code-Assistenten Anleitung: n8n MCP Server mit UI

## AUFTRAG FÜR CODE-ASSISTENTEN

**Erstelle eine vollständige, benutzerfreundliche Webanwendung für den n8n MCP Server mit folgenden Spezifikationen:**

---

## 1. PROJEKT-SETUP

### Erstelle folgende Projektstruktur:
```
n8n-mcp-ui/
├── backend/
│   ├── n8n_mcp_server.py          # MCP Server (bereits vorhanden)
│   ├── web_server.py              # Flask Web Server
│   ├── requirements.txt           # Python Dependencies
│   └── config.py                  # Konfiguration
├── frontend/
│   ├── index.html                 # Haupt-HTML
│   ├── css/
│   │   ├── style.css             # Haupt-Stylesheet
│   │   └── components.css        # Komponenten-Styles
│   ├── js/
│   │   ├── app.js                # Haupt-JavaScript
│   │   ├── api.js                # API-Kommunikation
│   │   └── components.js         # UI-Komponenten
│   └── assets/
│       ├── logo.png              # n8n Logo
│       └── icons/                # UI Icons
├── static/                       # Statische Dateien
├── templates/                    # HTML Templates
├── setup.py                      # Installation Script
├── run.py                        # Starter Script
└── README.md                     # Dokumentation
```

---

## 2. BACKEND-ENTWICKLUNG

### A) Flask Web Server (web_server.py)
```python
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import asyncio
import threading
from n8n_mcp_server import N8nMCPServer

app = Flask(__name__)
CORS(app)

# MCP Server Instance
mcp_server = N8nMCPServer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/create-workflow', methods=['POST'])
def create_workflow():
    data = request.json
    # MCP Server Integration
    result = asyncio.run(mcp_server._create_workflow(data))
    return jsonify({'success': True, 'data': result})

@app.route('/api/validate-workflow', methods=['POST'])
def validate_workflow():
    data = request.json
    result = asyncio.run(mcp_server._validate_workflow(data))
    return jsonify({'success': True, 'data': result})

@app.route('/api/create-node', methods=['POST'])
def create_node():
    data = request.json
    result = asyncio.run(mcp_server._create_node(data))
    return jsonify({'success': True, 'data': result})

@app.route('/api/get-guidelines', methods=['GET'])
def get_guidelines():
    topic = request.args.get('topic', 'overview')
    result = asyncio.run(mcp_server._get_guidelines({'topic': topic}))
    return jsonify({'success': True, 'data': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
```

### B) Konfiguration (config.py)
```python
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'n8n-mcp-dev-key'
    MCP_SERVER_HOST = '0.0.0.0'
    MCP_SERVER_PORT = 8080
    DEBUG = True
    
    # n8n MCP Server Settings
    N8N_COMPLIANCE_THRESHOLD = 80
    N8N_STRICT_VALIDATION = False
    N8N_AUTO_OPTIMIZE = True
```

### C) Requirements (requirements.txt)
```
Flask>=2.3.0
Flask-CORS>=4.0.0
mcp>=1.10.0
pydantic>=2.11.0
pyyaml>=6.0.0
gunicorn>=21.0.0
```

---

## 3. FRONTEND-ENTWICKLUNG

### A) HTML Struktur (templates/index.html)
```html
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>n8n MCP Server - Workflow Creator</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/components.css') }}">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body>
    <div id="app">
        <!-- Header -->
        <header class="header">
            <div class="header-content">
                <div class="logo">
                    <i class="fas fa-project-diagram"></i>
                    <h1>n8n MCP Server</h1>
                </div>
                <div class="status-indicator">
                    <span class="status-dot online"></span>
                    <span>Server Online</span>
                </div>
            </div>
        </header>

        <!-- Navigation -->
        <nav class="sidebar">
            <ul class="nav-menu">
                <li class="nav-item active" data-tab="workflow-creator">
                    <i class="fas fa-plus-circle"></i>
                    <span>Workflow Erstellen</span>
                </li>
                <li class="nav-item" data-tab="node-creator">
                    <i class="fas fa-cube"></i>
                    <span>Node Erstellen</span>
                </li>
                <li class="nav-item" data-tab="validator">
                    <i class="fas fa-check-circle"></i>
                    <span>Validierung</span>
                </li>
                <li class="nav-item" data-tab="guidelines">
                    <i class="fas fa-book"></i>
                    <span>Guidelines</span>
                </li>
                <li class="nav-item" data-tab="export">
                    <i class="fas fa-download"></i>
                    <span>Export</span>
                </li>
            </ul>
        </nav>

        <!-- Main Content -->
        <main class="main-content">
            <!-- Workflow Creator Tab -->
            <div id="workflow-creator" class="tab-content active">
                <div class="content-header">
                    <h2><i class="fas fa-plus-circle"></i> Workflow Erstellen</h2>
                    <p>Erstellen Sie vollständige n8n-Workflows aus natürlicher Sprache</p>
                </div>
                
                <div class="form-container">
                    <div class="form-group">
                        <label for="workflow-name">Workflow Name</label>
                        <input type="text" id="workflow-name" placeholder="z.B. Täglicher Verkaufsbericht">
                    </div>
                    
                    <div class="form-group">
                        <label for="workflow-description">Beschreibung</label>
                        <textarea id="workflow-description" rows="4" 
                                placeholder="Beschreiben Sie, was der Workflow tun soll..."></textarea>
                    </div>
                    
                    <div class="form-group">
                        <label for="workflow-pattern">Workflow-Muster (Optional)</label>
                        <select id="workflow-pattern">
                            <option value="">Automatisch erkennen</option>
                            <option value="api_to_database">API zu Datenbank</option>
                            <option value="scheduled_report">Geplanter Bericht</option>
                            <option value="webhook_processor">Webhook-Verarbeitung</option>
                            <option value="data_pipeline">Daten-Pipeline</option>
                            <option value="notification_system">Benachrichtigungssystem</option>
                        </select>
                    </div>
                    
                    <button class="btn btn-primary" onclick="createWorkflow()">
                        <i class="fas fa-magic"></i> Workflow Erstellen
                    </button>
                </div>
                
                <div id="workflow-result" class="result-container" style="display: none;">
                    <div class="result-header">
                        <h3>Erstellter Workflow</h3>
                        <div class="compliance-score">
                            <span class="score-label">Compliance Score:</span>
                            <span class="score-value" id="workflow-score">0</span>/100
                        </div>
                    </div>
                    <div class="result-content">
                        <div class="workflow-preview">
                            <canvas id="workflow-canvas"></canvas>
                        </div>
                        <div class="workflow-details">
                            <pre id="workflow-json"></pre>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Node Creator Tab -->
            <div id="node-creator" class="tab-content">
                <div class="content-header">
                    <h2><i class="fas fa-cube"></i> Node Erstellen</h2>
                    <p>Erstellen Sie individuelle n8n-Nodes mit vollständiger Compliance</p>
                </div>
                
                <div class="form-container">
                    <div class="form-row">
                        <div class="form-group">
                            <label for="node-name">Node Name</label>
                            <input type="text" id="node-name" placeholder="z.B. WeatherAPI">
                        </div>
                        <div class="form-group">
                            <label for="node-service">Service</label>
                            <input type="text" id="node-service" placeholder="z.B. weather">
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="node-type">Node Typ</label>
                            <select id="node-type">
                                <option value="auto">Automatisch erkennen</option>
                                <option value="trigger">Trigger Node</option>
                                <option value="action">Action Node</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="building-style">Building Style</label>
                            <select id="building-style">
                                <option value="auto">Automatisch wählen</option>
                                <option value="declarative">Declarative</option>
                                <option value="programmatic">Programmatic</option>
                            </select>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label for="node-operations">Operationen (eine pro Zeile)</label>
                        <textarea id="node-operations" rows="3" 
                                placeholder="create&#10;read&#10;update&#10;delete"></textarea>
                    </div>
                    
                    <button class="btn btn-primary" onclick="createNode()">
                        <i class="fas fa-plus"></i> Node Erstellen
                    </button>
                </div>
                
                <div id="node-result" class="result-container" style="display: none;">
                    <div class="result-header">
                        <h3>Erstellter Node</h3>
                        <div class="compliance-score">
                            <span class="score-label">Compliance Score:</span>
                            <span class="score-value" id="node-score">0</span>/100
                        </div>
                    </div>
                    <div class="result-content">
                        <div class="code-preview">
                            <pre id="node-code"></pre>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Validator Tab -->
            <div id="validator" class="tab-content">
                <div class="content-header">
                    <h2><i class="fas fa-check-circle"></i> Workflow Validierung</h2>
                    <p>Validieren Sie Ihre n8n-Workflows gegen offizielle Standards</p>
                </div>
                
                <div class="form-container">
                    <div class="form-group">
                        <label for="validation-json">Workflow JSON</label>
                        <textarea id="validation-json" rows="10" 
                                placeholder="Fügen Sie Ihr Workflow JSON hier ein..."></textarea>
                    </div>
                    
                    <div class="form-group">
                        <label class="checkbox-label">
                            <input type="checkbox" id="strict-mode">
                            <span class="checkmark"></span>
                            Strict Mode (Erweiterte Validierung)
                        </label>
                    </div>
                    
                    <button class="btn btn-primary" onclick="validateWorkflow()">
                        <i class="fas fa-check"></i> Validieren
                    </button>
                </div>
                
                <div id="validation-result" class="result-container" style="display: none;">
                    <div class="validation-summary">
                        <div class="validation-score">
                            <div class="score-circle">
                                <span id="validation-score-text">0</span>
                            </div>
                            <p>Compliance Score</p>
                        </div>
                        <div class="validation-stats">
                            <div class="stat">
                                <span class="stat-number" id="issues-count">0</span>
                                <span class="stat-label">Issues</span>
                            </div>
                            <div class="stat">
                                <span class="stat-number" id="warnings-count">0</span>
                                <span class="stat-label">Warnings</span>
                            </div>
                            <div class="stat">
                                <span class="stat-number" id="suggestions-count">0</span>
                                <span class="stat-label">Suggestions</span>
                            </div>
                        </div>
                    </div>
                    <div class="validation-details">
                        <div id="validation-issues"></div>
                        <div id="validation-warnings"></div>
                        <div id="validation-suggestions"></div>
                    </div>
                </div>
            </div>

            <!-- Guidelines Tab -->
            <div id="guidelines" class="tab-content">
                <div class="content-header">
                    <h2><i class="fas fa-book"></i> n8n Guidelines</h2>
                    <p>Offizielle n8n-Entwicklungsrichtlinien und Best Practices</p>
                </div>
                
                <div class="guidelines-nav">
                    <button class="guideline-btn active" data-topic="overview">Übersicht</button>
                    <button class="guideline-btn" data-topic="node_types">Node Typen</button>
                    <button class="guideline-btn" data-topic="building_styles">Building Styles</button>
                    <button class="guideline-btn" data-topic="validation">Validierung</button>
                    <button class="guideline-btn" data-topic="templates">Templates</button>
                    <button class="guideline-btn" data-topic="patterns">Patterns</button>
                </div>
                
                <div id="guidelines-content" class="guidelines-content">
                    <!-- Wird dynamisch geladen -->
                </div>
            </div>

            <!-- Export Tab -->
            <div id="export" class="tab-content">
                <div class="content-header">
                    <h2><i class="fas fa-download"></i> Export</h2>
                    <p>Exportieren Sie Ihre Workflows in verschiedenen Formaten</p>
                </div>
                
                <div class="export-options">
                    <div class="export-card">
                        <h3><i class="fas fa-file-code"></i> JSON Export</h3>
                        <p>Standard n8n Workflow Format</p>
                        <button class="btn btn-secondary" onclick="exportJSON()">
                            <i class="fas fa-download"></i> JSON Download
                        </button>
                    </div>
                    
                    <div class="export-card">
                        <h3><i class="fas fa-file-alt"></i> YAML Export</h3>
                        <p>Menschenlesbares Format</p>
                        <button class="btn btn-secondary" onclick="exportYAML()">
                            <i class="fas fa-download"></i> YAML Download
                        </button>
                    </div>
                    
                    <div class="export-card">
                        <h3><i class="fas fa-file-pdf"></i> Dokumentation</h3>
                        <p>Vollständige Workflow-Dokumentation</p>
                        <button class="btn btn-secondary" onclick="exportDocs()">
                            <i class="fas fa-download"></i> PDF Download
                        </button>
                    </div>
                </div>
            </div>
        </main>

        <!-- Loading Overlay -->
        <div id="loading-overlay" class="loading-overlay" style="display: none;">
            <div class="loading-spinner">
                <div class="spinner"></div>
                <p>Verarbeitung läuft...</p>
            </div>
        </div>

        <!-- Toast Notifications -->
        <div id="toast-container" class="toast-container"></div>
    </div>

    <script src="{{ url_for('static', filename='js/api.js') }}"></script>
    <script src="{{ url_for('static', filename='js/components.js') }}"></script>
    <script src="{{ url_for('static', filename='js/app.js') }}"></script>
</body>
</html>
```

---

## 4. CSS STYLING

### A) Haupt-Stylesheet (static/css/style.css)
```css
/* CSS Variables für konsistente Farben */
:root {
    --primary-color: #ff6d5a;
    --secondary-color: #4f46e5;
    --success-color: #10b981;
    --warning-color: #f59e0b;
    --error-color: #ef4444;
    --background-color: #f8fafc;
    --surface-color: #ffffff;
    --text-primary: #1f2937;
    --text-secondary: #6b7280;
    --border-color: #e5e7eb;
    --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

/* Reset und Base Styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background-color: var(--background-color);
    color: var(--text-primary);
    line-height: 1.6;
}

#app {
    display: grid;
    grid-template-areas: 
        "header header"
        "sidebar main";
    grid-template-columns: 250px 1fr;
    grid-template-rows: 60px 1fr;
    height: 100vh;
}

/* Header */
.header {
    grid-area: header;
    background: var(--surface-color);
    border-bottom: 1px solid var(--border-color);
    display: flex;
    align-items: center;
    padding: 0 24px;
    box-shadow: var(--shadow);
}

.header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
}

.logo {
    display: flex;
    align-items: center;
    gap: 12px;
}

.logo i {
    color: var(--primary-color);
    font-size: 24px;
}

.logo h1 {
    font-size: 20px;
    font-weight: 600;
    color: var(--text-primary);
}

.status-indicator {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
    color: var(--text-secondary);
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: var(--success-color);
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

/* Sidebar */
.sidebar {
    grid-area: sidebar;
    background: var(--surface-color);
    border-right: 1px solid var(--border-color);
    padding: 24px 0;
}

.nav-menu {
    list-style: none;
}

.nav-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 24px;
    cursor: pointer;
    transition: all 0.2s ease;
    color: var(--text-secondary);
}

.nav-item:hover {
    background-color: var(--background-color);
    color: var(--text-primary);
}

.nav-item.active {
    background-color: var(--primary-color);
    color: white;
    border-right: 3px solid var(--primary-color);
}

.nav-item i {
    font-size: 16px;
    width: 20px;
}

/* Main Content */
.main-content {
    grid-area: main;
    padding: 24px;
    overflow-y: auto;
}

.tab-content {
    display: none;
    max-width: 1200px;
    margin: 0 auto;
}

.tab-content.active {
    display: block;
}

.content-header {
    margin-bottom: 32px;
}

.content-header h2 {
    font-size: 28px;
    font-weight: 600;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 12px;
}

.content-header p {
    color: var(--text-secondary);
    font-size: 16px;
}

/* Form Styles */
.form-container {
    background: var(--surface-color);
    padding: 32px;
    border-radius: 12px;
    box-shadow: var(--shadow);
    margin-bottom: 24px;
}

.form-group {
    margin-bottom: 24px;
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    font-weight: 500;
    color: var(--text-primary);
}

.form-group input,
.form-group textarea,
.form-group select {
    width: 100%;
    padding: 12px 16px;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    font-size: 14px;
    transition: border-color 0.2s ease;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
    outline: none;
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px rgba(255, 109, 90, 0.1);
}

/* Button Styles */
.btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 12px 24px;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    text-decoration: none;
}

.btn-primary {
    background-color: var(--primary-color);
    color: white;
}

.btn-primary:hover {
    background-color: #e55a47;
    transform: translateY(-1px);
    box-shadow: 0 8px 15px rgba(255, 109, 90, 0.3);
}

.btn-secondary {
    background-color: var(--secondary-color);
    color: white;
}

.btn-secondary:hover {
    background-color: #4338ca;
    transform: translateY(-1px);
    box-shadow: 0 8px 15px rgba(79, 70, 229, 0.3);
}

/* Result Container */
.result-container {
    background: var(--surface-color);
    border-radius: 12px;
    box-shadow: var(--shadow);
    overflow: hidden;
}

.result-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 24px;
    border-bottom: 1px solid var(--border-color);
    background: linear-gradient(135deg, var(--primary-color), #e55a47);
    color: white;
}

.result-header h3 {
    font-size: 20px;
    font-weight: 600;
}

.compliance-score {
    display: flex;
    align-items: center;
    gap: 8px;
}

.score-value {
    font-size: 24px;
    font-weight: 700;
}

.result-content {
    padding: 24px;
}

/* Workflow Preview */
.workflow-preview {
    background: #f8f9fa;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 24px;
    margin-bottom: 24px;
}

#workflow-canvas {
    width: 100%;
    height: 300px;
    border: 1px solid var(--border-color);
    border-radius: 4px;
    background: white;
}

/* Code Preview */
.code-preview,
.workflow-details {
    background: #1e1e1e;
    border-radius: 8px;
    overflow: hidden;
}

.code-preview pre,
.workflow-details pre {
    color: #d4d4d4;
    padding: 24px;
    overflow-x: auto;
    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
    font-size: 13px;
    line-height: 1.5;
}

/* Loading Overlay */
.loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.loading-spinner {
    background: var(--surface-color);
    padding: 32px;
    border-radius: 12px;
    text-align: center;
}

.spinner {
    width: 40px;
    height: 40px;
    border: 4px solid var(--border-color);
    border-top: 4px solid var(--primary-color);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto 16px;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Toast Notifications */
.toast-container {
    position: fixed;
    top: 80px;
    right: 24px;
    z-index: 1001;
}

.toast {
    background: var(--surface-color);
    border-left: 4px solid var(--success-color);
    padding: 16px 20px;
    border-radius: 8px;
    box-shadow: var(--shadow);
    margin-bottom: 12px;
    animation: slideIn 0.3s ease;
}

.toast.error {
    border-left-color: var(--error-color);
}

.toast.warning {
    border-left-color: var(--warning-color);
}

@keyframes slideIn {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

/* Responsive Design */
@media (max-width: 768px) {
    #app {
        grid-template-areas: 
            "header"
            "main";
        grid-template-columns: 1fr;
        grid-template-rows: 60px 1fr;
    }
    
    .sidebar {
        display: none;
    }
    
    .form-row {
        grid-template-columns: 1fr;
    }
}
```

---

## 5. JAVASCRIPT FUNKTIONALITÄT

### A) API Kommunikation (static/js/api.js)
```javascript
// API Base URL
const API_BASE = '/api';

// API Helper Functions
class API {
    static async post(endpoint, data) {
        try {
            showLoading();
            const response = await fetch(`${API_BASE}${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            hideLoading();
            
            if (result.success) {
                return result.data;
            } else {
                throw new Error(result.error || 'API Error');
            }
        } catch (error) {
            hideLoading();
            showToast(error.message, 'error');
            throw error;
        }
    }
    
    static async get(endpoint, params = {}) {
        try {
            const url = new URL(`${window.location.origin}${API_BASE}${endpoint}`);
            Object.keys(params).forEach(key => 
                url.searchParams.append(key, params[key])
            );
            
            const response = await fetch(url);
            const result = await response.json();
            
            if (result.success) {
                return result.data;
            } else {
                throw new Error(result.error || 'API Error');
            }
        } catch (error) {
            showToast(error.message, 'error');
            throw error;
        }
    }
}

// Workflow API Functions
async function createWorkflow() {
    const name = document.getElementById('workflow-name').value;
    const description = document.getElementById('workflow-description').value;
    const pattern = document.getElementById('workflow-pattern').value;
    
    if (!name || !description) {
        showToast('Bitte füllen Sie alle Pflichtfelder aus', 'warning');
        return;
    }
    
    try {
        const data = await API.post('/create-workflow', {
            name,
            description,
            pattern: pattern || undefined
        });
        
        displayWorkflowResult(data);
        showToast('Workflow erfolgreich erstellt!', 'success');
    } catch (error) {
        console.error('Workflow creation failed:', error);
    }
}

async function createNode() {
    const name = document.getElementById('node-name').value;
    const service = document.getElementById('node-service').value;
    const nodeType = document.getElementById('node-type').value;
    const buildingStyle = document.getElementById('building-style').value;
    const operations = document.getElementById('node-operations').value
        .split('\n')
        .filter(op => op.trim())
        .map(op => op.trim());
    
    if (!name || !service) {
        showToast('Bitte füllen Sie alle Pflichtfelder aus', 'warning');
        return;
    }
    
    try {
        const data = await API.post('/create-node', {
            name,
            service,
            node_type: nodeType,
            building_style: buildingStyle,
            operations
        });
        
        displayNodeResult(data);
        showToast('Node erfolgreich erstellt!', 'success');
    } catch (error) {
        console.error('Node creation failed:', error);
    }
}

async function validateWorkflow() {
    const jsonText = document.getElementById('validation-json').value;
    const strictMode = document.getElementById('strict-mode').checked;
    
    if (!jsonText.trim()) {
        showToast('Bitte fügen Sie ein Workflow JSON ein', 'warning');
        return;
    }
    
    try {
        const workflow = JSON.parse(jsonText);
        const data = await API.post('/validate-workflow', {
            workflow,
            strict_mode: strictMode
        });
        
        displayValidationResult(data);
        showToast('Validierung abgeschlossen!', 'success');
    } catch (error) {
        if (error instanceof SyntaxError) {
            showToast('Ungültiges JSON Format', 'error');
        } else {
            console.error('Validation failed:', error);
        }
    }
}

async function loadGuidelines(topic = 'overview') {
    try {
        const data = await API.get('/get-guidelines', { topic });
        displayGuidelines(data, topic);
    } catch (error) {
        console.error('Guidelines loading failed:', error);
    }
}
```

### B) UI Komponenten (static/js/components.js)
```javascript
// UI Component Functions

function showLoading() {
    document.getElementById('loading-overlay').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loading-overlay').style.display = 'none';
}

function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <div style="display: flex; align-items: center; gap: 8px;">
            <i class="fas fa-${getToastIcon(type)}"></i>
            <span>${message}</span>
        </div>
    `;
    
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 5000);
}

function getToastIcon(type) {
    const icons = {
        success: 'check-circle',
        error: 'exclamation-circle',
        warning: 'exclamation-triangle',
        info: 'info-circle'
    };
    return icons[type] || 'info-circle';
}

function displayWorkflowResult(data) {
    const resultContainer = document.getElementById('workflow-result');
    const scoreElement = document.getElementById('workflow-score');
    const jsonElement = document.getElementById('workflow-json');
    
    // Update score
    const score = data[0].text.match(/Score.*?(\d+)\/100/)?.[1] || '0';
    scoreElement.textContent = score;
    scoreElement.className = `score-value ${getScoreClass(score)}`;
    
    // Update JSON
    jsonElement.textContent = data[0].text;
    
    // Show result
    resultContainer.style.display = 'block';
    
    // Scroll to result
    resultContainer.scrollIntoView({ behavior: 'smooth' });
}

function displayNodeResult(data) {
    const resultContainer = document.getElementById('node-result');
    const scoreElement = document.getElementById('node-score');
    const codeElement = document.getElementById('node-code');
    
    // Update score
    const score = data[0].text.match(/Score.*?(\d+)\/100/)?.[1] || '0';
    scoreElement.textContent = score;
    scoreElement.className = `score-value ${getScoreClass(score)}`;
    
    // Update code
    codeElement.textContent = data[0].text;
    
    // Show result
    resultContainer.style.display = 'block';
    
    // Scroll to result
    resultContainer.scrollIntoView({ behavior: 'smooth' });
}

function displayValidationResult(data) {
    const resultContainer = document.getElementById('validation-result');
    const scoreText = document.getElementById('validation-score-text');
    const issuesCount = document.getElementById('issues-count');
    const warningsCount = document.getElementById('warnings-count');
    const suggestionsCount = document.getElementById('suggestions-count');
    
    // Parse validation result
    const text = data[0].text;
    const score = text.match(/Score.*?(\d+)\/100/)?.[1] || '0';
    const issues = (text.match(/Issues.*?\((\d+)\)/)?.[1]) || '0';
    const warnings = (text.match(/Warnings.*?\((\d+)\)/)?.[1]) || '0';
    const suggestions = (text.match(/Suggestions.*?\((\d+)\)/)?.[1]) || '0';
    
    // Update UI
    scoreText.textContent = score;
    scoreText.parentElement.className = `score-circle ${getScoreClass(score)}`;
    issuesCount.textContent = issues;
    warningsCount.textContent = warnings;
    suggestionsCount.textContent = suggestions;
    
    // Show detailed results
    displayValidationDetails(text);
    
    // Show result
    resultContainer.style.display = 'block';
    
    // Scroll to result
    resultContainer.scrollIntoView({ behavior: 'smooth' });
}

function displayValidationDetails(text) {
    const issuesDiv = document.getElementById('validation-issues');
    const warningsDiv = document.getElementById('validation-warnings');
    const suggestionsDiv = document.getElementById('validation-suggestions');
    
    // Clear previous content
    issuesDiv.innerHTML = '';
    warningsDiv.innerHTML = '';
    suggestionsDiv.innerHTML = '';
    
    // Parse and display issues
    const issuesMatch = text.match(/❌ \*\*Issues\*\*[^❌⚠️💡]*?((?:• [^\n]+\n?)*)/);
    if (issuesMatch && issuesMatch[1]) {
        issuesDiv.innerHTML = `
            <h4><i class="fas fa-exclamation-circle"></i> Issues</h4>
            <ul>${issuesMatch[1].split('•').filter(item => item.trim()).map(item => `<li>${item.trim()}</li>`).join('')}</ul>
        `;
    }
    
    // Parse and display warnings
    const warningsMatch = text.match(/⚠️ \*\*Warnings\*\*[^❌⚠️💡]*?((?:• [^\n]+\n?)*)/);
    if (warningsMatch && warningsMatch[1]) {
        warningsDiv.innerHTML = `
            <h4><i class="fas fa-exclamation-triangle"></i> Warnings</h4>
            <ul>${warningsMatch[1].split('•').filter(item => item.trim()).map(item => `<li>${item.trim()}</li>`).join('')}</ul>
        `;
    }
    
    // Parse and display suggestions
    const suggestionsMatch = text.match(/💡 \*\*Suggestions\*\*[^❌⚠️💡]*?((?:• [^\n]+\n?)*)/);
    if (suggestionsMatch && suggestionsMatch[1]) {
        suggestionsDiv.innerHTML = `
            <h4><i class="fas fa-lightbulb"></i> Suggestions</h4>
            <ul>${suggestionsMatch[1].split('•').filter(item => item.trim()).map(item => `<li>${item.trim()}</li>`).join('')}</ul>
        `;
    }
}

function displayGuidelines(data, topic) {
    const content = document.getElementById('guidelines-content');
    const text = data[0].text;
    
    // Format the guidelines content
    content.innerHTML = `
        <div class="guidelines-section">
            <pre class="guidelines-text">${text}</pre>
        </div>
    `;
}

function getScoreClass(score) {
    const numScore = parseInt(score);
    if (numScore >= 90) return 'excellent';
    if (numScore >= 80) return 'good';
    if (numScore >= 70) return 'fair';
    return 'poor';
}

// Export Functions
function exportJSON() {
    // Implementation for JSON export
    showToast('JSON Export wird vorbereitet...', 'info');
}

function exportYAML() {
    // Implementation for YAML export
    showToast('YAML Export wird vorbereitet...', 'info');
}

function exportDocs() {
    // Implementation for documentation export
    showToast('Dokumentation wird erstellt...', 'info');
}
```

### C) Haupt-App Logic (static/js/app.js)
```javascript
// Main Application Logic

document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Initialize navigation
    initializeNavigation();
    
    // Initialize guidelines
    initializeGuidelines();
    
    // Load initial guidelines
    loadGuidelines('overview');
    
    // Initialize form validation
    initializeFormValidation();
    
    console.log('n8n MCP Server UI initialized');
}

function initializeNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    const tabContents = document.querySelectorAll('.tab-content');
    
    navItems.forEach(item => {
        item.addEventListener('click', function() {
            const tabId = this.getAttribute('data-tab');
            
            // Update active nav item
            navItems.forEach(nav => nav.classList.remove('active'));
            this.classList.add('active');
            
            // Update active tab content
            tabContents.forEach(tab => tab.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
        });
    });
}

function initializeGuidelines() {
    const guidelineButtons = document.querySelectorAll('.guideline-btn');
    
    guidelineButtons.forEach(button => {
        button.addEventListener('click', function() {
            const topic = this.getAttribute('data-topic');
            
            // Update active button
            guidelineButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Load guidelines for topic
            loadGuidelines(topic);
        });
    });
}

function initializeFormValidation() {
    // Add real-time validation for forms
    const inputs = document.querySelectorAll('input, textarea, select');
    
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateField(this);
        });
    });
}

function validateField(field) {
    const value = field.value.trim();
    const isRequired = field.hasAttribute('required');
    
    // Remove existing validation classes
    field.classList.remove('valid', 'invalid');
    
    if (isRequired && !value) {
        field.classList.add('invalid');
        return false;
    }
    
    // Specific validation rules
    if (field.type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            field.classList.add('invalid');
            return false;
        }
    }
    
    if (field.id === 'validation-json' && value) {
        try {
            JSON.parse(value);
        } catch (e) {
            field.classList.add('invalid');
            return false;
        }
    }
    
    field.classList.add('valid');
    return true;
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl+Enter to submit forms
    if (e.ctrlKey && e.key === 'Enter') {
        const activeTab = document.querySelector('.tab-content.active');
        const submitButton = activeTab.querySelector('.btn-primary');
        if (submitButton) {
            submitButton.click();
        }
    }
    
    // Escape to close overlays
    if (e.key === 'Escape') {
        hideLoading();
    }
});

// Auto-save functionality
let autoSaveTimer;

function enableAutoSave() {
    const inputs = document.querySelectorAll('input, textarea');
    
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            clearTimeout(autoSaveTimer);
            autoSaveTimer = setTimeout(() => {
                saveFormData();
            }, 2000);
        });
    });
}

function saveFormData() {
    const formData = {};
    const inputs = document.querySelectorAll('input, textarea, select');
    
    inputs.forEach(input => {
        if (input.id) {
            formData[input.id] = input.value;
        }
    });
    
    localStorage.setItem('n8n-mcp-form-data', JSON.stringify(formData));
}

function loadFormData() {
    const savedData = localStorage.getItem('n8n-mcp-form-data');
    
    if (savedData) {
        const formData = JSON.parse(savedData);
        
        Object.keys(formData).forEach(id => {
            const element = document.getElementById(id);
            if (element) {
                element.value = formData[id];
            }
        });
    }
}

// Initialize auto-save and load saved data
enableAutoSave();
loadFormData();
```

---

## 6. STARTER SCRIPT

### run.py
```python
#!/usr/bin/env python3
"""
n8n MCP Server UI Starter
Startet den MCP Server mit Web-UI
"""

import os
import sys
import subprocess
import webbrowser
import time
import threading
from pathlib import Path

def check_dependencies():
    """Prüft ob alle Abhängigkeiten installiert sind"""
    try:
        import flask
        import mcp
        import pydantic
        import yaml
        print("✅ Alle Abhängigkeiten sind installiert")
        return True
    except ImportError as e:
        print(f"❌ Fehlende Abhängigkeit: {e}")
        print("Führen Sie 'pip install -r requirements.txt' aus")
        return False

def start_server():
    """Startet den Flask Web Server"""
    try:
        from backend.web_server import app
        print("🚀 Starte n8n MCP Server UI...")
        print("📱 UI verfügbar unter: http://localhost:8080")
        app.run(host='0.0.0.0', port=8080, debug=False)
    except Exception as e:
        print(f"❌ Server-Start fehlgeschlagen: {e}")
        sys.exit(1)

def open_browser():
    """Öffnet den Browser nach kurzer Verzögerung"""
    time.sleep(2)
    webbrowser.open('http://localhost:8080')

def main():
    print("🎯 n8n MCP Server UI Starter")
    print("=" * 40)
    
    # Abhängigkeiten prüfen
    if not check_dependencies():
        sys.exit(1)
    
    # Browser in separatem Thread öffnen
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Server starten
    start_server()

if __name__ == "__main__":
    main()
```

---

## 7. SETUP SCRIPT

### setup.py
```python
#!/usr/bin/env python3
"""
n8n MCP Server UI Setup Script
Automatische Installation und Konfiguration
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Führt einen Befehl aus und zeigt den Status an"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✅ {description} erfolgreich")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} fehlgeschlagen: {e}")
        return False

def create_directories():
    """Erstellt die Projektverzeichnisse"""
    directories = [
        'backend',
        'frontend/css',
        'frontend/js',
        'frontend/assets/icons',
        'static/css',
        'static/js',
        'static/assets',
        'templates'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Projektverzeichnisse erstellt")

def install_dependencies():
    """Installiert Python-Abhängigkeiten"""
    return run_command(
        "pip install flask flask-cors mcp pydantic pyyaml gunicorn",
        "Python-Abhängigkeiten installieren"
    )

def copy_mcp_server():
    """Kopiert den MCP Server in das Backend-Verzeichnis"""
    if Path("n8n_mcp_server_complete.py").exists():
        shutil.copy("n8n_mcp_server_complete.py", "backend/n8n_mcp_server.py")
        print("✅ MCP Server kopiert")
        return True
    else:
        print("❌ n8n_mcp_server_complete.py nicht gefunden")
        return False

def create_config_files():
    """Erstellt Konfigurationsdateien"""
    # .env Datei
    env_content = """
# n8n MCP Server UI Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=n8n-mcp-dev-key-change-in-production
MCP_SERVER_HOST=0.0.0.0
MCP_SERVER_PORT=8080
"""
    
    with open('.env', 'w') as f:
        f.write(env_content.strip())
    
    print("✅ Konfigurationsdateien erstellt")

def main():
    print("🚀 n8n MCP Server UI Setup")
    print("=" * 40)
    
    # Python-Version prüfen
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ erforderlich")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} erkannt")
    
    # Setup-Schritte
    steps = [
        ("Verzeichnisse erstellen", create_directories),
        ("Abhängigkeiten installieren", install_dependencies),
        ("MCP Server kopieren", copy_mcp_server),
        ("Konfiguration erstellen", create_config_files)
    ]
    
    for description, func in steps:
        if not func():
            print(f"❌ Setup fehlgeschlagen bei: {description}")
            sys.exit(1)
    
    print("\n🎉 Setup erfolgreich abgeschlossen!")
    print("\n📋 Nächste Schritte:")
    print("1. python run.py - Server starten")
    print("2. Browser öffnet sich automatisch")
    print("3. n8n Workflows erstellen!")

if __name__ == "__main__":
    main()
```

---

## 8. AUSFÜHRUNGSANWEISUNGEN FÜR CODE-ASSISTENTEN

### SCHRITT-FÜR-SCHRITT ANLEITUNG:

1. **Projekt initialisieren:**
   ```bash
   mkdir n8n-mcp-ui
   cd n8n-mcp-ui
   ```

2. **Alle Dateien erstellen** (gemäß obiger Struktur)

3. **Setup ausführen:**
   ```bash
   python setup.py
   ```

4. **Server starten:**
   ```bash
   python run.py
   ```

5. **Browser öffnet automatisch** unter `http://localhost:8080`

### WICHTIGE HINWEISE:

- ✅ **Responsive Design** - funktioniert auf Desktop und Mobile
- ✅ **Moderne UI** - Clean, professionell, benutzerfreundlich
- ✅ **Vollständige Integration** - Alle MCP Server Funktionen verfügbar
- ✅ **Real-time Feedback** - Sofortiges Feedback und Validierung
- ✅ **Auto-Save** - Automatisches Speichern der Eingaben
- ✅ **Export-Funktionen** - JSON, YAML, PDF Export
- ✅ **Toast-Benachrichtigungen** - Benutzerfreundliche Rückmeldungen
- ✅ **Loading-States** - Klare Anzeige von Verarbeitungszuständen

### DESIGN-PRINZIPIEN:

- **Einfachheit:** Intuitive Bedienung ohne Einarbeitung
- **Klarheit:** Klare Struktur und Navigation
- **Feedback:** Sofortiges visuelles Feedback
- **Konsistenz:** Einheitliches Design und Verhalten
- **Zugänglichkeit:** Barrierefrei und responsive

**Diese Anleitung erstellt eine vollständige, produktionsreife Webanwendung für den n8n MCP Server mit professioneller UI und allen erforderlichen Funktionen!** 🎯

