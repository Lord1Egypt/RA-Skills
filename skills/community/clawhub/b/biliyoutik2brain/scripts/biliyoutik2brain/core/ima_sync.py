"""
ima_sync.py — biliyoutik2brain × IMA 知识库双向同步 (v1.11.0)

上行：每次 auto_archive 完成后，将知识条目上传到 IMA 知识库
下行：每次 enhance 前，搜索 IMA 知识库中已有知识，提供上下文
"""

import os
import json
import re
import subprocess
import tempfile
import time
from typing import Dict, List, Optional, Tuple

IMA_API = os.path.expanduser("~/.workbuddy/skills/skill_2053082144792322048/ima_api.cjs")
COS_UPLOAD = os.path.expanduser("~/.workbuddy/skills/skill_2053082144792322048/knowledge-base/scripts/cos-upload.cjs")
PREFLIGHT = os.path.expanduser("~/.workbuddy/skills/skill_2053082144792322048/knowledge-base/scripts/preflight-check.cjs")

# 知识库 ID（CHOI8467的知识库）
KB_ID = "o-DMUKfAhG4GnQtpTLoZFwtQgiY7hNreKSGWEWPRUNE="

# 文件夹 ID — biliyoutik2brain 知识存到「JVSClaw的Wiki」文件夹下
FOLDER_ID = "folder_7467960956364811"  # JVSClaw的Wiki

# IMA 知识库内 biliyoutik2brain 文件夹名
BILI_KNOWLEDGE_FOLDER = "biliyoutik2brain"

# ── 工具函数 ──

def _ima_api(api_path: str, body: dict) -> dict:
    """调用 IMA OpenAPI"""
    body_json = json.dumps(body, ensure_ascii=False)
    result = subprocess.run(
        ["node", IMA_API, api_path, body_json, "{}"],
        capture_output=True, text=True, timeout=30,
    )
    if result.returncode != 0:
        print(f"  [IMA] ❌ API调用失败: {result.stderr[:200]}")
        return {"code": -1, "msg": result.stderr}
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"code": -1, "msg": result.stdout[:200]}


def _find_bili_folder() -> Optional[str]:
    """在知识库根目录中查找 biliyoutik2brain 文件夹"""
    resp = _ima_api("openapi/wiki/v1/get_knowledge_list", {
        "knowledge_base_id": KB_ID,
        "cursor": "",
        "limit": 50,
    })
    items = resp.get("knowledge_list", [])
    for item in items:
        if item.get("title") == BILI_KNOWLEDGE_FOLDER:
            return item.get("media_id")
    return None


def _create_bili_folder() -> Optional[str]:
    """创建 biliyoutik2brain 文件夹"""
    resp = _ima_api("openapi/wiki/v1/create_folder", {
        "knowledge_base_id": KB_ID,
        "title": BILI_KNOWLEDGE_FOLDER,
    })
    if resp.get("code") == 0:
        folder_id = resp.get("data", {}).get("folder_id") or resp.get("folder_id")
        print(f"  [IMA] ✅ 创建文件夹: {BILI_KNOWLEDGE_FOLDER} ({folder_id})")
        return folder_id
    else:
        print(f"  [IMA] ❌ 创建文件夹失败: {resp.get('msg', '')[:100]}")
        return None


def _get_or_create_folder() -> Optional[str]:
    """获取或创建 biliyoutik2brain 文件夹"""
    folder_id = _find_bili_folder()
    if not folder_id:
        folder_id = _create_bili_folder()
    return folder_id


