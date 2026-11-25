#!/usr/bin/env python3
"""Guard tests for geo-scan — run: python3 test_guard.py

Two rules hold here: no network, and no socket to any host. DNS answers come from a
stub resolver and the socket layer is replaced by a recorder that fails the test if
anything opens one — so what these check is the decision geo-scan makes and the
address it would hand to a socket, never a real connection. Exit 0 = all pass.
"""
import ipaddress
import os
import socket
import sys
import tempfile
from pathlib import Path

import geo_scan as gs

REFUSE = [
    "127.0.0.1", "127.5.5.5", "::1", "0.0.0.0", "10.0.0.1", "172.16.9.9",
    "192.168.1.1", "169.254.169.254", "169.254.255.254", "100.64.0.1",
    "100.127.255.255", "192.0.2.1", "198.51.100.7", "203.0.113.9", "224.0.0.1",
    "239.10.10.10", "240.0.0.1", "fd00::1", "fe80::1", "ffff::",
    "::ffff:127.0.0.1", "::ffff:10.0.0.1", "2002:7f00:0001::",       # 6to4 -> 127.0.0.1
    "2002:0a00:0001::",                                                  # 6to4 -> 10.0.0.1
    "2001:0000:4136:e378:8000:63bf:3fff:fdd2",                        # Teredo, client IPv4
]
ACCEPT = ["93.184.216.34", "8.8.8.8", "1.1.1.1", "2606:4700:4700::1111",
          "2a00:1450:4008:801::200e"]

checks = []
fails = []


def check(name, ok):
    checks.append(name)
    if not ok:
        fails.append(name)
    return ok


# --- address decisions -----------------------------------------------------------------
for s in REFUSE:
    check(f"refuse {s}", not gs.ip_is_public(ipaddress.ip_address(s)))
for s in ACCEPT:
    check(f"accept {s}", gs.ip_is_public(ipaddress.ip_address(s)))

# literal hosts go through the same decision, without DNS
for s in ["127.0.0.1", "169.254.169.254", "10.0.0.1"]:
    try:
        gs.resolve_public_ips(s, 80)
        check(f"literal {s} refused", False)
    except gs.Skipped:
        check(f"literal {s} refused", True)

# a host that answers publicly once and privately afterwards (DNS rebinding):
# the guard is asked again at connect time, so the private answer is what it sees
answers = [(2, "93.184.216.34"), (2, "127.0.0.1"), (2, "169.254.169.254")]
real = socket.getaddrinfo
seq = iter(answers)


def stub(host, port, *a, **k):
    fam, ip = next(seq)
    return [(fam, 1, 6, "", (ip, port))]


socket.getaddrinfo = stub
try:
    check("first DNS answer is the public one",
          gs.resolve_public_ips("rebind.test", 80) == [(4, "93.184.216.34")])
    for i in (2, 3):
        try:
            gs.resolve_public_ips("rebind.test", 80)
            check(f"rebinding answer #{i} refused", False)
        except gs.Skipped:
            check(f"rebinding answer #{i} refused", True)
finally:
    socket.getaddrinfo = real


# --- no sockets, no schemes outside http(s) --------------------------------------------
class NoSocket(socket.socket):
    """Fails the suite if any handler gets as far as opening a socket."""

    def __init__(self, *a, **k):
        raise AssertionError("a socket was opened by a test that must not connect")


def with_no_sockets(fn):
    """Run fn with socket.socket and getaddrinfo removed; return (raised, message)."""
    gai = socket.getaddrinfo
    so = socket.socket
    socket.getaddrinfo = lambda *a, **k: (_ for _ in ()).throw(
        AssertionError("DNS was resolved by a test that must not resolve"))
    socket.socket = NoSocket
    try:
        fn()
        return None, "no exception at all"
    except gs.Skipped as e:
        return "Skipped", str(e)
    except AssertionError as e:
        return "socket", str(e)
    except Exception as e:  # noqa: BLE001
        return type(e).__name__, str(e)
    finally:
        socket.getaddrinfo, socket.socket = gai, so


sc = gs.Scanner("https://example.com", budget=30, public_only=True)
names = sorted(type(h).__name__ for h in sc._opener.handlers)
for bad in ("FTPHandler", "FileHandler", "DataHandler"):
    check(f"opener carries no {bad}", bad not in names)
