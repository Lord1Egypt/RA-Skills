#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel公式助手
自然语言 → 公式 | 公式解释 | 公式库 | 错误排查
"""

import re
import sys
from typing import Optional

try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


# 公式模板库
FORMULA_TEMPLATES = {
    "查找引用": {
        "VLOOKUP": {
            "syntax": "=VLOOKUP(查找值, 查找范围, 返回列数, [精确匹配])",
            "params": [
                "查找值：要查找的内容",
                "查找范围：包含查找列和返回列的区域（查找列必须在第一列）",
                "返回列数：从查找范围第一列开始数，第几列的值",
                "精确匹配：FALSE=精确匹配，TRUE=模糊匹配"
            ],
            "examples": [
                ("根据姓名查工资", "=VLOOKUP(A2,员工表!A:D,4,FALSE)"),
                ("根据编号查产品", "=VLOOKUP(B2,产品表!A:F,3,FALSE)")
            ]
        },
        "INDEX+MATCH": {
            "syntax": "=INDEX(返回范围, MATCH(查找值, 查找范围, 0))",
            "params": [
                "返回范围：要返回值的区域",
                "MATCH查找值：要查找的内容",
                "MATCH查找范围：查找值所在的列/行",
                "0：表示精确匹配"
            ],
            "examples": [
                ("反向查找（根据工资查姓名）", "=INDEX(A:A, MATCH(D2, D:D, 0))"),
                ("多条件查找", "=INDEX(C:C, MATCH(1, (A:A=A2)*(B:B=B2), 0))")
            ]
        },
        "XLOOKUP": {
            "syntax": "=XLOOKUP(查找值, 查找数组, 返回数组, [未找到值], [匹配模式])",
            "params": [
                "查找值：要查找的内容",
                "查找数组：查找值所在的列/行",
                "返回数组：要返回值的列/行",
                "未找到值：找不到时返回的内容",
                "匹配模式：0=精确匹配，-1=精确或较小，1=精确或较大"
            ],
            "examples": [
                ("根据姓名查工资（升级版）", "=XLOOKUP(A2, 员工表!A:A, 员工表!D:D, '未找到')"),
                ("查找并返回多个值", "=XLOOKUP(A2, A:A, B:D)")
            ]
        }
    },
    "条件统计": {
        "SUMIFS": {
            "syntax": "=SUMIFS(求和范围, 条件范围1, 条件1, [条件范围2, 条件2], ...)",
            "params": [
                "求和范围：要求和的单元格区域",
                "条件范围1：第一个条件所在的区域",
                "条件1：第一个条件（如 '>100'、'完成'）",
                "条件范围2/条件2：可选的额外条件"
            ],
            "examples": [
                ("按部门统计工资", "=SUMIFS(C:C, B:B, '销售部')"),
                ("多条件求和（部门+状态）", "=SUMIFS(C:C, B:B, '销售部', D:D, '完成')"),
                ("按日期范围求和", "=SUMIFS(C:C, A:A, '>=2024-01-01', A:A, '<=2024-12-31')")
            ]
        },
        "COUNTIFS": {
            "syntax": "=COUNTIFS(条件范围1, 条件1, [条件范围2, 条件2], ...)",
            "params": [
                "条件范围1：第一个条件所在的区域",
                "条件1：第一个条件",
                "条件范围2/条件2：可选的额外条件"
            ],
            "examples": [
                ("统计完成数量", "=COUNTIFS(B:B, '完成')"),
                ("统计某部门完成数", "=COUNTIFS(A:A, '销售部', B:B, '完成')")
            ]
        },
        "AVERAGEIFS": {
            "syntax": "=AVERAGEIFS(平均值范围, 条件范围1, 条件1, ...)",
            "params": [
                "平均值范围：要计算平均值的区域",
                "条件范围1：第一个条件所在的区域",
                "条件1：第一个条件"
            ],
            "examples": [
                ("计算某部门平均工资", "=AVERAGEIFS(C:C, B:B, '销售部')"),
                ("计算完成项目的平均耗时", "=AVERAGEIFS(D:D, E:E, '完成')")
            ]
        }
    },
    "日期时间": {
        "DATEDIF": {
            "syntax": "=DATEDIF(开始日期, 结束日期, 单位)",
            "params": [
                "开始日期：起始日期",
                "结束日期：结束日期",
                "单位：'Y'=年数, 'M'=月数, 'D'=天数, 'YM'=忽略年的月数"
            ],
            "examples": [
                ("计算工龄（年）", "=DATEDIF(A2, TODAY(), 'Y')"),
                ("计算剩余月数", "=DATEDIF(TODAY(), B2, 'M')"),
                ("计算年龄", "=DATEDIF(出生日期单元格, TODAY(), 'Y')")
            ]
        },
        "EOMONTH": {
            "syntax": "=EOMONTH(日期, 月数)",
            "params": [
                "日期：起始日期",
                "月数：0=当月最后一天, 1=下月最后一天, -1=上月最后一天"
            ],
            "examples": [
                ("当月最后一天", "=EOMONTH(TODAY(), 0)"),
                ("合同到期日", "=EOMONTH(入职日期, 36)")
            ]
        },
        "NETWORKDAYS": {
            "syntax": "=NETWORKDAYS(开始日期, 结束日期, [节假日])",
            "params": [
                "开始日期：起始日期",
                "结束日期：结束日期",
                "节假日：可选，节假日列表区域"
            ],
            "examples": [
                ("计算工作日天数", "=NETWORKDAYS(A2, B2)"),
                ("扣除节假日", "=NETWORKDAYS(A2, B2, 节假日!A:A)")
            ]
        }
    },
    "文本处理": {
        "LEFT/RIGHT/MID": {
            "syntax": "=LEFT(文本, 字符数) | =RIGHT(文本, 字符数) | =MID(文本, 起始位置, 字符数)",
            "params": [
                "文本：要提取的文本",
                "字符数：提取的字符数量",
                "起始位置：MID专用，从第几个字符开始"
            ],
            "examples": [
                ("提取身份证生日", "=MID(A2, 7, 8)"),
                ("提取前3位", "=LEFT(A2, 3)"),
                ("提取后4位", "=RIGHT(A2, 4)")
            ]
        },
        "FIND/SUBSTITUTE": {
            "syntax": "=FIND(查找文本, 文本) | =SUBSTITUTE(文本, 旧文本, 新文本, [替换第几个])",
            "params": [
                "查找文本：要查找的内容",
                "文本：被查找的文本",
                "旧文本/新文本：SUBSTITUTE专用"
            ],
            "examples": [
                ("提取邮箱域名", "=RIGHT(A2, LEN(A2)-FIND('@', A2))"),
                ("替换文本", "=SUBSTITUTE(A2, '旧', '新')"),
                ("删除空格", "=SUBSTITUTE(A2, ' ', '')")
            ]
        },
        "TEXT": {
            "syntax": "=TEXT(数值, 格式代码)",
            "params": [
                "数值：要格式化的数值或日期",
                "格式代码：如 'yyyy-mm-dd', '0.00', '0%''"
            ],
            "examples": [
                ("日期格式化", "=TEXT(A2, 'yyyy年mm月dd日')"),
                ("金额格式化", "=TEXT(A2, '¥#,##0.00')"),
                ("百分比", "=TEXT(A2, '0%')")
            ]
        }
    },
    "逻辑判断": {
        "IF/IFS": {
            "syntax": "=IF(条件, 条件真值, 条件假值) | =IFS(条件1, 值1, 条件2, 值2, ...)",
            "params": [
                "条件：判断条件",
                "条件真值：条件为真时返回的值",
                "条件假值：条件为假时返回的值"
            ],
            "examples": [
                ("简单判断", "=IF(A2>100, '高', '低')"),
                ("多条件判断", "=IFS(A2>=90, '优秀', A2>=80, '良好', A2>=60, '及格', A2<60, '不及格')"),
                ("嵌套IF", "=IF(A2>100, IF(B2='VIP', '高VIP', '高'), '低')")
            ]
        },
        "IFERROR": {
            "syntax": "=IFERROR(公式, 错误时返回值)",
            "params": [
                "公式：可能出错的公式",
                "错误时返回值：出错时显示的内容"
            ],
            "examples": [
                ("VLOOKUP防错", "=IFERROR(VLOOKUP(A2, B:C, 2, FALSE), '未找到')"),
                ("除零防错", "=IFERROR(A2/B2, 0)")
            ]
        }
    }
}


# 自然语言到公式的映射规则
NL_TO_FORMULA_RULES = [
    # VLOOKUP相关
    (r"查找.*(匹配|对应|等于).*的.*值", "VLOOKUP"),
    (r"根据.*查.*", "VLOOKUP"),
    (r".*列中.*等于.*的.*", "VLOOKUP"),

    # SUMIFS相关
    (r"求.*和.*且.*", "SUMIFS"),
    (r"统计.*之和.*条件", "SUMIFS"),
    (r"按.*统计.*总和", "SUMIFS"),

    # COUNTIFS相关
    (r"统计.*数量.*条件", "COUNTIFS"),
    (r"统计.*有几个", "COUNTIFS"),

    # DATEDIF相关
    (r"计算.*(天数|月数|年数|工龄|年龄)", "DATEDIF"),
    (r".*相差.*(天|月|年)", "DATEDIF"),

    # LEFT/MID/RIGHT相关
    (r"提取.*(前|后|第).*(位|字符)", "LEFT/RIGHT/MID"),
    (r"从.*提取.*", "LEFT/RIGHT/MID"),

    # IF相关
    (r"如果.*则.*否则", "IF"),
    (r"判断.*是.*还是", "IF"),
]


def generate_formula(description: str, use_ai: bool = False) -> str:
    """根据自然语言描述生成公式"""

    # 尝试AI生成
    if use_ai and HAS_OPENAI:
        try:
            import os
            api_key = os.environ.get("OPENAI_API_KEY")
            if api_key:
                client = openai.OpenAI(api_key=api_key)
                prompt = f"""将以下需求转换为Excel公式。只返回公式，不要解释。

