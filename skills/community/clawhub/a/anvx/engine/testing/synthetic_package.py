"""Realistic synthetic data package for a solo-dev AI-native SaaS.

Persona: Solo developer (maybe 1 contractor) running an AI-powered customer
support / content generation SaaS. ~45 paying customers at ~$40/month.
Monthly revenue ~$1,800. Total operational costs ~$1,350/month and growing
at ~7%/month while revenue grows at ~5%/month — the margin is compressing.

Pricing research (early 2026 published rates):
  OpenAI: GPT-4o $2.50/$10 per M tokens, GPT-4o-mini $0.15/$0.60, embeddings $0.02
  Anthropic: Claude Sonnet $3/$15, Claude Haiku $0.25/$1.25
  AWS: t3.medium ~$30/mo, Lambda ~$15/mo for light usage, S3 ~$5, RDS ~$30
  GCP: Cloud Run ~$25/mo, Cloud Storage ~$5, BigQuery ~$10
  Vercel: Pro plan $20/mo (usage within included tier)
  Cloudflare: Workers $5/mo + R2 ~$3/mo
  Twilio: ~20 SMS/day at $0.0079 each + phone number $1/mo ≈ $6/mo
  SendGrid: Essentials plan $19.95/mo for 50K emails
  Datadog: 2 hosts infra ($15/host) + 2GB logs ($3/GB) + 1 APM host ($8) = $44/mo
  LangSmith: Plus 1 seat $39/mo + trace overage ~$10/mo
  Pinecone: Serverless starter, 50K vectors ≈ $8/mo minimum
  Tavily: ~2,000 searches/mo at $0.008/credit = $16/mo
  Stripe: 2.9% + $0.30 per charge on ~$1,800/mo ≈ $82/mo in fees
  GitHub Team: $4/user/mo = $4; Notion: $8/mo; Linear: $8/mo; Figma: $15/mo
  Crypto: 2.5 ETH + 0.1 BTC + 1,500 USDC (personal holdings shown read-only)
"""
import csv
import json
import random
from collections import defaultdict
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

from engine.models import FinancialRecord, Provider, SpendCategory

_DATA_DIR = Path(__file__).resolve().parent / "data"
_RNG = random.Random(2026)

# ── Persona constants ──────────────────────────────────────────────

_STARTING_BALANCE = Decimal("12500.00")
_BASE_CUSTOMERS = 45
_MONTHLY_PRICE = Decimal("40.00")
_CUSTOMER_CHURN_RATE = 0.05  # ~2-3 leave per month
_CUSTOMER_ACQUISITION = 1.5  # ~1-2 new per month
_REVENUE_GROWTH = 1.05  # 5%/month
_COST_GROWTH = 1.07  # 7%/month — compresses margin

# Monthly cost profile (month 0 baseline)
_MONTHLY_COSTS = {
    # AI providers
    "OPENAI *API USAGE": Decimal("420.00"),
    "ANTHROPIC *API BILLING": Decimal("185.00"),
    # Cloud infra
    "AWS SERVICES": Decimal("80.00"),
    "GOOGLE CLOUD PLATFORM": Decimal("42.00"),
    "VERCEL INC": Decimal("20.00"),
    "CLOUDFLARE INC": Decimal("8.00"),
    # Comms
    "TWILIO COMMUNICATIONS": Decimal("6.00"),
    "SENDGRID EMAIL": Decimal("19.95"),
    # Monitoring
    "DATADOG INC": Decimal("44.00"),
    "LANGSMITH LANGCHAIN": Decimal("49.00"),
    # Data/search
    "PINECONE SYSTEMS": Decimal("8.00"),
    "TAVILY SEARCH": Decimal("16.00"),
    # Dev tools
    "GITHUB INC": Decimal("4.00"),
    "NOTION LABS": Decimal("8.00"),
    "LINEAR APP": Decimal("8.00"),
    "FIGMA INC": Decimal("15.00"),
}

# How often each provider bills (days between charges)
_BILLING_FREQUENCY: dict[str, int] = {
    "OPENAI *API USAGE": 7,       # weekly usage billing
    "ANTHROPIC *API BILLING": 7,  # weekly
    "AWS SERVICES": 7,            # weekly consolidated
    "GOOGLE CLOUD PLATFORM": 14,  # biweekly
    "VERCEL INC": 30,             # monthly
    "CLOUDFLARE INC": 30,         # monthly
    "TWILIO COMMUNICATIONS": 14,  # biweekly
    "SENDGRID EMAIL": 30,         # monthly
    "DATADOG INC": 30,            # monthly
    "LANGSMITH LANGCHAIN": 30,    # monthly
    "PINECONE SYSTEMS": 30,       # monthly
    "TAVILY SEARCH": 30,          # monthly
    "GITHUB INC": 30,
    "NOTION LABS": 30,
    "LINEAR APP": 30,
    "FIGMA INC": 30,
}

