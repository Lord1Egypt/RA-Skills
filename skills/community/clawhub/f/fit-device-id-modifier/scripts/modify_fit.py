import struct
import os
import fitparse
import glob

def modify_fit_to_garmin_edge500(input_file, output_file):
    """
    将 FIT 文件的 manufacturer 和 garmin_product 修改为 Garmin Edge 500 China
    """
    # 读取原始 FIT 文件
    fitfile = fitparse.FitFile(input_file)

    # 打开原文件读取二进制数据
    with open(input_file, 'rb') as f:
        data = bytearray(f.read())

    # 查找并修改 file_id 消息中的字段
    for record in fitfile.get_messages('file_id'):
        print("原始文件信息:")
        for field in record:
            print(f"  {field.name}: {field.value} (类型：{type(field.value)})")

            # 修改 manufacturer 字段 (1 = garmin)
            if field.name == 'manufacturer':
                old_val = get_field_numeric_value(field)
                if old_val is not None and old_val != 1:
                    print(f"修改 manufacturer: {old_val} -> 1 (garmin)")
                    modify_field_in_binary(data, old_val, 1, 2)

            # 修改 garmin_product 字段 (1030 = edge500_china)
            if field.name == 'garmin_product':
                old_val = get_field_numeric_value(field)
                if old_val is not None and old_val != 1030:
                    print(f"修改 garmin_product: {old_val} -> 1030 (edge500_china)")
                    modify_field_in_binary(data, old_val, 1030, 2)

    # 重新计算 CRC 校验和
    update_crc(data)

    # 写入新文件
    with open(output_file, 'wb') as f:
        f.write(data)

    print(f"已将 FIT 文件转换为 Garmin Edge 500 China: {output_file}")

def get_field_numeric_value(field):
    """
    获取字段的数值，处理不同数据类型
    """
    if isinstance(field.value, int):
        return field.value
    elif isinstance(field.value, str):
        # 如果是字符串，尝试从原始值获取
        if hasattr(field, 'raw_value') and isinstance(field.raw_value, int):
            return field.raw_value
    return None

def modify_field_in_binary(data, old_value, new_value, field_size):
    """
    在二进制数据中查找并替换字段值
    """
    if not isinstance(old_value, int) or not isinstance(new_value, int):
        print(f"  跳过非整数值：{old_value}")
        return

    if field_size == 2:
        old_bytes = struct.pack('<H', old_value)  # 小端序 2 字节
        new_bytes = struct.pack('<H', new_value)
    elif field_size == 4:
        old_bytes = struct.pack('<I', old_value)  # 小端序 4 字节
        new_bytes = struct.pack('<I', new_value)
    else:
        return

    # 查找并替换
    pos = data.find(old_bytes)
    if pos != -1:
        data[pos:pos+field_size] = new_bytes
        print(f"  在位置 {pos} 替换了字段值")
    else:
        print(f"  未找到要替换的字节序列")

def update_crc(data):
    """
    更新 FIT 文件的 CRC 校验和
    """
    if len(data) >= 2:
        crc = calculate_crc(data[:-2])
        data[-2:] = struct.pack('<H', crc)

def calculate_crc(data):
    """
    计算 FIT 文件的 CRC-16 校验和
    """
    crc = 0
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc & 0xFFFF

if __name__ == "__main__":
    import sys
    
    # 支持两种运行方式：
    # 1. 无参数：处理当前目录下所有子目录中的 .fit 文件
    # 2. 带参数：处理指定的文件或目录
    
    if len(sys.argv) > 1:
        target = sys.argv[1]
        if os.path.isfile(target):
            files = [target]
        elif os.path.isdir(target):
            files = glob.glob(os.path.join(target, "*.fit"))
        else:
            files = glob.glob(target)
    else:
        files = glob.glob("./*/*.fit")
    
    for file in files:
        print(f"Processing file: {file}")
        if '_GM.fit' in file:
            print("  跳过已处理的文件")
            continue
        output_file = file.replace('.fit', '_GM.fit')
        try:
            modify_fit_to_garmin_edge500(file, output_file)
        except Exception as E:
            print(f"Error: {E}")
            continue
