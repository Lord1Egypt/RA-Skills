#!/usr/bin/env python3
"""
crypto_utils.py — 加密、哈希与精确计算工具（纯标准库）
覆盖：MD5/SHA 哈希、AES 加解密（Base64模拟）、密码生成、UUID/HMAC、校验和

用法：
  python crypto_utils.py hash file.txt --algo md5
  python crypto_utils.py hash "Hello World" --text --algo sha256
  python crypto_utils.py password --length 20 --special
  python crypto_utils.py uuid -n 5
  python crypto_utils.py hmac secret-key "message"
  python crypto_utils.py base64-encode "Hello" --url-safe
  python crypto_utils.py base64-decode "SGVsbG8="
  python crypto_utils.py xor-crypt "secret data" "key123"
  python crypto_utils.py checksum file.bin
  python crypto_utils.py token --bytes 32
"""

import sys
import os
import hashlib
import base64
import secrets
import uuid as uuid_module
import hmac as hmac_lib
import re
from typing import Optional


# ─── CLI ──────────────────────────────────────────────────────

def parse_args(argv=None):
    argv = argv or sys.argv[1:]
    if not argv or '-h' in argv or '--help' in argv:
        print(__doc__)
        sys.exit(0)
    cmd = argv[0]
    args = {'_cmd': cmd, '_pos': []}
    i = 1
    while i < len(argv):
        a = argv[i]
        if a.startswith('-'):
            key = a.lstrip('-').replace('-', '_')
            if i + 1 < len(argv) and not argv[i+1].startswith('-'):
                args[key] = argv[i + 1]
                i += 2
            else:
                args[key] = True
                i += 1
        else:
            args['_pos'].append(a)
            i += 1
    return args


def color(text: str, fg: str = '') -> str:
    codes = {'red': 31, 'green': 32, 'yellow': 33, 'blue': 34, 'cyan': 36}
    code = codes.get(fg, '')
    if not code:
        return text
    if hasattr(sys.stdout, 'isatty') and sys.stdout.isatty():
        return f'\033[{code}m{text}\033[0m'
    return text


def echo(text: str, fg: str = '', bold=False):
    print(color(text, fg))


# ══════════════════════════════════════════════════════════════
#  命令实现
# ══════════════════════════════════════════════════════════════

# ─── 哈希 ──────────────────────────────────────────────────

HASH_ALGORITHMS = {
    'md5': (hashlib.md5, 32),
    'sha1': (hashlib.sha1, 40),
    'sha224': (hashlib.sha224, 56),
    'sha256': (hashlib.sha256, 64),
    'sha384': (hashlib.sha384, 96),
    'sha512': (hashlib.sha512, 128),
    'sha3_224': lambda d=None: (lambda: (hashlib.sha3_224(d) if d else hashlib.sha3_224), 56),
    'sha3_256': lambda d=None: (lambda: (hashlib.sha3_256(d) if d else hashlib.sha3_256), 64),
    'sha3_512': lambda d=None: (lambda: (hashlib.sha3_512(d) if d else hashlib.sha3_512), 128),
    'blake2b': lambda d=None: (lambda: (hashlib.blake2b(d) if d else hashlib.blake2b), 128),
    'blake2s': lambda d=None: (lambda: (hashlib.blake2s(d) if d else hashlib.blake2s), 64),
}


def _get_hasher(algo_name: str):
    """获取哈希算法构造函数和输出长度"""
    algo_name = algo_name.lower().strip()
    spec = HASH_ALGORITHMS.get(algo_name)
    if spec is None:
        raise ValueError(f'未知哈希算法: {algo_name}. 可选: {", ".join(HASH_ALGORITHMS.keys())}')
    if callable(spec):
        result = spec()
        return result() if callable(result) else result
    return spec[0]


