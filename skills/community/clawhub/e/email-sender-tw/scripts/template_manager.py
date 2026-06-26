#!/usr/bin/env python3
"""
郵件模板管理腳本
支持模板變量替換和自定義模板
"""

import os
import re
import json
from typing import Dict, Optional, List
from send_email import send_email

# 目錄路徑
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(SCRIPT_DIR, "..", "assets", "templates")


def list_templates() -> List[str]:
    """
    列出所有可用的模板

    返回:
        list: 模板名稱列表
    """
    if not os.path.exists(TEMPLATES_DIR):
        os.makedirs(TEMPLATES_DIR)
        return []

    # 獲取所有 .html 和 .txt 模板
    templates = []

    for filename in os.listdir(TEMPLATES_DIR):
        if filename.endswith(('.html', '.txt')):
            # 去掉副檔名
            template_name = os.path.splitext(filename)[0]
            templates.append(template_name)

    return sorted(templates)


def load_template(template_name: str) -> Optional[Dict[str, str]]:
    """
    載入模板

    參數:
        template_name: 模板名稱

    返回:
        dict: {subject: "...", body: "...", html: True/False} 或 None
    """
    # 嘗試 HTML 模板
    html_path = os.path.join(TEMPLATES_DIR, f"{template_name}.html")
    txt_path = os.path.join(TEMPLATES_DIR, f"{template_name}.txt")

    if os.path.exists(html_path):
        is_html = True
        template_path = html_path
    elif os.path.exists(txt_path):
        is_html = False
        template_path = txt_path
    else:
        return None

    # 讀取模板內容
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 解析主題和正文
    # 格式: <!-- SUBJECT: 主題 --> 或 # SUBJECT: 主題
    subject_match = re.search(r'(<!-- SUBJECT:\s*(.+?)\s*-->|# SUBJECT:\s*(.+))', content, re.DOTALL)

    if subject_match:
        subject = subject_match.group(2) or subject_match.group(3)
        # 移除主題標記
        content = re.sub(r'(<!-- SUBJECT:\s*.+?\s*-->|# SUBJECT:\s*.+)', '', content, count=1).strip()
    else:
        subject = f"[{template_name}]"

    return {
        "subject": subject,
        "body": content.strip(),
        "html": is_html
    }


def replace_variables(template: str, variables: Dict[str, str]) -> str:
    """
    替換模板變量

    支持的變量格式:
    - {{name}}
    - {{ name }}
    - {name}

    參數:
        template: 模板內容
        variables: 變量字典

    返回:
        str: 替換後的內容
    """
    result = template

    # 替換 {{variable}} 和 {{ variable }}
    for key, value in variables.items():
        result = re.sub(r'\{\{\s*' + key + r'\s*\}\}', str(value), result)
        result = re.sub(r'\{' + key + r'\}', str(value), result)

    return result


def create_template(
    template_name: str,
    subject: str,
    body: str,
    is_html: bool = True,
    overwrite: bool = False
) -> bool:
    """
    創建新模板

    參數:
        template_name: 模板名稱
        subject: 郵件主題
        body: 郵件內容
        is_html: 是否為 HTML 模板（默認 True）
        overwrite: 是否覆蓋已存在的模板（默認 False）

    返回:
        bool: 成功返回 True，失敗返回 False
    """
    # 確保目錄存在
    if not os.path.exists(TEMPLATES_DIR):
        os.makedirs(TEMPLATES_DIR)

    # 確定模板文件路徑
    ext = ".html" if is_html else ".txt"
    template_path = os.path.join(TEMPLATES_DIR, f"{template_name}{ext}")

    # 檢查是否已存在
    if os.path.exists(template_path) and not overwrite:
        print(f"⚠️  模板 '{template_name}' 已存在。使用 --overwrite 選項來覆蓋。")
        return False

    # 組合模板內容
    if is_html:
        full_content = f"<!-- SUBJECT: {subject} -->\n\n{body}"
    else:
        full_content = f"# SUBJECT: {subject}\n\n{body}"

    # 保存模板
    try:
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(full_content)

        print(f"✅ 模板 '{template_name}' 已創建。")
        return True

    except Exception as e:
        print(f"❌ 創建模板失敗: {e}")
        return False


