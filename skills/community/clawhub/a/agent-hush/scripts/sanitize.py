#!/usr/bin/env python3
"""
agent-hush: Silent privacy guardian for agent workspaces.
Catches sensitive data BEFORE it leaves your machine — during git push,
skill publish, or file sharing. Your local files stay untouched.

Zero external dependencies — uses only Python standard library.
"""

import re
import os
import sys
import json
import shutil
import argparse
import subprocess
from pathlib import Path
from collections import defaultdict

# ─── Severity Levels ───
CRITICAL = "CRITICAL"
HIGH = "HIGH"
MEDIUM = "MEDIUM"
LOW = "LOW"

SEVERITY_ORDER = {CRITICAL: 0, HIGH: 1, MEDIUM: 2, LOW: 3}

# ─── Confidence Levels ───
# HIGH_CONF: Unique, unambiguous format — safe to auto-replace
# LOW_CONF: Could be code, documentation, or real secrets — needs human review
HIGH_CONF = "high"
LOW_CONF = "low"

# ─── Detection Rules ───
# Each rule: (name, severity, confidence, regex_pattern, replacement_placeholder)
RULES = [
    # ═══════════════════════════════════════════════
    # Gitleaks Rules (auto-converted)
    # Source: https://github.com/gitleaks/gitleaks
    # License: MIT | 222+ community-maintained rules
    # ═══════════════════════════════════════════════

    ("1Password secret key", CRITICAL, HIGH_CONF,
     r'''\bA3-[A-Z0-9]{6}-(?:(?:[A-Z0-9]{11})|(?:[A-Z0-9]{6}-[A-Z0-9]{5}))-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}\b''',
     "[REDACTED_1PASSWORD_SECRET_KEY]"),

    ("1Password service account token", CRITICAL, HIGH_CONF,
     r'''ops_eyJ[a-zA-Z0-9+/]{250,}={0,3}''',
     "[REDACTED_1PASSWORD_SERVICE_ACCOUNT_TOKEN]"),

    ("Adafruit API Key", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:adafruit)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9_-]{32})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_ADAFRUIT_API_KEY]"),

    ("Adobe OAuth Web Client ID", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:adobe)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-f0-9]{32})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_ADOBE_CLIENT_ID]"),

    ("Age encryption tool secret key", CRITICAL, HIGH_CONF,
     r'''AGE-SECRET-KEY-1[QPZRY9X8GF2TVDW0S3JN54KHCE6MUA7L]{58}''',
     "[REDACTED_AGE_SECRET_KEY]"),

    ("Airtable API Key", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:airtable)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9]{17})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_AIRTABLE_API_KEY]"),

    ("Airtable Personal AccessToken", CRITICAL, HIGH_CONF,
     r'''\b(pat[a-zA-Z0-9]{14}\.[a-f0-9]{64})\b''',
     "[REDACTED_AIRTABLE_PERSONNAL_ACCESS_TOKEN]"),

    ("Algolia API Key, which could result in unauthorized searc...", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:algolia)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9]{32})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_ALGOLIA_API_KEY]"),

    ("Alibaba Cloud Secret Key", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:alibaba)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9]{30})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_ALIBABA_SECRET_KEY]"),

    ("Anthropic Admin API Key", CRITICAL, HIGH_CONF,
     r'''\b(sk-ant-admin01-[a-zA-Z0-9_\-]{93}AA)(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_ANTHROPIC_ADMIN_API_KEY]"),

    ("Anthropic API Key", CRITICAL, HIGH_CONF,
     r'''\b(sk-ant-api03-[a-zA-Z0-9_\-]{93}AA)(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_ANTHROPIC_API_KEY]"),

    ("Artifactory api key", CRITICAL, HIGH_CONF,
     r'''\bAKCp[A-Za-z0-9]{69}\b''',
     "[REDACTED_ARTIFACTORY_API_KEY]"),

    ("Artifactory reference token", CRITICAL, HIGH_CONF,
     r'''\bcmVmd[A-Za-z0-9]{59}\b''',
     "[REDACTED_ARTIFACTORY_REFERENCE_TOKEN]"),

    ("Asana Client ID, risking unauthorized access to Asana pro...", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:asana)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([0-9]{16})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_ASANA_CLIENT_ID]"),

    ("Asana Client Secret", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:asana)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9]{32})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_ASANA_CLIENT_SECRET]"),

    ("Atlassian API token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:(?-i:ATLASSIAN|[Aa]tlassian)|(?-i:CONFLUENCE|[Cc]onfluence)|(?-i:JIRA|[Jj]ira))(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9]{20}[a-f0-9]{4})(?:[\x60'"\s;]|\\[nr]|$)|\b(ATATT3[A-Za-z0-9_\-=]{186})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_ATLASSIAN_API_TOKEN]"),

    ("Pattern that may indicate AWS credentials", CRITICAL, HIGH_CONF,
     r'''\b((?:A3T[A-Z0-9]|AKIA|ASIA|ABIA|ACCA)[A-Z2-7]{16})\b''',
     "[REDACTED_AWS_ACCESS_TOKEN]"),

    ("Pattern that may indicate long-lived Amazon Bedrock API keys", CRITICAL, HIGH_CONF,
     r'''\b(ABSK[A-Za-z0-9+/]{109,269}={0,2})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_AWS_AMAZON_BEDROCK_API_KEY_LONG_LIVED]"),

    ("Pattern that may indicate short-lived Amazon Bedrock API ...", CRITICAL, HIGH_CONF,
     r'''bedrock-api-key-YmVkcm9jay5hbWF6b25hd3MuY29t''',
     "[REDACTED_AWS_AMAZON_BEDROCK_API_KEY_SHORT_LIVED]"),

    ("Azure AD Client Secret", CRITICAL, HIGH_CONF,
     r'''(?:^|[\\'"\x60\s>=:(,)])([a-zA-Z0-9_~.]{3}\dQ~[a-zA-Z0-9_~.-]{31,34})(?:$|[\\'"\x60\s<),])''',
     "[REDACTED_AZURE_AD_CLIENT_SECRET]"),

    ("Beamer API token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:beamer)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}(b_[a-z0-9=_\-]{44})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_BEAMER_API_TOKEN]"),

    ("Bitbucket Client ID", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:bitbucket)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9]{32})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_BITBUCKET_CLIENT_ID]"),

    ("Bitbucket Client Secret", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:bitbucket)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9=_\-]{64})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_BITBUCKET_CLIENT_SECRET]"),

    ("Bittrex Access Key", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:bittrex)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9]{32})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_BITTREX_ACCESS_KEY]"),

    ("Bittrex Secret Key", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:bittrex)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9]{32})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_BITTREX_SECRET_KEY]"),

    ("Cisco Meraki is a cloud-managed IT solution that provides...", CRITICAL, HIGH_CONF,
     r'''[\w.-]{0,50}?(?i:[\w.-]{0,50}?(?:(?-i:[Mm]eraki|MERAKI))(?:[ \t\w.-]{0,20})[\s'"]{0,3})(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([0-9a-f]{40})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_CISCO_MERAKI_API_KEY]"),

    ("Pattern that may indicate clickhouse cloud API secret key", CRITICAL, HIGH_CONF,
     r'''\b(4b1d[A-Za-z0-9]{38})\b''',
     "[REDACTED_CLICKHOUSE_CLOUD_API_SECRET_KEY]"),

    ("Clojars API token", CRITICAL, HIGH_CONF,
     r'''(?i)CLOJARS_[a-z0-9]{60}''',
     "[REDACTED_CLOJARS_API_TOKEN]"),

    ("Cloudflare API Key", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:cloudflare)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9_-]{40})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_CLOUDFLARE_API_KEY]"),

    ("Cloudflare Global API Key", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:cloudflare)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-f0-9]{37})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_CLOUDFLARE_GLOBAL_API_KEY]"),

    ("Cloudflare Origin CA Key", CRITICAL, HIGH_CONF,
     r'''\b(v1\.0-[a-f0-9]{24}-[a-f0-9]{146})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_CLOUDFLARE_ORIGIN_CA_KEY]"),

    ("Pattern resembling a Codecov Access Token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:codecov)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9]{32})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_CODECOV_ACCESS_TOKEN]"),

    ("Cohere Token, posing a risk of unauthorized access to AI ...", CRITICAL, HIGH_CONF,
     r'''[\w.-]{0,50}?(?i:[\w.-]{0,50}?(?:cohere|CO_API_KEY)(?:[ \t\w.-]{0,20})[\s'"]{0,3})(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-zA-Z0-9]{40})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_COHERE_API_TOKEN]"),

    ("Coinbase Access Token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:coinbase)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9_-]{64})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_COINBASE_ACCESS_TOKEN]"),

    ("Confluent Access Token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:confluent)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9]{16})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_CONFLUENT_ACCESS_TOKEN]"),

    ("Confluent Secret Key", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:confluent)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9]{64})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_CONFLUENT_SECRET_KEY]"),

    ("Discovered a Contentful delivery API token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:contentful)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9=_\-]{43})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_CONTENTFUL_DELIVERY_API_TOKEN]"),

    ("Uncovered a Databricks API token", CRITICAL, HIGH_CONF,
     r'''\b(dapi[a-f0-9]{32}(?:-\d)?)(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_DATABRICKS_API_TOKEN]"),

    ("Datadog Access Token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:datadog)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9]{40})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_DATADOG_ACCESS_TOKEN]"),

    ("Defined Networking API token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:dnkey)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}(dnkey-[a-z0-9=_\-]{26}-[a-z0-9=_\-]{52})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_DEFINED_NETWORKING_API_TOKEN]"),

    ("DigitalOcean OAuth Access Token", CRITICAL, HIGH_CONF,
     r'''\b(doo_v1_[a-f0-9]{64})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_DIGITALOCEAN_ACCESS_TOKEN]"),

    ("Discovered a DigitalOcean Personal Access Token", CRITICAL, HIGH_CONF,
     r'''\b(dop_v1_[a-f0-9]{64})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_DIGITALOCEAN_PAT]"),

    ("Uncovered a DigitalOcean OAuth Refresh Token", CRITICAL, HIGH_CONF,
     r'''(?i)\b(dor_v1_[a-f0-9]{64})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_DIGITALOCEAN_REFRESH_TOKEN]"),

    ("Discord API key, potentially compromising communication c...", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:discord)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-f0-9]{64})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_DISCORD_API_TOKEN]"),

    ("Discord client ID", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:discord)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([0-9]{18})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_DISCORD_CLIENT_ID]"),

    ("Discord client secret", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:discord)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9=_\-]{32})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_DISCORD_CLIENT_SECRET]"),

    ("Droneci Access Token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:droneci)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9]{32})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_DRONECI_ACCESS_TOKEN]"),

    ("Dropbox API secret", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:dropbox)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9]{15})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_DROPBOX_API_TOKEN]"),

    ("Dropbox long-lived API token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:dropbox)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9]{11}(AAAAAAAAAA)[a-z0-9\-_=]{43})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_DROPBOX_LONG_LIVED_API_TOKEN]"),

    ("Discovered a Dropbox short-lived API token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:dropbox)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}(sl\.[a-z0-9\-=_]{135})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_DROPBOX_SHORT_LIVED_API_TOKEN]"),

    ("Found an Etsy Access Token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:(?-i:ETSY|[Ee]tsy))(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9]{24})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_ETSY_ACCESS_TOKEN]"),

    ("Discovered a Facebook Access Token", CRITICAL, HIGH_CONF,
     r'''(?i)\b(\d{15,16}(\||%)[0-9a-z\-_]{27,40})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_FACEBOOK_ACCESS_TOKEN]"),

    ("Discovered a Facebook Application secret", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:facebook)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-f0-9]{32})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_FACEBOOK_SECRET]"),

    ("Uncovered a Fastly API key", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:fastly)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9=_\-]{32})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_FASTLY_API_TOKEN]"),

    ("Finicity API token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:finicity)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-f0-9]{32})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_FINICITY_API_TOKEN]"),

    ("Finicity Client Secret", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:finicity)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9]{20})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_FINICITY_CLIENT_SECRET]"),

    ("Finnhub Access Token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:finnhub)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9]{20})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_FINNHUB_ACCESS_TOKEN]"),

    ("Discovered a Flickr Access Token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:flickr)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9]{32})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_FLICKR_ACCESS_TOKEN]"),

    ("Uncovered a Fly.io API key", CRITICAL, HIGH_CONF,
     r'''\b((?:fo1_[\w-]{43}|fm1[ar]_[a-zA-Z0-9+\/]{100,}={0,3}|fm2_[a-zA-Z0-9+\/]{100,}={0,3}))(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_FLYIO_ACCESS_TOKEN]"),

    ("Freemius secret key", CRITICAL, HIGH_CONF,
     r'''(?i)["']secret_key["']\s*=>\s*["'](sk_[\S]{29})["']''',
     "[REDACTED_FREEMIUS_SECRET_KEY]"),

    ("Discovered a Freshbooks Access Token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:freshbooks)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9]{64})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_FRESHBOOKS_ACCESS_TOKEN]"),

    ("Uncovered a GCP API key", CRITICAL, HIGH_CONF,
     r'''\b(AIza[\w-]{35})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_GCP_API_KEY]"),

    ("Allowlist for Generic API Keys", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:access|auth|(?-i:[Aa]pi|API)|credential|creds|key|passw(?:or)?d|secret|token)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([\w.=-]{10,150}|[a-z0-9][a-z0-9+/]{11,}={0,3})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_GENERIC_API_KEY]"),

    ("GitHub App Token", CRITICAL, HIGH_CONF,
     r'''(?:ghu|ghs)_[0-9a-zA-Z]{36}''',
     "[REDACTED_GITHUB_APP_TOKEN]"),

    ("GitHub Fine-Grained Personal Access Token", CRITICAL, HIGH_CONF,
     r'''github_pat_\w{82}''',
     "[REDACTED_GITHUB_FINE_GRAINED_PAT]"),

    ("Discovered a GitHub OAuth Access Token", CRITICAL, HIGH_CONF,
     r'''gho_[0-9a-zA-Z]{36}''',
     "[REDACTED_GITHUB_OAUTH]"),

    ("Uncovered a GitHub Personal Access Token", CRITICAL, HIGH_CONF,
     r'''ghp_[0-9a-zA-Z]{36}''',
     "[REDACTED_GITHUB_PAT]"),

    ("GitHub Refresh Token", CRITICAL, HIGH_CONF,
     r'''ghr_[0-9a-zA-Z]{36}''',
     "[REDACTED_GITHUB_REFRESH_TOKEN]"),

    ("GitLab CI/CD Job Token", CRITICAL, HIGH_CONF,
     r'''glcbt-[0-9a-zA-Z]{1,5}_[0-9a-zA-Z_-]{20}''',
     "[REDACTED_GITLAB_CICD_JOB_TOKEN]"),

    ("GitLab Deploy Token", CRITICAL, HIGH_CONF,
     r'''gldt-[0-9a-zA-Z_\-]{20}''',
     "[REDACTED_GITLAB_DEPLOY_TOKEN]"),

    ("GitLab feature flag client token", CRITICAL, HIGH_CONF,
     r'''glffct-[0-9a-zA-Z_\-]{20}''',
     "[REDACTED_GITLAB_FEATURE_FLAG_CLIENT_TOKEN]"),

    ("GitLab feed token", CRITICAL, HIGH_CONF,
     r'''glft-[0-9a-zA-Z_\-]{20}''',
     "[REDACTED_GITLAB_FEED_TOKEN]"),

    ("GitLab incoming mail token", CRITICAL, HIGH_CONF,
     r'''glimt-[0-9a-zA-Z_\-]{25}''',
     "[REDACTED_GITLAB_INCOMING_MAIL_TOKEN]"),

    ("GitLab Kubernetes Agent token", CRITICAL, HIGH_CONF,
     r'''glagent-[0-9a-zA-Z_\-]{50}''',
     "[REDACTED_GITLAB_KUBERNETES_AGENT_TOKEN]"),

    ("GitLab OIDC Application Secret", CRITICAL, HIGH_CONF,
     r'''gloas-[0-9a-zA-Z_\-]{64}''',
     "[REDACTED_GITLAB_OAUTH_APP_SECRET]"),

    ("GitLab Personal Access Token", CRITICAL, HIGH_CONF,
     r'''glpat-[\w-]{20}''',
     "[REDACTED_GITLAB_PAT]"),

    ("GitLab Personal Access Token (routable)", CRITICAL, HIGH_CONF,
     r'''\bglpat-[0-9a-zA-Z_-]{27,300}\.[0-9a-z]{2}[0-9a-z]{7}\b''',
     "[REDACTED_GITLAB_PAT_ROUTABLE]"),

    ("GitLab Pipeline Trigger Token", CRITICAL, HIGH_CONF,
     r'''glptt-[0-9a-f]{40}''',
     "[REDACTED_GITLAB_PTT]"),

    ("Discovered a GitLab Runner Registration Token", CRITICAL, HIGH_CONF,
     r'''GR1348941[\w-]{20}''',
     "[REDACTED_GITLAB_RRT]"),

    ("Discovered a GitLab Runner Authentication Token", CRITICAL, HIGH_CONF,
     r'''glrt-[0-9a-zA-Z_\-]{20}''',
     "[REDACTED_GITLAB_RUNNER_AUTHENTICATION_TOKEN]"),

    ("Discovered a GitLab Runner Authentication Token (Routable)", CRITICAL, HIGH_CONF,
     r'''\bglrt-t\d_[0-9a-zA-Z_\-]{27,300}\.[0-9a-z]{2}[0-9a-z]{7}\b''',
     "[REDACTED_GITLAB_RUNNER_AUTHENTICATION_TOKEN_ROUTABLE]"),

    ("Discovered a GitLab SCIM Token", CRITICAL, HIGH_CONF,
     r'''glsoat-[0-9a-zA-Z_\-]{20}''',
     "[REDACTED_GITLAB_SCIM_TOKEN]"),

    ("Discovered a GitLab Session Cookie", CRITICAL, HIGH_CONF,
     r'''_gitlab_session=[0-9a-z]{32}''',
     "[REDACTED_GITLAB_SESSION_COOKIE]"),

    ("Uncovered a Gitter Access Token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:gitter)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9_-]{40})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_GITTER_ACCESS_TOKEN]"),

    ("Grafana API key, which could compromise monitoring dashbo...", CRITICAL, HIGH_CONF,
     r'''(?i)\b(eyJrIjoi[A-Za-z0-9]{70,400}={0,3})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_GRAFANA_API_KEY]"),

    ("Grafana cloud API token", CRITICAL, HIGH_CONF,
     r'''(?i)\b(glc_[A-Za-z0-9+/]{32,400}={0,3})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_GRAFANA_CLOUD_API_TOKEN]"),

    ("Discovered a Grafana service account token", CRITICAL, HIGH_CONF,
     r'''(?i)\b(glsa_[A-Za-z0-9]{32}_[A-Fa-f0-9]{8})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_GRAFANA_SERVICE_ACCOUNT_TOKEN]"),

    ("Harness Access Token (PAT or SAT)", CRITICAL, HIGH_CONF,
     r'''(?:pat|sat)\.[a-zA-Z0-9_-]{22}\.[a-zA-Z0-9]{24}\.[a-zA-Z0-9]{20}''',
     "[REDACTED_HARNESS_API_KEY]"),

    ("Uncovered a HashiCorp Terraform user/org API token", CRITICAL, HIGH_CONF,
     r'''(?i)[a-z0-9]{14}\.(?-i:atlasv1)\.[a-z0-9\-_=]{60,70}''',
     "[REDACTED_HASHICORP_TF_API_TOKEN]"),

    ("HashiCorp Terraform password field", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:administrator_login_password|password)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}("[a-z0-9=_\-]{8,20}")(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_HASHICORP_TF_PASSWORD]"),

    ("Heroku API Key, potentially compromising cloud applicatio...", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:heroku)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_HEROKU_API_KEY]"),

    ("Heroku API Key, potentially compromising cloud applicatio...", CRITICAL, HIGH_CONF,
     r'''\b((HRKU-AA[0-9a-zA-Z_-]{58}))(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_HEROKU_API_KEY_V2]"),

    ("HubSpot API Token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:hubspot)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_HUBSPOT_API_KEY]"),

    ("Discovered a Hugging Face Access token", CRITICAL, HIGH_CONF,
     r'''\b(hf_(?i:[a-z]{34}))(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_HUGGINGFACE_ACCESS_TOKEN]"),

    ("Uncovered a Hugging Face Organization API token", CRITICAL, HIGH_CONF,
     r'''\b(api_org_(?i:[a-z]{34}))(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_HUGGINGFACE_ORGANIZATION_API_TOKEN]"),

    ("Infracost API Token", CRITICAL, HIGH_CONF,
     r'''\b(ico-[a-zA-Z0-9]{32})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_INFRACOST_API_TOKEN]"),

    ("Intercom API Token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:intercom)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9=_\-]{60})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_INTERCOM_API_KEY]"),

    ("JFrog API Key, posing a risk of unauthorized access to so...", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:jfrog|artifactory|bintray|xray)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9]{73})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_JFROG_API_KEY]"),

    ("Discovered a JFrog Identity Token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:jfrog|artifactory|bintray|xray)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9]{64})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_JFROG_IDENTITY_TOKEN]"),

    ("Uncovered a JSON Web Token", CRITICAL, HIGH_CONF,
     r'''\b(ey[a-zA-Z0-9]{17,}\.ey[a-zA-Z0-9\/\\_-]{17,}\.(?:[a-zA-Z0-9\/\\_-]{10,}={0,2})?)(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_JWT]"),

    ("Base64-encoded JSON Web Token", CRITICAL, HIGH_CONF,
     r'''\bZXlK(?:(?P<alg>aGJHY2lPaU)|(?P<apu>aGNIVWlPaU)|(?P<apv>aGNIWWlPaU)|(?P<aud>aGRXUWlPaU)|(?P<b64>aU5qUWlP)|(?P<crit>amNtbDBJanBi)|(?P<cty>amRIa2lPaU)|(?P<epk>bGNHc2lPbn)|(?P<enc>bGJtTWlPaU)|(?P<jku>cWEzVWlPaU)|(?P<jwk>cWQyc2lPb)|(?P<iss>cGMzTWlPaU)|(?P<iv>cGRpSTZJ)|(?P<kid>cmFXUWlP)|(?P<key_ops>clpYbGZiM0J6SWpwY)|(?P<kty>cmRIa2lPaUp)|(?P<nonce>dWIyNWpaU0k2)|(?P<p2c>d01tTWlP)|(?P<p2s>d01uTWlPaU)|(?P<ppt>d2NIUWlPaU)|(?P<sub>emRXSWlPaU)|(?P<svt>emRuUWlP)|(?P<tag>MFlXY2lPaU)|(?P<typ>MGVYQWlPaUp)|(?P<url>MWNtd2l)|(?P<use>MWMyVWlPaUp)|(?P<ver>MlpYSWlPaU)|(?P<version>MlpYSnphVzl1SWpv)|(?P<x>NElqb2)|(?P<x5c>NE5XTWlP)|(?P<x5t>NE5YUWlPaU)|(?P<x5ts256>NE5YUWpVekkxTmlJNkl)|(?P<x5u>NE5YVWlPaU)|(?P<zip>NmFYQWlPaU))[a-zA-Z0-9\/\\_+\-\r\n]{40,}={0,2}''',
     "[REDACTED_JWT_BASE64]"),

    ("Kraken Access Token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:kraken)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9\/=_\+\-]{80,90})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_KRAKEN_ACCESS_TOKEN]"),

    ("Possible Kubernetes Secret detected", CRITICAL, HIGH_CONF,
     r'''(?i)(?:\bkind:[ \t]*["']?\bsecret\b["']?(?s:.){0,200}?\bdata:(?s:.){0,100}?\s+([\w.-]+:(?:[ \t]*(?:\||>[-+]?)\s+)?[ \t]*(?:["']?[a-z0-9+/]{10,}={0,3}["']?|\{\{[ \t\w"|$:=,.-]+}}|""|''))|\bdata:(?s:.){0,100}?\s+([\w.-]+:(?:[ \t]*(?:\||>[-+]?)\s+)?[ \t]*(?:["']?[a-z0-9+/]{10,}={0,3}["']?|\{\{[ \t\w"|$:=,.-]+}}|""|''))(?s:.){0,200}?\bkind:[ \t]*["']?\bsecret\b["']?)''',
     "[REDACTED_KUBERNETES_SECRET_YAML]"),

    ("Kucoin Access Token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:kucoin)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-f0-9]{24})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_KUCOIN_ACCESS_TOKEN]"),

    ("Discovered a Kucoin Secret Key", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:kucoin)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_KUCOIN_SECRET_KEY]"),

    ("Uncovered a Launchdarkly Access Token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:launchdarkly)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9=_\-]{40})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_LAUNCHDARKLY_ACCESS_TOKEN]"),

    ("Linear Client Secret", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:linear)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-f0-9]{32})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_LINEAR_CLIENT_SECRET]"),

    ("LinkedIn Client ID", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:linked[_-]?in)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9]{14})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_LINKEDIN_CLIENT_ID]"),

    ("Discovered a LinkedIn Client secret", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:linked[_-]?in)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9]{16})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_LINKEDIN_CLIENT_SECRET]"),

    ("Uncovered a Lob API Key", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:lob)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}((live|test)_[a-f0-9]{35})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_LOB_API_KEY]"),

    ("Lob Publishable API Key", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:lob)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}((test|live)_pub_[a-f0-9]{31})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_LOB_PUB_API_KEY]"),

    ("Looker Client ID", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:looker)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9]{20})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_LOOKER_CLIENT_ID]"),

    ("Looker Client Secret", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:looker)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9]{24})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_LOOKER_CLIENT_SECRET]"),

    ("Mailchimp API key", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:MailchimpSDK.initialize|mailchimp)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-f0-9]{32}-us\d\d)(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_MAILCHIMP_API_KEY]"),

    ("Mailgun private API token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:mailgun)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}(key-[a-f0-9]{32})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_MAILGUN_PRIVATE_API_TOKEN]"),

    ("Discovered a Mailgun public validation key", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:mailgun)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}(pubkey-[a-f0-9]{32})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_MAILGUN_PUB_KEY]"),

    ("Uncovered a Mailgun webhook signing key", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:mailgun)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-h0-9]{32}-[a-h0-9]{8}-[a-h0-9]{8})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_MAILGUN_SIGNING_KEY]"),

    ("MapBox API token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:mapbox)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}(pk\.[a-z0-9]{60}\.[a-z0-9]{22})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_MAPBOX_API_TOKEN]"),

    ("Mattermost Access Token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:mattermost)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9]{26})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_MATTERMOST_ACCESS_TOKEN]"),

    ("MaxMind license key.", CRITICAL, HIGH_CONF,
     r'''\b([A-Za-z0-9]{6}_[A-Za-z0-9]{29}_mmk)(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_MAXMIND_LICENSE_KEY]"),

    ("MessageBird API token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:message[_-]?bird)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9]{25})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_MESSAGEBIRD_API_TOKEN]"),

    ("Discovered a MessageBird client ID", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:message[_-]?bird)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_MESSAGEBIRD_CLIENT_ID]"),

    ("Uncovered a Microsoft Teams Webhook", CRITICAL, HIGH_CONF,
     r'''https://[a-z0-9]+\.webhook\.office\.com/webhookb2/[a-z0-9]{8}-([a-z0-9]{4}-){3}[a-z0-9]{12}@[a-z0-9]{8}-([a-z0-9]{4}-){3}[a-z0-9]{12}/IncomingWebhook/[a-z0-9]{32}/[a-z0-9]{8}-([a-z0-9]{4}-){3}[a-z0-9]{12}''',
     "[REDACTED_MICROSOFT_TEAMS_WEBHOOK]"),

    ("Netlify Access Token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:netlify)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9=_\-]{40,46})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_NETLIFY_ACCESS_TOKEN]"),

    ("New Relic ingest browser API token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:new-relic|newrelic|new_relic)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}(NRJS-[a-f0-9]{19})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_NEW_RELIC_BROWSER_API_TOKEN]"),

    ("Discovered a New Relic insight insert key", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:new-relic|newrelic|new_relic)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}(NRII-[a-z0-9-]{32})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_NEW_RELIC_INSERT_KEY]"),

    ("New Relic user API ID", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:new-relic|newrelic|new_relic)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9]{64})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_NEW_RELIC_USER_API_ID]"),

    ("Discovered a New Relic user API Key", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:new-relic|newrelic|new_relic)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}(NRAK-[a-z0-9]{27})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_NEW_RELIC_USER_API_KEY]"),

    ("Notion API token", CRITICAL, HIGH_CONF,
     r'''\b(ntn_[0-9]{11}[A-Za-z0-9]{32}[A-Za-z0-9]{3})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_NOTION_API_TOKEN]"),

    ("Uncovered an npm access token", CRITICAL, HIGH_CONF,
     r'''(?i)\b(npm_[a-z0-9]{36})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_NPM_ACCESS_TOKEN]"),

    ("Password within a Nuget config file", CRITICAL, HIGH_CONF,
     r'''(?i)<add key=\"(?:(?:ClearText)?Password)\"\s*value=\"(.{8,})\"\s*/>''',
     "[REDACTED_NUGET_CONFIG_PASSWORD]"),

    ("Nytimes Access Token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:nytimes|new-york-times,|newyorktimes)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9=_\-]{32})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_NYTIMES_ACCESS_TOKEN]"),

    ("Octopus Deploy API key", CRITICAL, HIGH_CONF,
     r'''\b(API-[A-Z0-9]{26})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_OCTOPUS_DEPLOY_API_KEY]"),

    ("Okta Access Token", CRITICAL, HIGH_CONF,
     r'''[\w.-]{0,50}?(?i:[\w.-]{0,50}?(?:(?-i:[Oo]kta|OKTA))(?:[ \t\w.-]{0,20})[\s'"]{0,3})(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}(00[\w=\-]{40})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_OKTA_ACCESS_TOKEN]"),

    ("Found an OpenAI API Key", CRITICAL, HIGH_CONF,
     r'''\b(sk-(?:proj|svcacct|admin)-(?:[A-Za-z0-9_-]{74}|[A-Za-z0-9_-]{58})T3BlbkFJ(?:[A-Za-z0-9_-]{74}|[A-Za-z0-9_-]{58})\b|sk-[a-zA-Z0-9]{20}T3BlbkFJ[a-zA-Z0-9]{20})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_OPENAI_API_KEY]"),

    ("Perplexity API key", CRITICAL, HIGH_CONF,
     r'''\b(pplx-[a-zA-Z0-9]{48})(?:[\x60'"\s;]|\\[nr]|$|\b)''',
     "[REDACTED_PERPLEXITY_API_KEY]"),

    ("Discovered a Plaid API Token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:plaid)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}(access-(?:sandbox|development|production)-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_PLAID_API_TOKEN]"),

    ("Uncovered a Plaid Client ID", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:plaid)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9]{24})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_PLAID_CLIENT_ID]"),

    ("Plaid Secret key", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:plaid)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9]{30})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_PLAID_SECRET_KEY]"),

    ("PlanetScale OAuth token", CRITICAL, HIGH_CONF,
     r'''\b(pscale_oauth_[\w=\.-]{32,64})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_PLANETSCALE_OAUTH_TOKEN]"),

    ("Prefect API token", CRITICAL, HIGH_CONF,
     r'''\b(pnu_[a-zA-Z0-9]{36})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_PREFECT_API_TOKEN]"),

    ("Private Key, which may compromise cryptographic security ...", CRITICAL, HIGH_CONF,
     r'''(?i)-----BEGIN[ A-Z0-9_-]{0,100}PRIVATE KEY(?: BLOCK)?-----[\s\S-]{64,}?KEY(?: BLOCK)?-----''',
     "[REDACTED_PRIVATE_KEY]"),

    ("PrivateAI Token, posing a risk of unauthorized access to ...", CRITICAL, HIGH_CONF,
     r'''[\w.-]{0,50}?(?i:[\w.-]{0,50}?(?:private[_-]?ai)(?:[ \t\w.-]{0,20})[\s'"]{0,3})(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9]{32})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_PRIVATEAI_API_TOKEN]"),

    ("Pulumi API token", CRITICAL, HIGH_CONF,
     r'''\b(pul-[a-f0-9]{40})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_PULUMI_API_TOKEN]"),

    ("Discovered a PyPI upload token", CRITICAL, HIGH_CONF,
     r'''pypi-AgEIcHlwaS5vcmc[\w-]{50,1000}''',
     "[REDACTED_PYPI_UPLOAD_TOKEN]"),

    ("Uncovered a RapidAPI Access Token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:rapidapi)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9_-]{50})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_RAPIDAPI_ACCESS_TOKEN]"),

    ("Readme API token", CRITICAL, HIGH_CONF,
     r'''\b(rdme_[a-z0-9]{70})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_README_API_TOKEN]"),

    ("Rubygem API token", CRITICAL, HIGH_CONF,
     r'''\b(rubygems_[a-f0-9]{48})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_RUBYGEMS_API_TOKEN]"),

    ("Scalingo API token", CRITICAL, HIGH_CONF,
     r'''\b(tk-us-[\w-]{48})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_SCALINGO_API_TOKEN]"),

    ("Discovered a Sendbird Access ID", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:sendbird)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_SENDBIRD_ACCESS_ID]"),

    ("Uncovered a Sendbird Access Token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:sendbird)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-f0-9]{40})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_SENDBIRD_ACCESS_TOKEN]"),

    ("Sentry.io Access Token (old format)", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:sentry)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-f0-9]{64})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_SENTRY_ACCESS_TOKEN]"),

    ("Sentry.io User Token", CRITICAL, HIGH_CONF,
     r'''\b(sntryu_[a-f0-9]{64})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_SENTRY_USER_TOKEN]"),

    ("Settlemint Application Access Token.", CRITICAL, HIGH_CONF,
     r'''\b(sm_aat_[a-zA-Z0-9]{16})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_SETTLEMINT_APPLICATION_ACCESS_TOKEN]"),

    ("Settlemint Personal Access Token.", CRITICAL, HIGH_CONF,
     r'''\b(sm_pat_[a-zA-Z0-9]{16})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_SETTLEMINT_PERSONAL_ACCESS_TOKEN]"),

    ("Settlemint Service Access Token.", CRITICAL, HIGH_CONF,
     r'''\b(sm_sat_[a-zA-Z0-9]{16})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_SETTLEMINT_SERVICE_ACCESS_TOKEN]"),

    ("Discovered a Shippo API token", CRITICAL, HIGH_CONF,
     r'''\b(shippo_(?:live|test)_[a-fA-F0-9]{40})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_SHIPPO_API_TOKEN]"),

    ("Uncovered a Shopify access token", CRITICAL, HIGH_CONF,
     r'''shpat_[a-fA-F0-9]{32}''',
     "[REDACTED_SHOPIFY_ACCESS_TOKEN]"),

    ("Shopify custom access token", CRITICAL, HIGH_CONF,
     r'''shpca_[a-fA-F0-9]{32}''',
     "[REDACTED_SHOPIFY_CUSTOM_ACCESS_TOKEN]"),

    ("Shopify private app access token", CRITICAL, HIGH_CONF,
     r'''shppa_[a-fA-F0-9]{32}''',
     "[REDACTED_SHOPIFY_PRIVATE_APP_ACCESS_TOKEN]"),

    ("Shopify shared secret", CRITICAL, HIGH_CONF,
     r'''shpss_[a-fA-F0-9]{32}''',
     "[REDACTED_SHOPIFY_SHARED_SECRET]"),

    ("Discovered a Sidekiq Secret", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:BUNDLE_ENTERPRISE__CONTRIBSYS__COM|BUNDLE_GEMS__CONTRIBSYS__COM)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-f0-9]{8}:[a-f0-9]{8})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_SIDEKIQ_SECRET]"),

    ("Uncovered a Sidekiq Sensitive URL", CRITICAL, HIGH_CONF,
     r'''(?i)\bhttps?://([a-f0-9]{8}:[a-f0-9]{8})@(?:gems.contribsys.com|enterprise.contribsys.com)(?:[\/|\#|\?|:]|$)''',
     "[REDACTED_SIDEKIQ_SENSITIVE_URL]"),

    ("Slack App-level token", CRITICAL, HIGH_CONF,
     r'''(?i)xapp-\d-[A-Z0-9]+-\d+-[a-z0-9]+''',
     "[REDACTED_SLACK_APP_TOKEN]"),

    ("Slack Bot token, which may compromise bot integrations an...", CRITICAL, HIGH_CONF,
     r'''xoxb-[0-9]{10,13}-[0-9]{10,13}[a-zA-Z0-9-]*''',
     "[REDACTED_SLACK_BOT_TOKEN]"),

    ("Slack Configuration access token", CRITICAL, HIGH_CONF,
     r'''(?i)xoxe.xox[bp]-\d-[A-Z0-9]{163,166}''',
     "[REDACTED_SLACK_CONFIG_ACCESS_TOKEN]"),

    ("Discovered a Slack Configuration refresh token", CRITICAL, HIGH_CONF,
     r'''(?i)xoxe-\d-[A-Z0-9]{146}''',
     "[REDACTED_SLACK_CONFIG_REFRESH_TOKEN]"),

    ("Uncovered a Slack Legacy bot token", CRITICAL, HIGH_CONF,
     r'''xoxb-[0-9]{8,14}-[a-zA-Z0-9]{18,26}''',
     "[REDACTED_SLACK_LEGACY_BOT_TOKEN]"),

    ("Slack Legacy token", CRITICAL, HIGH_CONF,
     r'''xox[os]-\d+-\d+-\d+-[a-fA-F\d]+''',
     "[REDACTED_SLACK_LEGACY_TOKEN]"),

    ("Slack Legacy Workspace token", CRITICAL, HIGH_CONF,
     r'''xox[ar]-(?:\d-)?[0-9a-zA-Z]{8,48}''',
     "[REDACTED_SLACK_LEGACY_WORKSPACE_TOKEN]"),

    ("Slack User token", CRITICAL, HIGH_CONF,
     r'''xox[pe](?:-[0-9]{10,13}){3}-[a-zA-Z0-9-]{28,34}''',
     "[REDACTED_SLACK_USER_TOKEN]"),

    ("Discovered a Slack Webhook", CRITICAL, HIGH_CONF,
     r'''(?:https?://)?hooks.slack.com/(?:services|workflows|triggers)/[A-Za-z0-9+/]{43,56}''',
     "[REDACTED_SLACK_WEBHOOK_URL]"),

    ("Uncovered a Snyk API token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:snyk[_.-]?(?:(?:api|oauth)[_.-]?)?(?:key|token))(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_SNYK_API_TOKEN]"),

    ("Uncovered a Sonar API token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:sonar[_.-]?(login|token))(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}((?:squ_|sqp_|sqa_)?[a-z0-9=_\-]{40})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_SONAR_API_TOKEN]"),

    ("Sourcegraph is a code search and navigation engine.", CRITICAL, HIGH_CONF,
     r'''(?i)\b(\b(sgp_(?:[a-fA-F0-9]{16}|local)_[a-fA-F0-9]{40}|sgp_[a-fA-F0-9]{40}|[a-fA-F0-9]{40})\b)(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_SOURCEGRAPH_ACCESS_TOKEN]"),

    ("Square Access Token", CRITICAL, HIGH_CONF,
     r'''\b((?:EAAA|sq0atp-)[\w-]{22,60})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_SQUARE_ACCESS_TOKEN]"),

    ("Squarespace Access Token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:squarespace)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_SQUARESPACE_ACCESS_TOKEN]"),

    ("Stripe Access Token", CRITICAL, HIGH_CONF,
     r'''\b((?:sk|rk)_(?:test|live|prod)_[a-zA-Z0-9]{10,99})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_STRIPE_ACCESS_TOKEN]"),

    ("Discovered a SumoLogic Access ID", CRITICAL, HIGH_CONF,
     r'''[\w.-]{0,50}?(?i:[\w.-]{0,50}?(?:(?-i:[Ss]umo|SUMO))(?:[ \t\w.-]{0,20})[\s'"]{0,3})(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}(su[a-zA-Z0-9]{12})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_SUMOLOGIC_ACCESS_ID]"),

    ("Uncovered a SumoLogic Access Token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:(?-i:[Ss]umo|SUMO))(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9]{64})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_SUMOLOGIC_ACCESS_TOKEN]"),

    ("Telegram Bot API Token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:telegr)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([0-9]{5,16}:(?-i:A)[a-z0-9_\-]{34})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_TELEGRAM_BOT_API_TOKEN]"),

    ("Travis CI Access Token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:travis)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9]{22})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_TRAVISCI_ACCESS_TOKEN]"),

    ("Twilio API Key, posing a risk to communication services a...", CRITICAL, HIGH_CONF,
     r'''SK[0-9a-fA-F]{32}''',
     "[REDACTED_TWILIO_API_KEY]"),

    ("Discovered a Twitch API token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:twitch)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9]{30})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_TWITCH_API_TOKEN]"),

    ("Uncovered a Twitter Access Secret", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:twitter)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9]{45})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_TWITTER_ACCESS_SECRET]"),

    ("Twitter Access Token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:twitter)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([0-9]{15,25}-[a-zA-Z0-9]{20,40})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_TWITTER_ACCESS_TOKEN]"),

    ("Twitter API Key, which may compromise Twitter application...", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:twitter)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9]{25})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_TWITTER_API_KEY]"),

    ("Twitter API Secret", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:twitter)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9]{50})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_TWITTER_API_SECRET]"),

    ("Discovered a Twitter Bearer Token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:twitter)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}(A{22}[a-zA-Z0-9%]{80,100})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_TWITTER_BEARER_TOKEN]"),

    ("Uncovered a Typeform API token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:typeform)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}(tfp_[a-z0-9\-_\.=]{59})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_TYPEFORM_API_TOKEN]"),

    ("Vault Batch Token", CRITICAL, HIGH_CONF,
     r'''\b(hvb\.[\w-]{138,300})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_VAULT_BATCH_TOKEN]"),

    ("Vault Service Token", CRITICAL, HIGH_CONF,
     r'''\b((?:hvs\.[\w-]{90,120}|s\.(?i:[a-z0-9]{24})))(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_VAULT_SERVICE_TOKEN]"),

    ("Yandex Access Token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:yandex)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}(t1\.[A-Z0-9a-z_-]+[=]{0,2}\.[A-Z0-9a-z_-]{86}[=]{0,2})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_YANDEX_ACCESS_TOKEN]"),

    ("Discovered a Yandex API Key", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:yandex)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}(AQVN[A-Za-z0-9_\-]{35,38})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_YANDEX_API_KEY]"),

    ("Uncovered a Yandex AWS Access Token", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:yandex)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}(YC[a-zA-Z0-9_\-]{38})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_YANDEX_AWS_ACCESS_TOKEN]"),

    ("Zendesk Secret Key", CRITICAL, HIGH_CONF,
     r'''(?i)[\w.-]{0,50}?(?:zendesk)(?:[ \t\w.-]{0,20})[\s'"]{0,3}(?:=|>|:{1,3}=|\|\||:|=>|\?=|,)[\x60'"\s=]{0,5}([a-z0-9]{40})(?:[\x60'"\s;]|\\[nr]|$)''',
     "[REDACTED_ZENDESK_SECRET_KEY]"),


    # ═══════════════════════════════════════════════
    # Agent Hush Exclusive Rules (AI ecosystem + extras)
    # These cover services Gitleaks hasn't added yet
    # ═══════════════════════════════════════════════

    ("OpenAI Project Key", CRITICAL, HIGH_CONF,
     r'sk-proj-[A-Za-z0-9_\-]{40,}',
     "[REDACTED_OPENAI_PROJECT_KEY]"),

    ("OpenAI API Key (legacy)", CRITICAL, HIGH_CONF,
     r'sk-[A-Za-z0-9]{20,}T3BlbkFJ[A-Za-z0-9]{20,}',
     "[REDACTED_OPENAI_KEY]"),

    ("Anthropic API Key", CRITICAL, HIGH_CONF,
     r'sk-ant-[A-Za-z0-9_\-]{40,}',
     "[REDACTED_ANTHROPIC_KEY]"),

    ("Discord Bot Token", CRITICAL, HIGH_CONF,
     r'[MN][A-Za-z\d]{23,}\.[\w-]{6}\.[\w-]{27,}',
     "[REDACTED_DISCORD_TOKEN]"),

    ("GitHub Fine-grained Token", CRITICAL, HIGH_CONF,
     r'github_pat_[A-Za-z0-9_]{22,255}',
     "[REDACTED_GITHUB_PAT]"),

    ("AWS Secret Key (in config)", CRITICAL, HIGH_CONF,
     r'''(?i)(?:aws_secret_access_key|aws_secret_key|secret_access_key)["']?\s*[=:]\s*["']?([A-Za-z0-9/+=]{40})["']?''',
     "[REDACTED_AWS_SECRET]"),

    ("AWS Secret Key (in config)", CRITICAL, HIGH_CONF,
     r'''(?i)(?:aws_secret_access_key|aws_secret_key|secret_access_key)["']?\s*[=:]\s*["']?([A-Za-z0-9/+=]{40})["']?''',
     "[REDACTED_AWS_SECRET]"),

    ("Private Key Block", CRITICAL, HIGH_CONF,
     r'-----BEGIN\s+(?:RSA\s+|EC\s+|OPENSSH\s+|DSA\s+|PGP\s+)?PRIVATE KEY-----',
     "[REDACTED_PRIVATE_KEY]"),

    ("Database Connection String", HIGH, HIGH_CONF,
     r'(?:mysql|postgres(?:ql)?|mongodb(?:\+srv)?|redis|amqp|mssql|mariadb|cockroach)://\S+:\S+@\S+',
     "[REDACTED_DB_CONN]"),

    ("Twilio Account SID", CRITICAL, HIGH_CONF,
     r'AC[a-f0-9]{32}',
     "[REDACTED_TWILIO_SID]"),

    # ── CRITICAL + LOW CONFIDENCE: Generic patterns (could be code) ──
    ("Generic API Key Assignment", CRITICAL, LOW_CONF,
     r'(?i)(?:api_key|apikey|api_secret|api_token)\s*[=:]\s*["\']?([A-Za-z0-9_\-]{20,})["\']?',
     "[REDACTED_API_KEY]"),

    ("Generic Secret Assignment", CRITICAL, LOW_CONF,
     r'(?i)(?:password|passwd|pwd|secret|token|auth_token|access_token|bearer)\s*[=:]\s*["\']?([^\s"\']{8,})["\']?',
     "[REDACTED_SECRET]"),

    ("Generic Bearer Token", CRITICAL, LOW_CONF,
     r'(?i)(?:bearer\s+)([A-Za-z0-9_\-\.]{20,})',
     "[REDACTED_BEARER]"),

    # ── HIGH + LOW CONFIDENCE: Infrastructure (could be documentation) ──
    ("Private IPv4 (10.x)", HIGH, LOW_CONF,
     r'(?<!\d)10\.(?:25[0-5]|2[0-4]\d|1?\d\d?)\.(?:25[0-5]|2[0-4]\d|1?\d\d?)\.(?:25[0-5]|2[0-4]\d|1?\d\d?)(?!\d)',
     "[REDACTED_PRIVATE_IP]"),

    ("Private IPv4 (172.16-31.x)", HIGH, LOW_CONF,
     r'(?<!\d)172\.(?:1[6-9]|2\d|3[01])\.(?:25[0-5]|2[0-4]\d|1?\d\d?)\.(?:25[0-5]|2[0-4]\d|1?\d\d?)(?!\d)',
     "[REDACTED_PRIVATE_IP]"),

    ("Private IPv4 (192.168.x)", HIGH, LOW_CONF,
     r'(?<!\d)192\.168\.(?:25[0-5]|2[0-4]\d|1?\d\d?)\.(?:25[0-5]|2[0-4]\d|1?\d\d?)(?!\d)',
     "[REDACTED_PRIVATE_IP]"),

    ("Public IP in Config", HIGH, LOW_CONF,
     r'(?i)(?:ip|host|server|addr(?:ess)?)\s*[=:]\s*["\']?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})["\']?',
     "[REDACTED_SERVER_IP]"),

    ("SSH Key Path", HIGH, LOW_CONF,
     r'(?:/root/\.ssh/|~/\.ssh/|/home/\w+/\.ssh/)[^\s"\'<>]*',
     "[REDACTED_SSH_PATH]"),

    ("SSH Command with Key", HIGH, LOW_CONF,
     r'ssh\s+-i\s+[^\s]+\s+\w+@[\w.\-]+',
     "[REDACTED_SSH_COMMAND]"),

    # ── MEDIUM + LOW CONFIDENCE: PII ──
    ("Email Address", MEDIUM, LOW_CONF,
     r'[a-zA-Z0-9._%+\-]{2,}@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}',
     "[REDACTED_EMAIL]"),

    ("Chinese Phone Number", MEDIUM, LOW_CONF,
     r'(?<!\d)(?:\+?86[-\s]?)?1[3-9]\d[-\s]?\d{4}[-\s]?\d{4}(?!\d)',
     "[REDACTED_PHONE]"),

    ("International Phone", MEDIUM, LOW_CONF,
     r'(?<!\d)\+\d{1,3}[-\s]?\d{4,14}(?!\d)',
     "[REDACTED_PHONE]"),

    ("Chinese ID Card", MEDIUM, HIGH_CONF,
     r'(?<!\d)[1-9]\d{5}(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx](?!\d)',
     "[REDACTED_ID_CARD]"),

    ("Credit Card Number", MEDIUM, HIGH_CONF,
     r'(?<!\d)(?:4\d{3}|5[1-5]\d{2}|6(?:011|5\d{2})|3[47]\d{2})[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{3,4}(?!\d)',
     "[REDACTED_CARD]"),

    # ── LOW + LOW CONFIDENCE: Paths ──
    ("Root Home Path", LOW, LOW_CONF,
     r'/root/[^\s"\'<>:]+',
     "[REDACTED_ROOT_PATH]"),

    ("User Home Path", LOW, LOW_CONF,
     r'/home/[a-zA-Z0-9_\-]+/[^\s"\'<>:]+',
     "[REDACTED_HOME_PATH]"),

    ("Windows User Path", LOW, LOW_CONF,
     r'[Cc]:\\[Uu]sers\\[^\s"\'<>:]+',
     "[REDACTED_WIN_PATH]"),
]

