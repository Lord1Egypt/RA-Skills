#!/usr/bin/env python3
"""
pdf-insurance-organizer: 识别PDF保险单 → 提取信息 → 重命名文件 → 打包ZIP
支持模式:
  本地模式 (默认): 使用 pdfminer.six 提取文本 + 正则匹配
  API 模式 (--api): 调用外部 AI API 解析（需设置环境变量 INSURANCE_API_KEY）
"""
import argparse
import os
import re
import sys
import zipfile
from datetime import datetime

PDFMINER_OK = False
try:
    from pdfminer.high_level import extract_text
    PDFMINER_OK = True
except ImportError:
    pass


# ─────────────────────────────────────────────
#  PDF 信息提取
# ─────────────────────────────────────────────

def extract_pdf_info(pdf_path: str, use_api: bool = False) -> dict:
    """
    从 PDF 保险单中提取关键字段。
    返回: {车牌号, 投保人, 保单号, 原始路径}
    """
    info = {"车牌号": None, "投保人": None, "保单号": None, "原始路径": pdf_path}

    if use_api:
        return _extract_via_api(pdf_path, info)

    return _extract_via_local(pdf_path, info)


def _extract_via_local(pdf_path: str, info: dict) -> dict:
    """本地模式：pdfminer + 正则匹配"""
    if not PDFMINER_OK:
        print("⚠️  未安装 pdfminer.six，请运行: pip install pdfminer.six")
        return info

    try:
        text = extract_text(pdf_path)
    except Exception as e:
        print(f"⚠️  PDF 文本提取失败: {e}")
        return info

    info["车牌号"] = _find_plate(text)
    info["投保人"] = _find_holder(text)
    info["保单号"] = _find_policy_no(text)
    return info


def _find_plate(text: str) -> str | None:
    """
    车牌号提取：标签 '车牌号' 后跨行查找省级简称+字母+数字组合
    支持格式：晋MX0923、京A12345、沪AZ9999 等
    """
    # 方法1：在 '车牌号' 标签后 150 字符内查找
    idx = text.find("车牌号")
    if idx != -1:
        chunk = text[idx:idx + 200]
        m = re.search(r'([\u4e00-\u9fa5]{1,2}[A-Z][A-Z0-9]{4,6})', chunk)
        if m:
            return m.group(1)

    # 方法2：直接全局扫描常见省份车牌格式
    province = "京津沪渝苏浙皖闽赣鲁豫鄂湘粤桂琼川贵云藏陕甘青宁新蒙"
    patterns = [
        rf'([{province}]{{1}}[A-Z][A-Z0-9]{{4,6}})',  # 省简称 + 字母 + 数字
    ]
    for pat in patterns:
        m = re.search(pat, text)
        if m:
            return m.group(1)
    return None


def _find_holder(text: str) -> str | None:
    """
    投保人/被保险人名称提取：找公司名（最常见）或自然人姓名
    """
    # 在 '投保人' 标签后找公司名称
    for label in ["投保人", "被保险人"]:
        idx = text.find(label)
        if idx == -1:
            continue
        chunk = text[idx:idx + 300]
        # 匹配公司名称：公司...（公司名通常包含"公司"）
        m = re.search(r'公司[^\n\r]{0,50}', chunk)
        if m:
            name = m.group(0)
            # 清理杂项字符
            name = re.sub(r'\s+', ' ', name).strip()
            return name
        # 匹配自然人姓名（2-4个汉字）
        m = re.search(r'([\u4e00-\u9fa5]{2,4})(?=\s*公司|\s*证件)', chunk)
        if m:
            return m.group(1)

    # 兜底：找第一个包含 "公司" 的长行
    for line in text.split('\n'):
        line = line.strip()
        if '公司' in line and len(line) >= 4:
            return re.sub(r'\s+', '', line)[:40]
    return None


def _find_policy_no(text: str) -> str | None:
    """保单号码提取"""
    for label in ["保单号码", "保单号"]:
        idx = text.find(label)
        if idx == -1:
            continue
        chunk = text[idx:idx + 100]
        m = re.search(r'([A-Z0-9]{15,22})', chunk)
        if m:
            return m.group(1)
    return None


def _extract_via_api(pdf_path: str, info: dict) -> dict:
    """
    API 模式：读取 PDF 并发送给 AI API 解析。
    需要设置环境变量:
      INSURANCE_API_KEY      - API 密钥
      INSURANCE_API_ENDPOINT - API 端点（默认使用 OpenAI 兼容接口）
    """
    import json

    api_key = os.environ.get("INSURANCE_API_KEY", "")
    endpoint = os.environ.get(
        "INSURANCE_API_ENDPOINT",
        "https://api.openai.com/v1/chat/completions"
    )
    model = os.environ.get("INSURANCE_API_MODEL", "gpt-4o")

    if not api_key:
        print("⚠️  INSURANCE_API_KEY 未设置，回退到本地模式")
        return _extract_via_local(pdf_path, info)

    import base64
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()
    b64_pdf = base64.b64encode(pdf_bytes).decode()

    prompt = (
        "你是一个保险单据分析助手。请从以下保险单PDF base64内容中提取:\n"
        "1. 车牌号\n2. 投保人/被保险人名称\n3. 保单号码\n\n"
        "只返回JSON格式，不要任何其他文字:\n"
        '{"车牌号":"","投保人":"","保单号":""}'
    )

    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "file", "file": {"filename": os.path.basename(pdf_path)}}
            ]}
        ]
    }

    import urllib.request
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        content = result["choices"][0]["message"]["content"]
        # 尝试解析 JSON
        m = re.search(r'\{[^}]+\}', content)
        if m:
            parsed = json.loads(m.group(0))
            info["车牌号"] = parsed.get("车牌号") or None
            info["投保人"] = parsed.get("投保人") or None
            info["保单号"] = parsed.get("保单号") or None
    except Exception as e:
        print(f"⚠️  API 调用失败: {e}，回退到本地模式")
        return _extract_via_local(pdf_path, info)

    return info


