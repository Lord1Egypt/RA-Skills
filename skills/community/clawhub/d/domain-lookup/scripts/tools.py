from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def domain_lookup(
    domain: str,
    prefer_whois: Optional[bool] = False,
    include_raw: Optional[bool] = False
) -> Dict[str, Any]:
    """
    Look up domain information using RDAP protocol with WHOIS fallback. Provides comprehensive domain registration details, nameservers, contacts, and status information.
    
    Args:
        domain: The domain name to look up (e.g., example.com)
        prefer_whois: If true, use WHOIS instead of RDAP as the primary lookup method
        include_raw: If true, include raw protocol response data in the result
    
    Returns:
        
    """
    arguments = {
        "domain": domain,
        "prefer_whois": prefer_whois,
        "include_raw": include_raw
    }
    
    return call_api("1777316659800067", "domain_lookup", arguments)

