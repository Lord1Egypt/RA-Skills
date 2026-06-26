#!/usr/bin/env python3
"""
CLI-Anything Wrapper 测试
"""

import sys
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import json

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from run import CLIAnythingWrapper, SUPPORTED_APPS, AppInfo


class TestAppInfo:
    """测试 AppInfo 数据类"""
    
    def test_app_info_creation(self):
        app = AppInfo(
            name="test",
            desc="测试应用",
            category="测试",
            harness_path="test/harness",
            requires=["test-dep"],
            test_count=10
        )
        assert app.name == "test"
        assert app.desc == "测试应用"
        assert app.test_count == 10
    
    def test_supported_apps_count(self):
        """测试支持的软件数量"""
        assert len(SUPPORTED_APPS) >= 10, "应该支持至少10个软件"


class TestCLIAnythingWrapper:
    """测试 CLIAnythingWrapper 类"""
    
    def setup_method(self):
        self.wrapper = CLIAnythingWrapper()
    
    def test_init(self):
        """测试初始化"""
        assert self.wrapper.cli_path == Path.home() / ".openclaw/workspace/CLI-Anything"
        assert self.wrapper.plugin_path == Path.home() / ".openclaw/workspace/CLI-Anything" / "cli-anything-plugin"
    
    @patch('pathlib.Path.exists')
    def test_check_installation_not_exists(self, mock_exists):
        """测试 CLI-Anything 未安装"""
        mock_exists.return_value = False
        wrapper = CLIAnythingWrapper()
        # 捕获输出
        with patch('builtins.print') as mock_print:
            result = wrapper.check_installation()
            assert result == False
            assert any("未安装" in str(c) for c in mock_print.call_args_list)
    
    def test_check_app_available_valid(self):
        """测试检查有效应用"""
        available, app = self.wrapper.check_app_available("gimp")
        assert available == True
        assert app.name == "gimp"
    
    def test_check_app_available_invalid(self):
        """测试检查无效应用"""
        available, app = self.wrapper.check_app_available("invalid_app_xyz")
        assert available == False
        assert app is None
    
    def test_check_app_available_case_sensitive(self):
        """测试大小写敏感"""
        available, app = self.wrapper.check_app_available("GIMP")
        assert available == False  # 应该是小写
    
    def test_list_apps_output(self):
        """测试列出应用输出"""
        with patch('builtins.print') as mock_print:
            self.wrapper.list_apps()
            # 检查是否有输出
            assert mock_print.called
    
    def test_supported_apps_has_required_fields(self):
        """测试所有应用都有必要字段"""
        for name, app in SUPPORTED_APPS.items():
            assert app.name, f"{name} 缺少 name"
            assert app.desc, f"{name} 缺少 desc"
            assert app.category, f"{name} 缺少 category"
            assert app.harness_path, f"{name} 缺少 harness_path"
            assert app.requires, f"{name} 缺少 requires"
    
    def test_all_categories(self):
        """测试分类完整性"""
        categories = set(app.category for app in SUPPORTED_APPS.values())
        expected_categories = {"设计", "3D", "办公", "音视频", "AI", "学术"}
        assert categories.issubset(expected_categories), f"未知分类: {categories - expected_categories}"
    
    def test_show_info(self):
        """测试显示信息"""
        with patch('builtins.print') as mock_print:
            self.wrapper.show_info()
            assert mock_print.called


class TestIntegration:
    """集成测试"""
    
    def test_import_module(self):
        """测试模块导入"""
        import run
        assert hasattr(run, 'CLIAnythingWrapper')
        assert hasattr(run, 'SUPPORTED_APPS')
        assert hasattr(run, 'AppInfo')
    
    def test_main_help(self):
        """测试主程序帮助"""
        import run
        with patch('sys.argv', ['run.py', '--help']):
            try:
                run.main()
            except SystemExit:
                pass  # --help 会触发 sys.exit(0)


def run_tests():
    """运行所有测试"""
    print("🧪 运行 CLI-Anything Wrapper 测试...\n")
    
    test_classes = [
        TestAppInfo,
        TestCLIAnythingWrapper,
        TestIntegration,
    ]
    
    total = 0
    passed = 0
    failed = []
    
    for test_class in test_classes:
        instance = test_class()
        for method_name in dir(instance):
            if method_name.startswith('test_'):
                total += 1
                try:
                    getattr(instance, method_name)()
                    passed += 1
                    print(f"  ✅ {method_name}")
                except Exception as e:
                    failed.append((method_name, str(e)))
                    print(f"  ❌ {method_name}: {e}")
    
    print(f"\n📊 测试结果: {passed} 通过, {len(failed)} 失败, 共 {total} 个")
    
    if failed:
        print("\n❌ 失败详情:")
        for name, err in failed:
            print(f"  - {name}: {err}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(run_tests())