#!/usr/bin/env python3
"""
Annotation Visualizer
Visualize bounding boxes on images
"""

import argparse
import json
import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from typing import Dict, List, Tuple, Optional


# Default colors for different classes
DEFAULT_COLORS = [
    (255, 0, 0),      # Red
    (0, 255, 0),      # Green
    (0, 0, 255),      # Blue
    (255, 255, 0),    # Yellow
    (255, 0, 255),   # Magenta
    (0, 255, 255),    # Cyan
    (255, 128, 0),    # Orange
    (128, 0, 255),    # Purple
    (255, 0, 128),    # Pink
    (128, 255, 0),    # Lime
]


def get_color(class_id: int, custom_colors: List[Tuple] = None) -> Tuple[int, int, int]:
    """Get color for a class"""
    if custom_colors and class_id < len(custom_colors):
        return custom_colors[class_id]
    return DEFAULT_COLORS[class_id % len(DEFAULT_COLORS)]


def parse_yolo_annotation(txt_path: str, img_width: int, img_height: int) -> List[Tuple]:
    """Parse YOLO format annotation"""
    annotations = []
    try:
        with open(txt_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) < 5:
                    continue
                
                class_id = int(parts[0])
                x_center = float(parts[1]) * img_width
                y_center = float(parts[2]) * img_height
                width = float(parts[3]) * img_width
                height = float(parts[4]) * img_height
                
                # Convert to corner coordinates
                x1 = int(x_center - width / 2)
                y1 = int(y_center - height / 2)
                x2 = int(x_center + width / 2)
                y2 = int(y_center + height / 2)
                
                annotations.append((class_id, x1, y1, x2, y2))
    except:
        pass
    return annotations


def parse_coco_annotation(coco_data: Dict, img_id: int, img_width: int, img_height: int) -> List[Tuple]:
    """Parse COCO format annotation"""
    annotations = []
    
    # Find image info
    images = {img['id']: img for img in coco_data.get('images', [])}
    img_info = images.get(img_id, {})
    
    # Get annotations for this image
    for ann in coco_data.get('annotations', []):
        if ann.get('image_id') != img_id:
            continue
        
        class_id = ann.get('category_id', 1) - 1  # COCO is 1-indexed
        bbox = ann.get('bbox', [0, 0, 0, 0])
        
        x1 = int(bbox[0])
        y1 = int(bbox[1])
        x2 = int(bbox[0] + bbox[2])
        y2 = int(bbox[1] + bbox[3])
        
        annotations.append((class_id, x1, y1, x2, y2))
    
    return annotations


def parse_voc_annotation(xml_path: str) -> List[Tuple]:
    """Parse VOC XML annotation"""
    annotations = []
    try:
        import xml.etree.ElementTree as ET
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        size = root.find('size')
        if size is not None:
            img_width = int(size.findtext('width', 0))
            img_height = int(size.findtext('height', 0))
        
        for obj in root.findall('object'):
            class_name = obj.findtext('name', 'object')
            bbox = obj.find('bndbox')
            
            if bbox is not None:
                xmin = int(float(bbox.findtext('xmin', 0)))
                ymin = int(float(bbox.findtext('ymin', 0)))
                xmax = int(float(bbox.findtext('xmax', 0)))
                ymax = int(float(bbox.findtext('ymax', 0)))
                
                annotations.append((0, xmin, ymin, xmax, ymax))
    except:
        pass
    
    return annotations


def parse_labelme_annotation(json_path: str) -> List[Tuple]:
    """Parse LabelMe JSON annotation"""
    annotations = []
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        for shape in data.get('shapes', []):
            points = shape.get('points', [])
            if len(points) < 2:
                continue
            
            xs = [p[0] for p in points]
            ys = [p[1] for p in points]
            
            x1 = int(min(xs))
            y1 = int(min(ys))
            x2 = int(max(xs))
            y2 = int(max(ys))
            
            annotations.append((0, x1, y1, x2, y2))
    except:
        pass
    
    return annotations


