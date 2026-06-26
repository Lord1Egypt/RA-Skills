#!/usr/bin/env python3
"""
match_jobs.py — Scorea una oferta laboral contra el perfil del usuario.

Toma un job posting (JSON con título, empresa, descripción, salario, etc.)
y devuelve un score 0-100 + flags + rationale.

Uso:
    python3 match_jobs.py --profile profile.json --config config.json --job-file job.json
    cat job.json | python3 match_jobs.py --profile profile.json --config config.json --stdin

Seguridad: el JSON de oferta proviene de boards externos y es untrusted.
Por eso este CLI NO acepta JSON inline como argumento — un posting con
comillas/backticks/caracteres de control podría romper el quoting del shell
y derivar en ejecución de comandos no deseados. Usá --job-file o --stdin.

Schema esperado del job JSON (al menos estos campos):
    {
      "id": "...",
      "url": "...",
      "title": "Senior Backend Engineer",
      "company": "Acme",
      "location": "Remote",
      "remote": true,
      "description": "We are looking for...",
      "salary": {"currency": "USD", "min_monthly": null, "max_monthly": null},
      "tags": ["python", "kubernetes"],
      "posted_at": "2026-04-20"
    }
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# Forzar UTF-8 en stdout (Windows default cp1252 no soporta varios glyphs)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


SCORE_MAX = 100


def _flatten_skills(profile: dict) -> set:
    flat = set()
    for v in (profile.get("skills") or {}).values():
        flat.update(s.lower().strip() for s in v if s)
    return flat


def _job_text(job: dict) -> str:
    parts = [
        job.get("title", "") or "",
        job.get("description", "") or "",
        " ".join(job.get("tags", []) or []),
        job.get("location", "") or "",
        job.get("company", "") or "",
    ]
    return " ".join(parts).lower()


def score_stack_match(profile: dict, job: dict) -> tuple[int, list[str]]:
    """+0..40 según overlap de stack."""
    profile_skills = _flatten_skills(profile)
    if not profile_skills:
        return 0, ["no se detectó stack en el perfil"]
    text = _job_text(job)
    matched = []
    for skill in profile_skills:
        pattern = r"(?<![\w.])" + re.escape(skill) + r"(?![\w])"
        if re.search(pattern, text):
            matched.append(skill)
    if not matched:
        return 0, ["sin overlap de stack"]
    # Hasta 8 matches contribuyen máximo (40 puntos = 5 por match)
    pts = min(40, len(matched) * 5)
    return pts, [f"stack overlap: {', '.join(sorted(matched)[:10])}"]


def score_seniority_match(profile: dict, job: dict, analysis: dict | None) -> tuple[int, list[str], list[str]]:
    """+0..20 según match de seniority. Flags si hay mismatch fuerte."""
    notes = []
    flags = []
    title = (job.get("title") or "").lower()

    profile_seniority = None
    if analysis:
        profile_seniority = (analysis.get("seniority") or {}).get("label")
    if not profile_seniority:
        # fallback a años
        years = float(profile.get("estimated_years_experience", 0) or 0)
        if years < 2:
            profile_seniority = "junior"
        elif years < 5:
            profile_seniority = "mid"
        elif years < 8:
            profile_seniority = "senior"
        else:
            profile_seniority = "staff"

    job_seniority = "unknown"
    if "principal" in title:
        job_seniority = "principal"
    elif "staff" in title:
        job_seniority = "staff"
    elif any(w in title for w in ("senior", "sr.", "sr ", "lead", "tech lead", "architect")):
        job_seniority = "senior"
    elif any(w in title for w in ("junior", "jr.", "jr ", "intern")):
        job_seniority = "junior"
    elif any(w in title for w in ("engineer", "developer", "swe", "sde")):
        job_seniority = "mid"

    order = ["junior", "mid", "senior", "staff", "principal"]
    if job_seniority == "unknown":
        return 12, ["seniority del puesto no claro"], []

    p_idx = order.index(profile_seniority) if profile_seniority in order else 1
    j_idx = order.index(job_seniority)
    diff = j_idx - p_idx
    if diff == 0:
        pts, msg = 20, f"seniority match exacto ({profile_seniority})"
    elif diff == 1:
        pts, msg = 15, f"un nivel arriba ({profile_seniority} → {job_seniority}) — stretch razonable"
    elif diff == -1:
        pts, msg = 8, f"un nivel abajo ({profile_seniority} → {job_seniority}) — probablemente subpago"
        flags.append("below_seniority")
    elif diff >= 2:
        pts, msg = 3, f"dos niveles arriba ({profile_seniority} → {job_seniority}) — riesgo de rechazo en filtros"
        flags.append("seniority_stretch")
    else:
        pts, msg = 5, f"dos niveles abajo ({profile_seniority} → {job_seniority}) — sub-utilización"
        flags.append("below_seniority")
    notes.append(msg)
    return pts, notes, flags


def score_remote_fit(profile: dict, job: dict, config: dict) -> tuple[int, list[str], list[str]]:
    """+0..15 según fit de modalidad."""
    must_haves = [m.lower() for m in (config.get("candidate", {}).get("must_haves") or [])]
    deal_breakers = [d.lower() for d in (config.get("candidate", {}).get("deal_breakers") or [])]
    text = _job_text(job)
    flags = []

    is_remote = bool(job.get("remote")) or "remote" in (job.get("location") or "").lower() or "remote" in text
    on_site_only = "on-site mandatory" in text or "no remote" in text or "must be in office" in text

    pts, notes = 0, []
    if "remote" in must_haves:
        if is_remote and not on_site_only:
            pts = 15
            notes.append("modalidad remote — match")
        else:
            pts = 0
            flags.append("not_remote")
            notes.append("requiere remote y la oferta no lo es")
    else:
        pts = 10
        notes.append("usuario no exige remote")

    for db in deal_breakers:
        if db in text:
            flags.append("deal_breaker")
            notes.append(f"deal-breaker presente: '{db}'")
            pts = max(0, pts - 10)

    return pts, notes, flags


def score_salary(profile: dict, job: dict, config: dict) -> tuple[int, list[str], list[str]]:
    """+0..15 según alineación salarial. -30 si por debajo del mínimo del usuario."""
    salary = job.get("salary") or {}
    user_salary = (config.get("candidate") or {}).get("salary") or {}
    min_user = user_salary.get("min_monthly")
    target_user = user_salary.get("target_monthly")
    stretch_user = user_salary.get("stretch_monthly")

    notes, flags = [], []

    if not salary or salary.get("min_monthly") is None and salary.get("max_monthly") is None:
        notes.append("oferta no expone salario")
        flags.append("no_salary_disclosed")
        return 7, notes, flags

    job_min = salary.get("min_monthly") or salary.get("max_monthly")
    job_max = salary.get("max_monthly") or salary.get("min_monthly")

    if min_user and job_max and job_max < min_user:
        notes.append(f"techo de oferta ({job_max}) < mínimo del usuario ({min_user})")
        flags.append("below_minimum")
        return -30, notes, flags

    if stretch_user and job_min and job_min >= stretch_user:
        notes.append(f"piso de oferta ({job_min}) >= stretch del usuario ({stretch_user}) — verificá fit de seniority")
        flags.append("salary_above_stretch")
        return 15, notes, flags

    if target_user and job_max and job_max >= target_user:
        notes.append(f"techo ({job_max}) >= target ({target_user})")
        flags.append("salary_meets_target")
        return 15, notes, flags

    if target_user and job_min and job_min < target_user:
        notes.append(f"piso ({job_min}) < target ({target_user}) — negociable si llegás a ronda final")
        return 8, notes, flags

    return 10, ["salario en rango aceptable"], flags


def score_freshness(job: dict) -> tuple[int, list[str]]:
    """+0..10 según qué tan reciente es el posting."""
    posted = job.get("posted_at")
    if not posted:
        return 5, ["sin fecha de publicación"]
    try:
        if "T" in posted:
            dt = datetime.fromisoformat(posted.replace("Z", "+00:00"))
        else:
            dt = datetime.fromisoformat(posted)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
    except ValueError:
        return 5, [f"fecha no parseable: {posted}"]
    age_days = (datetime.now(timezone.utc) - dt).days
    if age_days <= 2:
        return 10, [f"posteado hace {age_days}d — caliente"]
    if age_days <= 7:
        return 8, [f"posteado hace {age_days}d — reciente"]
    if age_days <= 14:
        return 5, [f"posteado hace {age_days}d — todavía vigente"]
    if age_days <= 30:
        return 2, [f"posteado hace {age_days}d — pool grande, baja conversión"]
    return 0, [f"posteado hace {age_days}d — probablemente cerrado/saturado"]


def score_company_tier(job: dict, analysis: dict | None) -> tuple[int, list[str]]:
    """+0..10 si la empresa está en target_companies del análisis."""
    if not analysis:
        return 0, []
    company = (job.get("company") or "").lower()
    targets = analysis.get("target_companies") or []
    for t in targets:
        if company == t["company"].lower():
            if t["fit"] == "high":
                return 10, [f"empresa en target list — fit alto"]
            if t["fit"] == "medium":
                return 6, [f"empresa en target list — fit medio"]
            return 3, [f"empresa en target list — explorar"]
    return 0, []


def evaluate(profile: dict, config: dict, job: dict, analysis: dict | None) -> dict:
    components = {}
    flags = []
    notes = []

    pts, n = score_stack_match(profile, job)
    components["stack"] = pts
    notes.extend(n)

    pts, n, f = score_seniority_match(profile, job, analysis)
    components["seniority"] = pts
    notes.extend(n)
    flags.extend(f)

    pts, n, f = score_remote_fit(profile, job, config)
    components["remote_fit"] = pts
    notes.extend(n)
    flags.extend(f)

    pts, n, f = score_salary(profile, job, config)
    components["salary"] = pts
    notes.extend(n)
    flags.extend(f)

    pts, n = score_freshness(job)
    components["freshness"] = pts
    notes.extend(n)

    pts, n = score_company_tier(job, analysis)
    components["company_tier"] = pts
    notes.extend(n)

    raw_total = sum(components.values())
    score = max(0, min(SCORE_MAX, raw_total))

    recommendation = "skip"
    if "deal_breaker" in flags or "below_minimum" in flags:
        recommendation = "skip"
    elif score >= 80:
        recommendation = "apply_priority"
    elif score >= 70:
        recommendation = "apply"
    elif score >= 55:
        recommendation = "consider"

    return {
        "job_id": job.get("id") or job.get("url"),
        "title": job.get("title"),
        "company": job.get("company"),
        "score": score,
        "components": components,
        "flags": sorted(set(flags)),
        "rationale": notes,
        "recommendation": recommendation,
    }


def load_job_from_args(args) -> dict:
    if args.job_file:
        return json.loads(args.job_file.read_text(encoding="utf-8"))
    if args.stdin:
        return json.loads(sys.stdin.read())
    sys.exit("Pasá --job-file <path> o --stdin (JSON inline no se acepta por seguridad)")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--analysis", type=Path, help="analysis.json (opcional, mejora el scoring)")
    parser.add_argument("--job-file", type=Path, help="Path a JSON del job (recomendado para data untrusted)")
    parser.add_argument("--stdin", action="store_true", help="Leer job JSON de stdin")
    args = parser.parse_args()

    profile = json.loads(args.profile.read_text(encoding="utf-8"))
    config = json.loads(args.config.read_text(encoding="utf-8"))
    analysis = (
        json.loads(args.analysis.read_text(encoding="utf-8"))
        if args.analysis and args.analysis.exists()
        else None
    )
    job = load_job_from_args(args)

    result = evaluate(profile, config, job, analysis)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
