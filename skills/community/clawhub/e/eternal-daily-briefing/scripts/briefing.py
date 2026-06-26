#!/usr/bin/env python3
"""
Daily Briefing — Consolidated morning update from multiple sources.
"""

import sys
import os
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path

CONFIG_DIR = Path.home() / '.briefing'
CONFIG_FILE = CONFIG_DIR / 'config.json'
TASKS_FILE = CONFIG_DIR / 'tasks.json'
EVENTS_FILE = CONFIG_DIR / 'events.json'

DEFAULT_CONFIG = {
    'location': 'Dhaka, Bangladesh',
    'news_topics': ['technology', 'business'],
    'news_region': 'BD',
    'crypto': ['BTC-USD', 'ETH-USD', 'SOL-USD'],
    'stocks': ['SPY', 'QQQ', 'NVDA', 'AAPL'],
    'forex': ['EURUSD=X', 'GBPUSD=X'],
    'timezone': 'UTC'
}


def load_config():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return {**DEFAULT_CONFIG, **json.load(f)}
    with open(CONFIG_FILE, 'w') as f:
        json.dump(DEFAULT_CONFIG, f, indent=2)
    return DEFAULT_CONFIG


def load_json_list(path):
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return []


def get_weather(location):
    """Fetch weather from wttr.in."""
    try:
        import requests
        url = f"https://wttr.in/{location}?format=j1"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        
        current = data['current_condition'][0]
        today = data['weather'][0]
        
        return {
            'temp_c': current['temp_C'],
            'temp_f': current['temp_F'],
            'feels_c': current['FeelsLikeC'],
            'desc': current['weatherDesc'][0]['value'],
            'humidity': current['humidity'],
            'wind_kmph': current['windspeedKmph'],
            'high_c': today['maxtempC'],
            'low_c': today['mintempC'],
            'uv': current.get('uvIndex', 'N/A'),
            'forecast': [
                {
                    'date': day['date'],
                    'high': day['maxtempC'],
                    'low': day['mintempC'],
                    'desc': day['hourly'][4]['weatherDesc'][0]['value']  # midday
                }
                for day in data['weather'][:3]
            ]
        }
    except Exception as e:
        return {'error': str(e)}


def get_news(topics, region='US'):
    """Fetch news from Google News RSS."""
    try:
        import requests
        from bs4 import BeautifulSoup
        
        headlines = []
        for topic in topics[:2]:  # limit to 2 topics
            try:
                url = f"https://news.google.com/rss/search?q={topic}&hl=en&gl={region}&ceid={region}:en"
                resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
                soup = BeautifulSoup(resp.content, 'xml')
                for item in soup.find_all('item', limit=4):
                    title = item.title.text if item.title else ''
                    if title:
                        headlines.append({
                            'title': title[:120],
                            'topic': topic,
                            'date': item.pubDate.text if item.pubDate else ''
                        })
            except Exception:
                pass
        
        return headlines
    except ImportError:
        return []


def get_market_data(symbols):
    """Fetch market data from Yahoo Finance."""
    try:
        import yfinance as yf
        
        results = []
        for sym in symbols:
            try:
                t = yf.Ticker(sym)
                hist = t.history(period="2d")
                if len(hist) >= 2:
                    current = hist['Close'].iloc[-1]
                    prev = hist['Close'].iloc[-2]
                    change_pct = ((current - prev) / prev) * 100
                    results.append({
                        'symbol': sym,
                        'price': round(current, 2),
                        'change_pct': round(change_pct, 2),
                        'up': change_pct >= 0
                    })
            except Exception:
                pass
        
        return results
    except ImportError:
        return []


def get_todays_tasks():
    """Get tasks due today or overdue."""
    tasks = load_json_list(TASKS_FILE)
    if not tasks:
        return []
    
    today = datetime.now().strftime('%Y-%m-%d')
    relevant = []
    
    for t in tasks:
        due = t.get('due', '')
        if due <= today or not due:
            relevant.append(t)
    
    # Sort: overdue first, then by priority
    priority_order = {'high': 0, 'medium': 1, 'low': 2}
    relevant.sort(key=lambda x: (
        0 if x.get('due', '') < today else 1,  # overdue first
        priority_order.get(x.get('priority', 'low'), 3)
    ))
    
    return relevant


def get_todays_events():
    """Get today's events."""
    events = load_json_list(EVENTS_FILE)
    today = datetime.now().strftime('%Y-%m-%d')
    return [e for e in events if e.get('date', '') == today]


