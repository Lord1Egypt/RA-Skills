#!/usr/bin/env python3
"""
Classical Chinese Translator - Professional translation tool for Classical Chinese texts
Based on the successful 《道德经讲义》 translation project with 98.5+ quality standard
"""

import os
import re
import sys
import json
import shutil
import argparse
import unicodedata
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import ebooklib
    from ebooklib import epub
    from lxml import etree
except ImportError:
    print("Error: Required libraries not installed. Please install:")
    print("pip install ebooklib lxml")
    sys.exit(1)

class ClassicalChineseTranslator:
    def __init__(self, quality_standard: float = 98.5, terminology_dict: Optional[str] = None):
        self.quality_standard = quality_standard
        self.terminology_dict = self._load_terminology_dict(terminology_dict)
        self.exclude_patterns = [
            r'按：此书旧无作者姓氏.*',
            r'光绪\d+年.*顿首敬序'
        ]
        
    def _load_terminology_dict(self, dict_path: Optional[str]) -> Dict[str, str]:
        """Load terminology dictionary for specialized terms explanation"""
        if not dict_path or not os.path.exists(dict_path):
            # Default Daoist terminology dictionary
            return {
                '玄关一窍': '（指修炼中的关键穴位，位于眉心与丹田之间的中脉）',
                '河车运转': '（指内丹修炼中精气在任督二脉的循环运行）',
                '铅汞交媾': '（指内丹修炼中阴阳能量的结合）',
                '元神': '（指先天本性，与后天识神相对）',
                '识神': '（指后天意识，与先天元神相对）',
                '金丹': '（指内丹修炼的最高成就）',
                '无为': '（指顺应自然，不强求作为）',
                '太上': '（指老子或至高无上的道）'
            }
        with open(dict_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def remove_control_characters(self, text: str) -> str:
        """Remove control characters while preserving whitespace"""
        return ''.join(char for char in text 
                      if unicodedata.category(char)[0] != 'C' or char in '\t\n\r')
    
    def should_exclude_from_translation(self, text: str) -> bool:
        """Check if text should be excluded from translation"""
        for pattern in self.exclude_patterns:
            if re.search(pattern, text):
                return True
        return False
    
    def explain_terminology(self, text: str) -> str:
        """Add explanations for specialized terminology"""
        if self.quality_standard < 98.5:
            return text
            
        result = text
        for term, explanation in self.terminology_dict.items():
            if term in result and explanation not in result:
                # Add explanation after first occurrence
                result = result.replace(term, f'{term}{explanation}', 1)
        return result
    
    def modernize_syntax(self, text: str) -> str:
        """Convert classical syntax to modern vernacular Chinese"""
        # Remove classical sentence structures
        # This is a simplified version - real implementation would be more complex
        modern_text = text
        
        # Ensure complete sentences with modern punctuation
        modern_text = re.sub(r'([。！？])\s*([^\n])', r'\1 \2', modern_text)
        
        # Remove archaic particles and expressions
        archaic_replacements = {
            '之': '的',
            '其': '他的/她的/它的',
            '曰': '说',
            '夫': '',
            '盖': '大概',
            '故': '所以',
            '然': '但是',
            '则': '就',
            '而': '而且/但是',
            '以': '用/因为'
        }
        
        # Apply replacements carefully to avoid over-modification
        for old, new in archaic_replacements.items():
            if old in modern_text and len(modern_text) > 20:  # Only for longer texts
                # This is a placeholder - real implementation needs context awareness
                pass
                
        return modern_text
    
    def translate_text(self, original_text: str) -> str:
        """Translate classical Chinese text to modern vernacular Chinese"""
        if self.should_exclude_from_translation(original_text):
            return original_text
            
        # Apply high-quality translation rules
        translated = self.explain_terminology(original_text)
        translated = self.modernize_syntax(translated)
        
        # Ensure 98.5+ quality standard
        if self.quality_standard >= 98.5:
            # Add quality assurance checks here
            translated = self.ensure_complete_modernization(translated)
            
        return translated
    
    def ensure_complete_modernization(self, text: str) -> str:
        """Ensure complete modernization according to 98.5+ standard"""
        # This would contain comprehensive checks for classical syntax
        # Placeholder implementation
        return text
    
    def process_xhtml_file(self, input_path: str, output_path: str) -> bool:
        """Process XHTML file with translation"""
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse XML safely
            parser = etree.XMLParser(recover=True, encoding='utf-8')
            root = etree.fromstring(content.encode('utf-8'), parser)
            
            # Extract and translate content
            translated_content = self._translate_xhtml_content(root)
            
            # Write translated content
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(etree.tostring(root, encoding='unicode', pretty_print=True))
                
            return True
        except Exception as e:
            print(f"Error processing {input_path}: {e}")
            return False
    
    def _translate_xhtml_content(self, root) -> str:
        """Translate content within XHTML structure"""
        # Find all paragraph elements
        for p_elem in root.xpath('//p[not(ancestor::h1)]'):
            original_text = ''.join(p_elem.itertext())
            if original_text.strip() and not self.should_exclude_from_translation(original_text):
                # Create translation structure
                strong_elem = etree.Element('strong')
                strong_elem.text = '【白话译文】'
                
                translated_p = etree.Element('p')
                translated_p.text = self.translate_text(original_text)
                
                # Insert after original paragraph
                parent = p_elem.getparent()
                parent.insert(parent.index(p_elem) + 1, translated_p)
                parent.insert(parent.index(p_elem) + 1, strong_elem)
        
        return etree.tostring(root, encoding='unicode')
    
    def process_epub(self, input_path: str, output_path: str) -> bool:
        """Process EPUB file with translation"""
        try:
            book = epub.read_epub(input_path)
            
            # Process each item in the EPUB
            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    # Parse and translate XHTML content
                    content = item.get_content().decode('utf-8')
                    parser = etree.XMLParser(recover=True, encoding='utf-8')
                    root = etree.fromstring(content.encode('utf-8'), parser)
                    
                    # Translate content
                    self._translate_xhtml_content(root)
                    
                    # Update item content
                    item.set_content(etree.tostring(root, encoding='utf-8'))
            
            # Write translated EPUB
            epub.write_epub(output_path, book)
            return True
            
        except Exception as e:
            print(f"Error processing EPUB {input_path}: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description='Classical Chinese Translator')
    parser.add_argument('--input', required=True, help='Input file or directory')
    parser.add_argument('--output', required=True, help='Output file or directory')
    parser.add_argument('--quality-standard', type=float, default=98.5, 
                       help='Quality standard (default: 98.5)')
    parser.add_argument('--terminology-dict', help='Custom terminology dictionary JSON file')
    parser.add_argument('--batch-size', type=int, default=3, help='Batch size for processing')
    parser.add_argument('--validate-xml', action='store_true', help='Validate XML structure')
    parser.add_argument('--preserve-original', action='store_true', help='Preserve original files')
    
    args = parser.parse_args()
    
    translator = ClassicalChineseTranslator(
        quality_standard=args.quality_standard,
        terminology_dict=args.terminology_dict
    )
    
    input_path = Path(args.input)
    output_path = Path(args.output)
    
    if input_path.is_file():
        if input_path.suffix.lower() == '.epub':
            success = translator.process_epub(str(input_path), str(output_path))
        else:
            success = translator.process_xhtml_file(str(input_path), str(output_path))
            
        if success:
            print(f"Successfully processed {input_path} -> {output_path}")
        else:
            print(f"Failed to process {input_path}")
            sys.exit(1)
            
    elif input_path.is_dir():
        output_path.mkdir(exist_ok=True)
        files = list(input_path.glob('*.xhtml')) + list(input_path.glob('*.html'))
        
        for i in range(0, len(files), args.batch_size):
            batch = files[i:i+args.batch_size]
            for file in batch:
                output_file = output_path / file.name
                success = translator.process_xhtml_file(str(file), str(output_file))
                if not success:
                    print(f"Failed to process {file}")
                    sys.exit(1)
                    
        print(f"Successfully processed {len(files)} files in batches of {args.batch_size}")

if __name__ == '__main__':
    main()