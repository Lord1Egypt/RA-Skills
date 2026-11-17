#!/usr/bin/env python3
"""Find EmpirioLabs AI models and their prices in the live public catalog.

Examples:
  python3 models.py --category image
  python3 models.py --endpoint audio/transcriptions
  python3 models.py --search "flux"
  python3 models.py --feature image_editing --featured
  python3 models.py --show flux-2-klein-4b
  python3 models.py --categories
  python3 models.py --category video --json

Reads GET https://api.empiriolabs.ai/v1/models, which is public: no API key is needed.
Python 3.8+, standard library only.
"""

from __future__ import annotations

import argparse
import gzip
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

__version__ = "1.0.0"

CATALOG_URL = "https://api.empiriolabs.ai/v1/models"
USER_AGENT = "empiriolabs-skills/" + __version__ + " (python-urllib)"
ALIASES = {
    "speech": "audio",
    "tts": "audio",
    "voice": "audio",
    "music": "audio",
    "stt": "transcription",
    "asr": "transcription",
    "chat": "text",
    "llm": "text",
    "embeddings": "embedding",
    "rerank": "reranker",
    "rerankers": "reranker",
    "images": "image",
    "videos": "video",
}


class CatalogError(Exception):
    pass


def _open(req, timeout):
    """The single network call. Tests replace this function."""
    return urllib.request.urlopen(req, timeout=timeout)


def fetch_json(url, timeout=60.0, attempts=4):
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json", "Accept-Encoding": "gzip"}
    for attempt in range(1, attempts + 1):
        req = urllib.request.Request(url, headers=headers, method="GET")
        try:
            with _open(req, timeout) as resp:
                body = resp.read()
                if (resp.headers.get("Content-Encoding") or "").lower() == "gzip":
                    body = gzip.decompress(body)
                return json.loads(body.decode("utf-8"))
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                raise CatalogError("Not found: " + url)
            if exc.code in (429, 500, 502, 503, 504) and attempt < attempts:
                time.sleep(min(2.0 ** attempt, 20.0))
                continue
            raise CatalogError("The catalog request failed with HTTP " + str(exc.code) + ".")
        except (urllib.error.URLError, OSError, ValueError) as exc:
            if attempt < attempts:
                time.sleep(min(2.0 ** attempt, 20.0))
                continue
            raise CatalogError("Could not read the catalog: " + str(getattr(exc, "reason", exc)))
    raise CatalogError("Could not read the catalog.")


def load_catalog():
    payload = fetch_json(CATALOG_URL)
    if not isinstance(payload, dict) or not isinstance(payload.get("data"), list):
        raise CatalogError("The catalog response was not in the expected format.")
    return payload


def price_rows(model):
    rows = []
    for row in model.get("pricing_rows") or []:
        if not isinstance(row, dict):
            continue
        label = str(row.get("label") or "").strip()
        value = " ".join(p for p in (str(row.get("value") or "").strip(), str(row.get("spec") or "").strip()) if p)
        rows.append(label + ": " + value if label else value)
    return rows


def price_summary(model, limit=2):
    rows = price_rows(model)
    if not rows:
        return "see " + str(model.get("api_url") or "https://empiriolabs.ai/pricing")
    text = "; ".join(rows[:limit])
    return text + ("; +" + str(len(rows) - limit) + " more" if len(rows) > limit else "")


def endpoint_matches(model, wanted):
    wanted = wanted.strip().lower()
    for endpoint in model.get("supported_endpoints") or []:
        if wanted in endpoint.lower():
            return True
    return False


def search_matches(model, words):
    haystack = " ".join([
        str(model.get("id") or ""),
        str(model.get("display_name") or ""),
        str(model.get("description") or ""),
        str(model.get("author") or ""),
        " ".join(model.get("aliases") or []),
        " ".join(model.get("features") or []),
    ]).lower()
    return all(word in haystack for word in words)


def filter_models(models, args):
    category = ALIASES.get((args.category or "").lower(), (args.category or "").lower()) or None
    words = [w for w in (args.search or "").lower().split() if w]
    out = []
    for model in models:
        if category and model.get("category") != category:
            continue
        if args.endpoint and not endpoint_matches(model, args.endpoint):
            continue
        if args.feature and args.feature not in (model.get("features") or []):
            continue
        if args.featured and not model.get("is_featured"):
            continue
        if words and not search_matches(model, words):
            continue
        out.append(model)
    return out


def compact(model):
    return {
        "id": model.get("id"),
        "name": model.get("display_name"),
        "category": model.get("category"),
        "featured": bool(model.get("is_featured")),
        "endpoints": model.get("supported_endpoints") or [],
        "prices": price_rows(model),
        "docs": model.get("api_url"),
    }


def print_table(models, total):
    for model in models:
        mark = "*" if model.get("is_featured") else " "
        print(mark + " " + str(model.get("id")).ljust(34) + " " + str(model.get("category") or "").ljust(13)
              + " " + price_summary(model))
    shown = len(models)
    note = str(shown) + " of " + str(total) + " matching models" if shown < total else str(total) + " matching models"
    sys.stdout.flush()
    print("\n" + note + ". * marks featured models. Use --show MODEL_ID for parameters and full pricing.",
          file=sys.stderr)


