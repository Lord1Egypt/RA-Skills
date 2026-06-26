#!/usr/bin/env python3
"""百度网盘文件上传 — 统一分片上传，支持断点续传和进度监控

Usage:
  upload.py <local_file> <remote_dir> <env_path> [--overwrite]

  local_file  : 本地文件路径
  remote_dir  : 网盘远程目录（如 /docker镜像）
  env_path    : .env文件路径（含AccessToken等）
  --overwrite : 覆盖已存在的文件（默认报错）

上传流程（所有文件统一）：
  precreate → superfile2(tmpfile) × N → create
  文件 ≤4MB 时仅1片，>4MB时自动分片（每片4MB）

断点续传：
  上传状态保存在本地 .upload_state.json（与源文件同目录）
  中断后重新执行同一文件上传时，自动检测已上传分片并跳过
  上传完成后自动删除状态文件
"""
import sys, os, json, math, hashlib, urllib.request, urllib.parse, urllib.error, time, subprocess, tempfile

CHUNK_SIZE = 4 * 1024 * 1024  # 4MB per slice
STATE_FILENAME = '.upload_state.json'  # saved alongside the source file


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


def md5_of_file(filepath, chunk_size=8192):
    """计算文件MD5"""
    h = hashlib.md5()
    with open(filepath, 'rb') as f:
        while True:
            data = f.read(chunk_size)
            if not data:
                break
            h.update(data)
    return h.hexdigest()


def md5_of_bytes(data):
    """计算bytes的MD5"""
    return hashlib.md5(data).hexdigest()


# ─── Progress display ───────────────────────────────────────────────────

def format_size(nbytes):
    """格式化文件大小"""
    if nbytes >= 1024**3:
        return f"{nbytes/1024**3:.2f}GB"
    elif nbytes >= 1024**2:
        return f"{nbytes/1024**2:.1f}MB"
    elif nbytes >= 1024:
        return f"{nbytes/1024:.1f}KB"
    return f"{nbytes}B"


def format_duration(seconds):
    """格式化时间"""
    if seconds < 60:
        return f"{seconds:.0f}s"
    elif seconds < 3600:
        return f"{seconds//60:.0f}m{seconds%60:.0f}s"
    return f"{seconds//3600:.0f}h{(seconds%3600)//60:.0f}m"


def print_progress(done_chunks, total_chunks, done_bytes, total_bytes, elapsed):
    """打印进度条"""
    pct = done_chunks / total_chunks if total_chunks else 1.0
    bar_len = 20
    filled = int(bar_len * pct)
    bar = '█' * filled + '░' * (bar_len - filled)

    speed = done_bytes / elapsed if elapsed > 0 else 0
    remaining_bytes = total_bytes - done_bytes
    eta = remaining_bytes / speed if speed > 0 else 0

    sys.stdout.write(
        f"\r  [{bar}] {pct*100:5.1f}% | "
        f"{format_size(done_bytes)}/{format_size(total_bytes)} | "
        f"{format_size(speed)}/s | "
        f"ETA {format_duration(eta)}"
    )
    sys.stdout.flush()
    if done_chunks == total_chunks:
        print()  # newline at completion


# ─── State management for resume ─────────────────────────────────────────

def state_path(local_file):
    """状态文件路径（与源文件同目录）"""
    return os.path.join(os.path.dirname(os.path.abspath(local_file)), STATE_FILENAME)


def save_state(local_file, remote_path, upload_id, total_chunks, block_list, done_chunks):
    """保存上传状态"""
    state = {
        'local_file': os.path.abspath(local_file),
        'file_size': os.path.getsize(local_file),
        'file_md5': md5_of_file(local_file),
        'remote_path': remote_path,
        'upload_id': upload_id,
        'total_chunks': total_chunks,
        'block_list': block_list,
        'done_chunks': sorted(done_chunks),
        'timestamp': time.time(),
    }
    with open(state_path(local_file), 'w') as f:
        json.dump(state, f, ensure_ascii=False)


