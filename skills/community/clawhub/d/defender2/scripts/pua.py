#!/usr/bin/env python3
"""
NPM Supply Chain Malware Detector
检测对象: os-info-checker-es6 及其变种
作者: AI Assistant/ @goog
日期: 2026-03-18
"""

import sys
import io

# Fix Windows console encoding for emoji support
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import base64
import re
import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Tuple, Optional

class UnicodePUADetector:
    """检测Unicode私有使用区(PUA)字符 - 攻击核心混淆技术"""
    
    # PUA字符范围
    PUA_RANGES = [
        (0xE000, 0xF8FF, 'BMP PUA'),      # 基本多文种平面
        (0xF0000, 0xFFFFD, 'PUA-A'),      # 辅助平面A
        (0x100000, 0x10FFFD, 'PUA-B'),    # 辅助平面B
    ]
    
    # Base64字符集（用于解码PUA）
    BASE64_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    
    @classmethod
    def detect(cls, text: str) -> List[Dict]:
        """检测文本中的PUA字符"""
        pua_chars = []
        for i, char in enumerate(text):
            code_point = ord(char)
            for start, end, pua_type in cls.PUA_RANGES:
                if start <= code_point <= end:
                    pua_chars.append({
                        'index': i,
                        'char': char,
                        'hex': f"U+{code_point:04X}" if code_point <= 0xFFFF else f"U+{code_point:05X}",
                        'type': pua_type,
                        'decimal': code_point
                    })
                    break
        return pua_chars
    
    @classmethod
    def decode_pua_to_base64(cls, text: str, pua_start: int = 0xE000) -> Optional[str]:
        """
        尝试将PUA字符解码为Base64
        假设攻击者使用PUA区域映射Base64字符集
        """
        result = []
        for char in text:
            code_point = ord(char)
            if pua_start <= code_point < pua_start + 64:
                idx = code_point - pua_start
                result.append(cls.BASE64_CHARS[idx])
            elif code_point == 0xE800:  # 假设的padding映射
                result.append('=')
        
        decoded_str = ''.join(result)
        # 验证是否是有效的base64
        if len(decoded_str) >= 4 and len(decoded_str) % 4 == 0:
            try:
                base64.b64decode(decoded_str, validate=True)
                return decoded_str
            except:
                pass
        return None


class MalwarePatternDetector:
    """恶意代码模式检测器"""
    
    # 已知恶意IOC
    IOC_PACKAGES = [
        'os-info-checker-es6',
        'skip-tot',
        'vue-dev-serverr', 
        'vue-dummyy',
        'vue-bit'
    ]
    
    IOC_IPS = ['140.82.54.223']
    IOC_URLS = [
        'calendar.app.google/t56nfUUcugH9ZUkx9',
        'calendar.app.google'
    ]
    IOC_FILENAMES = ['pqlatt', 'cjnilxo']
    
    # 危险代码模式
    DANGEROUS_PATTERNS = [
        (r'eval\s*\(\s*atob\s*\(', 'eval(atob())代码执行'),
        (r'eval\s*\(\s*Buffer\.from\s*\(', 'eval(Buffer.from())代码执行'),
        (r'Function\s*\(\s*atob\s*\(', 'Function构造器代码执行'),
        (r'new\s+Function\s*\(\s*["\'][^"\']*["\']\s*\)', '动态函数构造'),
    ]
    
    # 持久化/隐蔽技术
    PERSISTENCE_PATTERNS = [
        (r'existsSync.*?writeFileSync.*?unlinkSync', '单例锁文件模式'),
        (r'process\.on\s*\(\s*["\']uncaughtException["\']', '异常捕获持久化'),
        (r'process\.on\s*\(\s*["\']exit["\']', '进程退出处理'),
    ]
    
    @classmethod
    def scan_content(cls, content: str, filename: str = "unknown") -> List[str]:
        """扫描内容中的恶意模式"""
        findings = []
        content_lower = content.lower()
        
        # 1. 检查IOC - 包名引用
        for pkg in cls.IOC_PACKAGES:
            if pkg in content_lower:
                findings.append(f"🚫 发现已知恶意包引用: {pkg}")
        
        # 2. 检查IOC - IP/URL
        for ip in cls.IOC_IPS:
            if ip in content:
                findings.append(f"🚨 发现已知恶意IP: {ip}")
        
        for url in cls.IOC_URLS:
            if url in content:
                findings.append(f"🚨 发现已知C2地址: {url}")
        
        # 3. 检查IOC - 特定文件名
        for name in cls.IOC_FILENAMES:
            if name in content:
                findings.append(f"⚠️  发现恶意软件特征文件名: {name}")
        
        # 4. 检查危险代码模式
        for pattern, desc in cls.DANGEROUS_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                findings.append(f"⚠️  发现危险模式: {desc}")
        
        # 5. 检查持久化技术
        for pattern, desc in cls.PERSISTENCE_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE | re.DOTALL):
                findings.append(f"🔒 发现持久化技术: {desc}")
        
        # 6. 检查长Base64字符串（可能隐藏代码）
        base64_pattern = r'["\']([A-Za-z0-9+/]{100,}={0,2})["\']'
        matches = re.findall(base64_pattern, content)
        if matches:
            findings.append(f"🔍 发现{len(matches)}个长Base64字符串（可能隐藏代码）")
            # 尝试解码前几个
            for match in matches[:2]:
                try:
                    decoded = base64.b64decode(match).decode('utf-8', errors='ignore')
                    if any(k in decoded.lower() for k in ['http', 'require', 'eval', 'fetch', 'function']):
                        findings.append(f"   🚨 Base64解码后包含可疑关键词: {decoded[:60]}...")
                except:
                    pass
        
        return findings


