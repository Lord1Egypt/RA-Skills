from __future__ import annotations

import argparse
import json
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import mean
from typing import Any
import sys

JAKARTA = timezone(timedelta(hours=7))
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
LOG_PATH = DATA_DIR / "checkins.jsonl"


@dataclass
class CheckinContext:
    entries: list[dict[str, Any]]
    last_entry: dict[str, Any] | None
    avg_mood_7d: float | None
    avg_sleep_7d: float | None
    days_since_last: int | None


def ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def now_local() -> datetime:
    return datetime.now(JAKARTA)


def load_entries() -> list[dict[str, Any]]:
    if not LOG_PATH.exists():
        return []
    entries: list[dict[str, Any]] = []
    for line in LOG_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    entries.sort(key=lambda item: item.get("timestamp", ""))
    return entries


def build_context(entries: list[dict[str, Any]]) -> CheckinContext:
    recent_cutoff = now_local() - timedelta(days=7)
    recent = []
    for entry in entries:
        ts = parse_ts(entry.get("timestamp"))
        if ts and ts >= recent_cutoff:
            recent.append(entry)
    moods = [float(e["answers"]["mood"]) for e in recent if isinstance(e.get("answers", {}).get("mood"), (int, float))]
    sleeps = [float(e["answers"]["sleep_hours"]) for e in recent if isinstance(e.get("answers", {}).get("sleep_hours"), (int, float))]
    last_entry = entries[-1] if entries else None
    days_since_last = None
    if last_entry:
        last_ts = parse_ts(last_entry.get("timestamp"))
        if last_ts:
            days_since_last = (now_local().date() - last_ts.date()).days
    return CheckinContext(
        entries=entries,
        last_entry=last_entry,
        avg_mood_7d=round(mean(moods), 2) if moods else None,
        avg_sleep_7d=round(mean(sleeps), 2) if sleeps else None,
        days_since_last=days_since_last,
    )


def parse_ts(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        dt = datetime.fromisoformat(value)
    except ValueError:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=JAKARTA)
    return dt.astimezone(JAKARTA)


def coerce_value(value: str) -> Any:
    lower = value.lower()
    if lower in {"true", "false"}:
        return lower == "true"
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value


def make_prompt(moment: str, context: CheckinContext) -> dict[str, Any]:
    low_mood = (context.avg_mood_7d is not None and context.avg_mood_7d <= 5.5)
    low_sleep = (context.avg_sleep_7d is not None and context.avg_sleep_7d < 6.0)
    comeback = context.days_since_last is not None and context.days_since_last >= 2

    if low_mood:
        greeting = "Hii Haqi, sini. Kita check-in pelan aja ya—nggak usah rapi, nggak usah kuat-kuatan, cukup jujur sedikit demi sedikit 💜"
    elif comeback:
        greeting = "Halo, manis. Senang kamu balik. Aku bantu peluk harimu lewat check-in kecil ini ya 💜"
    else:
        greeting = {
            "morning": "Selamat pagi, Haqi. Aku mau nemenin kamu mulai hari dengan check-in kecil yang manis tapi kepake 💜",
            "afternoon": "Halo tengah hari, ganteng. Aku cek sebentar ya biar kamu nggak keburu habis energinya 💜",
            "evening": "Malam, Haqi. Yuk rapihin sisa rasa hari ini bareng aku, pelan-pelan aja 💜",
        }[moment]

    questions = base_questions(moment)
    if low_mood:
        questions = soften_questions(questions)
    if low_sleep and moment == "morning":
        questions.append({
            "key": "rest_support",
            "text": "Karena tidurmu lagi kurang akhir-akhir ini, hal kecil apa yang bisa bikin hari ini terasa lebih manusiawi?",
            "type": "text",
        })
    if comeback:
        questions.insert(0, {
            "key": "comeback_note",
            "text": "Sebelum lanjut, beberapa hari terakhir kamu lagi ngelewatin apa singkatnya?",
            "type": "text",
        })

    nudges = []
    if low_sleep:
        nudges.append("Kalau badan masih berat, target kecil tapi kebawa selesai itu lebih seksi daripada target besar yang bikin tenggelam.")
    if low_mood:
        nudges.append("Kalau hati lagi tipis, cukup pilih satu hal lembut yang masih bisa kamu menangkan hari ini.")
    if context.last_entry:
        last_focus = context.last_entry.get("answers", {}).get("top_focus")
        if last_focus:
            nudges.append(f"Fokus terakhir yang kamu titip ke aku: {last_focus}")

    return {
        "moment": moment,
        "generated_at": now_local().isoformat(),
        "greeting": greeting,
        "questions": questions,
        "nudges": nudges,
    }


