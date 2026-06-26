#!/usr/bin/env python3
"""批量写入飞书多维表格记录"""
import json, sys, ssl, urllib.request, time

def get_config():
    """从配置文件读取飞书凭据"""
    with open('/root/.openclaw/openclaw.json') as f:
        config = json.load(f)
    feishu_cfg = config.get('channels', {}).get('feishu', {})
    return feishu_cfg.get('appId', ''), feishu_cfg.get('appSecret', '')

def get_access_token(app_id, app_secret):
    url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
    data = json.dumps({'app_id': app_id, 'app_secret': app_secret}).encode()
    req = urllib.request.Request(url, data=data, method='POST')
    req.add_header('Content-Type', 'application/json')
    ctx = ssl._create_unverified_context()
    with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
        resp = json.loads(r.read())
    return resp.get('tenant_access_token', '')

def call_api(url, method, token, payload=None):
    ctx = ssl._create_unverified_context()
    data = json.dumps(payload, ensure_ascii=False).encode() if payload else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header('Authorization', f'Bearer {token}')
    req.add_header('Content-Type', 'application/json')
    with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
        return json.loads(r.read())

def batch_create_records(app_token, table_id, records, token, batch_size=50):
    """批量创建记录"""
    url = f'https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create'
    total = len(records)
    created = 0
    for i in range(0, total, batch_size):
        batch = records[i:i+batch_size]
        payload = {'records': batch}
        resp = call_api(url, 'POST', token, payload)
        if resp.get('code') == 0:
            n = len(resp.get('data', {}).get('records', []))
            created += n
            print(f'  [{i+1}-{min(i+batch_size,total)}/{total}] OK +{n}', file=sys.stderr)
        else:
            print(f'  [{i+1}-{min(i+batch_size,total)}/{total}] FAIL: {resp.get("msg")}', file=sys.stderr)
        time.sleep(0.3)
    return created

def batch_delete_records(app_token, table_id, record_ids, token, batch_size=50):
    """批量删除记录"""
    url = f'https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_delete'
    total = len(record_ids)
    deleted = 0
    for i in range(0, total, batch_size):
        batch = record_ids[i:i+batch_size]
        payload = {'records': batch}
        resp = call_api(url, 'POST', token, payload)
        if resp.get('code') == 0:
            deleted += len(batch)
            print(f'  [{i+1}-{min(i+batch_size,total)}/{total}] OK +{len(batch)}', file=sys.stderr)
        else:
            print(f'  [{i+1}-{min(i+batch_size,total)}/{total}] FAIL: {resp.get("msg")}', file=sys.stderr)
        time.sleep(0.3)
    return deleted

def add_permission(file_token, member_type, member_id, perm, token, file_type='bitable'):
    """添加协作者"""
    url = f'https://open.feishu.cn/open-apis/drive/v1/permissions/{file_token}/members?type={file_type}'
    payload = {
        'member_type': member_type,  # openid | email | userid
        'member_id': member_id,
        'perm': perm  # view | edit | full_access
    }
    return call_api(url, 'POST', token, payload)

if __name__ == '__main__':
    # 示例用法
    print(__doc__)
    print('Usage: import from this script and call the functions')