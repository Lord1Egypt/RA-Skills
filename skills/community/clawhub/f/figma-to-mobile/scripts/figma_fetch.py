#!/usr/bin/env python3
"""Fetch and simplify Figma node data for mobile code generation."""

import json
import os
import re
import sys
import time

try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Run: python -m pip install requests")
    sys.exit(1)


def parse_figma_url(url: str):
    """Extract file_key and node_id from a Figma URL."""
    file_match = re.search(r"figma\.com/(?:file|design)/([a-zA-Z0-9]+)", url)
    node_match = re.search(r"node-id=([0-9]+[-:][0-9]+)", url)
    if not file_match:
        return None, None
    file_key = file_match.group(1)
    node_id = node_match.group(1).replace("-", ":") if node_match else None
    return file_key, node_id


def rgba_to_hex(color: dict) -> str:
    """Convert Figma RGBA (0-1) to hex #RRGGBB or #AARRGGBB."""
    r = round(color.get("r", 0) * 255)
    g = round(color.get("g", 0) * 255)
    b = round(color.get("b", 0) * 255)
    a = round(color.get("a", 1) * 255)
    if a == 255:
        return f"#{r:02X}{g:02X}{b:02X}"
    return f"#{a:02X}{r:02X}{g:02X}{b:02X}"

def extract_effects(node: dict) -> list:
    """Extract shadow and blur effects from a node."""
    effects = node.get("effects", [])
    result = []
    for effect in effects:
        if not effect.get("visible", True):
            continue
        etype = effect.get("type")
        if etype in ("DROP_SHADOW", "INNER_SHADOW"):
            shadow = {"type": etype.lower().replace("_", "-")}
            color = effect.get("color")
            if color:
                shadow["color"] = rgba_to_hex(color)
            offset = effect.get("offset", {})
            shadow["offsetX"] = offset.get("x", 0)
            shadow["offsetY"] = offset.get("y", 0)
            shadow["radius"] = effect.get("radius", 0)
            shadow["spread"] = effect.get("spread", 0)
            result.append(shadow)
        elif etype == "LAYER_BLUR":
            result.append({"type": "blur", "radius": effect.get("radius", 0)})
    return result


def extract_fills(fills: list) -> dict:
    """Extract fill info: solid color, image, or gradient."""
    result = {}
    for fill in fills:
        if not fill.get("visible", True):
            continue
        ftype = fill.get("type")
        if ftype == "SOLID":
            result["backgroundColor"] = rgba_to_hex(fill.get("color", {}))
            break
        elif ftype == "IMAGE":
            result["hasImage"] = True
            break
        elif ftype in ("GRADIENT_LINEAR", "GRADIENT_RADIAL", "GRADIENT_ANGULAR", "GRADIENT_DIAMOND"):
            grad = {"type": ftype}
            stops = fill.get("gradientStops", [])
            if stops:
                grad["stops"] = [
                    {"color": rgba_to_hex(s.get("color", {})), "position": round(s.get("position", 0), 3)}
                    for s in stops
                ]
            result["gradient"] = grad
            break
    return result

