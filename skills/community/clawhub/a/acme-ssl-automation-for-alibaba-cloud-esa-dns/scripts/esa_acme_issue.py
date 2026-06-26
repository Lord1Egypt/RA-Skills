#!/usr/bin/env python3
import argparse
import base64
import datetime
import hashlib
import hmac
import ipaddress
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid



DEFAULT_CMD_TIMEOUT = 300
DIG_CMD_TIMEOUT = 20
ACME_CMD_TIMEOUT_PADDING = 900
ESA_REQ_MAX_ATTEMPTS = 3
AK_ENV_NAMES = ("ALIYUN_AK", "ALIBABACLOUD_ACCESS_KEY_ID")
SK_ENV_NAMES = ("ALIYUN_SK", "ALIBABACLOUD_ACCESS_KEY_SECRET")
STS_ENV_NAMES = ("ALIYUN_SECURITY_TOKEN", "ALIBABACLOUD_SECURITY_TOKEN")
ESA_REGION_ENV_NAMES = ("ALIYUN_ESA_REGION", "ALIBABACLOUD_ESA_REGION", "ESA_REGION")


def run(cmd, timeout=DEFAULT_CMD_TIMEOUT):
    try:
        p = subprocess.run(cmd, text=True, capture_output=True, timeout=timeout)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except FileNotFoundError:
        return 127, f"[ERR] command not found: {cmd[0]}"
    except OSError as e:
        return 127, f"[ERR] failed to execute command: {' '.join(cmd)} ({e})"
    except subprocess.TimeoutExpired as e:
        out = (e.stdout or "") + (e.stderr or "")
        out += f"\n[ERR] command timed out after {timeout}s: {' '.join(cmd)}"
        return 124, out


def redact_text(text, secrets=None):
    out = text or ""
    secrets = [s for s in (secrets or []) if s]
    for s in secrets:
        out = out.replace(s, "***REDACTED***")
    # basic AccessKeyId pattern mask
    out = re.sub(r"LTAI[0-9A-Za-z]{12,}", "LTAI***REDACTED***", out)
    return out


def first_env(*names):
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    return None


def is_valid_host(host):
    if not host or len(host) > 253 or host.startswith("*.") or ".." in host:
        return False
    labels = host.rstrip(".").split(".")
    for label in labels:
        if not re.fullmatch(r"[A-Za-z0-9-]{1,63}", label):
            return False
        if label.startswith("-") or label.endswith("-"):
            return False
    return True


def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def normalize_ip(ip):
    return str(ipaddress.ip_address(ip))


def is_valid_domain_for_cert(domain):
    if not domain:
        return False
    if domain.startswith("*."):
        return is_valid_host(domain[2:])
    return is_valid_host(domain)


def normalize_domains(domains):
    normalized = []
    for domain in domains or []:
        value = (domain or "").strip()
        if not value:
            continue
        if not is_valid_domain_for_cert(value):
            raise ValueError(f"invalid domain: {domain}")
        if value not in normalized:
            normalized.append(value)
    if not normalized:
        raise ValueError("no valid domains provided")
    return normalized


def build_domain_plan(domains):
    normalized = normalize_domains(domains)
    primary_domain = next((d for d in normalized if not d.startswith("*.")), normalized[0])
    issue_domains = [primary_domain] + [d for d in normalized if d != primary_domain]
    cert_basename = next((d for d in normalized if not d.startswith("*.")), primary_domain.lstrip("*."))
    return {
        "primary_domain": primary_domain,
        "issue_domains": issue_domains,
        "base_domain": primary_domain.lstrip("*."),
        "cert_basename": cert_basename.lstrip("*."),
    }


def record_type_for_ip(ip):
    return "AAAA" if ipaddress.ip_address(ip).version == 6 else "A"


def _authoritative_blocks(output):
    return [block.strip() for block in (output or "").split("== ") if block.strip()]


