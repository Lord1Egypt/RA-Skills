# 详细参考 - explain-code-tool-pro

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (python)

```python
import os
import re
import json
from collections import defaultdict
from datetime import datetime

class ProjectArchitectureAnalyzer:
    """项目架构分析器"""

    def __init__(self, project_root):
        self.root = project_root
        self.modules = {}
        self.dependencies = defaultdict(list)
        self.file_count = 0
        self.total_lines = 0

    def analyze(self):
        """执行完整架构分析"""
        self._scan_project()
        return self._generate_architecture_report()

    def _scan_project(self):
        """扫描项目结构"""
        supported = ('.js', '.ts', '.py', '.java', '.go')

        for root, dirs, files in os.walk(self.root):
            dirs[:] = [d for d in dirs if d not in
                       ('node_modules', '.git', 'dist', 'build', '__pycache__', 'vendor')]

            for file in files:
                if file.endswith(supported):
                    filepath = os.path.join(root, file)
                    rel_path = os.path.relpath(filepath, self.root)
                    module_name = self._get_module_name(rel_path)

                    self._analyze_file(filepath, module_name, rel_path)
                    self.file_count += 1

    def _get_module_name(self, rel_path):
        """获取模块名"""
        parts = rel_path.split(os.sep)
        if len(parts) > 1:
            return parts[0]
        return "root"

    def _analyze_file(self, filepath, module, rel_path):
        """分析单个文件"""
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')
            self.total_lines += len(lines)

            imports = self._extract_imports(content, filepath)
            for imp in imports:
                self.dependencies[module].append(imp)

            functions = self._extract_functions(content, filepath)
            classes = self._extract_classes(content, filepath)

            if module not in self.modules:
                self.modules[module] = {
                    "files": [],
                    "functions": 0,
                    "classes": 0,
                    "lines": 0
                }

            self.modules[module]["files"].append(rel_path)
            self.modules[module]["functions"] += len(functions)
            self.modules[module]["classes"] += len(classes)
            self.modules[module]["lines"] += len(lines)

    def _extract_imports(self, content, filepath):
        """提取导入语句"""
        imports = []
        patterns = [
            r'^import\s+.*\s+from\s+["\']([^"\']+)["\']',      # ES6
            r'^const\s+.*\s*=\s*require\(["\']([^"\']+)["\']\)',  # CommonJS
            r'^from\s+(\S+)\s+import',                           # Python
            r'^import\s+(\S+)',                                  # Python
        ]

        for line in content.split('\n'):
            for pattern in patterns:
                match = re.search(pattern, line.strip())
                if match:
                    imports.append(match.group(1))
        return imports

    def _extract_functions(self, content, filepath):
        """提取函数定义"""
        patterns = [
            r'(?:export\s+)?function\s+(\w+)',           # JS/TS
            r'(?:export\s+)?const\s+(\w+)\s*=\s*(?:async\s+)?\(',  # JS/TS arrow
            r'def\s+(\w+)',                               # Python
        ]
        functions = []
        for pattern in patterns:
            functions.extend(re.findall(pattern, content))
        return functions

    def _extract_classes(self, content, filepath):
        """提取类定义"""
        patterns = [
            r'class\s+(\w+)',           # JS/TS/Python
            r'interface\s+(\w+)',       # TS
        ]
        classes = []
        for pattern in patterns:
            classes.extend(re.findall(pattern, content))
        return classes

    def _generate_architecture_report(self):
        """生成架构报告"""
        return {
            "analysis_time": datetime.now().isoformat(),
            "project": self.root,
            "summary": {
                "total_files": self.file_count,
                "total_lines": self.total_lines,
                "total_modules": len(self.modules),
                "total_functions": sum(m["functions"] for m in self.modules.values()),
                "total_classes": sum(m["classes"] for m in self.modules.values()),
            },
            "modules": self.modules,
            "dependencies": dict(self.dependencies),
            "mermaid_diagram": self._generate_mermaid()
        }

    def _generate_mermaid(self):
        """生成Mermaid依赖图"""
        lines = ["graph TD"]
        for module in self.modules:
            deps = self.dependencies.get(module, [])
            for dep in deps:
                dep_short = dep.split('/')[-1].split('.')[0]
                if dep_short in self.modules or dep_short != module:
                    lines.append(f"    {module} --> {dep_short}")
        return '\n'.join(lines)

analyzer = ProjectArchitectureAnalyzer("./src")
report = analyzer.analyze()
print(json.dumps(report, indent=2, ensure_ascii=False))
```

