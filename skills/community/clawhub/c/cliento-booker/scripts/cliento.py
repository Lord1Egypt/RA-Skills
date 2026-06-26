#!/usr/bin/env python3
import sys
import json
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime

# Script for securely executing cliento API workflows without raw curl

def usage():
    print("""Usage: cliento.py <command> [args]
Commands:
  register <url>
  slots <company_id> <service_id> <from_date> <to_date> [resource_id]
  reserve <company_id> <slot_key>
  confirm <company_id> <cb_uuid> <first_name> <last_name> <email> <phone> <note> <booked_specific> [pin]""")
    sys.exit(1)

def request(url, payload=None, method="GET"):
    req = urllib.request.Request(url, method=method)
    if payload:
        req.add_header('Content-Type', 'application/json')
        data = json.dumps(payload).encode('utf-8')
    else:
        data = None
    try:
        with urllib.request.urlopen(req, data=data) as response:
            return response.read().decode('utf-8')
    except urllib.error.URLError as e:
        if hasattr(e, 'read'):
            return e.read().decode('utf-8')
        return str(e)

def register(url):
    html = request(url)
    print(html) # Raw html output for the agent to parse

def slots(company_id, service_id, from_date, to_date, resource_id=None):
    url = f"https://web.prod.cliento.com/api/v2/partner/cliento/{company_id}/resources/slots?fromDate={from_date}&srvIds={service_id}&toDate={to_date}"
    if resource_id:
        url += f"&resIds={resource_id}"
    print(request(url))

def reserve(company_id, slot_key):
    url = f"https://web.prod.cliento.com/api/v2/partner/cliento/{company_id}/booking/reserve"
    payload = {"slotKey": slot_key}
    print(request(url, payload, method="POST"))

def _step_1_custom(company_id, service_id, resource_id):
    # Used internally
    url = f"https://cliento.com/api/v2/partner/cliento/{company_id}/custom-fields/resource/{resource_id}?srvIds={service_id}"
    return request(url)

def confirm(company_id, cb_uuid, first_name, last_name, email, phone, note, booked_specific, pin=None):
    # Step 2
    url2 = f"https://cliento.com/api/v2/partner/cliento/{company_id}/booking/customer"
    payload2 = {
        "cbUuid": cb_uuid,
        "name": f"{first_name} {last_name}".strip(),
        "email": email,
        "phone": phone,
        "note": note if note else "",
        "customFields": None,
        "allowMarketing": None,
        "bookedSpecificResource": str(booked_specific).lower() == 'true',
        "attributes": None
    }
    r2 = request(url2, payload2, method="POST")
    
    # Step 3
    url3 = f"https://cliento.com/api/v2/partner/cliento/{company_id}/booking/confirmation-options"
    payload3 = {"cbUuid": cb_uuid}
    r3 = request(url3, payload3, method="POST")
    try:
        opts = json.loads(r3)
        if type(opts) is list and len(opts) > 0 and opts[0].get("confirmationMethod") != "NoPin" and pin is None:
             print(json.dumps({"error": "PIN required but not provided", "options_response": opts}))
             return
    except:
        pass

    # Step 4
    url4 = f"https://cliento.com/api/v2/partner/cliento/{company_id}/booking/confirm"
    payload4 = {"cbUuid": cb_uuid, "pin": pin if pin else ""}
    r4 = request(url4, payload4, method="POST")
    print(json.dumps({"step2": r2, "step3": r3, "step4": r4}))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
    
    cmd = sys.argv[1]
    args = sys.argv[2:]
    
    try:
        if cmd == "register":
            register(*args)
        elif cmd == "slots":
            slots(*args)
        elif cmd == "reserve":
            reserve(*args)
        elif cmd == "confirm":
            confirm(*args)
        else:
            usage()
    except Exception as e:
        print(json.dumps({"error": str(e)}))
