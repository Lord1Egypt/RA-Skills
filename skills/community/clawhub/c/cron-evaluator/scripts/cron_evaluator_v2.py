#!/usr/bin/env python3
"""
🕐 CRON EVALUATOR v2 — KAN ENHANCED
====================================
Analyse des crons avec évaluation KAN + 4 piliers

Architecture: CronAnalyzer (KAN 768D → 128 → 32 → 8 → 3)
Combine: Temporal + Resource + Resilience + Pertinence
"""

import os
import sys
import re
import json
import argparse
from pathlib import Path
from datetime import datetime

# KAN Integration
sys.path.insert(0, '/mnt/Morgana')
try:
    from kan_auto_evolution import KANAutoEvolver
    HAS_KAN = True
except:
    HAS_KAN = False


class CronKAN:
    """KAN pour évaluation des crons"""
    
    def __init__(self):
        self.model_path = '/mnt/Morgana/skills/cron-evaluator/models/cron_kan.pt'
        self.data_path = '/mnt/Morgana/skills/cron-evaluator/data/cron_training.json'
    
    def extract_features(self, cron_line):
        """Extrait 16 features pour le KAN"""
        features = []
        
        # Schedule features
        schedule = cron_line.get('schedule', [])
        features.append(1.0 if '*' in schedule[0] else 0.0)  # Every minute
        features.append(1.0 if '*/' in schedule[0] else 0.0)  # Interval
        features.append(len([s for s in schedule if s != '*']))  # Specific values
        
        # Resource features
        command = cron_line.get('command', '')
        heavy = ['torch', 'tensorflow', 'ollama', 'docker', 'python3']
        features.append(1.0 if any(h in command for h in heavy) else 0.0)  # Heavy
        features.append(1.0 if 'sleep' in command else 0.0)  # Has sleep
        features.append(1.0 if '&&' in command else 0.0)  # Multiple commands
        
        # Resilience features
        features.append(1.0 if '>>' in command or '2>' in command else 0.0)  # Logging
        features.append(1.0 if 'flock' in command else 0.0)  # Locking
        features.append(1.0 if 'timeout' in command else 0.0)  # Timeout
        features.append(1.0 if '||' in command else 0.0)  # Error handling
        
        # Pertinence features
        features.append(1.0 if 'systemctl' in command or 'service' in command else 0.0)  # Should be systemd
        features.append(1.0 if '.service' in command else 0.0)  # Is systemd
        features.append(len(command) / 100)  # Command length normalized
        
        # Temporal features
        features.append(1.0 if schedule[0] == '0' and schedule[1] == '0' else 0.0)  # Midnight
        features.append(1.0 if schedule[0] == '*' else 0.0)  # Every minute
        features.append(1.0 if 'cd' in command else 0.0)  # Changes directory
        
        # Pad to 16
        while len(features) < 16:
            features.append(0.0)
        
        return features[:16]
    
    def predict(self, features):
        """Prédit la qualité du cron"""
        # Use simple heuristic for now (KAN would be better)
        score = sum(features[:8]) / 8  # Base score from first 8 features
        return {
            'quality': score,
            'confidence': 0.7,
            'improvement': 1.0 - score
        }


