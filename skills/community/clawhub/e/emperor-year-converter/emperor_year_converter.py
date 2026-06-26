#!/usr/bin/env python3
"""
帝王纪年 ↔ 公元纪年 转换工具

数据来源: https://hanzi.unihan.com.cn/Emperor
覆盖范围: 西周厉王（公元前878年）至 清宣统（1911年）

用法:
    python emperor_year_converter.py                    # 交互模式
    python emperor_year_converter.py 贞观 2             # 帝王纪年 → 公元
    python emperor_year_converter.py --ad 645           # 公元 → 帝王纪年
    python emperor_year_converter.py --ad -221          # 公元前 → 帝王纪年
    python emperor_year_converter.py --search 乾隆      # 搜索年号
    python emperor_year_converter.py --list 唐           # 列出某朝代所有年号
"""

import json
import os
import sys

# ── 年号数据（内嵌） ────────────────────────────────────────

DATA = None

def _load_data():
    """加载年号数据"""
    global DATA
    if DATA is not None:
        return DATA

    # 优先从同目录的 JSON 文件加载
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "emperor_years_data.json")
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            DATA = json.load(f)
        return DATA

    print("错误: 找不到 emperor_years_data.json 数据文件", file=sys.stderr)
    sys.exit(1)


# ── 简繁转换（常见历史用字） ──────────────────────────────────

_SIMP_TO_TRAD = str.maketrans(
    "贞观宁庆显圣应义兴万历启国祯统临丰顺乐熙绍鉴庄权总宝祐龙凤华诏阳宪仪纪继绥靖济维嘉猷祺纶纯昭恒咸丕延泰康盛简灵惠襄匡桓献殇",
    "貞觀寧慶顯聖應義興萬曆啟國禎統臨豐順樂熙紹鑒莊權總寶祐龍鳳華詔陽憲儀紀繼綏靖濟維嘉猷祺綸純昭恆咸丕延泰康盛簡靈惠襄匡桓獻殤",
)

_TRAD_TO_SIMP = str.maketrans(
    "貞觀寧慶顯聖應義興萬曆啟國禎統臨豐順樂熙紹鑒莊權總寶祐龍鳳華詔陽憲儀紀繼綏靖濟維嘉猷祺綸純昭恆咸丕延泰康盛簡靈惠襄匡桓獻殤",
    "贞观宁庆显圣应义兴万历启国祯统临丰顺乐熙绍鉴庄权总宝祐龙凤华诏阳宪仪纪继绥靖济维嘉猷祺纶纯昭恒咸丕延泰康盛简灵惠襄匡桓献殇",
)


def _to_trad(text):
    """简体转繁体（仅覆盖年号常用字）"""
    return text.translate(_SIMP_TO_TRAD)


def _to_simp(text):
    """繁体转简体（仅覆盖年号常用字）"""
    return text.translate(_TRAD_TO_SIMP)


def _match_exact(keyword, text):
    """精确匹配：年号名完全等于关键词"""
    return (keyword == text or
            _to_trad(keyword) == text or
            _to_simp(keyword) == text)


def _match(keyword, text):
    """模糊匹配：关键词是文本的子串"""
    return (keyword in text or
            _to_trad(keyword) in text or
            _to_simp(keyword) in text)


def _find_entries(reign_name):
    """
    查找匹配的年号条目，优先精确匹配，无结果再模糊匹配。
    返回匹配的 entry 列表。
    """
    data = _load_data()

    # 第一轮：精确匹配年号名
    exact = [e for e in data if _match_exact(reign_name, e["reign"])]
    if exact:
        return exact

    # 第二轮：精确匹配帝王名
    exact_emperor = [e for e in data if _match_exact(reign_name, e["emperor"])]
    if exact_emperor:
        return exact_emperor

    # 第三轮：模糊匹配年号名（子串）
    fuzzy = [e for e in data if _match(reign_name, e["reign"])]
    if fuzzy:
        return fuzzy

    # 第四轮：模糊匹配帝王名（子串）
    return [e for e in data if _match(reign_name, e["emperor"])]

def format_ad(year):
    """格式化公元纪年"""
    if year > 0:
        return f"公元{year}年"
    elif year < 0:
        return f"公元前{-year}年"
    else:
        return "公元0年（不存在）"


