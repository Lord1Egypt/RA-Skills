#!/usr/bin/env python3
"""Phase 13.5 -- deterministic tests for secure remote source acquisition.

Every test here is deterministic and offline: the HTTP transport and the DNS
resolver are both injected, so the suite never depends on internet or DNS
availability, and it never contacts a real host. No AI subscription quota is
consumed and no real Codex or Kiro process is launched.

These tests cover acquisition only -- URL policy, SSRF guardrails, redirect
revalidation, response bounds, path safety, and the handoff into the existing
Phase 13 ingestion. They assert nothing about semantic meaning: that remains
AGY's authority.

The separate bounded live check against a real public source lives in
``tests/integration/test_remote_acquisition_live.py`` and is opt-in.
"""

from __future__ import annotations

import json
import socket
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

HELPERS_DIR = Path(__file__).resolve().parent / "helpers"
if str(HELPERS_DIR) not in sys.path:
    sys.path.insert(0, str(HELPERS_DIR))

import source_acquisition as sa  # noqa: E402
import source_ingestion as si  # noqa: E402
from source_grounding import compute_source_digest  # noqa: E402

from fake_http import (  # noqa: E402
    FakeOpener,
    FakeResponse,
    http_error,
    public_resolver,
    redirect,
    resolver_for,
)
from synthetic_docx import build_structured_docx  # noqa: E402
from synthetic_pdf import build_text_pdf  # noqa: E402

PUBLIC_URL = "https://sources.example.test/source.txt"
TXT_BODY = "\u6cbb\u7406\u67b6\u69cb\nGovernance Architecture\n".encode("utf-8")


class AcquisitionTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.out = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def acquire(self, url: str = PUBLIC_URL, **kwargs):
        opener = kwargs.pop("opener", None)
        if opener is None:
            opener = FakeOpener(
                routes={
                    url: FakeResponse(
                        TXT_BODY,
                        headers={
                            "Content-Type": "text/plain; charset=utf-8",
                            "Content-Length": str(len(TXT_BODY)),
                        },
                    )
                }
            )
        kwargs.setdefault("resolver", public_resolver)
        return sa.acquire_remote_source(url, kwargs.pop("source_id", "src_remote"),
                                       self.out, opener=opener, **kwargs)


# ---------------------------------------------------------------------------
# URL validation
# ---------------------------------------------------------------------------
class TestUrlValidation(AcquisitionTestCase):
    def test_https_accepted(self) -> None:
        parts = sa.validate_remote_url("https://example.test/a.pdf")
        self.assertEqual(parts.scheme, "https")

    def test_http_accepted(self) -> None:
        parts = sa.validate_remote_url("http://example.test/a.pdf")
        self.assertEqual(parts.scheme, "http")

    def test_file_scheme_rejected(self) -> None:
        with self.assertRaises(sa.RemoteSchemeUnsupported) as ctx:
            sa.validate_remote_url("file:///etc/passwd")
        self.assertEqual(ctx.exception.error_code, sa.ERROR_REMOTE_SCHEME_UNSUPPORTED)

    def test_ftp_scheme_rejected(self) -> None:
        with self.assertRaises(sa.RemoteSchemeUnsupported):
            sa.validate_remote_url("ftp://example.test/a.pdf")

    def test_data_scheme_rejected(self) -> None:
        with self.assertRaises(sa.RemoteSchemeUnsupported):
            sa.validate_remote_url("data:text/plain;base64,aGk=")

    def test_other_schemes_rejected(self) -> None:
        for url in (
            "javascript:alert(1)",
            "blob:https://example.test/x",
            "ssh://example.test/x",
            "gopher://example.test/x",
        ):
            with self.assertRaises(sa.RemoteSchemeUnsupported, msg=url):
                sa.validate_remote_url(url)

    def test_missing_scheme_rejected(self) -> None:
        with self.assertRaises(sa.RemoteSchemeUnsupported):
            sa.validate_remote_url("example.test/a.pdf")

    def test_embedded_credentials_rejected(self) -> None:
        with self.assertRaises(sa.RemoteCredentialsUnsupported) as ctx:
            sa.validate_remote_url("https://user:password@example.test/file")
        self.assertEqual(
            ctx.exception.error_code, sa.ERROR_REMOTE_CREDENTIALS_UNSUPPORTED
        )
        # The credential material must never be echoed back.
        self.assertNotIn("password", str(ctx.exception))

    def test_username_only_credentials_rejected(self) -> None:
        with self.assertRaises(sa.RemoteCredentialsUnsupported):
            sa.validate_remote_url("https://user@example.test/file")

    def test_empty_url_rejected(self) -> None:
        for url in ("", "   ", None):
            with self.assertRaises(sa.RemoteUrlInvalid):
                sa.validate_remote_url(url)  # type: ignore[arg-type]

    def test_missing_host_rejected(self) -> None:
        with self.assertRaises(sa.RemoteUrlInvalid):
            sa.validate_remote_url("https:///no-host")


