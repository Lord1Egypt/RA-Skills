---
name: Fritz Connection
description: Dieser Skill ermöglicht die Abfrage von Statusinformationen und die Steuerung einer AVM FRITZ!Box über die TR-064 Schnittstelle. Er bietet Funktionen für Status (Modell, Uptime), Traffic (Bandbreite, Volumen), Host-Listen, WLAN-Steuerung, Anruflisten sowie Reconnect und Reboot.
---

# Fritz Connection

FritzBox Router-Status über die TR-064 API mit `fritzconnection`.

## ⚠️ Sicherheitshinweise

**Folgende Befehle erfordern IMMER eine Rückfrage vor der Ausführung:**

- **`reconnect`** – Kappt die Internetverbindung für alle Geräte kurzzeitig (10-30 Sekunden)
- **`reboot`** – Startet den Router neu, **alles fällt aus** (Internet, WLAN, Telefonie) für 2-5 Minuten
- **`wlan on/off`** – Systemweite Auswirkung auf alle Geräte
- **Router-Konfiguration ändern** – Kann alle Devices betreffen

**Ausnahme:** Nur wenn explizit genehmigt ("mach mal", "ja bitte", etc.)

Diese Befehle betreffen nicht nur den User, sondern alle Geräte und Personen im Netzwerk.

## Voraussetzungen

```bash
cd ~/.openclaw/workspace/skills/fritz-status
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Konfiguration

In `~/.openclaw/skills/.env`:

```
FRITZBOX_HOST=192.168.178.1
FRITZBOX_PASSWORD=dein_passwort
```

Hinweis: FritzBox nutzt nur Passwort-Auth, kein Username.

## Nutzung

```bash
cd ~/.openclaw/workspace/skills/fritz-status

# Router-Status (Model, Uptime, WAN-IP)
.venv/bin/python scripts/fritz_status.py status

# Traffic-Statistiken (Bytes In/Out, Downstream/Upstream)
.venv/bin/python scripts/fritz_status.py traffic

# Verbundene Geräte (Name, IP, MAC, Status)
.venv/bin/python scripts/fritz_status.py hosts -v

# WLAN-Status (2.4GHz, 5GHz, Gastzugang)
.venv/bin/python scripts/fritz_status.py wlan

# Anrufliste (letzte 10 Anrufe)
.venv/bin/python scripts/fritz_status.py calls

# Anrufliste (letzte 20 Anrufe)
.venv/bin/python scripts/fritz_status.py calls -n 20

# Reconnect (neue IP anfordern) ⚠️ Rückfrage erforderlich!
.venv/bin/python scripts/fritz_status.py reconnect

# Reboot (Router neu starten) ⚠️ Rückfrage erforderlich!
.venv/bin/python scripts/fritz_status.py reboot
```

## Verfügbare Befehle

### `status`

Router-Status und Verbindungsinformationen.

**Output:**
```
🖥️  AVM FRITZ!Box 6660 Cable
📍 Host: 192.168.178.1
🔌 Connection: Connected
⏱️  Uptime: 456789 seconds (126h 49m)
🌐 External IP: 203.0.113.42
```

### `traffic`

Bandbreite und Datenvolumen.

**Output:**
```
📥 Max Downstream: 274 Mbit/s
📤 Max Upstream: 52 Mbit/s
📊 Total Received: 299.68 GB
📊 Total Sent: 20.34 GB
```

### `hosts`

Alle bekannten Geräte mit Status.

**Output:**
```
📱 Verbundene Geräte: 5

   ✅ Smartphone (192.168.178.10, AA:BB:CC:DD:EE:01)
   ✅ Laptop (192.168.178.20, AA:BB:CC:DD:EE:02)
   ✅ fritz.box (192.168.178.1, AA:BB:CC:DD:EE:03)
   ⏸️  Tablet (192.168.178.30, AA:BB:CC:DD:EE:04)
   ⏸️  SmartTV (192.168.178.40, AA:BB:CC:DD:EE:05)
```

**Legende:** ✅ = aktiv, ⏸️ = offline/inaktiv

### `wlan`

WLAN-Status aller Netzwerke (2.4 GHz, 5 GHz, Gastzugang).

**Output:**
```
📡 WLAN-Status

📶 2.4 GHz:
   Status: ✅ Enabled
   SSID: MeinWLAN
   Kanal: 6
   Standard: ax

📡 5 GHz:
   Status: ✅ Enabled
   SSID: MeinWLAN
   Kanal: 36
   Standard: ax

