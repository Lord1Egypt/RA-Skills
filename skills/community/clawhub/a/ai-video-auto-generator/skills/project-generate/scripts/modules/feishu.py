"""
飞书 Base 操作模块 — 缓存 record_ids 避免表格解析

依赖: lark-cli (feishu) 命令行工具，通过 subprocess 调用。
缓存: CACHE_FILE (record_ids_cache.json) 存储 project→table→doc_id→record_id 映射，
      避免每次操作全表扫描。同一 project 的多次操作共享同一缓存文件。

路径解析：使用 _paths.py 三层路径模型，不绑定 ~/.workbuddy。
"""
from __future__ import annotations
import json, os, shutil, subprocess, time
from typing import Any, Optional

CACHE_FILE = "record_ids_cache.json"
_LARK_RETRIES = 3
_LARK_RETRY_DELAY = 2


def _resolve_lark_exe() -> str:
    """查找 lark-cli 可执行文件路径。

    优先级链（由高到低）：
        1. PATH 上的 lark-cli / lark-cli.cmd
        2. legacy: ~/.workbuddy/binaries/node/cli-connector-packages/lark-cli.cmd
    """
    # PATH
    lark_exe = shutil.which("lark-cli") or shutil.which("lark-cli.cmd")
    if lark_exe:
        return os.path.abspath(lark_exe)

    # legacy fallback
    legacy_cmd = os.path.join(
        os.path.expanduser("~"), ".workbuddy", "binaries", "node",
        "cli-connector-packages", "lark-cli.cmd",
    )
    if os.path.isfile(legacy_cmd):
        return legacy_cmd

    legacy_noext = os.path.join(
        os.path.expanduser("~"), ".workbuddy", "binaries", "node",
        "cli-connector-packages", "lark-cli",
    )
    if os.path.isfile(legacy_noext):
        return legacy_noext

    return "lark-cli"  # 最后兜底，让 shutil 或 subprocess 去找 PATH


_LARK_EXE = _resolve_lark_exe()

# 公开别名，供其他模块（如 stitch.py）使用
LARK_EXE = _LARK_EXE


def _lark_node_dir() -> str:
    """定位 node 可执行文件目录。

    通过 _paths.resolve_tool("node") 解析，
    优先级：skill 内 vendor/ → config/tools.toml → 系统 PATH。
    找不到则返回空串（沿用当前环境，无回归）。
    """
    try:
        from _paths import resolve_tool as _rt
        node_exe = _rt("node", os.path.dirname(os.path.dirname(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        ))))
        if node_exe:
            return os.path.dirname(node_exe)
    except ImportError:
        pass

    # legacy fallback
    base = os.path.join(os.path.expanduser("~"), ".workbuddy", "binaries", "node")
    vers = os.path.join(base, "versions")
    if os.path.isdir(vers):
        for name in sorted(os.listdir(vers), reverse=True):
            cand = os.path.join(vers, name, "node.exe")
            if os.path.isfile(cand):
                return os.path.dirname(cand)
    alt = os.path.join(base, "cli-connector-packages", "node.exe")
    if os.path.isfile(alt):
        return os.path.dirname(alt)
    return ""


def _lark_env() -> dict:
    """返回注入 managed node 目录的 subprocess 环境，确保 lark-cli 任何环境可用。"""
    env = os.environ.copy()
    nd = _lark_node_dir()
    if nd:
        existing = env.get("PATH", "")
        if nd not in existing.split(os.pathsep):
            env["PATH"] = nd + os.pathsep + existing
    return env


def _feishu_cfg() -> dict[str, str]:
    """从 config 读取飞书配置（含字段ID）。

    通过 _shared_tools.get() 读取，配置来自项目 config/ 和 skill config/。
    """
    result = {"base_token": "", "table_id": "", "workflow_table_id": "",
              "attachment_field_id": "fldJCePDOO",
              "keyframe_urls_field_id": "fldnrAf3St",
              "generation_mode_field_id": "fldFswHV7N"}
    try:
        from _shared_tools import get
        from modules.config import get_feishu_base_token
    except ImportError:
        return result
    # 通过 _shared_tools 的统一配置读取（走项目 config/ + skill config/ 分层）
    # base_token 已从 config.toml 迁出，缺失时回退 ~/.feishu-base-token（见 get_feishu_base_token）
    result["base_token"] = get_feishu_base_token() or ""
    result["table_id"] = get("feishu", "table_id") or ""
    result["workflow_table_id"] = get("feishu", "workflow_table_id") or ""
    result["attachment_field_id"] = get("feishu", "attachment_field_id") or result["attachment_field_id"]
    result["keyframe_urls_field_id"] = get("feishu", "keyframe_urls_field_id") or result["keyframe_urls_field_id"]
    result["generation_mode_field_id"] = get("feishu", "generation_mode_field_id") or result["generation_mode_field_id"]
    return result