def reign_to_ad(reign_name, nth_year=1):
    """
    帝王纪年 → 公元纪年
    
    参数:
        reign_name: 年号名称（如"贞观"、"康熙"、"建元"）
        nth_year: 第几年（默认1）
    返回:
        匹配结果列表 [{"dynasty", "emperor", "reign", "nth_year", "ad_year", "ad_text"}, ...]
    """
    data = _load_data()
    results = []

    for entry in _find_entries(reign_name):

            start = entry["start"]
            end = entry["end"]
            # 计算实际可用年数（跳过公元0年）
            duration = 0
            for y in range(start, end + 1):
                if y != 0:
                    duration += 1

            if nth_year < 1 or nth_year > duration:
                results.append({
                    "dynasty": entry["dynasty"],
                    "emperor": entry["emperor"],
                    "reign": entry["reign"],
                    "error": f"年份超出范围（该年号共{duration}年，范围: 1~{duration}）",
                    "total_years": duration,
                    "start": start,
                    "end": end,
                })
                continue

            # 计算公元年（跳过0年）
            ad_year = start
            count = 0
            for y in range(start, end + 1):
                if y != 0:
                    count += 1
                    if count == nth_year:
                        ad_year = y
                        break

            results.append({
                "dynasty": entry["dynasty"],
                "emperor": entry["emperor"],
                "reign": entry["reign"],
                "nth_year": nth_year,
                "ad_year": ad_year,
                "ad_text": format_ad(ad_year),
                "total_years": duration,
                "start": start,
                "end": end,
            })

    return results


def ad_to_reign(ad_year):
    """
    公元纪年 → 帝王纪年
    
    参数:
        ad_year: 公元年（负数为公元前）
    返回:
        匹配结果列表 [{"dynasty", "emperor", "reign", "nth_year", "ad_year", "ad_text"}, ...]
    """
    data = _load_data()
    results = []

    if ad_year == 0:
        return [{"error": "公元0年不存在，公元前1年的下一年是公元1年"}]

    for entry in data:
        start = entry["start"]
        end = entry["end"]

        if start <= ad_year <= end:
            # 计算是该年号的第几年
            nth = 0
            for y in range(start, ad_year + 1):
                if y != 0:
                    nth += 1

            duration = sum(1 for y in range(start, end + 1) if y != 0)

            results.append({
                "dynasty": entry["dynasty"],
                "emperor": entry["emperor"],
                "reign": entry["reign"],
                "nth_year": nth,
                "ad_year": ad_year,
                "ad_text": format_ad(ad_year),
                "total_years": duration,
            })

    return results


def search_reign(keyword):
    """搜索年号/帝王/朝代"""
    data = _load_data()
    results = []
    keyword_lower = keyword.lower()

    for entry in data:
        if (_match(keyword, entry["dynasty"]) or
            _match(keyword, entry["emperor"]) or
            _match(keyword, entry["reign"])):
            results.append(entry)

    return results


def list_dynasty(dynasty_keyword):
    """列出某朝代所有年号"""
    data = _load_data()
    results = []

    for entry in data:
        if _match(dynasty_keyword, entry["dynasty"]):
            results.append(entry)

    return results


# ── 输出格式化 ──────────────────────────────────────────────

def print_reign_results(results, query=""):
    """打印年号转公元结果"""
    if not results:
        print(f"  未找到匹配「{query}」的年号")
        print(f"  提示: 试试 --search {query} 搜索相关年号")
        return

    # 分离成功和失败的结果
    ok_results = [r for r in results if "error" not in r]
    err_results = [r for r in results if "error" in r]

    # 先输出成功结果
    for r in ok_results:
        print(f"  ✅ {r['dynasty']} · {r['emperor']} · {r['reign']} {r['nth_year']}年 → {r['ad_text']}")
        print(f"     年号跨度: {format_ad(r['start'])}~{format_ad(r['end'])}（共{r['total_years']}年）")

    # 如果有成功结果，错误结果折叠显示
    if ok_results and err_results:
        print(f"  （另有 {len(err_results)} 个含「{query}」的年号因年份超出范围未显示）")
    elif err_results:
        # 全部失败，显示前几条详情
        for r in err_results[:5]:
            name = f"{r['dynasty']} · {r['emperor']} · {r['reign']}" if "dynasty" in r else ""
            if name:
                print(f"  ⚠ {name}（{format_ad(r['start'])}~{format_ad(r['end'])}）")
                print(f"    {r['error']}")
            else:
                print(f"  ❌ {r['error']}")
        if len(err_results) > 5:
            print(f"  ...还有 {len(err_results) - 5} 个同名年号也超出范围")


