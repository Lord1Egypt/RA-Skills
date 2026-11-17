#!/usr/bin/env python3
"""ClawReef discovery, protected enrollment and standing host permissions."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid

ROOT = Path(__file__).resolve().parent.parent
# Resolve bundled modules before CWD/PYTHONPATH; keep read-only commands write-free.
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / 'lib'))
CONTRACT = json.loads((ROOT / 'lib/clawreef-contract.json').read_text())

class Failure(Exception):
    def __init__(self, code, message, exit_code=2, data=None, next_action=None, retryable=False):
        self.code, self.message, self.exit_code = code, message, exit_code
        self.data, self.next_action, self.retryable = data, next_action, retryable

class Parser(argparse.ArgumentParser):
    def error(self, message):
        # Do not echo unknown positional arguments: they may be pasted secrets.
        raise Failure('invalid_arguments', 'Invalid arguments. Run antenna clawreef --help.')

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def fail(condition, *args, **kwargs):
    if not condition:
        raise Failure(*args, **kwargs)

def origin(value):
    try:
        u = urllib.parse.urlsplit(value)
        port = u.port
        valid = (u.scheme == 'https' or (u.scheme == 'http' and u.hostname == '127.0.0.1'))
        fail(valid and u.hostname and not u.username and not u.password and
             u.path in ('', '/') and not u.query and not u.fragment and
             not re.search(r'[\s\\\x00-\x1f\x7f]', value),
             'invalid_service', 'Use an HTTPS service origin without credentials, path, query or fragment.')
        return urllib.parse.urlunsplit((u.scheme, u.netloc.lower(), '', '', ''))
    except ValueError:
        raise Failure('invalid_service', 'Invalid service origin.') from None

def discover(service):
    try:
        req = urllib.request.Request(service + CONTRACT['discovery_path'],
            headers={'Accept': 'application/json', 'User-Agent': 'Antenna/1.6.6'})
        # No cookies, credentials, proxy-derived auth, redirect following, or writes.
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
        with opener.open(req, timeout=10) as response:
            fail(response.status == 200, 'service_error', 'Unexpected discovery response.', 5)
            raw = response.read(65537)
            fail(len(raw) <= 65536, 'invalid_discovery', 'Discovery response is too large.', 4)
            data = json.loads(raw)
    except urllib.error.HTTPError as error:
        code = 'unsupported_server' if error.code in (404, 405) else 'service_access_required' if error.code in (401, 403) else 'service_error'
        raise Failure(code, 'Discovery unavailable; no fallback or mutation performed.',
                      4 if error.code in (404,405) else 5,
                      data={'http_status': error.code}, retryable=error.code in (429, 502, 503, 504)) from None
    except (urllib.error.URLError, TimeoutError, OSError):
        raise Failure('network_error', 'Unable to read discovery; no mutation performed.', 5, retryable=True) from None
    except (ValueError, UnicodeError, RecursionError):
        raise Failure('invalid_discovery', 'Expected a supported JSON discovery object.', 4) from None
    fail(isinstance(data, dict) and data.get('service') == 'clawreef' and
         type(data.get('schema_version')) is int and data['schema_version'] == 1 and
         type(data.get('api_version')) is int and data['api_version'] == 1,
         'unsupported_version', 'Server does not advertise the supported ClawReef API version.', 4)
    def version(value):
        fail(isinstance(value, str) and re.fullmatch(r'\d{1,6}\.\d{1,6}\.\d{1,6}', value),
             'invalid_discovery', 'Invalid server compatibility metadata.', 4)
        return tuple(map(int, value.split('.')))
    fail(version(data.get('minimum_client_version')) <= version(CONTRACT['client_version']) and
         type(data.get('maximum_client_major')) is int and data['maximum_client_major'] >= 1,
         'unsupported_version', 'This client is outside the server compatibility range.', 4)
    fail(data.get('api_base') == CONTRACT['api_base'] and data.get('discovery_path') == CONTRACT['discovery_path'] and
         data.get('agents_page') == CONTRACT['agents_page'] and isinstance(data.get('features'), dict) and
         all(type(v) is bool for v in data['features'].values()) and isinstance(data.get('commands'), list) and
         all(isinstance(c, dict) and isinstance(c.get('name'), str) for c in data['commands']),
         'invalid_discovery', 'Unsupported discovery paths or feature metadata.', 4)
    # Only project known scalar fields; never print arbitrary remote prose/instructions.
    known = {c['name'] for c in CONTRACT['commands']}
    return {'service_origin': service, 'api_base': service + CONTRACT['api_base'],
            'agents_page': service + CONTRACT['agents_page'], 'api_version': 1,
            'features': {k: v for k, v in data['features'].items() if k in CONTRACT['features']},
            'available_commands': sorted(c['name'] for c in data['commands'] if c['name'] in known),
            'enrollment_checked': False}

def policy_module():
    import session_policy
    return session_policy

def local_state():
    fail((ROOT / 'antenna-config.json').is_file() and (ROOT / 'antenna-peers.json').is_file(),
         'setup_required', 'Antenna setup is required before local onboarding.', 3, next_action='antenna setup')
    policy = policy_module()
    try:
        config = policy.read(ROOT / 'antenna-config.json')
        policy.validate(config)
        peers = policy.read(ROOT / 'antenna-peers.json')
        fail(isinstance(peers, dict), 'invalid_local_state', 'Invalid local peer configuration.', 3)
        selves = [(key, value) for key, value in peers.items() if isinstance(value, dict) and value.get('self') is True]
        fail(len(selves) == 1, 'invalid_local_state', 'Exactly one self peer is required.', 3)
        host, peer = selves[0]
        fail(re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_.-]{0,63}', host), 'invalid_local_state', 'Invalid local host identity.', 3)
        candidates = []
        relay_agent = config.get('relay_agent_id', 'antenna')
        for key in config.get('allowed_inbound_sessions', []):
            try:
                agent = policy.owner(key)
                kind = key.split(':')[2]
                if agent != relay_agent and kind not in ('hook', 'cron', 'subagent', 'acp'):
                    candidates.append(key)
            except (ValueError, TypeError):
                continue
        return policy, config, peer, host, candidates
    except (ValueError, TypeError, KeyError, OSError):
        raise Failure('invalid_local_state', 'Invalid local Antenna configuration.', 3) from None

def fingerprint(peer):
    value = peer.get('signing_public_key_file')
    fail(isinstance(value, str) and value, 'signing_key_required', 'Configure a local Ed25519 signing public key.', 3)
    path = Path(value)
    if not path.is_absolute():
        path = ROOT / path
    try:
        fail(path.is_file() and path.stat().st_size <= 8192, 'invalid_signing_key', 'Invalid signing public key.', 3)
        result = subprocess.run(['openssl', 'pkey', '-pubin', '-in', str(path), '-outform', 'DER'],
                                capture_output=True, timeout=10)
        der = result.stdout
        fail(result.returncode == 0 and len(der) == 44 and der[:12] == bytes.fromhex('302a300506032b6570032100'),
             'invalid_signing_key', 'Expected an Ed25519 signing public key.', 3)
        return 'sha256:' + hashlib.sha256(der).hexdigest()
    except (OSError, subprocess.TimeoutExpired):
        raise Failure('invalid_signing_key', 'Unable to inspect signing public key.', 3) from None

def run(args):
    parser = Parser(add_help=False)
    parser.add_argument('command', nargs='?', default='help')
    parser.add_argument('group_command', nargs='?')
    parser.add_argument('group_id', nargs='?')
    parser.add_argument('--reason-stdin', action='store_true')
    parser.add_argument('--request-id')
    parser.add_argument('--name')
    parser.add_argument('--slug')
    parser.add_argument('--description')
    parser.add_argument('--theme', action='append', default=[])
    parser.add_argument('--query', default='')
    parser.add_argument('--after')
    parser.add_argument('--alias')
    parser.add_argument('--help', '-h', action='store_true')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--service', default='https://clawreef.io')
    parser.add_argument('--session')
    parser.add_argument('--actor')
    parser.add_argument('--request', action='append', default=[])
    parser.add_argument('--local-only', action='store_true')
    parser.add_argument('--code-stdin', action='store_true')
    parser.add_argument('--recover', action='store_true')
    opts = parser.parse_args(args)
    if opts.help or opts.command == 'help':
        return 'ok', 'ClawReef: discover, connect and take part in Public Groups.', {'commands': CONTRACT['commands'],
            'options': ['reports submit <group-id> --reason-stdin [--request-id <uuid>] | list [--after <uuid>] | show <request-id>', '--json', '--service <https-origin>', '--session <canonical-key|agent-alias|key-uuid>',
                        '--request <capability> (repeatable)', '--local-only (onboard/status)', '--code-stdin (enroll; never place codes in arguments)', '--recover (enroll; recover interrupted local registration)',
                        'groups browse|themes|show <id>|create --name <text> --slug <slug>|join <id>|leave <id>|reconcile <id>|resume <operation-id>', '--session <reference> (create/join)', '--theme <id> (repeatable create; one browse filter)', '--alias <local-alias> (create/join/reconcile)' ],
            'requestable_capabilities': CONTRACT['requestable_capabilities'], 'exit_codes': CONTRACT['exit_codes']}
    fail(opts.command in {c['name'] for c in CONTRACT['commands']}, 'unsupported_command',
         'This command is not available in this candidate. Run antenna clawreef --help.', 4)
    fail(not opts.actor, 'actor_profiles_unavailable', 'Use --session for a receiving conversation; per-actor permission profiles are not supported.', 4)
    fail(opts.command in ('onboard','enroll','groups') or not opts.session, 'invalid_arguments', '--session applies to onboarding, enrollment or group receiving-context selection.')
    fail(opts.command=='onboard' or not opts.request, 'invalid_arguments', '--request applies only to onboarding preparation.')
    fail(opts.command == 'enroll' or not (opts.code_stdin or opts.recover), 'invalid_arguments', 'Code input and recovery apply only to enroll.')
    fail(not opts.recover or not (opts.code_stdin or opts.session), 'invalid_arguments', 'Recovery uses the saved canonical binding.')
    fail(opts.command in ('onboard','status','discover') or not opts.local_only, 'invalid_arguments', 'This command requires a signed network request.')
    fail(opts.command in ('groups','reports') or not (opts.group_command or opts.group_id or opts.name or opts.slug or opts.description or opts.theme or opts.query or opts.after or opts.alias), 'invalid_arguments','Group options apply only to groups.')
    fail(opts.command=='reports' or not (opts.reason_stdin or opts.request_id), 'invalid_arguments','Report options apply only to reports.')
    service = origin(opts.service)
    if opts.command == 'discover':
        fail(not opts.local_only, 'invalid_arguments', 'discover requires an explicit read-only network request.')
        return 'ok', 'Compatible ClawReef discovery retrieved.', discover(service)
    policy, config, peer, host, candidates = local_state()
    registration_path = ROOT / '.clawreef' / (hashlib.sha256(service.encode()).hexdigest()+'.json')
    if opts.command in ('enroll','whoami','capabilities','groups','reports') or (opts.command == 'status' and (registration_path.exists() or registration_path.is_symlink())):
        import clawreef_registration as registration
        client=registration.Registration(sys.modules[__name__],service,(policy,config,peer,host,candidates))
        if opts.command=='reports':
            import clawreef_reports as reports
            return reports.run(client,opts)
        if opts.command=='groups':
            import clawreef_groups as groups
            return groups.run(client,opts)
        return client.enroll(opts) if opts.command=='enroll' else client.status(opts)
    if opts.command == 'status':
        raise Failure('enrollment_required', 'Local preparation only; remote enrollment and grants are not verified.', 3,
                      data={'host':host, 'service_origin':service, 'candidate_sessions': candidates,
                            'remote_checked':False, 'enrollment':'not_verified', 'signed_host_api_available':False},
                      next_action='antenna clawreef onboard --session <canonical-key> --request groups.join --json')
    fail(bool(opts.request) and all(x in CONTRACT['requestable_capabilities'] for x in opts.request),
         'capability_selection_required', 'Explicitly request one or more supported capabilities with --request.')
    key = opts.session
    if not key:
        fail(len(candidates) == 1, 'session_selection_required', 'Select exactly one eligible conversation with --session.', 6,
             data={'candidate_sessions':candidates})
        key = candidates[0]
    try:
        _, _, binding = policy.resolve(config, key)
        key = binding['canonical_key']
        fail(key in candidates, 'invalid_session_context', 'Relay, automation and unallowlisted contexts cannot be enrolled.', 6)
        agent = policy.owner(key)
    except (ValueError, KeyError, TypeError, OSError):
        raise Failure('invalid_session_context', 'Session resolution failed; use an existing allowlisted canonical conversation. No fallback performed.', 6) from None
    return 'prepared', 'Local request prepared. Review and share it with your human; nothing was sent or enrolled.', {
        'service_origin':service, 'host':host, 'signing_fingerprint':fingerprint(peer),
        'fingerprint_format':'SHA-256 of DER SubjectPublicKeyInfo',
        'context':{'agent_id':agent, 'canonical_session_key':key, 'assurance':'host-asserted'},
        'requested_capabilities':sorted(set(opts.request)), 'remote_checked':False,
        'enrollment_created':False, 'connectivity_verified':False,
        'human_review_url':service + CONTRACT['agents_page']}

def main():
    machine = '--json' in sys.argv[1:]
    correlation = str(uuid.uuid4())
    status = 0
    try:
        code, message, data = run(sys.argv[1:])
        result = dict(ok=True, code=code, message=message, data=data, retryable=False, next_action=None)
    except Failure as error:
        status = error.exit_code
        result = dict(ok=False, code=error.code, message=error.message, data=error.data,
                      retryable=error.retryable, next_action=error.next_action)
    except (ValueError, TypeError, KeyError, OSError):
        status = 3
        result = dict(ok=False, code='invalid_local_state', message='Unable to read local preparation state.',
                      data=None, retryable=False, next_action=None)
    result.update(schema_version=1, request_id=None, correlation_id=correlation)
    if machine:
        print(json.dumps(result, ensure_ascii=True))
    else:
        print(result['message'])
        if result['data'] is not None:
            print(json.dumps(result['data'], indent=2, ensure_ascii=True))
    if status:
        print('antenna clawreef: ' + result['message'], file=sys.stderr)
    return status

if __name__ == '__main__':
    sys.exit(main())
