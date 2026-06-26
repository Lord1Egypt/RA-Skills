from __future__ import annotations

from typing import Any


def _choose_primary_name(context: dict[str, Any]) -> str:
    names = context.get("activity_names", [])
    if isinstance(names, list) and names:
        return str(names[0])
    return "this little performance"


def write_roast_preview(context: dict[str, Any], prompt: str) -> str:
    activity_count = int(context.get("activity_count", 0) or 0)
    sports = [str(s) for s in context.get("sports", []) if s]
    totals = context.get("totals", {})
    hints = context.get("pattern_hints", {})
    tone = (context.get("style", {}) or {}).get("tone", "playful")
    spice = int((context.get("style", {}) or {}).get("spice", 3) or 0)

    if activity_count <= 0:
        return (
            "No Strava activity today, which means the training story has temporarily been replaced by plausible deniability. "
            "A rest day is fine; making the feed look this quiet just gives the roast less material and your excuses more room to breathe."
        )

    lead = _choose_primary_name(context)
    distance = totals.get("distance_km", 0)
    moving = totals.get("moving_minutes", 0)
    kudos = totals.get("kudos", 0)

    if activity_count == 1:
        paragraph = (
            f"{lead} was the day's whole little event: {distance} km and {moving} moving minutes, "
            f"which is respectable work for something that probably began as a normal idea. "
        )
    else:
        sport_mix = ", ".join(sports) if sports else "assorted effort"
        paragraph = (
            f"The day turned into {activity_count} activities across {sport_mix}, "
            f"adding up to {distance} km and {moving} moving minutes of carefully curated inconvenience. "
        )

    if bool(hints.get("repeat_sport_recently", False)):
        paragraph += "There is also just enough repetition in the pattern to suggest this is becoming a personality trait. "

    if kudos:
        paragraph += f"The {kudos} kudos imply other people are willing to encourage this behaviour, which feels generous if not entirely responsible."
    else:
        paragraph += "Mercifully, nobody rushed in to validate it."

    if tone == "coach" or spice == 0:
        paragraph = paragraph.replace("carefully curated inconvenience", "solid work")
        paragraph = paragraph.replace("personality trait", "habit")
        paragraph = paragraph.replace("which feels generous if not entirely responsible", "which is a nice bit of support")

    return " ".join(paragraph.split())
