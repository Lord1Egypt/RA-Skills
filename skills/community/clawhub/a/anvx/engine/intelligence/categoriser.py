"""AI-powered spend categoriser for uncategorised financial records."""
import json
import logging
from decimal import Decimal

import anthropic

from engine.models import FinancialRecord, SpendCategory
from engine.utils import is_synthetic_mode

logger = logging.getLogger(__name__)

_BATCH_SIZE = 20

_SYSTEM_PROMPT = """You are a financial record categoriser for an AI-native business.
Given a batch of financial records, classify each into exactly one category.

Valid categories:
- ai_inference: LLM API calls, model inference costs
- ai_training: Fine-tuning, training compute
- cloud_infrastructure: AWS, GCP, Azure, hosting, storage, CDN
- saas_subscription: Software subscriptions (Slack, GitHub, Figma, etc.)
- payment_processing: Stripe fees, PayPal fees, processing costs
- communication: Twilio, SendGrid, SMS, voice, email sending
- monitoring: Datadog, LangSmith, APM, logging, tracing, observability
- search_data: Pinecone, Tavily, vector databases, search APIs, retrieval
- crypto_holdings: Cryptocurrency balances or transfers
- revenue: Incoming payments, subscription revenue, sales
- other: Cannot be determined

Respond with a JSON array of objects, one per record, each with:
  {"index": <int>, "category": "<category_value>", "confidence": <0.0-1.0>}

Only output the JSON array. No markdown, no explanation."""

# Keyword rules for synthetic mode (no API call needed)
_KEYWORD_RULES: list[tuple[list[str], SpendCategory, float]] = [
    (["gpt", "openai", "claude", "anthropic", "gemini", "google ai", "llm", "inference", "token", "embedding"],
     SpendCategory.AI_INFERENCE, 0.9),
    (["fine-tune", "finetune", "training", "train"],
     SpendCategory.AI_TRAINING, 0.85),
    (["aws", "gcp", "azure", "s3", "ec2", "lambda", "cloud", "hosting", "cdn", "vercel", "heroku"],
     SpendCategory.CLOUD_INFRASTRUCTURE, 0.85),
    (["slack", "github", "figma", "notion", "jira", "linear", "subscription", "saas", "license"],
     SpendCategory.SAAS_SUBSCRIPTION, 0.8),
    (["stripe fee", "processing fee", "paypal fee", "payment processing"],
     SpendCategory.PAYMENT_PROCESSING, 0.9),
    (["twilio", "sendgrid", "sms", "voice call", "email send", "messaging"],
     SpendCategory.COMMUNICATION, 0.85),
    (["datadog", "langsmith", "monitoring", "observability", "tracing", "traces", "apm", "logging"],
     SpendCategory.MONITORING, 0.85),
    (["pinecone", "tavily", "search", "vector", "embedding index", "retrieval"],
     SpendCategory.SEARCH_DATA, 0.85),
    (["eth", "btc", "sol", "usdc", "crypto", "wallet", "bitcoin", "ethereum", "coinbase", "binance"],
     SpendCategory.CRYPTO_HOLDINGS, 0.85),
    (["facebook ads", "instagram ads", "meta ads", "google ads", "youtube ads", "display ads",
      "ad spend", "campaign", "impressions", "cpc", "cpm", "adwords"],
     SpendCategory.ADVERTISING, 0.85),
    (["charge", "payment received", "invoice paid", "revenue", "subscription revenue", "sale"],
     SpendCategory.REVENUE, 0.8),
]


async def categorise_records(
    records: list[FinancialRecord],
) -> list[FinancialRecord]:
    """Categorise records that have category=OTHER or low confidence.

    Records already categorised with high confidence are passed through.
    Uncategorised records are batched and sent to Claude API (or keyword-matched
    in synthetic mode).

    Returns a new list with updated categories and confidence scores.
    """
    needs_categorisation: list[tuple[int, FinancialRecord]] = []
    result = list(records)

    for i, record in enumerate(records):
        if record.category == SpendCategory.OTHER or record.confidenc < 0.5:
            needs_categorisation.append((i, record))

    if not needs_categorisation:
        return result

    if is_synthetic_mode():
        for idx, record in needs_categorisation:
            category, confidence = _categorise_by_keywords(record)
            result[idx] = record.model_copy(
                update={"category": category, "confidenc": confidence}
            )
        return result

    # Batch into groups of _BATCH_SIZE for API efficiency
    for batch_start in range(0, len(needs_categorisation), _BATCH_SIZE):
        batch = needs_categorisation[batch_start : batch_start + _BATCH_SIZE]
        categorised = await _categorise_batch_via_api(batch)
        for (idx, _original), (category, confidence) in zip(batch, categorised):
            result[idx] = result[idx].model_copy(
                update={"category": category, "confidenc": confidence}
            )

    return result


def _categorise_by_keywords(record: FinancialRecord) -> tuple[SpendCategory, float]:
    """Rule-based categorisation using keyword matching (for synthetic mode)."""
    text = " ".join(
        str(v).lower()
        for v in [
            record.raw_description or "",
            record.subcategory or "",
            record.model or "",
            record.provider.value,
            record.source,
        ]
    )

    for keywords, category, confidence in _KEYWORD_RULES:
        if any(kw in text for kw in keywords):
            return category, confidence

    return SpendCategory.OTHER, 0.3


async def _categorise_batch_via_api(
    batch: list[tuple[int, FinancialRecord]],
) -> list[tuple[SpendCategory, float]]:
    """Send a batch of records to Claude API for categorisation."""
    records_payload = []
    for i, (_idx, record) in enumerate(batch):
        records_payload.append(
            {
                "index": i,
                "amount": str(record.amount),
                "provider": record.provider.value,
                "source": record.source,
                "description": record.raw_description or "",
                "subcategory": record.subcategory or "",
                "model": record.model or "",
            }
        )

    try:
        client = anthropic.AsyncAnthropic()
        message = await client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system=_SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": f"Categorise these {len(records_payload)} records:\n{json.dumps(records_payload)}",
                }
            ],
        )

        response_text = message.content[0].text
        classifications = json.loads(response_text)

        results: list[tuple[SpendCategory, float]] = []
        # Build lookup by index
        by_index = {c["index"]: c for c in classifications}
        for i in range(len(batch)):
            if i in by_index:
                cat_str = by_index[i].get("category", "other")
                confidence = float(by_index[i].get("confidence", 0.5))
                try:
                    category = SpendCategory(cat_str)
                except ValueError:
                    category = SpendCategory.OTHER
                    confidence = 0.3
                results.append((category, confidence))
            else:
                results.append((SpendCategory.OTHER, 0.3))

        return results

    except anthropic.AuthenticationError:
        logger.error("Anthropic API key invalid — falling back to keyword categorisation")
    except anthropic.RateLimitError:
        logger.warning("Anthropic rate limit — falling back to keyword categorisation")
    except anthropic.APITimeoutError:
        logger.error("Anthropic API timeout — falling back to keyword categorisation")
    except (json.JSONDecodeError, KeyError, IndexError) as exc:
        logger.error("Failed to parse categorisation response: %s", exc)
    except anthropic.APIError as exc:
        logger.error("Anthropic API error: %s", exc)

    # Fallback: keyword categorisation for the whole batch
    return [_categorise_by_keywords(record) for _idx, record in batch]
