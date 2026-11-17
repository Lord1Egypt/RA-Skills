"""
验证器单元测试
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from layers.verifier import Verifier, VerificationResult


class TestVerifier:
    """Step 4 验证器测试"""

    def test_verify_empty_assets(self, tmp_path):
        """空资产列表的验证"""
        v = Verifier()
        result = v.verify(target_dir=tmp_path, assets=[])
        assert result.all_passed  # 无文件无错误
        assert result.test_passed  # 无测试时默认通过

    def test_verify_no_circular_deps(self, tmp_path):
        """无循环引用的简单文件"""
        # 创建简单的测试文件
        src = tmp_path / "src"
        src.mkdir()
        (src / "main.py").write_text("import sys\n\ndef main(): return 0\n")

        v = Verifier()
        result = v.verify(
            target_dir=tmp_path,
            assets=["src/main.py"],
        )
        assert result.dependency_ok

    def test_dependency_analysis_circular(self, tmp_path):
        """检测循环引用"""
        src = tmp_path / "src"
        src.mkdir()
        (src / "module_a.py").write_text("from module_b import func_b\n")
        (src / "module_b.py").write_text("from module_a import func_a\n")

        v = Verifier()
        result = v.verify(
            target_dir=tmp_path,
            assets=["src/module_a.py", "src/module_b.py"],
        )
        assert not result.dependency_ok
        assert any("循环引用" in i for i in result.issues)

    def test_hard_gate_verification(self, tmp_path):
        """HARD-GATE 验证：有标记但无测试"""
        src = tmp_path / "src"
        src.mkdir()
        (src / "main.py").write_text("# <!-- HARD-GATE -->\ndef main(): return 0\n")

        v = Verifier()
        result = v.verify(
            target_dir=tmp_path,
            assets=["src/main.py"],
        )
        assert not result.hard_gate_ok
        assert any("HARD-GATE" in i for i in result.issues)

    def test_to_dict(self):
        """VerificationResult.to_dict 格式"""
        vr = VerificationResult(all_passed=True, test_passed=True)
        d = vr.to_dict()
        assert d["all_passed"] is True
        assert "issues" in d
        assert "suggestions" in d
