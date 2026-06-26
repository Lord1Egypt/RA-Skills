#!/usr/bin/env python3
"""
CRM-in-a-Box CLI - File-based CRM management
Contacts, pipeline, and interactions as NDJSON files.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

DEFAULT_CRM_DIR = Path.home() / ".openclaw" / "workspace" / "crm"
CONFIG_TEMPLATE = {
    "pipeline_stages": ["new", "contacted", "meeting_scheduled", "proposal_sent", "negotiating", "won", "lost"],
    "labels": ["hot-lead", "warm-lead", "cold-lead", "referral", "conference", "inbound", "outbound"]
}

def init_crm(crm_dir=None):
    """Initialize a new CRM directory."""
    crm_dir = Path(crm_dir) if crm_dir else DEFAULT_CRM_DIR
    crm_dir.mkdir(parents=True, exist_ok=True)
    
    # Create config.yaml
    config_file = crm_dir / "config.yaml"
    if not config_file.exists():
        config_file.write_text(f"""# CRM Configuration
pipeline_stages:
{chr(10).join(f'  - {stage}' for stage in CONFIG_TEMPLATE['pipeline_stages'])}

labels:
{chr(10).join(f'  - {label}' for label in CONFIG_TEMPLATE['labels'])}
""")
    
    # Create empty NDJSON files
    for filename in ["contacts.ndjson", "pipeline.ndjson", "interactions.ndjson"]:
        filepath = crm_dir / filename
        if not filepath.exists():
            filepath.touch()
    
    print(f"✅ CRM initialized at: {crm_dir}")
    return crm_dir

def add_contact(crm_dir, name, email, company=None, phone=None, labels=None, notes=None):
    """Add a new contact to the CRM."""
    contacts_file = Path(crm_dir) / "contacts.ndjson"
    
    # Generate ID
    contact_id = f"c{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    contact = {
        "id": contact_id,
        "name": name,
        "email": email,
        "company": company,
        "phone": phone,
        "stage": "new",
        "labels": labels or [],
        "notes": notes or "",
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    
    with open(contacts_file, 'a') as f:
        f.write(json.dumps(contact) + "\n")
    
    print(f"✅ Contact added: {contact_id} - {name} ({email})")
    return contact_id

def update_pipeline(crm_dir, contact_id, stage, deal=None, value=None):
    """Update or create a pipeline entry for a contact."""
    pipeline_file = Path(crm_dir) / "pipeline.ndjson"
    
    pipeline_entry = {
        "id": f"p{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "contact_id": contact_id,
        "stage": stage,
        "deal": deal,
        "value": value,
        "updated_at": datetime.utcnow().isoformat() + "Z"
    }
    
    with open(pipeline_file, 'a') as f:
        f.write(json.dumps(pipeline_entry) + "\n")
    
    print(f"✅ Pipeline updated: {contact_id} → {stage}")
    return pipeline_entry["id"]

def log_interaction(crm_dir, contact_id, interaction_type, summary):
    """Log an interaction (email, call, meeting, note)."""
    interactions_file = Path(crm_dir) / "interactions.ndjson"
    
    interaction = {
        "id": f"i{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "contact_id": contact_id,
        "type": interaction_type,
        "summary": summary,
        "at": datetime.utcnow().isoformat() + "Z"
    }
    
    with open(interactions_file, 'a') as f:
        f.write(json.dumps(interaction) + "\n")
    
    print(f"✅ Interaction logged: {interaction_type} with {contact_id}")
    return interaction["id"]

def search_contacts(crm_dir, query):
    """Search contacts by name, email, or company."""
    contacts_file = Path(crm_dir) / "contacts.ndjson"
    
    if not contacts_file.exists():
        print("❌ No contacts file found. Run 'init' first.")
        return []
    
    results = []
    query_lower = query.lower()
    
    with open(contacts_file, 'r') as f:
        for line in f:
            if line.strip():
                contact = json.loads(line)
                if (query_lower in contact.get('name', '').lower() or
                    query_lower in contact.get('email', '').lower() or
                    query_lower in contact.get('company', '').lower()):
                    results.append(contact)
    
    print(f"\n📇 Found {len(results)} contact(s) matching '{query}':\n")
    for c in results:
        print(f"  {c['id']}: {c['name']} @ {c.get('company', 'N/A')} - {c['email']}")
        print(f"      Stage: {c.get('stage', 'new')} | Labels: {', '.join(c.get('labels', []))}")
        print()
    
    return results

def list_pipeline(crm_dir):
    """List all pipeline entries."""
    pipeline_file = Path(crm_dir) / "pipeline.ndjson"
    
    if not pipeline_file.exists():
        print("❌ No pipeline file found. Run 'init' first.")
        return []
    
    entries = []
    with open(pipeline_file, 'r') as f:
        for line in f:
            if line.strip():
                entries.append(json.loads(line))
    
    # Sort by value descending
    entries.sort(key=lambda x: x.get('value', 0) or 0, reverse=True)
    
    print("\n💰 Pipeline Summary:\n")
    total_value = 0
    for e in entries:
        value = e.get('value', 0) or 0
        total_value += value
        print(f"  {e['id']}: {e['contact_id']} → {e['stage']}")
        print(f"      Deal: {e.get('deal', 'N/A')} | Value: ${value:,.2f}")
        print(f"      Updated: {e.get('updated_at', 'N/A')}")
        print()
    
    print(f"Total Pipeline Value: ${total_value:,.2f}")
    return entries

def get_stats(crm_dir):
    """Get CRM statistics."""
    stats = {"contacts": 0, "pipeline_entries": 0, "interactions": 0, "by_stage": {}}
    
    crm_path = Path(crm_dir)
    
    # Count contacts
    contacts_file = crm_path / "contacts.ndjson"
    if contacts_file.exists():
        with open(contacts_file, 'r') as f:
            for line in f:
                if line.strip():
                    stats["contacts"] += 1
                    contact = json.loads(line)
                    stage = contact.get('stage', 'new')
                    stats["by_stage"][stage] = stats["by_stage"].get(stage, 0) + 1
    
    # Count pipeline entries
    pipeline_file = crm_path / "pipeline.ndjson"
    if pipeline_file.exists():
        with open(pipeline_file, 'r') as f:
            for line in f:
                if line.strip():
                    stats["pipeline_entries"] += 1
    
    # Count interactions
    interactions_file = crm_path / "interactions.ndjson"
    if interactions_file.exists():
        with open(interactions_file, 'r') as f:
            for line in f:
                if line.strip():
                    stats["interactions"] += 1
    
    print("\n📊 CRM Statistics:\n")
    print(f"  Total Contacts: {stats['contacts']}")
    print(f"  Pipeline Entries: {stats['pipeline_entries']}")
    print(f"  Interactions Logged: {stats['interactions']}")
    print("\n  By Stage:")
    for stage, count in sorted(stats["by_stage"].items()):
        print(f"    {stage}: {count}")
    print()
    
    return stats

def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("""CRM-in-a-Box CLI - File-based CRM Management

