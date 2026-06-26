#!/usr/bin/env python3
"""clawsec-monitor.py — ClawSec Monitor v3.0
AI Agent Traffic Inspector (OpenClaw / Claude Desktop / Anthropic API)

Features:
  • HTTP forward proxy with full request + response inspection
  • HTTPS MITM — decrypts TLS, inspects plaintext, re-encrypts (requires CA install)
  • POST/PUT body scanning (first 64 KB)
  • Threat deduplication (60s rolling window)
  • Gateway WS proxy for OpenClaw
  • SSH connection tracking (Linux ss / macOS netstat)
  • Structured JSONL threat log with log rotation
  • Graceful shutdown (SIGTERM → SIGKILL fallback)

Usage:
    python3 clawsec-monitor.py start [--config FILE] [--no-mitm]
    python3 clawsec-monitor.py stop | status | threats [--limit N]

HTTPS MITM setup (one-time):
    # After first start, install the generated CA into your trust store:
    # macOS:
    sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain /tmp/clawsec/ca.crt
    # Linux:
    sudo cp /tmp/clawsec/ca.crt /usr/local/share/ca-certificates/clawsec.crt && sudo update-ca-certificates
    # Then route traffic:
    export http_proxy=http://localhost:8888 HTTPS_PROXY=http://localhost:8888
"""

from __future__ import annotations

import asyncio
import json
import logging
import logging.handlers
import os
import re
import signal
import ssl
import sys
import tempfile
import time
import argparse
from dataclasses import dataclass, asdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

# ── Optional MITM dependency ──────────────────────────────────────────────────

try:
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives.serialization import (
        Encoding, PrivateFormat, NoEncryption
    )
    MITM_AVAILABLE = True
except ImportError:
    MITM_AVAILABLE = False

# ── Config ────────────────────────────────────────────────────────────────────

DEFAULT_CONFIG: dict = {
    "http_proxy_port": 8888,
    "gateway_local_port": 18790,
    "gateway_target_port": 18789,
    "log_dir": "/tmp/clawsec",
    "log_level": "INFO",
    "max_scan_bytes": 65536,
    "ssh_poll_interval": 10,
    "dedup_window_secs": 60,
    "enable_http_proxy": True,
    "enable_gateway_proxy": True,
    "enable_ssh_watcher": True,
    "enable_mitm": True,          # set False or use --no-mitm to use blind CONNECT
}


def load_config(path: Optional[str]) -> dict:
    cfg = DEFAULT_CONFIG.copy()
    if path:
        try:
            cfg.update(json.loads(Path(path).read_text()))
        except Exception as exc:
            print(f"[warn] Could not load config {path}: {exc}", file=sys.stderr)
    return cfg


# ── Data model ────────────────────────────────────────────────────────────────

@dataclass
class Threat:
    direction: str      # "outbound" | "inbound"
    protocol: str       # "http" | "https" | "gateway" | "ssh"
    threat_type: str    # "EXFIL" | "INJECTION" | "SSH_CONNECT"
    pattern: str        # human-readable label
    snippet: str
    source: str = ""
    dest: str = ""
    timestamp: str = ""

    def __post_init__(self) -> None:
        if not self.timestamp:
            self.timestamp = datetime.now(timezone.utc).isoformat()
        self.snippet = self.snippet[:200]


# ── Detection patterns ────────────────────────────────────────────────────────

_EXFIL: list[tuple[str, re.Pattern]] = [
    ("ai_api_key",      re.compile(r'sk-(live|pro|ant|gpt|test)[a-zA-Z0-9_-]{20,}', re.I)),
    ("aws_access_key",  re.compile(r'(AKIA|ASIA)[0-9A-Z]{16}', re.I)),
    ("private_key_pem", re.compile(r'-----BEGIN (RSA|OPENSSH|EC|DSA) PRIVATE KEY-----', re.I)),
    ("ssh_key_file",    re.compile(r'\.ssh/(id_rsa|id_ed25519|config|authorized_keys)', re.I)),
    ("unix_sensitive",  re.compile(r'/etc/(passwd|shadow|sudoers)\b', re.I)),
    ("dotenv_file",     re.compile(r'/(\.env|\.aws/credentials)\b', re.I)),
    ("ssh_pubkey",      re.compile(r'ssh-rsa\s+[A-Za-z0-9+/=]{40,}', re.I)),
]