def simplify_node(node: dict, parent_pos: dict = None) -> dict:
    """Simplify a Figma node to only the info needed for code generation."""
    bbox = node.get("absoluteBoundingBox") or {}
    node_type = node.get("type")
    result = {
        "id": node.get("id"),
        "type": node_type,
        "name": node.get("name"),
        "width": bbox.get("width"),
        "height": bbox.get("height"),
    }

    # Component instance detection
    if node_type == "INSTANCE":
        comp_id = node.get("componentId")
        if comp_id:
            result["componentId"] = comp_id
        # Variant properties (e.g. State=Default, Size=Large)
        variant_props = node.get("componentProperties", {})
        if variant_props:
            result["variantProperties"] = {
                k: v.get("value") for k, v in variant_props.items()
                if v.get("value") is not None
            }

    # Relative position
    if parent_pos and bbox:
        result["x"] = round(bbox.get("x", 0) - parent_pos.get("x", 0), 1)
        result["y"] = round(bbox.get("y", 0) - parent_pos.get("y", 0), 1)

    # Fills (background color, image, or gradient)
    fills = node.get("fills", [])
    fill_info = extract_fills(fills)
    result.update(fill_info)

    # Effects (shadows, blur)
    effects = extract_effects(node)
    if effects:
        result["effects"] = effects

    # Border / strokes
    strokes = node.get("strokes", [])
    for stroke in strokes:
        if stroke.get("type") == "SOLID" and stroke.get("visible", True):
            result["borderColor"] = rgba_to_hex(stroke.get("color", {}))
            result["borderWidth"] = node.get("strokeWeight", 1)
            break

    # Corner radius (uniform or per-corner)
    cr = node.get("cornerRadius")
    if cr and cr > 0:
        result["cornerRadius"] = cr
    else:
        radii = node.get("rectangleCornerRadii")
        if radii and any(r > 0 for r in radii):
            result["cornerRadii"] = radii  # [topLeft, topRight, bottomRight, bottomLeft]

    # Text properties
    if node_type == "TEXT":
        result["text"] = node.get("characters", "")
        style = node.get("style", {})
        if style:
            result["fontSize"] = style.get("fontSize")
            result["fontWeight"] = style.get("fontWeight")
            result["fontFamily"] = style.get("fontFamily")
            result["textAlignHorizontal"] = style.get("textAlignHorizontal")
            result["lineHeightPx"] = style.get("lineHeightPx")
            result["letterSpacing"] = style.get("letterSpacing")
        # Text auto-resize mode (affects wrap_content vs fixed size)
        text_auto_resize = node.get("style", {}).get("textAutoResize")
        if not text_auto_resize:
            text_auto_resize = node.get("textAutoResize")
        if text_auto_resize and text_auto_resize != "NONE":
            result["textAutoResize"] = text_auto_resize
        # Text color from fills
        for fill in fills:
            if fill.get("type") == "SOLID" and fill.get("visible", True):
                result["textColor"] = rgba_to_hex(fill.get("color", {}))
                break

    # Auto-layout
    layout_mode = node.get("layoutMode")
    if layout_mode:
        result["layoutMode"] = layout_mode
        result["itemSpacing"] = node.get("itemSpacing", 0)
        result["paddingLeft"] = node.get("paddingLeft", 0)
        result["paddingRight"] = node.get("paddingRight", 0)
        result["paddingTop"] = node.get("paddingTop", 0)
        result["paddingBottom"] = node.get("paddingBottom", 0)
        paa = node.get("primaryAxisAlignItems")
        if paa:
            result["primaryAxisAlignItems"] = paa
        caa = node.get("counterAxisAlignItems")
        if caa:
            result["counterAxisAlignItems"] = caa
        pss = node.get("primaryAxisSizingMode")
        if pss:
            result["primaryAxisSizingMode"] = pss
        css = node.get("counterAxisSizingMode")
        if css:
            result["counterAxisSizingMode"] = css
        lg = node.get("layoutGrow")
        if lg:
            result["layoutGrow"] = lg

    # Child layout properties (applicable even when parent has no layoutMode,
    # these are set on the child node itself within an auto-layout parent)
    layout_align = node.get("layoutAlign")
    if layout_align and layout_align != "INHERIT":
        result["layoutAlign"] = layout_align  # STRETCH = fill cross-axis
    layout_positioning = node.get("layoutPositioning")
    if layout_positioning and layout_positioning != "AUTO":
        result["layoutPositioning"] = layout_positioning  # ABSOLUTE = ignore auto-layout

    # Figma shared styles (design token references)
    styles_ref = node.get("styles")
    if styles_ref:
        result["styleRefs"] = styles_ref  # e.g. {"fill": "S:abc...", "text": "S:def..."}

    # Opacity
    opacity = node.get("opacity")
    if opacity is not None and opacity < 1:
        result["opacity"] = round(opacity, 3)

    # Visibility
    if not node.get("visible", True):
        result["visible"] = False

    # Children
    children = node.get("children", [])
    if children:
        current_pos = {"x": bbox.get("x", 0), "y": bbox.get("y", 0)}
        result["children"] = [
            simplify_node(child, current_pos)
            for child in children
            if child.get("visible", True)
        ]

    return result

