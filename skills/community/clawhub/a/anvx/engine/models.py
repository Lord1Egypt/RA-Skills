"""Core data models for Token Economy Intelligence."""
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from pydantic import BaseModel, Field

class SpendCategory(str, Enum):
	AI_INFERENCE = "ai_inference"
	AI_TRAINING = "ai_training"
	CLOUD_INFRASTRUCTURE = "cloud_infrastructure"
	SAAS_SUBSCRIPTION = "saas_subscription"
	PAYMENT_PROCESSING = "payment_processing"
	COMMUNICATION = "communication"
	MONITORING = "monitoring"
	SEARCH_DATA = "search_data"
	ADVERTISING = "advertising"
	CRYPTO_HOLDINGS = "crypto_holdings"
	REVENUE = "revenue"
	OTHER = "other"

class Provider(str, Enum):
	OPENAI = "openai"
	ANTHROPIC = "anthropic"
	GEMINI = "gemini"
	GOOGLE_ADS = "google_ads"
	STRIPE = "stripe"
	META = "meta"
	AWS = "aws"
	GCP = "gcp"
	VERCEL = "vercel"
	CLOUDFLARE = "cloudflare"
	TWILIO = "twilio"
	SENDGRID = "sendgrid"
	DATADOG = "datadog"
	LANGSMITH = "langsmith"
	PINECONE = "pinecone"
	TAVILY = "tavily"
	CRYPTO_WALLET = "crypto_wallet"
	COINBASE = "coinbase"
	BINANCE = "binance"
	OTHER = "other"

class FinancialRecord(BaseModel):
	"""A single financial record (cost, revenue, or holding)."""
	record_date: date
	amount: Decimal = Field(description="Negative = cost, positive = revenue")
	currency: str = "USD"
	category: SpendCategory
	subcategory: str | None = None
	provider: Provider
	model: str | None = None
	tokens_input: int | None = None
	tokens_output: int | None = None
	source: str
	raw_description: str | None = None
	confidenc: float = 1.0

class Anomaly(BaseModel):
	"""A detected spending anomaly."""
	category: str
	description: str
	current_amount: Decimal
	baseline_amount: Decimal
	deviation_percent: float
	severity: str = "medium"

class Recommendation(BaseModel):
	"""A cost optimization recommendation."""
	rec_type: str
	description: str
	estimated_monthly_savings: Decimal | None = None
	confidence: str = "medium"
	action_required: str
	category: SpendCategory
	source_module: str | None = None
	methodology: str | None = None

class FinancialSummary(BaseModel):
	"""The current state of the user's financial model."""
	last_updated: datetime
	total_monthly_spend: Decimal = Decimal("0")
	spend_by_category: dict[str, Decimal] = {}
	spend_by_provider: dict[str, Decimal] = {}
	revenue_monthly: Decimal | None = None
	crypto_holdings_usd: Decimal | None = None
	anomalies: list[Anomaly] = []
	recommendations: list[Recommendation] = []
	connected_accounts: list[str] = []
	data_coverage_days: int = 0
	record_count: int = 0
