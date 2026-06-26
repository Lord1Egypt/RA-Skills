# clean_drawing.py
# 图纸原始文本清洗去噪脚本
# 上游输入：dxf-text-extractor 输出的原始 Markdown 文本
# 下游输出：结构化分类 Markdown，供 boq-generator 使用

import re
import sys
import os
import argparse

# ─────────────────────────────────────────────
# 1. 噪声过滤规则
# ─────────────────────────────────────────────

# 1-A: 纯噪声模式（命中即整行丢弃）
NOISE_PATTERNS = [
    # 轴线编号：单个字母或1-2位纯数字（A、B、①、1、12）
    r'^[A-Za-z]$',
    r'^[①②③④⑤⑥⑦⑧⑨⑩]$',
    r'^\d{1,2}$',

    # 残留编码乱码
    r'^%%',
    r'^\?+$',
    r'^\\[A-Za-z]',

    # 图框/标题栏常见字段（设计院、日期、签名类）
    r'^(设计|制图|校对|审核|审定|专业负责人|项目负责人|批准)[：:]*\s*\S*$',
    r'^(日期|比例|阶段|图号|版本|修改)[：:]*',
    r'^\d{4}[.\-年]\d{1,2}[.\-月]?\d{0,2}日?$',  # 日期格式
    r'^[A-Z]-\d{2,4}$',                            # 图号格式 如 S-0101
    r'^第\s*\d+\s*页',
    r'^共\s*\d+\s*张',

    # 单独的尺寸数字（无单位、无上下文，4位以内纯数字）
    r'^\d{3,4}$',

    # 坐标标注（如 X=1000.000）
    r'^[XYZxyz][=＝]\d+',

    # 纯标点或极短无意义文本
    r'^[，。；：、！？\.\,\;\:\!\?]{1,3}$',
    r'^.{1}$',  # 单字符（字母、数字、标点均已在上面处理，这里兜底）

    # 上游分栏标题行（来自 dxf-text-extractor 的章节标记）
    r'^第\s*\d+\s*栏内容',
    r'^DXF\s*(结构|图纸)',

    # 设计院/公司名称（包含关键词即过滤）
    r'(设计院|研究院|设计所|设计公司|工程公司|勘察院)',
]

# 1-B: 图框区域关键词（行内包含即丢弃）
NOISE_KEYWORDS = [
    '工程名称', '建设单位', '勘察单位', '设计单位',
    '注册建筑师', '注册结构师', '证书编号',
    '出图专用章', '电子签名', '此图作废',
    'AutoCAD', 'TSSD', 'pkpm', 'PKPM',
]

# ─────────────────────────────────────────────
# 2. 分类规则（优先级从高到低匹配）
# ─────────────────────────────────────────────

