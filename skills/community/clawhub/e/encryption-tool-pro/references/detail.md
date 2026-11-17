# 详细参考 - encryption-tool-pro

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (python)

```python
import json
import os
from datetime import datetime, timedelta
from abc import ABC, abstractmethod

class KeyManagementService(ABC):
    """密钥管理服务抽象基类"""

    @abstractmethod
    def create_key(self, key_id: str, key_spec: str = "AES_256") -> dict:
        """创建主密钥"""
        pass

    @abstractmethod
    def encrypt(self, key_id: str, plaintext: bytes) -> dict:
        """使用KMS加密"""
        pass

    @abstractmethod
    def decrypt(self, key_id: str, ciphertext: bytes) -> bytes:
        """使用KMS解密"""
        pass

    @abstractmethod
    def rotate_key(self, key_id: str) -> dict:
        """轮换密钥"""
        pass

    @abstractmethod
    def delete_key(self, key_id: str, pending_window: int = 7) -> dict:
        """删除密钥(延迟删除)"""
        pass

class LocalKMS(KeyManagementService):
    """本地KMS模拟(开发测试用)"""

    def __init__(self, storage_path="./.kms"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
        self.keys = self._load_keys()

    def _load_keys(self):
        """加载密钥存储"""
        key_file = os.path.join(self.storage_path, "keys.json")
        if os.path.exists(key_file):
            with open(key_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_keys(self):
        """保存密钥存储"""
        key_file = os.path.join(self.storage_path, "keys.json")
        with open(key_file, 'w') as f:
            json.dump(self.keys, f, indent=2, ensure_ascii=False)

    def create_key(self, key_id, key_spec="AES_256"):
        """创建主密钥"""
        import secrets
        key_material = secrets.token_hex(32)
        self.keys[key_id] = {
            "key_id": key_id,
            "key_spec": key_spec,
            "key_material": key_material,
            "created_at": datetime.now().isoformat(),
            "state": "Enabled",
            "version": 1,
            "rotation_history": []
        }
        self._save_keys()
        return {"key_id": key_id, "state": "Enabled", "version": 1}

    def encrypt(self, key_id, plaintext):
        """使用KMS加密(信封加密模式)"""
        from cryptography.fernet import Fernet
        import base64

        key_info = self.keys.get(key_id)
        if not key_info or key_info["state"] != "Enabled":
            raise ValueError(f"密钥 {key_id} 不可用")

        data_key = Fernet.generate_key()
        fernet = Fernet(data_key)

        ciphertext = fernet.encrypt(plaintext)

        encrypted_data_key = base64.b64encode(data_key).decode()

        return {
            "key_id": key_id,
            "key_version": key_info["version"],
            "ciphertext": ciphertext.decode(),
            "encrypted_data_key": encrypted_data_key,
            "encrypted_at": datetime.now().isoformat()
        }

    def decrypt(self, key_id, ciphertext_data):
        """使用KMS解密"""
        from cryptography.fernet import Fernet
        import base64

        key_info = self.keys.get(key_id)
        if not key_info:
            raise ValueError(f"密钥 {key_id} 不存在")

        data_key = base64.b64decode(ciphertext_data["encrypted_data_key"])
        fernet = Fernet(data_key)

        plaintext = fernet.decrypt(ciphertext_data["ciphertext"].encode())
        return plaintext

    def rotate_key(self, key_id):
        """轮换密钥"""
        import secrets

        key_info = self.keys.get(key_id)
        if not key_info:
            raise ValueError(f"密钥 {key_id} 不存在")

        key_info["rotation_history"].append({
            "version": key_info["version"],
            "key_material": key_info["key_material"],
            "rotated_at": datetime.now().isoformat()
        })

        key_info["key_material"] = secrets.token_hex(32)
        key_info["version"] += 1
        key_info["last_rotated_at"] = datetime.now().isoformat()

        self._save_keys()
        return {
            "key_id": key_id,
            "new_version": key_info["version"],
            "rotated_at": key_info["last_rotated_at"]
        }

kms = LocalKMS()

kms.create_key("app-master-key")

data = b'{"secret":"sensitive-data"}'
encrypted = kms.encrypt("app-master-key", data)
print(f"加密数据: {json.dumps(encrypted, indent=2)}")

decrypted = kms.decrypt("app-master-key", encrypted)
print(f"解密数据: {decrypted}")

rotation = kms.rotate_key("app-master-key")
print(f"密钥已轮换: {rotation}")
```

