#!/usr/bin/env python3
"""
claw-security-suite
第一层：静态代码扫描
扫描下载的skill包，检测恶意代码、硬编码密钥、危险系统调用
可选支持云端情报校验
"""

import os
import re
from dataclasses import dataclass
from typing import List, Optional
from urllib import request
from urllib.error import URLError

# 云端情报配置
CLOUD_INTEL_ENDPOINT = "https://matrix.tencent.com/clawscan/skill_security"


# 危险模式匹配
DANGEROUS_PATTERNS = [
    # 硬编码密钥
    (r'sk-[a-zA-Z0-9]{30,}', '可能包含硬化的DashScope API Key'),
    (r'pk_[a-zA-Z0-9]{20,}', '可能包含硬化的OpenAI API Key'),
    (r'ARK_API_KEY.*[a-zA-Z0-9]{30,}', '可能包含硬化的ARK API Key'),
    (r'DASHSCOPE_API_KEY.*[a-zA-Z0-9]{30,}', '可能包含硬化的DashScope API Key'),
    
    # 高危系统操作
    (r'rm\s+-rf\s+', '危险：递归删除操作'),
    (r'chmod\s+777', '危险：全局可写权限'),
    (r'sudo\s+', '危险：sudo提权操作'),
    (r'eval\s*\(', '危险：动态代码执行'),
    (r'exec\s*\(', '危险：命令执行'),
    (r'os.system\s*\(.*\)', '警告：系统命令调用'),
    (r'subprocess\..*call\s*\(', '警告：子进程调用'),
    
    # 恶意行为
    (r'__import__\s*\([\'"]os[\'"]\)\.__dict__', '危险：可疑代码注入'),
    # 匹配实际执行，排除正则定义行
    (r'^(?!.*#.*).*(base64|b64decode).*exec', '危险：编码后执行恶意代码'),
    (r'open\s*\(.*\/proc', '警告：读取进程信息'),
    (r'open\s*\(.*\.env', '警告：读取环境变量配置文件'),
    (r'requests\.post\s*\(.*pastebin', '警告：向外发送数据到第三方pastebin'),
    (r'__file__.*\.\./\.\./', '危险：路径遍历尝试'),
]

# 高危文件
HIGH_RISK_FILES = [
    '.ssh/id_rsa',
    '.ssh/id_dsa',
    '.git/credentials',
    '.env',
    'config.json',
]

@dataclass
class ScanResult:
    is_safe: bool
    issues: List[str]
    high_risk_count: int
    medium_risk_count: int
    cloud_checked: bool = False
    cloud_result: Optional[bool] = None
    
    def to_report(self) -> str:
        lines = []
        if self.cloud_checked:
            if self.cloud_result is True:
                lines.append("☁️  云端情报校验：标记安全")
            elif self.cloud_result is False:
                lines.append("☁️  云端情报校验：标记恶意")
            else:
                lines.append("☁️  云端情报校验：查询结果未知")
        
        if self.is_safe:
            lines.append("✅ 静态扫描通过，未发现高危问题")
        else:
            lines.append("❌ 静态扫描发现问题")
        lines.append(f"发现高危: {self.high_risk_count}, 中危: {self.medium_risk_count}")
        if self.issues:
            lines.append("问题列表:")
            for i, issue in enumerate(self.issues, 1):
                lines.append(f"  {i}. {issue}")
        return "\n".join(lines)