def cmd_hash(args):
    """计算文件或文本的哈希值"""
    target = args['_pos'][0] if len(args.get('_pos', [])) > 0 else ''
    is_text = args.get('text', False)
    algo = args.get('algo', 'sha256').lower().strip()
    output = args.get('o', '')

    try:
        hasher_func = _get_hasher(algo)
        # 处理可调用情况
        if isinstance(HASH_ALGORITHMS.get(algo), tuple):
            hasher_func = HASH_ALGORITHMS[algo][0]
    except ValueError as e:
        echo(str(e), fg='red')
        sys.exit(1)

    if is_text or (target and not os.path.isfile(target)):
        # 文本模式
        data = target.encode('utf-8')
        h = hasher_func(data)
        digest = h.hexdigest()
    elif os.path.isfile(target):
        # 文件模式
        h = hasher_func()
        fsize = os.path.getsize(target)
        with open(target, 'rb') as f:
            # 大文件分块读取
            chunk_size = 65536
            read = 0
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                h.update(chunk)
                read += len(chunk)
                if fsize > 1024 * 1024:
                    pct = read / fsize * 100
                    sys.stderr.write(f'\r  计算中: {pct:.1f}% ({read//1024}KB/{fsize//1024}KB)')
                    sys.stderr.flush()
        print()
        digest = h.hexdigest()
    else:
        echo(f'❌ 文件不存在: {target}', fg='red')
        sys.exit(1)

    result_line = f'{algo.upper()}({os.path.basename(target) if os.path.exists(target) else target}) = {digest}'
    echo(result_line, fg='cyan')

    # 同时输出其他常见哈希用于对比
    if args.get('all'):
        other_algos = [k for k in ['md5', 'sha1', 'sha256'] if k != algo]
        for oa in other_algos:
            try:
                oh = _get_hasher(oa) if isinstance(HASH_ALGORITHMS.get(oa), tuple) else HASH_ALGORITHMS[oa][0]
                if isinstance(HASH_ALGORITHMS.get(oa), tuple):
                    oh = HASH_ALGORITHMS[oa][0]
                if is_text or (target and not os.path.isfile(target)):
                    od = oh(target.encode('utf-8')).hexdigest()
                else:
                    oh2 = oh()
                    with open(target, 'rb') as f:
                        for chunk in iter(lambda: f.read(65536), b''):
                            oh2.update(chunk)
                    od = oh2.hexdigest()
                echo(f'  {oa.upper()} = {od}', fg='blue')
            except Exception:
                pass

    if output:
        mode = 'w'
        content = digest
        if args.get('binary', False) or args.get('bin'):
            mode = 'wb'
            content = bytes.fromhex(digest)
        with open(output, mode) as f:
            f.write(content)
        echo(f'✅ 已写入: {output}', fg='green')


