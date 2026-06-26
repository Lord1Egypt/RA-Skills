"""
批量产品检测示例
================

展示如何使用 anomalib-detector 进行大规模产品缺陷检测。
"""

import os
import time
import json
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Optional
import numpy as np
import cv2


@dataclass
class BatchDetectionResult:
    """批量检测结果"""
    total: int = 0
    normal: int = 0
    anomaly: int = 0
    anomaly_rate: float = 0.0
    avg_score: float = 0.0
    max_score: float = 0.0
    min_score: float = 0.0
    processing_time: float = 0.0
    details: List[dict] = None
    
    def __post_init__(self):
        if self.details is None:
            self.details = []
    
    def summary(self) -> dict:
        """返回汇总信息"""
        return asdict(self)


class BatchDetector:
    """批量检测器"""
    
    def __init__(self, model_name: str = "patchcore", threshold: float = 0.5):
        self.model_name = model_name
        self.threshold = threshold
        self.results = []
        
    def detect_folder(self, folder_path: str, output_dir: Optional[str] = None) -> BatchDetectionResult:
        """检测文件夹中的所有图片"""
        folder = Path(folder_path)
        image_extensions = {".jpg", ".jpeg", ".png", ".bmp"}
        
        # 获取所有图片
        image_files = [
            f for f in folder.rglob("*") 
            if f.suffix.lower() in image_extensions
        ]
        
        print(f"找到 {len(image_files)} 张图片")
        
        start_time = time.time()
        scores = []
        
        for img_path in image_files:
            # 实际使用时:
            # result = self._detect_single(img_path)
            result = {
                "file": str(img_path),
                "score": np.random.random(),  # 模拟分数
                "anomaly": False
            }
            result["anomaly"] = result["score"] > self.threshold
            
            self.results.append(result)
            scores.append(result["score"])
            
            if result["anomaly"]:
                print(f"  ⚠️ {img_path.name}: {result['score']:.3f}")
        
        processing_time = time.time() - start_time
        scores = np.array(scores)
        
        # 生成汇总
        batch_result = BatchDetectionResult(
            total=len(scores),
            normal=int(np.sum(scores <= self.threshold)),
            anomaly=int(np.sum(scores > self.threshold)),
            anomaly_rate=float(np.sum(scores > self.threshold) / len(scores)),
            avg_score=float(np.mean(scores)),
            max_score=float(np.max(scores)),
            min_score=float(np.min(scores)),
            processing_time=processing_time,
            details=self.results
        )
        
        return batch_result
    
    def save_report(self, result: BatchDetectionResult, output_path: str):
        """保存检测报告"""
        report = result.summary()
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n报告已保存: {output_path}")


def main():
    """主函数"""
    print("=" * 60)
    print("   批量产品检测示例")
    print("=" * 60)
    
    # 初始化检测器
    detector = BatchDetector(
        model_name="patchcore",
        threshold=0.5
    )
    
    # 检测目录（替换为实际路径）
    test_folder = "./test_products"
    
    # 如果目录不存在，创建模拟数据
    if not os.path.exists(test_folder):
        os.makedirs(test_folder, exist_ok=True)
        print(f"\n📁 创建测试目录: {test_folder}")
        print("   (实际使用时替换为真实产品图片目录)")
    
    # 执行检测
    print(f"\n🔍 开始检测: {test_folder}")
    result = detector.detect_folder(test_folder)
    
    # 输出汇总
    print("\n" + "=" * 60)
    print("   检测汇总")
    print("=" * 60)
    print(f"  总计图片: {result.total}")
    print(f"  正常产品: {result.normal}")
    print(f"  异常产品: {result.anomaly}")
    print(f"  异常率:   {result.anomaly_rate:.1%}")
    print(f"  平均分数: {result.avg_score:.3f}")
    print(f"  最高分数: {result.max_score:.3f}")
    print(f"  处理时间: {result.processing_time:.2f}s")
    
    # 保存报告
    report_path = "./detection_report.json"
    detector.save_report(result, report_path)


if __name__ == "__main__":
    main()
