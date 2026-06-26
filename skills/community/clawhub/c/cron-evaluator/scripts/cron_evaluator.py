#!/usr/bin/env python3
"""
🕐 CRON EVALUATOR — Axioma Cluster
===================================
Analyse les crons pour: collisions, ressources, résilience, pertinence

Usage:
    python3 cron_evaluator.py --scan
    python3 cron_evaluator.py --health
    python3 cron_evaluator.py --suggest
"""

import argparse
import sys
import os
import re
from datetime import datetime, timedelta
from pathlib import Path


class CronEvaluator:
    """Évalue les crons selon 4 piliers"""
    
    def __init__(self):
        self.pillars = {
            'temporal': 'Détection collisions',
            'resource': 'Signature RAM/CPU',
            'resilience': 'Error handling + logs',
            'pertinence': 'Cron vs systemd vs webhook'
        }
    
    def scan_crontab(self):
        """Scan la crontab actuelle"""
        try:
            result = os.popen('crontab -l 2>/dev/null').read()
            return result if result else ""
        except:
            return ""
    
    def parse_cron_line(self, line):
        """Parse une ligne cron"""
        if not line or line.strip().startswith('#'):
            return None
        
        parts = line.strip().split()
        if len(parts) < 6:
            return None
        
        schedule = parts[:5]
        command = ' '.join(parts[5:])
        
        return {
            'schedule': schedule,
            'command': command,
            'raw': line
        }
    
    def calculate_frequency(self, schedule):
        """Calcule la fréquence d'exécution"""
        minute, hour, day, month, dow = schedule
        
        # Simplified frequency calculation
        if minute.startswith('*/'):
            interval = int(minute[2:])
            return f"every {interval} min"
        elif minute == '*':
            return "every minute"
        elif hour == '*':
            return "hourly"
        elif day == '*' and month == '*':
            return "daily"
        else:
            return "custom"
    
    def detect_temporal_collision(self, cron1, cron2):
        """Détecte collision temporelle"""
        # Simplified: both at 00:00
        if cron1['schedule'][0] == '0' and cron2['schedule'][0] == '0':
            if cron1['schedule'][1] == '0' and cron2['schedule'][1] == '0':
                return True
        return False
    
    def evaluate_pillar(self, cron, pillar):
        """Évalue un pilier"""
        score = 1.0
        issues = []
        
        if pillar == 'temporal':
            # Check if frequent cron on resource-heavy task
            if '*' in cron['schedule'][0] and 'python' in cron['command']:
                score = 0.6
                issues.append("Python script every minute = risk")
            
        elif pillar == 'resource':
            # Check for heavy commands
            heavy = ['torch', 'tensorflow', 'ollama', 'docker']
            if any(h in cron['command'] for h in heavy):
                score = 0.7
                issues.append("Heavy command detected")
        
        elif pillar == 'resilience':
            # Check for logging
            if '>>' not in cron['command'] and '2>' not in cron['command']:
                score = 0.6
                issues.append("No logging redirect")
            
            # Check for flock
            if 'flock' not in cron['command']:
                score *= 0.8
                issues.append("No flock lock")
        
        elif pillar == 'pertinence':
            # Check if should be systemd
            if 'service' in cron['command'] or 'systemctl' in cron['command']:
                score = 0.5
                issues.append("Should be systemd, not cron")
        
        return {'score': score, 'issues': issues}
    
    def evaluate_cron(self, cron):
        """Évalue un cron complet"""
        results = {}
        for pillar in self.pillars:
            results[pillar] = self.evaluate_pillar(cron, pillar)
        
        # Health score
        health = sum(r['score'] for r in results.values()) / len(results)
        
        return {
            'cron': cron,
            'pillars': results,
            'health': health,
            'frequency': self.calculate_frequency(cron['schedule'])
        }
    
    def scan_all(self):
        """Scan tous les crons"""
        crontab = self.scan_crontab()
        lines = crontab.split('\n')
        
        crons = []
        for line in lines:
            parsed = self.parse_cron_line(line)
            if parsed:
                crons.append(parsed)
        
        # Evaluate each
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
    parser = argparse.ArgumentParser(description='Cron Evaluator')
    parser.add_argument('--scan', action='store_true', help='Scan crontab')
    parser.add_argument('--health', action='store_true', help='Show health score')
    parser.add_argument('--suggest', action='store_true', help='Suggest optimizations')
    args = parser.parse_args()
    
    evaluator = CronEvaluator()
    
    if args.scan or args.health or args.suggest:
        result = evaluator.scan_all()
        
        print(f"""
╔═══════════════════════════════════════════════════════════╗
║  🕐 CRON EVALUATOR — Analyse Systémique             ║
╠═══════════════════════════════════════════════════════════╣
║  Total crons: {result['total']}
║  Health Score: {result['overall_health']*100:.0f}%
╚═══════════════════════════════════════════════════════════╝
        """)
        
        for r in result['results']:
            cron = r['cron']
            print(f"\n📋 Command: {cron['command'][:50]}...")
            print(f"   Frequency: {r['frequency']}")
            print(f"   Health: {r['health']*100:.0f}%")
            for pillar, data in r['pillars'].items():
                if data['issues']:
                    print(f"   ⚠️ {pillar}: {', '.join(data['issues'])}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
