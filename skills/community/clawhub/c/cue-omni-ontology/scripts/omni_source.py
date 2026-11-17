"""Turn a saved Cue Omni Reader result into a cue-omni-ontology source: exact content bytes + page_spans.

`ontology.py omni-source RESULT.json --out DIR --id ... --url ... --title ... --accessed-at ...` writes
  DIR/<stem>.md            the Omni content, byte-for-byte (its sha256 digest is checked)
  DIR/<stem>.source.json   a source record (parse_origin + sha256 + page_spans) to paste into quote-draft.json `sources`
  DIR/FY<fy>.pages.jsonl   optional (--fy): one {"page","text"} line per page span, the input `numeric-import --sources` reads

Result-shape handling is copied from cue-lead-pieces scripts/cue.py 0.4.2 (omni_response / bundle_from_response / Bridge),
which is regression-tested there against the real @cueai/omni-reader-mcp 1.8.x shapes. Copied, not imported: each skill
installs on its own.

Page mapping is conservative: a span is emitted only for grounding segments anchored to `source_pdf_page_1_based`
(basis omni_native_source_pdf_page). Text between segments of the SAME page joins that page; text between different pages,
segments with no page anchor, rendered-page-only anchors, multi-page segments and pages that reappear later stay uncovered,
so quotes there fall back to text_range evidence instead of a guessed page.

No parse is ever started here and no API key is read. Only when the saved result stores a part as an artifact is the user's
Omni Bridge started to read it back from the Bridge-local result cache (read_result: no key handled by this script, no credits).
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import time
from pathlib import Path

BRIDGE_DEFAULT = "npx -y @cueai/omni-reader-mcp@1.8.6"
OMNI = "omni_native_source_pdf_page"
STEM = re.compile(r"[^A-Za-z0-9_.-]+")


class OmniError(ValueError):
    pass


# ----------------------------------------------------------------------------- copied from cue-lead-pieces cue.py 0.4.2
class Bridge:
    """The official Cue Omni Reader MCP server over stdio. Used here only for read_result on artifact parts.
    The Bridge reads its key from its own environment or launcher; this module never reads, prints or passes a key."""

    def __init__(self, cmd=None, version="0"):
        import queue, shlex, subprocess, threading
        cmd = cmd or os.environ.get("CUE_OMNI_BRIDGE") or BRIDGE_DEFAULT
        try:
            self.p = subprocess.Popen(shlex.split(cmd), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                      stderr=subprocess.DEVNULL, text=True, bufsize=1)
        except OSError as e:
            raise OmniError(f"cannot start the Omni Bridge ({cmd.split()[0]}): {e.strerror}; set CUE_OMNI_BRIDGE to your omni-reader MCP command")
        self.q, self.i = queue.Queue(), 0
        threading.Thread(target=lambda: [self.q.put(line) for line in self.p.stdout], daemon=True).start()
        self.rpc("initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                                "clientInfo": {"name": "cue-omni-ontology", "version": version}}, 240)
        self.p.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n"); self.p.stdin.flush()

    def rpc(self, method, params, timeout=300):
        import queue
        self.i += 1
        self.p.stdin.write(json.dumps({"jsonrpc": "2.0", "id": self.i, "method": method, "params": params}) + "\n"); self.p.stdin.flush()
        end = time.time() + timeout
        while time.time() < end:
            try:
                line = self.q.get(timeout=2)
            except queue.Empty:
                if self.p.poll() is not None:
                    raise OmniError("the Omni Bridge exited (check CUE_OMNI_BRIDGE and run its `doctor --json`)")
                continue
            try:
                m = json.loads(line)
            except ValueError:
                continue
            if m.get("id") == self.i:
                if "error" in m:
                    raise OmniError(f"Omni Bridge {method}: {m['error'].get('message', m['error'])}")
                return m.get("result") or {}
        raise OmniError(f"Omni Bridge {method}: no answer within {timeout}s")

    def tool(self, name, args, timeout=300):
        r = self.rpc("tools/call", {"name": name, "arguments": args}, timeout)
        if isinstance(r.get("structuredContent"), dict):
            return r["structuredContent"]
        for c in r.get("content") or []:
            try:
                return json.loads(c.get("text", ""))
            except ValueError:
                return {"status": "completed", "result": {"kind": "inline", "text": c.get("text", "")}}
        return r

    def close(self):
        try:
            self.p.stdin.close(); self.p.terminate(); self.p.wait(10)
        except Exception:
            pass


def omni_response(o):
    """The parse / get_parse_status body inside whatever was saved: a full tools/call JSON-RPC response, its
    structuredContent, or the compact JSON from content[0].text."""
    if isinstance(o, dict) and "jsonrpc" in o and isinstance(o.get("result"), dict) and (
            "structuredContent" in o["result"] or "content" in o["result"]):
        o = o["result"]
    if isinstance(o, dict) and isinstance(o.get("structuredContent"), dict):
        return o["structuredContent"]
    if isinstance(o, dict) and isinstance(o.get("content"), list) and "status" not in o:
        for c in o["content"]:
            try:
                return json.loads(c.get("text", ""))
            except (ValueError, AttributeError):
                return {"status": "completed", "result": {"kind": "inline", "text": c.get("text", "")}}
    return o


def bundle_from_response(b, bridge=None, version="0"):
    """Real Bridge shape (1.8.x): result = {kind: bundle, bundle_protocol_version: omni.result_bundle.v1,
    parts: {content, grounding}}; each part is stored inline (text / value) or as an artifact (next_cursor ->
    Bridge-local read_result). Small results stay inline even when artifact delivery was requested."""
    res = b.get("result") or {}
    parts = res.get("parts") or {}
    out = {}
    for name in ("content", "grounding"):
        st = (parts.get(name) or {}).get("storage") or {}
        if st.get("kind") == "inline":
            out[name] = st.get("text") if "text" in st else st.get("value")
        elif st.get("kind") == "artifact":
            own = bridge is None
            br = bridge or Bridge(version=version)
            buf, cur = [], st.get("next_cursor")
            try:
                while cur:
                    r = br.tool("read_result", {"result_id": res.get("result_id"), "cursor": cur, "max_bytes": 65536}, 120)
                    if r.get("status") != "completed":
                        raise OmniError(f"read_result({name}) {r.get('status')}: {(r.get('error') or {}).get('code', '')} - the local "
                                        "result may have expired (see expires_at); re-parsing may be billed, ask the user first")
                    rr = r.get("result") or {}
                    buf.append(rr.get("text") or "")
                    cur = rr.get("next_cursor")
            finally:
                if own:
                    br.close()
            joined = "".join(buf)
            out[name] = joined if name == "content" else (json.loads(joined) if joined else {})
        if name == "grounding" and isinstance(out.get(name), str):      # grounding sometimes arrives as JSON text
            out[name] = json.loads(out[name]) if out[name] else {}
    if not isinstance(out.get("content"), str):
        raise OmniError("Omni result has no content part")
    dg = (parts.get("content") or {}).get("digest", "")
    if dg.startswith("sha256:") and hashlib.sha256(out["content"].encode("utf-8")).hexdigest() != dg[7:]:
        raise OmniError("Omni content does not match its sha256 digest (incomplete read?); nothing written")
    return {"detail": res.get("detail", "grounded"), "result_id": res.get("result_id"),
            "content": out["content"], "grounding": out.get("grounding") or {}}
# ----------------------------------------------------------------------------- end of copied code


def _find(o, pred):
    if pred(o):
        return o
    for v in (o.values() if isinstance(o, dict) else o if isinstance(o, list) else ()):
        x = _find(v, pred)
        if x is not None:
            return x
    return None


ERROR_HINTS = {
    "DETAIL_CAPABILITIES_UNAVAILABLE": "this Bridge cannot do grounded parsing for that source (measured with Bridge 1.8.3 on local files); "
                                       "use a public URL, or package the text with manual/synthetic pages",
    "SOURCE_ACCESS_DENIED": "Omni could not fetch this URL (measured for SEC EDGAR); download the file and package it yourself",
}


def load_bundle(path, bridge=None, version="0"):
    """Saved result file -> {content, grounding, detail}. Rejects plain Markdown / save_result text (no page sidecar)."""
    raw = Path(path).read_bytes().decode("utf-8")
    try:
        o = json.loads(raw)
    except ValueError:
        raise OmniError(f"{path}: not JSON. Plain Markdown (or text written by save_result) has no grounding sidecar, so page "
                        "numbers are lost; keep the tool call's structuredContent or the finished JSON response instead "
                        "(or pass --text-only to package it without page_spans)")
    b = omni_response(o)
    if isinstance(b, dict) and b.get("status") not in (None, "completed"):
        code = (b.get("error") or {}).get("code", "")
        raise OmniError(f"{path}: Omni status is {b.get('status')} {code}".rstrip() + "; nothing to package"
                        + (f" - {ERROR_HINTS[code]}" if code in ERROR_HINTS else ""))
    if isinstance(b, dict) and (b.get("result") or {}).get("kind") == "bundle":
        return bundle_from_response(b, bridge, version)
    full = _find(o, lambda x: isinstance(x, dict) and x.get("protocol_version") == "omni.result_bundle.v1")
    if full and isinstance((full.get("content") or {}).get("text"), str):
        return {"detail": full.get("detail", "grounded"), "result_id": None,
                "content": full["content"]["text"], "grounding": (full.get("grounding") or {}).get("value") or {}}
    t = _find(b, lambda x: isinstance(x, dict) and isinstance(x.get("text"), str) and x["text"])
    if t is None:
        raise OmniError(f"{path}: no Omni result found (expected a completed parse response or an omni.result_bundle.v1 bundle)")
    return {"detail": "text", "result_id": None, "content": t["text"], "grounding": {}}


def page_spans(content, grounding):
    """Grounding segments -> ordered, non-overlapping, unique-page spans over the content's UTF-8 bytes."""
    raw = content.encode("utf-8")
    warns, spans, seen = [], [], set()
    skipped = {"no_page_anchor": 0, "rendered_page_only": 0, "multi_page": 0, "page_reappears": 0, "bad_range": 0}
    segs = sorted((grounding or {}).get("segments") or [], key=lambda s: (s.get("content_range_utf8") or {}).get("start", 0))
    for sg in segs:
        rg = sg.get("content_range_utf8") or {}
        st, en = rg.get("start"), rg.get("end")
        anchors = [a for a in (sg.get("grounding") or {}).get("anchors") or [] if a.get("kind") == "page"]
        pages = {a.get("value") for a in anchors if a.get("basis") == "source_pdf_page_1_based"}
        if not (type(st) is int and type(en) is int and 0 <= st < en <= len(raw)):
            skipped["bad_range"] += 1; continue
        try:
            raw[:st].decode("utf-8"); raw[st:en].decode("utf-8")
        except UnicodeDecodeError:
            skipped["bad_range"] += 1; continue
        if not pages:
            skipped["rendered_page_only" if anchors else "no_page_anchor"] += 1; continue
        if len(pages) > 1:
            skipped["multi_page"] += 1; continue
        p = pages.pop()
        if type(p) is not int or p < 1:
            skipped["bad_range"] += 1; continue
        if spans and spans[-1]["page"] == p and st >= spans[-1]["end_utf8"]:
            spans[-1]["end_utf8"] = en                       # same page continues; the gap between its segments joins it
        elif p in seen:
            skipped["page_reappears"] += 1
        elif spans and st < spans[-1]["end_utf8"]:
            skipped["bad_range"] += 1
        else:
            spans.append({"page": p, "start_utf8": st, "end_utf8": en, "basis": OMNI}); seen.add(p)
    for k, n in skipped.items():
        if n:
            warns.append(f"{n} grounding segment(s) skipped ({k}); their text gets text_range evidence, not a page")
    covered = sum(s["end_utf8"] - s["start_utf8"] for s in spans)
    if spans and covered < len(raw):
        warns.append(f"{len(raw) - covered} of {len(raw)} content bytes are outside every page span (separators or unanchored text)")
    doc = (grounding or {}).get("document") or {}
    if doc.get("partial"):
        warns.append("Omni marked the document as partial")
    for x in doc.get("incomplete") or []:
        warns.append(f"incomplete {x.get('kind', '')} {x.get('values', '')} ({x.get('reason', '')})")
    for x in doc.get("truncated") or []:
        warns.append(f"truncated {x.get('count', '')} {x.get('kind', '')}(s) ({x.get('reason', '')})")
    return spans, warns


