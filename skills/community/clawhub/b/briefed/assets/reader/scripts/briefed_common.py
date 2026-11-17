"""
briefed_common.py — shared Gmail auth and private file helpers for Briefed scripts.

Everything Briefed writes (OAuth token, inbox metadata, email bodies) is
written owner-only (0600) via an atomic replace, so other local users can't
read it and a pre-planted symlink at the target path is replaced, not followed.
"""
import json, os, tempfile

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

TOKEN_FILE = os.environ.get('BRIEFED_GMAIL_TOKEN_FILE', os.path.expanduser('~/.openclaw/workspace/briefed-gmail-token.json'))
CLIENT_SECRET_FILE = os.environ.get('BRIEFED_GMAIL_CLIENT_SECRET', os.path.expanduser('~/client_secret.json'))
# Read-only: Briefed never sends, deletes, or modifies mail.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def write_private(path, text):
    """Atomically write text to path with 0600 permissions."""
    directory = os.path.dirname(os.path.abspath(path))
    os.makedirs(directory, mode=0o700, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=directory, prefix='.briefed-', suffix='.tmp')  # created 0600
    try:
        with os.fdopen(fd, 'w') as f:
            f.write(text)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def write_private_json(path, data):
    write_private(path, json.dumps(data, indent=2))


def append_private(path, text):
    """Append text to path, creating it 0600 if missing."""
    os.makedirs(os.path.dirname(os.path.abspath(path)), mode=0o700, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT | getattr(os, 'O_NOFOLLOW', 0), 0o600)
    with os.fdopen(fd, 'a') as f:
        f.write(text)


def get_gmail_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        os.chmod(TOKEN_FILE, 0o600)  # tighten tokens written by older versions
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CLIENT_SECRET_FILE):
                raise RuntimeError(
                    f"Missing OAuth client file: {CLIENT_SECRET_FILE}\n"
                    "Set BRIEFED_GMAIL_CLIENT_SECRET to your Google OAuth client JSON."
                )
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0, open_browser=True)

        write_private(TOKEN_FILE, creds.to_json())

    return build('gmail', 'v1', credentials=creds, cache_discovery=False)
