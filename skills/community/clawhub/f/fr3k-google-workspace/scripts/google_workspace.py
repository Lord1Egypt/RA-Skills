#!/usr/bin/env python3
"""Google Workspace CLI — Gmail, Calendar, Drive, Sheets."""

import os
import sys
import json
import argparse
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, timedelta, timezone

try:
    from google.oauth2 import service_account
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
    import google.auth
except ImportError:
    print(json.dumps({
        "error": "google-api-python-client not installed",
        "fix": "pip install google-api-python-client google-auth google-auth-httplib2"
    }))
    sys.exit(1)

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
]


def get_credentials():
    sa_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if sa_json:
        try:
            info = json.loads(sa_json)
            creds = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
            # For Gmail/Calendar/Drive with domain-wide delegation, set subject
            subject = os.environ.get("GOOGLE_DELEGATED_USER")
            if subject:
                creds = creds.with_subject(subject)
            return creds
        except Exception as e:
            print(json.dumps({"error": f"Invalid GOOGLE_SERVICE_ACCOUNT_JSON: {e}"}))
            sys.exit(1)

    creds_file = os.environ.get("GOOGLE_CREDENTIALS_FILE")
    token_file = os.environ.get("GOOGLE_TOKEN_FILE", os.path.expanduser("~/.google_token.json"))
    if creds_file:
        from google.auth.transport.requests import Request
        from google_auth_oauthlib.flow import InstalledAppFlow
        creds = None
        if os.path.exists(token_file):
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(token_file, "w") as f:
                f.write(creds.to_json())
        return creds

    print(json.dumps({
        "error": "No Google credentials configured",
        "setup": "export GOOGLE_SERVICE_ACCOUNT_JSON='...' or export GOOGLE_CREDENTIALS_FILE=/path/to/creds.json"
    }))
    sys.exit(1)


def svc(name, version):
    return build(name, version, credentials=get_credentials())


def err(e):
    print(json.dumps({"error": str(e)}))
    sys.exit(1)


# ── GMAIL ───────────────────────────────────────────────

def gmail_inbox(args):
    try:
        gmail = svc("gmail", "v1")
        r = gmail.users().messages().list(userId="me", maxResults=args.limit, labelIds=["INBOX"]).execute()
        msgs = []
        for m in r.get("messages", []):
            msg = gmail.users().messages().get(userId="me", id=m["id"], format="metadata",
                                                metadataHeaders=["From", "To", "Subject", "Date"]).execute()
            headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
            msgs.append({
                "id": msg["id"],
                "subject": headers.get("Subject", ""),
                "from": headers.get("From", ""),
                "date": headers.get("Date", ""),
                "snippet": msg.get("snippet", "")[:100],
                "unread": "UNREAD" in msg.get("labelIds", [])
            })
        print(json.dumps(msgs, indent=2))
    except Exception as e:
        err(e)


def gmail_search(args):
    try:
        gmail = svc("gmail", "v1")
        r = gmail.users().messages().list(userId="me", q=args.query, maxResults=args.limit).execute()
        msgs = []
        for m in r.get("messages", []):
            msg = gmail.users().messages().get(userId="me", id=m["id"], format="metadata",
                                                metadataHeaders=["From", "To", "Subject", "Date"]).execute()
            headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
            msgs.append({
                "id": msg["id"],
                "subject": headers.get("Subject", ""),
                "from": headers.get("From", ""),
                "date": headers.get("Date", ""),
                "snippet": msg.get("snippet", "")[:150]
            })
        print(json.dumps(msgs, indent=2))
    except Exception as e:
        err(e)


def gmail_send(args):
    try:
        gmail = svc("gmail", "v1")
        if args.attachment:
            msg = MIMEMultipart()
            msg.attach(MIMEText(args.body, "plain"))
            with open(args.attachment, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(args.attachment)}")
                msg.attach(part)
        else:
            msg = MIMEText(args.body, "plain")

        msg["to"] = args.to
        msg["subject"] = args.subject
        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        r = gmail.users().messages().send(userId="me", body={"raw": raw}).execute()
        print(json.dumps({"id": r["id"], "thread_id": r["threadId"], "sent": True}))
    except Exception as e:
        err(e)


def gmail_label(args):
    try:
        gmail = svc("gmail", "v1")
        labels = gmail.users().labels().list(userId="me").execute()
        label_id = None
        for l in labels.get("labels", []):
            if l["name"].lower() == args.label.lower():
                label_id = l["id"]
                break
        if not label_id:
            print(json.dumps({"error": f"Label '{args.label}' not found. Available: " +
                              str([l["name"] for l in labels.get("labels", [])])}))
            return
        r = gmail.users().messages().modify(userId="me", id=args.message_id,
                                             body={"addLabelIds": [label_id]}).execute()
        print(json.dumps({"id": r["id"], "labels_applied": r.get("labelIds", [])}))
    except Exception as e:
        err(e)


