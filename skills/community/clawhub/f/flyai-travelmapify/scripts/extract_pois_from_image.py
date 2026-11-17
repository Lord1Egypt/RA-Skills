#!/usr/bin/env python3
"""
Extract Points of Interest (POIs) from travel planning images using OCR and AI analysis.
Supports both Chinese and English text extraction.
"""

import os
import sys
import json
import argparse
from PIL import Image
import pytesseract

# Configure tesseract path if needed
# pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'

def extract_text_from_image(image_path):
    """
    Extract text from image using Tesseract OCR with Chinese+English support
    """
    try:
        # Open and preprocess image
        img = Image.open(image_path)
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Apply basic preprocessing for better OCR results
        # You can add more sophisticated preprocessing here
        
        # Extract text with Chinese and English language support
        text = pytesseract.image_to_string(
            img, 
            lang='chi_sim+eng',  # Simplified Chinese + English
            config='--psm 6 --oem 1'
        )
        
        return text.strip()
    
    except Exception as e:
        print(f"Error extracting text from {image_path}: {e}", file=sys.stderr)
        return ""

def identify_pois_from_text(text):
    """
    Identify potential POIs from extracted text using keyword patterns and heuristics
    """
    if not text:
        return []
    
    lines = text.split('\n')
    pois = []
    
    # Common location keywords and patterns
    location_keywords = [
        '街', '路', '广场', '公园', '博物馆', '景区', '大厦', '中心',
        'street', 'road', 'avenue', 'plaza', 'park', 'museum', 'center',
        'mall', 'tower', 'building', 'square', 'district', 'area'
    ]
    
    # Filter lines that likely contain POIs
    for line in lines:
        line = line.strip()
        if not line or len(line) < 2:
            continue
            
        # Skip lines that are clearly not locations
        if any(skip_word in line.lower() for skip_word in ['phone', 'tel', '电话', '联系方式', 'contact']):
            continue
            
        # Check if line contains location indicators
        has_location_keyword = any(keyword in line for keyword in location_keywords)
        has_chinese_chars = any('\u4e00' <= char <= '\u9fff' for char in line)
        has_english_words = any(char.isalpha() for char in line)
        
        # Heuristic: if it has Chinese characters or location keywords, treat as POI
        if has_chinese_chars or has_location_keyword or (has_english_words and len(line.split()) <= 5):
            # Clean up the POI name
            poi_name = line.replace('\t', ' ').replace('  ', ' ').strip()
            if poi_name:
                pois.append({
                    'name': poi_name,
                    'confidence': 0.8 if has_location_keyword else 0.6
                })
    
    return pois

def main():
    parser = argparse.ArgumentParser(description='Extract POIs from travel planning images')
    parser.add_argument('image_path', help='Path to the input image file')
    parser.add_argument('--output', '-o', help='Output JSON file path (default: stdout)')
    parser.add_argument('--min-confidence', type=float, default=0.5, 
                       help='Minimum confidence threshold (default: 0.5)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.image_path):
        print(f"Error: Image file not found: {args.image_path}", file=sys.stderr)
        sys.exit(1)
    
    # Extract text from image
    text = extract_text_from_image(args.image_path)
    
    if not text:
        print("No text extracted from image", file=sys.stderr)
        sys.exit(1)
    
    # Identify POIs from text
    raw_pois = identify_pois_from_text(text)
    
    # Filter by confidence
    filtered_pois = [poi for poi in raw_pois if poi['confidence'] >= args.min_confidence]
    
    # Prepare output
    result = {
        'source_image': args.image_path,
        'extracted_text': text,
        'raw_pois': raw_pois,
        'filtered_pois': filtered_pois,
        'total_pois': len(filtered_pois)
    }
    
    # Output result
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"Results saved to {args.output}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()