def visualize_image(image_path: str, annotations: List[Tuple], 
                   output_path: str, color: Tuple = (255, 0, 0),
                   thickness: int = 2, fill: bool = False,
                   show_label: bool = True, font_size: int = 16,
                   class_names: List[str] = None):
    """Draw bounding boxes on image"""
    try:
        img = Image.open(image_path).convert('RGB')
        draw = ImageDraw.Draw(img)
        
        # Try to load font, fallback to default
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        for i, (class_id, x1, y1, x2, y2) in enumerate(annotations):
            box_color = get_color(class_id)
            
            # Draw box
            if fill:
                draw.rectangle([x1, y1, x2, y2], outline=box_color, fill=box_color + (128,))
            else:
                draw.rectangle([x1, y1, x2, y2], outline=box_color, width=thickness)
            
            # Draw label
            if show_label:
                label = class_names[class_id] if class_names and class_id < len(class_names) else f"class_{class_id}"
                label_text = f" {label}"
                
                # Draw label background
                text_bbox = draw.textbbox((x1, y1), label_text, font=font)
                draw.rectangle(text_bbox, fill=box_color)
                draw.text((x1, y1), label_text, fill=(255, 255, 255), font=font)
        
        # Save
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
        img.save(output_path)
        return True
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return False


def cmd_yolo(args):
    """Visualize YOLO format"""
    images_dir = Path(args.images)
    labels_dir = Path(args.labels)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Parse colors
    colors = None
    if args.colors:
        colors = []
        for c in args.colors.split(','):
            c = c.strip()
            if c.isdigit():
                colors.append((int(c), 0, 0))
            elif c.startswith('#'):
                c = c[1:]
                colors.append(tuple(int(c[i:i+2], 16) for i in (0, 2, 4)))
    
    # Find all images
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    image_files = []
    for ext in image_extensions:
        image_files.extend(images_dir.glob(f"*{ext}"))
        image_files.extend(images_dir.glob(f"*{ext.upper()}"))
    
    print(f"Processing {len(image_files)} images...")
    
    for img_path in image_files:
        base_name = img_path.stem
        label_path = labels_dir / f"{base_name}.txt"
        
        if not label_path.exists():
            continue
        
        # Get image size
        with Image.open(img_path) as img:
            width, height = img.size
        
        # Parse annotations
        annotations = parse_yolo_annotation(str(label_path), width, height)
        
        if not annotations:
            continue
        
        # Visualize
        output_path = output_dir / img_path.name
        visualize_image(
            str(img_path), annotations, str(output_path),
            thickness=args.thickness, fill=args.fill,
            show_label=args.show_label, font_size=args.font_size
        )
        print(f"✓ {img_path.name} -> {output_path}")


def cmd_coco(args):
    """Visualize COCO format"""
    # Load COCO JSON
    with open(args.annotation, 'r') as f:
        coco_data = json.load(f)
    
    images_dir = Path(args.images)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Build image index
    images = {img['id']: img for img in coco_data.get('images', [])}
    
    # Group annotations by image
    by_image = {}
    for ann in coco_data.get('annotations', []):
        img_id = ann['image_id']
        if img_id not in by_image:
            by_image[img_id] = []
        by_image[img_id].append(ann)
    
    print(f"Processing {len(by_image)} images...")
    
    for img_id, anns in by_image.items():
        img_info = images.get(img_id, {})
        img_name = img_info.get('file_name', f'{img_id}.jpg')
        img_path = images_dir / img_name
        
        if not img_path.exists():
            continue
        
        # Get image size
        with Image.open(img_path) as img:
            width, height = img.size
        
        # Parse annotations
        annotations = []
        for ann in anns:
            class_id = ann.get('category_id', 1) - 1
            bbox = ann.get('bbox', [0, 0, 0, 0])
            x1 = int(bbox[0])
            y1 = int(bbox[1])
            x2 = int(bbox[0] + bbox[2])
            y2 = int(bbox[1] + bbox[3])
            annotations.append((class_id, x1, y1, x2, y2))
        
        if not annotations:
            continue
        
        # Visualize
        output_path = output_dir / img_name
        visualize_image(
            str(img_path), annotations, str(output_path),
            thickness=args.thickness, fill=args.fill,
            show_label=args.show_label, font_size=args.font_size
        )
        print(f"✓ {img_name} -> {output_path}")