def query_authoritative_records(zone, name, rrtype):
    code, ns_out = run(["dig", "+short", "NS", zone], timeout=DIG_CMD_TIMEOUT)
    if code != 0:
        return code, ns_out

    nameservers = [line.strip() for line in ns_out.splitlines() if line.strip()]
    if not nameservers:
        return 2, f"[ERR] no authoritative nameservers found for zone: {zone}"

    blocks = []
    overall_code = 0
    for ns in nameservers:
        ans_code, ans_out = run(["dig", "+short", rrtype, name, f"@{ns}"], timeout=DIG_CMD_TIMEOUT)
        if ans_code != 0 and overall_code == 0:
            overall_code = ans_code
        blocks.append(f"== {ns} ==\n{ans_out.strip()}")

    merged = "\n".join(blocks)
    if merged and not merged.endswith("\n"):
        merged += "\n"
    return overall_code, merged


ESA_API_VERSION = "2024-09-10"
_REGION = None  # must be auto-detected before use
_DEFAULT_SEED_REGION = "cn-hangzhou"
_FALLBACK_ESA_REGIONS = (
    "cn-hangzhou",
    "ap-southeast-1",
    "ap-southeast-7",
    "us-west-1",
    "eu-central-1",
)


def _percent_encode(value):
    return urllib.parse.quote(str(value), safe="~")


def _encode_params(params):
    return "&".join(f"{_percent_encode(k)}={_percent_encode(v)}" for k, v in params.items())


def _iso8601_timestamp():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _discover_esa_regions(client, preferred_region=None):
    """Best-effort ESA region discovery with sane fallbacks.

    ESA deployments do not always expose DescribeRegions. When that action is
    unavailable, fall back to a curated candidate list plus any explicit region
    hint so callers can still auto-detect the site.
    """
    candidates = []
    for region in [preferred_region, client.get("region"), _DEFAULT_SEED_REGION, *_FALLBACK_ESA_REGIONS]:
        if region and region not in candidates:
            candidates.append(region)
    try:
        resp = esa_req(client, "DescribeRegions", "GET", region=preferred_region or client.get("region") or _DEFAULT_SEED_REGION)
        regions = resp.get("Regions", [])
        discovered = [r["RegionId"] for r in regions if r.get("RegionId")]
        for region in discovered:
            if region not in candidates:
                candidates.append(region)
        if discovered:
            return candidates
        print(f"[WARN] DescribeRegions returned no region list, fallback to candidates: {', '.join(candidates)}.")
        return candidates
    except Exception as e:
        # DescribeRegions is not consistently available on ESA. Continue with
        # explicit and curated candidates instead of aborting early.
        print(f"[WARN] DescribeRegions failed: {e}. Fallback to candidates: {', '.join(candidates)}.")
        return candidates


def _is_retryable_esa_error(exc):
    text = str(exc).lower()
    retry_markers = (
        "connection reset",
        "timed out",
        "timeout",
        "temporarily unavailable",
        "remote end closed connection",
        "connection refused",
        "bad gateway",
        "service unavailable",
        "internal server error",
    )
    return any(marker in text for marker in retry_markers)


