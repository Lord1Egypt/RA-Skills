#!/usr/bin/env python3
"""
Code Simplifier - Core Implementation

This script provides the core functionality for the code-simplifier skill.
It analyzes and simplifies code using AST-based transformations.
"""

# 标准库
import ast
import json
import re
import sys
from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple


class ComplexityLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


@dataclass
class CodeMetrics:
    """Metrics for code complexity analysis."""

    cyclomatic_complexity: int
    nesting_depth: int
    line_count: int
    function_count: int
    average_function_length: float
    comment_density: float
    duplication_score: float


@dataclass
class RefactoringSuggestion:
    """Suggestion for code refactoring."""

    pattern_name: str
    description: str
    location: Tuple[int, int]  # (start_line, end_line)
    complexity_reduction: int
    risk_level: str
    example_before: str
    example_after: str


class MetricsVisitor(ast.NodeVisitor):
    """
    统一的AST访问者，一次性计算所有代码指标。

    该访问者合并了原本6个独立的访问者类：
    - ComplexityVisitor (圈复杂度)
    - NestingVisitor (嵌套深度)
    - FunctionCounter (函数计数)
    - 以及其他指标计算

    性能优势：只需遍历AST一次，而非多次。
    """

    def __init__(self):
        # 圈复杂度指标
        self.complexity = 1

        # 嵌套深度指标
        self.max_depth = 0
        self.current_depth = 0

        # 函数计数指标
        self.function_count = 0

    def _enter_scope(self):
        """进入作用域时增加深度并更新最大深度。"""
        self.current_depth += 1
        self.max_depth = max(self.max_depth, self.current_depth)

    def _exit_scope(self):
        """退出作用域时减少深度。"""
        self.current_depth -= 1

    def visit_FunctionDef(self, node):
        """访问函数定义节点。"""
        # 计数函数
        self.function_count += 1
        # 增加圈复杂度（每个函数都是一个决策点）
        self.complexity += 1
        # 进入函数作用域
        self._enter_scope()
        self.generic_visit(node)
        self._exit_scope()

    def visit_AsyncFunctionDef(self, node):
        """访问异步函数定义节点。"""
        self.function_count += 1
        self.complexity += 1
        self._enter_scope()
        self.generic_visit(node)
        self._exit_scope()

    def visit_ClassDef(self, node):
        """访问类定义节点。"""
        self._enter_scope()
        self.generic_visit(node)
        self._exit_scope()

    def visit_If(self, node):
        """访问if语句节点，增加圈复杂度。"""
        self.complexity += 1
        self._enter_scope()
        self.generic_visit(node)
        self._exit_scope()

    def visit_For(self, node):
        """访问for循环节点，增加圈复杂度。"""
        self.complexity += 1
        self._enter_scope()
        self.generic_visit(node)
        self._exit_scope()

    def visit_While(self, node):
        """访问while循环节点，增加圈复杂度。"""
        self.complexity += 1
        self._enter_scope()
        self.generic_visit(node)
        self._exit_scope()

    def visit_Try(self, node):
        """访问try语句节点。"""
        self._enter_scope()
        # 每个except处理器都增加复杂度
        for handler in node.handlers:
            self.complexity += 1
        self.generic_visit(node)
        self._exit_scope()

    def visit_ExceptHandler(self, node):
        """访问异常处理器节点（已在visit_Try中处理）。"""
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        """访问布尔操作节点，每个and/or增加复杂度。"""
        # and/or操作符数量 = 操作数个数 - 1
        self.complexity += len(node.values) - 1
        self.generic_visit(node)