class NPMPackageScanner:
    """NPM包扫描器"""
    
    @staticmethod
    def scan_package_json(filepath: str) -> List[str]:
        """扫描package.json文件"""
        findings = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            return [f"❌ 无法解析package.json: {e}"]
        
        name = data.get('name', '')
        
        # 检查包名是否在IOC列表
        if name in MalwarePatternDetector.IOC_PACKAGES:
            findings.append(f"🚫 警告: 这是已知恶意包: {name}")
        
        # 检查scripts
        scripts = data.get('scripts', {})
        install_scripts = ['preinstall', 'postinstall', 'install']
        for script_name in install_scripts:
            if script_name in scripts:
                script_content = scripts[script_name]
                findings.append(f"📦 发现{script_name}脚本")
                # 如果脚本执行.js文件，标记为需检查
                if '.js' in script_content or '.node' in script_content:
                    findings.append(f"   ⚠️  脚本执行外部文件: {script_content}")
        
        # 检查依赖
        deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
        for dep_name in MalwarePatternDetector.IOC_PACKAGES:
            if dep_name in deps:
                findings.append(f"🔗 依赖已知恶意包: {dep_name}@{deps[dep_name]}")
        
        return findings


class FileSystemScanner:
    """文件系统扫描器"""
    
    def __init__(self, target_path: str):
        self.target_path = Path(target_path)
        self.total_files = 0
        self.suspicious_files = 0
    
    def scan(self, recursive: bool = True) -> Dict[str, List[str]]:
        """执行扫描"""
        results = {}
        
        if self.target_path.is_file():
            findings = self.scan_file(str(self.target_path))
            if findings:
                results[str(self.target_path)] = findings
        elif self.target_path.is_dir():
            pattern = '**/*' if recursive else '*'
            for filepath in self.target_path.glob(pattern):
                if filepath.is_file() and filepath.suffix in ['.js', '.json', '.node', '.ts']:
                    self.total_files += 1
                    findings = self.scan_file(str(filepath))
                    if findings:
                        results[str(filepath)] = findings
                        self.suspicious_files += 1
        
        return results
    
    def scan_file(self, filepath: str) -> List[str]:
        """扫描单个文件"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            return [f"❌ 读取失败: {e}"]
        
        all_findings = []
        
        # 1. 如果是package.json，使用专用扫描器
        if filepath.endswith('package.json'):
            all_findings.extend(NPMPackageScanner.scan_package_json(filepath))
        
        # 2. 扫描恶意模式
        all_findings.extend(MalwarePatternDetector.scan_content(content, filepath))
        
        # 3. 扫描PUA字符
        pua_chars = UnicodePUADetector.detect(content)
        if len(pua_chars) > 5:  # 超过5个PUA字符视为可疑
            all_findings.append(f"🚨 发现{len(pua_chars)}个Unicode PUA字符（高度可疑）")
            # 尝试解码
            decoded_b64 = UnicodePUADetector.decode_pua_to_base64(content)
            if decoded_b64:
                all_findings.append(f"   成功解码PUA为Base64: {decoded_b64[:40]}...")
                try:
                    final_code = base64.b64decode(decoded_b64).decode('utf-8', errors='ignore')
                    all_findings.append(f"   最终解码: {final_code[:60]}...")
                except:
                    pass
        elif len(pua_chars) > 0:
            all_findings.append(f"⚠️  发现{len(pua_chars)}个PUA字符")
        
        return all_findings


def print_report(results: Dict[str, List[str]], total_files: int, suspicious_files: int):
    """打印扫描报告"""
    print("\\n" + "=" * 70)
    print("NPM恶意软件扫描报告")
    print("=" * 70)
    print(f"扫描文件总数: {total_files}")
    print(f"可疑文件数: {suspicious_files}")
    print(f"威胁等级: {'🚨 HIGH' if suspicious_files > 0 else '✅ CLEAN'}")
    print("=" * 70)
    
    if not results:
        print("\\n✅ 未发现明显恶意模式")
        return
    
    print(f"\\n发现 {len(results)} 个可疑文件:")
    print("-" * 70)
    
    for filepath, findings in results.items():
        print(f"\\n📄 {filepath}")
        for finding in findings:
            print(f"   {finding}")
    
    print("\\n" + "=" * 70)
    print("建议操作:")
    if suspicious_files > 0:
        print("  1. 🚫 立即停止运行相关代码")
        print("  2. 🔍 人工审查标记的文件")
        print("  3. 🧹 从node_modules中删除恶意包")
        print("  4. 📝 检查package.json移除恶意依赖")
    else:
        print("  ✅ 未发现明显威胁，但仍建议保持警惕")
    print("=" * 70)


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='检测NPM供应链恶意软件（如os-info-checker-es6变种）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python malware_detector.py ./my-project
  python malware_detector.py ./package.json
  python malware_detector.py ./node_modules/os-info-checker-es6 --recursive
        """
    )
    
    parser.add_argument('path', help='要扫描的路径（文件或目录）')
    parser.add_argument('-r', '--recursive', action='store_true', 
                       help='递归扫描子目录（默认对目录启用）')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='显示详细信息')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.path):
        print(f"❌ 错误: 路径不存在: {args.path}")
        sys.exit(1)
    
    print(f"🔍 开始扫描: {args.path}")
    print(f"⏱️  时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    scanner = FileSystemScanner(args.path)
    results = scanner.scan(recursive=args.recursive)
    
    print_report(results, scanner.total_files, scanner.suspicious_files)
    
    # 返回码：发现威胁返回1，清洁返回0
    sys.exit(1 if scanner.suspicious_files > 0 else 0)


if __name__ == "__main__":
    main()

