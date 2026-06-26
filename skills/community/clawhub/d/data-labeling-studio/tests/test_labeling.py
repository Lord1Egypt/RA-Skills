#!/usr/bin/env python3
"""
Data Labeling Studio - Unit Tests | 单元测试
"""

import unittest
import tempfile
import os
import json


class MockImageAnnotator:
    """Mock implementation for testing"""
    
    def __init__(self, annotation_type, labels, output_format="coco"):
        self.annotation_type = annotation_type
        self.labels = labels
        self.output_format = output_format
        self.active_learning = False
    
    def configure_active_learning(self, enabled, uncertainty_threshold=0.7, sample_batch_size=10):
        self.active_learning = enabled
        self.uncertainty_threshold = uncertainty_threshold
        self.sample_batch_size = sample_batch_size
    
    def annotate(self, image_dir, output_file, pre_annotate=False):
        # Mock annotations
        annotations = [
            {"id": 1, "file": "img1.jpg", "annotations": [{"label": "person", "bbox": [10, 10, 50, 50]}]},
            {"id": 2, "file": "img2.jpg", "annotations": [{"label": "car", "bbox": [20, 20, 100, 80]}]}
        ]
        
        # Save to file
        with open(output_file, 'w') as f:
            json.dump(annotations, f)
        
        return annotations


class MockTextAnnotator:
    """Mock implementation for testing"""
    
    def __init__(self, annotation_task, labels):
        self.annotation_task = annotation_task
        self.labels = labels
    
    def annotate(self, text_data, output_file, format="json"):
        # Mock annotations
        annotations = [
            {"id": 1, "text": "Sample text", "label": "PERSON"},
            {"id": 2, "text": "Another sample", "label": "ORG"}
        ]
        
        with open(output_file, 'w') as f:
            json.dump(annotations, f)
        
        return annotations


class MockQualityChecker:
    """Mock implementation for testing"""
    
    def check(self, annotations, ground_truth=None, metrics=None):
        # Mock quality report
        report = {
            "iou": 0.85,
            "consistency": 0.92,
            "coverage": 0.95,
            "accuracy": 0.88
        }
        return report


class TestImageAnnotator(unittest.TestCase):
    """Test image annotation functionality"""
    
    def test_annotator_creation(self):
        """Test annotator initialization"""
        annotator = MockImageAnnotator("bounding_box", ["person", "car"])
        self.assertEqual(annotator.annotation_type, "bounding_box")
        self.assertEqual(annotator.labels, ["person", "car"])
        self.assertEqual(annotator.output_format, "coco")
    
    def test_different_annotation_types(self):
        """Test different annotation types"""
        types = ["bounding_box", "polygon", "keypoint", "segmentation"]
        for ann_type in types:
            annotator = MockImageAnnotator(ann_type, ["label"])
            self.assertEqual(annotator.annotation_type, ann_type)
    
    def test_active_learning_config(self):
        """Test active learning configuration"""
        annotator = MockImageAnnotator("bounding_box", ["person"])
        annotator.configure_active_learning(enabled=True, uncertainty_threshold=0.8, sample_batch_size=20)
        
        self.assertTrue(annotator.active_learning)
        self.assertEqual(annotator.uncertainty_threshold, 0.8)
        self.assertEqual(annotator.sample_batch_size, 20)
    
    def test_annotate(self):
        """Test image annotation"""
        with tempfile.TemporaryDirectory() as tmpdir:
            annotator = MockImageAnnotator("bounding_box", ["person", "car"])
            output_file = os.path.join(tmpdir, "annotations.json")
            
            annotations = annotator.annotate("./images", output_file)
            
            self.assertEqual(len(annotations), 2)
            self.assertTrue(os.path.exists(output_file))


class TestTextAnnotator(unittest.TestCase):
    """Test text annotation functionality"""
    
    def test_annotator_creation(self):
        """Test annotator initialization"""
        annotator = MockTextAnnotator("ner", ["PERSON", "ORG"])
        self.assertEqual(annotator.annotation_task, "ner")
        self.assertEqual(annotator.labels, ["PERSON", "ORG"])
    
    def test_different_tasks(self):
        """Test different annotation tasks"""
        tasks = ["classification", "ner", "sentiment", "summarization"]
        for task in tasks:
            annotator = MockTextAnnotator(task, ["label"])
            self.assertEqual(annotator.annotation_task, task)
    
    def test_annotate(self):
        """Test text annotation"""
        with tempfile.TemporaryDirectory() as tmpdir:
            annotator = MockTextAnnotator("ner", ["PERSON", "ORG"])
            output_file = os.path.join(tmpdir, "annotations.json")
            
            annotations = annotator.annotate("./texts.txt", output_file)
            
            self.assertEqual(len(annotations), 2)
            self.assertTrue(os.path.exists(output_file))


class TestQualityChecker(unittest.TestCase):
    """Test quality checking functionality"""
    
    def test_quality_check(self):
        """Test quality check with metrics"""
        checker = MockQualityChecker()
        report = checker.check(
            annotations="./annotations.json",
            ground_truth="./gt.json",
            metrics=["iou", "consistency"]
        )
        
        self.assertIn("iou", report)
        self.assertIn("consistency", report)
        self.assertGreaterEqual(report["iou"], 0)
        self.assertLessEqual(report["iou"], 1)
    
    def test_quality_thresholds(self):
        """Test quality score ranges"""
        checker = MockQualityChecker()
        report = checker.check("./annotations.json")
        
        for metric, score in report.items():
            self.assertGreaterEqual(score, 0)
            self.assertLessEqual(score, 1)


class TestOutputFormats(unittest.TestCase):
    """Test output format support"""
    
    def test_image_formats(self):
        """Test image annotation output formats"""
        formats = ["coco", "pascal_voc", "yolo"]
        for fmt in formats:
            annotator = MockImageAnnotator("bounding_box", ["person"], output_format=fmt)
            self.assertEqual(annotator.output_format, fmt)


class TestLabels(unittest.TestCase):
    """Test label management"""
    
    def test_label_categories(self):
        """Test label category setup"""
        labels = ["person", "car", "dog", "cat", "bicycle"]
        annotator = MockImageAnnotator("bounding_box", labels)
        self.assertEqual(len(annotator.labels), 5)
    
    def test_ner_labels(self):
        """Test NER label setup"""
        labels = ["PERSON", "ORG", "LOC", "DATE", "PRODUCT"]
        annotator = MockTextAnnotator("ner", labels)
        self.assertEqual(annotator.labels, labels)


class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def test_complete_annotation_workflow(self):
        """Test complete annotation workflow"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create annotator with active learning
            annotator = MockImageAnnotator("bounding_box", ["person", "car", "dog"])
            annotator.configure_active_learning(enabled=True, uncertainty_threshold=0.7)
            
            # Annotate images
            output_file = os.path.join(tmpdir, "coco_annotations.json")
            annotations = annotator.annotate("./images", output_file, pre_annotate=True)
            
            # Verify annotations exist
            self.assertEqual(len(annotations), 2)
            self.assertTrue(os.path.exists(output_file))
            
            # Check quality
            checker = MockQualityChecker()
            report = checker.check(output_file)
            
            self.assertGreater(report["iou"], 0)
            self.assertGreater(report["consistency"], 0)


if __name__ == "__main__":
    unittest.main()