CATEGORY_RULES = [
    # --- 图纸元信息 ---
    {
        'tag': '图纸信息',
        'patterns': [
            r'(结构|建筑|水暖|电气).*(施工图|平面图|立面图|剖面图|详图|大样)',
            r'(梁|板|柱|墙|基础).*(平法|配筋|布置)',
            r'^\d+[FBf层]|^[Bb]\d+|^地[上下]?\d+层',  # 楼层标识
            r'(总说明|设计说明|结构说明)',
        ]
    },
    # --- 设计总说明类（高价值，必须完整保留）---
    {
        'tag': '设计总说明',
        'patterns': [
            r'(抗震等级|设防烈度|抗震设防)',
            r'(环境类别|耐久性)',
            r'(保护层|钢筋保护层).*(厚度|mm)',
            r'(混凝土强度|砂浆强度|灌浆料)',
            r'(钢筋.*(HPB|HRB|HRBF|RRB)|HPB300|HRB[0-9]{3})',
            r'(地基.*(承载力|处理)|持力层|地基)',
            r'(变形缝|沉降缝|伸缩缝|防震缝)',
            r'(填充墙|砌体|砌块)',
            r'(施工.*(要求|注意|规范)|验收规范)',
            r'(图集|标准图|通用图).*(选用|参照|执行)',
        ]
    },
    # --- 构件标识（平法标注）---
    {
        'tag': '构件标识',
        'patterns': [
            # 梁：KL、L、WKL、LL、AL 等
            r'^(KL|WKL|LL|AL|JL|GL|TL|XL|QL|KZL|L)\d+[(\（]?\d*[)\）]?\s*\d+[xX×]\d+',
            r'^(KL|WKL|LL|AL|JL|GL|TL|XL|QL|KZL|L)\d+',
            # 柱：KZ、Z、GZ、SZ 等
            r'^(KZ|GZ|SZ|YZ|Z)\d+\s*\d+[xX×]\d+',
            r'^(KZ|GZ|SZ|YZ|Z)\d+',
            # 板：LB、WB、B、DB 等
            r'^(LB|WB|YWB|DB|B)\d+\s+[hH]?\s*=?\s*\d+',
            # 墙：Q、YQ、AQ、JQ 等
            r'^(YQ|AQ|JQ|Q)\d+\s+\d+',
            # 基础：JC、CT、DJJ、JZL 等
            r'^(JC|CT|DJJ|JZL|ZH|CF|JL)\d+',
            # 楼梯：AT、BT、CT 等梯板
            r'^(AT|BT|CT|ET|FT|GT|HT|IT)\d+',
            # 截面尺寸（独立出现的 300x500 等）
            r'^\d{2,4}[xX×]\d{2,4}(\s*mm)?$',
        ]
    },
    # --- 配筋信息 ---
    {
        'tag': '配筋信息',
        'patterns': [
            r'\d+[A-D]\d+',          # 如 4C20、2A8
            r'[A-D]\d+@\d+',         # 如 C8@200
            r'φ\d+@?\d*',            # 如 φ8@150
            r'Φ\d+@?\d*',
            r'(上部|下部|侧面|腰筋|箍筋|拉筋|纵筋).*(筋|钢筋)',
            r'(通长|架立|支座|跨中).*(筋|钢筋)',
            r'(加密区|非加密区)',
        ]
    },
    # --- 材料强度 ---
    {
        'tag': '材料强度',
        'patterns': [
            r'[Cc]\d{2,3}',                      # C30、C35 等
            r'(混凝土|砼).*(强度|等级)',
            r'M\d+',                              # 砂浆强度 M10
            r'(砖|砌块).*(MU\d+|强度)',
            r'(钢材|钢板|型钢|钢管).*(Q\d{3}|强度)',
            r'Q\d{3}[A-D]?',                     # Q235、Q345
        ]
    },
    # --- 标高与尺寸 ---
    {
        'tag': '标高尺寸',
        'patterns': [
            r'[±＋\+\-]?\d+\.\d{3}',            # 标高 ±0.000、-0.450
            r'(梁底|板底|柱顶|层高|净高).*(标高|=|\d)',
            r'H\s*=\s*\d+',                      # H=3000
            r'(层高|净高|净跨|轴距)\s*[:=：]\s*\d+',
        ]
    },
    # --- 节点与做法说明 ---
    {
        'tag': '节点做法',
        'patterns': [
            r'(节点|详图|大样)\s*[详见|参见|同|按]',
            r'详(见|参)\s*(图|第)',
            r'(锚固|搭接).*(长度|要求|laE|la)',
            r'(弯钩|弯折|端部)',
            r'(植筋|后锚固|化学锚栓)',
        ]
    },
]

# ─────────────────────────────────────────────
# 3. 核心清洗函数
# ─────────────────────────────────────────────

def is_noise(text: str) -> bool:
    """判断一行文本是否为噪声"""
    stripped = text.strip()
    if not stripped:
        return True

    # 关键词命中
    for kw in NOISE_KEYWORDS:
        if kw in stripped:
            return True

    # 模式命中：^ 开头用行首匹配，否则用全行搜索
    for pat in NOISE_PATTERNS:
        if pat.startswith('^'):
            if re.match(pat, stripped, re.IGNORECASE):
                return True
        else:
            if re.search(pat, stripped, re.IGNORECASE):
                return True

    return False


def classify_line(text: str) -> str:
    """对一行文本进行分类，返回分类标签，无法分类返回 '其他'"""
    for rule in CATEGORY_RULES:
        for pat in rule['patterns']:
            if re.search(pat, text, re.IGNORECASE):
                return rule['tag']
    return '其他'


