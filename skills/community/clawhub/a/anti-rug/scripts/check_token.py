#!/usr/bin/env python3
"""
Anti-Rug Token Security Checker v3.1 - Refactored
Web3 token contract security analyzer with cross-validation engine.
"""

import argparse
import json
import logging
import sys
import time
from typing import Dict, Any, Optional, List

import requests

from config import (
    GOPLUS_ENDPOINTS, DEAD_ADDRESSES, CHAIN_NAMES,
    REQUEST_TIMEOUT, RETRY_WAIT, FATAL_RULES, RISK_WEIGHTS,
    SCENARIO_WEIGHTS, SCENARIO_A_SYMBOLS, SCENARIO_A_NAME_KEYWORDS,
    SCENARIO_B_MIN_HOLDERS, PROTOCOL_TAGS
)
from exceptions import (
    AntiRugError, NetworkError, APIError,
    ContractNotFoundError, UnsupportedChainError
)
from validators import get_all_validators

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s [%(levelname)s] %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)


def safe_float(value: Any, default: float = 0.0) -> float:
    """Safely convert value to float."""
    try:
        return float(value) if value not in (None, "", "null") else default
    except (ValueError, TypeError):
        return default


def is_flag(val: Any) -> bool:
    """Check if GoPlus flag is set ("1" = True)."""
    return str(val).strip() == "1"


# ══════════════════════════════════════════════════════════════
# API Client (Refactored from fetch_goplus)
# ══════════════════════════════════════════════════════════════

class GoPlusClient:
    """GoPlus API client with retry logic."""
    
    def __init__(self, custom_gateway: str = ""):
        self.endpoints = []
        if custom_gateway:
            self.endpoints.append(custom_gateway.rstrip("/"))
        self.endpoints.extend(GOPLUS_ENDPOINTS)
    
    def _make_request(self, url: str) -> requests.Response:
        """Make HTTP request with timeout."""
        return requests.get(
            url,
            timeout=REQUEST_TIMEOUT,
            headers={"User-Agent": "AntiRugCN/3.1", "Accept": "application/json"},
        )
    
    def _parse_response(self, response: requests.Response, addr_lower: str, contract_address: str) -> Optional[Dict]:
        """Parse API response and extract token data."""
        if response.status_code != 200:
            raise APIError(f"HTTP {response.status_code}", response.status_code)
        
        data = response.json()
        if data.get("code") != 1:
            raise APIError(f"API code={data.get('code')}: {data.get('message')}")
        
        result = data.get("result") or {}
        if not result:
            raise ContractNotFoundError("Contract not found on chain")
        
        token_data = result.get(addr_lower) or result.get(contract_address)
        return token_data
    
    def fetch(self, chain_id: str, contract_address: str) -> Optional[Dict]:
        """Fetch token data with retry logic."""
        addr_lower = contract_address.lower()
        
        for i, base in enumerate(self.endpoints):
            url = f"{base}/api/v1/token_security/{chain_id}?contract_addresses={contract_address}"
            try:
                logger.info(f"[GoPlus] Trying endpoint [{i+1}/{len(self.endpoints)}]: {base}")
                resp = self._make_request(url)
                return self._parse_response(resp, addr_lower, contract_address)
            except requests.exceptions.Timeout:
                logger.warning(f"[GoPlus] Timeout ({REQUEST_TIMEOUT}s): {base}")
            except requests.exceptions.ConnectionError as e:
                logger.warning(f"[GoPlus] Connection failed: {e}")
            except (json.JSONDecodeError, KeyError) as e:
                logger.warning(f"[GoPlus] Parse failed: {e}")
            
            if i < len(self.endpoints) - 1:
                time.sleep(RETRY_WAIT)
        
        raise NetworkError("All endpoints failed")


# ══════════════════════════════════════════════════════════════
# Scenario Classification
# ══════════════════════════════════════════════════════════════