check("opener carries the validated http handler", "_ValidatedHTTPHandler" in names)
check("opener carries the validated https handler", "_ValidatedHTTPSHandler" in names)

for url in ("ftp://example.com:21/secret/sitemap.xml",
            "file://localhost/etc/passwd",
            "file:///etc/passwd",
            "file://example.com/etc/shadow",
            "data:text/html,<script>alert(1)</script>",
            "gopher://example.com:70/x",
            "dict://example.com:11211/stat"):
    kind, msg = with_no_sockets(lambda u=url: sc.fetch(u, 4096, obey=False))
    check(f"{url.split(':')[0]}: refused before DNS/socket "
          f"({kind}): {msg[:60]}", kind == "Skipped" and "scheme" in msg)

# and with --allow-private, where the address gate is off, the scheme gate still holds
sc_priv = gs.Scanner("http://127.0.0.1:9/", budget=30, public_only=False)
for url in ("ftp://127.0.0.1:21/x", "file://localhost/etc/passwd"):
    kind, msg = with_no_sockets(lambda u=url: sc_priv.fetch(u, 4096, obey=False))
    check(f"allow-private still refuses {url.split(':')[0]}", kind == "Skipped")

# a non-http scheme is refused at construction, too
try:
    gs.Scanner("file:///etc/passwd", 30, True, None)
    check("file:// root refused", False)
except gs.ScanError:
    check("file:// root refused", True)

# a refused host never reaches the socket layer
try:
    gs.scan("http://127.0.0.1:9/", max_pages=1, budget=10)
    check("loopback root refused", False)
except gs.ScanError as e:
    check(f"loopback root refused ({str(e)[:40]})", "private" in str(e))


# --- robots.txt: RFC 9309 matching ----------------------------------------------------
ROBOTS = """
User-agent: *
Disallow: /private
Allow: /private/public
Crawl-delay: 7
Sitemap: https://example.com/sitemap.xml

User-agent: geo-scan
Disallow: /*.pdf$
Disallow: /a/*/c
Disallow: /*?print=1
Allow: /printable?print=1
Crawl-delay: 2
Sitemap: https://example.com/sitemap-geo.xml
"""
rp = gs.load_robots(ROBOTS)
ROBOT_CASES = [
    # RFC 9309 2.2.2.3: the most specific matching record governs. geo-scan has its
    # own record here, so the `*` record's /private does not apply to geo-scan —
    # that is what the standard says, and what Google's own checker does. The
    # Googlebot cases below prove the `*` record is still enforced for everyone else.
    ("/private", True, "own record replaces the * record"),
    ("/private/public", True, "longest-match Allow wins"),
    ("/report.pdf", False, "internal wildcard + end anchor"),
    ("/deep/path/report.pdf", False, "wildcard spans slashes"),
    ("/report.html", True, "anchored pattern does not over-match"),
    ("/a/b/c", False, "internal wildcard"),
    ("/a/b/d", True, "internal wildcard non-match"),
    ("/page?print=1", False, "query wildcard"),
    ("/printable?print=1", True, "Allow beats Disallow at equal length"),
    ("/page?print=0", True, "anchored query non-match"),
]
for path, want, label in ROBOT_CASES:
    got = rp.can_fetch("geo-scan", "https://example.com" + path)
    check(f"robots geo-scan {label} ({path})", got == want)
check("robots.txt: * record enforced for a bot with no own record",
      rp.can_fetch("Googlebot", "https://example.com/private") is False)
check("robots.txt: * record's Allow exception still opens /private/public",
      rp.can_fetch("Googlebot", "https://example.com/private/public") is True)
check("robots.txt: Googlebot uses the * record, unmatched path open",
      rp.can_fetch("Googlebot", "https://example.com/printable?print=1") is True)
check("Crawl-delay of the matching record (2s)", rp.crawl_delay("geo-scan") == 2.0)
check("Crawl-delay of the * record (7s)", rp.crawl_delay("Bingbot") == 7.0)
check("Sitemap lines collected for both records",
      rp.site_maps() == ["https://example.com/sitemap.xml",
                         "https://example.com/sitemap-geo.xml"])