def esa_req(client, action, method="POST", region=None, **params):
    effective_region = region or _REGION
    if not effective_region:
        print("[ERR] ESA region not detected. Cannot make API request.")
        sys.exit(2)
    query_params = {
        "AccessKeyId": client["ak"],
        "Action": action,
        "Format": "JSON",
        "SignatureMethod": "HMAC-SHA1",
        "SignatureNonce": str(uuid.uuid4()),
        "SignatureVersion": "1.0",
        "Timestamp": _iso8601_timestamp(),
        "Version": ESA_API_VERSION,
    }
    if client.get("sts_token"):
        query_params["SecurityToken"] = client["sts_token"]
    for k, v in params.items():
        query_params[k] = str(v)

    canonicalized_query = _encode_params(dict(sorted(query_params.items())))
    string_to_sign = f"{method.upper()}&%2F&{_percent_encode(canonicalized_query)}"
    signature = base64.b64encode(
        hmac.new(
            f"{client['sk']}&".encode("utf-8"),
            string_to_sign.encode("utf-8"),
            hashlib.sha1,
        ).digest()
    ).decode("utf-8")
    query_params["Signature"] = signature
    payload = _encode_params(dict(sorted(query_params.items()))).encode("utf-8")

    url = f"https://esa.{effective_region}.aliyuncs.com/"
    data = None if method.upper() == "GET" else payload
    if method.upper() == "GET":
        url = f"{url}?{payload.decode('utf-8')}"

    last_error = None
    for attempt in range(1, ESA_REQ_MAX_ATTEMPTS + 1):
        req = urllib.request.Request(url, data=data, method=method.upper())
        req.add_header("Accept", "application/json")
        if data is not None:
            req.add_header("Content-Type", "application/x-www-form-urlencoded")
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                body = resp.read().decode("utf-8")
            try:
                return json.loads(body)
            except json.JSONDecodeError as e:
                raise RuntimeError(f"ESA API returned non-JSON response: {body}") from e
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            error = RuntimeError(f"ESA API HTTP {e.code}: {body}")
            if attempt < ESA_REQ_MAX_ATTEMPTS and (e.code >= 500 or _is_retryable_esa_error(error)):
                time.sleep(attempt)
                last_error = error
                continue
            raise error from e
        except (urllib.error.URLError, ConnectionResetError, TimeoutError, OSError) as e:
            error = RuntimeError(f"ESA API request failed: {e}")
            if attempt < ESA_REQ_MAX_ATTEMPTS and _is_retryable_esa_error(error):
                time.sleep(attempt)
                last_error = error
                continue
            raise error from e
    if last_error:
        raise last_error
    raise RuntimeError("ESA API request failed for an unknown reason")


def parse_challenges(output):
    # acme.sh manual mode prints repeated blocks:
    # Domain: 'xxx'
    # TXT value: 'yyy'
    pairs = re.findall(r"Domain:\s*'([^']+)'[\s\S]*?TXT value:\s*'([^']+)'", output)
    return [{"fqdn": d, "token": t} for d, t in pairs]


def wait_dns_record(zone, fqdn, expected, rrtype, timeout=240):
    deadline = time.time() + timeout
    last = ""
    while time.time() < deadline:
        code, out = query_authoritative_records(zone, fqdn, rrtype)
        last = out
        if code in {2, 127}:
            return False, out
        blocks = _authoritative_blocks(out)
        ok_all = all(expected in block for block in blocks)
        if ok_all and blocks:
            return True, out
        time.sleep(5)
    return False, last


def wait_record_visible_in_esa(client, site_id, fqdn, token, timeout=120):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            resp = esa_req(client, "ListRecords", "GET", SiteId=site_id)
            records = resp.get("Records", [])
            for r in records:
                if r.get("RecordName") == fqdn and r.get("RecordType") == "TXT":
                    val = ((r.get("Data") or {}).get("Value") or "")
                    if val == token:
                        return True, r.get("RecordId")
        except Exception:
            pass
        time.sleep(3)
    return False, None


def ensure_a_record(client, site_id, zone, host, ip, dns_timeout=600, confirm_overwrite=False):
    ip = normalize_ip(ip)
    rrtype = record_type_for_ip(ip)
    records = esa_req(client, "ListRecords", "GET", SiteId=site_id).get("Records", [])
    target = None
    for r in records:
        if r.get("RecordName") == host and r.get("RecordType") in {"A/AAAA", "A", "AAAA"}:
            target = r
            break
    payload = json.dumps({"Value": ip}, separators=(",", ":"))
    if target:
        current = ((target.get("Data") or {}).get("Value") or "").strip()
        if current and current != ip and not confirm_overwrite:
            print(f"[CONFIRM] Existing {rrtype} record detected: {host} -> {current}")
            print(f"[CONFIRM] Requested new value: {ip}")
            print("[ERR] overwrite blocked. Re-run with --confirm-overwrite after user confirmation.")
            sys.exit(6)
        esa_req(client, "UpdateRecord", "POST", SiteId=site_id, RecordId=target.get("RecordId"), Type="A/AAAA", RecordName=host, Ttl=1, Data=payload, Proxied="false")
        print(f"[INFO] {rrtype} record update request accepted: {host} -> {ip}")
    else:
        esa_req(client, "CreateRecord", "POST", SiteId=site_id, Type="A/AAAA", RecordName=host, Ttl=1, Data=payload, Proxied="false")
        print(f"[INFO] {rrtype} record create request accepted: {host} -> {ip}")

    ok, out = wait_dns_record(zone, host, ip, rrtype=rrtype, timeout=dns_timeout)
    if not ok:
        print(out)
        print(f"[ERR] {rrtype} record not propagated on all authoritative NS: {host} -> {ip}")
        sys.exit(4)
    print(f"[OK] {rrtype} record propagated on authoritative NS: {host} -> {ip}")


