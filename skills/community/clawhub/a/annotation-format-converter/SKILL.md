# Annotation Format Converter

Convert annotation formats between COCO, YOLO, VOC, and LabelMe. Use when user needs to convert annotation files between different formats for computer vision tasks.

## Features

- **COCO → YOLO**: Convert COCO JSON to YOLO txt format
- **YOLO → COCO**: Convert YOLO txt to COCO JSON
- **VOC → COCO**: Convert Pascal VOC XML to COCO JSON
- **LabelMe → COCO**: Convert LabelMe JSON to COCO JSON
- **Auto-detect**: Automatically detect input format
- **Batch Convert**: Convert entire folders

## Usage

```bash
# Convert COCO JSON to YOLO
python scripts/converter.py coco2yolo input.json output_dir/

# Convert YOLO txt to COCO
python scripts/converter.py yolo2coco input_dir/ output.json

# Convert VOC XML to COCO
python scripts/converter.py voc2coco input_dir/ output.json

# Auto-detect and convert
python scripts/converter.py convert input.json output.json --from coco --to yolo

# List supported formats
python scripts/converter.py formats
```

## Supported Formats

| Format | Extension | Description |
|--------|-----------|-------------|
| COCO | .json | COCO JSON annotation |
| YOLO | .txt | YOLO darknet format |
| VOC | .xml | Pascal VOC XML |
| LabelMe | .json | LabelMe JSON |

## Examples

### COCO to YOLO
```
$ python scripts/converter.py coco2yolo annotations.json yolo_labels/

Converting COCO to YOLO...
✓ Converted 150 annotations to yolo_labels/
```

### YOLO to COCO
```
$ python scripts/converter.py yolo2coco labels/ output.json --image-dir images/

Converting YOLO to COCO...
✓ Converted 150 annotations to output.json
```

## Installation

```bash
pip install pillow tqdm
```

## Requirements

- Python 3.8+
- Pillow (for image dimensions)
- tqdm (for progress bar)
