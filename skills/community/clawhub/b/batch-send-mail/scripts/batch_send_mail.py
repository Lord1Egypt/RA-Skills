#!/usr/bin/env python3
"""
Bulk Email Sender
===============
批量发送个性化邮件，支持变量替换、HTML格式和附件。

用法:
python bulk_email_sender.py \
  --table contacts.csv \
  --template template.txt \
  --subject "邮件主题" \
  [--dry-run]

首次使用会提示输入 SMTP 配置并保存到配置文件，后续使用自动读取配置。
也可以通过命令行参数覆盖配置文件中的设置。
"""

import argparse
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header
import urllib.parse
import configparser
import os
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent.parent
CONFIG_PATH = SCRIPT_DIR / 'config' / 'config.ini'


def load_config():
    """加载配置文件，如果不存在则交互式创建"""
    config = configparser.ConfigParser()

    if CONFIG_PATH.exists():
        config.read(CONFIG_PATH, encoding='utf-8')
        if 'smtp' in config:
            return config
        else:
            print(f"配置文件 {CONFIG_PATH} 格式不正确，将重新创建...")

    # 配置不存在或格式不正确，交互式创建
    print("=== 首次使用，请配置 SMTP 信息 ===")
    print()
    server = input("请输入 SMTP 服务器地址 (例如: smtp.qq.com): ").strip()
    while not server:
        server = input("SMTP 服务器地址不能为空，请重新输入: ").strip()

    port_input = input(f"请输入 SMTP 端口 (默认 587): ").strip()
    port = int(port_input) if port_input else 587

    sender_email = input("请输入发件人邮箱地址: ").strip()
    while not sender_email or '@' not in sender_email:
        sender_email = input("邮箱格式不正确，请重新输入: ").strip()

    sender_password = input("请输入密码/授权码: ").strip()
    while not sender_password:
        sender_password = input("密码/授权码不能为空，请重新输入: ").strip()

    # 保存配置
    config['smtp'] = {
        'server': server,
        'port': str(port),
        'sender_email': sender_email,
        'sender_password': sender_password
    }

    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        config.write(f)

    print()
    print(f"✓ 配置已保存到 {CONFIG_PATH}")
    print()

    return config


def read_table(table_path):
    """读取表格文件，支持CSV和Excel"""
    ext = Path(table_path).suffix.lower()

    if ext == '.csv':
        df = pd.read_csv(table_path, header=None)
    elif ext in ['.xlsx', '.xls']:
        df = pd.read_excel(table_path, header=None)
    else:
        raise ValueError(f"不支持的文件格式: {ext}，请使用 .csv 或 .xlsx")

    return df


def read_template(template_path):
    """读取邮件模板"""
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()


def count_template_variables(template):
    """统计模板中的变量数量
    查找 {variable1}, {variable2}, ... 和 {v1}, {v2}, ... 格式的变量
    返回找到的最大变量编号
    """
    import re

    # 匹配 {variableN} 和 {vN} 格式
    pattern = r'\{(?:variable|v)(\d+)\}'
    matches = re.findall(pattern, template)

    if not matches:
        return 0

    # 返回最大编号
    return max(int(n) for n in matches)


def substitute_variables(template, variables):
    """替换模板中的变量

    变量格式: {variable1}, {variable2}, ... 或 {v1}, {v2}, ...
    替换后自动移除空行（变量为空导致的空白行）
    """
    result = template

    for i, value in enumerate(variables, start=1):
        # 处理 {variable1} 和 {v1} 两种格式
        placeholder1 = f"{{variable{i}}}"
        placeholder2 = f"{{v{i}}}"
        value_str = str(value) if pd.notna(value) else ""
        result = result.replace(placeholder1, value_str)
        result = result.replace(placeholder2, value_str)

    # 移除空行（只包含空白字符的行），处理变量为空的情况
    lines = result.splitlines()
    non_empty_lines = [line for line in lines if line.strip() != ""]
    # 保留原换行格式
    return '\n'.join(non_empty_lines)


