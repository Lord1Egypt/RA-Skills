# A2UI - Agent-to-User Interface Komplettl

## ✅ WICHTIG

A2UI (Agent-to-User Interface) ist ein offizieller Standard von Google f\u00fcr deklarative UI-Erstellung in Agenten. Es erm\u00f6glicht Agents, **sichere und interaktive User-Interfaces** zu erstellen ohne HTML-Code zu schreiben.

## 📋 WAS IST A2UI?

A2UI ist ein **JSON-basiertes Datenformat** mit folgender Struktur:

```json
{
  "beginRendering": {
    "surfaceId": "string - Die eindeutige ID der UI-Oberfl\u00e4che",
    "root": "string - ID der Wurzelkomponente"
  },
  "surfaceUpdate": {
    "surfaceId": "string",
    "components": [
      {
        "id": "string - ID der Komponente",
        "component": {
          "Komponententyp": {
            "prop1": "Wert1",
            "prop2": "Wert2"
          }
        }
      }
    ]
  },
  "dataModelUpdate": {
    "surfaceId": "string",
    "path": "string - JSON-Pointer (/status/cpu)",
    "contents": {object - Neue Daten f\u00fcr Data Model"}
  }
}
```

## 🎨 WIE A2UI MIT CLAWDBOT ARBEITET

### 1. Canvas Host Integration

**Problem:** A2UI ben\u00f6tigt einen **Canvas Host Server** und **gep\u00e4rte Nodes** (iOS/Android Apps).

**Status:** Ohne gepaarten Nodes → Kein A2UI m\u00f6glich

---

### 2. A2UI Spezifikation (v0.8)

**Verf\u00fcgbare Komponenten:**
- **Text:** Text-Elemente (h1, h2, h3, body, caption)
- **Image:** Bilder (icon, avatar, smallFeature, mediumFeature, largeFeature, header)
- **Icon:** Icons (check, arrow, add, arrowForward, etc.)
- **Card:** Karten-Container f\u00fcr Inhalte
- **Button:** Buttons mit Klick-Handler
- **Row:** Horizontaler Container
- **Column:** Vertikaler Container
- **Divider:** Trennlinie
- **TextField:** Eingabefelder
- **Dropdown:** Auswahlliste
- **Checkbox:** Checkboxen
- **Slider:** Schieberegler
- **ProgressBar:** Fortschrittsanzeige
- **Spacer:** Abstandhalter

## 📋 BEISPIELE F\u00dcR A2UI ERSTELLEN

### Beispiel 1: Einfache Card mit Text

```json
{
  "beginRendering": {
    "surfaceId": "mein-dashboard",
    "root": "main"
  },
  "surfaceUpdate": {
    "surfaceId": "mein-dashboard",
    "components": [
      {
        "id": "card-1",
        "component": {
          "Card": {
            "child": "card-content"
          }
        }
      }
    ]
  },
  {
    "id": "card-1",
    "component": {
          "Card": {
            "child": "title-text"
          }
        }
    },
  {
    "id": "title-text",
    "component": {
          "Text": {
            "usageHint": "h1",
            "text": {"literalString": "Mein Dashboard"}
          }
        }
    }
  }
}
```

### Beispiel 2: Dashboard mit Metriken (mit Icons)

```json
{
  "beginRendering": {
    "surfaceId": "status-dashboard",
    "root": "main"
  },
  "surfaceUpdate": {
    "surfaceId": "status-dashboard",
    "components": [
      {
        "id": "main-container",
        "component": {
          "Column": {
            "children": {"explicitList": ["header", "metrics", "footer"]}
          }
        }
      },
      {
        "id": "header",
        "propType": "Card"
      },
      {
        "id": "metrics",
        "component": {
          "Column": {
            "children": {"explicitList": ["cpu-card", "memory-card", "disk-card"]}
          }
        }
      },
      {
        "id": "cpu-card",
        "component": {
          "Card": {
            "child": "cpu-content"
          }
        },
      {
        "id": "cpu-content",
        "component": {
          "Row": {
            "children": {"explicitList": ["cpu-icon", "cpu-label", "cpu-value"]}
          }
        }
      },
      {
        "id": "cpu-icon",
        "component": {
          "Icon": {
            "name": "microchip"
          }
        }
      },
      {
        "id": "cpu-label",
        "component": {
          "Text": {
            "text": {"literalString": "CPU"}
          }
        }
      },
      {
        "id": "cpu-value",
        "component": {
          "Text": {
            "text": {"literalString": "23%"}
          }
        }
      }
    ]
  }
}
```

