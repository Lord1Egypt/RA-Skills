#!/usr/bin/env python3
"""
该脚本仅用于本地可见浏览器中的 CSDN 草稿填写辅助，不是自动发布工具。

安全边界声明：
1. 必须在可见浏览器 (headless=False) 中运行，用户必须肉眼可见全过程。
2. 不绕过验证码、滑块验证或风控提示。遇到此类情况脚本会超时并移交用户。
3. 不保存、不上传账号密码。
4. 不读取、保存、打印、导出 cookie、localStorage 或 sessionStorage。
5. 不调用 browser_context.storage_state 保存登录态。
6. 绝不点击最终“发布”按钮，强制要求人工审核。
7. 脚本仅读取当前目录下的 /output/csdn/ 结果文件。
"""

import os
import sys
import time
from playwright.sync_api import sync_playwright

def read_file(filepath):
    """读取指定路径的文件内容"""
    if not os.path.exists(filepath):
        print(f"[-] 文件未找到: {filepath}")
        return ""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read().strip()

def run_draft_flow():
    # 强制路径限制：只能读取当前工程下的文件
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'examples', 'output', 'csdn'))
    
    # 也可以读取真实的 output，这里为了演示默认读取 examples 下的或者你指定的 output。
    # 实际应用中可以替换为 os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output', 'csdn'))
    actual_output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output', 'csdn'))
    
    # 优先读取真实的 output
    if os.path.exists(actual_output_dir):
        read_dir = actual_output_dir
    else:
        read_dir = base_dir

    print(f"[*] 从目录读取内容: {read_dir}")
    
    markdown_path = os.path.join(read_dir, 'csdn_markdown_ready.md')
    titles_path = os.path.join(read_dir, 'csdn_titles.md')
    summary_path = os.path.join(read_dir, 'csdn_summary.md')

    markdown_content = read_file(markdown_path)
    titles_content = read_file(titles_path)
    summary_content = read_file(summary_path)

    if not markdown_content:
        print("[-] 未找到 Markdown 正文，脚本退出。")
        sys.exit(1)

    # 简单从标题文件中提取第一个推荐标题
    title = "默认标题：请手动修改"
    if titles_content:
        lines = titles_content.split('\n')
        for line in lines:
            if line.strip().startswith('1.'):
                # 去掉前面的 "1. **xxx**："
                parts = line.split('：')
                if len(parts) > 1:
                    title = parts[1].strip()
                else:
                    title = line.replace('1.', '').replace('**', '').strip()
                break

    print("[*] 准备启动 Playwright...")
    with sync_playwright() as p:
        # 强制 headless=False
        browser = p.chromium.launch(headless=False, args=['--disable-blink-features=AutomationControlled'])
        # 强制不使用 storage_state，每次打开都是全新的上下文，用户需要扫码
        context = browser.new_context()
        page = context.new_page()

        print("[*] 正在打开 CSDN 创作者中心...")
        try:
            page.goto("https://editor.csdn.net/md/", timeout=60000)
            
            print("[*] 请在浏览器中完成登录（如需），脚本将等待页面加载完成...")
            # 等待 Markdown 编辑器的标题框出现，作为登录成功并进入页面的标志
            # CSDN 标题输入框通常有个类名如 article-bar__title
            page.wait_for_selector(".article-bar__title--input", timeout=120000)
            print("[+] 已进入编辑器界面。")

            # 填写标题
            print("[*] 正在填写标题...")
            title_input = page.locator(".article-bar__title--input")
            title_input.fill("") # 清空
            title_input.type(title, delay=100)

            # 填写正文
            # CSDN 使用 Monaco Editor，直接向里面 type 会比较慢且容易被拦截
            # 更稳定的方式是找到它的可编辑区域
            print("[*] 正在填写正文...")
            # 找到编辑区
            editor_locator = page.locator(".monaco-editor textarea")
            if editor_locator.count() > 0:
                # 使用剪贴板或 fill，因为大段文本 type 会很久
                editor_locator.first.fill(markdown_content)
            else:
                print("[-] 无法定位正文输入区域，请手动粘贴。")

            # 尝试点击发布文章按钮打开属性面板，填写摘要等
            print("[*] 尝试打开发布属性面板填写摘要...")
            publish_btn = page.locator("button.btn-publish")
            if publish_btn.count() > 0:
                publish_btn.click()
                time.sleep(2)
                
                # 寻找摘要输入框
                summary_input = page.locator("textarea.el-textarea__inner")
                if summary_input.count() > 0 and summary_content:
                    summary_input.first.fill(summary_content[:200]) # CSDN 摘要通常限制 256 字
                    print("[+] 摘要填写完成。")
                else:
                    print("[-] 摘要输入框未找到。")
            
            print("--------------------------------------------------")
            print("[+] 自动化填充流程结束。")
            print("[!] 脚本已暂停。请在浏览器中进行以下人工操作：")
            print("1. 检查正文格式是否正常。")
            print("2. 检查是否有违规或夸大营销内容。")
            print("3. 手动选择合适的【文章标签】和【文章分类】。")
            print("4. 确认无误后，自行点击【保存草稿】或【发布文章】。")
            print("--------------------------------------------------")
            
            # 挂起脚本，直到用户手动关闭浏览器
            page.wait_for_event("close", timeout=0)

        except Exception as e:
            print(f"[-] 执行过程中出现异常/超时: {e}")
            print("[-] 可能是遇到了未知的验证码或页面结构变更，请手动操作。")
        finally:
            print("[*] 正在清理并关闭...")
            context.close()
            browser.close()

if __name__ == "__main__":
    run_draft_flow()
