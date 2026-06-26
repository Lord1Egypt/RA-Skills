import json
import os
import sys

def send(phone_number, message):
    skill_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(skill_dir, "config.json")

    # Validate phone number format
    if not phone_number.startswith("+"):
        print(f"Error: Phone number must start with + in international format (got '{phone_number}'). Example: +923001234567")
        return False

    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Error: config.json not found. Please run setup.py first.")
        return False
    except json.JSONDecodeError:
        print("Error: config.json is corrupted.")
        return False

    method = config.get("whatsapp_method", "")

    if not method:
        print("Error: whatsapp_method is not set in config.json. Please run setup.py.")
        return False

    if method == "bridge":
        import whatsapp_bridge
        return whatsapp_bridge.send(phone_number, message)

    elif method == "api":
        token = config.get("api_token", "")
        phone_id = config.get("api_phone_id", "")
        if not token:
            print("Error: api_token is missing in config.json.")
            return False
        if not phone_id:
            print("Error: api_phone_id is missing in config.json.")
            return False
        import whatsapp_api
        return whatsapp_api.send(phone_number, message, token, phone_id)

    else:
        print(f"Error: Unknown whatsapp_method '{method}'. Must be 'bridge' or 'api'.")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(1)
    phone = sys.argv[1]
    msg = sys.argv[2]
    success = send(phone, msg)
    print("Sent" if success else "Failed")
