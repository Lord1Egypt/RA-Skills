"""项目深度分析 → 结构化教程"""

import base64
from github import Github

from src.config import GitHubConfig
from src.storage.models import Project, AnalysisResult
from src.utils.llm_client import LLMClient


ANALYSIS_SYSTEM = """你是一位技术博主，擅长把复杂的开源项目用简单易懂的方式讲清楚。
你的目标受众是有一定编程基础但不一定了解 AI Agent 的开发者。"""

ANALYSIS_PROMPT = """请分析以下 GitHub 开源项目，生成一篇结构化的教程文章。

## 项目信息
- 名称: {name}
- 仓库: {repo_url}
- 描述: {description}
- 语言: {language}
- Stars: {stars}
- Topics: {topics}

## README 内容
{readme_content}

## 项目文件结构
{file_tree}

## 关键代码文件内容
{key_files_content}

---

请按以下模板生成教程（Markdown 格式）：

# {name}：一句话说清楚

## 这个项目解决了什么问题？
（大白话，≤3句，要让非技术人也能听懂）

## 它是怎么做的？
（架构/流程，极简版。如果适合，用 Mermaid 画一个简单流程图）

## 5分钟跑起来
（精确到每步命令，包括环境准备、安装、配置、运行）

```bash
# 每一步都要可直接复制执行
```

## 最有意思的点
（1-2个技术亮点，用类比解释。比如"就像给 AI 装了一个工具箱"）

## 踩坑提醒
（常见问题和解决方案，至少列 2-3 个）

## 相关资源
（官方文档、相关论文、类似项目等）
"""


class ProjectAnalyzer:
    """项目深度分析器"""

    def __init__(self, github_config: GitHubConfig, llm: LLMClient):
        self.github = Github(github_config.token) if github_config.token else Github()
        self.llm = llm

    def analyze(self, project: Project) -> AnalysisResult:
        """对项目进行深度分析，生成结构化教程"""
        print(f"📖 正在分析项目: {project.repo_full_name}")

        # 获取详细信息
        readme_content = self._get_full_readme(project.repo_full_name)
        file_tree = self._get_file_tree(project.repo_full_name)
        key_files = self._get_key_files(project.repo_full_name, file_tree)

        # LLM 生成教程
        prompt = ANALYSIS_PROMPT.format(
            name=project.name,
            repo_url=project.repo_url,
            description=project.description,
            language=project.language,
            stars=project.stars,
            topics=", ".join(project.topics),
            readme_content=readme_content[:5000],
            file_tree=file_tree,
            key_files_content=key_files[:8000],
        )

        full_markdown = self.llm.chat(prompt, system=ANALYSIS_SYSTEM, max_tokens=4096)

        return AnalysisResult(
            project=project,
            full_markdown=full_markdown,
        )

    def _get_full_readme(self, repo_full_name: str) -> str:
        """获取完整 README"""
        try:
            repo = self.github.get_repo(repo_full_name)
            readme = repo.get_readme()
            return base64.b64decode(readme.content).decode("utf-8", errors="replace")
        except Exception as e:
            print(f"  ⚠ 获取 README 失败: {e}")
            return ""

    def _get_file_tree(self, repo_full_name: str, max_depth: int = 3) -> str:
        """获取项目文件树（前 N 层）"""
        try:
            repo = self.github.get_repo(repo_full_name)
            contents = repo.get_contents("")
            lines = []
            self._walk_tree(contents, repo, lines, depth=0, max_depth=max_depth)
            return "\n".join(lines[:100])  # 限制行数
        except Exception as e:
            print(f"  ⚠ 获取文件树失败: {e}")
            return ""

    def _walk_tree(self, contents, repo, lines, depth, max_depth):
        """递归遍历文件树"""
        if depth >= max_depth:
            return
        indent = "  " * depth
        for item in contents:
            if item.name.startswith("."):
                continue
            if item.type == "dir":
                lines.append(f"{indent}📁 {item.name}/")
                try:
                    sub_contents = repo.get_contents(item.path)
                    self._walk_tree(sub_contents, repo, lines, depth + 1, max_depth)
                except Exception:
                    pass
            else:
                lines.append(f"{indent}📄 {item.name}")

    def _get_key_files(self, repo_full_name: str, file_tree: str) -> str:
        """识别并获取关键代码文件内容"""
        # 优先级：入口文件 > 主模块 > 配置文件
        key_patterns = [
            "main.py", "app.py", "cli.py", "run.py", "__main__.py",
            "index.ts", "index.js", "main.ts", "main.go", "main.rs",
            "setup.py", "pyproject.toml", "Cargo.toml",
        ]
        repo = self.github.get_repo(repo_full_name)
        result_parts = []
        files_read = 0

        try:
            contents = repo.get_contents("")
            all_files = self._collect_files(contents, repo, max_files=50)

            for filepath in all_files:
                filename = filepath.split("/")[-1]
                if filename in key_patterns or files_read < 3:
                    try:
                        file_content = repo.get_contents(filepath)
                        if file_content.size and file_content.size < 10000:
                            decoded = base64.b64decode(file_content.content).decode(
                                "utf-8", errors="replace"
                            )
                            result_parts.append(f"\n### {filepath}\n```\n{decoded[:3000]}\n```")
                            files_read += 1
                            if files_read >= 5:
                                break
                    except Exception:
                        continue
        except Exception as e:
            print(f"  ⚠ 获取关键文件失败: {e}")

        return "\n".join(result_parts)

    def _collect_files(self, contents, repo, max_files: int = 50) -> list[str]:
        """收集文件路径列表"""
        files = []
        for item in contents:
            if item.name.startswith("."):
                continue
            if item.type == "file":
                files.append(item.path)
            elif item.type == "dir" and len(files) < max_files:
                try:
                    sub = repo.get_contents(item.path)
                    for sub_item in sub:
                        if sub_item.type == "file":
                            files.append(sub_item.path)
                except Exception:
                    pass
            if len(files) >= max_files:
                break
        return files