🏠 Gastzugang:
   Status: ❌ Disabled
   SSID: MeinWLAN Gast

📡 WLAN ist AN
```

**WLAN-Netzwerke:**
- 📶 2.4 GHz – Hauptnetz (WLANConfiguration:1)
- 📡 5 GHz – Hauptnetz (WLANConfiguration:2)
- 🏠 Gastzugang – Gäste-WLAN (WLANConfiguration:3)

### `calls`

Anrufliste mit Typ, Nummer und Zeitstempel.

**Output:**
```
📋 Anrufliste (10 Einträge)

📞 Eingehend
   📞 01234567890
   🕐 03.03.2026 18:54 (0:39)

📵 Verpasst
   📞 09876543210
   🕐 02.03.2026 15:30 (0:00)

📱 Ausgehend
   📞 017000000000
   🕐 01.03.2026 12:15 (2:30)

📌 Letzter Anruf: 📞 Eingehend von 01234567890 am 03.03.26 18:54
```

**Optionen:**
- `-n, --limit N` - Anzahl Einträge (default: 10)

**Call-Typen:**
- 📞 Eingehend (Type 1) - Angenommene eingehende Anrufe
- 📵 Verpasst (Type 2) - Verpasste eingehende Anrufe
- 📱 Ausgehend (Type 3) - Ausgehende Anrufe

### `reconnect`

Erzwingt einen Reconnect und fordert eine neue externe IP an.

```bash
.venv/bin/python scripts/fritz_status.py reconnect
```

**Output:**
```
🔄 Reconnect angefordert. Warte auf neue Verbindung...
```

**⚠️ Systemweiter Eingriff:**
- Kappt die Internetverbindung für alle Geräte kurzzeitig
- Neue externe IP wird zugewiesen
- Dauert normalerweise 10-30 Sekunden
- **Niemals ohne Rückfrage ausführen!**

### `reboot`

Startet die FRITZ!Box neu.

```bash
.venv/bin/python scripts/fritz_status.py reboot
```

**Output:**
```
🔄 Reboot angefordert. Die FRITZ!Box startet jetzt neu.
   ⏱️  Das dauert normalerweise 2-5 Minuten.
   📡 Alle Geräte verlieren die Verbindung (Internet, WLAN, Telefonie).
```

**⚠️ Systemweiter Eingriff:**
- **Kappt ALLE Verbindungen** (Internet, WLAN, Telefonie) für 2-5 Minuten
- Alle Geräte im Netz verlieren die Verbindung
- Router startet komplett neu
- **Niemals ohne Rückfrage ausführen!**

## fritzconnection Library

Python-Library für FritzBox TR-064 API.

**Dokumentation:** https://fritzconnection.readthedocs.io/

### Zwei API-Interfaces

fritzconnection nutzt **zwei unterschiedliche APIs**:

| API | Methode | Verwendung |
|-----|---------|------------|
| **TR-064** | `fc.call_action(service, action, args)` | Netzwerk, Status, Konfiguration, Smart Home |
| **AHA-HTTP** | `fc.call_http(command, ain)` | Smart Home DECT, Device Stats, XML-Responses |

**TR-064** gibt Python-Datentypen zurück (Dict mit konvertierten Werten).
**HTTP-Interface** gibt rohe HTTP-Response (text/plain oder text/xml, braucht oft Parsen).

### Grundlegende Nutzung

```python
from fritzconnection import FritzConnection

fc = FritzConnection(address="192.168.178.1", password="pw")

# Router-Info
print(fc)  # Model-Informationen

# TR-064: Neue IP via Reconnect
fc.call_action("WANIPConn1", "ForceTermination")
fc.reconnect()  # Shortcut für obiges

