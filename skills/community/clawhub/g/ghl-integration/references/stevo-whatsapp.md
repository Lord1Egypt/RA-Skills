# GHL API v2 - Custom Provider (STEVO / WhatsApp QR) & Contact Resolution Reference

In GoHighLevel (GHL) locations using custom WhatsApp integrations like STEVO (Marketplace AppId: `682cd9287059b4173d8b17bd`), communications are routed through custom SMS pathways.

## 1. Inbound Message Payload Structure
When retrieving message history via `GET /conversations/{conversationId}/messages`, messages sent via STEVO carry:
* `"messageType": "TYPE_CUSTOM_SMS"`
* `"type": 20` (Internal channel type for custom gateway)
* Metadata pointing to the STEVO Marketplace App:
```json
{
  "meta": {
    "marketplace": {
      "appId": "682cd9287059b4173d8b17bd",
      "appName": "STEVO"
    }
  }
}
```

## 2. Outgoing Messaging Rule
To send automated WhatsApp messages through this integration using the API:
* Send the payload targeting the `"SMS"` type (`POST /conversations/messages` with `{"type": "SMS", "contactId": "...", "message": "..."}`). 
* The STEVO gateway automatically intercepts GHL outbound SMS payloads and delivers them to the recipient's phone number via WhatsApp (`Whatsapp QR`).

## 3. Contact Resolution & Duplicate Error Handling
When searching or creating contacts by phone:
* `POST /contacts/` returns HTTP 400 if duplicate contact prevention is enabled in the GHL location:
```json
{
  "statusCode": 400,
  "message": "This location does not allow duplicated contacts.",
  "meta": {
    "contactName": "...",
    "contactId": "WMQLFkkvBD0BWvElwFSw",
    "matchingField": "phone"
  }
}
```
* **Resolution Pattern:** When contact creation fails with HTTP 400 due to duplication, inspect `response["meta"]["contactId"]` directly to resolve the existing contact ID without failing the workflow.

## 4. Manager Notification Setup
To send system alerts (e.g. Stop-Loss alerts or qualified lead summaries) to the manager:
1. Store `MANAGER_PHONE` in environment or `.env`.
2. Resolve manager's contact ID using `find_or_create_contact_by_phone` (falling back to `meta.contactId` on duplicate error).
3. Post outbound message targeting `"type": "SMS"`.

## 5. Gateway Status and Disconnection Troubleshooting
In setups where STEVO/Papi integrations monitor the channel state:
* **Detection:** The CLI check (`ghl_client.py --action unanswered`) or system log outputs may display warning payloads or messages like:
  `[P-mon] papi_disconnected`
  `Instância Stevo '<instance_name_here>' está inactive`
* **Resolution:** This indicates the WhatsApp session has expired, crashed, or was unlinked from the phone. The operator must log into the STEVO / Papi control panel, locate the target instance, and scan the WhatsApp QR Code again to restore active messaging.
