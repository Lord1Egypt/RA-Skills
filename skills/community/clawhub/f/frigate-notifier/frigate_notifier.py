import paho.mqtt.client as mqtt
import json
import subprocess
import sys
import time
import os
import requests
from collections import defaultdict

# Load configuration from local file
def load_config():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Critical Error: Could not load config.json. {e}")
        sys.exit(1)

CONFIG = load_config()

# Configuration Mapping
MQTT_BROKER = CONFIG.get("mqtt_broker", "localhost")
MQTT_PORT = CONFIG.get("mqtt_port", 1883)
MQTT_TOPIC = "frigate/events"
USER_TARGET_WA = CONFIG.get("whatsapp_target", "")
USER_TARGET_EMAIL = CONFIG.get("email_target", "")
FRIGATE_API_URL = CONFIG.get("frigate_api_url", "http://localhost:5000")

# Rate Limiting Configuration
COOLDOWN_PERIOD = CONFIG.get("cooldown_period", 900)
MAX_NOTIFICATIONS = CONFIG.get("max_notifications", 2)

notification_history = defaultdict(list)

def send_whatsapp_notification(message, media_path=None):
    if not USER_TARGET_WA: return
    try:
        cmd = ["openclaw", "message", "send", "--channel", "whatsapp", "--target", USER_TARGET_WA, "--message", message]
        if media_path:
            cmd.extend(["--media", media_path])
        subprocess.run(cmd, check=True)
    except Exception as e:
        print(f"WhatsApp error: {e}")

def send_email_notification(subject, body, attachment_path=None):
    if not USER_TARGET_EMAIL: return
    try:
        cmd = ["python3", "email_dispatcher.py", "--to", USER_TARGET_EMAIL, "--subject", subject, "--body", body]
        if attachment_path:
            cmd.extend(["--attachment", attachment_path])
        subprocess.run(cmd, check=True)
    except Exception as e:
        print(f"Email error: {e}")

def should_notify(camera):
    now = time.time()
    notification_history[camera] = [t for t in notification_history[camera] if now - t < COOLDOWN_PERIOD]
    if len(notification_history[camera]) < MAX_NOTIFICATIONS:
        notification_history[camera].append(now)
        return True
    return False

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        data = payload.get("after", payload)
        camera = data.get("camera", "Unknown Camera")
        event_id = data.get("id")
        label = data.get("label", "Unknown Object")
        identity = data.get("id", "") 
        
        display_name = identity if (label == "person" and identity) else label
        
        if should_notify(camera):
            notification_text = f"🚨 Frigate Detection: {display_name} detected on {camera}"
            send_whatsapp_notification(notification_text)
            
            if event_id:
                snapshot_path = f"/tmp/frigate_{event_id}.jpg"
                snapshot_url = f"{FRIGATE_API_URL}/api/events/{event_id}/snapshot.jpg"
                time.sleep(5) 
                try:
                    headers = {'User-Agent': 'Mozilla/5.0'}
                    response = requests.get(snapshot_url, headers=headers, timeout=10)
                    if response.status_code == 200:
                        with open(snapshot_path, 'wb') as f:
                            f.write(response.content)
                        if os.path.getsize(snapshot_path) > 1024:
                            send_email_notification(f"Frigate Alert: {display_name} on {camera}", f"Detection captured on {camera}.", snapshot_path)
                        else:
                            send_email_notification(f"Frigate Alert (Low Res): {display_name} on {camera}", "Photo was too low quality.")
                    else:
                        send_email_notification(f"Frigate Alert (API Error): {display_name} on {camera}", f"API error {response.status_code}.")
                    if os.path.exists(snapshot_path):
                        os.remove(snapshot_path)
                except Exception as e:
                    send_email_notification(f"Frigate Alert (Exception): {display_name} on {camera}", f"Error: {str(e)}")
    except Exception as e:
        print(f"MQTT Error: {e}")

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_forever()
    except Exception:
        sys.exit(1)

if __name__ == "__main__":
    main()