def print_ad_results(results, ad_year):
    """打印公元转年号结果"""
    if not results:
        if ad_year < -878 or ad_year > 1911:
            print(f"  {format_ad(ad_year)} 超出数据范围（公元前878年~公元1911年）")
        else:
            print(f"  {format_ad(ad_year)} 未找到对应的帝王纪年")
        return

    if "error" in results[0]:
        print(f"  ❌ {results[0]['error']}")
        return

    print(f"  📅 {format_ad(ad_year)} 对应：")
    for r in results:
        reign_text = f"{r['reign']} {r['nth_year']}年" if r['reign'] != "無" else f"在位第{r['nth_year']}年（无年号）"
        print(f"     {r['dynasty']} · {r['emperor']} · {reign_text}")


def print_search_results(results, keyword):
    """打印搜索结果"""
    if not results:
        print(f"  未找到与「{keyword}」相关的记录")
        return

    print(f"  找到 {len(results)} 条相关记录：\n")
    current_dynasty = ""
    for r in results:
        if r["dynasty"] != current_dynasty:
            current_dynasty = r["dynasty"]
            print(f"  【{current_dynasty}】")

        reign_text = r['reign'] if r['reign'] != '無' else '（无年号）'
        start_text = format_ad(r['start'])
        end_text = format_ad(r['end'])
        duration = sum(1 for y in range(r['start'], r['end'] + 1) if y != 0)
        print(f"    {r['emperor']} · {reign_text}  {start_text}~{end_text}（{duration}年）")


# ── 批量转换 ────────────────────────────────────────────────

def batch_convert(input_path, output_path=None):
    """
    批量转换，从文件读取，每行一条。
    
    支持格式（自动识别）：
        贞观 2          → 年号转公元
        康熙            → 年号元年转公元
        公元 645        → 公元转年号
        公元前 221      → 公元前转年号
        -221            → 负数视为公元前
        645             → 正数视为公元
    """
    if not os.path.exists(input_path):
        print(f"  ❌ 文件不存在: {input_path}")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip() and not l.startswith("#")]

    output_lines = []
    output_lines.append(f"# 批量转换结果（共 {len(lines)} 条）\n")

    success = 0
    fail = 0

    for line in lines:
        parts = line.split()

        # 公元前 N
        if parts[0] == "公元前" and len(parts) >= 2:
            try:
                year = -abs(int(parts[1]))
                results = ad_to_reign(year)
                if results and "error" not in results[0]:
                    items = []
                    for r in results:
                        reign_text = f"{r['reign']} {r['nth_year']}年" if r['reign'] != "無" else f"在位第{r['nth_year']}年"
                        items.append(f"{r['dynasty']} {r['emperor']} {reign_text}")
                    output_lines.append(f"{line}\t→\t{' / '.join(items)}")
                    success += 1
                else:
                    output_lines.append(f"{line}\t→\t未找到")
                    fail += 1
            except ValueError:
                output_lines.append(f"{line}\t→\t格式错误")
                fail += 1
            continue

        # 公元 N
        if parts[0] == "公元" and len(parts) >= 2:
            try:
                year = int(parts[1])
                results = ad_to_reign(year)
                if results and "error" not in results[0]:
                    items = []
                    for r in results:
                        reign_text = f"{r['reign']} {r['nth_year']}年" if r['reign'] != "無" else f"在位第{r['nth_year']}年"
                        items.append(f"{r['dynasty']} {r['emperor']} {reign_text}")
                    output_lines.append(f"{line}\t→\t{' / '.join(items)}")
                    success += 1
                else:
                    output_lines.append(f"{line}\t→\t未找到")
                    fail += 1
            except ValueError:
                output_lines.append(f"{line}\t→\t格式错误")
                fail += 1
            continue

        # 纯数字：正数=公元，负数=公元前
        if len(parts) == 1:
            try:
                year = int(parts[0])
                results = ad_to_reign(year)
                if results and "error" not in results[0]:
                    items = []
                    for r in results:
                        reign_text = f"{r['reign']} {r['nth_year']}年" if r['reign'] != "無" else f"在位第{r['nth_year']}年"
                        items.append(f"{r['dynasty']} {r['emperor']} {reign_text}")
                    output_lines.append(f"{format_ad(year)}\t→\t{' / '.join(items)}")
                    success += 1
                else:
                    output_lines.append(f"{format_ad(year)}\t→\t未找到")
                    fail += 1
                continue
            except ValueError:
                pass  # 不是数字，当作年号处理

        # 年号 [N]
        reign_name = parts[0]
        nth_year = 1
        if len(parts) >= 2:
            try:
                nth_year = int(parts[1])
            except ValueError:
                reign_name = parts[1]
                if len(parts) >= 3:
                    try:
                        nth_year = int(parts[2])
                    except ValueError:
                        pass

        results = reign_to_ad(reign_name, nth_year)
        if results:
            items = []
            for r in results:
                if "error" in r and "ad_year" not in r:
                    items.append(r["error"])
                elif "error" in r:
                    items.append(r["error"])
                else:
                    items.append(f"{r['dynasty']} {r['emperor']} {r['reign']} {r['nth_year']}年 = {r['ad_text']}")
            output_lines.append(f"{line}\t→\t{' / '.join(items)}")
            success += 1 if not any("error" in r for r in results) else 0
            fail += 1 if any("error" in r for r in results) else 0
        else:
            output_lines.append(f"{line}\t→\t未找到")
            fail += 1

    # 统计
    output_lines.append(f"\n# 统计: 成功 {success} 条，失败 {fail} 条，共 {len(lines)} 条")

    result_text = "\n".join(output_lines)

    # 输出
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result_text + "\n")
        print(f"  ✅ 批量转换完成: {success} 成功 / {fail} 失败 / 共 {len(lines)} 条")
        print(f"  📄 结果已保存到: {output_path}")
    else:
        print(result_text)


