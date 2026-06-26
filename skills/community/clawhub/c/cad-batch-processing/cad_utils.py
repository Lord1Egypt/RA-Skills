#!/usr/bin/env python3
"""
CAD工具基础类
功能：读取解析DXF文件，提取图层、尺寸、坐标、文字、块、属性
"""

import ezdxf
import json
from typing import Dict, List, Any

class CADReader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.doc = None
        self.msp = None
        self.load()
    
    def load(self):
        """加载DXF文件"""
        try:
            self.doc = ezdxf.readfile(self.file_path)
            self.msp = self.doc.modelspace()
            return True
        except Exception as e:
            print(f"❌ 加载DXF失败: {e}")
            return False
    
    def extract_layers(self) -> List[Dict[str, Any]]:
        """提取所有图层信息"""
        layers = []
        for layer in self.doc.layers:
            layers.append({
                "name": str(layer.dxf.name),
                "color": int(layer.dxf.color),
                "linetype": str(layer.dxf.linetype),
                "locked": bool(layer.is_locked),
                "frozen": bool(layer.is_frozen)
            })
        return layers
    
    def extract_texts(self) -> List[Dict[str, Any]]:
        """提取所有文字"""
        texts = []
        for text in self.msp.query("TEXT"):
            texts.append({
                "text": text.dxf.text,
                "x": text.dxf.insert[0],
                "y": text.dxf.insert[1],
                "height": text.dxf.height,
                "layer": text.dxf.layer,
                "color": text.dxf.color
            })
        for mtext in self.msp.query("MTEXT"):
            texts.append({
                "text": mtext.text,
                "x": mtext.dxf.insert[0],
                "y": mtext.dxf.insert[1],
                "height": mtext.dxf.char_height,
                "layer": mtext.dxf.layer,
                "color": mtext.dxf.color
            })
        return texts
    
    def extract_blocks(self) -> List[Dict[str, Any]]:
        """提取所有块参照"""
        blocks = []
        for block_ref in self.msp.query("INSERT"):
            block = block_ref.block()
            attrs = []
            for attrib in block_ref.attribs:
                attrs.append({
                    "tag": attrib.dxf.tag,
                    "text": attrib.dxf.text,
                    "x": attrib.dxf.insert[0],
                    "y": attrib.dxf.insert[1]
                })
            blocks.append({
                "name": block_ref.dxf.name,
                "x": block_ref.dxf.insert[0],
                "y": block_ref.dxf.insert[1],
                "scale_x": block_ref.dxf.xscale,
                "scale_y": block_ref.dxf.yscale,
                "rotation": block_ref.dxf.rotation,
                "layer": block_ref.dxf.layer,
                "attributes": attrs
            })
        return blocks
    
    def extract_lines(self) -> List[Dict[str, Any]]:
        """提取所有线段（墙线等）"""
        lines = []
        for line in self.msp.query("LINE"):
            lines.append({
                "start_x": line.dxf.start[0],
                "start_y": line.dxf.start[1],
                "end_x": line.dxf.end[0],
                "end_y": line.dxf.end[1],
                "layer": line.dxf.layer,
                "color": line.dxf.color
            })
        return lines
    
    def extract_all(self) -> Dict[str, Any]:
        """提取所有信息"""
        # 只提取可JSON序列化的基础类型
        layers = []
        for layer in self.extract_layers():
            layers.append({k: v for k, v in layer.items() if k != 'locked_obj'})
        return {
            "file": self.file_path,
            "layers": layers,
            "texts": self.extract_texts(),
            "blocks": self.extract_blocks(),
            "lines": self.extract_lines()
        }
    
    def save_extracted(self, output_path: str):
        """保存提取结果到JSON"""
        data = self.extract_all()
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ 提取完成，保存到: {output_path}")
        return output_path


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python cad_utils.py <input.dxf> [output.json]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    reader = CADReader(input_file)
    if len(sys.argv) > 2:
        reader.save_extracted(sys.argv[2])
    else:
        data = reader.extract_all()
        print(json.dumps(data, ensure_ascii=False, indent=2))
