"""Offline, deterministic tests for the domain-recon helper.

These NEVER hit the network. Every source is exercised against the captured
fixtures in tests/fixtures/, with the HTTP layer either patched at the
`http_get_json` seam (parse/normalize behavior) or at the lower `_open` seam
(retry / backoff / failure-mode behavior).
"""
import email.message
import io
import socket
import ssl
import urllib.error

import pytest

import recon
from conftest import load_fixture, load_fixture_text


# ---------------------------------------------------------------------------
# Test doubles for the HTTP layer
# ---------------------------------------------------------------------------


class FakeResp:
    """Minimal stand-in for an http.client.HTTPResponse."""

    def __init__(self, body, content_type="application/json; charset=utf-8"):
        self._body = body if isinstance(body, bytes) else body.encode("utf-8")
        self.headers = email.message.Message()
        self.headers["Content-Type"] = content_type

    def read(self):
        return self._body


def make_http_error(code, retry_after=None, body=b""):
    hdrs = email.message.Message()
    if retry_after is not None:
        hdrs["Retry-After"] = str(retry_after)
    return urllib.error.HTTPError("http://x", code, "err", hdrs, io.BytesIO(body))


@pytest.fixture(autouse=True)
def _no_sleep(monkeypatch):
    """Never actually sleep during retry/backoff tests."""
    monkeypatch.setattr(recon, "_sleep", lambda *_a, **_k: None)


def patch_json(monkeypatch, mapping_or_value):
    """Patch http_get_json. If given a dict, dispatch by substring in the URL."""

    def fake(url, headers=None, timeout=15.0, retries=3):
        if isinstance(mapping_or_value, dict) and not _looks_like_payload(mapping_or_value):
            for key, val in mapping_or_value.items():
                if key in url:
                    return val
            raise AssertionError("no fixture mapped for URL: {}".format(url))
        return mapping_or_value

    monkeypatch.setattr(recon, "http_get_json", fake)


def _looks_like_payload(d):
    # A RIPEstat/RDAP payload dict has these hallmark keys; a URL->fixture
    # dispatch map won't.
    return any(k in d for k in ("data", "objectClassName", "Status", "archived_snapshots", "status"))


# ---------------------------------------------------------------------------
# Input validation / normalization
# ---------------------------------------------------------------------------


class TestNormalize:
    def test_domain_lowercases_and_strips_trailing_dot(self):
        assert recon.normalize_domain("Example.COM.") == "example.com"

    def test_domain_idn_punycode(self):
        # bücher.example -> xn--bcher-kva.example
        assert recon.normalize_domain("bücher.example") == "xn--bcher-kva.example"

    def test_domain_already_punycode_passthrough(self):
        assert recon.normalize_domain("xn--bcher-kva.example") == "xn--bcher-kva.example"

    @pytest.mark.parametrize("bad", ["", "   ", "localhost", "no spaces.com com", "a/b.com", "..com"])
    def test_domain_rejects_junk(self, bad):
        with pytest.raises(recon.InputError):
            recon.normalize_domain(bad)

    def test_ip_v4_roundtrip(self):
        assert recon.normalize_ip("8.8.8.8") == "8.8.8.8"

    def test_ip_v6_canonicalized(self):
        assert recon.normalize_ip("2606:4700:10::6814:179A") == "2606:4700:10::6814:179a"

    def test_ip_rejects_bad(self):
        with pytest.raises(recon.InputError):
            recon.normalize_ip("999.1.1.1")

    @pytest.mark.parametrize("val,expected", [("AS15169", 15169), ("as15169", 15169), ("15169", 15169)])
    def test_asn_forms(self, val, expected):
        assert recon.normalize_asn(val) == expected

    def test_asn_rejects_bad(self):
        with pytest.raises(recon.InputError):
            recon.normalize_asn("AS-bogus")

    @pytest.mark.parametrize(
        "val,kind",
        [("8.8.8.8", "ip"), ("2606:4700:10::1", "ip"), ("AS15169", "asn"), ("15169", "asn"), ("example.com", "domain")],
    )
    def test_classify_resource(self, val, kind):
        assert recon.classify_resource(val) == kind


# ---------------------------------------------------------------------------
# crt.sh
# ---------------------------------------------------------------------------


class TestCerts:
    def test_parse_dedup_and_sorted(self):
        entries = load_fixture("crtsh_example.json")
        res = recon.parse_certs(entries, "example.com")
        assert res["source"] == "crt.sh"
        # subdomains are unique and sorted despite duplicate name_value rows.
        assert res["subdomains"] == sorted(set(res["subdomains"]))
        assert res["subdomain_count"] == len(res["subdomains"])
        assert "example.com" in res["subdomains"]
        assert res["cert_count"] == len(entries)

    def test_wildcard_included_by_default(self):
        entries = load_fixture("crtsh_example.json")
        res = recon.parse_certs(entries, "example.com", include_wildcards=True)
        assert any(s.startswith("*.") for s in res["subdomains"])

    def test_wildcard_excluded_when_asked(self):
        entries = load_fixture("crtsh_example.json")
        res = recon.parse_certs(entries, "example.com", include_wildcards=False)
        assert all(not s.startswith("*.") for s in res["subdomains"])

    def test_wildcard_synthetic_entry(self):
        entries = [{"name_value": "*.sub.example.com\nsub.example.com", "common_name": "*.sub.example.com"}]
        res = recon.parse_certs(entries, "example.com")
        assert "*.sub.example.com" in res["subdomains"]
        assert "sub.example.com" in res["subdomains"]

    def test_excludes_out_of_scope_names(self):
        entries = [{"name_value": "a.example.com\nevil.attacker.test", "common_name": "a.example.com"}]
        res = recon.parse_certs(entries, "example.com")
        assert "a.example.com" in res["subdomains"]
        assert "evil.attacker.test" not in res["subdomains"]

    def test_empty_result(self):
        res = recon.parse_certs([], "example.com")
        assert res["subdomain_count"] == 0
        assert res["cert_count"] == 0

    def test_limit_caps_subdomains_but_keeps_full_count(self):
        entries = load_fixture("crtsh_example.json")
        full = recon.parse_certs(entries, "example.com")
        assert full["subdomain_count"] >= 2  # fixture has multiple unique names
        capped = recon.parse_certs(entries, "example.com", limit=1)
        assert len(capped["subdomains"]) == 1
        assert capped["subdomain_count"] == full["subdomain_count"]  # true total preserved
        assert capped["subdomains_truncated"] is True
        # the returned set is the first N of the sorted full set (deterministic)
        assert capped["subdomains"] == full["subdomains"][:1]

    def test_no_limit_not_truncated(self):
        entries = load_fixture("crtsh_example.json")
        res = recon.parse_certs(entries, "example.com")
        assert res["subdomains_truncated"] is False
        assert res["certs_truncated"] is False
        assert res["target"] == "example.com"

    def test_max_certs_caps_history(self):
        entries = load_fixture("crtsh_example.json")
        res = recon.parse_certs(entries, "example.com", max_certs=3)
        assert len(res["certs"]) == 3
        assert res["cert_count"] == len(entries)  # full count preserved
        assert res["certs_truncated"] is True

    def test_none_result(self):
        res = recon.parse_certs(None, "example.com")
        assert res["subdomains"] == []

    def test_parse_rejects_non_list(self):
        with pytest.raises(recon.ParseError):
            recon.parse_certs({"not": "a list"}, "example.com")

    def test_fetch_empty_body_is_empty_result(self, monkeypatch):
        # crt.sh returns an empty body for zero results -> must not blow up.
        monkeypatch.setattr(recon, "http_get", lambda *a, **k: "")
        res = recon.fetch_certs("example.com")
        assert res["subdomain_count"] == 0

    def test_fetch_end_to_end(self, monkeypatch):
        text = load_fixture_text("crtsh_example.json")
        monkeypatch.setattr(recon, "http_get", lambda *a, **k: text)
        res = recon.fetch_certs("example.com")
        assert res["cert_count"] == 12


# ---------------------------------------------------------------------------
# RDAP
# ---------------------------------------------------------------------------