def load_state(local_file, remote_path):
    """加载上传状态，返回 (upload_id, done_chunks, block_list) 或 None"""
    sp = state_path(local_file)
    if not os.path.exists(sp):
        return None
    try:
        with open(sp) as f:
            state = json.load(f)
        # Validate: same file, same remote path
        if (state.get('local_file') != os.path.abspath(local_file) or
                state.get('remote_path') != remote_path):
            return None
        # Validate: file hasn't changed
        if state.get('file_size') != os.path.getsize(local_file):
            return None
        if state.get('file_md5') != md5_of_file(local_file):
            return None
        return state
    except (json.JSONDecodeError, KeyError, OSError):
        return None


def clear_state(local_file):
    """删除上传状态文件"""
    sp = state_path(local_file)
    try:
        os.unlink(sp)
    except OSError:
        pass


# ─── Baidu Pan API helpers ───────────────────────────────────────────────

def api_get(url, token, params=None):
    """GET请求百度网盘API"""
    if params is None:
        params = {}
    params['access_token'] = token
    full_url = f"{url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(full_url, headers={'User-Agent': 'pan.baidu.com'})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.URLError as e:
        print(f"\nERROR: API请求失败 - {e}", file=sys.stderr)
        sys.exit(1)


def api_post(url, token, params=None, data=None):
    """POST请求（form-encoded）百度网盘API"""
    if params is None:
        params = {}
    params['access_token'] = token
    full_url = f"{url}?{urllib.parse.urlencode(params)}"

    if data:
        encoded_parts = []
        for k, v in data.items():
            encoded_parts.append(
                f"{urllib.parse.quote(str(k), safe='')}={urllib.parse.quote(str(v), safe='')}"
            )
        body = '&'.join(encoded_parts).encode('utf-8')
    else:
        body = b''

    req = urllib.request.Request(full_url, data=body, method='POST',
                                headers={'User-Agent': 'pan.baidu.com',
                                         'Content-Type': 'application/x-www-form-urlencoded'})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.URLError as e:
        print(f"\nERROR: API请求失败 - {e}", file=sys.stderr)
        sys.exit(1)


def curl_upload_slice(token, remote_path, upload_id, partseq, chunk_filepath):
    """用curl上传单个分片（百度网盘superfile2接口要求multipart/form-data）"""
    url = 'https://d.pcs.baidu.com/rest/2.0/pcs/superfile2'
    params = {
        'method': 'upload',
        'access_token': token,
        'path': remote_path,
        'type': 'tmpfile',
        'uploadid': upload_id,
        'partseq': str(partseq),
    }
    full_url = f"{url}?{urllib.parse.urlencode(params)}"

    for attempt in range(3):
        try:
            result = subprocess.run(
                ['curl', '-s', '-X', 'POST', full_url,
                 '-H', 'User-Agent: pan.baidu.com',
                 '-F', f'file=@{chunk_filepath}',
                 '--connect-timeout', '15', '--max-time', '120'],
                capture_output=True, text=True, timeout=130)
            if result.returncode != 0:
                raise RuntimeError(f"curl退出码{result.returncode}: {result.stderr}")
            data = json.loads(result.stdout)
            if 'error_code' in data:
                raise RuntimeError(f"API错误 {data.get('error_code')}: {data.get('error_msg')}")
            return data
        except Exception as e:
            if attempt < 2:
                print(f"\n    分片{partseq}上传失败（重试 {attempt+1}/3）: {e}")
                time.sleep(2)
            else:
                print(f"\nERROR: 分片{partseq}上传3次均失败 - {e}", file=sys.stderr)
                sys.exit(1)


def ensure_remote_dir(token, remote_dir):
    """确保远程目录存在，不存在则创建"""
    result = api_get('https://pan.baidu.com/rest/2.0/xpan/file', token,
                     {'method': 'list', 'dir': remote_dir, 'folder': 1})
    if result.get('errno', -1) == 0:
        return  # dir exists
    # Try to create
    result = api_post('https://pan.baidu.com/rest/2.0/xpan/file', token,
                      {'method': 'create'},
                      {'path': remote_dir, 'isdir': '1', 'size': '0'})
    if result.get('errno', -1) != 0:
        err_msg = result.get('errmsg', json.dumps(result, ensure_ascii=False))
        print(f"WARNING: 创建目录可能失败 - {err_msg}", file=sys.stderr)


