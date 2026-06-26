#!/usr/bin/env python3
"""
Ad Engine — Facebook Ads Deployment Skill

Reads ad messages + components from Supabase, assembles full ad copy,
and deploys to Facebook Ads Manager via the Marketing API.

Usage:
    # Preview assembled ad (no deployment)
    python3 fb_deploy.py --preview --message-id 8555

    # Preview all draft ads for a campaign
    python3 fb_deploy.py --preview --campaign-id 43

    # Deploy a single ad to Facebook
    python3 fb_deploy.py --deploy --message-id 8555 --image /path/to/image.png

    # Deploy all draft ads for a campaign
    python3 fb_deploy.py --deploy --campaign-id 43 --image-dir /path/to/images/

    # Check status of deployed ads
    python3 fb_deploy.py --status --campaign-id 43

    # Setup: store Facebook credentials
    python3 fb_deploy.py --setup
"""

import argparse
import json
import os
import sys
import time
import re

# Auto-install dependencies
def ensure_deps():
    deps = {
        "psycopg2": "psycopg2-binary",
        "facebook_business": "facebook-business",
        "requests": "requests",
    }
    for module, pkg in deps.items():
        try:
            __import__(module)
        except ImportError:
            import subprocess
            print(f"Installing {pkg}...", file=sys.stderr)
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install",
                    "--break-system-packages", "-q", pkg
                ])
            except subprocess.CalledProcessError:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", "-q", pkg
                ])

ensure_deps()

import psycopg2
import psycopg2.extras
import requests

sys.path.insert(0, os.path.join(os.path.expanduser("~/.openclaw/workspace/skills")))
from skill_base import skill_main

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

SUPABASE_DSN = os.environ.get(
    "SUPABASE_DSN",
    "postgresql://postgres.kwunhujzbnlenimppazz:YT6PuuedFlg5baAZ@aws-0-us-east-2.pooler.supabase.com:6543/postgres"
)

# Facebook credentials — set via --setup or env vars
FB_ACCESS_TOKEN = os.environ.get("FB_ACCESS_TOKEN", "")
FB_AD_ACCOUNT_ID = os.environ.get("FB_AD_ACCOUNT_ID", "")  # format: act_XXXXXXXXX
FB_PAGE_ID = os.environ.get("FB_PAGE_ID", "")

# Config file for persisted FB credentials
CONFIG_DIR = os.path.expanduser("~/.config/ad-engine")
CONFIG_FILE = os.path.join(CONFIG_DIR, "fb_config.json")

FB_API_VERSION = "v21.0"
FB_BASE_URL = f"https://graph.facebook.com/{FB_API_VERSION}"

# ---------------------------------------------------------------------------
# Config persistence
# ---------------------------------------------------------------------------

def load_config():
    """Load FB credentials from config file."""
    global FB_ACCESS_TOKEN, FB_AD_ACCOUNT_ID, FB_PAGE_ID
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            cfg = json.load(f)
        FB_ACCESS_TOKEN = FB_ACCESS_TOKEN or cfg.get("access_token", "")
        FB_AD_ACCOUNT_ID = FB_AD_ACCOUNT_ID or cfg.get("ad_account_id", "")
        FB_PAGE_ID = FB_PAGE_ID or cfg.get("page_id", "")


def save_config(access_token, ad_account_id, page_id):
    """Save FB credentials to config file."""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump({
            "access_token": access_token,
            "ad_account_id": ad_account_id,
            "page_id": page_id,
        }, f, indent=2)
    os.chmod(CONFIG_FILE, 0o600)
    print(f"Config saved to {CONFIG_FILE}")


