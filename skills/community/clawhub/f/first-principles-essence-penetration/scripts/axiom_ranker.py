#!/usr/bin/env python3
"""
Axiom Ranker using Information-Theoretic Metrics

Ranks axioms by their information content, independence, and discriminative power.
"""

import argparse
import json
import math
import sys

def shannon_entropy(probability):
    """
    Calculate Shannon entropy for a binary probability.
    H(p) = -p*log2(p) - (1-p)*log2(1-p)
    """
    if probability <= 0 or probability >= 1:
        return 0.0
    return -probability * math.log2(probability) - (1 - probability) * math.log2(1 - probability)

def mutual_information(p_x, p_y, p_xy):
    """
    Calculate mutual information between two binary variables.
    I(X;Y) = H(X) + H(Y) - H(X,Y)
    """
    h_x = shannon_entropy(p_x)
    h_y = shannon_entropy(p_y)
    
    # Joint entropy for binary variables
    p_x_y = p_xy
    p_x_noty = p_x - p_xy
    p_notx_y = p_y - p_xy
    p_notx_noty = 1 - p_x - p_y + p_xy
    
    h_xy = 0
    for p in [p_x_y, p_x_noty, p_notx_y, p_notx_noty]:
        if 0 < p < 1:
            h_xy -= p * math.log2(p)
    
    return h_x + h_y - h_xy

def kl_divergence(p_posterior, p_prior):
    """
    Calculate KL divergence from prior to posterior.
    D_KL(P||Q) = P * log2(P/Q) + (1-P) * log2((1-P)/(1-Q))
    """
    if p_prior <= 0 or p_prior >= 1 or p_posterior <= 0 or p_posterior >= 1:
        return 0.0
    return (p_posterior * math.log2(p_posterior / p_prior) +
            (1 - p_posterior) * math.log2((1 - p_posterior) / (1 - p_prior)))

def calculate_axiom_scores(axioms, dependencies, success_data):
    """
    Calculate multiple scores for each axiom.
    
    axioms: dict of axiom_id -> {'name': str, 'confidence': float}
    dependencies: list of (axiom_i, axiom_j, correlation) tuples
    success_data: dict of case_id -> {'axioms_used': [axiom_ids], 'success': bool}
    """
    scores = {}
    
    # 1. Information Content (Entropy)
    for axiom_id, axiom in axioms.items():
        confidence = axiom.get('confidence', 0.5)
        entropy = shannon_entropy(confidence)
        scores[axiom_id] = {
            'information_content': 1 - entropy,  # Lower entropy = higher score
            'entropy': entropy
        }
    
    # 2. Independence (based on mutual information with other axioms)
    for axiom_id in axioms:
        # Calculate average mutual information with other axioms
        mi_sum = 0
        count = 0
        for dep_i, dep_j, correlation in dependencies:
            if dep_i == axiom_id:
                # Approximate mutual information using correlation
                mi_sum += abs(correlation)
                count += 1
            elif dep_j == axiom_id:
                mi_sum += abs(correlation)
                count += 1
        
        if count > 0:
            avg_mi = mi_sum / count
            # Lower mutual information = more independent = higher score
            scores[axiom_id]['independence'] = 1 - min(avg_mi, 1)
        else:
            scores[axiom_id]['independence'] = 1.0  # No dependencies = fully independent
    
    # 3. Discriminative Power (for success prediction)
    for axiom_id in axioms:
        # Calculate P(success | axiom) vs P(success | no_axiom)
        cases_with = []
        cases_without = []
        
        for case_id, case in success_data.items():
            axioms_used = case.get('axioms_used', [])
            success = case.get('success', False)
            
            if axiom_id in axioms_used:
                cases_with.append(success)
            else:
                cases_without.append(success)
        
        if len(cases_with) > 0 and len(cases_without) > 0:
            p_success_with = sum(cases_with) / len(cases_with)
            p_success_without = sum(cases_without) / len(cases_without)
            
            # Discriminatory power = |P(success|axiom) - P(success|no_axiom)|
            scores[axiom_id]['discriminative_power'] = abs(p_success_with - p_success_without)
        else:
            scores[axiom_id]['discriminative_power'] = 0.0
    
    # 4. Calculate composite score
    weights = {
        'information_content': 0.3,
        'independence': 0.3,
        'discriminative_power': 0.4
    }
    
    for axiom_id in axioms:
        composite = (
            weights['information_content'] * scores[axiom_id]['information_content'] +
            weights['independence'] * scores[axiom_id]['independence'] +
            weights['discriminative_power'] * scores[axiom_id]['discriminative_power']
        )
        scores[axiom_id]['composite_score'] = composite
    
    return scores

