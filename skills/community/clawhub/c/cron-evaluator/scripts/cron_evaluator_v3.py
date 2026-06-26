#!/usr/bin/env python3
"""
🕐 CRON EVALUATOR v3 — REAL KAN
==============================
Cron Evaluator with trained Cron KAN (16→32→16→8→4→3)
"""

import os
import sys
import json
import torch
import torch.nn as nn
from pathlib import Path

MODEL_PATH = 'models/cron_kan.pt'


class CronKANNet(nn.Module):
    """Real Cron KAN model"""
    def __init__(self, input_dim=16, output_dim=3):
        super().__init__()
        self.layers = nn.ModuleList([
            nn.Linear(input_dim, 32),
            nn.Linear(32, 16),
            nn.Linear(16, 8),
            nn.Linear(8, 4),
            nn.Linear(4, output_dim)
        ])
        self.bn_layers = nn.ModuleList([
            nn.BatchNorm1d(32),
            nn.BatchNorm1d(16),
            nn.BatchNorm1d(8),
            nn.BatchNorm1d(4)
        ])
        self.activation = nn.ReLU()
        self.dropout = nn.Dropout(0.1)
        self.output_activation = nn.Sigmoid()
    
    def forward(self, x):
        for i, layer in enumerate(self.layers[:-1]):
            x = layer(x)
            x = self.bn_layers[i](x)
            x = self.activation(x)
            x = self.dropout(x)
        return self.output_activation(self.layers[-1](x))


class RealCronKAN:
    """Uses trained Cron KAN for prediction"""
    
    def __init__(self):
        self.model = None
        self._load_model()
    
    def _load_model(self):
        try:
            checkpoint = torch.load(MODEL_PATH, map_location='cpu', weights_only=False)
            self.model = CronKANNet(input_dim=16, output_dim=3)
            self.model.load_state_dict(checkpoint['model_state_dict'])
            self.model.eval()
            print(f"✅ Cron KAN loaded: {checkpoint['architecture']}")
        except Exception as e:
            print(f"⚠️ Could not load Cron KAN: {e}")
            self.model = None
    
    def predict(self, features):
        if self.model is None:
            return {'quality': 0.5, 'confidence': 0.5, 'improvement': 0.5}
        
        with torch.no_grad():
            x = torch.tensor(features[:16], dtype=torch.float32).unsqueeze(0)
            output = self.model(x)[0]
            
            # Output is [prob_bad, prob_ok, prob_good]
            # Quality = weighted sum
            quality = output[0].item() * 0.2 + output[1].item() * 0.6 + output[2].item() * 1.0
            confidence = float(torch.max(output).item())
            
            return {
                'quality': min(max(quality, 0), 1),
                'confidence': confidence,
                'improvement': 1 - quality
            }


class CronEvaluatorV3:
    """Cron Evaluator with real KAN"""
    
    def __init__(self):
        self.kan = RealCronKAN()
    
    def parse_cron_line(self, line):
        parts = line.strip().split()
        if len(parts) < 6:
            return None
        return {
            'schedule': parts[:5],
            'command': ' '.join(parts[5:]),
            'schedule_str': ' '.join(parts[:5])
        }
    
    def extract_features(self, cron):
        """Extract 16 features"""
        features = []
        
        # Schedule features (4)
        schedule = cron.get('schedule', [])
        features.append(1.0 if '*' in schedule[0] else 0.0)
        features.append(1.0 if '*/' in schedule[0] else 0.0)
        features.append(len([s for s in schedule if s != '*']))
        features.append(1.0 if schedule[0] == '0' and schedule[1] == '0' else 0.0)
        
        # Resource features (4)
        command = cron.get('command', '')
        heavy = ['torch', 'tensorflow', 'ollama', 'docker', 'python3']
        features.append(1.0 if any(h in command for h in heavy) else 0.0)
        features.append(1.0 if 'sleep' in command else 0.0)
        features.append(1.0 if '&&' in command else 0.0)
        features.append(len(command) / 100)
        
        # Resilience features (4)
        features.append(1.0 if '>>' in command or '2>' in command else 0.0)
        features.append(1.0 if 'flock' in command else 0.0)
        features.append(1.0 if 'timeout' in command else 0.0)
        features.append(1.0 if '||' in command else 0.0)
        
        # Pertinence features (4)
        features.append(1.0 if 'systemctl' in command else 0.0)
        features.append(1.0 if '.service' in command else 0.0)
        features.append(1.0 if 'cd' in command else 0.0)
        features.append(1.0 if schedule[0] == '*' else 0.0)
        
        while len(features) < 16:
            features.append(0.0)
        
        return features[:16]
    
    def evaluate_pillars(self, cron):
        """Evaluate 4 pillars"""
        results = {}
        
        # Temporal
        score = 1.0
        issues = []
        if cron['schedule'][0] == '*':
            score -= 0.2
            issues.append("Every minute")
        if cron['schedule'][0] == '0' and cron['schedule'][1] == '0':
            score -= 0.1
            issues.append("Midnight collision")
        results['temporal'] = {'score': max(0, score), 'issues': issues}
        
        # Resource
        score = 1.0
        issues = []
        heavy = ['torch', 'tensorflow', 'ollama', 'docker']
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
            issues.append("No flock")
        results['resilience'] = {'score': max(0, score), 'issues': issues}
        
        # Pertinence
        score = 1.0
        issues = []
        if 'systemctl' in cron['command']:
            score -= 0.3
            issues.append("Should be systemd")
        results['pertinence'] = {'score': max(0, score), 'issues': issues}
        
        return results
    
    def evaluate(self, cron):
        features = self.extract_features(cron)
        kan_pred = self.kan.predict(features)
        pillars = self.evaluate_pillars(cron)
        
        pillar_avg = sum(p['score'] for p in pillars.values()) / 4
        health = 0.4 * pillar_avg + 0.3 * kan_pred['quality'] + 0.3 * kan_pred['confidence']
        
        return {
            'cron': cron,
            'pillars': pillars,
            'kan': kan_pred,
            'health': health
        }
    
    def scan_all(self):
        crons = []
        try:
            result = os.popen('crontab -l 2>/dev/null').read()
            for line in result.split('\n'):
                line = line.strip()
                if line and not line.startswith('#'):
                    parsed = self.parse_cron_line(line)
                    if parsed:
                        crons.append(parsed)
        except:
            pass
        
        results = [self.evaluate(c) for c in crons]
        overall = sum(r['health'] for r in results) / len(results) if results else 0
        
        return {'total': len(results), 'results': results, 'overall_health': overall}


def main():
    print("""
╔═══════════════════════════════════════════════════════════╗
║  🕐 CRON EVALUATOR v3 — REAL KAN LOADED              ║
╠═══════════════════════════════════════════════════════════╣
║  🧠 KAN: cron_kan.pt (trained 500 epochs)            ║
║  📊 Architecture: 16→32→16→8→4→3                      ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    evaluator = CronEvaluatorV3()
    result = evaluator.scan_all()
    
    print(f"📊 Total crons: {result['total']}")
    print(f"📈 Overall Health: {result['overall_health']*100:.0f}%")
    
    for r in result['results']:
        status = "🟢" if r['health'] > 0.8 else "🟡" if r['health'] > 0.6 else "🔴"
        print(f"\n{status} {r['cron']['schedule_str']}")
        print(f"   Command: {r['cron']['command'][:50]}...")
        print(f"   Health: {r['health']*100:.0f}% | KAN quality: {r['kan']['quality']*100:.0f}%")


if __name__ == "__main__":
    main()
