"""The Chess-Results login, kept in the operating system's credential store.

One entry serves every host that starts this server — Claude Code, Codex, a
terminal — so the password is stored once and never in a file, a config or a
conversation. It is written by `cli.py login`, which asks for it hidden in the
user's own terminal.

Where it is looked for, first hit wins:

1. CHESS_RESULTS_PNO and CHESS_RESULTS_PASSWORD in the environment;
2. on macOS, the login keychain through Apple's `security` tool; elsewhere, the
   system store through the `keyring` package (Windows Credential Manager, Linux
   Secret Service);
3. a credentials file, for machines without a credential store (a headless server,
   a container): $CHESS_RESULTS_CREDENTIALS, else credentials.json in the host's
   plugin data folder ($PLUGIN_DATA, $CLAUDE_PLUGIN_DATA) if it gives one, else
   ~/.config/chess-results/credentials.json. The file must be the user's own and
   readable by nobody else (mode 600), or it is refused.

The file is the one route that reaches every process the same way — the command
line and an MCP server, in OpenClaw, Claude Code or Codex — without the host passing
anything: hosts start MCP servers with only a few inherited variables, and OpenClaw's
skill settings (skills.entries.*.apiKey/env) reach commands the agent runs, not MCP
servers.

On macOS the entry is written and read by the same program, /usr/bin/security,
which is on the entry's access list, so reading it never shows an authorization
dialog while the login keychain is unlocked (i.e. while the user is logged in).
`keyring` is deliberately not used there: the reader would be the Python binary,
and macOS would ask again after every Python update.

The store holds one generic password under the service "chess-results": the
account is the Chess-Results personal number, the secret the password. Nothing
here ever prints the password.
"""
import json
import os
import platform
import shutil
import stat
import subprocess
from pathlib import Path

SERVICE = 'chess-results'


class CredentialError(Exception):
    pass


def credentials_file():
    """Where the credentials file is looked for (it need not exist)."""
    if os.environ.get('CHESS_RESULTS_CREDENTIALS'):
        return Path(os.environ['CHESS_RESULTS_CREDENTIALS']).expanduser()
    for var in ('PLUGIN_DATA', 'CLAUDE_PLUGIN_DATA'):
        if os.environ.get(var) and (Path(os.environ[var]) / 'credentials.json').exists():
            return Path(os.environ[var]) / 'credentials.json'
    return Path.home() / '.config/chess-results/credentials.json'


def _from_file():
    path = credentials_file()
    if not path.exists():
        return None
    info = path.stat()
    if info.st_uid != os.getuid() or info.st_mode & (stat.S_IRWXG | stat.S_IRWXO):
        raise CredentialError(f'{path} must be your own and private: chmod 600 {path}')
    data = json.loads(path.read_text(encoding='utf-8'))
    if data.get('pno') and data.get('password'):
        return str(data['pno']), str(data['password'])
    raise CredentialError(f'{path} needs "pno" and "password".')


def store_file(pno, password, path=None):
    """Write the credentials file (mode 600) — for machines without a credential store."""
    path = Path(path).expanduser() if path else credentials_file()
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        json.dump({'pno': pno, 'password': password}, f)
    os.chmod(path, 0o600)
    return f'file {path}'


def _keyring():
    try:
        import keyring
        return keyring
    except ImportError:
        return None


def _security():
    return shutil.which('security') if platform.system() == 'Darwin' else None


def backend():
    """Where credentials are kept on this machine, for messages."""
    if _security():
        return 'macOS Keychain'
    if _keyring():
        return 'system credential store (keyring)'
    return None


def _keychain_account():
    """The personal number stored with the Keychain entry (its account field)."""
    out = subprocess.run([_security(), 'find-generic-password', '-s', SERVICE],
                         capture_output=True, text=True)
    if out.returncode != 0:
        return None
    for line in out.stdout.splitlines():
        line = line.strip()
        if line.startswith('"acct"'):
            return line.split('=', 1)[1].strip().strip('"') or None
    return None


