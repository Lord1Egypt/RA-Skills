# Fritz Connection (OpenClaw Skill)

[Deutsch](#deutsch) | [English](#english)

---

<a name="deutsch"></a>
## Deutsch

Dieser OpenClaw-Skill ermöglicht die Abfrage von Statusinformationen und die Steuerung einer AVM FRITZ!Box über die TR-064 Schnittstelle.

### 🚀 Features

- **Status:** Modell, Uptime und Verbindungsstatus.
- **Traffic:** Aktuelle Bandbreite und übertragenes Datenvolumen.
- **Hosts:** Liste der verbundenen Geräte im Netzwerk.
- **WLAN:** Status und Steuerung (An/Aus) von 2.4 GHz, 5 GHz und Gastzugang.
- **Anrufe:** Anzeige der letzten eingehenden, ausgehenden und verpassten Anrufe.
- **Steuerung:** Reconnect (neue IP) und Reboot der FRITZ!Box.

### 🛠️ Voraussetzungen

- Eine FRITZ!Box mit aktiviertem TR-064 (standardmäßig an).
- Python 3.x
- Die `fritzconnection` Library.

### 📦 Installation

```bash
cd ~/.openclaw/workspace/skills/fritz-status
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### ⚙️ Konfiguration

Erstelle oder ergänze die Datei `~/.openclaw/skills/.env`:

```env
FRITZBOX_HOST=192.168.178.1
FRITZBOX_PASSWORD=dein_passwort
```

### 📖 Nutzung

```bash
# Status abfragen
.venv/bin/python scripts/fritz_status.py status

# Anrufliste zeigen
.venv/bin/python scripts/fritz_status.py calls

# WLAN an/aus schalten
.venv/bin/python scripts/fritz_status.py wlan on
.venv/bin/python scripts/fritz_status.py wlan off
```

⚠️ **Hinweis:** Befehle wie `reconnect` oder `reboot` unterbrechen die Internetverbindung für alle Geräte im Netzwerk.

---

<a name="english"></a>
## English

This OpenClaw skill allows you to monitor and control your AVM FRITZ!Box router via the TR-064 interface.

### 🚀 Features

- **Status:** Model info, uptime, and connection state.
- **Traffic:** Current bandwidth and total data volume.
- **Hosts:** List of connected devices in your network.
- **WLAN:** Status and control (On/Off) for 2.4 GHz, 5 GHz, and guest access.
- **Calls:** View recent incoming, outgoing, and missed calls.
- **Control:** Reconnect (get a new IP) and reboot the FRITZ!Box.

### 🛠️ Requirements

- A FRITZ!Box with TR-064 support enabled (enabled by default).
- Python 3.x
- The `fritzconnection` library.

### 📦 Installation

```bash
cd ~/.openclaw/workspace/skills/fritz-status
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### ⚙️ Configuration

Create or update your `~/.openclaw/skills/.env` file:

```env
FRITZBOX_HOST=192.168.178.1
FRITZBOX_PASSWORD=your_password
```

### 📖 Usage

```bash
# Get status
.venv/bin/python scripts/fritz_status.py status

# Show call log
.venv/bin/python scripts/fritz_status.py calls

# Toggle WLAN on/off
.venv/bin/python scripts/fritz_status.py wlan on
.venv/bin/python scripts/fritz_status.py wlan off
```

⚠️ **Note:** Commands like `reconnect` or `reboot` will interrupt the internet connection for all devices in your network.

---

## License / Lizenz

MIT-0 - See [LICENSE](LICENSE) for details.