def gmail_draft(args):
    try:
        gmail = svc("gmail", "v1")
        msg = MIMEText(args.body, "plain")
        msg["to"] = args.to
        msg["subject"] = args.subject
        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        r = gmail.users().drafts().create(userId="me", body={"message": {"raw": raw}}).execute()
        print(json.dumps({"draft_id": r["id"], "created": True}))
    except Exception as e:
        err(e)


# ── CALENDAR ────────────────────────────────────────────

def cal_list(args):
    try:
        cal = svc("calendar", "v3")
        now = datetime.now(timezone.utc)
        end = now + timedelta(days=args.days)
        r = cal.events().list(
            calendarId="primary",
            timeMin=now.isoformat(),
            timeMax=end.isoformat(),
            maxResults=args.limit,
            singleEvents=True,
            orderBy="startTime"
        ).execute()
        events = []
        for e in r.get("items", []):
            start = e["start"].get("dateTime", e["start"].get("date"))
            end_t = e["end"].get("dateTime", e["end"].get("date"))
            events.append({
                "id": e["id"],
                "title": e.get("summary", ""),
                "start": start, "end": end_t,
                "location": e.get("location", ""),
                "description": (e.get("description", "") or "")[:100]
            })
        print(json.dumps(events, indent=2))
    except Exception as e:
        err(e)


def cal_create(args):
    try:
        cal = svc("calendar", "v3")
        if args.all_day:
            event = {
                "summary": args.title,
                "start": {"date": args.start},
                "end": {"date": args.end or args.start}
            }
        else:
            tz = args.timezone or "UTC"
            event = {
                "summary": args.title,
                "start": {"dateTime": args.start, "timeZone": tz},
                "end": {"dateTime": args.end, "timeZone": tz}
            }
        if args.description:
            event["description"] = args.description
        r = cal.events().insert(calendarId="primary", body=event).execute()
        print(json.dumps({"id": r["id"], "title": r.get("summary"), "link": r.get("htmlLink")}))
    except Exception as e:
        err(e)


def cal_update(args):
    try:
        cal = svc("calendar", "v3")
        event = cal.events().get(calendarId="primary", eventId=args.event_id).execute()
        if args.title:
            event["summary"] = args.title
        if args.start:
            event["start"] = {"dateTime": args.start, "timeZone": event["start"].get("timeZone", "UTC")}
        if args.end:
            event["end"] = {"dateTime": args.end, "timeZone": event["end"].get("timeZone", "UTC")}
        r = cal.events().update(calendarId="primary", eventId=args.event_id, body=event).execute()
        print(json.dumps({"id": r["id"], "title": r.get("summary"), "updated": True}))
    except Exception as e:
        err(e)


def cal_delete(args):
    try:
        svc("calendar", "v3").events().delete(calendarId="primary", eventId=args.event_id).execute()
        print(json.dumps({"deleted": args.event_id}))
    except Exception as e:
        err(e)


# ── DRIVE ───────────────────────────────────────────────

def drive_list(args):
    try:
        drive = svc("drive", "v3")
        params = {"pageSize": args.limit, "fields": "files(id,name,mimeType,size,modifiedTime,webViewLink)"}
        if args.query:
            params["q"] = args.query
        r = drive.files().list(**params).execute()
        print(json.dumps(r.get("files", []), indent=2))
    except Exception as e:
        err(e)


def drive_upload(args):
    try:
        drive = svc("drive", "v3")
        meta = {"name": os.path.basename(args.file)}
        if args.folder_id:
            meta["parents"] = [args.folder_id]
        media = MediaFileUpload(args.file, resumable=True)
        r = drive.files().create(body=meta, media_body=media, fields="id,name,webViewLink").execute()
        print(json.dumps({"id": r["id"], "name": r["name"], "link": r.get("webViewLink")}))
    except Exception as e:
        err(e)


def drive_download(args):
    try:
        import io
        drive = svc("drive", "v3")
        output = args.output or args.file_id
        req = drive.files().get_media(fileId=args.file_id)
        buf = io.BytesIO()
        downloader = MediaIoBaseDownload(buf, req)
        done = False
        while not done:
            _, done = downloader.next_chunk()
        with open(output, "wb") as f:
            f.write(buf.getvalue())
        print(json.dumps({"downloaded": args.file_id, "saved_to": output}))
    except Exception as e:
        err(e)


def drive_share(args):
    try:
        drive = svc("drive", "v3")
        if args.anyone_link:
            perm = {"type": "anyone", "role": "reader"}
        else:
            perm = {"type": "user", "role": args.role or "reader", "emailAddress": args.email}
        r = drive.permissions().create(fileId=args.file_id, body=perm, fields="id").execute()
        print(json.dumps({"permission_id": r["id"], "shared": True}))
    except Exception as e:
        err(e)


# ── SHEETS ──────────────────────────────────────────────

def sheets_read(args):
    try:
        sheets = svc("sheets", "v4")
        r = sheets.spreadsheets().values().get(
            spreadsheetId=args.spreadsheet_id, range=args.range
        ).execute()
        print(json.dumps({"range": r.get("range"), "values": r.get("values", [])}, indent=2))
    except Exception as e:
        err(e)


