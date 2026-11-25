#!/usr/bin/env python3
"""
geo-scan — Answer-Engine Readiness Audit
Scores how readily AI answer engines (ChatGPT search, Perplexity, Claude, Gemini /
AI Overviews, Copilot) can fetch, parse and quote a public website. No API key, no
account, stdlib only. Produces a Markdown report + JSON, with a prioritised action list.

Usage:
    python3 geo_scan.py https://example.com
    python3 geo_scan.py --url https://example.com --pages 12 --json out.json --md out.md
    python3 geo_scan.py https://example.com --quiet

Scoring model (100 points; the weights are our judgement, not validated against
observed citations):
    crawler access   20   robots.txt lets search/retrieval agents fetch the site (gate)
    machine-read     15   sitemap.xml + <lastmod> coverage (11), llms.txt (4, speculative)
    snippet rights   10   no noindex / nosnippet / max-snippet:0 (meta robots, X-Robots-Tag)
    structure        25   one h1, schema.org types, description, author, words, lists, canonical
    quotability      20   definitional phrases, hard figures, tables, question titles, h2 sections
    freshness        10   median page dateModified (or sitemap lastmod); future dates discarded

Gate: if robots.txt keeps every search/retrieval agent off the root URL, the total is
the crawler score alone — the other axes are reported but cannot help.

Politeness: geo-scan obeys robots.txt for its own user-agent token `geo-scan` (and `*`),
waits at least 1 s between requests (longer if Crawl-delay says so), stays on the
audited host, caps every download and the whole scan's wall time.

Safety: every address is validated before the socket opens. Hosts that are or resolve
to loopback, RFC1918, link-local (including the cloud metadata address), unique-local,
CGNAT, reserved, multicast or unspecified addresses are refused, redirects included;
the validated address is the connect target, so a second DNS answer cannot move the
request elsewhere. No proxy from the environment is used. `--allow-private` opts out.

Exit codes: 0 report produced (a low score is a finding, not a failure);
            2 scan or output failed (DNS, TLS, unreachable robots.txt, no page, a
              refused non-public host, or the --json/--md file could not be written).
"""

import argparse
import calendar
import codecs
import http.client
import ipaddress
import json
import re
import socket
import ssl
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import zlib
from html.parser import HTMLParser
from pathlib import Path
from types import SimpleNamespace

__version__ = "1.2.8"
UA_TOKEN = "geo-scan"
UA = f"{UA_TOKEN}/{__version__} (+https://github.com/AureliusClaw/geo-scan; answer-engine readiness audit)"

MAX_PAGES = 25
DEFAULT_PAGES = 8
DEFAULT_BUDGET = 120          # seconds for the whole scan, every request included
MAX_BUDGET = 120              # --budget is clamped to this; the CLI never runs longer
MIN_BUDGET = 10
DEFAULT_OUT_DIR = "out"      # --json/--md write here, and nowhere else
MIN_DELAY = 1.0               # seconds between requests; Crawl-delay raises it
SOCKET_TIMEOUT = 15
WATCHDOG_GRACE = 0.5          # the watchdog cuts a live socket this far past the deadline
MAX_REDIRECTS = 4             # hops per redirect chain, urllib's own default, made ours
CAP_ROBOTS = 512 * 1024       # RFC 9309 lets crawlers stop at 500 KiB
CAP_LLMS = 1024 * 1024
CAP_SITEMAP = 5 * 1024 * 1024
CAP_PAGE = 2 * 1024 * 1024
MAX_CHILD_SITEMAPS = 3
EST_FETCH = 3.0               # seconds one fetch is assumed to take when reserving budget
PAGE_RESERVE = 3              # page fetches optional requests must leave time for
MAX_DEPTH = 200               # open-element stack cap in the HTML parser

# Agents that fetch pages to answer or cite. These carry the crawler points.
SEARCH_AGENTS = [
    "Googlebot", "Bingbot", "OAI-SearchBot", "ChatGPT-User",
    "PerplexityBot", "Perplexity-User", "Claude-SearchBot", "Claude-User",
]
# Training / dataset crawlers. Blocking them is a legitimate policy and does not stop
# an engine from citing the site (Google-Extended, for one, does not affect Search or
# AI Overviews). Reported, never scored.
TRAINING_AGENTS = [
    "GPTBot", "ClaudeBot", "Google-Extended", "Applebot-Extended", "CCBot",
    "Bytespider", "Meta-ExternalAgent", "Amazonbot", "cohere-ai",
]

SCHEMA_GOOD = {
    "Article": 4, "BlogPosting": 4, "TechArticle": 4, "NewsArticle": 4,
    "ScholarlyArticle": 4, "QAPage": 4, "FAQPage": 2, "HowTo": 1,
    "WebPage": 1, "BreadcrumbList": 2, "Person": 2, "Organization": 2,
    "ImageObject": 1, "Table": 2, "DefinedTerm": 3, "LiveBlogPosting": 3,
}

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
        "param", "source", "track", "wbr"}
HEAD_TAGS = {"head", "title", "meta", "link", "style", "script", "noscript", "base", "template"}
SKIP_TAGS = {"script", "style", "noscript", "template"}


class ScanError(Exception):
    """Nothing usable could be fetched; the CLI exits 2."""


class Skipped(Exception):
    """geo-scan chose not to fetch a URL (robots.txt, other host, time budget)."""


# --------------------------------------------------------------------------- network

def _site(host):
    host = (host or "").lower().rstrip(".")
    return host[4:] if host.startswith("www.") else host


def _embedded_v4(ip):
    """The IPv4 hidden inside an IPv6 address, if any (v4-mapped, 6to4, Teredo).

    Without this, `2002:7f00:1::` (6to4 for 127.0.0.1) reads as a legal global
    IPv6 address and tunnels the request to loopback.
    """
    if ip.version != 6:
        return None
    mapped = getattr(ip, "ipv4_mapped", None)
    if mapped is not None:
        return mapped
    packed = ip.packed
    if packed[:2] == b"\x20\x02":                      # 2002::/16 6to4
        return ipaddress.IPv4Address(packed[2:6])
    if packed[:4] == b"\x20\x01\x00\x00":             # 2001::/32 Teredo
        return ipaddress.IPv4Address(bytes(b ^ 0xFF for b in packed[12:16]))
    return None


def ip_is_public(ip):
    """False for loopback, private, link-local (cloud metadata), ULA, CGNAT,
    reserved, multicast, unspecified — and for IPv6 that embeds any of those."""
    if ip.version == 6:
        inner = _embedded_v4(ip)
        if inner is not None and not ip_is_public(inner):
            return False
    if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
        return False
    if ip.is_multicast or ip.is_unspecified:
        return False
    mapped = getattr(ip, "ipv4_mapped", None)
    if mapped is not None:
        return ip_is_public(mapped)
    # CGNAT 100.64.0.0/10 is neither private nor reserved in Python's tables,
    # but it is not routable from an answer engine either. Test-NETs likewise.
    return bool(ip.is_global)


def _getaddrinfo_bounded(host, port, deadline=None):
    """`socket.getaddrinfo` with a wall-clock bound.

    The resolver has no timeout of its own and synchronous DNS sat outside the
    scan's declared ceiling (registry finding, 2026-11-23): the lookup runs on a
    daemon thread and the scan waits at most until the deadline — a stalled
    resolver can then hold a thread, but not the scan.
    """
    if deadline is None:
        return socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
    left = deadline - time.monotonic()
    if left < 0.2:
        raise Skipped("scan time budget exhausted before DNS")
    box = {}

    def look():
        try:
            box["r"] = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
        except (socket.gaierror, UnicodeError, OSError) as e:
            box["e"] = e

    t = threading.Thread(target=look, daemon=True)
    t.start()
    t.join(left)
    if t.is_alive():
        raise Skipped(f"DNS for {host} did not answer within the scan deadline")
    if "e" in box:
        raise box["e"]
    return box["r"]


