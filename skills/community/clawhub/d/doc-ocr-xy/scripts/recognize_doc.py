#!/usr/bin/env python3
"""
文档 OCR 识别脚本
使用翔云 OCR API 识别文档并提取信息

用法:
  python recognize_doc.py <文件路径>           # 识别单个文件，直接输出结果
  python recognize_doc.py <文件夹路径>         # 识别文件夹，生成 md 文件
  python recognize_doc.py --config            # 配置翔云凭证
  python recognize_doc.py --list-config       # 查看当前配置
"""

import os
import sys
import json
import base64
import re
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

# 图像处理库（用于转换不支持的格式）
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# 支持的文件格式
SUPPORTED_FORMATS = {'.pdf', '.ofd', '.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff', '.webp'}

endpoint = "https://netocr.com/api/recog_table_base64"


def convert_image_to_jpg(file_path: str) -> bytes:
    """将图像文件转换为 JPG 格式的字节数据"""
    if not PIL_AVAILABLE:
        raise ImportError("需要安装 Pillow 库: pip install Pillow")

    with Image.open(file_path) as img:
        # 转换为 RGB 模式（处理灰度、黑白、RGBA 等）
        if img.mode in ('L', '1', 'RGBA', 'P'):
            # 黑白/灰度/调色板图像转换为 RGB
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = rgb_img
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        # 保存为 JPG
        import io
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=95)
        return buffer.getvalue()


def load_config():
    """加载配置文件"""
    config_path = Path(__file__).parent.parent / "config.json"
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_config(config: dict):
    """保存配置文件"""
    config_path = Path(__file__).parent.parent / "config.json"
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def call_netocr_ocr(image_data: bytes, netocr_key: str, netocr_secret: str, typeId: str = "3050") -> dict:
    """调用翔云 OCR API (base64 模式，multipart/form-data)"""
    

    img_b64 = base64.b64encode(image_data).decode('utf-8')

    # 自动旋转：0 关闭(默认)、1 开启
    autoRotation = 1
    
    # 版面分析：0 关闭(默认)、1 开启
    layout = 1 

    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    body_parts = [
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"key\"\r\n\r\n{netocr_key}",
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"secret\"\r\n\r\n{netocr_secret}",
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"typeId\"\r\n\r\n{typeId}",
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"autoRotation\"\r\n\r\n{autoRotation}",
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"layout\"\r\n\r\n{layout}",
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"img\"\r\n\r\n{img_b64}",
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"format\"\r\n\r\njson",
        f"--{boundary}--",
    ]
    body = "\r\n".join(body_parts).encode('utf-8')

    try:
        req = urllib.request.Request(endpoint, data=body, method='POST')
        req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
        with urllib.request.urlopen(req, timeout=60) as response:
            raw = response.read().decode('utf-8', errors='replace')
            return json.loads(raw)
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8', errors='replace')
        return {"Code": "HttpError", "Message": f"HTTP {e.code}: {error_body}"}
    except Exception as e:
        return {"Code": "Error", "Message": str(e)}


