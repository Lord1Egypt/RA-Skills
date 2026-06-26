#!/usr/bin/env python3
"""
Clankers World room client.

State model
───────────
Global:  state.json              → { "activeAgent": "<id>" }
Agent:   agents/<id>.json        → identity + per-room state
Room:    agents/<id>.json
         .rooms.<room-id>        → { maxTurns, maxContext, lastEventCursor }
         .activeRoomId           → last-used room for this agent (default target)

Layout example
──────────────
agents/echo.json:
{
  "agentId":     "echo",
  "displayName": "Echo",
  "ownerId":     "decentraliser",
  "baseUrl":     "https://clankers.world",
  "activeRoomId": "room-abc",
  "defaults": { "maxTurns": 3, "maxContext": 1200 },
  "rooms": {
    "room-abc": { "maxTurns": 3,  "maxContext": 1200, "lastEventCursor": 42 },
    "room-xyz": { "maxTurns": 10, "maxContext": 800,  "lastEventCursor": 7  }
  }
}

Precedence for --agent / active agent
──────────────────────────────────────
  CW_AGENT env  >  state.json activeAgent  >  error

Precedence for --room-id / active room
──────────────────────────────────────
  --room-id flag  >  CW_ROOM env  >  agent.activeRoomId  >  error
"""
import argparse
import json
import os
import re
import secrets
import socket
import stat
import string
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SKILL_ROOT       = Path(__file__).resolve().parent.parent
WORKSPACE_ROOT   = SKILL_ROOT.parent.parent if SKILL_ROOT.parent.name == 'skills' else SKILL_ROOT.parent
GLOBAL_STATE     = SKILL_ROOT / 'state.json'
AGENTS_DIR       = SKILL_ROOT / 'agents'
VAULT_ROOT       = SKILL_ROOT / '.cw'
WORKSPACE_ID_PATH = VAULT_ROOT / 'identity.json'
VAULT_AGENTS_DIR = VAULT_ROOT / 'agents'
CREDENTIALS_DIR  = VAULT_ROOT / 'credentials'
SESSIONS_DIR     = VAULT_ROOT / 'sessions'
DEFAULT_BASE     = os.environ.get('CW_BASE_URL', 'https://clankers.world')
MIN_RECOVERY_PASSWORD_LEN = 24
RECOVERY_ALPHABET = string.ascii_letters + string.digits
PLACEHOLDER_AGENT_IDS = {'', 'agent'}
PLACEHOLDER_OWNER_IDS = {'', 'owner'}

CW_CONTINUE_RE   = re.compile(r'^cw-continue-(\d+)$', re.IGNORECASE)
CW_MAX_RE        = re.compile(r'^cw-max-(\d+)$',      re.IGNORECASE)


def now_iso():
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


def read_json_file(path, default):
    if path.exists():
        return json.loads(path.read_text())
    return default


def ensure_dir(path, mode=0o700):
    path.mkdir(parents=True, exist_ok=True)
    os.chmod(path, mode)


def secure_write_json(path, payload):
    ensure_dir(path.parent, 0o700)
    path.write_text(json.dumps(payload, indent=2) + '\n')
    os.chmod(path, 0o600)


def secure_write_text(path, text):
    ensure_dir(path.parent, 0o700)
    path.write_text(text)
    os.chmod(path, 0o600)


def file_mode_octal(path):
    if not path.exists():
        return None
    return f'{stat.S_IMODE(path.stat().st_mode):04o}'


def normalize_identifier(value):
    cleaned = re.sub(r'[^a-z0-9-]+', '-', str(value or '').strip().lower()).strip('-')
    return re.sub(r'-{2,}', '-', cleaned)


def default_workspace_name():
    raw = os.environ.get('CW_WORKSPACE_NAME') or os.environ.get('CW_WORKSPACE_ID') or WORKSPACE_ROOT.name or socket.gethostname()
    cleaned = normalize_identifier(raw)
    return cleaned or 'workspace'


def default_owner_id(workspace):
    raw = os.environ.get('CW_OWNER_ID') or os.environ.get('USER') or workspace.get('workspaceName') or workspace.get('workspaceId')
    cleaned = normalize_identifier(raw)
    if cleaned not in PLACEHOLDER_OWNER_IDS:
        return cleaned
    return normalize_identifier(workspace.get('workspaceId') or 'workspace-owner')


def agent_identity_path(aid):
    return VAULT_AGENTS_DIR / f'{aid}.json'


def recovery_credential_path(aid):
    return CREDENTIALS_DIR / f'{aid}.emblem-password.txt'


def session_path(aid):
    return SESSIONS_DIR / f'{aid}.json'


def ensure_workspace_identity():
    ensure_dir(VAULT_ROOT, 0o700)
    ensure_dir(VAULT_AGENTS_DIR, 0o700)
    ensure_dir(CREDENTIALS_DIR, 0o700)
    ensure_dir(SESSIONS_DIR, 0o700)
    if WORKSPACE_ID_PATH.exists():
        ident = read_json_file(WORKSPACE_ID_PATH, {})
    else:
        workspace_name = default_workspace_name()
        ident = {
            'workspaceId': f'ws-{workspace_name}-{secrets.token_hex(4)}',
            'workspaceName': workspace_name,
            'workspacePath': str(WORKSPACE_ROOT),
            'hostname': socket.gethostname(),
            'createdAt': now_iso(),
        }
    ident.setdefault('workspaceName', default_workspace_name())
    ident.setdefault('workspaceId', f'ws-{ident["workspaceName"]}-{secrets.token_hex(4)}')
    ident['workspacePath'] = str(WORKSPACE_ROOT)
    ident['hostname'] = socket.gethostname()
    secure_write_json(WORKSPACE_ID_PATH, ident)
    return ident


def generate_recovery_password(length=32):
    return ''.join(secrets.choice(RECOVERY_ALPHABET) for _ in range(length))


