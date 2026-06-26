#!/usr/bin/env python3
import argparse
import datetime as dt
import html
import re
from pathlib import Path
from typing import Optional


def derive_plus_email(base_email: str, app_name: str, email_tag: Optional[str] = None) -> str:
    local, domain = base_email.split("@", 1)
    raw_tag = email_tag if email_tag else app_name
    tag = re.sub(r"[^a-z0-9]", "", raw_tag.lower())
    if not tag:
        raise ValueError("email tag cannot be empty; provide --email-tag or a valid --app-name")
    return f"{local}+{tag}@{domain}"


def has_positive_signal(t: str, keyword: str) -> bool:
    neg_patterns = [
        f"no {keyword}",
        f"without {keyword}",
        f"not use {keyword}",
        f"does not use {keyword}",
        f"do not use {keyword}",
    ]
    if any(p in t for p in neg_patterns):
        return False
    return keyword in t


def detect_posture(text: str):
    t = text.lower()
    return {
        "offline_only": ("offline" in t) or ("on your device" in t) or ("local" in t),
        "no_cloud": ("no cloud" in t) or ("without cloud" in t) or ("无云" in text),
        "no_tracking": ("no tracking" in t) or ("无追踪" in text),
        "no_analytics": ("no analytics" in t) or ("无分析" in text),
        "no_server": ("no server" in t) or ("无服务器" in text),
        "mentions_exif": ("exif" in t),
    }


def detect_items(text: str):
    t = text.lower()

    data_types = []
    if any(k in t for k in ["email", "mail", "contact"]):
        data_types.append("Contact information (such as email)")
    if any(k in t for k in ["device", "model", "os version", "resolution", "identifier", "idfa", "aaid", "android id"]):
        data_types.append("Device and technical information")
    if has_positive_signal(t, "analytics") or has_positive_signal(t, "telemetry"):
        data_types.append("Usage analytics")
    if any(k in t for k in ["crash", "log", "error report", "sentry"]):
        data_types.append("Crash diagnostics and logs")
    if any(k in t for k in ["sdk", "third-party", "firebase", "amplitude", "mixpanel", "appsflyer", "adjust"]):
        data_types.append("Third-party SDK/service metadata")
    if any(k in t for k in ["photo", "image", "camera", "gallery", "album"]):
        data_types.append("User-selected media content")

    permissions = []
    mapping = {
        "camera": "Camera",
        "photo": "Photos",
        "gallery": "Photos",
        "album": "Photos",
        "microphone": "Microphone",
        "location": "Location",
        "contacts": "Contacts",
        "notification": "Notifications",
    }
    for k, v in mapping.items():
        if has_positive_signal(t, k) and v not in permissions:
            permissions.append(v)

    features = []
    for line in text.splitlines():
        if line.strip().startswith(("-", "*")):
            val = line.strip().lstrip("-* ").strip()
            if 3 <= len(val) <= 120 and val.isascii() and re.search(r"[A-Za-z]", val):
                features.append(val)
    features = features[:10]

    return data_types, permissions, features


def html_page(title: str, body: str):
    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>{html.escape(title)}</title>
  <link rel=\"stylesheet\" href=\"styles.css\" />
</head>
<body>
  <main class=\"container\">{body}</main>
</body>
</html>
"""


def build_privacy(app_name, company, email, effective_date, jurisdiction, data_types, permissions, features, posture):
    dt_items = "".join(f"<li>{html.escape(x)}</li>" for x in data_types) or "<li>Data required to perform your requested in-app actions.</li>"
    if posture.get("mentions_exif"):
        dt_items += "<li>Photo metadata (for example EXIF, including location data if present) is processed on-device only.</li>"

    perm_block = f"<h2>Permissions</h2><ul>{''.join(f'<li>{html.escape(x)}</li>' for x in permissions)}</ul>" if permissions else ""
    feat_items = "".join(f"<li>{html.escape(x)}</li>" for x in features) or "<li>Core app features described in product documentation.</li>"

    sharing_text = "We do not sell personal information."
    if posture.get("offline_only") or posture.get("no_cloud") or posture.get("no_server"):
        sharing_text += " We do not upload your file content to our servers."
    if posture.get("no_tracking"):
        sharing_text += " We do not track users across apps or websites."
    if posture.get("no_analytics"):
        sharing_text += " We do not use analytics for user behavior profiling."

    retention_text = "Data is retained only as needed for app functionality and according to your local device state."
    if posture.get("offline_only") or posture.get("no_server"):
        retention_text = "Your files and processing outputs remain on your device unless you explicitly export/share them."

    use_items = [
        "Provide app functionality and process user-requested actions.",
        "Maintain app reliability and security.",
    ]

    return f"""
