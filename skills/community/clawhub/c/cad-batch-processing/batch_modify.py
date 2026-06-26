#!/usr/bin/env python3
"""
CAD批量修改
功能：批量改图签、图层名、文字、线型、颜色、块属性
"""

import os
import sys
import ezdxf
from typing import Dict, List, Any

class BatchModifier:
    def __init__(self):
        pass
    
    def modify_text_in_file(self, file_path: str, find_text: str, replace_text: str) -> int:
        """批量替换文件中文字"""
        count = 0
        try:
            doc = ezdxf.readfile(file_path)
            msp = doc.modelspace()
            
            # 替换TEXT
            for text in msp.query("TEXT"):
                if find_text in text.dxf.text:
                    new_text = text.dxf.text.replace(find_text, replace_text)
                    text.dxf.text = new_text
                    count += 1
            
            # 替换MTEXT
            for mtext in msp.query("MTEXT"):
                content = mtext.text
                if find_text in content:
                    new_content = content.replace(find_text, replace_text)
                    mtext.text = new_content
                    count += 1
            
            # 替换块属性
            for block_ref in msp.query("INSERT"):
                for attrib in block_ref.attribs:
                    if find_text in attrib.dxf.text:
                        attrib.dxf.text = attrib.dxf.text.replace(find_text, replace_text)
                        count += 1
            
            if count > 0:
                doc.saveas(file_path)
                print(f"✅ {os.path.basename(file_path)}: 替换了 {count} 处文字")
            return count
        except Exception as e:
            print(f"❌ {os.path.basename(file_path)} 修改失败: {e}")
            return 0
    
    def rename_layer(self, file_path: str, old_name: str, new_name: str) -> int:
        """重命名图层"""
        count = 0
        try:
            doc = ezdxf.readfile(file_path)
            if old_name in doc.layers:
                layer = doc.layers.get(old_name)
                layer.rename(new_name)
                doc.saveas(file_path)
                print(f"✅ {os.path.basename(file_path)}: 图层 {old_name} → {new_name}")
                return 1
            else:
                print(f"⚠️ {os.path.basename(file_path)}: 图层 {old_name} 不存在")
                return 0
        except Exception as e:
            print(f"❌ {os.path.basename(file_path)} 修改失败: {e}")
            return 0
    
    def change_block_attribute(self, file_path: str, block_name: str, tag: str, new_value: str) -> int:
        """修改块属性"""
        count = 0
        try:
            doc = ezdxf.readfile(file_path)
            msp = doc.modelspace()
            for block_ref in msp.query("INSERT"):
                if block_ref.dxf.name == block_name:
                    for attrib in block_ref.attribs:
                        if attrib.dxf.tag == tag:
                            attrib.dxf.text = new_value
                            count += 1
            if count > 0:
                doc.saveas(file_path)
                print(f"✅ {os.path.basename(file_path)}: 修改了 {count} 个块属性")
            return count
        except Exception as e:
            print(f"❌ {os.path.basename(file_path)} 修改失败: {e}")
            return 0
    
    def change_layer_color(self, file_path: str, layer_name: str, color_index: int) -> int:
        """修改图层颜色"""
        try:
            doc = ezdxf.readfile(file_path)
            if layer_name in doc.layers:
                layer = doc.layers.get(layer_name)
                layer.color = color_index
                doc.saveas(file_path)
                print(f"✅ {os.path.basename(file_path)}: 图层 {layer_name} 颜色改为 {color_index}")
                return 1
            else:
                print(f"⚠️ {os.path.basename(file_path)}: 图层 {layer_name} 不存在")
                return 0
        except Exception as e:
            print(f"❌ {os.path.basename(file_path)} 修改失败: {e}")
            return 0
    
    def batch_modify_text_in_folder(self, folder_path: str, find_text: str, replace_text: str) -> int:
        """文件夹中批量替换文字"""
        total = 0
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(".dxf"):
                    full_path = os.path.join(root, file)
                    total += self.modify_text_in_file(full_path, find_text, replace_text)
        print(f"\n📊 总计替换: {total} 处")
        return total


def main():
    if len(sys.argv) < 5:
        print("""
CAD批量修改工具

Usage:
  1. 批量替换文字:
     python batch_modify.py text <folder> <find> <replace>

  2. 重命名图层:
     python batch_modify.py layer <file.dxf> <old_name> <new_name>

  3. 修改块属性:
     python batch_modify.py attr <file.dxf> <block_name> <tag> <new_value>

  4. 修改图层颜色:
     python batch_modify.py color <file.dxf> <layer_name> <color_index>
""")
        sys.exit(1)
    
    mode = sys.argv[1]
    modifier = BatchModifier()
    
    if mode == "text":
        folder = sys.argv[2]
        find = sys.argv[3]
        replace = sys.argv[4]
        modifier.batch_modify_text_in_folder(folder, find, replace)
    elif mode == "layer":
        file = sys.argv[2]
        old = sys.argv[3]
        new = sys.argv[4]
        modifier.rename_layer(file, old, new)
    elif mode == "attr":
        file = sys.argv[2]
        block = sys.argv[3]
        tag = sys.argv[4]
        new_val = sys.argv[5]
        modifier.change_block_attribute(file, block, tag, new_val)
    elif mode == "color":
        file = sys.argv[2]
        layer = sys.argv[3]
        color = int(sys.argv[4])
        modifier.change_layer_color(file, layer, color)
    else:
        print(f"❌ 未知模式: {mode}")
        sys.exit(1)


if __name__ == "__main__":
    main()
