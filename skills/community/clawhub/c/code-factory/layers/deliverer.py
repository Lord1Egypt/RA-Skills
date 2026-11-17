"""
Step 6: 交付器 —— 组装最终交付物。

输出：
- 项目路径（绝对路径）
- README.md 内容预览
- ASSET_MANIFEST.md 资源地图摘要
- manifest.json 机器可读摘要
- 测试结果摘要
"""

from pathlib import Path
from typing import Dict
from contracts.step_context import StepContext


class Deliverer:
    """Step 6 交付输出组装"""

    def deliver(
        self,
        project_path: Path,
        project_name: str,
        context: StepContext,
    ) -> Dict:
        """
        组装最终交付物。

        Returns:
            {
                "project_path": str,
                "readme_preview": str,
                "manifest_summary": str,
                "manifest_json_summary": str,
                "test_summary": str,
            }
        """
        result: Dict = {
            "project_path": str(project_path.absolute()),
            "readme_preview": self._get_readme_preview(project_path),
            "manifest_summary": self._get_manifest_summary(project_path),
            "manifest_json_summary": self._get_manifest_json_summary(project_path),
            "test_summary": self._get_test_summary(context),
        }
        return result

    def _get_readme_preview(self, project_path: Path) -> str:
        """获取 README 内容预览（前 500 字符）"""
        readme_path = project_path / "docs" / "README.md"
        if readme_path.exists():
            content = readme_path.read_text(encoding="utf-8")
            if len(content) > 500:
                return content[:500] + "\n...（截断）"
            return content
        return "(README.md 未找到)"

    def _get_manifest_summary(self, project_path: Path) -> str:
        """获取 ASSET_MANIFEST.md 资源地图摘要"""
        manifest_path = project_path / "ASSET_MANIFEST.md"
        if manifest_path.exists():
            content = manifest_path.read_text(encoding="utf-8")
            # 提取资源清单表格
            lines = content.split("\n")
            summary_lines = []
            in_table = False
            for line in lines:
                if line.startswith("| `"):
                    in_table = True
                    summary_lines.append(line)
                elif in_table and not line.startswith("|"):
                    break
            return "\n".join(summary_lines) if summary_lines else "(无资源清单)"
        return "(ASSET_MANIFEST.md 未找到)"

    def _get_manifest_json_summary(self, project_path: Path) -> str:
        """获取 manifest.json 机器可读摘要"""
        manifest_json = project_path / "manifest.json"
        if manifest_json.exists():
            import json
            try:
                data = json.loads(manifest_json.read_text(encoding="utf-8"))
                return json.dumps({
                    "project_name": data.get("project_name"),
                    "generated_at": data.get("generated_at"),
                    "asset_count": len(data.get("assets", [])),
                }, ensure_ascii=False, indent=2)
            except json.JSONDecodeError:
                return "(manifest.json 格式错误)"
        return "(manifest.json 未找到)"

    def _get_test_summary(self, context: StepContext) -> str:
        """获取测试结果摘要"""
        if context.verification_report:
            vr = context.verification_report
            passed = "✅ 全部通过" if vr.get("all_passed") else "❌ 存在失败"
            issues = vr.get("issues", [])
            if issues:
                return f"{passed}\n" + "\n".join(f"  - {i}" for i in issues)
            return passed
        return "（未执行验证）"