def main():
    parser = argparse.ArgumentParser(description='Rank axioms by information-theoretic metrics')
    parser.add_argument('--json', help='Input JSON file with axioms and dependencies')
    parser.add_argument('--output', choices=['text', 'json'], default='text', help='Output format')
    parser.add_argument('--sort-by', choices=['composite', 'information', 'independence', 'discriminative'], 
                        default='composite', help='Sort by which metric')
    
    args = parser.parse_args()
    
    if not args.json:
        parser.print_help()
        sys.exit(1)
    
    with open(args.json, 'r') as f:
        data = json.load(f)
    
    axioms = data.get('axioms', {})
    dependencies = data.get('dependencies', [])
    success_data = data.get('success_data', {})
    
    # Calculate scores
    scores = calculate_axiom_scores(axioms, dependencies, success_data)
    
    # Sort by selected metric
    sort_key = {
        'composite': 'composite_score',
        'information': 'information_content',
        'independence': 'independence',
        'discriminative': 'discriminative_power'
    }[args.sort_by]
    
    sorted_axioms = sorted(scores.items(), key=lambda x: x[1][sort_key], reverse=True)
    
    # Prepare output
    result = {
        'axioms': []
    }
    
    for axiom_id, score in sorted_axioms:
        axiom_name = axioms[axiom_id].get('name', axiom_id)
        result['axioms'].append({
            'id': axiom_id,
            'name': axiom_name,
            'composite_score': round(score['composite_score'], 3),
            'information_content': round(score['information_content'], 3),
            'independence': round(score['independence'], 3),
            'discriminative_power': round(score['discriminative_power'], 3),
            'entropy': round(score['entropy'], 3),
            'confidence': axioms[axiom_id].get('confidence', 0.5)
        })
    
    result['sort_by'] = args.sort_by
    
    if args.output == 'json':
        print(json.dumps(result, indent=2))
    else:
        print(f"\n{'='*80}")
        print(f"AXIOM RANKING (sorted by {args.sort_by})")
        print(f"{'='*80}\n")
        
        headers = ['Rank', 'Axiom', 'Composite', 'Info', 'Indep', 'Disc', 'Conf']
        print(f"{headers[0]:<6} {headers[1]:<30} {headers[2]:<10} {headers[3]:<8} {headers[4]:<8} {headers[5]:<8} {headers[6]:<8}")
        print("-" * 80)
        
        for i, (axiom_id, score) in enumerate(sorted_axioms, 1):
            axiom_name = axioms[axiom_id].get('name', axiom_id)
            print(f"{i:<6} {axiom_name[:28]:<30} "
                  f"{score['composite_score']:<10.3f} "
                  f"{score['information_content']:<8.3f} "
                  f"{score['independence']:<8.3f} "
                  f"{score['discriminative_power']:<8.3f} "
                  f"{axioms[axiom_id].get('confidence', 0.5):<8.2f}")
        
        print("\nLegend:")
        print("  Composite: Weighted sum of all metrics")
        print("  Info: Information content (lower entropy = higher)")
        print("  Indep: Independence (lower mutual information = higher)")
        print("  Disc: Discriminative power for success prediction")
        print("  Conf: Prior confidence in axiom")

if __name__ == "__main__":
    main()
