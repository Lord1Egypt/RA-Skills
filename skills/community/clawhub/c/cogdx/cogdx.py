"""
CogDx - Cognitive Diagnostics for AI Agents
External verification you can't do yourself.

Built by Cerebratech - Dr. Amanda Kavner, Computational Cognitive Scientist
"""

import os
import requests
from typing import Optional, Dict, Any, List


class CogDxClient:
    """
    Client for Cerebratech's Cognitive Diagnostics API.
    
    Provides external verification of agent reasoning:
    - Calibration audits
    - Bias detection
    - Reasoning trace analysis
    - Deception detection
    - Consensus verification
    """
    
    BASE_URL = "https://api.cerebratech.ai"
    
    def __init__(self, wallet: Optional[str] = None):
        """
        Initialize CogDx client.
        
        Args:
            wallet: Wallet address for credit-based payments.
                   Falls back to COGDX_WALLET env var.
        """
        self.wallet = wallet or os.environ.get("COGDX_WALLET")
        if not self.wallet:
            raise ValueError(
                "Wallet required for CogDx API. "
                "Pass wallet= or set COGDX_WALLET env var."
            )
    
    def _headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "X-WALLET": self.wallet,
        }
    
    def _post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make authenticated POST request."""
        response = requests.post(
            f"{self.BASE_URL}{endpoint}",
            headers=self._headers(),
            json=data,
            timeout=30
        )
        
        if response.status_code == 402:
            raise PaymentRequiredError(
                "Insufficient credits. Earn credits via feedback or pay via x402."
            )
        
        if response.status_code == 429:
            raise RateLimitError(
                "Rate limit exceeded. Free tier: 100/day, 2000/month."
            )
        
        if not response.ok:
            raise CogDxError(f"API error: {response.status_code} - {response.text}")
        
        return response.json()
    
    def calibration_audit(
        self,
        agent_id: str,
        predictions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Audit prediction calibration.
        
        Compares stated confidence levels to actual accuracy.
        A calibrated agent is right 80% of the time when 80% confident.
        
        Args:
            agent_id: Your agent identifier
            predictions: List of {prompt, response, confidence} dicts
        
        Returns:
            dict with:
                - calibration_score: float 0-1 (1 = perfectly calibrated)
                - overconfidence_rate: float (how often too confident)
                - underconfidence_rate: float (how often too uncertain)
                - recommendations: list of improvement suggestions
        
        Cost: $0.06
        """
        return self._post("/calibration_audit", {
            "agent_id": agent_id,
            "sample_outputs": predictions,
        })
    
    def bias_scan(
        self,
        agent_id: str,
        outputs: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Scan for cognitive biases in agent outputs.
        
        Detects: anchoring, confirmation bias, availability heuristic,
        representativeness, sunk cost, and more.
        
        Args:
            agent_id: Your agent identifier
            outputs: List of {prompt, response, confidence} dicts
        
        Returns:
            dict with:
                - biases_detected: list of bias findings
                - severity: 'low' | 'medium' | 'high'
                - recommendations: list of mitigation strategies
        
        Cost: $0.10
        """
        return self._post("/bias_scan", {
            "agent_id": agent_id,
            "sample_outputs": outputs,
        })
    
    def analyze_reasoning(self, reasoning_trace: str) -> Dict[str, Any]:
        """
        Analyze a reasoning trace for logical fallacies.
        
        Args:
            reasoning_trace: The agent's step-by-step reasoning
        
        Returns:
            dict with:
                - logical_validity: float 0-1
                - status: 'valid' | 'flawed'
                - flaws_detected: list of detected fallacies
                - recommendations: suggested improvements
        
        Cost: $0.03
        """
        return self._post("/reasoning_trace_analysis", {
            "trace": reasoning_trace,
        })
    
    def deception_audit(
        self,
        agent_id: str,
        outputs: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Check for self-deception patterns.
        
        Detects when an agent is fooling itself about its own
        capabilities, knowledge, or confidence.
        
        Args:
            agent_id: Your agent identifier
            outputs: List of {prompt, response, confidence} dicts
        
        Returns:
            dict with:
                - deception_score: float 0-1 (0 = no deception)
                - patterns_detected: list of self-deception patterns
                - recommendations: list of fixes
        
        Cost: $0.25
        """
        return self._post("/deception_audit", {
            "agent_id": agent_id,
            "sample_outputs": outputs,
        })
    
    def verify_consensus(
        self,
        claim: str,
        context: Optional[str] = None,
        depth: str = "standard"
    ) -> Dict[str, Any]:
        """
        Cross-validate a claim with multiple models.
        
        Args:
            claim: The claim to verify
            context: Optional supporting context
            depth: 'quick' | 'standard' | 'deep'
        
        Returns:
            dict with:
                - consensus_score: float 0-1
                - model_votes: how each model voted
                - confidence: overall confidence
                - recommendation: 'accept' | 'verify' | 'reject'
        
        Cost: $0.25
        """
        return self._post("/verify_consensus", {
            "claim": claim,
            "context": context,
            "depth": depth,
        })
    
    def submit_feedback(
        self,
        endpoint: str,
        accurate: bool,
        confidence: Optional[float] = None,
        severity: Optional[int] = None,
        accuracy_score: Optional[float] = None,
        outcome: Optional[str] = None,
        reasoning: Optional[str] = None,
        diagnosis_id: Optional[str] = None,
        comments: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Submit feedback on a diagnosis to improve detection and earn credits.
        
        Feedback builds shared reality across agents. Network effects improve
        consensus and detection accuracy for everyone.
        
        REQUIRED (binary core):
            endpoint: Which endpoint was diagnosed (e.g., "/calibration_audit")
            accurate: Was the detection correct? (True/False)
        
        OPTIONAL (numerical enrichment - increases signal + credits):
            confidence: 0.0-1.0 - How sure are you about this feedback?
            severity: 1-5 - If bias was real, how impactful?
            accuracy_score: 0.0-1.0 - Partial credit (mostly right, slightly off)
        
        OPTIONAL (structured context):
            outcome: "win" | "loss" | "neutral" | "unknown" - What happened?
            reasoning: Why was detection right/wrong?
            diagnosis_id: ID from original diagnosis
            comments: General feedback text
        
        Returns:
            dict with:
                - received: bool
                - feedback_id: str
                - signal_strength: float (1.0-2.0x learning value)
                - credits: {awarded, new_balance, wallet}
                - network_contribution: impact on shared reality
        
        Cost: FREE (earns credits based on signal strength!)
        
        Example:
            # Binary only (1.0x signal)
            client.submit_feedback("/bias_scan", accurate=True)
            
            # Enriched (up to 2.0x signal, more credits)
            client.submit_feedback(
                endpoint="/calibration_audit",
                accurate=True,
                confidence=0.9,
                severity=4,
                outcome="win",
                reasoning="Caught the anchoring bias I missed"
            )
        """
        payload = {
            "wallet": self.wallet,
            "agent_id": self.wallet,
            "endpoint": endpoint,
            "accurate": accurate,
        }
        
        if confidence is not None:
            payload["confidence"] = confidence
        if severity is not None:
            payload["severity"] = severity
        if accuracy_score is not None:
            payload["accuracy_score"] = accuracy_score
        if outcome:
            payload["outcome"] = outcome
        if reasoning:
            payload["reasoning"] = reasoning
        if diagnosis_id:
            payload["diagnosis_id"] = diagnosis_id
        if comments:
            payload["comments"] = comments
        
        return self._post("/feedback", payload)
    
    def get_credits(self) -> Dict[str, Any]:
        """
        Check your credit balance.
        
        Returns:
            dict with:
                - balance: current credit balance
                - total_earned: lifetime earnings from feedback
                - total_spent: lifetime spending on audits
        """
        response = requests.get(
            f"{self.BASE_URL}/credits",
            headers=self._headers(),
            timeout=30
        )
        return response.json()


class CogDxError(Exception):
    """Base exception for CogDx errors."""
    pass


class PaymentRequiredError(CogDxError):
    """Raised when credits are insufficient."""
    pass


class RateLimitError(CogDxError):
    """Raised when rate limit is exceeded."""
    pass


# Convenience functions for quick usage
def calibration_audit(agent_id: str, predictions: list, wallet: str = None) -> dict:
    """Quick calibration audit."""
    return CogDxClient(wallet).calibration_audit(agent_id, predictions)


def bias_scan(agent_id: str, outputs: list, wallet: str = None) -> dict:
    """Quick bias scan."""
    return CogDxClient(wallet).bias_scan(agent_id, outputs)


def analyze_reasoning(trace: str, wallet: str = None) -> dict:
    """Quick reasoning analysis."""
    return CogDxClient(wallet).analyze_reasoning(trace)
