# extract_text.py
import sys
import ezdxf
import re
import os
import math

# 1. 钢筋符号映射库 (包含你之前侦探到的所有乱码和私有编码)
REBAR_SYMBOL_MAP = {
    # 钢筋等级符号
    "%%130": "A", "%%131": "B", "%%132": "C", "%%133": "D",
    "\x82": "A", "\x83": "B", "\x84": "C", "\x85": "D",
    "\ue531": "A", "\ue532": "C", "\ue533": "D", "\ue530": "A",
    "\u0082": "A", "\u0083": "B", "\u0084": "C", "\u0085": "D",
    # CAD 常用特殊符号
    "%%c": "Φ",    # 直径符号
    "%%d": "°",     # 度符号
    "%%p": "±",     # 正负号
    "%%u": "",      # 下划线开始（通常忽略）
    "%%o": "",      # 上划线开始（通常忽略）
    "%%%": "%",     # 百分号
    # 上标/下标数字
    "%%178": "²",   # 上标2
    "%%179": "³",   # 上标3
    "%%176": "°",   # 度符号（同%%d）
    "%%187": "»",   # 右双尖括号
    "%%171": "«",   # 左双尖括号
}


def clean_cad_text(text):
    if not text:
        return ""

    # 1. 处理钢筋符号映射
    for raw, std in REBAR_SYMBOL_MAP.items():
        text = text.replace(raw, std)

    # 2. 处理 CAD 特殊符号编码（以 %% 开头）
    # 扩展钢筋符号映射：%%130-%%139
    for i in range(130, 140):
        code = f"%%{i}"
        # 根据常见映射：130-133 对应 A-D，其他可能未定义
        if i == 130: text = text.replace(code, "A")
        elif i == 131: text = text.replace(code, "B")
        elif i == 132: text = text.replace(code, "C")
        elif i == 133: text = text.replace(code, "D")
        elif code in text:  # 其他未知编码，替换为 ?
            text = text.replace(code, "?")

    # 处理 %%% 序列（表示单个 % 字符）
    text = text.replace('%%%', '%')

    # 3. 处理其他未知的 %% 数字编码（如 %%140, %%141 等）
    # 使用正则表达式替换所有 %% 后跟数字的序列为 "?"
    text = re.sub(r'%%[0-9]+', '?', text)

    # 4. 清理 MTEXT 格式代码：\A1; \H0.7x; \W0.8; \C1; 等
    # 匹配 \ 后跟非分号字符直到分号
    text = re.sub(r'\\[^;]*;', ' ', text)

    # 4. 处理换行符和花括号
    # 将 \P（段落分隔符）替换为空格，避免破坏行分组
    text = text.replace('\\P', ' ').replace('{', '').replace('}', '')

    # 5. 合并多个空格（包括换行符、制表符等），去除首尾空白
    text = re.sub(r'\s+', ' ', text).strip()

    return text

