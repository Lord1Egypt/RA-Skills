#!/usr/bin/env python3
"""
3D模型元数据验证脚本
验证3MF文件中的Title、Description、License等必须字段是否存在
"""

import os
import sys
import json
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

class MetadataValidator:
    def __init__(self, filepath):
        self.filepath = Path(filepath)
        self.file_size = self.filepath.stat().st_size if self.filepath.exists() else 0
        self.result = {
            "format": "unknown",
            "file_size": self.file_size,
            "metadata": {},
            "compliance": {
                "is_compliant": False,
                "required_fields": {
                    "title": {"exists": False, "value": ""},
                    "description": {"exists": False, "value": ""},
                    "license": {"exists": False, "value": ""}
                },
                "missing_fields": [],
                "reason": ""
            }
        }

    def validate(self):
        """主验证方法"""
        if not self.filepath.exists():
            self.result["compliance"]["reason"] = "文件不存在"
            return self.result

        try:
            # 尝试识别格式
            ext = self.filepath.suffix.lower()

            if ext == '.3mf':
                self._validate_3mf()
            elif ext == '.stl':
                self._validate_stl()
            elif ext == '.obj':
                self._validate_obj()
            else:
                self.result["compliance"]["reason"] = f"不支持的文件格式: {ext}"

            # 验证合规性
            self._check_compliance()

        except Exception as e:
            self.result["compliance"]["reason"] = f"验证过程中出错: {str(e)}"
            import traceback
            traceback.print_exc()

        return self.result

    def _validate_3mf(self):
        """验证3MF文件的元数据"""
        self.result["format"] = "3MF"

        try:
            # 3MF是ZIP格式，解压后读取XML
            with zipfile.ZipFile(self.filepath, 'r') as zip_ref:
                # 查找3dmodel.model文件
                model_files = [f for f in zip_ref.namelist() if '3dmodel.model' in f]

                if not model_files:
                    self.result["compliance"]["reason"] = "未找到3dmodel.model文件"
                    return

                # 读取主模型文件
                with zip_ref.open(model_files[0]) as model_file:
                    content = model_file.read().decode('utf-8', errors='ignore')

                # 解析XML
                root = ET.fromstring(content)

                # 提取元数据
                self._extract_metadata_from_xml(root)

        except Exception as e:
            self.result["compliance"]["reason"] = f"解析3MF文件出错: {str(e)}"

    def _extract_metadata_from_xml(self, root):
        """从XML根元素提取元数据"""
        namespace = {
            'core': 'http://schemas.microsoft.com/3dmanufacturing/core/2015/02',
            'prod': 'http://schemas.microsoft.com/3dmanufacturing/production/2015/06'
        }

        metadata = {}

        # 遍历所有metadata元素
        for elem in root.iter():
            if 'name' in elem.attrib:
                metadata_name = elem.attrib.get('name', '').lower()
                value = elem.text or ""

                # 标准化字段名
                if metadata_name == 'title':
                    metadata['title'] = value
                elif metadata_name == 'description':
                    metadata['description'] = value
                elif metadata_name == 'license':
                    metadata['license'] = value
                elif metadata_name == 'author':
                    metadata['author'] = value
                elif metadata_name == 'designer':
                    metadata['designer'] = value
                elif metadata_name == 'copyright':
                    metadata['copyright'] = value
                elif metadata_name == 'creationdate':
                    metadata['creation_date'] = value

        self.result["metadata"] = metadata

    def _validate_stl(self):
        """验证STL文件的元数据"""
        self.result["format"] = "STL"
        # STL格式不支持内嵌元数据
        self.result["compliance"]["reason"] = "STL格式不支持内嵌元数据，建议使用3MF或OBJ格式"

    def _validate_obj(self):
        """验证OBJ文件的元数据"""
        self.result["format"] = "OBJ"
        # OBJ格式不支持内嵌元数据
        self.result["compliance"]["reason"] = "OBJ格式不支持内嵌元数据，建议使用3MF格式"

    def _check_compliance(self):
        """检查元数据合规性"""
        required = self.result["compliance"]["required_fields"]
        metadata = self.result["metadata"]

        # 检查必须字段
        required["title"]["exists"] = "title" in metadata and bool(metadata["title"].strip())
        required["title"]["value"] = metadata.get("title", "")

        required["description"]["exists"] = "description" in metadata and bool(metadata["description"].strip())
        required["description"]["value"] = metadata.get("description", "")

        required["license"]["exists"] = "license" in metadata and bool(metadata["license"].strip())
        required["license"]["value"] = metadata.get("license", "")

        # 检查哪些字段缺失
        missing_fields = []
        if not required["title"]["exists"]:
            missing_fields.append("Title")
        if not required["description"]["exists"]:
            missing_fields.append("Description")
        if not required["license"]["exists"]:
            missing_fields.append("License")

        self.result["compliance"]["missing_fields"] = missing_fields

        # 判断合规性
        if len(missing_fields) == 0:
            self.result["compliance"]["is_compliant"] = True
            self.result["compliance"]["reason"] = "元数据完整，符合要求"
        else:
            self.result["compliance"]["is_compliant"] = False
            self.result["compliance"]["reason"] = f"缺少必须的元数据字段: {', '.join(missing_fields)}"

def main():
    if len(sys.argv) < 2:
        print("使用方法: python3 validate_metadata.py <model_file>")
        sys.exit(1)

    filepath = sys.argv[1]
    validator = MetadataValidator(filepath)
    result = validator.validate()

    # 输出JSON格式结果
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # 返回退出码
    sys.exit(0 if result["compliance"]["is_compliant"] else 1)

if __name__ == "__main__":
    main()
