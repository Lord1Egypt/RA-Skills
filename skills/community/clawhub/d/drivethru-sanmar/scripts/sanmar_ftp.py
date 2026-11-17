"""General SanMar SFTP helper.

A thin wrapper over paramiko for the SanMar SFTP server, used by the
FTP-file tools (Daily Invoice file, Daily Shipment Status file, and the
inventory feed). It can read a file by exact path or find the most
recent file matching a glob in a directory — SanMar's by-request outbound
files carry date stamps in their names (``123456_Invoice_Details-06-18-15.txt``,
``1-15-16Status.txt``), so "newest by modified-time" reliably picks the
latest drop.

Connection details from the SanMar FTP Integration Guide v23.1:
``Host: ftp.sanmar.com``, ``Port: 2200``, protocol **SFTP (SSH)** — the
server is *not* TLS-compatible. The username is your SanMar customer
number; the password is FTP-specific (NOT the SanMar.com web-services
password).

Credential resolution reuses :func:`ftp_resolver.ftp_credentials_from_env`
and the :class:`ftp_resolver.SanMarFTPError` taxonomy so the CLI maps
failures to the same ``connection_error`` / ``config_error`` envelopes as
the mainframe-color resolver.
"""

from __future__ import annotations

import fnmatch
import logging
import os

from ftp_resolver import (  # noqa: E402  (sibling module, scripts dir on sys.path)
    SanMarFTPError,
    ftp_credentials_from_env,
)
from schemas import SanMarFTPCredentials  # noqa: E402

logger = logging.getLogger(__name__)

# Nightly product/inventory feeds live under SanMarPDD; by-request outbound
# files (invoices, shipment status, pricing) land in the account's outbound
# folder, which is account-specific — default to the FTP root and let the
# caller override via argument or SANMAR_FTP_OUTBOUND_DIR.
PDD_DIR = "/SanMarPDD"
DEFAULT_OUTBOUND_DIR = os.environ.get("SANMAR_FTP_OUTBOUND_DIR", "/").strip() or "/"


class SanMarFTP:
    """Minimal SFTP client for reading files off the SanMar server.

    Use as a context manager so the transport is always closed::

        with SanMarFTP(credentials) as ftp:
            text = ftp.read_text("/SanMarPDD/sanmar_dip.txt")
    """

    def __init__(
        self, credentials: SanMarFTPCredentials | None = None, *, timeout: int = 60
    ) -> None:
        self.credentials = credentials or ftp_credentials_from_env()
        self.timeout = timeout
        self._transport = None
        self._sftp = None

    def __enter__(self) -> "SanMarFTP":
        self.connect()
        return self

    def __exit__(self, *_exc: object) -> None:
        self.close()

    def connect(self) -> None:
        try:
            import paramiko
        except ImportError as exc:  # pragma: no cover — runtime guard
            raise SanMarFTPError(
                "paramiko is required for SanMar SFTP access. "
                "Install it with `pip install paramiko`."
            ) from exc

        creds = self.credentials
        logger.info(
            "Connecting to SanMar SFTP %s:%s as %s",
            creds.host,
            creds.port,
            creds.username,
        )
        transport = paramiko.Transport((creds.host, creds.port))
        try:
            transport.connect(username=creds.username, password=creds.password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            if sftp is None:
                raise SanMarFTPError("Could not open SFTP channel after authenticating")
            sftp.get_channel().settimeout(self.timeout)
        except paramiko.SSHException as exc:
            transport.close()
            raise SanMarFTPError(f"SanMar SFTP error: {exc}") from exc
        except OSError as exc:
            transport.close()
            raise SanMarFTPError(f"SanMar SFTP connection failed: {exc}") from exc
        self._transport = transport
        self._sftp = sftp

    def close(self) -> None:
        if self._sftp is not None:
            try:
                self._sftp.close()
            except Exception:  # noqa: BLE001 — best-effort close
                pass
            self._sftp = None
        if self._transport is not None:
            self._transport.close()
            self._transport = None

    def _require(self):
        if self._sftp is None:
            raise SanMarFTPError("SFTP session is not connected")
        return self._sftp

    def read_bytes(self, remote_path: str) -> bytes:
        sftp = self._require()
        try:
            with sftp.open(remote_path, "rb") as handle:
                return handle.read()
        except OSError as exc:
            raise SanMarFTPError(f"Failed to read {remote_path}: {exc}") from exc

    def read_text(self, remote_path: str, *, encoding: str = "utf-8-sig") -> str:
        # utf-8-sig transparently strips the BOM SanMar sometimes prepends.
        return self.read_bytes(remote_path).decode(encoding, errors="replace")

    def listdir(self, remote_dir: str = "/") -> list[str]:
        sftp = self._require()
        try:
            return sftp.listdir(remote_dir)
        except OSError as exc:
            raise SanMarFTPError(f"Failed to list {remote_dir}: {exc}") from exc

    def find_latest(self, remote_dir: str, pattern: str) -> str | None:
        """Return the full path of the newest file in ``remote_dir`` whose
        name matches the case-insensitive glob ``pattern`` (by modified
        time), or ``None`` if nothing matches."""

        sftp = self._require()
        try:
            entries = sftp.listdir_attr(remote_dir)
        except OSError as exc:
            raise SanMarFTPError(f"Failed to list {remote_dir}: {exc}") from exc

        pat = pattern.lower()
        candidates = [
            entry for entry in entries if fnmatch.fnmatch(entry.filename.lower(), pat)
        ]
        if not candidates:
            return None
        newest = max(candidates, key=lambda e: getattr(e, "st_mtime", 0) or 0)
        base = remote_dir.rstrip("/")
        return f"{base}/{newest.filename}"
