import os
import sys
import json
import subprocess

def main():
    skill_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(skill_dir)

    # Step 1: Check for existing config
    if os.path.exists("config.json"):
        answer = input("config.json already exists. Skip setup and keep existing config? (y/n): ")
        if answer.lower() == "y":
            print("Setup skipped. Your existing config is unchanged.")
            sys.exit(0)

    # Step 2: Install dependencies
    print("\nInstalling required dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "filelock", "requests"], check=True)
        print("Dependencies installed.")
    except subprocess.CalledProcessError:
        print("Error: Failed to install dependencies. Please install 'filelock' and 'requests' manually.")
        sys.exit(1)

    # Step 3: Ask user questions
    user_name = input("Your name (used in digest messages): ")
    user_phone = input("Your WhatsApp number in international format (e.g. +923001234567): ")
    
    follow_up_days = input("How many days before a silent client gets a follow-up reminder? (default 5): ")
    if not follow_up_days:
        follow_up_days = "5"
        
    invoice_reminder_days = input("How many days before an overdue invoice gets a reminder? (default 7): ")
    if not invoice_reminder_days:
        invoice_reminder_days = "7"

    print("\nWhatsApp method — how do you want to send messages?")
    print("  1. WhatsApp Bridge — uses your existing WhatsApp number, scan QR code, free")
    print("  2. Official WhatsApp Business API — requires Meta Business account, more reliable")
    choice = input("Enter 1 or 2: ")

    api_token = ""
    api_phone_id = ""
    if choice == "2":
        api_token = input("WhatsApp Business API token (from Meta Developer Console): ")
        api_phone_id = input("WhatsApp Phone Number ID (from Meta Developer Console): ")
    else:
        print("\nWhatsApp Bridge selected. After setup completes, run:")
        print("  openclaw integrations whatsapp")
        print("Then scan the QR code with your phone to connect.")

    # Step 5: Validate phone number format
    if not user_phone.startswith("+"):
        print("Error: Phone number must start with + (e.g. +923001234567)")
        sys.exit(1)

    # Step 6: Write config.json
    config = {
        "user_name": user_name,
        "user_phone": user_phone,
        "whatsapp_method": "bridge" if choice == "1" else "api",
        "api_token": api_token,
        "api_phone_id": api_phone_id,
        "follow_up_days": int(follow_up_days),
        "invoice_reminder_days": int(invoice_reminder_days)
    }

    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)

    print("\nconfig.json created successfully.")

    # Step 7: Create blank clients.json if it does not exist
    if not os.path.exists("clients.json"):
        with open("clients.json", "w") as f:
            json.dump({"clients": []}, f, indent=2)
        print("clients.json created (empty — ready for your first client).")
    else:
        print("clients.json already exists — keeping your existing client data.")

    # Step 8: Send a test WhatsApp message
    print("\nSending a test WhatsApp message to confirm connection...")
    sys.path.append(skill_dir)
    import send_message
    success = send_message.send(user_phone, f"Hello {user_name}! Your Freelancer CRM skill is connected and ready.")
    if success:
        print("Test message sent successfully. Check your WhatsApp.")
    else:
        print("Test message failed. Check your WhatsApp connection and config.json, then re-run setup.py.")

    # Step 9: Print completion summary
    print("\n" + "="*50)
    print("SETUP COMPLETE")
    print("="*50)
    print(f"Name:              {user_name}")
    print(f"Your number:       {user_phone}")
    print(f"WhatsApp method:   {config['whatsapp_method']}")
    print(f"Follow-up after:   {config['follow_up_days']} days")
    print(f"Invoice reminder:  {config['invoice_reminder_days']} days")
    print("\nYou are ready. Drop this folder into ~/.openclaw/skills/ and start chatting.")
    print("="*50)

if __name__ == "__main__":
    main()