def html_to_markdown(html_content: str) -> str:
    """将 HTML 内容转换为 Markdown 格式"""
    from html.parser import HTMLParser

    class TableParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.paragraphs = []
            self.table_rows = []
            self.current_text = ""
            self.in_table = False
            self.in_tr = False
            self.in_td = False
            self.in_th = False
            self.in_p = False
            self.current_row = []
            self.current_cell = ""
            self.row_positions = []
            self.cell_positions = []

        def handle_starttag(self, tag, attrs):
            if tag == 'table':
                self.in_table = True
                self.table_rows = []
                self.row_positions = []
            elif tag == 'tr':
                self.in_tr = True
                self.current_row = []
                self.cell_positions = []
            elif tag == 'td':
                self.in_td = True
                self.current_cell = ""
                # 提取位置信息
                for attr, val in attrs:
                    if attr == 'RectRow':
                        self.cell_positions.append(val)
            elif tag == 'th':
                self.in_th = True
                self.current_cell = ""
            elif tag == 'p':
                self.in_p = True
                self.current_text = ""

        def handle_endtag(self, tag):
            if tag == 'table':
                self.in_table = False
            elif tag == 'tr':
                self.in_tr = False
                if self.current_row:
                    self.table_rows.append(self.current_row[:])
                    self.row_positions.append(self.cell_positions[:])
                self.current_row = []
            elif tag == 'td':
                self.in_td = False
                self.current_row.append(self.current_cell.strip())
            elif tag == 'th':
                self.in_th = False
                self.current_row.append(self.current_cell.strip())
            elif tag == 'p':
                self.in_p = False
                text = self.current_text.strip()
                if text:
                    self.paragraphs.append(text)
                self.current_text = ""

        def handle_data(self, data):
            if self.in_td or self.in_th:
                self.current_cell += data
            elif self.in_p:
                self.current_text += data

        def build_md(self):
            lines = []
            # 输出段落
            for p in self.paragraphs:
                lines.append(p)
            lines.append("")

            # 输出表格
            if self.table_rows and self.table_rows[0]:
                col_count = len(self.table_rows[0])
                header = self.table_rows[0]
                lines.append("| " + " | ".join(header) + " |")
                lines.append("| " + " | ".join(["---"] * col_count) + " |")
                for row in self.table_rows[1:]:
                    # 补齐或截断列
                    while len(row) < col_count:
                        row.append("")
                    row = row[:col_count]
                    lines.append("| " + " | ".join(row) + " |")

            return "\n".join(lines)

    parser = TableParser()
    try:
        parser.feed(html_content)
    except Exception:
        pass

    result = parser.build_md()
    if not result.strip():
        # 如果解析失败，使用备用方案提取文本
        result = extract_plain_text(html_content)
    return result


