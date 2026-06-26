#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.request
import urllib.error

KROKI_TYPES = {
    "actdiag", "blockdiag", "bpmn", "bytefield", "c4plantuml",
    "d2", "dbml", "ditaa", "erd", "excalidraw",
    "graphviz", "mermaid", "nomnoml", "nwdiag",
    "packetdiag", "pikchr", "plantuml", "rackdiag",
    "seqdiag", "structurizr", "svgbob", "symbolator",
    "tikz", "umlet", "vega", "vegalite",
    "wavedrom", "wireviz",
}

TYPE_ALIASES = {
    "dot": "graphviz",
    "c4": "c4plantuml",
    "vega-lite": "vegalite",
}

FORMAT_ACCEPT = {
    "svg": "image/svg+xml",
    "png": "image/png",
    "pdf": "application/pdf",
    "jpeg": "image/jpeg",
    "txt": "text/plain",
    "base64": "text/plain",
}


def normalize_type(diagram_type: str) -> str:
    t = (diagram_type or "").strip().lower()
    return TYPE_ALIASES.get(t, t)


def read_source(input_path: str | None) -> str:
    if input_path:
        with open(input_path, "r", encoding="utf-8") as f:
            return f.read()
    return sys.stdin.read()


def http_post(url: str, body: bytes, headers: dict | None = None, timeout: int = 60) -> bytes:
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("User-Agent", "Mozilla/5.0 (compatible; render_kroki/1.0)")
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def render_via_kroki(
    diagram_type: str,
    output_format: str,
    source: str,
    kroki_url: str,
    *,
    use_json: bool = False,
) -> bytes:
    base = kroki_url.rstrip("/")
    if use_json:
        payload = json.dumps({
            "diagram_source": source,
            "diagram_type": diagram_type,
            "output_format": output_format,
        })
        return http_post(
            base + "/",
            payload.encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
    url = f"{base}/{diagram_type}/{output_format}"
    accept = FORMAT_ACCEPT.get(output_format, "")
    headers = {"Content-Type": "text/plain; charset=utf-8"}
    if accept:
        headers["Accept"] = accept
    return http_post(url, source.encode("utf-8"), headers=headers)


def wrap_svg_in_html(svg_bytes: bytes, title: str = "Diagram") -> str:
    svg = svg_bytes.decode("utf-8", errors="replace")
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{title}</title>
  <style>body{{margin:0;padding:16px;background:#fafafa;color:#222;font-family:system-ui, -apple-system, Segoe UI, Roboto, Arial, Helvetica, sans-serif}}</style>
</head>
<body>
{svg}
</body>
</html>
"""


def mermaid_html_template(mermaid_code: str, title: str = "Mermaid Diagram") -> str:
    escaped = mermaid_code
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{title}</title>
  <style>
    body{{margin:0;padding:16px;background:#fafafa;color:#222;font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,Helvetica,sans-serif}}
    .container{{max-width:1200px;margin:0 auto}}
    pre.mermaid{{background:#fff;border:1px solid #ddd;border-radius:8px;padding:16px;overflow:auto}}
  </style>
</head>
<body>
  <div class="container">
    <pre class="mermaid">
{escaped}
    </pre>
  </div>
  <script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
    mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
  </script>
</body>
</html>
"""


def detect_format_from_output(out_path: str | None, requested_format: str | None) -> str:
    if requested_format:
        return requested_format
    if out_path:
        lower = out_path.lower()
        for ext, fmt in ((".svg", "svg"), (".png", "png"), (".pdf", "pdf"), (".jpeg", "jpeg"), (".jpg", "jpeg")):
            if lower.endswith(ext):
                return fmt
        if lower.endswith(".html") or lower.endswith(".htm"):
            return "html"
    return "svg"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render diagrams via Kroki (https://kroki.io) to SVG/PNG/PDF/HTML.",
    )
    parser.add_argument("--type", help="Diagram type (mermaid, plantuml, c4plantuml, graphviz, d2, ...)")
    parser.add_argument("--format", help="Output format: svg | png | pdf | jpeg | html")
    parser.add_argument("--in", dest="input_path", help="Input file path (default: stdin)")
    parser.add_argument("--out", dest="output_path", help="Output file path (default: stdout)")
    parser.add_argument("--kroki-url", default=os.environ.get("KROKI_URL", "https://kroki.io"), help="Kroki base URL")
    parser.add_argument("--title", default="Diagram", help="HTML title when --format html")
    parser.add_argument("--json", action="store_true", help="Use JSON POST API (POST / with JSON body)")
    parser.add_argument("--list-types", action="store_true", help="List all supported diagram types and exit")
    args = parser.parse_args()

    if args.list_types:
        for t in sorted(KROKI_TYPES):
            print(t)
        aliases = ", ".join(f"{k}→{v}" for k, v in sorted(TYPE_ALIASES.items()))
        print(f"\nAliases: {aliases}")
        return 0

    if not args.type:
        parser.error("the following arguments are required: --type")

    diagram_type = normalize_type(args.type)
    if diagram_type not in KROKI_TYPES:
        sorted_types = ", ".join(sorted(KROKI_TYPES))
        aliases = ", ".join(f"{k}→{v}" for k, v in sorted(TYPE_ALIASES.items()))
        print(f"Unsupported type: {diagram_type}", file=sys.stderr)
        print(f"Supported: {sorted_types}", file=sys.stderr)
        print(f"Aliases: {aliases}", file=sys.stderr)
        return 2

    output_format = detect_format_from_output(args.output_path, args.format)
    if output_format not in ("svg", "png", "pdf", "html", "jpeg", "txt", "base64"):
        print(f"Unsupported format: {output_format}. Use svg|png|pdf|jpeg|html.", file=sys.stderr)
        return 2

    try:
        source = read_source(args.input_path)
        if output_format == "html":
            if diagram_type == "mermaid" and not args.json:
                html = mermaid_html_template(source, title=args.title)
                data = html.encode("utf-8")
            else:
                svg_bytes = render_via_kroki(diagram_type, "svg", source, args.kroki_url, use_json=args.json)
                html = wrap_svg_in_html(svg_bytes, title=args.title)
                data = html.encode("utf-8")
        else:
            data = render_via_kroki(diagram_type, output_format, source, args.kroki_url, use_json=args.json)
    except urllib.error.HTTPError as e:
        msg = e.read().decode("utf-8", errors="replace")
        print(f"Kroki HTTP {e.code}: {msg}", file=sys.stderr)
        if e.code == 403:
            print("Hint: public Kroki may rate-limit; use --kroki-url to specify a private instance.", file=sys.stderr)
        return 1
    except urllib.error.URLError as e:
        print(f"Cannot connect to Kroki ({args.kroki_url}): {e.reason}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.output_path:
        with open(args.output_path, "wb") as f:
            f.write(data)
    else:
        if output_format in ("html", "svg", "txt", "base64"):
            sys.stdout.write(data.decode("utf-8", errors="replace"))
        else:
            sys.stdout.buffer.write(data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
