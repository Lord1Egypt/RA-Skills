#!/usr/bin/env python3
"""
CRS 审计工具 CLI — 上传券商月结单，生成税务审计底稿 Excel。

用法:
  python3 do_audit.py file1.pdf file2.pdf [--method FIFO|ACB] [--output /path/to/dir]

环境变量:
  CRS_API_KEY  — 必须设置（从 wealthlplantation.com 获取）
"""
import base64, json, os, sys, urllib.request, urllib.error

API_URL = 'https://api.wealthlplantation.com/api/process'

def main():
    # --- 解析参数 ---
    args = sys.argv[1:]
    method = 'FIFO'
    out_dir = None
    paths = []
    i = 0
    while i < len(args):
        if args[i] == '--method' and i + 1 < len(args):
            method = args[i + 1].upper()
            i += 2
        elif args[i] == '--output' and i + 1 < len(args):
            out_dir = args[i + 1]
            i += 2
        else:
            paths.append(args[i])
            i += 1

    if not paths:
        print('用法: python3 do_audit.py file1.pdf file2.pdf [--method FIFO|ACB] [--output /path/to/dir]')
        sys.exit(1)

    api_key = os.environ.get('CRS_API_KEY', '')
    if not api_key:
        print('ERROR: CRS_API_KEY 未设置。请在 https://wealthlplantation.com 获取。')
        sys.exit(1)

    # --- 编码文件 ---
    mime_map = {
        '.pdf': 'application/pdf',
        '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        '.csv': 'text/csv',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
    }

    files = []
    for p in paths:
        if not os.path.isfile(p):
            print(f'WARNING: 文件不存在，跳过: {p}')
            continue
        with open(p, 'rb') as f:
            data = base64.b64encode(f.read()).decode()
        ext = os.path.splitext(p)[1].lower()
        files.append({
            'data': data,
            'mimeType': mime_map.get(ext, 'application/pdf'),
            'name': os.path.basename(p),
        })
        print(f'  OK: {os.path.basename(p)} ({os.path.getsize(p) // 1024}KB)')

    if not files:
        print('ERROR: 没有有效文件。')
        sys.exit(1)

    # --- 发送请求 ---
    payload = json.dumps({'files': files, 'costMethod': method}).encode()
    print(f'上传 {len(files)} 个文件 ({len(payload) // 1024}KB)...')

    req = urllib.request.Request(API_URL, data=payload, headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
    })

    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            result = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        result = json.loads(e.read().decode())

    # --- 处理结果 ---
    if result.get('success'):
        if not out_dir:
            out_dir = os.path.dirname(os.path.abspath(paths[0]))
        os.makedirs(out_dir, exist_ok=True)
        years = result.get('years', [])
        for yr in years:
            fname = yr['excel']['filename']
            out_path = os.path.join(out_dir, fname)
            with open(out_path, 'wb') as f:
                f.write(base64.b64decode(yr['excel']['data']))
            s = yr['summary']
            print(f'  生成: {out_path}')
            print(f'    记录数: {s["recordCount"]}, 币种: {",".join(s["currencies"])}')
            if s.get('netGainLossCNY') is not None:
                print(f'    净损益(CNY): {s["netGainLossCNY"]}')
            if s.get('finalTaxDueCNY') is not None:
                print(f'    估算税额(CNY): {s["finalTaxDueCNY"]}')
            issues = s.get('auditIssues', [])
            for issue in issues[:5]:
                print(f'    {issue.get("icon", "")} {issue.get("message", "")}')
        meta = result.get('meta', {})
        quota = meta.get('quota', {})
        print(f'完成: {meta.get("totalRecordsRaw", 0)} 条原始 -> {meta.get("totalRecordsValid", 0)} 条有效, 耗时 {meta.get("totalTimeMs", 0) // 1000}s')
        if quota:
            print(f'配额: 本次使用 {quota.get("pagesUsed", 0)} 页, 剩余 {quota.get("pagesRemaining", 0)} 页')
    else:
        err = result.get('error', {})
        print(f'ERROR: [{err.get("code")}] {err.get("message")}')
        if err.get('details'):
            print(f'  详情: {err["details"]}')
        sys.exit(1)


if __name__ == '__main__':
    main()