class TestRdap:
    def test_domain_parse(self):
        obj = load_fixture("rdap_domain_example.json")
        res = recon.parse_rdap(obj, "domain")
        assert res["ldhName"] == "EXAMPLE.COM"
        assert res["nameservers"] == sorted(res["nameservers"])
        assert "registration" in res["events"]
        assert isinstance(res["status"], list)

    def test_ip_parse(self):
        obj = load_fixture("rdap_ip_8888.json")
        res = recon.parse_rdap(obj, "ip")
        assert res["startAddress"] == "8.8.8.0"
        assert res["endAddress"] == "8.8.8.255"

    def test_asn_parse(self):
        obj = load_fixture("rdap_asn_15169.json")
        res = recon.parse_rdap(obj, "asn")
        assert res["startAutnum"] == 15169

    def test_parse_rejects_non_dict(self):
        with pytest.raises(recon.ParseError):
            recon.parse_rdap([1, 2, 3], "domain")

    def test_fetch_autodetects_ip(self, monkeypatch):
        obj = load_fixture("rdap_ip_8888.json")
        captured = {}

        def fake(url, headers=None, timeout=15.0, retries=3):
            captured["url"] = url
            return obj

        monkeypatch.setattr(recon, "http_get_json", fake)
        res = recon.fetch_rdap("8.8.8.8")
        assert "/ip/" in captured["url"]
        assert res["kind"] == "ip"

    def test_rdap_requests_send_rdap_accept_header(self, monkeypatch):
        # RFC 7480: RDAP servers serve application/rdap+json; some (nic.cat/.aco)
        # reject a plain application/json Accept with HTTP 406. The RDAP path must
        # ask for the rdap+json media type.
        captured = {}

        def fake(url, headers=None, timeout=15.0, retries=3):
            captured["headers"] = headers or {}
            return load_fixture("rdap_ip_8888.json")

        monkeypatch.setattr(recon, "http_get_json", fake)
        recon.fetch_rdap("8.8.8.8")
        assert "rdap+json" in captured["headers"].get("Accept", "")

    def test_fetch_autodetects_asn(self, monkeypatch):
        obj = load_fixture("rdap_asn_15169.json")
        captured = {}

        def fake(url, headers=None, timeout=15.0, retries=3):
            captured["url"] = url
            return obj

        monkeypatch.setattr(recon, "http_get_json", fake)
        res = recon.fetch_rdap("AS15169")
        assert "/autnum/15169" in captured["url"]
        assert res["kind"] == "asn"


# ---------------------------------------------------------------------------
# DNS-over-HTTPS
# ---------------------------------------------------------------------------


class TestDns:
    def test_parse_a(self):
        res = recon.parse_dns(load_fixture("dns_google_a.json"), "example.com", "A")
        assert res["status_text"] == "NOERROR"
        assert res["answer_count"] == 2
        assert all(a["type"] == "A" for a in res["answers"])

    def test_parse_aaaa_cloudflare(self):
        res = recon.parse_dns(load_fixture("dns_cloudflare_aaaa.json"), "example.com", "AAAA")
        assert res["answer_count"] == 2
        assert all(":" in a["data"] for a in res["answers"])

    def test_parse_mx(self):
        res = recon.parse_dns(load_fixture("dns_google_mx.json"), "example.com", "MX")
        assert res["answers"][0]["type"] == "MX"

    def test_parse_txt(self):
        res = recon.parse_dns(load_fixture("dns_google_txt.json"), "example.com", "TXT")
        assert res["answer_count"] >= 1

    def test_nxdomain_status(self):
        res = recon.parse_dns({"Status": 3, "Answer": []}, "nope.example", "A")
        assert res["status_text"] == "NXDOMAIN"
        assert res["answer_count"] == 0

    def test_unsupported_type_rejected(self):
        with pytest.raises(recon.InputError):
            recon.fetch_dns("example.com", "SRV")

    def test_ptr_supported_for_hostname(self, monkeypatch):
        captured = {}

        def fake(url, headers=None, timeout=15.0, retries=3):
            captured["url"] = url
            return {"Status": 0, "Answer": [{"name": "x", "type": 12, "TTL": 1, "data": "host.example."}]}

        monkeypatch.setattr(recon, "http_get_json", fake)
        res = recon.fetch_dns("8.8.8.8", "PTR")
        # A bare IP builds the reverse in-addr.arpa pointer name.
        assert "8.8.8.8.in-addr.arpa" in captured["url"]
        assert res["query_type"] == "PTR"
        assert res["answers"][0]["type"] == "PTR"

    def test_ip_target_implies_ptr(self, monkeypatch):
        captured = {}

        def fake(url, headers=None, timeout=15.0, retries=3):
            captured["url"] = url
            return {"Status": 0, "Answer": []}

        monkeypatch.setattr(recon, "http_get_json", fake)
        # Asking for the default "A" of an IP literal is coerced to a PTR lookup.
        res = recon.fetch_dns("8.8.8.8")
        assert res["query_type"] == "PTR"
        assert "in-addr.arpa" in captured["url"]

    def test_ptr_ipv6_reverse_pointer(self, monkeypatch):
        captured = {}

        def fake(url, headers=None, timeout=15.0, retries=3):
            captured["url"] = url
            return {"Status": 0, "Answer": []}

        monkeypatch.setattr(recon, "http_get_json", fake)
        recon.fetch_dns("2606:4700:4700::1111", "PTR")
        assert "ip6.arpa" in captured["url"]

    def test_unknown_provider_rejected(self):
        with pytest.raises(recon.InputError):
            recon.fetch_dns("example.com", "A", provider="nope")

    def test_fetch_many(self, monkeypatch):
        mapping = {
            "type=A": load_fixture("dns_google_a.json"),
            "type=MX": load_fixture("dns_google_mx.json"),
        }

        def fake(url, headers=None, timeout=15.0, retries=3):
            for k, v in mapping.items():
                if k in url:
                    return v
            raise AssertionError(url)

        monkeypatch.setattr(recon, "http_get_json", fake)
        res = recon.fetch_dns_many("example.com", ["A", "MX"])
        assert set(res["records"]) == {"A", "MX"}


# ---------------------------------------------------------------------------
# ip-api.com
# ---------------------------------------------------------------------------


class TestIp:
    def test_parse_success(self):
        res = recon.parse_ip(load_fixture("ipapi_8888.json"))
        assert res["ip"] == "8.8.8.8"
        assert res["country_code"] == "US"
        assert res["as"].startswith("AS15169")

    def test_parse_failure_raises(self):
        with pytest.raises(recon.ReconError):
            recon.parse_ip({"status": "fail", "message": "reserved range", "query": "127.0.0.1"})

    def test_fetch_end_to_end(self, monkeypatch):
        patch_json(monkeypatch, load_fixture("ipapi_8888.json"))
        res = recon.fetch_ip("8.8.8.8")
        assert res["isp"] == "Google LLC"

    def test_fetch_rejects_bad_ip(self):
        with pytest.raises(recon.InputError):
            recon.fetch_ip("not-an-ip")


# ---------------------------------------------------------------------------
# RIPEstat (ASN / prefix / IP ownership)
# ---------------------------------------------------------------------------


class TestAsn:
    def test_parse_overview_with_prefixes(self):
        ov = load_fixture("ripestat_as_overview_15169.json")
        pf = load_fixture("ripestat_announced_prefixes_15169.json")
        res = recon.parse_asn_overview(ov, announced_prefixes=pf)
        assert res["holder"].startswith("GOOGLE")
        assert res["prefix_count"] == 5
        assert all("/" in p for p in res["prefixes"])

    def test_parse_overview_without_prefixes(self):
        ov = load_fixture("ripestat_as_overview_15169.json")
        res = recon.parse_asn_overview(ov)
        assert "prefixes" not in res

    def test_parse_network_info(self):
        res = recon.parse_network_info(load_fixture("ripestat_network_info_8888.json"))
        assert res["prefix"] == "8.8.8.0/24"
        assert "15169" in res["asns"]

    def test_parse_missing_data_raises(self):
        with pytest.raises(recon.ParseError):
            recon.parse_asn_overview({"no": "data"})

    def test_fetch_ip_uses_network_info(self, monkeypatch):
        captured = {}

        def fake(url, headers=None, timeout=15.0, retries=3):
            captured["url"] = url
            return load_fixture("ripestat_network_info_8888.json")

        monkeypatch.setattr(recon, "http_get_json", fake)
        res = recon.fetch_asn("8.8.8.8")
        assert "network-info" in captured["url"]
        assert res["kind"] == "ip"

    def test_fetch_asn_uses_overview_and_prefixes(self, monkeypatch):
        urls = []

        def fake(url, headers=None, timeout=15.0, retries=3):
            urls.append(url)
            if "as-overview" in url:
                return load_fixture("ripestat_as_overview_15169.json")
            if "announced-prefixes" in url:
                return load_fixture("ripestat_announced_prefixes_15169.json")
            raise AssertionError(url)

        monkeypatch.setattr(recon, "http_get_json", fake)
        res = recon.fetch_asn("AS15169")
        assert res["kind"] == "asn"
        assert res["prefix_count"] == 5
        assert any("as-overview" in u for u in urls)
        assert any("announced-prefixes" in u for u in urls)


# ---------------------------------------------------------------------------
# Wayback (bonus)
# ---------------------------------------------------------------------------


