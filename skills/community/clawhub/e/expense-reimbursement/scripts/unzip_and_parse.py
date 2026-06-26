#!/usr/bin/env python3
"""
报销票据解压+XML解析脚本

依赖声明：
  pip install python-docx  # 表单填写
  tesseract + tesseract-ocr-lang-chi  # OCR（Linux/Windows）

用法：
  python3 unzip_and_parse.py

环境变量（可选，默认使用 ~/Desktop/报销/）：
  export REIMBURSEMENT_DIR="/your/custom/path/"
"""
import zipfile
import os
import xml.etree.ElementTree as ET

# ── 可配置路径（支持环境变量覆盖）──────────────────────────────
REIMBURSEMENT_DIR = os.environ.get(
    "REIMBURSEMENT_DIR",
    os.path.join(os.path.expanduser("~/Desktop"), "报销")
)
UNZIP_TEMP = os.path.join(REIMBURSEMENT_DIR, "00_原始资料", "02_解压临时文件", "unzip_temp")
ZIPS_DIR   = os.path.join(REIMBURSEMENT_DIR, "00_原始资料", "01_差旅报销备份")

# ── 平台兼容 ────────────────────────────────────────────────
import platform
IS_MACOS = platform.system() == "Darwin"
IS_WINDOWS = platform.system() == "Windows"


def ensure_dirs():
    """确保目录存在"""
    os.makedirs(UNZIP_TEMP, exist_ok=True)
    os.makedirs(ZIPS_DIR, exist_ok=True)


def unzip_all():
    """
    递归解压 ZIPS_DIR 下所有 ZIP 文件到 unzip_temp/。
    兼容：ZIP 内再嵌套 ZIP 的情况（递归解压一层）。
    """
    if not os.path.exists(ZIPS_DIR):
        print(f"[WARN] ZIP目录不存在: {ZIPS_DIR}")
        return

    zips = [f for f in os.listdir(ZIPS_DIR) if f.endswith(".zip")]
    if not zips:
        print("[INFO] 未找到任何ZIP文件")
        return

    for zname in sorted(zips):
        zpath = os.path.join(ZIPS_DIR, zname)
        folder = zname.replace(".zip", "")
        out_dir = os.path.join(UNZIP_TEMP, folder)
        os.makedirs(out_dir, exist_ok=True)

        with zipfile.ZipFile(zpath, "r") as z:
            z.extractall(out_dir)
            print(f"  ✓ {zname} → {folder}/ ({len(z.namelist())} files)")

            # ZIP内再嵌套ZIP → 再解一层
            nested = [n for n in z.namelist() if n.endswith(".zip")]
            for nzip in nested:
                try:
                    with zipfile.ZipFile(os.path.join(out_dir, nzip), "r") as nz:
                        subfolder = nzip.replace(".zip", "")
                        nz.extractall(os.path.join(out_dir, subfolder))
                        print(f"    └ {nzip} (nested, extracted)")
                except Exception as e:
                    print(f"    └ {nzip} (nested, FAILED: {e})")


def parse_xml(path):
    """解析高德打车发票XML，返回关键字段（兼容多种命名空间）"""
    try:
        tree = ET.parse(path)
        root = tree.getroot()

        def find(tag):
            # 尝试无命名空间 + 标准XSD命名空间
            for t in [tag, f"{{{ns}}}{tag.split('}')[1] if '}' in tag else tag}"
                      for ns in ["", "http://invoice.xsd", "http://www.typing/xsd"]]:
                r = root.find(f".//{t}")
                if r is not None and r.text:
                    return r.text.strip()
            return ""

        return {
            "seller":       find("SellerName"),
            "addr":         find("SellerAddr"),
            "amount":       find("TotalTax-includedAmount"),
            "request_time": find("RequestTime"),
            "issue_time":   find("IssueTime"),
        }
    except Exception as e:
        return {"seller": "", "addr": "", "amount": "", "request_time": "", "issue_time": "", "error": str(e)}