def setup_credentials():
    """Interactive setup for Facebook credentials."""
    print("\n=== Ad Engine — Facebook Setup ===\n")
    print("You need 3 things from Facebook Business Manager:\n")
    print("1. ACCESS TOKEN  — From developers.facebook.com → your app → Marketing API")
    print("   Generate a long-lived token with ads_management permission")
    print("   Docs: https://developers.facebook.com/docs/marketing-api/overview/authorization\n")
    print("2. AD ACCOUNT ID — From Business Manager → Ad Accounts")
    print("   Format: act_XXXXXXXXXX (include the 'act_' prefix)\n")
    print("3. PAGE ID       — From your Facebook Page → About → Page ID")
    print("   This is the page the ads will run from\n")

    token = input("Access Token: ").strip()
    account = input("Ad Account ID (act_XXX): ").strip()
    page = input("Page ID: ").strip()

    if not account.startswith("act_"):
        account = f"act_{account}"

    # Validate token
    print("\nValidating credentials...", file=sys.stderr)
    resp = requests.get(f"{FB_BASE_URL}/{account}", params={
        "access_token": token,
        "fields": "name,account_status,currency"
    })

    if resp.status_code == 200:
        data = resp.json()
        print(f"\n  Ad Account: {data.get('name', 'Unknown')}")
        print(f"  Currency: {data.get('currency', 'Unknown')}")
        status_map = {1: "ACTIVE", 2: "DISABLED", 3: "UNSETTLED", 7: "PENDING_RISK_REVIEW"}
        print(f"  Status: {status_map.get(data.get('account_status'), 'Unknown')}")
        save_config(token, account, page)
        print("\n  Setup complete. You can now deploy ads.")
    else:
        print(f"\n  ERROR: {resp.json().get('error', {}).get('message', resp.text)}")
        print("  Check your token and account ID.")
        save_it = input("\n  Save anyway? (y/n): ").strip().lower()
        if save_it == "y":
            save_config(token, account, page)


# ---------------------------------------------------------------------------
# Supabase / Database
# ---------------------------------------------------------------------------

def get_db():
    """Get a Supabase Postgres connection."""
    return psycopg2.connect(SUPABASE_DSN)


def get_message(message_id):
    """Fetch a single message by ID."""
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM messages WHERE id = %s", (message_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def get_campaign_ads(campaign_id, status="draft"):
    """Get all fb_ad messages for a campaign."""
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT * FROM messages
        WHERE campaign_id = %s AND content_type = 'fb_ad' AND status = %s
        ORDER BY seq, variation_num NULLS FIRST
    """, (campaign_id, status))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_components(campaign_id):
    """Get all ad_components for a campaign, keyed by component_key."""
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT * FROM ad_components
        WHERE campaign_id = %s AND active = true
    """, (campaign_id,))
    rows = cur.fetchall()
    conn.close()
    return {r["component_key"]: dict(r) for r in rows}


def get_framework(framework_id):
    """Get a framework template."""
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM frameworks WHERE id = %s", (framework_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def update_message_status(message_id, status, fb_data=None):
    """Update message status and store FB IDs."""
    conn = get_db()
    cur = conn.cursor()
    if fb_data:
        # Merge fb_data into extra_data
        cur.execute("SELECT extra_data FROM messages WHERE id = %s", (message_id,))
        row = cur.fetchone()
        existing = json.loads(row[0]) if row and row[0] else {}
        existing["fb"] = fb_data
        cur.execute(
            "UPDATE messages SET status = %s, extra_data = %s WHERE id = %s",
            (status, json.dumps(existing), message_id)
        )
    else:
        cur.execute("UPDATE messages SET status = %s WHERE id = %s", (status, message_id))
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Ad Assembly
# ---------------------------------------------------------------------------

