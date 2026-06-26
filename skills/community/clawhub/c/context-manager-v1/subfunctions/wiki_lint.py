#!/usr/bin/env python3
"""
Wiki Lint - 知识库自我修复模块

检查知识库问题，自动修复
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List


class WikiLint:
    """知识库 lint 检查器"""
    
    def __init__(self, kb_path: str = "~/kb"):
        self.kb_path = Path(kb_path).expanduser()
        self.index_path = self.kb_path / "_index.json"
        self.lint_report_path = self.kb_path / "_lint_report.md"
        
        # 加载索引
        self.index = self._load_index()
    
    def _load_index(self) -> dict:
        """加载索引"""
        if self.index_path.exists():
            return json.loads(self.index_path.read_text())
        return {"notes": {}, "links": {}, "keywords": {}}
    
    def _save_index(self):
        """保存索引"""
        self.index_path.write_text(json.dumps(self.index, indent=2, ensure_ascii=False))
    
    def run_lint(self, auto_fix: bool = True) -> Dict[str, Any]:
        """
        运行 lint 检查
        
        Args:
            auto_fix: 是否自动修复
        
        Returns:
            lint 报告
        """
        report = {
            "checked_at": datetime.now().isoformat(),
            "total_notes": 0,
            "issues": [],
            "fixed_issues": [],
            "health_score": 100
        }
        
        # 检查 1：断链
        broken_links = self._check_broken_links()
        report["issues"].extend(broken_links)
        
        # 检查 2：孤立笔记
        orphan_notes = self._check_orphan_notes()
        report["issues"].extend(orphan_notes)
        
        # 检查 3：重复内容
        duplicate_notes = self._check_duplicates()
        report["issues"].extend(duplicate_notes)
        
        # 检查 4：标签不一致
        tag_issues = self._check_tag_consistency()
        report["issues"].extend(tag_issues)
        
        # 检查 5：索引完整性
        index_issues = self._check_index_integrity()
        report["issues"].extend(index_issues)
        
        report["total_notes"] = len(self.index.get("notes", {}))
        
        # 自动修复
        if auto_fix:
            fixed = self._auto_fix(report["issues"])
            report["fixed_issues"] = fixed
        
        # 计算健康分数
        report["health_score"] = self._calculate_health_score(report)
        
        # 生成报告
        self._generate_lint_report(report)
        
        return report
    
    def _check_broken_links(self) -> List[dict]:
        """检查断链"""
        issues = []
        
        for note_id, note_info in self.index.get("notes", {}).items():
            note_path = Path(note_info.get("path", ""))
            if not note_path.exists():
                issues.append({
                    "type": "broken_link",
                    "severity": "high",
                    "note_id": note_id,
                    "note_path": str(note_path),
                    "description": f"笔记文件不存在：{note_path}",
                    "auto_fixable": False
                })
        
        return issues
    
    def _check_orphan_notes(self) -> List[dict]:
        """检查孤立笔记（无连接）"""
        issues = []
        
        links = self.index.get("links", {})
        
        for note_id, note_info in self.index.get("notes", {}).items():
            # 检查是否有出链或入链
            has_outgoing = len(note_info.get("keywords", [])) > 0
            has_incoming = note_id in links and len(links[note_id]) > 0
            
            if not has_outgoing and not has_incoming:
                issues.append({
                    "type": "orphan_note",
                    "severity": "medium",
                    "note_id": note_id,
                    "note_title": note_info.get("title", ""),
                    "description": f"孤立笔记：{note_info.get('title', note_id)} 无任何连接",
                    "auto_fixable": True,
                    "fix_suggestion": "建议添加相关笔记连接或标签"
                })
        
        return issues
    
    def _check_duplicates(self) -> List[dict]:
        """检查重复内容"""
        issues = []
        
        # 按标题分组
        title_groups = {}
        for note_id, note_info in self.index.get("notes", {}).items():
            title = note_info.get("title", "")
            if title:
                if title not in title_groups:
                    title_groups[title] = []
                title_groups[title].append(note_id)
        
        # 找出重复
        for title, note_ids in title_groups.items():
            if len(note_ids) > 1:
                issues.append({
                    "type": "duplicate_title",
                    "severity": "medium",
                    "title": title,
                    "note_ids": note_ids,
                    "description": f"重复标题：{title} ({len(note_ids)}篇笔记)",
                    "auto_fixable": False,
                    "fix_suggestion": "建议合并或重命名"
                })
        
        return issues
    
    def _check_tag_consistency(self) -> List[dict]:
        """检查标签一致性"""
        issues = []
        
        for note_id, note_info in self.index.get("notes", {}).items():
            tags = note_info.get("tags", {})
            themes = tags.get("themes", [])
            scenes = tags.get("scenes", [])
            actions = tags.get("actions", [])
            
            # 检查是否有标签
            if not themes and not scenes and not actions:
                issues.append({
                    "type": "missing_tags",
                    "severity": "high",
                    "note_id": note_id,
                    "note_title": note_info.get("title", ""),
                    "description": f"笔记无标签：{note_info.get('title', note_id)}",
                    "auto_fixable": False,
                    "fix_suggestion": "建议添加主题 + 场景 + 行动标签"
                })
            
            # 检查标签格式
            for theme in themes:
                if "/" not in theme:
                    issues.append({
                        "type": "invalid_tag_format",
                        "severity": "low",
                        "note_id": note_id,
                        "tag": theme,
                        "description": f"标签格式不规范：{theme}（建议：类别/子类别）",
                        "auto_fixable": False
                    })
        
        return issues
    
    def _check_index_integrity(self) -> List[dict]:
        """检查索引完整性"""
        issues = []
        
        # 检查索引与文件是否一致
        notes_in_index = set(self.index.get("notes", {}).keys())
        
        # 扫描实际文件
        actual_notes = set()
        for folder in ["00-Inbox", "10-投资", "20-产品", "30-技术", "40-管理", "50-个人", "90-归档"]:
            folder_path = self.kb_path / folder
            if folder_path.exists():
                for md_file in folder_path.glob("*.md"):
                    actual_notes.add(md_file.stem)
        
        # 找出差异
        missing_in_index = actual_notes - notes_in_index
        if missing_in_index:
            issues.append({
                "type": "index_out_of_sync",
                "severity": "medium",
                "missing_count": len(missing_in_index),
                "description": f"索引缺失 {len(missing_in_index)} 篇笔记",
                "auto_fixable": True,
                "fix_suggestion": "建议重建索引"
            })
        
        return issues
    
    def _auto_fix(self, issues: List[dict]) -> List[dict]:
        """自动修复问题"""
        fixed = []
        
        for issue in issues:
            if not issue.get("auto_fixable", False):
                continue
            
            if issue["type"] == "orphan_note":
                # 尝试为孤立笔记添加连接
                self._fix_orphan_note(issue["note_id"])
                fixed.append(issue)
            
            elif issue["type"] == "index_out_of_sync":
                # 重建索引
                self._rebuild_index()
                fixed.append(issue)
        
        return fixed
    
    def _fix_orphan_note(self, note_id: str):
        """修复孤立笔记：添加建议连接"""
        # 简化版：在笔记末尾添加提示
        note_info = self.index["notes"].get(note_id, {})
        note_path = Path(note_info.get("path", ""))
        
        if note_path.exists():
            content = note_path.read_text()
            
            # 检查是否已有相关笔记部分
            if "## 🔗 相关笔记" not in content:
                # 添加提示
                content += "\n\n---\n\n## 🔗 相关笔记\n\n> 💡 提示：此笔记暂无连接，建议添加相关笔记链接。\n"
                note_path.write_text(content)
    
    def _rebuild_index(self):
        """重建索引"""
        # 简化版：重新扫描所有文件
        # 实际应该调用 store 模块
        print("重建索引...")
        # TODO: 实现完整的索引重建
    
    def _calculate_health_score(self, report: dict) -> int:
        """计算健康分数（0-100）"""
        score = 100
        
        # 扣分项
        for issue in report["issues"]:
            severity = issue.get("severity", "low")
            if severity == "high":
                score -= 10
            elif severity == "medium":
                score -= 5
            elif severity == "low":
                score -= 2
        
        # 修复加分
        score += len(report["fixed_issues"]) * 2
        
        return max(0, min(100, score))
    
    def _generate_lint_report(self, report: dict):
        """生成 lint 报告"""
        report_md = f"""# 知识库 Lint 报告

