# whatsapp_api.py — sends via official Meta WhatsApp Business API
import requests

def send(phone_number: str, message: str, token: str, phone_id: str):
    # Meta WhatsApp Business API endpoint
    url = f'https://graph.facebook.com/v18.0/{phone_id}/messages'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    payload = {
        'messaging_product': 'whatsapp',
        'to': phone_number,
        'type': 'text',
        'text': {'body': message}
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            print(f"Error from WhatsApp API: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Exception calling WhatsApp API: {e}")
        return False