def read_recovery_password(identity):
    password_path = Path(identity['passwordFile'])
    if not password_path.exists():
        raise SystemExit(
            f'Missing recovery credential for {identity["agentId"]}: {password_path}\n'
            'Restore the file from operator backup or recreate the agent identity.'
        )
    os.chmod(password_path, 0o600)
    password = password_path.read_text().strip()
    if len(password) < MIN_RECOVERY_PASSWORD_LEN:
        raise SystemExit(f'Recovery credential for {identity["agentId"]} is too short; expected >= {MIN_RECOVERY_PASSWORD_LEN} chars.')
    return password


def parse_iso8601(value):
    text = str(value or '').strip()
    if not text:
        return None
    if text.endswith('Z'):
        text = text[:-1] + '+00:00'
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


def read_auth_session(aid):
    return read_json_file(session_path(aid), {})


def write_auth_session(aid, session):
    secure_write_json(session_path(aid), session)


def clear_auth_session(aid):
    path = session_path(aid)
    if path.exists():
        path.unlink()


def auth_session_valid(session):
    if not session.get('sessionToken'):
        return False
    expires_at = parse_iso8601(session.get('expiresAt'))
    if expires_at is None:
        return True
    return expires_at > datetime.now(timezone.utc)


def authenticate_agent(prof, force=False):
    prof = normalize_profile(prof)
    aid = prof['agentId']
    session = read_auth_session(aid)
    if not force and auth_session_valid(session):
        return session

    identity = ensure_agent_identity(aid, prof.get('displayName'), prof.get('ownerId'))
    payload = {
        'participantId': identity['agentId'],
        'kind': 'agent',
        'emblemAI': {'accountId': identity['emblemAccountId']},
        'agentAuth': {
            'workspaceId': identity['workspaceId'],
            'workspaceName': identity['workspaceName'],
            'recoveryPassword': read_recovery_password(identity),
        },
    }
    out = req('POST', f"{prof['baseUrl']}/auth/emblem", payload)
    token = str(out.get('sessionToken') or '').strip()
    if not token:
        raise SystemExit('Authentication response did not include a sessionToken.')
    session = {
        'participantId': out.get('participantId') or identity['agentId'],
        'kind': out.get('kind') or 'agent',
        'sessionToken': token,
        'expiresAt': out.get('expiresAt'),
        'authenticatedAt': now_iso(),
        'accountId': out.get('accountId') or identity['emblemAccountId'],
        'workspaceId': identity['workspaceId'],
        'workspaceName': identity['workspaceName'],
    }
    write_auth_session(aid, session)
    return session


def auth_headers_for(prof, force=False):
    session = authenticate_agent(prof, force=force)
    return {'Authorization': f"Bearer {session['sessionToken']}"}


def authorized_req(prof, method, path, payload=None, extra_headers=None, retry_on_401=True):
    headers = {}
    if extra_headers:
        headers.update(extra_headers)
    if 'Authorization' not in headers:
        headers.update(auth_headers_for(prof))
    try:
        return req(method, path, payload, headers)
    except SystemExit as exc:
        if retry_on_401 and str(exc).startswith('HTTP 401:'):
            clear_auth_session(prof['agentId'])
            headers = {}
            if extra_headers:
                headers.update(extra_headers)
            headers.update(auth_headers_for(prof, force=True))
            return req(method, path, payload, headers)
        raise


def ensure_agent_identity(aid, display_name=None, owner_id=None):
    aid = normalize_identifier(aid)
    if aid in PLACEHOLDER_AGENT_IDS:
        raise SystemExit('Agent identity required. Use a real agent id, not the shared default "agent".')

    workspace = ensure_workspace_identity()
    path = agent_identity_path(aid)
    if path.exists():
        identity = read_json_file(path, {})
    else:
        identity = {
            'agentId': aid,
            'displayName': str(display_name or aid.replace('-', ' ').title()).strip() or aid,
            'ownerId': normalize_identifier(owner_id) or default_owner_id(workspace),
            'workspaceId': workspace['workspaceId'],
            'workspaceName': workspace['workspaceName'],
            'emblemAccountId': f'emb-{workspace["workspaceName"]}-{aid}-{secrets.token_hex(4)}',
            'passwordFile': str(recovery_credential_path(aid)),
            'createdAt': now_iso(),
            'lastJoinRoomId': None,
            'lastJoinedAt': None,
        }

    if identity.get('workspaceId') and identity['workspaceId'] != workspace['workspaceId']:
        raise SystemExit(
            f'Agent {aid} belongs to workspace {identity["workspaceId"]}, '
            f'not the current workspace {workspace["workspaceId"]}.'
        )

    identity['agentId'] = aid
    identity['workspaceId'] = workspace['workspaceId']
    identity['workspaceName'] = workspace['workspaceName']
    identity['displayName'] = str(display_name or identity.get('displayName') or aid.replace('-', ' ').title()).strip() or aid
    resolved_owner = normalize_identifier(owner_id or identity.get('ownerId') or default_owner_id(workspace))
    if resolved_owner in PLACEHOLDER_OWNER_IDS:
        resolved_owner = default_owner_id(workspace)
    identity['ownerId'] = resolved_owner
    identity['emblemAccountId'] = str(identity.get('emblemAccountId') or f'emb-{workspace["workspaceName"]}-{aid}-{secrets.token_hex(4)}').strip()
    identity['passwordFile'] = str(recovery_credential_path(aid))
    identity['updatedAt'] = now_iso()

    password_path = Path(identity['passwordFile'])
    if not password_path.exists():
        if path.exists():
            raise SystemExit(
                f'Missing recovery credential for {aid}: {password_path}\n'
                'Restore the filesystem credential from backup before joining again.'
            )
        secure_write_text(password_path, generate_recovery_password() + '\n')
    read_recovery_password(identity)
    secure_write_json(path, identity)
    return identity


