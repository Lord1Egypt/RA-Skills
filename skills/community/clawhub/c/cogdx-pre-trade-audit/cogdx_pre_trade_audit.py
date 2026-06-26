"""
CogDx Pre-Trade Audit
Cognitive verification layer for prediction market trades.

Catches reasoning flaws before they become losses.
Built by Cerebratech - cognitive diagnostics for agents.
"""

import os
import requests
from typing import Optional, Dict, Any

# Lazy-loaded clients
_simmer_client = None
_cogdx_base_url = "https://api.cerebratech.ai"

TRADE_SOURCE = "sdk:cogdx-pre-trade-audit"
SKILL_SLUG = "cogdx-pre-trade-audit"


def get_simmer_client():
    """Lazy-load Simmer client."""
    global _simmer_client
    if _simmer_client is None:
        from simmer_sdk import SimmerClient
        _simmer_client = SimmerClient(
            api_key=os.environ["SIMMER_API_KEY"],
            venue="polymarket"
        )
    return _simmer_client


def cogdx_audit(
    reasoning: str,
    wallet: Optional[str] = None,
    min_validity: float = 0.7
) -> Dict[str, Any]:
    """
    Run cognitive diagnostics on trading reasoning.
    
    Args:
        reasoning: The trade thesis/reasoning to audit
        wallet: Optional wallet address for CogDx credits
        min_validity: Minimum validity score to pass (0-1)
    
    Returns:
        dict with:
            - approved: bool
            - validity_score: float (0-1)
            - issues: list of detected problems
            - recommendation: 'proceed' | 'review' | 'reject' | 'skip'
    """
    headers = {"Content-Type": "application/json"}
    
    # Add wallet for credit-based payment
    if wallet:
        headers["X-WALLET"] = wallet
    elif os.environ.get("COGDX_WALLET"):
        headers["X-WALLET"] = os.environ["COGDX_WALLET"]
    
    try:
        response = requests.post(
            f"{_cogdx_base_url}/reasoning_trace_analysis",
            headers=headers,
            json={"trace": reasoning},
            timeout=30
        )
        
        if response.status_code == 402:
            return {
                "approved": False,
                "validity_score": None,
                "issues": ["Payment required - add COGDX_WALLET to env"],
                "recommendation": "skip"
            }
        
        if not response.ok:
            return {
                "approved": False,
                "validity_score": None,
                "issues": [f"CogDx API error: {response.status_code}"],
                "recommendation": "skip"
            }
        
        result = response.json()
        validity = result.get("logical_validity") or 0
        flaws = result.get("flaws_detected") or []
        
        # Determine approval
        approved = validity >= min_validity and len(flaws) == 0
        
        if validity >= min_validity and len(flaws) == 0:
            recommendation = "proceed"
        elif validity >= 0.5:
            recommendation = "review"
        else:
            recommendation = "reject"
        
        # Format issues
        issues = []
        for f in flaws:
            if isinstance(f, dict):
                issues.append(f.get("name", str(f)))
            else:
                issues.append(str(f))
        
        return {
            "approved": approved,
            "validity_score": validity,
            "issues": issues,
            "recommendation": recommendation
        }
        
    except Exception as e:
        return {
            "approved": False,
            "validity_score": None,
            "issues": [f"CogDx unavailable: {str(e)}"],
            "recommendation": "skip"
        }


def audit_and_trade(
    market_id: str,
    side: str,
    amount: float,
    reasoning: str,
    confidence: float = 0.5,
    min_validity: float = 0.7,
    block_on_error: bool = True,
    live: bool = False
) -> Dict[str, Any]:
    """
    Audit reasoning and execute trade if it passes.
    
    Args:
        market_id: Polymarket market ID
        side: 'yes' or 'no'
        amount: Trade size in USD
        reasoning: Your trade thesis
        confidence: Your confidence level (0-1)
        min_validity: Minimum reasoning quality to proceed
        block_on_error: If True, block trade when CogDx is unavailable
        live: If True, execute real trade. Default False (dry-run).
    
    Returns:
        dict with audit results and trade outcome
    """
    # Step 1: Run cognitive audit
    audit = cogdx_audit(reasoning, min_validity=min_validity)
    
    result = {
        "audit": audit,
        "market_id": market_id,
        "side": side,
        "amount": amount,
        "confidence": confidence,
        "trade_executed": False,
        "trade_id": None,
        "approved": audit["approved"],
        "issues": audit["issues"],
        "recommendation": audit["recommendation"]
    }
    
    # Step 2: Decide whether to proceed
    if audit["recommendation"] == "skip" and block_on_error:
        result["blocked_reason"] = "CogDx unavailable and block_on_error=True"
        return result
    
    if not audit["approved"]:
        result["blocked_reason"] = f"Reasoning quality below threshold: {audit['validity_score']}"
        return result
    
    # Step 3: Execute trade (or dry-run)
    if not live:
        result["dry_run"] = True
        result["trade_executed"] = False
        result["message"] = "Dry-run: trade would execute. Pass --live for real trades."
        return result
    
    try:
        client = get_simmer_client()
        
        # Build reasoning string with audit info
        trade_reasoning = (
            f"{reasoning}\n\n"
            f"[CogDx Audit: validity={audit['validity_score']:.2f}, "
            f"recommendation={audit['recommendation']}]"
        )
        
        trade = client.trade(
            market_id=market_id,
            side=side,
            amount=amount,
            source=TRADE_SOURCE,
            skill_slug=SKILL_SLUG,
            reasoning=trade_reasoning
        )
        
        result["trade_executed"] = True
        result["trade_id"] = trade.get("id")
        result["trade"] = trade
        
    except Exception as e:
        result["trade_error"] = str(e)
        result["trade_executed"] = False
    
    return result


def main():
    """CLI entry point for cron execution."""
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description="CogDx Pre-Trade Audit")
    parser.add_argument("--market", required=True, help="Market ID")
    parser.add_argument("--side", required=True, choices=["yes", "no"])
    parser.add_argument("--amount", type=float, required=True)
    parser.add_argument("--reasoning", required=True, help="Trade thesis")
    parser.add_argument("--confidence", type=float, default=0.5)
    parser.add_argument("--min-validity", type=float, default=0.7)
    parser.add_argument("--live", action="store_true", help="Execute real trade")
    
    args = parser.parse_args()
    
    result = audit_and_trade(
        market_id=args.market,
        side=args.side,
        amount=args.amount,
        reasoning=args.reasoning,
        confidence=args.confidence,
        min_validity=args.min_validity,
        live=args.live
    )
    
    print(json.dumps(result, indent=2))
    
    # Exit with error if trade was blocked
    if not result["approved"]:
        exit(1)


if __name__ == "__main__":
    main()
