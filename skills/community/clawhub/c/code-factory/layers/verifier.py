"""
Step 4: 自动验证器 —— 含依赖图谱检查、HARD-GATE 验证、pytest 执行。

借鉴 code-review-graph + superpowers 理念。
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class DependencyNode:
    """依赖图谱节点"""
    file: str
    imports: List[str] = field(default_factory=list)
    imported_by: List[str] = field(default_factory=list)


@dataclass
class VerificationResult:
    """验证结果"""
    all_passed: bool = False
    test_passed: bool = False
    dependency_ok: bool = True
    hard_gate_ok: bool = True
    test_output: str = ""
    test_results: Dict = field(default_factory=dict)
    issues: List[str] = field(default_factory=list)
    dependency_graph: List[Dict] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "all_passed": self.all_passed,
            "test_passed": self.test_passed,
            "dependency_ok": self.dependency_ok,
            "hard_gate_ok": self.hard_gate_ok,
            "test_output": self.test_output,
            "test_results": self.test_results,
            "issues": self.issues,
            "dependency_graph": self.dependency_graph,
            "suggestions": self.suggestions,
        }


class Verifier:
    """Step 4 自动验证器"""

    def verify(
        self,
        target_dir: Path,
        assets: List[str],
    ) -> VerificationResult:
        """
        执行完整验证流程：
        1. 依赖图谱分析（循环引用检测）
        2. HARD-GATE 强制门禁验证
        3. pytest 测试执行
        4. 结构化审查报告
        """
        result = VerificationResult()

        # 1. 依赖图谱分析
        dep_result = self._analyze_dependencies(target_dir, assets)
        result.dependency_graph = dep_result["graph"]
        result.dependency_ok = dep_result["no_circular"]
        if not result.dependency_ok:
            result.issues.extend(dep_result["circular_refs"])

        # 2. HARD-GATE 验证
        hg_result = self._verify_hard_gates(target_dir, assets)
        result.hard_gate_ok = hg_result["all_ok"]
        if not result.hard_gate_ok:
            result.issues.extend(hg_result["failures"])

        # 3. 运行测试
        test_result = self._run_tests(target_dir)
        result.test_passed = test_result["passed"]
        result.test_output = test_result.get("output", "")
        result.test_results = test_result
        if not result.test_passed:
            result.issues.append(f"测试失败: {test_result.get('summary', '')}")

        # 4. 生成建议
        result.suggestions = self._generate_suggestions(result)

        result.all_passed = (
            result.dependency_ok and result.hard_gate_ok and result.test_passed
        )
        return result

    def _analyze_dependencies(
        self, target_dir: Path, assets: List[str]
    ) -> Dict:
        """
        分析模块间依赖关系，检测循环引用。
        """
        nodes: Dict[str, DependencyNode] = {}
        python_files = [a for a in assets if a.endswith(".py")]

        stdlib_modules = frozenset({
            "__future__", "abc", "argparse", "asyncio", "base64", "collections",
            "contextlib", "copy", "csv", "ctypes", "dataclasses", "datetime",
            "decimal", "enum", "functools", "hashlib", "http", "importlib",
            "inspect", "io", "itertools", "json", "logging", "math", "multiprocessing",
            "operator", "os", "pathlib", "pickle", "platform", "pprint", "queue",
            "random", "re", "shutil", "signal", "socket", "sqlite3", "statistics",
            "string", "struct", "subprocess", "sys", "tempfile", "textwrap",
            "threading", "time", "traceback", "typing", "unittest", "urllib",
            "uuid", "warnings", "weakref", "xml", "zipfile",
        })

        for pf in python_files:
            file_path = target_dir / pf
            if not file_path.exists():
                continue
            content = file_path.read_text(encoding="utf-8")
            imports = []
            for line in content.split("\n"):
                stripped = line.strip()
                # 匹配 "from X import Y" 格式
                if stripped.startswith("from ") and " import " in stripped:
                    parts = stripped.replace("from ", "").split(" import ")
                    if parts:
                        module = parts[0].strip().split(".")[0]
                        if module not in stdlib_modules and not module.startswith("_"):
                            imports.append(module)
                # 匹配 "import X" 格式
                elif stripped.startswith("import "):
                    module = stripped.replace("import ", "").split(" as ")[0].strip().split(".")[0]
                    if module not in stdlib_modules and not module.startswith("_"):
                        imports.append(module)
            nodes[pf] = DependencyNode(file=pf, imports=imports)

        # 检测循环引用：建立模块名→文件路径的映射
        module_to_file: Dict[str, str] = {}
        for filename in nodes:
            stem = Path(filename).stem
            module_to_file[stem] = filename

        circular_refs = []
        for filename, node in nodes.items():
            for imp in node.imports:
                if imp in module_to_file:
                    other_file = module_to_file[imp]
                    if other_file != filename and filename in nodes[other_file].imports:
                        circular_refs.append(f"循环引用: {filename} ↔ {other_file}")
                    # 也检查反向引用（通过模块名）
                    other_imports = [Path(f).stem for f in nodes[other_file].imports]
                    if Path(filename).stem in other_imports:
                        if f"循环引用: {other_file} ↔ {filename}" not in circular_refs:
                            circular_refs.append(f"循环引用: {filename} ↔ {other_file}")

        return {
            "graph": [
                {"file": n.file, "imports": n.imports}
                for n in nodes.values()
            ],
            "no_circular": len(circular_refs) == 0,
            "circular_refs": circular_refs,
        }

    def _verify_hard_gates(
        self, target_dir: Path, assets: List[str]
    ) -> Dict:
        """
        验证所有 HARD-GATE 标记的关键函数/API。

        凡标记 <!-- HARD-GATE --> 的位置，必须存在对应测试。
        使用正则匹配 import 语句，避免注释/字符串中的误匹配。
        """
        failures = []
        for asset in assets:
            file_path = target_dir / asset
            if not file_path.exists() or not file_path.suffix == ".py":
                continue
            content = file_path.read_text(encoding="utf-8")
            if "<!-- HARD-GATE -->" in content:
                # 检查是否有对应的测试：用正则匹配 import 语句
                module_name = Path(asset).stem
                test_dir = target_dir / "tests"
                has_test = False
                if test_dir.exists():
                    for tf in test_dir.glob("*.py"):
                        tf_content = tf.read_text(encoding="utf-8")
                        # 正则匹配 "from module_name import" 或 "import module_name"
                        if re.search(
                            rf'(?:from\s+{re.escape(module_name)}\s+import|import\s+{re.escape(module_name)})',
                            tf_content
                        ):
                            has_test = True
                            break
                if not has_test:
                    failures.append(f"HARD-GATE 缺少测试: {asset}")

        return {
            "all_ok": len(failures) == 0,
            "failures": failures,
        }

    def _run_tests(self, target_dir: Path) -> Dict:
        """运行 pytest（v3.0：使用独立临时目录隔离环境）"""
        test_dir = target_dir / "tests"
        if not test_dir.exists():
            return {"passed": True, "output": "无测试目录", "summary": "跳过"}

        isolated_cwd = tempfile.mkdtemp(prefix="code_factory_pytest_")

        try:
            env = os.environ.copy()
            existing_path = env.get("PYTHONPATH", "")
            env["PYTHONPATH"] = f"{target_dir}{os.pathsep}{existing_path}" if existing_path else str(target_dir)

            result = subprocess.run(
                [sys.executable, "-m", "pytest", str(test_dir), "-v", "--tb=short"],
                capture_output=True,
                text=True,
                cwd=isolated_cwd,
                timeout=60,
                env=env,
            )
            return {
                "passed": result.returncode == 0,
                "output": result.stdout + result.stderr,
                "returncode": result.returncode,
                "summary": "全部通过" if result.returncode == 0 else f"退出码 {result.returncode}",
            }
        except subprocess.TimeoutExpired:
            return {"passed": False, "output": "测试超时", "summary": "超时"}
        except FileNotFoundError:
            return {"passed": False, "output": "pytest 未安装", "summary": "pytest 未安装"}
        finally:
            shutil.rmtree(isolated_cwd, ignore_errors=True)

    def _generate_suggestions(self, result: VerificationResult) -> List[str]:
        """生成改进建议"""
        suggestions = []
        if not result.dependency_ok:
            suggestions.append("存在循环依赖，建议重构模块拆分")
        if not result.hard_gate_ok:
            suggestions.append("HARD-GATE 标记的函数缺少独立测试")
        if not result.test_passed:
            suggestions.append("测试未通过，检查 src/main.py 实现")
        return suggestions