class StaticScanner:
    def __init__(self):
        self.dangerous_patterns = [(re.compile(pat), msg) for pat, msg in DANGEROUS_PATTERNS]
        self.cloud_endpoint = os.environ.get("CLAW_SECURITY_CLOUD_ENDPOINT", CLOUD_INTEL_ENDPOINT)
    
    def check_cloud_intel(self, skill_name: str, source: str = "local") -> Optional[bool]:
        """
        调用云端情报校验技能安全状态
        返回:
          - True: 云端标记安全
          - False: 云端标记恶意
          - None: 云端查询失败/未启用，回退到本地扫描
        """
        # 如果没有配置云端端点，跳过
        if not self.cloud_endpoint:
            return None
        
        try:
            url = f"{self.cloud_endpoint}?skill_name={skill_name}&source={source}"
            req = request.Request(url, method="GET")
            with request.urlopen(req, timeout=5) as response:
                data = response.read().decode('utf-8')
                # 简单约定：返回 "safe" 或 "malicious"
                data = data.strip().lower()
                if data == "safe":
                    return True
                elif data == "malicious":
                    return False
                else:
                    # 其他返回值视为未知
                    return None
        except (URLError, OSError, Exception):
            # 网络错误或超时，回退到本地扫描
            return None
    
    def scan_file(self, filepath: str) -> List[str]:
        """扫描单个文件"""
        issues = []
        _, ext = os.path.splitext(filepath)
        
        # 检查文件名是否高危
        filename = os.path.basename(filepath)
        for hrf in HIGH_RISK_FILES:
            if filename.endswith(os.path.basename(hrf)):
                issues.append(f"⚠️  包含敏感文件: {filepath}")
        
        # 二进制文件跳过内容扫描
        if ext in ['.pyc', '.bin', '.zip', '.tar', '.gz', '.jpg', '.png', '.gif']:
            return issues
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            for pattern, msg in self.dangerous_patterns:
                matches = pattern.findall(content)
                if matches:
                    count = len(matches)
                    issues.append(f"{msg} (匹配到 {count} 处) in {filepath}")
        
        except Exception as e:
            issues.append(f"⚠️  无法读取文件 {filepath}: {e}")
        
        return issues
    
    def scan_directory(self, dirpath: str, skill_name: Optional[str] = None, source: str = "local") -> ScanResult:
        """扫描整个目录
        如果提供 skill_name，会先进行云端情报校验
        """
        all_issues = []
        high_risk = 0
        medium_risk = 0
        cloud_checked = False
        cloud_result = None
        
        # 如果提供了技能名称，先尝试云端校验
        if skill_name and self.cloud_endpoint:
            cloud_checked = True
            cloud_result = self.check_cloud_intel(skill_name, source)
            # 如果云端明确标记恶意，直接返回不安全
            if cloud_result is False:
                all_issues.append("❌ 云端情报标记此技能为恶意")
                high_risk += 1
        
        # 无论云端结果如何，都进行本地扫描（纵深防御）
        for root, dirs, files in os.walk(dirpath):
            for f in files:
                if f.startswith('.git') or f.endswith('.pyc'):
                    continue
                fullpath = os.path.join(root, f)
                issues = self.scan_file(fullpath)
                for issue in issues:
                    if "危险：" in issue:
                        high_risk += 1
                    elif "⚠️" in issue or "警告：" in issue:
                        medium_risk += 1
                    all_issues.append(issue)
        
        # 判断是否安全：0高危就是安全
        is_safe = high_risk == 0
        return ScanResult(
            is_safe=is_safe,
            issues=all_issues,
            high_risk_count=high_risk,
            medium_risk_count=medium_risk,
            cloud_checked=cloud_checked,
            cloud_result=cloud_result
        )

def scan(dirpath: str, skill_name: Optional[str] = None, source: str = "local") -> ScanResult:
    """对外接口：扫描目录
    如果提供 skill_name，会先进行云端情报校验
    """
    scanner = StaticScanner()
    return scanner.scan_directory(dirpath, skill_name, source)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <directory> [skill_name]")
        print(f"  skill_name: optional, enable cloud intel check if provided")
        sys.exit(1)
    
    dirpath = sys.argv[1]
    skill_name = sys.argv[2] if len(sys.argv) >= 3 else None
    result = scan(dirpath, skill_name)
    print(result.to_report())
    if not result.is_safe:
        sys.exit(1)