def has_truncated_children(node: dict) -> bool:
    """Check if any node looks like it should have children but doesn't.
    Heuristic: FRAME/GROUP/INSTANCE/COMPONENT with no children but non-trivial size."""
    ntype = node.get("type")
    children = node.get("children", [])
    if ntype in ("FRAME", "GROUP", "INSTANCE", "COMPONENT", "COMPONENT_SET") and not children:
        bbox = node.get("absoluteBoundingBox") or {}
        w = bbox.get("width", 0)
        h = bbox.get("height", 0)
        if w > 10 and h > 10:
            return True
    for child in children:
        if has_truncated_children(child):
            return True
    return False


_last_request_time = 0

def _rate_limit():
    """Ensure at least 2 seconds between Figma API requests."""
    global _last_request_time
    elapsed = time.time() - _last_request_time
    if elapsed < 2.0:
        time.sleep(2.0 - elapsed)
    _last_request_time = time.time()


def _request_with_retry(url: str, headers: dict, timeout: int = 30, max_retries: int = 3) -> requests.Response:
    """Make a GET request with retry on 429/SSL errors."""
    _rate_limit()
    for attempt in range(max_retries):
        try:
            resp = requests.get(url, headers=headers, timeout=timeout)
            if resp.status_code == 429:
                raw_wait = int(resp.headers.get("Retry-After", 10 * (attempt + 1)))
                plan_tier = resp.headers.get("X-Figma-Plan-Tier", "unknown")
                limit_type = resp.headers.get("X-Figma-Rate-Limit-Type", "unknown")
                MAX_RETRY_WAIT = 120  # Never wait more than 2 minutes
                if raw_wait > MAX_RETRY_WAIT:
                    hours = raw_wait // 3600
                    mins = (raw_wait % 3600) // 60
                    msg = f"Figma API rate limited for {raw_wait}s ({hours}h {mins}m)."
                    if plan_tier.lower() in ("starter",) or limit_type == "monthly":
                        msg += (" Your Figma seat (View/Collab) only allows ~6 API calls per month."
                                " Ask your Figma admin to upgrade your seat to Dev or Full "
                                "for much higher limits (10-20 requests/minute).")
                    else:
                        msg += f" Plan tier: {plan_tier}, limit type: {limit_type}."
                    print(json.dumps({
                        "status": "error",
                        "error": "RATE_LIMIT_EXCEEDED",
                        "message": msg,
                        "retry_after_seconds": raw_wait,
                        "plan_tier": plan_tier,
                        "limit_type": limit_type
                    }))
                    sys.exit(1)
                print(f"  Rate limited (429), waiting {raw_wait}s...", file=sys.stderr)
                time.sleep(raw_wait)
                continue
            return resp
        except (requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
            if attempt < max_retries - 1:
                wait = 5 * (attempt + 1)
                print(f"  Connection error, retrying in {wait}s... ({e.__class__.__name__})", file=sys.stderr)
                time.sleep(wait)
            else:
                raise
    # Final attempt after all retries exhausted
    return requests.get(url, headers=headers, timeout=timeout)


def fetch_node(file_key: str, node_id: str, token: str, depth: int = 5) -> dict:
    """Fetch a node from Figma API with adaptive depth."""
    api_node_id = node_id.replace(":", "-")
    url = f"https://api.figma.com/v1/files/{file_key}/nodes?ids={api_node_id}&depth={depth}"
    headers = {"X-Figma-Token": token}
    resp = _request_with_retry(url, headers)
    resp.raise_for_status()
    data = resp.json()

    if "err" in data:
        raise Exception(f"Figma API error: {data['err']}")

    node_data = data.get("nodes", {}).get(node_id)
    if not node_data:
        raise Exception(f"Node {node_id} not found in response")

    document = node_data["document"]

    # Adaptive depth: if children seem truncated, retry with deeper depth
    if depth < 15 and has_truncated_children(document):
        new_depth = min(depth + 5, 15)
        print(f"Depth {depth} may be insufficient, retrying with depth={new_depth}...", file=sys.stderr)
        return fetch_node(file_key, node_id, token, new_depth)

    return document





# ---------------------------------------------------------------------------
# Multi-node compare helpers
# ---------------------------------------------------------------------------

def _node_key(node: dict) -> str:
    """Build a match key for a simplified node: name + type + rounded position."""
    name = (node.get("name") or "").strip()
    ntype = node.get("type") or ""
    x = round(node.get("x", 0) / 4) * 4   # bucket to nearest 4px to absorb minor drift
    y = round(node.get("y", 0) / 4) * 4
    return f"{name}|{ntype}|{x},{y}"


_COMPARE_SKIP_KEYS = {"id", "children"}

_SCALAR_KEYS = {
    "backgroundColor", "opacity", "visible", "text", "textColor",
    "fontSize", "fontWeight", "fontFamily", "textAlignHorizontal",
    "lineHeightPx", "letterSpacing", "textAutoResize",
    "width", "height", "x", "y", "cornerRadius", "cornerRadii",
    "borderColor", "borderWidth",
    "layoutMode", "itemSpacing",
    "paddingLeft", "paddingRight", "paddingTop", "paddingBottom",
    "primaryAxisAlignItems", "counterAxisAlignItems",
    "primaryAxisSizingMode", "counterAxisSizingMode",
    "layoutGrow", "layoutAlign", "layoutPositioning",
    "hasImage",
}


def _diff_nodes(base: dict, other: dict, path: str, results: list) -> None:
    """Recursively diff two simplified nodes. Appends change/added/removed entries."""
    # --- scalar attribute diff ---
    changes = {}
    for key in _SCALAR_KEYS:
        bv = base.get(key)
        ov = other.get(key)
        if bv != ov and not (bv is None and ov is None):
            changes[key] = {"from": bv, "to": ov}

    # gradient diff (nested dict) — compare as opaque value
    bg = base.get("gradient")
    og = other.get("gradient")
    if bg != og:
        changes["gradient"] = {"from": bg, "to": og}

    # effects diff — compare as opaque list
    be = base.get("effects")
    oe = other.get("effects")
    if be != oe:
        changes["effects"] = {"from": be, "to": oe}

    if changes:
        results.append({
            "path": path,
            "node_name": base.get("name") or other.get("name") or "",
            "changes": changes,
        })

    # --- children diff ---
    base_children = base.get("children", []) or []
    other_children = other.get("children", []) or []

    base_map = {}
    for i, child in enumerate(base_children):
        k = _node_key(child)
        # avoid key collision from identically-named nodes: append index suffix
        unique_k = k
        suffix = 0
        while unique_k in base_map:
            suffix += 1
            unique_k = f"{k}#{suffix}"
        base_map[unique_k] = (i, child)

    other_map = {}
    for i, child in enumerate(other_children):
        k = _node_key(child)
        unique_k = k
        suffix = 0
        while unique_k in other_map:
            suffix += 1
            unique_k = f"{k}#{suffix}"
        other_map[unique_k] = (i, child)

    base_keys = set(base_map)
    other_keys = set(other_map)

    for k in sorted(base_keys & other_keys):
        bi, bchild = base_map[k]
        oi, ochild = other_map[k]
        child_path = f"{path}.children[{bi}]" if path else f"children[{bi}]"
        _diff_nodes(bchild, ochild, child_path, results)

    for k in sorted(base_keys - other_keys):
        bi, bchild = base_map[k]
        child_path = f"{path}.children[{bi}]" if path else f"children[{bi}]"
        results.append({
            "_kind": "removed",
            "path": child_path,
            "node_name": bchild.get("name") or "",
        })

    for k in sorted(other_keys - base_keys):
        oi, ochild = other_map[k]
        child_path = f"{path}.children[{oi}]" if path else f"children[{oi}]"
        results.append({
            "_kind": "added",
            "path": child_path,
            "node_name": ochild.get("name") or "",
        })


def compare_nodes(nodes_data: list) -> dict:
    """
    Compare a list of simplified node dicts (all states).
    Returns the structured compare output with nodes[] and diff{}.
    nodes_data: list of {"node_id": str, "label": str, "data": dict}
    """
    if len(nodes_data) < 2:
        raise ValueError("compare_nodes requires at least 2 nodes")

    base_entry = nodes_data[0]
    base_data = base_entry["data"]

    all_changes = []
    all_added = []
    all_removed = []

    for other_entry in nodes_data[1:]:
        other_data = other_entry["data"]
        raw_results = []
        try:
            _diff_nodes(base_data, other_data, "", raw_results)
        except Exception as e:
            print(f"Warning: diff error between {base_entry['node_id']} and {other_entry['node_id']}: {e}",
                  file=sys.stderr)

        for item in raw_results:
            kind = item.pop("_kind", "changed")
            if kind == "added":
                all_added.append(item)
            elif kind == "removed":
                all_removed.append(item)
            else:
                all_changes.append(item)

    return {
        "nodes": nodes_data,
        "diff": {
            "changed": all_changes,
            "added": all_added,
            "removed": all_removed,
        },
    }


def export_svgs(file_key: str, node_ids: list, token: str) -> dict:
    """Export nodes as SVG via Figma API. Returns {node_id: svg_string}."""
    ids_param = ",".join(node_ids)
    url = f"https://api.figma.com/v1/images/{file_key}?ids={ids_param}&format=svg"
    headers = {"X-Figma-Token": token}
    _rate_limit()
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    results = {}
    images = data.get("images", {})
    for nid, svg_url in images.items():
        if svg_url:
            try:
                svg_resp = requests.get(svg_url, timeout=30)
                svg_resp.raise_for_status()
                results[nid] = svg_resp.text
            except Exception as e:
                print(f"Warning: failed to download SVG for {nid}: {e}", file=sys.stderr)
                results[nid] = None
        else:
            results[nid] = None
    return results


def _load_token() -> str | None:
    """Load FIGMA_TOKEN from environment, or a local dotenv file."""
    token = os.environ.get("FIGMA_TOKEN")
    if not token:
        for env_path in [".env.local", ".env"]:
            if not os.path.exists(env_path):
                continue
            with open(env_path, encoding="utf-8", errors="replace") as ef:
                for line in ef:
                    line = line.strip()
                    if line.startswith("FIGMA_TOKEN="):
                        token = line.split("=", 1)[1].strip().strip('"').strip("'")
                        break
            if token:
                break
    return token


def _require_token() -> str:
    """Return FIGMA_TOKEN or print instructions and exit."""
    token = _load_token()
    if not token:
        print("FIGMA_TOKEN_NOT_SET")
        print("")
        print("FIGMA_TOKEN is not set.")
        print("Do NOT paste tokens into chat logs or commit them to git.")
        print("")
        print("Recommended: set the FIGMA_TOKEN environment variable locally, then retry.")
        print("The token starts with 'figd_'. Get one at:")
        print("  Figma > avatar > Settings > Security > Personal Access Tokens")
        print("")
        print("If you insist on using a dotenv file, create/edit it locally and gitignore it:")
        print("  - .env.local (preferred) or .env in your project root")
        sys.exit(1)
    return token


def _write_output(output_json: str, output_file: str | None) -> None:
    """Write JSON to file or stdout."""
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output_json)
        print(f"Written to {output_file}", file=sys.stderr)
    else:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        print(output_json)