# ── 交互模式 ────────────────────────────────────────────────

def _clean_input(text):
    """
    清理用户输入中的控制字符。
    处理退格键(\x08, \x7f)的删除语义，去除其他不可见控制字符。
    """
    import re

    # 第一步：清理 ANSI 转义序列（如方向键 \x1b[A 等）
    text = re.sub(r'\x1b\[[0-9;]*[A-Za-z]', '', text)
    # 清理不完整的 ESC 序列
    text = re.sub(r'\x1b\[?[0-9;]*', '', text)

    # 第二步：模拟退格键的删除行为
    result = []
    for ch in text:
        if ch in ('\x08', '\x7f'):  # BS / DEL
            if result:
                result.pop()
        elif ord(ch) < 32 and ch not in ('\n', '\r', '\t'):
            # 跳过其他控制字符
            continue
        else:
            result.append(ch)

    return ''.join(result).strip()

def interactive_mode():
    """交互式转换"""
    # 启用 readline 行编辑（支持退格、方向键、历史记录）
    try:
        import readline  # noqa: F401
    except ImportError:
        pass

    print()
    print("═══════════════════════════════════════════")
    print("   帝王纪年 ↔ 公元纪年 转换工具")
    print("   数据范围: 西周厉王 ~ 清宣统")
    print("═══════════════════════════════════════════")
    print()
    print("  命令说明:")
    print("    <年号> [N]              年号→公元       贞观 2")
    print("    公元/ad <N>             公元→年号       ad 645")
    print("    公元前/bce <N>          公元前→年号     bce 221")
    print("    搜索/search <词>        搜索            search 乾隆")
    print("    朝代/list <词>          列出朝代年号    list 唐")
    print("    批量/batch <文件> [输出] 批量转换        batch input.txt")
    print("    q/quit/退出             退出程序")
    print()

    while True:
        try:
            raw = input("  > ")
            line = _clean_input(raw)
        except (EOFError, KeyboardInterrupt):
            print("\n  再见！")
            break

        if not line:
            continue
        if line in ("q", "quit", "exit", "退出"):
            print("  再见！")
            break

        parts = line.split()

        # 公元前 / bce → 帝王纪年
        if parts[0] in ("公元前", "bce") and len(parts) >= 2:
            try:
                year = -abs(int(parts[1]))
                results = ad_to_reign(year)
                print_ad_results(results, year)
            except ValueError:
                print("  请输入有效的数字")
            print()
            continue

        # 公元 / ad → 帝王纪年
        if parts[0] in ("公元", "ad") and len(parts) >= 2:
            try:
                year = int(parts[1])
                results = ad_to_reign(year)
                print_ad_results(results, year)
            except ValueError:
                print("  请输入有效的数字")
            print()
            continue

        # 搜索
        if parts[0] in ("搜索", "search", "找"):
            if len(parts) >= 2:
                results = search_reign(parts[1])
                print_search_results(results, parts[1])
            else:
                print("  请输入搜索关键词")
            print()
            continue

        # 列出朝代
        if parts[0] in ("朝代", "list", "dynasty", "列出"):
            if len(parts) >= 2:
                results = list_dynasty(parts[1])
                print_search_results(results, parts[1])
            else:
                print("  请输入朝代关键词")
            print()
            continue

        # 批量转换
        if parts[0] in ("批量", "batch"):
            if len(parts) >= 2:
                input_path = parts[1]
                output_path = parts[2] if len(parts) >= 3 else None
                batch_convert(input_path, output_path)
            else:
                print("  用法: batch <输入文件> [输出文件]")
            print()
            continue

        # 帝王纪年 → 公元
        reign_name = parts[0]
        nth_year = 1
        if len(parts) >= 2:
            try:
                nth_year = int(parts[1])
            except ValueError:
                # 可能是 "唐太宗 贞观" 这样的输入
                reign_name = parts[1]
                if len(parts) >= 3:
                    try:
                        nth_year = int(parts[2])
                    except ValueError:
                        pass

        results = reign_to_ad(reign_name, nth_year)
        print_reign_results(results, reign_name)
        print()


