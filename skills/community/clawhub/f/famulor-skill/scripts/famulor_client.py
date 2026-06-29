"""
Famulor API Client — full wrapper around the Famulor REST API.

Covers all documented endpoint groups (docs.famulor.io):
  - User (me)
  - Assistants (CRUD, lookups, webhooks)
  - Knowledge Bases & Documents (CRUD)
  - Phone Numbers (list, search, purchase, update, release)
  - SIP Trunks (CRUD)
  - Calls (make, get, list, delete)
  - Campaigns (list, create, update status, delete)
  - Leads (CRUD)
  - Mid-Call Tools (CRUD)
  - SMS & WhatsApp
  - AI Chatbot Conversations & AI Replies
  - Folders & Labels

Usage:
    from famulor_client import FamulorClient
    client = FamulorClient()  # reads FAMULOR_API_KEY from env

CLI:
    python3 famulor_client.py <method> [args...] [key=value ...]
"""

import requests
import os
import json
import sys


class FamulorClient:

    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("FAMULOR_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key required. Set FAMULOR_API_KEY env var or pass api_key param. "
                "Get your key at https://app.famulor.de → API Keys."
            )
        self.base_url = "https://app.famulor.de/api"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    # ── Internal ────────────────────────────────────────────────────────

    def _request(self, method, endpoint, data=None, params=None, files=None):
        url = f"{self.base_url}{endpoint}"
        try:
            if files:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Accept": "application/json",
                }
                resp = requests.request(method, url, headers=headers, data=data, files=files, params=params)
            else:
                resp = requests.request(method, url, headers=self.headers, json=data, params=params)
            resp.raise_for_status()
            if resp.status_code == 204:
                return {"status": True}
            return resp.json()
        except requests.exceptions.HTTPError as e:
            error_body = {}
            try:
                error_body = e.response.json()
            except Exception:
                error_body = {"raw": e.response.text}
            return {
                "error": True,
                "status_code": e.response.status_code,
                "message": error_body.get("message", str(e)),
                "errors": error_body.get("errors", {}),
            }

    # ── User ────────────────────────────────────────────────────────────

    def get_me(self):
        """Account info of the authenticated user (balance, plan, etc.)."""
        return self._request("GET", "/user/me")

    # ── Assistants ──────────────────────────────────────────────────────

    def create_assistant(self, payload: dict):
        """Create assistant. Payload must include all required fields.
        IMPORTANT: The correct endpoint is POST /user/assistant (singular)."""
        return self._request("POST", "/user/assistant", data=payload)

    def update_assistant(self, assistant_id, payload: dict):
        """Update assistant. PUT /user/assistant/{id} (singular).
        WARNING: `tools` in the payload REPLACES all existing built-in tools."""
        return self._request("PUT", f"/user/assistant/{assistant_id}", data=payload)

    def delete_assistant(self, assistant_id):
        return self._request("DELETE", f"/user/assistant/{assistant_id}")

    def list_assistants(self, per_page=100, page=1):
        return self._request("GET", "/user/assistants/get", params={"per_page": per_page, "page": page})

    def get_outbound_assistants(self):
        return self._request("GET", "/user/assistants/outbound")

    # ── Lookup ──────────────────────────────────────────────────────────

    def get_languages(self):
        return self._request("GET", "/user/assistants/languages")

    def get_voices(self, mode=None, language_id=None):
        """mode: pipeline | multimodal | dualplex; language_id: from get_languages()"""
        params = {}
        if mode:
            params["mode"] = mode
        if language_id:
            params["language_id"] = language_id
        return self._request("GET", "/user/assistants/voices", params=params)

    def get_models(self, type=None):
        """type: llm (pipeline, default) | multimodal | dualplex"""
        params = {"type": type} if type else {}
        return self._request("GET", "/user/assistants/models", params=params)

    def get_phone_numbers(self, type=None):
        """Phone numbers eligible for assistant assignment. type: inbound | outbound"""
        params = {"type": type} if type else {}
        return self._request("GET", "/user/assistants/phone-numbers", params=params)

    def get_synthesizer_providers(self):
        return self._request("GET", "/user/assistants/synthesizer-providers")

    def get_transcriber_providers(self):
        return self._request("GET", "/user/assistants/transcriber-providers")

    # ── Knowledge Bases ─────────────────────────────────────────────────

    def create_knowledgebase(self, name, description=None):
        data = {"name": name}
        if description:
            data["description"] = description
        return self._request("POST", "/user/knowledgebases", data=data)

    def list_knowledgebases(self):
        return self._request("GET", "/user/knowledgebases")

    def get_knowledgebase(self, kb_id):
        return self._request("GET", f"/user/knowledgebases/{kb_id}")

    def update_knowledgebase(self, kb_id, name=None, description=None):
        data = {}
        if name:
            data["name"] = name
        if description:
            data["description"] = description
        return self._request("PUT", f"/user/knowledgebases/{kb_id}", data=data)

    def delete_knowledgebase(self, kb_id):
        return self._request("DELETE", f"/user/knowledgebases/{kb_id}")

    # ── Documents ───────────────────────────────────────────────────────

    def create_document(self, kb_id, name, doc_type, description=None,
                        url=None, links=None, relative_links_limit=None, file_path=None):
        """doc_type: website | pdf | txt | docx. Processing is asynchronous."""
        if file_path:
            form_data = {"name": name, "type": doc_type}
            if description:
                form_data["description"] = description
            files = {"file": open(file_path, "rb")}
            return self._request("POST", f"/user/knowledgebases/{kb_id}/documents",
                                 data=form_data, files=files)
        else:
            data = {"name": name, "type": doc_type}
            if description:
                data["description"] = description
            if url:
                data["url"] = url
            if links:
                data["links"] = links
            if relative_links_limit:
                data["relative_links_limit"] = relative_links_limit
            return self._request("POST", f"/user/knowledgebases/{kb_id}/documents", data=data)

    def list_documents(self, kb_id):
        return self._request("GET", f"/user/knowledgebases/{kb_id}/documents")

    def get_document(self, kb_id, document_id):
        """Also useful to poll the async processing status of a document."""
        return self._request("GET", f"/user/knowledgebases/{kb_id}/documents/{document_id}")

    def update_document(self, kb_id, document_id, name=None, description=None):
        data = {}
        if name:
            data["name"] = name
        if description:
            data["description"] = description
        return self._request("PUT", f"/user/knowledgebases/{kb_id}/documents/{document_id}", data=data)

    def delete_document(self, kb_id, document_id):
        return self._request("DELETE", f"/user/knowledgebases/{kb_id}/documents/{document_id}")

    # ── Phone Numbers ───────────────────────────────────────────────────

    def list_phone_numbers(self):
        """All phone numbers on the account."""
        return self._request("GET", "/user/phone-numbers/all")

    def search_phone_numbers(self, country_code, contains=None):
        """Search purchasable numbers. country_code e.g. 'DE', 'US'."""
        params = {"country_code": country_code}
        if contains:
            params["contains"] = contains
        return self._request("GET", "/user/phone-numbers/search", params=params)

    def purchase_phone_number(self, phone_number):
        return self._request("POST", "/user/phone-numbers/purchase",
                             data={"phone_number": phone_number})

    def update_phone_number(self, phone_number_id, nickname):
        return self._request("PUT", f"/user/phone-numbers/{phone_number_id}",
                             data={"nickname": nickname})

    def release_phone_number(self, phone_number_id):
        """Releases the number and cancels its subscription."""
        return self._request("DELETE", f"/user/phone-numbers/{phone_number_id}")

    # ── SIP Trunks ──────────────────────────────────────────────────────

    def list_sip_trunks(self):
        return self._request("GET", "/user/phone-numbers/sip-trunks")

    def get_sip_trunk(self, trunk_id):
        return self._request("GET", f"/user/phone-numbers/sip-trunks/{trunk_id}")

    def create_sip_trunk(self, payload: dict):
        return self._request("POST", "/user/phone-numbers/sip-trunks", data=payload)

    def update_sip_trunk(self, trunk_id, payload: dict):
        return self._request("PUT", f"/user/phone-numbers/sip-trunks/{trunk_id}", data=payload)

    def delete_sip_trunk(self, phone_number_id):
        """Deleting a SIP trunk releases its phone number entry."""
        return self._request("DELETE", f"/user/phone-numbers/{phone_number_id}")

    # ── Calls ───────────────────────────────────────────────────────────

    def make_call(self, assistant_id, phone_number, variables=None):
        """Start an outbound call. phone_number in E.164 (e.g. +491701234567)."""
        data = {"assistant_id": assistant_id, "phone_number": phone_number}
        if variables:
            data["variables"] = variables
        return self._request("POST", "/user/make_call", data=data)

    def list_calls(self, assistant_id=None, page=1, per_page=25):
        params = {"page": page, "per_page": per_page}
        if assistant_id:
            params["assistant_id"] = assistant_id
        return self._request("GET", "/user/calls", params=params)

    def get_call(self, call_id):
        return self._request("GET", f"/user/calls/{call_id}")

    def delete_call(self, call_id):
        return self._request("DELETE", f"/user/calls/{call_id}")

    # ── Campaigns ───────────────────────────────────────────────────────

    def list_campaigns(self):
        return self._request("GET", "/user/campaigns")

    def create_campaign(self, payload: dict):
        return self._request("POST", "/user/campaigns", data=payload)

    def update_campaign_status(self, campaign_id, status):
        """status: start | stop (per docs: starts or stops a campaign)."""
        return self._request("POST", "/user/campaigns/update-status",
                             data={"campaign_id": campaign_id, "status": status})

    def delete_campaign(self, campaign_id):
        return self._request("DELETE", f"/user/campaign/{campaign_id}")

    # ── Leads ───────────────────────────────────────────────────────────

    def list_leads(self, page=1, per_page=25):
        return self._request("GET", "/user/leads", params={"page": page, "per_page": per_page})

    def create_lead(self, payload: dict):
        """POST /user/lead (singular). Variable names must match the assistant's variables."""
        return self._request("POST", "/user/lead", data=payload)

    def update_lead(self, lead_id, payload: dict):
        """NOTE: PUT /leads/{id} (no /user prefix, per docs)."""
        return self._request("PUT", f"/leads/{lead_id}", data=payload)

    def delete_lead(self, lead_id):
        return self._request("DELETE", f"/user/leads/{lead_id}")

    # ── Mid-Call Tools (custom API integrations) ────────────────────────

    def list_mid_call_tools(self):
        return self._request("GET", "/user/tools")

    def get_mid_call_tool(self, tool_id):
        return self._request("GET", f"/user/tools/{tool_id}")

    def create_mid_call_tool(self, payload: dict):
        return self._request("POST", "/user/tools", data=payload)

    def update_mid_call_tool(self, tool_id, payload: dict):
        return self._request("PUT", f"/user/tools/{tool_id}", data=payload)

    def delete_mid_call_tool(self, tool_id):
        return self._request("DELETE", f"/user/tools/{tool_id}")

    # ── SMS ─────────────────────────────────────────────────────────────

    def send_sms(self, to, message, from_number=None):
        """Send an SMS via your Famulor phone number."""
        data = {"to": to, "message": message}
        if from_number:
            data["from"] = from_number
        return self._request("POST", "/user/sms", data=data)

    # ── WhatsApp ────────────────────────────────────────────────────────

    def get_whatsapp_senders(self, status=None):
        params = {"status": status} if status else {}
        return self._request("GET", "/user/whatsapp/senders", params=params)

    def get_whatsapp_templates(self, sender_id, status=None):
        params = {"status": status} if status else {}
        return self._request("GET", f"/user/whatsapp/senders/{sender_id}/templates", params=params)

    def get_whatsapp_session_status(self, sender_id, recipient_phone):
        """Check if the 24h messaging window is open for a recipient."""
        return self._request("GET", "/user/whatsapp/session-status",
                             params={"sender_id": sender_id, "recipient_phone": recipient_phone})

    def send_whatsapp_template(self, payload: dict):
        """Send a template message (works outside the 24h window)."""
        return self._request("POST", "/user/whatsapp/send", data=payload)

    def send_whatsapp_freeform(self, payload: dict):
        """Send a freeform message (only within an active 24h window)."""
        return self._request("POST", "/user/whatsapp/send-freeform", data=payload)

    # ── AI Replies ──────────────────────────────────────────────────────

    def generate_ai_reply(self, payload: dict):
        """Generate an AI reply with an assistant based on a customer identifier."""
        return self._request("POST", "/user/ai/generate-reply", data=payload)

    # ── Conversations (AI Chatbot) ──────────────────────────────────────

    def list_conversations(self, **params):
        """Filters: type, assistant_id, customer_phone, external_identifier, per_page, cursor."""
        return self._request("GET", "/user/conversations", params=params or None)

    def get_conversation(self, conversation_uuid):
        return self._request("GET", f"/conversations/{conversation_uuid}")

    def create_conversation(self, assistant_uuid, type="widget", variables=None):
        """assistant_uuid: the assistant's UUID (string), not the numeric ID.
        type 'test' is free (development), 'widget' is paid."""
        data = {"assistant_id": assistant_uuid, "type": type}
        if variables:
            data["variables"] = variables
        return self._request("POST", "/conversations", data=data)

    def send_message(self, conversation_uuid, message):
        return self._request("POST", f"/conversations/{conversation_uuid}/messages",
                             data={"message": message})

    def enable_conversation_ai(self, conversation_uuid):
        """Re-enable AI replies after a human takeover."""
        return self._request("POST", f"/automate/conversations/{conversation_uuid}/enable-ai")

    def disable_conversation_ai(self, conversation_uuid):
        """Disable AI replies for a conversation (human takeover)."""
        return self._request("POST", f"/automate/conversations/{conversation_uuid}/disable-ai")

    # ── Test (convenience aliases) ──────────────────────────────────────

    def create_test_conversation(self, assistant_uuid):
        """Free test conversation (development)."""
        return self.create_conversation(assistant_uuid, type="test")

    def send_test_message(self, conversation_uuid, message):
        return self.send_message(conversation_uuid, message)

    # ── Webhooks ────────────────────────────────────────────────────────
    # All webhook endpoints take the assistant_id in the body (not in the URL).

    def enable_inbound_webhook(self, assistant_id, webhook_url):
        return self._request("POST", "/user/assistants/enable-inbound-webhook",
                             data={"assistant_id": assistant_id, "webhook_url": webhook_url})

    def disable_inbound_webhook(self, assistant_id):
        return self._request("POST", "/user/assistants/disable-inbound-webhook",
                             data={"assistant_id": assistant_id})

    def enable_conversation_ended_webhook(self, assistant_id, webhook_url):
        return self._request("POST", "/user/assistants/enable-conversation-ended-webhook",
                             data={"assistant_id": assistant_id, "webhook_url": webhook_url})

    def disable_conversation_ended_webhook(self, assistant_id):
        return self._request("POST", "/user/assistants/disable-conversation-ended-webhook",
                             data={"assistant_id": assistant_id})

    def disable_webhook(self, assistant_id):
        """Disable the post-call webhook of an assistant."""
        return self._request("POST", "/user/assistants/disable-webhook",
                             data={"assistant_id": assistant_id})

    # ── Folders ─────────────────────────────────────────────────────────

    def list_folders(self, page=1, per_page=50):
        return self._request("GET", "/user/folders", params={"page": page, "per_page": per_page})

    def create_folder(self, name, color=None):
        data = {"name": name}
        if color:
            data["color"] = color
        return self._request("POST", "/user/folder", data=data)

    def update_folder(self, folder_id, name=None, color=None):
        data = {}
        if name:
            data["name"] = name
        if color:
            data["color"] = color
        return self._request("PUT", f"/user/folder/{folder_id}", data=data)

    def delete_folder(self, folder_id):
        return self._request("DELETE", f"/user/folder/{folder_id}")

    # ── Labels ──────────────────────────────────────────────────────────

    def list_labels(self, page=1, per_page=50):
        return self._request("GET", "/user/labels", params={"page": page, "per_page": per_page})

    def create_label(self, name, color=None):
        data = {"name": name}
        if color:
            data["color"] = color
        return self._request("POST", "/user/label", data=data)

    def update_label(self, label_id, name=None, color=None):
        data = {}
        if name:
            data["name"] = name
        if color:
            data["color"] = color
        return self._request("PUT", f"/user/label/{label_id}", data=data)

    def delete_label(self, label_id):
        return self._request("DELETE", f"/user/label/{label_id}")


# ── CLI ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 famulor_client.py <method> [args...] [key=value ...]")
        client_methods = [m for m in dir(FamulorClient)
                         if not m.startswith("_") and callable(getattr(FamulorClient, m))]
        for m in sorted(client_methods):
            print(f"  {m}")
        sys.exit(1)

    client = FamulorClient()
    method_name = sys.argv[1]
    method = getattr(client, method_name, None)
    if not method:
        print(f"Error: Method '{method_name}' not found.")
        sys.exit(1)

    args = sys.argv[2:]
    positional_args = []
    kwargs = {}
    for arg in args:
        if "=" in arg:
            key, value = arg.split("=", 1)
            try:
                kwargs[key] = json.loads(value)
            except (json.JSONDecodeError, ValueError):
                kwargs[key] = value
        else:
            try:
                positional_args.append(json.loads(arg))
            except (json.JSONDecodeError, ValueError):
                positional_args.append(arg)

    result = method(*positional_args, **kwargs)
    print(json.dumps(result, indent=2, ensure_ascii=False))