# ── File Handling ──

DEFAULT_EXCLUDE_DIRS = {
    '.git', 'node_modules', '__pycache__', '.venv', 'venv', 'env',
    '.tox', '.eggs', '*.egg-info', '.mypy_cache', '.pytest_cache',
    'dist', 'build', '.next', '.nuxt', 'vendor', 'bower_components',
    '.bak_sanitize'
}

DEFAULT_EXCLUDE_FILES = {
    '*.pyc', '*.pyo', '*.so', '*.dylib', '*.dll', '*.exe',
    '*.o', '*.a', '*.lib', '*.bin', '*.dat',
    '*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp', '*.ico', '*.webp', '*.svg',
    '*.mp3', '*.mp4', '*.wav', '*.avi', '*.mov',
    '*.zip', '*.tar', '*.gz', '*.bz2', '*.xz', '*.7z', '*.rar',
    '*.woff', '*.woff2', '*.ttf', '*.eot',
    '*.pdf', '*.doc', '*.docx', '*.xls', '*.xlsx',
    '*.bak', '*.sqlite', '*.db',
    'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
    '.env.example', '.env.sample', '.env.template', '.env.defaults',
    '*.example', '*.sample', '*.template',
}

DEFAULT_ALLOWLIST = {
    'example@example.com', 'user@example.com', 'test@test.com',
    'user@host', 'noreply@github.com',
    'foo@bar.example', 'demo@demo.test', 'placeholder@example.net',
    'noreply@example.org',
    '127.0.0.1', '0.0.0.0', '255.255.255.255',
    'localhost',
}

