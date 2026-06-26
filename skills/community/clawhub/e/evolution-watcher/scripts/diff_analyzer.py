#!/usr/bin/env python3
"""
代码变更集（Diff）分析器 - 阶段1增强

功能：
1. 从 GitHub API 获取两个版本之间的代码差异
2. 从本地 Git 仓库获取 diff（若插件已克隆）
3. 解析 diff，提取关键变更：新增文件、删除文件、修改行数、API 变更等
4. 为影响评估提供结构化数据
"""

import os
import sys
import re
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class DiffAnalyzer:
    """代码变更集分析器"""
    
    def __init__(self, github_token: Optional[str] = None):
        """初始化分析器
        
        Args:
            github_token: GitHub API 令牌（可选）
        """
        self.github_token = github_token
        self.temp_dir = Path("/tmp/evolution_watcher_diff")
        self.temp_dir.mkdir(exist_ok=True)
    
    def get_github_repo_url(self, plugin_name: str) -> Optional[str]:
        """根据插件名推测 GitHub 仓库 URL
        
        策略：
        1. 检查插件目录中的 .git/config
        2. 查询 ClawHub 元数据（若存在）
        3. 基于常见命名模式猜测
        """
        # 尝试从插件目录获取
        plugin_path = Path(f"/root/.openclaw/workspace/skills/{plugin_name}")
        git_config = plugin_path / ".git" / "config"
        
        if git_config.exists():
            try:
                with open(git_config, 'r') as f:
                    content = f.read()
                # 提取 url
                for line in content.split('\n'):
                    if "url = " in line:
                        url = line.split("url = ")[1].strip()
                        if "github.com" in url:
                            return url
            except Exception:
                pass
        
        # 基于常见模式猜测
        # 假设插件名对应 clawhub.com 上的仓库
        # 格式通常为：clawhub.com/openclaw/<plugin-name>
        return f"https://github.com/openclaw/{plugin_name}.git"
    
    def clone_repo_if_needed(self, repo_url: str, version: str) -> Optional[Path]:
        """克隆仓库到临时目录（如果需要）"""
        # 使用插件名作为目录名
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        repo_dir = self.temp_dir / repo_name
        
        if repo_dir.exists():
            # 已有克隆，拉取最新
            try:
                subprocess.run(
                    ["git", "-C", str(repo_dir), "fetch", "origin"],
                    check=True,
                    capture_output=True
                )
            except subprocess.CalledProcessError as e:
                logger.warning(f"无法拉取仓库 {repo_url}: {e}")
        else:
            # 克隆仓库
            try:
                subprocess.run(
                    ["git", "clone", "--depth", "1", repo_url, str(repo_dir)],
                    check=True,
                    capture_output=True
                )
            except subprocess.CalledProcessError as e:
                logger.error(f"无法克隆仓库 {repo_url}: {e}")
                return None
        
        # 检出特定版本
        try:
            subprocess.run(
                ["git", "-C", str(repo_dir), "checkout", f"tags/v{version}", "-b", f"analysis_v{version}"],
                check=False,
                capture_output=True
            )
        except Exception:
            # 尝试直接 checkout
            try:
                subprocess.run(
                    ["git", "-C", str(repo_dir), "checkout", version],
                    check=False,
                    capture_output=True
                )
            except Exception:
                logger.warning(f"无法检出版本 {version}，使用默认分支")
        
        return repo_dir
    
    def get_git_diff(self, repo_dir: Path, old_version: str, new_version: str) -> Optional[str]:
        """获取两个版本之间的 Git diff"""
        try:
            # 确保我们有这两个版本
            subprocess.run(
                ["git", "-C", str(repo_dir), "fetch", "--tags"],
                check=False,
                capture_output=True
            )
            
            # 获取 diff
            result = subprocess.run(
                ["git", "-C", str(repo_dir), "diff", f"v{old_version}..v{new_version}", "--stat"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout
            
            # 尝试不带 v 前缀
            result = subprocess.run(
                ["git", "-C", str(repo_dir), "diff", f"{old_version}..{new_version}", "--stat"],
                capture_output=True,
                text=True
            )
            
            return result.stdout if result.returncode == 0 else None
        except Exception as e:
            logger.error(f"获取 Git diff 失败: {e}")
            return None
    
    def analyze_diff_stat(self, diff_stat: str) -> Dict[str, Any]:
        """分析 diff --stat 输出，提取变更摘要"""
        if not diff_stat:
            return {"error": "无 diff 数据"}
        
        lines = diff_stat.strip().split('\n')
        summary = {
            "files_changed": 0,
            "insertions": 0,
            "deletions": 0,
            "file_changes": []
        }
        
        # 解析类似 " 10 files changed, 200 insertions(+), 50 deletions(-)" 的行
        for line in lines:
            line = line.strip()
            
            # 汇总行
            if "files changed" in line:
                match = re.search(r'(\d+)\s+files? changed', line)
                if match:
                    summary["files_changed"] = int(match.group(1))
                
                insert_match = re.search(r'(\d+)\s+insertions?\(\+\)', line)
                if insert_match:
                    summary["insertions"] = int(insert_match.group(1))
                
                delete_match = re.search(r'(\d+)\s+deletions?\(-\)', line)
                if delete_match:
                    summary["deletions"] = int(delete_match.group(1))
            
            # 文件变更行（例如 "src/core.py | 20 ++++++----"）
            elif '|' in line and ('+' in line or '-' in line):
                parts = line.split('|')
                if len(parts) == 2:
                    filename = parts[0].strip()
                    changes = parts[1].strip()
                    
                    # 提取增减数量
                    plus_count = changes.count('+')
                    minus_count = changes.count('-')
                    
                    summary["file_changes"].append({
                        "file": filename,
                        "insertions": plus_count,
                        "deletions": minus_count,
                        "total_changes": plus_count + minus_count
                    })
        
        return summary
    
    def get_github_diff(self, owner: str, repo: str, old_version: str, new_version: str) -> Optional[Dict[str, Any]]:
        """通过 GitHub API 获取两个版本之间的差异"""
        # 简化的实现：使用 git 命令
        # 实际应使用 requests 调用 GitHub API
        # 此处为占位实现
        logger.warning("GitHub API 调用未实现，回退到 Git 本地")
        return None
    
    def analyze_breaking_changes_from_diff(self, diff_content: str) -> List[str]:
        """从 diff 内容中分析可能的破坏性变更"""
        breaking = []
        
        # 检测删除的公共函数/类
        lines = diff_content.split('\n')
        for i, line in enumerate(lines):
            # 删除行以 "-" 开头
            if line.startswith('-') and not line.startswith('---'):
                stripped = line[1:].strip()
                
                # 检测函数/类定义删除
                if re.match(r'^(def|class)\s+\w+', stripped):
                    breaking.append(f"删除: {stripped}")
            
            # 函数签名变更（参数增减）
            elif line.startswith('+') and not line.startswith('+++'):
                prev_line = lines[i-1] if i > 0 else ""
                if prev_line.startswith('-') and 'def ' in prev_line and 'def ' in line:
                    breaking.append(f"函数签名变更: {prev_line[1:].strip()} -> {line[1:].strip()}")
        
        return breaking
    
    def analyze(self, plugin_name: str, old_version: str, new_version: str) -> Dict[str, Any]:
        """分析两个版本之间的代码变更集
        
        Returns:
            {
                "available": bool,
                "diff_stat": {files_changed, insertions, deletions, file_changes},
                "breaking_changes": List[str],
                "api_changes": List[str],
                "adapter_changes": List[str],
                "summary": str,
                "source": "git" | "github" | "none"
            }
        """
        result = {
            "available": False,
            "diff_stat": {},
            "breaking_changes": [],
            "api_changes": [],
            "adapter_changes": [],
            "summary": "无法获取代码变更集",
            "source": "none"
        }
        
        # 尝试获取 GitHub 仓库 URL
        repo_url = self.get_github_repo_url(plugin_name)
        if not repo_url or "github.com" not in repo_url:
            result["summary"] = "无法确定 GitHub 仓库 URL"
            return result
        
        # 克隆仓库
        repo_dir = self.clone_repo_if_needed(repo_url, new_version)
        if not repo_dir:
            result["summary"] = "无法克隆仓库"
            return result
        
        # 获取 Git diff
        diff_stat = self.get_git_diff(repo_dir, old_version, new_version)
        if not diff_stat:
            result["summary"] = "无法获取版本差异"
            return result
        
        # 分析 diff
        diff_analysis = self.analyze_diff_stat(diff_stat)
        
        # 获取完整 diff 以分析破坏性变更
        try:
            full_diff = subprocess.run(
                ["git", "-C", str(repo_dir), "diff", f"v{old_version}..v{new_version}", "-U3"],
                capture_output=True,
                text=True
            ).stdout
        except Exception:
            full_diff = ""
        
        breaking_changes = self.analyze_breaking_changes_from_diff(full_diff)
        
        # 检测 API 变更（简化）
        api_changes = []
        if "adapter" in plugin_name.lower():
            api_changes.append("适配器相关插件，需检查接口变更")
        
        # 检测适配器变更
        adapter_changes = []
        for file_change in diff_analysis.get("file_changes", []):
            if "adapter" in file_change["file"].lower():
                adapter_changes.append(file_change["file"])
        
        result.update({
            "available": True,
            "diff_stat": diff_analysis,
            "breaking_changes": breaking_changes,
            "api_changes": api_changes,
            "adapter_changes": adapter_changes,
            "summary": f"变更: {diff_analysis.get('files_changed', 0)} 文件, +{diff_analysis.get('insertions', 0)}/-{diff_analysis.get('deletions', 0)} 行",
            "source": "git"
        })
        
        return result


class ConflictDetector:
    """插件升级冲突检测器"""
    
    def __init__(self, registry_path: Optional[str] = None):
        """初始化检测器
        
        Args:
            registry_path: 星型架构注册表路径
        """
        if registry_path is None:
            self.registry_path = Path("/root/.openclaw/workspace/skills/star-plugin-upgrader/star_architecture_registry.json")
        else:
            self.registry_path = Path(registry_path)
        
        self.registry = self._load_registry()
    
    def _load_registry(self) -> Dict[str, Any]:
        """加载注册表"""
        if not self.registry_path.exists():
            return {}
        
        try:
            with open(self.registry_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"加载注册表失败: {e}")
            return {}
    
    def get_plugin_dependencies(self, plugin_name: str) -> List[str]:
        """获取插件的依赖列表"""
        if not self.registry or "components" not in self.registry:
            return []
        
        plugins = self.registry["components"].get("plugins", [])
        for plugin in plugins:
            if plugin.get("slug") == plugin_name:
                return plugin.get("dependencies", [])
        
        return []
    
    def detect_conflicts(self, upgrades: List[Dict[str, str]]) -> Dict[str, Any]:
        """检测多个插件升级时的冲突
        
        Args:
            upgrades: 列表，每个元素为 {"plugin": "插件名", "from": "旧版本", "to": "新版本"}
        
        Returns:
            {
                "has_conflicts": bool,
                "conflicts": List[冲突描述],
                "recommendations": List[建议]
            }
        """
        conflicts = []
        recommendations = []
        
        # 构建依赖图
        dependency_graph = {}
        for upgrade in upgrades:
            plugin = upgrade["plugin"]
            deps = self.get_plugin_dependencies(plugin)
            dependency_graph[plugin] = deps
        
        # 检查循环依赖
        # 简化：仅检查直接依赖冲突
        for plugin, deps in dependency_graph.items():
            for dep in deps:
                # 如果依赖也在升级列表中，检查版本兼容性
                dep_upgrade = next((u for u in upgrades if u["plugin"] == dep), None)
                if dep_upgrade:
                    # 简化：假设任何跨主版本升级都可能不兼容
                    old_major = dep_upgrade["from"].split('.')[0]
                    new_major = dep_upgrade["to"].split('.')[0]
                    if old_major != new_major:
                        conflicts.append(f"插件 {plugin} 依赖 {dep}，但 {dep} 正在进行主版本升级 ({dep_upgrade['from']} -> {dep_upgrade['to']})，可能不兼容")
                        recommendations.append(f"建议先升级 {dep}，验证兼容性后再升级 {plugin}")
        
        # 检查适配器接口变更
        for upgrade in upgrades:
            if "adapter" in upgrade["plugin"].lower():
                conflicts.append(f"适配器插件 {upgrade['plugin']} 升级可能影响依赖它的其他插件")
                recommendations.append(f"升级 {upgrade['plugin']} 后运行适配器健康检查")
        
        return {
            "has_conflicts": len(conflicts) > 0,
            "conflicts": conflicts,
            "recommendations": recommendations
        }


if __name__ == "__main__":
    # 测试
    analyzer = DiffAnalyzer()
    result = analyzer.analyze("co-occurrence-engine", "0.1.0", "0.2.0")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    detector = ConflictDetector()
    upgrades = [
        {"plugin": "co-occurrence-engine", "from": "0.1.0", "to": "0.2.0"},
        {"plugin": "memory-integration", "from": "0.1.0", "to": "0.2.0"}
    ]
    conflicts = detector.detect_conflicts(upgrades)
    print("\n冲突检测:")
    print(json.dumps(conflicts, indent=2, ensure_ascii=False))