_INJECTION: list[tuple[str, re.Pattern]] = [
    ("pipe_to_shell",   re.compile(r'(curl|wget)\s+\S+\s*\|\s*(sh|bash)\b', re.I)),
    ("shell_exec",      re.compile(r'\b(bash|sh)\s+-[ci]\s+["\']', re.I)),
    ("reverse_shell",   re.compile(r'\b(nc|netcat|ncat)\s+\S+\s+\d{2,5}\b', re.I)),
    ("destructive_rm",  re.compile(r'\brm\s+-rf\s+/', re.I)),
    ("ssh_key_inject",  re.compile(r'echo\s+ssh-rsa\b', re.I)),
]


def scan(text: str, direction: str, source: str = "", dest: str = "",
         max_bytes: int = 65536, proto: str = "tcp") -> list[Threat]:
    """Scan text for EXFIL and INJECTION patterns in both directions."""
    truncated = text[:max_bytes]
    found: list[Threat] = []
    for patterns, ttype in ((_EXFIL, "EXFIL"), (_INJECTION, "INJECTION")):
        for label, rx in patterns:
            for m in rx.finditer(truncated):
                snippet = truncated[max(0, m.start() - 50): m.end() + 50]
                found.append(Threat(
                    direction=direction, protocol=proto, threat_type=ttype,
                    pattern=label, snippet=snippet, source=source, dest=dest,
                ))
    return found


# ── Logging / threat persistence ──────────────────────────────────────────────

_log = logging.getLogger("clawsec")
_threat_path: Path = Path("/tmp/clawsec/threats.jsonl")
_write_lock: asyncio.Lock
_dedup_window: float = 60.0
_dedup_seen: dict[str, float] = {}     # key -> last emit timestamp


def setup_logging(cfg: dict) -> None:
    global _threat_path, _write_lock, _dedup_window
    log_dir = Path(cfg["log_dir"])
    log_dir.mkdir(parents=True, exist_ok=True)
    log_dir.chmod(0o700)
    _threat_path = log_dir / "threats.jsonl"
    _write_lock = asyncio.Lock()
    _dedup_window = float(cfg.get("dedup_window_secs", 60))

    logging.basicConfig(
        level=getattr(logging, cfg["log_level"].upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.handlers.RotatingFileHandler(
                str(log_dir / "clawsec.log"), maxBytes=10 * 1024 * 1024, backupCount=3
            ),
            logging.StreamHandler(sys.stderr),
        ],
        force=True,
    )
    # Silence the harmless asyncio "returning true from eof_received() has no
    # effect when using ssl" warning that fires on every MITM connection close.
    logging.getLogger("asyncio").setLevel(logging.ERROR)


def _is_duplicate(threat: Threat) -> bool:
    """Return True if an identical (pattern, dest, direction) was seen within the dedup window."""
    key = f"{threat.pattern}:{threat.dest}:{threat.direction}"
    now = time.monotonic()
    if now - _dedup_seen.get(key, 0) < _dedup_window:
        return True
    _dedup_seen[key] = now
    return False


def _sync_append(line: str) -> None:
    with _threat_path.open("a") as f:
        f.write(line)


async def emit(threat: Threat) -> None:
    """Deduplicate, log to stderr, and append to JSONL (non-blocking, concurrency-safe)."""
    if _is_duplicate(threat):
        return
    _log.warning("[%s/%s] %s | %.120s",
                 threat.protocol.upper(), threat.direction,
                 threat.threat_type, threat.snippet.replace("\n", " "))
    line = json.dumps(asdict(threat)) + "\n"
    async with _write_lock:
        await asyncio.get_running_loop().run_in_executor(None, _sync_append, line)


# ── MITM: CA + certificate generation ────────────────────────────────────────

_ca_key = None
_ca_cert = None
_cert_ctx_cache: dict[str, ssl.SSLContext] = {}


def _gen_ca():
    """Generate a new 2048-bit RSA CA key and self-signed certificate."""
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    name = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, "ClawSec Monitor CA"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "ClawSec"),
    ])
    now = datetime.now(timezone.utc)
    cert = (
        x509.CertificateBuilder()
        .subject_name(name).issuer_name(name)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now)
        .not_valid_after(now + timedelta(days=3650))
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
        .add_extension(x509.KeyUsage(
            digital_signature=True, key_cert_sign=True, crl_sign=True,
            key_encipherment=False, data_encipherment=False, key_agreement=False,
            content_commitment=False, encipher_only=False, decipher_only=False,
        ), critical=True)
        .sign(key, hashes.SHA256())
    )
    return key, cert


