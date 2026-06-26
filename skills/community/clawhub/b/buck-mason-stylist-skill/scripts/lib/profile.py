"""Profile.md parser — extracted from run-headless-lookbook.py for testability.

Accepts the customer's profile as text (markdown) and returns a dict with the
fields the orchestrator reads (gender, sizes, link_payment_method, preferred_*
fields, reference_photos, etc.).

Two profile-form quirks the parser handles:

  (a) Schema form (templates/profile.example.md):
        reference_photos:
          - path: /Users/.../file.jpeg

  (b) Heading-list form (real-world profile.md):
        ## Reference photos
        - /Users/.../file.jpeg  (description ignored)

  - YAML-ish "key: value" lines (with or without the YAML list "-" prefix)
  - Values "true"/"false"/"null" are coerced to bool / None
  - Sizes block is parsed under "## Sizes" heading
  - preferred_link_payment_methods is parsed as a purpose -> card last4 map
"""
import re

__all__ = ["parse_profile", "parse_profile_path"]


def parse_profile(text: str) -> dict:
    """Parse a customer profile.md into a dict. Pure — no I/O."""
    out: dict = {}

    # Top-level "[- ]key: value" lines.
    for line in text.splitlines():
        m = re.match(r'^\s*-?\s*([a-z][a-z0-9_]*)\s*:\s*(.+?)\s*(?:#.*)?$', line)
        if m:
            k, v = m.group(1), m.group(2).strip()
            v = v.strip('"').strip("'")
            if v.lower() in ("true", "false"):
                v = (v.lower() == "true")
            elif v.lower() in ("null", "none", ""):
                v = None
            out.setdefault(k, v)

    # Reference photos — accept BOTH forms.
    photos = []
    # Form (a): "- path: /path/to/file"
    for m in re.finditer(r'^\s*-\s*path:\s*(.+?)\s*(?:#.*)?$', text, re.M):
        photos.append(m.group(1).strip().strip('"').strip("'"))
    # Form (b): heading-list — paths under "## Reference photos"
    if not photos:
        section = re.search(
            r'^\s*##\s*Reference\s+photos?\s*$\n(.*?)(?=^\s*##\s|\Z)',
            text, re.M | re.S | re.I,
        )
        if section:
            for line in section.group(1).splitlines():
                # Path may contain spaces (e.g. "Styling example pics"); capture
                # non-greedy through the file extension, then accept end-of-
                # path-marker = space-then-paren / space-then-hash / EOL.
                m = re.match(
                    r'^\s*-\s*(/.+?\.(?:jpe?g|png|heic|webp))(?:\s+[(#].*|\s*)$',
                    line, re.I,
                )
                if m:
                    photos.append(m.group(1))
    photos = [p for p in photos if p.startswith("/")]
    photos = list(dict.fromkeys(photos))   # dedup, preserve order
    if photos:
        out["reference_photos"] = photos

    # Sizes block — parse under "## Sizes" heading.
    sizes = {}
    in_sizes = False
    for line in text.splitlines():
        if re.match(r'^\s*##\s*Sizes', line, re.I):
            in_sizes = True
            continue
        if in_sizes and re.match(r'^\s*##', line):
            in_sizes = False
        if in_sizes:
            m = re.match(
                r'^\s*-?\s*(shirt|tee|pant|short|jacket|sport_coat|shoe|belt|jean)\s*:\s*([^\s#]+)',
                line,
            )
            if m:
                sizes[m.group(1)] = m.group(2)
    if sizes:
        out["sizes"] = sizes

    # Purpose -> Link card last4 map for MPP checkout payment-method selection.
    # The agent resolves last4 to a live Link payment-method id at checkout time.
    preferred_link_payment_methods = {}
    in_link_prefs = False
    for line in text.splitlines():
        if re.match(r'^\s*-?\s*preferred_link_payment_methods\s*:\s*(?:#.*)?$', line):
            in_link_prefs = True
            continue
        if in_link_prefs:
            if not line.strip():
                continue
            if re.match(r'^\S', line):
                break
            m = re.match(r'^\s+([A-Za-z0-9_-]+)\s*:\s*(.+?)\s*(?:#.*)?$', line)
            if m:
                purpose, last4 = m.group(1), m.group(2).strip().strip('"').strip("'")
                if re.match(r'^\d{4}$', last4):
                    preferred_link_payment_methods[purpose] = last4
    if preferred_link_payment_methods:
        out["preferred_link_payment_methods"] = preferred_link_payment_methods

    return out


def parse_profile_path(path) -> dict:
    """Read a profile.md file and parse it. Convenience wrapper."""
    import pathlib
    p = path if isinstance(path, str) else str(path)
    return parse_profile(pathlib.Path(p).read_text())