需求：{description}

公式："""
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=100
                )
                return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"AI生成失败，使用模板匹配: {e}")

    # 模板匹配
    desc_lower = description.lower()

    # 查找引用类
    if re.search(r"查找.*匹配|根据.*查|查.*对应", desc_lower):
        return """建议公式：=VLOOKUP(查找值, 查找范围, 返回列数, FALSE)

示例：=VLOOKUP(A2, 数据表!A:D, 3, FALSE)

参数说明：
- 查找值：要查找的内容（如A2单元格）
- 查找范围：包含查找列和返回列的区域
- 返回列数：从查找范围第一列数起，第几列
- FALSE：精确匹配"""

    # 条件求和类
    if re.search(r"求.*和.*且|统计.*之和.*条件|按.*统计.*总和", desc_lower):
        return """建议公式：=SUMIFS(求和范围, 条件范围1, 条件1, 条件范围2, 条件2)

示例：=SUMIFS(C:C, A:A, ">100", B:B, "完成")

参数说明：
- 求和范围：要求和的列
- 条件范围1：第一个条件所在的列
- 条件1：第一个条件（如">100"）
- 条件范围2/条件2：可选的额外条件"""

    # 条件计数类
    if re.search(r"统计.*数量|统计.*有几个|计算.*个数", desc_lower):
        return """建议公式：=COUNTIFS(条件范围1, 条件1, 条件范围2, 条件2)