def format_briefing(config, weather, news, markets, tasks, events, short=False):
    """Format the briefing."""
    now = datetime.now()
    day_name = now.strftime('%A')
    date_str = now.strftime('%B %d, %Y')
    
    if short:
        parts = [f"☀️ {day_name}, {date_str}"]
        
        if weather and 'error' not in weather:
            parts.append(f"🌤️ {weather['temp_c']}°C, {weather['desc']}")
        
        if markets:
            btc = next((m for m in markets if 'BTC' in m['symbol']), None)
            if btc:
                arrow = '📈' if btc['up'] else '📉'
                parts.append(f"{arrow} BTC ${btc['price']:,.0f} ({btc['change_pct']:+.1f}%)")
        
        if tasks:
            parts.append(f"📋 {len(tasks)} task(s)")
        
        if news:
            parts.append(f"📰 {news[0]['title'][:60]}")
        
        return ' | '.join(parts)
    
    lines = [
        f"\n{'═'*55}",
        f"  ☀️  DAILY BRIEFING — {day_name}, {date_str}",
        f"{'═'*55}",
    ]
    
    # Weather
    if weather and 'error' not in weather:
        lines.extend([
            f"",
            f"  🌤️  WEATHER — {config.get('location', 'Unknown')}",
            f"  {'─'*40}",
            f"  Now: {weather['temp_c']}°C ({weather['temp_f']}°F) — {weather['desc']}",
            f"  Feels like: {weather['feels_c']}°C | Humidity: {weather['humidity']}%",
            f"  High: {weather['high_c']}°C | Low: {weather['low_c']}°C",
        ])
        if weather.get('forecast'):
            lines.append(f"  Forecast:")
            for day in weather['forecast'][:3]:
                lines.append(f"    {day['date']}: {day['high']}°/{day['low']}° — {day['desc']}")
    elif weather and 'error' in weather:
        lines.append(f"\n  🌤️  Weather: ⚠️ Could not fetch ({weather['error']})")
    
    # Markets
    if markets:
        lines.extend([
            f"",
            f"  📈  MARKETS",
            f"  {'─'*40}",
        ])
        
        # Group by type
        crypto = [m for m in markets if '-USD' in m['symbol']]
        stocks = [m for m in markets if '-USD' not in m['symbol'] and '=' not in m['symbol']]
        forex = [m for m in markets if '=' in m['symbol']]
        
        if crypto:
            lines.append(f"  Crypto:")
            for m in crypto:
                arrow = '🟢' if m['up'] else '🔴'
                lines.append(f"    {arrow} {m['symbol']:12s} ${m['price']:>12,.2f}  ({m['change_pct']:+.1f}%)")
        
        if stocks:
            lines.append(f"  Indices/Stocks:")
            for m in stocks:
                arrow = '🟢' if m['up'] else '🔴'
                lines.append(f"    {arrow} {m['symbol']:12s} ${m['price']:>12,.2f}  ({m['change_pct']:+.1f}%)")
        
        if forex:
            lines.append(f"  Forex:")
            for m in forex:
                arrow = '🟢' if m['up'] else '🔴'
                lines.append(f"    {arrow} {m['symbol']:12s}  {m['price']:>12.4f}  ({m['change_pct']:+.2f}%)")
    
    # News
    if news:
        lines.extend([
            f"",
            f"  📰  TOP NEWS",
            f"  {'─'*40}",
        ])
        for i, article in enumerate(news[:5], 1):
            lines.append(f"  {i}. {article['title']}")
    
    # Tasks
    if tasks:
        lines.extend([
            f"",
            f"  📋  TODAY'S TASKS ({len(tasks)})",
            f"  {'─'*40}",
        ])
        today = datetime.now().strftime('%Y-%m-%d')
        for t in tasks[:8]:
            due = t.get('due', '')
            priority = t.get('priority', 'low')
            p_emoji = {'high': '🔴', 'medium': '🟡', 'low': '⚪'}.get(priority, '⚪')
            overdue = ' ⚠️ OVERDUE' if due and due < today else ''
            due_str = f" (due: {due})" if due else ''
            lines.append(f"  {p_emoji} {t['task']}{due_str}{overdue}")
    
    # Events
    if events:
        lines.extend([
            f"",
            f"  🎂  TODAY'S EVENTS ({len(events)})",
            f"  {'─'*40}",
        ])
        for e in events:
            lines.append(f"  🎯 {e.get('event', e.get('title', 'Event'))}")
    
    # If nothing loaded
    if not any([weather, news, markets, tasks, events]):
        lines.extend([
            f"",
            f"  ℹ️  Configure your briefing at {CONFIG_FILE}",
            f"  Add tasks to {TASKS_FILE}",
            f"  Add events to {EVENTS_FILE}",
        ])
    
    lines.append(f"\n{'═'*55}")
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Daily Briefing')
    parser.add_argument('--short', action='store_true', help='Compact output')
    parser.add_argument('--json', action='store_true', help='JSON output')
    parser.add_argument('--weather', action='store_true', help='Weather only')
    parser.add_argument('--news', action='store_true', help='News only')
    parser.add_argument('--crypto', action='store_true', help='Crypto only')
    parser.add_argument('--tasks', action='store_true', help='Tasks only')
    parser.add_argument('--location', help='Override location')
    args = parser.parse_args()
    
    config = load_config()
    if args.location:
        config['location'] = args.location
    
    # Fetch all data
    weather = get_weather(config['location'])
    news = get_news(config['news_topics'], config.get('news_region', 'US'))
    
    all_symbols = config.get('crypto', []) + config.get('stocks', []) + config.get('forex', [])
    markets = get_market_data(all_symbols)
    
    tasks = get_todays_tasks()
    events = get_todays_events()
    
    # Filter if specific section requested
    section = None
    if args.weather: section = 'weather'
    elif args.news: section = 'news'
    elif args.crypto: section = 'crypto'
    elif args.tasks: section = 'tasks'
    
    if section == 'weather':
        news, markets, tasks, events = [], [], [], []
    elif section == 'news':
        weather, markets, tasks, events = None, [], [], []
    elif section == 'crypto':
        weather, news, tasks, events = None, [], [], []
        markets = [m for m in markets if '-USD' in m['symbol']]
    elif section == 'tasks':
        weather, news, markets, events = None, [], [], []
    
    if args.json:
        result = {
            'date': datetime.now().isoformat(),
            'weather': weather,
            'news': news,
            'markets': markets,
            'tasks': tasks,
            'events': events
        }
        print(json.dumps(result, indent=2, default=str))
    else:
        print(format_briefing(config, weather, news, markets, tasks, events, short=args.short))


if __name__ == '__main__':
    main()
