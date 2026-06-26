"""
北汽社群数据导出 - 一键执行脚本
每天 00:55 定时执行

用法：
  python run.py          # 全流程执行
  python run.py clean    # 仅数据清洗
  python run.py audit    # 仅数据校对
  python run.py merge    # 仅数据合并
  python run.py verify   # 仅最终验证
"""

import pandas as pd
import os
import sys
import glob
from datetime import datetime, date

DOWNLOADS_DIR = os.path.expanduser("~\\Downloads")
TARGET_LABELS = ['温冷一期', '试点店']
NUMERIC_SRC_INDICES = {4: '群人数', 7: '员工人数', 8: '客户人数', 9: '今日入群', 10: '今日退群', 11: '今日消息'}
NUMERIC_TGT_INDICES = {8: '群人数', 11: '员工人数', 12: '客户人数', 13: '今日入群', 14: '今日退群', 15: '今日消息'}


def find_latest_source():
    """找到 Downloads 中最新下载的客户群导出文件（按创建时间/下载时间排序）"""
    candidates = []
    for f in os.listdir(DOWNLOADS_DIR):
        if "客户群导出" in f and f.endswith(".xlsx") and "清理后" not in f and "已更新" not in f:
            file_path = os.path.join(DOWNLOADS_DIR, f)
            ctime = os.path.getctime(file_path)  # 创建时间 = 下载时间
            candidates.append((file_path, ctime))
    
    if not candidates:
        print("[错误] 未在 Downloads 中找到客户群导出文件")
        sys.exit(1)
    
    candidates.sort(key=lambda x: x[1], reverse=True)
    return candidates[0][0]


def find_bi_file():
    """找到 BI_社群数据上传.xlsx"""
    bi_file = os.path.join(DOWNLOADS_DIR, "BI_社群数据上传.xlsx")
    if not os.path.exists(bi_file):
        # 尝试模糊匹配
        for f in os.listdir(DOWNLOADS_DIR):
            if "BI" in f and "社群数据上传" in f and f.endswith(".xlsx") and "已更新" not in f:
                return os.path.join(DOWNLOADS_DIR, f)
        print("[错误] 未找到 BI_社群数据上传.xlsx")
        sys.exit(1)
    return bi_file


def get_file_date(file_path):
    """获取文件的创建时间（下载日期），精确到日"""
    ctime = datetime.fromtimestamp(os.path.getctime(file_path))  # 创建时间 = 下载时间
    return ctime.strftime('%Y-%m-%d'), ctime.strftime('%Y%m%d')


def step_clean():
    """第 1 步：数据清洗"""
    print("=" * 60)
    print("第 1 步：数据清洗")
    print("=" * 60)
    
    source_file = find_latest_source()
    file_date, file_date_short = get_file_date(source_file)
    
    print(f"\n源文件：{os.path.basename(source_file)}")
    print(f"文件日期：{file_date}")
    
    df = pd.read_excel(source_file)
    print(f"原始数据：{len(df):,} 行，{len(df.columns)} 列")
    
    # O 列（群标签）
    o_col = df.columns[14]
    print(f"群标签列：{o_col}")
    
    # 筛选
    filtered_df = df[df[o_col].isin(TARGET_LABELS)].copy()
    
    print(f"\n筛选结果：")
    print(f"  原始行数：{len(df):,}")
    print(f"  保留行数：{len(filtered_df):,}")
    print(f"  删除行数：{len(df) - len(filtered_df):,}")
    
    # 验证关键指标
    print(f"\n关键指标验证：")
    src_sums = {}
    for idx, col_name in NUMERIC_SRC_INDICES.items():
        expected = pd.to_numeric(df[df[o_col].isin(TARGET_LABELS)].iloc[:, idx], errors='coerce').fillna(0).sum()
        actual = pd.to_numeric(filtered_df.iloc[:, idx], errors='coerce').fillna(0).sum()
        status = "[OK]" if expected == actual else "[ERR]"
        src_sums[col_name] = actual
        print(f"  {col_name}: {actual:,.0f} {status}")
    
    # 保存
    output_file = os.path.join(DOWNLOADS_DIR, f"客户群导出_清理后_温冷一期 + 试点店_{file_date_short}.xlsx")
    filtered_df.to_excel(output_file, index=False)
    print(f"\n已保存：{os.path.basename(output_file)}")
    
    return source_file, output_file, src_sums, file_date, file_date_short


