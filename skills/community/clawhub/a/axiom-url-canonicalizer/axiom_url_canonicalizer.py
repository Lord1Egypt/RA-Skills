"""
🛠️ axiom-url-canonicalizer — URL Normalizer
============================================

⚠️ LIMITATIONS CONNUES :
- Pas de résolution DNS (seulement normalisation)
- Pas de validation SSL/TLS
- IDN/percent-encoding partiel
- Pas de support pour javascript: / mailto: / data: schemes

NORMALISE LES URLs POUR SEO ET CACHE

Usage CLI:
    python3 axiom_url_canonicalizer.py "HTTP://Example.COM:80/Path/?b=2&a=1#frag"
    python3 axiom_url_canonicalizer.py --json "..."
"""

import re
import sys
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode, unquote


# ============================================================================
# Canonicalization
# ============================================================================

# Default ports to remove
DEFAULT_PORTS = {
    "http": "80",
    "https": "443",
    "ftp": "21",
    "ws": "80",
    "wss": "443",
}

# Schemes that should be lowercased
LOWERCASE_SCHEMES = {
    "http", "https", "ftp", "ftps", "ws", "wss", "file",
    "git", "ssh", "sftp", "mailto", "tel",
}

# Path-safe characters — see RFC 3986
PATH_UNRESERVED = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~!$&'()*+,;=:@/")


def canonicalize(
    url: str,
    sort_query: bool = True,
    strip_fragment: bool = True,
    strip_default_port: bool = True,
    force_https: bool = False,
    force_trailing_slash: bool = False,
    remove_tracking_params: bool = False,
) -> str:
    """
    Canonicalize a URL.

    Args:
        url: the URL to normalize
        sort_query: sort query parameters alphabetically
        strip_fragment: remove #fragment
        strip_default_port: remove :80 for http, :443 for https, etc.
        force_https: rewrite http:// to https://
        force_trailing_slash: ensure path ends with /
        remove_tracking_params: remove common tracking params (utm_*, fbclid, etc.)

    Returns:
        canonical URL string
    """
    if not isinstance(url, str):
        raise TypeError(f"url must be str, got {type(url).__name__}")

    if not url:
        return ""

    # First-pass: decode percent-encoded unreserved characters
    # urlparse needs a scheme to identify the URL properly
    has_scheme = bool(re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", url))

    if not has_scheme:
        # No scheme — assume http
        url = "http://" + url

    parsed = urlparse(url)

    # Scheme: lowercase
    scheme = parsed.scheme.lower() if parsed.scheme else "http"

    if force_https and scheme == "http":
        scheme = "https"

    # Netloc: host lowercase, strip default port
    netloc = parsed.netloc
    host = parsed.hostname or ""
    port = parsed.port

    # Userinfo
    userinfo = ""
    if "@" in netloc:
        userinfo, netloc = netloc.rsplit("@", 1)
        userinfo += "@"

    # Lowercase host
    host = host.lower()

    # Strip default port
    new_port = ""
    if port is not None:
        port_str = str(port)
        if strip_default_port and DEFAULT_PORTS.get(scheme) == port_str:
            pass  # omit port
        else:
            new_port = f":{port_str}"

    # IDN: convert to punycode (best-effort)
    try:
        if "xn--" not in host and any(ord(c) > 127 for c in host):
            host = host.encode("idna").decode("ascii")
    except (UnicodeError, UnicodeDecodeError):
        pass  # Leave as-is if IDN fails

    netloc = f"{userinfo}{host}{new_port}"

    # Path: normalize
    path = parsed.path or "/"

    # Decode unreserved percent-encoded chars
    # (only %XX where XX is unreserved)
    def decode_unreserved(match):
        ch = chr(int(match.group(1), 16))
        if ch in PATH_UNRESERVED and ch not in "/%":
            return ch
        return match.group(0)

    path = re.sub(r"%([0-9A-Fa-f]{2})", decode_unreserved, path)

    # Resolve /./ and /../
    segments = []
    for segment in path.split("/"):
        if segment == ".":
            continue
        if segment == "..":
            if segments and segments[-1] != "":
                segments.pop()
            continue
        segments.append(segment)

    path = "/".join(segments)
    if not path.startswith("/"):
        path = "/" + path

    # Multiple slashes → single
    path = re.sub(r"/+", "/", path)

    # Empty path → "/"
    if not path:
        path = "/"

    # Trailing slash
    if force_trailing_slash and not path.endswith("/"):
        path += "/"

    # Query: sort and filter
    query = ""
    if parsed.query:
        params = parse_qsl(parsed.query, keep_blank_values=True)

        if remove_tracking_params:
            TRACKING = re.compile(r"^(utm_|fbclid|gclid|mc_eid|_ga$|ref$|source$|cmpid$|ncid$|igshid$|yclid$|msclkid$|dclid$|spm$|scm$|tracking)", re.I)
            params = [(k, v) for k, v in params if not TRACKING.match(k)]

        if sort_query:
            params = sorted(params, key=lambda kv: (kv[0], kv[1]))

        if params:
            query = urlencode(params)

    # Fragment
    fragment = ""
    if not strip_fragment and parsed.fragment:
        fragment = parsed.fragment

    # Rebuild
    canonical = urlunparse((scheme, netloc, path, parsed.params, query, fragment))
    return canonical


# ============================================================================
# Comparison
# ============================================================================

def urls_equivalent(url_a: str, url_b: str, **kwargs) -> bool:
    """Check if two URLs are canonically equivalent."""
    return canonicalize(url_a, **kwargs) == canonicalize(url_b, **kwargs)


# ============================================================================
# Analysis
# ============================================================================

def analyze(url: str) -> dict:
    """
    Analyse une URL avec sa forme canonique.
    """
    if not url:
        return {"original": url, "valid": False, "error": "empty URL"}

    parsed = urlparse(url if "://" in url else "http://" + url)

    return {
        "original": url,
        "valid": bool(parsed.scheme and parsed.netloc),
        "scheme": parsed.scheme,
        "host": parsed.hostname,
        "port": parsed.port,
        "path": parsed.path,
        "query_params": dict(parse_qsl(parsed.query, keep_blank_values=True)),
        "fragment": parsed.fragment,
        "canonical": canonicalize(url),
    }


# ============================================================================
# CLI
# ============================================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="axiom-url-canonicalizer — URL normalizer "
    )
    parser.add_argument("url", nargs="?", help="URL à normaliser")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--no-sort", action="store_true", help="Don't sort query params")
    parser.add_argument("--keep-fragment", action="store_true", help="Keep #fragment")
    parser.add_argument("--force-https", action="store_true", help="Rewrite http→https")
    parser.add_argument("--force-trailing", action="store_true", help="Force trailing /")
    parser.add_argument("--strip-tracking", action="store_true", help="Remove utm_*, fbclid, etc.")
    args = parser.parse_args()

    if not args.url:
        parser.print_help()
        return 1

    try:
        canonical = canonicalize(
            args.url,
            sort_query=not args.no_sort,
            strip_fragment=not args.keep_fragment,
            force_https=args.force_https,
            force_trailing_slash=args.force_trailing,
            remove_tracking_params=args.strip_tracking,
        )

        if args.json:
            import json
            print(json.dumps(analyze(args.url), indent=2))
        else:
            print(f"Original:  {args.url}")
            print(f"Canonical: {canonical}")

        return 0

    except Exception as e:
        print(f"❌ Erreur : {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
