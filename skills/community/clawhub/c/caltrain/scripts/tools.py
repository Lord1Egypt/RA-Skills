from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def next_trains(
    origin: str,
    destination: str,
    when_iso: Optional[null] = None
) -> Dict[str, Any]:
    """
    Return the next few scheduled Caltrain departures.

Args:
    origin: Station name (e.g. 'San Jose Diridon', 'Palo Alto', 'San Francisco').
            Supports common abbreviations like 'SF' for San Francisco, 'SJ' for San Jose.
            If station is not found, use list_stations() to see all available options.
    destination: Station name (e.g. 'San Francisco', 'Mountain View', 'Tamien').
                 Supports common abbreviations like 'SF' for San Francisco, 'SJ' for San Jose.
                 If station is not found, use list_stations() to see all available options.
    when_iso: Optional ISO-8601 datetime (local time). Default: now.

Note: If you get a "Station not found" error, try using the list_stations() tool first
to see exact station names, then retry with the correct spelling.

    
    Args:
        origin: null
        destination: null
        when_iso: null
    
    Returns:
        null
    """
    arguments = {
        "origin": origin,
        "destination": destination,
        "when_iso": when_iso
    }
    
    return call_api("1777419073070083", "next_trains", arguments)

def list_stations(
) -> Dict[str, Any]:
    """
    List all available Caltrain stations.

This tool is useful when you need to find the exact station names, especially if
the next_trains() tool returns a "Station not found" error. Station names are
case-insensitive and support some common abbreviations like 'SF' and 'SJ'.

Returns a formatted list of all Caltrain stations that can be used as origin
or destination in the next_trains() tool.

    
    Args:
    
    Returns:
        null
    """
    arguments = {
    }
    
    return call_api("1777419073070083", "list_stations", arguments)

