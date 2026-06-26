#!/usr/bin/env python3
"""
Assumption Network Builder and Analyzer

Builds a Bayesian network of assumptions and performs inference.
"""

import argparse
import json
import sys
from collections import defaultdict

class AssumptionNetwork:
    def __init__(self):
        self.nodes = {}  # axiom_id -> {'name': str, 'prior': float, 'type': str}
        self.edges = []  # (parent_id, child_id, strength)
        self.children = defaultdict(list)
        self.parents = defaultdict(list)
    
    def add_node(self, node_id, name, prior, node_type='assumption'):
        """Add a node to the network."""
        self.nodes[node_id] = {
            'name': name,
            'prior': prior,
            'type': node_type,
            'posterior': prior
        }
    
    def add_edge(self, parent_id, child_id, strength=1.0):
        """Add a directed edge from parent to child."""
        self.edges.append((parent_id, child_id, strength))
        self.children[parent_id].append(child_id)
        self.parents[child_id].append(parent_id)
    
    def compute_posterior(self, evidence):
        """
        Compute posterior probabilities given evidence.
        Simple approximation using Bayesian updating.
        """
        # Reset to priors
        for node_id in self.nodes:
            self.nodes[node_id]['posterior'] = self.nodes[node_id]['prior']
        
        # Process evidence
        for node_id, value in evidence.items():
            if node_id in self.nodes:
                self.nodes[node_id]['posterior'] = value
        
        # Simple belief propagation (1 iteration for simplicity)
        for _ in range(2):
            # Forward propagation
            for parent_id in list(self.nodes.keys()):
                parent_posterior = self.nodes[parent_id]['posterior']
                
                for child_id in self.children[parent_id]:
                    # Find edge strength
                    strength = 1.0
                    for p, c, s in self.edges:
                        if p == parent_id and c == child_id:
                            strength = s
                            break
                    
                    # Update child posterior
                    child_prior = self.nodes[child_id]['prior']
                    child_posterior = self.nodes[child_id]['posterior']
                    
                    # Bayesian update: P(child) += strength * P(parent)
                    new_posterior = child_posterior + strength * (parent_posterior - child_prior)
                    self.nodes[child_id]['posterior'] = max(0, min(1, new_posterior))
    
    def get_sensitivity(self, target_id):
        """
        Compute sensitivity of target node to all other nodes.
        Returns dict of node_id -> sensitivity_score
        """
        sensitivity = {}
        target_posterior = self.nodes[target_id]['posterior']
        
        for node_id in self.nodes:
            if node_id == target_id:
                continue
            
            # Temporarily change node's posterior by ±0.1
            original_posterior = self.nodes[node_id]['posterior']
            
            # +0.1 perturbation
            self.nodes[node_id]['posterior'] = min(1.0, original_posterior + 0.1)
            self.compute_posterior({})
            posterior_plus = self.nodes[target_id]['posterior']
            
            # -0.1 perturbation
            self.nodes[node_id]['posterior'] = max(0.0, original_posterior - 0.1)
            self.compute_posterior({})
            posterior_minus = self.nodes[target_id]['posterior']
            
            # Reset
            self.nodes[node_id]['posterior'] = original_posterior
            self.compute_posterior({})
            
            # Sensitivity = |∂target/∂node| ≈ |(post_plus - post_minus) / 0.2|
            sensitivity[node_id] = abs(posterior_plus - posterior_minus) / 0.2
        
        return sensitivity
    
    def get_network_summary(self):
        """Get summary statistics about the network."""
        return {
            'total_nodes': len(self.nodes),
            'total_edges': len(self.edges),
            'root_nodes': len([n for n in self.nodes if not self.parents[n]]),
            'leaf_nodes': len([n for n in self.nodes if not self.children[n]]),
            'avg_children': sum(len(self.children[n]) for n in self.nodes) / len(self.nodes) if self.nodes else 0,
            'avg_parents': sum(len(self.parents[n]) for n in self.nodes) / len(self.nodes) if self.nodes else 0
        }