# HTTP: Device-Stats für Smart-Home
response = fc.call_http("getbasicdevicestats", ain="12345 7891011")
```

### Haupt-Services (TR-064)

| Service | Beschreibung | Status |
|---------|--------------|--------|
| **WANIPConnection** | WAN-Status, IP, Uptime, Reconnect | ✅ Implementiert |
| **WANCommonInterfaceConfig** | Traffic-Stats, Bandbreite | ✅ Implementiert |
| **Hosts** | Verbundene Geräte, MAC-Filter | ✅ Implementiert |
| **DeviceInfo** | Model, Firmware, Serial | ✅ Implementiert |
| **X_AVM-DE_OnTel** | Anrufliste, Telefonbuch | ✅ Implementiert |
| **WLANConfiguration** | WLAN-Netzwerke, Gäste-WLAN | ✅ Implementiert |
| **DeviceConfig** | Router-Reboot | ✅ Implementiert |
| **X_AVM-DE_Homeauto** | DECT-Smart-Home (Steckdosen, Thermostate) | 🔲 Geplant |
| **LANHostConfigManagement** | DHCP-Einstellungen | 🔲 Geplant |

### Geräte-Unterstützung

- **Fritz!Box** - Vollständig unterstützt (alle Services)
- **Fritz!Repeater** - Teilweise unterstützt (TR-064, aber weniger Services)
- **Fritz!Fon** - Nur über Box erreichbar

Die verfügbaren Services hängen vom Router-Modell und der Firmware ab.

## Erweiterungsideen

### WLAN-Steuerung

```python
# Gäste-WLAN an/aus
fc.call_action('WLANConfiguration:3', 'SetEnable', NewEnable=True)

# Haupt-WLAN an/aus (2.4 GHz)
fc.call_action('WLANConfiguration:1', 'SetEnable', NewEnable=False)

# Alle WLANs global an/aus
fc.call_action('WLANConfiguration:1', 'SetWLANGlobalEnable', NewWLANGlobalEnable=True)
```

### Smart Home (DECT via TR-064)

```python
# DECT-Geräte auflisten
devices = fc.call_action('X_AVM-DE_Homeauto', 'GetGenericDeviceInfos')

# Steckdose schalten
fc.call_action('X_AVM-DE_Homeauto', 'SetSwitch', NewSwitchState='ON')
```

### Smart Home (DECT via HTTP-Interface)

```python
# Device-Stats für ein DECT-Gerät
response = fc.call_http("getbasicdevicestats", ain="12345")

# Response enthält:
# - content-type: 'text/plain' oder 'text/xml'
# - encoding: z.B. 'utf-8'
# - content: Rohe Daten (muss geparst werden)
```

### Anrufliste (TR-064)

```python
# CallList-URL holen
result = fc.call_action('X_AVM-DE_OnTel:1', 'GetCallList')
call_list_url = result.get("NewCallListURL")

# XML herunterladen und parsen
import urllib.request
import xml.etree.ElementTree as ET

with urllib.request.urlopen(call_list_url) as response:
    xml_data = response.read()

root = ET.fromstring(xml_data)
for call in root.findall(".//Call"):
    call_type = call.find("Type").text  # 1=eingehend, 2=verpasst, 3=ausgehend
    caller = call.find("Caller").text
    timestamp = call.find("Date").text
```

### Call-Monitoring (Realtime)

```python
from fritzconnection.lib.fritzcallmonitor import FritzCallMonitor

# Realtime-Monitor für eingehende/ausgehende Anrufe
monitor = FritzCallMonitor(address="192.168.178.1", password="pw")
monitor.connect()

# Events:
# - ring: Eingehender Anruf
# - call: Ausgehender Anruf
# - connect: Verbindung hergestellt
# - disconnect: Verbindung beendet
```

### Reconnect (Neue IP)

```python
# WANIPConn1 - ForceTermination
fc.reconnect()

# Oder manuell:
fc.call_action("WANIPConn1", "ForceTermination")
```

### Reboot

```python
# DeviceConfig:1 - Reboot
fc.call_action("DeviceConfig:1", "Reboot")
```

## Python-API

```python
from scripts.fritz_status import FritzBoxClient

client = FritzBoxClient()

# Status
info = client.get_status()
print(info['model'], info['uptime'])

# Traffic
traffic = client.get_traffic()
print(traffic['bytes_received'], traffic['bytes_sent'])

# Hosts
hosts = client.get_hosts()
print(f"{hosts['count']} Geräte verbunden")
for device in hosts['devices']:
    print(f"  {device['name']}: {device['ip']} ({'active' if device['active'] else 'offline'})")
```

## Architektur

```
fritz-status/
├── SKILL.md              # Diese Datei
├── requirements.txt      # fritzconnection>=1.15.0
├── .gitignore
└── scripts/
    └── fritz_status.py   # CLI-Interface
```

## Links

- **Library:** https://github.com/kbr/fritzconnection
- **Doku:** https://fritzconnection.readthedocs.io/
- **TR-064 Dokumentation:** https://avm.de/service/schnittstellen/
- **AVM Service-Übersicht:** https://fritz.box:49000/tr64desc.xml