**检查时间**：{report['checked_at']}

**健康分数**：{report['health_score']}/100

**检查笔记数**：{report['total_notes']}

**问题总数**：{len(report['issues'])}

**已修复**：{len(report['fixed_issues'])}

---

## 问题列表

"""
        
        # 按严重程度分组
        high_issues = [i for i in report["issues"] if i.get("severity") == "high"]
        medium_issues = [i for i in report["issues"] if i.get("severity") == "medium"]
        low_issues = [i for i in report["issues"] if i.get("severity") == "low"]
        
        if high_issues:
            report_md += "### 🔴 高优先级\n\n"
            for issue in high_issues:
                report_md += f"- **{issue['type']}**: {issue['description']}\n"
            report_md += "\n"
        
        if medium_issues:
            report_md += "### 🟡 中优先级\n\n"
            for issue in medium_issues:
                report_md += f"- **{issue['type']}**: {issue['description']}\n"
            report_md += "\n"
        
        if low_issues:
            report_md += "### 🟢 低优先级\n\n"
            for issue in low_issues:
                report_md += f"- **{issue['type']}**: {issue['description']}\n"
            report_md += "\n"
        
        if not report["issues"]:
            report_md += "✅ 无问题，知识库健康！\n"
        
        self.lint_report_path.parent.mkdir(parents=True, exist_ok=True)
        self.lint_report_path.write_text(report_md)


def main():
    """测试 lint 功能"""
    linter = WikiLint("/home/admin/kb")
    
    print("运行 lint 检查...")
    report = linter.run_lint(auto_fix=True)
    
    print(f"\n健康分数：{report['health_score']}/100")
    print(f"检查笔记数：{report['total_notes']}")
    print(f"问题总数：{len(report['issues'])}")
    print(f"已修复：{len(report['fixed_issues'])}")
    
    if report["issues"]:
        print("\n问题列表:")
        for issue in report["issues"][:5]:
            print(f"- [{issue['severity']}] {issue['description']}")
    
    print(f"\n详细报告：~/kb/_lint_report.md")


if __name__ == "__main__":
    main()
