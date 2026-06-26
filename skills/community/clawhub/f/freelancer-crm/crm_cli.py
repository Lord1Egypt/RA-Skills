import sys
import os
import json
try:
    from filelock import FileLock
    HAS_FILELOCK = True
except ImportError:
    HAS_FILELOCK = False

def load_clients(clients_path):
    if not os.path.exists(clients_path):
        print("Error: clients.json not found. Please run setup.py first.")
        sys.exit(1)
    try:
        with open(clients_path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Error: clients.json is corrupted. Please check the file.")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 crm_cli.py [list|follow-ups|invoices|proposal|digest]")
        return

    cmd = sys.argv[1].lower()
    skill_dir = os.path.dirname(os.path.abspath(__file__))
    clients_path = os.path.join(skill_dir, "clients.json")

    if cmd == "list":
        data = load_clients(clients_path)
        print(json.dumps(data, indent=2))

    elif cmd == "add":
        if len(sys.argv) < 7:
            print("Usage: python3 crm_cli.py add <name> <status> <project> <amount> <phone>")
            return
        
        name, status, project, amount, phone = sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6]
        data = load_clients(clients_path)
        
        # Generate new ID
        new_id = 1
        if data["clients"]:
            new_id = max(c["id"] for c in data["clients"]) + 1
        
        from datetime import date
        new_client = {
            "id": new_id,
            "name": name,
            "status": status,
            "project": project,
            "invoice_amount": float(amount),
            "invoice_status": "pending",
            "invoice_sent_date": "",
            "phone": phone,
            "last_contact": date.today().strftime("%Y-%m-%d"),
            "notes": ""
        }
        
        data["clients"].append(new_client)
        
        # Write with filelock
        lock_path = clients_path + ".lock"
        if HAS_FILELOCK:
            lock = FileLock(lock_path)
            with lock:
                with open(clients_path, "w") as f:
                    json.dump(data, f, indent=2)
        else:
            with open(clients_path, "w") as f:
                json.dump(data, f, indent=2)
        
        print(f"Client '{name}' added successfully with ID {new_id}.")

    elif cmd == "update":
        if len(sys.argv) < 5:
            print("Usage: python3 crm_cli.py update <id> <field> <value>")
            return
        
        client_id = int(sys.argv[2])
        field = sys.argv[3]
        value = sys.argv[4]
        
        valid_fields = ["name", "status", "project", "invoice_amount", "invoice_status", "invoice_sent_date", "phone", "last_contact", "notes"]
        if field not in valid_fields:
            print(f"Error: '{field}' is not a valid field. Valid fields are: {', '.join(valid_fields)}")
            return

        data = load_clients(clients_path)
        client = next((c for c in data["clients"] if c["id"] == client_id), None)
        
        if not client:
            print(f"Error: No client found with ID {client_id}.")
            return
        
        if field == "invoice_amount":
            client[field] = float(value)
        else:
            client[field] = value
            
        # Write with filelock
        lock_path = clients_path + ".lock"
        if HAS_FILELOCK:
            lock = FileLock(lock_path)
            with lock:
                with open(clients_path, "w") as f:
                    json.dump(data, f, indent=2)
        else:
            with open(clients_path, "w") as f:
                json.dump(data, f, indent=2)
                
        print(f"Client '{client['name']}' updated: {field} → {value}")

    elif cmd == "follow-ups":
        import follow_up
        results = follow_up.check_follow_ups()
        if not results:
            print("No follow-ups needed.")
        else:
            for c in results:
                print(f"- {c['name']}: {c['days_silent']} days silent (Project: {c['project']})")

    elif cmd == "invoices":
        import invoice_tracker
        results = invoice_tracker.check_overdue_invoices()
        if not results:
            print("No overdue invoices.")
        else:
            for c in results:
                print(f"- {c['name']}: ${c['amount']} ({c['days_overdue']} days overdue)")

    elif cmd == "proposal":
        if len(sys.argv) < 6:
            print("Usage: python3 crm_cli.py proposal <name> <project> <cost> <timeline>")
        else:
            import proposal_generator
            print(proposal_generator.generate_proposal(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]))

    elif cmd == "digest":
        import weekly_digest
        print(weekly_digest.generate_digest())

    else:
        print(f"Unknown command: {cmd}")

if __name__ == "__main__":
    main()
