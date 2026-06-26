#!/usr/bin/env python3
"""
DOCX translate script — translates English text in DOCX to target language while preserving formatting.
Usage: python3 docx_translate.py <input.docx> [--output <output.docx>] [--src-lang en] [--tgt-lang zh]
"""

import argparse
import os
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

# Register namespaces
NSMAP = {
    '': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'w14': 'http://schemas.microsoft.com/office/word/2010/wordml',
    'w15': 'http://schemas.microsoft.com/office/word/2010/wordml',
}
for prefix, uri in NSMAP.items():
    ET.register_namespace(prefix, uri)


def load_translations(src_lang='en', tgt_lang='zh'):
    """Load translation mapping table. Add project-specific translations here."""
    if src_lang == 'en' and tgt_lang == 'zh':
        return [
            # Common business terms
            ("Table of Contents", "目录"),
            ("Executive Summary", "执行摘要"),
            ("Introduction", "简介"),
            ("Overview", "概述"),
            ("Background", "背景"),
            ("Objective", "目标"),
            ("Methodology", "方法论"),
            ("Results", "结果"),
            ("Discussion", "讨论"),
            ("Conclusion", "结论"),
            ("Recommendations", "建议"),
            ("Appendix", "附录"),
            ("References", "参考资料"),
            ("Figure", "图"),
            ("Table", "表格"),
            ("Note", "备注"),
            ("Warning", "警告"),
            ("Caution", "注意"),
            ("Important", "重要"),
        ]
    return []


def translate_xml(xml_path, translations):
    """Translate all w:t nodes in a Word XML file."""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    modified = False

    for elem in root.iter():
        if elem.tag.endswith('}t') and elem.text:
            text = elem.text
            for eng, chn in translations:
                if eng in text:
                    text = text.replace(eng, chn)
            if text != elem.text:
                elem.text = text
                modified = True

    if modified:
        tree.write(xml_path, xml_declaration=True, encoding='UTF-8')
    return modified


def translate_file(input_path, output_path=None, src_lang='en', tgt_lang='zh'):
    """Translate DOCX file."""
    if output_path is None:
        stem = Path(input_path).stem
        output_path = str(Path(input_path).parent / f"{stem}-{tgt_lang}{Path(input_path).suffix}")

    translations = load_translations(src_lang, tgt_lang)

    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        with zipfile.ZipFile(input_path, 'r') as z:
            z.extractall(tmpdir)

        # Translate document.xml and all related XML files
        for xml_file in Path(tmpdir).rglob('*.xml'):
            if translate_xml(str(xml_file), translations):
                print(f"Translated: {xml_file.name}")

        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zout:
            for fpath in Path(tmpdir).rglob('*'):
                if fpath.is_file():
                    arcname = fpath.relative_to(tmpdir)
                    zout.write(fpath, arcname)

    print(f"Output saved to: {output_path}")
    return output_path


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Translate DOCX files')
    parser.add_argument('input', help='Input DOCX file path')
    parser.add_argument('--output', '-o', help='Output DOCX file path')
    parser.add_argument('--src-lang', default='en', help='Source language code')
    parser.add_argument('--tgt-lang', default='zh', help='Target language code')
    args = parser.parse_args()
    translate_file(args.input, args.output, args.src_lang, args.tgt_lang)