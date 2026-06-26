#!/usr/bin/env python3
"""
analyze_profile.py — A partir del profile.json y del config.json, calcula:
  - Seniority estimado (junior/mid/senior/staff/principal)
  - Banda salarial sugerida por mercado
  - Gaps prioritarios para subir banda
  - Empresas target sugeridas (cruzando stack + seniority)

Uso:
    python3 analyze_profile.py path/to/profile.json --config path/to/config.json
    python3 analyze_profile.py profile.json --config config.json --out analysis.json
"""

import argparse
import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


SENIORITY_BAND_USD = {
    "junior": {
        "latam_remote": (1500, 3000),
        "us_remote": (5000, 7000),
        "eu_remote": (3300, 4900),
        "global_usd": (3000, 5000),
    },
    "mid": {
        "latam_remote": (3000, 5500),
        "us_remote": (7000, 11000),
        "eu_remote": (4900, 7700),
        "global_usd": (5000, 8000),
    },
    "senior": {
        "latam_remote": (5000, 9000),
        "us_remote": (11000, 16000),
        "eu_remote": (7700, 11000),
        "global_usd": (8000, 13000),
    },
    "staff": {
        "latam_remote": (8000, 14000),
        "us_remote": (16000, 24000),
        "eu_remote": (11000, 15400),
        "global_usd": (13000, 20000),
    },
    "principal": {
        "latam_remote": (12000, 22000),
        "us_remote": (22000, 35000),
        "eu_remote": (15400, 22000),
        "global_usd": (20000, 32000),
    },
}


SCOPE_KEYWORDS_HIGH = [
    "led", "architected", "designed", "built from scratch", "founded",
    "scaled", "owned", "drove", "spearheaded", "delivered",
    "lideré", "diseñé", "arquitecté", "construí", "escalé",
]
SCOPE_KEYWORDS_MID = [
    "implemented", "developed", "built", "shipped", "launched",
    "implementé", "desarrollé", "construí",
]
SCOPE_KEYWORDS_LOW = [
    "learned", "assisted", "supported", "helped",
    "aprendí", "asistí", "ayudé", "soporté",
]

IMPACT_METRIC_RE = re.compile(
    r"(\d+(?:[.,]\d+)?)\s*(%|x|×|ms|s\b|min|hour|hr|day|users|usuarios|"
    r"requests|rps|qps|gb|tb|k\b|million|m\b|billion|b\b|\$|usd|€|eur)",
    re.IGNORECASE,
)


