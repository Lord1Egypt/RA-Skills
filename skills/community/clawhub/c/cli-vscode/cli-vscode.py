#!/usr/bin/env python3
"""
CLI-VSCode: VSCode 命令行接口
让 AI Agent 可以直接操作 VSCode
"""

import click
import json
import os
import subprocess
from pathlib import Path


@click.group(invoke_without_command=True)
@click.option('--json', 'json_output', is_flag=True, help='Output in JSON format')
@click.pass_context
def cli(ctx, json_output):
    """CLI-VSCode: VSCode 命令行接口"""
    ctx.ensure_object(dict)
    ctx.obj['json_output'] = json_output
    
    if ctx.invoked_subcommand is None:
        click.echo("Use --help for available commands")


@cli.command()
@click.argument('file', required=False)
@click.pass_context
def open(ctx, file):
    """打开文件或 VSCode"""
    cmd = ['code']
    if file:
        cmd.append(file)
    
    try:
        subprocess.run(cmd, check=True)
        if ctx.obj.get('json_output'):
            click.echo(json.dumps({"action": "open", "file": file or "VSCode"}))
        else:
            click.echo(f"✓ 已打开：{file or 'VSCode'}")
    except FileNotFoundError:
        if ctx.obj.get('json_output'):
            click.echo(json.dumps({"error": "VSCode not found. Please install VSCode CLI."}))
        else:
            click.echo("✗ 错误：未找到 VSCode。请安装 code 命令行工具。")


@cli.command()
@click.option('--id', required=True, help='Extension ID')
@click.pass_context
def install_extension(ctx, id):
    """安装扩展"""
    cmd = ['code', '--install-extension', id]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        if ctx.obj.get('json_output'):
            click.echo(json.dumps({"action": "install_extension", "id": id, "status": "success"}))
        else:
            click.echo(f"✓ 已安装扩展：{id}")
    except subprocess.CalledProcessError as e:
        if ctx.obj.get('json_output'):
            click.echo(json.dumps({"error": str(e)}))
        else:
            click.echo(f"✗ 安装失败：{id}")


@cli.command()
@click.pass_context
def list_extensions(ctx):
    """列出已安装的扩展"""
    cmd = ['code', '--list-extensions']
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        extensions = result.stdout.strip().split('\n')
        
        if ctx.obj.get('json_output'):
            click.echo(json.dumps({"extensions": extensions}))
        else:
            click.echo(f"📦 已安装 {len(extensions)} 个扩展:")
            for ext in extensions[:20]:
                click.echo(f"  - {ext}")
            if len(extensions) > 20:
                click.echo(f"  ... 还有 {len(extensions) - 20} 个")
    except subprocess.CalledProcessError as e:
        if ctx.obj.get('json_output'):
            click.echo(json.dumps({"error": str(e)}))
        else:
            click.echo("✗ 无法列出扩展")


@cli.command()
@click.argument('folder')
@click.pass_context
def add_folder(ctx, folder):
    """添加文件夹到工作区"""
    cmd = ['code', '--add', folder]
    
    try:
        subprocess.run(cmd, check=True)
        if ctx.obj.get('json_output'):
            click.echo(json.dumps({"action": "add_folder", "folder": folder}))
        else:
            click.echo(f"✓ 已添加文件夹：{folder}")
    except subprocess.CalledProcessError as e:
        if ctx.obj.get('json_output'):
            click.echo(json.dumps({"error": str(e)}))
        else:
            click.echo(f"✗ 添加失败")


@cli.command()
@click.pass_context
def status(ctx):
    """显示 VSCode 状态"""
    # 检查 code 命令是否可用
    try:
        result = subprocess.run(['code', '--version'], capture_output=True, text=True)
        version = result.stdout.strip().split('\n')[0]
        
        status_info = {
            "installed": True,
            "version": version
        }
        
        if ctx.obj.get('json_output'):
            click.echo(json.dumps(status_info))
        else:
            click.echo(f"✓ VSCode 已安装")
            click.echo(f"  版本：{version}")
    except FileNotFoundError:
        if ctx.obj.get('json_output'):
            click.echo(json.dumps({"installed": False, "error": "VSCode CLI not found"}))
        else:
            click.echo("✗ VSCode 未安装或 code 命令不可用")


if __name__ == '__main__':
    cli()