def _list_all_sites(client, region=None):
    page = 1
    all_sites = []
    while True:
        resp = esa_req(client, "ListSites", "GET", region=region, PageNumber=page, PageSize=500)
        sites = resp.get("Sites", [])
        all_sites.extend(sites)
        total = int(resp.get("TotalCount", 0) or 0)
        if page * 500 >= total:
            break
        page += 1
    return all_sites


def _match_site(sites, base_domain):
    candidates = []
    for s in sites:
        sn = (s.get("SiteName") or "").lower().strip()
        if not sn:
            continue
        if base_domain == sn or base_domain.endswith("." + sn):
            candidates.append(s)
    if not candidates:
        return None
    candidates.sort(key=lambda s: len((s.get("SiteName") or "")), reverse=True)
    return candidates[0]


def auto_detect_region(client, base_domain, preferred_region=None):
    """Probe ESA regions to find which one hosts the target domain."""
    regions = _discover_esa_regions(client, preferred_region=preferred_region)
    print(f"[INFO] discovered {len(regions)} ESA region(s): {', '.join(regions)}")
    for region in regions:
        try:
            sites = _list_all_sites(client, region=region)
        except Exception:
            continue
        match = _match_site(sites, base_domain)
        if match:
            return region, str(match.get("SiteId")), match.get("SiteName")
    return None, None, None


def auto_site_id(client, base_domain):
    # Find best matching site by suffix, prefer exact domain match
    sites = _list_all_sites(client)
    match = _match_site(sites, base_domain)
    if not match:
        raise RuntimeError(f"No ESA site matched domain: {base_domain}")
    return str(match.get("SiteId")), match.get("SiteName")


def ensure_python_deps():
    return


def find_acme_sh():
    cands = [os.path.expanduser("~/.acme.sh/acme.sh"), shutil.which("acme.sh")]
    for c in cands:
        if c and os.path.exists(c):
            return c
    print("[ERR] acme.sh not found. Install acme.sh first.")
    sys.exit(2)


_I18N_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "i18n")
_I18N_CACHE = {}


def _load_i18n(lang):
    if lang in _I18N_CACHE:
        return _I18N_CACHE[lang]
    path = os.path.join(_I18N_DIR, f"{lang}.json")
    if not os.path.isfile(path):
        if lang != "en":
            return _load_i18n("en")
        print(f"[ERR] i18n file not found: {path}")
        sys.exit(2)
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    _I18N_CACHE[lang] = data
    return data


def print_security_reminders(has_sts_token, lang="en"):
    msgs = _load_i18n(lang).get("security", {})
    print(msgs.get("header", ""))
    for tip in msgs.get("tips", []):
        print(f"  {tip}")
    if not has_sts_token:
        print(msgs.get("warn", ""))


def make_acs_client(ak, sk, region, sts_token=None):
    return {
        "ak": ak,
        "sk": sk,
        "region": region,
        "sts_token": sts_token,
    }


def ensure_parent_dirs(paths):
    for path in paths:
        parent = os.path.dirname(os.path.abspath(path))
        if parent:
            os.makedirs(parent, exist_ok=True)