def estimate_seniority(profile: dict) -> tuple[str, float, dict]:
    """Devuelve (label, confidence_0_1, breakdown_dict)."""
    years = float(profile.get("estimated_years_experience", 0) or 0)
    titles = " ".join(profile.get("detected_titles", [])).lower()
    text = " ".join(profile.get("sections", {}).values()).lower()
    preamble = profile.get("preamble", "").lower()
    full = preamble + " " + text

    # Score por años (peso 30%)
    if years < 2:
        years_score, years_label = 0.1, "junior"
    elif years < 5:
        years_score, years_label = 0.35, "mid"
    elif years < 8:
        years_score, years_label = 0.6, "senior"
    elif years < 12:
        years_score, years_label = 0.8, "staff"
    else:
        years_score, years_label = 0.95, "principal"

    # Score por título declarado (peso 25%)
    if "principal" in titles:
        title_score, title_label = 0.95, "principal"
    elif "staff" in titles or "head of" in titles:
        title_score, title_label = 0.8, "staff"
    elif any(w in titles for w in ("senior", "sr.", "lead", "tech lead")):
        title_score, title_label = 0.6, "senior"
    elif any(w in titles for w in ("junior", "jr.", "intern", "trainee")):
        title_score, title_label = 0.1, "junior"
    elif titles:
        title_score, title_label = 0.35, "mid"
    else:
        title_score, title_label = 0.3, "mid"

    # Score por scope keywords (peso 25%) — usar word boundaries para evitar
    # falsos positivos del estilo "led" → "sca**led**"
    def count_kws(text_blob: str, kws: list[str]) -> int:
        return sum(
            len(re.findall(r"\b" + re.escape(k) + r"\b", text_blob))
            for k in kws
        )

    high_hits = count_kws(full, SCOPE_KEYWORDS_HIGH)
    mid_hits = count_kws(full, SCOPE_KEYWORDS_MID)
    low_hits = count_kws(full, SCOPE_KEYWORDS_LOW)
    if high_hits >= 3 and high_hits >= mid_hits:
        scope_score, scope_label = 0.85, "staff"
    elif high_hits >= 1:
        scope_score, scope_label = 0.65, "senior"
    elif mid_hits >= 3 and low_hits == 0:
        scope_score, scope_label = 0.45, "mid"
    elif low_hits > mid_hits:
        scope_score, scope_label = 0.15, "junior"
    else:
        scope_score, scope_label = 0.4, "mid"

    # Score por métricas de impacto (peso 20%)
    impact_count = len(IMPACT_METRIC_RE.findall(full))
    if impact_count >= 8:
        impact_score, impact_label = 0.9, "staff"
    elif impact_count >= 4:
        impact_score, impact_label = 0.65, "senior"
    elif impact_count >= 1:
        impact_score, impact_label = 0.4, "mid"
    else:
        impact_score, impact_label = 0.15, "junior"

    weighted = (
        years_score * 0.30
        + title_score * 0.25
        + scope_score * 0.25
        + impact_score * 0.20
    )

    if weighted < 0.25:
        final = "junior"
    elif weighted < 0.45:
        final = "mid"
    elif weighted < 0.7:
        final = "senior"
    elif weighted < 0.85:
        final = "staff"
    else:
        final = "principal"

    return final, round(weighted, 2), {
        "years": {"value": years, "score": years_score, "label": years_label},
        "titles": {"value": titles[:120] or "(none)", "score": title_score, "label": title_label},
        "scope_keywords": {
            "high_hits": high_hits, "mid_hits": mid_hits, "low_hits": low_hits,
            "score": scope_score, "label": scope_label,
        },
        "impact_metrics": {"count": impact_count, "score": impact_score, "label": impact_label},
    }


def estimate_modifiers(profile: dict, config: dict) -> dict:
    text = " ".join(profile.get("sections", {}).values()).lower()
    text += " " + profile.get("preamble", "").lower()

    tier_s_companies = [
        "stripe", "shopify", "gitlab", "hashicorp", "cloudflare", "datadog",
        "snowflake", "atlassian", "google", "meta", "facebook", "amazon",
        "apple", "microsoft", "netflix", "uber", "airbnb",
    ]
    tier_s_hit = any(
        re.search(r"\b" + re.escape(c) + r"\b", text) for c in tier_s_companies
    )

    has_oss = any(k in text for k in ["github.com/", "open source", "oss contribution", "contributor"])
    has_talks = any(
        re.search(r"\b" + re.escape(k) + r"\b", text)
        for k in ["speaker at", "keynote", "conference talk", "pycon", "kubecon", "rustconf"]
    )

    languages = profile.get("languages", {})
    english = languages.get("english", "unspecified")
    has_english_high = english in ("native", "c2", "c1")

    legacy_only = bool(re.search(r"\b(cobol|delphi|jsp|vb6|powerbuilder)\b", text)) and not re.search(
        r"\b(python|go|rust|typescript|kotlin|swift)\b", text
    )

    return {
        "tier_s_recent_employer": tier_s_hit,
        "has_oss_contributions": has_oss,
        "has_public_talks": has_talks,
        "english_high_proficiency": has_english_high,
        "english_level_detected": english,
        "stack_legacy_only": legacy_only,
    }


def apply_modifiers(band: tuple, modifiers: dict) -> tuple:
    low, high = band
    factor = 1.0
    if modifiers.get("tier_s_recent_employer"):
        factor *= 1.20
    if modifiers.get("has_oss_contributions"):
        factor *= 1.10
    if modifiers.get("has_public_talks"):
        factor *= 1.07
    if modifiers.get("stack_legacy_only"):
        factor *= 0.85
    if not modifiers.get("english_high_proficiency"):
        factor *= 0.85
    return int(low * factor), int(high * factor)


def derive_bands(seniority: str, modifiers: dict) -> dict:
    base = SENIORITY_BAND_USD.get(seniority, SENIORITY_BAND_USD["mid"])
    return {market: apply_modifiers(rng, modifiers) for market, rng in base.items()}