def _keychain_password(pno):
    """The stored password. Read with -g rather than -w: -w prints a password with
    non-ASCII characters (umlauts) as bare hex, indistinguishable from a password
    that is hex; -g marks that case as 0x… and is decoded here."""
    out = subprocess.run([_security(), 'find-generic-password', '-s', SERVICE, '-a', pno, '-g'],
                         capture_output=True, text=True)
    if out.returncode != 0:
        return None
    for line in out.stderr.splitlines():
        if line.startswith('password: '):
            value = line[len('password: '):]
            if value.startswith('0x'):
                return bytes.fromhex(value[2:].split()[0]).decode('utf-8')
            if value.startswith('"') and value.endswith('"'):
                return value[1:-1].replace('\\"', '"').replace('\\\\', '\\')
            return value or None
    return None


def load():
    """(personal number, password), or raise CredentialError saying how to set them."""
    pno, password = os.environ.get('CHESS_RESULTS_PNO'), os.environ.get('CHESS_RESULTS_PASSWORD')
    if pno and password:
        return pno, password
    if _security():
        pno = _keychain_account()
        if pno:
            password = _keychain_password(pno)
            if password:
                return pno, password
    elif _keyring():
        kr = _keyring()
        pno = kr.get_password(SERVICE, '__account__')
        password = kr.get_password(SERVICE, pno) if pno else None
        if pno and password:
            return pno, password
    found = _from_file()
    if found:
        return found
    raise CredentialError(
        'No Chess-Results login stored. Run, in your own terminal: python3 <skill>/scripts/cli.py login '
        '(add --file on a machine without a credential store), or set CHESS_RESULTS_PNO and '
        'CHESS_RESULTS_PASSWORD.')


def store(pno, password):
    """Save the login, replacing any earlier one."""
    if not pno or not password:
        raise CredentialError('Both the personal number and the password are needed.')
    forget()
    if _security():
        # The value goes on stdin through `security -i`, so it never appears in the
        # process list. -T names /usr/bin/security as trusted: the reader is then
        # always the writer, and macOS reads the entry without asking.
        cmd = (f'add-generic-password -U -s {SERVICE} -a {pno} -l "Chess-Results" '
               f'-T {_security()} -w "{_quote(password)}"\n')
        out = subprocess.run([_security(), '-i'], input=cmd, capture_output=True, text=True)
        if out.returncode != 0:
            raise CredentialError('The Keychain refused the entry: ' + (out.stderr.strip() or 'unknown error'))
        return backend()
    kr = _keyring()
    if kr:
        kr.set_password(SERVICE, '__account__', pno)
        kr.set_password(SERVICE, pno, password)
        return backend()
    raise CredentialError('No credential store on this system. Install it with: pip install keyring '
                          '(or set CHESS_RESULTS_PNO and CHESS_RESULTS_PASSWORD).')


def _quote(text):
    return text.replace('\\', '\\\\').replace('"', '\\"')


def forget():
    """Remove a stored login, if there is one."""
    kr = None if _security() else _keyring()
    if kr:
        pno = kr.get_password(SERVICE, '__account__')
        for account in filter(None, (pno, '__account__')):
            try:
                kr.delete_password(SERVICE, account)
            except Exception:
                pass
    elif _security():
        while subprocess.run([_security(), 'delete-generic-password', '-s', SERVICE],
                             capture_output=True).returncode == 0:
            pass


def source():
    """Which route load() would use, for messages."""
    if os.environ.get('CHESS_RESULTS_PNO') and os.environ.get('CHESS_RESULTS_PASSWORD'):
        return 'environment'
    if _security() and _keychain_account():
        return 'macOS Keychain'
    kr = None if _security() else _keyring()
    if kr and kr.get_password(SERVICE, '__account__'):
        return 'system credential store (keyring)'
    if credentials_file().exists():
        return f'file {credentials_file()}'
    return None


def status():
    """What is configured, without revealing the password."""
    try:
        pno, _ = load()
        return dict(stored=True, source=source(), account=pno)
    except CredentialError as e:
        return dict(stored=False, source=backend(), hint=str(e))
