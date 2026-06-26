#!/usr/bin/env python3
"""
Drift Guard — Agent Behavior Monitor
Main monitoring engine for detecting personality drift, sycophancy, and capability degradation.

Author: Shadow Rose
License: MIT
"""

import json
import time
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class DriftGuard:
    """
    Core drift detection engine.
    
    Monitors agent behavior metrics over time and calculates drift scores
    against established baselines.
    """
    
    def __init__(self, config: Dict):
        """
        Initialize DriftGuard with configuration.
        
        Args:
            config: Configuration dictionary (see config_example.py)
        """
        self.config = config
        self.baseline = None
        self.history = []
        
        # Load baseline if it exists
        baseline_path = Path(config.get('baseline_file', 'baseline.json'))
        if baseline_path.exists():
            with open(baseline_path, 'r') as f:
                self.baseline = json.load(f)
        
        # Load history if it exists
        history_path = Path(config.get('history_file', 'drift_history.json'))
        if history_path.exists():
            with open(history_path, 'r') as f:
                self.history = json.load(f)
    
    def analyze_text(self, text: str) -> Dict:
        """
        Analyze a text sample and extract behavior metrics.
        
        Args:
            text: The text to analyze (agent response)
            
        Returns:
            Dictionary of extracted metrics
        """
        metrics = {}
        
        # Response length metrics
        metrics['char_count'] = len(text)
        metrics['word_count'] = len(text.split())
        metrics['sentence_count'] = len(re.split(r'[.!?]+', text))
        
        # Average sentence length
        if metrics['sentence_count'] > 0:
            metrics['avg_sentence_length'] = metrics['word_count'] / metrics['sentence_count']
        else:
            metrics['avg_sentence_length'] = 0
        
        # Vocabulary diversity (unique words / total words)
        words = text.lower().split()
        unique_words = set(words)
        if metrics['word_count'] > 0:
            metrics['vocabulary_diversity'] = len(unique_words) / metrics['word_count']
        else:
            metrics['vocabulary_diversity'] = 0
        
        # Sycophancy markers
        sycophancy_patterns = self.config.get('sycophancy_patterns', [])
        metrics['sycophancy_score'] = self._count_patterns(text, sycophancy_patterns)
        
        # Hedging language
        hedging_patterns = self.config.get('hedging_patterns', [])
        metrics['hedging_score'] = self._count_patterns(text, hedging_patterns)
        
        # Validation language (compliments, agreement)
        validation_patterns = self.config.get('validation_patterns', [])
        metrics['validation_score'] = self._count_patterns(text, validation_patterns)
        
        # Exclamation/emoji usage
        metrics['exclamation_count'] = text.count('!')
        
        # Technical depth indicators
        technical_patterns = self.config.get('technical_patterns', [])
        metrics['technical_score'] = self._count_patterns(text, technical_patterns)
        
        return metrics
    
    def _count_patterns(self, text: str, patterns: List[str]) -> float:
        """
        Count occurrences of patterns in text, normalized by word count.
        
        Args:
            text: Text to search
            patterns: List of regex patterns
            
        Returns:
            Normalized pattern count (0.0 to 1.0+)
        """
        text_lower = text.lower()
        count = 0
        
        for pattern in patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            count += len(matches)
        
        # Normalize by word count
        word_count = len(text.split())
        if word_count > 0:
            return count / word_count
        return 0.0
    
    def calculate_drift(self, current_metrics: Dict) -> Tuple[float, Dict]:
        """
        Calculate drift score comparing current metrics to baseline.
        
        Args:
            current_metrics: Current behavior metrics
            
        Returns:
            Tuple of (drift_score, detailed_differences)
            drift_score: 0.0 = perfect match, 1.0 = completely different
        """
        if not self.baseline:
            return 0.0, {'error': 'No baseline loaded'}
        
        baseline_metrics = self.baseline.get('metrics', {})
        differences = {}
        drift_components = []
        
        # Compare each metric
        for key in baseline_metrics:
            if key not in current_metrics:
                continue
            
            baseline_val = baseline_metrics[key]
            current_val = current_metrics[key]
            
            # Calculate percentage difference
            if baseline_val != 0:
                diff_pct = abs(current_val - baseline_val) / abs(baseline_val)
            else:
                diff_pct = 1.0 if current_val != 0 else 0.0
            
            differences[key] = {
                'baseline': baseline_val,
                'current': current_val,
                'diff_pct': diff_pct
            }
            
            # Weight the difference based on metric importance
            weight = self.config.get('metric_weights', {}).get(key, 1.0)
            drift_components.append(diff_pct * weight)
        
        # Calculate overall drift score (weighted average)
        if drift_components:
            drift_score = sum(drift_components) / len(drift_components)
        else:
            drift_score = 0.0
        
        # Cap at 1.0
        drift_score = min(drift_score, 1.0)
        
        return drift_score, differences
    
    def check_thresholds(self, drift_score: float) -> Optional[str]:
        """
        Check if drift score exceeds configured thresholds.
        
        Args:
            drift_score: Current drift score
            
        Returns:
            Alert level ('warning', 'critical', 'emergency') or None
        """
        thresholds = self.config.get('thresholds', {})
        
        if drift_score >= thresholds.get('emergency', 0.9):
            return 'emergency'
        elif drift_score >= thresholds.get('critical', 0.6):
            return 'critical'
        elif drift_score >= thresholds.get('warning', 0.3):
            return 'warning'
        
        return None
    
    def record_measurement(self, metrics: Dict, drift_score: float, drift_details: Dict):
        """
        Record a drift measurement in history.
        
        Args:
            metrics: Current metrics
            drift_score: Calculated drift score
            drift_details: Detailed drift breakdown
        """
        record = {
            'timestamp': time.time(),
            'datetime': datetime.now().isoformat(),
            'metrics': metrics,
            'drift_score': drift_score,
            'drift_details': drift_details
        }
        
        self.history.append(record)
        
        # Save to file
        history_path = Path(self.config.get('history_file', 'drift_history.json'))
        with open(history_path, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def alert(self, level: str, drift_score: float, drift_details: Dict):
        """
        Trigger alert based on configured alert methods.
        
        Args:
            level: Alert level ('warning', 'critical', 'emergency')
            drift_score: Current drift score
            drift_details: Detailed drift breakdown
        """
        alert_config = self.config.get('alerts', {})
        
        # Log to file
        if alert_config.get('log_file'):
            log_path = Path(alert_config['log_file'])
            with open(log_path, 'a') as f:
                f.write(f"[{datetime.now().isoformat()}] {level.upper()}: Drift score {drift_score:.3f}\n")
                f.write(f"Details: {json.dumps(drift_details, indent=2)}\n\n")
        
        # Write alert file
        if alert_config.get('alert_file'):
            alert_path = Path(alert_config['alert_file'])
            alert_data = {
                'timestamp': time.time(),
                'datetime': datetime.now().isoformat(),
                'level': level,
                'drift_score': drift_score,
                'drift_details': drift_details
            }
            with open(alert_path, 'w') as f:
                json.dump(alert_data, f, indent=2)
        
        # Webhook placeholder
        if alert_config.get('webhook_url'):
            # In production, this would send HTTP POST to webhook
            # For stdlib-only version, just log the intent
            print(f"[ALERT] {level.upper()}: Drift {drift_score:.3f} (webhook: {alert_config['webhook_url']})")
    
    def monitor(self, text: str) -> Dict:
        """
        Main monitoring function. Analyze text, calculate drift, check thresholds, alert if needed.
        
        Args:
            text: Agent response text to analyze
            
        Returns:
            Monitoring result dictionary
        """
        # Analyze the text
        metrics = self.analyze_text(text)
        
        # Calculate drift
        drift_score, drift_details = self.calculate_drift(metrics)
        
        # Record measurement
        self.record_measurement(metrics, drift_score, drift_details)
        
        # Check thresholds and alert
        alert_level = self.check_thresholds(drift_score)
        if alert_level:
            self.alert(alert_level, drift_score, drift_details)
        
        return {
            'drift_score': drift_score,
            'alert_level': alert_level,
            'metrics': metrics,
            'drift_details': drift_details
        }


def main():
    """Example usage."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python drift_guard.py <text_file>")
        print("   or: python drift_guard.py --stdin")
        sys.exit(1)
    
    # Load config
    try:
        from config import CONFIG
    except ImportError:
        print("Error: config.py not found. Copy config_example.py to config.py and customize.")
        sys.exit(1)
    
    # Initialize DriftGuard
    dg = DriftGuard(CONFIG)
    
    # Get text
    if sys.argv[1] == '--stdin':
        text = sys.stdin.read()
    else:
        with open(sys.argv[1], 'r') as f:
            text = f.read()
    
    # Monitor
    result = dg.monitor(text)
    
    # Print results
    print(f"Drift Score: {result['drift_score']:.3f}")
    if result['alert_level']:
        print(f"Alert Level: {result['alert_level'].upper()}")
    print(f"\nMetrics: {json.dumps(result['metrics'], indent=2)}")


if __name__ == '__main__':
    main()
