#!/usr/bin/env python3
"""
evolution-watcher 监控脚本 MVP v0.6.0

功能：监控 ClawHub 上已安装插件的更新，生成报告
原则：只读操作，不执行任何自动升级
"""

import os
import sys
import json
import subprocess
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# 添加技能目录到路径，便于导入本地模块
skill_dir = Path(__file__).parent.parent
sys.path.insert(0, str(skill_dir))

# 导入第二阶段模块
try:
    from adapter_auto_fix import AdapterAutoFixer
except ImportError as e:
    print(f"⚠️  无法导入 AdapterAutoFixer: {e}")
    AdapterAutoFixer = None

class ImpactAssessor:
    """插件更新影响评估器"""
    
    def __init__(self, registry_path: str = None):
        """初始化评估器
        
        Args:
            registry_path: 星型架构注册表路径
        """
        self.registry_path = registry_path or "/root/.openclaw/workspace/skills/star-plugin-upgrader/star_architecture_registry.json"
        self.registry = self.load_registry()
    
    def load_registry(self) -> dict:
        """加载星型架构注册表"""
        try:
            if os.path.exists(self.registry_path):
                with open(self.registry_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"⚠️  无法加载星型架构注册表: {e}")
            return {}
    
    def get_plugin_safety_level(self, plugin_name: str) -> str:
        """从注册表获取插件安全级别"""
        if not self.registry or "components" not in self.registry:
            return "medium"  # 默认中等风险
        
        # 在 plugins 列表中查找
        plugins = self.registry["components"].get("plugins", [])
        for plugin in plugins:
            if plugin.get("slug") == plugin_name:
                return plugin.get("safety_level", "medium")
        
        return "medium"
    
    def parse_semver(self, version: str) -> tuple:
        """解析语义化版本号 (major.minor.patch)
        
        Returns:
            (major, minor, patch) 元组，解析失败返回 (0, 0, 0)
        """
        if not version:
            return (0, 0, 0)
        
        # 移除可能的 'v' 前缀和非数字后缀
        version = version.lstrip('v')
        parts = version.split('.')
        
        try:
            major = int(parts[0]) if len(parts) > 0 else 0
            minor = int(parts[1]) if len(parts) > 1 else 0
            patch = int(parts[2]) if len(parts) > 2 else 0
            return (major, minor, patch)
        except ValueError:
            return (0, 0, 0)
    
    def assess_impact(self, plugin_name: str, current_version: str, latest_version: str) -> dict:
        """评估插件更新的影响
        
        Returns:
            {
                "risk_level": "low|medium|high",
                "change_type": "patch|minor|major",
                "recommendation": "建议文本",
                "confidence": 0.0-1.0,
                "factors": ["因素列表"]
            }
        """
        factors = []
        
        # 1. 解析版本号
        current_semver = self.parse_semver(current_version)
        latest_semver = self.parse_semver(latest_version)
        
        # 2. 确定变更类型
        if current_semver[0] < latest_semver[0]:
            change_type = "major"
            factors.append("主要版本更新 (可能包含破坏性变更)")
        elif current_semver[1] < latest_semver[1]:
            change_type = "minor"
            factors.append("次要版本更新 (可能包含新功能)")
        elif current_semver[2] < latest_semver[2]:
            change_type = "patch"
            factors.append("补丁版本更新 (通常为错误修复)")
        else:
            change_type = "unknown"
            factors.append("版本号无法比较")
        
        # 3. 获取安全级别
        safety_level = self.get_plugin_safety_level(plugin_name)
        factors.append(f"安全级别: {safety_level}")
        
        # 4. 计算风险等级
        risk_matrix = {
            ("major", "critical"): "high",
            ("major", "medium"): "high",
            ("major", "low"): "medium",
            ("minor", "critical"): "medium",
            ("minor", "medium"): "medium",
            ("minor", "low"): "low",
            ("patch", "critical"): "medium",
            ("patch", "medium"): "low",
            ("patch", "low"): "low"
        }
        
        risk_level = risk_matrix.get((change_type, safety_level), "medium")
        
        # 5. 生成建议
        recommendations = {
            "high": "⚠️ **高风险**: 建议在测试环境中充分验证后再升级，并仔细检查变更日志。",
            "medium": "⚠️ **中等风险**: 建议在非关键环境中先行测试，确认兼容性后再升级。",
            "low": "✅ **低风险**: 可安全升级，但仍建议在低峰时段进行。"
        }
        
        recommendation = recommendations.get(risk_level, "建议查看变更日志后再决定是否升级。")
        
        # 6. 置信度 (基于版本号解析的可靠性)
        confidence = 1.0 if current_semver != (0, 0, 0) and latest_semver != (0, 0, 0) else 0.5
        
        return {
            "risk_level": risk_level,
            "change_type": change_type,
            "recommendation": recommendation,
            "confidence": confidence,
            "factors": factors
        }

