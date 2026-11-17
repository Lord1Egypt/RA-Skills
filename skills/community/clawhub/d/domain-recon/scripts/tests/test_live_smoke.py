"""Opt-in LIVE smoke tests — hit real endpoints to catch upstream schema drift.

These are SKIPPED unless RECON_LIVE=1 is set in the environment. They are never
part of the blocking gate. Keep them lightweight and courteous (one request per
source, generic public resources only).

    RECON_LIVE=1 pytest tests/test_live_smoke.py -v
"""
import os
import time

import pytest

import recon

pytestmark = pytest.mark.skipif(
    os.environ.get("RECON_LIVE") != "1",
    reason="live smoke tests are opt-in; set RECON_LIVE=1 to run",
)


def _pause():
    # Be polite to ip-api's 45 req/min and everyone else.
    time.sleep(1.5)


def live(fn):
    """Run a live check, but treat *transient upstream outages* as a skip.

    The purpose of the smoke suite is to catch upstream SCHEMA DRIFT, not to
    monitor uptime. A 5xx / 429 / network blip (crt.sh in particular is
    famously flaky) is skipped; a ParseError (the schema changed) or a 4xx
    still fails loudly, because that means our parser needs updating.
    """
    try:
        fn()
    except (recon.RateLimitError, recon.HTTPStatusError, recon.NetworkError) as e:
        status = getattr(e, "status", None)
        if isinstance(e, recon.HTTPStatusError) and status is not None and 400 <= status < 500:
            raise  # a real client-side / contract problem — do not hide it
        pytest.skip("transient upstream issue: {}".format(e))
    finally:
        _pause()


def test_live_dns():
    def check():
        res = recon.fetch_dns("example.com", "A")
        assert res["status_text"] == "NOERROR"
        assert res["answer_count"] >= 1

    live(check)


def test_live_certs():
    def check():
        res = recon.fetch_certs("example.com")
        assert res["source"] == "ct"
        # at least one CT source (crt.sh or certSpotter) must have answered
        assert res["sources_used"]
        assert res["cert_count"] >= 0

    live(check)


def test_live_rdap_io():
    # .io is absent from the IANA bootstrap AND rdap.org 404s it — the curated
    # supplement is what actually resolves it. This is the exact reported case.
    def check():
        recon._RDAP_BOOTSTRAP_CACHE.clear()
        res = recon.fetch_rdap("github.io")
        assert res["kind"] == "domain"
        assert res["ldhName"]
        # supplement is the expected winner; accept authoritative variants too.
        assert res["rdap_source"] in ("supplement", "iana-bootstrap")

    live(check)


def test_live_rdap_ai_bootstrap():
    # .ai IS in the IANA bootstrap -> exercises the bootstrap (not supplement) path.
    def check():
        recon._RDAP_BOOTSTRAP_CACHE.clear()
        res = recon.fetch_rdap("nic.ai")
        assert res["kind"] == "domain"
        assert res["ldhName"]

    live(check)


def test_live_rdap_domain():
    def check():
        res = recon.fetch_rdap("example.com")
        assert res["kind"] == "domain"
        assert res["ldhName"]

    live(check)


def test_live_ip():
    def check():
        res = recon.fetch_ip("8.8.8.8")
        assert res["ip"] == "8.8.8.8"
        assert res["country_code"]

    live(check)


def test_live_asn():
    def check():
        res = recon.fetch_asn("AS15169")
        assert res["holder"]
        assert res["prefix_count"] >= 1

    live(check)


def test_live_wayback():
    def check():
        res = recon.fetch_wayback("example.com")
        assert "archived" in res
        # CDX section is best-effort (archive.org is flaky); when present and not
        # degraded, it must carry the capture-history shape we parse.
        cdx = res.get("cdx") or {}
        if cdx and "error" not in cdx:
            assert "first_capture" in cdx and "recent" in cdx

    live(check)


def test_live_dns_ptr():
    def check():
        res = recon.fetch_dns("8.8.8.8", "PTR")
        assert res["query_type"] == "PTR"
        # 8.8.8.8 reliably has a PTR record (dns.google)
        assert res["answer_count"] >= 1

    live(check)


def test_live_profile():
    # The orchestrator end-to-end against a stable target. Fault-isolated by
    # design, so we assert the envelope rather than any single upstream's data.
    def check():
        rep = recon.run_profile("example.com", resolve_limit=2, ip_limit=3)
        assert rep["source"] == "profile"
        assert rep["target"] == "example.com"
        assert "hosts" in rep and "apex" in rep and "errors" in rep

    live(check)