class TestWayback:
    def test_parse_available(self):
        res = recon.parse_wayback(load_fixture("wayback_example.json"), "example.com")
        assert res["archived"] is True
        assert res["snapshot_url"].startswith("http")
        assert res["target"] == "example.com"

    def test_parse_absent(self):
        res = recon.parse_wayback({"url": "x", "archived_snapshots": {}}, "x")
        assert res["archived"] is False

    def test_fetch_rejects_bad_url(self):
        with pytest.raises(recon.InputError):
            recon.fetch_wayback("has a space")

    # --- CDX capture history ---

    def test_parse_cdx_rows(self):
        rows = load_fixture("wayback_cdx_recent_example.json")
        caps = recon.parse_cdx(rows)
        assert len(caps) == len(rows) - 1  # header dropped
        assert all(c["timestamp"] for c in caps)
        assert all(c["snapshot_url"].startswith("http://web.archive.org/web/") for c in caps)
        # header maps columns correctly regardless of position
        assert caps[0]["statuscode"] == "200"

    def test_parse_cdx_empty_and_header_only(self):
        assert recon.parse_cdx([]) == []
        assert recon.parse_cdx([["timestamp", "original"]]) == []
        assert recon.parse_cdx(None) == []

    def test_parse_cdx_rejects_non_list(self):
        with pytest.raises(recon.ParseError):
            recon.parse_cdx({"not": "rows"})

    def _cdx_dispatch(self, monkeypatch):
        first = load_fixture_text("wayback_cdx_first_example.json")
        recent = load_fixture_text("wayback_cdx_recent_example.json")

        def fake_http_get(url, headers=None, timeout=15.0, retries=3):
            if "collapse" in url:
                return recent  # stand-in for the month-collapse scan
            if "limit=-" in url:
                return recent
            if "limit=1" in url:
                return first
            raise AssertionError("unexpected cdx url: {}".format(url))

        monkeypatch.setattr(recon, "http_get", fake_http_get)

    def test_fetch_cdx_first_last_recent(self, monkeypatch):
        self._cdx_dispatch(monkeypatch)
        cdx = recon.fetch_cdx("example.com", cdx_limit=5)
        assert cdx["first_capture"]["timestamp"] == "20020120142510"
        # recent fixture is ascending; newest (last) is the final row
        assert cdx["last_capture"]["timestamp"] == "20020810100026"
        assert cdx["recent_count"] == 3
        # presented newest-first
        assert cdx["recent"][0]["timestamp"] == "20020810100026"
        assert "active_months" not in cdx  # count is opt-in

    def test_fetch_cdx_count_optin(self, monkeypatch):
        self._cdx_dispatch(monkeypatch)
        cdx = recon.fetch_cdx("example.com", cdx_limit=5, count=True)
        assert cdx["active_months"] == 3

    def test_fetch_cdx_degrades_gracefully(self, monkeypatch):
        def boom(url, headers=None, timeout=15.0, retries=3):
            raise recon.NetworkError("cdx down")

        monkeypatch.setattr(recon, "http_get", boom)
        cdx = recon.fetch_cdx("example.com")
        assert "error" in cdx  # captured, not raised

    def test_fetch_wayback_includes_cdx(self, monkeypatch):
        monkeypatch.setattr(recon, "http_get_json", lambda *a, **k: load_fixture("wayback_example.json"))
        self._cdx_dispatch(monkeypatch)
        res = recon.fetch_wayback("example.com", cdx=True, cdx_limit=5)
        assert res["archived"] is True
        assert res["cdx"]["first_capture"]["timestamp"] == "20020120142510"

    def test_fetch_wayback_no_cdx(self, monkeypatch):
        monkeypatch.setattr(recon, "http_get_json", lambda *a, **k: load_fixture("wayback_example.json"))
        res = recon.fetch_wayback("example.com", cdx=False)
        assert "cdx" not in res


# ---------------------------------------------------------------------------
# profile orchestrator  (patched at the fetch_* seams)
# ---------------------------------------------------------------------------


def _dns_many(ip="93.184.216.34"):
    return {
        "source": "doh",
        "name": "example.com",
        "provider": "google",
        "records": {
            "A": {"answers": [{"type": "A", "data": ip, "ttl": 300}], "answer_count": 1},
            "AAAA": {"answers": [], "answer_count": 0},
            "MX": {"answers": [{"type": "MX", "data": "0 mail.example.com.", "ttl": 300}], "answer_count": 1},
            "TXT": {"answers": [], "answer_count": 0},
            "NS": {"answers": [{"type": "NS", "data": "a.iana-servers.net.", "ttl": 300}], "answer_count": 1},
            "CAA": {"answers": [], "answer_count": 0},
        },
    }


def _install_profile_fakes(monkeypatch, resolve_map, certs_subs=None, ip_fail=None):
    certs_subs = certs_subs if certs_subs is not None else ["www.example.com", "api.example.com", "mail.example.com"]

    monkeypatch.setattr(
        recon, "fetch_certs",
        lambda *a, **k: {"source": "crt.sh", "target": "example.com", "subdomains": certs_subs,
                         "subdomain_count": len(certs_subs), "subdomains_truncated": False},
    )
    monkeypatch.setattr(
        recon, "fetch_rdap",
        lambda *a, **k: {"source": "rdap.org", "kind": "domain",
                         "events": {"registration": "2020-01-01"}, "nameservers": ["a.iana-servers.net"]},
    )
    monkeypatch.setattr(recon, "fetch_dns_many", lambda *a, **k: _dns_many())

    def fake_dns(name, rrtype, provider="google", timeout=20.0, retries=3):
        addr = resolve_map.get(name, {}).get(rrtype, [])
        return {"answers": [{"type": rrtype, "data": d, "ttl": 300} for d in addr]}

    monkeypatch.setattr(recon, "fetch_dns", fake_dns)

    def fake_ip(ip, timeout=20.0, retries=3):
        if ip_fail and ip == ip_fail:
            raise recon.RateLimitError("ip-api throttled")
        return {"source": "ip-api.com", "ip": ip, "as": "AS15133 Edgecast", "country": "US", "city": "LA"}

    monkeypatch.setattr(recon, "fetch_ip", fake_ip)
    monkeypatch.setattr(
        recon, "fetch_asn",
        lambda ip, **k: {"source": "ripestat", "kind": "ip", "prefix": "93.184.216.0/24", "asns": ["15133"]},
    )
    monkeypatch.setattr(
        recon, "fetch_wayback",
        lambda t, **k: {"source": "wayback", "url": t, "archived": True, "cdx": {"first_capture": {"timestamp": "2002"}}},
    )


class TestProfile:
    def test_happy_path_wiring_and_dedup(self, monkeypatch):
        # www shares the apex IP; api and mail share another -> 2 unique hosts.
        resolve_map = {
            "www.example.com": {"A": ["93.184.216.34"], "AAAA": []},
            "api.example.com": {"A": ["1.2.3.4"], "AAAA": []},
            "mail.example.com": {"A": ["1.2.3.4"], "AAAA": []},
        }
        _install_profile_fakes(monkeypatch, resolve_map)
        rep = recon.run_profile("example.com")
        assert rep["source"] == "profile"
        assert rep["target"] == "example.com"
        assert rep["apex"]["rdap"]["kind"] == "domain"
        assert set(rep["apex"]["dns"]["records"]) == {"A", "AAAA", "MX", "TXT", "NS", "CAA"}
        assert rep["subdomains"]["count"] == 3
        # unique IPs only: apex 93.184.216.34 (+www dup) and 1.2.3.4 (api+mail dup)
        assert set(rep["hosts"]) == {"93.184.216.34", "1.2.3.4"}
        assert rep["hosts"]["1.2.3.4"]["asn"]["asns"] == ["15133"]
        assert rep["errors"] == []
        assert len(rep["wayback"]) >= 1

    def test_fault_isolation_certs_down(self, monkeypatch):
        _install_profile_fakes(monkeypatch, {})
        monkeypatch.setattr(recon, "fetch_certs", lambda *a, **k: (_ for _ in ()).throw(recon.NetworkError("crt.sh 503")))
        rep = recon.run_profile("example.com")
        steps = [e["step"] for e in rep["errors"]]
        assert "certs" in steps
        # profile still produced the rest of the report
        assert rep["apex"]["rdap"] is not None
        assert rep["apex"]["dns"] is not None

    def test_single_source_failure_recorded_not_raised(self, monkeypatch):
        resolve_map = {"www.example.com": {"A": ["9.9.9.9"], "AAAA": []}}
        _install_profile_fakes(monkeypatch, resolve_map, ip_fail="9.9.9.9")
        rep = recon.run_profile("example.com")
        # the failed ip-api call for 9.9.9.9 is recorded, others still enriched
        assert any(e["step"] == "ip:9.9.9.9" for e in rep["errors"])
        assert "93.184.216.34" in rep["hosts"]

    def test_ip_limit_truncates(self, monkeypatch):
        resolve_map = {
            "www.example.com": {"A": ["1.1.1.1"], "AAAA": []},
            "api.example.com": {"A": ["2.2.2.2"], "AAAA": []},
            "mail.example.com": {"A": ["3.3.3.3"], "AAAA": []},
        }
        _install_profile_fakes(monkeypatch, resolve_map)
        rep = recon.run_profile("example.com", ip_limit=2)
        assert len(rep["hosts"]) == 2
        assert rep["hosts_truncated"] is True

    def test_rate_limit_spacing_between_ips(self, monkeypatch):
        resolve_map = {
            "www.example.com": {"A": ["1.1.1.1"], "AAAA": []},
            "api.example.com": {"A": ["2.2.2.2"], "AAAA": []},
            "mail.example.com": {"A": [], "AAAA": []},
        }
        _install_profile_fakes(monkeypatch, resolve_map)
        sleeps = []
        monkeypatch.setattr(recon, "_sleep", lambda d: sleeps.append(d))
        rep = recon.run_profile("example.com", pause=1.5)
        # 3 unique IPs (apex + 1.1.1.1 + 2.2.2.2) -> spacing applied 2 times
        assert len(rep["hosts"]) == 3
        assert sleeps == [1.5, 1.5]

    def test_wayback_step_runs_on_bounded_budget(self, monkeypatch):
        # The Wayback CDX index is the slowest source; the profile must call it
        # with a tight timeout and no retries so a slow archive.org can never
        # make the orchestrator read as hung. Capture the kwargs it passes.
        resolve_map = {"www.example.com": {"A": ["93.184.216.34"], "AAAA": []}}
        _install_profile_fakes(monkeypatch, resolve_map)
        seen = []
        monkeypatch.setattr(
            recon, "fetch_wayback",
            lambda t, **k: seen.append(k) or {"source": "wayback", "url": t, "archived": False, "cdx": {}},
        )
        recon.run_profile("example.com")
        assert seen, "profile should invoke the wayback step"
        for k in seen:
            assert k["timeout"] <= 8.0
            assert k["retries"] <= 1

    def test_human_render_profile(self, monkeypatch, capsys):
        resolve_map = {"www.example.com": {"A": ["93.184.216.34"], "AAAA": []}}
        _install_profile_fakes(monkeypatch, resolve_map)
        rc = recon.run(["profile", "example.com", "--human"])
        out = capsys.readouterr().out
        assert rc == 0
        assert "profile — example.com" in out
        assert "hosts:" in out