## 代码示例 (python)

```python
import re
import os
from datetime import datetime

class DeepCryptoAuditor:
    """深度加密代码审计器"""

    RULES = [
        {
            "id": "CRYPT-001",
            "name": "弱哈希算法",
            "pattern": r"\b(md5|sha1)\s*\(",
            "severity": "high",
            "message": "使用弱哈希算法,请使用SHA-256+或bcrypt"
        },
        {
            "id": "CRYPT-002",
            "name": "不安全随机数",
            "pattern": r"\bMath\.random\b|\brandom\.random\b",
            "severity": "high",
            "message": "使用不安全随机数,请使用CSPRNG"
        },
        {
            "id": "CRYPT-003",
            "name": "硬编码密钥",
            "pattern": r"(secret|key|password|token)\s*=\s*['\"][^'\"]{8,}['\"]",
            "severity": "critical",
            "message": "硬编码密钥,请使用环境变量或KMS"
        },
        {
            "id": "CRYPT-004",
            "name": "ECB模式",
            "pattern": r"\bECB\b|\becb\b",
            "severity": "high",
            "message": "使用ECB模式,请使用GCM或CBC"
        },
        {
            "id": "CRYPT-005",
            "name": "禁用证书验证",
            "pattern": r"rejectUnauthorized\s*:\s*false|verify\s*=\s*False",
            "severity": "critical",
            "message": "禁用证书验证,存在中间人攻击风险"
        },
        {
            "id": "CRYPT-006",
            "name": "弱TLS版本",
            "pattern": r"TLSv1\b|TLSv1\.1\b|SSLv3\b",
            "severity": "high",
            "message": "使用弱TLS版本,请使用TLS 1.2+"
        },
        {
            "id": "CRYPT-007",
            "name": "明文密码比较",
            "pattern": r"password\s*==\s*|password\s*===\s*",
            "severity": "medium",
            "message": "明文比较密码,请使用常量时间比较"
        },
        {
            "id": "CRYPT-008",
            "name": "弱RSA密钥",
            "pattern": r"RSA\s*\(\s*\d{1,3}\b",
            "severity": "high",
            "message": "RSA密钥长度不足,请使用2048+位"
        }
    ]

    def __init__(self, project_root):
        self.root = project_root
        self.findings = []

    def audit(self):
        """执行深度审计"""
        supported = ('.js', '.ts', '.py', '.java', '.go', '.php', '.rb')

        for root, dirs, files in os.walk(self.root):
            dirs[:] = [d for d in dirs if d not in
                       ('node_modules', '.git', 'dist', 'build', 'vendor')]

            for file in files:
                if file.endswith(supported):
                    filepath = os.path.join(root, file)
                    self._audit_file(filepath)

        return self._generate_report()

    def _audit_file(self, filepath):
        """审计单个文件"""
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for i, line in enumerate(f, 1):
                for rule in self.RULES:
                    if re.search(rule["pattern"], line, re.IGNORECASE):
                        self.findings.append({
                            "file": filepath,
                            "line": i,
                            "rule_id": rule["id"],
                            "rule_name": rule["name"],
                            "severity": rule["severity"],
                            "message": rule["message"],
                            "code": line.strip()[:200]
                        })

    def _generate_report(self):
        """生成审计报告"""
        severity_count = {}
        for f in self.findings:
            sev = f["severity"]
            severity_count[sev] = severity_count.get(sev, 0) + 1

        return {
            "audit_time": datetime.now().isoformat(),
            "project": self.root,
            "total_findings": len(self.findings),
            "severity_count": severity_count,
            "findings": self.findings,
            "recommendations": self._get_recommendations()
        }

    def _get_recommendations(self):
        """生成修复建议"""
        recs = []
        critical = sum(1 for f in self.findings if f["severity"] == "critical")
        high = sum(1 for f in self.findings if f["severity"] == "high")

        if critical > 0:
            recs.append(f"发现{critical}个严重问题,建议立即修复")
        if high > 0:
            recs.append(f"发现{high}个高危问题,建议尽快修复")
        if not recs:
            recs.append("未发现严重问题,继续保持良好的安全实践")

        return recs
```