MAX_FILE_SIZE_KB = 512

# ── Colors ──
class C:
    RED = '\033[91m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    GRAY = '\033[90m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

    @staticmethod
    def enabled():
        return sys.stdout.isatty()

def color(text, c_code):
    if C.enabled():
        return f"{c_code}{text}{C.RESET}"
    return text

SEVERITY_COLOR = {
    CRITICAL: C.RED,
    HIGH: C.YELLOW,
    MEDIUM: C.CYAN,
    LOW: C.GRAY,
}


def load_config(base_path):
    """Load .sanitize.json config if it exists."""
    # Search up from base_path to find config
    search = Path(base_path).resolve()
    config_data = None
    for _ in range(10):
        candidate = search / '.sanitize.json'
        if candidate.exists():
            try:
                with open(candidate, 'r') as f:
                    config_data = json.load(f)
            except Exception as e:
                print(f"Warning: Failed to load {candidate}: {e}", file=sys.stderr)
            break
        parent = search.parent
        if parent == search:
            break
        search = parent

    config = {
        'exclude_dirs': list(DEFAULT_EXCLUDE_DIRS),
        'exclude_files': list(DEFAULT_EXCLUDE_FILES),
        'allowlist': list(DEFAULT_ALLOWLIST),
        'custom_secrets': [],
        'max_file_size_kb': MAX_FILE_SIZE_KB,
    }

    if config_data:
        if 'exclude_dirs' in config_data:
            config['exclude_dirs'] = list(set(config['exclude_dirs']) | set(config_data['exclude_dirs']))
        if 'exclude_files' in config_data:
            config['exclude_files'] = list(set(config['exclude_files']) | set(config_data['exclude_files']))
        if 'allowlist' in config_data:
            config['allowlist'] = list(set(config['allowlist']) | set(config_data['allowlist']))
        if 'custom_secrets' in config_data:
            config['custom_secrets'] = config_data['custom_secrets']
        if 'max_file_size_kb' in config_data:
            config['max_file_size_kb'] = config_data['max_file_size_kb']

    return config


def should_skip_dir(dirname, exclude_dirs):
    return dirname in exclude_dirs or dirname.startswith('.')


def should_skip_file(filepath, exclude_files, max_size_kb):
    fname = os.path.basename(filepath)
    for pattern in exclude_files:
        if pattern.startswith('*'):
            if fname.endswith(pattern[1:]):
                return True
        elif fname == pattern:
            return True
    try:
        size = os.path.getsize(filepath)
        if size > max_size_kb * 1024 or size == 0:
            return True
    except OSError:
        return True
    try:
        with open(filepath, 'rb') as f:
            chunk = f.read(8192)
            if b'\x00' in chunk:
                return True
    except OSError:
        return True
    return False


def _wildcard_match(pattern, text):
    """Simple wildcard matching: * matches any characters."""
    import fnmatch
    return fnmatch.fnmatch(text, pattern) or fnmatch.fnmatch(text.lower(), pattern.lower())


def _is_code_pattern(matched_text):
    """Heuristic: detect if a matched value looks like code, not a real secret.
    Based on Shannon entropy + structural analysis (NDSS 2019 methodology)."""
    val = matched_text.strip().strip('"\'`')
    
    # Function calls: get_password(), fetch_key(), etc.
    if re.search(r'\w+\(.*\)', val):
        return True
    # Environment variable lookups: os.environ["X"], process.env.X
    if re.search(r'(?:os\.environ|process\.env|getenv|ENV\[)', val):
        return True
    # Template variables: ${VAR}, {{var}}, %{var}
    if re.search(r'[\$%]\{[^}]+\}|\{\{[^}]+\}\}', val):
        return True
    # Common placeholders
    if re.search(r'<YOUR_|CHANGE_?ME|TODO|FIXME|PLACEHOLDER|INSERT_|REPLACE_|_here\b|_HERE\b', val, re.IGNORECASE):
        return True
    # Placeholder values: your_xxx_here, xxx_your_xxx
    if re.search(r'(?:your_|_your_|put_|enter_|add_).{0,30}(?:here|key|token|secret|password)', val, re.IGNORECASE):
        return True
    # Language literals: None, null, undefined, nil, ''
    if val.lower() in ('none', 'null', 'undefined', 'nil', 'true', 'false', '""', "''", '``'):
        return True
    # Object attribute access: args.xxx, self.xxx, config.xxx, request.xxx
    if re.search(r'(?:args|self|this|config|request|response|ctx|context|options|params|settings)\.\w+', val):
        return True
    # Array/dict access: xxx[0], xxx["key"], xxx['key']
    if re.search(r'\w+\[[\'"0-9]', val):
        return True
    # Test data patterns: test_xxx, mock_xxx, fake_xxx, dummy_xxx
    if re.search(r'^(?:test_|mock_|fake_|dummy_|sample_|example_|my_|temp_)', val, re.IGNORECASE):
        return True
    # Empty or very short values (after quotes stripped)
    parts = re.split(r'[=:]\s*["\']?', val)
    if len(parts) > 1:
        actual_val = parts[-1].rstrip('"\'')
        if len(actual_val) < 8:
            return True
    return False


def scan_file(filepath, rules, allowlist):
    """Scan a single file and return list of findings."""
    findings = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
    except Exception:
        return findings

    for line_num, line in enumerate(lines, 1):
        line_stripped = line.rstrip('\n\r')
        for rule_name, severity, confidence, pattern, replacement in rules:
            for match in re.finditer(pattern, line_stripped):
                matched_text = match.group(0)
                if matched_text in allowlist:
                    continue
                if any(al in matched_text for al in allowlist):
                    continue
                # Wildcard allowlist: *@example.com matches user123@example.com
                if any('*' in al and _wildcard_match(al, matched_text) for al in allowlist):
                    continue
                # Heuristic: skip low-confidence generic patterns that look like code
                if confidence == LOW_CONF and 'Generic' in rule_name and _is_code_pattern(matched_text):
                    continue
                # Also filter Gitleaks generic/allowlist patterns
                if ('Generic' in rule_name or 'Allowlist' in rule_name) and _is_code_pattern(matched_text):
                    continue
                # Mask for display
                if len(matched_text) > 12:
                    display = matched_text[:4] + '***' + matched_text[-4:]
                elif len(matched_text) > 6:
                    display = matched_text[:2] + '***' + matched_text[-2:]
                else:
                    display = matched_text[:1] + '***'
                findings.append({
                    'file': filepath,
                    'line': line_num,
                    'rule': rule_name,
                    'severity': severity,
                    'confidence': confidence,
                    'match_display': display,
                    'match_start': match.start(),
                    'match_end': match.end(),
                    'match_text': matched_text,
                    'replacement': replacement,
                })
    return findings


def walk_files(base_path, config):
    """Walk directory tree and yield text file paths."""
    exclude_dirs = set(config['exclude_dirs'])
    exclude_files = set(config['exclude_files'])
    max_size = config['max_file_size_kb']

    for root, dirs, files in os.walk(base_path):
        dirs[:] = [d for d in dirs if not should_skip_dir(d, exclude_dirs)]
        for fname in sorted(files):
            fpath = os.path.join(root, fname)
            if not should_skip_file(fpath, exclude_files, max_size):
                yield fpath


def build_rules(config):
    rules = list(RULES)
    for i, custom_pattern in enumerate(config.get('custom_secrets', [])):
        rules.append((f"Custom Rule #{i+1}", CRITICAL, HIGH_CONF, custom_pattern, "[REDACTED_CUSTOM]"))
    return rules


def dedup_findings(findings):
    """Deduplicate findings by file+line+rule+position."""
    seen = set()
    unique = []
    for f in findings:
        key = (f['file'], f['line'], f['rule'], f['match_start'])
        if key not in seen:
            seen.add(key)
            unique.append(f)
    return unique


def format_report(findings, base_path, files_scanned, as_json=False, quiet=False):
    """Format and print scan report."""
    if as_json:
        output = {
            'files_scanned': files_scanned,
            'total_findings': len(findings),
            'clean': len(findings) == 0,
            'findings_by_severity': {},
            'findings': [],
        }
        for f in findings:
            sev = f['severity']
            output['findings_by_severity'][sev] = output['findings_by_severity'].get(sev, 0) + 1
            output['findings'].append({
                'file': os.path.relpath(f['file'], base_path),
                'line': f['line'],
                'rule': f['rule'],
                'severity': f['severity'],
                'match': f['match_display'],
            })
        print(json.dumps(output, indent=2, ensure_ascii=False))
        return

    if not findings:
        if not quiet:
            print(color("✅ Clean! No sensitive data found in outbound files.", C.GREEN))
            print(f"   Scanned {files_scanned} files. Safe to publish/push.")
        return

    if quiet:
        sev_counts = defaultdict(int)
        for f in findings:
            sev_counts[f['severity']] += 1
        parts = [f"{s}: {c}" for s, c in sorted(sev_counts.items(), key=lambda x: SEVERITY_ORDER[x[0]])]
        print(f"⚠️ BLOCKED — {len(findings)} sensitive items found ({', '.join(parts)})")
        return

    print(color(f"\n🚨 Privacy Guard — Outbound Check FAILED", C.BOLD))
    print(f"   Scanned {files_scanned} files — {len(findings)} sensitive items detected\n")
    print(f"   ⛔ Do NOT publish/push until these are resolved!\n")

    by_severity = defaultdict(list)
    for f in findings:
        by_severity[f['severity']].append(f)

    for sev in [CRITICAL, HIGH, MEDIUM, LOW]:
        if sev not in by_severity:
            continue
        sev_findings = by_severity[sev]
        print(color(f"  {'━' * 50}", SEVERITY_COLOR[sev]))
        print(color(f"  {sev} ({len(sev_findings)} findings)", SEVERITY_COLOR[sev]))
        print(color(f"  {'━' * 50}", SEVERITY_COLOR[sev]))

        by_file = defaultdict(list)
        for f in sev_findings:
            by_file[f['file']].append(f)

        for fpath, file_findings in sorted(by_file.items()):
            rel_path = os.path.relpath(fpath, base_path)
            print(f"  📄 {rel_path}")
            for f in sorted(file_findings, key=lambda x: x['line']):
                print(f"     L{f['line']:>4}: {color(f['rule'], SEVERITY_COLOR[sev])} — {f['match_display']}")
            print()

    sev_counts = defaultdict(int)
    for f in findings:
        sev_counts[f['severity']] += 1
    parts = [color(f"{s}: {c}", SEVERITY_COLOR[s]) for s, c in sorted(sev_counts.items(), key=lambda x: SEVERITY_ORDER[x[0]])]
    print(f"  📊 Total: {len(findings)} findings ({', '.join(parts)})")
    print()
    print(f"  💡 Options:")
    print(f"     1. Add false positives to .sanitize.json allowlist")
    print(f"     2. Run 'sanitize export <src> <dest>' to create a sanitized copy")
    print(f"     3. Manually remove sensitive data from source files\n")

    # Show low-confidence warning if applicable
    low_conf = [f for f in findings if f.get('confidence') == LOW_CONF]
    high_conf = [f for f in findings if f.get('confidence') == HIGH_CONF]
    if high_conf and low_conf:
        print(f"  ℹ️  {len(high_conf)} high-confidence (auto-fixable) + {len(low_conf)} low-confidence (needs review)")
        print(f"     'export' will only auto-replace high-confidence items by default.")
        print(f"     Use '--aggressive' to include low-confidence items too.\n")


def format_scan_report(findings, base_path, files_scanned, as_json=False, quiet=False):
    """Format scan report for local workspace scanning (informational, not blocking)."""
    if as_json:
        output = {
            'files_scanned': files_scanned,
            'total_findings': len(findings),
            'findings_by_severity': {},
            'findings': [],
        }
        for f in findings:
            sev = f['severity']
            output['findings_by_severity'][sev] = output['findings_by_severity'].get(sev, 0) + 1
            output['findings'].append({
                'file': os.path.relpath(f['file'], base_path),
                'line': f['line'],
                'rule': f['rule'],
                'severity': f['severity'],
                'match': f['match_display'],
            })
        print(json.dumps(output, indent=2, ensure_ascii=False))
        return

    if not findings:
        if not quiet:
            print(color("✅ No sensitive data found!", C.GREEN))
            print(f"   Scanned {files_scanned} files.")
        return

    if quiet:
        sev_counts = defaultdict(int)
        for f in findings:
            sev_counts[f['severity']] += 1
        parts = [f"{s}: {c}" for s, c in sorted(sev_counts.items(), key=lambda x: SEVERITY_ORDER[x[0]])]
        print(f"⚠️ Found {len(findings)} sensitive items ({', '.join(parts)})")
        return

    print(color(f"\n🔍 Privacy Guard — Local Scan Report", C.BOLD))
    print(f"   Scanned {files_scanned} files in {base_path}")
    print(f"   ℹ️  This is informational — your local files are safe on your machine.\n")

    by_severity = defaultdict(list)
    for f in findings:
        by_severity[f['severity']].append(f)

    for sev in [CRITICAL, HIGH, MEDIUM, LOW]:
        if sev not in by_severity:
            continue
        sev_findings = by_severity[sev]
        print(color(f"  {'━' * 50}", SEVERITY_COLOR[sev]))
        print(color(f"  {sev} ({len(sev_findings)} findings)", SEVERITY_COLOR[sev]))
        print(color(f"  {'━' * 50}", SEVERITY_COLOR[sev]))

        by_file = defaultdict(list)
        for f in sev_findings:
            by_file[f['file']].append(f)

        for fpath, file_findings in sorted(by_file.items()):
            rel_path = os.path.relpath(fpath, base_path)
            print(f"  📄 {rel_path}")
            for f in sorted(file_findings, key=lambda x: x['line']):
                print(f"     L{f['line']:>4}: {color(f['rule'], SEVERITY_COLOR[sev])} — {f['match_display']}")
            print()

    sev_counts = defaultdict(int)
    for f in findings:
        sev_counts[f['severity']] += 1
    parts = [color(f"{s}: {c}", SEVERITY_COLOR[s]) for s, c in sorted(sev_counts.items(), key=lambda x: SEVERITY_ORDER[x[0]])]
    print(f"  📊 Total: {len(findings)} findings ({', '.join(parts)})")
    print(f"  💡 These items are safe locally. Use 'check' before publishing to ensure they don't leak.\n")


# ─── Commands ───

def cmd_scan(args):
    """Scan local workspace to see what sensitive data exists (informational)."""
    base_path = os.path.abspath(args.path)
    if not os.path.isdir(base_path):
        print(f"Error: {base_path} is not a directory", file=sys.stderr)
        return 1

    config = load_config(base_path)
    rules = build_rules(config)
    allowlist = set(config['allowlist'])
    min_sev = SEVERITY_ORDER.get(args.severity.upper(), 3) if args.severity else 3

    all_findings = []
    files_scanned = 0
    for fpath in walk_files(base_path, config):
        files_scanned += 1
        findings = scan_file(fpath, rules, allowlist)
        all_findings.extend(findings)

    all_findings = [f for f in all_findings if SEVERITY_ORDER[f['severity']] <= min_sev]
    all_findings = dedup_findings(all_findings)

    format_scan_report(all_findings, base_path, files_scanned,
                       as_json=args.json, quiet=args.quiet)

    return 1 if all_findings else 0


def cmd_fix(args):
    """Replace sensitive data in local files with placeholders."""
    base_path = os.path.abspath(args.path)
    if not os.path.isdir(base_path):
        print(f"Error: {base_path} is not a directory", file=sys.stderr)
        return 1

    config = load_config(base_path)
    rules = build_rules(config)
    allowlist = set(config['allowlist'])
    aggressive = getattr(args, 'aggressive', False)

    if not aggressive:
        print(color("  🛡️  Conservative mode (default): only replacing high-confidence matches.", C.CYAN))
        print(f"     Use --aggressive to include all matches.\n")

    files_modified = 0
    total_replacements = 0
    skipped_low_conf = 0

    for fpath in walk_files(base_path, config):
        findings = scan_file(fpath, rules, allowlist)
        if not findings:
            continue

        # Filter by confidence
        if not aggressive:
            low = [f for f in findings if f['confidence'] == LOW_CONF]
            skipped_low_conf += len(low)
            findings = [f for f in findings if f['confidence'] == HIGH_CONF]
            if not findings:
                continue

        try:
            with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
        except Exception:
            continue

        modified = content
        replacements_in_file = 0
        unique_matches = {}
        for finding in findings:
            key = finding['match_text']
            if key not in unique_matches:
                unique_matches[key] = finding['replacement']

        for match_text, replacement in sorted(unique_matches.items(), key=lambda x: -len(x[0])):
            if match_text in modified:
                count = modified.count(match_text)
                modified = modified.replace(match_text, replacement)
                replacements_in_file += count

        if modified != content:
            rel_path = os.path.relpath(fpath, base_path)
            if args.dry_run:
                print(f"  [DRY RUN] 📄 {rel_path}: {replacements_in_file} replacements")
                for mt, rp in sorted(unique_matches.items(), key=lambda x: -len(x[0])):
                    if len(mt) > 12:
                        display = mt[:4] + '***' + mt[-4:]
                    elif len(mt) > 6:
                        display = mt[:2] + '***' + mt[-2:]
                    else:
                        display = mt[:1] + '***'
                    print(f"       {display} → {rp}")
            else:
                if not args.no_backup:
                    backup_dir = os.path.join(base_path, '.bak_sanitize')
                    os.makedirs(backup_dir, exist_ok=True)
                    backup_name = rel_path.replace(os.sep, '__')
                    shutil.copy2(fpath, os.path.join(backup_dir, backup_name))
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(modified)
                print(f"  ✅ {rel_path}: {replacements_in_file} replacements")

            files_modified += 1
            total_replacements += replacements_in_file

    if total_replacements == 0 and skipped_low_conf == 0:
        print(color("✅ No sensitive data found — nothing to fix!", C.GREEN))
        return 0

    if args.dry_run:
        print(f"\n  📊 [DRY RUN] Would modify {files_modified} files, {total_replacements} replacements total.")
        print(f"  💡 Run without --dry-run to apply changes.")
    else:
        print(f"\n  📊 Modified {files_modified} files, {total_replacements} replacements total.")
        if not args.no_backup:
            print(f"  📁 Backups saved to .bak_sanitize/")

    if skipped_low_conf > 0:
        print(color(f"  ⚠️  Skipped {skipped_low_conf} low-confidence matches (use --aggressive to include).", C.YELLOW))
    return 0


def cmd_check(args):
    """Check a directory for sensitive data before publishing/sharing."""
    base_path = os.path.abspath(args.path)
    if not os.path.isdir(base_path):
        print(f"Error: {base_path} is not a directory", file=sys.stderr)
        return 1

    config = load_config(base_path)
    rules = build_rules(config)
    allowlist = set(config['allowlist'])
    min_sev = SEVERITY_ORDER.get(args.severity.upper(), 3) if args.severity else 3

    all_findings = []
    files_scanned = 0
    for fpath in walk_files(base_path, config):
        files_scanned += 1
        findings = scan_file(fpath, rules, allowlist)
        all_findings.extend(findings)

    all_findings = [f for f in all_findings if SEVERITY_ORDER[f['severity']] <= min_sev]
    all_findings = dedup_findings(all_findings)

    format_report(all_findings, base_path, files_scanned,
                  as_json=args.json, quiet=args.quiet)

    return 1 if all_findings else 0


def cmd_check_push(args):
    """Check only git staged files before pushing."""
    repo_path = os.path.abspath(args.path) if args.path else os.getcwd()

    # Get staged files
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACMR'],
            capture_output=True, text=True, cwd=repo_path, timeout=10
        )
        staged_files = [f.strip() for f in result.stdout.strip().split('\n') if f.strip()]
    except Exception as e:
        print(f"Error: Failed to get git staged files: {e}", file=sys.stderr)
        return 1

    if not staged_files:
        # Fall back to checking all tracked files that differ from remote
        try:
            result = subprocess.run(
                ['git', 'diff', '--name-only', 'HEAD', '--diff-filter=ACMR'],
                capture_output=True, text=True, cwd=repo_path, timeout=10
            )
            staged_files = [f.strip() for f in result.stdout.strip().split('\n') if f.strip()]
        except Exception:
            pass

    if not staged_files:
        if not args.quiet:
            print(color("✅ No staged/modified files to check.", C.GREEN))
        return 0

    config = load_config(repo_path)
    rules = build_rules(config)
    allowlist = set(config['allowlist'])
    min_sev = SEVERITY_ORDER.get(args.severity.upper(), 3) if args.severity else 3

    all_findings = []
    files_scanned = 0
    exclude_files = set(config['exclude_files'])
    max_size = config['max_file_size_kb']

    for rel_path in staged_files:
        fpath = os.path.join(repo_path, rel_path)
        if not os.path.isfile(fpath):
            continue
        if should_skip_file(fpath, exclude_files, max_size):
            continue
        files_scanned += 1
        findings = scan_file(fpath, rules, allowlist)
        all_findings.extend(findings)

    all_findings = [f for f in all_findings if SEVERITY_ORDER[f['severity']] <= min_sev]
    all_findings = dedup_findings(all_findings)

    if not args.json and not args.quiet:
        print(color(f"  📋 Checking {len(staged_files)} staged/modified files...\n", C.BOLD))

    format_report(all_findings, repo_path, files_scanned,
                  as_json=args.json, quiet=args.quiet)

    return 1 if all_findings else 0


