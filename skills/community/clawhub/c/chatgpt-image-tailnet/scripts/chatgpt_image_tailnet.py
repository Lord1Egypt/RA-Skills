#!/usr/bin/env python3
import argparse
import base64
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, UTC

DEFAULT_BASE = "http://100.89.48.48:9377"
CHATGPT_URL = "https://chatgpt.com/"


def request(base, method, path, params=None, body=None, timeout=60):
    url = base.rstrip("/") + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    data = None
    headers = {"Content-Type": "application/json"}
    if body is not None:
        data = json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode()
        return json.loads(raw) if raw else {"ok": True}


def open_tab(base, user, session, url):
    out = request(base, "POST", "/tabs", body={"userId": user, "sessionKey": session, "url": url})
    return out["tabId"]


def wait_tab(base, user, tab, ms=12000):
    return request(base, "POST", f"/tabs/{tab}/wait", body={"userId": user, "timeout": ms, "waitForNetwork": False})


def snapshot_text(base, user, tab):
    out = request(base, "GET", f"/tabs/{tab}/snapshot", params={"userId": user, "format": "text"})
    return out.get("text") or out.get("snapshot") or json.dumps(out)


def click_ref(base, user, tab, ref):
    return request(base, "POST", f"/tabs/{tab}/click", body={"userId": user, "ref": ref})


def type_ref(base, user, tab, ref, text):
    return request(base, "POST", f"/tabs/{tab}/type", body={"userId": user, "ref": ref, "text": text, "mode": "fill", "delay": 20})


def evaluate(base, user, tab, expression):
    out = request(base, "POST", f"/tabs/{tab}/evaluate", body={"userId": user, "expression": expression}, timeout=120)
    return out.get("result")


def downloads(base, user, tab, include_data=False, consume=False):
    return request(
        base,
        "GET",
        f"/tabs/{tab}/downloads",
        params={
            "userId": user,
            "includeData": "true" if include_data else "false",
            "consume": "true" if consume else "false",
        },
        timeout=120,
    )


def find_ref(snapshot, label):
    pattern = re.compile(rf'button "{re.escape(label)}" \[(e\d+)\]')
    match = pattern.search(snapshot)
    return match.group(1) if match else None


def find_textbox_ref(snapshot):
    match = re.search(r'textbox "Chat with ChatGPT" \[(e\d+)\]', snapshot)
    return match.group(1) if match else None


def ensure_image_mode(base, user, tab):
    snap = snapshot_text(base, user, tab)
    if "Describe or edit an image" in snap:
        return snap
    create_ref = find_ref(snap, "Create an image")
    if not create_ref:
        raise RuntimeError("Could not find 'Create an image' button")
    click_ref(base, user, tab, create_ref)
    time.sleep(1.5)
    snap = snapshot_text(base, user, tab)
    if "Describe or edit an image" not in snap:
        raise RuntimeError("Image mode did not activate")
    return snap


def submit_prompt(base, user, tab, prompt):
    snap = ensure_image_mode(base, user, tab)
    textbox_ref = find_textbox_ref(snap)
    if not textbox_ref:
        raise RuntimeError("Could not find ChatGPT textbox")
    type_ref(base, user, tab, textbox_ref, prompt)
    time.sleep(0.7)
    result = evaluate(
        base,
        user,
        tab,
        '(() => { const b=[...document.querySelectorAll("button")].find(x => /send prompt/i.test(x.getAttribute("aria-label")||x.textContent||"")); if (!b) return {ok:false}; b.click(); return {ok:true}; })()'
    )
    if not result or not result.get("ok"):
        raise RuntimeError("Could not click send prompt")


def wait_for_image(base, user, tab, timeout_s=180, poll_s=5):
    deadline = time.time() + timeout_s
    last_snapshot = ""
    while time.time() < deadline:
        snap = snapshot_text(base, user, tab)
        last_snapshot = snap
        if "Generated image:" in snap:
            return snap
        time.sleep(poll_s)
    raise RuntimeError("Timed out waiting for generated image\n\nLast snapshot:\n" + last_snapshot[:2000])


def trigger_download_from_page(base, user, tab):
    result = evaluate(
        base,
        user,
        tab,
        '(async () => { const img=[...document.images].find(i => /Generated image:/i.test(i.alt||"")); if (!img) return {ok:false, why:"no image"}; const resp = await fetch(img.currentSrc, {credentials:"include"}); if (!resp.ok) return {ok:false, status:resp.status}; const blob = await resp.blob(); const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = "chatgpt-image.png"; document.body.appendChild(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 1000); return {ok:true, size: blob.size, type: blob.type, alt: img.alt}; })()'
    )
    if not result or not result.get("ok"):
        raise RuntimeError(f"Could not trigger image download: {result}")
    return result


def save_first_download(base, user, tab, output_path):
    for _ in range(20):
        out = downloads(base, user, tab, include_data=True, consume=True)
        items = out.get("downloads") or []
        if items:
            item = items[0]
            data = item.get("dataBase64")
            if not data:
                raise RuntimeError(f"Download captured but no inline data returned: {item}")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(base64.b64decode(data))
            return {
                "outputPath": output_path,
                "suggestedFilename": item.get("suggestedFilename"),
                "mimeType": item.get("mimeType"),
                "bytes": item.get("bytes"),
            }
        time.sleep(1)
    raise RuntimeError("No download captured from generated image")


def default_output_path():
    ts = datetime.now(UTC).strftime("%Y%m%d-%H%M%S")
    return os.path.join(os.path.dirname(__file__), "..", "generated", f"chatgpt-image-{ts}.png")


def main():
    ap = argparse.ArgumentParser(description="Generate and download a ChatGPT image through the remote Camoufox browser")
    ap.add_argument("prompt", help="Prompt to send to ChatGPT image generation")
    ap.add_argument("--base", default=DEFAULT_BASE)
    ap.add_argument("--user", default="lotfi")
    ap.add_argument("--session", default="chatgpt-image-helper")
    ap.add_argument("--output", default=None)
    ap.add_argument("--timeout", type=int, default=180)
    args = ap.parse_args()

    output = os.path.abspath(args.output or default_output_path())
    try:
        tab = open_tab(args.base, args.user, args.session, CHATGPT_URL)
        wait_tab(args.base, args.user, tab, 12000)
        submit_prompt(args.base, args.user, tab, args.prompt)
        wait_for_image(args.base, args.user, tab, timeout_s=args.timeout)
        dl_meta = trigger_download_from_page(args.base, args.user, tab)
        saved = save_first_download(args.base, args.user, tab, output)
        print(json.dumps({
            "ok": True,
            "tabId": tab,
            "prompt": args.prompt,
            "image": dl_meta,
            "saved": saved,
        }, indent=2))
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
