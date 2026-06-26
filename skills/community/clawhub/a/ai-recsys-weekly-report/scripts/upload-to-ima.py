#!/usr/bin/env python3
"""
IMA 知识库上传脚本 - 标准三步流程
  Step 1: create_media -> 获取 media_id + COS 凭证
  Step 2: cos-upload.cjs -> 上传文件到 COS
  Step 3: add_knowledge -> 关联到知识库

用法:
  python3 upload-to-ima.py --file <报告路径> --kb-id <知识库ID> [--title <标题>]

依赖:
  - ima-skills 的 cos-upload.cjs 脚本
  - Node.js (用于运行 cos-upload.cjs)
  - IMA 凭证文件: ~/.config/ima/client_id, ~/.config/ima/api_key

注意:
  - COS 上传失败时立即终止，不执行 add_knowledge
  - Node 路径需要根据实际环境配置 (见下方 NODE_PATH)
"""

import argparse
import json
import os
import subprocess
import sys
import urllib.request

# ============== 配置区（目标账号需修改） ==============
# cos-upload.cjs 脚本路径（相对于本脚本所在目录）
COS_UPLOAD_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  "..", "..", "ima笔记", "knowledge-base", "scripts", "cos-upload.cjs")

# Node.js 路径 — 请根据目标环境修改
NODE_PATH = os.path.expanduser("~/.workbuddy/binaries/node/versions/22.12.0/bin/node")
# 备选: /usr/local/bin/node 或 which node 的结果


def load_credentials():
    """从配置文件读取 IMA 凭证"""
    client_id_path = os.path.expanduser("~/.config/ima/client_id")
    api_key_path = os.path.expanduser("~/.config/ima/api_key")
    if not os.path.exists(client_id_path) or not os.path.exists(api_key_path):
        print("ERROR: 缺少 IMA 凭证。请先运行:")
        print("  mkdir -p ~/.config/ima")
        print('  echo "your_client_id" > ~/.config/ima/client_id')
        print('  echo "your_api_key" > ~/.config/ima/api_key')
        sys.exit(1)
    with open(client_id_path) as f:
        client_id = f.read().strip()
    with open(api_key_path) as f:
        api_key = f.read().strip()
    if not client_id or not api_key:
        print("ERROR: 凭证文件为空")
        sys.exit(1)
    return client_id, api_key