class ChangelogParser:
    """变更日志解析器"""
    
    def __init__(self):
        self.supported_formats = ["md", "txt", "markdown"]
        self.changelog_patterns = [
            r"^##?\s*\[?(v?[\d\.]+)\]?\s*[—-]?\s*\d{4}-\d{2}-\d{2}",
            r"^##?\s*\d{4}-\d{2}-\d{2}\s*[—-]?\s*\[?(v?[\d\.]+)\]?",
            r"^##?\s*\[?(v?[\d\.]+)\]?",
            r"^#\s*变更日志",
            r"^#\s*Changelog"
        ]
    
    def find_changelog_file(self, plugin_path: str) -> str:
        """查找插件目录中的变更日志文件"""
        plugin_dir = Path(plugin_path)
        if not plugin_dir.exists():
            return ""
        
        # 常见变更日志文件名
        common_names = [
            "CHANGELOG.md", "CHANGELOG", "changelog.md", "changelog",
            "CHANGES.md", "CHANGES", "changes.md", "changes",
            "HISTORY.md", "HISTORY", "history.md", "history",
            "RELEASE_NOTES.md", "RELEASE_NOTES", "release_notes.md", "release_notes"
        ]
        
        for name in common_names:
            file_path = plugin_dir / name
            if file_path.exists() and file_path.is_file():
                return str(file_path)
        
        return ""
    
    def parse_changelog(self, file_path: str) -> Dict[str, Dict]:
        """解析变更日志文件，返回版本到内容的映射"""
        if not file_path or not os.path.exists(file_path):
            return {}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"⚠️  无法读取变更日志文件 {file_path}: {e}")
            return {}
        
        # 按行分割
        lines = content.split('\n')
        versions = {}
        current_version = None
        current_content = []
        in_version_section = False
        
        for line in lines:
            # 检查是否为版本标题行
            version_match = None
            for pattern in self.changelog_patterns:
                import re
                match = re.match(pattern, line.strip(), re.IGNORECASE)
                if match:
                    version_match = match
                    break
            
            if version_match:
                # 保存前一个版本的内容
                if current_version and current_content:
                    versions[current_version] = {
                        "content": "\n".join(current_content).strip(),
                        "lines": len(current_content)
                    }
                
                # 提取版本号
                # 尝试从匹配中提取
                import re
                version_text = line.strip()
                # 查找版本号模式
                version_num_match = re.search(r'v?(\d+\.\d+\.\d+|\d+\.\d+)', version_text)
                if version_num_match:
                    current_version = version_num_match.group(1).lstrip('v')
                else:
                    # 如果没有明确的版本号，使用标题文本
                    current_version = version_text[:50]
                
                current_content = [line]
                in_version_section = True
            
            elif in_version_section:
                # 如果遇到新的顶级标题（# 开头），结束当前版本部分
                if line.strip().startswith('# ') and len(line.strip()) > 2:
                    if current_version and current_content:
                        versions[current_version] = {
                            "content": "\n".join(current_content).strip(),
                            "lines": len(current_content)
                        }
                    current_version = None
                    current_content = []
                    in_version_section = False
                else:
                    current_content.append(line)
            else:
                # 不在任何版本部分，跳过
                pass
        
        # 保存最后一个版本
        if current_version and current_content:
            versions[current_version] = {
                "content": "\n".join(current_content).strip(),
                "lines": len(current_content)
            }
        
        return versions
    
    def get_changelog_for_version(self, plugin_path: str, version: str) -> Dict[str, any]:
        """获取特定版本的变更日志"""
        changelog_file = self.find_changelog_file(plugin_path)
        if not changelog_file:
            return {"available": False, "message": "未找到变更日志文件"}
        
        versions = self.parse_changelog(changelog_file)
        if not versions:
            return {"available": False, "message": "变更日志文件为空或无法解析"}
        
        # 查找精确版本或最接近的版本
        target_version = version.lstrip('v')
        
        # 直接匹配
        if target_version in versions:
            return {
                "available": True,
                "version": target_version,
                "content": versions[target_version]["content"],
                "source_file": changelog_file,
                "exact_match": True
            }
        
        # 尝试匹配没有前缀v的版本
        for ver_key in versions.keys():
            if ver_key.lstrip('v') == target_version:
                return {
                    "available": True,
                    "version": ver_key,
                    "content": versions[ver_key]["content"],
                    "source_file": changelog_file,
                    "exact_match": True
                }
        
        # 如果没有精确匹配，返回所有可用版本
        return {
            "available": True,
            "version": target_version,
            "content": f"未找到版本 {target_version} 的变更日志。可用版本: {', '.join(versions.keys())}",
            "source_file": changelog_file,
            "exact_match": False,
            "available_versions": list(versions.keys())
        }
    
    def extract_breaking_changes(self, changelog_content: str) -> List[str]:
        """从变更日志内容中提取破坏性变更"""
        import re
        breaking_changes = []
        
        # 常见破坏性变更标识
        patterns = [
            r"###?\s*Breaking Changes?",
            r"###?\s*破坏性变更",
            r"⚠️\s*Breaking",
            r"BREAKING CHANGE",
            r"###?\s*重大变更"
        ]
        
        lines = changelog_content.split('\n')
        in_breaking_section = False
        
        for line in lines:
            line_lower = line.lower()
            
            # 检查是否进入破坏性变更部分
            for pattern in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    in_breaking_section = True
                    break
            
            # 如果在破坏性变更部分，收集内容
            if in_breaking_section:
                if line.strip() and not re.match(r'^#+\s', line):
                    breaking_changes.append(line.strip())
                elif re.match(r'^#+\s', line) and "breaking" not in line_lower:
                    # 遇到新的标题，退出破坏性变更部分
                    in_breaking_section = False
        
        return [bc for bc in breaking_changes if bc]
    
    def categorize_changes(self, changelog_content: str) -> Dict[str, any]:
        """将变更日志内容按类别分类（增强版 - B3 简化）
        
        增强功能：
        1. 添加 breaking_changes 类别，专门检测破坏性变更
        2. 添加 api_changes 类别，检测 API 相关变更
        3. 添加 adapter_changes 类别，检测适配器相关变更
        4. 更精确的模式匹配，支持多种语言和格式
        5. 提取变更项中的适配器变更关键词，便于后续映射
        """
        import re
        
        # 定义变更类别和对应的模式（增强版）
        categories = {
            "breaking_changes": [
                r"###?\s*Breaking Changes",
                r"###?\s*破坏性变更",
                r"###?\s*BREAKING CHANGES",
                r"###?\s*不兼容变更",
                r"###?\s*API Breaking",
                r"###?\s*接口破坏性变更",
                r"^##?\s*.*[⚠️🚨❗]"
            ],
            "added": [
                r"###?\s*Added",
                r"###?\s*新增",
                r"###?\s*New Features",
                r"###?\s*新功能",
                r"###?\s*Features",
                r"\+ "
            ],
            "changed": [
                r"###?\s*Changed",
                r"###?\s*变更",
                r"###?\s*修改",
                r"###?\s*改进",
                r"###?\s*Updates",
                r"###?\s*更新"
            ],
            "api_changes": [
                r"###?\s*API Changes",
                r"###?\s*API 变更",
                r"###?\s*接口变更",
                r"###?\s*方法变更",
                r"###?\s*函数变更"
            ],
            "adapter_changes": [
                r"###?\s*Adapter Changes",
                r"###?\s*适配器变更",
                r"###?\s*连接器变更",
                r"###?\s*插件接口变更",
                r"###?\s*星型架构变更"
            ],
            "fixed": [
                r"###?\s*Fixed",
                r"###?\s*修复",
                r"###?\s*Bug Fixes",
                r"###?\s*Bug修复",
                r"###?\s*错误修复",
                r"###?\s*问题修复"
            ],
            "removed": [
                r"###?\s*Removed",
                r"###?\s*移除",
                r"###?\s*删除",
                r"###?\s*废弃",
                r"###?\s*Deprecated and Removed"
            ],
            "deprecated": [
                r"###?\s*Deprecated",
                r"###?\s*弃用",
                r"###?\s*即将移除",
                r"###?\s*未来版本移除"
            ],
            "security": [
                r"###?\s*Security",
                r"###?\s*安全",
                r"###?\s*漏洞",
                r"###?\s*安全修复",
                r"###?\s*CVE"
            ]
        }
        
        # 初始化结果
        categorized = {cat: [] for cat in categories.keys()}
        categorized["uncategorized"] = []
        
        # 计算影响分数权重（增强版）
        weights = {
            "breaking_changes": 5.0,     # 破坏性变更风险最高
            "added": 1.0,
            "changed": 2.0,
            "api_changes": 3.0,          # API变更风险较高
            "adapter_changes": 4.0,      # 适配器变更风险高
            "fixed": 0.5,
            "removed": 3.5,
            "deprecated": 2.5,
            "security": 4.0,
            "uncategorized": 1.0
        }
        
        lines = changelog_content.split('\n')
        current_category = "uncategorized"
        current_items = []
        
        for line in lines:
            line_stripped = line.strip()
            
            # 检查是否为类别标题
            category_found = False
            for cat, patterns in categories.items():
                for pattern in patterns:
                    if re.match(pattern, line_stripped, re.IGNORECASE):
                        # 保存前一个类别的项目
                        if current_items:
                            categorized[current_category].extend(current_items)
                        
                        # 开始新类别
                        current_category = cat
                        current_items = []
                        category_found = True
                        break
                if category_found:
                    break
            
            if not category_found:
                # 如果是列表项（以-、*、+开头）或数字列表，添加到当前类别
                if line_stripped and (line_stripped.startswith('-') or 
                                     line_stripped.startswith('*') or 
                                     line_stripped.startswith('+') or
                                     re.match(r'^\d+\.', line_stripped)):
                    current_items.append(line_stripped)
                elif line_stripped and not line_stripped.startswith('#'):
                    # 非标题文本，如果当前有类别也添加
                    if current_category:
                        current_items.append(line_stripped)
        
        # 添加最后一个类别的项目
        if current_items:
            categorized[current_category].extend(current_items)
        
        # 清理空项目
        for cat in categorized:
            categorized[cat] = [item for item in categorized[cat] if item]
        
        # 计算影响分数
        impact_score = 0.0
        for cat, items in categorized.items():
            impact_score += len(items) * weights.get(cat, 1.0)
        
        # 计算破坏性变更分数（包括 breaking_changes, removed, deprecated）
        destructive_score = (
            len(categorized["breaking_changes"]) * 5.0 +
            len(categorized["removed"]) * 3.5 +
            len(categorized["deprecated"]) * 2.5 +
            len(categorized["api_changes"]) * 2.0 +
            len(categorized["adapter_changes"]) * 4.0
        )
        
        # 提取适配器变更关键词（用于后续映射）
        adapter_keywords = self._extract_adapter_keywords(categorized)
        
        return {
            "categories": categorized,
            "impact_score": round(impact_score, 2),
            "destructive_score": round(destructive_score, 2),
            "total_changes": sum(len(items) for items in categorized.values()),
            "category_counts": {cat: len(items) for cat, items in categorized.items() if items},
            "adapter_keywords": adapter_keywords,  # 新增：适配器变更关键词
            "has_breaking_changes": len(categorized["breaking_changes"]) > 0,
            "has_adapter_changes": len(categorized["adapter_changes"]) > 0
        }
    
    def _extract_adapter_keywords(self, categorized_changes: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """从分类的变更中提取适配器相关关键词
        
        Args:
            categorized_changes: 分类后的变更字典
            
        Returns:
            关键词映射：变更类型 -> [关键词列表]
        """
        adapter_patterns = {
            "function_rename": [
                r"rename",
                r"renamed",
                r"重命名",
                r"改名",
                r"function.*to",
                r"方法.*改为"
            ],
            "import_path_change": [
                r"import",
                r"导入",
                r"路径变更",
                r"路径更改",
                r"from.*to",
                r"module.*changed"
            ],
            "api_change": [
                r"API",
                r"接口",
                r"方法签名",
                r"参数变更",
                r"返回值",
                r"signature"
            ],
            "adapter_specific": [
                r"adapter",
                r"适配器",
                r"connector",
                r"连接器",
                r"plugin.*interface",
                r"插件接口"
            ]
        }
        
        extracted = {key: [] for key in adapter_patterns.keys()}
        
        for category, items in categorized_changes.items():
            for item in items:
                item_lower = item.lower()
                for change_type, patterns in adapter_patterns.items():
                    for pattern in patterns:
                        if re.search(pattern, item_lower, re.IGNORECASE):
                            # 提取上下文（最多5个词）
                            words = item.split()
                            context = " ".join(words[:min(8, len(words))])
                            if context not in extracted[change_type]:
                                extracted[change_type].append(context)
                            break  # 每个条目只匹配一种类型
        
        # 清理空列表
        return {k: v for k, v in extracted.items() if v}
    
    def generate_upgrade_script_suggestions(self, changelog_analysis: Dict, plugin_name: str) -> List[str]:
        """基于变更日志分析生成升级脚本建议"""
        suggestions = []
        categories = changelog_analysis.get("category_counts", {})
        
        if categories.get("removed"):
            suggestions.append(f"# 需要迁移已移除的功能")
            suggestions.append(f"# {plugin_name} 移除了 {categories['removed']} 个功能，请检查您的代码中是否使用了这些功能")
            suggestions.append("# 建议步骤:")
            suggestions.append("# 1. 搜索代码库中的相关API调用")
            suggestions.append("# 2. 查看替代方案或更新API用法")
            suggestions.append("# 3. 在测试环境中验证兼容性")
            suggestions.append("")
        
        if categories.get("deprecated"):
            suggestions.append(f"# 处理废弃的功能")
            suggestions.append(f"# {plugin_name} 废弃了 {categories['deprecated']} 个功能，将在未来版本中移除")
            suggestions.append("# 建议步骤:")
            suggestions.append("# 1. 检查代码中的废弃警告")
            suggestions.append("# 2. 迁移到推荐的新API")
            suggestions.append("# 3. 更新文档和配置")
            suggestions.append("")
        
        if categories.get("security"):
            suggestions.append(f"# 安全更新重要")
            suggestions.append(f"# {plugin_name} 包含 {categories['security']} 个安全修复，建议立即升级")
            suggestions.append("# 建议步骤:")
            suggestions.append("# 1. 立即在测试环境中验证")
            suggestions.append("# 2. 检查是否有相关漏洞影响您的系统")
            suggestions.append("# 3. 优先安排生产环境升级")
            suggestions.append("")
        
        if categories.get("added"):
            suggestions.append(f"# 新功能可用")
            suggestions.append(f"# {plugin_name} 添加了 {categories['added']} 个新功能")
            suggestions.append("# 建议步骤:")
            suggestions.append("# 1. 查看新功能的文档")
            suggestions.append("# 2. 评估是否集成到您的项目中")
            suggestions.append("# 3. 考虑性能影响和依赖变化")
            suggestions.append("")
        
        if categories.get("changed"):
            suggestions.append(f"# 现有功能变更")
            suggestions.append(f"# {plugin_name} 修改了 {categories['changed']} 个现有功能")
            suggestions.append("# 建议步骤:")
            suggestions.append("# 1. 测试相关功能的兼容性")
            suggestions.append("# 2. 更新配置和集成代码")
            suggestions.append("# 3. 通知团队成员变更影响")
            suggestions.append("")
        
        if categories.get("fixed"):
            suggestions.append(f"# Bug修复")
            suggestions.append(f"# {plugin_name} 修复了 {categories['fixed']} 个问题")
            suggestions.append("# 建议步骤:")
            suggestions.append("# 1. 检查您的系统是否受到这些Bug影响")
            suggestions.append("# 2. 验证修复是否解决了您遇到的问题")
            suggestions.append("# 3. 如果曾使用变通方案，考虑移除")
            suggestions.append("")
        
        # 如果没有特定建议，提供通用升级脚本
        if not suggestions:
            suggestions.append(f"# {plugin_name} 升级脚本")
            suggestions.append("# 请按照以下步骤安全升级:")
            suggestions.append("")
            suggestions.append("# 1. 备份当前配置和数据")
            suggestions.append(f"clawhub backup {plugin_name} --output {plugin_name}_backup_$(date +%Y%m%d)")
            suggestions.append("")
            suggestions.append("# 2. 在测试环境中升级")
            suggestions.append(f"clawhub update {plugin_name} --dry-run")
            suggestions.append("# 确认无错误后:")
            suggestions.append(f"clawhub update {plugin_name}")
            suggestions.append("")
            suggestions.append("# 3. 运行健康检查")
            suggestions.append(f"# 查看插件文档，运行相关测试")
            suggestions.append("")
            suggestions.append("# 4. 监控升级后的系统性能")
            suggestions.append("# 观察日志和指标24小时")
            suggestions.append("")
        
        return suggestions

class DependencyAnalyzer:
    """星型架构依赖关系分析器"""
    
    def __init__(self, registry_path: str = None):
        # 默认注册表路径
        if registry_path is None:
            self.registry_path = Path("/root/.openclaw/workspace/skills/star-plugin-upgrader/star_architecture_registry.json")
        else:
            self.registry_path = Path(registry_path)
        
        self.registry = None
        self.plugins = {}  # slug -> plugin info
        self.dependency_graph = {}  # slug -> [dependencies]
        self.reverse_graph = {}  # slug -> [dependents]
        self.edge_weights = {}  # (src, dst) -> weight (0.0-1.0)
        self.adapter_connections = []  # (src, dst, adapter_id, status, weight)
        self.load_registry()
    
    def load_registry(self):
        """加载星型架构注册表"""
        try:
            with open(self.registry_path, 'r', encoding='utf-8') as f:
                self.registry = json.load(f)
        except Exception as e:
            print(f"❌ 无法加载星型架构注册表: {e}")
            self.registry = {}
            return
        
        # 提取插件信息
        self.plugins = {}
        self.dependency_graph = {}
        self.reverse_graph = {}
        
        # 核心枢纽
        if "core_hub" in self.registry.get("components", {}):
            core = self.registry["components"]["core_hub"]
            self.plugins[core["slug"]] = {
                **core,
                "type": "core_hub"
            }
            # 核心枢纽可能有依赖吗？通常没有
            self.dependency_graph[core["slug"]] = []
        
        # 原生组件（非插件，但可能有依赖关系）
        if "native_memory" in self.registry.get("components", {}):
            native = self.registry["components"]["native_memory"]
            self.plugins[native["slug"]] = {
                **native,
                "type": "native"
            }
            self.dependency_graph[native["slug"]] = []
        
        # 插件列表
        for plugin in self.registry.get("components", {}).get("plugins", []):
            slug = plugin["slug"]
            self.plugins[slug] = {
                **plugin,
                "type": "plugin"
            }
            dependencies = plugin.get("dependencies", [])
            self.dependency_graph[slug] = dependencies
            
            # 构建反向图并记录边权重
            for dep in dependencies:
                if dep not in self.reverse_graph:
                    self.reverse_graph[dep] = []
                self.reverse_graph[dep].append(slug)
                # 记录边权重 (slug -> dep) 和反向边 (dep -> slug) 权重均为1.0
                self.edge_weights[(slug, dep)] = 1.0
                self.edge_weights[(dep, slug)] = 1.0
            
            # 确保依赖项也在图中（可能缺少）
            for dep in dependencies:
                if dep not in self.dependency_graph:
                    self.dependency_graph[dep] = []
        
        # 适配器关系（双向依赖） - 支持状态过滤
        self.adapter_connections = []
        adapters = self.registry.get("adapters", {})
        for adapter_id, adapter_info in adapters.items():
            connects = adapter_info.get("connects", [])
            status = adapter_info.get("status", "active")
            if len(connects) >= 2:
                src, dst = connects[0], connects[1]
                # 状态过滤：只有 active 状态的适配器才计入依赖图
                if status == "active":
                    # 添加双向边
                    if src not in self.dependency_graph:
                        self.dependency_graph[src] = []
                    if dst not in self.dependency_graph:
                        self.dependency_graph[dst] = []
                    # 避免重复
                    if dst not in self.dependency_graph[src]:
                        self.dependency_graph[src].append(dst)
                    if src not in self.dependency_graph[dst]:
                        self.dependency_graph[dst].append(src)
                    
                    # 更新反向图
                    if src not in self.reverse_graph:
                        self.reverse_graph[src] = []
                    if dst not in self.reverse_graph:
                        self.reverse_graph[dst] = []
                    if dst not in self.reverse_graph[src]:
                        self.reverse_graph[src].append(dst)
                    if src not in self.reverse_graph[dst]:
                        self.reverse_graph[dst].append(src)
                    
                    # 记录边权重（双向）
                    self.edge_weights[(src, dst)] = 1.0
                    self.edge_weights[(dst, src)] = 1.0
                    
                    self.adapter_connections.append((src, dst, adapter_id, status, 1.0))
                else:
                    # 非active适配器，记录但权重为0，不计入依赖图
                    self.adapter_connections.append((src, dst, adapter_id, status, 0.0))
    
    def get_direct_dependencies(self, plugin_slug: str) -> List[str]:
        """获取插件的直接依赖"""
        return self.dependency_graph.get(plugin_slug, [])
    
    def get_direct_dependents(self, plugin_slug: str) -> List[str]:
        """获取直接依赖此插件的插件（下游依赖）"""
        return self.reverse_graph.get(plugin_slug, [])
    
    def get_transitive_dependencies(self, plugin_slug: str, visited=None) -> List[str]:
        """获取传递依赖（所有依赖的依赖）"""
        if visited is None:
            visited = set()
        
        if plugin_slug in visited:
            return []
        
        visited.add(plugin_slug)
        all_deps = []
        
        for dep in self.dependency_graph.get(plugin_slug, []):
            if dep not in visited:
                all_deps.append(dep)
                all_deps.extend(self.get_transitive_dependencies(dep, visited))
        
        return list(set(all_deps))
    
    def get_transitive_dependents(self, plugin_slug: str, visited=None) -> List[str]:
        """获取传递依赖项（所有依赖此插件的插件）"""
        if visited is None:
            visited = set()
        
        if plugin_slug in visited:
            return []
        
        visited.add(plugin_slug)
        all_deps = []
        
        for dep in self.reverse_graph.get(plugin_slug, []):
            if dep not in visited:
                all_deps.append(dep)
                all_deps.extend(self.get_transitive_dependents(dep, visited))
        
        return list(set(all_deps))
    
    def analyze_impact(self, plugin_slug: str) -> Dict[str, any]:
        """分析插件升级的依赖影响"""
        if plugin_slug not in self.plugins:
            return {"error": f"插件 {plugin_slug} 不在注册表中"}
        
        plugin = self.plugins[plugin_slug]
        direct_deps = self.get_direct_dependencies(plugin_slug)
        direct_dependents = self.get_direct_dependents(plugin_slug)
        transitive_deps = self.get_transitive_dependencies(plugin_slug)
        transitive_dependents = self.get_transitive_dependents(plugin_slug)
        
        # 计算影响分数
        # 基础分数：加权下游依赖数量（考虑适配器状态）
        base_impact = sum(self.edge_weights.get((dep, plugin_slug), 0.0) for dep in direct_dependents)
        
        # 权重：插件安全级别
        safety_weights = {
            "critical": 3.0,
            "high": 2.0,
            "medium": 1.5,
            "low": 1.0
        }
        safety_weight = safety_weights.get(plugin.get("safety_level", "medium"), 1.0)
        
        # 插件类型权重
        type_weights = {
            "core_hub": 3.0,
            "plugin": 1.0,
            "native": 0.5
        }
        type_weight = type_weights.get(plugin.get("type", "plugin"), 1.0)
        
        # 依赖深度权重（传递依赖越多，影响越复杂）
        depth_weight = 1.0 + (len(transitive_dependents) * 0.1)
        
        # 最终影响分数
        impact_score = base_impact * safety_weight * type_weight * depth_weight
        
        # 风险等级
        if impact_score >= 10:
            risk_level = "high"
        elif impact_score >= 5:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        # 生成建议
        if len(direct_dependents) > 0:
            if risk_level == "high":
                recommendation = f"⚠️ **高影响**: {plugin_slug} 是 {len(direct_dependents)} 个插件的直接依赖，升级可能产生连锁反应。建议按依赖顺序升级：先升级 {plugin_slug}，然后依次升级依赖它的插件。"
            elif risk_level == "medium":
                recommendation = f"⚠️ **中等影响**: {plugin_slug} 有 {len(direct_dependents)} 个直接下游依赖。建议在升级前测试这些插件的兼容性。"
            else:
                recommendation = f"✅ **低影响**: {plugin_slug} 依赖关系简单，升级风险较低。但仍建议验证直接下游依赖。"
        else:
            recommendation = f"✅ **无下游依赖**: {plugin_slug} 没有其他插件直接依赖它，升级影响仅限于自身。"
        
        # 收集相关适配器连接
        adapter_connections = []
        for src, dst, adapter_id, status, weight in self.adapter_connections:
            if src == plugin_slug or dst == plugin_slug:
                other = dst if src == plugin_slug else src
                adapter_connections.append({
                    "adapter_id": adapter_id,
                    "connected_plugin": other,
                    "status": status,
                    "weight": weight,
                    "direction": "outgoing" if src == plugin_slug else "incoming"
                })
        
        return {
            "plugin": plugin_slug,
            "plugin_type": plugin.get("type"),
            "safety_level": plugin.get("safety_level", "medium"),
            "direct_dependencies": direct_deps,
            "direct_dependents": direct_dependents,
            "transitive_dependencies": transitive_deps,
            "transitive_dependents": transitive_dependents,
            "impact_score": round(impact_score, 2),
            "risk_level": risk_level,
            "recommendation": recommendation,
            "dependency_depth": len(transitive_dependents),
            "downstream_count": len(direct_dependents),
            "adapter_connections": adapter_connections,
            "active_adapter_count": sum(1 for ac in adapter_connections if ac["status"] == "active")
        }
    
    def generate_dependency_report(self, plugin_slug: str) -> str:
        """生成依赖关系报告"""
        analysis = self.analyze_impact(plugin_slug)
        if "error" in analysis:
            return f"错误: {analysis['error']}"
        
        report_lines = []
        report_lines.append(f"# {plugin_slug} 依赖关系分析")
        report_lines.append("")
        report_lines.append(f"**插件类型**: {analysis['plugin_type']}")
        report_lines.append(f"**安全级别**: {analysis['safety_level']}")
        report_lines.append("")
        report_lines.append(f"**直接影响分数**: {analysis['impact_score']}")
        report_lines.append(f"**依赖风险等级**: {analysis['risk_level']}")
        report_lines.append("")
        report_lines.append("## 直接依赖")
        report_lines.append("")
        if analysis['direct_dependencies']:
            for dep in analysis['direct_dependencies']:
                report_lines.append(f"- {dep}")
        else:
            report_lines.append("无直接依赖")
        report_lines.append("")
        report_lines.append("## 下游依赖（直接依赖此插件的插件）")
        report_lines.append("")
        if analysis['direct_dependents']:
            for dep in analysis['direct_dependents']:
                report_lines.append(f"- {dep}")
            report_lines.append("")
            report_lines.append(f"**共计**: {len(analysis['direct_dependents'])} 个插件直接依赖")
        else:
            report_lines.append("无下游依赖")
        report_lines.append("")
        report_lines.append("## 传递依赖（所有下游依赖链）")
        report_lines.append("")
        if analysis['transitive_dependents']:
            for dep in analysis['transitive_dependents']:
                report_lines.append(f"- {dep}")
            report_lines.append("")
            report_lines.append(f"**共计**: {len(analysis['transitive_dependents'])} 个插件在依赖链中")
        else:
            report_lines.append("无传递依赖")
        report_lines.append("")
        # 适配器连接
        report_lines.append("## 适配器连接")
        report_lines.append("")
        adapter_connections = analysis.get("adapter_connections", [])
        if adapter_connections:
            active_count = analysis.get("active_adapter_count", 0)
            report_lines.append(f"**活动适配器**: {active_count}/{len(adapter_connections)}")
            report_lines.append("")
            for conn in adapter_connections:
                status_emoji = {"active": "🟢", "pending": "🟡", "planned": "🟠", "disabled": "🔴"}.get(conn["status"], "⚪")
                weight_indicator = "✓" if conn["weight"] > 0 else "✗"
                report_lines.append(f"- {status_emoji} **{conn['adapter_id']}** → {conn['connected_plugin']} ({conn['status']}, 权重: {conn['weight']}) {weight_indicator}")
        else:
            report_lines.append("无适配器连接")
        report_lines.append("")
        report_lines.append("## 升级建议")
        report_lines.append("")
        report_lines.append(analysis['recommendation'])
        
        return "\n".join(report_lines)


class PriorityCalculator:
    """升级优先级计算器
    
    基于加权影响分数、风险等级、变更类型等因素计算插件升级优先级
    """
    
    def __init__(self):
        """初始化优先级计算器"""
        # 权重配置（可调整）
        self.weights = {
            "change_type": {
                "major": 3.0,    # 主版本更新
                "minor": 2.0,    # 次版本更新  
                "patch": 1.0     # 补丁版本更新
            },
            "risk_level": {
                "high": 0.3,     # 高风险 - 降低优先级
                "medium": 0.8,   # 中风险
                "low": 1.0       # 低风险 - 正常优先级
            },
            "impact_normalization": 0.01,  # 影响分数归一化因子
            "benefit_multiplier": {
                "security": 1.5,   # 安全修复
                "performance": 1.3, # 性能改进
                "feature": 1.2,    # 新功能
                "bugfix": 1.1      # 错误修复
            }
        }
    
    def calculate_priority_score(self, plugin_data: dict) -> float:
        """计算单个插件的升级优先级分数
        
        Args:
            plugin_data: 插件数据，包含 impact、dependency_analysis、changelog_analysis 等字段
        
        Returns:
            优先级分数 (0-100)，越高表示越应该优先升级
        """
        # 基础分数：版本差异程度
        change_type = plugin_data.get("impact", {}).get("change_type", "patch")
        base_score = self.weights["change_type"].get(change_type, 1.0)
        
        # 风险权重
        risk_level = plugin_data.get("impact", {}).get("risk_level", "medium")
        risk_weight = self.weights["risk_level"].get(risk_level, 0.8)
        
        # 影响分数归一化
        impact_score = plugin_data.get("dependency_analysis", {}).get("impact_score", 0.0)
        # 影响分数可能很大（如107.1），需要归一化到合理范围
        normalized_impact = min(impact_score * self.weights["impact_normalization"], 1.0)
        impact_weight = 1.0 + normalized_impact  # 影响越大，优先级略高
        
        # 收益权重（基于变更日志分析）
        benefit_weight = self._calculate_benefit_weight(plugin_data)
        
        # 计算最终优先级分数
        priority_score = base_score * risk_weight * impact_weight * benefit_weight
        
        # 将分数缩放到 0-100 范围以便阅读
        scaled_score = min(priority_score * 10, 100)  # 经验缩放因子
        
        return round(scaled_score, 1)
    
    def _calculate_benefit_weight(self, plugin_data: dict) -> float:
        """计算收益权重（基于变更日志中的改进类型）"""
        changelog_analysis = plugin_data.get("changelog_analysis", {})
        if not changelog_analysis:
            return 1.0  # 无变更日志信息，默认权重
        
        benefit_weight = 1.0
        
        # 检查变更类别
        categories = changelog_analysis.get("categories", {})
        for category, count in categories.items():
            if category in self.weights["benefit_multiplier"]:
                # 每类变更的贡献递减（log(count+1)）
                multiplier = self.weights["benefit_multiplier"][category]
                benefit_weight *= (1.0 + (multiplier - 1.0) * min(count / 10, 1.0))
        
        # 限制权重范围
        return min(max(benefit_weight, 0.5), 2.0)
    
    def calculate_priorities(self, updates: List[dict]) -> List[dict]:
        """计算所有可升级插件的优先级
        
        Args:
            updates: 更新检测结果列表，包含插件数据
        
        Returns:
            按优先级排序的插件列表，每个插件添加 priority_score 和 recommendation 字段
        """
        # 筛选需要更新的插件
        updatable_plugins = [p for p in updates if p.get("needs_update", False)]
        
        if not updatable_plugins:
            return []
        
        # 计算每个插件的优先级分数
        for plugin in updatable_plugins:
            plugin["priority_score"] = self.calculate_priority_score(plugin)
            plugin["priority_recommendation"] = self._generate_recommendation(plugin)
        
        # 按优先级分数降序排序
        sorted_plugins = sorted(updatable_plugins, key=lambda x: x["priority_score"], reverse=True)
        
        return sorted_plugins
    
    def _generate_recommendation(self, plugin_data: dict) -> str:
        """根据优先级分数生成升级建议"""
        score = plugin_data.get("priority_score", 0)
        risk_level = plugin_data.get("impact", {}).get("risk_level", "medium")
        
        if score >= 80:
            return "🚀 优先升级：收益高，风险可控"
        elif score >= 60:
            return "✅ 建议升级：收益与风险平衡"
        elif score >= 40:
            return "⚠️  谨慎升级：风险较高或收益有限"
        elif score >= 20:
            return "🔍 评估后升级：建议详细测试变更"
        else:
            return "⏸️  暂缓升级：高风险或低收益"
    
    def generate_priority_report(self, prioritized_plugins: List[dict]) -> str:
        """生成优先级矩阵报告
        
        Args:
            prioritized_plugins: 已排序的插件列表
        
        Returns:
            Markdown格式的优先级报告
        """
        if not prioritized_plugins:
            return "🎯 无需要升级的插件"
        
        report_lines = []
        report_lines.append("## 🎯 升级优先级建议")
        report_lines.append("")
        report_lines.append(f"共发现 **{len(prioritized_plugins)}** 个插件可升级，按优先级排序：")
        report_lines.append("")
        
        # 创建优先级表格
        table_lines = []
        table_lines.append("| # | 插件 | 优先级分 | 风险等级 | 影响分数 | 变更类型 | 建议行动 |")
        table_lines.append("| - | ---- | -------- | -------- | -------- | -------- | -------- |")
        
        for i, plugin in enumerate(prioritized_plugins, 1):
            name = plugin.get("name", "unknown")
            priority_score = plugin.get("priority_score", 0)
            risk_level = plugin.get("impact", {}).get("risk_level", "unknown")
            impact_score = plugin.get("dependency_analysis", {}).get("impact_score", 0)
            change_type = plugin.get("impact", {}).get("change_type", "unknown")
            recommendation = plugin.get("priority_recommendation", "")
            
            # 风险等级表情符号
            risk_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(risk_level, "⚪")
            
            table_lines.append(
                f"| {i} | **{name}** | {priority_score:.1f} | {risk_emoji} {risk_level} | "
                f"{impact_score:.1f} | {change_type} | {recommendation} |"
            )
        
        report_lines.extend(table_lines)
        report_lines.append("")
        report_lines.append("### 📊 优先级评分说明")
        report_lines.append("")
        report_lines.append("- **分数范围**: 0-100分，越高表示越应该优先升级")
        report_lines.append("- **风险等级**: 🔴 高风险 (需要谨慎评估) → 🟡 中风险 → 🟢 低风险")
        report_lines.append("- **影响分数**: 插件升级对系统架构的潜在影响程度")
        report_lines.append("- **变更类型**: major (主版本) / minor (次版本) / patch (补丁)")
        report_lines.append("")
        report_lines.append("### ⚖️ 权重配置")
        report_lines.append("")
        report_lines.append("| 因素 | 权重 | 说明 |")
        report_lines.append("| ---- | ---- | ---- |")
        report_lines.append(f"| 主版本更新 | {self.weights['change_type']['major']}× | 可能包含破坏性变更 |")
        report_lines.append(f"| 次版本更新 | {self.weights['change_type']['minor']}× | 通常包含新功能 |")
        report_lines.append(f"| 补丁更新 | {self.weights['change_type']['patch']}× | 错误修复和安全更新 |")
        report_lines.append(f"| 高风险 | {self.weights['risk_level']['high']}× | 降低优先级，需谨慎 |")
        report_lines.append(f"| 中风险 | {self.weights['risk_level']['medium']}× | 正常优先级 |")
        report_lines.append(f"| 低风险 | {self.weights['risk_level']['low']}× | 正常优先级 |")
        report_lines.append(f"| 安全修复 | {self.weights['benefit_multiplier']['security']}× | 提高优先级 |")
        report_lines.append(f"| 性能改进 | {self.weights['benefit_multiplier']['performance']}× | 提高优先级 |")
        report_lines.append(f"| 新功能 | {self.weights['benefit_multiplier']['feature']}× | 提高优先级 |")
        report_lines.append(f"| 错误修复 | {self.weights['benefit_multiplier']['bugfix']}× | 提高优先级 |")
        
        return "\n".join(report_lines)


class AdapterChangeDetector:
    """适配器变更检测器
    
    检测插件更新对星型架构适配器连接的兼容性影响
    """
    
    def __init__(self, registry_path: str = None):
        """初始化检测器
        
        Args:
            registry_path: 星型架构注册表路径，默认使用 star-plugin-upgrader 中的注册表
        """
        self.registry_path = registry_path or (skill_dir.parent / "star-plugin-upgrader" / "star_architecture_registry.json")
        self.registry = self.load_registry()
    
    def load_registry(self) -> dict:
        """加载星型架构注册表"""
        try:
            with open(self.registry_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"⚠️  无法加载星型架构注册表 {self.registry_path}: {e}")
            return {"plugins": [], "adapters": []}
    
    def detect_adapter_changes(self, plugin_name: str, changelog_content: str, change_type: str, changelog_analysis: Dict = None) -> dict:
        """检测适配器相关变更（增强版 - B3 简化）
        
        增强功能：
        1. 支持可选的 changelog_analysis 参数，利用分类后的变更信息
        2. 使用增强的关键词匹配，包括适配器特定变更类型
        3. 更精确的风险评估，基于变更类别和影响范围
        
        Args:
            plugin_name: 插件名称
            changelog_content: 变更日志内容
            change_type: 版本变更类型 (major/minor/patch)
            changelog_analysis: 可选的变更日志分析结果（来自 categorize_changes）
        
        Returns:
            适配器变更分析结果
        """
        analysis = {
            "has_adapter_changes": False,
            "adapter_change_type": None,  # interface_change, api_change, dependency_change, none
            "breaking_changes": [],
            "affected_adapters": [],  # 受影响的适配器ID列表
            "affected_plugins": [],   # 受影响的插件名称列表
            "risk_level": "low",      # 风险等级
            "recommendation": "无适配器变更",
            "detected_change_types": []  # 新增：检测到的具体变更类型列表
        }
        
        # 如果注册表为空，跳过分析
        if not self.registry.get("plugins"):
            return analysis
        
        # 查找插件在注册表中的信息
        plugin_info = self.find_plugin_in_registry(plugin_name)
        if not plugin_info:
            return analysis
        
        # 如果有 changelog_analysis，使用其分类结果
        if changelog_analysis:
            categories = changelog_analysis.get("categories", {})
            adapter_keywords = changelog_analysis.get("adapter_keywords", {})
            has_breaking_changes = changelog_analysis.get("has_breaking_changes", False)
            has_adapter_changes = changelog_analysis.get("has_adapter_changes", False)
            
            # 基于分类结果检测适配器变更
            adapter_change_detected = (
                has_adapter_changes or 
                len(categories.get("adapter_changes", [])) > 0 or
                len(categories.get("api_changes", [])) > 0 or
                len(categories.get("breaking_changes", [])) > 0 or
                any(len(items) > 0 for key, items in adapter_keywords.items())
            )
        else:
            # 回退到原始关键词匹配
            adapter_keywords_list = [
                "adapter", "interface", "api", "protocol", "connector",
                "breaking change", "breaking", "incompatible", "deprecated",
                "签名", "参数", "返回值", "方法", "函数"
            ]
            adapter_change_detected = any(keyword.lower() in changelog_content.lower() 
                                          for keyword in adapter_keywords_list)
            has_breaking_changes = False
            adapter_keywords = {}
        
        # 如果没有检测到适配器变更且不是主版本更新，返回基础分析
        if not adapter_change_detected and change_type != "major":
            return analysis
        
        # 标记存在适配器变更
        analysis["has_adapter_changes"] = True
        
        # 根据变更类型和分类结果确定适配器变更类型
        if change_type == "major":
            analysis["adapter_change_type"] = "interface_change"
            analysis["risk_level"] = "high"
            analysis["recommendation"] = "主版本更新可能包含适配器接口变更，请详细检查"
        elif change_type == "minor":
            analysis["adapter_change_type"] = "api_change"
            analysis["risk_level"] = "medium"
            analysis["recommendation"] = "次版本更新可能包含API变更，建议测试适配器兼容性"
        else:
            analysis["adapter_change_type"] = "dependency_change"
            analysis["risk_level"] = "low"
            analysis["recommendation"] = "补丁版本更新通常不影响适配器接口"
        
        # 提取破坏性变更（优先使用 changelog_analysis 中的 breaking_changes）
        if changelog_analysis and categories.get("breaking_changes"):
            breaking_changes = categories["breaking_changes"][:5]  # 最多5个
        else:
            breaking_changes = self.extract_breaking_changes(changelog_content)
        
        if breaking_changes:
            analysis["breaking_changes"] = breaking_changes
            analysis["risk_level"] = "high"
            analysis["recommendation"] = f"发现 {len(breaking_changes)} 个破坏性变更，适配器兼容性可能受影响"
        
        # 如果 changelog_analysis 中有 adapter_keywords，记录检测到的变更类型
        if adapter_keywords:
            for change_type_key, keywords in adapter_keywords.items():
                if keywords:
                    analysis["detected_change_types"].append(change_type_key)
            
            # 根据检测到的变更类型调整风险等级
            if "function_rename" in analysis["detected_change_types"]:
                analysis["adapter_change_type"] = "api_change"
                if analysis["risk_level"] != "high":
                    analysis["risk_level"] = "medium"
                analysis["recommendation"] += "（检测到函数重命名）"
            
            if "import_path_change" in analysis["detected_change_types"]:
                analysis["adapter_change_type"] = "interface_change"
                analysis["risk_level"] = "high"
                analysis["recommendation"] += "（检测到导入路径变更）"
        
        # 分析受影响的范围
        affected_analysis = self.analyze_affected_scope(plugin_info)
        analysis["affected_adapters"] = affected_analysis.get("affected_adapters", [])
        analysis["affected_plugins"] = affected_analysis.get("affected_plugins", [])
        
        # 根据受影响范围调整风险等级
        if analysis["affected_plugins"]:
            if analysis["risk_level"] != "high":
                analysis["risk_level"] = "medium"
            analysis["recommendation"] += f"，影响 {len(analysis['affected_plugins'])} 个下游插件"
        
        return analysis
    
    def find_plugin_in_registry(self, plugin_name: str) -> Optional[dict]:
        """在注册表中查找插件信息"""
        for plugin in self.registry.get("plugins", []):
            if plugin.get("name") == plugin_name:
                return plugin
        return None
    
    def extract_breaking_changes(self, changelog_content: str) -> List[str]:
        """从变更日志中提取破坏性变更描述"""
        breaking_changes = []
        lines = changelog_content.split('\n')
        
        # 查找标记为破坏性变更的行
        breaking_patterns = [
            "breaking change", "breaking:", "⚠️", "incompatible",
            "破坏性变更", "不兼容", "API变更", "接口变更"
        ]
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            if any(pattern in line_lower for pattern in breaking_patterns):
                # 提取变更描述（当前行和下一行）
                change_desc = line.strip()
                if i + 1 < len(lines) and lines[i + 1].strip():
                    change_desc += " " + lines[i + 1].strip()
                breaking_changes.append(change_desc[:200])  # 截断长描述
        
        return breaking_changes[:5]  # 最多返回5个
    
    def analyze_affected_scope(self, plugin_info: dict) -> dict:
        """分析插件变更对适配器连接的影响范围
        
        Args:
            plugin_info: 插件注册表信息
        
        Returns:
            影响范围分析结果
        """
        result = {
            "affected_adapters": [],
            "affected_plugins": []
        }
        
        plugin_id = plugin_info.get("id")
        plugin_name = plugin_info.get("name")
        
        # 查找该插件提供的适配器（作为提供者）
        provided_adapters = []
        for adapter in self.registry.get("adapters", []):
            if adapter.get("source_plugin") == plugin_id:
                provided_adapters.append(adapter)
        
        # 查找依赖该插件的适配器（作为消费者）
        dependent_adapters = []
        for adapter in self.registry.get("adapters", []):
            if adapter.get("target_plugin") == plugin_id:
                dependent_adapters.append(adapter)
        
        # 收集所有受影响的适配器
        all_affected_adapters = provided_adapters + dependent_adapters
        result["affected_adapters"] = [a.get("id") for a in all_affected_adapters]
        
        # 收集所有受影响的插件（通过适配器连接）
        affected_plugin_ids = set()
        for adapter in all_affected_adapters:
            affected_plugin_ids.add(adapter.get("source_plugin"))
            affected_plugin_ids.add(adapter.get("target_plugin"))
        
        # 移除当前插件自身
        affected_plugin_ids.discard(plugin_id)
        
        # 将插件ID转换为名称
        plugin_id_to_name = {
            p["id"]: p["name"] for p in self.registry.get("plugins", [])
        }
        
        result["affected_plugins"] = [
            plugin_id_to_name.get(pid, pid) 
            for pid in affected_plugin_ids 
            if pid in plugin_id_to_name
        ]
        
        return result
    
    def generate_adapter_change_report(self, analysis: dict) -> str:
        """生成适配器变更报告"""
        if not analysis["has_adapter_changes"]:
            return "🟢 **适配器变更**: 未检测到适配器相关变更"
        
        report_lines = []
        report_lines.append("## 🔌 适配器变更分析")
        report_lines.append("")
        
        # 变更类型和风险等级
        change_type_display = {
            "interface_change": "接口变更",
            "api_change": "API变更",
            "dependency_change": "依赖变更"
        }.get(analysis["adapter_change_type"], analysis["adapter_change_type"])
        
        risk_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(analysis["risk_level"], "⚪")
        
        report_lines.append(f"**变更类型**: {change_type_display}")
        report_lines.append(f"**风险等级**: {risk_emoji} {analysis['risk_level']}")
        report_lines.append("")
        
        # 受影响范围
        if analysis["affected_adapters"]:
            report_lines.append("**受影响适配器**:")
            for adapter_id in analysis["affected_adapters"][:5]:  # 最多显示5个
                report_lines.append(f"- `{adapter_id}`")
            if len(analysis["affected_adapters"]) > 5:
                report_lines.append(f"- ... 共 {len(analysis['affected_adapters'])} 个适配器")
            report_lines.append("")
        
        if analysis["affected_plugins"]:
            report_lines.append("**受影响插件**:")
            for plugin_name in analysis["affected_plugins"][:5]:  # 最多显示5个
                report_lines.append(f"- `{plugin_name}`")
            if len(analysis["affected_plugins"]) > 5:
                report_lines.append(f"- ... 共 {len(analysis['affected_plugins'])} 个插件")
            report_lines.append("")
        
        # 破坏性变更
        if analysis["breaking_changes"]:
            report_lines.append("**破坏性变更**:")
            for bc in analysis["breaking_changes"]:
                report_lines.append(f"- ⚠️ {bc}")
            report_lines.append("")
        
        # 建议
        report_lines.append("**建议**:")
        report_lines.append(f"- {analysis['recommendation']}")
        
        return "\n".join(report_lines)


class UpgradeScriptGenerator:
    """半自动升级脚本生成器
    
    根据优先级排序和适配器变更分析生成可执行的升级脚本
    支持干运行模式和安全验证
    """
    
    def __init__(self, config: dict = None):
        """初始化脚本生成器
        
        Args:
            config: 配置字典，包含脚本生成参数
        """
        self.config = config or {}
        self.default_config = {
            "dry_run": True,           # 默认干运行模式
            "include_rollback": True,  # 包含回滚机制
            "test_before_upgrade": True, # 升级前测试
            "batch_size": 1,           # 批量升级数量（1=逐个升级）
            "delay_between_upgrades": 30,  # 升级间隔（秒）
            "log_dir": "upgrade_logs", # 日志目录
            "backup_dir": "backups"    # 备份目录
        }
        self.config = {**self.default_config, **self.config}
        
        # 风险等级对应的安全措施
        self.risk_measures = {
            "high": {
                "pre_upgrade_test": True,
                "backup": True,
                "rollback_plan": True,
                "verify_after_upgrade": True,
                "delay_after_upgrade": 60
            },
            "medium": {
                "pre_upgrade_test": True,
                "backup": True,
                "rollback_plan": True,
                "verify_after_upgrade": True,
                "delay_after_upgrade": 30
            },
            "low": {
                "pre_upgrade_test": False,
                "backup": False,
                "rollback_plan": False,
                "verify_after_upgrade": True,
                "delay_after_upgrade": 10
            }
        }
    
    def generate_upgrade_script(self, prioritized_plugins: List[dict], output_path: str = None) -> dict:
        """生成升级脚本
        
        Args:
            prioritized_plugins: 已排序的插件列表（来自PriorityCalculator）
            output_path: 脚本输出路径，如果为None则只返回内容
        
        Returns:
            脚本生成结果，包含脚本内容和元数据
        """
        if not prioritized_plugins:
            return {
                "success": False,
                "error": "没有需要升级的插件",
                "script_content": "",
                "metadata": {}
            }
        
        # 脚本元数据
        metadata = {
            "total_plugins": len(prioritized_plugins),
            "high_risk_count": sum(1 for p in prioritized_plugins if p.get("impact", {}).get("risk_level") == "high"),
            "medium_risk_count": sum(1 for p in prioritized_plugins if p.get("impact", {}).get("risk_level") == "medium"),
            "low_risk_count": sum(1 for p in prioritized_plugins if p.get("impact", {}).get("risk_level") == "low"),
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "dry_run": self.config["dry_run"]
        }
        
        # 生成脚本内容
        script_lines = []
        
        # 脚本头部
        script_lines.append("#!/bin/bash")
        script_lines.append("# =========================================================")
        script_lines.append("# evolution-watcher 半自动升级脚本")
        script_lines.append("# 生成时间: " + metadata["generated_at"])
        script_lines.append("# 总插件数: " + str(metadata["total_plugins"]))
        script_lines.append("# 高风险: " + str(metadata["high_risk_count"]) + ", 中风险: " + str(metadata["medium_risk_count"]) + ", 低风险: " + str(metadata["low_risk_count"]))
        script_lines.append("# 模式: " + ("干运行 (预览)" if self.config["dry_run"] else "实际执行"))
        script_lines.append("# =========================================================")
        script_lines.append("")
        
        # 配置变量
        script_lines.append("# 配置变量")
        script_lines.append("DRY_RUN=" + ("true" if self.config["dry_run"] else "false"))
        script_lines.append("LOG_DIR=\"" + self.config["log_dir"] + "\"")
        script_lines.append("BACKUP_DIR=\"" + self.config["backup_dir"] + "\"")
        script_lines.append("BATCH_SIZE=" + str(self.config["batch_size"]))
        script_lines.append("DELAY_BETWEEN_UPGRADES=" + str(self.config["delay_between_upgrades"]))
        script_lines.append("")
        
        # 创建目录
        script_lines.append("# 创建必要目录")
        script_lines.append("mkdir -p \"$LOG_DIR\"")
        script_lines.append("mkdir -p \"$BACKUP_DIR\"")
        script_lines.append("")
        
        # 日志函数
        script_lines.append("# 日志函数")
        script_lines.append("log() {")
        script_lines.append("    local level=$1")
        script_lines.append("    local message=$2")
        script_lines.append("    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')")
        script_lines.append("    echo \"[$timestamp] [$level] $message\" | tee -a \"$LOG_DIR/upgrade.log\"")
        script_lines.append("}")
        script_lines.append("")
        
        # 验证函数
        script_lines.append("# 验证函数")
        script_lines.append("verify_clawhub() {")
        script_lines.append("    if ! command -v clawhub &> /dev/null; then")
        script_lines.append("        log \"ERROR\" \"ClawHub CLI 未安装或不在 PATH 中\"")
        script_lines.append("        return 1")
        script_lines.append("    fi")
        script_lines.append("    log \"INFO\" \"ClawHub CLI 验证成功\"")
        script_lines.append("    return 0")
        script_lines.append("}")
        script_lines.append("")
        
        # 备份函数
        script_lines.append("# 备份函数")
        script_lines.append("backup_plugin() {")
        script_lines.append("    local plugin_name=$1")
        script_lines.append("    local timestamp=$(date '+%Y%m%d_%H%M%S')")
        script_lines.append("    local backup_file=\"$BACKUP_DIR/${plugin_name}_${timestamp}.tar.gz\"")
        script_lines.append("    ")
        script_lines.append("    if [ \"$DRY_RUN\" = \"true\" ]; then")
        script_lines.append("        log \"INFO\" \"[干运行] 将备份插件: $plugin_name 到 $backup_file\"")
        script_lines.append("        return 0")
        script_lines.append("    fi")
        script_lines.append("    ")
        script_lines.append("    # 实际备份逻辑（需要根据实际情况调整）")
        script_lines.append("    log \"INFO\" \"备份插件: $plugin_name\"")
        script_lines.append("    # 示例：tar -czf \"$backup_file\" -C /root/.openclaw/workspace/skills \"$plugin_name\"")
        script_lines.append("    log \"INFO\" \"备份保存到: $backup_file\"")
        script_lines.append("}")
        script_lines.append("")
        
        # 升级函数
        script_lines.append("# 升级函数")
        script_lines.append("upgrade_plugin() {")
        script_lines.append("    local plugin_name=$1")
        script_lines.append("    local risk_level=$2")
        script_lines.append("    local adapter_changes=$3")
        script_lines.append("    ")
        script_lines.append("    log \"INFO\" \"开始升级插件: $plugin_name (风险等级: $risk_level)\"")
        script_lines.append("    ")
        script_lines.append("    # 根据风险等级应用安全措施")
        script_lines.append("    local measures=\"${risk_measures[$risk_level]}\"")
        script_lines.append("    ")
        script_lines.append("    if [ \"$DRY_RUN\" = \"true\" ]; then")
        script_lines.append("        log \"INFO\" \"[干运行] 将执行: clawhub update $plugin_name\"")
        script_lines.append("        log \"INFO\" \"[干运行] 适配器变更检测: $adapter_changes\"")
        script_lines.append("        return 0")
        script_lines.append("    fi")
        script_lines.append("    ")
        script_lines.append("    # 实际升级命令")
        script_lines.append("    log \"INFO\" \"执行: clawhub update $plugin_name\"")
        script_lines.append("    if clawhub update \"$plugin_name\"; then")
        script_lines.append("        log \"SUCCESS\" \"插件 $plugin_name 升级成功\"")
        script_lines.append("        return 0")
        script_lines.append("    else")
        script_lines.append("        log \"ERROR\" \"插件 $plugin_name 升级失败\"")
        script_lines.append("        return 1")
        script_lines.append("    fi")
        script_lines.append("}")
        script_lines.append("")
        
        # 风险等级措施映射
        script_lines.append("# 风险等级措施映射")
        script_lines.append("declare -A risk_measures")
        for risk_level, measures in self.risk_measures.items():
            script_lines.append(f"risk_measures[{risk_level}]=\"{measures}\"")
        script_lines.append("")
        
        # 主升级逻辑
        script_lines.append("# 主升级逻辑")
        script_lines.append("main() {")
        script_lines.append("    log \"INFO\" \"开始升级流程\"")
        script_lines.append("    ")
        script_lines.append("    # 验证环境")
        script_lines.append("    if ! verify_clawhub; then")
        script_lines.append("        exit 1")
        script_lines.append("    fi")
        script_lines.append("    ")
        script_lines.append("    # 按优先级顺序升级")
        script_lines.append("    local success_count=0")
        script_lines.append("    local fail_count=0")
        script_lines.append("    ")
        
        # 为每个插件生成升级步骤
        for i, plugin in enumerate(prioritized_plugins, 1):
            plugin_name = plugin.get("name", "unknown")
            risk_level = plugin.get("impact", {}).get("risk_level", "medium")
            adapter_changes = "有" if plugin.get("adapter_change_analysis", {}).get("has_adapter_changes") else "无"
            priority_score = plugin.get("priority_score", 0)
            
            script_lines.append(f"    # 插件 {i}: {plugin_name} (优先级: {priority_score:.1f}, 风险: {risk_level}, 适配器变更: {adapter_changes})")
            script_lines.append(f"    log \"INFO\" \"处理插件 {i}/{metadata['total_plugins']}: {plugin_name}\"")
            
            # 根据风险等级决定是否备份
            if self.risk_measures.get(risk_level, {}).get("backup", False):
                script_lines.append(f"    backup_plugin \"{plugin_name}\"")
            
            # 升级插件
            script_lines.append(f"    if ! upgrade_plugin \"{plugin_name}\" \"{risk_level}\" \"{adapter_changes}\"; then")
            script_lines.append(f"        log \"ERROR\" \"插件 {plugin_name} 升级失败\"")
            script_lines.append(f"        fail_count=$((fail_count + 1))")
            script_lines.append(f"        # 根据配置决定是否继续")
            script_lines.append(f"        if [ \"$STOP_ON_ERROR\" = \"true\" ]; then")
            script_lines.append(f"            log \"ERROR\" \"由于错误停止升级流程\"")
            script_lines.append(f"            break")
            script_lines.append(f"        fi")
            script_lines.append(f"    else")
            script_lines.append(f"        success_count=$((success_count + 1))")
            script_lines.append(f"    fi")
            
            # 如果不是最后一个插件，添加延迟
            if i < len(prioritized_plugins):
                delay = self.risk_measures.get(risk_level, {}).get("delay_after_upgrade", self.config["delay_between_upgrades"])
                script_lines.append(f"    ")
                script_lines.append(f"    # 升级后延迟")
                script_lines.append(f"    if [ \"$DRY_RUN\" != \"true\" ]; then")
                script_lines.append(f"        log \"INFO\" \"等待 {delay} 秒...\"")
                script_lines.append(f"        sleep {delay}")
                script_lines.append(f"    fi")
            
            script_lines.append(f"    ")
        
        # 结果汇总
        script_lines.append("    # 结果汇总")
        script_lines.append("    log \"INFO\" \"升级完成: 成功 $success_count, 失败 $fail_count\"")
        script_lines.append("    ")
        script_lines.append("    if [ $fail_count -eq 0 ]; then")
        script_lines.append("        log \"SUCCESS\" \"所有插件升级成功!\"")
        script_lines.append("        exit 0")
        script_lines.append("    else")
        script_lines.append("        log \"WARNING\" \"有 $fail_count 个插件升级失败\"")
        script_lines.append("        exit 1")
        script_lines.append("    fi")
        script_lines.append("}")
        script_lines.append("")
        script_lines.append("# 执行主函数")
        script_lines.append("main \"$@\"")
        
        script_content = "\n".join(script_lines)
        
        # 如果需要，写入文件
        if output_path:
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(script_content)
                os.chmod(output_path, 0o755)  # 赋予执行权限
                metadata["script_path"] = output_path
            except Exception as e:
                return {
                    "success": False,
                    "error": f"脚本写入失败: {e}",
                    "script_content": script_content,
                    "metadata": metadata
                }
        
        return {
            "success": True,
            "script_content": script_content,
            "metadata": metadata
        }
    
    def generate_python_script(self, prioritized_plugins: List[dict], output_path: str = None) -> dict:
        """生成Python升级脚本（替代bash脚本）"""
        # 简化的Python脚本生成，可根据需要扩展
        script_lines = []
        script_lines.append("#!/usr/bin/env python3")
        script_lines.append("\"\"\"")
        script_lines.append("evolution-watcher 半自动升级脚本 (Python版本)")
        script_lines.append("生成时间: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        script_lines.append("\"\"\"")
        script_lines.append("")
        script_lines.append("import subprocess")
        script_lines.append("import time")
        script_lines.append("import sys")
        script_lines.append("import os")
        script_lines.append("")
        script_lines.append("DRY_RUN = " + str(self.config["dry_run"]).lower())
        script_lines.append("")
        script_lines.append("# 插件升级列表（按优先级排序）")
        script_lines.append("PLUGINS_TO_UPGRADE = [")
        for plugin in prioritized_plugins:
            name = plugin.get("name", "unknown")
            risk = plugin.get("impact", {}).get("risk_level", "medium")
            score = plugin.get("priority_score", 0)
            script_lines.append(f"    {{'name': '{name}', 'risk': '{risk}', 'score': {score}}},")
        script_lines.append("]")
        script_lines.append("")
        script_lines.append("def run_command(cmd):")
        script_lines.append("    \"\"\"执行命令\"\"\"")
        script_lines.append("    print(f'执行: {cmd}')")
        script_lines.append("    if DRY_RUN:")
        script_lines.append("        print('[干运行] 跳过实际执行')")
        script_lines.append("        return True")
        script_lines.append("    try:")
        script_lines.append("        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)")
        script_lines.append("        if result.returncode == 0:")
        script_lines.append("            print('成功')")
        script_lines.append("            return True")
        script_lines.append("        else:")
        script_lines.append("            print(f'失败: {result.stderr}')")
        script_lines.append("            return False")
        script_lines.append("    except Exception as e:")
        script_lines.append("        print(f'异常: {e}')")
        script_lines.append("        return False")
        script_lines.append("")
        script_lines.append("def main():")
        script_lines.append("    print('开始升级流程')")
        script_lines.append("    ")
        script_lines.append("    for i, plugin in enumerate(PLUGINS_TO_UPGRADE, 1):")
        script_lines.append("        name = plugin['name']")
        script_lines.append("        risk = plugin['risk']")
        script_lines.append("        print(f'处理插件 {i}/{len(PLUGINS_TO_UPGRADE)}: {name} (风险: {risk})')")
        script_lines.append("        ")
        script_lines.append("        # 执行升级")
        script_lines.append("        success = run_command(f'clawhub update {name}')")
        script_lines.append("        ")
        script_lines.append("        if not success:")
        script_lines.append("            print(f'插件 {name} 升级失败')")
        script_lines.append("            # 根据配置决定是否继续")
        script_lines.append("            break")
        script_lines.append("        ")
        script_lines.append("        # 延迟")
        script_lines.append("        if i < len(PLUGINS_TO_UPGRADE) and not DRY_RUN:")
        script_lines.append("            print('等待30秒...')")
        script_lines.append("            time.sleep(30)")
        script_lines.append("    ")
        script_lines.append("    print('升级流程完成')")
        script_lines.append("")
        script_lines.append("if __name__ == '__main__':")
        script_lines.append("    main()")
        
        script_content = "\n".join(script_lines)
        
        if output_path:
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(script_content)
                os.chmod(output_path, 0o755)
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                    "script_content": script_content
                }
        
        return {
            "success": True,
            "script_content": script_content
        }
    
    def generate_upgrade_report(self, script_result: dict, prioritized_plugins: List[dict]) -> str:
        """生成升级脚本报告"""
        if not script_result.get("success"):
            return "❌ 脚本生成失败: " + script_result.get("error", "未知错误")
        
        report_lines = []
        report_lines.append("## 🚀 半自动升级脚本已生成")
        report_lines.append("")
        report_lines.append("### 📊 升级概览")
        report_lines.append("")
        report_lines.append(f"**总插件数**: {len(prioritized_plugins)}")
        report_lines.append(f"**高风险插件**: {sum(1 for p in prioritized_plugins if p.get('impact', {}).get('risk_level') == 'high')}")
        report_lines.append(f"**中风险插件**: {sum(1 for p in prioritized_plugins if p.get('impact', {}).get('risk_level') == 'medium')}")
        report_lines.append(f"**低风险插件**: {sum(1 for p in prioritized_plugins if p.get('impact', {}).get('risk_level') == 'low')}")
        report_lines.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"**模式**: {'干运行 (预览)' if self.config['dry_run'] else '实际执行'}")
        report_lines.append("")
        
        report_lines.append("### 📋 升级顺序")
        report_lines.append("")
        report_lines.append("| # | 插件 | 优先级分 | 风险等级 | 适配器变更 | 升级建议 |")
        report_lines.append("| - | ---- | -------- | -------- | ---------- | -------- |")
        
        for i, plugin in enumerate(prioritized_plugins, 1):
            name = plugin.get("name", "unknown")
            priority_score = plugin.get("priority_score", 0)
            risk_level = plugin.get("impact", {}).get("risk_level", "unknown")
            adapter_changes = "有" if plugin.get("adapter_change_analysis", {}).get("has_adapter_changes") else "无"
            recommendation = plugin.get("priority_recommendation", "")
            
            risk_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(risk_level, "⚪")
            
            report_lines.append(
                f"| {i} | **{name}** | {priority_score:.1f} | {risk_emoji} {risk_level} | "
                f"{adapter_changes} | {recommendation} |"
            )
        
        report_lines.append("")
        
        report_lines.append("### ⚙️ 安全措施")
        report_lines.append("")
        report_lines.append("| 风险等级 | 升级前测试 | 备份 | 回滚计划 | 升级后验证 | 延迟(秒) |")
        report_lines.append("| -------- | ---------- | ---- | -------- | ---------- | -------- |")
        
        for risk_level, measures in self.risk_measures.items():
            test = "✅" if measures.get("pre_upgrade_test") else "❌"
            backup = "✅" if measures.get("backup") else "❌"
            rollback = "✅" if measures.get("rollback_plan") else "❌"
            verify = "✅" if measures.get("verify_after_upgrade") else "❌"
            delay = measures.get("delay_after_upgrade", 0)
            
            risk_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(risk_level, "⚪")
            report_lines.append(f"| {risk_emoji} {risk_level} | {test} | {backup} | {rollback} | {verify} | {delay} |")
        
        report_lines.append("")
        
        report_lines.append("### 📝 脚本信息")
        report_lines.append("")
        if script_result.get("metadata", {}).get("script_path"):
            report_lines.append(f"**脚本路径**: `{script_result['metadata']['script_path']}`")
            report_lines.append(f"**执行权限**: 已赋予 (755)")
        else:
            report_lines.append("**脚本路径**: 未保存到文件（仅内存中）")
        
        report_lines.append(f"**脚本类型**: Bash + Python双版本")
        report_lines.append(f"**包含回滚**: {'✅ 是' if self.config['include_rollback'] else '❌ 否'}")
        report_lines.append(f"**批量大小**: {self.config['batch_size']}")
        report_lines.append("")
        
        report_lines.append("### 🚦 执行说明")
        report_lines.append("")
        report_lines.append("1. **干运行模式**: 默认启用，仅预览升级步骤，不实际执行")
        report_lines.append("2. **实际执行**: 设置 `DRY_RUN=false` 或修改配置中的 `dry_run` 参数")
        report_lines.append("3. **手动验证**: 建议先在高风险插件上手动验证升级步骤")
        report_lines.append("4. **回滚准备**: 确保有备份或回滚计划，特别是高风险插件")
        report_lines.append("5. **环境准备**: 确保 ClawHub CLI 已安装并配置正确")
        report_lines.append("")
        report_lines.append("### 💡 使用示例")
        report_lines.append("")
        report_lines.append("```bash")
        report_lines.append("# 查看脚本内容")
        report_lines.append("cat upgrade_script.sh")
        report_lines.append("")
        report_lines.append("# 干运行模式（默认）")
        report_lines.append("./upgrade_script.sh")
        report_lines.append("")
        report_lines.append("# 实际执行模式")
        report_lines.append("DRY_RUN=false ./upgrade_script.sh")
        report_lines.append("```")
        
        return "\n".join(report_lines)


