#!/usr/bin/env python3
"""
GHL CRM Mastery — API CLI Tool
SetupClaw.Tech · v1.3.0

Usage:
    # Contacts
    python3 ghl_api.py contacts list [--limit N]
    python3 ghl_api.py contacts get --id "CONTACT_ID"
    python3 ghl_api.py contacts search --query "email@example.com"
    python3 ghl_api.py contacts search-phone --query "+15555550123"
    python3 ghl_api.py contacts update --id "CONTACT_ID" --field value
    python3 ghl_api.py contacts add-tags --id "CONTACT_ID" --tags "tag1,tag2"
    python3 ghl_api.py contacts remove-tag --id "CONTACT_ID" --tag-id "TAG_ID"

    # Conversations
    python3 ghl_api.py conversations list [--limit N]
    python3 ghl_api.py conversations get --contact-id "CONTACT_ID"
    python3 ghl_api.py conversations send --contact-id "CONTACT_ID" --message "Hello" --type sms

    # Notes
    python3 ghl_api.py notes add --contact-id "CONTACT_ID" --body "Research findings..."
    python3 ghl_api.py notes list --contact-id "CONTACT_ID"

    # Opportunities
    python3 ghl_api.py opportunities list [--limit N]
    python3 ghl_api.py opportunities get --id "OPP_ID"
    python3 ghl_api.py opportunities update --id "OPP_ID" --stage "STAGE_ID"

    # Calendars
    python3 ghl_api.py calendars list
    python3 ghl_api.py calendars events --id "CALENDAR_ID"

    # Tags, Forms, Workflows
    python3 ghl_api.py tags list
    python3 ghl_api.py forms list
    python3 ghl_api.py forms submissions --id "FORM_ID"
    python3 ghl_api.py workflows list
    python3 ghl_api.py workflows trigger --id "WORKFLOW_ID" --contact-id "CONTACT_ID"

    # System
    python3 ghl_api.py health

Environment variables required:
    GHL_API_KEY       - GoHighLevel Private Integration Token
    GHL_LOCATION_ID   - GoHighLevel Location ID
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime

BASE_URL = "https://services.leadconnectorhq.com"
API_KEY = os.environ.get("GHL_API_KEY", "")
LOCATION_ID = os.environ.get("GHL_LOCATION_ID", "")

MAX_RETRIES = 3
RETRY_DELAY = 2


def check_env():
    if not API_KEY:
        print("ERROR: GHL_API_KEY not set.")
        print("Run: export GHL_API_KEY=$(grep GHL_API_KEY ~/.openclaw/.env | cut -d= -f2)")
        sys.exit(1)
    if not LOCATION_ID:
        print("ERROR: GHL_LOCATION_ID not set.")
        print("Run: export GHL_LOCATION_ID=$(grep GHL_LOCATION_ID ~/.openclaw/.env | cut -d= -f2)")
        sys.exit(1)


def api_request(method, path, params=None, body=None):
    check_env()
    url = f"{BASE_URL}{path}"
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Version": "2021-07-28",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    data = json.dumps(body).encode() if body else None

    for attempt in range(MAX_RETRIES):
        try:
            req = urllib.request.Request(url, data=data, headers=headers, method=method)
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = RETRY_DELAY * (2 ** attempt)
                print(f"  Rate limited. Waiting {wait}s... ({attempt + 1}/{MAX_RETRIES})")
                time.sleep(wait)
                continue
            elif e.code == 500 and attempt == 0:
                print("  Server error (500). Retrying in 5s...")
                time.sleep(5)
                continue
            else:
                error_body = e.read().decode() if e.fp else ""
                print(f"ERROR: HTTP {e.code} - {e.reason}")
                if error_body:
                    try:
                        print(json.dumps(json.loads(error_body), indent=2))
                    except json.JSONDecodeError:
                        print(error_body)
                sys.exit(1)
        except urllib.error.URLError as e:
            print(f"ERROR: Connection failed - {e.reason}")
            sys.exit(1)

    print(f"ERROR: Max retries ({MAX_RETRIES}) exceeded.")
    sys.exit(1)


# === CONTACTS ===

def cmd_contacts_list(limit=5):
    data = api_request("GET", "/contacts/", params={"locationId": LOCATION_ID, "limit": limit})
    contacts = data.get("contacts", [])
    print(f"Contacts ({len(contacts)} of {data.get('meta', {}).get('total', '?')}):")
    for c in contacts:
        name = f"{c.get('firstName', '')} {c.get('lastName', '')}".strip() or "(no name)"
        print(f"  - {name} | {c.get('email', '—')} | {c.get('phone', '—')} | ID: {c.get('id', '?')}")
    return data

def cmd_contacts_get(contact_id):
    data = api_request("GET", f"/contacts/{contact_id}")
    c = data.get("contact", data)
    name = f"{c.get('firstName', '')} {c.get('lastName', '')}".strip() or "(no name)"
    print(f"Contact: {name}")
    print(f"  Email: {c.get('email', '—')}")
    print(f"  Phone: {c.get('phone', '—')}")
    print(f"  Company: {c.get('companyName', '—')}")
    print(f"  Tags: {', '.join(c.get('tags', [])) or '—'}")
    print(f"  Source: {c.get('source', '—')}")
    print(f"  Date Added: {c.get('dateAdded', '—')}")
    print(f"  ID: {c.get('id', '?')}")
    custom = c.get("customFields", c.get("customField", []))
    if custom:
        print("  Custom Fields:")
        for cf in custom:
            print(f"    {cf.get('id', '?')}: {cf.get('value', '—')}")
    return data

def cmd_contacts_search(query):
    data = api_request("GET", "/contacts/search/duplicate", params={"locationId": LOCATION_ID, "email": query})
    contacts = data.get("contacts", data.get("contact", []))
    if isinstance(contacts, dict):
        contacts = [contacts]
    print(f"Search by email '{query}': {len(contacts)} found")
    for c in contacts:
        name = f"{c.get('firstName', '')} {c.get('lastName', '')}".strip()
        print(f"  - {name} | {c.get('email', '')} | {c.get('phone', '')} | ID: {c.get('id', '?')}")
    return data

def cmd_contacts_search_phone(query):
    data = api_request("GET", "/contacts/search/duplicate", params={"locationId": LOCATION_ID, "phone": query})
    contacts = data.get("contacts", data.get("contact", []))
    if isinstance(contacts, dict):
        contacts = [contacts]
    print(f"Search by phone '{query}': {len(contacts)} found")
    for c in contacts:
        name = f"{c.get('firstName', '')} {c.get('lastName', '')}".strip()
        print(f"  - {name} | {c.get('email', '')} | {c.get('phone', '')} | ID: {c.get('id', '?')}")
    return data

def cmd_contacts_update(contact_id, updates):
    data = api_request("PUT", f"/contacts/{contact_id}", body=updates)
    print(f"  ✓ Contact {contact_id} updated: {json.dumps(updates)}")
    return data

def cmd_contacts_add_tags(contact_id, tags):
    data = api_request("POST", f"/contacts/{contact_id}/tags", body={"tags": tags})
    print(f"  ✓ Tags added to {contact_id}: {', '.join(tags)}")
    return data

def cmd_contacts_remove_tag(contact_id, tag_id):
    data = api_request("DELETE", f"/contacts/{contact_id}/tags/{tag_id}")
    print(f"  ✓ Tag {tag_id} removed from {contact_id}")
    return data


# === CONVERSATIONS ===

def cmd_conversations_list(limit=5):
    data = api_request("GET", "/conversations/search", params={"locationId": LOCATION_ID, "limit": limit})
    convos = data.get("conversations", [])
    print(f"Conversations ({len(convos)}):")
    for c in convos:
        print(f"  - ID: {c.get('id', '?')} | Contact: {c.get('contactId', '?')} | Last: {c.get('lastMessageDate', '?')}")
    return data

def cmd_conversations_get(contact_id):
    data = api_request("GET", "/conversations/search", params={"locationId": LOCATION_ID, "contactId": contact_id})
    convos = data.get("conversations", [])
    if not convos:
        print(f"No conversations found for contact {contact_id}")
        return data
    convo_id = convos[0].get("id")
    print(f"Conversation ID: {convo_id}")
    messages = api_request("GET", f"/conversations/{convo_id}/messages", params={"limit": 20})
    msgs = messages.get("messages", {}).get("messages", messages.get("messages", []))
    if isinstance(msgs, list):
        print(f"Messages ({len(msgs)}):")
        for m in msgs:
            direction = m.get("direction", "?")
            body = m.get("body", "(no body)")
            ts = m.get("dateAdded", "?")
            msg_type = m.get("type", "?")
            print(f"  [{direction}] [{msg_type}] {ts}: {body[:200]}")
    return messages

def cmd_conversations_send(contact_id, message, msg_type="SMS"):
    """Send a message via GHL. TCPA compliance enforced by handler layer."""
    timestamp = datetime.utcnow().isoformat() + "Z"
    body = {"type": msg_type, "contactId": contact_id, "message": message}
    data = api_request("POST", "/conversations/messages", body=body)
    print(f"  ✓ [{timestamp}] OUTBOUND {msg_type} to {contact_id}: {message[:100]}")
    return data


# === NOTES ===

def cmd_notes_add(contact_id, body_text):
    timestamp = datetime.utcnow().isoformat() + "Z"
    data = api_request("POST", f"/contacts/{contact_id}/notes", body={"body": body_text, "userId": ""})
    print(f"  ✓ Note added to {contact_id} at {timestamp}")
    return data

def cmd_notes_list(contact_id):
    data = api_request("GET", f"/contacts/{contact_id}/notes")
    notes = data.get("notes", [])
    print(f"Notes for {contact_id} ({len(notes)}):")
    for n in notes:
        print(f"  [{n.get('dateAdded', '?')}] {n.get('body', '(empty)')[:200]}")
    return data


# === OPPORTUNITIES ===

def cmd_opportunities_list(limit=5):
    data = api_request("GET", "/opportunities/search", params={"location_id": LOCATION_ID, "limit": limit})
    opps = data.get("opportunities", [])
    print(f"Opportunities ({len(opps)}):")
    for o in opps:
        print(f"  - {o.get('name', '?')} | Stage: {o.get('pipelineStageId', '?')} | Value: ${o.get('monetaryValue', 0)}")
    return data

def cmd_opportunities_get(opp_id):
    data = api_request("GET", f"/opportunities/{opp_id}")
    o = data.get("opportunity", data)
    print(f"Opportunity: {o.get('name', '?')}")
    print(f"  Stage: {o.get('pipelineStageId', '?')} | Value: ${o.get('monetaryValue', 0)} | Status: {o.get('status', '?')}")
    return data

def cmd_opportunities_update(opp_id, stage_id):
    data = api_request("PUT", f"/opportunities/{opp_id}", body={"pipelineStageId": stage_id})
    print(f"  ✓ Opportunity {opp_id} moved to stage {stage_id}")
    return data


# === CALENDARS ===

def cmd_calendars_list():
    data = api_request("GET", "/calendars/", params={"locationId": LOCATION_ID})
    cals = data.get("calendars", [])
    print(f"Calendars ({len(cals)}):")
    for c in cals:
        print(f"  - {c.get('name', '?')} | ID: {c.get('id', '?')}")
    return data

def cmd_calendars_events(cal_id):
    data = api_request("GET", f"/calendars/{cal_id}/events", params={"locationId": LOCATION_ID})
    events = data.get("events", [])
    print(f"Events ({len(events)}):")
    for e in events:
        print(f"  - {e.get('title', '?')} | {e.get('startTime', '?')} | Contact: {e.get('contactId', '?')}")
    return data


# === TAGS, FORMS, WORKFLOWS ===

def cmd_tags_list():
    data = api_request("GET", f"/locations/{LOCATION_ID}/tags")
    tags = data.get("tags", [])
    print(f"Tags ({len(tags)}):")
    for t in tags:
        print(f"  - {t.get('name', '?')} | ID: {t.get('id', '?')}")
    return data

def cmd_forms_list():
    data = api_request("GET", "/forms/", params={"locationId": LOCATION_ID})
    forms = data.get("forms", [])
    print(f"Forms ({len(forms)}):")
    for f_item in forms:
        print(f"  - {f_item.get('name', '?')} | ID: {f_item.get('id', '?')}")
    return data

def cmd_forms_submissions(form_id):
    data = api_request("GET", "/forms/submissions", params={"formId": form_id, "locationId": LOCATION_ID})
    subs = data.get("submissions", [])
    print(f"Submissions ({len(subs)}):")
    for s in subs:
        print(f"  - Contact: {s.get('contactId', '?')} | {s.get('createdAt', '?')}")
    return data

def cmd_workflows_list():
    data = api_request("GET", "/workflows/", params={"locationId": LOCATION_ID})
    workflows = data.get("workflows", [])
    print(f"Workflows ({len(workflows)}):")
    for w in workflows:
        print(f"  - {w.get('name', '?')} | ID: {w.get('id', '?')} | Status: {w.get('status', '?')}")
    return data

def cmd_workflows_trigger(workflow_id, contact_id):
    """Trigger only. NEVER create/edit/delete workflows."""
    data = api_request("POST", f"/workflows/{workflow_id}/trigger", body={"contactId": contact_id})
    print(f"  ✓ Workflow {workflow_id} triggered for {contact_id}")
    return data


# === HEALTH ===

def cmd_health():
    print("Checking GHL API connection...")
    print(f"  API Key: {API_KEY[:8]}...{API_KEY[-4:]}" if len(API_KEY) > 12 else f"  API Key: {API_KEY}")
    print(f"  Location: {LOCATION_ID}")
    print()
    try:
        data = api_request("GET", "/contacts/", params={"locationId": LOCATION_ID, "limit": 1})
        total = data.get("meta", {}).get("total", "?")
        print(f"  ✓ Connection OK — {total} contacts in location")
    except SystemExit:
        print("  ✗ Connection failed")
        sys.exit(1)


# === CLI ROUTER ===

def parse_args():
    args = sys.argv[1:]
    params = {}
    positional = []
    i = 0
    while i < len(args):
        if args[i].startswith("--") and i + 1 < len(args):
            params[args[i][2:]] = args[i + 1]
            i += 2
        else:
            positional.append(args[i])
            i += 1
    return positional, params


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    pos, params = parse_args()
    resource = pos[0] if pos else ""
    action = pos[1] if len(pos) > 1 else "list"
    limit = int(params.get("limit", 5))

    routes = {
        ("contacts", "list"): lambda: cmd_contacts_list(limit),
        ("contacts", "get"): lambda: cmd_contacts_get(params["id"]),
        ("contacts", "search"): lambda: cmd_contacts_search(params["query"]),
        ("contacts", "search-phone"): lambda: cmd_contacts_search_phone(params["query"]),
        ("contacts", "update"): lambda: cmd_contacts_update(params.pop("id"), params),
        ("contacts", "add-tags"): lambda: cmd_contacts_add_tags(params["id"], params["tags"].split(",")),
        ("contacts", "remove-tag"): lambda: cmd_contacts_remove_tag(params["id"], params["tag-id"]),
        ("conversations", "list"): lambda: cmd_conversations_list(limit),
        ("conversations", "get"): lambda: cmd_conversations_get(params["contact-id"]),
        ("conversations", "send"): lambda: cmd_conversations_send(params["contact-id"], params["message"], params.get("type", "SMS")),
        ("notes", "add"): lambda: cmd_notes_add(params["contact-id"], params["body"]),
        ("notes", "list"): lambda: cmd_notes_list(params["contact-id"]),
        ("opportunities", "list"): lambda: cmd_opportunities_list(limit),
        ("opportunities", "get"): lambda: cmd_opportunities_get(params["id"]),
        ("opportunities", "update"): lambda: cmd_opportunities_update(params["id"], params["stage"]),
        ("calendars", "list"): lambda: cmd_calendars_list(),
        ("calendars", "events"): lambda: cmd_calendars_events(params["id"]),
        ("tags", "list"): lambda: cmd_tags_list(),
        ("forms", "list"): lambda: cmd_forms_list(),
        ("forms", "submissions"): lambda: cmd_forms_submissions(params["id"]),
        ("workflows", "list"): lambda: cmd_workflows_list(),
        ("workflows", "trigger"): lambda: cmd_workflows_trigger(params["id"], params["contact-id"]),
        ("health", "list"): lambda: cmd_health(),
        ("health", "health"): lambda: cmd_health(),
    }

    handler = routes.get((resource, action))
    if handler:
        try:
            handler()
        except KeyError as e:
            print(f"Missing required parameter: --{e.args[0]}")
            print(f"Run: python3 ghl_api.py {resource} {action} --help")
            sys.exit(1)
    else:
        print(f"Unknown command: {resource} {action}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