def _upload_markdown(file_path: str, title: str) -> bool:
    """上传 markdown 文件到 IMA 知识库根目录

    流程: preflight → check_repeated_names → create_media → COS upload → add_knowledge
    """
    if not os.path.exists(file_path):
        print(f"  [IMA] ❌ 文件不存在: {file_path}")
        return False

    # Step 1: preflight
    preflight_result = subprocess.run(
        ["node", PREFLIGHT, "--file", file_path],
        capture_output=True, text=True, timeout=10,
    )
    if preflight_result.returncode != 0:
        print(f"  [IMA] ❌ preflight 失败: {preflight_result.stderr[:200]}")
        return False
    
    try:
        pf = json.loads(preflight_result.stdout)
        if not pf.get("pass"):
            print(f"  [IMA] ❌ 不支持的文件类型: {pf.get('reason', '')}")
            return False
    except json.JSONDecodeError:
        print(f"  [IMA] ❌ preflight 返回非法JSON")
        return False
    
    file_name = pf["file_name"]
    file_ext = pf["file_ext"]
    file_size = pf["file_size"]
    media_type = pf["media_type"]
    content_type = pf["content_type"]

    # Step 2: check_repeated_names
    check_resp = _ima_api("openapi/wiki/v1/check_repeated_names", {
        "params": [{"name": file_name, "media_type": media_type}],
        "knowledge_base_id": KB_ID,
        "folder_id": FOLDER_ID,
    })
    if check_resp.get("code") == 0:
        params_out = check_resp.get("data", {}).get("params", [])
        if params_out and params_out[0].get("is_repeated"):
            # 追加时间戳
            ts = time.strftime("%Y%m%d%H%M%S")
            base_name = os.path.splitext(file_name)[0]
            file_name = f"{base_name}_{ts}{file_ext}"
            print(f"  [IMA] 重名，追加时间戳: {file_name}")

    # Step 3: create_media — IMA 以这里的 file_name 作为最终显示标题
    create_resp = _ima_api("openapi/wiki/v1/create_media", {
        "file_name": title,  # 用目标文件名，而非 preflight 返回的临时文件名
        "file_size": file_size,
        "content_type": content_type,
        "knowledge_base_id": KB_ID,
        "file_ext": "md",
        "folder_id": FOLDER_ID,
    })
    if create_resp.get("code") != 0:
        print(f"  [IMA] ❌ create_media 失败: {create_resp.get('msg', '')[:100]}")
        return False
    
    data = create_resp.get("data", create_resp)
    media_id = data.get("media_id", "")
    cos_cred = data.get("cos_credential", {})
    if not media_id or not cos_cred:
        print(f"  [IMA] ❌ create_media 缺少 media_id 或 cos_credential")
        return False

    # Step 4: COS upload
    cos_result = subprocess.run(
        [
            "node", COS_UPLOAD,
            "--file", file_path,
            "--secret-id", cos_cred["secret_id"],
            "--secret-key", cos_cred["secret_key"],
            "--token", cos_cred["token"],
            "--bucket", cos_cred["bucket_name"],
            "--region", cos_cred["region"],
            "--cos-key", cos_cred["cos_key"],
            "--content-type", content_type,
            "--start-time", str(cos_cred.get("start_time", "")),
            "--expired-time", str(cos_cred.get("expired_time", "")),
            "--timeout", "60000",
        ],
        capture_output=True, text=True, timeout=90,
    )
    if cos_result.returncode != 0:
        print(f"  [IMA] ❌ COS 上传失败: {cos_result.stderr[:200]}")
        return False

    # Step 5: add_knowledge
    add_resp = _ima_api("openapi/wiki/v1/add_knowledge", {
        "media_type": media_type,
        "media_id": media_id,
        "title": title,
        "knowledge_base_id": KB_ID,
        "folder_id": FOLDER_ID,
        "file_info": {
            "cos_key": cos_cred["cos_key"],
            "file_size": file_size,
            "file_name": title,
        },
    })
    if add_resp.get("code") == 0:
        print(f"  [IMA] ✅ 上传成功: {title}")
        return True
    else:
        print(f"  [IMA] ❌ add_knowledge 失败: {add_resp.get('msg', '')[:100]}")
        return False


def _search_knowledge(query: str, top_n: int = 5) -> List[dict]:
    """搜索 IMA 知识库中 biliyoutik2brain 的已有知识"""
    resp = _ima_api("openapi/wiki/v1/search_knowledge", {
        "query": query,
        "knowledge_base_id": KB_ID,
        "cursor": "",
    })
    if resp.get("code") != 0:
        return []
    data = resp.get("data", resp)
    items = data.get("info_list", []) or data.get("knowledge_list", [])
    return items[:top_n]


def _get_media_content(media_id: str) -> str:
    """获取 markdown 知识条目内容"""
    resp = _ima_api("openapi/wiki/v1/get_media_info", {"media_id": media_id})
    if resp.get("code") == 0:
        info = resp.get("data", resp)
        title = info.get("title", "")
        # markdown 文件通过 url 下载
        url_info = info.get("url_info", {})
        url = url_info.get("url", "")
        if url and info.get("media_type") == 7:
            try:
                import urllib.request
                with urllib.request.urlopen(url, timeout=10) as f:
                    content = f.read().decode('utf-8', errors='ignore')
                    # 取前300字作为摘要
                    abstract = content[:300].replace('\n', ' ')
                    return f"{title}: {abstract}"
            except Exception:
                pass
        return title if title else ""
    return ""

# ── 公开发口 ──

def _build_ima_content(
    video_title: str,
    video_url: str,
    speaker: str,
    domain: str,
    essence: str = "",
    usages: List[str] = None,
    summary: str = "",
) -> str:
    """按三层维度生成 IMA markdown 内容（仅当前视频提炼）"""
    if usages is None:
        usages = []
    now = time.strftime("%Y-%m-%d %H:%M")
    
    lines = []
    lines.append(f"## {video_title}")
    lines.append(f"> 来源: {video_url} | 处理日期: {now} | 领域: {domain}")
    lines.append(f"> UP主: {speaker}")
    lines.append("")

    # 底层认知: essence（视频的框架性认知）
    if essence:
        lines.append("### 底层认知")
        for line in essence.split("。"):
            line = line.strip()
            if line:
                lines.append(f"- {line}。")
        lines.append("")

    # 自用方法论: usages（可落地的方法/步骤）
    if usages:
        lines.append("### 自用方法论")
        for item in usages:
            lines.append(f"- {item}")
        lines.append("")

    # 独家观点: summary 中提取核心命题句
    viewpoints = _extract_viewpoints(summary)
    if viewpoints:
        lines.append("### 独家观点")
        for item in viewpoints:
            lines.append(f"- {item}")
        lines.append("")

    if not essence and not usages and not viewpoints and summary:
        lines.append(f"**摘要**: {summary}")
        lines.append("")

    return "\n".join(lines)


