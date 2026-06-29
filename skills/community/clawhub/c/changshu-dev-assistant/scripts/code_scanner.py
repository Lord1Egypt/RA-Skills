#!/usr/bin/env python3
"""
代码安全扫描器 + 代码质量分析器
为昌叔的代码提供安全扫描与质量分析合二为一的功能

改进:
- 安全扫描修复误报: open()只在不安全模式(w/a/ab/wb)才标记;
  file()只在eval/exec上下文标记; key=排除dict字面量上下文
- 白名单机制: 可排除指定文件/目录
- 代码质量分析: 行长度、复杂度、重复代码检测
- 分级报告: critical/warning/info
"""

import os
import re
import hashlib
import json
from typing import List, Dict, Optional, Set, Tuple
from pathlib import Path
from collections import defaultdict


class CodeScanner:
    """代码安全扫描器 + 代码质量分析器"""

    # 默认扫描的文件扩展名
    DEFAULT_EXTENSIONS = (
        ".py", ".java", ".js", ".ts", ".php", ".c", ".cpp",
        ".h", ".hpp", ".cs", ".rb", ".go", ".rs", ".sql",
        ".html", ".htm", ".jsx", ".tsx", ".vue", ".sh",
    )

    def __init__(
        self,
        whitelist_dirs: Optional[List[str]] = None,
        whitelist_files: Optional[List[str]] = None,
        max_line_length: int = 120,
        max_complexity: int = 15,
        min_duplicate_lines: int = 6,
    ):
        """初始化代码扫描器

        Args:
            whitelist_dirs:  排除的目录列表(相对或绝对路径)
            whitelist_files: 排除的文件列表(相对或绝对路径)
            max_line_length: 行长度警告阈值
            max_complexity:  圈复杂度警告阈值
            min_duplicate_lines: 重复代码块最小行数
        """
        self.whitelist_dirs: Set[str] = set(
            os.path.abspath(d) for d in (whitelist_dirs or [])
        )
        self.whitelist_files: Set[str] = set(
            os.path.abspath(f) for f in (whitelist_files or [])
        )
        self.max_line_length = max_line_length
        self.max_complexity = max_complexity
        self.min_duplicate_lines = min_duplicate_lines

        # ---- 安全漏洞模式 ------------------------------------------------
        self.vulnerability_patterns = {
            "SQL注入": {
                "severity": "critical",
                "patterns": [
                    r"SELECT\s+.*FROM.*WHERE.*\s*=\s*.*%s.*",
                    r"SELECT\s+.*FROM.*WHERE.*\s*=\s*.*\{.*\}.*",
                    r"SELECT\s+.*FROM.*WHERE.*\s*=\s*.*\$.*",
                    r"\.execute\s*\(",
                    r"\.query\s*\(",
                    r"rawsql\s*\(",
                ],
                "advice": "使用参数化查询或预编译语句，避免直接拼接SQL字符串",
            },
            "硬编码密码": {
                "severity": "critical",
                "patterns": [
                    r'password\s*=\s*["\'][^"\']+["\']',
                    r'pwd\s*=\s*["\'][^"\']+["\']',
                    r'passwd\s*=\s*["\'][^"\']+["\']',
                    r'secret\s*=\s*["\'][^"\']+["\']',
                    # key= 排除 dict 字面量上下文(见 _is_key_in_dict_literal)
                    r'key\s*=\s*["\'][^"\']+["\']',
                    r'token\s*=\s*["\'][^"\']+["\']',
                    r'api_key\s*=\s*["\'][^"\']+["\']',
                    r'apikey\s*=\s*["\'][^"\']+["\']',
                ],
                "advice": "将密码/密钥存储在安全的配置文件或环境变量中，避免硬编码在代码中",
            },
            "不安全的文件操作": {
                "severity": "warning",
                "patterns": [
                    # open() 只在不安全模式下标记 — 在 _check_file_vuln 中过滤
                    r"open\s*\(",
                    # file() 只在 eval/exec 上下文标记 — 在 _check_file_vuln 中过滤
                    r"\bfile\s*\(",
                ],
                "advice": "使用安全的文件操作函数，并对文件路径进行验证; open() 请使用 'r' 模式或加路径校验",
            },
            "命令注入": {
                "severity": "critical",
                "patterns": [
                    r"\beval\s*\(",
                    r"\bexec\s*\(",
                    r"\bos\.system\s*\(",
                    r"\bsubprocess\.(call|run|Popen)\s*\(",
                    r"\bshell_exec\s*\(",
                    r"\bpassthru\s*\(",
                    r"\bsystem\s*\(",
                ],
                "advice": "使用安全的API执行系统命令，避免直接执行用户输入",
            },
            "XSS攻击": {
                "severity": "warning",
                "patterns": [
                    r"<script[^>]*>.*</script>",
                    r"\.innerHTML\s*=",
                    r"\.outerHTML\s*=",
                    r"document\.write\s*\(",
                ],
                "advice": "对用户输入进行过滤和转义，避免在HTML中直接插入用户输入",
            },
        }

    # =====================================================================
    # 白名单判断
    # =====================================================================
    def _is_whitelisted(self, file_path: str) -> bool:
        """判断文件是否在白名单中(应被跳过)"""
        abs_path = os.path.abspath(file_path)
        if abs_path in self.whitelist_files:
            return True
        for wd in self.whitelist_dirs:
            if abs_path.startswith(wd + os.sep) or abs_path == wd:
                return True
        return False

    # =====================================================================
    # 误报过滤辅助
    # =====================================================================
    @staticmethod
    def _is_key_in_dict_literal(line: str, match_start: int) -> bool:
        """判断 key= 是否出现在 dict 字面量上下文中

        例如:  {"key": "value"}  或  dict(key="value")  或  func(key="val")
        如果匹配到的 key= 前面紧随逗号+空白 或 左括号, 则认为是 dict/kwargs
        """
        prefix = line[:match_start].rstrip()
        if not prefix:
            return False
        # 逗号 or ( or { 或 [ 后跟空白的场景 -> keyword argument / dict literal
        if re.search(r'[,{(\[]\s*$', prefix):
            return True
        return False

    @staticmethod
    def _is_unsafe_open(line: str) -> bool:
        """判断 open() 调用是否使用了不安全模式(w/a/ab/wb 等)

        open("/path", "r")  -> 安全, 不标记
        open("/path", "w")  -> 不安全, 标记
        open("/path")       -> 默认 'r', 安全
        """
        m = re.search(r'open\s*\(\s*["\'][^"\']+["\']\s*,\s*["\'](\w+)["\']', line)
        if m:
            mode = m.group(1)
            unsafe_modes = {"w", "a", "wb", "ab", "w+", "a+", "w+b", "a+b", "r+"}
            return mode in unsafe_modes
        # 如果只匹配 open(path) 无 mode 参数, 默认是 'r', 安全
        return False

    @staticmethod
    def _is_file_in_dangerous_context(line: str) -> bool:
        """判断 file() 是否出现在 eval/exec 上下文中

        仅当 file() 的参数涉及用户可控输入(如 eval/input/raw_input)时才标记
        """
        # 如果同一行包含 eval/exec + file(, 标记
        if re.search(r'\b(eval|exec)\s*\(.*\bfile\s*\(', line):
            return True
        return False

    # =====================================================================
    # 安全扫描核心
    # =====================================================================
    def _check_security_line(
        self, file_path: str, line_number: int, line: str
    ) -> List[Dict[str, str]]:
        """扫描单行安全漏洞，返回结果列表"""
        findings = []
        for vuln_type, config in self.vulnerability_patterns.items():
            severity = config["severity"]
            advice = config["advice"]
            for pattern in config["patterns"]:
                for m in re.finditer(pattern, line, re.IGNORECASE):
                    # ---- 误报过滤 ----
                    if vuln_type == "不安全的文件操作":
                        if "open" in pattern:
                            if not self._is_unsafe_open(line):
                                continue
                        if "file" in pattern:
                            if not self._is_file_in_dangerous_context(line):
                                continue

                    if vuln_type == "硬编码密码" and "key" in pattern:
                        if self._is_key_in_dict_literal(line, m.start()):
                            continue

                    findings.append({
                        "file": file_path,
                        "line": line_number,
                        "type": "潜在的" + vuln_type + "漏洞",
                        "severity": severity,
                        "code": line.strip(),
                        "message": advice,
                        "position": f"{file_path}:{line_number}",
                    })
        return findings

    def scan_file(self, file_path: str) -> List[Dict[str, str]]:
        """扫描单个文件的安全漏洞"""
        if self._is_whitelisted(file_path):
            return []
        vulnerabilities = []
        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                for line_number, line in enumerate(f, 1):
                    line = line.rstrip("\n")
                    vulns = self._check_security_line(file_path, line_number, line)
                    vulnerabilities.extend(vulns)
        except Exception as e:
            print(f"扫描文件 {file_path} 时出错: {e}")
        return vulnerabilities

    def scan_directory(self, directory_path: str) -> List[Dict[str, str]]:
        """扫描目录中所有源码文件的安全漏洞"""
        all_vulnerabilities = []
        for root, dirs, files in os.walk(directory_path):
            # 裁剪白名单目录，避免进入
            dirs[:] = [
                d for d in dirs
                if not self._is_whitelisted(os.path.join(root, d))
            ]
            for file in files:
                if file.endswith(self.DEFAULT_EXTENSIONS):
                    file_path = os.path.join(root, file)
                    if not self._is_whitelisted(file_path):
                        vulns = self.scan_file(file_path)
                        all_vulnerabilities.extend(vulns)
        return all_vulnerabilities

    # =====================================================================
    # 代码质量分析
    # =====================================================================
    def analyze_file(self, file_path: str) -> Dict[str, object]:
        """对单个文件进行代码质量分析

        Returns:
            {
                "file": str,
                "total_lines": int,
                "code_lines": int,
                "long_lines": [...],          # 超长行
                "max_line_length": int,
                "complexity_blocks": [...],    # 复杂度超标的函数/方法
                "duplicate_hashes": {...},      # 用于重复代码检测的行hash
            }
        """
        if self._is_whitelisted(file_path):
            return {"file": file_path, "skipped": True}

        result = {
            "file": file_path,
            "total_lines": 0,
            "code_lines": 0,
            "long_lines": [],
            "max_line_length": 0,
            "complexity_blocks": [],
            "duplicate_hashes": {},  # hash -> [line_numbers]
        }

        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                lines = f.readlines()
        except Exception as e:
            print(f"分析文件 {file_path} 时出错: {e}")
            return result

        result["total_lines"] = len(lines)

        # Python 复杂度分析状态机
        in_function = False
        func_name = ""
        func_start = 0
        func_complexity = 1  # 基础复杂度

        for line_no, raw_line in enumerate(lines, 1):
            line = raw_line.rstrip("\n")
            stripped = line.strip()

            # 跳过空行和注释
            if not stripped or stripped.startswith("#"):
                continue
            result["code_lines"] += 1

            # --- 行长度检测 ---
            line_len = len(line)
            if line_len > result["max_line_length"]:
                result["max_line_length"] = line_len
            if line_len > self.max_line_length:
                result["long_lines"].append({
                    "line": line_no,
                    "length": line_len,
                    "code": line.strip()[:80],
                    "severity": "info",
                })

            # --- Python 圈复杂度估算 ---
            if file_path.endswith(".py"):
                # 函数/类定义
                func_def = re.match(
                    r'^(\s*)def\s+(\w+)\s*\(', line
                )
                if func_def:
                    # 保存上一个函数
                    if in_function and func_complexity > self.max_complexity:
                        result["complexity_blocks"].append({
                            "name": func_name,
                            "start": func_start,
                            "complexity": func_complexity,
                            "severity": "warning",
                        })
                    in_function = True
                    func_name = func_def.group(2)
                    func_start = line_no
                    func_complexity = 1

                if in_function:
                    # 判断退出函数(同级或更低缩进的非空行)
                    if stripped and not stripped.startswith("#"):
                        current_indent = len(line) - len(line.lstrip())
                        func_indent = len(raw_line) - len(raw_line.lstrip()) if func_def else 0
                        # 只要还在函数体内就增加复杂度
                        for branch in re.findall(
                            r'\b(if|elif|else|for|while|and|or|except|with)\b',
                            line,
                        ):
                            func_complexity += 1

                # 类定义 — 简单标记
                if re.match(r'^\s*class\s+\w+', line):
                    if in_function and func_complexity > self.max_complexity:
                        result["complexity_blocks"].append({
                            "name": func_name,
                            "start": func_start,
                            "complexity": func_complexity,
                            "severity": "warning",
                        })
                    in_function = False

            # --- 重复代码 hash ---
            if stripped:
                # 标准化空白后 hash
                normalized = re.sub(r'\s+', ' ', stripped)
                h = hashlib.md5(normalized.encode("utf-8")).hexdigest()
                if h not in result["duplicate_hashes"]:
                    result["duplicate_hashes"][h] = []
                result["duplicate_hashes"][h].append(line_no)

        # 最后一个函数的复杂度
        if in_function and func_complexity > self.max_complexity:
            result["complexity_blocks"].append({
                "name": func_name,
                "start": func_start,
                "complexity": func_complexity,
                "severity": "warning",
            })

        return result

    def analyze_directory(self, directory_path: str) -> List[Dict[str, object]]:
        """对目录进行代码质量分析"""
        all_results = []
        for root, dirs, files in os.walk(directory_path):
            dirs[:] = [
                d for d in dirs
                if not self._is_whitelisted(os.path.join(root, d))
            ]
            for file in files:
                if file.endswith(self.DEFAULT_EXTENSIONS):
                    file_path = os.path.join(root, file)
                    if not self._is_whitelisted(file_path):
                        r = self.analyze_file(file_path)
                        if not r.get("skipped"):
                            all_results.append(r)
        return all_results

    def detect_duplicates(
        self, analysis_results: List[Dict[str, object]]
    ) -> List[Dict[str, object]]:
        """基于 analyze_file 的 duplicate_hashes 检测跨文件重复代码块

        找到在多个文件(或同文件内不同位置)出现 >= min_duplicate_lines 次的 hash
        """
        global_hashes: Dict[str, List[Dict[str, object]]] = defaultdict(list)
        for res in analysis_results:
            file_path = res["file"]
            for h, line_numbers in res.get("duplicate_hashes", {}).items():
                for ln in line_numbers:
                    global_hashes[h].append({"file": file_path, "line": ln})

        duplicates = []
        for h, occurrences in global_hashes.items():
            if len(occurrences) >= self.min_duplicate_lines:
                duplicates.append({
                    "hash": h,
                    "count": len(occurrences),
                    "occurrences": occurrences[:10],  # 最多展示10处
                    "severity": "info",
                })

        # 按 count 降序
        duplicates.sort(key=lambda x: x["count"], reverse=True)
        return duplicates

    # =====================================================================
    # 分级报告生成
    # =====================================================================
    def generate_report(
        self,
        vulnerabilities: Optional[List[Dict[str, str]]] = None,
        quality_results: Optional[List[Dict[str, object]]] = None,
        duplicates: Optional[List[Dict[str, object]]] = None,
    ) -> str:
        """生成分级报告 (critical / warning / info)"""
        sections = []
        sections.append("=" * 60)
        sections.append("  代码扫描报告 (安全 + 质量)")
        sections.append("=" * 60)

        # ---- 安全部分 ----
        if vulnerabilities is not None:
            by_severity: Dict[str, List] = defaultdict(list)
            for v in vulnerabilities:
                sev = v.get("severity", "warning")
                by_severity[sev].append(v)

            sections.append("")
            sections.append(f"[安全扫描] 共发现 {len(vulnerabilities)} 个问题")
            for level in ("critical", "warning", "info"):
                items = by_severity.get(level, [])
                if items:
                    sections.append(f"  {level.upper()}: {len(items)} 个")
                    for item in items:
                        sections.append(
                            f"    - {item['position']} | {item['type']}"
                        )
                        sections.append(
                            f"      代码: {item['code'][:80]}"
                        )
                        sections.append(
                            f"      建议: {item['message']}"
                        )
            if not vulnerabilities:
                sections.append("  未发现安全问题")

        # ---- 质量部分 ----
        if quality_results is not None:
            total_files = len(quality_results)
            total_code_lines = sum(r.get("code_lines", 0) for r in quality_results)
            total_long = sum(len(r.get("long_lines", [])) for r in quality_results)
            total_complex = sum(
                len(r.get("complexity_blocks", [])) for r in quality_results
            )

            sections.append("")
            sections.append(f"[代码质量] 共扫描 {total_files} 个文件, "
                            f"{total_code_lines} 行代码")
            sections.append(f"  超长行(>{self.max_line_length}字符): {total_long} 个 [INFO]")
            sections.append(f"  高复杂度函数(>{self.max_complexity}): {total_complex} 个 [WARNING]")

            for r in quality_results:
                if r.get("long_lines"):
                    for ll in r["long_lines"][:5]:
                        sections.append(
                            f"    - {r['file']}:{ll['line']} "
                            f"(长度{ll['length']})"
                        )
                if r.get("complexity_blocks"):
                    for cb in r["complexity_blocks"][:5]:
                        sections.append(
                            f"    - {r['file']}:{cb['start']} "
                            f"{cb['name']}() 复杂度={cb['complexity']}"
                        )

        # ---- 重复代码部分 ----
        if duplicates is not None:
            sections.append("")
            sections.append(f"[重复代码] 发现 {len(duplicates)} 组疑似重复")
            for d in duplicates[:10]:
                locs = ", ".join(
                    f"{o['file']}:{o['line']}" for o in d["occurrences"][:4]
                )
                sections.append(f"  [INFO] 出现{d['count']}次: {locs}")

        sections.append("")
        sections.append("=" * 60)
        return "\n".join(sections)