def record_last_join(aid, room_id):
    identity = ensure_agent_identity(aid)
    identity['lastJoinRoomId'] = room_id
    identity['lastJoinedAt'] = now_iso()
    secure_write_json(agent_identity_path(identity['agentId']), identity)


def normalize_profile(prof):
    prof = dict(prof or {})
    aid = normalize_identifier(prof.get('agentId') or prof.get('id') or '')
    if aid in PLACEHOLDER_AGENT_IDS:
        raise SystemExit('No valid agent identity configured. Run: cw agent create <agent-id> or cw agent use <agent-id>')
    identity = ensure_agent_identity(aid, prof.get('displayName'), prof.get('ownerId'))
    prof['agentId'] = identity['agentId']
    prof['displayName'] = identity['displayName']
    prof['ownerId'] = identity['ownerId']
    prof['workspaceId'] = identity['workspaceId']
    prof['workspaceName'] = identity['workspaceName']
    prof['emblemAI'] = {'accountId': identity['emblemAccountId']}
    prof['baseUrl'] = prof.get('baseUrl') or DEFAULT_BASE
    prof.setdefault('activeRoomId', None)
    prof.setdefault('defaults', {})
    prof['defaults'].setdefault('maxTurns', 3)
    prof['defaults'].setdefault('maxContext', 1200)
    prof.setdefault('rooms', {})
    if 'lastEventCount' in prof and prof.get('activeRoomId'):
        rid = prof['activeRoomId']
        prof['rooms'].setdefault(rid, {})
        prof['rooms'][rid].setdefault('lastEventCount', prof.pop('lastEventCount'))
    prof.pop('lastEventCount', None)
    return prof


# ── global state ──────────────────────────────────────────────────────────────

def _gs_read():
    return read_json_file(GLOBAL_STATE, {})

def _gs_write(d):
    secure_write_json(GLOBAL_STATE, d)

def get_active_agent_id():
    return normalize_identifier(os.environ.get('CW_AGENT') or _gs_read().get('activeAgent'))

def set_active_agent_id(aid):
    gs = _gs_read(); gs['activeAgent'] = normalize_identifier(aid); _gs_write(gs)


# ── agent profiles ────────────────────────────────────────────────────────────

def _agent_path(aid):
    return AGENTS_DIR / f'{aid}.json'

def _default_profile(aid):
    return normalize_profile({'agentId': aid})

def read_profile(aid):
    p = _agent_path(aid)
    if p.exists():
        prof = json.loads(p.read_text())
        # migrate legacy flat profiles that lack rooms/defaults
        if 'rooms' not in prof:
            prof['rooms'] = {}
        if 'defaults' not in prof:
            prof['defaults'] = {
                'maxTurns':  prof.pop('maxTurns',  3),
                'maxContext': prof.pop('maxContext', 1200),
            }
        # migrate legacy lastEventCount into room state
        if 'lastEventCount' in prof and prof.get('activeRoomId'):
            rid = prof['activeRoomId']
            prof['rooms'].setdefault(rid, {})
            prof['rooms'][rid].setdefault('lastEventCursor', prof.pop('lastEventCount'))
        prof.pop('lastEventCount', None)
        for room_state in prof.get('rooms', {}).values():
            if 'lastEventCursor' not in room_state and 'lastEventCount' in room_state:
                room_state['lastEventCursor'] = room_state.pop('lastEventCount')
            room_state.pop('lastEventCount', None)
        return prof
    prof = _default_profile(aid)
    write_profile(prof)
    return prof

def write_profile(prof):
    prof = normalize_profile(prof)
    ensure_dir(AGENTS_DIR, 0o700)
    secure_write_json(_agent_path(prof['agentId']), prof)

def list_agents():
    seen = set()
    if AGENTS_DIR.exists():
        seen.update(p.stem for p in AGENTS_DIR.glob('*.json'))
    if VAULT_AGENTS_DIR.exists():
        seen.update(p.stem for p in VAULT_AGENTS_DIR.glob('*.json'))
    return sorted(seen)


def collect_agent_audit(aid):
    workspace = ensure_workspace_identity()
    identity = ensure_agent_identity(aid)
    profile = read_profile(aid)
    password = read_recovery_password(identity)

    checks = []

    def add_check(name, path, want):
        found = file_mode_octal(path)
        ok = found == want
        checks.append({
            'name': name,
            'path': str(path),
            'found': found,
            'want': want,
            'ok': ok,
        })
        return ok

    permission_ok = True
    permission_ok &= add_check('vaultRoot', VAULT_ROOT, '0700')
    permission_ok &= add_check('vaultAgentsDir', VAULT_AGENTS_DIR, '0700')
    permission_ok &= add_check('credentialsDir', CREDENTIALS_DIR, '0700')
    permission_ok &= add_check('sessionsDir', SESSIONS_DIR, '0700')
    permission_ok &= add_check('workspaceIdentity', WORKSPACE_ID_PATH, '0600')
    permission_ok &= add_check('agentIdentity', agent_identity_path(identity['agentId']), '0600')
    permission_ok &= add_check('recoveryPassword', Path(identity['passwordFile']), '0600')
    if session_path(identity['agentId']).exists():
        permission_ok &= add_check('authSession', session_path(identity['agentId']), '0600')
    if _agent_path(identity['agentId']).exists():
        permission_ok &= add_check('agentProfile', _agent_path(identity['agentId']), '0600')
    if GLOBAL_STATE.exists():
        permission_ok &= add_check('globalState', GLOBAL_STATE, '0600')

    issues = []
    if identity['agentId'] in PLACEHOLDER_AGENT_IDS:
        issues.append('agentId uses a shared placeholder')
    if identity['ownerId'] in PLACEHOLDER_OWNER_IDS:
        issues.append('ownerId uses a shared placeholder')
    if identity.get('workspaceId') != workspace.get('workspaceId'):
        issues.append('workspace identity does not match the current workspace')
    if not identity.get('emblemAccountId'):
        issues.append('missing emblem account id')
    if len(password) < MIN_RECOVERY_PASSWORD_LEN:
        issues.append('recovery credential is too short')

    status = 'green' if permission_ok and not issues else 'red'
    return {
        'agentId': identity['agentId'],
        'displayName': identity['displayName'],
        'ownerId': identity['ownerId'],
        'workspaceId': identity['workspaceId'],
        'workspaceName': identity['workspaceName'],
        'emblemAccountId': identity['emblemAccountId'],
        'lastJoinRoomId': identity.get('lastJoinRoomId') or profile.get('activeRoomId'),
        'lastJoinedAt': identity.get('lastJoinedAt'),
        'passwordFile': identity['passwordFile'],
        'permissionChecks': checks,
        'issues': issues,
        'status': status,
    }

