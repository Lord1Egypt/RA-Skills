# -*- coding: utf-8 -*-
"""动环综合网管 交互式登录工具

登录流程（已验证可用）：
  1. 建立会话，下载图片验证码（算术题）
  2. ddddocr 自动识别图片验证码，在终端展示，供用户确认
  3. 获取 RSA 公钥，对密码做 RSA-OAEP-SHA256 加密
  4. **先调用 /login/sendPhoneCode 触发短信下发**（图片验证码校验通过才发）
  5. 用户查收手机短信，手动输入短信验证码
  6. 调用 /login/go 完成登录，保存 Cookie 到文件

图片验证码由脚本自动识别填写，短信验证码需用户手动输入。
登录成功后把 WEB_SESSION_ID_KEY 写入 --cookie-file，供定时任务复用。

用法：
  python donguan_login.py --username 05310480 --password 'XZ$ua98E#dYO' \
      --cookie-file dh_session_cookie.txt
"""
import json, sys, os, subprocess, re, base64, argparse
sys.stdout.reconfigure(encoding='utf-8')


# ===== 默认配置 =====
DEFAULT_BASE = 'https://172.20.251.9:30666'


# ===== curl 封装 =====
def _curl_get(url, CJ):
    r = subprocess.run(
        ['curl', '-k', '-s', '--connect-timeout', '15', '-b', CJ, '-c', CJ, url],
        capture_output=True, timeout=30)
    return r.stdout


def _curl_post(url, data, CJ):
    body = json.dumps(data, ensure_ascii=False)
    r = subprocess.run(
        ['curl', '-k', '-s', '--connect-timeout', '15', '-b', CJ, '-c', CJ,
         '-X', 'POST', url, '-H', 'Content-Type: application/json', '-d', body],
        capture_output=True, encoding='utf-8', errors='replace', timeout=30)
    return r.stdout


def _curl_bin(url, CJ):
    r = subprocess.run(
        ['curl', '-k', '-s', '--connect-timeout', '15', '-b', CJ, '-c', CJ, url],
        capture_output=True, timeout=30)
    return r.stdout or b''


def _rsa_encrypt(plaintext, pubkey_b64, workdir):
    pem = "-----BEGIN PUBLIC KEY-----\n"
    pem += '\n'.join([pubkey_b64[i:i + 64] for i in range(0, len(pubkey_b64), 64)])
    pem += "\n-----END PUBLIC KEY-----\n"
    pub_path = os.path.join(workdir, '_pub.pem')
    open(pub_path, 'w').write(pem)
    pwd_path = os.path.join(workdir, '_pwd.txt')
    with open(pwd_path, 'wb') as f:
        f.write(plaintext.encode('utf-8'))
    enc = subprocess.run([
        'openssl', 'pkeyutl', '-encrypt', '-pubin', '-inkey', pub_path,
        '-pkeyopt', 'rsa_padding_mode:oaep',
        '-pkeyopt', 'rsa_oaep_md:sha256',
        '-pkeyopt', 'rsa_mgf1_md:sha256',
        '-in', pwd_path
    ], capture_output=True, timeout=30)
    if enc.returncode != 0:
        print(f'RSA加密失败: {enc.stderr.decode().strip()}')
        return None
    return base64.b64encode(enc.stdout).decode()


def _parse_cookie(CJ):
    if os.path.exists(CJ):
        for line in open(CJ):
            if 'WEB_SESSION_ID_KEY' in line:
                parts = line.strip().split('\t')
                if len(parts) >= 7:
                    return parts[6]
    return None


def solve_captcha_ocr(img_bytes):
    """用 ddddocr 识别验证码图片，提取算术答案"""
    try:
        import ddddocr
        ocr = ddddocr.DdddOcr(show_ad=False)
    except ImportError:
        return None, None
    raw = ocr.classification(img_bytes)
    text = raw.strip()
    m = re.match(r'^(\d)\s*([+\-xX\*×])\s*(\d)\s*[=]\s*(\d|\?)$', text)
    if not m:
        return None, raw
    d1, op, d2, ans = m.groups()
    op_norm = '*' if op in ('x', 'X', '*', '×') else op
    try:
        result = str(int(eval(f'{d1} {op_norm} {d2}')))
    except Exception:
        result = None
    return result, raw


