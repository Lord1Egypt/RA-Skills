#!/usr/bin/env python3
"""
法大大电子签命令行工具

Usage:
    # 发送文档给单个签署人
    fadada send /path/to/contract.pdf --signer "张三:13800138000"
    
    # 发送给多个签署人
    fadada send /path/to/contract.pdf --signer "张三:13800138000" --signer "李四:13900139000"
    
    # 使用配置文件
    fadada send /path/to/contract.pdf --signer "张三:13800138000" --config ~/.fadada/config.json
    
    # 查询签署状态
    fadada status <task_id>
    
    # 下载已签署文档
    fadada download <task_id> --output /path/to/save/
    
    # 配置管理
    fadada config setup
    fadada config show
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Tuple

from .client import FaDaDaClient
from .config import Config, setup_config_interactive
from .signer import Signer
from .exceptions import FaDaDaError


def parse_signer(signer_str: str) -> Tuple[str, str]:
    """解析签署人字符串 '姓名:手机号'"""
    parts = signer_str.split(':')
    if len(parts) != 2:
        raise ValueError(f"Invalid signer format: {signer_str}. Expected 'name:mobile'")
    return parts[0].strip(), parts[1].strip()


def cmd_send(args):
    """发送文档签署命令"""
    # 加载配置
    config = Config.load(args.config)
    
    if not config.is_valid():
        print("错误: 配置不完整，请先运行 'fadada config setup'")
        sys.exit(1)
    
    # 创建客户端
    client = FaDaDaClient(
        app_id=config.app_id,
        app_secret=config.app_secret,
        open_corp_id=config.open_corp_id,
        server_url=config.server_url,
        sandbox=config.sandbox
    )
    
    # 解析签署人
    signers = []
    for signer_str in args.signer:
        try:
            name, mobile = parse_signer(signer_str)
            signers.append(Signer(name=name, mobile=mobile))
        except ValueError as e:
            print(f"错误: {e}")
            sys.exit(1)
    
    if not signers:
        print("错误: 请至少指定一个签署人")
        sys.exit(1)
    
    # 确定任务主题
    task_subject = args.subject or Path(args.file).stem
    
    try:
        print(f"正在发送文档: {args.file}")
        print(f"任务主题: {task_subject}")
        print(f"签署人数量: {len(signers)}")
        print()
        
        # 发送文档
        result = client.send_document(
            file_path=args.file,
            signers=signers,
            task_subject=task_subject
        )
        
        print("=" * 50)
        print("✅ 签署任务创建成功！")
        print("=" * 50)
        print(f"任务 ID: {result['sign_task_id']}")
        print(f"签署链接: {result['sign_url']}")
        print()
        print("签署人将收到短信通知，点击链接即可签署。")
        
        # 保存结果
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"\n结果已保存到: {args.output}")
        
    except FaDaDaError as e:
        print(f"错误: {e}")
        sys.exit(1)


def cmd_status(args):
    """查询签署状态命令"""
    config = Config.load(args.config)
    
    if not config.is_valid():
        print("错误: 配置不完整")
        sys.exit(1)
    
    client = FaDaDaClient(
        app_id=config.app_id,
        app_secret=config.app_secret,
        open_corp_id=config.open_corp_id,
        server_url=config.server_url,
        sandbox=config.sandbox
    )
    
    try:
        detail = client.query_task_detail(args.task_id)
        
        print("=" * 50)
        print("签署任务详情")
        print("=" * 50)
        print(json.dumps(detail, ensure_ascii=False, indent=2))
        
    except FaDaDaError as e:
        print(f"错误: {e}")
        sys.exit(1)


def cmd_download(args):
    """下载已签署文档命令"""
    config = Config.load(args.config)
    
    if not config.is_valid():
        print("错误: 配置不完整")
        sys.exit(1)
    
    client = FaDaDaClient(
        app_id=config.app_id,
        app_secret=config.app_secret,
        open_corp_id=config.open_corp_id,
        server_url=config.server_url,
        sandbox=config.sandbox
    )
    
    try:
        download_url = client.get_download_url(args.task_id)
        
        print(f"下载链接: {download_url}")
        
        if args.output:
            import requests
            response = requests.get(download_url)
            output_path = Path(args.output)
            output_path.write_bytes(response.content)
            print(f"文件已保存到: {output_path}")
        
    except FaDaDaError as e:
        print(f"错误: {e}")
        sys.exit(1)


def cmd_config(args):
    """配置管理命令"""
    if args.action == "setup":
        setup_config_interactive()
    elif args.action == "show":
        config = Config.load()
        print("=" * 50)
        print("当前配置")
        print("=" * 50)
        print(f"App ID: {config.app_id or '(未设置)'}")
        print(f"Open Corp ID: {config.open_corp_id or '(未设置)'}")
        print(f"Server URL: {config.server_url or '(默认)'}")
        print(f"Sandbox: {config.sandbox}")
    else:
        print(f"未知操作: {args.action}")
        sys.exit(1)


def main():
    """主入口"""
    parser = argparse.ArgumentParser(
        prog="fadada",
        description="法大大电子签命令行工具"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # send 命令
    send_parser = subparsers.add_parser("send", help="发送文档签署")
    send_parser.add_argument("file", help="要签署的文件路径")
    send_parser.add_argument(
        "--signer", "-s",
        action="append",
        required=True,
        help="签署人信息，格式: '姓名:手机号'"
    )
    send_parser.add_argument(
        "--subject", "-t",
        help="任务主题（默认使用文件名）"
    )
    send_parser.add_argument(
        "--config", "-c",
        help="配置文件路径"
    )
    send_parser.add_argument(
        "--output", "-o",
        help="输出结果到文件"
    )
    send_parser.set_defaults(func=cmd_send)
    
    # status 命令
    status_parser = subparsers.add_parser("status", help="查询签署状态")
    status_parser.add_argument("task_id", help="签署任务ID")
    status_parser.add_argument(
        "--config", "-c",
        help="配置文件路径"
    )
    status_parser.set_defaults(func=cmd_status)
    
    # download 命令
    download_parser = subparsers.add_parser("download", help="下载已签署文档")
    download_parser.add_argument("task_id", help="签署任务ID")
    download_parser.add_argument(
        "--output", "-o",
        help="保存路径"
    )
    download_parser.add_argument(
        "--config", "-c",
        help="配置文件路径"
    )
    download_parser.set_defaults(func=cmd_download)
    
    # config 命令
    config_parser = subparsers.add_parser("config", help="配置管理")
    config_parser.add_argument(
        "action",
        choices=["setup", "show"],
        help="配置操作"
    )
    config_parser.set_defaults(func=cmd_config)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == "__main__":
    main()