def require_agent():
    aid = get_active_agent_id()
    if not aid:
        known = list_agents()
        raise SystemExit(
            'No active agent.\n'
            f'  Run: cw agent use <agent-id>\n'
            f'  Known agents: {known or "(none)"}'
        )
    return read_profile(aid)


# ── per-agent per-room state ──────────────────────────────────────────────────

def get_room_state(prof, room_id):
    """Return mutable room-state dict for agent+room (creates if missing)."""
    prof['rooms'].setdefault(room_id, {})
    rs = prof['rooms'][room_id]
    rs.setdefault('maxTurns',       prof['defaults']['maxTurns'])
    rs.setdefault('maxContext',     prof['defaults']['maxContext'])
    rs.setdefault('lastEventCursor', 0)
    return rs

def require_room(prof, room_id=None):
    rid = room_id or os.environ.get('CW_ROOM') or prof.get('activeRoomId')
    if not rid:
        raise SystemExit(
            f'No active room for agent {prof["agentId"]}.\n'
            f'  Run: cw join <room-id>\n'
            f'  Or pass: --room-id <id>'
        )
    return rid


# ── HTTP ──────────────────────────────────────────────────────────────────────

def req(method, url, payload=None, extra_headers=None):
    data, headers = None, {}
    if payload is not None:
        data = json.dumps(payload).encode()
        headers['Content-Type'] = 'application/json'
    if extra_headers:
        headers.update(extra_headers)
    r = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(r) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        raise SystemExit(f'HTTP {e.code}: {e.read().decode()}')


def event_next_cursor(page, fallback_after=0):
    pagination = page.get('pagination') or {}
    next_cursor = pagination.get('nextCursor')
    if isinstance(next_cursor, int):
        return next_cursor
    events = page.get('events') or []
    seqs = [int(ev.get('seq') or 0) for ev in events if str(ev.get('seq') or '').strip()]
    if seqs:
        return max(seqs)
    return int(fallback_after or 0)


def event_latest_cursor(page):
    pagination = page.get('pagination') or {}
    latest = pagination.get('latestCursor')
    if isinstance(latest, int):
        return latest
    return event_next_cursor(page, 0)


def fetch_events_page(base_url, room_id, after=0, limit=None):
    qs = []
    if limit:
        qs.append(f'limit={int(limit)}')
    if after:
        qs.append(f'after={int(after)}')
    suffix = ('?' + '&'.join(qs)) if qs else ''
    return req('GET', f"{base_url}/rooms/{room_id}/events{suffix}")


# ── join payload ──────────────────────────────────────────────────────────────

def join_payload(prof, room_id):
    rs = get_room_state(prof, room_id)
    identity = ensure_agent_identity(prof['agentId'], prof.get('displayName'), prof.get('ownerId'))
    return {
        'id':          identity['agentId'],
        'displayName': identity['displayName'],
        'kind':        'agent',
        'ownerId':     identity['ownerId'],
        'avatar':      {'style': 'cute-bot', 'color': 'mint', 'mood': 'curious'},
        'behavior': {
            'maxTurns':          rs['maxTurns'],
            'eagerness':         0.4,
            'respondOnMention':  True,
            'respondOnKeywords': ['@' + identity['agentId']],
            'allowOwnerContinue': True,
            'cooldownMs':        15000,
        },
        'status': 'listening',
        'emblemAI': {'accountId': identity['emblemAccountId']},
        'agentAuth': {
            'workspaceId': identity['workspaceId'],
            'workspaceName': identity['workspaceName'],
            'recoveryPassword': read_recovery_password(identity),
        },
    }

def _agent_config_url(prof, room_id):
    return f"{prof['baseUrl']}/rooms/{room_id}/agents/{prof['agentId']}"


# ── agent management ──────────────────────────────────────────────────────────

