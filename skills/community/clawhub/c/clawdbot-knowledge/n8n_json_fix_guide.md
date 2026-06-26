# N8N JSON-Strukturen Korrektur-Leitfaden

## 🔍 **Identifizierte Probleme mit den aktuellen JSON-Strukturen:**

### 1. **Naming Convention Probleme:**
- ❌ Node-Namen verwenden nicht PascalCase (z.B. "weatherapi" statt "WeatherAPI")
- ❌ Node-Typen folgen nicht der N8N-Konvention
- ❌ Display-Namen sind nicht benutzerfreundlich

### 2. **Strukturelle Probleme:**
- ❌ Position wird als Integer statt Float angegeben
- ❌ Fehlende oder falsche Pflichtfelder
- ❌ Parameter-Validierung unvollständig

### 3. **N8N-Compliance Probleme:**
- ❌ Node-Typen beginnen nicht mit "n8n-nodes-base."
- ❌ TypeVersion fehlt oder ist falsch
- ❌ Credentials-Handling nicht korrekt

## ✅ **Korrekte N8N-konforme JSON-Strukturen:**

### **Beispiel 1: HTTP Request Node (Korrekt)**
```json
{
  "id": "node_12345678",
  "name": "WeatherAPI",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 1,
  "position": [100.0, 100.0],
  "parameters": {
    "method": "GET",
    "url": "https://api.openweathermap.org/data/2.5/weather",
    "options": {},
    "headers": {},
    "qs": {
      "q": "Berlin",
      "appid": "={{$credentials.apiKey}}"
    }
  }
}
```

### **Beispiel 2: Webhook Trigger (Korrekt)**
```json
{
  "id": "node_87654321",
  "name": "WebhookTrigger",
  "type": "n8n-nodes-base.webhook",
  "typeVersion": 1,
  "position": [50.0, 50.0],
  "parameters": {
    "httpMethod": "POST",
    "path": "webhook-endpoint",
    "options": {
      "noResponseBody": false
    }
  }
}
```

### **Beispiel 3: Email Send Node (Korrekt)**
```json
{
  "id": "node_11223344",
  "name": "SendNotification",
  "type": "n8n-nodes-base.emailSend",
  "typeVersion": 1,
  "position": [300.0, 100.0],
  "parameters": {
    "fromEmail": "noreply@company.com",
    "toEmail": "admin@company.com",
    "subject": "Weather Alert",
    "message": "Current weather data received",
    "options": {}
  }
}
```

### **Beispiel 4: Code Node (Korrekt)**
```json
{
  "id": "node_55667788",
  "name": "ProcessData",
  "type": "n8n-nodes-base.code",
  "typeVersion": 1,
  "position": [200.0, 100.0],
  "parameters": {
    "language": "javascript",
    "jsCode": "// Process weather data\nconst data = $input.all();\nconst processed = data.map(item => ({\n  temperature: item.json.main.temp,\n  city: item.json.name,\n  timestamp: new Date().toISOString()\n}));\nreturn processed;"
  }
}
```

## 🛠️ **Validierungsregeln für N8N-Compliance:**

### **Pflichtfelder:**
- ✅ `id`: Eindeutige Node-ID (String)
- ✅ `name`: PascalCase Node-Name (String)
- ✅ `type`: N8N Node-Typ mit "n8n-nodes-base." Präfix
- ✅ `typeVersion`: Version (Integer, meist 1)
- ✅ `position`: [x, y] Koordinaten als Float-Array

### **Naming Conventions:**
- ✅ Node-Namen: PascalCase (z.B. "WeatherAPI", "DatabaseConnector")
- ✅ Node-Typen: "n8n-nodes-base.{serviceName}"
- ✅ Parameter-Namen: camelCase

### **Position Format:**
- ✅ Korrekt: `[100.0, 200.0]` (Float-Werte)
- ❌ Falsch: `[100, 200]` (Integer-Werte)

### **Parameter-Struktur:**
- ✅ Alle Parameter in `parameters` Objekt
- ✅ Credentials über `credentials` Feld referenzieren
- ✅ Optionen in `options` Unter-Objekt

## 🔧 **Automatische Korrekturen implementieren:**

### **1. Name Normalisierung:**
```python
def normalize_node_name(name: str) -> str:
    # Entferne Sonderzeichen und konvertiere zu PascalCase
    words = re.sub(r'[^a-zA-Z0-9\s_-]', '', name).replace('_', ' ').replace('-', ' ').split()
    return ''.join(word.capitalize() for word in words if word) or "CustomNode"
```

### **2. Node-Typ Korrektur:**
```python
def fix_node_type(service: str, node_type: str = "action") -> str:
    if node_type == "trigger":
        return f"n8n-nodes-base.{service.lower()}Trigger"
    return f"n8n-nodes-base.{service.lower()}"
```

### **3. Position Korrektur:**
```python
def fix_position(position: List) -> List[float]:
    return [float(position[0]), float(position[1])] if len(position) >= 2 else [100.0, 100.0]
```

## 📋 **Workflow-Beispiel (Vollständig korrekt):**
```json
{
  "id": "workflow_123",
  "name": "WeatherDataPipeline",
  "active": false,
  "nodes": [
    {
      "id": "node_trigger",
      "name": "ScheduleTrigger",
      "type": "n8n-nodes-base.scheduleTrigger",
      "typeVersion": 1,
      "position": [50.0, 100.0],
      "parameters": {
        "rule": {
          "interval": [{
            "field": "cronExpression",
            "expression": "0 */6 * * *"
          }]
        }
      }
    },
    {
      "id": "node_api",
      "name": "WeatherAPI",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 1,
      "position": [250.0, 100.0],
      "parameters": {
        "method": "GET",
        "url": "https://api.openweathermap.org/data/2.5/weather",
        "qs": {
          "q": "Berlin",
          "appid": "={{$credentials.openWeatherMap.apiKey}}"
        }
      }
    }
  ],
  "connections": {
    "node_trigger": {
      "main": [
        {
          "node": "node_api",
          "type": "main",
          "index": 0
        }
      ]
    }
  },
  "settings": {},
  "staticData": {},
  "tags": [],
  "meta": {
    "description": "Automated weather data collection pipeline"
  }
}
```

## 🎯 **Nächste Schritte:**
1. Implementieren Sie die Normalisierungsfunktionen in Ihrem MCP-Server
2. Aktualisieren Sie alle Node-Templates mit korrekten Strukturen
3. Fügen Sie Validierung für alle generierten JSON-Strukturen hinzu
4. Testen Sie die generierten Workflows in N8N