def city_from_addr(addr):
    """从服务商地址关键词判断城市（支持中英文，可扩展）"""
    if not addr:
        return "未知"
    kw_map = [
        # 中国城市
        (["苏州", "相城区", "姑苏区"], "苏州"),
        (["杭州", "拱墅", "滨江", "萧山", "余杭", "西湖区", "临平"], "杭州"),
        (["北京", "朝阳区", "海淀区", "丰台区", "东城区", "西城区"], "北京"),
        (["哈尔滨", "道里", "南岗", "香坊"], "哈尔滨"),
        (["无锡", "梁溪", "新吴"], "无锡"),
        (["上海", "浦东", "黄浦", "静安", "徐汇"], "上海"),
        (["义乌"], "义乌"),
        (["南京", "玄武", "鼓楼"], "南京"),
        (["深圳", "南山", "福田", "宝安"], "深圳"),
        (["广州", "天河", "越秀", "番禺"], "广州"),
        (["成都", "锦江", "高新", "武侯"], "成都"),
        (["武汉", "武昌", "洪山", "江汉"], "武汉"),
        (["西安", "雁塔", "碑林"], "西安"),
        (["重庆", "渝中", "江北", "南岸"], "重庆"),
        (["天津", "和平", "河西"], "天津"),
        # 东南亚
        (["Singapore", "Tanjong", "Raffles"], "Singapore"),
        (["Bangkok", "Sukhumvit", "Silom"], "Bangkok"),
        (["Kuala Lumpur", "Petaling Jaya", "Bangsar"], "Kuala Lumpur"),
        (["Jakarta", "Sudirman", "Thamrin"], "Jakarta"),
        (["Bali", "Denpasar", "Kuta", "Seminyak"], "Bali"),
        (["Ho Chi Minh", "District 1", "Nguyen", "Pham"], "Ho Chi Minh City"),
        (["Hanoi", "Old Quarter", "Ba Dinh"], "Hanoi"),
        (["Manila", "Makati", "BGC", "Bonifacio"], "Manila"),
        (["Grab/", "Grab ", "Grabz"], "Southeast Asia"),
        # 欧洲
        (["London", "Westminster", "Camden", "Hackney"], "London"),
        (["Paris", "Rue ", "Boulevard ", "Av. "], "Paris"),
        (["Berlin", "Mitte", "Kreuzberg", "Prenzlauer"], "Berlin"),
        (["Amsterdam", "Centrum", "Zuid", "Noord"], "Amsterdam"),
        (["Barcelona", "Eixample", "Gràcia", "Barceloneta"], "Barcelona"),
        (["Madrid", "Centro", "Salamanca", "Chueca"], "Madrid"),
        (["Milan", "Centro", "Brera", "Navigli"], "Milan"),
        (["Rome", "Centro", "Trastevere", "Testaccio"], "Rome"),
        # 美国
        (["New York", "Manhattan", "Brooklyn", "Queens"], "New York"),
        (["Los Angeles", "LAX", "Santa Monica", "Venice"], "Los Angeles"),
        (["San Francisco", "SOMA", "Mission", "Castro"], "San Francisco"),
        (["Chicago", "Loop", "Lincoln Park", "Wicker"], "Chicago"),
        (["Seattle", "Downtown", "Capitol Hill", "Belltown"], "Seattle"),
        (["Boston", "Back Bay", "Beacon Hill", "South End"], "Boston"),
    ]
    for keywords, city in kw_map:
        if any(k in addr for k in keywords):
            return city
    return "其他:" + addr[:18]


def scan_receipts():
    """扫描解压目录，解析所有XML，生成清单"""
    if not os.path.exists(UNZIP_TEMP):
        print("[INFO] 解压目录不存在，先运行 unzip_all()")
        return []

    rows = []
    for folder in sorted(os.listdir(UNZIP_TEMP)):
        folder_path = os.path.join(UNZIP_TEMP, folder)
        if not os.path.isdir(folder_path):
            continue
        for fname in sorted(os.listdir(folder_path)):
            if not fname.endswith(".xml"):
                continue
            fpath = os.path.join(folder_path, fname)
            data = parse_xml(fpath)
            data["folder"] = folder
            data["xml_file"] = fname
            data["city"] = city_from_addr(data.get("addr", ""))
            rows.append(data)

    if not rows:
        print("[INFO] 未解析到任何XML票据")
        return rows

    print(f"\n{'#':<4} {'文件夹':<22} {'金额':>8}  {'服务商':<28}  {'城市':<8}  {'开票日期'}")
    print("-" * 95)
    for i, r in enumerate(rows, 1):
        amt    = r.get("amount", "")
        seller = r.get("seller", "")[:26]
        city   = r.get("city", "")
        issue  = r.get("issue_time", "")[:10]
        error  = r.get("error", "")
        note   = f" ⚠ {error}" if error else ""
        print(f"{i:<4} {r['folder']:<22} {amt:>8}  {seller:<28}  {city:<8}  {issue}{note}")

    print(f"\n共解析 {len(rows)} 张票据")
    return rows


if __name__ == "__main__":
    print(f"[INFO] 报销目录: {REIMBURSEMENT_DIR}")
    print(f"[INFO] 解压目录: {UNZIP_TEMP}")
    print(f"[INFO] ZIP目录:  {ZIPS_DIR}")
    print()
    ensure_dirs()
    print("=== 解压所有ZIP ===")
    unzip_all()
    print()
    print("=== 解析XML票据清单 ===")
    scan_receipts()