class ClawHubMonitor:
    """ClawHub 插件监控器"""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or skill_dir / "config" / "monitor_sources.json"
        self.config = self.load_config()
        self.plugins = []  # 插件列表
        self.updates = []  # 更新检测结果
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 影响评估器
        self.impact_assessor = ImpactAssessor()
        
        # 变更日志解析器
        self.changelog_parser = ChangelogParser()
        
        # 依赖关系分析器
        self.dependency_analyzer = DependencyAnalyzer()
        
        # 升级优先级计算器
        self.priority_calculator = PriorityCalculator()
        
        # 适配器变更检测器
        self.adapter_change_detector = AdapterChangeDetector()
        
        # 半自动升级脚本生成器
        self.upgrade_script_generator = UpgradeScriptGenerator()
        
        # 适配器自动修复器（第二阶段）
        self.adapter_auto_fixer = AdapterAutoFixer() if AdapterAutoFixer else None
        
        # 确保报告目录存在
        self.report_dir = skill_dir / self.config["report"]["output_dir"]
        self.report_dir.mkdir(parents=True, exist_ok=True)
    
    def load_config(self) -> dict:
        """加载配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️  配置文件不存在: {self.config_path}")
            return self.default_config()
        except json.JSONDecodeError as e:
            print(f"❌ 配置文件 JSON 解析错误: {e}")
            return self.default_config()
    
    def default_config(self) -> dict:
        """默认配置"""
        return {
            "clawhub": {"enabled": True, "check_frequency_hours": 24},
            "report": {"output_dir": "reports", "keep_reports_days": 30}
        }
    
    def run_clawhub_command(self, command: List[str]) -> Tuple[bool, str]:
        """执行 ClawHub CLI 命令"""
        try:
            result = subprocess.run(
                ["clawhub"] + command,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode == 0, result.stdout.strip()
        except subprocess.TimeoutExpired:
            return False, "命令执行超时"
        except FileNotFoundError:
            return False, "clawhub 命令未找到，请确保已安装 ClawHub CLI"
        except Exception as e:
            return False, f"命令执行异常: {e}"
    
    def get_installed_plugins(self) -> List[Dict]:
        """获取已安装插件列表"""
        success, output = self.run_clawhub_command(["list"])
        if not success:
            print(f"❌ 无法获取已安装插件: {output}")
            return []
        
        plugins = []
        for line in output.split('\n'):
            line = line.strip()
            if not line or ' ' not in line:
                continue
            
            # 解析 "plugin_name version" 格式
            parts = line.split()
            if len(parts) >= 2:
                plugin_name = parts[0]
                current_version = parts[1]
                
                plugins.append({
                    "name": plugin_name,
                    "current_version": current_version,
                    "latest_version": None,
                    "needs_update": False,
                    "last_checked": self.timestamp
                })
        
        return plugins
    
    def get_latest_version(self, plugin_name: str) -> Tuple[bool, Optional[str]]:
        """获取插件最新版本"""
        success, output = self.run_clawhub_command(["inspect", plugin_name])
        if not success:
            return False, None
        
        # 解析输出，查找 "Latest:" 行
        for line in output.split('\n'):
            line = line.strip()
            if line.startswith("Latest:"):
                version = line.split(":", 1)[1].strip()
                return True, version
        
        return False, None
    
    def get_plugin_path(self, plugin_name: str) -> str:
        """获取插件目录路径"""
        # 假设插件安装在 workspace/skills/ 目录下
        base_path = Path("/root/.openclaw/workspace/skills")
        plugin_path = base_path / plugin_name
        
        # 检查路径是否存在
        if plugin_path.exists() and plugin_path.is_dir():
            return str(plugin_path)
        
        # 回退：检查技能目录
        skill_path = Path(__file__).parent.parent / plugin_name
        if skill_path.exists():
            return str(skill_path)
        
        # 如果都不存在，返回默认路径（可能插件未本地安装）
        return str(plugin_path)
    
    def check_updates(self) -> List[Dict]:
        """检查插件更新"""
        print("🔄 开始检查插件更新...")
        
        self.plugins = self.get_installed_plugins()
        if not self.plugins:
            print("❌ 未发现已安装插件")
            return []
        
        print(f"📦 发现 {len(self.plugins)} 个已安装插件")
        
        updates = []
        # 测试模式检测
        test_mode = os.getenv("EVOLUTION_WATCHER_TEST") == "true"
        if test_mode:
            print("🧪 测试模式已启用 - 模拟 self-improving 插件更新 (1.2.15 → 1.2.16)")
        
        for plugin in self.plugins:
            # 测试模式：模拟 self-improving 插件需要更新
            if test_mode and plugin['name'] == 'self-improving':
                original_version = plugin['current_version']
                plugin['current_version'] = '1.2.15'  # 模拟旧版本
                print(f"  检查插件: {plugin['name']} ({original_version} → {plugin['current_version']}) [测试模式]...", end='', flush=True)
            else:
                print(f"  检查插件: {plugin['name']} ({plugin['current_version']})...", end='', flush=True)
            
            success, latest_version = self.get_latest_version(plugin['name'])
            if not success:
                print(f" ❌ 获取最新版本失败")
                plugin["error"] = "无法获取最新版本"
                updates.append(plugin)
                continue
            
            plugin["latest_version"] = latest_version
            plugin["needs_update"] = latest_version != plugin["current_version"]
            
            if plugin["needs_update"]:
                print(f" ⚠️  发现新版本: {latest_version}")
                # 进行影响评估
                impact = self.impact_assessor.assess_impact(
                    plugin['name'],
                    plugin['current_version'],
                    plugin['latest_version']
                )
                plugin["impact"] = impact
                
                # 尝试获取变更日志
                plugin_path = self.get_plugin_path(plugin['name'])
                changelog = self.changelog_parser.get_changelog_for_version(
                    plugin_path,
                    plugin['latest_version']
                )
                plugin["changelog"] = changelog
                
                # 如果找到破坏性变更，更新风险等级
                if changelog.get("available") and changelog.get("exact_match"):
                    # 变更日志分类分析
                    changelog_analysis = self.changelog_parser.categorize_changes(
                        changelog.get("content", "")
                    )
                    plugin["changelog_analysis"] = changelog_analysis
                    
                    # 适配器变更检测（使用增强的分类分析）
                    adapter_change_analysis = self.adapter_change_detector.detect_adapter_changes(
                        plugin['name'],
                        changelog.get("content", ""),
                        plugin.get("impact", {}).get("change_type", "patch"),
                        changelog_analysis  # 传递分类分析结果
                    )
                    plugin["adapter_change_analysis"] = adapter_change_analysis
                    
                    # 如果适配器变更风险高，提升整体风险等级
                    if adapter_change_analysis.get("risk_level") == "high" and plugin["impact"]["risk_level"] != "high":
                        plugin["impact"]["risk_level"] = "high"
                        plugin["impact"]["factors"].append("适配器变更风险高")
                        plugin["impact"]["recommendation"] = (
                            "⚠️ **高风险**: 适配器变更可能影响星型架构连接，请详细测试适配器兼容性。"
                        )
                    
                    # 适配器自动修复分析（第二阶段）
                    if self.adapter_auto_fixer and changelog.get("content"):
                        try:
                            auto_fix_result = self.adapter_auto_fixer.analyze_plugin_update(
                                plugin['name'],
                                plugin['current_version'],
                                plugin['latest_version'],
                                changelog.get("content", "")
                            )
                            plugin["auto_fix_analysis"] = auto_fix_result
                            if auto_fix_result.get("has_changes"):
                                print(f"   🔧 检测到适配器修复建议: {auto_fix_result['proposal_count']} 个")
                        except Exception as e:
                            print(f"⚠️  适配器自动修复分析失败 {plugin['name']}: {e}")
                            plugin["auto_fix_analysis"] = {"error": str(e)}
                    
                    # 生成升级脚本建议
                    upgrade_suggestions = self.changelog_parser.generate_upgrade_script_suggestions(
                        changelog_analysis, plugin['name']
                    )
                    plugin["upgrade_suggestions"] = upgrade_suggestions
                    
                    # 依赖关系分析
                    try:
                        dependency_analysis = self.dependency_analyzer.analyze_impact(plugin['name'])
                        plugin["dependency_analysis"] = dependency_analysis
                    except Exception as e:
                        print(f"⚠️  依赖关系分析失败 {plugin['name']}: {e}")
                        plugin["dependency_analysis"] = {"error": str(e)}
                    
                    breaking_changes = self.changelog_parser.extract_breaking_changes(
                        changelog.get("content", "")
                    )
                    if breaking_changes:
                        plugin["breaking_changes"] = breaking_changes
                        # 提升风险等级
                        if plugin["impact"]["risk_level"] != "high":
                            plugin["impact"]["risk_level"] = "high"
                            plugin["impact"]["factors"].append("变更日志中包含破坏性变更")
                            plugin["impact"]["recommendation"] = (
                                "⚠️ **高风险**: 变更日志中包含破坏性变更，强烈建议在测试环境中充分验证后再升级。"
                            )
            else:
                print(f" ✅ 已是最新")
            
            updates.append(plugin)
        
        self.updates = updates
        return updates
    
    def generate_console_report(self) -> str:
        """生成控制台报告"""
        if not self.updates:
            return "⚠️  没有插件更新信息"
        
        # 统计信息
        total = len(self.updates)
        up_to_date = sum(1 for p in self.updates if not p["needs_update"])
        outdated = sum(1 for p in self.updates if p["needs_update"])
        
        report_lines = []
        report_lines.append("🔄 evolution-watcher v0.6.0")
        report_lines.append(f"📅 检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"📊 监控源: ClawHub (已安装 {total} 个插件)")
        report_lines.append("")
        
        if outdated > 0:
            report_lines.append(f"📈 发现 {outdated} 个插件可升级:")
            for plugin in self.updates:
                if plugin["needs_update"]:
                    risk_emoji = {
                        "high": "🔴",
                        "medium": "🟡",
                        "low": "🟢"
                    }.get(plugin.get("impact", {}).get("risk_level", "medium"), "🟡")
                    
                    risk_level = plugin.get("impact", {}).get("risk_level", "unknown")
                    change_type = plugin.get("impact", {}).get("change_type", "unknown")
                    
                    # 变更日志指示器
                    changelog_emoji = "📋" if plugin.get("changelog", {}).get("available") else ""
                    
                    report_lines.append(
                        f"   • {risk_emoji} {plugin['name']}: {plugin['current_version']} → {plugin['latest_version']} "
                        f"({change_type}, 风险: {risk_level}) {changelog_emoji}"
                    )
        else:
            report_lines.append("🎉 所有插件均为最新版本!")
        
        report_lines.append("")
        report_lines.append("📋 详细对比:")
        
        # 简单表格
        table_header = "┌──────────────────────┬────────────┬────────────┬──────────┐"
        table_footer = "└──────────────────────┴────────────┴────────────┴──────────┘"
        
        report_lines.append(table_header)
        report_lines.append("│ 插件                 │ 当前版本   │ 最新版本   │ 状态     │")
        report_lines.append("├──────────────────────┼────────────┼────────────┼──────────┤")
        
        for plugin in self.updates:
            name = plugin["name"][:20].ljust(20)
            current = plugin["current_version"][:10].ljust(10)
            latest = plugin["latest_version"][:10].ljust(10) if plugin["latest_version"] else "N/A".ljust(10)
            
            if plugin.get("error"):
                status = "❌ 错误".ljust(8)
            elif plugin["needs_update"]:
                status = "⚠️ 可升级".ljust(8)
            else:
                status = "✅ 最新".ljust(8)
            
            report_lines.append(f"│ {name} │ {current} │ {latest} │ {status} │")
        
        report_lines.append(table_footer)
        
        return "\n".join(report_lines)
    
    def generate_markdown_report(self) -> str:
        """生成 Markdown 格式报告"""
        if not self.updates:
            return "# 插件更新报告\n\n没有插件更新信息。"
        
        total = len(self.updates)
        outdated = sum(1 for p in self.updates if p["needs_update"])
        
        report_lines = []
        report_lines.append(f"# 插件更新报告")
        report_lines.append("")
        report_lines.append(f"**检查时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"**监控源**: ClawHub")
        report_lines.append(f"**已安装插件**: {total} 个")
        report_lines.append(f"**可升级插件**: {outdated} 个")
        report_lines.append("")
        
        if outdated > 0:
            report_lines.append("## 📦 可升级插件")
            report_lines.append("")
            report_lines.append("| 插件 | 当前版本 | 最新版本 | 变更类型 | 风险等级 |")
            report_lines.append("|------|----------|----------|----------|----------|")
            
            for plugin in self.updates:
                if plugin["needs_update"]:
                    impact = plugin.get("impact", {})
                    change_type = impact.get("change_type", "unknown")
                    risk_level = impact.get("risk_level", "medium")
                    
                    # 风险等级表情符号
                    risk_emoji = {
                        "high": "🔴",
                        "medium": "🟡",
                        "low": "🟢"
                    }.get(risk_level, "🟡")
                    
                    report_lines.append(
                        f"| {plugin['name']} | {plugin['current_version']} | {plugin['latest_version']} | "
                        f"{change_type} | {risk_emoji} {risk_level} |"
                    )
            
            report_lines.append("")
            # 添加升级优先级矩阵
            prioritized_plugins = self.priority_calculator.calculate_priorities(self.updates)
            if prioritized_plugins:
                priority_report = self.priority_calculator.generate_priority_report(prioritized_plugins)
                report_lines.append(priority_report)
                report_lines.append("")
            report_lines.append("## 🚀 升级建议")
            report_lines.append("")
            report_lines.append("```bash")
            for plugin in self.updates:
                if plugin["needs_update"]:
                    report_lines.append(f"clawhub update {plugin['name']}")
            report_lines.append("```")
            report_lines.append("")
            report_lines.append("## ⚠️ 影响评估")
            report_lines.append("")
            for plugin in self.updates:
                if plugin["needs_update"]:
                    impact = plugin.get("impact", {})
                    changelog = plugin.get("changelog", {})
                    
                    report_lines.append(f"### {plugin['name']}")
                    report_lines.append("")
                    report_lines.append(f"**风险评估**: {impact.get('risk_level', 'unknown')}")
                    report_lines.append("")
                    report_lines.append(f"**建议**: {impact.get('recommendation', '无建议')}")
                    report_lines.append("")
                    report_lines.append("**评估因素**:")
                    for factor in impact.get('factors', []):
                        report_lines.append(f"- {factor}")
                    
                    # 变更日志信息
                    if changelog.get("available"):
                        report_lines.append("")
                        report_lines.append("**变更日志**:")
                        if changelog.get("exact_match"):
                            report_lines.append("")
                            report_lines.append("```markdown")
                            # 截断长内容
                            content = changelog.get("content", "")
                            if len(content) > 1000:
                                content = content[:1000] + "\n... (内容过长，已截断)"
                            report_lines.append(content)
                            report_lines.append("```")
                            
                            # 破坏性变更
                            breaking_changes = plugin.get("breaking_changes", [])
                            if breaking_changes:
                                report_lines.append("")
                                report_lines.append("**破坏性变更**:")
                                for bc in breaking_changes:
                                    report_lines.append(f"- ⚠️ {bc}")
                            
                            # 变更分类分析
                            changelog_analysis = plugin.get("changelog_analysis")
                            if changelog_analysis:
                                report_lines.append("")
                                report_lines.append("**变更分类**:")
                                report_lines.append("")
                                # 显示分类统计
                                category_counts = changelog_analysis.get("category_counts", {})
                                if category_counts:
                                    for cat, count in category_counts.items():
                                        if count > 0:
                                            emoji = {
                                                "added": "🟢",
                                                "changed": "🟡", 
                                                "fixed": "🔵",
                                                "removed": "🔴",
                                                "deprecated": "🟠",
                                                "security": "🔴",
                                                "uncategorized": "⚪"
                                            }.get(cat, "⚪")
                                            report_lines.append(f"{emoji} **{cat}**: {count} 项")
                                    
                                    report_lines.append("")
                                    report_lines.append(f"**影响分数**: {changelog_analysis.get('impact_score', 0)}")
                                    report_lines.append(f"**破坏性分数**: {changelog_analysis.get('destructive_score', 0)}")
                                    report_lines.append(f"**总变更数**: {changelog_analysis.get('total_changes', 0)}")
                                
                                # 升级脚本建议
                                upgrade_suggestions = plugin.get("upgrade_suggestions", [])
                                if upgrade_suggestions:
                                    report_lines.append("")
                                    report_lines.append("**升级脚本建议**:")
                                    report_lines.append("")
                                    report_lines.append("```bash")
                                    for line in upgrade_suggestions:
                                        report_lines.append(line)
                                    report_lines.append("```")
                                
                                # 依赖关系分析
                                dependency_analysis = plugin.get("dependency_analysis")
                                if dependency_analysis and "error" not in dependency_analysis:
                                    report_lines.append("")
                                    report_lines.append("**依赖关系分析**:")
                                    report_lines.append("")
                                    report_lines.append(f"**直接影响分数**: {dependency_analysis.get('impact_score', 0)}")
                                    report_lines.append(f"**依赖风险等级**: {dependency_analysis.get('risk_level', 'unknown')}")
                                    report_lines.append(f"**下游依赖插件数**: {dependency_analysis.get('downstream_count', 0)}")
                                    report_lines.append("")
                                    report_lines.append("**直接下游依赖**:")
                                    dependents = dependency_analysis.get('direct_dependents', [])
                                    if dependents:
                                        for dep in dependents:
                                            report_lines.append(f"- {dep}")
                                    else:
                                        report_lines.append("无直接下游依赖")
                                    report_lines.append("")
                                    # 适配器连接
                                    adapter_connections = dependency_analysis.get('adapter_connections', [])
                                    if adapter_connections:
                                        active_count = dependency_analysis.get('active_adapter_count', 0)
                                        report_lines.append("**适配器连接**:")
                                        report_lines.append("")
                                        report_lines.append(f"活动适配器: {active_count}/{len(adapter_connections)}")
                                        report_lines.append("")
                                        for conn in adapter_connections:
                                            status_emoji = {"active": "🟢", "pending": "🟡", "planned": "🟠", "disabled": "🔴"}.get(conn["status"], "⚪")
                                            weight_indicator = "✓" if conn["weight"] > 0 else "✗"
                                            report_lines.append(f"- {status_emoji} {conn['adapter_id']} → {conn['connected_plugin']} ({conn['status']}) {weight_indicator}")
                                    report_lines.append("")
                                    report_lines.append("**升级建议**:")
                                    report_lines.append(dependency_analysis.get('recommendation', '无建议'))
                                    
                                    # 适配器变更分析
                                    adapter_change_analysis = plugin.get("adapter_change_analysis")
                                    if adapter_change_analysis:
                                        report_lines.append("")
                                        report_lines.append("**适配器变更分析**:")
                                        report_lines.append("")
                                        report_lines.append(f"**检测结果**: {'检测到适配器变更' if adapter_change_analysis.get('has_adapter_changes') else '未检测到适配器变更'}")
                                        if adapter_change_analysis.get("has_adapter_changes"):
                                            change_type_display = {
                                                "interface_change": "接口变更",
                                                "api_change": "API变更",
                                                "dependency_change": "依赖变更"
                                            }.get(adapter_change_analysis.get("adapter_change_type"), adapter_change_analysis.get("adapter_change_type"))
                                            risk_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(adapter_change_analysis.get("risk_level"), "⚪")
                                            report_lines.append(f"**变更类型**: {change_type_display}")
                                            report_lines.append(f"**风险等级**: {risk_emoji} {adapter_change_analysis.get('risk_level')}")
                                            report_lines.append("")
                                            affected_adapters = adapter_change_analysis.get("affected_adapters", [])
                                            if affected_adapters:
                                                report_lines.append("**受影响适配器**:")
                                                for adapter_id in affected_adapters[:3]:
                                                    report_lines.append(f"- `{adapter_id}`")
                                                if len(affected_adapters) > 3:
                                                    report_lines.append(f"- ... 共 {len(affected_adapters)} 个适配器")
                                                report_lines.append("")
                                            affected_plugins = adapter_change_analysis.get("affected_plugins", [])
                                            if affected_plugins:
                                                report_lines.append("**受影响插件**:")
                                                for plugin_name in affected_plugins[:3]:
                                                    report_lines.append(f"- `{plugin_name}`")
                                                if len(affected_plugins) > 3:
                                                    report_lines.append(f"- ... 共 {len(affected_plugins)} 个插件")
                                                report_lines.append("")
                                            breaking_changes = adapter_change_analysis.get("breaking_changes", [])
                                            if breaking_changes:
                                                report_lines.append("**破坏性变更**:")
                                                for bc in breaking_changes[:2]:
                                                    report_lines.append(f"- ⚠️ {bc}")
                                                if len(breaking_changes) > 2:
                                                    report_lines.append(f"- ... 共 {len(breaking_changes)} 个破坏性变更")
                                                report_lines.append("")
                                            report_lines.append(f"**建议**: {adapter_change_analysis.get('recommendation', '无建议')}")
                                elif dependency_analysis and "error" in dependency_analysis:
                                    report_lines.append("")
                                    report_lines.append("**依赖关系分析**: 无法分析（插件可能不在星型架构注册表中）")
                        else:
                            report_lines.append(f"⚠️ 未找到版本 {plugin['latest_version']} 的精确变更日志。")
                            if changelog.get("available_versions"):
                                report_lines.append(f"可用版本: {', '.join(changelog.get('available_versions', []))}")
                    else:
                        report_lines.append("")
                        report_lines.append("**变更日志**: 未找到变更日志文件。")
                    
                    report_lines.append("")
            
            # 适配器自动修复建议（第二阶段）
            auto_fix_analysis = plugin.get("auto_fix_analysis")
            if auto_fix_analysis and auto_fix_analysis.get("has_changes"):
                report_lines.append("")
                report_lines.append("## 🔧 适配器自动修复建议")
                report_lines.append("")
                report_lines.append(auto_fix_analysis.get("report", "无详细报告"))
                report_lines.append("")
            
            report_lines.append("> ⚠️ **重要**: 升级前请确认变更日志，建议在测试环境中先行验证。")
        
            # 生成半自动升级脚本
            prioritized_plugins = self.priority_calculator.calculate_priorities(self.updates)
            if prioritized_plugins:
                script_result = self.upgrade_script_generator.generate_upgrade_script(prioritized_plugins)
                upgrade_report = self.upgrade_script_generator.generate_upgrade_report(script_result, prioritized_plugins)
                report_lines.append(upgrade_report)
                report_lines.append("")
        
        report_lines.append("")
        report_lines.append("## 📊 完整状态")
        report_lines.append("")
        report_lines.append("| 插件 | 当前版本 | 最新版本 | 状态 |")
        report_lines.append("|------|----------|----------|------|")
        
        for plugin in self.updates:
            if plugin.get("error"):
                status = "错误"
                latest = "N/A"
            elif plugin["needs_update"]:
                status = "可升级"
                latest = plugin["latest_version"]
            else:
                status = "最新"
                latest = plugin["latest_version"]
            
            report_lines.append(
                f"| {plugin['name']} | {plugin['current_version']} | {latest} | {status} |"
            )
        
        return "\n".join(report_lines)
    
    def save_reports(self):
        """保存报告文件"""
        # 控制台报告
        console_report = self.generate_console_report()
        print("\n" + console_report)
        
        # Markdown 报告
        md_report = self.generate_markdown_report()
        md_file = self.report_dir / f"updates_{self.timestamp}.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(md_report)
        print(f"📋 Markdown 报告已保存: {md_file}")
        
        # JSON 日志
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "check_id": self.timestamp,
            "total_plugins": len(self.updates),
            "outdated_plugins": sum(1 for p in self.updates if p["needs_update"]),
            "plugins": self.updates
        }
        
        log_file = self.report_dir / "updates_log.json"
        log_data = []
        
        # 读取现有日志（如果有）
        if log_file.exists():
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    log_data = json.load(f)
            except json.JSONDecodeError:
                log_data = []
        
        # 添加新条目
        log_data.append(log_entry)
        
        # 保持最近 N 天记录
        keep_days = self.config["report"].get("keep_reports_days", 30)
        cutoff_date = datetime.now() - timedelta(days=keep_days)
        
        filtered_logs = []
        for entry in log_data:
            entry_date = datetime.fromisoformat(entry["timestamp"].replace('Z', '+00:00'))
            if entry_date > cutoff_date:
                filtered_logs.append(entry)
        
        # 保存日志
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(filtered_logs, f, indent=2, ensure_ascii=False)
        
        print(f"📝 监控日志已更新: {log_file}")
        
        # 保存摘要
        summary_file = self.report_dir / "summary.json"
        summary = {
            "last_check": datetime.now().isoformat(),
            "total_plugins": len(self.updates),
            "outdated_plugins": sum(1 for p in self.updates if p["needs_update"]),
            "check_id": self.timestamp
        }
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
    
    def cleanup_old_reports(self):
        """清理旧报告文件"""
        keep_days = self.config["report"].get("keep_reports_days", 30)
        cutoff_date = datetime.now() - timedelta(days=keep_days)
        
        for report_file in self.report_dir.glob("updates_*.md"):
            # 从文件名解析日期
            try:
                # updates_20260317_220000.md
                date_str = report_file.stem.split('_')[1]
                file_date = datetime.strptime(date_str, "%Y%m%d")
                
                if file_date.date() < cutoff_date.date():
                    report_file.unlink()
                    print(f"🧹 清理旧报告: {report_file.name}")
            except (ValueError, IndexError):
                pass
    
    def run(self):
        """执行完整监控流程"""
        print("=" * 60)
        print("🦞 evolution-watcher MVP v0.6.0")
        print("=" * 60)
        
        if not self.config["clawhub"]["enabled"]:
            print("❌ ClawHub 监控已禁用，请检查配置文件")
            return
        
        # 检查更新
        updates = self.check_updates()
        if not updates:
            print("❌ 更新检查失败或无插件数据")
            return
        
        # 生成并保存报告
        self.save_reports()
        
        # 清理旧报告
        self.cleanup_old_reports()
        
        print("=" * 60)
        print("✅ 监控任务完成")
        print("=" * 60)

def main():
    parser = argparse.ArgumentParser(description="evolution-watcher 监控脚本")
    parser.add_argument("--config", help="配置文件路径")
    parser.add_argument("--report-only", action="store_true", help="仅生成报告，不检查更新")
    parser.add_argument("--force", action="store_true", help="强制运行，忽略频率限制")
    
    args = parser.parse_args()
    
    monitor = ClawHubMonitor(args.config)
    monitor.run()

if __name__ == "__main__":
    main()