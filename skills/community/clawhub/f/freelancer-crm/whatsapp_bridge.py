# whatsapp_bridge.py — sends via OpenClaw WhatsApp Bridge (Baileys)
import subprocess

def send(phone_number: str, message: str):
    # This assumes the 'openclaw' CLI is available in the environment
    # and configured for the correct gateway.
    try:
        result = subprocess.run(
            ['openclaw', 'whatsapp', 'send', '--to', phone_number, '--message', message],
            capture_output=True, text=True
        )
        return result.returncode == 0
    except FileNotFoundError:
        print("Error: 'openclaw' CLI not found.")
        return False