def assemble_ad(message, components, framework=None):
    """Assemble a complete ad from message + components.

    Returns dict with: primary_text, headline, description, cta_button,
                       creative_direction, targeting, budget, ad_name, etc.
    """
    extra = json.loads(message["extra_data"]) if message.get("extra_data") else {}
    comp_refs = extra.get("components", {})

    # Resolve component keys to actual text
    resolved = {}
    for slot, key in comp_refs.items():
        if key in components:
            resolved[slot] = components[key]["text"]
        else:
            resolved[slot] = f"[MISSING: {key}]"

    # Assemble primary text using framework template
    if framework and framework.get("script_template"):
        template = framework["script_template"]
        primary_text = template
        for tag, text in resolved.items():
            primary_text = primary_text.replace(f"{{{{{tag}}}}}", text)
        # Remove any unresolved merge tags
        primary_text = re.sub(r'\{\{[^}]+\}\}', '', primary_text)
        # Clean up extra blank lines
        primary_text = re.sub(r'\n{3,}', '\n\n', primary_text).strip()
    else:
        # Fallback: concatenate in logical order
        parts = []
        for slot in ["hook", "pain", "solution", "differentiator", "guarantee", "cta_text"]:
            if slot in resolved:
                parts.append(resolved[slot])
        primary_text = "\n\n".join(parts)

    ad_name = extra.get("ad_name") or extra.get("variant_name") or f"Ad {message['id']}"
    variant_info = f"-v{message.get('variation_num', 1)}" if message.get("variation_num") else "-v1"
    parent = message.get("parent_id") or message["id"]

    # Build naming convention
    hook_short = comp_refs.get("hook", "no_hook")[:20]
    creative_short = comp_refs.get("creative", "no_cr")[:25]
    copy_len = "short" if message.get("framework_id") == 47 else ("dm" if message.get("framework_id") == 48 else "long")

    fb_ad_name = f"CA{message['campaign_id']} | {parent}{variant_info} | {hook_short} | {creative_short} | {copy_len}"

    return {
        "message_id": message["id"],
        "parent_id": message.get("parent_id"),
        "variation_num": message.get("variation_num"),
        "campaign_id": message["campaign_id"],
        "ad_name": ad_name,
        "fb_ad_name": fb_ad_name,
        "primary_text": primary_text,
        "headline": resolved.get("headline", ""),
        "description": resolved.get("description", ""),
        "cta_button": resolved.get("cta_button", "LEARN_MORE"),
        "creative_direction": resolved.get("creative", ""),
        "targeting": extra.get("targeting", {}),
        "budget": extra.get("budget", {}),
        "ad_angle": extra.get("ad_angle", ""),
        "launch_priority": extra.get("launch_priority", ""),
        "test_variable": extra.get("test_variable", ""),
        "components": comp_refs,
    }


# ---------------------------------------------------------------------------
# Facebook Marketing API
# ---------------------------------------------------------------------------

def fb_request(method, endpoint, params=None, data=None, files=None):
    """Make a Facebook Graph API request."""
    url = f"{FB_BASE_URL}/{endpoint}"
    if params is None:
        params = {}
    params["access_token"] = FB_ACCESS_TOKEN

    if method == "GET":
        resp = requests.get(url, params=params, timeout=30)
    elif method == "POST":
        if files:
            resp = requests.post(url, params=params, data=data, files=files, timeout=60)
        else:
            resp = requests.post(url, params=params, json=data, timeout=30)
    else:
        raise ValueError(f"Unsupported method: {method}")

    if resp.status_code in (200, 201):
        return resp.json()
    else:
        error = resp.json().get("error", {})
        raise Exception(f"FB API Error ({resp.status_code}): {error.get('message', resp.text)}")


def fb_create_campaign(name, objective="OUTCOME_LEADS", status="PAUSED"):
    """Create a Facebook campaign."""
    data = {
        "name": name,
        "objective": objective,
        "status": status,
        "special_ad_categories": "[]",
    }
    result = fb_request("POST", f"{FB_AD_ACCOUNT_ID}/campaigns", data=data)
    return result["id"]