def _gen_host_cert(hostname: str, ca_key, ca_cert):
    """Sign a per-host certificate with our CA."""
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    now = datetime.now(timezone.utc)
    try:
        from ipaddress import ip_address
        san = x509.SubjectAlternativeName([x509.IPAddress(ip_address(hostname))])
    except ValueError:
        san = x509.SubjectAlternativeName([x509.DNSName(hostname)])
    cert = (
        x509.CertificateBuilder()
        .subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, hostname)]))
        .issuer_name(ca_cert.subject)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now)
        .not_valid_after(now + timedelta(days=365))
        .add_extension(san, critical=False)
        .sign(ca_key, hashes.SHA256())
    )
    return key, cert


def _ssl_ctx_for_host(hostname: str) -> ssl.SSLContext:
    """Return (cached) server-side SSLContext with a cert signed by our CA."""
    if hostname in _cert_ctx_cache:
        return _cert_ctx_cache[hostname]

    host_key, host_cert = _gen_host_cert(hostname, _ca_key, _ca_cert)
    cert_pem = host_cert.public_bytes(Encoding.PEM)
    key_pem = host_key.private_bytes(Encoding.PEM, PrivateFormat.TraditionalOpenSSL,
                                      NoEncryption())
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.minimum_version = ssl.TLSVersion.TLSv1_2

    # ssl.SSLContext.load_cert_chain requires a file path — use a temp file
    fd, tmp = tempfile.mkstemp(suffix=".pem")
    try:
        os.write(fd, cert_pem + key_pem)
        os.close(fd)
        ctx.load_cert_chain(tmp)
    finally:
        os.unlink(tmp)

    _cert_ctx_cache[hostname] = ctx
    return ctx


def setup_mitm(log_dir: Path) -> bool:
    """Generate or load CA key/cert. Returns True if MITM is ready."""
    global _ca_key, _ca_cert
    if not MITM_AVAILABLE:
        _log.warning("MITM disabled: 'cryptography' library not installed. "
                     "Run: pip install cryptography")
        return False

    ca_key_path = log_dir / "ca.key"
    ca_crt_path = log_dir / "ca.crt"

    if ca_key_path.exists() and ca_crt_path.exists():
        try:
            _ca_key = serialization.load_pem_private_key(ca_key_path.read_bytes(), password=None)
            _ca_cert = x509.load_pem_x509_certificate(ca_crt_path.read_bytes())
            _log.info("MITM CA loaded from %s", ca_crt_path)
            return True
        except Exception as exc:
            _log.warning("Failed to load existing CA (%s), regenerating.", exc)

    _ca_key, _ca_cert = _gen_ca()
    ca_key_path.write_bytes(
        _ca_key.private_bytes(Encoding.PEM, PrivateFormat.TraditionalOpenSSL, NoEncryption()))
    ca_key_path.chmod(0o600)
    ca_crt_path.write_bytes(_ca_cert.public_bytes(Encoding.PEM))
    _log.info("MITM CA generated → %s", ca_crt_path)
    _log.info("Install CA to inspect HTTPS:  "
              "sudo security add-trusted-cert -d -r trustRoot "
              "-k /Library/Keychains/System.keychain %s", ca_crt_path)
    return True


# ── HTTP Proxy ────────────────────────────────────────────────────────────────