def _extract_viewpoints(summary: str) -> List[str]:
    """从摘要中提取核心观点句（按句号/分号/换行拆分，取长度>15的句子）"""
    if not summary:
        return []
    sentences = re.split(r'[。；\n]', summary)
    result = []
    for s in sentences:
        s = s.strip()
        if len(s) > 15 and len(s) < 120:
            result.append(s)
    return result[:8]  # 最多8条


def _extract_video_id(url: str) -> str:
    """从视频 URL 提取平台识别码
    
    B站: video/BVxxx → BVxxx
    YouTube: watch?v=xxx → xxx
    其他：返回空字符串
    """
    if not url:
        return ""
    # B站 BV/av 号
    m = re.search(r'/(BV[\w]+|av\d+)', url)
    if m:
        return m.group(1)
    # YouTube
    m = re.search(r'[?&]v=([\w_-]+)', url)
    if m:
        return m.group(1)
    # 短链 b23.tv 展开后也可能出现 BV 号，当前留空等 upstream 解析
    return ""


def upload_knowledge_to_ima(
    speaker: str,
    video_title: str,
    summary: str,
    keywords: List[str],
    domain: str,
    video_url: str = "",
    essence: str = "",
    usages: List[str] = None,
    markdown_path: str = "",
) -> bool:
    """将知识条目上传到 IMA 知识库

    v1.11.0: 按三层维度（底层认知/方法论/观点）组织内容
    文件名格式: {UP主} {视频标题} {视频ID}.md
    内容仅含当前视频的提炼（essence→底层认知, usages→方法论, summary→观点）
    """
    # 文件名: "不聪明钱交易 吞没形态进场就被套 BV1wKVj6nEf4.md"
    # 从 video_url 提取 BV 号或其它平台 ID
    vid = _extract_video_id(video_url)
    title = f"{speaker} {video_title[:60]}{' ' + vid if vid else ''}.md"

    # 生成新内容（三层维度）
    new_content = _build_ima_content(
        video_title=video_title,
        video_url=video_url or "",
        speaker=speaker,
        domain=domain,
        essence=essence or "",
        usages=usages or [],
        summary=summary,
    )

    # 写入临时文件 → 上传
    try:
        fd, file_path = tempfile.mkstemp(suffix=".md", prefix="bili_")
        with os.fdopen(fd, 'w') as f:
            f.write(new_content)
        
        result = _upload_markdown(file_path, title)
        if not result:
            ts = time.strftime("%Y%m%d%H%M%S")
            title2 = f"{speaker} {video_title[:60]}{' ' + _extract_video_id(video_url) if _extract_video_id(video_url) else ''}_{ts}.md"
            result = _upload_markdown(file_path, title2)
        
        return result
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


def _get_media_raw_content(media_id: str) -> str:
    """下载 markdown 笔记的完整内容"""
    resp = _ima_api("openapi/wiki/v1/get_media_info", {"media_id": media_id})
    if resp.get("code") != 0:
        return ""
    url_info = resp.get("data", {}).get("url_info", {})
    url = url_info.get("url", "")
    if url:
        try:
            import urllib.request
            with urllib.request.urlopen(url, timeout=10) as f:
                return f.read().decode('utf-8', errors='ignore')
        except Exception:
            pass
    return ""


def fetch_knowledge_from_ima(speaker: str, domain: str = "", top_n: int = 5) -> str:
    """从 IMA 知识库拉取已有知识上下文

    返回拼接的知识文本，用于增强 LLM prompt
    """
    queries = [speaker]
    if domain:
        queries.append(domain)
    
    all_items = []
    seen_ids = set()
    for q in queries:
        items = _search_knowledge(q, top_n=3)
        for item in items:
            mid = item.get("media_id", "")
            if mid and mid not in seen_ids:
                seen_ids.add(mid)
                all_items.append(item)
    
    if not all_items:
        return ""
    
    parts = ["[IMA知识库已有知识]"]
    for item in all_items[:top_n]:
        title = item.get("title", "")
        media_id = item.get("media_id", "")
        content = _get_media_content(media_id) if media_id else ""
        if content:
            parts.append(f"- {content}")
        elif title:
            parts.append(f"- {title}")
    
    return "\n".join(parts)
