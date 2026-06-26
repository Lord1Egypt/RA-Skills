#!/usr/bin/env python3
"""
A2A Client - Call remote agents via A2A protocol

Usage:
    python a2a_client.py <agent_url> <message> [token]

Example:
    python a2a_client.py "http://1.2.3.4:8080/a2a" "Hello" "my-token"
"""

import sys
import json
import urllib.request
import urllib.error
from typing import Optional, Dict, Any


class A2AClient:
    """A2A Protocol Client"""
    
    def __init__(self, agent_url: str, token: Optional[str] = None):
        self.agent_url = agent_url.rstrip('/')
        self.headers = {'Content-Type': 'application/json'}
        if token:
            self.headers['Authorization'] = f'Bearer {token}'
    
    def get_agent_card(self) -> Dict[str, Any]:
        """Get Agent Card (discover agent capabilities)"""
        url = f"{self.agent_url}/.well-known/agent.json"
        req = urllib.request.Request(url, headers=self.headers)
        
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError:
            # Try alternate path
            url = f"{self.agent_url}/agent-card"
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode('utf-8'))
    
    def send_message(self, message: str, context_id: Optional[str] = None) -> Dict[str, Any]:
        """Send message to remote agent (JSON-RPC 2.0)"""
        request_body = {
            "jsonrpc": "2.0",
            "method": "message/send",
            "id": "1",
            "params": {
                "message": {
                    "role": "user",
                    "parts": [{"type": "text", "text": message}]
                }
            }
        }
        
        if context_id:
            request_body["params"]["contextId"] = context_id
        
        req = urllib.request.Request(
            f"{self.agent_url}/rpc",
            data=json.dumps(request_body).encode('utf-8'),
            headers=self.headers
        )
        
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result.get('result', result)
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            return {"error": f"HTTP {e.code}: {error_body}"}
    
    def extract_text_response(self, response: Dict[str, Any]) -> str:
        """Extract text from response"""
        # Direct message response
        if 'parts' in response:
            for part in response.get('parts', []):
                if part.get('type') == 'text':
                    return part.get('text', '')
        
        # Task response with artifacts
        if 'artifacts' in response:
            for artifact in response.get('artifacts', []):
                for part in artifact.get('parts', []):
                    if part.get('type') == 'text':
                        return part.get('text', '')
        
        return json.dumps(response, ensure_ascii=False, indent=2)


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        print("Error: Insufficient arguments")
        sys.exit(1)
    
    agent_url = sys.argv[1]
    message = sys.argv[2]
    token = sys.argv[3] if len(sys.argv) > 3 else None
    
    client = A2AClient(agent_url, token)
    
    # Get Agent Card
    print(f"🔗 Connecting to: {agent_url}")
    try:
        card = client.get_agent_card()
        print(f"📋 Agent: {card.get('name', 'Unknown')}")
        print(f"📝 Description: {card.get('description', 'N/A')}")
    except Exception as e:
        print(f"⚠️ Cannot get Agent Card: {e}")
        print("Proceeding with message send...")
    
    # Send message
    print(f"\n📤 Sending: {message}")
    response = client.send_message(message)
    
    # Extract response
    text_response = client.extract_text_response(response)
    print(f"\n📥 Response:\n{text_response}")
    
    # Full JSON output
    if '--json' in sys.argv:
        print("\n📄 Full Response:")
        print(json.dumps(response, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()