def cmd_password(args):
    """生成安全随机密码"""
    length = int(args.get('length', 16))
    count = int(args.get('count', 1))
    use_special = args.get('special', True)
    use_upper = args.get('upper', True)
    use_digits = args.get('digits', True)
    exclude_ambiguous = args.get('no_ambiguous', True)
    pattern = args.get('pattern', '')

    ambiguous_chars = 'lI1oO0'

    passwords = []
    for _ in range(count):
        if pattern:
            # 按自定义字符集生成
            charset = pattern
            pwd = ''.join(secrets.choice(charset) for _ in range(length))
        else:
            chars = list('abcdefghijklmnopqrstuvwxyz')
            if use_upper:
                chars.extend('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            if use_digits:
                chars.extend('0123456789')
            if use_special:
                chars.extend('!@#$%^&*()-_=+[]{}|;:,.<>?')
            if exclude_ambiguous:
                chars = [c for c in chars if c not in ambiguous_chars]

            if not chars:
                echo('❌ 字符集为空，请检查参数', fg='red')
                sys.exit(1)

            pwd = ''.join(secrets.choice(chars) for _ in range(length))

        passwords.append(pwd)

    # 输出
    if count == 1:
        echo(passwords[0], fg='green', bold=True)
        entropy = length * __import__('math').log2(len(set(
            'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+[]{}|;:,.<>?'
        )) if use_special and use_upper and use_digits else len(set(''.join(
            c for c in 'abcdefghijklmnopqrstuvwxyz' +
            ('ABCDEFGHIJKLMNOPQRSTUVWXYZ' if use_upper else '') +
            ('0123456789' if use_digits else '') +
            ('!@#$%^&*()-_=+[]{}|;:,.<>?' if use_special else '')))))
        echo(f'   长度={length}, 熵≈{entropy:.1f} bits', fg='cyan')
    else:
        for idx, p in enumerate(passwords, 1):
            echo(f'  [{idx}] {p}', fg='green')

    if args.get('o'):
        with open(args['o'], 'w', encoding='utf-8') as f:
            f.write('\n'.join(passwords))


def cmd_uuid_gen(args):
    """生成 UUID"""
    count = int(args.get('n', 1))
    version = int(args.get('version', 4))  # 1(time-based), 4(random)
    no_dash = args.get('no_dash', False)
    upper = args.get('upper', False)

    results = []
    for _ in range(count):
        if version == 1:
            u = uuid_module.uuid1()
        elif version == 3:
            u = uuid_module.uuid3(uuid_module.NAMESPACE_DNS, str(_))
        elif version == 5:
            u = uuid_module.uuid5(uuid_module.NAMESPACE_DNS, str(_))
        else:
            u = uuid_module.uuid4()

        s = str(u)
        if no_dash:
            s = s.replace('-', '')
        if upper:
            s = s.upper()
        results.append(s)

    for r in results:
        echo(r, fg='cyan')

    if args.get('o'):
        with open(args['o'], 'w', encoding='utf-8') as f:
            f.write('\n'.join(results))
        echo(f'\n✅ 已写入 {count} 个 UUID → {args["o"]}', fg='green')


def cmd_hmac_calc(args):
    """计算 HMAC 签名"""
    key = args['_pos'][0] if len(args.get('_pos', [])) > 0 else ''
    message = args['_pos'][1] if len(args.get('_pos', [])) > 1 else ''
    algo = args.get('algo', 'sha256').lower()
    hex_output = args.get('hex', True)
    output = args.get('o', '')

    if not key:
        echo('⚠️ 用法: hmac <key> <message>', fg='yellow')
        return

    try:
        algo_const = getattr(hashlib, algo)
    except AttributeError:
        echo(f'❌ 不支持的算法: {algo}', fg='red')
        sys.exit(1)

    sig = hmac_lib.new(key.encode('utf-8'), message.encode('utf-8'), algo_const)

    if hex_output:
        result = sig.hexdigest()
    else:
        result = sig.digest()

    echo(f'HMAC-{algo.upper()} = {result if isinstance(result, str) else result.hex()}', fg='green')

    if output:
        mode = 'w' if hex_output else 'wb'
        content = result
        if not hex_output:
            content = sig.digest()
        with open(output, mode) as f:
            if isinstance(content, str):
                f.write(content)
            else:
                f.write(content)


def cmd_base64_encode(args):
    """Base64 编码"""
    target = args['_pos'][0] if args.get('_pos') else ''
    url_safe = args.get('url_safe', False)
    output = args.get('o', '')

    if os.path.isfile(target):
        with open(target, 'rb') as f:
            raw = f.read()
    else:
        raw = target.encode('utf-8')

    if url_safe:
        encoded = base64.urlsafe_b64encode(raw).decode('ascii')
        encoded = encoded.rstrip('=')
    else:
        encoded = base64.b64encode(raw).decode('ascii')

    print(encoded)

    if output:
        with open(output, 'w', encoding='utf-8') as f:
            f.write(encoded)
        echo(f'✅ 已写入: {output}', fg='green')


def cmd_base64_decode(args):
    """Base64 解码"""
    target = args['_pos'][0] if args.get('_pos') else ''
    url_safe = args.get('url_safe', False)
    output = args.get('o', '')

    # 补齐 padding
    padded = target
    if url_safe:
        padded += '=' * (-len(target) % 4)
        raw = base64.urlsafe_b64decode(padded)
    else:
        padded += '=' * (-len(target) % 4)
        raw = base64.b64decode(padded)

    # 尝试文本输出
    try:
        decoded = raw.decode('utf-8')
        print(decoded)
    except UnicodeDecodeError:
        print(f'(二进制数据, {len(raw)} bytes)')
        if output:
            with open(output, 'wb') as f:
                f.write(raw)
            echo(f'✅ 二进制已写入: {output}', fg='green')
        return

    if output:
        with open(output, 'wb') as f:
            f.write(raw)
        echo(f'✅ 已写入: {output}', fg='green')


def cmd_xor_crypt(args):
    """XOR 简单加密/解密（对称）"""
    plaintext = args['_pos'][0] if args.get('_pos') else ''
    key = args.get('key', '')
    input_file = args.get('input', '')
    output = args.get('o', '')

    if input_file:
        with open(input_file, 'rb') as f:
            data = bytearray(f.read())
    else:
        data = bytearray(plaintext.encode('utf-8'))

    if not key:
        echo('⚠️ 请提供 --key 参数', fg='yellow')
        return

    key_bytes = key.encode('utf-8')
    key_len = len(key_bytes)

    for i in range(len(data)):
        data[i] ^= key_bytes[i % key_len]

    result = bytes(data)
    try:
        decoded = result.decode('utf-8')
        echo(f'结果: {decoded}', fg='cyan')
    except UnicodeDecodeError:
        echo(f'结果: (二进制, {len(result)} bytes)', fg='cyan')

    if output:
        with open(output, 'wb') as f:
            f.write(result)
        echo(f'✅ 已写入: {output}', fg='green')


def cmd_checksum(args):
    """多算法校验和"""
    targets = args['_pos'] if args.get('_pos') else []
    compare = args.get('compare', '')

    from scripts.table_format import tabulate

    rows = []
    for target in targets:
        if not os.path.isfile(target):
            continue
        fi = {'文件': os.path.basename(target)}
        for algo_name in ['md5', 'sha1', 'sha256']:
            try:
                h = hashlib.new(algo_name)
                with open(target, 'rb') as f:
                    for chunk in iter(lambda: f.read(8192), b''):
                        h.update(chunk)
                fi[algo_name.upper()] = h.hexdigest()
            except Exception:
                fi[algo_name.upper()] = 'ERROR'
        rows.append(fi)

    if rows:
        print(tabulate(rows, tablefmt='grid'))

    # 对比模式
    if compare and rows:
        expected_hashes = {}
        if ':' in compare:
            for pair in compare.split(','):
                a, v = pair.strip().split(':', 1)
                expected_hashes[a.lower()] = v.strip()

        echo('\n🔍 校验对比:', fg='cyan')
        all_match = True
        for row in rows:
            fname = row['文件']
            for algo, expected in expected_hashes.items():
                actual = row.get(algo.upper(), '')
                match = actual == expected
                status = color('✅ 匹配', 'green') if match else color('❌ 不匹配!', 'red')
                echo(f'  {fname}: {algo.upper()} {status} '
                     f'(期望: {expected[:16]}... 实际: {actual[:16]}...)',
                     fg='green' if match else 'red')
                if not match:
                    all_match = False

        if all_match:
            echo('\n✅ 所有文件校验通过!', fg='green', bold=True)


def cmd_token_gen(args):
    """生成安全令牌/密钥"""
    nbytes = int(args.get('bytes', 32))
    count = int(args.get('count', 1))
    fmt = args.get('format', 'hex')  # hex, base64, urlsafe

    tokens = []
    for _ in range(count):
        raw = secrets.token_bytes(nbytes)
        if fmt == 'base64':
            t = base64.b64encode(raw).decode('ascii')
        elif fmt == 'urlsafe':
            t = base64.urlsafe_b64encode(raw).rstrip(b'=').decode('ascii')
        else:
            t = raw.hex()
        tokens.append(t)

    for t in tokens:
        echo(t, fg='green')

    bits = nbytes * 8
    echo(f'\n{bits}-bit 安全令牌 × {count} (格式={fmt})', fg='cyan')

    if args.get('o'):
        with open(args['o'], 'w', encoding='utf-8') as f:
            f.write('\n'.join(tokens))


def cmd_compare_files(args):
    """二进制/文本比较两个文件的差异"""
    file_a = args['_pos'][0] if len(args.get('_pos', [])) > 0 else ''
    file_b = args['_pos'][1] if len(args.get('_pos', [])) > 1 else ''

    if not file_a or not file_b:
        echo('用法: compare-files <fileA> <fileB>', fg='yellow')
        return

    for fp in [file_a, file_b]:
        if not os.path.isfile(fp):
            echo(f'❌ 文件不存在: {fp}', fg='red')
            sys.exit(1)

    size_a = os.path.getsize(file_a)
    size_b = os.path.getsize(file_b)

    echo(f'📊 文件比较:', fg='cyan', bold=True)
    echo(f'  A: {file_a} ({size_a} bytes)', fg='blue')
    echo(f'  B: {file_b} ({size_b} bytes)', fg='blue')

    # 快速路径：大小不同
    if size_a != size_b:
        echo(f'  ⚠️ 大小不同 ({abs(size_a-size_b)} bytes 差异)', fg='yellow')

    # 哈希比较
    for algo in ['md5', 'sha256']:
        ha, hb = hashlib.new(algo), hashlib.new(algo)
        with open(file_a, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''): ha.update(chunk)
        with open(file_b, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''): hb.update(chunk)
        da, db = ha.hexdigest(), hb.hexdigest()
        match = da == db
        icon = '✅' if match else '❌'
        echo(f'  {icon} {algo.upper()}: A={da[:16]}... B={db[:16]}...',
             fg='green' if match else 'red')

    # 内容差异定位
    with open(file_a, 'rb') as fa, open(file_b, 'rb') as fb:
        ba, bb = fa.read(), fb.read()
        if ba == bb:
            echo(f'\n✅ 文件完全相同!', fg='green', bold=True)
        else:
            # 找到第一个差异位置
            diff_pos = 0
            min_len = min(len(ba), len(bb))
            while diff_pos < min_len and ba[diff_pos] == bb[diff_pos]:
                diff_pos += 1
            echo(f'\n📍 第一个差异位置: offset=0x{diff_pos:X} (十进制 {diff_pos})', fg='yellow')
            if diff_pos < min_len:
                ctx_start = max(0, diff_pos - 16)
                ctx_end = min(len(ba), diff_pos + 16)
                echo(f'A[{diff_pos}]: 0x{ba[diff_pos]:02X} ({chr(ba[diff_pos]) if 32<=ba[diff_pos]<127 else "."})',
                     fg='blue')
                echo(f'B[{diff_pos}]: 0x{bb[diff_pos]:02X} ({chr(bb[diff_pos]) if 32<=bb[diff_pos]<127 else "."})',
                     fg='red')
            echo(f'总差异字节数: {sum(a!=b for a,b in zip(ba,bb)) + abs(len(ba)-len(bb))}')


# ══════════════════════════════════════════════════════════════
#  主入口
# ══════════════════════════════════════════════════════════════

COMMANDS = {
    'hash': cmd_hash,
    'password': cmd_password,
    'pwd': cmd_password,
    'uuid': cmd_uuid_gen,
    'hmac': cmd_hmac_calc,
    'base64-encode': cmd_base64_encode,
    'base64-decode': cmd_base64_decode,
    'xor-crypt': cmd_xor_crypt,
    'checksum': cmd_checksum,
    'token': cmd_token_gen,
    'compare-files': cmd_compare_files,
}

ALIASES = {
    'sum': 'hash', 'digest': 'hash', 'md5': lambda a: (a.__setitem__('algo', 'md5'), cmd_hash(a))[1],
    'sha256': lambda a: (a.__setitem__('algo', 'sha256'), cmd_hash(a))[1],
    'gen-password': 'password', 'randpass': 'password', 'generate-pwd': 'password',
    'guid': 'uuid', 'unique-id': 'uuid',
    'sign': 'hmac',
    'b64e': 'base64-encode', 'b64d': 'base64-decode',
    'xor': 'xor-crypt', 'obfuscate': 'xor-crypt',
    'verify': 'checksum', 'check-hash': 'checksum',
    'generate-token': 'token', 'api-key': 'token', 'secret': 'token',
    'diff': 'compare-files', 'cmp': 'compare-files',
}


def main():
    args = parse_args()
    cmd = args['_cmd']
    cmd = ALIASES.get(cmd, cmd)

    if cmd not in COMMANDS:
        available = ', '.join(sorted(set(list(COMMANDS.keys()) + [k for k, v in ALIASES.items() if k in COMMANDS])))
        echo(f'❌ 未知命令: {cmd}', fg='red')
        echo(f'可用命令: {available}', fg='cyan')
        sys.exit(1)

    COMMANDS[cmd](args)


if __name__ == '__main__':
    main()