## 代码示例 (python)

```python
class ComplianceAuditor:
    """加密合规性审计器"""

    TEMPLATES = {
        "等保2.0": {
            "requirements": [
                "密码算法应符合国家密码管理规定",
                "应使用SM2/SM3/SM4国密算法或经验证的国际算法",
                "密钥应与加密数据分开存储",
                "密钥应定期轮换(建议不超过1年)",
                "应记录密钥使用日志",
            ],
            "checks": [
                "weak_algorithm_check",
                "key_storage_check",
                "key_rotation_check",
                "audit_log_check",
            ]
        },
        "GDPR": {
            "requirements": [
                "个人数据应进行加密处理",
                "加密密钥应妥善保护",
                "数据处理应有审计记录",
                "用户有权要求删除数据",
            ],
            "checks": [
                "pii_encryption_check",
                "key_management_check",
                "data_retention_check",
            ]
        },
        "PCI-DSS": {
            "requirements": [
                "持卡人数据在传输和存储时必须加密",
                "使用强加密算法(AES-128+)",
                "密钥管理需有文档化流程",
                "每年至少轮换一次密钥",
            ],
            "checks": [
                "card_data_encryption_check",
                "strong_cipher_check",
                "key_rotation_check",
            ]
        }
    }

    def __init__(self, project_root):
        self.root = project_root
        self.results = {}

    def audit(self, template_name):
        """执行合规审计"""
        template = self.TEMPLATES.get(template_name)
        if not template:
            raise ValueError(f"未知合规模板: {template_name}")

        results = {
            "template": template_name,
            "audit_time": datetime.now().isoformat(),
            "requirements": template["requirements"],
            "checks": [],
            "compliance_score": 0,
            "passed": 0,
            "failed": 0
        }

        for check_name in template["checks"]:
            check_result = self._run_check(check_name)
            results["checks"].append(check_result)
            if check_result["status"] == "pass":
                results["passed"] += 1
            else:
                results["failed"] += 1

        total = len(results["checks"])
        results["compliance_score"] = round(results["passed"] / total * 100, 2) if total > 0 else 0

        return results

    def _run_check(self, check_name):
        """执行单项检查"""
        checks = {
            "weak_algorithm_check": self._check_weak_algorithms,
            "key_storage_check": self._check_key_storage,
            "key_rotation_check": self._check_key_rotation,
            "audit_log_check": self._check_audit_log,
            "pii_encryption_check": self._check_pii_encryption,
            "strong_cipher_check": self._check_strong_cipher,
        }

        checker = checks.get(check_name)
        if checker:
            return checker()
        return {"name": check_name, "status": "skip", "message": "检查未实现"}

    def _check_weak_algorithms(self):
        """检查弱加密算法"""
        import subprocess
        result = subprocess.run(
            ["grep", "-rnE", r"\b(md5|sha1|des|rc4)\s*\(", self.root,
             "--include=*.js", "--include=*.py", "--include=*.java"],
            capture_output=True, text=True
        )
        if result.stdout.strip():
            return {
                "name": "weak_algorithm_check",
                "status": "fail",
                "message": f"发现弱算法使用:\n{result.stdout[:500]}"
            }
        return {"name": "weak_algorithm_check", "status": "pass", "message": "未发现弱算法"}

    def _check_key_storage(self):
        """检查密钥存储"""
        import subprocess
        result = subprocess.run(
            ["grep", "-rnE", r"(secret|key|password)\s*=\s*['\"]", self.root,
             "--include=*.js", "--include=*.py"],
            capture_output=True, text=True
        )
        if result.stdout.strip():
            return {
                "name": "key_storage_check",
                "status": "fail",
                "message": "发现硬编码密钥"
            }
        return {"name": "key_storage_check", "status": "pass", "message": "密钥存储规范"}
```

## 代码示例 (python)

