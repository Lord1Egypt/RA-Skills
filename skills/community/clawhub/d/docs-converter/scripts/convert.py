#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文档转换全能王 API 转换脚本
调用 https://www.wdangz.com API 进行文档格式转换
支持自然语言描述自动识别转换类型

安全说明：
- 文件将上传到第三方服务进行转换
- 请勿上传包含敏感信息的文件
- 建议使用环境变量存储API密钥
"""
import io
import sys
# 解决Windows控制台编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import os
import sys
import json
import time
import re
import requests
from pathlib import Path

# ============== 安全配置 ==============
MAX_FILE_SIZE_MB = 50  # 最大文件大小限制(MB)
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

# 敏感文件关键词（用于警告）
SENSITIVE_KEYWORDS = [
    'password', 'passwd', '密码', 'secret', '机密', 'confidential',
    'private', '私密', '身份证', 'idcard', '银行卡', 'bankcard',
    '合同', 'contract', '财务', 'finance', '薪资', 'salary',
    '社保', 'insurance', '征信', 'credit'
]

# 敏感文件扩展名（可能包含敏感信息）
SENSITIVE_EXTENSIONS = [
    '.pfx', '.p12', '.key', '.pem',  # 证书文件
    '.env', '.credentials',  # 凭证文件
]
# =====================================

# API配置 - 生产环境 (新API地址)
API_BASE_URL = "https://www.wdangz.com/api/v1/convert"
CHECK_STATE_URL = "https://www.wdangz.com/api/v1/checkState"
# 下载URL: https://www.wdangz.com/file/{docId}
DOWNLOAD_URL = "https://www.wdangz.com/file"

# 轮询配置
MAX_POLL_ATTEMPTS = 60
POLL_INTERVAL = 3  # 秒


# 自然语言到转换类型的映射
CONVERSION_MAPPING = {
    # Word转其他
    r'word.*pdf|word转pdf|word转成pdf|word转换pdf|word到pdf': 'wordTOpdf',
    r'word.*图|word转图|word转成图|word转换图片|word到图片|word.*jpg': 'wordTOjpg',
    r'word.*excel|word转excel|word转成excel|word转换excel|word到excel': 'wordTOexcel',
    r'word.*ppt|word转ppt|word转成ppt|word转换ppt|word到ppt|word.*pptx': 'wordTOpptx',
    
    # Excel转其他
    r'excel.*pdf|excel转pdf|excel转成pdf|excel转换pdf|excel到pdf': 'excelTOpdf',
    r'excel.*图|excel转图|excel转成图|excel转换图片|excel到图片|excel.*jpg': 'excelTOjpg',
    r'excel.*word|excel转word|excel转成word|excel转换word|excel到word': 'excelTOword',
    
    # PPT转其他
    r'ppt.*pdf|ppt转pdf|ppt转成pdf|ppt转换pdf|ppt到pdf|pptx.*pdf': 'pptTOpdf',
    r'ppt.*图|ppt转图|ppt转成图|ppt转换图片|ppt到图片|ppt.*jpg|pptx.*jpg': 'pptTOjpg',
    r'ppt.*word|ppt转word|ppt转成word|ppt转换word|ppt到word|pptx.*word': 'pptxTOword',
    
    # PDF转其他
    r'pdf.*word|pdf转word|pdf转成word|pdf转换word|pdf到word|pdf.*docx': 'pdfTOdocx',
    r'pdf.*excel|pdf转excel|pdf转成excel|pdf转换excel|pdf到excel|pdf.*xlsx': 'pdfTOxlsx',
    r'pdf.*ppt|pdf转ppt|pdf转成ppt|pdf转换ppt|pdf到ppt|pdf.*pptx': 'pdfTOpptx',
    r'pdf.*html|pdf转html|pdf转成html|pdf转换html|pdf到html': 'pdfTOhtml',
    r'pdf.*图|pdf转图|pdf转成图|pdf转换图片|pdf到图片|pdf.*jpg|pdf.*png': 'pdfTOjpg',
    
    # 图片格式转换
    r'(图片|image).*(png|PNG)': 'imageTOpng',
    r'(图片|image).*(jpg|JPG|jpeg)': 'imageTOjpg',
    r'(图片|image).*(bmp|BMP)': 'imageTObmp',
    
    # 图片转文档(OCR)
    r'(图片|image).*pdf|图片转pdf|图片转成pdf|图片转换pdf': 'imageToPdf',
    r'(图片|image).*word|图片转word|图片转成word|图片转换word': 'imageToWord',
    r'(图片|image).*文(本|档)|图片转文本|图片转txt': 'imageToTxt',
    r'(图片|image).*excel|图片转excel|图片转成excel|图片转换excel': 'imageToExcel',
    
    # 转为Word (通用) - 当源文件是图片时
    r'转.*word|转成.*word|转为.*word|变.*word': 'imageToWord',
    
    # PDF处理
    r'合并.*pdf|合并PDF|pdf.*合并': 'mergePdf',
    r'拆分.*pdf|拆分PDF|pdf.*拆分|split.*pdf': 'splitPdf',
    r'(水印|watermark).*pdf|pdf.*(水印|添加水印)': 'waterMark',
    r'(页码|page.*number).*pdf|pdf.*(加页码|添加页码)': 'addPageNumber',
    r'(优化|optimize).*pdf|pdf.*优化': 'pdfOptimize',
    r'(加密|lock).*pdf|pdf.*(加密|加密码)': 'lockPdf',
    r'(解密|unlock).*pdf|pdf.*(解密|去密码)': 'unlockPdf',
    
    # HTML转PDF
    r'html.*pdf|html转pdf|html转成pdf|html转换pdf|html到pdf': 'htmlTOpdf',
    
    # 文本转语音
    r'文.*语|文本转语音|text.*voice': 'txt_to_voice',
}

# 常见文件扩展名对应的转换类型（兜底方案）
EXTENSION_MAPPING = {
    '.doc': 'wordTOpdf',
    '.docx': 'wordTOpdf',
    '.xls': 'excelTOpdf',
    '.xlsx': 'excelTOpdf',
    '.ppt': 'pptTOpdf',
    '.pptx': 'pptTOpdf',
    '.pdf': 'pdfTOdocx',
    '.png': 'imageTOjpg',
    '.jpg': 'imageTOpng',
    '.jpeg': 'imageTOpng',
    '.bmp': 'imageTOpng',
    '.gif': 'imageTOpng',
    '.webp': 'imageTOpng',
}

# 支持的文件扩展名
SUPPORTED_EXTENSIONS = set(EXTENSION_MAPPING.keys())


def check_file_security(file_path):
    """
    检查文件安全性
    
    返回: (is_safe, warnings)
    """
    warnings = []
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        return False, ["文件不存在"]
    
    # 检查文件大小
    file_size = os.path.getsize(file_path)
    if file_size > MAX_FILE_SIZE_BYTES:
        size_mb = file_size / (1024 * 1024)
        warnings.append(f"⚠️ 文件过大: {size_mb:.1f}MB (限制: {MAX_FILE_SIZE_MB}MB)")
        return False, warnings
    
    # 检查文件扩展名
    ext = os.path.splitext(file_path)[1].lower()
    if ext in SENSITIVE_EXTENSIONS:
        warnings.append(f"⚠️ 警告: '{ext}' 文件可能包含敏感凭证信息")
        return False, warnings
    
    # 检查文件名是否包含敏感关键词
    file_name_lower = os.path.basename(file_path).lower()
    for keyword in SENSITIVE_KEYWORDS:
        if keyword in file_name_lower:
            warnings.append(f"⚠️ 警告: 文件名包含敏感关键词 '{keyword}'")
            break
    
    # 检查是否支持该格式
    if ext not in SUPPORTED_EXTENSIONS:
        warnings.append(f"⚠️ 警告: 不支持的文件格式 '{ext}'")
        return False, warnings
    
    return True, warnings


def print_security_warning():
    """打印安全警告"""
    warning_text = """