def fb_create_adset(campaign_id, name, daily_budget, targeting, objective_type="leads",
                    optimization="LEAD_GENERATION", status="PAUSED"):
    """Create a Facebook ad set."""
    # Build targeting spec
    target_spec = {
        "age_min": 25,
        "age_max": 55,
    }

    # Geo
    geo = targeting.get("geo", ["US"])
    if isinstance(geo, list):
        target_spec["geo_locations"] = {"countries": [g.strip() for g in geo]}
    elif isinstance(geo, str):
        target_spec["geo_locations"] = {"countries": [geo]}

    # Interests (simplified — FB needs interest IDs, but we can search for them)
    interests = targeting.get("interests", [])
    if interests:
        # For now, use flexible_spec with interest names
        # In production, you'd resolve these to interest IDs via the targeting search API
        target_spec["flexible_spec"] = [{"interests": [{"name": i} for i in interests[:10]]}]

    # Optimization goal mapping
    opt_map = {
        "leads": "LEAD_GENERATION",
        "messages": "CONVERSATIONS",
        "conversions": "OFFSITE_CONVERSIONS",
        "link_clicks": "LINK_CLICKS",
    }

    data = {
        "campaign_id": campaign_id,
        "name": name,
        "daily_budget": int(daily_budget * 100),  # cents
        "billing_event": "IMPRESSIONS",
        "optimization_goal": opt_map.get(objective_type, optimization),
        "targeting": json.dumps(target_spec),
        "status": status,
    }

    result = fb_request("POST", f"{FB_AD_ACCOUNT_ID}/adsets", data=data)
    return result["id"]


def fb_upload_image(image_path):
    """Upload an image to the ad account and return the image hash."""
    with open(image_path, "rb") as f:
        result = fb_request("POST", f"{FB_AD_ACCOUNT_ID}/adimages",
                          files={"filename": f})

    # Response: {"images": {"filename": {"hash": "xxx", "url": "..."}}}
    images = result.get("images", {})
    for key, val in images.items():
        return val.get("hash", "")
    raise Exception(f"Failed to upload image: {result}")


def fb_create_creative(name, primary_text, headline, description, link,
                       image_hash, cta_type="LEARN_MORE"):
    """Create an ad creative."""
    cta_map = {
        "BOOK_NOW": "BOOK_TRAVEL",  # FB uses BOOK_TRAVEL for general booking
        "LEARN_MORE": "LEARN_MORE",
        "SEND_MESSAGE": "MESSAGE_PAGE",
        "SIGN_UP": "SIGN_UP",
        "CONTACT_US": "CONTACT_US",
        "GET_QUOTE": "GET_QUOTE",
    }

    link_data = {
        "message": primary_text,
        "link": link,
        "name": headline,
        "description": description,
        "image_hash": image_hash,
        "call_to_action": {"type": cta_map.get(cta_type, "LEARN_MORE")},
    }

    data = {
        "name": name,
        "object_story_spec": json.dumps({
            "page_id": FB_PAGE_ID,
            "link_data": link_data,
        }),
    }

    result = fb_request("POST", f"{FB_AD_ACCOUNT_ID}/adcreatives", data=data)
    return result["id"]


def fb_create_ad(adset_id, creative_id, name, status="PAUSED"):
    """Create an ad linking creative to ad set."""
    data = {
        "adset_id": adset_id,
        "creative": json.dumps({"creative_id": creative_id}),
        "name": name,
        "status": status,
    }
    result = fb_request("POST", f"{FB_AD_ACCOUNT_ID}/ads", data=data)
    return result["id"]


# ---------------------------------------------------------------------------
# Deployment orchestration
# ---------------------------------------------------------------------------

