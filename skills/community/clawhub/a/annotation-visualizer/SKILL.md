# Annotation Visualizer

Visualize bounding boxes and labels on images. Supports COCO, YOLO, VOC, and LabelMe formats. Use when user wants to visualize annotations on images for quality checking or debugging.

## Features

- **Multi-format Support**: COCO, YOLO, VOC, LabelMe
- **Customizable Colors**: Per-class colors or auto-generated
- **Label Display**: Show class names and confidence
- **Box Styles**: Filled or outline boxes
- **Batch Processing**: Visualize entire dataset

## Usage

```bash
# Visualize YOLO annotations
python scripts/visualize.py yolo images/ labels/ output/

# Visualize COCO annotations
python scripts/visualize.py coco annotations.json images/ output/

# Custom colors and styles
python scripts/visualize.py yolo images/ labels/ output/ \
  --colors red,green,blue \
  --thickness 2 \
  --fill
```

## Examples

```
$ python scripts/visualize.py yolo ./images ./labels ./output

Processing 100 images...
✓ Saved visualization for image1.jpg -> output/image1.jpg
✓ Saved visualization for image2.jpg -> output/image2.jpg
...
```

## Supported Formats

| Format | Input | Description |
|--------|-------|-------------|
| YOLO | .txt | YOLO darknet format |
| COCO | .json | COCO JSON annotation |
| VOC | .xml | Pascal VOC XML |
| LabelMe | .json | LabelMe JSON |

## Installation

```bash
pip install pillow
```

## Options

- `--colors`: Comma-separated colors for each class
- `--thickness`: Box line thickness (default: 2)
- `--fill`: Fill boxes with semi-transparent color
- `--show-label`: Show class labels on boxes
- `--font-size`: Label font size (default: 16)