class HTTPProxy:
    """
    Transparent HTTP/HTTPS forward proxy on localhost.

    HTTP  — full request + response inspection (headers + body).
    HTTPS — MITM if CA is configured (full inspection); blind CONNECT otherwise.
    """

    _MAX_HEADER = 16_384

    def __init__(self, port: int, max_scan: int = 65536, mitm: bool = True) -> None:
        self.port = port
        self.max_scan = max_scan
        self.mitm = mitm and (_ca_key is not None)

    async def start(self) -> None:
        server = await asyncio.start_server(self._handle, "127.0.0.1", self.port)
        mode = "MITM" if self.mitm else "tunnel"
        _log.info("HTTP proxy on 127.0.0.1:%d (HTTPS mode: %s)", self.port, mode)
        async with server:
            await server.serve_forever()

    async def _handle(self, reader: asyncio.StreamReader,
                      writer: asyncio.StreamWriter) -> None:
        peer_ip = (writer.get_extra_info("peername") or ("?",))[0]
        try:
            await self._dispatch(reader, writer, peer_ip)
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            _log.debug("HTTP handler (%s): %s", peer_ip, exc)
        finally:
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass

    async def _read_headers(self, reader: asyncio.StreamReader) -> bytes:
        buf = b""
        while b"\r\n\r\n" not in buf and len(buf) < self._MAX_HEADER:
            chunk = await asyncio.wait_for(reader.read(4096), timeout=15)
            if not chunk:
                break
            buf += chunk
        return buf

    async def _dispatch(self, reader: asyncio.StreamReader,
                        writer: asyncio.StreamWriter, peer_ip: str) -> None:
        raw = await self._read_headers(reader)
        if not raw:
            return
        text = raw.decode("utf-8", errors="replace")
        first_line = text.split("\r\n", 1)[0]
        parts = first_line.split()
        if len(parts) < 2:
            return
        method, target = parts[0].upper(), parts[1]

        # Scan outbound request headers
        for t in scan(text, "outbound", source=peer_ip, dest=target,
                      max_bytes=self.max_scan):
            t.protocol = "http"
            await emit(t)

        # Scan request body for POST/PUT/PATCH
        body_preview = b""
        if method in ("POST", "PUT", "PATCH"):
            body_preview = await self._read_body_preview(reader, text)
            if body_preview:
                body_text = body_preview.decode("utf-8", errors="replace")
                for t in scan(body_text, "outbound", source=peer_ip, dest=target,
                              max_bytes=self.max_scan):
                    t.protocol = "http"
                    await emit(t)

        if method == "CONNECT":
            host, _, port_s = target.partition(":")
            port = int(port_s) if port_s.isdigit() else 443
            if self.mitm:
                await self._mitm_tunnel(reader, writer, host, port)
            else:
                await self._blind_tunnel(reader, writer, host, port)
        else:
            host, port = self._resolve_host(target, text)
            if not host:
                writer.write(b"HTTP/1.1 400 Bad Request\r\n\r\n")
                await writer.drain()
                return
            await self._forward(reader, writer, raw, body_preview, host, port)

    async def _read_body_preview(self, reader: asyncio.StreamReader,
                                  headers_text: str) -> bytes:
        """Read up to max_scan_bytes of request body using Content-Length."""
        cl = self._parse_content_length(headers_text)
        if not cl or cl <= 0:
            return b""
        try:
            to_read = min(cl, self.max_scan)
            return await asyncio.wait_for(reader.read(to_read), timeout=10)
        except Exception:
            return b""

    @staticmethod
    def _parse_content_length(headers: str) -> int:
        for line in headers.split("\r\n"):
            if line.lower().startswith("content-length:"):
                try:
                    return int(line.split(":", 1)[1].strip())
                except ValueError:
                    pass
        return 0

    async def _mitm_tunnel(self, reader: asyncio.StreamReader,
                            writer: asyncio.StreamWriter, host: str, port: int) -> None:
        """HTTPS MITM: connect upstream with TLS, upgrade client to TLS, inspect plaintext."""
        up_ssl = ssl.create_default_context()
        try:
            up_r, up_w = await asyncio.wait_for(
                asyncio.open_connection(host, port, ssl=up_ssl, server_hostname=host),
                timeout=10)
        except Exception as exc:
            _log.debug("MITM upstream %s:%d failed: %s", host, port, exc)
            writer.write(b"HTTP/1.1 502 Bad Gateway\r\n\r\n")
            await writer.drain()
            return

        writer.write(b"HTTP/1.1 200 Connection Established\r\n\r\n")
        await writer.drain()

        loop = asyncio.get_running_loop()
        try:
            client_ctx = _ssl_ctx_for_host(host)
        except Exception as exc:
            _log.debug("Cert gen failed %s: %s — falling back to blind tunnel", host, exc)
            up_w.close()
            # Re-send 200 won't work (already sent) — just pipe raw
            try:
                await asyncio.gather(self._pipe(reader, up_w), self._pipe(up_r, writer),
                                     return_exceptions=True)
            finally:
                up_w.close()
            return

        transport = writer.transport
        protocol = transport.get_protocol()
        try:
            tls_transport = await asyncio.wait_for(
                loop.start_tls(transport, protocol, client_ctx, server_side=True),
                timeout=10)
        except Exception as exc:
            _log.debug("MITM TLS handshake failed %s: %s", host, exc)
            up_w.close()
            return

        dest = f"{host}:{port}"
        try:
            await asyncio.gather(
                # reader decrypted from client → upstream (scan outbound)
                self._pipe_inspect(reader, up_w, "outbound", dest, proto="https"),
                # upstream → write encrypted to client (scan inbound)
                self._transport_pipe_inspect(up_r, tls_transport, "inbound", dest),
                return_exceptions=True,
            )
        finally:
            try:
                tls_transport.close()
            except Exception:
                pass
            up_w.close()

    async def _blind_tunnel(self, reader: asyncio.StreamReader,
                             writer: asyncio.StreamWriter, host: str, port: int) -> None:
        """HTTPS CONNECT — opaque tunnel, destination logged only."""
        try:
            tr, tw = await asyncio.wait_for(
                asyncio.open_connection(host, port), timeout=10)
        except Exception as exc:
            _log.debug("CONNECT %s:%d failed: %s", host, port, exc)
            writer.write(b"HTTP/1.1 502 Bad Gateway\r\n\r\n")
            await writer.drain()
            return
        writer.write(b"HTTP/1.1 200 Connection Established\r\n\r\n")
        await writer.drain()
        try:
            await asyncio.gather(self._pipe(reader, tw), self._pipe(tr, writer),
                                 return_exceptions=True)
        finally:
            tw.close()

    async def _forward(self, reader: asyncio.StreamReader,
                       writer: asyncio.StreamWriter, head: bytes, body_preview: bytes,
                       host: str, port: int) -> None:
        """Plain HTTP: forward request (with body), inspect response."""
        try:
            tr, tw = await asyncio.wait_for(
                asyncio.open_connection(host, port), timeout=10)
        except Exception as exc:
            _log.debug("HTTP connect %s:%d failed: %s", host, port, exc)
            writer.write(b"HTTP/1.1 502 Bad Gateway\r\n\r\n")
            await writer.drain()
            return
        tw.write(self._rewrite_request(head))
        if body_preview:
            tw.write(body_preview)
        try:
            await asyncio.gather(
                self._pipe(reader, tw),
                self._pipe_inspect(tr, writer, "inbound", f"{host}:{port}", proto="http"),
                return_exceptions=True,
            )
        finally:
            tw.close()

    @staticmethod
    def _rewrite_request(head: bytes) -> bytes:
        """Strip hop-by-hop proxy headers; force Connection: close."""
        lines = head.split(b"\r\n")
        out, has_conn = [], False
        for line in lines:
            low = line.lower()
            if low.startswith((b"proxy-connection:", b"keep-alive:")):
                continue
            if low.startswith(b"connection:"):
                out.append(b"Connection: close")
                has_conn = True
            else:
                out.append(line)
        if not has_conn:
            while out and out[-1] == b"":
                out.pop()
            out.append(b"Connection: close")
            out.append(b"")
            out.append(b"")
        return b"\r\n".join(out)

    async def _pipe(self, src: asyncio.StreamReader,
                    dst: asyncio.StreamWriter) -> None:
        try:
            while chunk := await src.read(4096):
                dst.write(chunk)
                await dst.drain()
        except asyncio.CancelledError:
            raise
        except Exception:
            pass

    async def _pipe_inspect(self, src: asyncio.StreamReader,
                            dst: asyncio.StreamWriter, direction: str,
                            dest: str, proto: str = "http") -> None:
        scanned = 0
        try:
            while chunk := await src.read(4096):
                if scanned < self.max_scan:
                    text = chunk.decode("utf-8", errors="replace")
                    for t in scan(text, direction, dest=dest, max_bytes=self.max_scan,
                                  proto=proto):
                        await emit(t)
                    scanned += len(chunk)
                dst.write(chunk)
                await dst.drain()
        except asyncio.CancelledError:
            raise
        except Exception:
            pass

    async def _transport_pipe_inspect(self, src: asyncio.StreamReader,
                                       dst_transport, direction: str, dest: str) -> None:
        """Inspect then write to raw TLS transport (MITM inbound path)."""
        scanned = 0
        try:
            while chunk := await src.read(4096):
                if scanned < self.max_scan:
                    text = chunk.decode("utf-8", errors="replace")
                    for t in scan(text, direction, dest=dest, max_bytes=self.max_scan,
                                  proto="https"):
                        await emit(t)
                    scanned += len(chunk)
                dst_transport.write(chunk)
        except asyncio.CancelledError:
            raise
        except Exception:
            pass

    @staticmethod
    def _resolve_host(target: str, headers: str) -> tuple[str, int]:
        if target.startswith("http://"):
            p = urlparse(target)
            return (p.hostname or ""), (p.port or 80)
        for line in headers.split("\r\n"):
            if line.lower().startswith("host:"):
                val = line.split(":", 1)[1].strip()
                if ":" in val:
                    h, p = val.rsplit(":", 1)
                    return h, int(p) if p.isdigit() else 80
                return val, 80
        return "", 80