Usage: crm_cli.py <command> [args]

Commands:
  init [dir]                          Initialize new CRM
  add-contact <name> <email> [--company X] [--phone Y] [--labels a,b] [--notes Z]
  update-pipeline <contact_id> <stage> [--deal X] [--value Y]
  log-interaction <contact_id> <type> <summary>
  search <query>                      Search contacts
  pipeline                            List pipeline
  stats                               Show statistics

Types: email, call, meeting, note
Stages: new, contacted, meeting_scheduled, proposal_sent, negotiating, won, lost

Examples:
  ./crm_cli.py init ./mycompany
  ./crm_cli.py add-contact "John Doe" "john@example.com" --company "Acme" --labels "hot-lead,inbound"
  ./crm_cli.py update-pipeline c20260331120000 proposal_sent --deal "Enterprise License" --value 12000
  ./crm_cli.py log-interaction c20260331120000 email "Sent intro email about Denver market"
  ./crm_cli.py search "Acme"
  ./crm_cli.py pipeline
  ./crm_cli.py stats
""")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "init":
        crm_dir = sys.argv[2] if len(sys.argv) > 2 else None
        init_crm(crm_dir)
    
    elif command == "add-contact" and len(sys.argv) >= 4:
        crm_dir = DEFAULT_CRM_DIR
        name = sys.argv[2]
        email = sys.argv[3]
        
        # Parse optional args
        kwargs = {}
        i = 4
        while i < len(sys.argv):
            if sys.argv[i] == "--company" and i + 1 < len(sys.argv):
                kwargs["company"] = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--phone" and i + 1 < len(sys.argv):
                kwargs["phone"] = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--labels" and i + 1 < len(sys.argv):
                kwargs["labels"] = sys.argv[i + 1].split(",")
                i += 2
            elif sys.argv[i] == "--notes" and i + 1 < len(sys.argv):
                kwargs["notes"] = sys.argv[i + 1]
                i += 2
            else:
                i += 1
        
        add_contact(crm_dir, name, email, **kwargs)
    
    elif command == "update-pipeline" and len(sys.argv) >= 4:
        crm_dir = DEFAULT_CRM_DIR
        contact_id = sys.argv[2]
        stage = sys.argv[3]
        
        kwargs = {}
        i = 4
        while i < len(sys.argv):
            if sys.argv[i] == "--deal" and i + 1 < len(sys.argv):
                kwargs["deal"] = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--value" and i + 1 < len(sys.argv):
                kwargs["value"] = float(sys.argv[i + 1])
                i += 2
            else:
                i += 1
        
        update_pipeline(crm_dir, contact_id, stage, **kwargs)
    
    elif command == "log-interaction" and len(sys.argv) >= 5:
        crm_dir = DEFAULT_CRM_DIR
        contact_id = sys.argv[2]
        interaction_type = sys.argv[3]
        summary = " ".join(sys.argv[4:])
        log_interaction(crm_dir, contact_id, interaction_type, summary)
    
    elif command == "search" and len(sys.argv) >= 3:
        crm_dir = DEFAULT_CRM_DIR
        query = sys.argv[2]
        search_contacts(crm_dir, query)
    
    elif command == "pipeline":
        crm_dir = DEFAULT_CRM_DIR
        list_pipeline(crm_dir)
    
    elif command == "stats":
        crm_dir = DEFAULT_CRM_DIR
        get_stats(crm_dir)
    
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