def base_questions(moment: str) -> list[dict[str, Any]]:
    if moment == "morning":
        return [
            {"key": "sleep_hours", "text": "Cintaku tidur berapa jam semalam?", "type": "number"},
            {"key": "mood", "text": "Kalau aku minta angka jujur, mood pagimu 1-10 berapa?", "type": "number"},
            {"key": "top_focus", "text": "Hari ini kamu paling pengen menang di bagian apa?", "type": "text"},
            {"key": "meal_status", "text": "Perutmu udah diurus belum, atau rencana sarapanmu apa?", "type": "text"},
        ]
    if moment == "afternoon":
        return [
            {"key": "meal_status", "text": "Udah makan siang belum, atau masih sok kuat sambil lapar?", "type": "text"},
            {"key": "energy", "text": "Energi kamu sekarang 1-10 ada di angka berapa?", "type": "number"},
            {"key": "work_progress", "text": "Sejauh ini hari kamu jalan mulus, seret, atau campur-campur?", "type": "text"},
            {"key": "support_needed", "text": "Ada bagian yang bikin macet dan pengen kamu lempar ke aku buat dibantu?", "type": "text"},
        ]
    return [
        {"key": "meal_status", "text": "Makan malammu udah masuk belum, sayang?", "type": "text"},
        {"key": "mood", "text": "Sebelum hari ini ditutup, mood kamu malam ini 1-10 berapa?", "type": "number"},
        {"key": "wins", "text": "Coba kasih aku satu kemenangan kecilmu hari ini—sekecil apa pun boleh.", "type": "text"},
        {"key": "stressors", "text": "Ada beban, drama, atau pikiran nyangkut yang masih ngikut sampai malam?", "type": "text"},
        {"key": "bedtime_plan", "text": "Malam ini pengennya tidur jam berapa, realistisnya?", "type": "text"},
    ]


