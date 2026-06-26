#!/usr/bin/env python3
"""
代码变更分析工具
用于分析git变更，提取修改信息供AI审核助手使用
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class FileChange:
    """文件变更信息"""
    path: str
    change_type: str  # added, modified, deleted, renamed
    additions: int
    deletions: int
    is_binary: bool
    file_type: str  # source, config, test, doc, other
    
    def to_dict(self):
        return asdict(self)


@dataclass
class ChangeAnalysis:
    """变更分析结果"""
    timestamp: str
    total_files: int
    total_additions: int
    total_deletions: int
    changes: List[FileChange]
    risk_level: str  # high, medium, low
    suspicious_files: List[str]
    
    def to_dict(self):
        return {
            'timestamp': self.timestamp,
            'total_files': self.total_files,
            'total_additions': self.total_additions,
            'total_deletions': self.total_deletions,
            'changes': [c.to_dict() for c in self.changes],
            'risk_level': self.risk_level,
            'suspicious_files': self.suspicious_files
        }


class GitChangeAnalyzer:
    """Git变更分析器"""
    
    # 配置文件模式
    CONFIG_PATTERNS = {
        'package.json', 'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
        'tsconfig.json', 'tsconfig.*.json',
        '.eslintrc', '.eslintrc.*', '.prettierrc', '.prettierrc.*',
        'webpack.config.js', 'webpack.*.js', 'vite.config.*',
        '.env', '.env.*', 'config.*',
        'Dockerfile', 'docker-compose.*',
        '.gitignore', '.dockerignore'
    }
    
    # 源代码扩展名
    SOURCE_EXTENSIONS = {
        '.js', '.jsx', '.ts', '.tsx', '.py', '.java', '.go', 
        '.rs', '.c', '.cpp', '.h', '.cs', '.rb', '.php'
    }
    
    # 测试文件模式
    TEST_PATTERNS = {
        '*.test.js', '*.test.ts', '*.test.jsx', '*.test.tsx',
        '*.spec.js', '*.spec.ts', '*.spec.jsx', '*.spec.tsx',
        'test_*.py', '*_test.py', '*_test.go',
        '*Tests.java', '*Test.java'
    }
    
    # 文档文件扩展名
    DOC_EXTENSIONS = {'.md', '.txt', '.rst', '.adoc'}
    
    def __init__(self, repo_path: str = '.'):
        self.repo_path = Path(repo_path).resolve()
        
    def get_git_diff(self, commit_hash: Optional[str] = None) -> str:
        """获取git diff输出"""
        try:
            if commit_hash:
                # 获取指定commit的变更
                cmd = ['git', 'show', '--numstat', '--format=', commit_hash]
            else:
                # 获取工作区变更
                cmd = ['git', 'diff', '--numstat']
            
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Git命令执行失败: {e}", file=sys.stderr)
            return ""
    
    def get_staged_diff(self) -> str:
        """获取暂存区变更"""
        try:
            cmd = ['git', 'diff', '--cached', '--numstat']
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Git命令执行失败: {e}", file=sys.stderr)
            return ""
    
    def classify_file_type(self, file_path: str) -> str:
        """判断文件类型"""
        path = Path(file_path)
        name = path.name
        ext = path.suffix.lower()
        
        # 检查是否为配置文件
        for pattern in self.CONFIG_PATTERNS:
            if pattern.startswith('*'):
                if name.endswith(pattern[1:]):
                    return 'config'
            elif name == pattern:
                return 'config'
        
        # 检查是否为测试文件
        for pattern in self.TEST_PATTERNS:
            if pattern.startswith('*'):
                if name.endswith(pattern[1:]):
                    return 'test'
            elif pattern.endswith('*'):
                if name.startswith(pattern[:-1]):
                    return 'test'
            elif name == pattern:
                return 'test'
        
        # 检查扩展名
        if ext in self.SOURCE_EXTENSIONS:
            return 'source'
        elif ext in self.DOC_EXTENSIONS:
            return 'doc'
        else:
            return 'other'
    
    def parse_diff(self, diff_output: str) -> List[FileChange]:
        """解析git diff输出"""
        changes = []
        
        for line in diff_output.strip().split('\n'):
            if not line:
                continue
                
            parts = line.split('\t')
            if len(parts) < 3:
                continue
            
            additions, deletions, file_path = parts[0], parts[1], parts[2]
            
            # 处理重命名文件
            if ' => ' in file_path:
                old_path, new_path = file_path.split(' => ')
                file_path = new_path
                change_type = 'renamed'
            elif additions == '0' and deletions == '0':
                change_type = 'renamed'
            elif additions == '-' and deletions == '-':
                # 二进制文件
                changes.append(FileChange(
                    path=file_path,
                    change_type='modified',
                    additions=0,
                    deletions=0,
                    is_binary=True,
                    file_type=self.classify_file_type(file_path)
                ))
                continue
            elif int(additions) > 0 and int(deletions) == 0:
                change_type = 'added'
            elif int(additions) == 0 and int(deletions) > 0:
                change_type = 'deleted'
            else:
                change_type = 'modified'
            
            try:
                changes.append(FileChange(
                    path=file_path,
                    change_type=change_type,
                    additions=int(additions) if additions != '-' else 0,
                    deletions=int(deletions) if deletions != '-' else 0,
                    is_binary=False,
                    file_type=self.classify_file_type(file_path)
                ))
            except ValueError:
                continue
        
        return changes
    
    def assess_risk(self, changes: List[FileChange]) -> tuple:
        """评估变更风险等级"""
        suspicious = []
        risk_score = 0
        
        for change in changes:
            # 配置文件修改
            if change.file_type == 'config':
                risk_score += 3
                suspicious.append(f"{change.path} (配置文件)")
            
            # 删除文件
            if change.change_type == 'deleted':
                risk_score += 2
                suspicious.append(f"{change.path} (文件删除)")
            
            # 大规模修改
            if change.additions + change.deletions > 100:
                risk_score += 2
                suspicious.append(f"{change.path} (大规模修改: +{change.additions}/-{change.deletions})")
        
        # 文件数量过多
        if len(changes) > 10:
            risk_score += 2
        
        # 确定风险等级
        if risk_score >= 8:
            risk_level = 'high'
        elif risk_score >= 4:
            risk_level = 'medium'
        else:
            risk_level = 'low'
        
        return risk_level, suspicious
    
    def analyze(self, commit_hash: Optional[str] = None, 
                staged: bool = False) -> ChangeAnalysis:
        """执行变更分析"""
        # 获取diff
        if staged:
            diff = self.get_staged_diff()
        else:
            diff = self.get_git_diff(commit_hash)
        
        # 解析变更
        changes = self.parse_diff(diff)
        
        # 计算统计
        total_additions = sum(c.additions for c in changes)
        total_deletions = sum(c.deletions for c in changes)
        
        # 评估风险
        risk_level, suspicious = self.assess_risk(changes)
        
        return ChangeAnalysis(
            timestamp=datetime.now().isoformat(),
            total_files=len(changes),
            total_additions=total_additions,
            total_deletions=total_deletions,
            changes=changes,
            risk_level=risk_level,
            suspicious_files=suspicious
        )


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='分析Git代码变更')
    parser.add_argument('--commit', '-c', help='指定commit hash')
    parser.add_argument('--staged', '-s', action='store_true', 
                       help='分析暂存区变更')
    parser.add_argument('--output', '-o', choices=['json', 'text'], 
                       default='text', help='输出格式')
    parser.add_argument('--repo', '-r', default='.', help='Git仓库路径')
    
    args = parser.parse_args()
    
    analyzer = GitChangeAnalyzer(args.repo)
    analysis = analyzer.analyze(args.commit, args.staged)
    
    if args.output == 'json':
        print(json.dumps(analysis.to_dict(), indent=2, ensure_ascii=False))
    else:
        print(f"\n{'='*60}")
        print(f"代码变更分析报告")
        print(f"{'='*60}")
        print(f"分析时间: {analysis.timestamp}")
        print(f"修改文件数: {analysis.total_files}")
        print(f"新增行数: +{analysis.total_additions}")
        print(f"删除行数: -{analysis.total_deletions}")
        print(f"风险等级: {analysis.risk_level.upper()}")
        
        if analysis.suspicious_files:
            print(f"\n可疑修改:")
            for file in analysis.suspicious_files:
                print(f"  ⚠️  {file}")
        
        print(f"\n文件变更详情:")
        print(f"{'类型':<10} {'文件':<40} {'变更':<15}")
        print(f"{'-'*10} {'-'*40} {'-'*15}")
        
        for change in analysis.changes:
            emoji = {
                'added': '➕',
                'modified': '📝',
                'deleted': '❌',
                'renamed': '🔄'
            }.get(change.change_type, '?')
            
            change_str = f"+{change.additions}/-{change.deletions}"
            print(f"{emoji} {change.change_type:<8} {change.path:<40} {change_str:<15}")
        
        print(f"\n{'='*60}\n")


if __name__ == '__main__':
    main()