def create_message(email_addr, cc_list, variables, template, subject, sender_email, is_html=False, attachments=None):
    """创建邮件消息"""
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email_addr

    # 添加抄送人（如果有）
    if cc_list and len(cc_list) > 0:
        msg['Cc'] = ', '.join(cc_list)

    msg['Subject'] = subject

    # 替换变量
    content = substitute_variables(template, variables)

    # 添加正文
    mime_type = 'html' if is_html else 'plain'
    body = MIMEText(content, mime_type, 'utf-8')
    msg.attach(body)

    # 添加附件
    if attachments:
        for attach_path in attachments:
            if not os.path.exists(attach_path):
                print(f"警告: 附件不存在，跳过: {attach_path}")
                continue

            with open(attach_path, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
            encoders.encode_base64(part)

            # 正确处理中文文件名（RFC 2231 编码）
            filename = os.path.basename(attach_path)
            try:
                # 尝试 RFC 2231 编码，兼容大多数邮箱客户端
                filename_encoded = urllib.parse.quote(filename)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename*=UTF-8\'\'{filename_encoded}'
                )
            except Exception:
                # 降级方案：使用传统编码
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename="{filename}"'
                )

            msg.attach(part)

    return msg, content


def preview_message(email_addr, content, index):
    """干运行模式：预览邮件内容"""
    print("=" * 60)
    print(f"[{index+1}] 收件人: {email_addr}")
    print("-" * 60)
    print(content)
    print("-" * 60)
    print()


def clean_email(email_str):
    """清理邮箱地址中的特殊Unicode字符，只保留合法ASCII字符"""
    # 替换各种Unicode连字符/空格为普通ASCII
    email_clean = email_str
    # 非断字连字符 U+2011 → 普通减号
    email_clean = email_clean.replace('\u2011', '')
    # 不换行空格 U+00A0 → 普通空格
    email_clean = email_clean.replace('\u00A0', ' ')
    # 其他非ASCII字符去掉
    email_clean = ''.join(c for c in email_clean if ord(c) < 128)
    # 去掉开头的非字母数字字符（清理残留的横线空格）
    email_clean = email_clean.strip().lstrip('-_ ').strip()
    return email_clean

def send_emails(df, template, args):
    """发送邮件主逻辑"""
    total = len(df)
    success = 0
    failed = 0

    print(f"开始处理，共 {total} 个收件人...")
    print()

    if args.dry_run:
        print("=== 干运行模式 (预览不发送) ===")
        print()

    # 连接 SMTP
    if not args.dry_run:
        try:
            if args.smtp_port == 465:
                server = smtplib.SMTP_SSL(args.smtp_server, args.smtp_port)
            else:
                server = smtplib.SMTP(args.smtp_server, args.smtp_port)
                server.starttls()

            server.login(args.sender_email, args.sender_password)
            print("✓ SMTP 连接成功")
            print()
        except Exception as e:
            print(f"✗ SMTP 连接失败: {e}")
            return 0, total

    # 逐个处理
    for idx, row in df.iterrows():
        # 第一列是收件人邮箱
        email_addr = str(row.iloc[0]) if pd.notna(row.iloc[0]) else ""
        email_addr = clean_email(email_addr)
        if not email_addr or '@' not in email_addr:
            print(f"[{idx+1}] 跳过无效邮箱: {email_addr} (原始: {row.iloc[0]})")
            failed += 1
            continue

        # 第二列是抄送人列表（用 | 分割），为空则无抄送
        cc_list = []
        if df.shape[1] >= 2:
            cc_str = str(row.iloc[1]) if pd.notna(row.iloc[1]) else ""
            if cc_str and cc_str.strip():
                # 对每个抄送人也清理
                for cc in cc_str.split('|'):
                    cc_clean = clean_email(cc)
                    if cc_clean:
                        cc_list.append(cc_clean)

        # 第三列及以后是模板变量
        if df.shape[1] >= 3:
            variables = row.iloc[2:].tolist()
        else:
            variables = []

        # 创建消息
        msg, content = create_message(
            email_addr, cc_list, variables, template,
            args.subject, args.sender_email,
            args.html, args.attachments
        )

        # 干运行只预览
        if args.dry_run:
            preview_message(email_addr, content, idx)
            success += 1
            continue

        # 实际发送
        try:
            # 收集所有收件人：主送 + 抄送
            all_recipients = [email_addr] + cc_list
            server.send_message(msg, to_addrs=all_recipients)
            cc_info = f" (抄送: {', '.join(cc_list)})" if cc_list else ""
            print(f"[{idx+1}] ✓ 成功发送给 {email_addr}{cc_info}")
            success += 1
        except Exception as e:
            cc_info = f" (抄送: {', '.join(cc_list)})" if cc_list else ""
            print(f"[{idx+1}] ✗ 发送失败 {email_addr}{cc_info}: {e}")
            failed += 1

    if not args.dry_run:
        server.quit()

    print()
    print("=" * 60)
    print(f"处理完成: 成功 {success}, 失败 {failed}, 总计 {total}")
    print("=" * 60)

    return success, failed


