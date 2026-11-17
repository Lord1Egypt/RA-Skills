"""CLAWREEF-HTTP-1 signing primitives; no network, enrollment or key generation.

The caller supplies the reviewed host/actor binding and selected service. This
module never resolves an alias or infers identity from a runtime session ID.
"""
import base64
import datetime
import hashlib
import os
from pathlib import Path
import re
import secrets
import stat
import subprocess
import tempfile
import uuid

FIELDS = ('audience', 'method', 'path', 'query', 'host_id', 'actor_id', 'key_id',
          'timestamp', 'nonce', 'idempotency_key', 'body_sha256')

class SigningError(ValueError):
    pass

def canonical(fields):
    if set(fields) != set(FIELDS) or not all(isinstance(fields[x], str) for x in FIELDS):
        raise SigningError('Invalid signing fields')
    result = bytearray(b'CLAWREEF-HTTP-1\n')
    for name in FIELDS:
        value = fields[name].encode('utf-8')
        result.extend(name.encode() + b':' + str(len(value)).encode() + b':' + value + b'\n')
    return bytes(result)

def timestamp():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

def operation_id():
    return timestamp().replace('-', '').replace(':', '') + '.' + str(uuid.uuid4())

def nonce():
    return base64.urlsafe_b64encode(secrets.token_bytes(16)).decode().rstrip('=')

def sign(fields, private_key_path, expected_key_id):
    """Use a protected existing key; never echo OpenSSL diagnostics or key data.

    Open once without following a final symlink, verify inode permissions/owner,
    then pass that same descriptor to OpenSSL to avoid a pathname-swap race.
    Only public canonical bytes are written to a private temporary directory.
    """
    fd = None
    try:
        fd = os.open(private_key_path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        info = os.fstat(fd)
        if (not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or
                info.st_mode & 0o077 or not 0 < info.st_size <= 8192):
            raise SigningError('Unsafe signing key file')
        key_path = '/proc/self/fd/' + str(fd)
        public = subprocess.run(['openssl','pkey','-in',key_path,'-pubout','-outform','DER','-passin','pass:'],
            pass_fds=(fd,), capture_output=True, timeout=10)
        der = public.stdout
        if (public.returncode or len(der) != 44 or der[:12] != bytes.fromhex('302a300506032b6570032100') or
                'ed25519-sha256:' + hashlib.sha256(der).hexdigest() != expected_key_id or
                fields['key_id'] != expected_key_id):
            raise SigningError('Signing key does not match reviewed binding')
        os.lseek(fd, 0, os.SEEK_SET)
        with tempfile.TemporaryDirectory(prefix='antenna-http-') as directory:
            source = Path(directory) / 'canonical'
            source.write_bytes(canonical(fields))
            source.chmod(0o600)
            signed = subprocess.run(['openssl','pkeyutl','-sign','-rawin','-inkey',key_path,
                '-passin','pass:','-in',str(source)],pass_fds=(fd,),capture_output=True,timeout=10)
            if signed.returncode or len(signed.stdout) != 64:
                raise SigningError('Unable to sign request')
            return base64.b64encode(signed.stdout).decode()
    except (OSError, subprocess.TimeoutExpired, KeyError, TypeError):
        raise SigningError('Unable to use protected signing key') from None
    finally:
        if fd is not None:
            os.close(fd)

def headers(fields, signature):
    """Signed request headers only; never add cookies or reusable human tokens."""
    names = {'host_id':'X-ClawReef-Host','actor_id':'X-ClawReef-Actor','key_id':'X-ClawReef-Key-Id',
             'timestamp':'X-ClawReef-Timestamp','nonce':'X-ClawReef-Nonce','idempotency_key':'Idempotency-Key'}
    result = {'X-ClawReef-Protocol':'CLAWREEF-HTTP-1','X-ClawReef-Signature':signature}
    result.update({header:fields[field] for field,header in names.items() if fields[field]})
    return result