def step_audit(source_file, cleaned_file, src_sums):
    """第 2 步：数据校对"""
    print("\n" + "=" * 60)
    print("第 2 步：数据校对")
    print("=" * 60)
    
    df = pd.read_excel(source_file)
    cleaned_df = pd.read_excel(cleaned_file)
    o_col = df.columns[14]
    target_df = df[df[o_col].isin(TARGET_LABELS)]
    
    print(f"\n源文件行数：{len(target_df):,}")
    print(f"清理后行数：{len(cleaned_df):,}")
    
    # 指标对比
    print(f"\n{'指标':<12} {'源文件':>10} {'清理后':>10} {'差异':>8} {'状态':>6}")
    print("-" * 50)
    
    all_ok = True
    cleaned_sums = {}
    for idx, col_name in NUMERIC_SRC_INDICES.items():
        src_val = pd.to_numeric(target_df.iloc[:, idx], errors='coerce').fillna(0).sum()
        cleaned_val = pd.to_numeric(cleaned_df.iloc[:, idx], errors='coerce').fillna(0).sum()
        diff = cleaned_val - src_val
        status = "[OK]" if diff == 0 else "[ERR]"
        if diff != 0:
            all_ok = False
        cleaned_sums[col_name] = cleaned_val
        print(f"  {col_name:<10} {src_val:>10,.0f} {cleaned_val:>10,.0f} {diff:>+8.0f} {status:>6}")
    
    # 分标签统计
    print(f"\n分标签统计：")
    for label in TARGET_LABELS:
        subset = cleaned_df[cleaned_df.iloc[:, 14] == label]
        print(f"\n  {label} ({len(subset):,} 行)")
        for idx, col_name in NUMERIC_SRC_INDICES.items():
            val = pd.to_numeric(subset.iloc[:, idx], errors='coerce').fillna(0).sum()
            print(f"    {col_name}: {val:,.0f}")
    
    # 数据质量
    print(f"\n数据质量检查：")
    for idx, col_name in NUMERIC_SRC_INDICES.items():
        nulls = cleaned_df.iloc[:, idx].isna().sum()
        negs = (pd.to_numeric(cleaned_df.iloc[:, idx], errors='coerce').fillna(0) < 0).sum()
        issues = []
        if nulls > 0: issues.append(f"{nulls}个空值")
        if negs > 0: issues.append(f"{negs}个负值")
        status = ", ".join(issues) if issues else "[OK]"
        print(f"  {col_name}: {status}")
    
    result = "[PASS] 校对通过" if all_ok else "[FAIL] 存在差异"
    print(f"\n校对结论：{result}")
    
    return all_ok, cleaned_sums