# ---------------------------------------------------------------------------
# HTTP layer failure modes  (patched at the `_open` seam)
# ---------------------------------------------------------------------------


class TestHttpLayer:
    def test_429_then_success(self, monkeypatch):
        calls = {"n": 0}

        def flaky(req, timeout):
            calls["n"] += 1
            if calls["n"] == 1:
                raise make_http_error(429, retry_after=1)
            return FakeResp('{"ok": true}')

        monkeypatch.setattr(recon, "_open", flaky)
        assert recon.http_get_json("http://x") == {"ok": True}
        assert calls["n"] == 2

    def test_429_exhausted_raises_ratelimit(self, monkeypatch):
        monkeypatch.setattr(recon, "_open", lambda req, timeout: (_ for _ in ()).throw(make_http_error(429)))
        with pytest.raises(recon.RateLimitError):
            recon.http_get("http://x", retries=2)

    def test_5xx_retries_then_raises(self, monkeypatch):
        calls = {"n": 0}

        def boom(req, timeout):
            calls["n"] += 1
            raise make_http_error(503)

        monkeypatch.setattr(recon, "_open", boom)
        with pytest.raises(recon.HTTPStatusError):
            recon.http_get("http://x", retries=2)
        assert calls["n"] == 3  # initial + 2 retries

    def test_404_not_retried(self, monkeypatch):
        calls = {"n": 0}

        def notfound(req, timeout):
            calls["n"] += 1
            raise make_http_error(404)

        monkeypatch.setattr(recon, "_open", notfound)
        with pytest.raises(recon.HTTPStatusError) as ei:
            recon.http_get("http://x", retries=3)
        assert ei.value.status == 404
        assert calls["n"] == 1  # no retries on a 4xx

    def test_timeout_retries_then_networkerror(self, monkeypatch):
        def slow(req, timeout):
            raise socket.timeout("timed out")

        monkeypatch.setattr(recon, "_open", slow)
        with pytest.raises(recon.NetworkError):
            recon.http_get("http://x", retries=1)

    def test_dns_failure_is_networkerror(self, monkeypatch):
        def nodns(req, timeout):
            raise urllib.error.URLError("Name or service not known")

        monkeypatch.setattr(recon, "_open", nodns)
        with pytest.raises(recon.NetworkError):
            recon.http_get("http://x", retries=0)

    def test_malformed_json_raises_parseerror(self, monkeypatch):
        monkeypatch.setattr(recon, "_open", lambda req, timeout: FakeResp("{not valid json"))
        with pytest.raises(recon.ParseError):
            recon.http_get_json("http://x")

    def test_empty_body_raises_parseerror(self, monkeypatch):
        monkeypatch.setattr(recon, "_open", lambda req, timeout: FakeResp(""))
        with pytest.raises(recon.ParseError):
            recon.http_get_json("http://x")

    def test_retry_after_header_respected(self, monkeypatch):
        seen = {"delays": []}
        monkeypatch.setattr(recon, "_sleep", lambda d: seen["delays"].append(d))
        calls = {"n": 0}

        def flaky(req, timeout):
            calls["n"] += 1
            if calls["n"] == 1:
                raise make_http_error(429, retry_after=3)
            return FakeResp('{"ok": 1}')

        monkeypatch.setattr(recon, "_open", flaky)
        recon.http_get_json("http://x")
        assert seen["delays"] == [3.0]


# ---------------------------------------------------------------------------
# CLI surface  (end-to-end via run(), output captured)
# ---------------------------------------------------------------------------


class TestCli:
    def test_ip_json_output(self, monkeypatch, capsys):
        patch_json(monkeypatch, load_fixture("ipapi_8888.json"))
        rc = recon.run(["ip", "8.8.8.8"])
        out = capsys.readouterr().out
        assert rc == 0
        assert '"ip-api.com"' in out

    def test_ip_human_output(self, monkeypatch, capsys):
        patch_json(monkeypatch, load_fixture("ipapi_8888.json"))
        rc = recon.run(["ip", "8.8.8.8", "--human"])
        out = capsys.readouterr().out
        assert rc == 0
        assert "ip-api — 8.8.8.8" in out

    def test_bad_input_returns_exit_2(self, capsys):
        rc = recon.run(["ip", "not-an-ip"])
        err = capsys.readouterr().err
        assert rc == 2
        assert "error:" in err

    def test_asn_human_caps_prefix_list(self, monkeypatch, capsys):
        # Human mode must not dump a 1000+ prefix wall; it caps and says "+N more".
        big = {
            "source": "ripestat",
            "kind": "asn",
            "asn": "15169",
            "holder": "GOOGLE",
            "announced": True,
            "prefix_count": 100,
            "prefixes": ["10.{}.0.0/16".format(i) for i in range(100)],
        }
        monkeypatch.setattr(recon, "fetch_asn", lambda *a, **k: big)
        rc = recon.run(["asn", "AS15169", "--human"])
        out = capsys.readouterr().out
        assert rc == 0
        assert "+85 more" in out
        assert out.count("/16") == recon._HUMAN_PREFIX_CAP

    def test_certs_human(self, monkeypatch, capsys):
        text = load_fixture_text("crtsh_example.json")
        monkeypatch.setattr(recon, "http_get", lambda *a, **k: text)
        rc = recon.run(["certs", "example.com", "--human"])
        out = capsys.readouterr().out
        assert rc == 0
        assert "certs — example.com (via crtsh)" in out


# ---------------------------------------------------------------------------
# CT fallback: crt.sh -> certSpotter  (Tweak 1)
# ---------------------------------------------------------------------------


class TestCertspotterParse:
    def test_scopes_and_dedup(self):
        entries = load_fixture("certspotter_example.json")
        res = recon.parse_certspotter(entries, "example.com")
        assert res["source"] == "certspotter"
        assert "www.example.com" in res["subdomains"]
        assert "*.example.com" in res["subdomains"]
        # out-of-apex SANs are dropped exactly like crt.sh
        assert "unrelated.attacker.test" not in res["subdomains"]
        assert res["subdomains"] == sorted(set(res["subdomains"]))
        assert res["cert_count"] == 3

    def test_no_wildcards(self):
        entries = load_fixture("certspotter_example.json")
        res = recon.parse_certspotter(entries, "example.com", include_wildcards=False)
        assert all(not s.startswith("*.") for s in res["subdomains"])

    def test_error_object_raises(self):
        # certSpotter returns {"code","message"} (a dict) when it rejects a query.
        with pytest.raises(recon.ParseError):
            recon.parse_certspotter({"code": "rate_limited", "message": "slow down"}, "example.com")

    def test_non_list_raises(self):
        with pytest.raises(recon.ParseError):
            recon.parse_certspotter(42, "example.com")

    def test_none_is_empty(self):
        assert recon.parse_certspotter(None, "example.com")["subdomain_count"] == 0