### Beispiel 3: Fortschrittsanzeige mit ProgressBar

```json
{
  "beginRendering": {
    "surfaceId": "progress-ui",
    "root": "main"
  },
  "surfaceUpdate": {
    "surfaceId": "progress-ui",
    "components": [
      {
        "id": "main-container",
        "component": {
          "Column": {
            "children": {"explicitList": ["progress-title", "progress-bar"]}
          }
        }
      },
      {
        "id": "progress-title",
        "component": {
          "Text": {
            "text": {"literalString": "Aufgaben-Status"}
          }
        }
      },
      {
        "id": "progress-bar",
        "component": {
          "ProgressBar": {
            "value": 0.65,
            "max": 1.0
          }
        }
      }
    ]
  }
}
```

## 📱 WIE KLAWDBOT MIT A2UI INTEGRIEREN

### Option 1: A2UI als Base64-SVG im Chat anzeigen

**Pro:**
- Echte A2UI-Komponenten werden als grafische Bilder angezeigt
- Sehr visuell und interaktiv

**Nachteil:**
- Base64-SVG-Code muss in speziellem Format erstellt werden
- Gr\u00f6\u00dfe, dass Telegram das anzeigt

**Vorgehensweise:**
1. A2UI JSONL erstellen
2. Mit A2UI-Helfer Base64-SVG konvertieren
3. Als Base64-kodierten Markdown-Codeblock senden

**Beispiel:**
```json
{
  "beginRendering": {"surfaceId": "chart-view", "root": "main"},
  "surfaceUpdate": {
    "surfaceId": "chart-view",
    "components": [
      {
        "id": "chart-card",
        "component": {"Card": {"child": "chart-content"}},
      {
        "id": "chart-content",
        "component": {"Column": {"children": {"explicitList": ["chart-title", "bars", "legend"]}}}
      }
    ]
  }
}
```

### Option 2: Canvas-Node erstellen

**Pro:**
- Echte WebSocket-basierte A2UI
- Wird vom Canvas-Host nativ unterst\u00fctzt und gerendert

**Nachteil:**
- Ben\u00f6tigt iOS/Android-Entwicklung
- Oder Canvas-Node via `clawdbot nodes add --type canvas`

**Befehle:**
```bash
# Canvas-Node erstellen
clawdbot nodes add --type canvas

# Dann A2UI senden
clawdbot nodes canvas a2ui push --jsonl meine_dashboard.jsonl --node <node-id>
```

### Option 3: Markdown-Dashboards (tempor\u00e4r)

**Pro:**
- Funktioniert ohne Canvas-Node
- Einfach zu implementieren
- Aktuell getanzt du

**Aktuelle L\u00f6sung:**
- Ich habe eine Markdown-Dokumentation erstellt
- Ich kann visuelle Dashboards erstellen
- Sie sehen aber Text statt Grafiken

---

## 📊 AKTUELLE STATUS

### ✅ Erledigt:
- A2UI-Spezifikation dokumentiert
- Beispiele erstellt
- Markdown-Template bereit

### ⚠️ Offene Fragen:
- **Welche L\u00f6sung bevorzugst du?**
- **Soll ich Canvas-Nodes erstellen?**
- **Oder soll ich Markdown-Dashboards weiterentwickeln?**
- **Base64-SVG Charts erstellen?**

**Status:** Fertig zur Auswahl! 🎯