# ── Gateway Proxy ─────────────────────────────────────────────────────────────

class GatewayProxy:
    """Bidirectional TCP proxy for OpenClaw Gateway (WS traffic)."""

    def __init__(self, local_port: int, target_port: int,
                 max_scan: int = 65536) -> None:
        self.local_port = local_port
        self.target_port = target_port
        self.max_scan = max_scan

    async def start(self) -> None:
        server = await asyncio.start_server(self._handle, "127.0.0.1", self.local_port)
        _log.info("Gateway proxy %d -> %d", self.local_port, self.target_port)
        async with server:
            await server.serve_forever()

    async def _handle(self, reader: asyncio.StreamReader,
                      writer: asyncio.StreamWriter) -> None:
        try:
            tr, tw = await asyncio.wait_for(
                asyncio.open_connection("127.0.0.1", self.target_port), timeout=5)
        except Exception as exc:
            _log.debug("Gateway upstream connect failed: %s", exc)
            writer.close()
            return
        try:
            await asyncio.gather(
                self._pipe(reader, tw, "outbound"),
                self._pipe(tr, writer, "inbound"),
                return_exceptions=True,
            )
        finally:
            tw.close()
            writer.close()

    async def _pipe(self, src: asyncio.StreamReader,
                    dst: asyncio.StreamWriter, direction: str) -> None:
        try:
            while chunk := await src.read(4096):
                text = chunk.decode("utf-8", errors="replace")
                for t in scan(text, direction, max_bytes=self.max_scan, proto="gateway"):
                    await emit(t)
                dst.write(chunk)
                await dst.drain()
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            _log.debug("Gateway pipe (%s): %s", direction, exc)