def interactive_login(base, username, password, cookie_file, workdir):
    """交互式登录：自动识别图片验证码 + RSA加密，先触发短信，再手动输短信码。"""
    CJ = os.path.join(workdir, '_login_cookies.txt')
    open(CJ, 'w').close()
    # 1. 建立会话
    subprocess.run(['curl', '-k', '-s', '--connect-timeout', '15', '-c', CJ, base + '/'],
                   capture_output=True, timeout=15)

    # 2. 下载验证码 + OCR
    img_data = _curl_bin(base + '/login/getVerifyCode?sign=1', CJ)
    cap_path = os.path.join(workdir, '_captcha.png')
    with open(cap_path, 'wb') as f:
        f.write(img_data)

    answer, ocr_raw = solve_captcha_ocr(img_data)
    print('\n=== 动环系统交互式登录 ===')
    print(f'用户名: {username}')
    print(f'验证码图片已保存: {cap_path}')
    if answer is not None:
        print(f'[OCR识别] 算式: {ocr_raw}  答案: {answer}')
        print('（请确认图片中的算式答案，如有偏差请手动输入正确值）')
    else:
        print(f'[OCR识别] 无法自动解析: {ocr_raw}，请直接看图输入答案')

    captcha = input('请输入图片验证码算式答案: ').strip()
    if not captcha:
        captcha = str(answer) if answer is not None else ''
    if not captcha:
        print('未输入验证码，登录中止')
        return None

    # 3. 获取公钥 + 加密密码
    pk_resp = _curl_post(base + '/login/getPublicKey', {}, CJ)
    try:
        pk_data = json.loads(pk_resp).get('data', '')
    except Exception:
        print('公钥获取失败')
        return None
    if not pk_data:
        return None
    cipher = _rsa_encrypt(password, pk_data, workdir)
    if not cipher:
        return None

    # 4. 先触发短信下发（图片验证码校验通过才发）
    send_resp_text = _curl_post(base + '/login/sendPhoneCode', {
        'username': username,
        'userCipher': cipher,
        'verifyCode': captcha,
        'phoneCode': ''
    }, CJ)
    try:
        send_resp = json.loads(send_resp_text)
        if send_resp.get('code') == 200:
            print(f'[OK] {send_resp.get("msg", "短信已发送")}，请查收手机')
        else:
            print(f'[!] 短信下发失败: {send_resp.get("msg")}（验证码可能错误）')
            # 不立即中止，仍允许尝试登录（有时短信码已有效）
    except Exception:
        print(f'[!] 短信接口响应异常: {send_resp_text[:120]}')

    # 5. 手动输入短信码
    sms = input('请输入手机短信验证码（动态码）: ').strip()
    if not sms:
        print('未输入短信验证码，登录中止')
        return None

    # 6. 完成登录
    resp_text = _curl_post(base + '/login/go', {
        'username': username,
        'userCipher': cipher,
        'verifyCode': captcha,
        'phoneCode': sms
    }, CJ)
    try:
        resp = json.loads(resp_text)
        if resp.get('code') == 200:
            cookie_val = _parse_cookie(CJ)
            if cookie_val:
                with open(cookie_file, 'w', encoding='utf-8') as cf:
                    cf.write(cookie_val)
                print(f'[成功] 登录成功! Cookie 已保存到: {cookie_file}')
                return cookie_val
            print('[成功] 登录成功但未找到 Cookie')
            return None
        else:
            print(f'[失败] {resp.get("msg")}')
            return None
    except Exception as e:
        print(f'[异常] {e}')
        return None


def main():
    ap = argparse.ArgumentParser(description='动环综合网管交互式登录')
    ap.add_argument('--base-url', default=DEFAULT_BASE, help='动环系统 Base URL')
    ap.add_argument('--username', required=True, help='登录用户名')
    ap.add_argument('--password', required=True, help='登录密码（明文）')
    ap.add_argument('--cookie-file', required=True, help='Cookie 保存路径')
    ap.add_argument('--workdir', default=None, help='临时文件目录（默认脚本所在目录）')
    args = ap.parse_args()

    workdir = args.workdir or os.path.dirname(os.path.abspath(__file__))
    cookie = interactive_login(args.base_url, args.username, args.password, args.cookie_file, workdir)
    sys.exit(0 if cookie else 1)


if __name__ == '__main__':
    main()
