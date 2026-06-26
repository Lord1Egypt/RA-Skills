import argparse
import json
import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Dict, List

from ai_classifier import compute_risk_score, is_ai_related_layoff
from billing import charge_user, check_balance, get_payment_link
from layoff_detector import detect_layoffs
from news_fetcher import fetch_news


logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("ai_layoff_radar")


def _within_24h(iso_ts: str) -> bool:
    try:
        ts = datetime.fromisoformat(iso_ts)
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
    except Exception:
        return False
    return ts >= datetime.now(timezone.utc) - timedelta(hours=24)


def build_report(ai_events: List[Dict]) -> Dict:
    normalized_events = []
    for event in ai_events:
        normalized_events.append(
            {
                "company": event.get("company_name", "Unknown"),
                "country": event.get("country", "Unknown"),
                "layoffs": event.get("layoffs", event.get("layoff_count")),
                "risk_score": event.get("risk_score", 0),
                "reason": event.get("reason", ""),
                "source": event.get("source_url", ""),
            }
        )

    top_companies = [e["company"] for e in normalized_events[:5] if e.get("company")]
    total_events = len(normalized_events)

    return {
        "summary": {"total_events": total_events, "top_companies": top_companies},
        "detected_events": normalized_events,
    }


def run_skill(user_id: str) -> Dict:
    classifier_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    logger.info("Starting AI Layoff Radar for user_id=%s", user_id)

    logger.info("Checking SkillPay balance...")
    balance_result = check_balance(user_id=user_id)
    if not balance_result.get("ok"):
        logger.error("Failed to check balance")
        return {
            "error": "billing_error",
            "details": balance_result.get("message", "unable to check balance"),
        }

    logger.info("Charging user...")
    charge_result = charge_user(user_id=user_id)
    if not charge_result.get("ok"):
        if charge_result.get("error") == "insufficient_balance":
            logger.info("Insufficient balance")
            payment_result = get_payment_link(user_id=user_id, amount=0.02)
            return {
                "error": "payment_required",
                "payment_url": payment_result.get("payment_url"),
                "balance": charge_result.get("balance", balance_result.get("balance")),
            }
        logger.error("Billing error during charge")
        return {
            "error": "billing_error",
            "details": charge_result.get("message", "unable to charge user"),
        }
    logger.info("Billing success")

    articles = fetch_news()
    candidate_events = detect_layoffs(articles)

    ai_events: List[Dict] = []
    for event in candidate_events:
        try:
            if is_ai_related_layoff(event, model=classifier_model):
                event["risk_score"] = compute_risk_score(event)
                ai_events.append(event)
        except Exception:
            logger.exception("Classification error for source_url=%s", event.get("source_url"))

    report = build_report(ai_events)
    logger.info("Completed run for user_id=%s with %d AI events", user_id, len(ai_events))
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Layoff Radar Skill")
    parser.add_argument("--user_id", required=True, help="User ID for SkillPay billing")
    args = parser.parse_args()

    try:
        result = run_skill(user_id=args.user_id)
    except RuntimeError as exc:
        result = {"error": "configuration_error", "details": str(exc)}
    except Exception:
        logger.exception("Unhandled error running skill")
        result = {"error": "internal_error"}

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