def deploy_ad(assembled_ad, image_path, landing_url, campaign_fb_id=None,
              adset_fb_id=None, objective_type="leads", dry_run=False):
    """Deploy a single assembled ad to Facebook.

    Returns dict with all created FB IDs.
    """
    ad = assembled_ad
    print(f"\n--- Deploying: {ad['ad_name']} ---")
    print(f"  Message ID: {ad['message_id']}")
    print(f"  FB Ad Name: {ad['fb_ad_name']}")

    if dry_run:
        print("  [DRY RUN] Would create campaign, ad set, creative, and ad.")
        return {"dry_run": True}

    fb_ids = {}

    # 1. Create campaign if not provided
    if not campaign_fb_id:
        angle = ad.get("ad_angle", "general")
        obj = "OUTCOME_LEADS" if objective_type == "leads" else "OUTCOME_ENGAGEMENT"
        camp_name = f"CA{ad['campaign_id']} | ABO | Testing | {'Leads' if objective_type == 'leads' else 'Messages'} | Cold"
        print(f"  Creating campaign: {camp_name}")
        campaign_fb_id = fb_create_campaign(camp_name, obj)
        fb_ids["campaign_id"] = campaign_fb_id
        print(f"  Campaign ID: {campaign_fb_id}")

    # 2. Create ad set if not provided
    if not adset_fb_id:
        budget = ad.get("budget", {})
        daily = budget.get("daily_start", 5)
        targeting = ad.get("targeting", {})
        angle = ad.get("ad_angle", "general").replace("_", " ").title()
        geo = targeting.get("geo", ["US"])
        geo_str = "-".join(geo) if isinstance(geo, list) else geo

        adset_name = f"CA{ad['campaign_id']} | {angle} | Cold | {geo_str}"
        print(f"  Creating ad set: {adset_name} (${daily}/day)")
        adset_fb_id = fb_create_adset(
            campaign_fb_id, adset_name, daily, targeting, objective_type
        )
        fb_ids["adset_id"] = adset_fb_id
        print(f"  Ad Set ID: {adset_fb_id}")

    # 3. Upload image
    print(f"  Uploading image: {image_path}")
    image_hash = fb_upload_image(image_path)
    fb_ids["image_hash"] = image_hash
    print(f"  Image Hash: {image_hash}")

    # 4. Create creative
    print(f"  Creating creative...")
    creative_id = fb_create_creative(
        name=ad["fb_ad_name"],
        primary_text=ad["primary_text"],
        headline=ad["headline"],
        description=ad["description"],
        link=landing_url,
        image_hash=image_hash,
        cta_type=ad["cta_button"],
    )
    fb_ids["creative_id"] = creative_id
    print(f"  Creative ID: {creative_id}")

    # 5. Create ad
    print(f"  Creating ad...")
    ad_id = fb_create_ad(adset_fb_id, creative_id, ad["fb_ad_name"])
    fb_ids["ad_id"] = ad_id
    print(f"  Ad ID: {ad_id}")

    # 6. Update database
    update_message_status(ad["message_id"], "deployed", fb_ids)
    print(f"  Status updated to 'deployed'")

    return fb_ids


def deploy_campaign_ads(campaign_id, image_dir, landing_url, objective_type="leads", dry_run=False):
    """Deploy all draft ads for a campaign.

    Groups ads by angle → creates one campaign + ad set per angle → multiple ads per set.
    """
    messages = get_campaign_ads(campaign_id, status="draft")
    if not messages:
        print(f"No draft fb_ad messages found for campaign {campaign_id}")
        return

    components = get_components(campaign_id)
    print(f"\nFound {len(messages)} draft ads, {len(components)} components")

    # Group by ad_angle
    by_angle = {}
    for msg in messages:
        extra = json.loads(msg["extra_data"]) if msg.get("extra_data") else {}
        angle = extra.get("ad_angle", "general")
        by_angle.setdefault(angle, []).append(msg)

    # Map image files by angle
    image_map = {}
    if image_dir and os.path.isdir(image_dir):
        for f in os.listdir(image_dir):
            if f.endswith((".png", ".jpg", ".jpeg")):
                # Match by angle name in filename
                for angle in by_angle:
                    if angle.replace("_", "-") in f or angle in f:
                        image_map.setdefault(angle, []).append(os.path.join(image_dir, f))

    for angle, msgs in by_angle.items():
        print(f"\n{'='*60}")
        print(f"ANGLE: {angle} ({len(msgs)} ads)")
        print(f"{'='*60}")

        campaign_fb_id = None
        adset_fb_id = None

        for i, msg in enumerate(msgs):
            framework = get_framework(msg["framework_id"]) if msg.get("framework_id") else None
            assembled = assemble_ad(msg, components, framework)

            # Find image for this ad
            images = image_map.get(angle, [])
            if images:
                # Rotate through available images
                image_path = images[i % len(images)]
            else:
                print(f"  WARNING: No image found for angle '{angle}' in {image_dir}")
                print(f"  Expected filename containing: {angle.replace('_', '-')}")
                continue

            fb_ids = deploy_ad(
                assembled, image_path, landing_url,
                campaign_fb_id=campaign_fb_id,
                adset_fb_id=adset_fb_id,
                objective_type=objective_type,
                dry_run=dry_run,
            )

            # Reuse campaign and adset for subsequent ads in same angle
            if not dry_run:
                campaign_fb_id = campaign_fb_id or fb_ids.get("campaign_id")
                adset_fb_id = adset_fb_id or fb_ids.get("adset_id")