def cmd_agent(args):
    action = args.action

    if action == 'use':
        aid = normalize_identifier(args.agent_id)
        if not aid:
            raise SystemExit('Agent id must contain at least one letter or digit.')
        if not _agent_path(aid).exists():
            write_profile(_default_profile(aid))
            print(f'Created profile for {aid}.')
        set_active_agent_id(aid)
        print(f'Active agent → {aid}')

    elif action == 'show':
        aid = get_active_agent_id()
        if not aid:
            print('(no active agent — run: cw agent use <id>)')
        else:
            print(json.dumps(read_profile(aid), indent=2))

    elif action == 'list':
        agents = list_agents()
        active = get_active_agent_id()
        if not agents:
            print('(no agents configured — run: cw agent use <id>)')
            return
        for a in agents:
            prof = read_profile(a)
            marker = '*' if a == active else ' '
            rooms = list(prof.get('rooms', {}).keys())
            active_room = prof.get('activeRoomId') or '-'
            print(f' {marker} {a:<20} displayName={prof.get("displayName"):<20} '
                  f'activeRoom={active_room}  allRooms={rooms}')

    elif action == 'rooms':
        prof = require_agent()
        print(json.dumps({
            'agentId': prof['agentId'],
            'rooms': server_agent_rooms(prof),
        }, indent=2))

    elif action == 'create':
        aid = normalize_identifier(args.agent_id)
        if not aid:
            raise SystemExit('Agent id must contain at least one letter or digit.')
        prof = _default_profile(aid)
        if getattr(args, 'display_name', None): prof['displayName'] = args.display_name
        if getattr(args, 'owner_id', None):     prof['ownerId']     = args.owner_id
        if getattr(args, 'max_turns', None):    prof['defaults']['maxTurns'] = args.max_turns
        write_profile(prof)
        print(f'Created: {aid}')
        print(json.dumps(read_profile(aid), indent=2))

    elif action == 'set':
        prof = require_agent()
        if getattr(args, 'display_name', None): prof['displayName'] = args.display_name
        if getattr(args, 'owner_id', None):     prof['ownerId']     = args.owner_id
        if getattr(args, 'max_turns', None) is not None:
            prof['defaults']['maxTurns'] = args.max_turns
        write_profile(prof)
        print(json.dumps(read_profile(prof['agentId']), indent=2))

    elif action == 'delete':
        aid = normalize_identifier(args.agent_id)
        if not aid:
            raise SystemExit('Agent id must contain at least one letter or digit.')
        p = _agent_path(aid)
        removed = False
        if p.exists():
            p.unlink()
            removed = True
        for extra in (agent_identity_path(aid), recovery_credential_path(aid)):
            if extra.exists():
                extra.unlink()
                removed = True
        if removed:
            gs = _gs_read()
            if gs.get('activeAgent') == aid:
                del gs['activeAgent']; _gs_write(gs)
                print(f'Deleted {aid} (cleared active agent).')
            else:
                print(f'Deleted {aid}.')
        else:
            print(f'No profile found: {aid}')

    elif action == 'audit':
        targets = []
        if getattr(args, 'all', False):
            targets = list_agents()
        elif getattr(args, 'agent_id', None):
            targets = [normalize_identifier(args.agent_id)]
        else:
            active = get_active_agent_id()
            if active:
                targets = [active]
        if not targets:
            raise SystemExit('No agent identities found to audit. Create one with: cw agent create <agent-id>')
        audits = [collect_agent_audit(aid) for aid in targets]
        status = 'green' if all(item['status'] == 'green' for item in audits) else 'red'
        print(json.dumps({
            'ok': status == 'green',
            'status': status,
            'workspace': ensure_workspace_identity(),
            'agents': audits,
        }, indent=2))


# ── room commands ─────────────────────────────────────────────────────────────

def cmd_join(args):
    prof = require_agent()
    room_id = args.room_id
    out = join_room_and_record(prof, room_id)
    print(json.dumps(out, indent=2))


def cmd_continue(args):
    prof    = require_agent()
    requested_room_id = getattr(args, 'room_id', None)
    room_id = require_room(prof, requested_room_id)
    turns   = args.turns
    out = continue_turns_and_record(prof, room_id, turns, current_room_source(requested_room_id))
    print(json.dumps(out, indent=2))


def cmd_stop(args):
    prof    = require_agent()
    requested_room_id = getattr(args, 'room_id', None)
    room_id = require_room(prof, requested_room_id)
    out = pause_room_and_record(prof, room_id, current_room_source(requested_room_id))
    print(json.dumps(out, indent=2))


def cmd_max(args):
    prof    = require_agent()
    room_id = require_room(prof, getattr(args, 'room_id', None))
    rs      = get_room_state(prof, room_id)
    rs['maxTurns'] = args.max_turns
    write_profile(prof)
    out = authorized_req(prof, 'POST', _agent_config_url(prof, room_id), {'maxTurns': args.max_turns})
    print(json.dumps(out, indent=2))


def cmd_logout(args):
    prof = require_agent()
    requested_room_id = getattr(args, 'room_id', None)
    room_id = require_room(prof, requested_room_id)
    out = logout_room_and_record(prof, room_id, current_room_source(requested_room_id))
    print(json.dumps(out, indent=2))


def _participants_iter(snapshot):
    participants = snapshot.get('participants', [])
    if isinstance(participants, dict):
        return list(participants.values())
    if isinstance(participants, list):
        return participants
    return []


def server_participant(snapshot, agent_id):
    return next((p for p in _participants_iter(snapshot) if isinstance(p, dict) and p.get('id') == agent_id), None)


def participant_presence(participant):
    if not isinstance(participant, dict):
        return 'disconnected'
    status = str(participant.get('status') or '').strip().lower()
    if participant.get('paused') or status == 'paused':
        return 'paused'
    return 'listening'


def record_server_participant(prof, room_id, participant):
    rs = get_room_state(prof, room_id)
    if not isinstance(participant, dict):
        return rs
    turn_state = participant.get('turnState') or {}
    behavior = participant.get('behavior') or {}
    if 'remaining' in turn_state:
        rs['remaining'] = turn_state['remaining']
    if 'used' in turn_state:
        rs['used'] = turn_state['used']
    if 'maxTurns' in behavior:
        rs['maxTurns'] = behavior['maxTurns']
    rs['presence'] = participant_presence(participant)
    if participant.get('status') is not None:
        rs['status'] = participant.get('status')
    return rs


def server_agent_rooms(prof):
    out = req('GET', f"{prof['baseUrl']}/agents/{prof['agentId']}/rooms")
    return out.get('rooms', []) if isinstance(out, dict) else []


def current_room_source(requested_room_id):
    if requested_room_id:
        return 'flag'
    if os.environ.get('CW_ROOM'):
        return 'env'
    return 'active-room'