def resolve_public_ips(host, port, public_only=True, deadline=None):
    """One DNS pass: every answer validated, then returned in resolution order.

    The returned tuples are what `connect` dials — the validated answer IS the
    connect target, so a second, different DNS answer (DNS rebinding) cannot move
    the request to a private host. `deadline` (monotonic clock) bounds the
    resolver wait. Raises Skipped when the host must not be dialed.
    """
    try:
        literal = ipaddress.ip_address(host.strip("[]"))
    except ValueError:
        literal = None
    if literal is not None:
        if public_only and not ip_is_public(literal):
            raise Skipped(f"{host} is a private/loopback/link-local address; refused")
        return [(literal.version, str(literal))]
    try:
        infos = _getaddrinfo_bounded(host, port, deadline)
    except (socket.gaierror, UnicodeError) as e:
        raise Skipped(f"DNS lookup failed for {host}: {e}") from None
    out, seen = [], set()
    for info in infos:
        raw = str(info[4][0]).split("%", 1)[0]
        try:
            ip = ipaddress.ip_address(raw)
        except ValueError:
            raise Skipped(f"{host} resolved to an unusable address {raw!r}; refused") from None
        if public_only and not ip_is_public(ip):
            raise Skipped(f"{host} resolves to {ip}, not a public address; refused")
        if (ip.version, raw) not in seen:
            seen.add((ip.version, raw))
            out.append((ip.version, raw))
    if not out:
        raise Skipped(f"{host} resolved to no usable address")
    return out


def is_public_host(host):
    """False if the host is an IP or resolves to any non-public address.

    Unresolvable stays True: there is nothing to refuse here, the fetch itself
    fails with a DNS error. The guard that actually decides where a request goes
    is `resolve_public_ips()` at connect time.
    """
    try:
        resolve_public_ips(host, 443)
    except Skipped as e:
        return "DNS lookup failed" in str(e)
    return True


def describe_error(e):
    reason = getattr(e, "reason", e)
    if isinstance(e, urllib.error.HTTPError):
        return f"HTTP {e.code}"
    if isinstance(reason, ssl.SSLCertVerificationError):
        return (f"TLS certificate verification failed ({reason.verify_message}). geo-scan does "
                "not fall back to unverified TLS. On macOS with a python.org Python, run "
                "'Install Certificates.command' once")
    if isinstance(reason, socket.gaierror):
        return f"DNS lookup failed ({reason})"
    if isinstance(reason, (socket.timeout, TimeoutError)):
        return "timed out"
    return str(reason)[:160]


def _decode(raw, content_type):
    enc = None
    m = re.search(r"charset=[\"']?([\w.:-]+)", content_type or "", re.I)
    if m:
        enc = m.group(1)
    else:
        m = re.search(rb"<meta[^>]{0,200}?charset=[\"']?([\w.:-]+)", raw[:4096], re.I)
        if m:
            enc = m.group(1).decode("ascii", "ignore")
    try:
        codecs.lookup(enc or "utf-8")
    except LookupError:
        enc = None
    return raw.decode(enc or "utf-8", "replace")


class _GuardedRedirect(urllib.request.HTTPRedirectHandler):
    """Follows a redirect only if the target passes the same checks as a direct fetch.

    Pacing is held here too: urllib would issue the redirect's follow-up GET the instant
    the 3xx arrives, which is a second request inside the same second and a burst the
    site did not agree to. So the redirect waits out the same delay a normal fetch
    waits out before it hands the new request back to urllib.
    """

    def __init__(self, check, pace=None):
        super().__init__()
        self._check = check
        self._pace = pace or (lambda: None)
        self._hops = 0

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # urllib attaches redirect_dict to a request after its first hop, so its
        # absence marks a new chain: the counter counts hops per chain, never
        # across the scan's pages, and a 25-page site with one redirect each is fine.
        if not hasattr(req, "redirect_dict"):
            self._hops = 0
        self._hops += 1
        if self._hops > MAX_REDIRECTS:
            fp.close()
            raise Skipped(f"redirect chain longer than {MAX_REDIRECTS} hops")
        try:
            self._check(newurl)
            self._pace()
        except Skipped:
            fp.close()
            raise
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _validated_socket(host, port, ips, timeout, source_address=None, deadline=None,
                      register=None):
    """Open the TCP socket to one of the already-validated addresses.

    Every dial attempt is bounded by the scan's wall clock, not just by its own socket
    timeout: N addresses at 15 s each would otherwise spend N×15 s before the scan's
    time limit was ever consulted. `register` hands each candidate socket to the
    Scanner's watchdog before the dial, so the deadline can close a socket that a
    trickling server is holding open.
    """
    last = None
    for version, ip in ips:
        sock = None
        family = socket.AF_INET6 if version == 6 else socket.AF_INET
        addr = (ip, port, 0, 0) if version == 6 else (ip, port)
        try:
            left = timeout if deadline is None else min(timeout, deadline - time.monotonic())
            if left < 1:
                raise Skipped("scan time budget exhausted before connect")
            sock = socket.socket(family, socket.SOCK_STREAM)
            sock.settimeout(left)
            if source_address:
                sock.bind(source_address)
            if register:
                register(sock)
            sock.connect(addr)
            return sock
        except OSError as e:
            last = e
            if sock is not None:
                try:
                    sock.close()
                except OSError:
                    pass
    raise last or Skipped(f"{host}: no address to dial")


class _ValidatedHTTPConnection(http.client.HTTPConnection):
    """An HTTPConnection that dials the addresses the guard just approved.

    The guard's DNS answer is the connect target: nothing looks the host up a
    second time after the check, which is what closes DNS rebinding (T09).
    """

    def __init__(self, host, port=None, timeout=None, source_address=None, *,
                 guard=None, deadline=None, register=None):
        super().__init__(host, port, timeout=timeout, source_address=source_address)
        self._guard = guard
        self._deadline = deadline
        self._register = register

    def connect(self):
        ips = self._guard.approve(self.host, self.port, deadline=self._deadline)
        self.sock = _validated_socket(self.host, self.port, ips, self.timeout,
                                       self.source_address, deadline=self._deadline,
                                       register=self._register)


class _ValidatedHTTPSConnection(http.client.HTTPSConnection):
    """HTTPS to a validated IP, with SNI and certificate checks still on the hostname."""

    def __init__(self, host, port=None, timeout=None, source_address=None, *,
                 context=None, guard=None, deadline=None, register=None):
        super().__init__(host, port, timeout=timeout, source_address=source_address,
                         context=context)
        self._guard = guard
        self._deadline = deadline
        self._register = register

    def connect(self):
        ips = self._guard.approve(self.host, self.port, deadline=self._deadline)
        raw = _validated_socket(self.host, self.port, ips, self.timeout,
                                self.source_address, deadline=self._deadline,
                                register=self._register)
        try:
            self.sock = self._context.wrap_socket(raw, server_hostname=self.host)
            if self._register:      # the watchdog must cut the TLS socket, not the raw one
                self._register(self.sock)
        except Exception:
            try:
                raw.close()
            except OSError:
                pass
            raise


class HostGuard:
    """Decides, per connection, which addresses geo-scan may dial.

    `public_only` is on by default and the Hermes plugin never turns it off; the
    CLI needs an explicit `--allow-private`, which says so on stderr and marks the
    report. There is no environment variable and no config file that changes it.
    """

    def __init__(self, public_only=True, log=None):
        self.public_only = public_only
        self._log = log or (lambda msg: None)

    def approve(self, host, port, deadline=None):
        return resolve_public_ips(host, port, public_only=self.public_only,
                                  deadline=deadline)


class _ValidatedHTTPHandler(urllib.request.HTTPHandler):
    def __init__(self, guard, deadline=None, register=None):
        super().__init__()
        self._guard = guard
        self._deadline = deadline
        self._register = register

    def http_open(self, req):
        return self.do_open(_ValidatedHTTPConnection, req, guard=self._guard,
                            deadline=self._deadline, register=self._register)


class _ValidatedHTTPSHandler(urllib.request.HTTPSHandler):
    def __init__(self, guard, context=None, deadline=None, register=None):
        super().__init__(context=context)
        self._guard = guard
        self._deadline = deadline
        self._register = register

    def https_open(self, req):
        return self.do_open(_ValidatedHTTPSConnection, req, context=self._context,
                            guard=self._guard, deadline=self._deadline,
                            register=self._register)