def describe(model):
    lines = [
        str(model.get("display_name") or model.get("id")) + " (" + str(model.get("id")) + ")",
        "Category: " + str(model.get("category")),
    ]
    if model.get("author"):
        lines.append("Author: " + str(model.get("author")))
    if model.get("description"):
        lines.append("Description: " + str(model.get("description")))
    if model.get("supported_endpoints"):
        lines.append("Endpoints: " + ", ".join(model["supported_endpoints"]))
    io_in = ", ".join(model.get("input_modalities") or [])
    io_out = ", ".join(model.get("output_modalities") or [])
    if io_in or io_out:
        lines.append("Input: " + (io_in or "-") + "  Output: " + (io_out or "-"))
    if model.get("features"):
        lines.append("Features: " + ", ".join(model["features"]))
    if model.get("context_window"):
        lines.append("Context window: " + str(model["context_window"]) + " tokens")
    if model.get("max_output_tokens"):
        lines.append("Max output: " + str(model["max_output_tokens"]) + " tokens")
    rows = price_rows(model)
    lines.append("Pricing:" if rows else "Pricing: see " + str(model.get("api_url") or "https://empiriolabs.ai/pricing"))
    lines.extend("  " + row for row in rows)
    params = [p for p in model.get("supported_parameters") or [] if isinstance(p, dict)]
    if params:
        lines.append("Parameters:")
        for param in params:
            bits = [str(param.get("type") or "")]
            if param.get("required"):
                bits.append("required")
            if param.get("default") not in (None, ""):
                bits.append("default " + json.dumps(param.get("default")))
            if param.get("options"):
                options = [str(o) for o in param["options"]]
                bits.append("options " + ", ".join(options[:12]) + (", ..." if len(options) > 12 else ""))
            low, high = param.get("min"), param.get("max")
            if low is not None and high is not None:
                bits.append("range " + str(low) + " to " + str(high))
            elif high is not None:
                bits.append("up to " + str(high))
            elif low is not None:
                bits.append("at least " + str(low))
            lines.append("  " + str(param.get("name")).ljust(24) + " " + "; ".join(b for b in bits if b))
    limits = model.get("limits")
    note = limits.get("note") if isinstance(limits, dict) else None
    if note:
        lines.append("Notes:")
        lines.extend("  " + line for line in str(note).strip().splitlines() if line.strip())
    if model.get("api_url"):
        lines.append("Docs: " + str(model["api_url"]))
    if model.get("chat_url"):
        lines.append("Playground: " + str(model["chat_url"]))
    return "\n".join(lines)


def build_parser():
    parser = argparse.ArgumentParser(
        prog="models.py",
        description="Find EmpirioLabs AI models and prices in the live public catalog (no API key needed).",
        epilog="Prices are final per-request prices. Pricing page: https://empiriolabs.ai/pricing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--category", help="text, image, video, audio, transcription, research, 3d, embedding, "
                                           "reranker, tools, or decision (see --categories).")
    parser.add_argument("--endpoint", help="Only models serving this endpoint, for example images/generations.")
    parser.add_argument("--search", help="Words that must all appear in the id, name, description, or features.")
    parser.add_argument("--feature", help="Only models with this feature, for example image_editing or reasoning.")
    parser.add_argument("--featured", action="store_true", help="Only featured models.")
    parser.add_argument("--limit", type=int, default=60, help="Maximum rows to print (default 60, 0 for all).")
    parser.add_argument("--show", metavar="MODEL_ID", help="Show parameters, pricing, and notes for one model.")
    parser.add_argument("--categories", action="store_true", help="List categories with model counts.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of text.")
    return parser


def run(args):
    if args.show:
        try:
            model = fetch_json(CATALOG_URL + "/" + urllib.parse.quote(args.show, safe=""))
        except CatalogError:
            model = None
        if not isinstance(model, dict) or not model.get("id"):
            catalog = load_catalog()
            wanted = args.show.lower()
            model = next((m for m in catalog["data"] if str(m.get("id", "")).lower() == wanted
                          or wanted in [a.lower() for a in m.get("aliases") or []]), None)
        if not model:
            print("Error: no model with id " + args.show + ". Try --search.", file=sys.stderr)
            return 1
        print(json.dumps(model, indent=2, ensure_ascii=False) if args.json else describe(model))
        return 0
    catalog = load_catalog()
    models = catalog["data"]
    if args.categories:
        counts = {}
        for model in models:
            counts[model.get("category")] = counts.get(model.get("category"), 0) + 1
        rows = [{"slug": c.get("slug"), "name": c.get("name"), "models": counts.get(c.get("slug"), 0)}
                for c in catalog.get("categories") or [] if isinstance(c, dict)]
        if args.json:
            print(json.dumps(rows, indent=2))
        else:
            for row in rows:
                print(str(row["slug"]).ljust(14) + " " + str(row["models"]).rjust(4) + "  " + str(row["name"]))
        return 0
    matched = filter_models(models, args)
    limited = matched if args.limit <= 0 else matched[: args.limit]
    if args.json:
        print(json.dumps([compact(m) for m in limited], indent=2, ensure_ascii=False))
    else:
        print_table(limited, len(matched))
    return 0


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="backslashreplace")
        except (AttributeError, ValueError):
            pass
    args = build_parser().parse_args(argv)
    try:
        return run(args)
    except CatalogError as exc:
        print("Error: " + str(exc), file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