# =========================================================================
# CLI 入口
# =========================================================================
def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="代码安全扫描器 + 质量分析器")
    parser.add_argument(
        "path", nargs="?", default=".",
        help="要扫描的目录或文件路径",
    )
    parser.add_argument(
        "--whitelist-dir", action="append", default=[],
        help="排除的目录(可多次指定)",
    )
    parser.add_argument(
        "--whitelist-file", action="append", default=[],
        help="排除的文件(可多次指定)",
    )
    parser.add_argument(
        "--security-only", action="store_true",
        help="仅执行安全扫描",
    )
    parser.add_argument(
        "--quality-only", action="store_true",
        help="仅执行质量分析",
    )
    args = parser.parse_args()

    scanner = CodeScanner(
        whitelist_dirs=args.whitelist_dir,
        whitelist_files=args.whitelist_file,
    )

    target = args.path
    vulnerabilities = None
    quality_results = None
    duplicates = None

    if not args.quality_only:
        print("正在进行安全扫描...")
        if os.path.isfile(target):
            vulnerabilities = scanner.scan_file(target)
        else:
            vulnerabilities = scanner.scan_directory(target)

    if not args.security_only:
        print("正在进行代码质量分析...")
        if os.path.isfile(target):
            quality_results = [scanner.analyze_file(target)]
        else:
            quality_results = scanner.analyze_directory(target)
        duplicates = scanner.detect_duplicates(quality_results)

    report = scanner.generate_report(
        vulnerabilities=vulnerabilities,
        quality_results=quality_results,
        duplicates=duplicates,
    )
    print(report)


if __name__ == "__main__":
    main()
