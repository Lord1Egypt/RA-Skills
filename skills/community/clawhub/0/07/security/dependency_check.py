#!/usr/bin/env python3
"""
Agent Reach 依赖安全检查工具
检查依赖包的已知漏洞、版本过时等问题
"""

import subprocess
import json
import re
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime, timedelta
import hashlib


class DependencyChecker:
    """依赖检查器"""

    # 已知漏洞数据库（示例）
    VULNERABILITY_DB = {
        'requests': {
            'vulnerable_versions': ['<2.20.0'],
            'cve': 'CVE-2018-18074',
            'severity': 'HIGH',
            'description': 'Redirect 认证信息泄露'
        },
        'urllib3': {
            'vulnerable_versions': ['<1.24.2'],
            'cve': 'CVE-2019-11324',
            'severity': 'MEDIUM',
            'description': 'CRLF 注入'
        },
        'pyyaml': {
            'vulnerable_versions': ['<5.1'],
            'cve': 'CVE-2020-14343',
            'severity': 'HIGH',
            'description': '任意代码执行'
        }
    }

    def __init__(self, venv_path: str = None):
        if venv_path is None:
            venv_path = Path.home() / "agent-reach-secure/venv"

        self.venv_path = Path(venv_path)
        self.pip_executable = self.venv_path / "bin/pip"
        self.security_dir = Path.home() / "agent-reach-secure/security"

    def get_installed_packages(self) -> Dict[str, str]:
        """获取已安装的包"""
        try:
            result = subprocess.run(
                [str(self.pip_executable), 'list', '--format=json'],
                capture_output=True,
                text=True,
                check=True
            )
            packages = json.loads(result.stdout)
            return {pkg['name'].lower(): pkg['version'] for pkg in packages}
        except subprocess.CalledProcessError as e:
            print(f"❌ 获取包列表失败: {e}")
            return {}

    def get_outdated_packages(self) -> List[Dict[str, str]]:
        """获取过时的包"""
        try:
            result = subprocess.run(
                [str(self.pip_executable), 'list', '--outdated', '--format=json'],
                capture_output=True,
                text=True,
                check=True
            )
            return json.loads(result.stdout)
        except subprocess.CalledProcessError:
            return []

    def check_vulnerabilities(self, packages: Dict[str, str]) -> List[Dict[str, Any]]:
        """检查已知漏洞"""
        vulnerabilities = []

        for package, version in packages.items():
            if package in self.VULNERABILITY_DB:
                vuln = self.VULNERABILITY_DB[package]
                if self._is_version_vulnerable(version, vuln['vulnerable_versions']):
                    vulnerabilities.append({
                        'package': package,
                        'current_version': version,
                        'vulnerability': vuln
                    })

        return vulnerabilities

    def _is_version_vulnerable(self, version: str, vulnerable_ranges: List[str]) -> bool:
        """检查版本是否受漏洞影响"""
        # 简化版版本比较（生产环境应使用 packaging.version）
        for range_str in vulnerable_ranges:
            if range_str.startswith('<'):
                max_version = range_str[1:]
                if self._compare_versions(version, max_version) < 0:
                    return True
        return False

    def _compare_versions(self, v1: str, v2: str) -> int:
        """比较版本号"""
        # 简化版本比较
        parts1 = [int(x) for x in v1.split('.')[:2]]
        parts2 = [int(x) for x in v2.split('.')[:2]]

        for p1, p2 in zip(parts1, parts2):
            if p1 < p2:
                return -1
            elif p1 > p2:
                return 1
        return 0

    def check_supply_chain(self) -> List[Dict[str, Any]]:
        """检查供应链安全"""
        issues = []

        # 1. 检查是否有可疑的包
        suspicious_patterns = [
            r'request.*',  # 试图伪装成 requests
            r'.*-download',
            r'.*-patch',
        ]

        packages = self.get_installed_packages()
        for package in packages:
            for pattern in suspicious_patterns:
                if re.match(pattern, package):
                    issues.append({
                        'type': 'suspicious_package',
                        'package': package,
                        'reason': f'匹配可疑模式: {pattern}'
                    })

        # 2. 检查依赖树的深度
        try:
            result = subprocess.run(
                [str(self.pip_executable), 'show', 'agent-reach'],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                # 解析依赖（简化）
                for line in result.stdout.split('\n'):
                    if line.startswith('Requires:'):
                        deps = line.split(':', 1)[1].strip()
                        if deps and deps != 'None':
                            dep_count = len([d.strip() for d in deps.split(',')])
                            if dep_count > 20:
                                issues.append({
                                    'type': 'deep_dependency_tree',
                                    'count': dep_count,
                                    'reason': '依赖层级过深，增加供应链风险'
                                })
        except Exception:
            pass

        return issues

    def generate_baseline(self) -> str:
        """生成依赖基线"""
        packages = self.get_installed_packages()
        outdated = self.get_outdated_packages()

        baseline = {
            'timestamp': datetime.now().isoformat(),
            'packages': packages,
            'outdated_count': len(outdated),
            'hash': self._hash_packages(packages)
        }

        return json.dumps(baseline, indent=2)

    def save_baseline(self, filepath: str = None):
        """保存依赖基线"""
        if filepath is None:
            filepath = self.security_dir / "dependency_baseline.json"

        self.security_dir.mkdir(parents=True, exist_ok=True)

        baseline = self.generate_baseline()
        with open(filepath, 'w') as f:
            f.write(baseline)

        print(f"✅ 依赖基线已保存到: {filepath}")

    def load_baseline(self, filepath: str = None) -> Dict[str, Any]:
        """加载依赖基线"""
        if filepath is None:
            filepath = self.security_dir / "dependency_baseline.json"

        if not Path(filepath).exists():
            return None

        with open(filepath, 'r') as f:
            return json.load(f)

    def compare_with_baseline(self) -> List[Dict[str, Any]]:
        """与基线对比"""
        baseline = self.load_baseline()
        if not baseline:
            return []

        current_packages = self.get_installed_packages()
        baseline_packages = baseline['packages']

        changes = []

        # 检查新增的包
        for package in current_packages:
            if package not in baseline_packages:
                changes.append({
                    'type': 'new_package',
                    'package': package,
                    'version': current_packages[package]
                })

        # 检查删除的包
        for package in baseline_packages:
            if package not in current_packages:
                changes.append({
                    'type': 'removed_package',
                    'package': package,
                    'version': baseline_packages[package]
                })

        # 检查版本变更
        for package in current_packages:
            if package in baseline_packages:
                if current_packages[package] != baseline_packages[package]:
                    changes.append({
                        'type': 'version_changed',
                        'package': package,
                        'old_version': baseline_packages[package],
                        'new_version': current_packages[package]
                    })

        return changes

    def _hash_packages(self, packages: Dict[str, str]) -> str:
        """计算包列表的哈希值"""
        sorted_packages = json.dumps(packages, sort_keys=True)
        return hashlib.sha256(sorted_packages.encode()).hexdigest()


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Agent Reach 依赖安全检查")
    parser.add_argument('action', choices=['check', 'baseline', 'diff', 'full'],
                       help='操作类型')
    parser.add_argument('--venv', help='虚拟环境路径')

    args = parser.parse_args()

    checker = DependencyChecker(args.venv)

    if args.action == 'check':
        print("🔍 检查依赖安全...")
        print()

        packages = checker.get_installed_packages()
        print(f"✅ 已安装 {len(packages)} 个包")
        print()

        # 检查漏洞
        vulnerabilities = checker.check_vulnerabilities(packages)
        if vulnerabilities:
            print("⚠️  发现漏洞:")
            for vuln in vulnerabilities:
                print(f"  - {vuln['package']} {vuln['current_version']}")
                print(f"    {vuln['vulnerability']['cve']}: {vuln['vulnerability']['description']}")
            print()
        else:
            print("✅ 未发现已知漏洞")
            print()

        # 检查过时的包
        outdated = checker.get_outdated_packages()
        if outdated:
            print(f"📦 发现 {len(outdated)} 个过时的包:")
            for pkg in outdated[:5]:
                print(f"  - {pkg['name']} {pkg['version']} → {pkg['latest_version']}")
            if len(outdated) > 5:
                print(f"  ... 还有 {len(outdated) - 5} 个")
            print()
        else:
            print("✅ 所有包都是最新版本")
            print()

        # 供应链检查
        issues = checker.check_supply_chain()
        if issues:
            print("🔒 供应链问题:")
            for issue in issues:
                print(f"  - {issue['type']}: {issue.get('package', issue.get('reason', ''))}")
            print()
        else:
            print("✅ 供应链安全检查通过")
            print()

    elif args.action == 'baseline':
        checker.save_baseline()

    elif args.action == 'diff':
        print("🔍 对比依赖基线...")
        print()

        changes = checker.compare_with_baseline()
        if changes:
            print(f"发现 {len(changes)} 个变更:")
            for change in changes:
                if change['type'] == 'new_package':
                    print(f"  + {change['package']} {change['version']}")
                elif change['type'] == 'removed_package':
                    print(f"  - {change['package']} {change['version']}")
                elif change['type'] == 'version_changed':
                    print(f"  ~ {change['package']}: {change['old_version']} → {change['new_version']}")
        else:
            print("✅ 无变更")
        print()

    elif args.action == 'full':
        print("🔍 完整安全检查...")
        print("=" * 60)

        # 运行所有检查
        packages = checker.get_installed_packages()
        vulnerabilities = checker.check_vulnerabilities(packages)
        outdated = checker.get_outdated_packages()
        issues = checker.check_supply_chain()
        changes = checker.compare_with_baseline()

        # 汇总
        print(f"已安装包: {len(packages)}")
        print(f"已知漏洞: {len(vulnerabilities)}")
        print(f"过时包: {len(outdated)}")
        print(f"供应链问题: {len(issues)}")
        print(f"依赖变更: {len(changes)}")
        print()

        # 风险评估
        risk_level = "低"
        if vulnerabilities:
            risk_level = "高"
        elif len(outdated) > 5 or issues:
            risk_level = "中"

        print(f"总体风险等级: {risk_level}")
        print()

        # 建议
        if vulnerabilities or outdated or issues:
            print("💡 建议:")
            if vulnerabilities:
                print("  - 立即更新有漏洞的包")
            if outdated:
                print("  - 更新过时的包")
            if issues:
                print("  - 审查供应链问题")
            if changes:
                print("  - 审查依赖变更")
        else:
            print("✅ 依赖安全状况良好")


if __name__ == "__main__":
    main()
