#!/usr/bin/env python3
"""
适配器自动修复模块 - evolution-watcher 第二阶段

功能：
1. 适配器变更精确定位
2. 修复模板库管理
3. diff生成与展示
4. 安全应用与验证

第一阶段：基础框架，支持 memory-sync-enhanced 和 self-improving 适配器试点
"""

import os
import sys
import json
import yaml
import re
import difflib
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)

# ============================================================================
# 数据结构定义
# ============================================================================

class ChangeType(Enum):
    """变更类型枚举"""
    FUNCTION_RENAME = "function_rename"
    PARAMETER_ADD = "parameter_add"
    PARAMETER_REMOVE = "parameter_remove"
    PARAMETER_RENAME = "parameter_rename"
    CONFIG_KEY_CHANGE = "config_key_change"
    IMPORT_PATH_CHANGE = "import_path_change"
    RETURN_TYPE_CHANGE = "return_type_change"
    CLASS_RENAME = "class_rename"
    METHOD_SIGNATURE_CHANGE = "method_signature_change"
    UNKNOWN = "unknown"


@dataclass
class ChangeLocation:
    """变更位置信息"""
    file_path: Path
    line_start: int
    line_end: int
    old_content: str
    new_content: str
    change_type: ChangeType
    confidence: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FixTemplate:
    """修复模板"""
    template_id: str
    name: str
    description: str
    detection_patterns: List[Dict[str, Any]]
    extraction_rules: List[Dict[str, Any]]
    fix_action: Dict[str, Any]
    risk_level: str
    confidence: float = 0.0


@dataclass
class DetectedChange:
    """检测到的变更"""
    change_id: str
    plugin_name: str
    old_version: str
    new_version: str
    change_type: ChangeType
    locations: List[ChangeLocation]
    affected_adapters: List[str]
    fix_template: Optional[FixTemplate] = None
    extraction_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FixProposal:
    """修复建议"""
    proposal_id: str
    detected_change: DetectedChange
    diff_content: str
    affected_files: List[Path]
    risk_level: str
    confidence: float
    apply_command: str = ""
    backup_path: Optional[Path] = None


# ============================================================================
# 修复模板库管理
# ============================================================================

