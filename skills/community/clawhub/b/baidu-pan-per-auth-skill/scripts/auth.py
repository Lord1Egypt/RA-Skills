#!/usr/bin/env python3
"""百度网盘OAuth2.0授权码模式 — 获取/刷新access_token

Usage:
  auth.py code <code> <env_path>   — 授权码换token
  auth.py refresh <env_path>       — 刷新token
"""
import sys, json, urllib.request, urllib.parse, datetime

TOKEN_KEYS = ('AccessToken', 'RefreshToken', 'ExpiresIn', 'Scope', 'AuthDate')


def load_env(path):
    """解析简单key=value格式.env文件"""
    cfg = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                cfg[k.strip()] = v.strip()
    return cfg


def write_env_tokens(env_path, data):
    """更新.env中的token字段（去重：先移除旧值再写入新值）"""
    lines = []
    with open(env_path) as f:
        for line in f:
            k = line.split('=', 1)[0].strip() if '=' in line else ''
            if k in TOKEN_KEYS:
                continue
            lines.append(line)
    # 确保末尾有换行
    if lines and not lines[-1].endswith('\n'):
        lines[-1] += '\n'
    with open(env_path, 'w') as f:
        f.writelines(lines)
        f.write(f"AccessToken={data['access_token']}\n")
        f.write(f"RefreshToken={data['refresh_token']}\n")
        f.write(f"ExpiresIn={data['expires_in']}\n")
        f.write(f"Scope={data.get('scope', '')}\n")
        f.write(f"AuthDate={datetime.date.today().isoformat()}\n")


def _request_token(params):
    """发起token请求，返回JSON"""
    url = f'https://openapi.baidu.com/oauth/2.0/token?{urllib.parse.urlencode(params)}'
    req = urllib.request.Request(url, headers={'User-Agent': 'pan.baidu.com'})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
    except urllib.error.URLError as e:
        print(f"ERROR: 网络请求失败 - {e}", file=sys.stderr)
        sys.exit(1)
    if 'access_token' not in data:
        print(f"ERROR: {json.dumps(data, ensure_ascii=False)}", file=sys.stderr)
        sys.exit(1)
    return data


def exchange_code(code, env_path):
    """用授权码换取access_token"""
    cfg = load_env(env_path)
    data = _request_token({
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': cfg['AppKey'],
        'client_secret': cfg['SecretKey'],
        'redirect_uri': 'oob',
    })
    write_env_tokens(env_path, data)
    print(f"✅ Token获取成功！有效期{data['expires_in']}秒（{int(data['expires_in'])//86400}天）")
    print(f"   过期日期：{datetime.date.today() + datetime.timedelta(seconds=int(data['expires_in']))}")


def refresh_token(env_path):
    """用refresh_token刷新access_token"""
    cfg = load_env(env_path)
    if 'RefreshToken' not in cfg or not cfg['RefreshToken']:
        print("ERROR: .env中无RefreshToken，请先执行首次授权(auth.py code)", file=sys.stderr)
        sys.exit(1)
    data = _request_token({
        'grant_type': 'refresh_token',
        'refresh_token': cfg['RefreshToken'],
        'client_id': cfg['AppKey'],
        'client_secret': cfg['SecretKey'],
    })
    write_env_tokens(env_path, data)
    print(f"✅ Token刷新成功！有效期{data['expires_in']}秒（{int(data['expires_in'])//86400}天）")
    print(f"   过期日期：{datetime.date.today() + datetime.timedelta(seconds=int(data['expires_in']))}")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage:")
        print("  auth.py code <code> <env_path>   — 授权码换token")
        print("  auth.py refresh <env_path>       — 刷新token")
        sys.exit(1)
    action = sys.argv[1]
    if action == 'code':
        if len(sys.argv) < 4:
            print("ERROR: code命令需要 <code> <env_path> 两个参数", file=sys.stderr)
            sys.exit(1)
        exchange_code(sys.argv[2], sys.argv[3])
    elif action == 'refresh':
        refresh_token(sys.argv[2])
    else:
        print(f"Unknown action: {action}", file=sys.stderr)
        sys.exit(1)
