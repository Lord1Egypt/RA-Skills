#!/usr/bin/env python3
"""
Annotation Format Converter
Convert between COCO, YOLO, VOC, and LabelMe formats
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from PIL import Image

# Simple progress indicator
def tqdm(iterable, desc=""):
    """Simple progress indicator"""
    items = list(iterable)
    total = len(items)
    for i, item in enumerate(items):
        if i % max(1, total // 10) == 0:
            print(f"{desc}: {i}/{total}")
        yield item
    print(f"{desc}: {total}/{total}")


def get_image_dimensions(image_path: str) -> tuple:
    """Get image width and height"""
    try:
        with Image.open(image_path) as img:
            return img.width, img.height
    except:
        return 0, 0


def coco_to_yolo(coco_json: Dict, output_dir: str, image_dir: str = "") -> int:
    """Convert COCO JSON to YOLO txt format"""
    os.makedirs(output_dir, exist_ok=True)
    
    images = {img['id']: img for img in coco_json.get('images', [])}
    categories = {cat['id']: cat for cat in coco_json.get('categories', [])}
    annotations = coco_json.get('annotations', [])
    
    # Group annotations by image
    by_image = {}
    for ann in annotations:
        img_id = ann['image_id']
        if img_id not in by_image:
            by_image[img_id] = []
        by_image[img_id].append(ann)
    
    converted = 0
    for img_id, anns in tqdm(by_image.items(), desc="Converting"):
        img_info = images.get(img_id, {})
        img_name = img_info.get('file_name', f'{img_id}.jpg')
        
        if image_dir:
            img_path = os.path.join(image_dir, img_name)
        else:
            img_path = img_name
        
        width = img_info.get('width', 0)
        height = img_info.get('height', 0)
        
        if width == 0 or height == 0:
            # Try to get from image file
            if os.path.exists(img_path):
                width, height = get_image_dimensions(img_path)
        
        if width == 0 or height == 0:
            print(f"Warning: Cannot get dimensions for {img_name}, skipping")
            continue
        
        # Get base name without extension
        base_name = os.path.splitext(img_name)[0]
        output_path = os.path.join(output_dir, f"{base_name}.txt")
        
        with open(output_path, 'w') as f:
            for ann in anns:
                category_id = ann['category_id']
                bbox = ann['bbox']  # [x, y, w, h]
                
                # Convert to YOLO format (center_x, center_y, w, h) normalized
                x_center = (bbox[0] + bbox[2] / 2) / width
                y_center = (bbox[1] + bbox[3] / 2) / height
                w = bbox[2] / width
                h = bbox[3] / height
                
                # YOLO uses 0-indexed class IDs
                f.write(f"{category_id - 1} {x_center} {y_center} {w} {h}\n")
        
        converted += 1
    
    return converted


def yolo_to_coco(yolo_dir: str, output_json: str, image_dir: str = "", 
                 categories: List[Dict] = None) -> int:
    """Convert YOLO txt to COCO JSON"""
    yolo_dir = Path(yolo_dir)
    
    if categories is None:
        # Default categories
        categories = [
            {"id": 1, "name": "object", "supercategory": "object"}
        ]
    
    # Get all txt files
    txt_files = list(yolo_dir.glob("*.txt"))
    if not txt_files:
        print(f"No .txt files found in {yolo_dir}")
        return 0
    
    images = []
    annotations = []
    ann_id = 1
    
    for idx, txt_file in enumerate(tqdm(txt_files, desc="Converting")):
        base_name = txt_file.stem
        img_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
        
        img_path = None
        width, height = 0, 0
        
        if image_dir:
            for ext in img_extensions:
                potential_path = os.path.join(image_dir, base_name + ext)
                if os.path.exists(potential_path):
                    img_path = potential_path
                    width, height = get_image_dimensions(img_path)
                    break
        else:
            # Try to find image in same directory
            for ext in img_extensions:
                potential_path = str(yolo_dir / (base_name + ext))
                if os.path.exists(potential_path):
                    img_path = potential_path
                    width, height = get_image_dimensions(img_path)
                    break
        
        if width == 0 or height == 0:
            print(f"Warning: Cannot get dimensions for {base_name}, using default 640x640")
            width, height = 640, 640
        
        img_id = idx + 1
        images.append({
            "id": img_id,
            "file_name": os.path.basename(img_path) if img_path else f"{base_name}.jpg",
            "width": width,
            "height": height
        })
        
        # Parse YOLO annotations
        with open(txt_file, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) < 5:
                    continue
                
                class_id = int(parts[0]) + 1  # COCO uses 1-indexed
                x_center = float(parts[1]) * width
                y_center = float(parts[2]) * height
                w = float(parts[3]) * width
                h = float(parts[4]) * height
                
                # Convert to COCO bbox [x, y, w, h]
                x = x_center - w / 2
                y = y_center - h / 2
                
                annotations.append({
                    "id": ann_id,
                    "image_id": img_id,
                    "category_id": class_id,
                    "bbox": [x, y, w, h],
                    "area": w * h,
                    "iscrowd": 0
                })
                ann_id += 1
    
    coco_data = {
        "images": images,
        "annotations": annotations,
        "categories": categories
    }
    
    with open(output_json, 'w') as f:
        json.dump(coco_data, f, indent=2)
    
    return len(images)


def voc_to_coco(voc_dir: str, output_json: str, image_dir: str = "",
                categories: List[Dict] = None) -> int:
    """Convert Pascal VOC XML to COCO JSON"""
    voc_dir = Path(voc_dir)
    
    if categories is None:
        categories = [
            {"id": 1, "name": "object", "supercategory": "object"}
        ]
    
    # Get all XML files
    xml_files = list(voc_dir.glob("*.xml"))
    if not xml_files:
        print(f"No .xml files found in {voc_dir}")
        return 0
    
    images = []
    annotations = []
    ann_id = 1
    
    import xml.etree.ElementTree as ET
    
    for idx, xml_file in enumerate(tqdm(xml_files, desc="Converting")):
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
        except:
            continue
        
        # Get image info
        filename = root.findtext('filename', 'unknown.jpg')
        size = root.find('size')
        if size is not None:
            width = int(size.findtext('width', 0))
            height = int(size.findtext('height', 0))
        else:
            width, height = 0, 0
        
        if width == 0 or height == 0:
            # Try to get from image
            base_name = os.path.splitext(filename)[0]
            if image_dir:
                for ext in ['.jpg', '.jpeg', '.png', '.bmp']:
                    img_path = os.path.join(image_dir, base_name + ext)
                    if os.path.exists(img_path):
                        width, height = get_image_dimensions(img_path)
                        break
        
        img_id = idx + 1
        images.append({
            "id": img_id,
            "file_name": filename,
            "width": width,
            "height": height
        })
        
        # Get annotations
        for obj in root.findall('object'):
            class_name = obj.findtext('name', 'object')
            class_id = 1  # Default
            
            bbox = obj.find('bndbox')
            if bbox is not None:
                xmin = float(bbox.findtext('xmin', 0))
                ymin = float(bbox.findtext('ymin', 0))
                xmax = float(bbox.findtext('xmax', 0))
                ymax = float(bbox.findtext('ymax', 0))
                
                w = xmax - xmin
                h = ymax - ymin
                
                annotations.append({
                    "id": ann_id,
                    "image_id": img_id,
                    "category_id": class_id,
                    "bbox": [xmin, ymin, w, h],
                    "area": w * h,
                    "iscrowd": 0
                })
                ann_id += 1
    
    coco_data = {
        "images": images,
        "annotations": annotations,
        "categories": categories
    }
    
    with open(output_json, 'w') as f:
        json.dump(coco_data, f, indent=2)
    
    return len(images)


def labelme_to_coco(labelme_dir: str, output_json: str,
                    categories: List[Dict] = None) -> int:
    """Convert LabelMe JSON to COCO JSON"""
    if categories is None:
        categories = [
            {"id": 1, "name": "object", "supercategory": "object"}
        ]
    
    json_files = list(Path(labelme_dir).glob("*.json"))
    if not json_files:
        print(f"No .json files found in {labelme_dir}")
        return 0
    
    images = []
    annotations = []
    ann_id = 1
    
    for idx, json_file in enumerate(tqdm(json_files, desc="Converting")):
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
        except:
            continue
        
        img_path = data.get('imagePath', '')
        width = data.get('imageWidth', 0)
        height = data.get('imageHeight', 0)
        
        if width == 0 or height == 0:
            # Try to get from image
            base_name = os.path.splitext(img_path)[0]
            for ext in ['.jpg', '.jpeg', '.png', '.bmp']:
                potential_path = os.path.join(labelme_dir, base_name + ext)
                if os.path.exists(potential_path):
                    width, height = get_image_dimensions(potential_path)
                    break
        
        img_id = idx + 1
        images.append({
            "id": img_id,
            "file_name": img_path,
            "width": width,
            "height": height
        })
        
        # Get shapes
        for shape in data.get('shapes', []):
            points = shape.get('points', [])
            if len(points) < 2:
                continue
            
            # Get bounding box
            xs = [p[0] for p in points]
            ys = [p[1] for p in points]
            xmin, xmax = min(xs), max(xs)
            ymin, ymax = min(ys), max(ys)
            
            w = xmax - xmin
            h = ymax - ymin
            
            annotations.append({
                "id": ann_id,
                "image_id": img_id,
                "category_id": 1,
                "bbox": [xmin, ymin, w, h],
                "area": w * h,
                "iscrowd": 0
            })
            ann_id += 1
    
    coco_data = {
        "images": images,
        "annotations": annotations,
        "categories": categories
    }
    
    with open(output_json, 'w') as f:
        json.dump(coco_data, f, indent=2)
    
    return len(images)


def detect_format(file_path: str) -> str:
    """Auto-detect annotation format"""
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.json':
        # Try to detect if COCO or LabelMe
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            if 'images' in data and 'annotations' in data:
                return 'coco'
            if 'shapes' in data:
                return 'labelme'
        except:
            pass
    elif ext == '.txt':
        return 'yolo'
    elif ext == '.xml':
        return 'voc'
    
    return 'unknown'


def cmd_convert(args):
    """Convert between formats"""
    if args.from_format == 'coco' and args.to_format == 'yolo':
        with open(args.input, 'r') as f:
            coco_data = json.load(f)
        count = coco_to_yolo(coco_data, args.output, args.image_dir)
        print(f"✓ Converted {count} images to {args.output}/")
    
    elif args.from_format == 'yolo' and args.to_format == 'coco':
        count = yolo_to_coco(args.input, args.output, args.image_dir)
        print(f"✓ Converted {count} images to {args.output}")
    
    elif args.from_format == 'voc' and args.to_format == 'coco':
        count = voc_to_coco(args.input, args.output, args.image_dir)
        print(f"✓ Converted {count} images to {args.output}")
    
    elif args.from_format == 'labelme' and args.to_format == 'coco':
        count = labelme_to_coco(args.input, args.output)
        print(f"✓ Converted {count} images to {args.output}")
    
    else:
        print(f"Conversion {args.from_format} → {args.to_format} not supported")
        sys.exit(1)


def cmd_formats(args):
    """List supported formats"""
    print("Supported formats:")
    print("  COCO    - .json (COCO JSON annotation)")
    print("  YOLO    - .txt (YOLO darknet format)")
    print("  VOC     - .xml (Pascal VOC XML)")
    print("  LabelMe - .json (LabelMe JSON)")
    print()
    print("Supported conversions:")
    print("  COCO → YOLO")
    print("  YOLO → COCO")
    print("  VOC → COCO")
    print("  LabelMe → COCO")


def main():
    parser = argparse.ArgumentParser(
        description="Annotation Format Converter - Convert between COCO, YOLO, VOC, LabelMe"
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # convert command
    parser_convert = subparsers.add_parser("convert", help="Convert between formats")
    parser_convert.add_argument("input", help="Input file or directory")
    parser_convert.add_argument("output", help="Output file or directory")
    parser_convert.add_argument("--from", "-f", dest="from_format", 
                                 choices=['coco', 'yolo', 'voc', 'labelme'],
                                 required=True, help="Input format")
    parser_convert.add_argument("--to", "-t", dest="to_format",
                                 choices=['coco', 'yolo', 'voc', 'labelme'],
                                 required=True, help="Output format")
    parser_convert.add_argument("--image-dir", "-i", default="",
                                 help="Image directory (for dimension lookup)")
    parser_convert.set_defaults(func=cmd_convert)
    
    # formats command
    parser_formats = subparsers.add_parser("formats", help="List supported formats")
    parser_formats.set_defaults(func=cmd_formats)
    
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
