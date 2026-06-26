#!/usr/bin/env python3
"""
编码处理工具 - 确保扫描器正确读取各种编码的文件

问题:
- 样本文件没有声明编码（metadata.json 在外部）
- 使用 errors='ignore' 会丢弃无法解码的字符
- 编码不匹配导致规则匹配失败

支持的编码形式:
1. UTF-8 (无 BOM) - Linux/macOS 标准
2. UTF-8 BOM (EF BB BF) - Windows 常见
3. UTF-16 LE/BE - Windows 程序/文档
4. UTF-32 LE/BE - 罕见但存在
5. GBK/GB2312 - 中文 Windows
6. Big5 - 繁体中文
7. Shift-JIS - 日文
8. EUC-KR - 韩文
9. Latin-1/ISO-8859 - 欧洲语言
10. Windows-1252 - Windows 西欧

解决方案:
1. 检测 BOM 头（优先）
2. 使用 chardet 自动检测编码
3. 优先 UTF-8，失败则用检测的编码
4. 使用 errors='replace' 不丢字符（替换为 ）
"""

import chardet
from pathlib import Path
from typing import Tuple, Optional

# BOM 头定义
BOMS = {
    b'\xef\xbb\xbf': 'utf-8-sig',  # UTF-8 BOM
    b'\xff\xfe': 'utf-16-le',       # UTF-16 LE
    b'\xfe\xff': 'utf-16-be',       # UTF-16 BE
    b'\xff\xfe\x00\x00': 'utf-32-le',  # UTF-32 LE
    b'\x00\x00\xfe\xff': 'utf-32-be',  # UTF-32 BE
}

# 常见编码优先级（根据平台）
COMMON_ENCODINGS = {
    'windows': ['utf-8-sig', 'utf-8', 'gbk', 'gb2312', 'big5', 'latin-1', 'windows-1252'],
    'linux': ['utf-8', 'utf-8-sig', 'latin-1', 'iso-8859-1'],
    'darwin': ['utf-8', 'utf-8-sig', 'latin-1'],
    'default': ['utf-8', 'utf-8-sig', 'gbk', 'latin-1'],
}


def detect_bom(file_path: str) -> Optional[str]:
    """
    检测 BOM 头
    
    Args:
        file_path: 文件路径
    
    Returns:
        encoding - 如果有 BOM 头，返回对应编码；否则返回 None
    """
    try:
        path = Path(file_path)
        if not path.exists():
            return None
        
        with open(path, 'rb') as f:
            header = f.read(4)  # 读取前 4 字节（最长 BOM）
            
            # 按长度从长到短匹配（UTF-32 > UTF-16 > UTF-8）
            for bom, encoding in sorted(BOMS.items(), key=lambda x: -len(x[0])):
                if header.startswith(bom):
                    return encoding
            
            return None
    except Exception:
        return None


def get_platform() -> str:
    """检测当前平台"""
    import sys
    if sys.platform.startswith('win'):
        return 'windows'
    elif sys.platform.startswith('darwin'):
        return 'darwin'
    elif sys.platform.startswith('linux'):
        return 'linux'
    return 'default'


def detect_encoding(file_path: str, read_bytes: int = 10000) -> Tuple[Optional[str], float]:
    """
    检测文件编码（综合 BOM + chardet）
    
    Args:
        file_path: 文件路径
        read_bytes: 读取多少字节用于检测（默认 10KB）
    
    Returns:
        (encoding, confidence) - 编码名称和置信度
    """
    try:
        path = Path(file_path)
        if not path.exists():
            return None, 0.0
        
        # 1. 优先检测 BOM 头
        bom_encoding = detect_bom(str(path))
        if bom_encoding:
            return bom_encoding, 1.0  # BOM 检测置信度 100%
        
        # 2. 使用 chardet 检测
        with open(path, 'rb') as f:
            raw = f.read(read_bytes)
            if not raw:
                return None, 0.0
            
            result = chardet.detect(raw)
            return result['encoding'], result['confidence']
    except Exception:
        return None, 0.0


def read_file_safe(file_path: str) -> Tuple[str, str]:
    """
    安全读取文件，自动处理编码
    
    策略:
    1. 检测 BOM 头（最高优先级）
    2. 平台特定编码优先级（Windows: UTF-8 BOM/GBK, Linux: UTF-8）
    3. chardet 自动检测
    4. 使用 errors='replace' 不丢字符
    
    Args:
        file_path: 文件路径
    
    Returns:
        (content, actual_encoding) - 文件内容和实际使用的编码
    """
    path = Path(file_path)
    
    # 策略 1: 检测 BOM 头（最高优先级）
    bom_encoding = detect_bom(str(path))
    if bom_encoding:
        try:
            with open(path, 'r', encoding=bom_encoding, errors='replace') as f:
                content = f.read()
            return content, bom_encoding
        except Exception:
            pass
    
    # 策略 2: chardet 检测编码（优先于平台默认，因为更准确）
    detected_encoding, confidence = detect_encoding(str(path))
    
    if detected_encoding and confidence > 0.7:
        try:
            with open(path, 'r', encoding=detected_encoding, errors='replace') as f:
                content = f.read()
            return content, detected_encoding
        except Exception:
            pass
    
    # 策略 3: 根据平台尝试常见编码（使用 replace 避免失败）
    platform = get_platform()
    preferred_encodings = COMMON_ENCODINGS.get(platform, COMMON_ENCODINGS['default'])
    
    for encoding in preferred_encodings:
        try:
            with open(path, 'r', encoding=encoding, errors='replace') as f:
                content = f.read()
            return content, encoding
        except Exception:
            continue
    
    # 策略 3: 降级方案 - 二进制读取后强制 UTF-8
    try:
        with open(path, 'rb') as f:
            raw = f.read()
        content = raw.decode('utf-8', errors='replace')
        return content, 'utf-8'
    except Exception:
        pass
    
    # 策略 4: 最后手段 - ignore（会丢字符，但避免崩溃）
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    return content, 'utf-8'


def read_file_with_fallback(file_path: str, preferred_encodings: list = None) -> Tuple[str, str, bool]:
    """
    读取文件，尝试多种编码
    
    Args:
        file_path: 文件路径
        preferred_encodings: 优先尝试的编码列表（默认 ['utf-8', 'gbk', 'latin-1']）
    
    Returns:
        (content, encoding, success) - 内容、编码、是否成功
    """
    if preferred_encodings is None:
        preferred_encodings = ['utf-8', 'gbk', 'latin-1', 'gb2312', 'big5']
    
    for encoding in preferred_encodings:
        try:
            with open(file_path, 'r', encoding=encoding, errors='strict') as f:
                content = f.read()
            return content, encoding, True
        except (UnicodeDecodeError, UnicodeError):
            continue
        except Exception:
            break
    
    # 全部失败，使用 replace 模式
    content, encoding = read_file_safe(file_path)
    return content, encoding, False


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("用法：python encoding_utils.py <文件路径>")
        print("示例：python encoding_utils.py samples/malicious/payload.bash")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    print(f"检测文件：{file_path}")
    
    # 检测编码
    detected, confidence = detect_encoding(file_path)
    print(f"检测编码：{detected} (置信度：{confidence:.2f})")
    
    # 安全读取
    content, actual = read_file_safe(file_path)
    print(f"实际使用：{actual}")
    print(f"文件大小：{len(content)} 字符")
    print(f"前 200 字符:\n{content[:200]}")
