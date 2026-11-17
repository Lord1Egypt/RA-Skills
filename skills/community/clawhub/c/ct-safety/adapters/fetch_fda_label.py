#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fetch_fda_label.py / FDA 药品标签检索（第三证据源 for #4 多源三角验证）

经 openFDA 公开 REST API (https://api.fda.gov/drug/label.json) 检索药品的官方
标签（说明书），提取 adverse_reactions / warnings 章节，判断某不良事件
(MedDRA PT) 是否已收录于标签（labeled vs unlabeled）。

这是 pharmacovigilance 的关键区分：
  - labeled   = 标签已收录该风险 -> 已知/预期风险 (Known / labeled)
  - unlabeled = 标签未收录该风险 -> 新信号/未预期 (New / Unexpected)，更值得关注

无需 API key（低频可用，限流）；可选 --api-key 提升配额。
仅读公开数据，零保密数据或信息输入。与 FAERS 同属 openFDA，网络层风格对齐
fetch_faers.py（瞬时错误重试、超时一致）。
"""
import argparse
import base64
import json
import os
import sys
import time

try:
    import requests
except ImportError:
    requests = None

BASE = "https://api.fda.gov/drug/label.json"
_RETRY_STATUSES = {404, 429, 500, 502, 503, 504}

# Skill root (parent of the scripts/ dir). Used to locate a local .env that
# holds the openFDA key WITHOUT shipping it inside the published package.
_SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DOTENV = os.path.join(_SKILL_ROOT, ".env")

# OpenFDA key obfuscation (ct-base §5, private-credential best practice).
# A skill-root .env may store either a plaintext key OR an `obf:`-prefixed
# XOR+base64 obfuscated blob. `resolve_api_key` auto-detects the prefix and
# decodes the latter; plaintext values pass through unchanged. Obfuscation is
# NOT real encryption — it only prevents the plaintext key from being caught by
# naive scanners or accidentally copied when a .env is moved around.
_OBF_KEY = b"ct-safety-openfda-obf-v1-8c2f"


def _deobfuscate(val):
    """Decode an `obf:`-prefixed XOR+base64 blob; return *val* unchanged otherwise."""
    if not val or not val.startswith("obf:"):
        return val
    try:
        raw = base64.b64decode(val[len("obf:"):].strip())
        dec = bytes(c ^ _OBF_KEY[i % len(_OBF_KEY)] for i, c in enumerate(raw))
        return dec.decode("utf-8")
    except Exception:
        return val


def resolve_api_key(cli_key, dotenv_path=None):
    """Resolve an openFDA API key. Priority (highest first):

    1. CLI ``--api-key`` (explicit, always wins)
    2. Environment variable ``OPENFDA_API_KEY``
    3. A ``.env`` file at the skill root (``OPENFDA_API_KEY=...``)

    Returns ``None`` when no key is available — keyless anonymous access still
    works. A skill-root ``.env`` is git-ignored (and listed in ``.clawhubignore``),
    so a user's key never leaks into a packaged skill.
    """
    if cli_key:
        return cli_key
    env = os.environ.get("OPENFDA_API_KEY")
    if env:
        return env
    if dotenv_path is None:
        dotenv_path = _DOTENV
    if dotenv_path and os.path.isfile(dotenv_path):
        try:
            with open(dotenv_path, "r", encoding="utf-8") as fh:
                for line in fh:
                    s = line.strip()
                    if not s or s.startswith("#"):
                        continue
                    if s.startswith("OPENFDA_API_KEY="):
                        val = s.split("=", 1)[1].strip().strip('"').strip("'")
                        if val:
                            return _deobfuscate(val)
        except Exception:
            pass
    return None


def _q(search, limit=5, api_key=None):
    params = {"search": search, "limit": limit}
    api_key = resolve_api_key(api_key, _DOTENV)
    if api_key:
        params["api_key"] = api_key
    return params


def _get_json(params, api_key=None, retries=3, delay=1.5, timeout=120):
    """requests.get against BASE with transient-error retry. Mirrors
    fetch_faers._get_json (same retry policy / generous timeout)."""
    api_key = resolve_api_key(api_key, _DOTENV)
    if api_key:
        params = dict(params)
        params["api_key"] = api_key
    last = None
    for attempt in range(1, retries + 1):
        r = requests.get(BASE, params=params, timeout=timeout)
        if r.status_code == 200:
            return r.json()
        last = r
        if r.status_code not in _RETRY_STATUSES or attempt == retries:
            r.raise_for_status()
        time.sleep(delay * attempt)
    last.raise_for_status()


# 常见 PV 事件同义词（best-effort，用于标签文本子串匹配）。
# 仅覆盖高频安全性信号；未列出的事件退化为事件名本身的子串匹配。
EVENT_SYNONYMS = {
    "PNEUMONITIS": ["pneumonitis", "interstitial lung disease", "ild",
                    "pulmonary fibrosis", "drug-induced lung"],
    "HEPATOTOXICITY": ["hepatotoxicity", "liver injury", "hepatic injury",
                       "hepatitis", "transaminase"],
    "MYOCARDITIS": ["myocarditis", "cardiac inflammation"],
    "QT PROLONGATION": ["qt prolongation", "qt interval", "long qt"],
    "STEVENS-JOHNSON SYNDROME": ["stevens-johnson", "toxic epidermal"],
    "RASH": ["rash", "dermatitis", "exanthem"],
    "DIARRHEA": ["diarrhea", "loose stool"],
    "NAUSEA": ["nausea", "vomiting"],
    "NEUTROPENIA": ["neutropenia", "neutrophil count"],
    "THROMBOCYTOPENIA": ["thrombocytopenia", "platelet count"],
    "PERIPHERAL NEUROPATHY": ["peripheral neuropathy", "neuropathy"],
    "ANAPHYLAXIS": ["anaphylaxis", "anaphylactic"],
}


def _synonyms(event):
    """Return a de-duplicated list of lowercase match strings for `event`."""
    u = (event or "").upper().strip()
    syns = [(event or "").lower(), u.lower()]
    if u in EVENT_SYNONYMS:
        syns += EVENT_SYNONYMS[u]
    for tok in (event or "").replace("-", " ").split():
        tok = tok.lower().strip()
        if tok:
            syns.append(tok)
    out = []
    for s in syns:
        s = s.strip()
        if s and s not in out:
            out.append(s)
    return out


def fetch_label(drug, api_key=None, run=False, out=None, limit=5,
                timeout=120, retries=3):
    """Fetch FDA label sections (adverse_reactions + warnings) for `drug`.

    Search order: substance_name -> brand_name -> generic_name -> free-text;
    first that yields results wins. PREVIEW (run=False) prints and returns None.
    """
    if requests is None:
        raise RuntimeError("requests not installed: pip install requests")
    if not run:
        print("[PREVIEW] would query openFDA drug/label.json for drug=%r "
              "(use --run to execute)" % drug)
        return None

    searches = [
        'openfda.substance_name:"%s"' % drug,
        'openfda.brand_name:"%s"' % drug,
        'openfda.generic_name:"%s"' % drug,
        '"%s"' % drug,
    ]
    adverse = []
    warnings = []
    matched_terms = []
    n_results = 0
    for s in searches:
        try:
            j = _get_json(_q(s, limit=limit, api_key=api_key),
                          api_key=api_key, timeout=timeout, retries=retries)
            results = j.get("results", [])
            if not results:
                continue
            n_results = len(results)
            for r in results:
                ofda = r.get("openfda", {})
                for k in ("substance_name", "brand_name", "generic_name"):
                    for v in (ofda.get(k) or []):
                        if v and v not in matched_terms:
                            matched_terms.append(v)
                for sec in ("adverse_reactions", "warnings"):
                    for blk in (r.get(sec) or []):
                        if sec == "adverse_reactions":
                            adverse.append(blk)
                        else:
                            warnings.append(blk)
            break  # first search that yields results wins
        except Exception as e:  # noqa: BLE001 - try next search strategy
            print("[WARN] label search %r failed: %s" % (s, e))
            continue

    result = {
        "source": "FDA Label (openFDA drug/label.json)",
        "query": drug,
        "matched_drug_terms": matched_terms[:10],
        "n_results": n_results,
        "adverse_reactions": adverse,
        "warnings": warnings,
    }
    if out:
        with open(out, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print("[OK] wrote", out, "(n_results=%d)" % n_results)
    return result


def check_event(label_data, event):
    """Return {status, matched_terms, note} for whether `event` is present in the
    label's adverse_reactions / warnings text.

      - labeled   : at least one synonym found in label text
      - unlabeled : label retrieved (n_results>0) but event not found
      - unknown   : no label data / n_results==0 / no text

    Pure (no network); safe to unit-test with a constructed label_data dict.
    """
    if not label_data or label_data.get("n_results", 0) == 0:
        return {"status": "unknown", "matched_terms": [],
                "note": "无标签数据（未检索或零结果）"}
    text = " ".join(
        (label_data.get("adverse_reactions") or [])
        + (label_data.get("warnings") or [])
    ).lower()
    if not text.strip():
        return {"status": "unknown", "matched_terms": [],
                "note": "标签无 adverse_reactions/warnings 文本"}
    syns = _synonyms(event)
    hit = [s for s in syns if s and s in text]
    if hit:
        return {"status": "labeled", "matched_terms": hit[:5],
                "note": "标签已收录该风险（已知/预期）"}
    return {"status": "unlabeled", "matched_terms": [],
            "note": "标签未收录该风险（新信号/未预期，更值得关注）"}


def main():
    ap = argparse.ArgumentParser(description="Fetch FDA label (openFDA) for a drug.")
    ap.add_argument("--drug", required=True)
    ap.add_argument("--api-key", help="openFDA API key (raises quota to 120k/day). "
                                        "Also read from env OPENFDA_API_KEY or skill-root .env (git-ignored). "
                                        "Optional: keyless anonymous quota works for low-volume use.")
    ap.add_argument("--limit", type=int, default=5)
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--out")
    args = ap.parse_args()
    res = fetch_label(args.drug, args.api_key, args.run, args.out, args.limit)
    if res and not args.out:
        print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