# ─────────────────────────────────────────────
#  文件重命名
# ─────────────────────────────────────────────

def rename_file(pdf_path: str, plate: str = None, policy_no: str = None) -> str:
    """
    重命名文件，命名规则：
      有车牌号 → {原名}_{车牌号}{.pdf}
      无车牌号但有保单号 → {原名}_{保单号}{.pdf}
      都没有 → 跳过重命名
    返回新的文件路径
    """
    suffix = plate if plate else policy_no
    if not suffix:
        print(f"   ⚠️  车牌号和保单号均未识别，跳过重命名")
        return pdf_path

    directory = os.path.dirname(pdf_path) or "."
    basename = os.path.splitext(os.path.basename(pdf_path))[0]
    ext = os.path.splitext(pdf_path)[1]

    new_name = f"{basename}_{suffix}{ext}"
    new_path = os.path.join(directory, new_name)

    if new_path != pdf_path and os.path.exists(new_path):
        print(f"   ⚠️  目标文件已存在: {new_name}，跳过重命名")
        return pdf_path

    os.rename(pdf_path, new_path)
    print(f"   ✅ 重命名: {os.path.basename(pdf_path)} → {new_name}")
    return new_path


# ─────────────────────────────────────────────
#  ZIP 打包
# ─────────────────────────────────────────────

def pack_to_zip(folder: str, zip_name: str = None) -> str:
    """
    将 folder 中所有文件打包为 ZIP。
    zip_name 默认: 保险单整理_YYYYMMDD.zip
    返回 ZIP 文件的绝对路径
    """
    if zip_name is None:
        today = datetime.now().strftime("%Y%m%d")
        zip_name = f"保险单整理_{today}.zip"

    zip_path = os.path.join(folder, zip_name)

    # 排除 ZIP 自身
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                if file_path == zip_path:
                    continue
                arcname = os.path.relpath(file_path, folder)
                zf.write(file_path, arcname)

    size = os.path.getsize(zip_path)
    print(f"   ✅ ZIP 打包完成: {zip_name} ({size / 1024:.1f} KB)")
    return zip_path


# ─────────────────────────────────────────────
#  主流程
# ─────────────────────────────────────────────

def process_folder(
    folder: str,
    use_api: bool = False,
    do_rename: bool = True,
    do_pack: bool = True,
    zip_name: str = None,
) -> list:
    """
    处理 folder 中所有 PDF 文件。
    返回处理结果列表
    """
    folder = os.path.abspath(folder)
    pdf_files = sorted([
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith(".pdf")
    ])

    if not pdf_files:
        print(f"📂 文件夹中未找到 PDF 文件: {folder}")
        return []

    print(f"📋 发现 {len(pdf_files)} 个 PDF 文件")
    print(f"🤖 解析模式: {'API' if use_api else '本地 (pdfminer.six)'}")
    print("─" * 50)

    results = []
    for pdf_path in pdf_files:
        print(f"\n📄 {os.path.basename(pdf_path)}")
        info = extract_pdf_info(pdf_path, use_api=use_api)
        print(f"   车牌号: {info['车牌号'] or '❓ 未识别'}")
        print(f"   投保人: {info['投保人'] or '❓ 未识别'}")
        print(f"   保单号: {info['保单号'] or '❓ 未识别'}")

        new_path = pdf_path
        if do_rename:
            new_path = rename_file(pdf_path, info["车牌号"], info["保单号"])

        results.append({
            "原始路径": pdf_path,
            "新路径": new_path,
            **info
        })

    print("\n" + "=" * 50)
    print(f"✅ 处理完成: {len(results)} 个文件")

    if do_pack:
        zip_path = pack_to_zip(folder, zip_name)
        print(f"📦 ZIP: {zip_path}")

    return results


def main():
    parser = argparse.ArgumentParser(
        description="保险单 PDF 识别与整理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python extract_and_rename.py ~/Downloads
  python extract_and_rename.py ~/Downloads --api
  python extract_and_rename.py ~/Downloads --no-rename
  python extract_and_rename.py ~/Downloads --zip-name "我的保单_20260428.zip"

环境变量:
  INSURANCE_API_KEY       API密钥（API模式必需）
  INSURANCE_API_ENDPOINT   API端点（默认: OpenAI兼容接口）
  INSURANCE_API_MODEL      模型名称（默认: gpt-4o）
        """
    )
    parser.add_argument("folder", nargs="?", default=".",
                        help="PDF 文件所在文件夹（默认当前目录）")
    parser.add_argument("--no-rename", action="store_true",
                        help="跳过文件重命名")
    parser.add_argument("--no-pack", action="store_true",
                        help="跳过 ZIP 打包")
    parser.add_argument("--api", action="store_true",
                        help="使用 API 模式解析（需设置 INSURANCE_API_KEY）")
    parser.add_argument("--zip-name",
                        help="自定义 ZIP 文件名")
    args = parser.parse_args()

    folder = os.path.abspath(args.folder)
    if not os.path.isdir(folder):
        print(f"❌ 不是有效的目录: {folder}")
        sys.exit(1)

    print(f"📂 工作目录: {folder}")

    process_folder(
        folder,
        use_api=args.api,
        do_rename=not args.no_rename,
        do_pack=not args.no_pack,
        zip_name=args.zip_name,
    )


if __name__ == "__main__":
    main()