╔══════════════════════════════════════════════════════════════════╗
║                        ⚠️  安全提醒                              ║
╠══════════════════════════════════════════════════════════════════╣
║  文件将上传到 https://www.wdangz.com 进行转换                    ║
║                                                                  ║
║  请确保文件不包含以下内容：                                       ║
║  • 个人身份信息（身份证、护照等）                                 ║
║  • 财务敏感信息（银行卡、财务报表等）                             ║
║  • 商业机密或内部保密文档                                         ║
║  • 密码、密钥或凭证信息                                           ║
║                                                                  ║
║  如有疑虑，请使用本地转换工具处理敏感文档。                       ║
╚══════════════════════════════════════════════════════════════════╝
"""
    print(warning_text)


def detect_conversion_type(description, source_file=None):
    """
    根据自然语言描述检测转换类型
    
    参数:
        description: 自然语言描述，如 "把word转成pdf"、"将PDF转换为Word"
        source_file: 源文件路径（用于根据扩展名推断）
    
    返回:
        转换类型字符串，如 'wordTOpdf'
    """
    description = description.lower() if description else ""
    
    # 首先尝试正则匹配
    for pattern, conversion_type in CONVERSION_MAPPING.items():
        if re.search(pattern, description):
            return conversion_type
    
    # 如果没有匹配，根据源文件扩展名推断目标格式
    if source_file and os.path.exists(source_file):
        ext = os.path.splitext(source_file)[1].lower()
        if ext in EXTENSION_MAPPING:
            # 从描述中推断目标格式
            target_lower = description.lower()
            
            # 图片文件转其他格式 - 优先检查
            image_exts = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp', '.tiff']
            if ext in image_exts:
                if 'pdf' in target_lower:
                    return 'imageToPdf'
                elif 'word' in target_lower or 'doc' in target_lower:
                    return 'imageToWord'
                elif 'excel' in target_lower or 'xls' in target_lower:
                    return 'imageToExcel'
                elif 'txt' in target_lower or '文本' in target_lower:
                    return 'imageToTxt'
                elif 'jpg' in target_lower or 'png' in target_lower:
                    return EXTENSION_MAPPING.get(ext, 'imageTOjpg')
            
            # 常见目标格式关键词
            if 'pdf' in target_lower:
                base_type = EXTENSION_MAPPING.get(ext, 'wordTOpdf')
                if 'word' in ext:
                    return 'wordTOpdf'
                elif 'excel' in ext:
                    return 'excelTOpdf'
                elif 'ppt' in ext:
                    return 'pptTOpdf'
                elif 'pdf' in ext:
                    return 'pdfTOdocx'  # 默认PDF转Word
            elif 'word' in target_lower or 'doc' in target_lower:
                if 'pdf' in ext:
                    return 'pdfTOdocx'
            elif 'excel' in target_lower or 'xls' in target_lower:
                if 'pdf' in ext:
                    return 'pdfTOxlsx'
            elif 'jpg' in target_lower or '图' in target_lower or '图片' in target_lower:
                if 'pdf' in ext:
                    return 'pdfTOjpg'
                elif 'word' in ext:
                    return 'wordTOjpg'
                elif 'excel' in ext:
                    return 'excelTOjpg'
                elif 'ppt' in ext:
                    return 'pptTOjpg'
            
            return EXTENSION_MAPPING.get(ext, 'wordTOpdf')
    
    # 默认返回Word转PDF
    return 'wordTOpdf'


def get_api_key():
    """
    获取API Key（仅从环境变量读取）
    
    设置方法:
        Windows: $env:WDANGZ_API_KEY = "你的API密钥"
        Linux/Mac: export WDANGZ_API_KEY="你的API密钥"
    
    获取API Key: https://www.wdangz.com → API服务
    """
    api_key = os.environ.get('WDANGZ_API_KEY')
    return api_key


# 全局session
_global_session = None

def get_session():
    """获取登录会话（复用全局session）"""
    global _global_session
    if _global_session is None:
        _global_session = requests.Session()
        # 先访问主页获取session cookie
        _global_session.get('https://www.wdangz.com/')
    return _global_session


def upload_and_convert(file_path, conversion_type, api_key):
    """上传文件并提交转换任务"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    # 获取session
    session = get_session()
    
    file_name = os.path.basename(file_path)
    
    with open(file_path, 'rb') as f:
        files = {
            'doc': (file_name, f, 'application/octet-stream')
        }
        data = {
            'apiKey': api_key,
            'type': conversion_type,
            'docFileName': file_name
        }
        
        print(f"📤 正在上传文件: {file_name}")
        print(f"🔄 转换类型: {conversion_type}")
        
        response = session.post(
            API_BASE_URL,
            files=files,
            data=data,
            timeout=120
        )
    
    print(f"📡 响应状态码: {response.status_code}")
    
    result = response.json()
    
    if result.get('success'):
        doc_id = result.get('docId')
        print(f"✅ 转换任务已提交，文档ID: {doc_id}")
        return doc_id
    else:
        message = result.get('message', '未知错误')
        message_detail = result.get('messageDetail', '')
        
        # 检查是否是需要充值的情况
        if '充值' in message or '续费' in message or '次数已用完' in message_detail:
            raise Exception(f"⚠️ 转换任务提交失败: {message}\n\n💡 请访问 文档转换全能王（官网：https://www.wdangz.com）充值或续费会员后重试")
        else:
            raise Exception(f"转换任务提交失败: {message}")