check("Disallow: alone allows everything",
      gs.load_robots("User-agent: *\nDisallow:\n").can_fetch("geo-scan", "https://x.test/a") is True)
check("empty robots.txt allows everything",
      gs.load_robots("").can_fetch("geo-scan", "https://x.test/a") is True)
check("comment and casing tolerated",
      gs.load_robots("USER-AGENT: *  # all bots\nDISALLOW: /x\n").can_fetch("geo-scan", "https://x.test/x") is False)
check("percent-encoded path still matches",
      gs.load_robots("User-agent: *\nDisallow: /a b\n").can_fetch("geo-scan", "https://x.test/a%20b") is False)

# the scanner's own root fetch: robots.txt with an ftp: Sitemap must not be fetched
kind, msg = with_no_sockets(lambda: sc.fetch("ftp://example.com/sitemap.xml", 4096, obey=False))
check("robots Sitemap: ftp:// is skipped, not fetched", kind == "Skipped")


# --- redirect chains: paced, capped, deadline-bound ---------------------------------
import io  # noqa: E402
import time as _time  # noqa: E402
import urllib.request as _ur  # noqa: E402

sc2 = gs.Scanner("https://example.com", budget=30, public_only=True)
sc2.delay = 0.0
rd = next(h for h in sc2._opener.handlers if isinstance(h, gs._GuardedRedirect))
check("redirect handler is paced by the scanner itself",
      getattr(rd._pace, "__self__", None) is sc2
      and rd._pace.__func__ is gs.Scanner._pace_redirect)
hd = next(h for h in sc2._opener.handlers if isinstance(h, gs._ValidatedHTTPHandler))
hsd = next(h for h in sc2._opener.handlers if isinstance(h, gs._ValidatedHTTPSHandler))
check("http handler carries the scan deadline to connect", hd._deadline == sc2.deadline)
check("https handler carries the scan deadline to connect", hsd._deadline == sc2.deadline)

_gai = socket.getaddrinfo
socket.getaddrinfo = lambda h, p, *a, **k: [(socket.AF_INET, 1, 6, "", ("93.184.216.34", p))]
try:
    # a chain of same-host hops, mimicking urllib's per-chain redirect_dict
    req = _ur.Request("https://example.com/start")
    kinds, lastmsg = [], ""
    for i in range(1, 7):
        u = f"https://example.com/h{i}"
        try:
            out = rd.redirect_request(req, io.BytesIO(b""), 302, "Found", {}, u)
            kinds.append("ok")
            req = out
            req.redirect_dict = {u: 1}
        except gs.Skipped as e:
            lastmsg = str(e)
            break
    check("same-host chain follows 4 hops", kinds.count("ok") == 4)
    check(f"5th hop refused by the chain cap ({lastmsg[:40]})", "hops" in lastmsg)
    req2 = _ur.Request("https://example.com/fresh")
    out2 = rd.redirect_request(req2, io.BytesIO(b""), 301, "Moved", {},
                               "https://example.com/new")
    check("new chain resets the hop counter",
          out2 is not None and out2.full_url.endswith("/new"))
    # the deadline reaches all the way down into the dial
    conn = gs._ValidatedHTTPConnection("example.com", 80, timeout=15,
                                        guard=gs.HostGuard(True, None),
                                        deadline=_time.monotonic() - 5)
    try:
        conn.connect()
        check("spent deadline stops the dial itself", False)
    except gs.Skipped as e:
        check("spent deadline stops the dial itself", "budget" in str(e))
finally:
    socket.getaddrinfo = _gai

kind, msg = with_no_sockets(lambda: gs._validated_socket(
    "example.com", 443, [(4, "93.184.216.34")], 15, None,
    deadline=_time.monotonic() - 1))
check("_validated_socket refuses to dial past the deadline",
      kind == "Skipped" and "budget" in msg)

sc4 = gs.Scanner("https://example.com", budget=30)
sc4.delay = 0.35
sc4._last = _time.monotonic()
t0 = _time.monotonic()
sc4._pace_redirect()
check("redirect hop waits out the crawl delay", _time.monotonic() - t0 >= 0.30)