class Scanner:
    """Paced, capped, deadline-bound, robots-obedient GETs against one site."""

    def __init__(self, root, budget, public_only=True, log=None):
        u = urllib.parse.urlparse(root)
        if u.scheme not in ("http", "https"):
            raise ScanError(f"unsupported scheme {u.scheme!r}: geo-scan fetches http(s) only")
        self.origin = f"{u.scheme}://{u.netloc}"
        self.host = u.hostname or ""
        self.public_only = public_only
        self.guard = HostGuard(public_only, log)
        # the ceiling is the ceiling, here and not only in scan(): whoever constructs
        # a Scanner gets the declared maximum, never a caller-inflated one
        budget = max(MIN_BUDGET, min(MAX_BUDGET, float(budget)))
        self.deadline = time.monotonic() + budget
        self.delay = MIN_DELAY
        self.robots: "Robots | None" = None   # set by scan(): the Robots matcher
        self.notes = []
        self.requests = 0
        self._last = None
        self._log = log or (lambda msg: None)
        # The ceiling the skill declares has to survive a server that drips bytes:
        # urllib's header parsing and the BufferedReader behind r.read() block with
        # no hook at our deadline, so the one thing that ends such a wait for sure
        # is closing the socket from outside. The watchdog does exactly that.
        self._live = None
        self._live_lock = threading.Lock()
        self._watchdog = None
        self._aborted = False
        # ProxyHandler({}) on purpose: an HTTP_PROXY in the environment would reroute
        # the audit through a host we never validated and never scored.
        #
        # The opener is assembled by hand instead of build_opener(): the default
        # factory also registers FTPHandler, FileHandler and DataHandler, and those
        # dial/read outside the guarded HTTP(S) connections — `Sitemap: ftp://host/`
        # in a robots.txt got anonymous FTP with an attacker-chosen path, and
        # `file://localhost/...` read the local disk. Only http(s) handlers live here.
        self._opener = urllib.request.OpenerDirector()
        for handler in (urllib.request.ProxyHandler({}),
                        urllib.request.UnknownHandler(),
                        _ValidatedHTTPHandler(self.guard, deadline=self.deadline,
                                              register=self._register),
                        _ValidatedHTTPSHandler(self.guard,
                                              context=ssl.create_default_context(),
                                              deadline=self.deadline,
                                              register=self._register),
                        _GuardedRedirect(self._guard_redirect, pace=self._pace_redirect),
                        urllib.request.HTTPDefaultErrorHandler(),
                        urllib.request.HTTPErrorProcessor()):
            self._opener.add_handler(handler)

    def _register(self, sock):
        """Hand the live socket to the watchdog; start the watchdog on first use.

        The deadline gives no hook inside urllib's blocking reads, so the watchdog
        waits until deadline + WATCHDOG_GRACE and then closes whatever socket is
        live. After the deadline is spent, `fetch` refuses new requests anyway —
        cutting the in-flight one is the missing half of the declared ceiling.
        """
        with self._live_lock:
            self._live = sock
        if self._watchdog is None:
            self._watchdog = threading.Timer(max(0.0, self.remaining()) + WATCHDOG_GRACE,
                                             self._abort_live)
            self._watchdog.daemon = True
            self._watchdog.start()

    def _abort_live(self):
        self._aborted = True
        with self._live_lock:
            sock, self._live = self._live, None
        if sock is not None:
            # close() alone does NOT wake a recv() already blocked in another
            # thread (POSIX leaves it parked); shutdown() is what forces the
            # blocked read to fail and the fetch to unwind.
            try:
                sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            try:
                sock.close()
            except OSError:
                pass

    def _pace_redirect(self):
        """Pacing held on the redirect hop, not just the first request.

        urllib fires the follow-up GET the instant the 3xx lands; without this the
        hop ignores the delay the site asked for. Same delay, same deadline check,
        then the hop's own timestamp becomes the anchor for the next one.
        """
        now = time.monotonic()
        wait = 0.0 if self._last is None else max(0.0, self._last + self.delay - now)
        if self.deadline - now - wait < 1:
            raise Skipped("scan time budget exhausted before redirect hop")
        if wait:
            time.sleep(wait)
        self._last = time.monotonic()

    def remaining(self):
        return self.deadline - time.monotonic()

    def can_spare(self, slots):
        """True if one optional request still leaves time for `slots` page fetches."""
        return self.remaining() > (slots + 1) * (self.delay + EST_FETCH)

    def _guard_redirect(self, url):
        why = None
        if not self.same_site(url):
            why = "other host"
        elif urllib.parse.urlparse(url).scheme not in ("http", "https"):
            why = f"unsupported scheme {urllib.parse.urlparse(url).scheme!r}"
        elif self.robots is not None and not self.robots.can_fetch(UA_TOKEN, url):
            why = "robots.txt disallows geo-scan"
        if why:
            raise Skipped(f"redirect to {url} not followed: {why}")
        self._guard(url)

    def _guard(self, url):
        """Pre-flight refusal with a readable message; `approve()` decides at connect."""
        host = urllib.parse.urlparse(url).hostname or ""
        if not host:
            raise Skipped(f"{url}: no host to fetch")
        self.guard.approve(host, urllib.parse.urlparse(url).port
                           or (443 if urllib.parse.urlparse(url).scheme == "https" else 80),
                           deadline=self.deadline)

    def same_site(self, url):
        return _site(urllib.parse.urlparse(url).hostname) == _site(self.host)

    def fetch(self, url, cap, obey=True):
        # Scheme first, before any handler is reached: ftp:, file:, data:, gopher: all
        # have their own urllib handlers and none of them pass through the address guard.
        scheme = urllib.parse.urlparse(url).scheme.lower()
        if scheme not in ("http", "https"):
            raise Skipped(f"unsupported scheme {scheme!r}: geo-scan fetches http(s) only")
        if not self.same_site(url):
            raise Skipped("other host; geo-scan stays on the audited host")
        if obey and self.robots is not None and not self.robots.can_fetch(UA_TOKEN, url):
            raise Skipped("robots.txt disallows geo-scan")
        self._guard(url)
        now = time.monotonic()
        wait = 0.0 if self._last is None else max(0.0, self._last + self.delay - now)
        remaining = self.deadline - now - wait
        if remaining < 2:
            raise Skipped("scan time budget exhausted")
        if wait:
            time.sleep(wait)
        self._log(f"GET {url}")
        req = urllib.request.Request(url, headers={
            "User-Agent": UA,
            "Accept": "text/html,application/xml,application/xhtml+xml,text/plain,*/*;q=0.8",
            "Accept-Encoding": "gzip",
            "Accept-Language": "en,en-US;q=0.8,de;q=0.6",
        })
        t0 = time.monotonic()
        self.requests += 1
        # anchor the pacing clock at issue time: a 3xx arriving inside this open()
        # paces its follow-up GET against t0, not against some older request
        self._last = t0
        try:
            with self._opener.open(req, timeout=min(SOCKET_TIMEOUT, remaining)) as r:
                raw, truncated = self._read(r, cap)
                return SimpleNamespace(
                    url=url, final_url=r.geturl(), code=r.getcode(), headers=r.headers,
                    raw=raw, text=_decode(raw, r.headers.get("Content-Type")),
                    truncated=truncated, secs=round(time.monotonic() - t0, 2))
        except (OSError, urllib.error.URLError, http.client.HTTPException) as e:
            # the watchdog cut this socket on purpose; say so instead of reporting
            # whatever OSError the close surfaced as
            if self._aborted:
                raise TimeoutError("scan time budget exhausted — in-flight connection "
                                   "closed at the deadline") from None
            raise
        finally:
            with self._live_lock:
                self._live = None
            self._last = time.monotonic()

    def _read(self, r, cap):
        buf = bytearray()
        while len(buf) <= cap:
            if time.monotonic() > self.deadline:
                raise TimeoutError("scan time budget exhausted mid-download")
            chunk = r.read(65536)
            if not chunk:
                break
            buf += chunk
        truncated = len(buf) > cap
        raw = bytes(buf[:cap])
        if r.headers.get("Content-Encoding", "").lower() == "gzip" or raw[:2] == b"\x1f\x8b":
            d = zlib.decompressobj(16 + zlib.MAX_WBITS)
            try:
                raw = d.decompress(raw, cap)
                truncated = truncated or bool(d.unconsumed_tail)
            except zlib.error:
                pass
        return raw, truncated


# --------------------------------------------------------------------------- robots.txt

def _pattern_to_rx(pattern):
    """RFC 9309 path pattern -> regex: `*` matches any sequence, a trailing `$` anchors."""
    anchor = pattern.endswith("$")
    body = pattern[:-1] if anchor else pattern
    rx = ".*".join(re.escape(p) for p in body.split("*"))
    return re.compile("^" + rx + ("$" if anchor else ""))


def _robot_path(url):
    """The absolute path and query a robots.txt rule is matched against (RFC 9309 2.2)."""
    u = urllib.parse.urlparse(url)
    path = u.path or "/"
    return f"{path}?{u.query}" if u.query else path