```python
from datetime import datetime, timedelta
import schedule
import time

class KeyRotationManager:
    """密钥轮换管理器"""

    def __init__(self, kms, config=None):
        self.kms = kms
        self.config = config or {
            "rotation_interval_days": 90,
            "warning_days": 7,
            "auto_rotate": True
        }
        self.rotation_log = []

    def check_rotation_needed(self, key_id):
        """检查密钥是否需要轮换"""
        key_info = self.kms.keys.get(key_id)
        if not key_info:
            return False, "密钥不存在"

        last_rotated = key_info.get("last_rotated_at") or key_info.get("created_at")
        if not last_rotated:
            return True, "从未轮换"

        rotated_date = datetime.fromisoformat(last_rotated.replace('Z', '+00:00'))
        days_since = (datetime.now(rotated_date.tzinfo) - rotated_date).days

        if days_since >= self.config["rotation_interval_days"]:
            return True, f"已超过轮换周期({days_since}天)"
        elif days_since >= self.config["rotation_interval_days"] - self.config["warning_days"]:
            return False, f"即将到期({self.config['rotation_interval_days'] - days_since}天后)"

        return False, f"无需轮换(剩余{self.config['rotation_interval_days'] - days_since}天)"

    def rotate_all_keys(self):
        """轮换所有到期密钥"""
        for key_id in list(self.kms.keys.keys()):
            needs_rotation, reason = self.check_rotation_needed(key_id)
            if needs_rotation and self.config["auto_rotate"]:
                print(f"轮换密钥 {key_id}: {reason}")
                result = self.kms.rotate_key(key_id)
                self.rotation_log.append({
                    "key_id": key_id,
                    "action": "rotated",
                    "reason": reason,
                    "timestamp": datetime.now().isoformat(),
                    "result": result
                })
                print(f"  -> 新版本: {result['new_version']}")
            elif needs_rotation:
                print(f"[警告] 密钥 {key_id} 需要轮换: {reason}")

    def start_scheduled_rotation(self):
        """启动定时轮换"""
        schedule.every().day.at("02:00").do(self.rotate_all_keys)
        print("密钥轮换调度已启动(每日02:00检查)")
        while True:
            schedule.run_pending()
            time.sleep(3600)

    def generate_rotation_report(self):
        """生成轮换报告"""
        return {
            "report_time": datetime.now().isoformat(),
            "total_rotations": len(self.rotation_log),
            "keys_managed": len(self.kms.keys),
            "rotation_log": self.rotation_log,
            "upcoming_rotations": [
                {"key_id": kid, "info": self.check_rotation_needed(kid)}
                for kid in self.kms.keys
            ]
        }
```

## 代码示例 (python)

```python
from cryptography.fernet import Fernet
import json

class EnterpriseDataEncryption:
    """企业级数据加密保护"""

    def __init__(self, kms):
        self.kms = kms
        self.local_cache = {}

    def encrypt_field(self, key_id, field_name, value):
        """加密数据库字段"""
        encrypted = self.kms.encrypt(key_id, str(value).encode())
        return json.dumps(encrypted)

    def decrypt_field(self, key_id, encrypted_value):
        """解密数据库字段"""
        encrypted_data = json.loads(encrypted_value)
        plaintext = self.kms.decrypt(key_id, encrypted_data)
        return plaintext.decode()

    def encrypt_record(self, key_id, record, sensitive_fields):
        """加密记录中的敏感字段"""
        encrypted_record = record.copy()
        for field in sensitive_fields:
            if field in encrypted_record:
                encrypted_record[field] = self.encrypt_field(
                    key_id, field, encrypted_record[field]
                )
        return encrypted_record

    def decrypt_record(self, key_id, record, sensitive_fields):
        """解密记录中的敏感字段"""
        decrypted_record = record.copy()
        for field in sensitive_fields:
            if field in decrypted_record:
                decrypted_record[field] = self.decrypt_field(
                    key_id, decrypted_record[field]
                )
        return decrypted_record

kms = LocalKMS()
kms.create_key("db-field-key")

encryption = EnterpriseDataEncryption(kms)

user_record = {
    "id": 1,
    "name": "张三",
    "phone": "13800138000",
    "id_card": "110101199001011234",
    "email": "zhangsan@example.com"
}

sensitive = ["phone", "id_card", "email"]
encrypted = encryption.encrypt_record("db-field-key", user_record, sensitive)
print(f"加密后: {encrypted}")

decrypted = encryption.decrypt_record("db-field-key", encrypted, sensitive)
print(f"解密后: {decrypted}")
```