class CodeSimplifier:
    """Main class for code simplification."""

    def __init__(self, language: str = "python"):
        self.language = language
        self.metrics = None
        self.suggestions = []

    def analyze(self, code: str) -> CodeMetrics:
        """Analyze code complexity and return metrics."""
        if self.language == "python":
            return self._analyze_python(code)
        else:
            raise ValueError(f"Unsupported language: {self.language}")

    def _analyze_python(self, code: str) -> CodeMetrics:
        """Analyze Python code complexity."""
        try:
            tree = ast.parse(code)
            total_lines = code.count("\n") + 1

            # 使用统一访问者一次性计算所有指标
            visitor = MetricsVisitor()
            visitor.visit(tree)

            # 计算基于文本的指标
            comment_density = self._calculate_comment_density(code)
            duplication = self._calculate_duplication_score(code)
            avg_func_length = (
                total_lines / visitor.function_count
                if visitor.function_count > 0
                else 0.0
            )

            self.metrics = CodeMetrics(
                cyclomatic_complexity=visitor.complexity,
                nesting_depth=visitor.max_depth,
                line_count=total_lines,
                function_count=visitor.function_count,
                average_function_length=avg_func_length,
                comment_density=comment_density,
                duplication_score=duplication,
            )

            return self.metrics

        except SyntaxError as e:
            raise ValueError(f"Syntax error in code: {e}")

    def _calculate_comment_density(self, code: str) -> float:
        """Calculate comment density as percentage of commented lines."""
        lines = code.split("\n")
        total_lines = len(lines)
        comment_lines = 0

        in_multiline_comment = False

        for line in lines:
            stripped = line.strip()

            # Check for multiline comments
            if '"""' in line or "'''" in line:
                in_multiline_comment = not in_multiline_comment
                comment_lines += 1
            elif in_multiline_comment:
                comment_lines += 1
            elif stripped.startswith("#"):
                comment_lines += 1

        return (comment_lines / total_lines * 100) if total_lines > 0 else 0.0

    def _calculate_duplication_score(self, code: str) -> float:
        """Calculate code duplication score (simplified)."""
        lines = code.split("\n")
        unique_lines = set()

        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                unique_lines.add(stripped)

        total_lines = len(
            [l for l in lines if l.strip() and not l.strip().startswith("#")]
        )

        if total_lines == 0:
            return 0.0

        duplication = 1.0 - (len(unique_lines) / total_lines)
        return max(0.0, min(1.0, duplication)) * 100

    def generate_suggestions(self, code: str) -> List[RefactoringSuggestion]:
        """Generate refactoring suggestions based on code analysis."""
        self.suggestions = []

        if self.language == "python":
            self._generate_python_suggestions(code)

        return self.suggestions

    def _generate_python_suggestions(self, code: str):
        """Generate refactoring suggestions for Python code."""
        lines = code.split("\n")

        # Check for deeply nested code
        self._check_nested_conditions(code, lines)

        # Check for long functions
        self._check_long_functions(code, lines)

        # Check for duplicate code
        self._check_duplicate_code(code, lines)

        # Check for complex boolean expressions
        self._check_complex_booleans(code, lines)

        # Check for missing type hints
        self._check_type_hints(code, lines)

    def _check_nested_conditions(self, code: str, lines: List[str]):
        """Check for deeply nested conditional statements."""
        pattern = r"if .*:\s*\n(\s+)if .*:\s*\n(\s+)if .*:"
        matches = list(re.finditer(pattern, code, re.MULTILINE))

        for match in matches:
            start_line = code[: match.start()].count("\n")
            end_line = code[: match.end()].count("\n")

            # Extract the nested code block
            nested_code = "\n".join(lines[start_line : min(end_line + 5, len(lines))])

            suggestion = RefactoringSuggestion(
                pattern_name="Deeply Nested Conditions",
                description="Multiple nested if statements reduce readability",
                location=(start_line + 1, end_line + 1),
                complexity_reduction=3,
                risk_level="low",
                example_before=(nested_code[:200] + "..." if len(nested_code) > 200 else nested_code),
                example_after="""# Consider using early returns or extracting nested logic
if not condition1:
    return None
if not condition2:
    return None
if not condition3:
    return None
# Process success case""",
            )
            self.suggestions.append(suggestion)

    def _check_long_functions(self, code: str, lines: List[str]):
        """Check for functions that are too long."""
        # Simple check: functions with more than 30 lines
        in_function = False
        function_start = 0
        function_lines = []

        for i, line in enumerate(lines):
            stripped = line.strip()

            if stripped.startswith("def ") or stripped.startswith("async def "):
                if in_function and len(function_lines) > 30:
                    # Found a long function
                    suggestion = RefactoringSuggestion(
                        pattern_name="Long Function",
                        description=f"Function with {len(function_lines)} lines exceeds recommended limit",
                        location=(function_start + 1, i),
                        complexity_reduction=2,
                        risk_level="medium",
                        example_before="\n".join(function_lines[:10]) + "\n...",
                        example_after="""# Consider extracting parts into helper functions
def long_function():
    result1 = _helper1()
    result2 = _helper2()
    return _combine_results(result1, result2)

def _helper1():
    # Extracted logic 1
    pass

def _helper2():
    # Extracted logic 2
    pass""",
                    )
                    self.suggestions.append(suggestion)

                in_function = True
                function_start = i
                function_lines = []
            elif in_function:
                if stripped and not stripped.startswith("#"):
                    function_lines.append(line)
                # Check for function end (simplified)
                if (
                    stripped
                    and len(stripped) > 0
                    and stripped[0] not in " \t#"
                    and i > function_start
                ):
                    if not (
                        stripped.startswith("def ") or stripped.startswith("class ")
                    ):
                        # Still in function
                        pass
                    else:
                        # New function/class starts
                        in_function = False

    def _check_duplicate_code(self, code: str, lines: List[str]):
        """Check for duplicate code patterns."""
        # Simple duplicate detection: repeated blocks of 3+ identical lines
        line_hashes = [hash(line.strip()) for line in lines if line.strip()]

        for i in range(len(line_hashes) - 2):
            for j in range(i + 1, min(i + 10, len(line_hashes) - 2)):
                if (
                    line_hashes[i] == line_hashes[j]
                    and line_hashes[i + 1] == line_hashes[j + 1]
                    and line_hashes[i + 2] == line_hashes[j + 2]
                ):
                    suggestion = RefactoringSuggestion(
                        pattern_name="Duplicate Code",
                        description="Similar code blocks found in multiple places",
                        location=(i + 1, i + 3),
                        complexity_reduction=1,
                        risk_level="low",
                        example_before="\n".join(lines[i : i + 3]),
                        example_after="""# Extract duplicate code into a reusable function
def process_item(item):
    # Common processing logic
    return processed_item

# Use the function in multiple places
result1 = process_item(item1)
result2 = process_item(item2)""",
                    )
                    self.suggestions.append(suggestion)
                    break

    def _check_complex_booleans(self, code: str, lines: List[str]):
        """Check for complex boolean expressions."""
        pattern = r"if .* and .* and .*:|if .* or .* or .*:"
        matches = list(re.finditer(pattern, code, re.MULTILINE))

        for match in matches:
            start_line = code[: match.start()].count("\n")

            suggestion = RefactoringSuggestion(
                pattern_name="Complex Boolean Expression",
                description="Boolean expression with multiple conditions reduces readability",
                location=(start_line + 1, start_line + 1),
                complexity_reduction=1,
                risk_level="low",
                example_before=match.group(0),
                example_after="""# Extract complex condition into a descriptive variable or function
is_valid = (condition1 and condition2 and condition3)
if is_valid:
    # Process valid case

# Or extract to a function
def should_process(item):
    return (item.condition1 and
            item.condition2 and
            item.condition3)""",
            )
            self.suggestions.append(suggestion)

    def _check_type_hints(self, code: str, lines: List[str]):
        """Check for missing type hints in function definitions."""
        pattern = r"def (\w+)\(([^)]*)\):"
        matches = list(re.finditer(pattern, code, re.MULTILINE))

        for match in matches:
            func_name = match.group(1)
            params = match.group(2)

            # Check if type hints are present
            if ":" not in params and "->" not in code[match.end() : match.end() + 50]:
                start_line = code[: match.start()].count("\n")

                suggestion = RefactoringSuggestion(
                    pattern_name="Missing Type Hints",
                    description=f"Function '{func_name}' is missing type annotations",
                    location=(start_line + 1, start_line + 1),
                    complexity_reduction=0,  # Doesn't reduce complexity but improves maintainability
                    risk_level="low",
                    example_before=match.group(0),
                    example_after=f"""def {func_name}(param1: str, param2: int) -> bool:
    # Function with type hints
    return True""",
                )
                self.suggestions.append(suggestion)

    def simplify(self, code: str, apply_changes: bool = False) -> str:
        """Simplify code based on analysis and suggestions."""
        if self.metrics is None:
            self.analyze(code)

        if not self.suggestions:
            self.generate_suggestions(code)

        if not apply_changes:
            return code

        # Apply simplifications (simplified implementation)
        simplified = code

        # Apply early return pattern for nested conditions
        simplified = self._apply_early_return_pattern(simplified)

        # Extract duplicate code patterns
        simplified = self._extract_duplicate_functions(simplified)

        # Simplify boolean expressions
        simplified = self._simplify_boolean_expressions(simplified)

        return simplified

    def _apply_early_return_pattern(self, code: str) -> str:
        """Apply early return pattern to nested conditions."""
        lines = code.split("\n")
        result = []
        i = 0

        while i < len(lines):
            line = lines[i]

            # Simple pattern matching for nested ifs
            if (
                line.strip().startswith("if ")
                and i + 1 < len(lines)
                and lines[i + 1].strip().startswith("if ")
            ):
                # Check for nested pattern
                indent1 = len(line) - len(line.lstrip())
                indent2 = len(lines[i + 1]) - len(lines[i + 1].lstrip())

                if indent2 > indent1:
                    # Found nested if, apply early return
                    condition = line.strip()[3:-1]  # Remove 'if ' and ':'
                    result.append(line)
                    result.append(
                        f"{' ' * (indent1 + 4)}return None  # Early return for failed condition"
                    )

                    # Skip the nested if for now (simplified)
                    i += 2
                    continue

            result.append(line)
            i += 1

        return "\n".join(result)

    def _extract_duplicate_functions(self, code: str) -> str:
        """Extract duplicate code into functions (simplified)."""
        # This is a simplified implementation
        # In a real implementation, this would use AST analysis
        return code

    def _simplify_boolean_expressions(self, code: str) -> str:
        """Simplify complex boolean expressions."""
        # Simple pattern: if a and b and c:
        pattern = r"(if\s+)(\w+)\s+and\s+(\w+)\s+and\s+(\w+)(\s*:)"

        def replace_match(match):
            prefix = match.group(1)
            vars = [match.group(2), match.group(3), match.group(4)]
            suffix = match.group(5)

            # Create a descriptive variable name
            var_name = "_".join(vars) + "_valid"
            return f"{prefix}{var_name}{suffix}\n    {var_name} = {' and '.join(vars)}"

        return re.sub(pattern, replace_match, code, flags=re.MULTILINE)