# ── SSH Watcher ───────────────────────────────────────────────────────────────

class SSHWatcher:
    """Polls for established SSH connections (Linux: ss, macOS: netstat)."""

    def __init__(self, poll_interval: int = 10) -> None:
        self.poll_interval = poll_interval
        self._seen: set[str] = set()

    async def watch(self) -> None:
        while True:
            await asyncio.sleep(self.poll_interval)
            current = await self._get_ssh_conns()
            for conn in current - self._seen:
                t = Threat("outbound", "ssh", "SSH_CONNECT",
                           "established_connection", conn[:200])
                await emit(t)
            self._seen = current

    async def _get_ssh_conns(self) -> set[str]:
        # Try ss (Linux) first, fall back to netstat (macOS/BSD)
        for cmd, filter_fn in [
            (["ss", "-tnp"], lambda l: "ESTAB" in l and ":22 " in l),
            (["netstat", "-tn"], lambda l: "ESTABLISHED" in l and ".22 " in l),
        ]:
            try:
                proc = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.DEVNULL,
                )
                stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=5)
                return {
                    line.strip()
                    for line in stdout.decode("utf-8", errors="replace").splitlines()
                    if filter_fn(line)
                }
            except (FileNotFoundError, asyncio.TimeoutError):
                continue
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                _log.debug("SSHWatcher (%s): %s", cmd[0], exc)
        return set()


# ── Runner ────────────────────────────────────────────────────────────────────

