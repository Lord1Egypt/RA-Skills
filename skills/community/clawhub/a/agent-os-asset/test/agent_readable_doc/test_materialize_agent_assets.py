from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from support import load_skill_script


class MaterializeAgentAssetsTest(unittest.TestCase):
    def test_materializes_document_with_archived_source_map(self) -> None:
        materializer = load_skill_script("materialize_agent_assets.py")
        validator = load_skill_script("validate_agent_doc.py")
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "slides" / "report.pdf"
            source.parent.mkdir(parents=True)
            source.write_bytes(b"pdf")
            target = root / "slides" / "report.agent.md"
            result = materializer.materialize_document(
                root=root,
                source=source,
                archive_path=root / "Archived" / "slides" / "report.pdf",
                target=target,
                normalized_text=(
                    "# report\n\n## Sampled Text\n\n"
                    "推荐系统排序模型优化\nFTRL 特征工程 Pipeline\n"
                ),
            )
            target.write_text(result.markdown, encoding="utf-8")
            self.assertIn("推荐系统排序模型优化", result.manifest_row["summary"])
            self.assertIn("## Summary / 摘要", result.markdown)
            self.assertIn("## Insight / 洞察", result.markdown)
            self.assertIn("## Details / 详情", result.markdown)
            self.assertIn("## Source Map / 来源映射", result.markdown)
            self.assertIn("Use when locating or understanding report. / 适用于定位或理解 report。", result.markdown)
            self.assertIn("Skip when the original layout", result.markdown)
            self.assertIn("/ 当需要原始版式", result.markdown)
            self.assertIn("[[Archived/slides/report.pdf]]", result.markdown)
            self.assertEqual(validator.validate(target), [])


if __name__ == "__main__":
    unittest.main()