def precreate_file(token, remote_path, file_size, block_list, overwrite=False):
    """precreate步骤：初始化上传，返回 uploadid 和已上传分片信息"""
    data = {
        'path': remote_path,
        'size': str(file_size),
        'isdir': '0',
        'autoinit': '1',
        'block_list': json.dumps(block_list),
        'content_md5': md5_of_file(remote_path),  # placeholder, will be overridden
    }
    if overwrite:
        data['ondup'] = 'overwrite'

    # Calculate actual file md5 from the source — but we don't have the file path here
    # So we skip content_md5 (it's optional for precreate)
    del data['content_md5']

    result = api_post('https://pan.baidu.com/rest/2.0/xpan/file', token,
                      {'method': 'precreate'}, data)

    if result.get('errno', -1) != 0 and 'return_type' not in result:
        err_msg = result.get('errmsg', json.dumps(result, ensure_ascii=False))
        print(f"ERROR: precreate失败 - {err_msg}", file=sys.stderr)
        sys.exit(1)

    upload_id = result.get('uploadid')
    if not upload_id:
        print(f"ERROR: precreate未返回uploadid - {json.dumps(result, ensure_ascii=False)}", file=sys.stderr)
        sys.exit(1)

    # return_type=1 means the file already has some blocks uploaded
    # block_list in response shows which blocks are already on server
    server_block_list = result.get('block_list', [])

    return upload_id, server_block_list


def create_file(token, remote_path, file_size, block_list, upload_id):
    """create步骤：合并所有分片，完成上传"""
    result = api_post('https://pan.baidu.com/rest/2.0/xpan/file', token,
                      {'method': 'create'},
                      {'path': remote_path,
                       'size': str(file_size),
                       'isdir': '0',
                       'block_list': json.dumps(block_list),
                       'uploadid': upload_id})

    if result.get('errno', -1) != 0 and 'fs_id' not in result:
        err_msg = result.get('errmsg', json.dumps(result, ensure_ascii=False))
        print(f"ERROR: create合并失败 - {err_msg}", file=sys.stderr)
        sys.exit(1)

    return result


# ─── Main upload logic ──────────────────────────────────────────────────