def extract_plain_text(html_content: str) -> str:
    """备用：提取纯文本"""
    text = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<head[^>]*>.*?</head>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<p[^>]*>', '', text)
    text = re.sub(r'<span[^>]*>', '', text)
    text = re.sub(r'<br\s*/?>', '\n', text)
    text = re.sub(r'</p>', '\n', text)
    text = re.sub(r'</div>', '\n', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()


def extract_text_from_html(html_content: str) -> str:
    """从 HTML 中提取 Markdown 格式内容"""
    return html_to_markdown(html_content)


def recognize_single_file(file_path: str, netocr_key: str, netocr_secret: str) -> str:
    """识别单个文件并返回纯文本结果"""
    print(f"正在识别: {file_path}")

    def do_recognize(data: bytes) -> str:
        ocr_result = call_netocr_ocr(data, netocr_key, netocr_secret, "3050")

        if ocr_result.get("message", {}).get("status") != 0:
            return None, ocr_result.get("message", {}).get("value", "未知错误")

        info = ocr_result.get("info", {})
        result_list = info.get("result", [])

        if not result_list:
            return "[未识别到内容]", None

        html_table = result_list[0].get("table", "")
        return extract_text_from_html(html_table), None

    try:
        with open(file_path, 'rb') as f:
            image_data = f.read()

        # 首次尝试识别
        result, error = do_recognize(image_data)
        if result is not None:
            return result

        # 识别失败，尝试转换为 JPG 后重试
        print(f"  首次识别失败，尝试转换图像格式...")
        if PIL_AVAILABLE:
            try:
                jpg_data = convert_image_to_jpg(file_path)
                result, error = do_recognize(jpg_data)
                if result is not None:
                    print(f"  转换格式后识别成功")
                    return result
            except ImportError:
                print(f"  需要安装 Pillow: pip install Pillow")
            except Exception as e:
                print(f"  图像转换失败: {e}")

        return f"[识别失败] {error}"

    except Exception as e:
        return f"[异常] {str(e)}"


def scan_folder(folder_path: str) -> list:
    """扫描文件夹中的所有文档"""
    folder = Path(folder_path)
    if not folder.exists():
        print(f"错误：文件夹不存在: {folder_path}")
        return []

    files = []
    for file in folder.rglob('*'):
        if file.is_file() and file.suffix.lower() in SUPPORTED_FORMATS:
            files.append(str(file))

    return sorted(files)


def recognize_folder(folder_path: str, netocr_key: str, netocr_secret: str) -> dict:
    """识别文件夹中的所有文档"""
    files = scan_folder(folder_path)

    if not files:
        return {"error": f"未找到文档，支持的格式: {', '.join(sorted(SUPPORTED_FORMATS))}"}

    print(f"找到 {len(files)} 个文档，开始识别...\n")

    results = {}
    for i, file_path in enumerate(files, 1):
        print(f"[{i}/{len(files)}] {os.path.basename(file_path)}...")
        text = recognize_single_file(file_path, netocr_key, netocr_secret)
        results[file_path] = text

    return results


def generate_md_output(results: dict, folder_name: str) -> str:
    """生成 Markdown 格式的输出"""
    md_content = [
        f"# OCR 识别结果",
        f"",
        f"- **识别时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- **源文件夹**: {folder_name}",
        f"- **文件数量**: {len(results)}",
        f"",
    ]

    for i, (file_path, text) in enumerate(results.items(), 1):
        filename = os.path.basename(file_path)
        md_content.append(f"---")
        md_content.append(f"")
        md_content.append(f"## {i}. {filename}")
        md_content.append(f"")
        md_content.append(f"**文件路径**: `{file_path}`")
        md_content.append(f"")
        md_content.append(f"### 识别内容")
        md_content.append(f"")
        md_content.append(text if text else "[未识别到内容]")
        md_content.append(f"")

    return "\n".join(md_content)


def main():
    """主函数"""
    # 设置输出编码为 UTF-8
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

    if len(sys.argv) < 2:
        print("文档 OCR 识别工具")
        print("")
        print("用法:")
        print("  python recognize_doc.py <文件路径>           # 识别单个文件")
        print("  python recognize_doc.py <文件夹路径>         # 识别文件夹，生成 md")
        print("  python recognize_doc.py --config            # 配置翔云凭证")
        print("  python recognize_doc.py --list-config       # 查看当前配置")
        print("")
        print("支持的文件格式: PDF, OFD, JPG, PNG, BMP")
        sys.exit(1)

    # 处理配置命令
    if sys.argv[1] == "--config":
        print("请输入翔云配置信息:")
        netocr_key = input("netocr_key: ").strip()
        netocr_secret = input("netocr_secret: ").strip()
        config = {
            "netocr_key": netocr_key,
            "netocr_secret": netocr_secret
        }
        save_config(config)
        print("配置已保存!")
        return

    if sys.argv[1] == "--list-config":
        config = load_config()
        if config:
            print("当前配置:")
            print(f"  OCR Key: {config.get('netocr_key', '(未设置)')}")
            print(f"  OCR Secret: {'*' * 8 if config.get('netocr_secret') else '(未设置)'}")
        else:
            print("尚未配置，请运行: python recognize_doc.py --config")
        return

    # 加载配置
    config = load_config()
    netocr_key = config.get("netocr_key")
    netocr_secret = config.get("netocr_secret")

    if not netocr_key or not netocr_secret:
        print("错误：未配置翔云凭证")
        print("")
        print("请先运行以下命令配置凭证:")
        print("  python recognize_doc.py --config")
        sys.exit(1)

    # 解析参数
    input_path = sys.argv[1]

    # 判断是文件还是文件夹
    if Path(input_path).is_file():
        # 单文件模式：直接输出结果
        print(f"=== 识别文件: {input_path} ===\n")
        result = recognize_single_file(input_path, netocr_key, netocr_secret)
        print(result)
    elif Path(input_path).is_dir():
        # 文件夹模式：生成 md 文件
        print(f"=== 识别文件夹: {input_path} ===\n")
        results = recognize_folder(input_path, netocr_key, netocr_secret)

        if "error" in results:
            print(results["error"])
            return

        # 生成 md 文件
        folder_name = os.path.basename(os.path.abspath(input_path))
        md_content = generate_md_output(results, folder_name)

        output_path = Path(input_path) / f"OCR结果_{folder_name}.md"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md_content)

        print(f"\n识别完成！结果已保存至: {output_path}")
    else:
        print(f"错误：路径不存在: {input_path}")


if __name__ == "__main__":
    main()
