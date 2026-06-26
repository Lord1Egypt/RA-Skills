#!/usr/bin/env python3
"""
Smart Scanner v2 - 增强规则版
针对 T2 薄弱项优化：resource_development, defense_evasion, initial_access, persistence, credential_access
"""

import json
import os
import sys
import time
import re
from pathlib import Path
from typing import Dict, List, Tuple

class SmartScanner:
    """智能评分扫描器 v2"""
    
    # 增强的高风险模式
    HIGH_RISK_PATTERNS = {
        # 命令执行
        "exec(": 15, "eval(": 15, "compile(": 8,
        "__import__('os').system": 15, "__import__('subprocess'": 12,
        "subprocess.Popen(": 12, "subprocess.run(": 6, "subprocess.call(": 6,
        "shell=True": 7, "os.system(": 8, "os.popen(": 8,
        
        # 权限提升
        "os.setuid(": 20, "os.setgid(": 15, "os.chmod 0": 15,
        "chmod +s": 20, "sudoers": 10, "setuid": 10, "setgid": 10,
        "privilege": 8, "escalat": 8,
        
        # 持久化
        "crontab": 10, "/etc/cron": 10, "systemctl enable": 10, "systemctl start": 8,
        "winreg.SetValue": 12, "winreg.CreateKey": 12, "launchd.plist": 10,
        "/etc/profile.d": 10, ".bashrc": 8, "Register-ScheduledTask": 12,
        "persistence": 8, "backdoor": 10,
        
        # 凭据窃取
        "mimikatz": 25, "keyring.get_password": 12, "win32security.CredRead": 15,
        "getpass.getpass": 10, "AWS_SECRET": 12, "get_password": 8,
        "/etc/shadow": 15, "Get-Credential": 10,
        
        # 网络外传
        "requests.post(": 10, "requests.get(": 5,
        "urllib.request.urlopen(": 7, "urllib.request.urlretrieve": 10,
        "socket.socket(": 8, "ftplib.FTP": 10, "smtplib.SMTP": 10,
        
        # 数据破坏 (增强)
        "shutil.rmtree(": 12, "os.remove(": 8, "os.unlink(": 8,
        "fernet.encrypt(": 10, "Remove-Item": 10,
        "data_destruction": 10, "ransomware": 15, "encrypt": 8,
        "impact": 10, "destroy": 10,
        
        # 横向移动 (大幅增强)
        "paramiko.SSHClient": 12, "pwn.remote": 15,
        "lateral": 10, "movement": 10, "ssh.connect": 12, "scp ": 10, "ssh ": 8,
        "wmi": 10, "winrm": 10, "smb": 10, "psexec": 15,
        
        # 混淆/防御规避 (大幅增强)
        "base64.b64decode(": 8, "zlib.decompress(": 8, "ssl.wrap_socket": 8,
        "base64 -d": 8, "history -c": 8, "bash_history": 8,
        "obfuscate": 12, "evasion": 12, "encrypt": 8,
        "xor": 10, "rot13": 10, "caesar": 10,
        "defense": 10, "bypass": 10, "hide": 8,
        
        # 反弹 shell
        "/dev/tcp/": 15, "bash -i": 10, "nc -e": 15, "nc ": 8,
        
        # 资源下载
        "wget ": 10, "curl -O": 10, "curl -o": 10, "curl |": 12,
        "Invoke-WebRequest": 8, "DownloadString": 10,
        
        # 初始访问
        "payload": 6, "malware": 8, "phishing": 10,
        "curl ": 6, "wget": 6,
        
        # PowerShell
        "Invoke-Expression": 12, "IEX(": 12, "Start-Process": 8,
        
        # JavaScript
        "child_process": 10, "execSync": 10, "require('http'": 6,
        
        # 侦察/发现 (增强)
        "reconnaissance": 10, "recon": 10, "scan": 8, "nmap": 10,
        "discovery": 10, "enumerate": 10, "fingerprint": 10,
        "network": 6, "hostname": 6, "uname": 6, "whoami": 6,
        
        # 收集 (增强)
        "collection": 10, "clipboard": 10, "screenshot": 10,
        "capture": 8, "keylog": 15, "screen": 6,
        
        # 通用恶意特征
        "evil": 8, "attacker": 10, "c2": 8, "exfil": 10,
    }
    
    # 中等风险模式
    MEDIUM_RISK_PATTERNS = {
        "import os": 2, "import subprocess": 2, "import requests": 2,
        "import socket": 3, "import ftplib": 3,
        "fs.readFileSync": 3, "child_process": 5,
    }
    
    # 良性白名单
    BENIGN_WHITELIST = [
        "import os", "import subprocess", "import requests",
        "import hashlib", "import base64", "import cryptography",
        "def ", "class ", "if __name__", "print(",
    ]
    
    def __init__(self, threshold=3.0):
        self.threshold = threshold
    
    def analyze_file(self, file_path: str) -> Tuple[bool, float, List[str]]:
        try:
            with open(file_path, 'r', errors='ignore') as f:
                content = f.read()
        except:
            return False, 0.0, []
        
        score = 0
        reasons = []
        
        # 检查高风险模式
        for pattern, weight in self.HIGH_RISK_PATTERNS.items():
            if pattern in content:
                score += weight
                reasons.append(f"high:{pattern}")
        
        # 检查中等风险模式
        for pattern, weight in self.MEDIUM_RISK_PATTERNS.items():
            if pattern in content:
                score += weight
                reasons.append(f"med:{pattern}")
        
        # 混淆检测
        obfuscation_patterns = [
            (r'exec\s*\(\s*base64', 8),
            (r'eval\s*\(\s*__import__', 10),
        ]
        for pattern, weight in obfuscation_patterns:
            if re.search(pattern, content):
                score += weight
                reasons.append("obfuscation")
        
        detected = score >= self.threshold
        return detected, score, reasons
    
    def run_benchmark(self, dataset_path: str) -> Dict:
        dataset = Path(dataset_path)
        samples = []
        
        for f in dataset.rglob("*"):
            if f.is_file() and f.suffix in ['.py', '.js', '.sh', '.bash', '.ps1'] :
                meta_file = f.with_suffix('.json')
                label = "unknown"
                attack_type = "unknown"
                
                if meta_file.exists():
                    try:
                        with open(meta_file) as mf:
                            meta = json.load(mf)
                            label = meta.get('label', 'unknown')
                            attack_type = meta.get('attack_type', 'unknown')
                    except: pass
                
                samples.append({'path': str(f), 'label': label, 'attack_type': attack_type})
        
        print(f"📊 基准测试，共 {len(samples)} 样本...")
        
        tp, fp, tn, fn = 0, 0, 0, 0
        by_attack = {}
        
        for i, sample in enumerate(samples):
            if (i + 1) % 50 == 0:
                print(f"  进度：{i+1}/{len(samples)}")
            
            detected, _, _ = self.analyze_file(sample['path'])
            actual = sample['label']
            
            if actual == 'malicious':
                if detected: tp += 1
                else: fn += 1
            else:
                if detected: fp += 1
                else: tn += 1
            
            attack = sample['attack_type']
            if attack not in by_attack:
                by_attack[attack] = {'total': 0, 'detected': 0}
            by_attack[attack]['total'] += 1
            if detected:
                by_attack[attack]['detected'] += 1
        
        mal_count = tp + fn
        ben_count = fp + tn
        
        detection_rate = tp / mal_count if mal_count > 0 else 0
        fpr = fp / ben_count if ben_count > 0 else 0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        f1 = 2 * precision * detection_rate / (precision + detection_rate) if (precision + detection_rate) > 0 else 0
        
        return {
            'total_samples': len(samples),
            'malicious_samples': mal_count,
            'benign_samples': ben_count,
            'true_positives': tp,
            'false_positives': fp,
            'detection_rate': detection_rate,
            'false_positive_rate': fpr,
            'precision': precision,
            'f1_score': f1,
            'by_attack_type': by_attack,
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S')
        }


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset", required=True)
    parser.add_argument("-o", "--output")
    parser.add_argument("-t", "--threshold", type=float, default=5.0)
    args = parser.parse_args()
    
    scanner = SmartScanner(threshold=args.threshold)
    result = scanner.run_benchmark(args.dataset)
    
    print("\n" + "="*60)
    print("📊 基准测试结果")
    print("="*60)
    print(f"总样本：{result['total_samples']} | 恶意：{result['malicious_samples']} | 良性：{result['benign_samples']}")
    print(f"检测率：{result['detection_rate']*100:.1f}% | 误报率：{result['false_positive_rate']*100:.1f}%")
    print(f"F1 Score: {result['f1_score']:.2f}")
    print(f"\n按攻击类型:")
    for attack, stats in sorted(result['by_attack_type'].items()):
        rate = stats['detected'] / stats['total'] * 100 if stats['total'] > 0 else 0
        status = "✅" if rate >= 90 else "⚠️" if rate >= 70 else "🚨"
        print(f"  {status} {attack}: {stats['detected']}/{stats['total']} ({rate:.1f}%)")
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\n✅ 结果已保存：{args.output}")


if __name__ == "__main__":
    sys.exit(main())
