"""
Anomalib 工业异常检测 - 基础使用示例
=====================================

本示例展示如何使用 anomalib-detector 进行工业产品缺陷检测。
运行前请确保已安装: pip install anomalib
"""

import os
import cv2
import numpy as np
from pathlib import Path

# ============================================================
# 示例 1: 快速开始 - 使用 Patchcore 模型
# ============================================================

def quick_start_patchcore():
    """Patchcore 模型快速使用"""
    from anomalib.data import MVTecAD
    from anomalib.models import Patchcore
    from anomalib.engine import Engine
    
    print("=" * 50)
    print("示例 1: Patchcore 快速开始")
    print("=" * 50)
    
    # 1. 准备数据
    print("\n[1] 准备 MVTecAD bottle 数据集...")
    datamodule = MVTecAD(
        category="bottle",
        root="./datasets/MVTecAD",
        image_size=(256, 256)
    )
    datamodule.setup()  # 下载并准备数据
    
    # 2. 创建模型
    print("\n[2] 创建 Patchcore 模型...")
    model = Patchcore(
        pre_trained=True,
        backbone="wide_resnet50_2",
        layers=["layer2", "layer3"],
        coreset_sampling_ratio=0.1
    )
    print(f"    骨干网络: {model.backbone}")
    print(f"    特征层: {model.layers}")
    
    # 3. 训练
    print("\n[3] 开始训练...")
    engine = Engine(
        max_epochs=1,  # 演示用，实际需要更多 epochs
        devices=1,
        accelerator="cpu"
    )
    # engine.fit(model=model, datamodule=datamodule)
    print("    (训练代码已注释，实际运行请取消注释)")
    
    # 4. 预测
    print("\n[4] 运行预测...")
    # predictions = engine.predict(model=model, datamodule=datamodule)
    print("    (预测代码已注释)")
    
    print("\n✅ 示例 1 完成!")


# ============================================================
# 示例 2: Padim 模型（特征融合）
# ============================================================

def example_padim():
    """Padim 模型使用示例 - 适合纹理缺陷检测"""
    from anomalib.models import Padim
    
    print("\n" + "=" * 50)
    print("示例 2: Padim 模型")
    print("=" * 50)
    
    # Padim 使用预计算的特征统计
    model = Padim(
        backbone="resnet18",
        layers=["layer1", "layer2", "layer3"],
        pre_trained=True
    )
    
    print(f"    骨干网络: {model.backbone}")
    print(f"    特征层: {model.layers}")
    print("    Padim 特点: 使用多层特征统计，适合纹理类缺陷")
    
    print("\n✅ 示例 2 完成!")


# ============================================================
# 示例 3: 自定义数据集
# ============================================================

def example_custom_dataset():
    """使用自定义数据集进行检测"""
    from anomalib.data import Folder
    
    print("\n" + "=" * 50)
    print("示例 3: 自定义数据集")
    print("=" * 50)
    
    # 目录结构:
    # dataset/
    #   ├── train/
    #   │   └── normal/           # 正常训练样本
    #   ├── test/
    #   │   ├── normal/           # 正常测试样本
    #   │   └── abnormal/         # 异常测试样本
    #   └── ground_truth/
    #       └── abnormal/         # 分割标注（可选）
    
    datamodule = Folder(
        name="custom_products",
        root="./my_dataset",
        normal_dir="train/normal",
        abnormal_dir="test/abnormal",
        mask_dir="ground_truth/abnormal",
        normal_split_ratio=0.2,  # 20% 作为验证集
        image_size=(256, 256)
    )
    
    print("    数据集: custom_products")
    print("    正常目录: train/normal")
    print("    异常目录: test/abnormal")
    print("    分割标注: ground_truth/abnormal")
    print("    图像尺寸: 256x256")
    
    print("\n✅ 示例 3 完成!")


# ============================================================
# 示例 4: 推理与结果处理
# ============================================================

def example_inference():
    """推理与结果可视化"""
    print("\n" + "=" * 50)
    print("示例 4: 推理与可视化")
    print("=" * 50)
    
    # 模拟检测结果
    class MockResult:
        def __init__(self):
            self.image_path = "product_001.jpg"
            self.is_anomaly = True
            self.anomaly_score = 0.73
            self.heatmap = np.random.rand(256, 256)
            self.pred_mask = np.random.randint(0, 2, (256, 256))
    
    result = MockResult()
    
    print(f"\n[检测结果]")
    print(f"    图片: {result.image_path}")
    print(f"    异常判定: {'是 ⚠️' if result.is_anomaly else '否 ✅'}")
    print(f"    异常分数: {result.anomaly_score:.3f} (阈值: 0.5)")
    print(f"    热力图尺寸: {result.heatmap.shape}")
    print(f"    分割掩码尺寸: {result.pred_mask.shape}")
    
    # 实际使用时的代码:
    # result = detector.detect("path/to/image.jpg")
    # 
    # # 保存热力图
    # cv2.imwrite("heatmap.jpg", (result.heatmap * 255).astype(np.uint8))
    # 
    # # 叠加显示
    # image = cv2.imread(result.image_path)
    # heatmap_color = cv2.applyColorMap((result.heatmap * 255).astype(np.uint8), cv2.COLORMAP_JET)
    # overlay = cv2.addWeighted(image, 0.7, heatmap_color, 0.3, 0)
    # cv2.imwrite("overlay.jpg", overlay)
    
    print("\n✅ 示例 4 完成!")


# ============================================================
# 示例 5: 批量检测
# ============================================================

def example_batch_detection():
    """批量检测处理"""
    print("\n" + "=" * 50)
    print("示例 5: 批量检测")
    print("=" * 50)
    
    # 模拟批量处理结果
    results = [
        {"file": "bottle_001.jpg", "score": 0.12, "anomaly": False},
        {"file": "bottle_002.jpg", "score": 0.89, "anomaly": True},
        {"file": "bottle_003.jpg", "score": 0.34, "anomaly": False},
        {"file": "bottle_004.jpg", "score": 0.95, "anomaly": True},
        {"file": "bottle_005.jpg", "score": 0.08, "anomaly": False},
    ]
    
    print("\n[批量检测结果]")
    print("-" * 40)
    print(f"{'文件名':<20} {'异常分数':<12} {'判定':<8}")
    print("-" * 40)
    
    total = len(results)
    anomalies = sum(1 for r in results if r["anomaly"])
    
    for r in results:
        status = "⚠️ 异常" if r["anomaly"] else "✅ 正常"
        print(f"{r['file']:<20} {r['score']:<12.2f} {status:<8}")
    
    print("-" * 40)
    print(f"总计: {total} 张, 异常: {anomalies} 张, 异常率: {anomalies/total*100:.1f}%")
    
    print("\n✅ 示例 5 完成!")


# ============================================================
# 主函数
# ============================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("   Anomalib 工业异常检测 - 使用示例")
    print("=" * 60)
    
    # 运行所有示例
    example_padim()
    example_custom_dataset()
    example_inference()
    example_batch_detection()
    
    # 跳过需要下载的快速开始
    print("\n" + "=" * 60)
    print("   所有示例执行完成!")
    print("=" * 60)
    print("\n💡 提示:")
    print("   - 示例 1 (quick_start_patchcore) 需要下载模型和数据")
    print("   - 运行前请确保网络连接正常")
    print("   - 完整训练示例请参考 SKILL.md 文档")