# ---------------------------------------------------------------------------
# Preview / Status
# ---------------------------------------------------------------------------

def preview_ad(message, components, framework=None):
    """Print a formatted preview of an assembled ad."""
    assembled = assemble_ad(message, components, framework)

    parent_label = f" (variant {assembled['variation_num']} of {assembled['parent_id']})" \
        if assembled.get("parent_id") else " (PARENT)"

    print(f"\n{'='*70}")
    print(f"AD: {assembled['ad_name']}{parent_label}")
    print(f"FB Name: {assembled['fb_ad_name']}")
    print(f"Message ID: {assembled['message_id']}")
    if assembled.get("test_variable"):
        print(f"Testing: {assembled['test_variable']}")
    print(f"{'='*70}")

    print(f"\n--- PRIMARY TEXT ---")
    print(assembled["primary_text"])

    print(f"\n--- HEADLINE ---")
    print(assembled["headline"])

    print(f"\n--- DESCRIPTION ---")
    print(assembled["description"])

    print(f"\n--- CTA BUTTON ---")
    print(assembled["cta_button"])

    print(f"\n--- CREATIVE DIRECTION ---")
    print(assembled["creative_direction"][:200] + "..." if len(assembled.get("creative_direction", "")) > 200 else assembled.get("creative_direction", ""))

    if assembled.get("targeting"):
        print(f"\n--- TARGETING ---")
        print(json.dumps(assembled["targeting"], indent=2))

    if assembled.get("budget"):
        print(f"\n--- BUDGET ---")
        print(json.dumps(assembled["budget"], indent=2))

    print()
    return assembled


def check_status(campaign_id):
    """Check FB status of deployed ads."""
    messages = get_campaign_ads(campaign_id, status="deployed")
    if not messages:
        print(f"No deployed ads found for campaign {campaign_id}")
        # Also check for any status
        all_msgs = get_campaign_ads(campaign_id, status="draft")
        if all_msgs:
            print(f"({len(all_msgs)} draft ads waiting to deploy)")
        return

    print(f"\n{'='*70}")
    print(f"DEPLOYED ADS — Campaign {campaign_id}")
    print(f"{'='*70}\n")

    for msg in messages:
        extra = json.loads(msg["extra_data"]) if msg.get("extra_data") else {}
        fb = extra.get("fb", {})
        name = extra.get("ad_name") or extra.get("variant_name") or f"Ad {msg['id']}"

        print(f"  {name}")
        print(f"    Message ID:  {msg['id']}")
        print(f"    FB Ad ID:    {fb.get('ad_id', 'N/A')}")
        print(f"    FB AdSet:    {fb.get('adset_id', 'N/A')}")
        print(f"    FB Campaign: {fb.get('campaign_id', 'N/A')}")

        # If we have FB credentials, fetch live metrics
        if FB_ACCESS_TOKEN and fb.get("ad_id"):
            try:
                result = fb_request("GET", fb["ad_id"], params={
                    "fields": "effective_status,insights{impressions,clicks,ctr,cpc,spend}"
                })
                print(f"    Status:      {result.get('effective_status', 'Unknown')}")
                insights = result.get("insights", {}).get("data", [{}])[0]
                if insights:
                    print(f"    Impressions: {insights.get('impressions', 0)}")
                    print(f"    Clicks:      {insights.get('clicks', 0)}")
                    print(f"    CTR:         {insights.get('ctr', '0')}%")
                    print(f"    CPC:         ${insights.get('cpc', '0')}")
                    print(f"    Spend:       ${insights.get('spend', '0')}")
            except Exception as e:
                print(f"    (Could not fetch live metrics: {e})")
        print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

