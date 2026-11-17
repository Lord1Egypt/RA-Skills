#!/usr/bin/env python3
"""
VPK (Valve Pak) 文件解析器
用于提取 Dota 2 pak01_001.vpk 中的本地化文件

用法: python3 unpack_vpk.py <vpk_file> [output_dir]

VPK 格式参考: https://developer.valvesoftware.com/wiki/VPK_File_Format
"""
import struct
import os
import sys

def read_cstring(f):
    """读取 null-terminated C string"""
    chars = []
    while True:
        c = f.read(1)
        if not c or c == b'\x00':
            break
        chars.append(c.decode('latin-1'))
    return ''.join(chars)

def parse_vpk(vpk_path, output_dir=None):
    """解析 VPK 文件，提取所有文件到 output_dir"""
    
    with open(vpk_path, 'rb') as f:
        # 读取文件头
        signature = f.read(4)
        if signature[:3] != b'VPK':
            print(f"Error: Invalid VPK signature: {signature}")
            return
        
        version = struct.unpack('<I', f.read(4))[0]
        tree_offset = struct.unpack('<I', f.read(4))[0]
        
        print(f"VPK Version: {version}")
        print(f"Tree offset: {tree_offset}")
        
        # 跳到文件目录
        f.seek(tree_offset)
        
        if output_dir is None:
            output_dir = os.path.splitext(os.path.basename(vpk_path))[0] + "_extracted"
        
        os.makedirs(output_dir, exist_ok=True)
        
        extracted = 0
        
        while True:
            # 读取目录条目的头
            tree_type = f.read(1)
            if not tree_type or tree_type == b'\x00':
                break
            
            tree_type = tree_type.decode('latin-1')
            
            # 读取目录结构: type/filename.ext
            # 每个文件有: 预加载数据大小(2字节)、文件大小(4字节)、文件偏移(4字节)、CRC32(4字节)
            # 文件名以 \0 结尾
            
            filename = read_cstring(f)
            
            if not filename:
                break
            
            # 读取文件元数据
            preload_bytes = struct.unpack('<H', f.read(2))[0]
            archive_id = struct.unpack('<I', f.read(4))[0]
            file_offset = struct.unpack('<I', f.read(4))[0]
            file_length = struct.unpack('<I', f.read(4))[0]
            crc32 = struct.unpack('<I', f.read(4))[0]
            
            # 跳过预加载数据和末端对齐
            if preload_bytes > 0:
                f.read(preload_bytes)
            
            # 跳过偶数字节对齐
            align = (preload_bytes + 12) % 2
            if align:
                f.read(1)
            
            # 计算实际在归档中的偏移
            archive_offset = file_offset + 12
            
            full_path = os.path.join(output_dir, tree_type, filename)
            
            # 只提取我们需要的文件类型
            if 'localization' in full_path.lower() or 'english' in full_path.lower() or \
               'resource' in full_path.lower() or 'txt' in full_path.lower():
                print(f"Found: {full_path}")
                
                # 跳到文件数据位置
                current_pos = f.tell()
                # VPK 2.0 的文件偏移是相对于文件数据段的开始
                if version >= 2:
                    f.seek(tree_offset - 12 + archive_offset)
                else:
                    f.seek(archive_offset)
                
                data = f.read(file_length)
                
                # 保存
                out_path = os.path.join(output_dir, full_path.replace('/', '_'))
                with open(out_path, 'wb') as out:
                    out.write(data)
                extracted += 1
                print(f"  -> Extracted to {out_path} ({len(data)} bytes)")
                
                # 恢复位置
                f.seek(current_pos)
        
        print(f"\nExtracted {extracted} localization files to {output_dir}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    vpk_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    parse_vpk(vpk_file, output_dir)