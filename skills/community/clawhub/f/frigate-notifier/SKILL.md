# Frigate WhatsApp & Email Notifier

A robust monitoring skill that bridges Frigate NVR MQTT events to real-time WhatsApp and Email notifications.

## 🚀 Features
- **Identity-Aware**: Utilises Frigate's face recognition to name specific people in alerts.
- **Multi-Channel**: Simultaneous delivery to WhatsApp (via OpenClaw) and Email (via SMTP).
- **Smart Snapshots**: Implements a "Broad Fix" fallback, fetching thumbnails if a formal event snapshot isn't available.
- **Flood Protection**: Built-in rate limiting (configurable) to prevent notification fatigue.
- **Browser Masquerading**: Uses realistic headers to ensure API images are delivered without being blocked.

## 🛠️ Installation

### 1. Dependencies
Ensure the following Python libraries are installed on the host:
`pip install paho-mqtt requests`

### 2. Configuration
Create a `config.json` file in the same directory as the script with the following structure:

```json
{
  "mqtt_broker": "YOUR_MQTT_BROKER_IP",
  "mqtt_port": 1883,
  "frigate_api_url": "http://YOUR_FRIGATE_IP:5000",
  "whatsapp_target": "+COUNTRY_CODE_NUMBER",
  "email_target": "your@email.com",
  "smtp_server": "your.smtp.server",
  "smtp_port": 587,
  "smtp_user": "user@email.com",
  "smtp_pass": "yourpassword",
  "smtp_security": "tls",
  "cooldown_period": 900,
  "max_notifications": 2
}
```

### 3. Deployment
Run the notifier in the background:
`nohup python3 frigate_notifier.py > frigate_notifier.log 2>&1 &`

## 📖 How it Works
The skill subscribes to the `frigate/events` topic. When a detection occurs, it resolves the identity, checks the rate limit, fetches the best available image from the API, and dispatches the alerts.