def upload_file(local_file, remote_dir, env_path, overwrite=False):
    """上传文件到百度网盘（统一分片流程，支持断点续传）"""
    if not os.path.isfile(local_file):
        print(f"ERROR: 文件不存在 - {local_file}", file=sys.stderr)
        sys.exit(1)

    cfg = load_env(env_path)
    token = cfg.get('AccessToken', '')
    if not token:
        print("ERROR: .env中无AccessToken，请先授权", file=sys.stderr)
        sys.exit(1)

    file_size = os.path.getsize(local_file)
    filename = os.path.basename(local_file)
    remote_path = remote_dir.rstrip('/') + '/' + filename
    if not remote_path.startswith('/'):
        remote_path = '/' + remote_path

    total_chunks = math.ceil(file_size / CHUNK_SIZE) if file_size > 0 else 1

    print(f"📤 上传: {filename}")
    print(f"   本地: {local_file}")
    print(f"   远程: {remote_path}")
    print(f"   大小: {format_size(file_size)} ({total_chunks} 片)")

    ensure_remote_dir(token, remote_dir)

    # ─── Calculate block MD5s ────────────────────────────────────────
    print("  计算分片MD5...", end=' ')
    block_list = []
    with open(local_file, 'rb') as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            block_list.append(md5_of_bytes(chunk))
    print(f"完成 ({len(block_list)} 片)")

    # ─── Resume check ────────────────────────────────────────────────
    saved = load_state(local_file, remote_path)
    upload_id = None
    done_chunks = set()
    start_chunk = 0

    if saved and saved.get('upload_id') and saved.get('block_list') == block_list:
        upload_id = saved['upload_id']
        done_chunks = set(saved.get('done_chunks', []))
        if done_chunks:
            print(f"  🔄 断点续传: 已有 {len(done_chunks)}/{total_chunks} 片, 从第 {min(c for c in range(total_chunks) if c not in done_chunks)+1} 片继续")
            # Re-precreate to refresh uploadid and get server-side block status
            upload_id, server_blocks = precreate_file(token, remote_path, file_size, block_list, overwrite)
            # Server blocks override our local state (server is source of truth)
            if server_blocks:
                done_chunks = set(server_blocks)
                print(f"  服务端确认已上传: {len(done_chunks)} 片")
            start_chunk = 0  # we'll skip via done_chunks check

    # ─── Precreate (if not resuming) ─────────────────────────────────
    if upload_id is None:
        upload_id, server_blocks = precreate_file(token, remote_path, file_size, block_list, overwrite)
        if server_blocks:
            done_chunks = set(server_blocks)
            print(f"  服务端已有 {len(done_chunks)} 片")

    print(f"  uploadid: {upload_id[:20]}...")

    # ─── Upload slices ───────────────────────────────────────────────
    tmp_dir = tempfile.mkdtemp(prefix='baidu_upload_')
    start_time = time.time()
    done_bytes = done_chunks.__len__() * CHUNK_SIZE
    # Adjust done_bytes for last chunk
    if (total_chunks - 1) in done_chunks:
        last_chunk_size = file_size - (total_chunks - 1) * CHUNK_SIZE
        done_bytes = done_bytes - CHUNK_SIZE + last_chunk_size

    try:
        with open(local_file, 'rb') as f:
            for idx in range(total_chunks):
                # Skip already uploaded chunks
                if idx in done_chunks:
                    continue

                chunk_data = f.read(CHUNK_SIZE)
                chunk_path = os.path.join(tmp_dir, f'chunk_{idx}')
                with open(chunk_path, 'wb') as cf:
                    cf.write(chunk_data)

                curl_upload_slice(token, remote_path, upload_id, idx, chunk_path)
                os.unlink(chunk_path)

                done_chunks.add(idx)

                # Calculate progress
                elapsed = time.time() - start_time
                # Recalculate done_bytes precisely
                done_bytes = 0
                for c in done_chunks:
                    if c == total_chunks - 1:
                        done_bytes += file_size - c * CHUNK_SIZE
                    else:
                        done_bytes += CHUNK_SIZE

                print_progress(len(done_chunks), total_chunks, done_bytes, file_size, elapsed)

                # Save state every 10 chunks (or every chunk if total < 50)
                save_interval = 10 if total_chunks >= 50 else 1
                if len(done_chunks) % save_interval == 0 or len(done_chunks) == total_chunks:
                    save_state(local_file, remote_path, upload_id, total_chunks, block_list, list(done_chunks))

    except KeyboardInterrupt:
        # Save state on Ctrl+C so we can resume
        save_state(local_file, remote_path, upload_id, total_chunks, block_list, list(done_chunks))
        elapsed = time.time() - start_time
        print(f"\n\n⏸ 上传中断！已保存进度 ({len(done_chunks)}/{total_chunks} 片)")
        print(f"   重新运行相同命令即可断点续传")
        print(f"   状态文件: {state_path(local_file)}")
        sys.exit(2)
    finally:
        try:
            os.rmdir(tmp_dir)
        except OSError:
            pass

    # ─── Create (merge) ──────────────────────────────────────────────
    print("  合并分片...", end=' ')
    result = create_file(token, remote_path, file_size, block_list, upload_id)
    print("完成")

    # ─── Clean up state ──────────────────────────────────────────────
    clear_state(local_file)

    fs_id = result.get('fs_id', 'N/A')
    md5 = result.get('md5', 'N/A')
    server_filename = result.get('server_filename', filename)
    elapsed = time.time() - start_time
    avg_speed = file_size / elapsed if elapsed > 0 else 0

    print(f"\n✅ 上传成功！")
    print(f"   文件: {server_filename}")
    print(f"   fs_id: {fs_id}")
    print(f"   MD5: {md5}")
    print(f"   耗时: {format_duration(elapsed)}")
    print(f"   平均速度: {format_size(avg_speed)}/s")


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage:")
        print("  upload.py <local_file> <remote_dir> <env_path> [--overwrite]")
        print()
        print("断点续传: 中断后重新运行相同命令即可自动续传")
        sys.exit(1)

    local_file = sys.argv[1]
    remote_dir = sys.argv[2]
    env_path = sys.argv[3]
    overwrite = '--overwrite' in sys.argv

    upload_file(local_file, remote_dir, env_path, overwrite)