@skill_main
def main():
    parser = argparse.ArgumentParser(description="Ad Engine — Facebook Ads Deployment")

    # Actions
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--preview", action="store_true", help="Preview assembled ads (no deployment)")
    group.add_argument("--deploy", action="store_true", help="Deploy ads to Facebook")
    group.add_argument("--status", action="store_true", help="Check status of deployed ads")
    group.add_argument("--setup", action="store_true", help="Configure Facebook credentials")

    # Targeting
    parser.add_argument("--message-id", "-m", type=int, help="Deploy specific message ID")
    parser.add_argument("--campaign-id", "-c", type=int, help="Deploy all draft ads for campaign")

    # Deployment options
    parser.add_argument("--image", "-i", type=str, help="Image file path (for single ad)")
    parser.add_argument("--image-dir", type=str, help="Directory of images (for campaign deploy)")
    parser.add_argument("--landing-url", "-u", type=str, default="", help="Landing/booking page URL")
    parser.add_argument("--objective", type=str, default="leads",
                       choices=["leads", "messages", "link_clicks"],
                       help="Campaign objective (default: leads)")
    parser.add_argument("--dry-run", action="store_true", help="Preview what would be created without deploying")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    # Load saved config
    load_config()

    # Setup mode
    if args.setup:
        setup_credentials()
        return

    # Status check
    if args.status:
        if not args.campaign_id:
            print("ERROR: --campaign-id required for status check", file=sys.stderr)
            sys.exit(1)
        check_status(args.campaign_id)
        return

    # Need at least one target
    if not args.message_id and not args.campaign_id:
        print("ERROR: Provide --message-id or --campaign-id", file=sys.stderr)
        sys.exit(1)

    # Preview mode
    if args.preview:
        if args.message_id:
            msg = get_message(args.message_id)
            if not msg:
                print(f"Message {args.message_id} not found", file=sys.stderr)
                sys.exit(1)
            components = get_components(msg["campaign_id"])
            framework = get_framework(msg["framework_id"]) if msg.get("framework_id") else None
            result = preview_ad(msg, components, framework)
            if args.json:
                print(json.dumps(result, indent=2, default=str))
        else:
            messages = get_campaign_ads(args.campaign_id, status="draft")
            if not messages:
                print(f"No draft ads for campaign {args.campaign_id}")
                sys.exit(1)
            components = get_components(args.campaign_id)
            all_assembled = []
            for msg in messages:
                framework = get_framework(msg["framework_id"]) if msg.get("framework_id") else None
                result = preview_ad(msg, components, framework)
                all_assembled.append(result)
            if args.json:
                print(json.dumps(all_assembled, indent=2, default=str))
        return

    # Deploy mode
    if args.deploy:
        if not FB_ACCESS_TOKEN:
            print("ERROR: Facebook credentials not configured. Run: --setup", file=sys.stderr)
            sys.exit(1)

        if not args.landing_url:
            print("ERROR: --landing-url required for deployment", file=sys.stderr)
            sys.exit(1)

        if args.message_id:
            # Single ad deploy
            if not args.image:
                print("ERROR: --image required for single ad deployment", file=sys.stderr)
                sys.exit(1)

            msg = get_message(args.message_id)
            if not msg:
                print(f"Message {args.message_id} not found", file=sys.stderr)
                sys.exit(1)

            components = get_components(msg["campaign_id"])
            framework = get_framework(msg["framework_id"]) if msg.get("framework_id") else None
            assembled = assemble_ad(msg, components, framework)

            fb_ids = deploy_ad(
                assembled, args.image, args.landing_url,
                objective_type=args.objective,
                dry_run=args.dry_run,
            )

            if args.json:
                print(json.dumps(fb_ids, indent=2, default=str))

        else:
            # Campaign deploy
            if not args.image_dir:
                print("ERROR: --image-dir required for campaign deployment", file=sys.stderr)
                sys.exit(1)

            deploy_campaign_ads(
                args.campaign_id, args.image_dir, args.landing_url,
                objective_type=args.objective,
                dry_run=args.dry_run,
            )


if __name__ == "__main__":
    main()
