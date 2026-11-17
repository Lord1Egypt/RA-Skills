"""
Saga 协调器单元测试
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from middlewares.saga_coordinator import SagaCoordinator


class TestSagaCoordinator:
    """SagaCoordinator 单元测试"""

    def test_empty_compensation(self):
        """无注册补偿时 compensate_all 返回空列表"""
        saga = SagaCoordinator()
        result = saga.compensate_all()
        assert result == []

    def test_single_compensation(self, tmp_path):
        """单个补偿函数执行"""
        calls = []

        saga = SagaCoordinator()
        saga.register("Step3", lambda: calls.append("compensated"))
        result = saga.compensate_all()

        assert result == ["Step3"]
        assert calls == ["compensated"]

    def test_reverse_order_compensation(self, tmp_path):
        """补偿按逆序执行"""
        order = []

        saga = SagaCoordinator()
        saga.register("Step1", lambda: order.append(1))
        saga.register("Step2", lambda: order.append(2))
        saga.register("Step3", lambda: order.append(3))

        result = saga.compensate_all()

        # 逆序：Step3 → Step2 → Step1
        assert order == [3, 2, 1]
        assert result == ["Step3", "Step2", "Step1"]

    def test_compensation_failure_doesnt_block(self, tmp_path):
        """一个补偿失败不应阻断后续补偿"""
        order = []

        def failing():
            order.append("fail")
            raise RuntimeError("补偿失败")

        saga = SagaCoordinator()
        saga.register("Step3", failing)
        saga.register("Step2", lambda: order.append("ok"))

        result = saga.compensate_all()

        # 逆序执行：Step2 先于 Step3（后注册的先执行）
        # Step2 成功 → 添加到 order
        # Step3 失败 → 被 try/except 捕获，不影响 Step2
        assert "fail" in order
        assert "ok" in order
        assert "Step2" in result  # Step2 补偿成功
        assert "Step3" not in result  # Step3 补偿失败

    def test_registered_steps_property(self, tmp_path):
        """registered_steps 属性"""
        saga = SagaCoordinator()
        saga.register("Phase0", lambda: None)
        saga.register("Step3", lambda: None)

        assert saga.registered_steps == ["Phase0", "Step3"]

    def test_compensate_all_clears_registrations(self, tmp_path):
        """compensate_all 后清空注册列表"""
        saga = SagaCoordinator()
        saga.register("Step3", lambda: None)

        saga.compensate_all()
        assert saga.registered_steps == []

    def test_file_cleanup_compensation(self, tmp_path):
        """文件清理补偿（模拟 AssetHandler 的补偿）"""
        # 创建一些文件
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "main.py").write_text("test")
        (tmp_path / "test.txt").write_text("test")

        import shutil

        def cleanup():
            for subdir in ("src",):
                p = tmp_path / subdir
                if p.exists():
                    shutil.rmtree(p, ignore_errors=True)
            for pattern in ("*.txt",):
                for f in tmp_path.glob(pattern):
                    f.unlink()

        saga = SagaCoordinator()
        saga.register("Step3", cleanup)
        saga.compensate_all()

        assert not (tmp_path / "src").exists()
        assert not (tmp_path / "test.txt").exists()

    def test_multiple_registrations_same_step(self, tmp_path):
        """同一步骤可以注册多次"""
        calls = []
        saga = SagaCoordinator()
        saga.register("Step3", lambda: calls.append("first"))
        saga.register("Step3", lambda: calls.append("second"))
        saga.compensate_all()

        assert calls == ["second", "first"]  # 逆序