class Robots:
    """RFC 9309 robots.txt matcher.

    Replaces `urllib.robotparser.RobotFileParser`, whose matcher treats an internal
    `*` and a trailing `$` as literal characters: `Disallow: /*.pdf$` and
    `Disallow: /a/*/c` both allowed the URLs they name. Here:

    * `*` matches any sequence of characters, `$` anchors the end of path-and-query;
    * rule precedence follows the length of the rule's path pattern — the behaviour
      of Google's own matcher, so `Disallow: /private` outranks `Allow: /*` — and
      `Allow` beats `Disallow` at equal length (RFC 9309 2.2.2: most octets wins,
      allow on ties);
    * the record set used is the one with the most specific matching `User-agent`
      token (`*` as fallback), records with equal tokens merged;
    * `Crawl-delay` is honoured, taking the longest delay among matching records.
    """

    def __init__(self, groups=None, sitemaps=None, allow_all=False, disallow_all=False):
        self.groups = groups or []        # [(tokens, [(allow, regex, spec_len)], delay)]
        self.sitemaps = list(sitemaps or [])
        self.allow_all = allow_all
        self.disallow_all = disallow_all

    # -- API used by the rest of geo-scan (kept robotparser-compatible) -------------
    def site_maps(self):
        return self.sitemaps or None

    def _matches(self, token, agent):
        token, agent = token.lower(), (agent or "").lower()
        return token == "*" or (token != "" and token in agent)

    def _record_for(self, agent):
        """(rules, delay) of the most specific matching record set, else None."""
        best_len, rules, delay = -1, [], None
        for tokens, group_rules, group_delay in self.groups:
            hit = [t for t in tokens if self._matches(t, agent)]
            if not hit:
                continue
            length = max(len(t) for t in hit)
            if length > best_len:
                best_len, rules, delay = length, list(group_rules), group_delay
            elif length == best_len:
                rules += group_rules
                if group_delay:
                    delay = group_delay if delay is None else max(delay, group_delay)
        return (rules, delay) if best_len >= 0 else (None, None)

    def can_fetch(self, agent, url):
        if self.allow_all:
            return True
        if self.disallow_all:
            return False
        found = self._record_for(agent)
        if found[0] is None:
            return True
        path = _robot_path(url)
        candidates = [path]
        unquoted = urllib.parse.unquote(path)
        if unquoted != path:
            candidates.append(unquoted)
        best, allowed = -1, True
        for allow, rx, spec in found[0]:
            if any(rx.match(c) for c in candidates) and (spec > best or (spec == best and allow)):
                best, allowed = spec, allow
        return allowed if best >= 0 else True

    def crawl_delay(self, agent):
        if self.allow_all or self.disallow_all:
            return None
        return self._record_for(agent)[1]


def load_robots(text):
    """Parse robots.txt into a `Robots` matcher (RFC 9309 group and rule syntax)."""
    groups, sitemaps = [], []
    tokens, rules, delay = [], [], None

    def flush():
        if tokens:
            groups.append((tokens, rules, delay))

    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip().lower()
        value = value.strip()
        if key == "user-agent":
            if rules and tokens:          # a new record starts after the rules
                flush()
                tokens, rules, delay = [], [], None
            if value:
                tokens.append(value)
        elif key in ("disallow", "allow"):
            if not value:
                continue                  # `Disallow:` alone means "allow everything"
            # specificity = length of the pattern as written. This is the behaviour
            # of Google's own matcher (google/robotstxt, robots.cc:
            # LongestMatchRobotsMatchStrategy returns `pattern.length()` as the
            # priority), which is what an audit must agree with: `Disallow:
            # /private` (8 octets) beats `Allow: /*` (2), not the other way round
            # as consumed-length ranking would make it.
            rules.append((key == "allow", _pattern_to_rx(value), len(value)))
        elif key == "crawl-delay":
            try:
                d = float(value)
                if d > 0:
                    delay = d if delay is None else max(delay, d)
            except ValueError:
                pass
        elif key == "sitemap":
            if value:
                sitemaps.append(value)
    flush()
    return Robots(groups, sitemaps)


def agent_access(rp, root, samples):
    """Per agent: 'blocked' (root disallowed), 'partial' (some samples disallowed), 'open'."""
    st = {}
    for bot in SEARCH_AGENTS + TRAINING_AGENTS:
        if not rp.can_fetch(bot, root):
            st[bot] = "blocked"
        elif all(rp.can_fetch(bot, u) for u in samples):
            st[bot] = "open"
        else:
            st[bot] = "partial"
    return st


# --------------------------------------------------------------------------- sitemaps

def _local(tag):
    return tag.rsplit("}", 1)[-1].lower() if isinstance(tag, str) else ""


