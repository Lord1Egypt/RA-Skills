"""Key expiry tracking and notifications."""
from datetime import datetime, timedelta
from typing import List, Dict, Any


def parse_expiry(expiry_str: str) -> datetime:
    """Parse ISO date string to datetime.
    
    Args:
        expiry_str: ISO format date (YYYY-MM-DD)
    
    Returns:
        datetime object
    """
    return datetime.fromisoformat(expiry_str)


def is_expiring_soon(expiry_str: str, days: int = 7) -> bool:
    """Check if a credential is expiring within N days.
    
    Args:
        expiry_str: ISO format expiry date
        days: Number of days threshold
    
    Returns:
        True if expiring within the threshold
    """
    try:
        expiry_date = parse_expiry(expiry_str)
        now = datetime.now()
        delta = expiry_date - now
        return timedelta(0) <= delta <= timedelta(days=days)
    except (ValueError, TypeError):
        return False


def is_expired(expiry_str: str) -> bool:
    """Check if a credential has already expired.
    
    Args:
        expiry_str: ISO format expiry date
    
    Returns:
        True if expired
    """
    try:
        expiry_date = parse_expiry(expiry_str)
        return datetime.now() > expiry_date
    except (ValueError, TypeError):
        return False


def get_expiring_credentials(credentials: List[Dict[str, Any]], days: int = 7) -> List[Dict[str, Any]]:
    """Filter credentials that are expiring soon.
    
    Args:
        credentials: List of credential metadata
        days: Number of days threshold
    
    Returns:
        List of expiring credentials
    """
    expiring = []
    
    for cred in credentials:
        expiry = cred.get("expires")
        if not expiry:
            continue
        
        if is_expiring_soon(expiry, days):
            cred_copy = cred.copy()
            cred_copy["days_until_expiry"] = (parse_expiry(expiry) - datetime.now()).days
            cred_copy["is_expired"] = is_expired(expiry)
            expiring.append(cred_copy)
    
    return expiring