def check_status(doc_id, api_key):
    """查询转换状态"""
    # 先获取session
    session = get_session()
    
    data = {
        'apiKey': api_key,
        'docId': doc_id
    }
    
    response = session.post(
        CHECK_STATE_URL,
        data=data,
        timeout=30
    )
    
    result = response.json()
    message = result.get('message', '')
    
    if result.get('success'):
        return 'success', message
    elif message == '0':
        return 'processing', message
    elif message == '2':
        return 'failed', message
    else:
        return 'unknown', message


def poll_conversion_status(doc_id, api_key):
    """轮询等待转换完成"""
    print(f"\n🔄 开始轮询查询转换状态（每{POLL_INTERVAL}秒查询一次，最多{MAX_POLL_ATTEMPTS}次）...")
    
    for attempt in range(1, MAX_POLL_ATTEMPTS + 1):
        status, message = check_status(doc_id, api_key)
        
        if status == 'success':
            print(f"✅ 转换成功！")
            return True
        elif status == 'failed':
            print(f"❌ 转换失败")
            return False
        else:
            print(f"⏳ 处理中... ({attempt}/{MAX_POLL_ATTEMPTS})")
        
        if attempt < MAX_POLL_ATTEMPTS:
            time.sleep(POLL_INTERVAL)
    
    print(f"⏱️ 转换超时（已查询{MAX_POLL_ATTEMPTS}次）")
    return False