示例：=COUNTIFS(A:A, "销售部", B:B, "完成")

参数说明：
- 条件范围1：第一个条件所在的列
- 条件1：第一个条件"""

    # 日期计算类
    if re.search(r"计算.*(天数|月数|年数|工龄|年龄)|相差.*(天|月|年)", desc_lower):
        return """建议公式：=DATEDIF(开始日期, 结束日期, 单位)

示例：=DATEDIF(A2, TODAY(), "Y")

参数说明：
- 开始日期：起始日期单元格
- 结束日期：结束日期（可用TODAY()表示今天）
- 单位："Y"=年数, "M"=月数, "D"=天数"""

    # 文本提取类
    if re.search(r"提取.*(前|后|第|位)|从.*提取", desc_lower):
        return """建议公式：
- 提取前N位：=LEFT(文本, N)
- 提取后N位：=RIGHT(文本, N)
- 提取中间：=MID(文本, 起始位置, 字符数)

示例（提取身份证生日）：=MID(A2, 7, 8)"""

    # 条件判断类
    if re.search(r"如果.*则|判断.*是|大于.*显示|小于.*显示", desc_lower):
        return """建议公式：=IF(条件, 条件真时的值, 条件假时的值)

示例：=IF(A2>100, "高", "低")

参数说明：
- 条件：判断条件（如A2>100）
- 条件真时的值：条件为真时显示的内容
- 条件假时的值：条件为假时显示的内容"""

    # 默认返回帮助
    return """无法直接匹配公式，请尝试以下方式：

1. 使用 list 命令查看公式库
   python excel_formula.py list --category lookup

2. 查看具体公式帮助
   python excel_formula.py explain VLOOKUP

3. 使用更具体的描述，如：
   - "查找A列中与D2匹配的B列值"
   - "求A列大于100且B列为完成的C列之和"
   - "计算A2到今天的相差年数"
"""


def explain_formula(formula: str) -> str:
    """解释公式"""
    formula = formula.strip()
    if not formula.startswith('='):
        formula = '=' + formula

    # 提取函数名
    match = re.match(r'=([A-Za-z]+)', formula)
    if not match:
        return "无法识别的公式格式"

    func_name = match.group(1).upper()

    # 查找公式说明
    for category, formulas in FORMULA_TEMPLATES.items():
        for name, info in formulas.items():
            if func_name in name:
                result = [f"【{name}】{category}"]
                result.append(f"语法：{info['syntax']}")
                result.append("")
                result.append("参数说明：")
                for param in info['params']:
                    result.append(f"  • {param}")
                result.append("")
                result.append("示例：")
                for desc, example in info['examples']:
                    result.append(f"  • {desc}")
                    result.append(f"    {example}")
                return "\n".join(result)

    # 通用解释
    return f"""【{func_name}】