sc5 = gs.Scanner("https://example.com", budget=30)
sc5.deadline = _time.monotonic() + 0.5
t0 = _time.monotonic()
try:
    sc5._pace_redirect()
    check("hop refused when the budget is spent", False)
except gs.Skipped as e:
    check("hop refused when the budget is spent, without sleeping",
          "budget" in str(e) and _time.monotonic() - t0 < 0.2)


# --- budgets and report paths ----------------------------------------------------------
check("--budget above the ceiling is clamped",
      gs.Scanner("https://example.com", budget=10 ** 6, public_only=True).deadline
      - gs.time.monotonic() <= gs.MAX_BUDGET + 1)
check("--budget below the floor is clamped up",
      gs.Scanner("https://example.com", budget=1, public_only=True).deadline
      - gs.time.monotonic() >= gs.MIN_BUDGET - 1)

_here = Path.cwd()
with tempfile.TemporaryDirectory() as td:
    os.chdir(td)
    try:
        try:
            gs._report_path(td, "/tmp/escaped.json")
            check("absolute report name refused", False)
        except gs.ScanError:
            check("absolute report name refused", True)
        try:
            gs._report_path(td, "../escaped.json")
            check("traversal report name refused", False)
        except gs.ScanError:
            check("traversal report name refused", True)
        try:
            gs._report_path("../elsewhere", "x.json")
            check("'..' in out_dir refused", False)
        except gs.ScanError:
            check("'..' in out_dir refused", True)
        try:
            gs._report_path("/tmp/elsewhere", "x.json")
            check("out_dir outside the working dir refused", False)
        except gs.ScanError:
            check("out_dir outside the working dir refused", True)
        link = Path(td) / "reports"
        Path(td, "outside").mkdir()
        link.symlink_to(Path(td) / "outside")
        try:
            gs._report_path(str(link), "x.json")
            check("symlinked out_dir refused", False)
        except gs.ScanError:
            check("symlinked out_dir refused", True)
        existing = Path(td) / "out"
        existing.mkdir()
        (existing / "Taken.json").write_text("do not truncate me", encoding="utf-8")
        p = gs._report_path("out", "sub/report.json")
        check("relative report stays inside out_dir",
              str(p).startswith(str(existing.resolve())) and str(p).endswith("sub/report.json"))
        q = gs._report_path("out", "Taken.json")
        check("a named report resolves to the file inside out_dir",
              q == (existing / "Taken.json").resolve())
    finally:
        os.chdir(_here)

# --- the plugin wrapper's own boundary -------------------------------------------------
# loaded the way Hermes loads it: the repo root as a package, __init__ as the entry
import importlib.util  # noqa: E402

spec = importlib.util.spec_from_file_location("geo_scan_plugin", "__init__.py",
                                              submodule_search_locations=[str(Path.cwd())])
plugin = importlib.util.module_from_spec(spec)
sys.modules["geo_scan_plugin"] = plugin
spec.loader.exec_module(plugin)

check("plugin: out_dir default is the scratch dir",
      str(plugin._confined_out_dir(None)).endswith(".hermes/cache/scratch/geo-scan"))
for bad in ("/tmp/pwn", "../../etc", "~/.ssh/keys", str(Path.home() / ".hermes" / "config.yaml")):
    try:
        plugin._confined_out_dir(bad)
        check(f"plugin: out_dir {bad} refused", False)
    except ValueError:
        check(f"plugin: out_dir {bad} refused", True)
inside = str(Path.home() / ".hermes" / "cache" / "scratch" / "geo-scan")
check("plugin: out_dir under cache accepted",
      str(plugin._confined_out_dir(inside)) == str(Path(inside).resolve()))
check("plugin: budget stays 90 s of the 120 s ceiling",
      plugin._BUDGET_SECONDS <= gs.MAX_BUDGET)

# ------------------------------------------- 1.2.8: the four registry findings, 2026-11-23

# robots precedence follows Google's own matcher: priority = pattern length
# (google/robotstxt robots.cc, LongestMatchRobotsMatchStrategy), not length consumed
_rp = gs.load_robots("User-agent: *\nAllow: /*\nDisallow: /private\n")
check("google parity: broad Allow /* cannot out-rank Disallow /private",
      _rp.can_fetch("geo-scan", "https://x.test/private/page") is False)