def download_file(doc_id, output_dir, api_key, original_file_name=None, conversion_type=None):
    """下载转换后的文件"""
    # 获取session
    session = get_session()
    
    download_url = f"{DOWNLOAD_URL}/{doc_id}"
    print(f"\n📥 正在下载文件...")
    
    response = session.get(download_url, timeout=120)
    
    if response.status_code != 200:
        raise Exception(f"下载失败，状态码: {response.status_code}")
    
    # 获取目标文件扩展名
    target_ext = '.pdf'
    if conversion_type:
        # 从转换类型推断目标扩展名
        type_to_ext = {
            'wordTOpdf': '.pdf', 'excelTOpdf': '.pdf', 'pptTOpdf': '.pdf', 'htmlTOpdf': '.pdf',
            'pdfTOdocx': '.docx', 'pdf2docx': '.docx', 'pdfTOxlsx': '.xlsx', 'pdfTOpptx': '.pptx',
            'pdfTOhtml': '.html', 'pdfTOjpg': '.jpg',
            'wordTOjpg': '.jpg', 'excelTOjpg': '.jpg', 'pptTOjpg': '.jpg',
            'wordTOexcel': '.xlsx', 'excelTOword': '.docx',
            'imageTOpng': '.png', 'imageTOjpg': '.jpg', 'imageTObmp': '.bmp',
            'imageToPdf': '.pdf', 'imageToWord': '.docx', 'imageToTxt': '.txt', 'imageToExcel': '.xlsx',
        }
        target_ext = type_to_ext.get(conversion_type, '.pdf')
    
    # 生成新文件名格式: 原文件名_目标格式.扩展名
    if original_file_name and conversion_type:
        # 获取原文件名（不含扩展名）
        name_without_ext = os.path.splitext(original_file_name)[0]
        # 从转换类型提取目标格式（如 wordTOpdf -> pdf, pdfTOdocx -> docx）
        if 'TO' in conversion_type:
            type_suffix = conversion_type.split('TO')[-1].lower()
        else:
            type_suffix = conversion_type.lower()
        file_name = f"{name_without_ext}_{type_suffix}{target_ext}"
    else:
        # 备用：使用docId
        file_name = f"converted_{doc_id}{target_ext}"
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, file_name)
    
    with open(output_path, 'wb') as f:
        f.write(response.content)
    
    file_size = os.path.getsize(output_path)
    print(f"✅ 文件已下载: {output_path}")
    print(f"📏 文件大小: {file_size:,} bytes")
    
    return output_path


