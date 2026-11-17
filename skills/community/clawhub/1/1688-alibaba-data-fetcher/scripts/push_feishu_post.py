#!/usr/bin/env python3
"""
1688 飞书推送 - 使用 post + md 标签，正确渲染 markdown 表格
直接调用飞书 open API（不依赖 OpenClaw message 工具，因为后者走 text 路径不渲染表格）

用法：
  python3 push_feishu_post.py <markdown.md> [chat_id]

环境变量（从 scripts/env.ps1 加载；也可直接 export）：
  FEISHU_APP_ID      - 飞书应用 App ID（cli_xxx）
  FEISHU_APP_SECRET  - 飞书应用 App Secret
  FEISHU_CHAT_ID     - 默认目标群聊 chat_id（oc_xxx）
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# ===================== 配置加载 =====================
# 优先从同级 env.ps1 / env.sh 加载环境变量（如有）

def _load_env_file():
    """从 scripts/env.ps1 或 scripts/env.sh 加载 FEISHU_* 变量。
    不依赖 PowerShell 解析（PowerShell 变量语法复杂），改用简单 regex 提取。
    """
    scripts_dir = Path(__file__).resolve().parent
    for fname in ('env.ps1', 'env.sh'):
        env_path = scripts_dir / fname
        if not env_path.exists():
            continue
        try:
            text = env_path.read_text(encoding='utf-8')
        except Exception:
            continue
        import re
        for var in ('FEISHU_APP_ID', 'FEISHU_APP_SECRET', 'FEISHU_CHAT_ID'):
            m = re.search(rf'{var}\s*=\s*["\']?([^"\'#\r\n]+)', text)
            if m and not os.environ.get(var):
                val = m.group(1).strip().rstrip(';').strip()
                # env.ps1 可能写成 "<FEISHU_APP_ID>" 这种占位，跳过
                if val and not val.startswith('<'):
                    os.environ[var] = val


_load_env_file()

APP_ID = os.environ.get('FEISHU_APP_ID', '')
APP_SECRET = os.environ.get('FEISHU_APP_SECRET', '')
DEFAULT_CHAT_ID = os.environ.get('FEISHU_CHAT_ID', '')

FEISHU_BASE = 'https://open.feishu.cn/open-apis'
TOKEN_CACHE = Path(__file__).resolve().parent / '.feishu_token.json'


# ===================== Token 管理 =====================

def get_tenant_access_token(force_refresh=False):
    """获取 tenant_access_token，优先用缓存（提前 60s 续期）"""
    if not force_refresh and TOKEN_CACHE.exists():
        try:
            with open(TOKEN_CACHE, encoding='utf-8') as f:
                cached = json.load(f)
            if cached.get('expire', 0) > time.time() + 60:
                return cached['token']
        except Exception:
            pass

    if not APP_ID or not APP_SECRET:
        raise RuntimeError('缺少 FEISHU_APP_ID / FEISHU_APP_SECRET（配置在 scripts/env.ps1）')

    url = f'{FEISHU_BASE}/auth/v3/tenant_access_token/internal'
    body = json.dumps({'app_id': APP_ID, 'app_secret': APP_SECRET}).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=body,
        headers={'Content-Type': 'application/json'},
        method='POST',
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    if data.get('code') != 0:
        raise RuntimeError(f'获取 token 失败: code={data.get("code")} msg={data.get("msg")}')

    token = data['tenant_access_token']
    expire_in = data.get('expire', 7200)
    with open(TOKEN_CACHE, 'w', encoding='utf-8') as f:
        json.dump({'token': token, 'expire': time.time() + expire_in}, f)
    return token


# ===================== 发送消息 =====================

def send_post_md(chat_id, markdown_text):
    """
    发送 post 类型消息，content 使用 md 标签（支持 GFM 表格、任务列表、删除线、代码块等）
    API 文档: https://open.feishu.cn/document/server-docs/im-v1/message-content-description/create_json
    """
    token = get_tenant_access_token()

    # post content 结构：每个段落是一个 list of tags
    # 一个 md 标签就够（整段 markdown 作为一个段落）
    content_obj = {
        'zh_cn': {
            'content': [
                [{'tag': 'md', 'text': markdown_text}],
            ],
        },
    }
    body = {
        'receive_id': chat_id,
        'msg_type': 'post',
        'content': json.dumps(content_obj, ensure_ascii=False),
    }

    def _post():
        url = f'{FEISHU_BASE}/im/v1/messages?receive_id_type=chat_id'
        req = urllib.request.Request(
            url,
            data=json.dumps(body).encode('utf-8'),
            headers={
                'Content-Type': 'application/json; charset=utf-8',
                'Authorization': f'Bearer {token}',
            },
            method='POST',
        )
        return urllib.request.urlopen(req, timeout=15)

    try:
        with _post() as resp:
            data = json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode('utf-8', errors='replace')
        raise RuntimeError(f'飞书 API HTTP {e.code}: {err_body}')

    # token 过期类错误重试一次
    if data.get('code') in (99991663, 99991668, 99991664):
        token = get_tenant_access_token(force_refresh=True)
        with _post() as resp:
            data = json.loads(resp.read().decode('utf-8'))

    if data.get('code') != 0:
        raise RuntimeError(f'发送失败: code={data.get("code")} msg={data.get("msg")}')

    return data.get('data', {}).get('message_id')


# ===================== 主函数 =====================

def main():
    import argparse
    ap = argparse.ArgumentParser(description='1688 飞书推送（post+md，正确渲染表格）')
    ap.add_argument('markdown', nargs='?', help='Markdown 文件路径')
    ap.add_argument('chat_id', nargs='?', default=DEFAULT_CHAT_ID, help=f'目标 chat_id（默认从 env 读取: {DEFAULT_CHAT_ID or "未配置"}）')
    ap.add_argument('--check', action='store_true', help='仅检查 token 是否能获取，不发送')
    args = ap.parse_args()

    if args.check:
        token = get_tenant_access_token()
        print(f'✅ token 获取成功（前 8 位）: {token[:8]}...')
        return

    if not args.chat_id:
        print('错误: 未指定 chat_id，且 env 中未配置 FEISHU_CHAT_ID', file=sys.stderr)
        sys.exit(1)

    md_path = Path(args.markdown)
    if not md_path.exists():
        print(f'文件不存在: {md_path}', file=sys.stderr)
        sys.exit(1)

    md_text = md_path.read_text(encoding='utf-8')
    print(f'→ 读取 {md_path} ({len(md_text)} chars)')
    print(f'→ chat_id: {args.chat_id}')

    msg_id = send_post_md(args.chat_id, md_text)
    print(f'✅ 发送成功，message_id: {msg_id}')


if __name__ == '__main__':
    main()
