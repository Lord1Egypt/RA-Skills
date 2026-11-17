# -*- coding: utf-8 -*-
"""扣子智能体一键部署与发布 (main.py)
用法:
  python3 main.py full --name "名称" --prompt-file ./prompt_v21.txt --kb-dir ./kb_txt --connector 1024
  python3 main.py create-kb --name "知识库名"
  python3 main.py upload-docs --dataset-id <id> --kb-dir <dir>
  python3 main.py create-bot --name "名称" --prompt-file <file>
  python3 main.py bind-kb --bot-id <id> --dataset-id <id>
  python3 main.py publish --bot-id <id> --connector 1024
"""
import os, sys, json, time, argparse

# 凭证读取：扣子开放 API Token（skill_draft_credential 配置后自动注入）
API_TOKEN = os.getenv("COZE_COZE_API_7673888213613690895") or os.getenv("COZE_API_TOKEN")
if not API_TOKEN:
    raise SystemExit("缺少扣子开放 API Token 凭证，请先配置 skill_draft_credential")

BASE = "https://api.coze.cn"
HDRS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
    "Agw-Js-Conv": "str",   # 防数字精度丢失，缺失会 400
}

try:
    from coze_workload_identity import requests  # 扣子沙箱：走安全代理通道
except ImportError:
    import requests  # 外部环境（ClawHub/GitHub 等）：降级标准库


def _call(method, path, payload=None, timeout=60):
    url = BASE + path
    r = requests.request(method, url, headers=HDRS,
                         data=json.dumps(payload).encode() if payload is not None else None,
                         timeout=timeout)
    try:
        data = r.json()
    except Exception:
        raise Exception(f"非JSON响应 {r.status_code}: {r.text[:500]}")
    if r.status_code >= 400 or (isinstance(data, dict) and data.get("code") not in (0, None)):
        raise Exception(f"API错误 {path}: {data}")
    return data


def create_kb(name, desc=""):
    """创建知识库，返回 dataset_id"""
    data = _call("POST", "/v1/datasets", {
        "name": name, "description": desc,
        "space_id": os.environ.get("COZE_SPACE_ID", ""),
    })
    did = data.get("data", {}).get("dataset_id") or data.get("dataset_id")
    print(f"[create-kb] dataset_id={did}")
    return did