def install_certificate(acme_sh, primary_domain, cert_dst, key_dst, reload_cmd, secrets):
    if not reload_cmd.strip():
        print("[ERR] empty --reload-cmd")
        sys.exit(2)
    try:
        ensure_parent_dirs([cert_dst, key_dst])
    except OSError as e:
        print(f"[ERR] failed to prepare certificate directory: {e}")
        sys.exit(5)

    cmd = [
        acme_sh,
        "--install-cert",
        "-d",
        primary_domain,
        "--ecc",
        "--fullchain-file",
        cert_dst,
        "--key-file",
        key_dst,
        "--reloadcmd",
        reload_cmd,
    ]
    code, out = run(cmd, timeout=120)
    print(redact_text(out, secrets))
    if code != 0:
        print("[ERR] failed to install certificate via acme.sh")
        sys.exit(5)
    print(f"[OK] installed to {cert_dst}, {key_dst}")


def available_langs():
    if not os.path.isdir(_I18N_DIR):
        return ["en"]
    langs = sorted([f[:-5] for f in os.listdir(_I18N_DIR) if f.endswith(".json")])
    return langs or ["en"]


def build_arg_parser():
    parser = argparse.ArgumentParser(description="Issue cert via acme.sh + ESA DNS TXT automation (supports wildcard)")
    parser.add_argument("-d", "--domain", action="append", required=True, help="can repeat, e.g. -d example.com -d '*.example.com'")
    parser.add_argument("--site-id", required=False, help="ESA site id (optional; auto-detect by domain if omitted)")
    parser.add_argument("--region", default=first_env(*ESA_REGION_ENV_NAMES), help="ESA region hint, e.g. cn-hangzhou")
    parser.add_argument("--ak", default=first_env(*AK_ENV_NAMES))
    parser.add_argument("--sk", default=first_env(*SK_ENV_NAMES))
    parser.add_argument(
        "--sts-token",
        default=first_env(*STS_ENV_NAMES),
        help="optional STS security token; recommended for temporary credentials",
    )
    langs = available_langs()
    default_lang = "en" if "en" in langs else langs[0]
    parser.add_argument("--lang", default=default_lang, choices=langs, help="output language for security reminders (default: en)")
    parser.add_argument("--ttl", default="60")
    parser.add_argument("--dns-timeout", type=int, default=600)
    parser.add_argument("--install-cert", dest="install_cert", action="store_true", default=False)
    parser.add_argument("--no-install-cert", dest="install_cert", action="store_false")
    parser.add_argument("--cert-path", default=None, help="target crt path")
    parser.add_argument("--key-path", default=None, help="target key path")
    parser.add_argument("--reload-cmd", default="systemctl reload nginx")
    parser.add_argument("--ensure-a-record", action="append", default=[], help="ensure IPv4/IPv6 record, format: host=ip")
    parser.add_argument("--confirm-overwrite", action="store_true", default=False, help="required to overwrite existing A/AAAA record value")
    return parser


def parse_args(argv=None):
    return build_arg_parser().parse_args(argv)


def validate_credentials(ak, sk):
    if ak and sk:
        return
    print("[ERR] missing --ak/--sk")
    print("[ERR] supported env names: ALIYUN_AK/ALIYUN_SK or ALIBABACLOUD_ACCESS_KEY_ID/ALIBABACLOUD_ACCESS_KEY_SECRET")
    sys.exit(2)


def resolve_domain_plan_or_exit(domains):
    try:
        return build_domain_plan(domains)
    except ValueError as e:
        print(f"[ERR] {e}")
        sys.exit(2)