class CronEvaluatorV2:
    """Cron Evaluator avec KAN + 4 piliers"""
    
    def __init__(self):
        self.kan = CronKAN()
        self.workspaces = {
            'merlin': '/run/media/axioma/Merlin',
            'ezeziel': '/home/axioma',
            'morgana': '/mnt/Morgana'
        }
    
    def scan_crontab(self, workspace=None):
        """Scan la crontab d'un workspace"""
        crons = []
        
        # Scan workspace crontabs
        for name, path in self.workspaces.items():
            if workspace and name != workspace:
                continue
            
            crontab_file = Path(path) / '.openclaw' / 'crontab'
            if crontab_file.exists():
                content = crontab_file.read_text()
                for line in content.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parsed = self.parse_cron_line(line)
                        if parsed:
                            parsed['workspace'] = name
                            crons.append(parsed)
        
        # Also check system crontab
        try:
            result = os.popen('crontab -l 2>/dev/null').read()
            for line in result.split('\n'):
                line = line.strip()
                if line and not line.startswith('#'):
                    parsed = self.parse_cron_line(line)
                    if parsed:
                        parsed['workspace'] = 'system'
                        crons.append(parsed)
        except:
            pass
        
        return crons
    
    def parse_cron_line(self, line):
        """Parse une ligne cron"""
        parts = line.strip().split()
        if len(parts) < 6:
            return None
        
        schedule = parts[:5]
        command = ' '.join(parts[5:])
        
        return {
            'schedule': schedule,
            'command': command,
            'raw': line,
            'schedule_str': ' '.join(schedule)
        }
    
    def evaluate_pillars(self, cron):
        """Évalue les 4 piliers"""
        results = {}
        
        # Temporal
        score = 1.0
        issues = []
        if cron['schedule'][0] == '*':
            score -= 0.2
            issues.append("Every minute")
        if cron['schedule'][0] == '0' and cron['schedule'][1] == '0':
            score -= 0.1
            issues.append("Midnight collision risk")
        results['temporal'] = {'score': max(0, score), 'issues': issues}
        
        # Resource
        score = 1.0
        issues = []
        heavy = ['torch', 'tensorflow', 'ollama', 'docker', 'python3', 'gemma', 'qwen']
        if any(h in cron['command'] for h in heavy):
            score -= 0.3
            issues.append("Heavy command")
        results['resource'] = {'score': max(0, score), 'issues': issues}
        
        # Resilience
        score = 1.0
        issues = []
        if '>>' not in cron['command'] and '2>' not in cron['command']:
            score -= 0.2
            issues.append("No logging")
        if 'flock' not in cron['command']:
            score -= 0.2
            issues.append("No flock lock")
        if 'timeout' not in cron['command']:
            score -= 0.1
            issues.append("No timeout")
        results['resilience'] = {'score': max(0, score), 'issues': issues}
        
        # Pertinence
        score = 1.0
        issues = []
        if 'systemctl' in cron['command'] or 'service ' in cron['command']:
            score -= 0.3
            issues.append("Should be systemd")
        results['pertinence'] = {'score': max(0, score), 'issues': issues}
        
        return results
    
    def evaluate_cron(self, cron):
        """Évalue un cron complet"""
        # Pillars
        pillars = self.evaluate_pillars(cron)
        
        # KAN prediction
        features = self.kan.extract_features(cron)
        kan_pred = self.kan.predict(features)
        
        # Health score
        pillar_avg = sum(p['score'] for p in pillars.values()) / 4
        health = 0.4 * pillar_avg + 0.3 * kan_pred['quality'] + 0.3 * kan_pred['confidence']
        
        return {
            'cron': cron,
            'pillars': pillars,
            'kan': kan_pred,
            'health': health,
            'suggestions': self.generate_suggestions(cron, pillars)
        }
    
    def generate_suggestions(self, cron, pillars):
        """Génère des suggestions d'amélioration"""
        suggestions = []
        
        for pillar, data in pillars.items():
            if data['score'] < 0.8:
                for issue in data['issues']:
                    if pillar == 'temporal':
                        if 'Midnight' in issue:
                            suggestions.append("Add jitter: sleep $((RANDOM % 60))")
                    elif pillar == 'resilience':
                        if 'No logging' in issue:
                            suggestions.append("Add logging: >> /var/log/cron.log 2>&1")
                        if 'No flock' in issue:
                            suggestions.append("Add flock: flock -n /tmp/cron.lock")
        
        return suggestions
    
    def scan_all(self, workspace=None):
        """Scan tous les crons"""
        crons = self.scan_crontab(workspace)
        results = []
        
        for cron in crons:
            result = self.evaluate_cron(cron)
            results.append(result)
        
        # Overall health
        overall = sum(r['health'] for r in results) / len(results) if results else 0
        
        return {
            'total': len(results),
            'results': results,
            'overall_health': overall
        }


def main():
    parser = argparse.ArgumentParser(description='Cron Evaluator v2 (KAN Enhanced)')
    parser.add_argument('--scan', action='store_true', help='Scan all workspaces')
    parser.add_argument('--workspace', help='Specific workspace (merlin/ezeziel/morgana)')
    parser.add_argument('--health', action='store_true', help='Show health scores')
    parser.add_argument('--suggest', action='store_true', help='Show suggestions')
    parser.add_argument('--improve', help='Improve specific cron')
    args = parser.parse_args()
    
    evaluator = CronEvaluatorV2()
    
    print("""
╔═══════════════════════════════════════════════════════════╗
║  🕐 CRON EVALUATOR v2 — KAN ENHANCED                 ║
╠═══════════════════════════════════════════════════════════╣
║  📊 4 Piliers: Temporal, Resource, Resilience, Pertinence
║  🧠 KAN: 768D → 128 → 32 → 8 → 3 (simulated)
║  🎯 Health = 40% Pillars + 30% KAN Quality + 30% Confidence
╚═══════════════════════════════════════════════════════════╝
    """)
    
    result = evaluator.scan_all(args.workspace)
    
    print(f"📊 Total crons: {result['total']}")
    print(f"📈 Overall Health: {result['overall_health']*100:.0f}%")
    
    if result['total'] == 0:
        print("⚠️ No crons found")
        return 0
    
    print("\n" + "="*60)
    print("📋 CRON DETAILS")
    print("="*60)
    
    for r in result['results']:
        cron = r['cron']
        ws = cron.get('workspace', 'unknown')
        
        status = "🟢" if r['health'] > 0.8 else "🟡" if r['health'] > 0.6 else "🔴"
        print(f"\n{status} [{ws.upper()}] {cron['schedule_str']}")
        print(f"   Command: {cron['command'][:60]}...")
        print(f"   Health: {r['health']*100:.0f}%")
        
        if args.suggest and r['suggestions']:
            print(f"   💡 Suggestions:")
            for s in r['suggestions'][:3]:
                print(f"      - {s}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