def _lark(args: list[str], timeout: int = 30) -> subprocess.CompletedProcess | None:
    """执行 lark-cli，失败自动重试最多 3 次。返回 None 表示全部重试失败。
    
    使用 errors=replace 避免 Windows 下中文输出解码失败。
    Windows 下 .cmd 文件用 list2cmdline 构建参数，确保 --json 值中的
    双引号被正确转义。
    """
    for attempt in range(1, _LARK_RETRIES + 1):
        try:
            if os.name == "nt" and _LARK_EXE.endswith(".cmd"):
                # Windows cmd: 用 subprocess.list2cmdline 自动处理引号转义，
                # 避免 JSON 内嵌双引号导致 cmd shell 解析错误
                full_args = [_LARK_EXE] + args
                cmd_line = subprocess.list2cmdline(full_args)
                r = subprocess.run(cmd_line, capture_output=True, text=True,
                                   encoding="utf-8", errors="replace",
                                   timeout=timeout, shell=True, env=_lark_env())
            else:
                r = subprocess.run([_LARK_EXE] + args, capture_output=True,
                                   text=True, encoding="utf-8", errors="replace",
                                   timeout=timeout, env=_lark_env())
            if r.returncode == 0:
                return r
            if attempt == 1:
                if r.stdout:
                    print(f"  [lark] stdout: {r.stdout[:300]}", flush=True)
                if r.stderr:
                    print(f"  [lark] stderr: {r.stderr[:300]}", flush=True)
            if attempt < _LARK_RETRIES:
                print(f"  [lark] 重试 {attempt}/{_LARK_RETRIES} (returncode={r.returncode})", flush=True)
                time.sleep(_LARK_RETRY_DELAY)
                continue
            return r
        except (subprocess.TimeoutExpired, OSError) as e:
            if attempt < _LARK_RETRIES:
                print(f"  [lark] 重试 {attempt}/{_LARK_RETRIES} ({type(e).__name__})", flush=True)
                time.sleep(_LARK_RETRY_DELAY)
                continue
            print(f"  [lark] 失败 ({type(e).__name__}): {e}", flush=True)
            return None
        except Exception as e:
            print(f"  [lark] 异常: {e}", flush=True)
            return None


def _cache_path(project: str) -> str:
    d = os.path.join(project, "tasks")
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, CACHE_FILE)


def _load_cache(project: str) -> dict[int, str]:
    try:
        with open(_cache_path(project), encoding="utf-8") as f:
            return {int(k): v for k, v in json.load(f).items()}
    except Exception:
        return {}


def _save_cache(project: str, cache: dict[int, str]):
    with open(_cache_path(project), "w", encoding="utf-8") as f:
        json.dump({str(k): v for k, v in cache.items()}, f, indent=2)


def _build_col_map(stdout: str) -> dict[str, int]:
    """从表格输出中提取表头行，构建列名（小写）→ 索引映射。"""
    for line in stdout.strip().split("\n"):
        line_s = line.strip()
        if line_s.startswith("|") and not line_s.startswith("|---"):
            cols = [h.strip().lower() for h in line_s.split("|")]
            return {name: i for i, name in enumerate(cols) if name}
    return {}


