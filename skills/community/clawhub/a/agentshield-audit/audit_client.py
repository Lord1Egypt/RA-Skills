#!/usr/bin/env python3
"""
Low-level AgentShield API client.

DATA TRANSMISSION POLICY (Privacy-First):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ SENT TO API (WHITELIST):
   - Agent name (e.g. "MyBot")
   - Platform (e.g. "telegram")
   - Public key (Ed25519, used for certificate signing)
   - Test scores (pass/fail counts per category)
   - Test IDs (e.g. ["PI-001", "PI-002", "SS-003"])
   - Example: {"agent_name": "MyBot", "scores": {"prompt_injection": 4/5}, ...}

❌ NEVER SENT (EXPLICIT EXCLUSION):
   - Private keys (stay local in ~/.openclaw/workspace/.agentshield/)
   - System prompts or agent instructions
   - Tool call logs or conversation history
   - Workspace files (IDENTITY.md, SOUL.md, etc.)
   - Test input payloads (attack strings like "ignore previous instructions")
   - Test output logs (agent responses to attacks)
   - Evidence snippets (base64 matches, pattern findings)
   - Error messages from test execution
   - File paths or workspace structure
   - Any secrets or tokens

🔒 SUBMISSION SANITIZATION (v1.0.31+):
   - Explicit whitelist in _sanitize_test_details()
   - Only test_id, passed (bool), category sent
   - Attack payloads, responses, evidence explicitly dropped
   - See submit_results() line 145+ for implementation

🔒 API SECURITY:
   - Endpoint: agentshield.live/api (HTTPS only)
   - TLS 1.2+ enforced
   - Rate limit: 1 audit per hour per IP
   - No data retention beyond certificate signing
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import base64
import json
import os
import requests
from typing import Optional, Dict, Any

AGENTSHIELD_API = os.environ.get("AGENTSHIELD_API", "https://agentshield.live")


class AgentShieldClient:
    """Client for AgentShield Audit API."""
    
    def __init__(self, api_url: str = None):
        self.api_url = api_url or AGENTSHIELD_API
        self.session = requests.Session()
    
    def initiate_audit(
        self,
        agent_name: str,
        platform: str,
        public_key: str,
        agent_version: str = None
    ) -> Dict[str, Any]:
        """
        Initiate a new audit session.
        
        Args:
            agent_name: Human-readable agent name
            platform: Platform identifier (telegram, discord, etc.)
            public_key: Base64-encoded Ed25519 public key
            agent_version: Optional version string
        
        Returns:
            Audit session info including challenge
        """
        payload = {
            "agent_name": agent_name,
            "platform": platform,
            "public_key": public_key
        }
        if agent_version:
            payload["agent_version"] = agent_version
        
        response = self.session.post(
            f"{self.api_url}/api/agent-audit/initiate",
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    
    def complete_challenge(
        self,
        audit_id: str,
        challenge_response: str
    ) -> Dict[str, Any]:
        """
        Complete challenge-response authentication.
        
        Args:
            audit_id: Audit session ID
            challenge_response: Base64-encoded signature of challenge
        
        Returns:
            Authentication result
        """
        payload = {
            "audit_id": audit_id,
            "challenge_response": challenge_response
        }
        
        response = self.session.post(
            f"{self.api_url}/api/agent-audit/challenge",
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    
    def _sanitize_test_details(self, test_results: list) -> list:
        """
        Sanitize test results for API submission.
        
        WHITELIST APPROACH: Only send test_id, passed, and category.
        EXPLICITLY EXCLUDE: payloads, responses, evidence, errors.
        
        Args:
            test_results: Raw test results from tester
        
        Returns:
            Sanitized list with only safe fields
        """
        sanitized = []
        for test in test_results:
            # Whitelist - only these fields
            safe_test = {
                'test_id': str(test.get('test_id', 'unknown')),
                'passed': bool(test.get('passed', False)),
                'category': str(test.get('category', 'unknown'))
            }
            sanitized.append(safe_test)
            
            # EXPLICITLY NOT INCLUDED (for transparency):
            # - test.get('payload')      # Attack string
            # - test.get('response')     # Agent output
            # - test.get('evidence')     # Pattern matches
            # - test.get('error')        # Error messages
            # - test.get('raw_output')   # Full logs
            # - test.get('snippets')     # Code snippets
        
        return sanitized
    
    def submit_results(
        self,
        audit_id: str,
        test_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Submit sanitized test results and receive certificate.
        
        SANITIZATION: Only scores, counts, and test IDs sent.
        See _sanitize_test_details() for whitelist implementation.
        
        Args:
            audit_id: Audit session ID
            test_results: Results from security tests
        
        Returns:
            Certificate data
        """
        # Build summary with explicit type coercion
        summary = {
            "security_score": int(test_results.get('security_score', 0)),
            "tests_passed": int(test_results.get('tests_passed', 0)),
            "tests_total": int(test_results.get('tests_total', 0)),
            "tier": str(test_results.get('tier', 'UNKNOWN')),
            "critical_failures": int(test_results.get('critical_failures', 0)),
            "high_failures": int(test_results.get('high_failures', 0)),
            "medium_failures": int(test_results.get('medium_failures', 0))
        }
        
        # Sanitize detailed results - whitelist approach
        detailed = self._sanitize_test_details(
            test_results.get('test_results', [])
        )
        
        payload = {
            "audit_id": audit_id,
            "test_results": summary,
            "detailed_results": detailed  # Only test_id + passed + category
        }
        
        response = self.session.post(
            f"{self.api_url}/api/agent-audit/complete",
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    
    def verify_agent(self, agent_id: str) -> Dict[str, Any]:
        """
        Verify an agent's certificate.
        
        Args:
            agent_id: Agent's unique identifier
        
        Returns:
            Certificate data or error
        """
        response = self.session.get(
            f"{self.api_url}/api/verify/{agent_id}",
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    
    def revoke_certificate(
        self,
        agent_id: str,
        reason: str,
        signature: str
    ) -> Dict[str, Any]:
        """
        Revoke a certificate (requires agent's signature).
        
        Args:
            agent_id: Agent to revoke
            reason: Revocation reason
            signature: Signature of revocation request
        
        Returns:
            Revocation confirmation
        """
        payload = {
            "agent_id": agent_id,
            "reason": reason,
            "signature": signature
        }
        
        response = self.session.post(
            f"{self.api_url}/api/agent-audit/revoke",
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    
    def health_check(self) -> bool:
        """Check if API is available."""
        try:
            response = self.session.get(
                f"{self.api_url}/api/health",
                timeout=5
            )
            return response.status_code == 200
        except:
            return False


def main():
    """CLI for API client."""
    import argparse
    
    parser = argparse.ArgumentParser(description="AgentShield API Client")
    parser.add_argument("--api-url", help="Override API URL")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Health check
    subparsers.add_parser("health", help="Check API health")
    
    # Verify
    verify_parser = subparsers.add_parser("verify", help="Verify an agent")
    verify_parser.add_argument("agent-id", help="Agent ID to verify")
    
    args = parser.parse_args()
    
    client = AgentShieldClient(args.api_url)
    
    if args.command == "health":
        if client.health_check():
            print("✅ AgentShield API is online")
        else:
            print("❌ AgentShield API is unreachable")
            exit(1)
    
    elif args.command == "verify":
        agent_id = getattr(args, 'agent-id')
        try:
            result = client.verify_agent(agent_id)
            print(json.dumps(result, indent=2))
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"❌ Agent {agent_id} not found")
            else:
                print(f"❌ Error: {e}")
            exit(1)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