def parse_sitemap(raw):
    """-> (kind, [(loc, lastmod)]); kind is 'sitemapindex', 'urlset' or another root tag."""
    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        # truncated or broken XML: salvage the <loc> entries, no lastmod
        text = raw.decode("utf-8", "replace")
        kind = "sitemapindex" if "<sitemapindex" in text else "urlset"
        return kind, [(u, "") for u in re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", text)]
    items = []
    for el in root:
        if _local(el.tag) not in ("url", "sitemap"):
            continue
        loc = lastmod = ""
        for c in el:
            if _local(c.tag) == "loc":
                loc = (c.text or "").strip()
            elif _local(c.tag) == "lastmod":
                lastmod = (c.text or "").strip()
        if loc:
            items.append((loc, lastmod))
    return _local(root.tag), items


def discover_sitemap(sc, rp, reserve=0):
    """Find a sitemap (robots.txt Sitemap: lines, /sitemap.xml, /wp-sitemap.xml), expand one index level.

    Child sitemaps after the first are skipped when they would eat into the time kept
    for `reserve` page fetches."""
    sources = list(rp.site_maps() or []) if hasattr(rp, "site_maps") else []
    sources += [sc.origin + "/sitemap.xml", sc.origin + "/wp-sitemap.xml"]
    seen, tried = set(), []
    for src in sources:
        if src in seen or len(tried) >= 3:
            continue
        seen.add(src)
        try:
            r = sc.fetch(src, CAP_SITEMAP)
        except Skipped as e:
            tried.append(f"{src}: skipped ({e})")
            sc.notes.append(f"{src}: skipped ({e})")
            continue
        except Exception as e:  # noqa: BLE001
            tried.append(f"{src}: {describe_error(e)}")
            continue
        kind, items = parse_sitemap(r.raw)
        if r.truncated:
            sc.notes.append(f"{src} larger than {CAP_SITEMAP // 2**20} MB; read truncated")
        if not items:
            tried.append(f"{src}: no <loc> entries")
            continue
        info = {"source": src, "children": 0, "expanded": 0}
        if kind == "sitemapindex":
            children = sorted(items, key=lambda t: t[1], reverse=True)
            info["children"] = len(children)
            pairs = []
            for i, (child, _) in enumerate(children[:MAX_CHILD_SITEMAPS]):
                if i and not sc.can_spare(reserve):
                    sc.notes.append(f"child sitemaps from {child} on: skipped to keep time "
                                    "budget for pages")
                    break
                try:
                    cr = sc.fetch(child, CAP_SITEMAP)
                except Skipped as e:
                    sc.notes.append(f"child sitemap {child}: skipped ({e})")
                    continue
                except Exception as e:  # noqa: BLE001
                    sc.notes.append(f"child sitemap {child}: {describe_error(e)}")
                    continue
                ckind, citems = parse_sitemap(cr.raw)
                if ckind == "sitemapindex":
                    sc.notes.append(f"child sitemap {child} is itself an index; not expanded")
                    continue
                info["expanded"] += 1
                pairs += citems
            items = pairs
        pages = [(lm, loc) for loc, lm in items
                 if not re.search(r"\.xml(\.gz)?$", urllib.parse.urlparse(loc).path)]
        if not pages:
            tried.append(f"{src}: no page URLs" + (" in the expanded child sitemaps"
                                                    if kind == "sitemapindex" else ""))
            continue
        info["urls"] = len(pages)
        info["with_lastmod"] = sum(1 for lm, _ in pages if lm)
        info["lastmods"] = [lm for lm, _ in pages if lm]
        pages.sort(key=lambda t: t[0], reverse=True)   # freshest first, undated last
        info["pages"] = [loc for _, loc in pages]
        return info, tried
    return None, tried


# --------------------------------------------------------------------------- page parsing

class Page(HTMLParser):
    """Collects the structural facts the scorer needs."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.lang = ""
        self.metas = {}
        self.robots_meta = []
        self.headings = {1: [], 2: [], 3: []}
        self.jsonld = []
        self.words = 0
        self.text = []
        self.list_items = 0
        self.tables = 0
        self.scripts = 0
        self.canonical = None
        self.img_total = 0
        self.img_no_alt = 0
        self.nosnippet = 0
        self._stack = []
        self._in_head = False
        self._skip = 0
        self._svg = 0
        self._title_done = False
        self._heading = None
        self._jsonld = None

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        if "data-nosnippet" in a:
            self.nosnippet += 1
        if tag == "html" and not self.lang:
            self.lang = a.get("lang", "").strip().lower()
        if tag == "head":
            self._in_head = True
        elif self._in_head and tag not in HEAD_TAGS:
            self._in_head = False   # body content without an explicit <body>
        if tag == "meta":
            key = (a.get("property") or a.get("name") or "").lower()
            if key:
                self.metas[key] = a.get("content", "")
            if key in ("robots", "googlebot", "bingbot"):
                self.robots_meta.append(a.get("content", ""))
        elif tag == "link" and "canonical" in a.get("rel", "").lower().split():
            self.canonical = a.get("href")
        elif tag == "img":
            self.img_total += 1
            if "alt" not in a:   # alt="" is correct for decorative images
                self.img_no_alt += 1
        elif tag == "li":
            self.list_items += 1
        elif tag == "table":
            self.tables += 1
        elif tag == "script":
            self.scripts += 1
            if a.get("type", "").lower().strip() == "application/ld+json":
                self._jsonld = []
        if tag in VOID:
            return
        if len(self._stack) >= MAX_DEPTH:
            # unclosed-tag soup: retire the outermost element so the stack stays bounded
            self._close(self._stack.pop(0))
        self._stack.append(tag)
        if tag in SKIP_TAGS:
            self._skip += 1
        elif tag == "svg":
            self._svg += 1
        elif tag in ("h1", "h2", "h3"):
            if self._heading:   # browsers close an open heading when another one starts
                self._flush_heading()
            self._heading = (int(tag[1]), [])

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        for i in range(len(self._stack) - 1, -1, -1):   # innermost match first
            if self._stack[i] == tag:
                break
        else:
            return
        while len(self._stack) > i:
            self._close(self._stack.pop())

    def _close(self, tag):
        if tag in SKIP_TAGS:
            self._skip = max(0, self._skip - 1)
        if tag == "svg":
            self._svg = max(0, self._svg - 1)
        elif tag == "head":
            self._in_head = False
        elif tag == "title" and not self._svg and self.title:
            self._title_done = True
        elif tag in ("h1", "h2", "h3") and self._heading and self._heading[0] == int(tag[1]):
            self._flush_heading()
        if tag == "script" and self._jsonld is not None:
            raw = "".join(self._jsonld)
            self._jsonld = None
            try:
                self.jsonld.append(json.loads(raw))
            except json.JSONDecodeError:
                self.jsonld.append({"_unparseable": raw[:80]})

    def _flush_heading(self):
        lvl, parts = self._heading
        self.headings[lvl].append(" ".join(parts)[:120])
        self._heading = None

    def handle_data(self, data):
        if self._jsonld is not None:
            self._jsonld.append(data)
            return
        text = data.strip()
        if not text:
            return
        top = self._stack[-1] if self._stack else ""
        if top == "title":
            if not self._svg and not self._title_done:
                self.title = (self.title + " " + text).strip()[:200]
            return
        if self._in_head and top in ("head", "html", ""):
            self._in_head = False
        if self._skip or self._in_head or self._svg:
            return
        self.words += len(text.split())
        if len(self.text) < 4000:
            self.text.append(text)
        if self._heading:
            self._heading[1].append(text)

    def finish(self):
        self.close()
        if self._heading:
            self._flush_heading()


def types_in(node, acc):
    if isinstance(node, dict):
        t = node.get("@type")
        if isinstance(t, str):
            acc.add(t)
        elif isinstance(t, list):
            acc.update(x for x in t if isinstance(x, str))
        for v in node.values():
            types_in(v, acc)
    elif isinstance(node, list):
        for v in node:
            types_in(v, acc)


def dates_in(node, acc):
    if isinstance(node, dict):
        for k in ("datePublished", "dateModified", "dateCreated"):
            if isinstance(node.get(k), str):
                acc.append(node[k])
        for v in node.values():
            dates_in(v, acc)
    elif isinstance(node, list):
        for v in node:
            dates_in(v, acc)


def parse_date(s):
    """Day-precision UTC timestamp from an ISO-ish date string, or None."""
    m = re.search(r"((?:19|20)\d{2})-(\d{2})-(\d{2})", s or "")
    if not m:
        return None
    try:
        y, mo, d = (int(x) for x in m.groups())
        time.strptime(f"{y}-{mo}-{d}", "%Y-%m-%d")
        return calendar.timegm((y, mo, d, 0, 0, 0, 0, 0, 0))
    except ValueError:
        return None


def snippet_directives(robots_meta, x_robots):
    """Lower-cased directives from meta robots/googlebot/bingbot and X-Robots-Tag headers."""
    out = set()
    values = list(robots_meta)
    for v in x_robots:
        # "googlebot: noindex" applies to that bot only; keep it for the bots we score
        m = re.match(r"\s*([\w-]+)\s*:\s*(.*)$", v)
        if m and m.group(1).lower() not in ("max-snippet", "max-image-preview",
                                             "max-video-preview", "unavailable_after"):
            if m.group(1).lower() not in ("googlebot", "bingbot", "all"):
                continue
            v = m.group(2)
        values.append(v)
    for v in values:
        for d in v.split(","):
            d = re.sub(r"\s+", "", d.lower())
            if d:
                out.add(d)
    return out


QUOTABLE = re.compile(
    r"(\bis defined as|\brefers to\b|\bmeans that\b|\bin short\b|\bthe difference between\b|"
    r"\bkey takeaways?\b|\bfor example\b|\be\.g\.|\bcompared to\b|\bthree (?:ways|steps|reasons)\b|"
    # German — the target market for this skill writes German, and an English-only
    # phrase list scored every German site near zero (45/45 <=8/20 on 2026-10-26).
    r"\bist definiert als\b|\bbezeichnet\b|\bbedeutet\b|\bkurz gesagt\b|\bzusammengefasst\b|"
    r"\bder unterschied zwischen\b|\bim vergleich\b|\bdas wichtigsten?[en]?\b|"
    r"\bzum beispiel\b|\bz\. ?B\.\b|\bauf einen blick\b|\bwissenswertes\b|"
    r"\bwie funktioniert\b|\bwas ist\b|\bwie lange\b|\bwie viel\b|\bwann\b|\bwer\b)",
    re.I)
# Figures: currency amounts, percentages, measured quantities. Plain durations
# ("5 min read", "30 days") are left out — they are mostly UI widgets.
STAT = re.compile(
    r"(?:[$€£]\s?\d[\d.,]*(?:\s?(?:k|m|bn|million|billion|euro|eur|cent|ct\.?)\b)?"
    r"|\d[\d.]{1,3}\s?(?:Euro|EUR|cent|Prozent|Minuten|Sekunden|Stunden|Tagen|Jahren|Monaten|"
    r"Km|km|kg|Kg|Meter|Metern|GB|MB|TB|ms|fach|mal)\b"
    r"|\b\d[\d.,]*\s?(?:%|percent\b|ms\b|GB\b|MB\b|TB\b|kg\b|km\b|USD\b|EUR\b|€|"
    r"million\b|billion\b|x\b))",
    re.I)
QUESTION_TITLE = re.compile(
    r"\?|\b(?:how|what|why|when|which|can you|does|is it)\b"
    r"|\b(?:wie|was|warum|weshalb|wann|welche?s?|kann man|sind|ist|brauche ich|lohnt)\b",
    re.I)


def analyse_page(url, html_body):
    p = Page()
    try:
        p.feed(html_body)
        p.finish()
    except Exception as e:  # noqa: BLE001 - a malformed page is a finding, not a crash
        return {"url": url, "error": f"parse: {e}"}
    types = set()
    for block in p.jsonld:
        types_in(block, types)
    dates = []
    for block in p.jsonld:
        dates_in(block, dates)
    text_blob = " ".join(p.text)
    return {
        "url": url,
        "title": p.title or p.metas.get("og:title", ""),
        "lang": p.lang,
        "words": p.words,
        "h1": len(p.headings[1]),
        "h2": len(p.headings[2]),
        "list_items": p.list_items,
        "tables": p.tables,
        "canonical": bool(p.canonical),
        "schema_types": sorted(types),
        "schema_score": sum(SCHEMA_GOOD.get(t, 0) for t in types),
        "description": bool(p.metas.get("description") or p.metas.get("og:description")),
        "author": bool(p.metas.get("author") or "person" in {t.lower() for t in types}),
        "og": bool(p.metas.get("og:title")),
        "dates": dates[:8],
        "img_no_alt": p.img_no_alt,
        "img_total": p.img_total,
        "robots_meta": p.robots_meta,
        "data_nosnippet": p.nosnippet,
        "scripts": p.scripts,
        "js_shell": p.words < 50 and p.scripts >= 3,
        "quotable_hits": len(QUOTABLE.findall(text_blob)),
        "stat_hits": len(STAT.findall(text_blob)),
        "question_title": bool(QUESTION_TITLE.search(p.title or "")),
    }


def _plain_text(resp):
    ct = (resp.headers.get("Content-Type") or "").lower()
    head = resp.text.lstrip()[:200].lower()
    return bool(resp.text.strip()) and "html" not in ct and not head.startswith(
        ("<!doctype", "<html", "<?xml", "<head", "<body"))


def _median(xs):
    xs = sorted(xs)
    return xs[len(xs) // 2] if xs else None


def _page_key(url):
    """Identity of a page across www./apex, scheme and trailing-slash variants."""
    u = urllib.parse.urlparse(url)
    return _site(u.hostname), u.path.rstrip("/") or "/", u.query


def _get_page(sc, url):
    """The response, or the exception that stopped it (reported where the page is scored)."""
    try:
        return sc.fetch(url, CAP_PAGE)
    except Exception as e:  # noqa: BLE001
        return e


# --------------------------------------------------------------------------- scan

def scan(root, max_pages=DEFAULT_PAGES, budget=DEFAULT_BUDGET, public_only=True, log=None):
    """Audit one site. Raises ScanError when nothing usable could be fetched.

    `public_only=True` is the default and the Hermes plugin never passes anything
    else: every address is validated before the socket opens, so a host cannot
    resolve public once and private afterwards.
    """
    max_pages = max(1, min(MAX_PAGES, int(max_pages)))
    # The declared ceiling is the ceiling: a caller cannot stretch the scan past
    # MAX_BUDGET, and the plugin asks for 90 s of that.
    budget = max(MIN_BUDGET, min(MAX_BUDGET, float(budget)))
    sc = Scanner(root, budget, public_only, log)
    if not sc.host:
        raise ScanError(f"not a URL: {root}")
    if public_only:
        try:
            sc.guard.approve(sc.host, urllib.parse.urlparse(root).port
                             or (443 if urllib.parse.urlparse(root).scheme == "https" else 80),
                             deadline=sc.deadline)
        except Skipped as e:
            raise ScanError(str(e)) from None
    f = {"root": root, "version": __version__, "checks": [], "pages": [], "notes": sc.notes,
         "signals": {"public_only": public_only}}
    if not public_only:
        sc.notes.append("public_only=false: this host was not required to be a public "
                        "address; the score is not comparable with a public audit")

    # 1. robots.txt — read first, then obeyed for every later request (RFC 9309)
    robots_note = ""
    rp = Robots(disallow_all=True)   # until the file says otherwise: fetch nothing
    try:
        r = sc.fetch(sc.origin + "/robots.txt", CAP_ROBOTS, obey=False)
        rp = load_robots(r.text)
        robots_note = f"robots.txt HTTP {r.code}" + ("" if r.text.strip() else " (empty)")
        if r.truncated:
            sc.notes.append("robots.txt over 512 KiB; only the first 512 KiB was parsed")
    except urllib.error.HTTPError as e:
        if 400 <= e.code < 500:
            rp.allow_all = True
            robots_note = f"robots.txt HTTP {e.code} = no restrictions (RFC 9309)"
        else:
            rp.disallow_all = True
            robots_note = f"robots.txt HTTP {e.code} = full disallow (RFC 9309: server error)"
    except Skipped as e:
        raise ScanError(f"robots.txt: {e}") from None
    except Exception as e:  # noqa: BLE001
        raise ScanError(f"robots.txt unreachable at {sc.origin}: {describe_error(e)}. "
                        "RFC 9309 treats an unreachable robots.txt as full disallow, so "
                        "geo-scan stops here.") from None
    sc.robots = rp
    cd = rp.crawl_delay(UA_TOKEN) if not (rp.allow_all or rp.disallow_all) else None
    if cd:
        sc.delay = max(MIN_DELAY, float(cd))
        sc.notes.append(f"Crawl-delay {cd}s honoured")

    # 2. the root page next, so a long Crawl-delay cannot starve it behind optional fetches
    fetched = {root: _get_page(sc, root)}
    reserve = min(PAGE_RESERVE, max_pages - 1)

    # 3. machine readability: llms.txt + sitemap; llms-full.txt last and only if time allows
    mach_pts, mach_ev = 0.0, []
    llms_ok = llms_full_ok = False
    try:
        r = sc.fetch(sc.origin + "/llms.txt", CAP_LLMS)
        if r.code == 200 and _plain_text(r):
            llms_ok = True
            mach_pts += 3
            size = f"≥{CAP_LLMS:,}" if r.truncated else f"{len(r.raw):,}"
            mach_ev.append(f"llms.txt present ({size} bytes)")
        elif r.code == 200:
            mach_ev.append("llms.txt answers with HTML (catch-all route), not counted")
    except Skipped as e:
        sc.notes.append(f"llms.txt: skipped ({e})")
    except Exception:  # noqa: BLE001
        pass

    sm, tried = discover_sitemap(sc, rp, reserve)
    if sm and sm["urls"]:
        cov = sm["with_lastmod"] / sm["urls"]
        mach_pts += 7 + 4 * cov
        src = urllib.parse.urlparse(sm["source"]).path
        mach_ev.insert(0, f"{src}: {sm['urls']} page URLs"
                          + (f" (from {sm['expanded']} of {sm['children']} child sitemaps)"
                             if sm["children"] else "")
                          + f", {sm['with_lastmod']} with <lastmod>")
        f["sitemap"] = {"source": sm["source"], "urls": sm["urls"],
                        "with_lastmod": sm["with_lastmod"], "pages": sm["pages"][:50]}
    else:
        mach_ev.insert(0, "no usable sitemap (" + "; ".join(tried)[:200] + ")")

    if llms_ok and not sc.can_spare(reserve):
        sc.notes.append("llms-full.txt: skipped to keep time budget for pages")
    elif llms_ok:
        try:
            r = sc.fetch(sc.origin + "/llms-full.txt", CAP_LLMS)
            if r.code == 200 and _plain_text(r):
                llms_full_ok = True
                mach_pts += 1
                size = f"≥{CAP_LLMS:,}" if r.truncated else f"{len(r.raw):,}"
                mach_ev.append(f"llms-full.txt present ({size} bytes)")
        except Skipped as e:
            sc.notes.append(f"llms-full.txt: skipped ({e})")
        except Exception:  # noqa: BLE001
            pass
    f["checks"].append({"id": "machine", "name": "Machine readability",
                        "score": round(min(15, mach_pts), 1), "max": 15,
                        "status": "ok" if mach_pts >= 9 else "thin",
                        "evidence": " · ".join(mach_ev)})

    # 4. page candidates: root + freshest sitemap URLs on the same site, each page once
    candidates = [root]
    seen = {_page_key(root)}
    if not isinstance(fetched[root], Exception):
        seen.add(_page_key(fetched[root].final_url))
    for u in (sm or {}).get("pages", []):
        if len(candidates) >= max_pages:
            break
        if sc.same_site(u) and _page_key(u) not in seen:
            seen.add(_page_key(u))
            candidates.append(u)
    samples = candidates[1:4]

    # 5. crawler access (search/retrieval agents score; training crawlers are reported)
    st = agent_access(rp, root, samples)
    val = {"open": 1.0, "partial": 0.5, "blocked": 0.0}
    search = {b: st[b] for b in SEARCH_AGENTS}
    crawl_pts = 20.0 * sum(val[v] for v in search.values()) / len(search)
    s_blocked = [b for b, v in search.items() if v == "blocked"]
    s_partial = [b for b, v in search.items() if v == "partial"]
    t_blocked = [b for b in TRAINING_AGENTS if st[b] == "blocked"]
    gate = len(s_blocked) == len(SEARCH_AGENTS)
    ev = [robots_note,
          f"{len(SEARCH_AGENTS) - len(s_blocked)}/{len(SEARCH_AGENTS)} search/retrieval agents may "
          f"fetch the root" + (f" and {len(samples)} sampled paths" if samples else "")]
    if s_blocked:
        ev.append(f"BLOCKED: {', '.join(s_blocked)}")
    if s_partial:
        ev.append(f"some sampled paths disallowed for {', '.join(s_partial)}")
    ev.append("training crawlers blocked (not scored): " + (", ".join(t_blocked) or "none"))
    f["checks"].insert(0, {"id": "robots", "name": "Crawler access (robots.txt)",
                           "score": round(crawl_pts, 1), "max": 20,
                           "status": "GATE: blocked" if gate else
                                     ("open" if crawl_pts == 20 else "restricted"),
                           "evidence": " · ".join(ev)})
    f["signals"] = {
        "llms_txt": llms_ok, "llms_full": llms_full_ok, "sitemap": bool(f.get("sitemap")),
        "sitemap_lastmod_coverage": round(sm["with_lastmod"] / sm["urls"], 2)
                                    if sm and sm["urls"] else 0,
        "robots_server_error": rp.disallow_all,
        "blocked_search_agents": s_blocked, "partial_search_agents": s_partial,
        "blocked_training_agents": t_blocked, "gate": gate,
        "public_only": sc.public_only,
    }

    # 6. pages (the root was fetched in step 2)
    struct_sum = quot_sum = 0.0
    snip_sum = 0.0
    snip_bad = {"noindex": 0, "nosnippet": 0, "data-nosnippet": 0}
    page_newest = []
    now = time.time()
    for u in candidates:
        r = fetched.pop(u) if u in fetched else _get_page(sc, u)
        if isinstance(r, Skipped):
            sc.notes.append(f"{u}: skipped ({r})")
            continue
        if isinstance(r, Exception):
            sc.notes.append(f"{u}: {describe_error(r)}")
            continue
        if not sc.same_site(r.final_url):
            sc.notes.append(f"{u}: redirects off-site to {r.final_url}; not scored")
            continue
        if r.final_url.rstrip("/") != u.rstrip("/"):
            sc.notes.append(f"{u}: redirects to {r.final_url}")
        ct = (r.headers.get("Content-Type") or "").lower()
        if ct and "html" not in ct:
            sc.notes.append(f"{u}: {ct.split(';')[0]}, not HTML; not scored")
            continue
        info = analyse_page(u, r.text)
        if "error" in info:
            sc.notes.append(f"{u}: {info['error']}")
            continue
        info.update(http=r.code, secs=r.secs, final_url=r.final_url, truncated=r.truncated)
        f["pages"].append(info)
        if info["js_shell"]:
            sc.notes.append(f"{u}: {info['words']} words of text and {info['scripts']} scripts — "
                            "looks JS-rendered; crawlers without JS see the same")
        # snippet rights
        d = snippet_directives(info["robots_meta"], r.headers.get_all("X-Robots-Tag") or [])
        info["directives"] = sorted(d)
        if d & {"noindex", "none"}:
            snip_bad["noindex"] += 1
        elif d & {"nosnippet", "max-snippet:0"}:
            snip_bad["nosnippet"] += 1
        elif info["data_nosnippet"]:
            snip_bad["data-nosnippet"] += 1
            snip_sum += 0.75
        else:
            snip_sum += 1
        # structure (8 points per page)
        s = 0
        s += info["h1"] == 1
        s += 2 if info["schema_score"] >= 4 else 0
        s += info["description"]
        s += info["author"]
        s += info["words"] >= 300
        s += info["list_items"] >= 5
        s += info["canonical"]
        struct_sum += s / 8.0
        # quotability (5 points per page)
        q = 0
        q += info["quotable_hits"] >= 2
        q += info["stat_hits"] >= 1
        q += info["tables"] >= 1
        q += info["question_title"]
        q += info["h2"] >= 2
        quot_sum += q / 5.0
        # freshness: this page's newest plausible date
        ds = [t for t in (parse_date(x) for x in info["dates"]) if t and t <= now + 86400]
        if ds:
            page_newest.append(max(ds))

    pages = f["pages"]
    if not pages and not gate:
        raise ScanError("no page could be fetched and analysed: "
                        + "; ".join(sc.notes[-3:] or ["no candidates"]))
    n = max(1, len(pages))

    snip_pts = 10 * snip_sum / n if pages else 0.0
    bad = [f"{k} on {v}" for k, v in snip_bad.items() if v]
    f["checks"].insert(2, {"id": "snippet", "name": "Snippet permissions",
                           "score": round(snip_pts, 1), "max": 10,
                           "status": "ok" if not bad else "RESTRICTED",
                           "evidence": ((f"{n - snip_bad['noindex'] - snip_bad['nosnippet']}/{n} pages "
                                         "may be indexed and quoted (meta robots, X-Robots-Tag)")
                                        if pages else "no page fetched")
                                       + (" · " + ", ".join(bad) if bad else "")})

    median_words = _median([p_["words"] for p_ in pages]) or 0
    with_schema = sum(1 for p_ in pages if p_["schema_score"] >= 4)
    one_h1 = sum(1 for p_ in pages if p_["h1"] == 1)
    struct_pts = 25 * struct_sum / n
    f["checks"].append({"id": "structure", "name": "Page structure",
                        "score": round(struct_pts, 1), "max": 25,
                        "status": "ok" if struct_pts >= 15 else "thin",
                        "evidence": f"{with_schema}/{n} pages carry article-level schema.org markup · "
                                    f"{one_h1}/{n} have exactly one <h1> · median word count {median_words}"})

    quot_pts = 20 * quot_sum / n
    qh = sum(p_["quotable_hits"] for p_ in pages)
    sh = sum(p_["stat_hits"] for p_ in pages)
    tb = sum(1 for p_ in pages if p_["tables"])
    f["checks"].append({"id": "quotable", "name": "Quotability",
                        "score": round(quot_pts, 1), "max": 20,
                        "status": "ok" if quot_pts >= 11 else "thin",
                        "evidence": f"{qh} definitional phrases, {sh} hard figures, tables on {tb}/{n} "
                                    f"pages · phrase lists: English + German"})

    fresh_pts, fresh_ev = 0.0, ""
    newest = _median(page_newest)
    source = f"median newest page date ({len(page_newest)}/{n} pages dated)"
    if newest is None and sm:
        lms = [t for t in (parse_date(x) for x in sm["lastmods"]) if t and t <= now + 86400]
        newest = _median(lms)
        source = f"median sitemap <lastmod> ({len(lms)} URLs; no page-level dates)"
    if newest is not None:
        age = (now - newest) / 86400
        fresh_pts = 10 if age <= 30 else 7 if age <= 120 else 4 if age <= 365 else 1
        fresh_ev = f"{source}: {age:.0f} days old"
    else:
        fresh_ev = "no machine-readable dates found"
    f["checks"].append({"id": "fresh", "name": "Freshness",
                        "score": float(fresh_pts), "max": 10,
                        "status": "ok" if fresh_pts >= 7 else "thin", "evidence": fresh_ev})

    langs = sorted({p_["lang"].split("-")[0] for p_ in pages if p_["lang"]} - {"en", "de"})
    if langs:
        sc.notes.append(f"page language {', '.join(langs)}: the quotability phrase lists cover "
                        "English and German, so that axis under-scores pages in other languages")

    total = sum(c["score"] for c in f["checks"])
    if gate:
        total = next(c["score"] for c in f["checks"] if c["id"] == "robots")
        sc.notes.insert(0, "GATE: no search/retrieval agent may fetch the root URL, so the total "
                           "is the crawler score alone; the other axes are shown for reference")
    f["score"] = round(total, 1)
    f["grade"] = ("A" if total >= 80 else "B" if total >= 65 else
                  "C" if total >= 50 else "D" if total >= 35 else "F")
    f["requests"] = sc.requests
    f["actions"] = actions(f)
    return f


def actions(f):
    acts = []
    sig = f.get("signals") or {}
    checks = {c["id"]: c for c in f["checks"]}
    if sig.get("robots_server_error"):
        acts.append(("high", "robots.txt returns a server error; RFC 9309 crawlers treat that as "
                             "'disallow everything'. Fix the error or serve a plain robots.txt."))
    elif sig.get("gate"):
        acts.append(("high", "robots.txt keeps every search/retrieval agent (Googlebot, Bingbot, "
                             "OAI-SearchBot, PerplexityBot, …) off the site; engines that obey it "
                             "cannot fetch or cite these pages."))
    elif sig.get("blocked_search_agents"):
        acts.append(("high", f"robots.txt blocks {', '.join(sig['blocked_search_agents'])}; those "
                             "search/retrieval agents cannot fetch pages to cite them. Training "
                             "crawlers can stay blocked independently."))
    if sig.get("partial_search_agents"):
        acts.append(("low", "Some sampled pages are disallowed for search/retrieval agents; confirm "
                            "the content you want cited is reachable."))
    if checks.get("snippet", {}).get("status") == "RESTRICTED":
        acts.append(("high", "Some pages carry noindex / nosnippet / max-snippet:0 / data-nosnippet; "
                             "Google will not quote that text in snippets or AI Overviews. Remove "
                             "it unless the restriction is intended."))
    if not sig.get("sitemap"):
        acts.append(("high", "Publish sitemap.xml with an accurate <lastmod> on every URL and list "
                             "it in robots.txt with a Sitemap: line."))
    elif sig.get("sitemap_lastmod_coverage", 0) < 0.5:
        acts.append(("medium", "Add an accurate <lastmod> to sitemap URLs (only change it when the "
                               "content changes)."))
    if checks.get("structure", {}).get("score", 0) < 15:
        acts.append(("medium", "Add JSON-LD that matches the visible content (Article/BlogPosting "
                               "with author and dateModified, BreadcrumbList); keep exactly one "
                               "<h1> per page. Use FAQPage only on pages that really are FAQs."))
    if checks.get("quotable", {}).get("score", 0) < 11:
        acts.append(("medium", "Add a 40-60 word definitional answer plus one hard figure or comparison "
                               "table near the top of each page — that is the block engines quote."))
    if checks.get("fresh", {}).get("score", 0) < 7:
        acts.append(("medium", "Refresh or retire stale pages and expose an honest dateModified."))
    if not sig.get("llms_txt"):
        acts.append(("low", "Optional: llms.txt is a proposal with no confirmed consumer among the "
                            "major engines (Google says it does not use it). Publish one only if it "
                            "is cheap to maintain."))
    return acts


def to_md(f):
    lines = [f"# Answer-engine readiness — {f['root']}",
             "",
             f"**Score {f['score']}/100 · grade {f['grade']}** · geo-scan {f.get('version', __version__)} · "
             f"{time.strftime('%Y-%m-%d %H:%M %Z')} · {f.get('requests', '?')} requests",
             "",
             "| axis | score | status | evidence |",
             "|---|---|---|---|"]
    for c in f["checks"]:
        lines.append(f"| {c['name']} | {c['score']}/{c['max']} | {c['status']} | {c['evidence']} |")
    lines += ["", "## Actions", ""]
    for prio, text in f["actions"]:
        lines.append(f"- **{prio}** — {text}")
    if f["pages"]:
        lines += ["", "## Pages", "",
                  "| url | words | h1 | schema | figures | quotes | robots directives |",
                  "|---|---|---|---|---|---|---|"]
        for p_ in f["pages"][:25]:
            lines.append(f"| {p_['url']} | {p_['words']} | {p_['h1']} | "
                         f"{','.join(p_['schema_types'])[:40] or '—'} | {p_['stat_hits']} | "
                         f"{p_['quotable_hits']} | {','.join(p_.get('directives', [])) or '—'} |")
    if f["notes"]:
        lines += ["", "## Notes", ""] + [f"- {n}" for n in f["notes"][:15]]
    lines += ["", "_Weights are geo-scan's judgement, not validated against observed citations. "
                  "CDN/WAF bot blocking and JS rendering are invisible to this tool._"]
    return "\n".join(lines) + "\n"


def _report_path(out_dir, name, base=None):
    """Confine a caller-named report to out_dir; refuse traversal and symlinks.

    out_dir itself must live inside `base` (the working directory by default) and must
    not be a symlink; the report name may be bare (`report.json`) or relative inside
    out_dir (`2026/report.json`). An absolute name, a `..` escape, or a target that is
    already a symlink is refused: the contract says writes go under out_dir, so that
    is what the code does.
    """
    base = Path(base or Path.cwd()).resolve()
    if ".." in Path(out_dir).parts or ".." in Path(name).parts:
        raise ScanError("'..' is not allowed in --out-dir or a report name")
    root = Path(out_dir).expanduser()
    if root.is_symlink():
        raise ScanError(f"--out-dir must not be a symlink: {out_dir}")
    root = root.resolve()
    if root != base and base not in root.parents:
        raise ScanError(f"--out-dir must be inside the working directory ({base}): {out_dir}")
    given = Path(name).expanduser()
    if given.is_absolute():
        raise ScanError(f"report name must be inside --out-dir ({out_dir}), not absolute: {name}")
    target = (root / given).resolve()
    if target != root and root not in target.parents:
        raise ScanError(f"report name escapes --out-dir ({out_dir}): {name}")
    if target.is_symlink():
        raise ScanError(f"refusing to write through an existing symlink: {name}")
    root.mkdir(parents=True, exist_ok=True)
    return target


def main():
    ap = argparse.ArgumentParser(description="Answer-engine readiness audit (no API key).")
    ap.add_argument("url", nargs="?", help="site to audit")
    ap.add_argument("--url", dest="url_opt", help="site to audit (alternative to the positional)")
    ap.add_argument("--pages", type=int, default=DEFAULT_PAGES,
                    help=f"pages to sample, 1-{MAX_PAGES} (default {DEFAULT_PAGES})")
    ap.add_argument("--budget", type=int, default=DEFAULT_BUDGET,
                    help=f"max seconds for the whole scan (default {DEFAULT_BUDGET}, "
                         f"hard ceiling {MAX_BUDGET})")
    ap.add_argument("--json", dest="json_out", metavar="NAME",
                    help="write the JSON report as this name inside --out-dir")
    ap.add_argument("--md", dest="md_out", metavar="NAME",
                    help="write the Markdown report as this name inside --out-dir")
    ap.add_argument("--out-dir", dest="out_dir", default=DEFAULT_OUT_DIR,
                    help=f"directory reports may be written to (default {DEFAULT_OUT_DIR}/); "
                         "--json/--md cannot point outside it")
    ap.add_argument("--quiet", action="store_true", help="no output; exit code only")
    ap.add_argument("--allow-private", dest="allow_private", action="store_true",
                    help="dial private/loopback/link-local HTTP(S) addresses too (staging "
                         "boxes); off by default, and the report is marked as not a public "
                         "audit. Never re-enables ftp:, file: or any other scheme")
    ap.add_argument("--version", action="version", version=f"geo-scan {__version__}")
    args = ap.parse_args()

    url = args.url_opt or args.url
    if not url:
        ap.error("a URL is required")
    root = url if "://" in url else "https://" + url
    pages = max(1, min(MAX_PAGES, args.pages))
    if pages != args.pages and not args.quiet:
        print(f"geo-scan: --pages clamped to {pages} (allowed 1-{MAX_PAGES})", file=sys.stderr)
    budget = max(MIN_BUDGET, min(MAX_BUDGET, args.budget))
    if budget != args.budget and not args.quiet:
        print(f"geo-scan: --budget clamped to {budget} s (allowed "
              f"{MIN_BUDGET}-{MAX_BUDGET})", file=sys.stderr)
    if args.allow_private and not args.quiet:
        print("geo-scan: --allow-private is set: this run may dial hosts outside the public "
              "internet over http(s), so its score is not comparable with a public audit",
              file=sys.stderr)
    log = None if args.quiet else (lambda msg: print(msg, file=sys.stderr, flush=True))
    try:
        f = scan(root, max_pages=pages, budget=budget, log=log,
                 public_only=not args.allow_private)
    except ScanError as e:
        if not args.quiet:
            print(f"geo-scan: {e}", file=sys.stderr)
        return 2
    except Exception as e:  # noqa: BLE001
        if not args.quiet:
            print(f"geo-scan: fatal: {e}", file=sys.stderr)
        return 2
    if not args.quiet:
        print(to_md(f))
    try:
        if args.json_out:
            slim = {k: v for k, v in f.items() if k != "pages"}
            slim["pages"] = [{k: v for k, v in p_.items() if k != "title"} for p_ in f["pages"]]
            with open(_report_path(args.out_dir, args.json_out), "w", encoding="utf-8") as fh:
                json.dump(slim, fh, indent=1)
        if args.md_out:
            with open(_report_path(args.out_dir, args.md_out), "w", encoding="utf-8") as fh:
                fh.write(to_md(f))
    except ScanError as e:
        if not args.quiet:
            print(f"geo-scan: {e}", file=sys.stderr)
        return 2
    except OSError as e:
        if not args.quiet:
            print(f"geo-scan: cannot write {e.filename or 'output'}: {e.strerror or e}",
                  file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