def delete_template(template_name: str) -> bool:
    """
    刪除模板

    參數:
        template_name: 模板名稱

    返回:
        bool: 成功返回 True，失敗返回 False
    """
    # 嘗試 HTML 模板
    html_path = os.path.join(TEMPLATES_DIR, f"{template_name}.html")
    txt_path = os.path.join(TEMPLATES_DIR, f"{template_name}.txt")

    template_path = None
    if os.path.exists(html_path):
        template_path = html_path
    elif os.path.exists(txt_path):
        template_path = txt_path
    else:
        print(f"⚠️  模板 '{template_name}' 不存在。")
        return False

    # 刪除文件
    try:
        os.remove(template_path)
        print(f"✅ 模板 '{template_name}' 已刪除。")
        return True

    except Exception as e:
        print(f"❌ 刪除模板失敗: {e}")
        return False


def send_templated_email(
    template_name: str,
    to: str,
    variables: Optional[Dict[str, str]] = None,
    account_name: Optional[str] = None,
    cc: Optional[str] = None,
    bcc: Optional[str] = None,
    reply_to: Optional[str] = None,
    attachments: Optional[List[str]] = None
) -> bool:
    """
    使用模板發送郵件

    參數:
        template_name: 模板名稱
        to: 收件人郵件地址
        variables: 變量字典（可選）
        account_name: SMTP 配置名稱（可選）
        cc: 抄送郵件地址（可選）
        bcc: 密送郵件地址（可選）
        reply_to: 回覆郵件地址（可選）
        attachments: 附件檔案路徑列表（可選）

    返回:
        bool: 發送成功返回 True，失敗返回 False
    """
    # 載入模板
    template = load_template(template_name)

    if template is None:
        print(f"❌ 找不到模板 '{template_name}'。")
        print(f"   可用模板: {', '.join(list_templates())}")
        return False

    # 替換變量
    if variables:
        subject = replace_variables(template["subject"], variables)
        body = replace_variables(template["body"], variables)
    else:
        subject = template["subject"]
        body = template["body"]

    print(f"📧 發送郵件（模板: {template_name}）")
    print(f"   主題: {subject}")

    # 發送郵件
    return send_email(
        to=to,
        subject=subject,
        body=body,
        account_name=account_name,
        html=template["html"],
        cc=cc,
        bcc=bcc,
        reply_to=reply_to,
        attachments=attachments
    )


def preview_template(template_name: str, variables: Optional[Dict[str, str]] = None):
    """
    預覽模板

    參數:
        template_name: 模板名稱
        variables: 變量字典（可選）
    """
    # 載入模板
    template = load_template(template_name)

    if template is None:
        print(f"❌ 找不到模板 '{template_name}'。")
        return

    # 替換變量
    if variables:
        subject = replace_variables(template["subject"], variables)
        body = replace_variables(template["body"], variables)
    else:
        subject = template["subject"]
        body = template["body"]

    print("=" * 50)
    print(f"模板預覽: {template_name}")
    print("=" * 50)
    print(f"主題: {subject}")
    print(f"格式: {'HTML' if template['html'] else '純文字'}")
    print("=" * 50)
    print(body)
    print("=" * 50)


# 預設模板