def build_source(result_path, out_dir, meta, parse_origin="omni_live", fy=None, stem=None, text_only=False,
                 bridge=None, version="0", validators=None):
    """Write <stem>.md, <stem>.source.json (and FY<fy>.pages.jsonl) under out_dir; never overwrites a file."""
    if parse_origin not in {"omni_live", "omni_replay"}:
        raise OmniError("parse_origin must be omni_live (fresh result) or omni_replay (a saved result re-used later)")
    try:
        b = load_bundle(result_path, bridge, version)
    except OmniError:
        if not text_only:
            raise
        txt = Path(result_path).read_bytes().decode("utf-8")
        b = {"detail": "text", "result_id": None, "content": txt, "grounding": {}}
    spans, warns = page_spans(b["content"], b["grounding"])
    if not spans:
        if not text_only:
            raise OmniError("the result has no source-PDF page anchors (detail=text, rendered pages only, or a non-PDF source); "
                            "re-run with --text-only to package it without page_spans (every quote then gets text_range evidence)")
        warns.append("packaged without page_spans: evidence will use text_range locators")
    if validators:
        validators(meta)
    stem = STEM.sub("_", stem or meta["id"]).strip("._") or "source"
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    targets = [out / f"{stem}.md", out / f"{stem}.source.json"] + ([out / f"FY{int(fy)}.pages.jsonl"] if fy else [])
    clash = [t.name for t in targets if t.exists()]
    if clash:
        raise OmniError(f"refusing to overwrite {', '.join(clash)} in {out}")
    raw = b["content"].encode("utf-8")
    targets[0].write_bytes(raw)
    record = dict(meta, parse_origin=parse_origin, content_file=targets[0].name,
                  sha256=hashlib.sha256(raw).hexdigest(), page_spans=spans)
    targets[1].write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if fy:
        lines = [json.dumps({"page": s["page"], "text": raw[s["start_utf8"]:s["end_utf8"]].decode("utf-8")}, ensure_ascii=False)
                 for s in spans]
        targets[2].write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    return {"status": "written", "content_file": str(targets[0]), "source_record": str(targets[1]),
            "pages_jsonl": str(targets[2]) if fy else None, "content_bytes": len(raw), "detail": b["detail"],
            "pages": [s["page"] for s in spans], "warnings": warns,
            "next": "copy the source record into quote-draft.json `sources` (content_file is relative to the draft), then run prepare"}