def identify_gaps(profile: dict, seniority: str, modifiers: dict) -> list:
    gaps = []
    text_blob = " ".join(profile.get("sections", {}).values()).lower()
    impact_count = len(IMPACT_METRIC_RE.findall(text_blob))
    if impact_count < 4:
        gaps.append({
            "gap": "métricas_de_impacto",
            "evidence": f"solo {impact_count} bullets con métricas cuantificables",
            "fix": "Reescribir 3-5 bullets de los roles más recientes en formato 'reduje/aumenté/mejoré X% / $Y / Nms'. Sin números, el CV se lee como mid aunque seas senior.",
            "effort": "low",
            "expected_uplift_band": "+30-50% dentro de la misma banda de seniority",
            "priority": 1,
        })
    if not modifiers.get("english_high_proficiency"):
        gaps.append({
            "gap": "inglés_certificable",
            "evidence": f"nivel detectado: {modifiers.get('english_level_detected')}",
            "fix": "Tomar Cambridge C1/C2 o EF SET, agregar score al CV. Practicar 30 min/día con un tutor real (italki, preply). Sin C1+, el mercado USD baja ~2x el techo.",
            "effort": "medium",
            "expected_uplift_band": "abre mercado us_remote y eu_remote (+50-100% sobre LATAM)",
            "priority": 2,
        })
    if not modifiers.get("has_oss_contributions") and seniority in ("senior", "staff", "principal"):
        gaps.append({
            "gap": "oss_publico",
            "evidence": "sin contribuciones públicas detectadas",
            "fix": "Contribuir a 1-2 proyectos OSS relevantes a tu stack (no docs/typo fixes — features mergeadas). Linkear el GitHub en el CV. Para staff+ es casi requisito.",
            "effort": "high",
            "expected_uplift_band": "+10-15% en negociación, mejor pase de filtros tech-heavy",
            "priority": 3,
        })
    if seniority in ("mid", "senior") and not re.search(r"\b(led|lideré|mentor|mentor[eé]|hiring)\b", text_blob):
        gaps.append({
            "gap": "leadership_demostrable",
            "evidence": "no se detectó leadership/mentoría/hiring en bullets",
            "fix": "Agregar bullets concretos: 'mentoreé N juniors', 'lideré N initiatives cross-team', 'participé en hiring loop de N candidatos'. Sin esto, hay un techo en senior.",
            "effort": "low",
            "expected_uplift_band": "habilita pase a staff (+30-50%)",
            "priority": 2,
        })
    if modifiers.get("stack_legacy_only"):
        gaps.append({
            "gap": "stack_modernizado",
            "evidence": "stack dominante legacy (Cobol/Delphi/JSP/VB6)",
            "fix": "Side project con stack moderno (Python/Go/TS + cloud) durante 3-6 meses. Side project público > certificación.",
            "effort": "high",
            "expected_uplift_band": "abre 5-10x más empresas",
            "priority": 1,
        })
    if not profile.get("skills", {}).get("cloud_devops"):
        gaps.append({
            "gap": "cloud_certificacion",
            "evidence": "sin keywords de AWS/GCP/Azure/Kubernetes",
            "fix": "AWS Solutions Architect Associate o GCP Cloud Engineer. ~40h estudio, ~$150 examen. Aceleran filtros automáticos.",
            "effort": "low",
            "expected_uplift_band": "+5-10% banda, +50% pase de filtros",
            "priority": 4,
        })
    gaps.sort(key=lambda g: g["priority"])
    return gaps


