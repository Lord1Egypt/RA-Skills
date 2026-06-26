#!/usr/bin/env python3
"""
track_applications.py — CRUD sobre data/applications.json para llevar el
estado de cada postulación. Sub-comandos: add, update, list, get,
pending-followups, archive-stale.

Uso:
    python3 track_applications.py add --job-id <id> --slug <slug> \
        --title "Senior Backend" --company "Acme" --url "https://..." \
        [--status drafted] [--notes "..."]

    python3 track_applications.py update --job-id <id> \
        --status submitted --submitted-at 2026-04-29 \
        [--notes "..."]

    python3 track_applications.py list [--status submitted] [--json]
    python3 track_applications.py get --job-id <id>
    python3 track_applications.py pending-followups --config config.json
    python3 track_applications.py archive-stale --config config.json [--dry-run]

Estados válidos (configurables en config.json):
    drafted → submitted → viewed → screening → interview → offer/rejected/ghosted/withdrawn
"""

import argparse
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


DEFAULT_STATUSES = [
    "drafted", "submitted", "viewed", "screening", "interview",
    "offer", "rejected", "withdrawn", "ghosted",
]
ACTIVE_STATUSES = {"drafted", "submitted", "viewed", "screening", "interview"}
DEFAULT_FOLLOW_UP_DAYS = [3, 7, 14]


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _data_path() -> Path:
    """Ubica data/applications.json relativo al script (uno arriba, en data/)."""
    here = Path(__file__).resolve().parent
    return here.parent / "data" / "applications.json"


def _load(path: Path) -> dict:
    if not path.exists():
        return {"applications": []}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.exit(f"applications.json corrupto ({e}). Hacé backup manual antes de continuar.")


