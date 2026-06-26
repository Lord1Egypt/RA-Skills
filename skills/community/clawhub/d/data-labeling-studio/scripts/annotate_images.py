#!/usr/bin/env python3
"""
Image Annotation Tool | 图像标注工具
"""

import argparse
import json
import os
from pathlib import Path


class ImageAnnotator:
    """图像标注器"""
    
    def __init__(self, annotation_type, labels, output_format="coco"):
        self.annotation_type = annotation_type
        self.labels = labels
        self.output_format = output_format
        self.active_learning = False
        self.annotations = []
    
    def configure_active_learning(self, enabled=True, uncertainty_threshold=0.7, sample_batch_size=10):
        """配置主动学习"""
        self.active_learning = enabled
        self.uncertainty_threshold = uncertainty_threshold
        self.sample_batch_size = sample_batch_size
        print(f"🤖 Active learning: {'enabled' if enabled else 'disabled'}")
    
    def scan_images(self, image_dir):
        """扫描图像目录"""
        extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
        images = []
        for ext in extensions:
            images.extend(Path(image_dir).glob(f"*{ext}"))
            images.extend(Path(image_dir).glob(f"*{ext.upper()}"))
        return sorted(list(set(images)))
    
    def mock_annotate_image(self, image_path):
        """模拟图像标注（实际应使用标注界面或AI模型）"""
        import random
        
        # 模拟标注结果
        num_objects = random.randint(0, 3)
        annotations = []
        
        for _ in range(num_objects):
            label = random.choice(self.labels)
            if self.annotation_type == "bounding_box":
                # 模拟边界框 [x, y, width, height]
                bbox = [
                    random.randint(10, 200),
                    random.randint(10, 200),
                    random.randint(50, 150),
                    random.randint(50, 150)
                ]
                annotations.append({"label": label, "bbox": bbox})
            elif self.annotation_type == "polygon":
                # 模拟多边形
                annotations.append({"label": label, "polygon": [[10, 10], [50, 10], [50, 50], [10, 50]]})
            elif self.annotation_type == "keypoint":
                # 模拟关键点
                annotations.append({"label": label, "keypoints": [[30, 30], [40, 40]]})
        
        return annotations
    
    def annotate(self, image_dir, output_file, pre_annotate=False):
        """执行标注"""
        print(f"🏷️  Starting image annotation")
        print(f"   Directory: {image_dir}")
        print(f"   Type: {self.annotation_type}")
        print(f"   Labels: {', '.join(self.labels)}")
        print(f"   Format: {self.output_format}")
        
        # 扫描图像
        images = self.scan_images(image_dir)
        print(f"   Found {len(images)} images")
        
        if len(images) == 0:
            print("⚠️  No images found!")
            return []
        
        # 标注
        for idx, img_path in enumerate(images, 1):
            if idx % 10 == 0 or idx == 1:
                print(f"   Processing {idx}/{len(images)}: {img_path.name}")
            
            ann = self.mock_annotate_image(img_path)
            self.annotations.append({
                "id": idx,
                "file_name": img_path.name,
                "path": str(img_path),
                "annotations": ann
            })
        
        # 保存
        self._save_annotations(output_file)
        
        print(f"\n✅ Annotation completed!")
        print(f"   Total images: {len(images)}")
        print(f"   Output: {output_file}")
        
        return self.annotations
    
    def _save_annotations(self, output_file):
        """保存标注结果"""
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        if self.output_format == "coco":
            # COCO格式
            coco_format = {
                "images": [],
                "annotations": [],
                "categories": [{"id": i+1, "name": label} for i, label in enumerate(self.labels)]
            }
            ann_id = 1
            for img_ann in self.annotations:
                img_id = img_ann["id"]
                coco_format["images"].append({
                    "id": img_id,
                    "file_name": img_ann["file_name"]
                })
                for ann in img_ann["annotations"]:
                    label_id = self.labels.index(ann["label"]) + 1
                    coco_ann = {
                        "id": ann_id,
                        "image_id": img_id,
                        "category_id": label_id
                    }
                    if "bbox" in ann:
                        coco_ann["bbox"] = ann["bbox"]
                    if "polygon" in ann:
                        coco_ann["segmentation"] = [ann["polygon"]]
                    coco_format["annotations"].append(coco_ann)
                    ann_id += 1
            
            with open(output_file, 'w') as f:
                json.dump(coco_format, f, indent=2)
        else:
            with open(output_file, 'w') as f:
                json.dump(self.annotations, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Image Annotation Tool")
    parser.add_argument("--input", required=True, help="Image directory")
    parser.add_argument("--type", default="bounding_box", choices=["bounding_box", "polygon", "keypoint", "segmentation"], help="Annotation type")
    parser.add_argument("--labels", required=True, help="Comma-separated labels")
    parser.add_argument("--format", default="coco", choices=["coco", "pascal_voc", "yolo"], help="Output format")
    parser.add_argument("--output", required=True, help="Output annotation file")
    parser.add_argument("--active-learning", action="store_true", help="Enable active learning")
    parser.add_argument("--pre-annotate", action="store_true", help="Use model for pre-annotation")
    args = parser.parse_args()
    
    # 解析标签
    labels = [l.strip() for l in args.labels.split(",")]
    
    # 创建标注器
    annotator = ImageAnnotator(args.type, labels, args.format)
    
    if args.active_learning:
        annotator.configure_active_learning(enabled=True)
    
    # 执行标注
    annotator.annotate(args.input, args.output, pre_annotate=args.pre_annotate)


if __name__ == "__main__":
    main()