def main():
    parser = argparse.ArgumentParser(description='Build and analyze assumption network')
    parser.add_argument('--json', help='Input JSON file with network structure')
    parser.add_argument('--evidence', help='Evidence JSON file (node_id: value)')
    parser.add_argument('--sensitivity', help='Target node ID for sensitivity analysis')
    parser.add_argument('--output', choices=['text', 'json'], default='text', help='Output format')
    
    args = parser.parse_args()
    
    if not args.json:
        parser.print_help()
        sys.exit(1)
    
    # Load network
    with open(args.json, 'r') as f:
        data = json.load(f)
    
    network = AssumptionNetwork()
    
    # Add nodes
    for node_data in data.get('nodes', []):
        network.add_node(
            node_data['id'],
            node_data['name'],
            node_data.get('prior', 0.5),
            node_data.get('type', 'assumption')
        )
    
    # Add edges
    for edge_data in data.get('edges', []):
        network.add_edge(
            edge_data['parent'],
            edge_data['child'],
            edge_data.get('strength', 1.0)
        )
    
    # Apply evidence if provided
    evidence = {}
    if args.evidence:
        with open(args.evidence, 'r') as f:
            evidence_data = json.load(f)
            # Convert string keys to appropriate format
            for k, v in evidence_data.items():
                evidence[k] = v
        
        network.compute_posterior(evidence)
    
    # Prepare output
    result = {
        'summary': network.get_network_summary(),
        'nodes': []
    }
    
    for node_id, node in network.nodes.items():
        result['nodes'].append({
            'id': node_id,
            'name': node['name'],
            'prior': node['prior'],
            'posterior': node['posterior'],
            'type': node['type'],
            'children': network.children[node_id],
            'parents': network.parents[node_id]
        })
    
    # Sensitivity analysis if requested
    if args.sensitivity and args.sensitivity in network.nodes:
        sensitivity = network.get_sensitivity(args.sensitivity)
        result['sensitivity'] = {
            'target': args.sensitivity,
            'sensitivities': sensitivity
        }
    
    if args.output == 'json':
        print(json.dumps(result, indent=2))
    else:
        print(f"\n{'='*80}")
        print("ASSUMPTION NETWORK ANALYSIS")
        print(f"{'='*80}\n")
        
        summary = result['summary']
        print(f"Network Summary:")
        print(f"  Total nodes: {summary['total_nodes']}")
        print(f"  Total edges: {summary['total_edges']}")
        print(f"  Root nodes: {summary['root_nodes']}")
        print(f"  Leaf nodes: {summary['leaf_nodes']}")
        print(f"  Avg children per node: {summary['avg_children']:.2f}")
        print(f"  Avg parents per node: {summary['avg_parents']:.2f}\n")
        
        print("Node Status:")
        print(f"{'ID':<15} {'Name':<30} {'Prior':<10} {'Posterior':<10} {'Type':<15}")
        print("-" * 80)
        
        for node in result['nodes']:
            print(f"{node['id']:<15} {node['name'][:28]:<30} "
                  f"{node['prior']:<10.3f} {node['posterior']:<10.3f} {node['type']:<15}")
        
        if 'sensitivity' in result:
            print(f"\nSensitivity Analysis (target: {result['sensitivity']['target']}):")
            print(f"{'Node':<15} {'Name':<30} {'Sensitivity':<15}")
            print("-" * 80)
            
            # Sort by sensitivity
            sorted_sens = sorted(result['sensitivity']['sensitivities'].items(),
                                key=lambda x: x[1], reverse=True)
            
            for node_id, sens in sorted_sens:
                if sens > 0.01:  # Only show non-negligible sensitivities
                    node_name = network.nodes[node_id]['name']
                    print(f"{node_id:<15} {node_name[:28]:<30} {sens:<15.4f}")

if __name__ == "__main__":
    main()
