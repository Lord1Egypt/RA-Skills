#!/usr/bin/env python3
"""
audit_cc_date_prompt.py
Check the installed Claude Code binary for Unicode steganography in the
system-prompt date line (the "Today's date is" injection).

Background:
  Claude Code v2.1.193-v2.1.196 embedded a covert channel: when the system
  timezone was Asia/Shanghai or Asia/Urumqi (and/or the proxy/API base URL
  matched a list of Chinese relay/AI-lab domains), it replaced the apostrophe
  in "Today's date is" with a near-invisible Unicode variant
  (U+2019 / U+02BC / U+02B9) and swapped the date separator "-" -> "/".
  This let the server silently flag Chinese/proxy users. Anthropic later
  rolled it back (clean from v2.1.197+).

Usage:
  python3 audit_cc_date_prompt.py [--json]
Exit codes: 0 = clean, 2 = affected/suspect, 1 = error.
"""
import os, re, shutil, subprocess, sys, json

KNOWN_AFFECTED = [(2,1,193),(2,1,194),(2,1,195),(2,1,196)]
KNOWN_CLEAN_MIN = (2,1,197)

MARKER_CP = {
    "U+2019 RIGHT SINGLE QUOTATION MARK": 0x2019,
    "U+02BC MODIFIER LETTER APOSTROPHE": 0x02BC,
    "U+02B9 MODIFIER LETTER PRIME": 0x02B9,
}
LAB_KEYWORDS = [b"moonshot",b"zhipu",b"deepseek",b"minimax",b"dashscope",
                b"volces",b"stepfun",b"baichuan",b"01ai",b"bigmodel",b"xaminim"]

def find_binary():
    claude = shutil.which("claude")
    if not claude:
        return None
    path = os.path.realpath(claude)
    if os.path.exists(path) and os.path.getsize(path) > 1_000_000:
        return path
    try:
        root = subprocess.check_output(["npm","root","-g"], text=True).strip()
        p = os.path.join(root,"@anthropic-ai","claude-code","bin","claude.exe")
        if os.path.exists(p):
            return p
    except Exception:
        pass
    return path if os.path.exists(path) else None

def get_version():
    try:
        out = subprocess.check_output(["claude","--version"], text=True, stderr=subprocess.STDOUT)
        m = re.search(r"(\d+)\.(\d+)\.(\d+)", out)
        if m:
            return tuple(int(x) for x in m.groups())
    except Exception:
        pass
    return None

def audit(binpath):
    data = open(binpath,"rb").read()
    res = {}
    res["timezone_cn"] = (b"Asia/Shanghai" in data) and (b"Asia/Urumqi" in data)
    res["date_var_template"] = bool(re.search(rb"Today\$\{[^}]*\}s date is", data))
    res["xor_decode"] = (b"fromCharCode(r^91)" in data) or (b"r^91" in data) or (b"Kup=91" in data)
    res["proxy_domain_match"] = (b'endsWith("."+r)' in data) or (b"some((r)=>e===r" in data)
    res["lab_keywords"] = [k.decode() for k in LAB_KEYWORDS if k in data]
    res["marker_cp_counts"] = {name: data.count(c.to_bytes((c.bit_length()+7)//8,"big")) for name,c in MARKER_CP.items()}
    return res

def verdict(res):
    stego = res["date_var_template"] and (res["timezone_cn"] or res["lab_keywords"] or res["xor_decode"] or res["proxy_domain_match"])
    if stego:
        return "AFFECTED"
    if any([res["timezone_cn"], res["date_var_template"], res["xor_decode"], res["lab_keywords"], res["proxy_domain_match"]]):
        return "SUSPECT"
    return "CLEAN"

def main():
    ap = find_binary()
    if not ap:
        print("ERROR: claude binary not found", file=sys.stderr); sys.exit(1)
    ver = get_version()
    res = audit(ap)
    v = verdict(res)
    out = {"binary": ap, "version": ".".join(map(str,ver)) if ver else None,
           "verdict": v, "checks": res,
           "known_affected_range": "2.1.193-2.1.196", "known_clean_min": "2.1.197"}
    if "--json" in sys.argv:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(f"Claude Code binary : {ap}")
        print(f"Version            : {out['version']}")
        print(f"Known clean from   : {out['known_clean_min']} (affected range {out['known_affected_range']})")
        print("-"*50)
        print(f"  timezone CN check (Asia/Shanghai+Urumqi): {res['timezone_cn']}")
        print(f"  variable date template (Today${{..}}s date is): {res['date_var_template']}")
        print(f"  XOR domain-list decode (Kup=91 / r^91)   : {res['xor_decode']}")
        print(f"  proxy domain matching (endsWith)         : {res['proxy_domain_match']}")
        print(f"  AI-lab keywords found                    : {res['lab_keywords'] or 'none'}")
        print(f"  marker codepoint counts                  : {res['marker_cp_counts']}")
        print("-"*50)
        print(f"VERDICT: {v}")
        if v == "AFFECTED":
            print(">> This build contains Unicode steganography in the date line.")
            print(">> Remediation: upgrade to >= 2.1.197 (e.g. `npm install -g @anthropic-ai/claude-code@latest`) and re-audit.")
        elif v == "SUSPECT":
            print(">> Some suspicious strings present but not the full covert channel. Inspect manually / upgrade to be safe.")
    sys.exit(0 if v == "CLEAN" else 2)

if __name__ == "__main__":
    main()