# SpendCategory mapping for bank CSV categoriser verification
_BANK_CATEGORY: dict[str, SpendCategory] = {
    "OPENAI *API USAGE": SpendCategory.AI_INFERENCE,
    "ANTHROPIC *API BILLING": SpendCategory.AI_INFERENCE,
    "AWS SERVICES": SpendCategory.CLOUD_INFRASTRUCTURE,
    "GOOGLE CLOUD PLATFORM": SpendCategory.CLOUD_INFRASTRUCTURE,
    "VERCEL INC": SpendCategory.CLOUD_INFRASTRUCTURE,
    "CLOUDFLARE INC": SpendCategory.CLOUD_INFRASTRUCTURE,
    "TWILIO COMMUNICATIONS": SpendCategory.COMMUNICATION,
    "SENDGRID EMAIL": SpendCategory.COMMUNICATION,
    "DATADOG INC": SpendCategory.MONITORING,
    "LANGSMITH LANGCHAIN": SpendCategory.MONITORING,
    "PINECONE SYSTEMS": SpendCategory.SEARCH_DATA,
    "TAVILY SEARCH": SpendCategory.SEARCH_DATA,
    "GITHUB INC": SpendCategory.SAAS_SUBSCRIPTION,
    "NOTION LABS": SpendCategory.SAAS_SUBSCRIPTION,
    "LINEAR APP": SpendCategory.SAAS_SUBSCRIPTION,
    "FIGMA INC": SpendCategory.SAAS_SUBSCRIPTION,
}


# ── PART 1: Bank CSV ──────────────────────────────────────────────


def generate_bank_csv(
    start_date: date | None = None,
    end_date: date | None = None,
) -> Path:
    """Generate a realistic 90-day bank statement CSV.

    Returns the path to the written file.
    """
    if end_date is None:
        end_date = date.today()
    if start_date is None:
        start_date = end_date - timedelta(days=90)

    rng = random.Random(2026)
    _DATA_DIR.mkdir(parents=True, exist_ok=True)
    out_path = _DATA_DIR / "bank_statement.csv"

    rows: list[dict] = []
    balance = _STARTING_BALANCE

    current = start_date
    # Stagger initial billing dates so providers don't all hit day 1.
    # Monthly billers anchor to different days; weekly billers start offset.
    last_billed: dict[str, date] = {}
    provider_list = list(_MONTHLY_COSTS.keys())
    for i, desc in enumerate(provider_list):
        freq = _BILLING_FREQUENCY[desc]
        # Offset each provider by a few days so they don't all fire on day 1
        offset = (i * 3) % freq
        last_billed[desc] = start_date - timedelta(days=freq - offset)

    while current <= end_date:
        is_weekend = current.weekday() >= 5
        months_elapsed = (current - start_date).days / 30.0
        cost_growth = Decimal(str(round(_COST_GROWTH ** months_elapsed, 4)))
        rev_growth = Decimal(str(round(_REVENUE_GROWTH ** months_elapsed, 4)))

        day_rows: list[dict] = []

        # ── Stripe revenue transfers (twice per month, ~1st and ~15th) ──
        if current.day in (1, 2, 15, 16) and not is_weekend:
            half_month_rev = (
                _BASE_CUSTOMERS * _MONTHLY_PRICE * rev_growth / 2
            ).quantize(Decimal("0.01"))
            # Add noise
            half_month_rev = (
                half_month_rev * Decimal(str(round(rng.uniform(0.92, 1.08), 3)))
            ).quantize(Decimal("0.01"))
            balance += half_month_rev
            day_rows.append({
                "date": current.isoformat(),
                "description": "STRIPE TRANSFER",
                "amount": str(half_month_rev),
                "balance": str(balance),
            })
            # Stripe fee: 2.9% + $0.30 per charge, assume ~22 charges per half
            n_charges = rng.randint(18, 26)
            fee = (
                half_month_rev * Decimal("0.029")
                + Decimal("0.30") * n_charges
            ).quantize(Decimal("0.01"))
            balance -= fee
            day_rows.append({
                "date": current.isoformat(),
                "description": "STRIPE PROCESSING FEE",
                "amount": str(-fee),
                "balance": str(balance),
            })

        # ── Occasional mid-month refund (once in 90 days) ──
        if current == start_date + timedelta(days=37):
            refund = Decimal("-40.00")
            balance += refund
            day_rows.append({
                "date": current.isoformat(),
                "description": "STRIPE REFUND — CUSTOMER #38",
                "amount": str(refund),
                "balance": str(balance),
            })

        # ── Provider charges (skip weekends for most) ──
        if not is_weekend:
            for description, base_monthly in _MONTHLY_COSTS.items():
                freq = _BILLING_FREQUENCY[description]
                last = last_billed.get(description)
                if last is not None and (current - last).days < freq:
                    continue

                # Calculate charge: (monthly / (30/freq)) * growth * noise
                charges_per_month = 30 / freq
                charge = (
                    base_monthly / Decimal(str(charges_per_month))
                    * cost_growth
                    * Decimal(str(round(rng.uniform(0.88, 1.12), 3)))
                ).quantize(Decimal("0.01"))

                balance -= charge
                day_rows.append({
                    "date": current.isoformat(),
                    "description": description,
                    "amount": str(-charge),
                    "balance": str(balance),
                })
                last_billed[description] = current

        # ── One-off charges ──
        # Domain renewal
        if current == start_date + timedelta(days=22):
            balance -= Decimal("14.99")
            day_rows.append({
                "date": current.isoformat(),
                "description": "NAMECHEAP DOMAIN RENEWAL",
                "amount": "-14.99",
                "balance": str(balance),
            })
        # Conference ticket
        if current == start_date + timedelta(days=55):
            balance -= Decimal("299.00")
            day_rows.append({
                "date": current.isoformat(),
                "description": "AI CONF 2026 EARLY BIRD",
                "amount": "-299.00",
                "balance": str(balance),
            })

        rows.extend(day_rows)
        current += timedelta(days=1)

    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "description", "amount", "balance"])
        writer.writeheader()
        writer.writerows(rows)

    return out_path


