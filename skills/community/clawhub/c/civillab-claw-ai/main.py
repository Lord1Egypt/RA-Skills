"""
CivilLabClaw-AI 主入口

使用方法：
    python main.py <skill_type> [options]
    
示例：
    python main.py ml_struct --test
    python main.py dl_damage --image test.jpg
    python main.py smart_monitor --data data.csv
"""

import argparse
import sys
from pathlib import Path

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))


def main():
    parser = argparse.ArgumentParser(description="CivilLabClaw-AI 技能包")
    parser.add_argument("skill", choices=["ml_struct", "dl_damage", "digital_twin", "smart_monitor"],
                        help="子技能类型")
    parser.add_argument("--test", action="store_true", help="运行测试")
    parser.add_argument("--image", type=str, help="输入图像路径")
    parser.add_argument("--data", type=str, help="输入数据路径")
    parser.add_argument("--config", type=str, help="配置文件路径")
    
    args = parser.parse_args()
    
    print(f"=== CivilLabClaw-AI ===")
    print(f"技能：{args.skill}")
    
    if args.test:
        run_test(args.skill)
    elif args.image:
        run_image_analysis(args.image)
    elif args.data:
        run_data_analysis(args.data)
    else:
        print("请指定 --test, --image, 或 --data 参数")


def run_test(skill_type: str):
    """运行测试"""
    print(f"\n运行 {skill_type} 测试...")
    
    if skill_type == "ml_struct":
        from ml_struct.predictor import StructuralPredictor
        predictor = StructuralPredictor()
        result = predictor.predict({})
        print(f"测试结果：{result['status']}")
        
    elif skill_type == "dl_damage":
        from dl_damage.detector import DamageDetector
        detector = DamageDetector()
        print(f"检测器初始化完成：{detector.model_type}")
        
    elif skill_type == "digital_twin":
        from digital_twin.twinner import DigitalTwin
        twin = DigitalTwin()
        print(f"数字孪生初始化完成：{twin.model_type}")
        
    elif skill_type == "smart_monitor":
        from smart_monitor.analyzer import MonitorAnalyzer
        analyzer = MonitorAnalyzer()
        print(f"监测分析器初始化完成")
    
    print("测试完成 ✓")


def run_image_analysis(image_path: str):
    """运行图像分析"""
    from dl_damage.detector import DamageDetector
    
    detector = DamageDetector()
    result = detector.detect(image_path)
    
    print(f"\n检测结果:")
    print(f"  损伤数量：{result['summary']['total_detections']}")
    print(f"  严重程度：{result['summary']['max_severity']}")
    
    for det in result['detections']:
        print(f"  - {det['type']}: 置信度 {det['confidence']:.2f}")


def run_data_analysis(data_path: str):
    """运行数据分析"""
    from smart_monitor.analyzer import MonitorAnalyzer
    
    analyzer = MonitorAnalyzer()
    result = analyzer.analyze(Path(data_path))
    
    print(f"\n分析结果:")
    print(f"  模态数量：{len(result['modal_parameters']['modes'])}")
    print(f"  异常数量：{result['anomalies']['summary']['total_anomalies']}")
    
    for mode in result['modal_parameters']['modes']:
        print(f"  - 模态 {mode['mode']}: {mode['frequency']:.2f} Hz")


if __name__ == "__main__":
    main()