def ima_api(client_id, api_key, path, body):
    """调用 IMA OpenAPI"""
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        f"https://ima.qq.com/{path}",
        data=data,
        headers={
            "ima-openapi-clientid": client_id,
            "ima-openapi-apikey": api_key,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def find_node():
    """查找可用的 Node.js 路径"""
    # 优先使用配置的路径
    if os.path.exists(NODE_PATH):
        return NODE_PATH
    # 回退到系统 PATH
    for candidate in ["/usr/local/bin/node", "/opt/homebrew/bin/node", "node"]:
        try:
            r = subprocess.run([candidate, "--version"], capture_output=True, timeout=5)
            if r.returncode == 0:
                return candidate
        except Exception:
            continue
    print(f"ERROR: 找不到 Node.js。请修改脚本中的 NODE_PATH 配置。当前: {NODE_PATH}")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="上传 Markdown 报告到 IMA 知识库")
    parser.add_argument("--file", required=True, help="要上传的 Markdown 文件路径")
    parser.add_argument("--kb-id", required=True, help="目标知识库 ID")
    parser.add_argument("--title", default=None, help="自定义标题（默认使用文件名）")
    args = parser.parse_args()

    file_path = os.path.abspath(args.file)
    if not os.path.exists(file_path):
        print(f"ERROR: 文件不存在: {file_path}")
        sys.exit(1)

    file_name = args.title or os.path.basename(file_path)
    file_ext = file_path.rsplit(".", 1)[-1] if "." in file_path else "md"
    file_size = os.path.getsize(file_path)

    # 文件类型映射
    ext_map = {
        "md": (7, "text/markdown"),
        "pdf": (1, "application/pdf"),
        "docx": (3, "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
        "txt": (13, "text/plain"),
    }
    media_type, content_type = ext_map.get(file_ext, (7, "text/markdown"))

    kb_id = args.kb_id.strip()
    client_id, api_key = load_credentials()
    node_bin = find_node()

    # 检查 cos-upload.cjs 是否存在
    cos_script = os.path.abspath(COS_UPLOAD_SCRIPT)
    if not os.path.exists(cos_script):
        # 尝试 skill 内置相对路径
        alt_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cos-upload-wrapper.cjs")
        if os.path.exists(alt_script):
            cos_script = alt_script
        else:
            print(f"ERROR: 找不到 cos-upload.cjs 脚本")
            print(f"  查找路径1: {os.path.abspath(COS_UPLOAD_SCRIPT)}")
            print(f"  查找路径2: {alt_script}")
            print(f"  请确保已安装 ima-skills skill")
            sys.exit(1)

    print(f"文件: {file_name} ({file_size} bytes)")
    print(f"类型: media_type={media_type}, content_type={content_type}")
    print(f"Node: {node_bin}")

    # === Step 1: create_media ===
    print("\n[Step 1] 创建媒体...")
    try:
        result = ima_api(client_id, api_key, "openapi/wiki/v1/create_media", {
            "file_name": file_name,
            "file_size": file_size,
            "content_type": content_type,
            "knowledge_base_id": kb_id,
            "file_ext": file_ext,
        })
    except Exception as e:
        print(f"FAIL: create_media API 调用异常: {e}")
        sys.exit(1)

    if result.get("code") != 0:
        print(f"FAIL: create_media 返回错误: {result.get('msg', result)}")
        sys.exit(1)

    media_id = result["data"]["media_id"]
    cos_cred = result["data"]["cos_credential"]
    print(f"OK media_id={media_id}")

    # === Step 2: COS Upload ===
    print("\n[Step 2] 上传 COS (cos-upload.cjs)...")
    upload_args = [
        node_bin, cos_script,
        "--file", file_path,
        "--secret-id", cos_cred["secret_id"],
        "--secret-key", cos_cred["secret_key"],
        "--token", cos_cred["token"],
        "--bucket", cos_cred["bucket_name"],
        "--region", cos_cred["region"],
        "--cos-key", cos_cred["cos_key"],
        "--content-type", content_type,
        "--start-time", str(cos_cred["start_time"]),
        "--expired-time", str(cos_cred["expired_time"]),
    ]

    try:
        r = subprocess.run(upload_args, capture_output=True, text=True, timeout=120)
        stdout = r.stdout.strip() if r.stdout else ""
        stderr = r.stderr.strip()[:300] if r.stderr else ""
        if stdout:
            print(f"输出: {stdout}")
        if stderr:
            print(f"日志: {stderr}")

        if r.returncode != 0:
            print(f"\nFAIL: COS 上传失败 (exit code={r.returncode})，终止流程")
            print("提示: COS 文件未成功写入，不要继续 add_knowledge")
            sys.exit(1)
    except subprocess.TimeoutExpired:
        print("FAIL: COS 上传超时 (>120s)")
        sys.exit(1)
    except Exception as e:
        print(f"FAIL: COS 上传异常: {e}")
        sys.exit(1)

    print("OK COS 上传成功")

    # === Step 3: add_knowledge ===
    print("\n[Step 3] 添加到知识库...")
    try:
        add_result = ima_api(client_id, api_key, "openapi/wiki/v1/add_knowledge", {
            "media_type": media_type,
            "media_id": media_id,
            "title": file_name,
            "knowledge_base_id": kb_id,
            "file_info": {
                "cos_key": cos_cred["cos_key"],
                "file_size": file_size,
                "file_name": file_name,
            },
        })
    except Exception as e:
        print(f"FAIL: add_knowledge API 异常: {e}")
        sys.exit(1)

    print(json.dumps(add_result, indent=2, ensure_ascii=False))

    if add_result.get("code") == 0:
        print("\n=== 全部成功！请刷新 IMA 知识库查看文件 ===")
    else:
        print(f"\nFAIL: add_knowledge 错误: {add_result.get('msg')}")


if __name__ == "__main__":
    main()
