#!/usr/bin/env python3
"""
Find historical events similar to current market conditions.
Detects rapid price changes, volatility spikes, trend reversals.
"""

import argparse
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple


def calculate_change(df: pd.DataFrame, window_days: int = 90) -> float:
    """Calculate percentage change over a window."""
    if len(df) < window_days:
        return 0.0
    start_price = df['close'].iloc[-window_days]
    end_price = df['close'].iloc[-1]
    return ((end_price - start_price) / start_price) * 100


def calculate_volatility(df: pd.DataFrame, window_days: int = 30) -> float:
    """Calculate rolling volatility (standard deviation of daily returns)."""
    if len(df) < window_days:
        return 0.0
    returns = df['close'].pct_change().dropna()
    return returns.iloc[-window_days:].std() * 100


def detect_rapid_change(df: pd.DataFrame, threshold_pct: float = 20.0, min_window: int = 30, max_window: int = 90) -> List[Dict]:
    """Detect periods of rapid price change in historical data."""
    events = []
    
    for window in range(min_window, min(max_window + 1, len(df))):
        # Rolling window calculation
        for i in range(window, len(df)):
            start_price = df['close'].iloc[i - window]
            end_price = df['close'].iloc[i]
            change_pct = ((end_price - start_price) / start_price) * 100
            
            # Check if change exceeds threshold
            if abs(change_pct) >= threshold_pct:
                start_date = df['date'].iloc[i - window]
                end_date = df['date'].iloc[i]
                
                # Check if this event overlaps with existing ones (merge overlapping)
                is_overlapping = False
                for existing in events:
                    if start_date <= existing['end_date'] and end_date >= existing['start_date']:
                        is_overlapping = True
                        break
                
                if not is_overlapping:
                    events.append({
                        'start_date': start_date,
                        'end_date': end_date,
                        'change_pct': round(change_pct, 2),
                        'direction': 'increase' if change_pct > 0 else 'decrease',
                        'window_days': window,
                        'start_price': round(start_price, 4),
                        'end_price': round(end_price, 4)
                    })
    
    # Sort by absolute change magnitude and return top events
    events.sort(key=lambda x: abs(x['change_pct']), reverse=True)
    return events


def detect_volatility_spike(df: pd.DataFrame, threshold_vol: float = 3.0, window_days: int = 30) -> List[Dict]:
    """Detect periods of elevated volatility."""
    events = []
    returns = df['close'].pct_change().dropna()
    
    for i in range(window_days, len(returns)):
        vol = returns.iloc[i - window_days:i].std() * 100
        
        if vol >= threshold_vol:
            start_date = df['date'].iloc[i - window_days]
            end_date = df['date'].iloc[i]
            
            events.append({
                'start_date': start_date,
                'end_date': end_date,
                'volatility': round(vol, 2),
                'threshold': threshold_vol
            })
    
    # Deduplicate overlapping events
    deduped = []
    for event in events:
        is_overlapping = False
        for existing in deduped:
            if event['start_date'] <= existing['end_date'] and event['end_date'] >= existing['start_date']:
                is_overlapping = True
                break
        if not is_overlapping:
            deduped.append(event)
    
    return deduped


def get_current_event_characteristics(df: pd.DataFrame, lookback_days: int = 90) -> Dict:
    """Extract current event characteristics from recent data."""
    change_90d = calculate_change(df, 90)
    change_60d = calculate_change(df, 60)
    change_30d = calculate_change(df, 30)
    volatility_30d = calculate_volatility(df, 30)
    
    direction = 'increase' if change_90d > 0 else 'decrease'
    
    # Determine event type based on characteristics
    event_type = 'unknown'
    if abs(change_90d) >= 40:
        event_type = 'major_price_move'
    elif abs(change_90d) >= 20:
        event_type = 'rapid_price_change'
    elif volatility_30d >= 3.0:
        event_type = 'high_volatility'
    
    return {
        'change_90d': round(change_90d, 2),
        'change_60d': round(change_60d, 2),
        'change_30d': round(change_30d, 2),
        'volatility_30d': round(volatility_30d, 2),
        'direction': direction,
        'event_type': event_type,
        'current_price': round(df['close'].iloc[-1], 4),
        'current_date': df['date'].iloc[-1]
    }


def find_similar_historical_events(df: pd.DataFrame, current_event: Dict, similarity_threshold: float = 0.5) -> List[Dict]:
    """Find historical events similar to current event characteristics."""
    target_change = abs(current_event['change_90d'])
    target_direction = current_event['direction']
    
    # Find all rapid changes in history
    threshold_pct = target_change * similarity_threshold
    all_events = detect_rapid_change(df, threshold_pct=max(threshold_pct, 10))
    
    # Filter by direction
    similar_events = [e for e in all_events if e['direction'] == target_direction]
    
    # Add similarity score
    for event in similar_events:
        similarity = min(abs(event['change_pct']) / target_change, 1.0)
        event['similarity_score'] = round(similarity, 2)
    
    # Sort by similarity and return top events
    similar_events.sort(key=lambda x: x['similarity_score'], reverse=True)
    
    return similar_events[:10]  # Return top 10 similar events


def main():
    parser = argparse.ArgumentParser(description='Find historical events similar to current conditions')
    parser.add_argument('--data', required=True, help='Input data file (CSV or JSON from fetch_indicator)')
    parser.add_argument('--threshold', type=float, default=20.0, help='Minimum change percentage threshold')
    parser.add_argument('--window-min', type=int, default=30, help='Minimum window days')
    parser.add_argument('--window-max', type=int, default=90, help='Maximum window days')
    parser.add_argument('--output', '-o', help='Output file (JSON)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    # Load data
    if args.data.endswith('.json'):
        with open(args.data, 'r') as f:
            data = json.load(f)
        df = pd.DataFrame(data['data'])
    else:
        df = pd.read_csv(args.data)
    
    # Get current event characteristics
    current_event = get_current_event_characteristics(df)
    print(f"\nCurrent Event Characteristics:")
    print(f"  90-day change: {current_event['change_90d']}% ({current_event['direction']})")
    print(f"  60-day change: {current_event['change_60d']}%")
    print(f"  30-day change: {current_event['change_30d']}%")
    print(f"  30-day volatility: {current_event['volatility_30d']}%")
    print(f"  Event type: {current_event['event_type']}")
    
    # Find similar historical events
    similar_events = find_similar_historical_events(df, current_event)
    
    print(f"\nSimilar Historical Events Found: {len(similar_events)}")
    for i, event in enumerate(similar_events[:5], 1):
        print(f"\n  Event {i}:")
        print(f"    Period: {event['start_date']} to {event['end_date']} ({event['window_days']} days)")
        print(f"    Change: {event['change_pct']}% ({event['direction']})")
        print(f"    Similarity: {event['similarity_score']}")
    
    # Output
    result = {
        'current_event': current_event,
        'similar_events': similar_events
    }
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\nSaved to: {args.output}")
    else:
        if args.json:
            print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()