## 代码示例 (python)

```python
class CodeDocGenerator:
    """批量代码文档生成器"""

    def __init__(self, project_root, output_dir="./docs"):
        self.root = project_root
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_all(self):
        """生成所有文档"""
        self._generate_api_docs()
        self._generate_module_docs()
        self._generate_architecture_doc()
        self._generate_index()

    def _generate_api_docs(self):
        """生成API文档"""
        api_doc = {
            "title": "API 文档",
            "generated_at": datetime.now().isoformat(),
            "endpoints": []
        }

        for root, _, files in os.walk(self.root):
            for file in files:
                if file.endswith(('.js', '.ts', '.py')):
                    filepath = os.path.join(root, file)
                    endpoints = self._extract_api_endpoints(filepath)
                    api_doc["endpoints"].extend(endpoints)

        api_path = os.path.join(self.output_dir, "api.md")
        with open(api_path, 'w', encoding='utf-8') as f:
            f.write(self._format_api_doc(api_doc))

    def _extract_api_endpoints(self, filepath):
        """提取API端点"""
        endpoints = []
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

            patterns = [
                (r'@(Get|Post|Put|Delete|Patch)\(["\']([^"\']+)["\']\)', 'decorator'),
                (r'app\.(get|post|put|delete|patch)\(["\']([^"\']+)["\']', 'express'),
                (r'@(app\.)?route\(["\']([^"\']+)["\'].*methods=["\'](\w+)["\']\)', 'flask'),
            ]

            for pattern, source in patterns:
                for match in re.finditer(pattern, content):
                    method = match.group(1).upper() if source == 'decorator' else \
                             match.group(1).upper() if source == 'express' else \
                             match.group(3).upper()
                    path = match.group(2)
                    endpoints.append({
                        "method": method,
                        "path": path,
                        "file": filepath,
                        "source": source
                    })

        return endpoints

    def _format_api_doc(self, doc):
        """格式化API文档"""
        lines = [
            f"# {doc['title']}",
            f"\n> 生成时间: {doc['generated_at']}",
            f"\n## 端点列表\n"
        ]

        for ep in doc["endpoints"]:
            lines.append(f"### {ep['method']} {ep['path']}")
            lines.append(f"- 文件: `{ep['file']}`")
            lines.append(f"- 来源: {ep['source']}\n")

        return '\n'.join(lines)

    def _generate_module_docs(self):
        """生成模块文档"""
        for root, dirs, files in os.walk(self.root):
            dirs[:] = [d for d in dirs if d[0] != '.' and d not in
                       ('node_modules', '__pycache__')]

            for file in files:
                if file.endswith(('.js', '.ts', '.py')):
                    filepath = os.path.join(root, file)
                    doc = self._generate_file_doc(filepath)
                    if doc:
                        rel_path = os.path.relpath(filepath, self.root)
                        doc_path = os.path.join(
                            self.output_dir,
                            rel_path.replace(os.sep, '_') + '.md'
                        )
                        with open(doc_path, 'w', encoding='utf-8') as f:
                            f.write(doc)

    def _generate_file_doc(self, filepath):
        """为单个文件生成文档"""
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        functions = re.findall(
            r'(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*\(([^)]*)\)',
            content
        )
        classes = re.findall(r'class\s+(\w+)', content)

        if not functions and not classes:
            return None

        lines = [
            f"# {os.path.basename(filepath)}",
            f"\n> 文件路径: `{filepath}`",
            f"> 生成时间: {datetime.now().isoformat()}\n"
        ]

        if functions:
            lines.append("## 函数\n")
            for name, params in functions:
                lines.append(f"### `{name}({params})`")
                lines.append(f"\n参数: `{params or '无'}`\n")

        if classes:
            lines.append("\n## 类\n")
            for cls in classes:
                lines.append(f"### `{cls}`\n")
        return '\n'.join(lines)
```