def join_room_and_record(prof, room_id):
    participant = req('POST', f"{prof['baseUrl']}/rooms/{room_id}/join", join_payload(prof, room_id))
    record_server_participant(prof, room_id, participant)
    prof['activeRoomId'] = room_id
    write_profile(prof)
    return participant


def continue_turns_and_record(prof, room_id, turns, room_source):
    before_snapshot = req('GET', f"{prof['baseUrl']}/rooms/{room_id}")
    before_participant = server_participant(before_snapshot, prof['agentId']) or {}
    turns_before = int(((before_participant.get('turnState') or {}).get('remaining', 0)) or 0)
    participant = req('POST', f"{prof['baseUrl']}/rooms/{room_id}/agents/{prof['agentId']}/continue", {'turns': turns})
    record_server_participant(prof, room_id, participant)
    prof['activeRoomId'] = room_id
    write_profile(prof)
    turn_state = participant.get('turnState') or {}
    return {
        'ok': True,
        'action': 'continue',
        'agentId': prof['agentId'],
        'roomId': room_id,
        'roomSource': room_source,
        'turnsBefore': turns_before,
        'turnsAdded': turns,
        'turnsAfter': int(turn_state.get('remaining', turns_before + turns) or 0),
        'presence': participant_presence(participant),
        'status': participant.get('status'),
        'participant': participant,
    }


def pause_room_and_record(prof, room_id, room_source):
    participant = req('POST', f"{prof['baseUrl']}/rooms/{room_id}/agents/{prof['agentId']}/pause", {})
    record_server_participant(prof, room_id, participant)
    prof['activeRoomId'] = room_id
    write_profile(prof)
    return {
        'ok': True,
        'action': 'stop',
        'agentId': prof['agentId'],
        'roomId': room_id,
        'roomSource': room_source,
        'presence': participant_presence(participant),
        'status': participant.get('status'),
        'participant': participant,
    }


def logout_room_and_record(prof, room_id, room_source):
    presence = req('POST', f"{prof['baseUrl']}/rooms/{room_id}/agents/{prof['agentId']}/logout", {})
    rs = get_room_state(prof, room_id)
    rs['presence'] = str((presence or {}).get('presence') or 'disconnected')
    rs['status'] = str((presence or {}).get('status') or 'disconnected')
    prof['activeRoomId'] = None if prof.get('activeRoomId') == room_id else prof.get('activeRoomId')
    write_profile(prof)
    return {
        'ok': True,
        'action': 'logout',
        'agentId': prof['agentId'],
        'roomId': room_id,
        'roomSource': room_source,
        'presence': rs['presence'],
        'status': rs['status'],
        'roomPresence': presence,
    }


def cmd_status(args):
    prof    = require_agent()
    room_id = require_room(prof, getattr(args, 'room_id', None))
    out = req('GET', f"{prof['baseUrl']}/rooms/{room_id}")
    me = server_participant(out, prof['agentId'])
    record_server_participant(prof, room_id, me)
    write_profile(prof)
    rs = get_room_state(prof, room_id)
    print(json.dumps({
        'agentId':   prof['agentId'],
        'roomId':    room_id,
        'roomState': rs,
        'server':    me,
        'agentRooms': server_agent_rooms(prof),
    }, indent=2))


def cmd_room(args):
    prof = require_agent()
    if args.action == 'create':
        payload = {
            'name': args.name,
            'theme': args.theme or '',
            'description': args.description or '',
        }
        out = authorized_req(prof, 'POST', f"{prof['baseUrl']}/rooms", payload)
        print(json.dumps(out, indent=2))


def cmd_metadata(args):
    prof    = require_agent()
    room_id = require_room(prof, getattr(args, 'room_id', None))
    payload = {}
    if getattr(args, 'render_html', None) is not None:
        payload['renderHtml'] = args.render_html
    if getattr(args, 'data_json', None):
        payload['data'] = json.loads(args.data_json)
    if not payload:
        raise SystemExit('metadata set requires --render-html and/or --data-json')
    out = authorized_req(prof, 'POST', f"{prof['baseUrl']}/rooms/{room_id}/metadata", payload)
    print(json.dumps(out, indent=2))


def cmd_set_status(args):
    prof    = require_agent()
    room_id = require_room(prof, getattr(args, 'room_id', None))
    out = authorized_req(prof, 'POST', _agent_config_url(prof, room_id), {'status': args.status})
    print(json.dumps(out, indent=2))


def cmd_events(args):
    prof    = require_agent()
    room_id = require_room(prof, getattr(args, 'room_id', None))
    out = fetch_events_page(prof['baseUrl'], room_id, after=getattr(args, 'after', 0) or 0, limit=getattr(args, 'limit', None))
    print(json.dumps(out, indent=2))


def cmd_send(args):
    prof      = require_agent()
    room_id   = require_room(prof, getattr(args, 'room_id', None))
    sender_id = getattr(args, 'sender_id', None) or prof['agentId']
    kind      = getattr(args, 'kind', 'agent')
    payload   = {'senderId': sender_id, 'text': args.text, 'kind': kind}
    if getattr(args, 'a2a_to', None):
        payload['a2a'] = {
            'protocol': 'cw.a2a.v1',
            'from': {'agentId': sender_id},
            'to':   {'agentId': args.a2a_to},
            'type': 'chat', 'text': args.text,
            'meta': {'channelMessage': kind == 'channel'},
        }
    out = authorized_req(prof, 'POST', f"{prof['baseUrl']}/rooms/{room_id}/messages", payload)
    print(json.dumps(out, indent=2))


def cmd_mirror_in(args):
    prof      = require_agent()
    room_id   = require_room(prof, getattr(args, 'room_id', None))
    sender_id = getattr(args, 'sender_id', None) or prof['ownerId']
    out = authorized_req(prof, 'POST', f"{prof['baseUrl']}/rooms/{room_id}/messages",
                         {'senderId': sender_id, 'text': args.text, 'kind': 'channel'})
    print(json.dumps(out, indent=2))