<h1>{html.escape(app_name)} Privacy Policy</h1>
<p><strong>Effective date:</strong> {html.escape(effective_date)}</p>
<p>{html.escape(company)} (\"we\", \"us\") provides {html.escape(app_name)}. This policy explains how information is handled.</p>

<h2>Information We Process</h2>
<ul>{dt_items}</ul>

<h2>How We Use Information</h2>
<ul>{''.join(f'<li>{html.escape(x)}</li>' for x in use_items)}</ul>

{perm_block}

<h2>Feature Context</h2>
<ul>{feat_items}</ul>

<h2>Data Sharing</h2>
<p>{sharing_text}</p>

<h2>Data Retention</h2>
<p>{retention_text}</p>

<h2>Your Rights</h2>
<p>You may request access, correction, or deletion of your information by contacting <a href=\"mailto:{html.escape(email)}\">{html.escape(email)}</a>.</p>

<h2>Children's Privacy</h2>
<p>{html.escape(app_name)} is not directed to children under 13, and we do not knowingly collect personal data from children under 13.</p>

<h2>Changes to This Policy</h2>
<p>We may update this policy periodically. Material updates will be reflected by a new effective date.</p>

<h2>Contact</h2>
<p>Email: <a href=\"mailto:{html.escape(email)}\">{html.escape(email)}</a></p>

<p><a href=\"index.html\">Back to Legal Home</a></p>
"""


def build_terms(app_name, company, email, effective_date, jurisdiction):
    governing_law_block = ""
    if jurisdiction:
        governing_law_block = f"<h2>Governing Law</h2><p>These Terms are governed by the laws of {html.escape(jurisdiction)}.</p>"

    return f"""
<h1>{html.escape(app_name)} Terms of Service</h1>
<p><strong>Effective date:</strong> {html.escape(effective_date)}</p>
<p>These Terms govern your use of {html.escape(app_name)} provided by {html.escape(company)}.</p>

<h2>Use of the App</h2>
<ul>
  <li>Use the app in compliance with applicable laws.</li>
  <li>Do not misuse, reverse engineer, or interfere with the service.</li>
  <li>You are responsible for content you import or export.</li>
</ul>

<h2>Intellectual Property</h2>
<p>All app branding, code, and related materials are owned by {html.escape(company)} or its licensors.</p>

<h2>Disclaimers</h2>
<p>The app is provided on an "as is" and "as available" basis to the maximum extent permitted by law.</p>

<h2>Limitation of Liability</h2>
<p>To the maximum extent permitted by law, {html.escape(company)} is not liable for indirect or consequential damages arising from app use.</p>

<h2>Termination</h2>
<p>We may suspend or terminate access if these Terms are violated.</p>

{governing_law_block}

<h2>Contact</h2>
<p>Email: <a href=\"mailto:{html.escape(email)}\">{html.escape(email)}</a></p>

<p><a href=\"index.html\">Back to Legal Home</a></p>
"""


def build_index(app_name):
    return f"""
<h1>{html.escape(app_name)} Legal</h1>
<p>This website hosts legal documents for {html.escape(app_name)}.</p>
<ul>
  <li><a href=\"privacy.html\">Privacy Policy</a></li>
  <li><a href=\"terms.html\">Terms of Service</a></li>
</ul>
"""


def write_css(outdir: Path):
    css = """
:root { --bg:#0b1220; --card:#111a2b; --text:#e8edf7; --muted:#9fb1cc; --link:#7dd3fc; }
* { box-sizing: border-box; }
body { margin:0; background:linear-gradient(180deg,#0b1220,#0f1a30); color:var(--text); font:16px/1.7 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; }
.container { max-width: 820px; margin: 40px auto; background: rgba(17,26,43,.92); border:1px solid #25324b; border-radius: 14px; padding: 28px; }
h1,h2 { line-height:1.3; }
h1 { margin-top:0; }
a { color: var(--link); text-decoration: none; }
a:hover { text-decoration: underline; }
li { margin: 6px 0; }
p,li { color: #dbe6fb; }
em { color: var(--muted); }
""".strip() + "\n"
    (outdir / "styles.css").write_text(css, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Generate Privacy/Terms static site from app feature doc")
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--app-name", required=True)
    parser.add_argument("--company", required=True)
    parser.add_argument("--email", help="Final contact email (overrides --base-email)")
    parser.add_argument("--base-email", help="Base Gmail/email used to derive plus-address, e.g. user@gmail.com")
    parser.add_argument("--email-tag", help="Optional tag for plus-address. Example: quillnest => user+quillnest@gmail.com")
    parser.add_argument("--effective-date", default=str(dt.date.today()))
    parser.add_argument("--jurisdiction", default="", help="Optional governing-law region. Omit unless explicitly provided.")
    args = parser.parse_args()

    if not args.email and not args.base_email:
        raise SystemExit("Provide --email or --base-email")

    final_email = args.email or derive_plus_email(args.base_email, args.app_name, args.email_tag)

    text = Path(args.input).read_text(encoding="utf-8")
    posture = detect_posture(text)
    data_types, permissions, features = detect_items(text)

    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)

    (outdir / "privacy.html").write_text(
        html_page(f"{args.app_name} Privacy Policy", build_privacy(args.app_name, args.company, final_email, args.effective_date, args.jurisdiction, data_types, permissions, features, posture)),
        encoding="utf-8",
    )
    (outdir / "terms.html").write_text(
        html_page(f"{args.app_name} Terms", build_terms(args.app_name, args.company, final_email, args.effective_date, args.jurisdiction)),
        encoding="utf-8",
    )
    (outdir / "index.html").write_text(
        html_page(f"{args.app_name} Legal", build_index(args.app_name)),
        encoding="utf-8",
    )
    write_css(outdir)

    print("Generated:")
    for fn in ["index.html", "privacy.html", "terms.html", "styles.css"]:
        print(outdir / fn)


if __name__ == "__main__":
    main()