## 代码示例 (python)

```python
class CodeComplexityAnalyzer:
    """代码复杂度分析器"""

    def __init__(self, project_root):
        self.root = project_root
        self.results = []

    def analyze(self):
        """分析代码复杂度"""
        for root, _, files in os.walk(self.root):
            for file in files:
                if file.endswith(('.js', '.ts', '.py')):
                    filepath = os.path.join(root, file)
                    self._analyze_file(filepath)
        return sorted(self.results, key=lambda x: x['complexity'], reverse=True)

    def _analyze_file(self, filepath):
        """分析单个文件复杂度"""
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        complexity = 0
        complexity += len(re.findall(r'\bif\b', content))
        complexity += len(re.findall(r'\belse\b', content))
        complexity += len(re.findall(r'\bfor\b', content))
        complexity += len(re.findall(r'\bwhile\b', content))
        complexity += len(re.findall(r'\bcase\b', content))
        complexity += len(re.findall(r'\bcatch\b', content))
        complexity += len(re.findall(r'&&\|\|\?', content))

        lines = content.split('\n')

        self.results.append({
            'file': filepath,
            'lines': len(lines),
            'complexity': complexity,
            'rating': self._rate_complexity(complexity),
            'suggestion': self._suggest(complexity)
        })

    def _rate_complexity(self, score):
        """评级"""
        if score < 5: return "低"
        elif score < 10: return "中"
        elif score < 20: return "高"
        else: return "极高"

    def _suggest(self, score):
        """建议"""
        if score < 5: return "复杂度良好,保持现状"
        elif score < 10: return "建议关注复杂函数"
        elif score < 20: return "建议重构降低复杂度"
        else: return "强烈建议重构,复杂度过高"
```

## 代码示例 (python)

```python
class LegacySystemAnalyzer:
    """遗留系统逆向分析器"""

    def __init__(self, project_root):
        self.root = project_root
        self.architecture = ProjectArchitectureAnalyzer(project_root)
        self.complexity = CodeComplexityAnalyzer(project_root)
        self.docs = CodeDocGenerator(project_root)

    def full_analysis(self):
        """完整逆向分析"""
        print("=== 遗留系统逆向分析 ===")

        print("1. 架构分析...")
        arch_report = self.architecture.analyze()

        print("2. 复杂度分析...")
        complexity_report = self.complexity.analyze()

        print("3. 文档生成...")
        self.docs.generate_all()

        print("4. 生成综合报告...")
        report = {
            "analysis_time": datetime.now().isoformat(),
            "project": self.root,
            "architecture": arch_report,
            "complexity": {
                "total_files": len(complexity_report),
                "high_complexity_files": [
                    r for r in complexity_report if r["rating"] in ["高", "极高"]
                ],
                "average_complexity": sum(r["complexity"] for r in complexity_report) / len(complexity_report)
            },
            "recommendations": self._generate_recommendations(arch_report, complexity_report)
        }
        return report

    def _generate_recommendations(self, arch, complexity):
        """生成改进建议"""
        recs = []
        high_complex = [r for r in complexity if r["rating"] == "极高"]
        if high_complex:
            recs.append(f"发现{len(high_complex)}个极高复杂度文件,建议优先重构")

        if arch["summary"]["total_files"] > 100:
            recs.append("项目文件较多,建议按模块拆分文档")

        return recs
```