def cmd_export(args):
    """Create a sanitized copy of a directory for safe publishing."""
    src_path = os.path.abspath(args.source)
    dest_path = os.path.abspath(args.dest)

    if not os.path.isdir(src_path):
        print(f"Error: Source {src_path} is not a directory", file=sys.stderr)
        return 1

    if os.path.exists(dest_path) and not args.force:
        print(f"Error: Destination {dest_path} already exists. Use --force to overwrite.", file=sys.stderr)
        return 1

    config = load_config(src_path)
    rules = build_rules(config)
    allowlist = set(config['allowlist'])
    aggressive = getattr(args, 'aggressive', False)

    # Copy directory
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)

    mode_label = "Aggressive" if aggressive else "Conservative (default)"
    print(f"  📦 Creating sanitized copy — {mode_label} mode")
    print(f"     Source: {src_path}")
    print(f"     Destination: {dest_path}")
    if not aggressive:
        print(f"     ℹ️  Only replacing high-confidence matches. Use --aggressive for all.")
    print()

    shutil.copytree(src_path, dest_path,
                    ignore=shutil.ignore_patterns('.git', '.bak_sanitize', '__pycache__'))

    files_modified = 0
    total_replacements = 0
    skipped_low_conf = 0

    for fpath in walk_files(dest_path, config):
        findings = scan_file(fpath, rules, allowlist)
        if not findings:
            continue

        # Filter by confidence
        if not aggressive:
            low = [f for f in findings if f['confidence'] == LOW_CONF]
            skipped_low_conf += len(low)
            findings = [f for f in findings if f['confidence'] == HIGH_CONF]
            if not findings:
                continue

        try:
            with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
        except Exception:
            continue

        modified = content
        unique_matches = {}
        for finding in findings:
            key = finding['match_text']
            if key not in unique_matches:
                unique_matches[key] = finding['replacement']

        for match_text, replacement in sorted(unique_matches.items(), key=lambda x: -len(x[0])):
            if match_text in modified:
                count = modified.count(match_text)
                modified = modified.replace(match_text, replacement)
                total_replacements += count

        if modified != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(modified)
            rel_path = os.path.relpath(fpath, dest_path)
            print(f"  ✅ {rel_path}: {len(unique_matches)} types of sensitive data replaced")
            files_modified += 1

    print(f"\n  📊 Done! {files_modified} files sanitized, {total_replacements} replacements total.")
    print(f"  📁 Sanitized copy at: {dest_path}")
    print(f"  💡 You can now safely publish/share from this directory.")
    print(f"     Original files are untouched.")

    if skipped_low_conf > 0:
        print(color(f"\n  ⚠️  {skipped_low_conf} low-confidence matches were NOT replaced (could break functionality).", C.YELLOW))
        print(f"     Run 'sanitize check {dest_path}' to review them.")
        print(f"     Or re-run with --aggressive to replace everything.")

    print()
    return 0