def suggest_target_companies(profile: dict, seniority: str, config: dict) -> list:
    """Cruza stack del CV con la lista de empresas configuradas y por tier."""
    skills = profile.get("skills", {})
    stack_flat = set()
    for v in skills.values():
        stack_flat.update(s.lower() for s in v)

    configured = config.get("platforms", {}).get("company_pages", {}).get("companies", [])

    # Heurística simple: para cada empresa configurada, devolverla con un fit_note
    # basado en si su stack conocido (hardcoded abajo) cruza con el del CV.
    company_stacks = {
        "stripe": {"ruby", "go", "scala", "typescript"},
        "shopify": {"ruby", "rails", "react", "graphql"},
        "gitlab": {"ruby", "go", "vue"},
        "hashicorp": {"go", "terraform", "kubernetes"},
        "vercel": {"typescript", "nextjs", "next.js", "react", "rust"},
        "supabase": {"typescript", "postgres", "go", "elixir"},
        "cloudflare": {"go", "rust", "typescript"},
        "datadog": {"python", "go", "scala"},
        "mercadolibre": {"java", "scala", "kotlin", "react"},
        "globant": {"java", "python", "react", "node.js"},
        "rappi": {"kotlin", "swift", "python", "go"},
        "nubank": {"clojure", "scala", "kotlin"},
        "modo": {"node.js", "react", "kotlin", "swift"},
    }

    suggestions = []
    for company in configured:
        key = company.lower()
        known_stack = company_stacks.get(key, set())
        overlap = sorted(known_stack & stack_flat)
        suggestions.append({
            "company": company,
            "stack_overlap": overlap,
            "fit": "high" if len(overlap) >= 2 else ("medium" if overlap else "explore"),
            "career_page_search": f"site:greenhouse.io {company} OR site:lever.co {company}",
        })

    high = [s for s in suggestions if s["fit"] == "high"]
    medium = [s for s in suggestions if s["fit"] == "medium"]
    explore = [s for s in suggestions if s["fit"] == "explore"]
    return high + medium + explore[:5]


def stack_assessment(profile: dict) -> dict:
    skills = profile.get("skills", {})
    counts = {cat: len(v) for cat, v in skills.items()}
    if not counts:
        return {"dominant_category": None, "secondary_category": None, "breadth": "unknown"}
    sorted_cats = sorted(counts.items(), key=lambda kv: -kv[1])
    dominant = sorted_cats[0][0] if sorted_cats else None
    secondary = sorted_cats[1][0] if len(sorted_cats) > 1 else None
    total = sum(counts.values())
    breadth = "wide" if total >= 15 else ("medium" if total >= 8 else "narrow")
    return {"dominant_category": dominant, "secondary_category": secondary, "breadth": breadth, "by_category": counts}


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze parsed profile against config")
    parser.add_argument("profile_path", type=Path)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--out", type=Path, help="Si se omite, imprime a stdout")
    args = parser.parse_args()

    if not args.profile_path.exists():
        sys.exit(f"No existe profile: {args.profile_path}")
    if not args.config.exists():
        sys.exit(f"No existe config: {args.config}")

    profile = json.loads(args.profile_path.read_text(encoding="utf-8"))
    config = json.loads(args.config.read_text(encoding="utf-8"))

    seniority, confidence, breakdown = estimate_seniority(profile)
    modifiers = estimate_modifiers(profile, config)
    bands = derive_bands(seniority, modifiers)
    gaps = identify_gaps(profile, seniority, modifiers)
    targets = suggest_target_companies(profile, seniority, config)
    stack = stack_assessment(profile)

    target_salary = config.get("candidate", {}).get("salary", {}).get("target_monthly")
    aspiration_check = None
    if target_salary:
        market_pref = (config.get("markets") or ["global_usd"])[0]
        market_band = bands.get(market_pref, bands.get("global_usd"))
        if market_band:
            low, high = market_band
            if target_salary < low:
                aspiration_check = {
                    "status": "below_market",
                    "message": f"Tu target ({target_salary} USD) está por debajo de la banda detectada ({low}-{high}). Podés pedir más.",
                }
            elif target_salary <= high:
                aspiration_check = {
                    "status": "aligned",
                    "message": f"Tu target ({target_salary} USD) cae dentro de la banda detectada ({low}-{high}). Realista.",
                }
            else:
                aspiration_check = {
                    "status": "above_band",
                    "message": (
                        f"Tu target ({target_salary} USD) está por encima de la banda detectada ({low}-{high}). "
                        f"Cerrá los gaps marcados como priority 1-2 antes de fijar piso ahí."
                    ),
                }

    analysis = {
        "seniority": {"label": seniority, "confidence": confidence, "breakdown": breakdown},
        "stack": stack,
        "modifiers_applied": modifiers,
        "salary_bands_usd_monthly": {
            market: {"low": low, "high": high}
            for market, (low, high) in bands.items()
        },
        "aspiration_check": aspiration_check,
        "gaps_to_close": gaps,
        "target_companies": targets,
    }

    payload = json.dumps(analysis, indent=2, ensure_ascii=False)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload, encoding="utf-8")
        print(f"OK — análisis escrito en {args.out}")
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
