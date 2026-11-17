"""
SECURITY & PRIVACY NOTICE:
This reference demonstrates programmatic prediction against a Google Cloud Vertex AI endpoint.
- External Network Transmission: Invoking predict_gemma transmits prompt payloads to Google Cloud.
- Privacy & Compliance: Verify endpoint region, project compliance, and data retention settings.
  Do NOT send confidential, proprietary, or regulated data unless authorized by organizational policy.
- Required Environment Variables:
  - GOOGLE_CLOUD_PROJECT: Target Google Cloud project ID
  - GOOGLE_CLOUD_LOCATION: Deployment region (e.g. us-central1)
  - GOOGLE_CLOUD_ENDPOINT_ID: Target Vertex AI endpoint resource ID
- Immutable Artifact Pinning: Tokenizers and local artifacts use pinned revisions with trust_remote_code=False.
"""

import os
from typing import Optional, List, Dict
from transformers import AutoTokenizer

# Target model identifier and immutable commit revision for tokenizer verification
MODEL_ID = "google/gemma-4-31B-it"
MODEL_REVISION = "7b2d51ae52dc0a905a92a548232c454e56eb6009"

def format_gemma_prompt(
    messages: List[Dict[str, str]],
    tokenizer_id: Optional[str] = None,
    revision: Optional[str] = None,
) -> str:
    """
    Applies official Gemma chat template formatting to turn messages.
    Uses immutable commit revision and trust_remote_code=False.
    """
    target = tokenizer_id or os.environ.get("GEMMA_TOKENIZER_PATH") or MODEL_ID
    target_rev = None if os.path.exists(target) else (revision or MODEL_REVISION)

    tokenizer = AutoTokenizer.from_pretrained(
        target,
        revision=target_rev,
        trust_remote_code=False,
    )
    return tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )

def predict_gemma(
    prompt: str,
    project: Optional[str] = None,
    location: Optional[str] = None,
    endpoint_id: Optional[str] = None,
    max_tokens: int = 1024,
) -> List[str]:
    """
    Submits a prediction request to a deployed Gemma 4 Vertex AI endpoint.
    Requires Google Cloud authentication (gcloud auth application-default login or Service Account).
    """
    try:
        from google.cloud import aiplatform
    except ImportError:
        raise ImportError("google-cloud-aiplatform is required for Vertex AI deployment. Run: pip install google-cloud-aiplatform")

    project = project or os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = location or os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    endpoint_id = endpoint_id or os.environ.get("GOOGLE_CLOUD_ENDPOINT_ID")

    if not project or not endpoint_id:
        raise ValueError("Missing GOOGLE_CLOUD_PROJECT or GOOGLE_CLOUD_ENDPOINT_ID environment variable.")

    aiplatform.init(project=project, location=location)
    endpoint = aiplatform.Endpoint(endpoint_id)

    instances = [{"prompt": prompt, "max_tokens": max_tokens}]
    response = endpoint.predict(instances=instances)
    return [str(pred) for pred in response.predictions]