def _save(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def _find(data: dict, job_id: str) -> dict | None:
    for app in data["applications"]:
        if app.get("job_id") == job_id:
            return app
    return None


def cmd_add(args) -> int:
    path = args.store or _data_path()
    data = _load(path)
    if _find(data, args.job_id):
        sys.exit(f"Ya existe una postulación con job_id={args.job_id}. Usá 'update'.")
    now = _now_iso()
    app = {
        "job_id": args.job_id,
        "slug": args.slug,
        "title": args.title,
        "company": args.company,
        "url": args.url,
        "status": args.status,
        "score": args.score,
        "created_at": now,
        "updated_at": now,
        "submitted_at": None,
        "events": [{"at": now, "type": "created", "status": args.status}],
        "notes": args.notes or "",
    }
    if args.status == "submitted":
        app["submitted_at"] = now
    data["applications"].append(app)
    _save(path, data)
    print(f"OK — agregada {args.job_id} ({args.title} @ {args.company}) status={args.status}")
    return 0


def cmd_update(args) -> int:
    path = args.store or _data_path()
    data = _load(path)
    app = _find(data, args.job_id)
    if not app:
        sys.exit(f"No existe postulación con job_id={args.job_id}.")
    now = _now_iso()
    if args.status:
        if app["status"] == args.status:
            print(f"Sin cambios: status ya era {args.status}")
        else:
            app["events"].append({"at": now, "type": "status_change", "from": app["status"], "to": args.status})
            app["status"] = args.status
            if args.status == "submitted" and not app.get("submitted_at"):
                app["submitted_at"] = args.submitted_at or now
    if args.notes:
        app["events"].append({"at": now, "type": "note", "text": args.notes})
        app["notes"] = (app.get("notes") or "") + ("\n" if app.get("notes") else "") + f"[{now}] {args.notes}"
    if args.submitted_at and not app.get("submitted_at"):
        app["submitted_at"] = args.submitted_at
    app["updated_at"] = now
    _save(path, data)
    print(f"OK — actualizada {args.job_id} → status={app['status']}")
    return 0


def cmd_get(args) -> int:
    path = args.store or _data_path()
    data = _load(path)
    app = _find(data, args.job_id)
    if not app:
        sys.exit(f"No existe postulación con job_id={args.job_id}.")
    print(json.dumps(app, indent=2, ensure_ascii=False))
    return 0


def cmd_list(args) -> int:
    path = args.store or _data_path()
    data = _load(path)
    apps = data["applications"]
    if args.status:
        apps = [a for a in apps if a.get("status") == args.status]
    if args.json:
        print(json.dumps(apps, indent=2, ensure_ascii=False))
        return 0
    if not apps:
        print("(sin postulaciones)")
        return 0
    print(f"{'STATUS':<12} {'SCORE':<6} {'COMPANY':<20} {'TITLE':<40} {'JOB_ID':<20} {'SUBMITTED':<12}")
    for a in apps:
        submitted = (a.get("submitted_at") or "")[:10]
        company = (a.get("company") or "")[:20]
        title = (a.get("title") or "")[:40]
        score = str(a.get("score") or "")
        print(f"{a['status']:<12} {score:<6} {company:<20} {title:<40} {a['job_id'][:20]:<20} {submitted:<12}")
    return 0


def cmd_pending_followups(args) -> int:
    path = args.store or _data_path()
    data = _load(path)
    follow_up_days = DEFAULT_FOLLOW_UP_DAYS
    if args.config and args.config.exists():
        cfg = json.loads(args.config.read_text(encoding="utf-8"))
        follow_up_days = cfg.get("tracking", {}).get("follow_up_days", DEFAULT_FOLLOW_UP_DAYS)

    now = datetime.now(timezone.utc)
    pending = []
    for app in data["applications"]:
        if app.get("status") not in ACTIVE_STATUSES:
            continue
        ref = app.get("submitted_at") or app.get("updated_at") or app.get("created_at")
        if not ref:
            continue
        try:
            ref_dt = datetime.fromisoformat(ref.replace("Z", "+00:00"))
        except ValueError:
            continue
        days_since = (now - ref_dt).days
        triggers_hit = [d for d in follow_up_days if days_since >= d]
        if not triggers_hit:
            continue
        last_trigger = max(triggers_hit)
        pending.append({
            "job_id": app["job_id"],
            "title": app.get("title"),
            "company": app.get("company"),
            "status": app["status"],
            "days_since": days_since,
            "follow_up_milestone": last_trigger,
            "url": app.get("url"),
            "suggested_action": _suggest_action(last_trigger, app),
        })
    if args.json:
        print(json.dumps(pending, indent=2, ensure_ascii=False))
        return 0
    if not pending:
        print("(sin follow-ups pendientes)")
        return 0
    for p in pending:
        print(f"[{p['days_since']}d] {p['company']} — {p['title']} ({p['status']})")
        print(f"   → {p['suggested_action']}")
        print(f"   {p['url']}")
    return 0


def _suggest_action(milestone_day: int, app: dict) -> str:
    if milestone_day <= 3:
        return (
            "Mandá un mensaje breve por LinkedIn al recruiter o hiring manager. "
            "Mencioná tu interés genuino + 1 detalle del rol que te llamó la atención."
        )
    if milestone_day <= 7:
        return (
            "Verificá si el posting sigue activo. Buscá conexiones que trabajen en la empresa "
            "para pedir referido interno (LinkedIn → empresa → 2nd connections)."
        )
    if milestone_day <= 14:
        return (
            "Mandá un follow-up final preguntando estado. Si no hay respuesta en 3-5 días más, "
            "marcá como 'ghosted' y soltá. No vale la pena más energía ahí."
        )
    return "Marcá como 'ghosted' y archivá. Liberá energía mental para nuevas oportunidades."


def cmd_archive_stale(args) -> int:
    path = args.store or _data_path()
    data = _load(path)
    cutoff_days = 60
    if args.config and args.config.exists():
        cfg = json.loads(args.config.read_text(encoding="utf-8"))
        cutoff_days = cfg.get("tracking", {}).get("auto_archive_after_days", 60)
    now = datetime.now(timezone.utc)
    archived = 0
    for app in data["applications"]:
        if app.get("status") not in ACTIVE_STATUSES:
            continue
        ref = app.get("updated_at") or app.get("created_at")
        if not ref:
            continue
        try:
            ref_dt = datetime.fromisoformat(ref.replace("Z", "+00:00"))
        except ValueError:
            continue
        if (now - ref_dt).days >= cutoff_days:
            if args.dry_run:
                print(f"[dry-run] archivaría {app['job_id']} ({app.get('company')}) — {(now - ref_dt).days}d sin update")
            else:
                app["events"].append({"at": _now_iso(), "type": "auto_archived", "from": app["status"]})
                app["status"] = "ghosted"
                app["updated_at"] = _now_iso()
            archived += 1
    if not args.dry_run:
        _save(path, data)
    print(f"{'(dry-run) ' if args.dry_run else ''}archivadas {archived} postulaciones stale.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--store", type=Path, help="Path alternativo al applications.json (testing)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add")
    p_add.add_argument("--job-id", required=True)
    p_add.add_argument("--slug", required=True)
    p_add.add_argument("--title", default="")
    p_add.add_argument("--company", default="")
    p_add.add_argument("--url", default="")
    p_add.add_argument("--status", default="drafted", choices=DEFAULT_STATUSES)
    p_add.add_argument("--score", type=int)
    p_add.add_argument("--notes", default="")
    p_add.set_defaults(func=cmd_add)

    p_upd = sub.add_parser("update")
    p_upd.add_argument("--job-id", required=True)
    p_upd.add_argument("--status", choices=DEFAULT_STATUSES)
    p_upd.add_argument("--submitted-at")
    p_upd.add_argument("--notes")
    p_upd.set_defaults(func=cmd_update)

    p_get = sub.add_parser("get")
    p_get.add_argument("--job-id", required=True)
    p_get.set_defaults(func=cmd_get)

    p_list = sub.add_parser("list")
    p_list.add_argument("--status", choices=DEFAULT_STATUSES)
    p_list.add_argument("--json", action="store_true")
    p_list.set_defaults(func=cmd_list)

    p_pf = sub.add_parser("pending-followups")
    p_pf.add_argument("--config", type=Path)
    p_pf.add_argument("--json", action="store_true")
    p_pf.set_defaults(func=cmd_pending_followups)

    p_arch = sub.add_parser("archive-stale")
    p_arch.add_argument("--config", type=Path)
    p_arch.add_argument("--dry-run", action="store_true")
    p_arch.set_defaults(func=cmd_archive_stale)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
