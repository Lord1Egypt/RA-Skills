"""Generate and display cost optimisation recommendations."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from engine.analytics import EventTracker
from engine.intelligence import FinancialModelManager, generate_recommendations
from engine.utils import format_currency


def main() -> None:
    tracker = EventTracker()

    model = FinancialModelManager()
    model.load()

    if model.get_summary().record_count == 0:
        print("No data yet. Run setup.py first.")
        sys.exit(1)

    recs = generate_recommendations(model.records)
    tracker.track("recommendation_viewed", "intelligence", "openclaw",
                  {"count": len(recs)})

    if not recs:
        print("No recommendations right now — your spending looks healthy.")
        return

    print(f"Found {len(recs)} recommendation{'s' if len(recs) != 1 else ''}:\n")

    for i, r in enumerate(recs, 1):
        savings = format_currency(r.estimated_monthly_savings) + "/mo" if r.estimated_monthly_savings else "TBD"
        confidence_label = {"high": "High confidence", "medium": "Medium confidence", "low": "Low confidence"}

        print(f"{i}. {r.description}")
        print(f"   Estimated savings: {savings} ({confidence_label.get(r.confidence, r.confidence)})")
        print(f"   Action: {r.action_required}")
        print()
        print(f"   Want me to help you make this change?")
        print()

    model.save()


if __name__ == "__main__":
    main()