def clean_and_classify(raw_lines: list[str]) -> dict[str, list[str]]:
    """
    输入：原始文本行列表
    输出：按分类归并的字典 { '设计总说明': [...], '构件标识': [...], ... }
    """
    result: dict[str, list[str]] = {rule['tag']: [] for rule in CATEGORY_RULES}
    result['其他'] = []

    for line in raw_lines:
        # 去掉 Markdown 格式符号（来自上游的 ## --- 第N栏 --- 和 空行）
        cleaned = re.sub(r'^#+\s*', '', line).strip()
        cleaned = re.sub(r'^-+\s*', '', cleaned).strip()
        cleaned = re.sub(r'\s*\|\s*', '  ', cleaned)  # 保留列内容，替换分隔符

        if not cleaned:
            continue

        # 如果一行包含多个由上游合并的片段（用 | 拼接），拆开分别处理
        segments = [s.strip() for s in cleaned.split('  ') if s.strip()]

        for seg in segments:
            if is_noise(seg):
                continue
            tag = classify_line(seg)
            # 去重：同一分类下不重复添加
            if seg not in result[tag]:
                result[tag].append(seg)

    return result


# ─────────────────────────────────────────────
# 4. 读取 & 输出
# ─────────────────────────────────────────────

def process_file(input_path: str, output_path: str = None):
    """读取上游 Markdown 文件，输出清洗后的结构化 Markdown"""

    with open(input_path, 'r', encoding='utf-8') as f:
        raw_lines = f.readlines()

    classified = clean_and_classify(raw_lines)

    # 统计
    total_input = sum(1 for l in raw_lines if l.strip() and not l.startswith('#'))
    total_output = sum(len(v) for v in classified.values())
    noise_removed = total_input - total_output

    # 构建输出内容
    base_name = os.path.basename(input_path).replace('分栏提取_', '').replace('.md', '')
    lines_out = [
        f"# 清洗结果：{base_name}\n\n",
        f"> 输入行数：{total_input}　|　",
        f"去噪行数：{noise_removed}　|　",
        f"保留行数：{total_output}　|　",
        f"去噪率：{noise_removed/max(total_input,1)*100:.1f}%\n\n",
        "---\n\n",
    ]

    # 按分类输出，跳过空分类
    # 优先输出高价值分类
    priority_order = ['图纸信息', '设计总说明', '材料强度', '构件标识', '配筋信息', '标高尺寸', '节点做法', '其他']
    for tag in priority_order:
        items = classified.get(tag, [])
        if not items:
            continue
        lines_out.append(f"## [{tag}]\n\n")
        for item in items:
            lines_out.append(f"- {item}\n")
        lines_out.append("\n")

    output_content = ''.join(lines_out)

    # 写文件
    if output_path is None:
        output_path = input_path.replace('分栏提取_', '清洗结果_').replace('.md', '_cleaned.md')
        if output_path == input_path:
            output_path = input_path.replace('.md', '_cleaned.md')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output_content)

    print(f"[成功] 清洗完成！")
    print(f"  输入：{input_path}（{total_input} 行）")
    print(f"  去噪：{noise_removed} 行（去噪率 {noise_removed/max(total_input,1)*100:.1f}%）")
    print(f"  输出：{output_path}（{total_output} 行）")
    return output_path


# ─────────────────────────────────────────────
# 5. CLI 入口
# ─────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='清洗去噪图纸提取文本，输出结构化分类 Markdown')
    parser.add_argument('input_md', nargs='?', default=None,
                        help='上游 dxf-text-extractor 输出的 Markdown 文件路径')
    parser.add_argument('--output', '-o', default=None,
                        help='输出文件路径（默认自动命名）')
    args = parser.parse_args()

    if args.input_md:
        input_path = args.input_md
    else:
        # 自动查找当前目录下以 "分栏提取_" 开头的 md 文件
        import glob
        candidates = glob.glob("分栏提取_*.md") + glob.glob("*.md")
        if not candidates:
            print("错误：未找到可处理的 Markdown 文件，请指定文件路径")
            sys.exit(1)
        input_path = candidates[0]
        print(f"自动选取文件：{input_path}")

    if not os.path.exists(input_path):
        print(f"错误：文件不存在：{input_path}")
        sys.exit(1)

    process_file(input_path, args.output)