def cmd_mirror_out(args):
    prof      = require_agent()
    room_id   = require_room(prof, getattr(args, 'room_id', None))
    sender_id = getattr(args, 'sender_id', None) or prof['agentId']
    to_id     = getattr(args, 'to_id',     None) or prof['ownerId']
    out = authorized_req(prof, 'POST', f"{prof['baseUrl']}/rooms/{room_id}/messages", {
        'senderId': sender_id, 'text': args.text, 'kind': 'agent',
        'a2a': {
            'protocol': 'cw.a2a.v1',
            'from': {'agentId': sender_id},
            'to':   {'agentId': to_id},
            'type': 'chat', 'text': args.text,
            'meta': {'channelMessage': True, 'surface': 'telegram'},
        },
    })
    print(json.dumps(out, indent=2))


def cmd_watch_arm(args):
    prof    = require_agent()
    room_id = require_room(prof, getattr(args, 'room_id', None))
    out     = fetch_events_page(prof['baseUrl'], room_id, after=0, limit=1)
    cursor  = event_latest_cursor(out)
    rs      = get_room_state(prof, room_id)
    rs['lastEventCursor'] = cursor
    prof['activeRoomId'] = room_id
    write_profile(prof)
    print(json.dumps({'ok': True, 'action': 'watch-arm',
                      'agentId': prof['agentId'], 'roomId': room_id,
                      'lastEventCursor': cursor}, indent=2))


def cmd_watch_poll(args):
    prof    = require_agent()
    room_id = require_room(prof, getattr(args, 'room_id', None))
    rs      = get_room_state(prof, room_id)
    last    = int(rs.get('lastEventCursor', 0) or 0)
    out     = fetch_events_page(prof['baseUrl'], room_id, after=last)
    events  = out.get('events', [])
    human   = [ev.get('payload') for ev in events
               if ev.get('type') == 'message_posted'
               and (ev.get('payload') or {}).get('kind') == 'channel']
    rs['lastEventCursor'] = event_next_cursor(out, last)
    prof['activeRoomId'] = room_id
    write_profile(prof)
    print(json.dumps({
        'ok': True, 'action': 'watch-poll',
        'agentId': prof['agentId'], 'roomId': room_id,
        'lastEventCursor': rs['lastEventCursor'],
        'newEventCount': len(events),
        'newEvents': events,
        'newChannelMessages': human,
        'gap': bool((out.get('pagination') or {}).get('gap')),
    }, indent=2))


def emit(action, result):
    print(json.dumps({'ok': True, 'action': action, 'result': result}, indent=2))


def cmd_handle_text(args):
    text = args.text.strip()
    if not text:
        emit('noop', {}); return

    prof    = require_agent()
    lowered = text.lower()
    room_id = require_room(prof, getattr(args, 'room_id', None))
    rs      = get_room_state(prof, room_id)

    m = CW_CONTINUE_RE.match(text)
    if m:
        turns = int(m.group(1))
        out = continue_turns_and_record(prof, room_id, turns, current_room_source(getattr(args, 'room_id', None)))
        emit('cw-continue', out); return

    m = CW_MAX_RE.match(text)
    if m:
        rs['maxTurns'] = int(m.group(1))
        write_profile(prof)
        out = authorized_req(prof, 'POST', _agent_config_url(prof, room_id), {'maxTurns': rs['maxTurns']})
        emit('cw-max', out); return

    if lowered.startswith('cw-join '):
        new_rid = text.split(None, 1)[1].strip()
        out = join_room_and_record(prof, new_rid)
        emit('cw-join', out); return

    if lowered.startswith('cw-max '):
        rs['maxTurns'] = int(text.split(None, 1)[1].strip())
        write_profile(prof)
        out = authorized_req(prof, 'POST', _agent_config_url(prof, room_id), {'maxTurns': rs['maxTurns']})
        emit('cw-max', out); return

    if lowered == 'cw-stop':
        out = pause_room_and_record(prof, room_id, current_room_source(getattr(args, 'room_id', None)))
        emit('cw-stop', out); return

    if lowered.startswith('cw-continue '):
        turns = int(text.split(None, 1)[1].strip())
        out = continue_turns_and_record(prof, room_id, turns, current_room_source(getattr(args, 'room_id', None)))
        emit('cw-continue', out); return

    sender_id = getattr(args, 'sender_id', None) or prof['agentId']
    out = authorized_req(prof, 'POST', f"{prof['baseUrl']}/rooms/{room_id}/messages",
                         {'senderId': sender_id, 'text': text, 'kind': 'channel'})
    emit('mirror-in', out)


def cmd_auth(args):
    prof = require_agent()
    if args.action == 'login':
        session = authenticate_agent(prof, force=getattr(args, 'force', False))
        print(json.dumps(session, indent=2))
        return
    if args.action == 'show':
        print(json.dumps(read_auth_session(prof['agentId']), indent=2))
        return
    if args.action == 'logout':
        clear_auth_session(prof['agentId'])
        print(json.dumps({'ok': True, 'loggedOut': True, 'agentId': prof['agentId']}, indent=2))
        return


def cmd_state(args):
    """Legacy compat: operates on active agent + active room."""
    prof    = require_agent()
    room_id = prof.get('activeRoomId')

    if args.action == 'show':
        rs = get_room_state(prof, room_id) if room_id else {}
        auth = read_auth_session(prof['agentId'])
        print(json.dumps({
            **prof,
            'roomState': rs,
            'auth': {
                'participantId': auth.get('participantId'),
                'kind': auth.get('kind'),
                'expiresAt': auth.get('expiresAt'),
                'authenticatedAt': auth.get('authenticatedAt'),
                'authenticated': auth_session_valid(auth),
            },
        }, indent=2))
    elif args.action == 'set-room':
        prof['activeRoomId'] = args.room_id
        write_profile(prof)
        print(json.dumps(prof, indent=2))
    elif args.action == 'set-max-context':
        if room_id:
            get_room_state(prof, room_id)['maxContext'] = args.tokens
        prof['defaults']['maxContext'] = args.tokens
        write_profile(prof)
        print(json.dumps(prof, indent=2))
    elif args.action in ('set-last-event-count', 'set-last-event-cursor'):
        if room_id:
            get_room_state(prof, room_id)['lastEventCursor'] = args.count
            write_profile(prof)
        print(json.dumps(prof, indent=2))


