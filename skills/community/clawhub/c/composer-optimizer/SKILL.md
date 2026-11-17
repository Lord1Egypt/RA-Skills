"""
Composer TRADITIONAL_IRA Strategy Optimizer
Mean-variance optimization — no forced cuts, optimizer zeros out weak/redundant.
Outputs: trading_bot/composer_optimized_trad_ira.json
"""
import json, os, numpy as np, pandas as pd
from scipy.optimize import minimize
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(BASE, 'symphony_cache.json')
OUTPUT = os.path.join(BASE, 'dashboard', 'composer_trad_ira_optimized.json')

RISK_FREE = 0.0425  # 4.25% Fed rate
MAX_WEIGHT = 0.15
TRADING_DAYS = 252

def load_strategies():
    with open(CACHE) as f:
        data = json.load(f)
    syms = data.get('symphonies', [])
    if isinstance(syms, dict):
        # Flatten if nested by account
        all_s = []
        for k, v in syms.items():
            if isinstance(v, list):
                all_s.extend(v)
        syms = all_s
    
    print(f'Loaded {len(syms)} symphonies')
    
    # Filter for reasonable strategies
    valid = []
    for s in syms:
        ret = s.get('simple_return', 0) or 0
        val = s.get('value', 0) or 0
        name = s.get('name', '')[:50]
        deposits = s.get('net_deposits', 0) or 0
        
        # Skip zero-value or zero-return with no deposits
        if val <= 1 and deposits <= 1:
            continue
        
        # Estimate Sharpe if we have return (simplified: no returns history in cache)
        # Use return / 15 as a rough annualized Sharpe proxy
        sharpe = max(0, ret * 100 / 15)  # very rough
        
        # Estimate max DD (rough: higher return = potentially higher DD)
        dd = min(50, max(5, abs(ret) * 100 * 0.3))
        
        # Consistency proxy: higher net deposits vs value = more consistent
        
        valid.append({
            'id': s.get('id', ''),
            'name': name,
            'return': ret,
            'value': val,
            'sharpe': round(sharpe, 2),
            'max_dd': round(dd, 1),
        })
    
    print(f'Valid strategies: {len(valid)}')
    return valid


def score_strategies(strategies):
    """Multi-factor scoring"""
    for s in strategies:
        ret_score = s['return'] if s['return'] else 0
        sharpe_score = s['sharpe'] / 5  # normalize
        dd_score = -s['max_dd'] / 100
        consistency = 0.5  # default since we lack monthly data
        
        s['score'] = round(
            0.35 * min(ret_score, 5) +  # cap return influence
            0.35 * sharpe_score +
            0.15 * dd_score +
            0.15 * consistency,
            3
        )
    return sorted(strategies, key=lambda x: x['score'], reverse=True)


def optimize_weights(strategies):
    """Mean-variance optimization for max Sharpe"""
    n = len(strategies)
    if n < 3:
        return strategies  # too few to optimize
    
    # Build synthetic returns for optimization
    # Use return + sharpe to estimate mean and std
    np.random.seed(42)
    returns = np.zeros((60, n))  # 60 months
    for i, s in enumerate(strategies):
        monthly_ret = s['return'] / 12 if s['return'] else 0
        monthly_std = abs(monthly_ret / max(0.01, s['sharpe'])) if s['sharpe'] > 0 else monthly_ret * 2
        returns[:, i] = np.random.normal(monthly_ret, monthly_std, 60)
    
    mean_returns = np.array([max(0, s.get('return', 0) / 12) for s in strategies])
    cov_matrix = np.cov(returns.T)
    
    # Add regularization
    cov_matrix += np.eye(n) * 0.001
    
    def neg_sharpe(weights):
        weights = np.array(weights)
        port_return = np.dot(weights, mean_returns) * 12  # annualize
        port_std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix * 12, weights)))
        if port_std == 0:
            return 999
        return -(port_return - RISK_FREE) / port_std
    
    constraints = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0}]
    bounds = [(0, MAX_WEIGHT) for _ in range(n)]
    
    init = np.array([1.0/n] * n)
    result = minimize(neg_sharpe, init, method='SLSQP', bounds=bounds, constraints=constraints, options={'maxiter': 1000})
    
    if result.success:
        weights = result.x
        # Round and filter
        for i, s in enumerate(strategies):
            s['optimized_weight'] = round(float(weights[i]), 4)
        
        # Mark zeroed-out strategies
        kept = [s for s in strategies if s['optimized_weight'] > 0.001]
        zeroed = [s for s in strategies if s['optimized_weight'] <= 0.001]
        
        print(f'Optimized: {len(kept)} kept, {len(zeroed)} zeroed out')
        
        # Renormalize kept weights
        total = sum(s['optimized_weight'] for s in kept)
        for s in kept:
            s['optimized_weight'] = round(s['optimized_weight'] / total, 4)
        
        return kept, zeroed, float(-result.fun)  # (kept, zeroed, optimal_sharpe)
    else:
        print(f'Optimization failed: {result.message}')
        return strategies, [], 0


def run():
    print('=' * 60)
    print('COMPOSER TRADITIONAL IRA OPTIMIZER')
    print('=' * 60)
    print(f'Risk-free rate: {RISK_FREE*100:.2f}%')
    print(f'Max weight: {MAX_WEIGHT*100:.0f}%')
    print()
    
    # Load
    strategies = load_strategies()
    
    # Score
    scored = score_strategies(strategies)
    
    # Optimize
    kept, zeroed, sharpe = optimize_weights(scored)
    
    # Output
    result = {
        'generated': datetime.now().isoformat(),
        'account': 'TRADITIONAL_IRA',
        'risk_free_rate': RISK_FREE,
        'total_symphonies_before': len(strategies),
        'kept_count': len(kept),
        'zeroed_count': len(zeroed),
        'reduction_pct': round((1 - len(kept)/len(strategies)) * 100, 1),
        'optimal_sharpe': round(sharpe, 2),
        'top_allocation': [],
        'zeroed_out': [s['name'][:40] for s in zeroed[:20]],
    }
    
    for s in kept[:25]:
        alloc_pct = s['optimized_weight'] * 100
        dollar = s['value']
        target_dollar = alloc_pct / 100 * sum(x['value'] for x in kept) if s['value'] else 0
        result['top_allocation'].append({
            'name': s['name'],
            'return': f"{s['return']*100:+.1f}%" if s['return'] else 'N/A',
            'sharpe': s['sharpe'],
            'weight': f"{alloc_pct:.1f}%",
            'current_value': f"${s['value']:,.0f}",
        })
    
    with open(OUTPUT, 'w') as f:
        json.dump(result, f, indent=2)
    
    # Print summary
    print(f'\n{"="*60}')
    print(f'RESULTS')
    print(f'{"="*60}')
    print(f'Before: {len(strategies)} strategies')
    print(f'After:  {len(kept)} kept ({len(zeroed)} zeroed) = {result["reduction_pct"]}% reduction')
    print(f'Optimal Sharpe: {sharpe:.2f}')
    print(f'\nTop 15 Allocations:')
    print(f'{"Strategy":45} {"Weight":>8} {"Return":>8} {"Sharpe":>8}')
    print('-' * 75)
    for s in kept[:15]:
        print(f'{s["name"][:45]:45} {s["optimized_weight"]*100:>7.1f}% {s["return"]*100:>+7.1f}% {s["sharpe"]:>8.2f}')
    
    print(f'\nSaved to: {OUTPUT}')
    return result

if __name__ == '__main__':
    run()