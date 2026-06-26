#!/usr/bin/env python3
"""
Data Labeling Studio - Basic Usage Example | 基础使用示例
"""

from labeling_studio import ImageAnnotator, TextAnnotator, QualityChecker


def image_annotation_example():
    """Image bounding box annotation example"""
    # Initialize image annotator
    annotator = ImageAnnotator(
        annotation_type="bounding_box",
        labels=["person", "car", "dog", "cat", "bicycle"],
        output_format="coco"
    )
    
    # Configure active learning
    annotator.configure_active_learning(
        enabled=True,
        uncertainty_threshold=0.7,
        sample_batch_size=10
    )
    
    # Annotate images
    annotations = annotator.annotate(
        image_dir="./images",
        output_file="./annotations/coco_instances.json",
        pre_annotate=True  # Use model for initial suggestions
    )
    
    print(f"✅ Annotated {len(annotations)} images")


def text_ner_example():
    """Text NER annotation example"""
    # Initialize text annotator for NER
    annotator = TextAnnotator(
        annotation_task="ner",
        labels=["PERSON", "ORG", "LOC", "DATE", "PRODUCT"]
    )
    
    # Annotate from file
    annotations = annotator.annotate(
        text_data="./data/corpus.txt",
        output_file="./annotations/ner_labels.json",
        format="json"
    )
    
    print(f"✅ Annotated {len(annotations)} text samples")


def quality_check_example():
    """Annotation quality check example"""
    # Initialize quality checker
    checker = QualityChecker()
    
    # Run quality check
    report = checker.check(
        annotations="./annotations/coco.json",
        ground_truth="./annotations/ground_truth.json",
        metrics=["iou", "consistency", "coverage", "accuracy"]
    )
    
    print("✅ Quality Check Report")
    print("-" * 30)
    print(f"IoU (Intersection over Union): {report['iou']:.3f}")
    print(f"Consistency Score: {report['consistency']:.3f}")
    print(f"Coverage: {report['coverage']:.1%}")
    print(f"Accuracy: {report['accuracy']:.3f}")


if __name__ == "__main__":
    print("🏷️ Data Labeling Studio - Basic Examples")
    print("=" * 50)
    
    print("Example 1: Image Annotation")
    print("-" * 30)
    print("See image_annotation_example() function above")
    
    print("\nExample 2: Text NER Annotation")
    print("-" * 30)
    print("See text_ner_example() function above")
    
    print("\nExample 3: Quality Check")
    print("-" * 30)
    print("See quality_check_example() function above")
    
    print("\n✨ Examples completed!")