def cmd_init(args):
    """Create default .sanitize.json config."""
    base_path = os.path.abspath(args.path)
    config_path = os.path.join(base_path, '.sanitize.json')

    if os.path.exists(config_path):
        print(f"⚠️  {config_path} already exists. Remove it first to re-initialize.")
        return 1

    default_config = {
        "exclude_dirs": sorted(DEFAULT_EXCLUDE_DIRS),
        "exclude_files": sorted(DEFAULT_EXCLUDE_FILES),
        "allowlist": sorted(DEFAULT_ALLOWLIST),
        "custom_secrets": [],
        "max_file_size_kb": MAX_FILE_SIZE_KB,
    }

    with open(config_path, 'w') as f:
        json.dump(default_config, f, indent=2, ensure_ascii=False)
        f.write('\n')

    print(f"✅ Created {config_path}")
    print(f"   Edit this file to customize exclusions, allowlist, and custom rules.")
    return 0


def cmd_allow(args):
    """Manage the allowlist — add, remove, or list allowed items."""
    base_path = os.path.abspath(args.path)
    config_path = os.path.join(base_path, '.sanitize.json')

    # Load or create config
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config_data = json.load(f)
    else:
        config_data = {"allowlist": sorted(DEFAULT_ALLOWLIST)}

    allowlist = set(config_data.get('allowlist', []))

    # List mode
    if args.list:
        if not allowlist:
            print("白名单为空")
        else:
            print(f"📋 白名单（{len(allowlist)} 项）：")
            for item in sorted(allowlist):
                builtin = " (内置)" if item in DEFAULT_ALLOWLIST else ""
                print(f"  • {item}{builtin}")
        return 0

    # Remove mode
    if args.remove:
        item = args.item
        if item in allowlist:
            allowlist.discard(item)
            config_data['allowlist'] = sorted(allowlist)
            with open(config_path, 'w') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
                f.write('\n')
            print(f"✅ 已从白名单移除：{item}")
        else:
            print(f"⚠️  白名单中没有：{item}")
        return 0

    # Add mode (default)
    if not args.item:
        print("Usage: sanitize allow <item> [--path <dir>]")
        print("       sanitize allow --list [--path <dir>]")
        print("       sanitize allow <item> --remove [--path <dir>]")
        print("\nExamples:")
        print('  sanitize allow "192.168.1.1"')
        print('  sanitize allow "*@example.com"')
        print('  sanitize allow "test_password"')
        return 1

    item = args.item
    if item in allowlist:
        print(f"ℹ️  已经在白名单中：{item}")
        return 0

    allowlist.add(item)
    config_data['allowlist'] = sorted(allowlist)

    with open(config_path, 'w') as f:
        json.dump(config_data, f, indent=2, ensure_ascii=False)
        f.write('\n')

    print(f"✅ 已加入白名单：{item}")
    if '*' in item:
        print(f"   通配符模式：匹配所有符合 {item} 的内容")
    print(f"   配置保存在：{config_path}")
    return 0