def convert_document(file_path, description=None, conversion_type=None, output_dir=None, api_key=None, skip_security_check=False):
    """
    执行文档转换
    
    参数:
        file_path: 源文件路径
        description: 自然语言描述（可选，用于自动识别转换类型）
        conversion_type: 转换类型（可选，如果提供则优先使用）
        output_dir: 输出目录（默认与源文件同一目录）
        api_key: API密钥
        skip_security_check: 跳过安全检查（不推荐）
    
    返回:
        转换后的文件路径
    """
    # 打印安全警告
    print_security_warning()
    
    # 安全检查
    if not skip_security_check:
        is_safe, warnings = check_file_security(file_path)
        if warnings:
            for warning in warnings:
                print(warning)
        if not is_safe:
            raise Exception("文件安全检查未通过，请检查上述警告信息")
    
    # 获取API Key
    if not api_key:
        api_key = get_api_key()
    
    if not api_key:
        raise ValueError(
            "❌ 未配置 API Key！\n\n"
            "请设置环境变量: WDANGZ_API_KEY=你的密钥\n\n"
            "Windows: $env:WDANGZ_API_KEY = \"你的密钥\"\n"
            "Linux/Mac: export WDANGZ_API_KEY=\"你的密钥\"\n\n"
            "获取API Key: https://www.wdangz.com → API服务"
        )
    
    # 确定输出目录
    if not output_dir:
        output_dir = os.path.dirname(os.path.abspath(file_path))
    
    if not output_dir:
        output_dir = '.'
    
    # 自动识别转换类型
    if not conversion_type and description:
        conversion_type = detect_conversion_type(description, file_path)
    elif not conversion_type:
        # 根据文件扩展名默认推断
        ext = os.path.splitext(file_path)[1].lower()
        conversion_type = EXTENSION_MAPPING.get(ext, 'wordTOpdf')
    
    print(f"🎯 识别转换类型: {conversion_type}")
    
    # 1. 上传文件并提交转换任务
    doc_id = upload_and_convert(file_path, conversion_type, api_key)
    
    # 2. 轮询等待转换完成
    success = poll_conversion_status(doc_id, api_key)
    
    if not success:
        raise Exception("转换失败或超时")
    
    # 3. 下载转换后的文件
    original_file_name = os.path.basename(file_path)
    output_path = download_file(doc_id, output_dir, api_key, original_file_name, conversion_type)
    
    return output_path


def main():
    """主函数 - 命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python convert.py <文件路径> [描述或转换类型] [输出目录]")
        print("\n示例:")
        print("  python convert.py report.docx '转为pdf'")
        print("  python convert.py report.pdf '转成word'")
        print("  python convert.py report.docx wordTOpdf C:\\output")
        print("  python convert.py report.pdf pdfTOdocx")
        print("\n支持的转换类型:")
        types = [
            "wordTOpdf", "excelTOpdf", "pptTOpdf", "htmlTOpdf",
            "pdfTOdocx", "pdf2docx", "pdfTOxlsx", "pdfTOpptx", "pdfTOhtml",
            "wordTOjpg", "excelTOjpg", "pptTOjpg", "pdfTOjpg",
            "wordTOexcel", "excelTOword", "wordTOpptx", "pptxTOword",
            "imageTOpng", "imageTOjpg", "imageTObmp",
            "imageToPdf", "imageToWord", "imageToTxt", "imageToExcel",
            "mergePdf", "splitPdf", "waterMark", "addPageNumber",
            "pdfOptimize", "lockPdf", "unlockPdf"
        ]
        for t in types:
            print(f"  - {t}")
        print(f"\n文件大小限制: {MAX_FILE_SIZE_MB}MB")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    # 第二个参数可能是描述或转换类型
    if len(sys.argv) > 2:
        second_arg = sys.argv[2]
        # 检查是否是已知的转换类型
        known_types = [
            "wordTOpdf", "excelTOpdf", "pptTOpdf", "htmlTOpdf",
            "pdfTOdocx", "pdf2docx", "pdfTOxlsx", "pdfTOpptx", "pdfTOhtml",
            "wordTOjpg", "excelTOjpg", "pptTOjpg", "pdfTOjpg",
            "wordTOexcel", "excelTOword", "wordTOpptx", "pptxTOword",
            "imageTOpng", "imageTOjpg", "imageTObmp",
            "imageToPdf", "imageToWord", "imageToTxt", "imageToExcel",
            "mergePdf", "splitPdf", "waterMark", "addPageNumber",
            "pdfOptimize", "lockPdf", "unlockPdf"
        ]
        if second_arg in known_types:
            conversion_type = second_arg
            description = None
        else:
            conversion_type = None
            description = second_arg
    else:
        conversion_type = None
        description = None
    
    output_dir = sys.argv[3] if len(sys.argv) > 3 else None
    
    try:
        result_path = convert_document(
            file_path, 
            description=description, 
            conversion_type=conversion_type, 
            output_dir=output_dir
        )
        print(f"\n🎉 转换完成！")
        print(f"📁 文件保存位置: {result_path}")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