def resolve_site_context(ak, sk, site_id, base_domain, sts_token=None, region=None):
    global _REGION

    preferred_region = region or _DEFAULT_SEED_REGION

    if site_id:
        resolved_site_id = str(site_id)
        detected_region = None
        zone = base_domain
        seed_client = make_acs_client(ak, sk, preferred_region, sts_token=sts_token)
        regions = _discover_esa_regions(seed_client, preferred_region=region)
        for region in regions:
            try:
                client_tmp = make_acs_client(ak, sk, region, sts_token=sts_token)
                site = esa_req(client_tmp, "GetSite", "POST", region=region, SiteId=resolved_site_id)
                zone = (site.get("SiteName") or base_domain)
                detected_region = region
                break
            except Exception:
                continue
        if not detected_region:
            print(f"[ERR] SiteId={resolved_site_id} not found in any known ESA region")
            sys.exit(2)
        _REGION = detected_region
        client = make_acs_client(ak, sk, _REGION, sts_token=sts_token)
        print(f"[OK] auto-detected region={_REGION} for SiteId={resolved_site_id} site={zone}")
        return client, resolved_site_id, zone

    client_probe = make_acs_client(ak, sk, preferred_region, sts_token=sts_token)
    detected_region, resolved_site_id, zone = auto_detect_region(client_probe, base_domain, preferred_region=region)
    if not detected_region:
        print(f"[ERR] No ESA site matched domain '{base_domain}' in any known region")
        sys.exit(2)
    _REGION = detected_region
    client = make_acs_client(ak, sk, _REGION, sts_token=sts_token)
    print(f"[OK] auto-detected region={_REGION} SiteId={resolved_site_id} for site={zone}")
    return client, resolved_site_id, zone


def parse_ensure_a_records(items):
    parsed = []
    for item in items:
        if "=" not in item:
            print(f"[ERR] invalid --ensure-a-record format: {item}, expect host=ip")
            sys.exit(2)
        host, ip = item.split("=", 1)
        host = host.strip()
        ip = ip.strip()
        if not is_valid_host(host):
            print(f"[ERR] invalid host in --ensure-a-record: {host}")
            sys.exit(2)
        if not is_valid_ip(ip):
            print(f"[ERR] invalid IP in --ensure-a-record: {ip}")
            sys.exit(2)
        parsed.append((host, ip))
    return parsed


def ensure_requested_records(client, site_id, zone, records, dns_timeout, confirm_overwrite):
    for host, ip in records:
        ensure_a_record(
            client,
            site_id,
            zone,
            host,
            ip,
            dns_timeout=dns_timeout,
            confirm_overwrite=confirm_overwrite,
        )


def build_issue_command(acme_sh, issue_domains):
    cmd = [acme_sh, "--issue", "--dns"]
    for domain in issue_domains:
        cmd.extend(["-d", domain])
    cmd.extend([
        "--yes-I-know-dns-manual-mode-enough-go-ahead-please",
        "--keylength",
        "ec-256",
    ])
    return cmd


def build_renew_command(acme_sh, primary_domain):
    return [
        acme_sh,
        "--renew",
        "-d",
        primary_domain,
        "--ecc",
        "--yes-I-know-dns-manual-mode-enough-go-ahead-please",
        "--keylength",
        "ec-256",
    ]


def group_challenges(challenges):
    grouped = {}
    for challenge in challenges:
        grouped.setdefault(challenge["fqdn"], [])
        if challenge["token"] not in grouped[challenge["fqdn"]]:
            grouped[challenge["fqdn"]].append(challenge["token"])
    return grouped


def request_challenges(acme_sh, issue_domains, dns_timeout, secrets):
    issue_cmd = build_issue_command(acme_sh, issue_domains)
    code, out = run(issue_cmd, timeout=dns_timeout + ACME_CMD_TIMEOUT_PADDING)
    challenges = parse_challenges(out)
    if not challenges:
        print(redact_text(out, secrets))
        print("[ERR] failed to parse challenge tokens")
        sys.exit(3)

    print("[OK] challenges:")
    for challenge in challenges:
        print(f"  - {challenge['fqdn']} = {challenge['token']}")
    return group_challenges(challenges)