# ---------------------------------------------------------------------------
# SSRF guardrails
# ---------------------------------------------------------------------------
class TestHostGuardrails(AcquisitionTestCase):
    def test_localhost_rejected(self) -> None:
        with self.assertRaises(sa.RemoteHostBlocked) as ctx:
            sa.check_host_allowed("localhost", resolver=public_resolver)
        self.assertEqual(ctx.exception.error_code, sa.ERROR_REMOTE_HOST_BLOCKED)

    def test_localhost_subdomain_rejected(self) -> None:
        with self.assertRaises(sa.RemoteHostBlocked):
            sa.check_host_allowed("api.localhost", resolver=public_resolver)

    def test_loopback_ipv4_literal_rejected(self) -> None:
        with self.assertRaises(sa.RemoteHostBlocked):
            sa.check_host_allowed("127.0.0.1")

    def test_loopback_ipv6_literal_rejected(self) -> None:
        with self.assertRaises(sa.RemoteHostBlocked):
            sa.check_host_allowed("::1")
        with self.assertRaises(sa.RemoteHostBlocked):
            sa.check_host_allowed("[::1]")

    def test_private_ipv4_literals_rejected(self) -> None:
        for host in ("10.0.0.1", "172.16.0.1", "192.168.1.1"):
            with self.assertRaises(sa.RemoteHostBlocked, msg=host):
                sa.check_host_allowed(host)

    def test_link_local_and_metadata_rejected(self) -> None:
        for host in ("169.254.0.1", "169.254.169.254"):
            with self.assertRaises(sa.RemoteHostBlocked, msg=host):
                sa.check_host_allowed(host)

    def test_private_ipv6_literals_rejected(self) -> None:
        for host in ("fc00::1", "fd00::1", "fe80::1"):
            with self.assertRaises(sa.RemoteHostBlocked, msg=host):
                sa.check_host_allowed(host)

    def test_unspecified_and_multicast_rejected(self) -> None:
        for host in ("0.0.0.0", "::", "224.0.0.1"):
            with self.assertRaises(sa.RemoteHostBlocked, msg=host):
                sa.check_host_allowed(host)

    def test_ipv4_mapped_ipv6_loopback_rejected(self) -> None:
        """::ffff:127.0.0.1 must be unwrapped before classification."""
        with self.assertRaises(sa.RemoteHostBlocked):
            sa.check_host_allowed("::ffff:127.0.0.1")
        with self.assertRaises(sa.RemoteHostBlocked):
            sa.check_host_allowed("::ffff:10.0.0.1")

    def test_hostname_resolving_to_loopback_rejected(self) -> None:
        resolver = resolver_for({"evil.example.test": "127.0.0.1"})
        with self.assertRaises(sa.RemoteHostBlocked) as ctx:
            sa.check_host_allowed("evil.example.test", resolver=resolver)
        self.assertIn("non-public", str(ctx.exception))

    def test_hostname_resolving_to_private_rejected(self) -> None:
        resolver = resolver_for({"internal.example.test": "10.1.2.3"})
        with self.assertRaises(sa.RemoteHostBlocked):
            sa.check_host_allowed("internal.example.test", resolver=resolver)

    def test_public_hostname_accepted(self) -> None:
        resolved = sa.check_host_allowed(
            "sources.example.test", resolver=resolver_for({"sources.example.test": "93.184.216.34"})
        )
        self.assertEqual(resolved, ["93.184.216.34"])

    def test_fails_closed_when_any_address_is_private(self) -> None:
        """A name with a mixed answer set is refused, not partially trusted."""

        def mixed(*_a: object, **_k: object) -> list[tuple]:
            return [
                (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 0)),
                (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("127.0.0.1", 0)),
            ]

        with self.assertRaises(sa.RemoteHostBlocked):
            sa.check_host_allowed("mixed.example.test", resolver=mixed)

    def test_unresolvable_host_blocked(self) -> None:
        def fails(*_a: object, **_k: object):
            raise socket.gaierror("nope")

        with self.assertRaises(sa.RemoteHostBlocked):
            sa.check_host_allowed("missing.example.test", resolver=fails)

    def test_blocked_host_never_reaches_transport(self) -> None:
        opener = FakeOpener(routes={})
        with self.assertRaises(sa.RemoteHostBlocked):
            sa.acquire_remote_source(
                "https://127.0.0.1/secret", "src_x", self.out, opener=opener
            )
        self.assertEqual(opener.requested, [])