def step_merge(cleaned_file, src_sums, file_date, file_date_short):
    """第 3 步：数据合并"""
    print("\n" + "=" * 60)
    print("第 3 步：数据合并")
    print("=" * 60)
    
    src_df = pd.read_excel(cleaned_file)
    bi_file = find_bi_file()
    tgt_df = pd.read_excel(bi_file)
    
    print(f"\n清理后文件：{len(src_df):,} 行")
    print(f"BI 原始文件：{len(tgt_df):,} 行")
    print(f"统计日期（源文件下载日期）：{file_date}")
    
    # 创建新行
    new_rows = []
    for idx, row in src_df.iterrows():
        new_row = {
            tgt_df.columns[0]: '',
            tgt_df.columns[1]: '',
            tgt_df.columns[2]: '',
            tgt_df.columns[3]: file_date,
            tgt_df.columns[4]: row.iloc[0],
            tgt_df.columns[5]: row.iloc[1],
            tgt_df.columns[6]: row.iloc[2],
            tgt_df.columns[7]: row.iloc[3],
            tgt_df.columns[8]: row.iloc[4],
            tgt_df.columns[9]: row.iloc[5],
            tgt_df.columns[10]: row.iloc[6],
            tgt_df.columns[11]: row.iloc[7],
            tgt_df.columns[12]: row.iloc[8],
            tgt_df.columns[13]: row.iloc[9],
            tgt_df.columns[14]: row.iloc[10],
            tgt_df.columns[15]: row.iloc[11],
            tgt_df.columns[16]: row.iloc[12],
            tgt_df.columns[17]: row.iloc[13],
            tgt_df.columns[18]: row.iloc[14],
        }
        new_rows.append(new_row)
    
    new_rows_df = pd.DataFrame(new_rows)
    
    # 转换数字列
    print("\n转换数字列格式：")
    for tgt_idx, col_name in NUMERIC_TGT_INDICES.items():
        col = tgt_df.columns[tgt_idx]
        new_rows_df[col] = pd.to_numeric(new_rows_df[col], errors='coerce').fillna(0).astype(int)
        print(f"  {col_name} -> int")
    
    # 合并
    result_df = pd.concat([tgt_df, new_rows_df], ignore_index=True)
    
    # 保存
    output_file = os.path.join(DOWNLOADS_DIR, f"BI_社群数据上传_已更新_{file_date_short}.xlsx")
    result_df.to_excel(output_file, index=False)
    
    print(f"\n新增行数：{len(new_rows_df):,}")
    print(f"合并后总行数：{len(result_df):,}")
    print(f"已保存：{os.path.basename(output_file)}")
    
    return output_file, len(tgt_df)


