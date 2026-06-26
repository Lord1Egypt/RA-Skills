#!/usr/bin/env python3
"""
3D模型验证脚本
支持STL、OBJ、3MF等常见格式的完整性检查和尺寸提取
"""

import os
import sys
import json
import struct
from pathlib import Path

class ModelValidator:
    def __init__(self, filepath):
        self.filepath = Path(filepath)
        self.file_size = self.filepath.stat().st_size
        self.result = {
            "valid": False,
            "format": "unknown",
            "size": {"x": 0, "y": 0, "z": 0},
            "vertices": 0,
            "faces": 0,
            "file_size": self.file_size,
            "errors": []
        }

    def validate(self):
        """主验证方法"""
        if not self.filepath.exists():
            self.result["errors"].append("文件不存在")
            return self.result

        try:
            # 尝试识别格式
            ext = self.filepath.suffix.lower()

            if ext == '.stl':
                self._validate_stl()
            elif ext == '.obj':
                self._validate_obj()
            elif ext == '.3mf':
                self.result["errors"].append("3MF格式需要额外库支持，暂不支持")
            else:
                self.result["errors"].append(f"不支持的文件格式: {ext}")

            # 如果没有错误，标记为有效
            if not self.result["errors"]:
                self.result["valid"] = True

        except Exception as e:
            self.result["errors"].append(f"验证过程中出错: {str(e)}")

        return self.result

    def _validate_stl(self):
        """验证STL文件"""
        self.result["format"] = "STL"

        with open(self.filepath, 'rb') as f:
            # 读取前80字节
            header = f.read(80)
            f.seek(80)

            # 读取面数量
            try:
                face_count = struct.unpack('<I', f.read(4))[0]
            except:
                # 可能是ASCII STL
                f.seek(0)
                content = f.read().decode('ascii', errors='ignore')
                if 'facet normal' in content:
                    # ASCII STL
                    self._parse_ascii_stl(content)
                else:
                    self.result["errors"].append("无法识别STL格式")
                return

            # 二进制STL
            self.result["faces"] = face_count
            self.result["vertices"] = face_count * 3

            # 验证文件大小是否合理
            expected_size = 80 + 4 + (face_count * 50)  # 每个面50字节
            if self.file_size < expected_size:
                self.result["errors"].append("文件可能被截断")

            # 尝试读取几个面来提取尺寸
            f.seek(84)
            vertices = []
            for i in range(min(face_count, 1000)):  # 最多读1000个面
                # 跳过法向量
                f.read(12)
                # 读取三个顶点
                for j in range(3):
                    x = struct.unpack('<f', f.read(4))[0]
                    y = struct.unpack('<f', f.read(4))[0]
                    z = struct.unpack('<f', f.read(4))[0]
                    vertices.append((x, y, z))
                # 跳过属性字节
                f.read(2)

            if vertices:
                self._calculate_bounding_box(vertices)

    def _parse_ascii_stl(self, content):
        """解析ASCII STL"""
        self.result["format"] = "STL (ASCII)"

        # 统计面数和顶点
        face_count = content.count('facet normal')
        self.result["faces"] = face_count
        self.result["vertices"] = face_count * 3

        # 尝试提取顶点坐标
        import re
        vertex_pattern = r'vertex\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)'
        matches = re.findall(vertex_pattern, content)

        if matches:
            vertices = [(float(x), float(y), float(z)) for x, y, z in matches]
            self._calculate_bounding_box(vertices)

    def _validate_obj(self):
        """验证OBJ文件"""
        self.result["format"] = "OBJ"

        with open(self.filepath, 'r', encoding='utf-8', errors='ignore') as f:
            vertices = []
            face_count = 0

            for line in f:
                line = line.strip()
                if line.startswith('v '):
                    # 顶点
                    parts = line.split()
                    if len(parts) >= 4:
                        x = float(parts[1])
                        y = float(parts[2])
                        z = float(parts[3])
                        vertices.append((x, y, z))
                elif line.startswith('f '):
                    # 面
                    face_count += 1

            self.result["vertices"] = len(vertices)
            self.result["faces"] = face_count

            if vertices:
                self._calculate_bounding_box(vertices)

            # 检查材质文件
            obj_dir = self.filepath.parent
            for line in open(self.filepath, 'r', encoding='utf-8', errors='ignore'):
                if line.startswith('mtllib '):
                    mtl_file = line.split()[1]
                    mtl_path = obj_dir / mtl_file
                    if not mtl_path.exists():
                        self.result["warnings"] = f"材质文件不存在: {mtl_file}"

    def _calculate_bounding_box(self, vertices):
        """计算边界框"""
        if not vertices:
            return

        xs = [v[0] for v in vertices]
        ys = [v[1] for v in vertices]
        zs = [v[2] for v in vertices]

        self.result["size"] = {
            "x": round(max(xs) - min(xs), 2),
            "y": round(max(ys) - min(ys), 2),
            "z": round(max(zs) - min(zs), 2)
        }

        self.result["bounds"] = {
            "min": {"x": round(min(xs), 2), "y": round(min(ys), 2), "z": round(min(zs), 2)},
            "max": {"x": round(max(xs), 2), "y": round(max(ys), 2), "z": round(max(zs), 2)}
        }

def main():
    if len(sys.argv) < 2:
        print("使用方法: python3 validate_3d_model.py <model_file>")
        sys.exit(1)

    filepath = sys.argv[1]
    validator = ModelValidator(filepath)
    result = validator.validate()

    # 输出JSON格式结果
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # 返回退出码
    sys.exit(0 if result["valid"] else 1)

if __name__ == "__main__":
    main()
