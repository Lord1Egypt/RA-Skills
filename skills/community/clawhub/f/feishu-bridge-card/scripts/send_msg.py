import sys
import json
import requests

def send_feishu_card(webhook_url, title, content_list, color="blue"):
    """
    Sends an interactive message card to Feishu.
    color: blue, wathet, turquoise, green, yellow, orange, red, carmine, violet, purple, indigo, grey
    """
    elements = []
    for item in content_list:
        elements.append({
            "tag": "div",
            "text": {
                "content": item,
                "tag": "lark_md"
            }
        })

    payload = {
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": True,
                "enable_forward": True
            },
            "header": {
                "title": {
                    "content": title,
                    "tag": "plain_text"
                },
                "template": color
            },
            "elements": elements
        }
    }
    
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        print(f"Card sent successfully: {response.text}")
    except Exception as e:
        print(f"Error sending card: {e}")
        sys.exit(1)

def send_feishu_text(webhook_url, text):
    headers = {'Content-Type': 'application/json'}
    payload = {
        "msg_type": "text",
        "content": {
            "text": text
        }
    }
    try:
        response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        print(f"Text sent successfully: {response.text}")
    except Exception as e:
        print(f"Error sending text: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("  Text: python3 send_msg.py <url> text <message>")
        print("  Card: python3 send_msg.py <url> card <title> <color> <content_json_list>")
        sys.exit(1)
    
    url = sys.argv[1]
    mode = sys.argv[2]
    
    if mode == "text":
        send_feishu_text(url, sys.argv[3])
    elif mode == "card":
        title = sys.argv[3]
        color = sys.argv[4]
        content_list = json.loads(sys.argv[5])
        send_feishu_card(url, title, content_list, color)
