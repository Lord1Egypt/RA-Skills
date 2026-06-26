# Data Labeling Studio

## Metadata
- **Name**: data-labeling-studio
- **Display Name**: Data Labeling Studio | 数据标注工作室
- **Description**: 
  - EN: Intelligent data labeling and annotation toolkit supporting image, text, audio, and video with active learning and quality control.
  - ZH: 智能数据标注和注释工具包，支持图像、文本、音频和视频，包含主动学习和质量控制。
- **Version**: 1.0.0
- **Author**: Kimi Claw
- **Tags**: data-labeling, annotation, image-annotation, text-annotation, active-learning, quality-control, dataset, ml-training
- **Category**: Data Processing
- **Icon**: 🏷️

## Capabilities

### Actions

#### image_annotate
Perform image annotation
- **image_dir**: Image directory path (string, required)
- **annotation_type**: Type of annotation (string, required) - bounding_box, polygon, keypoint, segmentation
- **labels**: Label categories (array, required)
- **output_format**: Output format (string) - coco, pascal_voc, yolo
- **active_learning**: Enable active learning suggestions (boolean, default: true)

#### text_annotate
Perform text annotation
- **text_data**: Text data source (string/object, required)
- **annotation_task**: Task type (string, required) - classification, ner, sentiment, summarization
- **labels**: Label categories (array, required)
- **output_format**: Output format (string) - json, csv, spacy

#### audio_annotate
Perform audio annotation
- **audio_dir**: Audio directory path (string, required)
- **annotation_type**: Type (string, required) - transcription, speaker_id, emotion, event
- **segment_duration**: Segment duration in seconds (float, default: 5.0)

#### video_annotate
Perform video annotation
- **video_path**: Video file path (string, required)
- **annotation_type**: Type (string, required) - object_tracking, action_recognition, scene_detection
- **frame_sample_rate**: Frame sampling rate (int, default: 1)

#### quality_check
Check annotation quality and consistency
- **annotations**: Annotation file path (string, required)
- **ground_truth**: Ground truth file path (string, optional)
- **metrics**: Quality metrics (array) - iou, accuracy, consistency, coverage

#### dataset_export
Export labeled dataset to ML format
- **annotations**: Annotation source (string, required)
- **format**: Target format (string, required) - coco, yolo, tfrecord, huggingface
- **output_dir**: Output directory (string, required)
- **split_ratios**: Train/val/test split (object) - {train: 0.8, val: 0.1, test: 0.1}

## Requirements
- Python 3.8+
- Pillow >= 10.0.0 (for image processing)
- OpenCV >= 4.8.0 (for image/video annotation)
- NumPy >= 1.24.0
- Pandas >= 2.0.0
- LabelImg >= 1.8.0 (optional)
- Librosa >= 0.10.0 (for audio processing)
- scikit-learn >= 1.3.0 (for active learning)

## Examples

### Image Annotation
```python
from labeling_studio import ImageAnnotator

# Initialize annotator
annotator = ImageAnnotator(
    annotation_type="bounding_box",
    labels=["person", "car", "dog", "cat"],
    output_format="coco"
)

# Annotate images with active learning
annotator.annotate(
    image_dir="./images",
    output_file="./annotations/coco.json",
    active_learning=True  # AI suggests uncertain samples
)

# Export to YOLO format
annotator.export("./annotations", format="yolo")
```

### Text Annotation
```python
from labeling_studio import TextAnnotator

# NER annotation
annotator = TextAnnotator(
    annotation_task="ner",
    labels=["PERSON", "ORG", "LOC", "DATE"]
)

# Annotate from file
annotations = annotator.annotate(
    text_data="./data/corpus.txt",
    output_file="./annotations/ner.json"
)
```

### Quality Check
```python
from labeling_studio import QualityChecker

# Check annotation quality
checker = QualityChecker()
report = checker.check(
    annotations="./annotations/coco.json",
    ground_truth="./annotations/ground_truth.json",
    metrics=["iou", "consistency", "coverage"]
)

print(f"Average IoU: {report['iou']:.2f}")
print(f"Consistency Score: {report['consistency']:.2f}")
print(f"Coverage: {report['coverage']:.2f}")
```

## Scripts
- `scripts/annotate_images.py`: 图像标注工具
- `scripts/annotate_text.py`: 文本标注工具
- `scripts/annotate_audio.py`: 音频标注工具
- `scripts/annotate_video.py`: 视频标注工具
- `scripts/quality_check.py`: 质量检查工具
- `scripts/export_dataset.py`: 数据集导出工具

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
# Image annotation with active learning
python scripts/annotate_images.py --input ./images --type bbox --labels person,car --format coco

# Text NER annotation
python scripts/annotate_text.py --input ./texts.txt --task ner --labels PERSON,ORG,LOC

# Quality check
python scripts/quality_check.py --annotations ./coco.json --ground-truth ./gt.json

# Export to YOLO
python scripts/export_dataset.py --input ./coco.json --format yolo --output ./yolo_dataset
```

## License
MIT License