def create_txt_records(client, site_id, grouped, ttl):
    record_ids = []
    for fqdn, tokens in grouped.items():
        for token in tokens:
            rec = esa_req(
                client,
                "CreateRecord",
                "POST",
                SiteId=site_id,
                RecordName=fqdn,
                Type="TXT",
                Ttl=ttl,
                Data=json.dumps({"Value": token}, separators=(",", ":")),
                Proxied="false",
            )
            rid = rec.get("RecordId")
            print(f"[INFO] ESA API accepted create request: {fqdn} token={token[:10]}... RecordId={rid}")

            visible, confirmed_rid = wait_record_visible_in_esa(client, site_id, fqdn, token, timeout=120)
            if not visible:
                print(f"[ERR] ESA record not visible after create: {fqdn} token={token}")
                print("[ERR] Do NOT claim DNS is ready. Please check ESA console/API permissions/filters.")
                sys.exit(4)

            record_ids.append(confirmed_rid or rid)
            print(f"[OK] ESA TXT confirmed in ListRecords: {fqdn} RecordId={confirmed_rid or rid}")
    return record_ids


def wait_for_txt_records(zone, grouped, dns_timeout, secrets):
    for fqdn, tokens in grouped.items():
        for token in tokens:
            ok, out = wait_dns_record(zone, fqdn, token, rrtype="TXT", timeout=dns_timeout)
            if not ok:
                print(redact_text(out, secrets))
                print(f"[ERR] TXT not propagated: {fqdn} token={token}")
                sys.exit(4)
        print(f"[OK] authoritative TXT visible: {fqdn} ({len(tokens)} value(s))")


def renew_certificate(acme_sh, primary_domain, dns_timeout, secrets):
    renew_cmd = build_renew_command(acme_sh, primary_domain)
    code, out = run(renew_cmd, timeout=dns_timeout + ACME_CMD_TIMEOUT_PADDING)
    print(redact_text(out, secrets))
    if code != 0:
        print("[ERR] renew/sign failed")
        sys.exit(5)


def maybe_install_certificate(args, acme_sh, primary_domain, cert_basename, secrets):
    if not args.install_cert:
        return
    cert_dst = args.cert_path or f"/etc/nginx/ssl/{cert_basename}.crt"
    key_dst = args.key_path or f"/etc/nginx/ssl/{cert_basename}.key"
    install_certificate(acme_sh, primary_domain, cert_dst, key_dst, args.reload_cmd, secrets)


def cleanup_txt_records(client, site_id, record_ids):
    for rid in record_ids:
        if not rid:
            continue
        try:
            esa_req(client, "DeleteRecord", "POST", SiteId=site_id, RecordId=rid)
            print(f"[OK] cleaned TXT RecordId={rid}")
        except Exception as e:
            print(f"[WARN] cleanup failed RecordId={rid}: {e}")


def run_certificate_flow(args, client, site_id, zone, acme_sh, domain_plan, secrets):
    grouped = request_challenges(acme_sh, domain_plan["issue_domains"], args.dns_timeout, secrets)
    record_ids = []
    try:
        record_ids = create_txt_records(client, site_id, grouped, args.ttl)
        wait_for_txt_records(zone, grouped, args.dns_timeout, secrets)
        renew_certificate(acme_sh, domain_plan["primary_domain"], args.dns_timeout, secrets)
        maybe_install_certificate(args, acme_sh, domain_plan["primary_domain"], domain_plan["cert_basename"], secrets)
    finally:
        cleanup_txt_records(client, site_id, record_ids)


def main():
    args = parse_args()
    ensure_python_deps()
    validate_credentials(args.ak, args.sk)
    print_security_reminders(bool(args.sts_token), lang=args.lang)
    secrets = [args.ak, args.sk, args.sts_token]
    domain_plan = resolve_domain_plan_or_exit(args.domain)
    acme_sh = find_acme_sh()
    client, site_id, zone = resolve_site_context(
        args.ak,
        args.sk,
        args.site_id,
        domain_plan["base_domain"],
        sts_token=args.sts_token,
        region=args.region,
    )
    requested_records = parse_ensure_a_records(args.ensure_a_record)
    ensure_requested_records(
        client,
        site_id,
        zone,
        requested_records,
        dns_timeout=args.dns_timeout,
        confirm_overwrite=args.confirm_overwrite,
    )
    run_certificate_flow(args, client, site_id, zone, acme_sh, domain_plan, secrets)


if __name__ == "__main__":
    main()