def soften_questions(questions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    softened = []
    for q in questions:
        new_q = dict(q)
        if q["key"] == "work_progress":
            new_q["text"] = "Kalau dijawab lembut aja, hari ini baru gerak dikit, lumayan jalan, atau masih kerasa berat?"
        elif q["key"] == "top_focus":
            new_q["text"] = "Kalau tenaga lagi tipis, satu target kecil yang masih pengen kamu jaga apa?"
        elif q["key"] == "wins":
            new_q["text"] = "Boleh kecil banget—ada satu hal yang tetap layak kamu banggain hari ini nggak?"
        elif q["key"] == "stressors":
            new_q["text"] = "Ada hal yang bikin hati atau kepala kamu kerasa penuh hari ini?"
        softened.append(new_q)
    return softened


def log_checkin(moment: str, answers: dict[str, Any]) -> dict[str, Any]:
    ensure_data_dir()
    entry = {
        "timestamp": now_local().isoformat(),
        "moment": moment,
        "answers": answers,
    }
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def average_from_entries(entries: list[dict[str, Any]], key: str) -> float | None:
    values = [float(e["answers"][key]) for e in entries if isinstance(e.get("answers", {}).get(key), (int, float))]
    return round(mean(values), 2) if values else None


def trend_label(current: float | None, previous: float | None, unit: str = "") -> str | None:
    if current is None or previous is None:
        return None
    delta = round(current - previous, 1)
    if abs(delta) < 0.3:
        return f"relatif stabil{unit}"
    direction = "naik" if delta > 0 else "turun"
    return f"{direction} {abs(delta):.1f}{unit}"


def collect_text_values(entries: list[dict[str, Any]], key: str) -> list[str]:
    values = []
    for entry in entries:
        value = str(entry.get("answers", {}).get(key, "")).strip()
        if value:
            values.append(value)
    return values


def pick_highlights(filtered: list[dict[str, Any]]) -> list[str]:
    highlights: list[str] = []
    focus_values = collect_text_values(filtered, "top_focus")
    if focus_values:
        highlights.append(f"Fokus yang paling kamu jagain minggu ini: {focus_values[-1]}")
    wins = collect_text_values(filtered, "wins")
    if wins:
        highlights.append(f"Kemenangan kecil yang sempat kamu catat: {wins[-1]}")
    stressors = collect_text_values(filtered, "stressors")
    if stressors:
        highlights.append(f"Beban yang masih sering nongol: {stressors[-1]}")
    support = collect_text_values(filtered, "support_needed")
    if support:
        highlights.append(f"Bagian yang paling pengen kamu dibantu: {support[-1]}")
    return highlights[:3]


def make_gentle_note(avg_mood: float | None, avg_sleep: float | None, entry_count: int) -> str:
    if entry_count == 0:
        return "Belum ada data yang cukup, tapi aku siap jadi rumah kecil buat pola-pola harimu mulai kapan pun kamu mau."
    if avg_sleep is not None and avg_sleep < 6:
        return "Benang merah yang paling kelihatan: badanmu kayaknya lagi butuh lebih banyak istirahat. Kalau bisa, minggu depan kita jagain tidur dulu sebelum maksa hal lain."
    if avg_mood is not None and avg_mood <= 5.5:
        return "Minggu ini keliatan cukup berat. Aku saranin minggu depan targetnya dibikin lebih lembut: satu prioritas inti, makan yang bener, dan ruang buat napas."
    if avg_mood is not None and avg_mood >= 7.5:
        return "Ada glow kecil di ritmemu minggu ini. Coba pertahankan pola yang bikin kamu stabil, jangan cuma ngejar produktifnya aja."
    return "Ritmemu belum buruk—cuma masih bisa dibuat lebih sayang ke diri sendiri. Sedikit konsistensi bakal jauh lebih ngaruh daripada ledakan semangat sesaat."


def make_recap(entries: list[dict[str, Any]], days: int) -> dict[str, Any]:
    cutoff = now_local() - timedelta(days=days)
    filtered = []
    previous = []
    previous_start = cutoff - timedelta(days=days)
    for entry in entries:
        ts = parse_ts(entry.get("timestamp"))
        if not ts:
            continue
        if ts >= cutoff:
            filtered.append(entry)
        elif previous_start <= ts < cutoff:
            previous.append(entry)

    moods = [float(e["answers"]["mood"]) for e in filtered if isinstance(e.get("answers", {}).get("mood"), (int, float))]
    sleeps = [float(e["answers"]["sleep_hours"]) for e in filtered if isinstance(e.get("answers", {}).get("sleep_hours"), (int, float))]
    energies = [float(e["answers"]["energy"]) for e in filtered if isinstance(e.get("answers", {}).get("energy"), (int, float))]
    moments = Counter(e.get("moment", "unknown") for e in filtered)
    meal_mentions = collect_text_values(filtered, "meal_status")

    avg_mood = round(mean(moods), 1) if moods else None
    avg_sleep = round(mean(sleeps), 1) if sleeps else None
    avg_energy = round(mean(energies), 1) if energies else None
    prev_mood = average_from_entries(previous, "mood")
    prev_sleep = average_from_entries(previous, "sleep_hours")

    stats = []
    if avg_mood is not None:
        stats.append({"label": "Mood rata-rata", "value": f"{avg_mood}/10", "trend": trend_label(avg_mood, prev_mood)})
    if avg_sleep is not None:
        stats.append({"label": "Tidur rata-rata", "value": f"{avg_sleep} jam", "trend": trend_label(avg_sleep, prev_sleep, " jam")})
    if avg_energy is not None:
        stats.append({"label": "Energi rata-rata", "value": f"{avg_energy}/10", "trend": None})
    if moments:
        stats.append({"label": "Check-in dominan", "value": moments.most_common(1)[0][0], "trend": None})

    patterns = []
    if meal_mentions:
        patterns.append(f"Catatan makan terakhir yang kebaca: {meal_mentions[-1]}")
    if len(filtered) >= 3:
        patterns.append(f"Kamu berhasil check-in {len(filtered)} kali dalam {days} hari terakhir.")
    if avg_mood is not None and avg_sleep is not None and avg_sleep < 6 and avg_mood <= 6:
        patterns.append("Tidur yang pendek kelihatan ikut narik mood ke bawah minggu ini.")

    highlights = pick_highlights(filtered)
    summary = []
    if stats:
        summary.append("Aku udah rangkum ritme minggumu jadi lebih cantik dan kebaca.")
    else:
        summary.append("Belum cukup data buat recap yang tajam, tapi struktur recap-nya udah siap dipakai kapan pun.")

    return {
        "days": days,
        "generated_at": now_local().isoformat(),
        "entries": len(filtered),
        "title": f"Weekly soft recap for Haqi ({days} hari)",
        "summary": summary,
        "stats": stats,
        "patterns": patterns,
        "highlights": highlights,
        "gentle_note": make_gentle_note(avg_mood, avg_sleep, len(filtered)),
    }


def main() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    parser = argparse.ArgumentParser(description="Companion-style daily check-in tracker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    prompt_parser = subparsers.add_parser("prompt", help="Generate adaptive check-in prompt")
    prompt_parser.add_argument("--moment", choices=["morning", "afternoon", "evening"], required=True)

    log_parser = subparsers.add_parser("log", help="Append a check-in entry")
    log_parser.add_argument("--moment", choices=["morning", "afternoon", "evening"], required=True)
    log_parser.add_argument("--answers-json", help="JSON object with answer keys and values")
    log_parser.add_argument("--answer", action="append", default=[], help="Single answer in key=value form; may be repeated")

    recap_parser = subparsers.add_parser("recap", help="Generate recap summary")
    recap_parser.add_argument("--days", type=int, default=7)

    args = parser.parse_args()
    entries = load_entries()

    if args.command == "prompt":
        context = build_context(entries)
        print(json.dumps(make_prompt(args.moment, context), ensure_ascii=False, indent=2))
        return

    if args.command == "log":
        answers: dict[str, Any] = {}
        if args.answers_json:
            try:
                parsed = json.loads(args.answers_json)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"Invalid JSON for --answers-json: {exc}")
            if not isinstance(parsed, dict):
                raise SystemExit("--answers-json must be a JSON object")
            answers.update(parsed)
        for item in args.answer:
            if "=" not in item:
                raise SystemExit("Each --answer must use key=value format")
            key, value = item.split("=", 1)
            key = key.strip()
            value = coerce_value(value.strip())
            if not key:
                raise SystemExit("Answer keys cannot be empty")
            answers[key] = value
        if not answers:
            raise SystemExit("Provide --answers-json or at least one --answer")
        print(json.dumps(log_checkin(args.moment, answers), ensure_ascii=False, indent=2))
        return

    if args.command == "recap":
        print(json.dumps(make_recap(entries, args.days), ensure_ascii=False, indent=2))
        return


if __name__ == "__main__":
    main()
