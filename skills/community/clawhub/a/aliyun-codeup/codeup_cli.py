#!/usr/bin/env python3
"""
阿里云云效 Codeup CLI 工具
查询项目分支、提交记录等
"""

import subprocess
import sys
import os
import tempfile
import shutil
from urllib.parse import urlparse
from datetime import datetime

def get_token():
    """从环境变量获取令牌"""
    token = os.getenv('YUNXIAO_PERSONAL_TOKEN')
    if not token:
        print("❌ 错误：未配置 YUNXIAO_PERSONAL_TOKEN 环境变量")
        print("请在 ~/.zshrc 中添加：export YUNXIAO_PERSONAL_TOKEN=\"pt-xxx\"")
        sys.exit(1)
    return token

def parse_project_url(url):
    """解析项目 URL"""
    parsed = urlparse(url)
    path = parsed.path.strip('/')
    # 移除末尾的 /branches, /commits, /tree 等
    if '/' in path:
        parts = path.split('/')
        if parts[-1] in ['branches', 'commits', 'tree', 'blob', '-']:
            path = '/'.join(parts[:-1])
    return path

def clone_and_query(url, query_type='branches'):
    """临时克隆并查询"""
    token = get_token()
    project_path = parse_project_url(url)
    
    # 创建临时目录
    tmp_dir = tempfile.mkdtemp(prefix='codeup_')
    repo_name = project_path.split('/')[-1]
    repo_path = os.path.join(tmp_dir, repo_name)
    
    try:
        # 克隆仓库（获取所有分支信息）
        git_url = f"https://oauth2:{token}@codeup.aliyun.com/{project_path}.git"
        print(f"📥 正在克隆项目 {repo_name}...")
        subprocess.run(
            ['git', 'clone', '--quiet', '--no-tags', git_url, repo_path],
            check=True,
            capture_output=True,
            timeout=120
        )
        
        if query_type == 'branches':
            return query_branches(repo_path, repo_name)
        elif query_type == 'commits':
            return query_commits(repo_path, repo_name)
        elif query_type == 'stats':
            return query_stats(repo_path, repo_name)
        else:
            return {'success': False, 'error': f'未知的查询类型：{query_type}'}
        
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'error': '克隆超时，项目可能过大'
        }
    except subprocess.CalledProcessError as e:
        return {
            'success': False,
            'error': f'Git 操作失败：{e.stderr.decode() if e.stderr else str(e)}'
        }
    finally:
        # 清理临时目录
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir, ignore_errors=True)

def query_branches(repo_path, repo_name):
    """查询分支列表"""
    # 获取所有分支
    result = subprocess.run(
        ['git', 'branch', '-a', '--sort=-committerdate'],
        cwd=repo_path,
        capture_output=True,
        text=True,
        check=True
    )
    
    # 解析分支
    branches = []
    for line in result.stdout.strip().split('\n'):
        if line.strip() and 'HEAD' not in line:
            branch = line.replace('*', '').replace('remotes/origin/', '').strip()
            if branch:
                branches.append(branch)
    
    # 分类统计
    main_branches = [b for b in branches if b in ['master', 'main', 'develop']]
    feature_branches = [b for b in branches if b.startswith('feature/') or b.startswith('feat/')]
    hotfix_branches = [b for b in branches if b.startswith('hotfix/') or b.startswith('fix/')]
    other_branches = [b for b in branches if b not in main_branches + feature_branches + hotfix_branches]
    
    return {
        'success': True,
        'project': repo_name,
        'branches': branches,
        'total': len(branches),
        'categories': {
            'main': main_branches,
            'feature': feature_branches,
            'hotfix': hotfix_branches,
            'other': other_branches
        }
    }