def step_verify(source_file, cleaned_file, merged_file, original_rows, file_date):
    """第 4 步：最终验证"""
    print("\n" + "=" * 60)
    print("第 4 步：最终验证")
    print("=" * 60)
    
    src_df = pd.read_excel(source_file)
    cleaned_df = pd.read_excel(cleaned_file)
    merged_df = pd.read_excel(merged_file)
    
    o_col = src_df.columns[14]
    target_df = src_df[src_df[o_col].isin(TARGET_LABELS)]
    new_data = merged_df.tail(len(cleaned_df))
    
    print(f"\n{'指标':<12} {'源文件':>10} {'清理后':>10} {'合并后':>10} {'状态':>6}")
    print("-" * 60)
    
    all_ok = True
    for src_idx, col_name in NUMERIC_SRC_INDICES.items():
        tgt_idx = src_idx + 4
        src_val = pd.to_numeric(target_df.iloc[:, src_idx], errors='coerce').fillna(0).sum()
        cleaned_val = pd.to_numeric(cleaned_df.iloc[:, src_idx], errors='coerce').fillna(0).sum()
        merged_val = pd.to_numeric(new_data.iloc[:, tgt_idx], errors='coerce').fillna(0).sum()
        status = "[OK]" if src_val == cleaned_val == merged_val else "[ERR]"
        if status == "[ERR]":
            all_ok = False
        print(f"  {col_name:<10} {src_val:>10,.0f} {cleaned_val:>10,.0f} {merged_val:>10,.0f} {status:>6}")
    
    # 行数验证
    expected_rows = original_rows + len(cleaned_df)
    actual_rows = len(merged_df)
    rows_ok = expected_rows == actual_rows
    print(f"\n行数验证：{original_rows:,} + {len(cleaned_df):,} = {expected_rows:,}（实际 {actual_rows:,}）{'[OK]' if rows_ok else '[ERR]'}")
    
    # 日期验证
    d_col = merged_df.columns[3]
    dates = new_data[d_col].unique()
    print(f"统计日期：{list(dates)} {'[OK]' if file_date in str(dates) else '[ERR]'}")
    
    # 记录结果供通知使用
    result_file = os.path.join(DOWNLOADS_DIR, ".baic_community_result.txt")
    tuiqun_val = pd.to_numeric(new_data.iloc[:, 14], errors='coerce').fillna(0).sum()
    
    if all_ok and rows_ok:
        status = "[PASS] 全部验证通过"
        print(f"\n{'=' * 60}")
        print(f"[PASS] 全部验证通过!")
        print(f"{'=' * 60}")
    else:
        status = "[FAIL] 存在差异，请检查"
        print(f"\n{'=' * 60}")
        print(f"[FAIL] 存在差异，请检查!")
        print(f"{'=' * 60}")
    
    # 写入结果文件
    with open(result_file, 'w', encoding='utf-8') as f:
        f.write(f"北汽社群数据导出 - 执行完成\n")
        f.write(f"执行时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"统计日期：{file_date}\n")
        f.write(f"今日退群：{tuiqun_val:.0f}\n")
        f.write(f"新增行数：{len(new_data):,}\n")
        f.write(f"合并后总行数：{actual_rows:,}\n")
        f.write(f"校对结果：{status}\n")
    
    return all_ok and rows_ok


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    
    print("=" * 60)
    print("社群数据处理流程")
    print(f"执行时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"执行模式：{mode}")
    print("=" * 60)
    
    if mode in ("all", "clean"):
        source_file, cleaned_file, src_sums, file_date, file_date_short = step_clean()
    
    if mode in ("all", "audit"):
        if mode == "audit":
            source_file = find_latest_source()
            file_date, file_date_short = get_file_date(source_file)
            cleaned_file = os.path.join(DOWNLOADS_DIR, f"客户群导出_清理后_温冷一期 + 试点店_{file_date_short}.xlsx")
            src_sums = {}
        audit_ok, cleaned_sums = step_audit(source_file, cleaned_file, src_sums)
    
    if mode in ("all", "merge"):
        if mode == "merge":
            source_file = find_latest_source()
            file_date, file_date_short = get_file_date(source_file)
            cleaned_file = os.path.join(DOWNLOADS_DIR, f"客户群导出_清理后_温冷一期 + 试点店_{file_date_short}.xlsx")
            src_sums = {}
        merged_file, original_rows = step_merge(cleaned_file, src_sums, file_date, file_date_short)
    
    if mode in ("all", "verify"):
        if mode == "verify":
            source_file = find_latest_source()
            file_date, file_date_short = get_file_date(source_file)
            cleaned_file = os.path.join(DOWNLOADS_DIR, f"客户群导出_清理后_温冷一期 + 试点店_{file_date_short}.xlsx")
            merged_file = os.path.join(DOWNLOADS_DIR, f"BI_社群数据上传_已更新_{file_date_short}.xlsx")
            bi_file = find_bi_file()
            original_rows = len(pd.read_excel(bi_file))
        step_verify(source_file, cleaned_file, merged_file, original_rows, file_date)
    
    print(f"\n流程完成！")
    
    # 通过 OpenClaw 发送飞书通知
    notify_feishu(mode, results if 'results' in dir() else {})


def notify_feishu(mode, results):
    """执行完成后通过 OpenClaw 发飞书通知"""
    try:
        import subprocess
        
        # 构建通知内容
        msg = "北汽社群数据导出 - 执行完成\n"
        msg += f"执行时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        if results:
            msg += f"\n今日退群：{results.get('today_quit', 'N/A')}"
            msg += f"\n新增行数：{results.get('new_rows', 'N/A')}"
            msg += f"\n合并后总行数：{results.get('total_rows', 'N/A')}"
            msg += f"\n校对结果：{results.get('status', 'N/A')}"
        
        # 写入临时文件供 OpenClaw 读取
        notify_file = os.path.join(DOWNLOADS_DIR, ".baic_community_result.txt")
        with open(notify_file, 'w', encoding='utf-8') as f:
            f.write(msg)
        
        print(f"\n通知内容已写入：{notify_file}")
    except Exception as e:
        print(f"通知发送失败：{e}")


if __name__ == "__main__":
    main()