# ── CLI 入口 ────────────────────────────────────────────────

def print_usage():
    print("""
帝王纪年 ↔ 公元纪年 转换工具

用法:
    python emperor_year_converter.py                    交互模式
    python emperor_year_converter.py 贞观 2             贞观二年 → 公元
    python emperor_year_converter.py 康熙               康熙元年 → 公元
    python emperor_year_converter.py --ad 645           公元645年 → 帝王纪年
    python emperor_year_converter.py --ad -221          公元前221年 → 帝王纪年
    python emperor_year_converter.py --search 乾隆      搜索年号
    python emperor_year_converter.py --list 唐           列出唐朝所有年号
    python emperor_year_converter.py --batch input.txt              批量转换（输出到终端）
    python emperor_year_converter.py --batch input.txt output.txt   批量转换（保存到文件）

批量文件格式（每行一条，# 开头为注释）:
    贞观 2
    康熙 61
    公元 645
    公元前 221
    1644
    -221
""")


def main():
    args = sys.argv[1:]

    if not args:
        interactive_mode()
        return 0

    if args[0] in ("-h", "--help", "help"):
        print_usage()
        return 0

    # 批量转换
    if args[0] == "--batch" and len(args) >= 2:
        input_path = args[1]
        output_path = args[2] if len(args) >= 3 else None
        batch_convert(input_path, output_path)
        return 0

    # 公元 → 帝王纪年
    if args[0] == "--ad" and len(args) >= 2:
        try:
            year = int(args[1])
            results = ad_to_reign(year)
            print_ad_results(results, year)
        except ValueError:
            print("  请输入有效的数字")
        return 0

    # 搜索
    if args[0] == "--search" and len(args) >= 2:
        results = search_reign(args[1])
        print_search_results(results, args[1])
        return 0

    # 列出朝代
    if args[0] == "--list" and len(args) >= 2:
        results = list_dynasty(args[1])
        print_search_results(results, args[1])
        return 0

    # 帝王纪年 → 公元
    reign_name = args[0]
    nth_year = 1
    if len(args) >= 2:
        try:
            nth_year = int(args[1])
        except ValueError:
            pass

    results = reign_to_ad(reign_name, nth_year)
    print_reign_results(results, reign_name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