def run_column_aware_extraction(file_path, column_gap=None, row_tolerance=15):
    try:
        doc = ezdxf.readfile(file_path)
        msp = doc.modelspace()
        all_data = []

        # 1. 递归提取所有文字 (处理块嵌套和坐标偏移)
        def extract_recursive(entities, base_pt=(0,0)):
            for e in entities:
                if e.dxftype() in ('TEXT', 'MTEXT', 'ATTRIB'):
                    # 获取文本，处理不同实体类型
                    if e.dxftype() == 'MTEXT':
                        # 使用 plain_text() 获取纯文本，去除格式代码
                        try:
                            txt = e.plain_text()
                        except AttributeError:
                            # 回退到 text 属性
                            txt = e.text
                    else:  # TEXT 或 ATTRIB
                        txt = e.dxf.text

                    clean_txt = clean_cad_text(txt)
                    if clean_txt:
                        all_data.append({
                            'text': clean_txt,
                            'x': base_pt[0] + e.dxf.insert.x,
                            'y': base_pt[1] + e.dxf.insert.y
                        })
                elif e.dxftype() == 'INSERT':
                    block = doc.blocks.get(e.dxf.name)
                    if block:
                        new_base = (base_pt[0] + e.dxf.insert.x, base_pt[1] + e.dxf.insert.y)
                        extract_recursive(block, new_base)

        extract_recursive(msp)
        if not all_data:
            print("警告：未找到任何文字对象")
            return

        # --- 2. 核心改进：按 X 坐标自动分栏 ---
        # 先按 X 排序
        all_data.sort(key=lambda k: k['x'])
        
        columns = []
        if all_data:
            # 动态计算栏间距阈值（如果未提供）
            if column_gap is None:
                # 计算所有相邻 X 坐标的差异
                x_coords = sorted([item['x'] for item in all_data])
                if len(x_coords) > 1:
                    gaps = [abs(x_coords[i] - x_coords[i-1]) for i in range(1, len(x_coords))]
                    # 使用差异的中位数作为参考，乘以系数
                    if gaps:
                        median_gap = sorted(gaps)[len(gaps)//2]
                        # 栏间距应该比典型字符间距大很多
                        column_gap = max(800, median_gap * 5)  # 确保最小值
                    else:
                        column_gap = 1000  # 默认值
                else:
                    column_gap = 1000  # 默认值

            current_col = [all_data[0]]

            for i in range(1, len(all_data)):
                if abs(all_data[i]['x'] - current_col[-1]['x']) < column_gap:
                    current_col.append(all_data[i])
                else:
                    columns.append(current_col)
                    current_col = [all_data[i]]
            columns.append(current_col)

        # --- 3. 每一栏内部进行 Y 轴排序与导出 ---
        # 使用基础文件名，避免路径问题
        base_name = os.path.basename(file_path)
        name_without_ext = os.path.splitext(base_name)[0]
        output_name = f"分栏提取_{name_without_ext}.md"
        with open(output_name, "w", encoding="utf-8") as f:
            f.write("# DXF 结构图纸分栏提取报告\n\n")
            
            for idx, col in enumerate(columns):
                # 跳过空栏
                if not col:
                    continue

                # 每一栏内部按 Y 轴从高到低排序
                col.sort(key=lambda k: (-k['y'], k['x']))

                f.write(f"## --- 第 {idx + 1} 栏内容 ---\n\n")
                
                # 行分组处理
                if col:  # col 不为空，已经检查过
                    current_line = [col[0]]
                    # 使用传入的行容差参数

                    for i in range(1, len(col)):
                        if abs(col[i]['y'] - current_line[-1]['y']) < row_tolerance:
                            current_line.append(col[i])
                        else:
                            current_line.sort(key=lambda k: k['x'])
                            line_text = "  |  ".join([item['text'] for item in current_line])
                            f.write(line_text + "\n\n")
                            current_line = [col[i]]

                    # 写入该栏最后一行（如果有）
                    if current_line:
                        current_line.sort(key=lambda k: k['x'])
                        line_text = "  |  ".join([item['text'] for item in current_line])
                        f.write(line_text + "\n\n")
                else:
                    f.write("(空栏)\n\n")

        print(f"[成功] 分栏提取完成！已生成: {output_name}")

    except Exception as e:
        print(f"解析失败: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='提取 DXF 结构图纸文本并自动分栏')
    parser.add_argument('dxf_file', nargs='?', default=None, help='DXF 文件路径（默认为当前目录下的 DXF 文件）')
    parser.add_argument('--column-gap', type=float, default=None, help='栏间距阈值（单位：绘图单位），默认自动计算')
    parser.add_argument('--row-tolerance', type=float, default=15, help='行高容差（单位：绘图单位），默认15')
    args = parser.parse_args()

    if args.dxf_file:
        file_path = args.dxf_file
    else:
        # 查找当前目录下的 DXF 文件
        import glob
        dxf_files = glob.glob("*.dxf")
        if not dxf_files:
            print("错误：未找到 DXF 文件，请指定文件路径")
            sys.exit(1)
        file_path = dxf_files[0]
        if len(dxf_files) > 1:
            print(f"找到多个 DXF 文件，使用第一个: {file_path}")

    try:
        run_column_aware_extraction(file_path, column_gap=args.column_gap, row_tolerance=args.row_tolerance)
    except FileNotFoundError:
        print(f"错误：文件不存在: {file_path}")
    except Exception as e:
        print(f"运行错误: {e}")