class TestCtFallback:
    def test_crtsh_down_falls_back_to_certspotter(self, monkeypatch):
        cs_text = load_fixture_text("certspotter_example.json")

        def fake_http_get(url, headers=None, timeout=15.0, retries=3):
            if "crt.sh" in url:
                raise recon.HTTPStatusError(502, url)
            if "certspotter" in url:
                return cs_text
            raise AssertionError("unexpected url: " + url)

        monkeypatch.setattr(recon, "http_get", fake_http_get)
        res = recon.fetch_certs("example.com")
        assert res["source"] == "ct"
        assert res["sources_used"] == ["certspotter"]
        assert "www.example.com" in res["subdomains"]
        assert "mail.example.com" in res["subdomains"]
        assert "unrelated.attacker.test" not in res["subdomains"]
        # the crt.sh 502 is recorded for audit, not swallowed silently
        assert any(e["source"] == "crtsh" and "502" in e["error"] for e in res["errors"])

    def test_both_sources_down_raises_clean_error(self, monkeypatch):
        monkeypatch.setattr(
            recon, "http_get",
            lambda *a, **k: (_ for _ in ()).throw(recon.NetworkError("name resolution failed")),
        )
        with pytest.raises(recon.ReconError):
            recon.fetch_certs("example.com")

    def test_crtsh_empty_200_is_answer_not_outage(self, monkeypatch):
        # A 200 with an empty body means "no certs logged" — a real answer.
        # The fallback must NOT be queried in that case.
        seen = []

        def fake(url, headers=None, timeout=15.0, retries=3):
            seen.append(url)
            if "crt.sh" in url:
                return ""  # crt.sh's zero-result sentinel
            raise AssertionError("fallback should not be hit: " + url)

        monkeypatch.setattr(recon, "http_get", fake)
        res = recon.fetch_certs("example.com")
        assert res["sources_used"] == ["crtsh"]
        assert res["subdomain_count"] == 0
        assert res["errors"] == []
        assert not any("certspotter" in u for u in seen)

    def test_merge_all_unions_and_dedups(self, monkeypatch):
        crt_text = load_fixture_text("crtsh_example.json")
        cs_text = load_fixture_text("certspotter_example.json")

        def fake(url, headers=None, timeout=15.0, retries=3):
            if "crt.sh" in url:
                return crt_text
            if "certspotter" in url:
                return cs_text
            raise AssertionError("unexpected url: " + url)

        monkeypatch.setattr(recon, "http_get", fake)
        res = recon.fetch_certs("example.com", merge_all=True)
        assert res["sources_used"] == ["crtsh", "certspotter"]
        # crt.sh gives example.com + *.example.com; certSpotter adds www/api/mail
        assert set(res["subdomains"]) == {
            "*.example.com", "api.example.com", "example.com",
            "mail.example.com", "www.example.com",
        }
        # cert-history rows are concatenated across both sources
        assert res["cert_count"] == 12 + 3

    def test_fallback_error_surfaces_in_profile(self, monkeypatch):
        resolve_map = {"www.example.com": {"A": ["93.184.216.34"], "AAAA": []}}
        _install_profile_fakes(monkeypatch, resolve_map)
        monkeypatch.setattr(
            recon, "fetch_certs",
            lambda *a, **k: {
                "source": "ct", "subdomains": ["www.example.com"], "subdomain_count": 1,
                "subdomains_truncated": False, "sources_used": ["certspotter"],
                "errors": [{"source": "crtsh", "error": "HTTP 502 from crt.sh"}],
            },
        )
        rep = recon.run_profile("example.com")
        assert rep["subdomains"]["ct_sources"] == ["certspotter"]
        assert any(e["step"] == "certs:crtsh" for e in rep["errors"])


# ---------------------------------------------------------------------------
# RDAP IANA bootstrap: .io / ccTLD resolution  (Tweak 2)
# ---------------------------------------------------------------------------


class TestRdapBootstrap:
    @pytest.fixture(autouse=True)
    def _clear_cache(self):
        recon._RDAP_BOOTSTRAP_CACHE.clear()
        yield
        recon._RDAP_BOOTSTRAP_CACHE.clear()

    def test_parse_bootstrap_maps_tlds(self):
        m = recon.parse_rdap_bootstrap(load_fixture("rdap_bootstrap_dns.json"))
        assert m["ai"] == "https://rdap.identitydigital.services/rdap"
        assert m["com"].startswith("https://rdap.verisign.com")
        # .io is intentionally absent from IANA's bootstrap (matches reality)
        assert "io" not in m

    def test_parse_bootstrap_rejects_missing_services(self):
        with pytest.raises(recon.ParseError):
            recon.parse_rdap_bootstrap({"version": "1.0"})

    def test_base_via_bootstrap_for_ai(self, monkeypatch):
        # .ai IS in the bootstrap -> authoritative server, origin 'iana-bootstrap'
        monkeypatch.setattr(recon, "http_get_json", lambda url, **k: load_fixture("rdap_bootstrap_dns.json"))
        base, origin, bootstrap_ok = recon._rdap_base_for_domain("example.ai", 5, 1)
        assert origin == "iana-bootstrap"
        assert base == "https://rdap.identitydigital.services/rdap/domain/example.ai"
        assert bootstrap_ok is True

    def test_base_via_supplement_for_io(self, monkeypatch):
        # .io is NOT in the bootstrap -> the curated supplement resolves it. This
        # is the exact reported case (rdap.org 404s .io).
        monkeypatch.setattr(recon, "http_get_json", lambda url, **k: load_fixture("rdap_bootstrap_dns.json"))
        base, origin, bootstrap_ok = recon._rdap_base_for_domain("example.io", 5, 1)
        assert origin == "supplement"
        assert base == "https://rdap.identitydigital.services/rdap/domain/example.io"
        assert bootstrap_ok is True

    def test_supplement_works_even_if_bootstrap_unreachable(self, monkeypatch):
        # bootstrap down, but .io is in the supplement -> still resolves.
        monkeypatch.setattr(
            recon, "http_get_json",
            lambda url, **k: (_ for _ in ()).throw(recon.NetworkError("iana down")),
        )
        base, origin, bootstrap_ok = recon._rdap_base_for_domain("example.io", 5, 1)
        assert origin == "supplement"
        assert "identitydigital" in base
        assert bootstrap_ok is False  # bootstrap was unreachable; supplement carried it

    def test_base_none_for_unmapped_tld(self, monkeypatch):
        # Bootstrap reachable + TLD absent everywhere -> no base, but bootstrap_ok
        # is True: absence is authoritative, which lets fetch_rdap report the TLD
        # as unsupported rather than blindly hitting rdap.org for a 404.
        monkeypatch.setattr(recon, "http_get_json", lambda url, **k: load_fixture("rdap_bootstrap_dns.json"))
        base, origin, bootstrap_ok = recon._rdap_base_for_domain("example.zzz", 5, 1)
        assert base is None and origin is None
        assert bootstrap_ok is True

    def test_bootstrap_is_cached(self, monkeypatch):
        calls = {"n": 0}

        def fake(url, **k):
            calls["n"] += 1
            return load_fixture("rdap_bootstrap_dns.json")

        monkeypatch.setattr(recon, "http_get_json", fake)
        recon._rdap_base_for_domain("a.ai", 5, 1)
        recon._rdap_base_for_domain("b.ai", 5, 1)
        assert calls["n"] == 1  # fetched once, then memoized

    def test_fetch_ai_uses_bootstrap_server(self, monkeypatch):
        urls = []

        def fake(url, headers=None, timeout=15.0, retries=3):
            urls.append(url)
            if "data.iana.org" in url:
                return load_fixture("rdap_bootstrap_dns.json")
            if "identitydigital" in url:
                return load_fixture("rdap_domain_example.json")
            raise AssertionError("unexpected url: " + url)

        monkeypatch.setattr(recon, "http_get_json", fake)
        res = recon.fetch_rdap("example.ai")
        assert res["kind"] == "domain"
        assert res["rdap_source"] == "iana-bootstrap"
        assert any("identitydigital" in u for u in urls)
        assert not any("rdap.org" in u for u in urls)  # authoritative, not the redirector

    def test_fetch_io_uses_supplement_server(self, monkeypatch):
        # The reported case: .io resolves via the supplement, NOT rdap.org.
        urls = []

        def fake(url, headers=None, timeout=15.0, retries=3):
            urls.append(url)
            if "data.iana.org" in url:
                return load_fixture("rdap_bootstrap_dns.json")  # io absent here
            if "identitydigital" in url:
                return load_fixture("rdap_domain_example.json")
            raise AssertionError("unexpected url: " + url)

        monkeypatch.setattr(recon, "http_get_json", fake)
        res = recon.fetch_rdap("example.io")
        assert res["kind"] == "domain"
        assert res["rdap_source"] == "supplement"
        assert any("identitydigital" in u for u in urls)
        assert not any("rdap.org" in u for u in urls)

    def test_fetch_unmapped_tld_when_bootstrap_ok_is_unsupported(self, monkeypatch):
        # Bootstrap reachable + TLD absent from bootstrap AND supplement -> the
        # registry has no public RDAP server. rdap.org (bootstrap-backed) would
        # only 404, so we return a first-class 'unsupported' result and never
        # touch the redirector.
        urls = []

        def fake(url, headers=None, timeout=15.0, retries=3):
            urls.append(url)
            if "data.iana.org" in url:
                return load_fixture("rdap_bootstrap_dns.json")
            raise AssertionError("should not fetch anything beyond the bootstrap: " + url)

        monkeypatch.setattr(recon, "http_get_json", fake)
        res = recon.fetch_rdap("example.zzz")  # .zzz in neither bootstrap nor supplement
        assert res["supported"] is False
        assert res["rdap_source"] == "none"
        assert res["kind"] == "domain"
        assert res["tld"] == "zzz"
        assert "zzz" in res["reason"]
        assert not any("rdap.org" in u for u in urls)  # no spurious 404 fetch

    def test_fetch_unmapped_tld_bootstrap_unreachable_falls_back_to_rdap_org(self, monkeypatch):
        # Bootstrap UNREACHABLE + TLD not in supplement -> absence is
        # inconclusive, so we must not claim 'unsupported'; fall back to rdap.org.
        urls = []

        def fake(url, headers=None, timeout=15.0, retries=3):
            urls.append(url)
            if "data.iana.org" in url:
                raise recon.NetworkError("iana down")
            if "rdap.org" in url:
                return load_fixture("rdap_domain_example.json")
            raise AssertionError("unexpected url: " + url)

        monkeypatch.setattr(recon, "http_get_json", fake)
        res = recon.fetch_rdap("example.zzz")
        assert res["rdap_source"] == "rdap.org"
        assert res["supported"] is True
        assert any("rdap.org/domain" in u for u in urls)

    def test_bootstrap_unreachable_io_still_uses_supplement(self, monkeypatch):
        def fake(url, headers=None, timeout=15.0, retries=3):
            if "data.iana.org" in url:
                raise recon.NetworkError("iana unreachable")
            if "identitydigital" in url:
                return load_fixture("rdap_domain_example.json")
            raise AssertionError("unexpected url: " + url)

        monkeypatch.setattr(recon, "http_get_json", fake)
        res = recon.fetch_rdap("example.io")
        assert res["rdap_source"] == "supplement"

    def test_authoritative_404_falls_back_to_rdap_org(self, monkeypatch):
        def fake(url, headers=None, timeout=15.0, retries=3):
            if "data.iana.org" in url:
                return load_fixture("rdap_bootstrap_dns.json")
            if "identitydigital" in url:
                raise recon.HTTPStatusError(404, url)
            if "rdap.org" in url:
                return load_fixture("rdap_domain_example.json")
            raise AssertionError("unexpected url: " + url)

        monkeypatch.setattr(recon, "http_get_json", fake)
        res = recon.fetch_rdap("example.io")  # supplement server 404s -> redirector
        assert res["rdap_source"] == "rdap.org"

    def test_no_bootstrap_flag_uses_rdap_org(self, monkeypatch):
        urls = []

        def fake(url, headers=None, timeout=15.0, retries=3):
            urls.append(url)
            if "rdap.org" in url:
                return load_fixture("rdap_domain_example.json")
            raise AssertionError("bootstrap should be skipped: " + url)

        monkeypatch.setattr(recon, "http_get_json", fake)
        res = recon.fetch_rdap("example.io", use_bootstrap=False)
        assert res["rdap_source"] == "rdap.org"
        assert not any("data.iana.org" in u for u in urls)
        assert not any("identitydigital" in u for u in urls)

    def test_ip_and_asn_still_use_rdap_org(self, monkeypatch):
        # bootstrap is domain-only; IP/ASN keep the rdap.org path (verified live).
        seen = []

        def fake(url, headers=None, timeout=15.0, retries=3):
            seen.append(url)
            if "/ip/" in url:
                return load_fixture("rdap_ip_8888.json")
            raise AssertionError("unexpected url: " + url)

        monkeypatch.setattr(recon, "http_get_json", fake)
        res = recon.fetch_rdap("8.8.8.8")
        assert res["rdap_source"] == "rdap.org"
        assert any("rdap.org/ip/" in u for u in seen)