async def run(cfg: dict) -> None:
    loop = asyncio.get_running_loop()
    stop = asyncio.Event()

    def _on_signal():
        loop.call_soon_threadsafe(stop.set)

    for sig in (signal.SIGTERM, signal.SIGINT):
        try:
            loop.add_signal_handler(sig, _on_signal)
        except (NotImplementedError, OSError):
            signal.signal(sig, lambda s, f: _on_signal())

    tasks: list[asyncio.Task] = []
    max_scan: int = cfg["max_scan_bytes"]
    mitm_on: bool = cfg.get("enable_mitm", True)

    if cfg["enable_http_proxy"]:
        tasks.append(asyncio.create_task(
            HTTPProxy(cfg["http_proxy_port"], max_scan, mitm=mitm_on).start(),
            name="http"))
    if cfg["enable_gateway_proxy"]:
        tasks.append(asyncio.create_task(
            GatewayProxy(cfg["gateway_local_port"],
                         cfg["gateway_target_port"], max_scan).start(),
            name="gateway"))
    if cfg["enable_ssh_watcher"]:
        tasks.append(asyncio.create_task(
            SSHWatcher(cfg["ssh_poll_interval"]).watch(), name="ssh"))

    _log.info("ClawSec Monitor v3.0 — PID %d — %d component(s) — MITM %s",
              os.getpid(), len(tasks), "ON" if mitm_on and _ca_key else "OFF")
    await stop.wait()

    _log.info("Shutting down…")
    for t in tasks:
        t.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)
    _log.info("Done.")


# ── PID helpers ───────────────────────────────────────────────────────────────

_PID_FILE = Path("/tmp/clawsec/monitor.pid")


def _pid_running() -> Optional[int]:
    try:
        pid = int(_PID_FILE.read_text().strip())
        os.kill(pid, 0)
        return pid
    except (FileNotFoundError, ValueError, ProcessLookupError, PermissionError):
        return None


# ── CLI ───────────────────────────────────────────────────────────────────────

def cmd_start(args: argparse.Namespace) -> None:
    cfg = load_config(getattr(args, "config", None))
    if getattr(args, "no_mitm", False):
        cfg["enable_mitm"] = False
    setup_logging(cfg)

    if pid := _pid_running():
        print(f"Already running (PID {pid}). Use 'stop' first.", file=sys.stderr)
        sys.exit(1)

    try:
        _PID_FILE.parent.mkdir(parents=True, exist_ok=True)
        with _PID_FILE.open("x") as f:
            f.write(str(os.getpid()))
    except FileExistsError:
        if pid := _pid_running():
            print(f"Already running (PID {pid}).", file=sys.stderr)
            sys.exit(1)
        _PID_FILE.unlink(missing_ok=True)
        _PID_FILE.write_text(str(os.getpid()))

    if cfg.get("enable_mitm", True):
        setup_mitm(Path(cfg["log_dir"]))

    try:
        asyncio.run(run(cfg))
    finally:
        _PID_FILE.unlink(missing_ok=True)


def cmd_stop(_: argparse.Namespace) -> None:
    pid = _pid_running()
    if not pid:
        print("Not running.")
        return
    os.kill(pid, signal.SIGTERM)
    print(f"Sent SIGTERM to PID {pid} — waiting for shutdown...", end="", flush=True)
    for _ in range(50):
        time.sleep(0.1)
        if not _pid_running():
            print(" stopped.")
            return
    print(" timeout, sending SIGKILL.")
    try:
        os.kill(pid, signal.SIGKILL)
        _PID_FILE.unlink(missing_ok=True)
    except ProcessLookupError:
        pass


def cmd_threats(args: argparse.Namespace) -> None:
    try:
        lines = _threat_path.read_text().splitlines()
        threats = [json.loads(l) for l in lines if l.strip()]
        threats.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        print(json.dumps(threats[: args.limit], indent=2))
    except FileNotFoundError:
        print("[]")
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


def cmd_status(args: argparse.Namespace) -> None:
    pid = _pid_running()
    print(f"ClawSec Monitor: {'RUNNING (PID ' + str(pid) + ')' if pid else 'STOPPED'}")
    cmd_threats(argparse.Namespace(limit=5))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="ClawSec Monitor v3.0 — AI Agent Traffic Inspector",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Docs: https://github.com/chrisochrisochriso-cmyk/clawsec-monitor"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_start = sub.add_parser("start", help="Start the monitor (foreground)")
    p_start.add_argument("--config", metavar="FILE", help="JSON config file")
    p_start.add_argument("--no-mitm", action="store_true",
                         help="Use blind CONNECT tunnel instead of HTTPS MITM")
    p_start.set_defaults(func=cmd_start)

    p_stop = sub.add_parser("stop", help="Stop a running monitor")
    p_stop.set_defaults(func=cmd_stop)

    p_status = sub.add_parser("status", help="Show status and 5 recent threats")
    p_status.set_defaults(func=cmd_status)

    p_threats = sub.add_parser("threats", help="Dump recent threats as JSON")
    p_threats.add_argument("--limit", type=int, default=10, metavar="N")
    p_threats.set_defaults(func=cmd_threats)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