def upload_docs(dataset_id, kb_dir):
    """遍历目录上传 .md/.txt 文档（file_base64 须放 source_info 内并带 file_type），返回成功列表"""
    import base64
    ok, fail = [], []
    files = [fn for fn in sorted(os.listdir(kb_dir)) if fn.endswith((".md", ".txt"))]
    # 每次最多 10 个文件，分批；限流时重试
    for i in range(0, len(files), 5):
        batch = files[i:i+5]
        doc_bases = []
        for fn in batch:
            path = os.path.join(kb_dir, fn)
            with open(path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            ftype = fn.rsplit(".", 1)[-1]
            doc_bases.append({
                "name": fn,
                "source_info": {"file_base64": b64, "file_type": ftype},
            })
        for attempt in range(3):
            try:
                data = _call("POST", "/open_api/knowledge/document/create", {
                    "dataset_id": dataset_id,
                    "format_type": 0,
                    "document_bases": doc_bases,
                    "chunk_strategy": {
                        "separator": "\n\n", "max_tokens": 800,
                        "remove_extra_spaces": False, "remove_urls_emails": False,
                        "chunk_type": 1,
                    },
                }, timeout=120)
                ok.extend([d["name"] for d in data.get("document_infos", [])])
                for d in data.get("document_infos", []):
                    print(f"[upload] {d['name']} OK (status={d.get('status')})")
                break
            except Exception as e:
                print(f"[upload] 批次{i//5+1} 第{attempt+1}次失败: {e}", flush=True)
                if "limit" in str(e).lower() or "710005002" in str(e):
                    time.sleep(5 + attempt * 5)
                    continue
                fail.extend([d["name"] for d in doc_bases])
                break
        else:
            fail.extend([d["name"] for d in doc_bases])
    return ok, fail


def create_bot(name, prompt_file):
    """创建智能体，配置系统提示词+开场白+预置问题，返回 bot_id"""
    with open(prompt_file, "r", encoding="utf-8") as f:
        prompt = f.read()
    data = _call("POST", "/v1/bot/create", {
        "space_id": os.environ.get("COZE_SPACE_ID", ""),
        "name": name,
        "prompt_info": {"prompt": prompt},
        "onboarding_info": {
            "prologue": "您好，我是您的 AI 客服机器人方案设计助手，输入您的行业和需求，我来帮您生成《功能设计清单》。",
            "suggested_questions": [
                "帮我设计一个女装店客服机器人",
                "医美机构客服怎么设计话术",
                "跨境电商客户总问物流多久到",
                "帮我写一段报价话术",
            ],
        },
    })
    bot = data.get("data", {})
    bot_id = bot.get("bot_id") or data.get("bot_id")
    print(f"[create-bot] bot_id={bot_id}")
    return bot_id


def bind_kb(bot_id, dataset_id):
    """绑定知识库 + auto_call"""
    data = _call("POST", "/v1/bot/update", {
        "bot_id": bot_id,
        "knowledge": {
            "dataset_ids": [dataset_id],
            "auto_call": True,
            "search_strategy": 0,
        },
    })
    print(f"[bind-kb] {dataset_id} -> {bot_id} OK")
    return data


def publish(bot_id, connector="1024"):
    """发布为 API 服务"""
    data = _call("POST", "/v1/bot/publish", {
        "bot_id": bot_id,
        "connector_ids": [connector],
    })
    version = data.get("data", {}).get("version") or data.get("version")
    print(f"[publish] version={version} (connector={connector})")
    return version


def full(name, prompt_file, kb_dir, connector="1024", bot_id=None, dataset_id=None):
    """一键完整链路"""
    print("==> 1/5 创建/复用知识库")
    if not dataset_id:
        dataset_id = create_kb(name + "-知识库")
    print("==> 2/5 上传行业文档")
    ok, fail = upload_docs(dataset_id, kb_dir)
    if fail:
        print(f"   警告: {len(fail)} 个文档上传失败: {fail}")
    print("==> 3/5 创建/复用智能体")
    if not bot_id:
        bot_id = create_bot(name, prompt_file)
    print("==> 4/5 绑定知识库")
    bind_kb(bot_id, dataset_id)
    print("==> 5/5 发布为 API 服务")
    version = publish(bot_id, connector)
    print("\n部署完成:")
    print(f"  bot_id={bot_id}")
    print(f"  dataset_id={dataset_id}")
    print(f"  version={version}")
    print("  (发布后约 30-60 秒生效，随后可跑 run_all_tests.py 回归)")
    return {"bot_id": bot_id, "dataset_id": dataset_id, "version": version}


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="扣子智能体一键部署与发布")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("full")
    p.add_argument("--name", required=True)
    p.add_argument("--prompt-file", required=True)
    p.add_argument("--kb-dir", required=True)
    p.add_argument("--connector", default="1024")
    p.add_argument("--bot-id", default=None)
    p.add_argument("--dataset-id", default=None)

    p = sub.add_parser("create-kb")
    p.add_argument("--name", required=True)

    p = sub.add_parser("upload-docs")
    p.add_argument("--dataset-id", required=True)
    p.add_argument("--kb-dir", required=True)

    p = sub.add_parser("create-bot")
    p.add_argument("--name", required=True)
    p.add_argument("--prompt-file", required=True)

    p = sub.add_parser("bind-kb")
    p.add_argument("--bot-id", required=True)
    p.add_argument("--dataset-id", required=True)

    p = sub.add_parser("publish")
    p.add_argument("--bot-id", required=True)
    p.add_argument("--connector", default="1024")

    a = ap.parse_args()
    if a.cmd == "full":
        full(a.name, a.prompt_file, a.kb_dir, a.connector, a.bot_id, a.dataset_id)
    elif a.cmd == "create-kb":
        create_kb(a.name)
    elif a.cmd == "upload-docs":
        upload_docs(a.dataset_id, a.kb_dir)
    elif a.cmd == "create-bot":
        create_bot(a.name, a.prompt_file)
    elif a.cmd == "bind-kb":
        bind_kb(a.bot_id, a.dataset_id)
    elif a.cmd == "publish":
        publish(a.bot_id, a.connector)