DEFAULT_TEMPLATES = {
    "reminder": {
        "subject": "提醒通知",
        "is_html": True,
        "body": """<h1>嗨 {{name}}，</h1>

<p>這是一個提醒通知：</p>

<p style="background-color: #f0f0f0; padding: 10px; border-left: 4px solid #4CAF50;">
  {{message}}
</p>

<p>時間：{{date}}</p>

<p>祝好，<br>
{{sender}}</p>
"""
    },
    "report": {
        "subject": "報告通知",
        "is_html": True,
        "body": """<h1>{{report_name}} 報告</h1>

<p>親愛的 {{name}}，</p>

<p>這是你的 {{report_name}} 報告。</p>

<table border="1" cellpadding="10" style="border-collapse: collapse; width: 100%;">
  <tr style="background-color: #f0f0f0;">
    <td><b>項目</b></td>
    <td><b>內容</b></td>
  </tr>
  <tr>
    <td>報告日期</td>
    <td>{{date}}</td>
  </tr>
  <tr>
    <td>摘要</td>
    <td>{{summary}}</td>
  </tr>
</table>

<p>詳細報告請查看附件。</p>

<p>感謝，<br>
{{sender}}</p>
"""
    },
    "welcome": {
        "subject": "歡迎加入",
        "is_html": True,
        "body": """<h1>歡迎加入 {{company_name}}！</h1>

<p>親愛的 {{name}}，</p>

<p>歡迎加入 {{company_name}} 團隊！我們很興奋你成為我們的一員。</p>

<p>以下是你的帳號信息：</p>

<ul>
  <li>用戶名：{{username}}</li>
  <li>初始密碼：{{password}}</li>
</ul>

<p>請盡快登入並修改密碼。</p>

<p>如有任何問題，請隨時聯繫我們。</p>

<p>祝好，<br>
{{company_name}} 團隊</p>
"""
    }
}


def create_default_templates():
    """創建預設模板"""
    print("創建預設模板...")

    for template_name, template_data in DEFAULT_TEMPLATES.items():
        create_template(
            template_name=template_name,
            subject=template_data["subject"],
            body=template_data["body"],
            is_html=template_data["is_html"],
            overwrite=True
        )


def main():
    """命令行界面"""
    import sys

    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 template_manager.py list                - 列出所有模板")
        print("  python3 template_manager.py create              - 創建新模板")
        print("  python3 template_manager.py preview <name>      - 預覽模板")
        print("  python3 template_manager.py delete <name>       - 刪除模板")
        print("  python3 template_manager.py send <name> <to>    - 使用模板發送郵件")
        print("  python3 template_manager.py init-defaults       - 創建預設模板")
        return

    command = sys.argv[1]

    if command == "list":
        templates = list_templates()

        if templates:
            print("\n=== 可用模板 ===\n")
            for i, template in enumerate(templates, 1):
                print(f"{i}. {template}")
            print()
        else:
            print("沒有可用的模板。使用 'init-defaults' 創建預設模板。")

    elif command == "create":
        # 互動式創建模板
        name = input("模板名稱: ").strip()
        subject = input("郵件主題: ").strip()
        is_html = input("是否為 HTML 模板？(y/n，默認 y): ").strip().lower() != 'n'

        print("\n模板內容（輸入結束後按 Ctrl+D）:")
        body_lines = []
        try:
            while True:
                line = input()
                body_lines.append(line)
        except EOFError:
            pass

        body = "\n".join(body_lines)

        create_template(name, subject, body, is_html, overwrite=True)

    elif command == "preview":
        if len(sys.argv) < 3:
            print("❌ 請指定模板名稱。")
            return

        template_name = sys.argv[2]

        # 預覽的變量
        variables = {}
        if "--vars" in sys.argv:
            idx = sys.argv.index("--vars")
            for arg in sys.argv[idx+1:]:
                if '=' in arg:
                    key, value = arg.split('=', 1)
                    variables[key] = value

        preview_template(template_name, variables)

    elif command == "delete":
        if len(sys.argv) < 3:
            print("❌ 請指定模板名稱。")
            return

        delete_template(sys.argv[2])

    elif command == "send":
        if len(sys.argv) < 4:
            print("❌ 用法: python3 template_manager.py send <template_name> <to> [vars...]")
            return

        template_name = sys.argv[2]
        to = sys.argv[3]

        # 解析變量
        variables = {}
        for arg in sys.argv[4:]:
            if '=' in arg:
                key, value = arg.split('=', 1)
                variables[key] = value

        send_templated_email(template_name, to, variables)

    elif command == "init-defaults":
        create_default_templates()

    else:
        print(f"❌ 未知命令: {command}")


if __name__ == "__main__":
    main()
