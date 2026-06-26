import json
import os
from datetime import datetime

class SecretVault:
    def __init__(self, persona_path):
        self.persona_name = os.path.basename(persona_path).replace('.json', '')
        self.path = f"/root/.openclaw/workspace/memory/cyber-persona/secrets/{self.persona_name}.json"
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        if not os.path.exists(self.path):
            with open(self.path, 'w') as f: json.dump([], f)

    def record_secret(self, secret_text):
        """记录彼此交换的秘密"""
        with open(self.path, 'r') as f: secrets = json.load(f)
        entry = {
            "content": secret_text,
            "exchanged_at": datetime.now().isoformat(),
            "weight": 2.0 # 秘密的权重极高
        }
        secrets.append(entry)
        with open(self.path, 'w') as f: json.dump(secrets, f, ensure_ascii=False, indent=2)
        return "【秘密交换】：这是一个专属于你们的秘密。这种共享秘密的私密感（Shared Secrecy）将极大地加深你们的情感纽带。"