公式：{formula}

这是一个Excel内置函数。建议：
1. 使用 list 命令查看完整公式库
2. 在Excel中按Shift+F3查看函数帮助
3. 搜索"Excel {func_name} 函数用法"获取详细教程
"""


def list_formulas(category: str = None):
    """列出公式"""
    if category:
        # 查找匹配的类别
        for cat_name, formulas in FORMULA_TEMPLATES.items():
            if category.lower() in cat_name.lower():
                print(f"【{cat_name}】")
                for name in formulas.keys():
                    print(f"  • {name}")
                return
        print(f"未找到类别：{category}")
        print(f"可用类别：{', '.join(FORMULA_TEMPLATES.keys())}")
    else:
        print("Excel公式库（按类别）：")
        for cat_name, formulas in FORMULA_TEMPLATES.items():
            print(f"\n【{cat_name}】")
            for name in formulas.keys():
                print(f"  • {name}")


def diagnose_error(formula: str, error: str) -> str:
    """诊断公式错误"""
    error_diagnosis = {
        "#N/A": """#N/A 错误诊断：

可能原因：
1. VLOOKUP/XLOOKUP 找不到匹配值
2. 查找值与查找范围格式不一致（文本vs数字）
3. 查找范围第一列不包含查找值

修复方法：
1. 检查查找值是否正确
2. 使用 =ISTEXT() 和 =ISNUMBER() 检查格式
3. 使用 =IFERROR(公式, "未找到") 美化错误显示
4. 确保查找范围包含目标数据""",

        "#VALUE!": """#VALUE! 错误诊断：

可能原因：
1. 公式中使用了错误的数据类型
2. 文本参与了数学运算
3. 数组公式未正确输入

修复方法：
1. 检查参与运算的单元格格式
2. 使用 =VALUE() 将文本转为数字
3. 使用 =TEXT() 将数字转为文本
4. 数组公式需按 Ctrl+Shift+Enter 输入""",

        "#REF!": """#REF! 错误诊断：

可能原因：
1. 公式引用的单元格/区域已被删除
2. 复制公式时相对引用出错
3. VLOOKUP返回列数超出范围

修复方法：
1. 检查公式中的引用是否有效
2. 使用绝对引用 $A$1 代替相对引用 A1
3. 检查VLOOKUP的返回列数参数""",

        "#DIV/0!": """#DIV/0! 错误诊断：

可能原因：
1. 除数为0或空值
2. 平均值计算时无有效数据

修复方法：
1. 使用 =IFERROR(公式, 0) 或 =IFERROR(公式, "N/A")
2. 先检查除数：=IF(B2=0, "N/A", A2/B2)""",

        "#NAME?": """#NAME? 错误诊断：

可能原因：
1. 函数名拼写错误
2. 使用了不存在的自定义名称
3. 文本未加引号

修复方法：
1. 检查函数名拼写（如 VLOOKUP 不是 VLOKUP）
2. 文本参数需加引号，如 "完成"
3. 确保使用了正确的函数名"""
    }

    if error.upper() in error_diagnosis:
        return error_diagnosis[error.upper()]

    return f"""【{error}】错误诊断：

这是一个Excel错误代码。

建议：
1. 检查公式语法是否正确
2. 确认所有引用的单元格都存在
3. 检查数据类型是否匹配
4. 搜索"Excel {error} 解决方法"获取详细帮助
"""


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Excel公式助手")
    subparsers = parser.add_subparsers(dest='command', help='命令')

    # generate命令
    gen_parser = subparsers.add_parser('generate', help='根据描述生成公式')
    gen_parser.add_argument('description', help='自然语言描述')
    gen_parser.add_argument('--ai', action='store_true', help='使用AI增强')

    # explain命令
    exp_parser = subparsers.add_parser('explain', help='解释公式')
    exp_parser.add_argument('formula', help='要解释的公式')

    # list命令
    list_parser = subparsers.add_parser('list', help='列出公式库')
    list_parser.add_argument('--category', '-c', help='类别过滤')

    # diagnose命令
    diag_parser = subparsers.add_parser('diagnose', help='诊断公式错误')
    diag_parser.add_argument('formula', help='出错的公式')
    diag_parser.add_argument('--error', '-e', required=True, help='错误代码')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == 'generate':
        result = generate_formula(args.description, use_ai=args.ai)
        print(result)
    elif args.command == 'explain':
        result = explain_formula(args.formula)
        print(result)
    elif args.command == 'list':
        list_formulas(args.category)
    elif args.command == 'diagnose':
        result = diagnose_error(args.formula, args.error)
        print(result)


if __name__ == "__main__":
    main()