def main():
    # 加载配置
    config = load_config()

    parser = argparse.ArgumentParser(
        description='批量发送个性化邮件'
    )
    parser.add_argument('--table', required=True, help='表格文件路径 (CSV 或 .xlsx)')
    parser.add_argument('--template', required=True, help='邮件模板文件路径')
    parser.add_argument('--subject', required=True, help='邮件主题')
    parser.add_argument('--smtp-server', help='SMTP 服务器地址（覆盖配置文件）')
    parser.add_argument('--smtp-port', type=int, help='SMTP 端口（覆盖配置文件，默认: 587）')
    parser.add_argument('--sender-email', help='发件人邮箱（覆盖配置文件）')
    parser.add_argument('--sender-password', help='发件人密码/授权码（覆盖配置文件）')
    parser.add_argument('--attachments', nargs='*', help='通用附件文件路径，多个用空格分隔')
    parser.add_argument('--dry-run', action='store_true', help='干运行模式，只预览不发送')
    parser.add_argument('--html', action='store_true', help='HTML格式邮件')
    parser.add_argument('--show-config', action='store_true', help='显示当前配置并退出')

    args = parser.parse_args()

    # 从配置文件读取，命令行参数覆盖
    if 'smtp' in config:
        args.smtp_server = args.smtp_server or config['smtp'].get('server', None)
        args.smtp_port = args.smtp_port or config['smtp'].getint('port', 587)
        args.sender_email = args.sender_email or config['smtp'].get('sender_email', None)
        args.sender_password = args.sender_password or config['smtp'].get('sender_password', None)

    # 显示配置并退出
    if args.show_config:
        print("当前 SMTP 配置:")
        print(f"  服务器: {args.smtp_server}")
        print(f"  端口: {args.smtp_port}")
        print(f"  发件人邮箱: {args.sender_email}")
        print(f"  配置文件: {CONFIG_PATH}")
        return

    # 检查必填项
    missing = []
    if not args.smtp_server:
        missing.append('smtp-server')
    if not args.smtp_port:
        missing.append('smtp-port')
    if not args.sender_email:
        missing.append('sender-email')
    if not args.sender_password:
        missing.append('sender-password')

    if missing:
        print(f"错误: 以下配置缺失: {', '.join(missing)}")
        print(f"请在配置文件 {CONFIG_PATH} 中设置，或通过命令行参数提供")
        return

    # 读取表格
    try:
        df = read_table(args.table)
    except Exception as e:
        print(f"读取表格失败: {e}")
        return

    print(f"读取表格成功，共 {len(df)} 行")

    # 读取模板
    try:
        template = read_template(args.template)
    except Exception as e:
        print(f"读取模板失败: {e}")
        return

    print(f"读取模板成功，模板长度: {len(template)} 字符")
    print(f"使用配置文件: {CONFIG_PATH}")

    # 检查模板变量数量与表格列数是否匹配
    table_variable_count = df.shape[1] - 2  # 减去第一列收件人邮箱 + 第二列抄送
    # 如果只有两列（只有邮箱和抄送，没有变量），变量数为0
    if table_variable_count < 0:
        table_variable_count = 0
    template_variable_count = count_template_variables(template)

    if table_variable_count != template_variable_count:
        print()
        print(f"⚠️  警告: 模板变量数量与表格变量列数不匹配")
        print(f"    表格格式: 第一列=收件人邮箱, 第二列=抄送人列表(|分隔), 第三列及以后=模板变量")
        print(f"    表格中变量列数: {table_variable_count} (除收件人邮箱和抄送列外)")
        print(f"    模板中找到变量: {template_variable_count} 个")
        print(f"    请检查表格和模板是否匹配")
        print()

    # 发送邮件
    send_emails(df, template, args)


if __name__ == '__main__':
    main()