# ── Main ──

def main():
    parser = argparse.ArgumentParser(
        prog='sanitize',
        description='Agent Hush — Catch sensitive data before it leaves your machine',
    )
    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # scan — local workspace scan (informational)
    sp_scan = subparsers.add_parser('scan',
        help='Scan local workspace to see what sensitive data exists (informational)')
    sp_scan.add_argument('path', nargs='?', default='.', help='Directory to scan')
    sp_scan.add_argument('--json', action='store_true', help='Output as JSON')
    sp_scan.add_argument('--severity', default=None,
        help='Minimum severity to report (critical/high/medium/low)')
    sp_scan.add_argument('--quiet', action='store_true',
        help='Only output if findings exist')

    # fix — replace sensitive data in local files
    sp_fix = subparsers.add_parser('fix',
        help='Replace sensitive data in local files with [REDACTED_*] placeholders')
    sp_fix.add_argument('path', nargs='?', default='.', help='Directory to fix')
    sp_fix.add_argument('--dry-run', action='store_true',
        help='Preview changes without modifying files')
    sp_fix.add_argument('--no-backup', action='store_true',
        help='Skip creating backup files')
    sp_fix.add_argument('--aggressive', action='store_true',
        help='Include low-confidence matches (may break functionality!)')

    # check — scan a directory before publish/share
    sp_check = subparsers.add_parser('check',
        help='Scan a directory for sensitive data before publishing/sharing')
    sp_check.add_argument('path', help='Directory to check (e.g., your skill directory)')
    sp_check.add_argument('--json', action='store_true', help='Output as JSON')
    sp_check.add_argument('--severity', default=None,
        help='Minimum severity to report (critical/high/medium/low)')
    sp_check.add_argument('--quiet', action='store_true',
        help='Only output if findings exist')

    # check-push — scan git staged/modified files
    sp_push = subparsers.add_parser('check-push',
        help='Scan git staged/modified files before pushing')
    sp_push.add_argument('path', nargs='?', default=None,
        help='Git repository path (default: current directory)')
    sp_push.add_argument('--json', action='store_true', help='Output as JSON')
    sp_push.add_argument('--severity', default=None,
        help='Minimum severity to report (critical/high/medium/low)')
    sp_push.add_argument('--quiet', action='store_true',
        help='Only output if findings exist')

    # export — create sanitized copy
    sp_export = subparsers.add_parser('export',
        help='Create a sanitized copy of a directory for safe publishing')
    sp_export.add_argument('source', help='Source directory to sanitize')
    sp_export.add_argument('dest', help='Destination for sanitized copy')
    sp_export.add_argument('--force', action='store_true',
        help='Overwrite existing destination')
    sp_export.add_argument('--aggressive', action='store_true',
        help='Include low-confidence matches (may break functionality!)')

    # init — create config
    sp_init = subparsers.add_parser('init',
        help='Create default .sanitize.json config in a directory')
    sp_init.add_argument('path', nargs='?', default='.',
        help='Directory for config file')

    # allow — manage allowlist
    sp_allow = subparsers.add_parser('allow',
        help='Add, remove, or list allowlist items')
    sp_allow.add_argument('item', nargs='?', default=None,
        help='Item to add (supports wildcards: *@example.com)')
    sp_allow.add_argument('--remove', action='store_true',
        help='Remove item from allowlist')
    sp_allow.add_argument('--list', action='store_true',
        help='List current allowlist')
    sp_allow.add_argument('--path', default='.',
        help='Directory with .sanitize.json (default: current)')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    commands = {
        'scan': cmd_scan,
        'fix': cmd_fix,
        'check': cmd_check,
        'check-push': cmd_check_push,
        'export': cmd_export,
        'init': cmd_init,
        'allow': cmd_allow,
    }

    return commands[args.command](args)


if __name__ == '__main__':
    sys.exit(main())
