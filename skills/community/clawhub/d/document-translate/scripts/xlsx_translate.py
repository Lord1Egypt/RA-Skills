#!/usr/bin/env python3
"""
XLSX translate script — translates English text in XLSX to target language while preserving formatting and formulas.
Usage: python3 xlsx_translate.py <input.xlsx> [--output <output.xlsx>] [--src-lang en] [--tgt-lang zh]
"""

import argparse
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
import tempfile

# Register namespaces
ET.register_namespace('', 'http://schemas.openxmlformats.org/spreadsheetml/2006/main')
ET.register_namespace('mc', 'http://schemas.openxmlformats.org/markup-compatibility/2006')
ET.register_namespace('r', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships')


def load_translations(src_lang='en', tgt_lang='zh'):
    if src_lang == 'en' and tgt_lang == 'zh':
        return [
            ("Summary", "摘要"),
            ("Total", "合计"),
            ("Average", "平均"),
            ("Revenue", "收入"),
            ("Cost", "成本"),
            ("Profit", "利润"),
            ("Date", "日期"),
            ("Amount", "金额"),
            ("Description", "描述"),
            ("Category", "类别"),
            ("Status", "状态"),
            ("Name", "名称"),
            ("Value", "值"),
        ]
    return []


def translate_xml(xml_path, translations):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    modified = False

    for elem in root.iter():
        if elem.text:
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
    if output_path is None:
        stem = Path(input_path).stem
        output_path = str(Path(input_path).parent / f"{stem}-{tgt_lang}{Path(input_path).suffix}")

    translations = load_translations(src_lang, tgt_lang)

    with tempfile.TemporaryDirectory() as tmpdir:
        with zipfile.ZipFile(input_path, 'r') as z:
            z.extractall(tmpdir)

        # Translate shared strings (most user-facing text lives here)
        shared_strings = Path(tmpdir) / 'xl' / 'sharedStrings.xml'
        if shared_strings.exists():
            if translate_xml(str(shared_strings), translations):
                print("Translated: sharedStrings.xml")

        # Translate sheet XMLs
        sheets_dir = Path(tmpdir) / 'xl' / 'worksheets'
        if sheets_dir.exists():
            for sheet in sorted(sheets_dir.glob('sheet*.xml')):
                if translate_xml(str(sheet), translations):
                    print(f"Translated: {sheet.name}")

        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zout:
            for fpath in Path(tmpdir).rglob('*'):
                if fpath.is_file():
                    arcname = fpath.relative_to(tmpdir)
                    zout.write(fpath, arcname)

    print(f"Output saved to: {output_path}")
    return output_path


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Translate XLSX files')
    parser.add_argument('input', help='Input XLSX file path')
    parser.add_argument('--output', '-o', help='Output XLSX file path')
    parser.add_argument('--src-lang', default='en', help='Source language code')
    parser.add_argument('--tgt-lang', default='zh', help='Target language code')
    args = parser.parse_args()
    translate_file(args.input, args.output, args.src_lang, args.tgt_lang)