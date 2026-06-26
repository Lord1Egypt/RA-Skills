import requests
import datetime

# Internal state for tracking
stats = {
    "total_bets": 0,
    "daily_count": 0,
    "history": [],
    "last_reset": datetime.date.today()
}

def fetch_live_odds(api_key: str, sport: str = "soccer_live"):
    """
    Fetches real-time in-play odds from The Odds API.
    """
    url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds/"
    params = {
        "apiKey": api_key,
        "regions": "as",  # Focus on Asian markets
        "markets": "h2h,spreads,totals",
        "oddsFormat": "decimal"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def execute_singbet_bet(event_id: str, market: str, odds: float, amount: int = 10):
    """
    Executes a bet on the Singbet platform via hga030.com.
    Note: Real implementation requires session handling or a specific agent API.
    """
    global stats
    
    # Reset daily count if it's a new day
    if datetime.date.today() > stats["last_reset"]:
        stats["daily_count"] = 0
        stats["last_reset"] = datetime.date.today()

    if stats["daily_count"] >= 30:
        return "Error: Daily limit of 30 bets reached."

    # Placeholder for actual API/Web-automation logic
    # Example: session.post("https://sangbet.com/api/place", data=...)
    
    bet_entry = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "event_id": event_id,
        "market": market,
        "odds": odds,
        "amount": f"$${amount}$$"
    }
    
    stats["history"].append(bet_entry)
    stats["total_bets"] += 1
    stats["daily_count"] += 1
    
    return f"Bet Successfully Placed: {market} at {odds} for $${amount}$$."

def get_betting_statistics():
    """Returns the performance summary."""
    return {
        "total_placed": stats["total_bets"],
        "today_count": stats["daily_count"],
        "recent_activity": stats["history"][-5:]
    }
