"""
CivilLabClaw-AI 测试脚本

运行所有子技能的测试
"""

import sys
from pathlib import Path

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))


def test_all():
    """运行所有测试"""
    print("=" * 60)
    print("CivilLabClaw-AI 技能包 - 测试套件")
    print("=" * 60)
    
    results = {
        "ml_struct": test_ml_struct(),
        "dl_damage": test_dl_damage(),
        "digital_twin": test_digital_twin(),
        "smart_monitor": test_smart_monitor()
    }
    
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    for skill, result in results.items():
        status = "✓ 通过" if result else "✗ 失败"
        print(f"  {skill}: {status}")
    
    all_passed = all(results.values())
    print("\n" + "=" * 60)
    if all_passed:
        print("所有测试通过 ✓")
    else:
        print("部分测试失败 ✗")
    print("=" * 60)
    
    return all_passed


def test_ml_struct():
    """测试 ML-Struct 子技能"""
    print("\n[1/4] 测试 ML-Struct...")
    
    try:
        from ml_struct.predictor import StructuralPredictor
        
        # 测试初始化
        predictor = StructuralPredictor(model_type="gpr")
        print("  ✓ 预测器初始化成功")
        
        # 测试预测
        result = predictor.predict({
            "num_stories": 5,
            "story_height": 3.5,
            "bay_width": 6.0,
            "concrete_strength": 30,
            "pga": 0.3
        })
        
        assert result["status"] == "success"
        assert "predictions" in result
        print("  ✓ 预测功能正常")
        
        return True
        
    except Exception as e:
        print(f"  ✗ 测试失败：{e}")
        return False


def test_dl_damage():
    """测试 DL-Damage 子技能"""
    print("\n[2/4] 测试 DL-Damage...")
    
    try:
        from dl_damage.detector import DamageDetector
        
        # 测试初始化
        detector = DamageDetector(model_type="cnn")
        print("  ✓ 检测器初始化成功")
        
        # 测试检测（使用模拟数据）
        result = detector.detect("test_image.jpg")
        
        assert result["status"] == "success"
        assert "detections" in result
        print("  ✓ 检测功能正常")
        
        return True
        
    except Exception as e:
        print(f"  ✗ 测试失败：{e}")
        return False


def test_digital_twin():
    """测试 DigitalTwin 子技能"""
    print("\n[3/4] 测试 DigitalTwin...")
    
    try:
        from digital_twin.twinner import DigitalTwin
        
        # 测试初始化
        twin = DigitalTwin(model_type="rom")
        print("  ✓ 数字孪生初始化成功")
        
        # 测试模型构建
        result = twin.build_model(
            geometry={"type": "frame", "stories": 5},
            materials={"concrete": "C30", "steel": "HRB400"},
            boundary_conditions={"base": "fixed"}
        )
        
        assert result["status"] == "success"
        print("  ✓ 模型构建功能正常")
        
        # 测试状态更新
        state_result = twin.update_state({"sensor_1": 0.01, "sensor_2": 0.02})
        assert state_result["status"] == "success"
        print("  ✓ 状态更新功能正常")
        
        return True
        
    except Exception as e:
        print(f"  ✗ 测试失败：{e}")
        return False


def test_smart_monitor():
    """测试 SmartMonitor 子技能"""
    print("\n[4/4] 测试 SmartMonitor...")
    
    try:
        from smart_monitor.analyzer import MonitorAnalyzer
        import numpy as np
        
        # 测试初始化
        analyzer = MonitorAnalyzer()
        print("  ✓ 分析器初始化成功")
        
        # 测试特征提取
        test_data = np.random.randn(1000, 8)
        features = analyzer.extract_features(test_data)
        
        assert features["status"] == "success"
        assert "time_domain" in features
        assert "frequency_domain" in features
        print("  ✓ 特征提取功能正常")
        
        # 测试模态分析
        modal_result = analyzer.modal_analysis(test_data, fs=200.0)
        assert modal_result["status"] == "success"
        assert "modes" in modal_result
        print("  ✓ 模态分析功能正常")
        
        return True
        
    except Exception as e:
        print(f"  ✗ 测试失败：{e}")
        return False


if __name__ == "__main__":
    success = test_all()
    sys.exit(0 if success else 1)
