"""ARTCLAW AI Creative Suite — Skill Package

This package provides AI content creation capabilities via the ARTCLAW REST API,
including image generation, video generation, workflow execution,
multimodal analysis, and prompt enhancement.

REST API Base: https://artclaw.com/api/v1
Auth: API Key (starts with vk_) passed as `X-API-KEY` HTTP header
Get your key: https://artclaw.com/settings
"""

SKILL_NAME = "artclaw-creative-suite"
SKILL_VERSION = "1.1.0"
API_BASE_URL = "https://artclaw.com/api/v1"

API_CONFIG = {
    "base_url": API_BASE_URL,
    "auth_header": "X-API-KEY",
}

ENDPOINTS = {
    # Generation (async, returns job_id)
    "generate_image": ("POST", "/generate/image"),
    "generate_video": ("POST", "/generate/video"),
    "generate_marketing_image": ("POST", "/generate/marketing-image"),
    # Workflows
    "list_workflows": ("GET", "/workflows/"),
    "run_workflow": ("POST", "/workflows/{workflow_id}/run"),
    # Analysis (synchronous)
    "analyze_image": ("POST", "/analyze/image"),
    "analyze_video": ("POST", "/analyze/video"),
    "analyze_script": ("POST", "/analyze/script"),
    "analyze_characters": ("POST", "/analyze/characters"),
    # Job management
    "get_job": ("GET", "/jobs/{job_id}"),
    "list_jobs": ("GET", "/jobs/"),
    "cancel_job": ("POST", "/jobs/{job_id}/cancel"),
    # Account
    "account_info": ("GET", "/account/info"),
    # Auth
    "verify_key": ("POST", "/auth/verify"),
}


def get_api_config() -> dict:
    """Return the REST API configuration for this skill."""
    return API_CONFIG
