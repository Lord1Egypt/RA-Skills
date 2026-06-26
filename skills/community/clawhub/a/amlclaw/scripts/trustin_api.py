"""
TrustIn API integration for AML address screening.

This module provides integration with TrustIn's KYA (Know Your Address) API
for blockchain address risk assessment.
"""

import os
import json
import requests
from typing import Dict, Optional, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class KYAResult:
    """Result from TrustIn KYA API."""
    risk_score: int
    risk_level: str
    recommendation: str
    details: Dict[str, Any]
    raw_response: Optional[Dict] = None
    error: Optional[str] = None

class TrustInAPI:
    """Client for TrustIn API (Async Tasks)."""
    
    BASE_URL = "https://api.trustin-webui-dev.com/api/v2/investigate"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize TrustIn API client.
        
        Args:
            api_key: TrustIn API key. Optional — works without key (desensitized mode).
        """
        self.api_key = api_key or os.getenv("TRUSTIN_API_KEY") or ""
        # No raise — works without key in desensitized mode
        
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "text/plain",
            "User-Agent": "amlclaw-address-screening/0.1.0"
        })
    
    def _make_request(self, endpoint: str, data: Dict, require_auth: bool = False) -> Dict:
        """Make request to TrustIn API."""
        url = f"{self.BASE_URL}/{endpoint}"
        if self.api_key:
            url += f"?apikey={self.api_key}"
            
        try:
            # The API expects raw string payload in text/plain format according to curl
            response = self.session.post(url, data=json.dumps(data), timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            raise Exception("TrustIn API request timed out")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise Exception("Invalid authorization (Check API Key)")
            else:
                raise Exception(f"TrustIn API error: {e}")
        except json.JSONDecodeError:
            raise Exception("Invalid response from TrustIn API")

    def _wait_for_task(self, task_id: int, max_retries: int = 30) -> bool:
        """Poll get_status until finished."""
        import time
        for _ in range(max_retries):
            res = self._make_request("get_status", {"task_id": task_id}, require_auth=True)
            if res.get("code") == 0 and res.get("data") == "finished":
                return True
            time.sleep(2)
        return False

    def async_detect(self, chain_name: str, address: str, **kwargs) -> KYAResult:
        """Execute the asynchronous submit->poll->result pipeline."""
        chain_mapping = {
            "Tron": "Tron",
            "Ethereum": "Ethereum",
            "Bitcoin": "Bitcoin",
            "Solana": "Solana"
        }
        
        if chain_name not in chain_mapping:
            raise ValueError(f"Unsupported chain for TrustIn API: {chain_name}")

        submit_payload = {
            "chain_name": chain_mapping[chain_name],
            "address": address,
            "inflow_hops": kwargs.get("inflow_hops", 3),
            "outflow_hops": kwargs.get("outflow_hops", 3),
            "max_nodes_per_hop": kwargs.get("max_nodes_per_hop", 100)
        }
        
        if kwargs.get("min_timestamp"):
            submit_payload["min_timestamp"] = kwargs["min_timestamp"]
        if kwargs.get("max_timestamp"):
            submit_payload["max_timestamp"] = kwargs["max_timestamp"]
        
        try:
            submit_res = self._make_request("submit_task", submit_payload)
            task_id = submit_res.get("data")
            if submit_res.get("code") != 0 or not task_id:
                raise Exception(f"Failed to submit task: {submit_res.get('msg')}")

            # Polling
            if not self._wait_for_task(task_id):
                raise Exception(f"Task {task_id} timed out while processing.")

            # Get Result
            result_payload = {
                "task_id": task_id,
                "token": "usdt" # Defaulting to usdt based on example
            }
            final_res = self._make_request("get_result", result_payload, require_auth=True)
            
            if final_res.get("code") == 0:
                raw_data = final_res.get("data", {})
                
                # The 'data' field might be stringified JSON
                if isinstance(raw_data, str):
                    try:
                        raw_data = json.loads(raw_data)
                    except json.JSONDecodeError:
                        raw_data = {}
                
                # Support the new dict wrapper containing inflow_total_amount
                if isinstance(raw_data, dict):
                    raw_graph = raw_data.get("graph", raw_data.get("paths", raw_data))
                else:
                    raw_graph = raw_data
                
                # Heuristically calculate risk score from raw graph tags priority
                max_priority = 4
                risk_tags = set()
                
                # Helper to process tags
                def process_tags(tags_list):
                    nonlocal max_priority
                    for tag in tags_list:
                        if isinstance(tag, dict):
                            prio = tag.get("priority", 4)
                            risk_tags.add(tag.get("primary_category", "Unknown"))
                            if prio < max_priority:
                                max_priority = prio
                
                if isinstance(raw_graph, list):
                    for flow in raw_graph:
                        if isinstance(flow, dict):
                            process_tags(flow.get("tags", []))
                            for node in flow.get("path", []):
                                if isinstance(node, dict):
                                    process_tags(node.get("tags", []))
                elif isinstance(raw_graph, dict):
                    process_tags(raw_graph.get("tags", []))
                    for node in raw_graph.get("path", []):
                        if isinstance(node, dict):
                            process_tags(node.get("tags", []))
                
                # Priority 1: Critical (100), Priority 2: High (80), Priority 3: Medium (60), Priority 4: Low (20)
                risk_score_map = {1: 100, 2: 80, 3: 60, 4: 20}
                risk_score = risk_score_map.get(max_priority, 20)
                
                recommendation = "No specific risk tags identified"
                if risk_tags:
                    recommendation = f"Risk tags: {', '.join(list(risk_tags)[:3])}"

                if risk_score <= 20:
                    risk_level = "LOW"
                elif risk_score <= 40:
                    risk_level = "MEDIUM_LOW"
                elif risk_score <= 60:
                    risk_level = "MEDIUM"
                elif risk_score <= 80:
                    risk_level = "HIGH"
                else:
                    risk_level = "CRITICAL"

                return KYAResult(
                    risk_score=risk_score,
                    risk_level=risk_level,
                    recommendation=recommendation,
                    details=final_res,
                    raw_response=final_res
                )
            else:
                error_msg = final_res.get("msg", "Unknown API error")
                raise Exception(f"Failed to fetch result: {error_msg}")

        except Exception as e:
            import traceback
            traceback.print_exc()
            return KYAResult(
                risk_score=50,
                risk_level="UNKNOWN",
                recommendation=f"API Error/Fallback: {str(e)}",
                details={"api_error": str(e), "fallback": True},
                error=str(e)
            )

    def kya_lite_detect(self, chain_name: str, address: str) -> KYAResult:
        """Fallback wrapper, using async_detect under the hood with 1 hop."""
        return self.async_detect(chain_name, address, inflow_hops=1, outflow_hops=1)
    
    def kya_pro_detect(self, chain_name: str, address: str, **kwargs) -> KYAResult:
        """Wrapper to async_detect"""
        return self.async_detect(chain_name, address, **kwargs)

# Helper functions for direct usage
def screen_with_trustin(
    chain: str,
    address: str,
    api_key: Optional[str] = None,
    use_pro: bool = False,
    **kwargs
) -> Dict:
    """
    Convenience function to screen address with TrustIn API.
    
    Args:
        chain: Blockchain network
        address: Wallet address
        api_key: TrustIn API key (optional)
        use_pro: Use KYA Pro instead of KYA Lite
        **kwargs: Additional parameters for KYA Pro
    
    Returns:
        Dictionary with screening results
    """
    api = TrustInAPI(api_key=api_key)
    
    if use_pro:
        result = api.kya_pro_detect(chain, address, **kwargs)
    else:
        result = api.kya_lite_detect(chain, address)
    
    return {
        "risk_score": result.risk_score,
        "risk_level": result.risk_level,
        "recommendation": result.recommendation,
        "details": result.details,
        "api_used": True,
        "api_error": result.error,
        "timestamp": datetime.now().isoformat()
    }

# Export for easy import
__all__ = [
    "TrustInAPI",
    "KYAResult",
    "screen_with_trustin"
]