#!/usr/bin/env python3
"""
CLI-Notion: Notion 命令行接口
让 AI Agent 可以直接操作 Notion
"""

import click
import json
import os
import requests
from pathlib import Path


@click.group(invoke_without_command=True)
@click.option('--api-key', envvar='NOTION_API_KEY', help='Notion API Key')
@click.option('--json', 'json_output', is_flag=True, help='Output in JSON format')
@click.pass_context
def cli(ctx, api_key, json_output):
    """CLI-Notion: Notion 命令行接口"""
    ctx.ensure_object(dict)
    ctx.obj['json_output'] = json_output
    ctx.obj['api_key'] = api_key
    ctx.obj['headers'] = {
        'Authorization': f'Bearer {api_key}',
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json'
    } if api_key else {}
    
    if ctx.invoked_subcommand is None:
        click.echo("Use --help for available commands")


@cli.command()
@click.option('--parent', required=True, help='Parent database ID')
@click.option('--title', required=True, help='Page title')
@click.pass_context
def create_page(ctx, parent, title):
    """创建页面"""
    api_key = ctx.obj.get('api_key')
    if not api_key:
        click.echo("✗ 错误：需要 NOTION_API_KEY")
        return
    
    url = 'https://api.notion.com/v1/pages'
    data = {
        "parent": {"database_id": parent},
        "properties": {
            "Name": {
                "title": [{"text": {"content": title}}]
            }
        }
    }
    
    try:
        response = requests.post(url, headers=ctx.obj['headers'], json=data)
        response.raise_for_status()
        result = response.json()
        
        if ctx.obj.get('json_output'):
            click.echo(json.dumps({"action": "create_page", "id": result['id'], "title": title}))
        else:
            click.echo(f"✓ 已创建页面：{title}")
    except requests.exceptions.RequestException as e:
        if ctx.obj.get('json_output'):
            click.echo(json.dumps({"error": str(e)}))
        else:
            click.echo(f"✗ 创建失败：{str(e)}")


@cli.command()
@click.option('--database', required=True, help='Database ID')
@click.pass_context
def list_pages(ctx, database):
    """列出数据库中的页面"""
    api_key = ctx.obj.get('api_key')
    if not api_key:
        click.echo("✗ 错误：需要 NOTION_API_KEY")
        return
    
    url = f'https://api.notion.com/v1/databases/{database}/query'
    
    try:
        response = requests.post(url, headers=ctx.obj['headers'])
        response.raise_for_status()
        result = response.json()
        
        pages = []
        for page in result.get('results', []):
            title = page['properties'].get('Name', {}).get('title', [{}])[0].get('plain_text', 'Untitled')
            pages.append({"id": page['id'], "title": title})
        
        if ctx.obj.get('json_output'):
            click.echo(json.dumps({"pages": pages}))
        else:
            click.echo(f"📊 找到 {len(pages)} 个页面:")
            for p in pages[:10]:
                click.echo(f"  - {p['title']}")
            if len(pages) > 10:
                click.echo(f"  ... 还有 {len(pages) - 10} 个")
    except requests.exceptions.RequestException as e:
        if ctx.obj.get('json_output'):
            click.echo(json.dumps({"error": str(e)}))
        else:
            click.echo(f"✗ 查询失败：{str(e)}")


@cli.command()
@click.argument('page_id')
@click.pass_context
def get_page(ctx, page_id):
    """获取页面详情"""
    api_key = ctx.obj.get('api_key')
    if not api_key:
        click.echo("✗ 错误：需要 NOTION_API_KEY")
        return
    
    url = f'https://api.notion.com/v1/pages/{page_id}'
    
    try:
        response = requests.get(url, headers=ctx.obj['headers'])
        response.raise_for_status()
        result = response.json()
        
        if ctx.obj.get('json_output'):
            click.echo(json.dumps(result))
        else:
            click.echo(f"📄 页面详情：{page_id}")
    except requests.exceptions.RequestException as e:
        if ctx.obj.get('json_output'):
            click.echo(json.dumps({"error": str(e)}))
        else:
            click.echo(f"✗ 获取失败：{str(e)}")


@cli.command()
@click.pass_context
def status(ctx):
    """检查 API 状态"""
    api_key = ctx.obj.get('api_key')
    
    if not api_key:
        if ctx.obj.get('json_output'):
            click.echo(json.dumps({"status": "error", "message": "No API key"}))
        else:
            click.echo("✗ 未设置 NOTION_API_KEY")
        return
    
    # 简单测试：尝试获取用户信息
    url = 'https://api.notion.com/v1/users/me'
    try:
        response = requests.get(url, headers=ctx.obj['headers'])
        if response.status_code == 200:
            user = response.json()
            if ctx.obj.get('json_output'):
                click.echo(json.dumps({"status": "ok", "user": user['name']}))
            else:
                click.echo(f"✓ API 正常 | 用户：{user['name']}")
        else:
            if ctx.obj.get('json_output'):
                click.echo(json.dumps({"status": "error", "code": response.status_code}))
            else:
                click.echo(f"✗ API 错误：{response.status_code}")
    except requests.exceptions.RequestException as e:
        if ctx.obj.get('json_output'):
            click.echo(json.dumps({"status": "error", "message": str(e)}))
        else:
            click.echo(f"✗ 连接失败：{str(e)}")


if __name__ == '__main__':
    cli()