# ---------------------------------------------------------------------------
# Redirects
# ---------------------------------------------------------------------------
class TestRedirects(AcquisitionTestCase):
    def test_public_to_public_redirect_followed(self) -> None:
        first = "https://a.example.test/one"
        second = "https://b.example.test/two"
        opener = FakeOpener(
            routes={
                first: redirect(second),
                second: FakeResponse(TXT_BODY, headers={"Content-Type": "text/plain"}),
            }
        )
        result = sa.acquire_remote_source(
            first,
            "src_redir",
            self.out,
            opener=opener,
            resolver=resolver_for(
                {"a.example.test": "93.184.216.34", "b.example.test": "93.184.216.35"}
            ),
        )
        self.assertEqual(result.redirect_count, 1)
        self.assertEqual(result.requested_url, first)
        self.assertEqual(result.final_url, second)
        self.assertEqual(opener.requested, [first, second])

    def test_redirect_to_localhost_blocked(self) -> None:
        first = "https://a.example.test/one"
        opener = FakeOpener(routes={first: redirect("http://localhost/admin")})
        with self.assertRaises(sa.RemoteRedirectBlocked) as ctx:
            sa.acquire_remote_source(
                first, "src_r", self.out, opener=opener, resolver=public_resolver
            )
        self.assertEqual(ctx.exception.error_code, sa.ERROR_REMOTE_REDIRECT_BLOCKED)
        self.assertEqual(opener.requested, [first])

    def test_redirect_to_private_ip_blocked(self) -> None:
        first = "https://a.example.test/one"
        opener = FakeOpener(routes={first: redirect("http://10.0.0.5/internal")})
        with self.assertRaises(sa.RemoteRedirectBlocked):
            sa.acquire_remote_source(
                first, "src_r", self.out, opener=opener, resolver=public_resolver
            )

    def test_redirect_to_metadata_endpoint_blocked(self) -> None:
        first = "https://a.example.test/one"
        opener = FakeOpener(
            routes={first: redirect("http://169.254.169.254/latest/meta-data/")}
        )
        with self.assertRaises(sa.RemoteRedirectBlocked):
            sa.acquire_remote_source(
                first, "src_r", self.out, opener=opener, resolver=public_resolver
            )

    def test_redirect_to_unsupported_scheme_blocked(self) -> None:
        first = "https://a.example.test/one"
        opener = FakeOpener(routes={first: redirect("file:///etc/passwd")})
        with self.assertRaises(sa.RemoteRedirectBlocked):
            sa.acquire_remote_source(
                first, "src_r", self.out, opener=opener, resolver=public_resolver
            )

    def test_redirect_introducing_credentials_blocked(self) -> None:
        first = "https://a.example.test/one"
        opener = FakeOpener(
            routes={first: redirect("https://user:secret@b.example.test/two")}
        )
        with self.assertRaises(sa.RemoteRedirectBlocked) as ctx:
            sa.acquire_remote_source(
                first, "src_r", self.out, opener=opener, resolver=public_resolver
            )
        self.assertNotIn("secret", str(ctx.exception))

    def test_redirect_limit_enforced(self) -> None:
        routes = {}
        for index in range(10):
            routes[f"https://h{index}.example.test/x"] = redirect(
                f"https://h{index + 1}.example.test/x"
            )
        opener = FakeOpener(routes=routes)
        with self.assertRaises(sa.RemoteTooManyRedirects) as ctx:
            sa.acquire_remote_source(
                "https://h0.example.test/x",
                "src_loop",
                self.out,
                opener=opener,
                resolver=public_resolver,
                max_redirects=3,
            )
        self.assertEqual(ctx.exception.error_code, sa.ERROR_REMOTE_TOO_MANY_REDIRECTS)
        self.assertEqual(len(opener.requested), 4)

    def test_redirect_loop_terminates(self) -> None:
        first = "https://a.example.test/one"
        opener = FakeOpener(routes={first: redirect(first)})
        with self.assertRaises(sa.RemoteTooManyRedirects):
            sa.acquire_remote_source(
                first, "src_loop", self.out, opener=opener, resolver=public_resolver
            )

    def test_relative_redirect_resolved_against_current_url(self) -> None:
        first = "https://a.example.test/dir/one"
        opener = FakeOpener(
            routes={
                first: redirect("../two"),
                "https://a.example.test/two": FakeResponse(
                    TXT_BODY, headers={"Content-Type": "text/plain"}
                ),
            }
        )
        result = sa.acquire_remote_source(
            first, "src_rel", self.out, opener=opener, resolver=public_resolver
        )
        self.assertEqual(result.final_url, "https://a.example.test/two")