# ---------------------------------------------------------------------------
# RDAP graceful degradation: 'unsupported' is a first-class result, not an error
# ---------------------------------------------------------------------------


class TestRdapUnsupported:
    @pytest.fixture(autouse=True)
    def _clear_cache(self):
        recon._RDAP_BOOTSTRAP_CACHE.clear()
        yield
        recon._RDAP_BOOTSTRAP_CACHE.clear()

    def test_builder_shape(self):
        res = recon._rdap_unsupported("example.zzz", "domain", "example.zzz")
        assert res["source"] == "rdap"
        assert res["kind"] == "domain"
        assert res["target"] == "example.zzz"
        assert res["supported"] is False
        assert res["rdap_source"] == "none"
        assert res["tld"] == "zzz"
        assert "zzz" in res["reason"]

    def test_supported_flag_present_on_normal_result(self, monkeypatch):
        # The contract is symmetric: a real answer carries supported=True so a
        # caller can branch on a single field.
        def fake(url, headers=None, timeout=15.0, retries=3):
            if "data.iana.org" in url:
                return load_fixture("rdap_bootstrap_dns.json")
            if "identitydigital" in url:
                return load_fixture("rdap_domain_example.json")
            raise AssertionError("unexpected url: " + url)

        monkeypatch.setattr(recon, "http_get_json", fake)
        res = recon.fetch_rdap("example.ai")
        assert res["supported"] is True

    def test_no_bootstrap_flag_never_reports_unsupported(self, monkeypatch):
        # With the bootstrap disabled we cannot know a TLD is unsupported, so we
        # must fall back to rdap.org, never emit a false 'unsupported'.
        def fake(url, headers=None, timeout=15.0, retries=3):
            if "rdap.org" in url:
                return load_fixture("rdap_domain_example.json")
            raise AssertionError("bootstrap should be skipped: " + url)

        monkeypatch.setattr(recon, "http_get_json", fake)
        res = recon.fetch_rdap("example.zzz", use_bootstrap=False)
        assert res["rdap_source"] == "rdap.org"
        assert res["supported"] is True

    def test_human_render_unsupported(self):
        res = recon._rdap_unsupported("example.zzz", "domain", "example.zzz")
        out = recon.render_human(res)
        assert "unsupported for .zzz" in out
        assert "no public RDAP server" in out
        # must NOT print the misleading "RDAP (domain) — None" header
        assert "— None" not in out

    def test_human_render_redacted_handle_falls_back_to_name(self):
        # Registries like .io/.de redact the top-level handle; the header must
        # fall back to the domain, never print "RDAP (domain) — None" (roadmap #3).
        res = {"source": "rdap", "kind": "domain", "supported": True, "handle": None,
               "ldhName": "groupvault.io", "target": "groupvault.io", "events": {}, "status": []}
        out = recon.render_human(res)
        assert "RDAP (domain) — groupvault.io" in out
        assert "— None" not in out

    def test_profile_unsupported_rdap_is_not_an_error(self, monkeypatch):
        # An unsupported-TLD apex must degrade gracefully inside profile: a clean
        # structured signal under apex.rdap, and NOT an entry in errors[].
        resolve_map = {}
        _install_profile_fakes(monkeypatch, resolve_map)
        monkeypatch.setattr(
            recon, "fetch_rdap",
            lambda *a, **k: recon._rdap_unsupported("example.zzz", "domain", "example.zzz"),
        )
        rep = recon.run_profile("example.zzz")
        assert rep["apex"]["rdap"]["supported"] is False
        assert rep["apex"]["rdap"]["rdap_source"] == "none"
        assert not any(e["step"] == "rdap" for e in rep["errors"])

    def test_profile_human_render_unsupported_rdap(self, monkeypatch):
        resolve_map = {}
        _install_profile_fakes(monkeypatch, resolve_map)
        monkeypatch.setattr(
            recon, "fetch_rdap",
            lambda *a, **k: recon._rdap_unsupported("example.zzz", "domain", "example.zzz"),
        )
        rep = recon.run_profile("example.zzz")
        out = recon.render_human(rep)
        assert "rdap: unsupported" in out
        assert "registration: None" not in out


# ---------------------------------------------------------------------------
# RDAP third state: 'unreachable' — the endpoint is delegated (bootstrap-present)
# but reset/timed-out from our egress. Distinct from both PASS and 'unsupported'.
# ---------------------------------------------------------------------------


def _reset_neterr(msg="network error: reset"):
    return recon.NetworkError(msg, cause=ConnectionResetError(104, "Connection reset by peer"))


class TestUnreachableSignalClassifier:
    def test_connection_reset_is_unreachable(self):
        assert recon._is_unreachable_signal(_reset_neterr()) is True

    def test_errno_104_oserror_is_unreachable(self):
        e = recon.NetworkError("x", cause=OSError(104, "Connection reset by peer"))
        assert recon._is_unreachable_signal(e) is True

    def test_read_timeout_is_unreachable(self):
        assert recon._is_unreachable_signal(recon.NetworkError("t", cause=socket.timeout("timed out"))) is True

    def test_tls_handshake_reset_is_unreachable(self):
        import ssl as _ssl
        e = recon.NetworkError("tls", cause=_ssl.SSLError("[SSL] record layer failure: connection reset"))
        assert recon._is_unreachable_signal(e) is True

    def test_urlerror_wrapping_reset_is_unreachable(self):
        wrapped = urllib.error.URLError(ConnectionResetError(104, "reset"))
        assert recon._is_unreachable_signal(recon.NetworkError("w", cause=wrapped)) is True

    def test_rate_limit_is_NOT_unreachable(self):
        # A 429/ban must never be misfiled as the retryable-transport state.
        assert recon._is_unreachable_signal(recon.RateLimitError("rate limited")) is False

    def test_http_status_is_NOT_unreachable(self):
        assert recon._is_unreachable_signal(recon.HTTPStatusError(500, "http://x")) is False

    def test_dns_resolution_failure_is_NOT_unreachable(self):
        # gaierror is an OSError but not ECONNRESET — must not be swallowed here.
        e = recon.NetworkError("dns", cause=socket.gaierror(-2, "Name or service not known"))
        assert recon._is_unreachable_signal(e) is False

    def test_connection_refused_is_NOT_unreachable(self):
        e = recon.NetworkError("refused", cause=ConnectionRefusedError(111, "Connection refused"))
        assert recon._is_unreachable_signal(e) is False