class FixTemplateLibrary:
    """修复模板库管理"""
    
    def __init__(self, templates_path: Optional[Path] = None):
        """初始化模板库
        
        Args:
            templates_path: 模板文件路径，默认使用 config/fix_templates.yaml
        """
        if templates_path is None:
            base_dir = Path(__file__).parent.parent
            self.templates_path = base_dir / "config" / "fix_templates.yaml"
        else:
            self.templates_path = Path(templates_path)
        
        self.templates: Dict[str, FixTemplate] = {}
        self.load_templates()
    
    def load_templates(self) -> bool:
        """加载模板文件"""
        try:
            if not self.templates_path.exists():
                logger.warning(f"模板文件不存在: {self.templates_path}")
                return False
            
            with open(self.templates_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            self.templates.clear()
            
            for template_data in data.get("templates", []):
                template = FixTemplate(
                    template_id=template_data.get("id", ""),
                    name=template_data.get("name", ""),
                    description=template_data.get("description", ""),
                    detection_patterns=template_data.get("detection_patterns", []),
                    extraction_rules=template_data.get("extraction", []),
                    fix_action=template_data.get("fix_action", {}),
                    risk_level=template_data.get("risk_level", "medium"),
                    confidence=template_data.get("confidence", 0.0)
                )
                self.templates[template.template_id] = template
            
            logger.info(f"加载了 {len(self.templates)} 个修复模板")
            return True
            
        except Exception as e:
            logger.error(f"加载模板文件失败: {e}")
            return False
    
    def match_template(self, changelog_content: str, diff_content: Optional[str] = None) -> List[FixTemplate]:
        """匹配变更内容到修复模板
        
        Args:
            changelog_content: 变更日志内容
            diff_content: 代码差异内容（可选）
        
        Returns:
            匹配的模板列表
        """
        matched_templates = []
        
        for template in self.templates.values():
            if self._check_template_match(template, changelog_content, diff_content):
                matched_templates.append(template)
        
        # 按置信度排序
        matched_templates.sort(key=lambda t: t.confidence, reverse=True)
        return matched_templates
    
    def _check_template_match(self, template: FixTemplate, changelog_content: str, diff_content: Optional[str]) -> bool:
        """检查模板是否匹配"""
        changelog_lower = changelog_content.lower()
        
        for pattern_info in template.detection_patterns:
            pattern_type = pattern_info.get("type", "")
            patterns = pattern_info.get("patterns", [])
            
            if pattern_type == "changelog_keyword":
                # 检查变更日志中的关键词
                for pattern in patterns:
                    if pattern.lower() in changelog_lower:
                        return True
            
            elif pattern_type == "diff_pattern" and diff_content:
                # 检查差异内容中的模式
                for pattern in patterns:
                    if re.search(pattern, diff_content):
                        return True
        
        return False
    
    def extract_change_data(self, template: FixTemplate, changelog_content: str) -> Dict[str, Any]:
        """从变更日志中提取变更数据
        
        Args:
            template: 修复模板
            changelog_content: 变更日志内容
        
        Returns:
            提取的变更数据字典
        """
        extraction_data = {}
        
        for extraction_rule in template.extraction_rules:
            source = extraction_rule.get("source", "changelog")
            regex_pattern = extraction_rule.get("regex", "")
            groups = extraction_rule.get("groups", [])
            
            if source == "changelog" and regex_pattern:
                match = re.search(regex_pattern, changelog_content, re.IGNORECASE)
                if match:
                    for i, group_name in enumerate(groups):
                        if i + 1 <= len(match.groups()):
                            extraction_data[group_name] = match.group(i + 1)
        
        return extraction_data


# ============================================================================
# 适配器变更精确定位
# ============================================================================

class AdapterChangeLocator:
    """适配器变更精确定位器"""
    
    def __init__(self, template_library: Optional[FixTemplateLibrary] = None):
        """初始化定位器
        
        Args:
            template_library: 修复模板库实例，如果为None则创建默认实例
        """
        self.template_library = template_library or FixTemplateLibrary()
        self.registry_cache = None
    
    def locate_adapter_changes(self, plugin_name: str, old_version: str, new_version: str, 
                              changelog_content: str) -> List[DetectedChange]:
        """定位适配器相关变更
        
        Args:
            plugin_name: 插件名称
            old_version: 旧版本
            new_version: 新版本
            changelog_content: 变更日志内容
        
        Returns:
            检测到的变更列表
        """
        logger.info(f"开始定位 {plugin_name} ({old_version} → {new_version}) 的适配器变更")
        
        # 1. 匹配修复模板
        matched_templates = self.template_library.match_template(changelog_content)
        
        if not matched_templates:
            logger.info(f"未找到匹配的修复模板: {plugin_name}")
            return []
        
        # 2. 提取变更数据
        detected_changes = []
        
        for template in matched_templates:
            extraction_data = self.template_library.extract_change_data(template, changelog_content)
            
            if not extraction_data:
                logger.debug(f"模板 {template.template_id} 未提取到变更数据")
                continue
            
            # 3. 查找受影响的适配器
            affected_adapters = self._find_affected_adapters(plugin_name, template)
            
            # 4. 创建检测到的变更对象
            change = DetectedChange(
                change_id=f"{plugin_name}_{template.template_id}_{old_version}_{new_version}",
                plugin_name=plugin_name,
                old_version=old_version,
                new_version=new_version,
                change_type=ChangeType(template.template_id),
                locations=[],  # 第一阶段暂不实现具体位置定位
                affected_adapters=affected_adapters,
                fix_template=template,
                extraction_data=extraction_data
            )
            
            detected_changes.append(change)
            logger.info(f"检测到变更: {template.name} ({template.template_id}), 影响适配器: {affected_adapters}")
        
        return detected_changes
    
    def _find_affected_adapters(self, plugin_name: str, template: FixTemplate) -> List[str]:
        """查找受影响的适配器
        
        第一阶段简化实现：基于插件名称和变更类型推断
        
        Args:
            plugin_name: 插件名称
            template: 修复模板
        
        Returns:
            受影响的适配器名称列表
        """
        # 简化逻辑：根据插件名称推断适配器
        affected_adapters = []
        
        # memory-sync-enhanced 相关的适配器
        if plugin_name == "memory-sync-enhanced":
            affected_adapters = [
                "self_improving_adapter",
                "msp_adapter", 
                "unified_memory_adapter",
                "xiaolongxia_adapter"
            ]
        
        # self-improving 相关的适配器
        elif plugin_name == "self-improving":
            affected_adapters = [
                "self_improving_adapter",
                "memory_sync_enhanced_adapter"  # 假设存在
            ]
        
        # 根据变更类型进一步筛选
        if template.template_id == "function_rename":
            # 函数重命名主要影响直接调用的适配器
            pass
        elif template.template_id == "import_path_change":
            # 导入路径变更影响所有导入该模块的适配器
            pass
        
        return affected_adapters


# ============================================================================
# Diff生成器
# ============================================================================

class DiffGenerator:
    """Diff生成器"""
    
    @staticmethod
    def generate_unified_diff(old_content: str, new_content: str, old_file: str = "原文件", 
                             new_file: str = "建议修改", context_lines: int = 3) -> str:
        """生成统一差异格式
        
        Args:
            old_content: 旧内容
            new_content: 新内容
            old_file: 旧文件名
            new_file: 新文件名
            context_lines: 上下文行数
        
        Returns:
            unified diff格式字符串
        """
        old_lines = old_content.splitlines(keepends=True)
        new_lines = new_content.splitlines(keepends=True)
        
        diff = difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile=old_file,
            tofile=new_file,
            n=context_lines
        )
        
        return ''.join(diff)
    
    @staticmethod
    def generate_fix_proposal_diff(change: DetectedChange, adapter_file_path: Path) -> Optional[str]:
        """为修复建议生成diff
        
        Args:
            change: 检测到的变更
            adapter_file_path: 适配器文件路径
        
        Returns:
            diff内容，如果无法生成则返回None
        """
        if not adapter_file_path.exists():
            logger.warning(f"适配器文件不存在: {adapter_file_path}")
            return None
        
        # 读取适配器文件内容
        try:
            with open(adapter_file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
        except Exception as e:
            logger.error(f"读取适配器文件失败: {adapter_file_path}, 错误: {e}")
            return None
        
        # 生成修改后的内容（第一阶段简化：基于模板生成示例）
        modified_content = DiffGenerator._apply_fix_template(original_content, change)
        
        if original_content == modified_content:
            logger.info(f"无需修改适配器文件: {adapter_file_path}")
            return None
        
        # 生成diff
        diff = DiffGenerator.generate_unified_diff(
            original_content,
            modified_content,
            old_file=str(adapter_file_path),
            new_file=str(adapter_file_path) + " (建议修改)"
        )
        
        return diff
    
    @staticmethod
    def _apply_fix_template(original_content: str, change: DetectedChange) -> str:
        """应用修复模板生成修改后的内容
        
        第一阶段简化实现：仅演示功能
        
        Args:
            original_content: 原始内容
            change: 检测到的变更
        
        Returns:
            修改后的内容
        """
        if not change.fix_template:
            return original_content
        
        template = change.fix_template
        extraction_data = change.extraction_data
        
        # 根据模板类型应用不同的修复
        if template.template_id == "function_rename":
            old_name = extraction_data.get("old_name", "")
            new_name = extraction_data.get("new_name", "")
            
            if old_name and new_name:
                # 简单替换函数调用
                pattern = f"{old_name}\\("
                replacement = f"{new_name}("
                modified_content = re.sub(pattern, replacement, original_content)
                return modified_content
        
        elif template.template_id == "import_path_change":
            old_path = extraction_data.get("old_path", "")
            new_path = extraction_data.get("new_path", "")
            
            if old_path and new_path:
                pattern = f"from {old_path} import"
                replacement = f"from {new_path} import"
                modified_content = re.sub(pattern, replacement, original_content)
                return modified_content
        
        # 其他模板类型暂不实现
        return original_content


# ============================================================================
# 修复建议生成器
# ============================================================================

class FixProposalGenerator:
    """修复建议生成器"""
    
    def __init__(self, locator: AdapterChangeLocator, diff_generator: DiffGenerator):
        """初始化生成器
        
        Args:
            locator: 变更定位器
            diff_generator: diff生成器
        """
        self.locator = locator
        self.diff_generator = diff_generator
    
    def generate_proposals(self, plugin_name: str, old_version: str, new_version: str,
                          changelog_content: str) -> List[FixProposal]:
        """生成修复建议
        
        Args:
            plugin_name: 插件名称
            old_version: 旧版本
            new_version: 新版本
            changelog_content: 变更日志内容
        
        Returns:
            修复建议列表
        """
        # 1. 定位变更
        detected_changes = self.locator.locate_adapter_changes(
            plugin_name, old_version, new_version, changelog_content
        )
        
        if not detected_changes:
            return []
        
        # 2. 为每个变更生成修复建议
        proposals = []
        
        for change in detected_changes:
            # 为每个受影响的适配器生成diff
            for adapter_name in change.affected_adapters:
                # 查找适配器文件路径（简化逻辑）
                adapter_file_path = self._find_adapter_file(adapter_name)
                if not adapter_file_path or not adapter_file_path.exists():
                    logger.warning(f"未找到适配器文件: {adapter_name}")
                    continue
                
                # 生成diff
                diff_content = self.diff_generator.generate_fix_proposal_diff(change, adapter_file_path)
                if not diff_content:
                    continue
                
                # 创建修复建议
                proposal = FixProposal(
                    proposal_id=f"{change.change_id}_{adapter_name}",
                    detected_change=change,
                    diff_content=diff_content,
                    affected_files=[adapter_file_path],
                    risk_level=change.fix_template.risk_level if change.fix_template else "medium",
                    confidence=change.fix_template.confidence if change.fix_template else 0.5,
                    apply_command=f"# 手动应用命令:\n# patch {adapter_file_path} < diff.patch"
                )
                
                proposals.append(proposal)
                logger.info(f"生成修复建议: {proposal.proposal_id}, 风险等级: {proposal.risk_level}")
        
        return proposals
    
    def _find_adapter_file(self, adapter_name: str) -> Optional[Path]:
        """查找适配器文件路径
        
        第一阶段简化实现：基于已知路径
        
        Args:
            adapter_name: 适配器名称
        
        Returns:
            适配器文件路径
        """
        # 适配器名称到文件的映射
        adapter_file_map = {
            "self_improving_adapter": "/root/.openclaw/workspace/integration/adapter/self_improving_adapter.py",
            "msp_adapter": "/root/.openclaw/workspace/integration/adapter/msp_adapter.py",
            "unified_memory_adapter": "/root/.openclaw/workspace/integration/adapter/unified_memory_adapter.py",
            "xiaolongxia_adapter": "/root/.openclaw/workspace/integration/adapter/xiaolongxia_adapter.py",
            "memory_sync_enhanced_adapter": "/root/.openclaw/workspace/integration/adapter/memory_sync_enhanced_adapter.py"
        }
        
        file_path = adapter_file_map.get(adapter_name)
        if file_path:
            return Path(file_path)
        
        # 尝试在适配器目录中查找
        adapter_dir = Path("/root/.openclaw/workspace/integration/adapter")
        if adapter_dir.exists():
            for file in adapter_dir.glob("*.py"):
                if adapter_name.replace("_adapter", "") in file.stem:
                    return file
        
        return None


# ============================================================================
# 报告生成器
# ============================================================================

class FixReportGenerator:
    """修复报告生成器"""
    
    @staticmethod
    def generate_markdown_report(proposals: List[FixProposal]) -> str:
        """生成Markdown格式报告
        
        Args:
            proposals: 修复建议列表
        
        Returns:
            Markdown报告内容
        """
        if not proposals:
            return "## 🔍 适配器修复分析\n\n🟢 **未检测到需要修复的适配器变更**"
        
        report_lines = []
        report_lines.append("## 🔧 适配器自动修复建议")
        report_lines.append("")
        report_lines.append(f"**检测时间**: {FixReportGenerator._current_timestamp()}")
        report_lines.append(f"**检测到变更**: {len(proposals)} 个适配器需要修复")
        report_lines.append("")
        
        # 按风险等级分组
        high_risk = [p for p in proposals if p.risk_level == "high"]
        medium_risk = [p for p in proposals if p.risk_level == "medium"]
        low_risk = [p for p in proposals if p.risk_level == "low"]
        
        if high_risk:
            report_lines.append("### 🔴 高风险修复建议")
            for proposal in high_risk:
                report_lines.extend(FixReportGenerator._format_proposal(proposal))
        
        if medium_risk:
            report_lines.append("### 🟡 中风险修复建议")
            for proposal in medium_risk:
                report_lines.extend(FixReportGenerator._format_proposal(proposal))
        
        if low_risk:
            report_lines.append("### 🟢 低风险修复建议")
            for proposal in low_risk:
                report_lines.extend(FixReportGenerator._format_proposal(proposal))
        
        # 添加应用说明
        report_lines.append("")
        report_lines.append("## 📋 用户授权与应用流程")
        report_lines.append("")
        report_lines.append("### 🔐 授权确认（B1 用户授权流程）")
        report_lines.append("")
        report_lines.append("**交互确认步骤**:")
        report_lines.append("1. **审核diff**：仔细检查上方显示的代码变更")
        report_lines.append("2. **授权决策**：")
        report_lines.append("   - **同意修复**：回复 `同意修复 <修复ID>`（如 `同意修复 {proposal_id}`）")
        report_lines.append("   - **拒绝修复**：回复 `拒绝修复 <修复ID>` 或直接忽略")
        report_lines.append("3. **执行修复**：授权后系统将自动备份原文件并应用修复")
        report_lines.append("4. **验证结果**：修复后自动运行适配器健康检查")
        report_lines.append("")
        report_lines.append("**安全机制**:")
        report_lines.append("- 🔒 **备份优先**：修复前自动创建 `.backup` 文件")
        report_lines.append("- 🔍 **变更透明**：完整 diff 展示，无隐藏修改")
        report_lines.append("- ⏮️ **回滚支持**：可从备份文件一键恢复")
        report_lines.append("- 🧪 **健康检查**：修复后验证适配器功能完整性")
        report_lines.append("")
        report_lines.append("### 🛠️ 手动应用（备用方案）")
        report_lines.append("若希望手动应用修复，请按以下步骤操作：")
        report_lines.append("")
        report_lines.append("1. **备份原文件**:")
        for proposal in proposals:
            for file_path in proposal.affected_files:
                report_lines.append(f"   ```bash\n   cp {file_path} {file_path}.backup\n   ```")
        report_lines.append("2. **应用修复**:")
        report_lines.append("   ```bash")
        for proposal in proposals:
            for i, file_path in enumerate(proposal.affected_files):
                patch_file = f"fix_{proposal.proposal_id}_{i}.patch"
                report_lines.append(f"   # 修复 {proposal.proposal_id} - {file_path}")
                report_lines.append(f"   cat > {patch_file} << 'EOF'")
                # 简化diff内容，避免heredoc过长
                report_lines.append(f"   # [diff内容见上方]")
                report_lines.append(f"   EOF")
                report_lines.append(f"   patch {file_path} < {patch_file}")
                report_lines.append(f"   rm {patch_file}")
        report_lines.append("   ```")
        report_lines.append("3. **验证修改**:")
        report_lines.append("   ```bash")
        report_lines.append("   python3 /root/.openclaw/workspace/skills/memory-adapter-framework/scripts/adapter_cli.py health")
        report_lines.append("   ```")
        
        return "\n".join(report_lines)
    
    @staticmethod
    def _format_proposal(proposal: FixProposal) -> List[str]:
        """格式化单个修复建议"""
        lines = []
        change = proposal.detected_change
        
        lines.append(f"#### 📝 修复建议: {proposal.proposal_id}")
        lines.append("")
        lines.append(f"**插件**: {change.plugin_name} ({change.old_version} → {change.new_version})")
        lines.append(f"**变更类型**: {change.change_type.value}")
        lines.append(f"**风险等级**: {proposal.risk_level}")
        lines.append(f"**置信度**: {proposal.confidence:.1%}")
        lines.append(f"**受影响文件**: {', '.join(str(p) for p in proposal.affected_files)}")
        lines.append("")
        
        # 显示完整diff（最多100行）
        diff_lines = proposal.diff_content.split('\n')
        if len(diff_lines) > 100:
            preview_lines = diff_lines[:100]
            preview_lines.append(f"... (已截断，完整diff共 {len(diff_lines)} 行)")
        else:
            preview_lines = diff_lines
        
        lines.append("**建议修改 (diff)**:")
        lines.append("```diff")
        lines.extend(preview_lines)
        lines.append("```")
        lines.append("")
        
        # 备份说明
        backup_file = proposal.backup_path
        if backup_file and backup_file.exists():
            backup_info = f"已创建备份: `{backup_file}`"
        else:
            backup_info = "**建议手动备份**:"
            for file_path in proposal.affected_files:
                backup_info += f"\n- `cp {file_path} {file_path}.backup`"
        
        lines.append("**备份状态**:")
        lines.append(backup_info)
        lines.append("")
        
        # 详细应用步骤
        lines.append("**详细应用步骤**:")
        lines.append("1. **备份原文件**:")
        for file_path in proposal.affected_files:
            lines.append(f"   ```bash\n   cp {file_path} {file_path}.backup\n   ```")
        lines.append("2. **应用修复**:")
        lines.append("   ```bash")
        # 生成patch文件并应用
        patch_cmds = []
        for i, file_path in enumerate(proposal.affected_files):
            patch_file = f"fix_{proposal.proposal_id}_{i}.patch"
            lines.append(f"   # 保存diff到patch文件")
            lines.append(f"   cat > {patch_file} << 'EOF'")
            # 将diff内容嵌入heredoc（需要转义）
            lines.append(f"   {proposal.diff_content.replace(chr(10), chr(10) + '   ')}")
            lines.append(f"   EOF")
            lines.append(f"   patch {file_path} < {patch_file}")
            lines.append(f"   rm {patch_file}")
        lines.append("   ```")
        lines.append("3. **验证修改**:")
        lines.append("   ```bash")
        lines.append("   # 运行适配器健康检查")
        lines.append("   python3 /root/.openclaw/workspace/skills/memory-adapter-framework/scripts/adapter_cli.py health")
        lines.append("   ```")
        lines.append("")
        
        return lines
    
    @staticmethod
    def _current_timestamp() -> str:
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-d %H:%M:%S")


# ============================================================================
# 修复执行引擎 (B2)
# ============================================================================

class FixApplier:
    """修复执行引擎（B2） - 实际应用修复、备份、验证"""
    
    def __init__(self, backup_suffix: str = ".backup"):
        """初始化修复执行引擎
        
        Args:
            backup_suffix: 备份文件后缀
        """
        self.backup_suffix = backup_suffix
        self.applied_fixes: List[Dict] = []
    
    def apply_fix(self, proposal: FixProposal, require_backup: bool = True) -> Dict[str, Any]:
        """应用单个修复建议
        
        Args:
            proposal: 修复建议
            require_backup: 是否要求先备份
            
        Returns:
            应用结果
        """
        results = {
            "proposal_id": proposal.proposal_id,
            "success": False,
            "backup_created": False,
            "files_modified": [],
            "errors": []
        }
        
        # 1. 备份文件
        backup_paths = []
        if require_backup:
            for file_path in proposal.affected_files:
                backup_path = file_path.with_suffix(file_path.suffix + self.backup_suffix)
                try:
                    import shutil
                    shutil.copy2(file_path, backup_path)
                    backup_paths.append(backup_path)
                    results["backup_created"] = True
                    logger.info(f"已创建备份: {file_path} -> {backup_path}")
                except Exception as e:
                    error_msg = f"备份失败 {file_path}: {e}"
                    logger.error(error_msg)
                    results["errors"].append(error_msg)
                    return results  # 备份失败，不继续
        
        # 2. 应用diff
        # 将diff内容解析为补丁并应用
        # 简化实现：将diff内容写入临时patch文件，然后使用patch命令
        import tempfile
        import subprocess
        
        for file_path in proposal.affected_files:
            try:
                # 创建临时patch文件
                with tempfile.NamedTemporaryFile(mode='w', suffix='.patch', delete=False) as tmp:
                    tmp.write(proposal.diff_content)
                    tmp_path = tmp.name
                
                # 应用patch
                cmd = ["patch", str(file_path), "-i", tmp_path]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    results["files_modified"].append(str(file_path))
                    logger.info(f"成功应用修复到 {file_path}")
                else:
                    error_msg = f"应用patch失败 {file_path}: {result.stderr}"
                    logger.error(error_msg)
                    results["errors"].append(error_msg)
                    # 回滚：恢复备份
                    self._restore_backup(file_path, backup_paths)
                    results["errors"].append("已回滚修改")
                    break
                
                # 删除临时文件
                import os
                os.unlink(tmp_path)
                
            except Exception as e:
                error_msg = f"应用修复时异常 {file_path}: {e}"
                logger.error(error_msg)
                results["errors"].append(error_msg)
                self._restore_backup(file_path, backup_paths)
                break
        
        if not results["errors"] and results["files_modified"]:
            results["success"] = True
            logger.info(f"修复 {proposal.proposal_id} 应用成功")
        
        # 记录应用历史
        self.applied_fixes.append(results)
        return results
    
    def _restore_backup(self, file_path: Path, backup_paths: List[Path]):
        """从备份恢复文件"""
        for backup_path in backup_paths:
            if backup_path.stem == file_path.stem and backup_path.suffix.endswith(self.backup_suffix):
                try:
                    import shutil
                    shutil.copy2(backup_path, file_path)
                    logger.info(f"已从备份恢复: {backup_path} -> {file_path}")
                except Exception as e:
                    logger.error(f"恢复备份失败 {backup_path}: {e}")
                break
    
    def run_health_check(self) -> Dict[str, Any]:
        """运行适配器健康检查"""
        try:
            import subprocess
            cmd = ["python3", "/root/.openclaw/workspace/skills/memory-adapter-framework/scripts/adapter_cli.py", "health"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            return {
                "success": result.returncode == 0,
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


# ============================================================================
# 主接口
# ============================================================================

class AdapterAutoFixer:
    """适配器自动修复器（主接口）"""
    
    def __init__(self):
        """初始化自动修复器"""
        self.template_library = FixTemplateLibrary()
        self.locator = AdapterChangeLocator(self.template_library)
        self.diff_generator = DiffGenerator()
        self.proposal_generator = FixProposalGenerator(self.locator, self.diff_generator)
        self.report_generator = FixReportGenerator()
        self.fix_applier = FixApplier()  # B2 修复执行引擎
    
    def analyze_plugin_update(self, plugin_name: str, old_version: str, new_version: str,
                             changelog_content: str) -> Dict[str, Any]:
        """分析插件更新的适配器影响
        
        Args:
            plugin_name: 插件名称
            old_version: 旧版本
            new_version: 新版本
            changelog_content: 变更日志内容
        
        Returns:
            分析结果
        """
        logger.info(f"开始分析 {plugin_name} 更新的适配器影响")
        
        # 生成修复建议
        proposals = self.proposal_generator.generate_proposals(
            plugin_name, old_version, new_version, changelog_content
        )
        
        # 生成报告
        report = self.report_generator.generate_markdown_report(proposals)
        
        # 返回结果
        return {
            "plugin_name": plugin_name,
            "old_version": old_version,
            "new_version": new_version,
            "proposal_count": len(proposals),
            "proposals": proposals,
            "report": report,
            "has_changes": len(proposals) > 0
        }
    
    def apply_fix(self, proposal: FixProposal, require_backup: bool = True) -> Dict[str, Any]:
        """应用修复建议（B2 修复执行引擎）
        
        Args:
            proposal: 修复建议
            require_backup: 是否要求先备份
            
        Returns:
            应用结果
        """
        logger.info(f"开始应用修复建议: {proposal.proposal_id}")
        result = self.fix_applier.apply_fix(proposal, require_backup)
        
        # 运行健康检查（可选）
        if result["success"]:
            health_result = self.fix_applier.run_health_check()
            result["health_check"] = health_result
        
        return result
    
    def apply_fix_by_id(self, proposal_id: str, proposals: List[FixProposal]) -> Dict[str, Any]:
        """根据ID应用修复建议
        
        Args:
            proposal_id: 修复建议ID
            proposals: 修复建议列表
            
        Returns:
            应用结果
        """
        for proposal in proposals:
            if proposal.proposal_id == proposal_id:
                return self.apply_fix(proposal)
        
        return {
            "success": False,
            "error": f"未找到修复建议 {proposal_id}"
        }


# ============================================================================
# 测试函数
# ============================================================================

def test_adapter_auto_fixer():
    """测试适配器自动修复器"""
    print("🧪 测试适配器自动修复器...")
    
    # 创建自动修复器实例
    fixer = AdapterAutoFixer()
    
    # 测试数据：模拟 memory-sync-enhanced 更新
    test_plugin = "memory-sync-enhanced"
    test_old_version = "2.0.0"
    test_new_version = "2.1.0"
    test_changelog = """
    Version 2.1.0
    -------------
    
    New Features:
    - Added new API endpoint for batch processing
    
    Breaking Changes:
    - Renamed function 'process_memory' to 'process_memory_batch'
    - Changed import path from 'memory_sync.core' to 'memory_sync.advanced'
    
    Bug Fixes:
    - Fixed memory leak in co-occurrence tracker
    """
    
    print(f"测试插件: {test_plugin} ({test_old_version} → {test_new_version})")
    
    # 分析更新
    result = fixer.analyze_plugin_update(
        test_plugin, test_old_version, test_new_version, test_changelog
    )
    
    # 打印结果
    print(f"\n📊 分析结果:")
    print(f"- 检测到变更: {result['has_changes']}")
    print(f"- 修复建议数: {result['proposal_count']}")
    
    if result['proposal_count'] > 0:
        print(f"\n📋 报告预览:")
        report_lines = result['report'].split('\n')
        for line in report_lines[:30]:  # 只显示前30行
            print(line)
    
    return result


def test_end_to_end():
    """B4 端到端测试：完整插件更新 + 适配器修复流程"""
    print("🚀 B4 端到端测试：完整插件更新 + 适配器修复流程")
    print("=" * 60)
    
    import tempfile
    import shutil
    from pathlib import Path
    import sys
    import os
    
    # 创建临时测试适配器文件
    temp_dir = tempfile.mkdtemp(prefix="evol_test_")
    test_adapter_path = Path(temp_dir) / "test_adapter.py"
    test_adapter_content = '''"""测试适配器文件 - 用于端到端测试"""
from memory_sync.core import process_memory

def adapter_function(data):
    """处理记忆数据"""
    result = process_memory(data)
    return result

def another_function():
    """另一个函数，也使用 process_memory"""
    return process_memory({"key": "value"})
'''
    test_adapter_path.write_text(test_adapter_content, encoding='utf-8')
    print(f"📁 创建测试适配器文件: {test_adapter_path}")
    
    # 保存原始方法
    original_find_adapter_file = FixProposalGenerator._find_adapter_file
    
    # 猴子补丁：使 _find_adapter_file 返回测试文件
    def patched_find_adapter_file(self, adapter_name):
        # 只针对测试适配器名称返回测试文件
        if adapter_name == "self_improving_adapter":
            return test_adapter_path
        # 其他适配器返回原路径
        return original_find_adapter_file(self, adapter_name)
    
    FixProposalGenerator._find_adapter_file = patched_find_adapter_file
    print("🔧 已应用猴子补丁，将 self_improving_adapter 映射到测试文件")
    
    try:
        # 创建自动修复器实例（使用补丁后的类）
        fixer = AdapterAutoFixer()
        
        # 测试数据：模拟 memory-sync-enhanced 更新，包含适配器相关变更
        test_plugin = "memory-sync-enhanced"
        test_old_version = "2.0.0"
        test_new_version = "2.1.0"
        test_changelog = """
        Version 2.1.0
        -------------
        
        Breaking Changes:
        - Renamed function 'process_memory' to 'process_memory_batch'
        - Changed import path from 'memory_sync.core' to 'memory_sync.advanced'
        
        Adapter Changes:
        - Updated adapter interface to support batch processing
        """
        
        print(f"📦 模拟插件更新: {test_plugin} ({test_old_version} → {test_new_version})")
        
        # 1. 分析更新
        print("\n🔍 步骤1: 分析插件更新...")
        analysis_result = fixer.analyze_plugin_update(
            test_plugin, test_old_version, test_new_version, test_changelog
        )
        
        print(f"   - 检测到变更: {analysis_result['has_changes']}")
        print(f"   - 修复建议数: {analysis_result['proposal_count']}")
        
        if analysis_result['proposal_count'] == 0:
            print("   ⚠️  未生成修复建议，无法进行端到端测试")
            # 显示详细日志以调试
            print("   📝 调试信息：")
            print(f"   - 测试文件存在: {test_adapter_path.exists()}")
            print(f"   - 测试文件内容前200字符: {test_adapter_content[:200]}")
            return False
        
        # 2. 展示修复建议
        print("\n📋 步骤2: 修复建议报告...")
        report_lines = analysis_result['report'].split('\n')
        for i, line in enumerate(report_lines[:30]):  # 显示前30行
            if i < 30:
                print(f"   {line}")
            else:
                print("   ... (报告过长，已截断)")
                break
        
        # 3. 模拟用户授权（选择第一个修复建议）
        print("\n🔐 步骤3: 模拟用户授权...")
        proposals = analysis_result['proposals']
        first_proposal = proposals[0]
        print(f"   - 选择修复建议: {first_proposal.proposal_id}")
        print(f"   - 变更类型: {first_proposal.detected_change.change_type.value}")
        print(f"   - 风险等级: {first_proposal.risk_level}")
        print(f"   - 受影响文件: {first_proposal.affected_files}")
        print(f"   - 模拟用户回复: '同意修复 {first_proposal.proposal_id}'")
        
        # 4. 应用修复
        print("\n🔧 步骤4: 应用修复...")
        # 首先备份原始测试文件内容
        original_content = test_adapter_path.read_text(encoding='utf-8')
        apply_result = fixer.apply_fix(first_proposal, require_backup=True)
        
        print(f"   - 应用成功: {apply_result['success']}")
        if apply_result['success']:
            print(f"   - 备份创建: {apply_result['backup_created']}")
            print(f"   - 修改文件: {apply_result['files_modified']}")
            # 验证文件是否实际修改
            modified_content = test_adapter_path.read_text(encoding='utf-8')
            if modified_content != original_content:
                print("   ✅ 文件内容已变更")
                # 显示变更示例
                import difflib
                diff = list(difflib.unified_diff(
                    original_content.splitlines(keepends=True),
                    modified_content.splitlines(keepends=True),
                    fromfile='original',
                    tofile='modified',
                    n=3
                ))
                if diff:
                    print("   📋 变更示例:")
                    for line in diff[:10]:
                        print(f"      {line.rstrip()}")
            else:
                print("   ⚠️  文件内容未变化")
        else:
            print(f"   - 错误: {apply_result['errors']}")
        
        # 5. 健康检查（模拟）
        print("\n🏥 步骤5: 运行适配器健康检查...")
        health_result = fixer.fix_applier.run_health_check()
        print(f"   - 健康检查成功: {health_result['success']}")
        if health_result.get('exit_code') is not None:
            print(f"   - 退出码: {health_result['exit_code']}")
        if health_result.get('stdout'):
            print(f"   - 输出: {health_result['stdout'][:200]}...")
        
        # 6. 测试总结
        print("\n📊 测试总结:")
        all_success = apply_result['success'] and health_result['success']
        if all_success:
            print("✅ 端到端测试通过！修复执行引擎工作正常。")
        else:
            print("❌ 端到端测试失败。")
            print(f"   - 修复应用: {'✅' if apply_result['success'] else '❌'}")
            print(f"   - 健康检查: {'✅' if health_result['success'] else '❌'}")
        
        return all_success
        
    finally:
        # 恢复原始方法
        FixProposalGenerator._find_adapter_file = original_find_adapter_file
        print("🔄 已恢复原始方法")
        
        # 清理临时文件
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
            print(f"🧹 已清理临时目录: {temp_dir}")
        except Exception as e:
            print(f"⚠️  清理临时目录失败: {e}")


if __name__ == "__main__":
    # 设置日志
    logging.basicConfig(level=logging.INFO)
    
    # 运行基本测试
    print("🧪 运行基本功能测试...")
    test_result = test_adapter_auto_fixer()
    
    # 运行端到端测试
    print("\n" + "=" * 60)
    end_to_end_result = test_end_to_end()
    
    print("\n✅ 所有测试完成")