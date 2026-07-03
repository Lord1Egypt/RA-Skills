from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def get_usd_rate(
) -> Dict[str, Any]:
    """
    Get current USD/RUB exchange rate from zenrus.ru
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659852291", "get_usd_rate", arguments)

def get_eur_rate(
) -> Dict[str, Any]:
    """
    Get current EUR/RUB exchange rate from zenrus.ru
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659852291", "get_eur_rate", arguments)

def get_brent_usd_rate(
) -> Dict[str, Any]:
    """
    Get current Brent crude oil price in USD per barrel from zenrus.ru
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659852291", "get_brent_usd_rate", arguments)

def get_brent_rub_rate(
) -> Dict[str, Any]:
    """
    Get current Brent crude oil price in RUB per barrel from zenrus.ru
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659852291", "get_brent_rub_rate", arguments)

def calculate_barrels_for_rub(
    amount: float
) -> Dict[str, Any]:
    """
    Calculate how many barrels of Brent crude oil can be purchased for a given amount in Russian Rubles
    
    Args:
        amount: Amount in Russian Rubles
    
    Returns:
        
    """
    arguments = {
        "amount": amount
    }
    
    return call_api("1777316659852291", "calculate_barrels_for_rub", arguments)

def calculate_barrels_for_usd(
    amount: float
) -> Dict[str, Any]:
    """
    Calculate how many barrels of Brent crude oil can be purchased for a given amount in US Dollars
    
    Args:
        amount: Amount in US Dollars
    
    Returns:
        
    """
    arguments = {
        "amount": amount
    }
    
    return call_api("1777316659852291", "calculate_barrels_for_usd", arguments)

def calculate_barrels_for_eur(
    amount: float
) -> Dict[str, Any]:
    """
    Calculate how many barrels of Brent crude oil can be purchased for a given amount in Euros
    
    Args:
        amount: Amount in Euros
    
    Returns:
        
    """
    arguments = {
        "amount": amount
    }
    
    return call_api("1777316659852291", "calculate_barrels_for_eur", arguments)

