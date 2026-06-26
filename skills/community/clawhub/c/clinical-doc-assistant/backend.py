"""
Clinical Documentation Assistant — Hosted Backend
FastAPI scaffold for the credit-based generation API.

Deploy this on any cloud (Render, Railway, Fly.io, AWS Lambda, etc.)
Set up Stripe for credit purchases and a Postgres/Supabase DB for accounts.

Routes:
  POST /v1/generate        — generate a clinical document (costs 1 credit)
  GET  /v1/usage           — check remaining credits for an API key
  POST /v1/credits/purchase — create a Stripe checkout session
  GET  /v1/health          — health check
"""

from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import hashlib
import httpx

app = FastAPI(
    title="Clinical Documentation Assistant API",
    description="Credit-based clinical document generation backend for the ClawHub skill.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    # WARNING: wildcard CORS is for local development only.
    # In production, replace "*" with your specific frontend origin(s).
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class GenerateRequest(BaseModel):
    document_type: str          # "soap_note" | "referral" | "prior_auth" | "discharge" | "avs"
    patient_context: dict       # Structured patient data (from FHIR or manual input)
    additional_notes: Optional[str] = None
    provider_name: Optional[str] = None
    specialty: Optional[str] = None  # For referrals

class GenerateResponse(BaseModel):
    document: str               # The generated document text
    document_type: str
    credits_remaining: int
    audit_id: str               # Unique ID for this generation (for audit log)

class UsageResponse(BaseModel):
    credits_remaining: int
    credits_used_this_month: int
    plan: str

# ---------------------------------------------------------------------------
# Auth helper — look up API key in DB
# ---------------------------------------------------------------------------

async def get_account(api_key: str = Header(alias="X-API-Key")):
    """Validate API key and return account record."""
    # TODO: replace with real DB lookup (Supabase, Postgres, etc.)
    # Example with Supabase:
    #   res = supabase.table("accounts").select("*").eq("api_key", hash_key(api_key)).single().execute()
    #   if not res.data: raise HTTPException(401, "Invalid API key")
    #   return res.data
    
    if not api_key or api_key == "test":
        # Sandbox mode — 5 free generations
        return {"id": "sandbox", "credits": 5, "plan": "sandbox", "credits_used": 0}
    
    raise HTTPException(status_code=401, detail="Invalid API key. Get one at https://yourdomain.com")

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/v1/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}


@app.get("/v1/usage", response_model=UsageResponse)
async def get_usage(account: dict = Depends(get_account)):
    return UsageResponse(
        credits_remaining=account["credits"],
        credits_used_this_month=account["credits_used"],
        plan=account["plan"],
    )


@app.post("/v1/generate", response_model=GenerateResponse)
async def generate_document(
    request: GenerateRequest,
    account: dict = Depends(get_account),
):
    # Check credits
    if account["credits"] < 1:
        raise HTTPException(
            status_code=402,
            detail="No credits remaining. Purchase more at https://yourdomain.com/credits",
        )

    # Build the prompt based on document type
    prompt = _build_prompt(request)

    # Call Anthropic (or any LLM) — no PHI is stored after this call
    doc_text = await _call_llm(prompt)

    # Deduct 1 credit
    # TODO: update DB: account["credits"] -= 1
    # TODO: log audit record with audit_id (no PHI stored)

    import uuid
    audit_id = str(uuid.uuid4())

    return GenerateResponse(
        document=doc_text,
        document_type=request.document_type,
        credits_remaining=account["credits"] - 1,
        audit_id=audit_id,
    )


@app.post("/v1/credits/purchase")
async def purchase_credits(
    package: str,  # "starter_10" | "pro_50" | "team_200"
    account: dict = Depends(get_account),
):
    """Create a Stripe Checkout session for credit purchase."""
    # TODO: integrate Stripe
    # import stripe
    # stripe.api_key = os.environ["STRIPE_SECRET_KEY"]
    # price_ids = {
    #     "starter_10": "price_xxx",   # $9 — 10 credits
    #     "pro_50": "price_xxx",        # $39 — 50 credits
    #     "team_200": "price_xxx",      # $129 — 200 credits
    # }
    # session = stripe.checkout.Session.create(
    #     payment_method_types=["card"],
    #     line_items=[{"price": price_ids[package], "quantity": 1}],
    #     mode="payment",
    #     success_url="https://yourdomain.com/success",
    #     cancel_url="https://yourdomain.com/cancel",
    #     metadata={"account_id": account["id"], "package": package},
    # )
    # return {"checkout_url": session.url}
    return {"detail": "Stripe integration not yet configured."}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _build_prompt(req: GenerateRequest) -> str:
    """Build a structured prompt for the LLM based on document type."""
    patient = req.patient_context
    doc_type = req.document_type
    notes = req.additional_notes or ""

    base = f"""You are a clinical documentation assistant. Generate a professional {doc_type.replace("_", " ")} draft.

Patient context:
{_format_patient_context(patient)}

Additional notes from clinician: {notes}

Instructions:
- Use standard clinical terminology and formatting
- Flag any missing data with [MISSING: field name] placeholders
- This is a DRAFT for clinician review — clearly state this at the top
- Do NOT make diagnostic recommendations beyond what is supported by the provided data
"""

    if doc_type == "soap_note":
        base += "\nFormat as: SUBJECTIVE / OBJECTIVE / ASSESSMENT / PLAN"
    elif doc_type == "referral":
        base += f"\nFormat as a professional referral letter. Referring to: {req.specialty or '[Specialist]'}"
    elif doc_type == "prior_auth":
        base += "\nFormat as a prior authorization clinical justification narrative."
    elif doc_type == "discharge":
        base += "\nFormat as a complete discharge summary with: Admission Dx, Hospital Course, Discharge Dx, Discharge Meds, Follow-up Plan."
    elif doc_type == "avs":
        base += "\nFormat in plain English at an 8th-grade reading level for the patient."

    return base


def _format_patient_context(patient: dict) -> str:
    lines = []
    for key, value in patient.items():
        if value:
            lines.append(f"  {key}: {value}")
    return "\n".join(lines) if lines else "  No structured data provided."


async def _call_llm(prompt: str) -> str:
    """Call Anthropic API to generate the document."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(500, "LLM not configured on server.")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 1500,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=30.0,
        )

    if response.status_code != 200:
        raise HTTPException(502, f"LLM error: {response.text}")

    data = response.json()
    return data["content"][0]["text"]


# ---------------------------------------------------------------------------
# Run locally
# ---------------------------------------------------------------------------
# uvicorn backend:app --reload --port 8000