def main():
    """Command-line interface for code simplifier."""
    import argparse

    parser = argparse.ArgumentParser(description="Code Simplifier Tool")
    parser.add_argument("file", help="File to analyze/simplify")
    parser.add_argument(
        "--analyze", action="store_true", help="Analyze code complexity"
    )
    parser.add_argument(
        "--suggest", action="store_true", help="Generate refactoring suggestions"
    )
    parser.add_argument("--simplify", action="store_true", help="Simplify the code")
    parser.add_argument("--output", help="Output file for simplified code")
    parser.add_argument(
        "--format", choices=["text", "json"], default="text", help="Output format"
    )

    args = parser.parse_args()

    try:
        with open(args.file, "r", encoding="utf-8") as f:
            code = f.read()

        simplifier = CodeSimplifier(language="python")

        if args.analyze:
            metrics = simplifier.analyze(code)

            if args.format == "json":
                print(
                    json.dumps(
                        {
                            "cyclomatic_complexity": metrics.cyclomatic_complexity,
                            "nesting_depth": metrics.nesting_depth,
                            "line_count": metrics.line_count,
                            "function_count": metrics.function_count,
                            "average_function_length": metrics.average_function_length,
                            "comment_density": metrics.comment_density,
                            "duplication_score": metrics.duplication_score,
                        },
                        indent=2,
                    )
                )
            else:
                print("Code Complexity Analysis:")
                print(f"  Cyclomatic Complexity: {metrics.cyclomatic_complexity}")
                print(f"  Maximum Nesting Depth: {metrics.nesting_depth}")
                print(f"  Line Count: {metrics.line_count}")
                print(f"  Function Count: {metrics.function_count}")
                print(
                    f"  Average Function Length: {metrics.average_function_length:.1f} lines"
                )
                print(f"  Comment Density: {metrics.comment_density:.1f}%")
                print(f"  Duplication Score: {metrics.duplication_score:.1f}%")

        if args.suggest:
            suggestions = simplifier.generate_suggestions(code)

            if args.format == "json":
                print(
                    json.dumps(
                        [
                            {
                                "pattern_name": s.pattern_name,
                                "description": s.description,
                                "location": s.location,
                                "complexity_reduction": s.complexity_reduction,
                                "risk_level": s.risk_level,
                            }
                            for s in suggestions
                        ],
                        indent=2,
                    )
                )
            else:
                print(f"\nRefactoring Suggestions ({len(suggestions)} found):")
                for i, suggestion in enumerate(suggestions, 1):
                    print(f"\n{i}. {suggestion.pattern_name}")
                    print(f"   Description: {suggestion.description}")
                    print(
                        f"   Location: Lines {suggestion.location[0]}-{suggestion.location[1]}"
                    )
                    print(
                        f"   Complexity Reduction: {suggestion.complexity_reduction} points"
                    )
                    print(f"   Risk Level: {suggestion.risk_level}")

        if args.simplify:
            simplified = simplifier.simplify(code, apply_changes=True)

            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(simplified)
                print(f"Simplified code written to {args.output}")
            else:
                print(simplified)

        if not any([args.analyze, args.suggest, args.simplify]):
            # Default: show analysis
            metrics = simplifier.analyze(code)
            print("Code Complexity Analysis:")
            print(f"  Cyclomatic Complexity: {metrics.cyclomatic_complexity}")
            print(f"  Maximum Nesting Depth: {metrics.nesting_depth}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