# ---------------------------------------------------------------------------
# Response handling
# ---------------------------------------------------------------------------
class TestResponseHandling(AcquisitionTestCase):
    def test_small_download_succeeds(self) -> None:
        result = self.acquire()
        self.assertEqual(result.downloaded_bytes, len(TXT_BODY))
        self.assertEqual(result.source_digest, compute_source_digest(TXT_BODY))
        payload = Path(result.local_payload_path)
        self.assertTrue(payload.is_file())
        self.assertEqual(payload.read_bytes(), TXT_BODY)
        self.assertEqual(result.redirect_count, 0)
        self.assertEqual(result.content_type, "text/plain; charset=utf-8")

    def test_content_length_over_limit_rejected_before_download(self) -> None:
        opener = FakeOpener(
            routes={
                PUBLIC_URL: FakeResponse(
                    b"x" * 100,
                    headers={"Content-Length": "10000", "Content-Type": "text/plain"},
                )
            }
        )
        with self.assertRaises(sa.RemoteResponseTooLarge) as ctx:
            self.acquire(opener=opener, max_bytes=1000)
        self.assertEqual(ctx.exception.error_code, sa.ERROR_REMOTE_RESPONSE_TOO_LARGE)
        self.assertIn("Content-Length", str(ctx.exception))

    def test_streaming_body_over_limit_rejected(self) -> None:
        """The cap holds even when Content-Length lies."""
        opener = FakeOpener(
            routes={
                PUBLIC_URL: FakeResponse(
                    b"x" * 5000,
                    headers={"Content-Length": "10", "Content-Type": "text/plain"},
                    chunk_size=256,
                )
            }
        )
        with self.assertRaises(sa.RemoteResponseTooLarge) as ctx:
            self.acquire(opener=opener, max_bytes=1000)
        self.assertIn("streaming", str(ctx.exception))

    def test_missing_content_length_still_size_limited(self) -> None:
        opener = FakeOpener(
            routes={
                PUBLIC_URL: FakeResponse(
                    b"y" * 4096, headers={"Content-Type": "text/plain"}, chunk_size=512
                )
            }
        )
        with self.assertRaises(sa.RemoteResponseTooLarge):
            self.acquire(opener=opener, max_bytes=1024)

    def test_invalid_content_length_header_is_ignored(self) -> None:
        opener = FakeOpener(
            routes={
                PUBLIC_URL: FakeResponse(
                    TXT_BODY,
                    headers={"Content-Length": "not-a-number", "Content-Type": "text/plain"},
                )
            }
        )
        result = self.acquire(opener=opener)
        self.assertIsNone(result.declared_content_length)
        self.assertEqual(result.downloaded_bytes, len(TXT_BODY))

    def test_http_404_rejected(self) -> None:
        opener = FakeOpener(routes={PUBLIC_URL: http_error(404)})
        with self.assertRaises(sa.RemoteHttpError) as ctx:
            self.acquire(opener=opener)
        self.assertEqual(ctx.exception.error_code, sa.ERROR_REMOTE_HTTP_ERROR)
        self.assertEqual(ctx.exception.status, 404)

    def test_http_403_rejected(self) -> None:
        opener = FakeOpener(routes={PUBLIC_URL: http_error(403)})
        with self.assertRaises(sa.RemoteHttpError) as ctx:
            self.acquire(opener=opener)
        self.assertEqual(ctx.exception.status, 403)

    def test_http_500_rejected(self) -> None:
        opener = FakeOpener(routes={PUBLIC_URL: http_error(500)})
        with self.assertRaises(sa.RemoteHttpError) as ctx:
            self.acquire(opener=opener)
        self.assertEqual(ctx.exception.status, 500)

    def test_http_error_page_never_becomes_the_source(self) -> None:
        opener = FakeOpener(routes={PUBLIC_URL: http_error(404)})
        with self.assertRaises(sa.RemoteHttpError):
            self.acquire(opener=opener)
        self.assertEqual(list(self.out.iterdir()), [])

    def test_non_2xx_success_body_rejected(self) -> None:
        opener = FakeOpener(
            routes={PUBLIC_URL: FakeResponse(b"body", status=204, headers={})}
        )
        # 204 is a success code; a 199/3xx surfaced as a plain response is not.
        opener.routes[PUBLIC_URL] = FakeResponse(b"body", status=199, headers={})
        with self.assertRaises(sa.RemoteHttpError):
            self.acquire(opener=opener)

    def test_connection_timeout_handled(self) -> None:
        opener = FakeOpener(
            routes={PUBLIC_URL: urllib.error.URLError(socket.timeout("timed out"))}
        )
        with self.assertRaises(sa.RemoteTimeout) as ctx:
            self.acquire(opener=opener)
        self.assertEqual(ctx.exception.error_code, sa.ERROR_REMOTE_TIMEOUT)

    def test_read_timeout_handled_and_partial_removed(self) -> None:
        opener = FakeOpener(
            routes={
                PUBLIC_URL: FakeResponse(
                    b"z" * 4096,
                    headers={"Content-Type": "text/plain"},
                    chunk_size=256,
                    read_timeout_after=2,
                )
            }
        )
        with self.assertRaises(sa.RemoteTimeout):
            self.acquire(opener=opener)
        self.assertEqual(list(self.out.iterdir()), [])

    def test_unsupported_content_encoding_rejected(self) -> None:
        opener = FakeOpener(
            routes={
                PUBLIC_URL: FakeResponse(
                    b"\x1f\x8b compressed",
                    headers={"Content-Type": "text/plain", "Content-Encoding": "gzip"},
                )
            }
        )
        with self.assertRaises(sa.RemoteContentEncodingUnsupported) as ctx:
            self.acquire(opener=opener)
        self.assertEqual(
            ctx.exception.error_code, sa.ERROR_REMOTE_CONTENT_ENCODING_UNSUPPORTED
        )

    def test_identity_content_encoding_accepted(self) -> None:
        opener = FakeOpener(
            routes={
                PUBLIC_URL: FakeResponse(
                    TXT_BODY,
                    headers={"Content-Type": "text/plain", "Content-Encoding": "identity"},
                )
            }
        )
        self.assertEqual(self.acquire(opener=opener).downloaded_bytes, len(TXT_BODY))

    def test_identity_accept_encoding_requested(self) -> None:
        opener = FakeOpener(
            routes={PUBLIC_URL: FakeResponse(TXT_BODY, headers={"Content-Type": "text/plain"})}
        )
        captured: list[object] = []
        original = opener.open

        def spy(request, timeout=None):
            captured.append(request)
            return original(request, timeout=timeout)

        opener.open = spy  # type: ignore[assignment]
        self.acquire(opener=opener)
        self.assertEqual(captured[0].get_header("Accept-encoding"), "identity")
        self.assertEqual(captured[0].get_method(), "GET")

    def test_partial_file_removed_on_failure(self) -> None:
        opener = FakeOpener(
            routes={
                PUBLIC_URL: FakeResponse(
                    b"q" * 8192, headers={"Content-Type": "text/plain"}, chunk_size=512
                )
            }
        )
        with self.assertRaises(sa.RemoteResponseTooLarge):
            self.acquire(opener=opener, max_bytes=1024)
        leftovers = list(self.out.iterdir())
        self.assertEqual(leftovers, [], f"partial payload left behind: {leftovers}")

    def test_successful_write_leaves_no_partial_file(self) -> None:
        result = self.acquire()
        names = sorted(p.name for p in self.out.iterdir())
        self.assertEqual(names, [Path(result.local_payload_path).name])
        self.assertFalse(any(n.endswith(".part") for n in names))

    def test_bytes_are_stored_unmodified(self) -> None:
        body = b"line one\r\nline two\r\n\xef\xbb\xbftail"
        opener = FakeOpener(
            routes={PUBLIC_URL: FakeResponse(body, headers={"Content-Type": "text/plain"})}
        )
        result = self.acquire(opener=opener)
        self.assertEqual(Path(result.local_payload_path).read_bytes(), body)
        self.assertEqual(result.source_digest, compute_source_digest(body))