# ── PART 2: Stripe charges ────────────────────────────────────────


def generate_stripe_charges(
    start_date: date | None = None,
    end_date: date | None = None,
) -> Path:
    """Generate 90 days of Stripe charge data as JSON.

    Models 45 customers with churn/acquisition, fees, and refunds.
    """
    if end_date is None:
        end_date = date.today()
    if start_date is None:
        start_date = end_date - timedelta(days=90)

    rng = random.Random(2026)
    _DATA_DIR.mkdir(parents=True, exist_ok=True)
    out_path = _DATA_DIR / "stripe_charges.json"

    # Initialize customer pool
    active_customers = [f"cus_{1000 + i}" for i in range(_BASE_CUSTOMERS)]
    charges: list[dict] = []
    next_cust_id = 1000 + _BASE_CUSTOMERS

    current = start_date
    month_cursor = start_date.month

    while current <= end_date:
        # Monthly events: churn + acquisition at month boundaries
        if current.month != month_cursor:
            month_cursor = current.month
            # Churn 2-3
            n_churn = rng.randint(2, 3)
            for _ in range(min(n_churn, len(active_customers))):
                churned = rng.choice(active_customers)
                active_customers.remove(churned)
                charges.append({
                    "id": f"ch_cancel_{churned}_{current.isoformat()}",
                    "customer": churned,
                    "amount": 0,
                    "status": "canceled",
                    "created": current.isoformat(),
                    "description": "Subscription canceled",
                })
            # Acquire 1-2
            n_new = rng.randint(1, 2)
            for _ in range(n_new):
                cust = f"cus_{next_cust_id}"
                next_cust_id += 1
                active_customers.append(cust)

        # Daily charges: each active customer pays once per month
        # Distribute charges across the month (~1-3 per day)
        if current.weekday() < 5:  # business days
            day_of_month = current.day
            for cust in active_customers:
                # Each customer's billing day is hash-derived
                billing_day = (hash(cust) % 28) + 1
                if billing_day == day_of_month:
                    amount_cents = int(
                        float(_MONTHLY_PRICE) * 100
                        * rng.uniform(0.95, 1.05)  # slight plan variance
                    )
                    fee_cents = int(amount_cents * 0.029 + 30)
                    charges.append({
                        "id": f"ch_{cust}_{current.isoformat()}",
                        "customer": cust,
                        "amount": amount_cents,
                        "amount_usd": round(amount_cents / 100, 2),
                        "fee_cents": fee_cents,
                        "fee_usd": round(fee_cents / 100, 2),
                        "status": "succeeded",
                        "created": current.isoformat(),
                        "description": f"Subscription — {cust}",
                    })

        # Refunds: 2-3 over the whole period
        if current == start_date + timedelta(days=25):
            refund_cust = rng.choice(active_customers)
            charges.append({
                "id": f"re_{refund_cust}_{current.isoformat()}",
                "customer": refund_cust,
                "amount": -4000,
                "amount_usd": -40.00,
                "status": "refunded",
                "created": current.isoformat(),
                "description": f"Refund — {refund_cust}",
            })
        if current == start_date + timedelta(days=62):
            refund_cust = rng.choice(active_customers)
            charges.append({
                "id": f"re_{refund_cust}_{current.isoformat()}",
                "customer": refund_cust,
                "amount": -4000,
                "amount_usd": -40.00,
                "status": "refunded",
                "created": current.isoformat(),
                "description": f"Refund — {refund_cust}",
            })

        current += timedelta(days=1)

    with open(out_path, "w") as f:
        json.dump({"charges": charges, "total": len(charges)}, f, indent=2)

    return out_path