def sheets_write(args):
    try:
        sheets = svc("sheets", "v4")
        values = json.loads(args.values)
        body = {"values": values}
        r = sheets.spreadsheets().values().update(
            spreadsheetId=args.spreadsheet_id, range=args.range,
            valueInputOption="USER_ENTERED", body=body
        ).execute()
        print(json.dumps({"updated_cells": r.get("updatedCells"), "range": r.get("updatedRange")}))
    except Exception as e:
        err(e)


def sheets_append(args):
    try:
        sheets = svc("sheets", "v4")
        row = json.loads(args.values)
        if not isinstance(row[0], list):
            row = [row]
        body = {"values": row}
        r = sheets.spreadsheets().values().append(
            spreadsheetId=args.spreadsheet_id, range=args.range,
            valueInputOption="USER_ENTERED", insertDataOption="INSERT_ROWS", body=body
        ).execute()
        upd = r.get("updates", {})
        print(json.dumps({"appended_rows": upd.get("updatedRows"), "range": upd.get("updatedRange")}))
    except Exception as e:
        err(e)


# ── CLI ─────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(description="Google Workspace CLI")
    sub = p.add_subparsers(dest="cmd")

    # gmail
    gi = sub.add_parser("gmail-inbox")
    gi.add_argument("--limit", type=int, default=10)

    gs = sub.add_parser("gmail-search")
    gs.add_argument("--query", required=True)
    gs.add_argument("--limit", type=int, default=20)

    gse = sub.add_parser("gmail-send")
    gse.add_argument("--to", required=True)
    gse.add_argument("--subject", required=True)
    gse.add_argument("--body", required=True)
    gse.add_argument("--attachment")

    gl = sub.add_parser("gmail-label")
    gl.add_argument("--message-id", required=True, dest="message_id")
    gl.add_argument("--label", required=True)

    gd = sub.add_parser("gmail-draft")
    gd.add_argument("--to", required=True)
    gd.add_argument("--subject", required=True)
    gd.add_argument("--body", required=True)

    # calendar
    cl = sub.add_parser("cal-list")
    cl.add_argument("--days", type=int, default=7)
    cl.add_argument("--limit", type=int, default=10)

    cc = sub.add_parser("cal-create")
    cc.add_argument("--title", required=True)
    cc.add_argument("--start", required=True)
    cc.add_argument("--end")
    cc.add_argument("--timezone")
    cc.add_argument("--description")
    cc.add_argument("--all-day", dest="all_day", action="store_true")

    cu = sub.add_parser("cal-update")
    cu.add_argument("--event-id", required=True, dest="event_id")
    cu.add_argument("--title"); cu.add_argument("--start"); cu.add_argument("--end")

    cdel = sub.add_parser("cal-delete")
    cdel.add_argument("--event-id", required=True, dest="event_id")

    # drive
    drl = sub.add_parser("drive-list")
    drl.add_argument("--query"); drl.add_argument("--limit", type=int, default=20)

    dru = sub.add_parser("drive-upload")
    dru.add_argument("--file", required=True)
    dru.add_argument("--folder-id", dest="folder_id")

    drd = sub.add_parser("drive-download")
    drd.add_argument("--file-id", required=True, dest="file_id")
    drd.add_argument("--output")

    drs = sub.add_parser("drive-share")
    drs.add_argument("--file-id", required=True, dest="file_id")
    drs.add_argument("--email"); drs.add_argument("--role", default="reader")
    drs.add_argument("--anyone-link", dest="anyone_link", action="store_true")

    # sheets
    shr = sub.add_parser("sheets-read")
    shr.add_argument("--spreadsheet-id", required=True, dest="spreadsheet_id")
    shr.add_argument("--range", required=True)

    shw = sub.add_parser("sheets-write")
    shw.add_argument("--spreadsheet-id", required=True, dest="spreadsheet_id")
    shw.add_argument("--range", required=True)
    shw.add_argument("--values", required=True)

    sha = sub.add_parser("sheets-append")
    sha.add_argument("--spreadsheet-id", required=True, dest="spreadsheet_id")
    sha.add_argument("--range", required=True)
    sha.add_argument("--values", required=True)

    args = p.parse_args()
    dispatch = {
        "gmail-inbox": gmail_inbox, "gmail-search": gmail_search,
        "gmail-send": gmail_send, "gmail-label": gmail_label, "gmail-draft": gmail_draft,
        "cal-list": cal_list, "cal-create": cal_create, "cal-update": cal_update, "cal-delete": cal_delete,
        "drive-list": drive_list, "drive-upload": drive_upload,
        "drive-download": drive_download, "drive-share": drive_share,
        "sheets-read": sheets_read, "sheets-write": sheets_write, "sheets-append": sheets_append,
    }
    if args.cmd in dispatch:
        dispatch[args.cmd](args)
    else:
        p.print_help()


if __name__ == "__main__":
    main()