# ---------------------------------------------------------------------------
# Path safety
# ---------------------------------------------------------------------------
class TestPathSafety(AcquisitionTestCase):
    def test_content_disposition_traversal_ignored(self) -> None:
        opener = FakeOpener(
            routes={
                PUBLIC_URL: FakeResponse(
                    TXT_BODY,
                    headers={
                        "Content-Type": "text/plain",
                        "Content-Disposition": 'attachment; filename="../../../../etc/passwd"',
                    },
                )
            }
        )
        result = self.acquire(opener=opener)
        payload = Path(result.local_payload_path)
        self.assertEqual(payload.parent, self.out.resolve())
        self.assertEqual(payload.name, "src_remote.txt")
        self.assertNotIn("passwd", payload.name)
        # It may be recorded as metadata, but it never drives the path.
        self.assertIn("passwd", result.content_disposition or "")

    def test_url_basename_traversal_cannot_escape(self) -> None:
        url = "https://sources.example.test/a/../../../../etc/passwd"
        opener = FakeOpener(
            routes={url: FakeResponse(TXT_BODY, headers={"Content-Type": "text/plain"})}
        )
        result = sa.acquire_remote_source(
            url, "src_trav", self.out, opener=opener, resolver=public_resolver
        )
        payload = Path(result.local_payload_path)
        self.assertEqual(payload.parent, self.out.resolve())
        self.assertTrue(payload.name.startswith("src_trav"))

    def test_payload_never_escapes_output_dir(self) -> None:
        for source_id in ("src_..", "src_...", "src_a.b-c_d"):
            with tempfile.TemporaryDirectory() as d:
                out = Path(d)
                opener = FakeOpener(
                    routes={
                        PUBLIC_URL: FakeResponse(
                            TXT_BODY, headers={"Content-Type": "text/plain"}
                        )
                    }
                )
                result = sa.acquire_remote_source(
                    PUBLIC_URL, source_id, out, opener=opener, resolver=public_resolver
                )
                payload = Path(result.local_payload_path)
                self.assertEqual(payload.resolve().parent, out.resolve(), source_id)

    def test_invalid_source_id_rejected(self) -> None:
        for source_id in ("../evil", "evil", "src_/x", "", "src_ x"):
            with self.assertRaises(sa.RemoteUrlInvalid, msg=source_id):
                sa.acquire_remote_source(
                    PUBLIC_URL, source_id, self.out, opener=FakeOpener()
                )

    def test_safe_payload_name_uses_allowlisted_suffix(self) -> None:
        self.assertEqual(
            sa.safe_payload_name("src_a", url="https://h.test/x.pdf"), "src_a.pdf"
        )
        self.assertEqual(
            sa.safe_payload_name("src_a", url="https://h.test/x.exe"), "src_a.bin"
        )
        self.assertEqual(
            sa.safe_payload_name("src_a", content_type="application/pdf"), "src_a.pdf"
        )
        self.assertEqual(
            sa.safe_payload_name("src_a", url="https://h.test/x"), "src_a.bin"
        )

    def test_output_directory_is_created(self) -> None:
        nested = self.out / "deep" / "dir"
        opener = FakeOpener(
            routes={PUBLIC_URL: FakeResponse(TXT_BODY, headers={"Content-Type": "text/plain"})}
        )
        result = sa.acquire_remote_source(
            PUBLIC_URL, "src_nested", nested, opener=opener, resolver=public_resolver
        )
        self.assertEqual(Path(result.local_payload_path).parent, nested.resolve())


