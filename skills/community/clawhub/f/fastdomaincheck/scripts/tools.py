from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def check_domains(
    domains: null
) -> Dict[str, Any]:
    """
    
Check if multiple domain names are registered.

Usage:
    Input: A list of domain names to check (e.g. ["example.com", "test.com"])
    Output: JSON object containing registration status of each domain:
    {
      "results": {
        "example.com": {
          "registered": true
        },
        "test.com": {
          "registered": false
        }
      }
    }

    
    Args:
        domains: null
    
    Returns:
        null
    """
    arguments = {
        "domains": domains
    }
    
    return call_api("1777419077803011", "check_domains", arguments)