class TestRdapUnreachable:
    @pytest.fixture(autouse=True)
    def _clear_cache(self):
        recon._RDAP_BOOTSTRAP_CACHE.clear()
        yield
        recon._RDAP_BOOTSTRAP_CACHE.clear()

    def test_authoritative_reset_yields_unreachable_not_error(self, monkeypatch):
        # .ai is delegated in the bootstrap -> identitydigital. If that
        # authoritative server resets the connection, we must classify it as
        # 'unreachable' (retryable), NOT crash and NOT claim 'unsupported'.
        urls = []

        def fake(url, headers=None, timeout=15.0, retries=3):
            urls.append(url)
            if "data.iana.org" in url:
                return load_fixture("rdap_bootstrap_dns.json")
            if "identitydigital" in url:
                raise _reset_neterr()
            raise AssertionError("unexpected url: " + url)

        monkeypatch.setattr(recon, "http_get_json", fake)
        res = recon.fetch_rdap("example.ai")
        assert res["source"] == "rdap"
        assert res["supported"] is True          # a server exists...
        assert res["rdap_source"] == "unreachable"  # ...we just couldn't reach it
        assert res["retryable"] is True
        assert res["tld"] == "ai"
        assert res["origin"] == "iana-bootstrap"
        assert "retryable" in res["reason"].lower()
        assert "errno 104" in res["reason"].lower() or "reset" in res["reason"].lower()
        # Must NOT fall through to the redirector (same broken backend from our egress).
        assert not any("rdap.org" in u for u in urls)

    def test_authoritative_reset_is_distinct_from_unsupported(self, monkeypatch):
        # Guard the whole point: reachable-but-unreachable must never reuse the
        # 'supported: false / rdap_source: none' shape (which asserts no server).
        def fake(url, headers=None, timeout=15.0, retries=3):
            if "data.iana.org" in url:
                return load_fixture("rdap_bootstrap_dns.json")
            if "identitydigital" in url:
                raise _reset_neterr()
            raise AssertionError("unexpected url: " + url)

        monkeypatch.setattr(recon, "http_get_json", fake)
        res = recon.fetch_rdap("example.ai")
        assert not (res["supported"] is False)
        assert res["rdap_source"] != "none"

    def test_authoritative_refused_still_falls_back_to_rdap_org(self, monkeypatch):
        # A NON-reset transport failure (connection refused / DNS / 5xx) is NOT
        # the 'unreachable' state — it should still try the redirector so we
        # don't over-claim. Keeps the trigger narrow.
        urls = []

        def fake(url, headers=None, timeout=15.0, retries=3):
            urls.append(url)
            if "data.iana.org" in url:
                return load_fixture("rdap_bootstrap_dns.json")
            if "identitydigital" in url:
                raise recon.NetworkError("refused", cause=ConnectionRefusedError(111, "refused"))
            if "rdap.org" in url:
                return load_fixture("rdap_domain_example.json")
            raise AssertionError("unexpected url: " + url)

        monkeypatch.setattr(recon, "http_get_json", fake)
        res = recon.fetch_rdap("example.ai")
        assert res["rdap_source"] == "rdap.org"
        assert res["supported"] is True
        assert any("rdap.org/domain" in u for u in urls)

    def test_supplement_endpoint_reset_is_unreachable(self, monkeypatch):
        # .io resolves via the curated supplement; a reset there is unreachable
        # too, with origin reported as 'supplement'.
        def fake(url, headers=None, timeout=15.0, retries=3):
            if "data.iana.org" in url:
                return load_fixture("rdap_bootstrap_dns.json")  # io absent -> supplement
            if "identitydigital" in url:
                raise _reset_neterr()
            raise AssertionError("unexpected url: " + url)

        monkeypatch.setattr(recon, "http_get_json", fake)
        res = recon.fetch_rdap("example.io")
        assert res["rdap_source"] == "unreachable"
        assert res["origin"] == "supplement"

    def test_builder_shape(self):
        err = recon.RdapUnreachable(endpoint="https://rdap.nic.beer/domain/x.beer",
                                    origin="iana-bootstrap", detail="reset")
        res = recon._rdap_unreachable("x.beer", "domain", "x.beer", err)
        assert res["source"] == "rdap"
        assert res["supported"] is True
        assert res["rdap_source"] == "unreachable"
        assert res["retryable"] is True
        assert res["tld"] == "beer"
        assert res["endpoint"] == "https://rdap.nic.beer/domain/x.beer"

    def test_cli_exit_code_is_3(self, monkeypatch, capsys):
        # The whole tri/quad-state is kept honest by the exit code: 'unreachable'
        # gets its own code 3, not folded into success (0) or error (2).
        monkeypatch.setattr(
            recon, "fetch_rdap",
            lambda *a, **k: recon._rdap_unreachable(
                "example.beer", "domain", "example.beer",
                recon.RdapUnreachable("https://rdap.nic.beer", "iana-bootstrap", "reset"),
            ),
        )
        rc = recon.run(["rdap", "example.beer"])
        out = capsys.readouterr().out
        assert rc == 3
        assert '"unreachable"' in out

    def test_human_render_unreachable(self):
        err = recon.RdapUnreachable("https://rdap.nic.beer", "iana-bootstrap", "reset")
        res = recon._rdap_unreachable("example.beer", "domain", "example.beer", err)
        out = recon.render_human(res)
        assert "endpoint unreachable (retryable)" in out
        assert "— None" not in out

    def test_profile_unreachable_rdap_is_not_an_error(self, monkeypatch):
        resolve_map = {}
        _install_profile_fakes(monkeypatch, resolve_map)
        err = recon.RdapUnreachable("https://rdap.nic.beer", "iana-bootstrap", "reset")
        monkeypatch.setattr(
            recon, "fetch_rdap",
            lambda *a, **k: recon._rdap_unreachable("example.beer", "domain", "example.beer", err),
        )
        rep = recon.run_profile("example.beer")
        assert rep["apex"]["rdap"]["rdap_source"] == "unreachable"
        assert not any(e["step"] == "rdap" for e in rep["errors"])
        out = recon.render_human(rep)
        assert "rdap: unreachable" in out


# ---------------------------------------------------------------------------
# RDAP fourth state: 'broken' — the endpoint is delegated (bootstrap-present)
# and *responded*, but with an unusable response (untrusted/self-signed TLS
# cert, or an HTTP 4xx/5xx). Distinct from PASS, 'unsupported' (no server), and
# 'unreachable' (transport reset/timeout — no response at all).
# ---------------------------------------------------------------------------


def _cert_neterr(msg="unable to get local issuer certificate"):
    inner = ssl.SSLCertVerificationError(
        1, "[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: " + msg
    )
    return recon.NetworkError("net", cause=urllib.error.URLError(inner))


class TestEndpointFaultClassifier:
    def test_bad_cert_is_broken_not_retryable(self):
        assert recon._endpoint_fault(_cert_neterr()) == ("bad-cert", False, None)

    def test_self_signed_cert_is_broken(self):
        assert recon._endpoint_fault(_cert_neterr("self-signed certificate")) == ("bad-cert", False, None)

    def test_http_426_is_broken_not_retryable(self):
        assert recon._endpoint_fault(recon.HTTPStatusError(426, "u")) == ("http-426", False, 426)

    def test_http_404_apex_is_broken_not_retryable(self):
        assert recon._endpoint_fault(recon.HTTPStatusError(404, "u")) == ("http-404", False, 404)

    def test_http_500_is_broken_but_retryable(self):
        assert recon._endpoint_fault(recon.HTTPStatusError(500, "u")) == ("http-500", True, 500)

    def test_http_503_is_broken_but_retryable(self):
        assert recon._endpoint_fault(recon.HTTPStatusError(503, "u")) == ("http-503", True, 503)

    # --- boundary: these must NEVER be misfiled as 'broken' ---
    def test_connection_reset_is_NOT_broken(self):
        # A transport reset belongs to 'unreachable', which is checked first.
        assert recon._endpoint_fault(_reset_neterr()) is None
        assert recon._is_unreachable_signal(_reset_neterr()) is True

    def test_tls_handshake_reset_is_NOT_broken(self):
        # A TLS-RST is a reset (unreachable), not a cert-verification failure.
        e = recon.NetworkError("tls", cause=ssl.SSLError("[SSL] record layer failure: connection reset"))
        assert recon._endpoint_fault(e) is None
        assert recon._is_unreachable_signal(e) is True

    def test_read_timeout_is_NOT_broken(self):
        assert recon._endpoint_fault(recon.NetworkError("t", cause=socket.timeout("timed out"))) is None

    def test_rate_limit_is_NOT_broken(self):
        # A 429/ban is a rate-limit to honour, never a 'broken endpoint'.
        assert recon._endpoint_fault(recon.RateLimitError("rate limited")) is None

    def test_http_429_status_is_NOT_broken(self):
        assert recon._endpoint_fault(recon.HTTPStatusError(429, "u")) is None

    def test_dns_resolution_failure_is_NOT_broken(self):
        e = recon.NetworkError("dns", cause=socket.gaierror(-2, "Name or service not known"))
        assert recon._endpoint_fault(e) is None

    def test_connection_refused_is_NOT_broken(self):
        e = recon.NetworkError("refused", cause=ConnectionRefusedError(111, "Connection refused"))
        assert recon._endpoint_fault(e) is None

    def test_parse_error_is_NOT_broken(self):
        assert recon._endpoint_fault(recon.ParseError("bad json")) is None