# ---------------------------------------------------------------------------
# Handoff into existing Phase 13 ingestion
# ---------------------------------------------------------------------------
class TestIngestionHandoff(AcquisitionTestCase):
    def _acquire_body(self, body: bytes, *, url: str, content_type: str, source_id: str):
        opener = FakeOpener(
            routes={url: FakeResponse(body, headers={"Content-Type": content_type})}
        )
        return sa.acquire_and_ingest(
            url, source_id, self.out, opener=opener, resolver=public_resolver
        )

    def test_remote_pdf_uses_existing_pdf_ingestion(self) -> None:
        body = build_text_pdf(["Remote Page One", "Remote Page Two"])
        acquisition, extraction = self._acquire_body(
            body,
            url="https://sources.example.test/doc.pdf",
            content_type="application/pdf",
            source_id="src_rpdf",
        )
        self.assertEqual(extraction.source_format, si.FORMAT_PDF)
        self.assertEqual(extraction.block_count, 2)
        self.assertEqual([b.locator["start"] for b in extraction.blocks], [1, 2])
        self.assertEqual(extraction.source_digest, acquisition.source_digest)

    def test_remote_markdown_uses_existing_markdown_ingestion(self) -> None:
        body = b"# Remote Heading\n\nBody text.\n\n## Nested\n\nMore.\n"
        _acq, extraction = self._acquire_body(
            body,
            url="https://sources.example.test/notes.md",
            content_type="text/markdown",
            source_id="src_rmd",
        )
        self.assertEqual(extraction.source_format, si.FORMAT_MARKDOWN)
        self.assertEqual(
            extraction.blocks[0].locator["heading_path"], ["Remote Heading"]
        )

    def test_remote_text_uses_existing_text_ingestion(self) -> None:
        _acq, extraction = self._acquire_body(
            TXT_BODY,
            url="https://sources.example.test/source.txt",
            content_type="text/plain",
            source_id="src_rtxt",
        )
        self.assertEqual(extraction.source_format, si.FORMAT_TEXT)
        self.assertIn("\u6cbb\u7406\u67b6\u69cb", extraction.blocks[0].text)

    def test_remote_docx_uses_existing_docx_ingestion(self) -> None:
        _acq, extraction = self._acquire_body(
            build_structured_docx(),
            url="https://sources.example.test/report.docx",
            content_type=(
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
            source_id="src_rdocx",
        )
        self.assertEqual(extraction.source_format, si.FORMAT_DOCX)
        self.assertEqual(extraction.block_count, 6)

    def test_remote_html_uses_existing_html_ingestion(self) -> None:
        body = (
            b"<!DOCTYPE html><html><head><title>T</title>"
            b"<script>var x=1;</script></head><body>"
            b"<h1>Remote</h1><p>Static only.</p>"
            b'<img src="https://example.invalid/i.png">'
            b'<iframe src="https://example.invalid/f"></iframe>'
            b"</body></html>"
        )
        _acq, extraction = self._acquire_body(
            body,
            url="https://sources.example.test/page.html",
            content_type="text/html; charset=utf-8",
            source_id="src_rhtml",
        )
        self.assertEqual(extraction.source_format, si.FORMAT_HTML)
        serialized = json.dumps(extraction.to_dict(), ensure_ascii=False)
        self.assertIn("Static only.", serialized)
        self.assertNotIn("var x=1", serialized)
        self.assertNotIn("example.invalid", serialized)

    def test_unsupported_remote_binary_uses_existing_error(self) -> None:
        opener = FakeOpener(
            routes={
                "https://sources.example.test/pic.png": FakeResponse(
                    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR",
                    headers={"Content-Type": "image/png"},
                )
            }
        )
        with self.assertRaises(si.SourceFormatUnsupported) as ctx:
            sa.acquire_and_ingest(
                "https://sources.example.test/pic.png",
                "src_rpng",
                self.out,
                opener=opener,
                resolver=public_resolver,
            )
        self.assertEqual(ctx.exception.error_code, si.ERROR_SOURCE_FORMAT_UNSUPPORTED)

    def test_content_type_is_advisory_not_format_authority(self) -> None:
        """An HTML body mislabelled as PDF must not be treated as a PDF."""
        body = b"<!DOCTYPE html><html><body><h1>Not a PDF</h1><p>Text.</p></body></html>"
        opener = FakeOpener(
            routes={
                "https://sources.example.test/wrong": FakeResponse(
                    body, headers={"Content-Type": "application/pdf"}
                )
            }
        )
        acquisition, extraction = sa.acquire_and_ingest(
            "https://sources.example.test/wrong",
            "src_wrong",
            self.out,
            opener=opener,
            resolver=public_resolver,
        )
        self.assertEqual(acquisition.content_type, "application/pdf")
        self.assertEqual(extraction.source_format, si.FORMAT_HTML)

    def test_acquisition_digest_matches_ingestion_digest(self) -> None:
        acquisition, extraction = self._acquire_body(
            TXT_BODY,
            url="https://sources.example.test/source.txt",
            content_type="text/plain",
            source_id="src_dig",
        )
        self.assertEqual(acquisition.source_digest, extraction.source_digest)
        self.assertEqual(
            acquisition.source_digest, compute_source_digest(TXT_BODY)
        )

    def test_retrieval_time_does_not_affect_identity(self) -> None:
        """retrieved_at is audit metadata only."""
        first_acq, first_ext = self._acquire_body(
            TXT_BODY,
            url="https://sources.example.test/source.txt",
            content_type="text/plain",
            source_id="src_time",
        )
        second_acq, second_ext = self._acquire_body(
            TXT_BODY,
            url="https://sources.example.test/source.txt",
            content_type="text/plain",
            source_id="src_time",
        )
        self.assertEqual(first_acq.source_digest, second_acq.source_digest)
        self.assertEqual(
            [b.block_id for b in first_ext.blocks], [b.block_id for b in second_ext.blocks]
        )

    def test_no_phase12_artifact_written_by_acquisition(self) -> None:
        self.acquire()
        for artifact in (
            "source_inventory.json",
            "claim_traceability.json",
            "source_coverage.json",
            "source_grounded_qa.json",
        ):
            self.assertFalse((self.out / artifact).exists(), artifact)

    def test_acquisition_assigns_no_priority(self) -> None:
        result = self.acquire()
        serialized = json.dumps(result.to_dict(), ensure_ascii=False)
        for word in ("HIGH", "MEDIUM", "LOW"):
            self.assertNotIn(word, serialized)


# ---------------------------------------------------------------------------
# Transport configuration
# ---------------------------------------------------------------------------
class TestTransportConfiguration(AcquisitionTestCase):
    def test_opener_installs_no_local_or_proxy_handlers(self) -> None:
        """file:, ftp:, data: and ambient proxies must be unreachable."""
        opener = sa.build_opener()
        names = {type(h).__name__ for h in opener.handlers}
        for banned in ("FileHandler", "FTPHandler", "DataHandler", "ProxyHandler"):
            self.assertNotIn(banned, names, banned)
        self.assertIn("HTTPHandler", names)
        self.assertIn("HTTPSHandler", names)
        # No scheme-open method exists for the dangerous schemes.
        for scheme in ("file", "ftp", "data"):
            self.assertNotIn(scheme, opener.handle_open, scheme)

    def test_opener_supports_only_http_schemes(self) -> None:
        opener = sa.build_opener()
        self.assertEqual(
            {s for s in opener.handle_open if s in ("http", "https", "file", "ftp", "data")},
            {"http", "https"},
        )

    def test_opener_disables_automatic_redirects(self) -> None:
        opener = sa.build_opener()
        handler = next(
            h for h in opener.handlers if isinstance(h, sa._NoRedirectHandler)
        )
        self.assertIsNone(
            handler.redirect_request(None, None, 302, "Found", None, "https://x.test/")
        )

    def test_no_tls_verification_bypass_in_module(self) -> None:
        source = (SCRIPTS_DIR / "source_acquisition.py").read_text(encoding="utf-8")
        for banned in (
            "_create_unverified_context",
            "CERT_NONE",
            "verify=False",
            "check_hostname = False",
        ):
            self.assertNotIn(banned, source, banned)

    def test_no_ambient_credential_sources_used(self) -> None:
        source = (SCRIPTS_DIR / "source_acquisition.py").read_text(encoding="utf-8")
        for banned in ("netrc", "HTTPBasicAuth", "Cookie", "Authorization"):
            self.assertNotIn(banned, source, banned)

    def test_cli_exposes_no_auth_or_insecure_options(self) -> None:
        import acquire_source as cli

        options = {
            option
            for action in cli.build_parser()._actions
            for option in action.option_strings
        }
        for banned in (
            "--header",
            "--cookie",
            "--user",
            "--token",
            "--insecure",
            "--auth",
            "--netrc",
        ):
            self.assertNotIn(banned, options, banned)
        self.assertIn("--url", options)
        self.assertIn("--source-id", options)
        self.assertIn("--output-dir", options)


if __name__ == "__main__":
    unittest.main(verbosity=2)