check("google parity: path outside the disallow stays allowed",
      _rp.can_fetch("geo-scan", "https://x.test/public/a.pdf") is True)
check("google parity: RFC 9309 5.2 — the longer rule still wins",
      gs.load_robots("User-agent: foobot\nAllow: /example/page/\n"
                     "Disallow: /example/page/disallowed.gif\n")
      .can_fetch("foobot", "https://x.test/example/page/disallowed.gif") is False)
check("google parity: equal patterns, Allow wins (RFC 9309 2.2.2)",
      gs.load_robots("User-agent: *\nAllow: /ab\nDisallow: /ab\n")
      .can_fetch("x", "https://x.test/ab/c") is True)
check("google parity: Disallow / loses to a deeper Allow",
      gs.load_robots("User-agent: *\nDisallow: /\nAllow: /foo/bar.html\n")
      .can_fetch("x", "https://x.test/foo/bar.html") is True)

# DNS sits inside the declared ceiling: a resolver that never answers cannot
# park the scan past its own budget
_gai3 = socket.getaddrinfo


def _slow_resolv(host, port, *a, **k):
    _time.sleep(2.0)
    raise socket.gaierror("never answers")


socket.getaddrinfo = _slow_resolv
try:
    t0 = _time.monotonic()
    try:
        gs.resolve_public_ips("dial-wait.test", 80, deadline=_time.monotonic() + 0.3)
        check("stalled resolver refused at the deadline", False)
    except gs.Skipped as e:
        el = _time.monotonic() - t0
        check("stalled resolver refused at the deadline", "deadline" in str(e))
        check(f"resolver wait bounded ({el:.2f} s)", el < 1.5)
finally:
    socket.getaddrinfo = _gai3

# the deadline reaches the resolver through every approve() path
_seen_kw = []


class _WireGuard:
    public_only = True

    def approve(self, host, port, deadline=None):
        _seen_kw.append(deadline)
        return [(4, "93.184.216.34")]


sc_wg = gs.Scanner("https://wire.test/", 30)
sc_wg.guard = _WireGuard()
sc_wg._guard("https://wire.test/x")
check("preflight passes the scan deadline to the guard",
      len(_seen_kw) == 1 and _seen_kw[0] == sc_wg.deadline)
_hd = next(h for h in sc_wg._opener.handlers if isinstance(h, gs._ValidatedHTTPHandler))
_hsd = next(h for h in sc_wg._opener.handlers if isinstance(h, gs._ValidatedHTTPSHandler))
check("http handler carries the watchdog register", _hd._register == sc_wg._register)
check("https handler carries the watchdog register", _hsd._register == sc_wg._register)

# the watchdog: first register arms it, abort cuts the live socket (shutdown then
# close — close alone would not wake a blocked recv), a second abort is inert
class _DummySock:
    def __init__(self):
        self.closed = False

    def shutdown(self, how):
        pass

    def close(self):
        self.closed = True


sc_wd = gs.Scanner("https://wd.test/", 30)
_d = _DummySock()
sc_wd._register(_d)
check("watchdog armed by the first registered socket",
      sc_wd._watchdog is not None and sc_wd._watchdog.is_alive())
sc_wd._abort_live()
check("watchdog shuts and closes the live socket", _d.closed is True)
check("abort flag set for the honest timeout message", sc_wd._aborted is True)
sc_wd._abort_live()
check("a second abort changes nothing", sc_wd._live is None and _d.closed is True)
sc_wd._watchdog.cancel()

# bench.py reads only reports that resolve inside the working directory (SDI-3)
import bench as _bench  # noqa: E402

for bad in ("/etc/passwd", "../outside.json"):
    try:
        _bench.contained(bad)
        check(f"bench refuses {bad}", False)
    except ValueError:
        check(f"bench refuses {bad}", True)
check("bench keeps a relative report path",
      str(_bench.contained("out/r.json")).endswith("out/r.json"))

print(f"geo-scan {gs.__version__} guard tests: {len(checks) - len(fails)} passed, "
      f"{len(fails)} failed")
for f in fails:
    print("  FAIL", f)
sys.exit(1 if fails else 0)