def main():
    args = sys.argv[1:]

    if not args:
        print("Usage: python figma_fetch.py <figma_url> [<figma_url2> ...] [options]")
        print("")
        print("Single node:")
        print("  python figma_fetch.py '<url_with_node_id>' [--depth N] [--export-svg id1,id2]")
        print("")
        print("Multi-state compare:")
        print("  python figma_fetch.py '<url1>' '<url2>' --compare")
        print("  python figma_fetch.py '<base_url>' --nodes '100:200,100:300' --compare")
        print("")
        print("Example:")
        print("  python figma_fetch.py 'https://www.figma.com/design/ABC/Project?node-id=100-200'")
        sys.exit(1)

    # -----------------------------------------------------------------------
    # Parse flags
    # -----------------------------------------------------------------------
    compare_mode = "--compare" in args
    depth = 5
    export_ids = None
    output_file = None
    extra_node_ids: list[str] = []   # from --nodes flag
    url_args: list[str] = []          # positional URL arguments

    i = 0
    while i < len(args):
        a = args[i]
        if a == "--depth" and i + 1 < len(args):
            depth = int(args[i + 1])
            i += 2
        elif a == "--export-svg" and i + 1 < len(args):
            export_ids = args[i + 1].split(",")
            i += 2
        elif a == "--output" and i + 1 < len(args):
            output_file = args[i + 1]
            i += 2
        elif a == "--nodes" and i + 1 < len(args):
            extra_node_ids = [nid.strip() for nid in args[i + 1].split(",") if nid.strip()]
            i += 2
        elif a == "--compare":
            i += 1  # already captured above
        elif not a.startswith("--"):
            url_args.append(a)
            i += 1
        else:
            i += 1  # unknown flag, skip

    if not url_args:
        print("ERROR: No Figma URL provided.")
        sys.exit(1)

    token = _require_token()

    # -----------------------------------------------------------------------
    # Compare mode
    # -----------------------------------------------------------------------
    if compare_mode:
        # Build list of (file_key, node_id) pairs to fetch
        targets: list[tuple[str, str]] = []

        base_url = url_args[0]
        base_file_key, base_node_id = parse_figma_url(base_url)
        if not base_file_key:
            print(f"ERROR: Could not parse Figma URL: {base_url}")
            sys.exit(1)

        if base_node_id:
            targets.append((base_file_key, base_node_id))

        # Additional URLs (url2, url3, ...)
        for extra_url in url_args[1:]:
            fk, nid = parse_figma_url(extra_url)
            if not fk:
                print(f"ERROR: Could not parse Figma URL: {extra_url}")
                sys.exit(1)
            if not nid:
                print(f"ERROR: URL must contain a node-id parameter: {extra_url}")
                sys.exit(1)
            targets.append((fk, nid))

        # --nodes flag: additional node IDs on the same file
        for nid in extra_node_ids:
            nid = nid.replace("-", ":")
            targets.append((base_file_key, nid))

        if len(targets) < 2:
            print("ERROR: --compare requires at least 2 node targets.")
            print("  Provide multiple URLs, or use --nodes '100:200,100:300'")
            sys.exit(1)

        # Fetch all nodes
        nodes_data = []
        for idx, (fk, nid) in enumerate(targets):
            print(f"Fetching node {nid} from file {fk} (depth={depth})...", file=sys.stderr)
            try:
                raw = fetch_node(fk, nid, token, depth)
            except Exception as e:
                print(f"ERROR fetching node {nid}: {e}")
                sys.exit(1)
            simplified = simplify_node(raw)
            label = simplified.get("name") or f"State {idx + 1}"
            nodes_data.append({
                "node_id": nid,
                "label": label,
                "data": simplified,
            })

        print(f"Comparing {len(nodes_data)} nodes...", file=sys.stderr)
        result = compare_nodes(nodes_data)
        output_json = json.dumps(result, indent=2, ensure_ascii=False)
        _write_output(output_json, output_file)
        return

    # -----------------------------------------------------------------------
    # Single-URL mode
    # -----------------------------------------------------------------------
    url = url_args[0]

    file_key, node_id = parse_figma_url(url)
    if not file_key:
        print(f"ERROR: Could not parse Figma URL: {url}")
        sys.exit(1)

    # SVG export mode
    if export_ids:
        print(f"Exporting {len(export_ids)} node(s) as SVG...", file=sys.stderr)
        svgs = export_svgs(file_key, export_ids, token)
        print(json.dumps(svgs, indent=2, ensure_ascii=False))
        return

    # Require a specific node-id (not the root canvas 0:1)
    if not node_id or node_id in ("0:1", "0-1"):
        print(json.dumps({
            "status": "error",
            "error": "NO_SPECIFIC_NODE",
            "message": "This link points to the entire page, not a specific frame. "
                       "Please select the frame you want in Figma, right-click it, "
                       "and choose 'Copy link to selection', then send that link."
        }))
        sys.exit(1)

    print(f"Fetching node {node_id} from file {file_key} (depth={depth})...", file=sys.stderr)
    raw_node = fetch_node(file_key, node_id, token, depth)
    simplified = simplify_node(raw_node)

    output_json = json.dumps(simplified, indent=2, ensure_ascii=False)
    _write_output(output_json, output_file)


if __name__ == "__main__":
    main()