def cmd_voc(args):
    """Visualize VOC format"""
    import xml.etree.ElementTree as ET
    
    xml_dir = Path(args.annotations)
    images_dir = Path(args.images)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all XML files
    xml_files = list(xml_dir.glob("*.xml"))
    
    print(f"Processing {len(xml_files)} images...")
    
    for xml_path in xml_files:
        base_name = xml_path.stem
        img_path = None
        
        # Find image
        for ext in ['.jpg', '.jpeg', '.png', '.bmp']:
            potential = images_dir / (base_name + ext)
            if potential.exists():
                img_path = potential
                break
        
        if not img_path:
            continue
        
        # Parse annotations
        annotations = parse_voc_annotation(str(xml_path))
        
        if not annotations:
            continue
        
        # Visualize
        output_path = output_dir / img_path.name
        visualize_image(
            str(img_path), annotations, str(output_path),
            thickness=args.thickness, fill=args.fill,
            show_label=args.show_label, font_size=args.font_size
        )
        print(f"✓ {img_path.name} -> {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Annotation Visualizer - Visualize bounding boxes on images"
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # yolo command
    parser_yolo = subparsers.add_parser("yolo", help="Visualize YOLO format")
    parser_yolo.add_argument("images", help="Images directory")
    parser_yolo.add_argument("labels", help="YOLO labels directory")
    parser_yolo.add_argument("output", help="Output directory")
    parser_yolo.add_argument("--colors", help="Comma-separated colors")
    parser_yolo.add_argument("--thickness", "-t", type=int, default=2, help="Box thickness")
    parser_yolo.add_argument("--fill", action="store_true", help="Fill boxes")
    parser_yolo.add_argument("--show-label", action="store_true", default=True, help="Show labels")
    parser_yolo.add_argument("--font-size", type=int, default=16, help="Font size")
    parser_yolo.set_defaults(func=cmd_yolo)
    
    # coco command
    parser_coco = subparsers.add_parser("coco", help="Visualize COCO format")
    parser_coco.add_argument("annotation", help="COCO JSON file")
    parser_coco.add_argument("images", help="Images directory")
    parser_coco.add_argument("output", help="Output directory")
    parser_coco.add_argument("--colors", help="Comma-separated colors")
    parser_coco.add_argument("--thickness", "-t", type=int, default=2, help="Box thickness")
    parser_coco.add_argument("--fill", action="store_true", help="Fill boxes")
    parser_coco.add_argument("--show-label", action="store_true", default=True, help="Show labels")
    parser_coco.add_argument("--font-size", type=int, default=16, help="Font size")
    parser_coco.set_defaults(func=cmd_coco)
    
    # voc command
    parser_voc = subparsers.add_parser("voc", help="Visualize VOC format")
    parser_voc.add_argument("annotations", help="VOC XML directory")
    parser_voc.add_argument("images", help="Images directory")
    parser_voc.add_argument("output", help="Output directory")
    parser_voc.add_argument("--thickness", "-t", type=int, default=2, help="Box thickness")
    parser_voc.add_argument("--fill", action="store_true", help="Fill boxes")
    parser_voc.add_argument("--show-label", action="store_true", default=True, help="Show labels")
    parser_voc.add_argument("--font-size", type=int, default=16, help="Font size")
    parser_voc.set_defaults(func=cmd_voc)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        return
    
    try:
        args.func(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
