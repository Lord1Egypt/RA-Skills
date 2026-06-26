#!/usr/bin/env python3
"""
GitCode PR Code Review Script
Analyzes PR changes and outputs top 3 issues with severity scores.
Includes automatic line number verification.
"""

import sys
import json
import re
import urllib.request
import urllib.error
import os
import tempfile
import shutil
import atexit
from typing import List, Dict, Any, Optional, Tuple


class CodeReviewer:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://gitcode.com/api/v5"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "User-Agent": "OpenClaw-CodeReview/1.0"
        }
        self.token = token
        self.temp_dir = tempfile.mkdtemp(prefix='code_review_')
        self.file_cache = {}  # Cache downloaded files
        
        # Register cleanup on exit
        atexit.register(self.cleanup)
    
    def cleanup(self):
        """Clean up temporary files on exit."""
        if hasattr(self, 'temp_dir') and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
                print(f"Cleaned up temp directory: {self.temp_dir}", file=sys.stderr)
            except Exception as e:
                print(f"Warning: Failed to clean up temp directory: {e}", file=sys.stderr)

    def parse_pr_url(self, pr_url: str) -> tuple:
        """Extract owner, repo, PR number from GitCode URL."""
        pattern = r"https?://gitcode\.com/([^/]+)/([^/]+)/pull/(\d+)"
        match = re.match(pattern, pr_url)
        if not match:
            raise ValueError(f"Invalid GitCode PR URL: {pr_url}")
        return match.group(1), match.group(2), int(match.group(3))

    def fetch_pr_files(self, owner: str, repo: str, pr_number: int) -> List[Dict]:
        """Fetch changed files and diff from PR using API."""
        # Get file list
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}/files"
        req = urllib.request.Request(url, headers=self.headers)
        
        with urllib.request.urlopen(req, timeout=30) as response:
            files = json.loads(response.read().decode('utf-8'))
        
        # Get full diff once
        diff_url = f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}/diff"
        diff_req = urllib.request.Request(diff_url, headers=self.headers)
        
        try:
            with urllib.request.urlopen(diff_req, timeout=30) as diff_response:
                full_diff = diff_response.read().decode('utf-8')
        except Exception as e:
            print(f"Warning: Could not fetch diff: {e}", file=sys.stderr)
            full_diff = ''
        
        # Extract patch for each file
        for file_info in files:
            filename = file_info.get('filename', '')
            file_info['patch'] = self.extract_file_diff(full_diff, filename)
        
        return files
    
    def extract_file_diff(self, diff_content: str, target_file: str) -> str:
        """Extract diff for a specific file from the full diff."""
        if not diff_content:
            return ''
        
        lines = diff_content.split('\n')
        result = []
        in_target_file = False
        
        for line in lines:
            if line.startswith('diff --git'):
                # Check if we're entering the target file
                in_target_file = target_file in line
                if in_target_file:
                    result.append(line)
            elif in_target_file:
                result.append(line)
                # Check if we're at the end of this file's diff
                if line.startswith('diff --git'):
                    break
        
        return '\n'.join(result)

    def download_file_content(self, owner: str, repo: str, sha: str, file_path: str) -> Optional[str]:
        """Download the actual file content from the PR branch."""
        cache_key = f"{owner}/{repo}/{sha}/{file_path}"
        if cache_key in self.file_cache:
            return self.file_cache[cache_key]
        
        raw_url = f"https://raw.gitcode.com/{owner}/{repo}/raw/{sha}/{file_path}"
        try:
            req = urllib.request.Request(raw_url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=30) as response:
                content = response.read().decode('utf-8')
                self.file_cache[cache_key] = content
                return content
        except Exception as e:
            print(f"Warning: Could not download {file_path}: {e}", file=sys.stderr)
            return None

    def find_exact_line_number(self, file_content: str, code_snippet: str) -> Optional[int]:
        """Find the exact line number of a code snippet in the file."""
        if not file_content or not code_snippet:
            return None
        
        lines = file_content.split('\n')
        snippet_lines = code_snippet.strip().split('\n')
        snippet_first_line = snippet_lines[0].strip()
        
        for i, line in enumerate(lines, 1):
            if snippet_first_line in line:
                # Verify the full snippet matches
                match = True
                for j, snippet_line in enumerate(snippet_lines):
                    if i + j - 1 < len(lines):
                        if snippet_line.strip() not in lines[i + j - 1]:
                            match = False
                            break
                    else:
                        match = False
                        break
                
                if match:
                    return i
        
        return None

    def verify_and_correct_line_numbers(self, owner: str, repo: str, sha: str, issues: List[Dict]) -> List[Dict]:
        """Verify and correct line numbers for all issues."""
        corrected_issues = []
        verification_stats = {"corrected": 0, "verified": 0, "failed": 0}
        
        print(f"\nVerifying line numbers for {len(issues)} issues...", file=sys.stderr)
        
        for issue in issues:
            file_path = issue.get('file', '')
            original_line = issue.get('line', 0)
            code_snippet = issue.get('code', '')
            
            if not code_snippet:
                print(f"  ⚠️  Skipping {file_path}:{original_line} - no code snippet available", file=sys.stderr)
                verification_stats["failed"] += 1
                corrected_issues.append(issue)
                continue
            
            # Download the file content
            file_content = self.download_file_content(owner, repo, sha, file_path)
            
            if not file_content:
                print(f"  ⚠️  Could not download {file_path}, keeping original line {original_line}", file=sys.stderr)
                issue['line_verified'] = False
                verification_stats["failed"] += 1
                corrected_issues.append(issue)
                continue
            
            # Find the exact line number
            exact_line = self.find_exact_line_number(file_content, code_snippet)
            
            if exact_line:
                if exact_line != original_line:
                    print(f"  ✅ Corrected: {file_path}:{original_line} -> {exact_line}", file=sys.stderr)
                    issue['line'] = exact_line
                    issue['original_line'] = original_line
                    issue['line_verified'] = True
                    verification_stats["corrected"] += 1
                else:
                    print(f"  ✅ Verified: {file_path}:{original_line}", file=sys.stderr)
                    issue['line_verified'] = True
                    verification_stats["verified"] += 1
            else:
                print(f"  ⚠️  Could not find code snippet in {file_path}, keeping original line {original_line}", file=sys.stderr)
                issue['line_verified'] = False
                verification_stats["failed"] += 1
            
            corrected_issues.append(issue)
        
        # Print summary
        print(f"\nLine verification complete:", file=sys.stderr)
        print(f"  - Verified (correct): {verification_stats['verified']}", file=sys.stderr)
        print(f"  - Corrected: {verification_stats['corrected']}", file=sys.stderr)
        print(f"  - Failed/Unverified: {verification_stats['failed']}", file=sys.stderr)
        
        return corrected_issues

    def calculate_diff_position(self, patch: str, file_line: int) -> Optional[int]:
        """Calculate the position in the diff for a given file line number.
        
        GitCode API uses 'position' which is the line number within the diff hunk,
        not the absolute file line number.
        """
        if not patch:
            return None
        
        lines = patch.split('\n')
        position = 0
        current_file_line = 0
        hunk_start_line = 0
        in_hunk = False
        
        for line in lines:
            if line.startswith('@@'):
                # Parse hunk header: @@ -old_start,old_count +new_start,new_count @@
                match = re.search(r'\+(\d+)', line)
                if match:
                    hunk_start_line = int(match.group(1))
                    current_file_line = hunk_start_line
                    in_hunk = True
                continue
            
            if not in_hunk:
                continue
            
            if line.startswith('+') and not line.startswith('+++'):
                position += 1
                if current_file_line == file_line:
                    return position
                current_file_line += 1
            elif line.startswith('-') and not line.startswith('---'):
                position += 1
            elif not line.startswith('diff') and not line.startswith('index'):
                position += 1
                if current_file_line == file_line:
                    return position
                current_file_line += 1
        
        return None

    def analyze_code(self, file_path: str, patch: str) -> List[Dict]:
        """Analyze code changes and return issues."""
        issues = []
        lines = patch.split('\n')
        line_number = 0
        current_added_lines = []  # Store added lines for context
        
        for line in lines:
            if line.startswith('@@'):
                # Parse line number from hunk header
                match = re.search(r'\+(\d+)', line)
                if match:
                    line_number = int(match.group(1))
                current_added_lines = []
                continue
            
            if line.startswith('+') and not line.startswith('+++'):
                added_line = line[1:]
                line_issues = self.check_line_issues(file_path, line_number, added_line, patch)
                
                # Add code snippet to each issue
                for issue in line_issues:
                    issue['code'] = added_line.strip()
                    issue['code_context'] = self.get_code_context(patch, line_number)
                
                issues.extend(line_issues)
                line_number += 1
            elif not line.startswith('-') and not line.startswith('---'):
                line_number += 1
        
        return issues
    
    def get_code_context(self, patch: str, target_line: int, context_lines: int = 3) -> str:
        """Get surrounding code context for a line."""
        lines = patch.split('\n')
        result = []
        current_line = 0
        
        for line in lines:
            if line.startswith('@@'):
                match = re.search(r'\+(\d+)', line)
                if match:
                    current_line = int(match.group(1))
                continue
            
            if line.startswith('+') and not line.startswith('+++'):
                if abs(current_line - target_line) <= context_lines:
                    prefix = ">>>" if current_line == target_line else "   "
                    result.append(f"{prefix} {line[1:]}")
                current_line += 1
            elif not line.startswith('-') and not line.startswith('---') and not line.startswith('diff'):
                if abs(current_line - target_line) <= context_lines:
                    result.append(f"    {line}")
                current_line += 1
        
        return '\n'.join(result[-10:])  # Limit context size

    def check_line_issues(self, file_path: str, line_number: int, code: str, patch: str = "") -> List[Dict]:
        """Check a single line for issues. Only report real problems."""
        issues = []
        code_lower = code.lower()
        code_stripped = code.strip()
        
        # Skip empty lines and comments
        if not code_stripped or code_stripped.startswith('//') or code_stripped.startswith('/*'):
            return issues
        
        # ==================== Critical Issues (Severity 9-10) ====================
        
        # SQL injection - string concatenation in SQL
        if re.search(r'(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE)\s+.*["\']\s*\+', code, re.IGNORECASE):
            if not re.search(r'prepare|parameter|bind', code_lower):
                issues.append({
                    "file": file_path,
                    "line": line_number,
                    "type": "安全问题",
                    "severity": 10,
                    "description": "SQL注入风险: 字符串拼接构建SQL语句",
                    "suggestion": "使用参数化查询、预编译语句或ORM，永远不要拼接用户输入到SQL"
                })
        
        # Command injection
        if re.search(r'(exec|system|popen|subprocess)\s*\([^)]*["\'].*\+', code, re.IGNORECASE):
            issues.append({
                "file": file_path,
                "line": line_number,
                "type": "安全问题",
                "severity": 10,
                "description": "命令注入风险: 用户输入直接拼接到系统命令",
                "suggestion": "使用参数列表传递命令参数，避免shell=True，或完全禁止用户输入进入命令"
            })
        
        # XSS - innerHTML with user input
        if 'innerhtml' in code_lower and ('user' in code_lower or 'input' in code_lower or 'data' in code_lower):
            if 'sanitize' not in code_lower and 'escape' not in code_lower and 'textcontent' not in code_lower:
                issues.append({
                    "file": file_path,
                    "line": line_number,
                    "type": "安全问题",
                    "severity": 9,
                    "description": "XSS风险: 用户数据直接插入innerHTML",
                    "suggestion": "使用textContent代替innerHTML，或使用DOMPurify等库清理HTML"
                })
        
        # eval usage
        if re.search(r'\beval\s*\(', code):
            issues.append({
                "file": file_path,
                "line": line_number,
                "type": "安全问题",
                "severity": 9,
                "description": "严重安全风险: 使用eval执行动态代码",
                "suggestion": "完全避免使用eval，改用JSON.parse、Function构造器或其他安全替代方案"
            })
        
        # ==================== High Severity Issues (Severity 7-8) ====================
        
        # Unhandled async/await errors
        if re.search(r'await\s+', code) and 'try' not in code_lower:
            # Check if it's inside a try block by looking at context
            if not self._is_in_try_block(patch, line_number):
                issues.append({
                    "file": file_path,
                    "line": line_number,
                    "type": "代码实现问题",
                    "severity": 7,
                    "description": "异步操作可能未处理异常",
                    "suggestion": "使用try-catch包裹await，或使用.catch()处理Promise错误"
                })
        
        # Missing return in non-void function (simplified check)
        if re.search(r'function\s+\w+\s*\([^)]*\)\s*\{', code):
            if not self._has_return_statement(patch, line_number):
                issues.append({
                    "file": file_path,
                    "line": line_number,
                    "type": "代码实现问题",
                    "severity": 6,
                    "description": "函数可能缺少返回值",
                    "suggestion": "确保所有代码路径都有返回值，或明确标记为void"
                })
        
        # Hardcoded credentials
        if re.search(r'(password|secret|key|token)\s*[=:]\s*["\'][^"\']{4,}["\']', code_lower):
            if not re.search(r'(getenv|env\.|config|settings)', code_lower):
                issues.append({
                    "file": file_path,
                    "line": line_number,
                    "type": "安全问题",
                    "severity": 9,
                    "description": "硬编码敏感信息: 密码/密钥直接写在代码中",
                    "suggestion": "使用环境变量、配置文件或密钥管理服务存储敏感信息"
                })
        
        # ==================== Medium Severity Issues (Severity 5-6) ====================
        
        # Resource leak - file/database connection without close
        if re.search(r'(open|connect|create)\s*\(', code_lower):
            if not self._has_cleanup_in_scope(patch, line_number, ['close', 'disconnect', 'release', 'end']):
                issues.append({
                    "file": file_path,
                    "line": line_number,
                    "type": "代码实现问题",
                    "severity": 6,
                    "description": "可能的资源泄漏: 打开的资源未关闭",
                    "suggestion": "使用try-finally或with语句确保资源被正确释放"
                })
        
        # Infinite loop risk
        if re.search(r'while\s*\(\s*(true|1)\s*\)', code_lower):
            if 'break' not in code_lower and 'return' not in code_lower:
                issues.append({
                    "file": file_path,
                    "line": line_number,
                    "type": "代码实现问题",
                    "severity": 6,
                    "description": "潜在无限循环: while(true)没有break条件",
                    "suggestion": "确保循环有明确的退出条件，或添加break/return语句"
                })
        
        # Race condition in async code
        if re.search(r'await.*\.then\(|await.*\.catch\(', code_lower):
            issues.append({
                "file": file_path,
                "line": line_number,
                "type": "代码实现问题",
                "severity": 5,
                "description": "可能的竞态条件: await和Promise链混用",
                "suggestion": "统一使用async/await或Promise链，不要混用"
            })
        
        return issues
    
    def _is_in_try_block(self, patch: str, line_number: int) -> bool:
        """Check if current line is inside a try block."""
        lines = patch.split('\n')
        current_line = 0
        in_try = False
        brace_count = 0
        
        for line in lines:
            if line.startswith('@@'):
                match = re.search(r'\+(\d+)', line)
                if match:
                    current_line = int(match.group(1))
                continue
            
            if line.startswith('+') and not line.startswith('+++'):
                code = line[1:]
                if 'try' in code.lower() and '{' in code:
                    in_try = True
                    brace_count = code.count('{') - code.count('}')
                elif in_try:
                    brace_count += code.count('{') - code.count('}')
                    if brace_count <= 0:
                        in_try = False
                
                if current_line == line_number:
                    return in_try
                current_line += 1
            elif not line.startswith('-') and not line.startswith('---'):
                if current_line == line_number:
                    return in_try
                current_line += 1
        
        return False
    
    def _has_return_statement(self, patch: str, line_number: int) -> bool:
        """Check if function has return statement."""
        lines = patch.split('\n')
        current_line = 0
        in_function = False
        brace_count = 0
        
        for line in lines:
            if line.startswith('@@'):
                match = re.search(r'\+(\d+)', line)
                if match:
                    current_line = int(match.group(1))
                continue
            
            if line.startswith('+') and not line.startswith('+++'):
                code = line[1:]
                if re.search(r'function\s+\w+', code):
                    in_function = True
                    brace_count = code.count('{') - code.count('}')
                elif in_function:
                    brace_count += code.count('{') - code.count('}')
                    if 'return' in code:
                        return True
                    if brace_count <= 0:
                        in_function = False
                
                current_line += 1
            elif not line.startswith('-') and not line.startswith('---'):
                current_line += 1
        
        return False
    
    def _has_cleanup_in_scope(self, patch: str, line_number: int, cleanup_keywords: List[str]) -> bool:
        """Check if there's cleanup code in the same scope."""
        lines = patch.split('\n')
        current_line = 0
        found_open = False
        
        for line in lines:
            if line.startswith('@@'):
                match = re.search(r'\+(\d+)', line)
                if match:
                    current_line = int(match.group(1))
                continue
            
            if line.startswith('+') and not line.startswith('+++'):
                code = line[1:].lower()
                if current_line >= line_number:
                    # Check for cleanup after the open
                    for keyword in cleanup_keywords:
                        if keyword in code:
                            return True
                current_line += 1
            elif not line.startswith('-') and not line.startswith('---'):
                current_line += 1
        
        return False

    def review_pr(self, pr_url: str) -> Dict[str, Any]:
        """Main entry point for PR review."""
        owner, repo, pr_number = self.parse_pr_url(pr_url)
        
        print(f"Reviewing PR: {owner}/{repo}#{pr_number}", file=sys.stderr)
        
        files = self.fetch_pr_files(owner, repo, pr_number)
        print(f"Found {len(files)} changed files", file=sys.stderr)
        
        # Get the PR's head SHA for downloading files
        pr_sha = None
        if files and len(files) > 0:
            pr_sha = files[0].get('sha')
        
        # Debug: show first file info
        if files:
            first = files[0]
            print(f"First file: {first.get('filename')}", file=sys.stderr)
            print(f"Has patch: {bool(first.get('patch'))}", file=sys.stderr)
            if first.get('patch'):
                print(f"Patch length: {len(first['patch'])}", file=sys.stderr)
                print(f"Patch preview: {first['patch'][:200]}", file=sys.stderr)
        
        all_issues = []
        
        for file_info in files:
            file_path = file_info.get('filename', '')
            patch = file_info.get('patch', '')
            
            # Skip binary files and non-code files
            if not patch or any(file_path.endswith(ext) for ext in ['.md', '.txt', '.json', '.yml', '.yaml']):
                continue
            
            issues = self.analyze_code(file_path, patch)
            all_issues.extend(issues)
        
        # Sort by severity descending
        all_issues.sort(key=lambda x: x['severity'], reverse=True)
        
        # Take top 3
        top_issues = all_issues[:3]
        
        # Verify and correct line numbers
        if pr_sha and top_issues:
            print(f"\nVerifying line numbers using SHA: {pr_sha}", file=sys.stderr)
            top_issues = self.verify_and_correct_line_numbers(owner, repo, pr_sha, top_issues)
        
        result = {
            "pr_url": pr_url,
            "total_issues": len(all_issues),
            "reviewed_issues": len(top_issues),
            "issues": top_issues
        }
        
        return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python review_pr.py <pr_url> [token]", file=sys.stderr)
        print("Or set GITCODE_TOKEN environment variable", file=sys.stderr)
        sys.exit(1)
    
    pr_url = sys.argv[1]
    token = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not token:
        token = os.environ.get('GITCODE_TOKEN')
    
    if not token:
        print("Error: GitCode token required. Provide as argument or set GITCODE_TOKEN env var.", file=sys.stderr)
        sys.exit(1)
    
    reviewer = CodeReviewer(token)
    result = reviewer.review_pr(pr_url)
    
    # Save to file
    output_file = "review_result.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\nReview complete. Result saved to: {output_file}", file=sys.stderr)
    print(f"Total issues found: {result['total_issues']}", file=sys.stderr)
    print(f"Top {result['reviewed_issues']} issues selected with verified line numbers", file=sys.stderr)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