def query_commits(repo_path, repo_name):
    """查询最近提交"""
    result = subprocess.run(
        ['git', 'log', '--oneline', '-20', '--all'],
        cwd=repo_path,
        capture_output=True,
        text=True,
        check=True
    )
    
    commits = []
    for line in result.stdout.strip().split('\n'):
        if line.strip():
            parts = line.split(' ', 1)
            if len(parts) == 2:
                commits.append({
                    'hash': parts[0],
                    'message': parts[1]
                })
    
    return {
        'success': True,
        'project': repo_name,
        'commits': commits,
        'total': len(commits)
    }

def query_stats(repo_path, repo_name):
    """查询仓库统计"""
    # 分支数
    result = subprocess.run(
        ['git', 'branch', '-a'],
        cwd=repo_path,
        capture_output=True,
        text=True,
        check=True
    )
    branch_count = len([l for l in result.stdout.strip().split('\n') if l.strip() and 'HEAD' not in l])
    
    # 提交数
    result = subprocess.run(
        ['git', 'rev-list', '--count', '--all'],
        cwd=repo_path,
        capture_output=True,
        text=True,
        check=True
    )
    commit_count = int(result.stdout.strip())
    
    # 贡献者数
    result = subprocess.run(
        ['git', 'log', '--format=%aN', '--all'],
        cwd=repo_path,
        capture_output=True,
        text=True,
        check=True
    )
    contributors = len(set(result.stdout.strip().split('\n')))
    
    return {
        'success': True,
        'project': repo_name,
        'stats': {
            'branches': branch_count,
            'commits': commit_count,
            'contributors': contributors
        }
    }

def format_output(result, query_type):
    """格式化输出"""
    if not result['success']:
        print(f"❌ 错误：{result['error']}")
        return
    
    print(f"\n📊 项目：{result['project']}")
    
    if query_type == 'branches':
        print(f"📊 分支总数：{result['total']}\n")
        
        cats = result['categories']
        if cats['main']:
            print("【主分支】")
            for b in cats['main']:
                print(f"  ✓ {b}")
            print()
        
        if cats['feature']:
            print(f"【功能分支】({len(cats['feature'])})")
            for b in sorted(cats['feature'])[:10]:
                print(f"  🔧 {b}")
            if len(cats['feature']) > 10:
                print(f"  ... 还有 {len(cats['feature']) - 10} 个")
            print()
        
        if cats['hotfix']:
            print(f"【热修复分支】({len(cats['hotfix'])})")
            for b in sorted(cats['hotfix'])[:10]:
                print(f"  🐛 {b}")
            if len(cats['hotfix']) > 10:
                print(f"  ... 还有 {len(cats['hotfix']) - 10} 个")
            print()
        
        if cats['other']:
            print(f"【其他分支】({len(cats['other'])})")
            for b in sorted(cats['other'])[:5]:
                print(f"  📁 {b}")
    
    elif query_type == 'commits':
        print(f"📊 最近提交：{result['total']}\n")
        for i, commit in enumerate(result['commits'][:10], 1):
            print(f"  {i}. {commit['hash']} {commit['message']}")
    
    elif query_type == 'stats':
        stats = result['stats']
        print(f"\n【仓库统计】")
        print(f"  分支数：{stats['branches']}")
        print(f"  提交数：{stats['commits']}")
        print(f"  贡献者：{stats['contributors']}")
    
    print()

def main():
    if len(sys.argv) < 2:
        print("阿里云云效 Codeup 工具")
        print("\n用法:")
        print("  codeup_cli.py <项目 URL> [查询类型]")
        print("\n查询类型:")
        print("  branches - 查询分支列表（默认）")
        print("  commits  - 查询最近提交")
        print("  stats    - 查询仓库统计")
        print("\n示例:")
        print("  codeup_cli.py https://codeup.aliyun.com/flashexpress/ard/be/tools/data-admin-api")
        print("  codeup_cli.py https://codeup.aliyun.com/... branches")
        sys.exit(1)
    
    url = sys.argv[1]
    query_type = sys.argv[2] if len(sys.argv) > 2 else 'branches'
    
    result = clone_and_query(url, query_type)
    format_output(result, query_type)

if __name__ == '__main__':
    main()