def classify_scenario(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Classify token into scenario A/B/C based on symbol, name, and holder count.
    """
    name = str(raw.get("token_name", "")).strip().lower()
    symbol = str(raw.get("token_symbol", "")).strip().lower()
    try:
        holder_count = int(raw.get("holder_count", 0) or 0)
    except (ValueError, TypeError):
        holder_count = 0
    
    # Scenario A: Pegged assets
    symbol_match = symbol in SCENARIO_A_SYMBOLS
    name_match = any(kw in name for kw in SCENARIO_A_NAME_KEYWORDS)
    if symbol_match or name_match:
        confidence = "high" if (symbol_match and name_match) else "medium"
        matched_by = []
        if symbol_match:
            matched_by.append(f"Symbol '{symbol.upper()}' in whitelist")
        if name_match:
            matched_by.append(f"Name contains pegged keyword")
        return {
            "scenario": "A",
            "label": "Pegged Asset / Stablecoin",
            "confidence": confidence,
            "rationale": "; ".join(matched_by),
            "tolerance": "High - institutional permissions are expected",
        }
    
    # Scenario B: Eco tokens
    if holder_count >= SCENARIO_B_MIN_HOLDERS:
        return {
            "scenario": "B",
            "label": "Ecosystem Token / DeFi / GameFi",
            "confidence": "medium",
            "rationale": f"{holder_count:,} holders indicates established user base",
            "tolerance": "Medium - allow proxy + treasury concentration",
        }
    
    # Scenario C: Meme/Unknown (default)
    return {
        "scenario": "C",
        "label": "Meme Coin / Unknown Token",
        "confidence": "high",
        "rationale": "Low holder count, no pegged indicators",
        "tolerance": "Low - all permissions treated as potential rug tools",
    }


# ══════════════════════════════════════════════════════════════
# Indicator Extraction
# ══════════════════════════════════════════════════════════════

def extract_indicators(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Extract and normalize security indicators from API response."""
    holders = raw.get("holders", [])
    lp_holders = raw.get("lp_holders", [])
    
    # Calculate top 10 concentration
    top10_pct = sum(safe_float(h.get("percent")) * 100 for h in holders[:10])
    
    # Calculate protocol-held percentage
    protocol_held_pct = sum(
        safe_float(h.get("percent")) * 100
        for h in holders
        if any(tag in str(h.get("tag", "")).lower() for tag in PROTOCOL_TAGS)
    )
    
    # Calculate LP locked percentage
    lp_locked_pct = sum(
        safe_float(lp.get("percent")) * 100
        for lp in lp_holders
        if is_flag(lp.get("is_locked", "0"))
    )
    
    owner_addr = raw.get("owner_address", "") or ""
    
    return {
        "is_honeypot": is_flag(raw.get("is_honeypot", "0")),
        "buy_tax": safe_float(raw.get("buy_tax")),
        "sell_tax": safe_float(raw.get("sell_tax")),
        "is_mintable": is_flag(raw.get("is_mintable", "0")),
        "has_blacklist": is_flag(raw.get("is_blacklist", "0")),
        "is_open_source": is_flag(raw.get("is_open_source", "0")),
        "is_proxy": is_flag(raw.get("is_proxy", "0")),
        "hidden_owner": is_flag(raw.get("hidden_owner", "0")),
        "can_take_back_ownership": is_flag(raw.get("can_take_back_ownership", "0")),
        "owner_change_balance": is_flag(raw.get("owner_change_balance", "0")),
        "selfdestruct": is_flag(raw.get("selfdestruct", "0")),
        "trading_cooldown": is_flag(raw.get("trading_cooldown", "0")),
        "is_whitelisted": is_flag(raw.get("is_whitelisted", "0")),
        "owner_is_dead": addr_is_dead(owner_addr),
        "lp_locked_pct": lp_locked_pct,
        "top10_pct": top10_pct,
        "protocol_held_pct": protocol_held_pct,
        "holder_count": int(raw.get("holder_count", 0) or 0),
    }


def addr_is_dead(addr: str) -> bool:
    """Check if address is dead/black hole address."""
    return not addr or str(addr).lower() in DEAD_ADDRESSES


# ══════════════════════════════════════════════════════════════
# Fatal Rules Engine (Refactored)
# ══════════════════════════════════════════════════════════════

def check_fatal(indicators: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Check all fatal rules against indicators.
    Returns list of triggered fatal findings.
    """
    fatals = []
    for rule in FATAL_RULES:
        try:
            if rule["check"](indicators):
                fatals.append({
                    "code": rule["code"],
                    "description": rule["description"],
                    "implication": rule["implication"],
                })
        except Exception as e:
            logger.warning(f"Fatal rule {rule['code']} check failed: {e}")
    return fatals


# ══════════════════════════════════════════════════════════════
# Cross-Validation Engine (Refactored with validators module)
# ══════════════════════════════════════════════════════════════

def cross_validate(indicators: Dict[str, Any], scenario: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Run all registered validators to analyze indicator relationships.
    """
    findings = []
    for validator in get_all_validators():
        try:
            result = validator(indicators, scenario)
            if result:
                findings.append(result)
        except Exception as e:
            logger.warning(f"Validator failed: {e}")
    return findings


# ══════════════════════════════════════════════════════════════
# Risk Scoring
# ══════════════════════════════════════════════════════════════

def compute_risk_score(
    indicators: Dict[str, Any],
    scenario: Dict[str, Any],
    fatals: List[Dict],
    cross_findings: List[Dict]
) -> Dict[str, Any]:
    """Compute dynamic risk score based on indicators and scenario."""
    sc = scenario.get("scenario", "C")
    weights = SCENARIO_WEIGHTS.get(sc, RISK_WEIGHTS)
    
    # Contract security (0-100, lower is better)
    contract_risk = 0
    if indicators["is_honeypot"]:
        contract_risk = 100
    elif indicators["hidden_owner"]:
        contract_risk = 90
    elif indicators["selfdestruct"]:
        contract_risk = 95
    elif not indicators["is_open_source"]:
        contract_risk = 40
    
    # Tax risk
    tax_risk = min(100, max(indicators["buy_tax"], indicators["sell_tax"]) * 2)
    
    # Liquidity risk
    liquidity_risk = max(0, 100 - indicators["lp_locked_pct"])
    
    # Concentration risk
    effective_concentration = max(0, indicators["top10_pct"] - indicators["protocol_held_pct"])
    concentration_risk = min(100, effective_concentration * 1.5)
    
    # Base score
    base_score = (
        contract_risk * weights["contract"] +
        tax_risk * weights["tax"] +
        liquidity_risk * weights["liquidity"] +
        concentration_risk * weights["concentration"]
    )
    
    # Apply cross-validation adjustments
    cv_adjustment = sum(f.get("score_delta", 0) for f in cross_findings)
    final_score = max(0, min(100, base_score + cv_adjustment))
    
    return {
        "base_score": round(base_score, 1),
        "cv_adjustment": cv_adjustment,
        "final_score": round(final_score, 1),
        "dimension_scores": {
            "contract_security": round(contract_risk, 1),
            "tax_risk": round(tax_risk, 1),
            "liquidity_risk": round(liquidity_risk, 1),
            "concentration_risk": round(concentration_risk, 1),
        },
        "weights_used": weights,
    }


# ══════════════════════════════════════════════════════════════
# Verdict Generation
# ══════════════════════════════════════════════════════════════

def generate_verdict(
    indicators: Dict[str, Any],
    scenario: Dict[str, Any],
    fatals: List[Dict],
    score: Dict[str, Any]
) -> Dict[str, Any]:
    """Generate final verdict based on all analysis."""
    final_score = score["final_score"]
    sc = scenario.get("scenario", "C")
    
    # Fatal findings override everything
    if fatals:
        if sc == "A":
            return {
                "risk_level": "CRITICAL",
                "risk_label": "🛑 COUNTERFEIT",
                "verdict": (
                    f"🛑 COUNTERFEIT DETECTED! This token claims to be a {scenario['label']} "
                    f"but has fatal flaws: {', '.join(f['code'] for f in fatals)}. "
                    "Verify contract address against official sources immediately."
                ),
            }
        return {
            "risk_level": "CRITICAL",
            "risk_label": "🛑 DO NOT BUY",
            "verdict": (
                f"🛑 CRITICAL: {len(fatals)} fatal vulnerability(s) detected. "
                f"{fatals[0]['description']}. {fatals[0]['implication']}. "
                "Your funds will likely be lost."
            ),
        }
    
    # Score-based verdicts
    if final_score >= 75:
        return {
            "risk_level": "HIGH",
            "risk_label": "🔴 High Risk",
            "verdict": f"🔴 High risk (score: {final_score}/100). Multiple serious issues. Avoid.",
        }
    elif final_score >= 50:
        return {
            "risk_level": "MEDIUM",
            "risk_label": "🟡 Medium Risk",
            "verdict": f"🟡 Medium risk (score: {final_score}/100). Caution required. Limit position to 5%.",
        }
    elif final_score >= 25:
        return {
            "risk_level": "LOW_MEDIUM",
            "risk_label": "🟡 Low-Medium Risk",
            "verdict": f"🟡 Minor concerns (score: {final_score}/100). Research team background before investing.",
        }
    else:
        return {
            "risk_level": "LOW",
            "risk_label": "✅ Low Risk",
            "verdict": f"✅ Base security passed (score: {final_score}/100). Contract is safe, but market risk remains.",
        }


# ══════════════════════════════════════════════════════════════
# Main Parser
# ══════════════════════════════════════════════════════════════

def parse_and_assess(raw: Dict, contract_address: str, chain_id: str) -> Dict[str, Any]:
    """Main analysis pipeline."""
    scenario = classify_scenario(raw)
    indicators = extract_indicators(raw)
    fatals = check_fatal(indicators)
    cross_findings = cross_validate(indicators, scenario)
    score = compute_risk_score(indicators, scenario, fatals, cross_findings)
    verdict = generate_verdict(indicators, scenario, fatals, score)
    
    return {
        "status": "success",
        "chain": CHAIN_NAMES.get(chain_id, chain_id),
        "contract_address": contract_address,
        "basic_info": {
            "token_name": raw.get("token_name", "Unknown"),
            "token_symbol": raw.get("token_symbol", "Unknown"),
            "total_supply": raw.get("total_supply", "Unknown"),
            "holder_count": raw.get("holder_count", "Unknown"),
        },
        "scenario_classification": scenario,
        "indicators": indicators,
        "fatal_findings": fatals,
        "cross_validations": cross_findings,
        "risk_score": score,
        "final_verdict": verdict,
    }


def check_token(chain_id: str, contract_address: str, api_gateway: str = "") -> Dict[str, Any]:
    """Main entry point."""
    contract_address = contract_address.strip()
    chain_id = str(chain_id).strip()
    
    if not contract_address:
        return {"status": "error", "message": "Contract address required"}
    
    if chain_id not in CHAIN_NAMES:
        return {"status": "error", "message": f"Unsupported chain: {chain_id}"}
    
    if chain_id != "solana":
        if not contract_address.startswith("0x") or len(contract_address) != 42:
            return {"status": "error", "message": f"Invalid EVM address: {contract_address}"}
    
    try:
        client = GoPlusClient(api_gateway)
        raw = client.fetch(chain_id, contract_address)
        if raw is None:
            return {"status": "error", "message": "Contract not found"}
        return parse_and_assess(raw, contract_address, chain_id)
    except AntiRugError as e:
        return {"status": "error", "message": str(e)}
    except Exception as e:
        logger.exception("Unexpected error")
        return {"status": "error", "message": f"Internal error: {str(e)}"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Anti-Rug Token Security Checker v3.1")
    parser.add_argument("--chain_id", required=True, help="Chain ID (1=ETH, 56=BSC...)")
    parser.add_argument("--contract_address", required=True, help="Token contract address")
    parser.add_argument("--api_gateway", default="", help="Custom API gateway (optional)")
    args = parser.parse_args()
    
    result = check_token(
        chain_id=args.chain_id,
        contract_address=args.contract_address,
        api_gateway=args.api_gateway,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