# ── PART 3: Full profile (all 14 connectors + bank + Stripe) ─────


def generate_full_profile(
    start_date: date | None = None,
    end_date: date | None = None,
) -> dict:
    """Generate internally-consistent synthetic data across all surfaces.

    Returns a summary dict with stats and paths. The connector synthetic
    records are generated via each connector's get_synthetic_records() which
    already embed the optimization-triggering patterns:

    - Model routing: OpenAI gpt-4o generates 25 requests/day, 80% with
      <500 input tokens (developer defaulting to GPT-4o for simple
      classification/extraction tasks).
    - Caching: Anthropic claude-sonnet has CV≈0.03 on input tokens
      (customer support bot reusing ~1800-token system prompt).
    - Batch processing: OpenAI has 27 requests/day with near-zero std dev
      (nightly report generation + hourly classification cron).
    - Unit economics: AI costs at ~35% of revenue with costs growing 7%/mo
      vs revenue at 5%/mo — margin compressing from 25% toward breakeven.
    - Price comparison: Both OpenAI and Anthropic used for overlapping
      inference tasks, enabling direct workload cost comparison.
    - Spend forecast: All costs have upward growth multiplier baked into
      the synthetic generators (8% OpenAI, 6% Anthropic, 5% Stripe revenue).
    """
    if end_date is None:
        end_date = date.today()
    if start_date is None:
        start_date = end_date - timedelta(days=90)

    from engine.connectors import (
        AWSCostsConnector, AnthropicBillingConnector, BinanceExchangeConnector,
        CloudflareCostsConnector, CoinbaseExchangeConnector,
        CryptoWalletConnector, DatadogCostsConnector, GCPCostsConnector,
        LangSmithCostsConnector, OpenAIBillingConnector, PineconeCostsConnector,
        SendGridCostsConnector, StripeConnector, TavilyCostsConnector,
        TwilioCostsConnector, VercelCostsConnector,
    )

    connectors = [
        ("openai", OpenAIBillingConnector),
        ("anthropic", AnthropicBillingConnector),
        ("stripe", StripeConnector),
        ("crypto_wallet", CryptoWalletConnector),
        ("coinbase", CoinbaseExchangeConnector),
        ("binance", BinanceExchangeConnector),
        ("aws", AWSCostsConnector),
        ("gcp", GCPCostsConnector),
        ("vercel", VercelCostsConnector),
        ("cloudflare", CloudflareCostsConnector),
        ("twilio", TwilioCostsConnector),
        ("sendgrid", SendGridCostsConnector),
        ("datadog", DatadogCostsConnector),
        ("langsmith", LangSmithCostsConnector),
        ("pinecone", PineconeCostsConnector),
        ("tavily", TavilyCostsConnector),
    ]

    by_provider: dict[str, list[FinancialRecord]] = {}
    all_records: list[FinancialRecord] = []

    for name, cls in connectors:
        records = cls().get_synthetic_records(start_date, end_date)
        by_provider[name] = records
        all_records.extend(records)

    # Generate companion files
    bank_path = generate_bank_csv(start_date, end_date)
    stripe_path = generate_stripe_charges(start_date, end_date)

    # Aggregate stats
    total_costs = sum(r.amount for r in all_records if r.amount < 0)
    total_revenue = sum(r.amount for r in all_records if r.category == SpendCategory.REVENUE)
    total_holdings = sum(
        r.amount for r in all_records if r.category == SpendCategory.CRYPTO_HOLDINGS
    )

    by_category: dict[str, Decimal] = defaultdict(Decimal)
    for r in all_records:
        by_category[r.category.value] += abs(r.amount) if r.amount < 0 else r.amount

    return {
        "period": {"start": start_date.isoformat(), "end": end_date.isoformat()},
        "records_total": len(all_records),
        "records_by_provider": {k: len(v) for k, v in by_provider.items()},
        "total_costs": str(total_costs),
        "total_revenue": str(total_revenue),
        "total_holdings": str(total_holdings),
        "by_category": {k: str(v) for k, v in sorted(by_category.items(), key=lambda x: x[1], reverse=True)},
        "bank_csv_path": str(bank_path),
        "stripe_charges_path": str(stripe_path),
        "all_records": all_records,
        "by_provider": by_provider,
    }