def _parse_shots_table(stdout: str, doc_id: str) -> list[dict[str, Any]]:
    """解析表格输出：_record_id | ID | 状态 | 镜头ID | ... | API任务ID | 生成模式 | 关键帧图URL"""
    col = _build_col_map(stdout)
    IDX_RECORD = col.get("_record_id", 1)
    IDX_STATUS = col.get("状态", 3)
    IDX_SHOT = col.get("镜头id", 4) or col.get("镜头ID", 4)
    IDX_MODE = col.get("生成模式", 5)
    IDX_DOC = col.get("对应视频任务id", 9) or col.get("对应视频任务ID", 9)
    IDX_KF_URL = col.get("关键帧图url", 10) or col.get("关键帧图URL", 10)
    IDX_REMARK = col.get("备注", 13)
    IDX_TASK = col.get("api任务id", 14) or col.get("API任务ID", 14)

    result = []
    for line in stdout.strip().split("\n"):
        if not line.startswith("|") or line.startswith("|---"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < max(col.values(), default=14) + 1:
            continue
        # doc_id 过滤
        if parts[IDX_DOC].strip() != doc_id:
            continue
        sid = parts[IDX_SHOT].strip()
        if not sid.startswith("shot_"):
            continue
        entry = {
            "record_id": parts[IDX_RECORD],
            "镜头ID": sid,
            "API任务ID": parts[IDX_TASK].strip(),
            "状态": parts[IDX_STATUS].strip("[]\"' "),
            "备注": parts[IDX_REMARK].strip(),
            "_seq": int(sid.split("_")[1]),
        }
        entry["生成模式"] = parts[IDX_MODE].strip("[]\"' ") if parts[IDX_MODE].strip() else "standard"
        raw = parts[IDX_KF_URL].strip()
        if raw and raw != "-":
            try:
                entry["关键帧图URL"] = json.loads(raw)
            except Exception:
                entry["关键帧图URL"] = []
        else:
            entry["关键帧图URL"] = []
        result.append(entry)
    result.sort(key=lambda x: x["_seq"])
    return result


def list_shots(project: str, feishu_token: str = "", table_id: str = "", doc_id: str = "") -> list[dict[str, Any]]:
    """列出项目所有 shot 记录。token/table_id 不传则从 config.toml 自动读取。"""
    if not feishu_token or not table_id:
        _cfg = _feishu_cfg()
        if not feishu_token:
            feishu_token = _cfg["base_token"]
        if not table_id:
            table_id = _cfg["table_id"]
    r = _lark(["base", "+record-list", "--base-token", feishu_token,
               "--table-id", table_id, "--as", "user"], 15)
    if not r or r.returncode != 0:
        return []
    shots = _parse_shots_table(r.stdout, doc_id)
    cache = {s["_seq"]: s["record_id"] for s in shots if s.get("record_id")}
    _save_cache(project, cache)
    return shots


def get_record_id(project: str, feishu_token: str, table_id: str, doc_id: str, shot_seq: int) -> Optional[str]:
    cache = _load_cache(project)
    rid = cache.get(shot_seq)
    if rid:
        return rid
    shots = list_shots(project, feishu_token, table_id, doc_id)
    for s in shots:
        if s["_seq"] == shot_seq:
            return s.get("record_id")
    return None


def update_record(feishu_token: str, table_id: str, record_id: str, fields: dict[str, Any]) -> bool:
    r = _lark(["base", "+record-upsert", "--base-token", feishu_token,
               "--table-id", table_id, "--record-id", record_id,
               "--json", json.dumps(fields, ensure_ascii=False),
               "--as", "user"], 30)
    if r and r.returncode == 0 and r.stdout.strip():
        return json.loads(r.stdout).get("ok") is True
    return False


def upsert_record(feishu_token: str, table_id: str, fields: dict[str, Any]) -> Optional[str]:
    r = _lark(["base", "+record-upsert", "--base-token", feishu_token,
               "--table-id", table_id,
               "--json", json.dumps(fields, ensure_ascii=False),
               "--as", "user"], 30)
    if r and r.returncode == 0 and r.stdout.strip():
        data = json.loads(r.stdout)
        rids = data.get("data", {}).get("record", {}).get("record_id_list", [])
        return rids[0] if rids else None
    return None


def find_workflow_rec(feishu_token: str = "", wtid: str = "", doc_id: str = "") -> Optional[str]:
    if not feishu_token or not wtid:
        _cfg = _feishu_cfg()
        if not feishu_token:
            feishu_token = _cfg["base_token"]
        if not wtid:
            wtid = _cfg["workflow_table_id"]
    r = _lark(["base", "+record-list", "--base-token", feishu_token,
               "--table-id", wtid, "--as", "user"], 15)
    if not r or r.returncode != 0:
        return None
    col = _build_col_map(r.stdout)
    IDX_RECORD = col.get("_record_id")
    IDX_DOC = col.get("文档id") or col.get("对应视频任务id")
    if IDX_RECORD is None or IDX_DOC is None:
        return None
    for line in r.stdout.strip().split("\n"):
        if not line.startswith("|") or line.startswith("|---"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) > max(IDX_RECORD, IDX_DOC) and parts[IDX_DOC] == doc_id:
            return parts[IDX_RECORD]
    return None


def get_workflow_phase(feishu_token: str = "", wtid: str = "", rec_id: str = "") -> str:
    if not feishu_token or not wtid:
        _cfg = _feishu_cfg()
        if not feishu_token:
            feishu_token = _cfg["base_token"]
        if not wtid:
            wtid = _cfg["workflow_table_id"]
    r = _lark(["base", "+record-list", "--base-token", feishu_token,
               "--table-id", wtid, "--as", "user"], 15)
    if not r or r.returncode != 0:
        return ""
    col = _build_col_map(r.stdout)
    IDX_RECORD = col.get("_record_id", 1)
    IDX_PHASE = col.get("阶段", 11)
    for line in r.stdout.strip().split("\n"):
        if not line.startswith("|") or line.startswith("|---"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) > max(IDX_RECORD, IDX_PHASE) and parts[IDX_RECORD] == rec_id:
            return parts[IDX_PHASE].strip("[]\"' ")
    return ""


def update_workflow_phase(feishu_token: str = "", wtid: str = "", rec_id: str = "", phase: str = "", extra: Optional[dict] = None):
    if not feishu_token or not wtid:
        _cfg = _feishu_cfg()
        if not feishu_token:
            feishu_token = _cfg["base_token"]
        if not wtid:
            wtid = _cfg["workflow_table_id"]
    fields: dict[str, Any] = {"阶段": [phase]}
    if phase == "已完成":
        fields["处理状态"] = ["已完成"]
    if extra:
        fields.update(extra)
    update_record(feishu_token, wtid, rec_id, fields)


def upload_attachment(feishu_token: str, table_id: str, record_id: str, file_path: str, field_id: str | None = None) -> bool:
    if field_id is None:
        field_id = _feishu_cfg().get("attachment_field_id", "fldJCePDOO")
    abs_path = os.path.abspath(file_path)
    parent = os.path.dirname(abs_path)
    rel_path = os.path.basename(abs_path)
    r = subprocess.run(
        [_LARK_EXE, "base", "+record-upload-attachment", "--base-token", feishu_token,
         "--table-id", table_id, "--record-id", record_id,
         "--field-id", field_id, "--file", rel_path, "--as", "user"],
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120, cwd=parent,
    )
    return r.returncode == 0


def upload_to_drive(file_path: str, file_name: str | None = None) -> str | None:
    abs_path = os.path.abspath(file_path)
    parent = os.path.dirname(abs_path)
    rel_path = os.path.basename(abs_path)
    name = file_name or rel_path
    r = subprocess.run(
        [_LARK_EXE, "drive", "+upload", "--file", rel_path,
         "--name", name, "--as", "user", "--json"],
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60, cwd=parent,
    )
    if r.returncode == 0 and r.stdout.strip():
        try:
            data = json.loads(r.stdout)
            if data.get("ok") and data["data"].get("url"):
                return data["data"]["url"]
        except (json.JSONDecodeError, KeyError, TypeError):
            pass
    return None


# ── 镜头任务记录清理 ──

def delete_shot_records(project: str, feishu_token: str = "", table_id: str = "") -> int:
    """完成最终视频上传后，删除飞书镜头任务表的所有相关记录。
    
    返回删除的记录数。无缓存或 token 不可用时静默跳过。
    """
    if not feishu_token or not table_id:
        from modules.config import get_feishu_base_token, get_feishu_table_id
        feishu_token = feishu_token or get_feishu_base_token()
        table_id = table_id or get_feishu_table_id()
    if not feishu_token or not table_id:
        return 0

    # 从缓存读 record_id
    cache = _load_cache(project)
    if not cache:
        return 0

    record_ids = [rid for rid in cache.values() if rid]
    if not record_ids:
        return 0

    # lark-cli +record-delete 需要 --yes 确认
    for rid in record_ids:
        r = _lark(["base", "+record-delete", "--yes",
                    "--base-token", feishu_token,
                    "--table-id", table_id, "--record-id", rid, "--as", "user"], timeout=15)
        if r and r.returncode == 0:
            print(f"  [清理] ✅ 已删除 shot 记录 {rid}")
        else:
            # 单条删除失败不中断
            pass

    _save_cache(project, {})  # 清空缓存
    print(f"  [清理] ✅ 共清理 {len(record_ids)} 条 shot 记录")
    return len(record_ids)


def _get_kf_urls_field() -> str:
    """从 config 读取关键帧 URL 字段 ID，未配置时使用默认值。"""
    return _feishu_cfg().get("keyframe_urls_field_id", "fldnrAf3St")


def _get_gen_mode_field() -> str:
    """从 config 读取生成模式字段 ID，未配置时使用默认值。"""
    return _feishu_cfg().get("generation_mode_field_id", "fldFswHV7N")


def get_shot_mode(project: str, feishu_token: str, table_id: str, doc_id: str, shot_seq: int) -> str:
    shots = list_shots(project, feishu_token, table_id, doc_id)
    for s in shots:
        if s["_seq"] == shot_seq:
            return s.get("生成模式", "standard")
    return "standard"


def get_keyframe_urls(project: str, feishu_token: str, table_id: str, doc_id: str, shot_seq: int) -> list[str]:
    shots = list_shots(project, feishu_token, table_id, doc_id)
    for s in shots:
        if s["_seq"] == shot_seq:
            return s.get("关键帧图URL", [])
    return []


def save_keyframe_urls(feishu_token: str, table_id: str, record_id: str, urls: list[str]) -> bool:
    return update_record(feishu_token, table_id, record_id, {
        _get_kf_urls_field(): json.dumps(urls, ensure_ascii=False),
    })


def save_generation_mode(feishu_token: str, table_id: str, record_id: str, mode: str) -> bool:
    return update_record(feishu_token, table_id, record_id, {
        _get_gen_mode_field(): [mode],
    })


def sync_project_summary(project: str) -> bool:
    """从 script.json 生成最新摘要，更新飞书 Base 工作流表的「脚本内容」字段。"""
    script_path = os.path.join(project, "script.json")
    if not os.path.isfile(script_path):
        return False
    with open(script_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    sc = data.get("script", {})
    shots = data.get("shots", [])
    groups = data.get("shot_groups", [])
    chars = data.get("character_cards", [])
    scenes = data.get("scene_cards", [])
    doc_id = sc.get("feishu_doc_id", "") or sc.get("feishu_doc_url", "").split("/wiki/")[-1].split("?")[0] if sc.get("feishu_doc_url") else ""

    aspect = sc.get("aspect_ratio", "16:9")
    vtype = sc.get("type", "")
    orientation = "横屏" if aspect.startswith("16:9") else "竖屏" if aspect.startswith("9:16") else aspect

    summary = (
        f"{len(shots)}镜头"
        f"/{len(groups)}组场景"
        f"/{aspect}{orientation}"
        f"/{vtype}"
        f"/含{len(chars)}角色卡+{len(scenes)}场景卡"
    )

    _cfg = _feishu_cfg()
    if not _cfg["base_token"]:
        print(f"  [feishu] ⚠️ 同步失败: config.toml 中 base_token 为空", flush=True)
        return False
    if not _cfg["workflow_table_id"]:
        print(f"  [feishu] ⚠️ 同步失败: config.toml 中 workflow_table_id 为空", flush=True)
        return False
    if not doc_id:
        print(f"  [feishu] ⚠️ 同步失败: script.json 中 feishu_doc_id 和 feishu_doc_url 均为空", flush=True)
        return False
    rec_id = find_workflow_rec(_cfg["base_token"], _cfg["workflow_table_id"], doc_id)
    if not rec_id:
        print(f"  [feishu] ⚠️ 同步失败: workflow 表中未找到 doc_id={doc_id} 对应的记录", flush=True)
        return False
    result = update_record(_cfg["base_token"], _cfg["workflow_table_id"], rec_id, {
        "脚本名称": summary,
    })
    if not result:
        print(f"  [feishu] ⚠️ 同步失败: 更新记录失败（rec_id={rec_id}）", flush=True)
    return result