class TestRdapBroken:
    @pytest.fixture(autouse=True)
    def _clear_cache(self):
        recon._RDAP_BOOTSTRAP_CACHE.clear()
        yield
        recon._RDAP_BOOTSTRAP_CACHE.clear()

    def test_authoritative_bad_cert_yields_broken_not_error(self, monkeypatch):
        # .ai is delegated in the bootstrap. If BOTH its authoritative server and
        # the rdap.org redirector present an untrusted cert (rdap.org redirects
        # the client back to the same backend), classify 'broken' (non-retryable),
        # not a crash and not 'unsupported'. The authoritative cause (bad-cert) is
        # preserved even though the redirector was also tried.
        urls = []

        def fake(url, headers=None, timeout=15.0, retries=3):
            urls.append(url)
            if "data.iana.org" in url:
                return load_fixture("rdap_bootstrap_dns.json")
            if "identitydigital" in url or "rdap.org" in url:
                raise _cert_neterr()
            raise AssertionError("unexpected url: " + url)

        monkeypatch.setattr(recon, "http_get_json", fake)
        res = recon.fetch_rdap("example.ai")
        assert res["source"] == "rdap"
        assert res["supported"] is True          # a server exists...
        assert res["rdap_source"] == "broken"    # ...it just serves a bad cert
        assert res["cause"] == "bad-cert"
        assert res["retryable"] is False
        assert res["tld"] == "ai"
        assert res["origin"] == "iana-bootstrap"
        assert "not retryable" in res["reason"].lower()
        # It DID try the redirector (rescue chance) before concluding broken.
        assert any("rdap.org" in u for u in urls)

    def test_authoritative_http_426_yields_broken_not_retryable(self, monkeypatch):
        def fake(url, headers=None, timeout=15.0, retries=3):
            if "data.iana.org" in url:
                return load_fixture("rdap_bootstrap_dns.json")
            if "identitydigital" in url or "rdap.org" in url:
                raise recon.HTTPStatusError(426, url)
            raise AssertionError("unexpected url: " + url)

        monkeypatch.setattr(recon, "http_get_json", fake)
        res = recon.fetch_rdap("example.ai")
        assert res["rdap_source"] == "broken"
        assert res["cause"] == "http-426"
        assert res["http_status"] == 426
        assert res["retryable"] is False

    def test_authoritative_http_500_yields_broken_but_retryable(self, monkeypatch):
        def fake(url, headers=None, timeout=15.0, retries=3):
            if "data.iana.org" in url:
                return load_fixture("rdap_bootstrap_dns.json")
            if "identitydigital" in url or "rdap.org" in url:
                raise recon.HTTPStatusError(500, url)
            raise AssertionError("unexpected url: " + url)

        monkeypatch.setattr(recon, "http_get_json", fake)
        res = recon.fetch_rdap("example.ai")
        assert res["rdap_source"] == "broken"
        assert res["cause"] == "http-500"
        assert res["retryable"] is True
        assert "retryable" in res["reason"].lower()

    def test_broken_only_after_redirector_also_fails(self, monkeypatch):
        # If the authoritative server has a fault but the rdap.org redirector
        # resolves to a working server, we return that real data — NOT 'broken'.
        # 'broken' is reserved for when both paths are exhausted.
        def fake(url, headers=None, timeout=15.0, retries=3):
            if "data.iana.org" in url:
                return load_fixture("rdap_bootstrap_dns.json")
            if "identitydigital" in url:
                raise _cert_neterr()          # authoritative bad cert...
            if "rdap.org" in url:
                return load_fixture("rdap_domain_example.json")  # ...redirector rescues
            raise AssertionError("unexpected url: " + url)

        monkeypatch.setattr(recon, "http_get_json", fake)
        res = recon.fetch_rdap("example.ai")
        assert res["rdap_source"] == "rdap.org"
        assert res["supported"] is True

    def test_broken_is_distinct_from_unsupported_and_unreachable(self, monkeypatch):
        # Guard the whole point: a broken endpoint must never reuse the
        # 'supported: false / rdap_source: none' shape (no server) nor the
        # 'unreachable' label (transport reset).
        def fake(url, headers=None, timeout=15.0, retries=3):
            if "data.iana.org" in url:
                return load_fixture("rdap_bootstrap_dns.json")
            if "identitydigital" in url or "rdap.org" in url:
                raise _cert_neterr()
            raise AssertionError("unexpected url: " + url)

        monkeypatch.setattr(recon, "http_get_json", fake)
        res = recon.fetch_rdap("example.ai")
        assert not (res["supported"] is False)
        assert res["rdap_source"] not in ("none", "unreachable")

    def test_authoritative_parse_error_still_falls_back_to_rdap_org(self, monkeypatch):
        # A non-classifiable failure (e.g. malformed JSON) is NOT 'broken' — it
        # should still try the redirector. Keeps the trigger narrow.
        urls = []

        def fake(url, headers=None, timeout=15.0, retries=3):
            urls.append(url)
            if "data.iana.org" in url:
                return load_fixture("rdap_bootstrap_dns.json")
            if "identitydigital" in url:
                raise recon.ParseError("invalid JSON")
            if "rdap.org" in url:
                return load_fixture("rdap_domain_example.json")
            raise AssertionError("unexpected url: " + url)

        monkeypatch.setattr(recon, "http_get_json", fake)
        res = recon.fetch_rdap("example.ai")
        assert res["rdap_source"] == "rdap.org"
        assert res["supported"] is True
        assert any("rdap.org/domain" in u for u in urls)

    def test_builder_shape_bad_cert(self):
        err = recon.RdapBroken(endpoint="https://rdap.nic.cr/domain/nic.cr",
                               origin="iana-bootstrap", cause="bad-cert", retryable=False)
        res = recon._rdap_broken("nic.cr", "domain", "nic.cr", err)
        assert res["source"] == "rdap"
        assert res["supported"] is True
        assert res["rdap_source"] == "broken"
        assert res["retryable"] is False
        assert res["cause"] == "bad-cert"
        assert res["tld"] == "cr"
        assert res["endpoint"] == "https://rdap.nic.cr/domain/nic.cr"

    def test_cli_exit_code_is_4_for_non_retryable_broken(self, monkeypatch, capsys):
        monkeypatch.setattr(
            recon, "fetch_rdap",
            lambda *a, **k: recon._rdap_broken(
                "example.cr", "domain", "example.cr",
                recon.RdapBroken("https://rdap.nic.cr", "iana-bootstrap", "bad-cert", False),
            ),
        )
        rc = recon.run(["rdap", "example.cr"])
        out = capsys.readouterr().out
        assert rc == 4
        assert '"broken"' in out

    def test_cli_exit_code_is_3_for_retryable_broken_5xx(self, monkeypatch, capsys):
        # A retryable 5xx 'broken' shares the retryable tier (exit 3) with
        # 'unreachable' — the actionable signal is "retry later".
        monkeypatch.setattr(
            recon, "fetch_rdap",
            lambda *a, **k: recon._rdap_broken(
                "example.tld", "domain", "example.tld",
                recon.RdapBroken("https://rdap.example", "iana-bootstrap", "http-500", True, 500),
            ),
        )
        rc = recon.run(["rdap", "example.tld"])
        assert rc == 3

    def test_human_render_broken(self):
        err = recon.RdapBroken("https://rdap.nic.cr", "iana-bootstrap", "bad-cert", False)
        res = recon._rdap_broken("example.cr", "domain", "example.cr", err)
        out = recon.render_human(res)
        assert "endpoint broken" in out
        assert "bad-cert" in out
        assert "— None" not in out

    def test_profile_broken_rdap_is_not_an_error(self, monkeypatch):
        resolve_map = {}
        _install_profile_fakes(monkeypatch, resolve_map)
        err = recon.RdapBroken("https://rdap.nic.cr", "iana-bootstrap", "bad-cert", False)
        monkeypatch.setattr(
            recon, "fetch_rdap",
            lambda *a, **k: recon._rdap_broken("example.cr", "domain", "example.cr", err),
        )
        rep = recon.run_profile("example.cr")
        assert rep["apex"]["rdap"]["rdap_source"] == "broken"
        assert not any(e["step"] == "rdap" for e in rep["errors"])
        out = recon.render_human(rep)
        assert "rdap: broken" in out
