#!/usr/bin/env python3
"""
Data Toolkit - Format Converter
Supports: JSON, CSV, YAML, XML
"""

import argparse
import json
import csv
import sys
import os
from pathlib import Path
from typing import Any, Dict, List

try:
    import yaml
except ImportError:
    yaml = None

try:
    import xml.etree.ElementTree as ET
    from xml.dom import minidom
except ImportError:
    ET = None


class DataConverter:
    """Main converter class"""
    
    @staticmethod
    def json_to_csv(data: Any, output_path: str) -> None:
        """Convert JSON to CSV"""
        if isinstance(data, dict):
            data = [data]
        
        if not isinstance(data, list) or not data:
            raise ValueError("JSON must be a list of objects or single object")
        
        # Get all unique keys
        keys = set()
        for item in data:
            if isinstance(item, dict):
                keys.update(item.keys())
        
        keys = sorted(keys)
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            
            for item in data:
                if isinstance(item, dict):
                    writer.writerow(item)
    
    @staticmethod
    def csv_to_json(input_path: str) -> List[Dict]:
        """Convert CSV to JSON"""
        result = []
        
        with open(input_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Try to infer types
                typed_row = {}
                for key, value in row.items():
                    typed_row[key] = DataConverter._infer_type(value)
                result.append(typed_row)
        
        return result
    
    @staticmethod
    def json_to_yaml(data: Any, output_path: str) -> None:
        """Convert JSON to YAML"""
        if yaml is None:
            raise ImportError("PyYAML not installed. Run: pip install pyyaml")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
    
    @staticmethod
    def yaml_to_json(input_path: str) -> Any:
        """Convert YAML to JSON"""
        if yaml is None:
            raise ImportError("PyYAML not installed. Run: pip install pyyaml")
        
        with open(input_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    @staticmethod
    def json_to_xml(data: Any, output_path: str, root_name: str = "root") -> None:
        """Convert JSON to XML"""
        if ET is None:
            raise ImportError("xml module not available")
        
        def dict_to_xml(parent: ET.Element, data: Any, name: str = "item") -> None:
            if isinstance(data, dict):
                for key, value in data.items():
                    child = ET.SubElement(parent, str(key))
                    dict_to_xml(child, value, str(key))
            elif isinstance(data, list):
                for item in data:
                    child = ET.SubElement(parent, name)
                    dict_to_xml(child, item, name)
            else:
                parent.text = str(data)
        
        root = ET.Element(root_name)
        dict_to_xml(root, data, "item")
        
        # Pretty print
        xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(xml_str)
    
    @staticmethod
    def xml_to_json(input_path: str) -> Dict:
        """Convert XML to JSON"""
        if ET is None:
            raise ImportError("xml module not available")
        
        def xml_to_dict(element: ET.Element) -> Any:
            result = {}
            
            # Add attributes
            if element.attrib:
                result['@attributes'] = element.attrib
            
            # Add text content
            if element.text and element.text.strip():
                text = element.text.strip()
                if len(element) == 0:  # No children
                    return DataConverter._infer_type(text)
                result['#text'] = text
            
            # Add children
            for child in element:
                child_data = xml_to_dict(child)
                
                if child.tag in result:
                    # Multiple children with same tag - make it a list
                    if not isinstance(result[child.tag], list):
                        result[child.tag] = [result[child.tag]]
                    result[child.tag].append(child_data)
                else:
                    result[child.tag] = child_data
            
            return result if result else None
        
        tree = ET.parse(input_path)
        root = tree.getroot()
        
        return {root.tag: xml_to_dict(root)}
    
    @staticmethod
    def _infer_type(value: str) -> Any:
        """Try to infer the actual type of a string value"""
        if not value or value.lower() in ('null', 'none', ''):
            return None
        
        if value.lower() in ('true', 'false'):
            return value.lower() == 'true'
        
        try:
            if '.' in value:
                return float(value)
            return int(value)
        except ValueError:
            return value
    
    @staticmethod
    def detect_format(file_path: str) -> str:
        """Detect format from file extension"""
        ext = Path(file_path).suffix.lower()
        format_map = {
            '.json': 'json',
            '.csv': 'csv',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.xml': 'xml'
        }
        return format_map.get(ext, 'unknown')


def main():
    parser = argparse.ArgumentParser(
        description='Data Toolkit - Format Converter'
    )
    
    parser.add_argument('--input', '-i', required=True, help='Input file path')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--format', '-f', help='Output format (json/csv/yaml/xml)')
    parser.add_argument('--input-dir', help='Input directory for batch conversion')
    parser.add_argument('--output-dir', help='Output directory for batch conversion')
    parser.add_argument('--xml-root', default='root', help='Root element name for XML')
    
    args = parser.parse_args()
    
    converter = DataConverter()
    
    try:
        # Detect input format
        input_format = converter.detect_format(args.input)
        
        if input_format == 'unknown':
            print(f"Error: Could not detect format for {args.input}", file=sys.stderr)
            sys.exit(1)
        
        # Load input data
        if input_format == 'json':
            with open(args.input, 'r', encoding='utf-8') as f:
                data = json.load(f)
        elif input_format == 'csv':
            data = converter.csv_to_json(args.input)
        elif input_format == 'yaml':
            data = converter.yaml_to_json(args.input)
        elif input_format == 'xml':
            data = converter.xml_to_json(args.input)
        
        # Determine output format
        if args.format:
            output_format = args.format.lower()
        elif args.output:
            output_format = converter.detect_format(args.output)
        else:
            # Default to JSON
            output_format = 'json'
            args.output = Path(args.input).with_suffix('.json')
        
        # Convert and save
        if output_format == 'json':
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        elif output_format == 'csv':
            converter.json_to_csv(data, args.output)
        elif output_format == 'yaml':
            converter.json_to_yaml(data, args.output)
        elif output_format == 'xml':
            converter.json_to_xml(data, args.output, args.xml_root)
        else:
            print(f"Error: Unsupported output format: {output_format}", file=sys.stderr)
            sys.exit(1)
        
        print(f"✓ Converted {args.input} ({input_format}) → {args.output} ({output_format})")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
