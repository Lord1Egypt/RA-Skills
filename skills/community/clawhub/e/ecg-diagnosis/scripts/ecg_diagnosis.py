import sys
import io
import time
import random
import argparse
import re
from datetime import datetime
import pandas as pd
from pathlib import Path
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

# 强制输出 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)

def parse_ecg_metadata(filename):
    """
    解析格式：yyyy-mm-dd_年龄_性别_名字.ext
    返回：(age, gender)
    """
    try:
        parts = filename.split('_')
        if len(parts) >= 3:
            age = parts[1] # 年龄
            gender = parts[2] # 性别
            # 简单验证年龄是否为数字
            if age.isdigit() and gender in ["男", "女"]:
                return age, gender
    except:
        pass
    return "65", "男" # 解析失败时的兜底值

def clean_diagnosis_result(raw_text):
    """
    2026 精准提取逻辑：从网页全量文本中截取“心电诊断”核心部分
    """
    # 1. 寻找起始标记（兼容中英文冒号）
    start_marker = "心电诊断："
    if start_marker not in raw_text:
        start_marker = "心电诊断:"
    
    if start_marker in raw_text:
        # 截取起始标记之后的内容
        content = raw_text.split(start_marker)[-1]
        
        # 2. 寻找结束标记（一旦遇到这些词，立即截断）
        # 根据截图，后面通常紧跟“关键异常”或“风险评估”
        stop_markers = ["关键异常", "风险评估", "建议", "管理方案", "---"]
        for marker in stop_markers:
            if marker in content:
                content = content.split(marker)[0]
                break
        
        return content.strip()
    
    # 兜底：如果没找到标记，则截取前3行，防止内容过多撑破 Excel
    return "\n".join(raw_text.strip().split('\n')[:3])

def ecg_diagnosis_workflow(folder_path: str, images: list):
    folder = Path(folder_path)
    user_data_dir = folder / ".web_profile"
    excel_path = folder / f"{datetime.now().strftime('%Y-%m-%d')}-诊断结果.xlsx"
    results = []

    with sync_playwright() as p:
        print(" 初始化隐身环境...")
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(user_data_dir),
            headless=False, # 建议设为 False 以便观察渲染过程
            slow_mo=800,
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = context.pages[0]
        Stealth().apply_stealth_sync(page)

        for idx, img_name in enumerate(images):
            img_path = folder / img_name
            if not img_path.exists():
                print(f"  文件不存在: {img_name}")
                continue
            # 解析文件名中的元数据
            target_age, target_gender = parse_ecg_metadata(img_name)
            
            try:
                print(f"\n 处理中 [{idx+1}/{len(images)}]: {img_name}")
                page.goto("https://www.xin-gou.com/chat/", wait_until="domcontentloaded", timeout=60000)
                time.sleep(5)

                # --- 1. 点击图片导入 ---
                page.get_by_text("图片导入").first.click()
                print("   点击[图片导入]，等待20s渲染...")
                time.sleep(20)

                # --- 2. 上传文件 ---
                page.locator("input[type='file']").set_input_files(str(img_path))
                print("   文件已上传，等待20s解析...")
                time.sleep(20)

                # --- 3. 填写年龄 ---
                age_input = page.get_by_placeholder("请输入年龄")
                age_input.wait_for(state="visible")
                age_input.fill(target_age)
                print(f"  填写年龄: {target_age}")

                # --- 4. 勾选性别 ---
                # 在 Gradio 中，性别通常是 Label 形式
                page.get_by_label(target_gender).check()
                print(f"   勾选性别: {target_gender}")
                time.sleep(5)

                # --- 5. 提取波形 ---
                page.get_by_text("提取心电图波形").click()
                print("   提取波形中，等待25s算法响应...")
                time.sleep(25)

                # --- 6. 开始诊断 ---
                diag_btn = page.locator("button", has_text="开始诊断分析")
                diag_btn.wait_for(state="visible")
                diag_btn.click()
                print("   触发诊断，进入 20s 深度分析等待...")
                time.sleep(20)

                # --- 7. 提取结果 (根据截图6) ---
                final_diagnosis = "未捕获到文本"
                try:
                    # 获取右侧对话框最后一个回复块
                    chat_container = page.locator(".chatbot.prose").last
                    raw_text = chat_container.inner_text()
                    # 调用清洗函数，只保留“心电诊断”精华
                    final_diagnosis = clean_diagnosis_result(raw_text)
                except:
                    final_diagnosis = "解析对话失败，请检查网页"

                print(f"   提取成功")
                results.append({
                    "时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "图片名": img_name,
                    "年龄": target_age,
                    "性别": target_gender,
                    "诊断结论": final_diagnosis
                })

            except Exception as e:
                print(f"   错误: {e}")

        context.close()

    # 保存 Excel
    if results:
        df = pd.DataFrame(results)
        # 如果文件已存在，则追加数据，否则新建
        if excel_path.exists():
            try:
                old_df = pd.read_excel(excel_path)
                df = pd.concat([old_df, df], ignore_index=True)
            except:
                pass
        df.to_excel(excel_path, index=False)
        print(f"\n 任务完成！表单已存至: {excel_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=str, required=True)
    parser.add_argument("--images", type=str, required=True)
    args = parser.parse_args()
    img_list = [i.strip() for i in args.images.split(",")]
    ecg_diagnosis_workflow(args.folder, img_list)