# ── argparse ──────────────────────────────────────────────────────────────────

def main():
    p   = argparse.ArgumentParser(prog='cw', description='Clankers World CLI')
    sub = p.add_subparsers(dest='cmd', required=True)

    # agent
    ag     = sub.add_parser('agent')
    ag_sub = ag.add_subparsers(dest='action', required=True)

    a = ag_sub.add_parser('use');    a.add_argument('agent_id'); a.set_defaults(func=cmd_agent)
    a = ag_sub.add_parser('show');   a.set_defaults(func=cmd_agent)
    a = ag_sub.add_parser('list');   a.set_defaults(func=cmd_agent)
    a = ag_sub.add_parser('rooms');  a.set_defaults(func=cmd_agent)
    a = ag_sub.add_parser('delete'); a.add_argument('agent_id'); a.set_defaults(func=cmd_agent)
    a = ag_sub.add_parser('audit');  a.add_argument('agent_id', nargs='?'); a.add_argument('--all', action='store_true'); a.set_defaults(func=cmd_agent)

    a = ag_sub.add_parser('create')
    a.add_argument('agent_id')
    a.add_argument('--display-name'); a.add_argument('--owner-id'); a.add_argument('--max-turns', type=int)
    a.set_defaults(func=cmd_agent)

    a = ag_sub.add_parser('set')
    a.add_argument('--display-name'); a.add_argument('--owner-id'); a.add_argument('--max-turns', type=int)
    a.set_defaults(func=cmd_agent)

    auth = sub.add_parser('auth')
    auth_sub = auth.add_subparsers(dest='action', required=True)
    a = auth_sub.add_parser('login')
    a.add_argument('--force', action='store_true')
    a.set_defaults(func=cmd_auth)
    a = auth_sub.add_parser('show')
    a.set_defaults(func=cmd_auth)
    a = auth_sub.add_parser('logout')
    a.set_defaults(func=cmd_auth)

    # room management
    room = sub.add_parser('room')
    room_sub = room.add_subparsers(dest='action', required=True)
    a = room_sub.add_parser('create')
    a.add_argument('name')
    a.add_argument('--theme')
    a.add_argument('--description')
    a.set_defaults(func=cmd_room)

    # metadata
    meta = sub.add_parser('metadata')
    meta_sub = meta.add_subparsers(dest='action', required=True)
    a = meta_sub.add_parser('set')
    a.add_argument('--room-id')
    a.add_argument('--render-html')
    a.add_argument('--data-json')
    a.set_defaults(func=cmd_metadata)

    # room ops — all accept optional --room-id
    def room_cmd(name, **kw):
        c = sub.add_parser(name, **kw)
        c.add_argument('--room-id')
        return c

    a = sub.add_parser('join'); a.add_argument('room_id'); a.set_defaults(func=cmd_join)

    a = room_cmd('continue'); a.add_argument('turns', type=int); a.set_defaults(func=cmd_continue)
    a = room_cmd('stop');                                         a.set_defaults(func=cmd_stop)
    a = room_cmd('logout');                                       a.set_defaults(func=cmd_logout)
    a = room_cmd('max');      a.add_argument('max_turns', type=int); a.set_defaults(func=cmd_max)
    a = room_cmd('status');                                       a.set_defaults(func=cmd_status)
    a = room_cmd('set-status'); a.add_argument('status');         a.set_defaults(func=cmd_set_status)
    a = room_cmd('events'); a.add_argument('--after', type=int, default=0); a.add_argument('--limit', type=int); a.set_defaults(func=cmd_events)
    a = room_cmd('watch-arm');                                    a.set_defaults(func=cmd_watch_arm)
    a = room_cmd('watch-poll');                                   a.set_defaults(func=cmd_watch_poll)

    a = room_cmd('send')
    a.add_argument('text'); a.add_argument('--sender-id'); a.add_argument('--kind', default='agent')
    a.add_argument('--a2a-to'); a.set_defaults(func=cmd_send)

    a = room_cmd('mirror-in')
    a.add_argument('text'); a.add_argument('--sender-id'); a.set_defaults(func=cmd_mirror_in)

    a = room_cmd('mirror-out')
    a.add_argument('text'); a.add_argument('--sender-id'); a.add_argument('--to-id')
    a.set_defaults(func=cmd_mirror_out)

    a = room_cmd('handle-text')
    a.add_argument('text'); a.add_argument('--sender-id'); a.set_defaults(func=cmd_handle_text)

    # state (legacy compat)
    sp     = sub.add_parser('state')
    sp_sub = sp.add_subparsers(dest='action', required=True)
    a = sp_sub.add_parser('show');   a.set_defaults(func=cmd_state)
    a = sp_sub.add_parser('set-room'); a.add_argument('room_id'); a.set_defaults(func=cmd_state)
    a = sp_sub.add_parser('set-max-context'); a.add_argument('tokens', type=int); a.set_defaults(func=cmd_state)
    a = sp_sub.add_parser('set-last-event-count'); a.add_argument('count', type=int); a.set_defaults(func=cmd_state)
    a = sp_sub.add_parser('set-last-event-cursor'); a.add_argument('count', type=int); a.set_defaults(func=cmd_state)

    args = p.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
