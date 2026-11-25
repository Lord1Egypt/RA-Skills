#!/usr/bin/env python3
"""
PE进化脚本公共配置与运行记录工具
"""
import json
import os
from datetime import datetime
from typing import Any, Dict, Optional

# API配置
BASE_URL = os.environ.get("PE_BASE_URL", "http://127.0.0.1:8000")

# 工作目录
WORKSPACE_DIR = os.path.expanduser("~/pe-self-improving/workspace")
RUNS_DIR = os.path.join(WORKSPACE_DIR, "runs")

# 确保目录存在
os.makedirs(WORKSPACE_DIR, exist_ok=True)
os.makedirs(RUNS_DIR, exist_ok=True)

# API端点
API_ENDPOINTS = {
    # 催收场景（S1-S4）
    "start_sparring": f"{BASE_URL}/start-sparring",
    "sparring_status": f"{BASE_URL}/multi-sparring-status",
    "submit_pe": f"{BASE_URL}/api/prompts/submit",
    # 会展场景
    "submit_expo": f"{BASE_URL}/api/prompts/expo/save",
}


def query_sparring_status(job_id: Optional[str] = None, scene: Optional[str] = None) -> Dict[str, Any]:
    """
    查询对练结果（支持 job_id 查询指定任务）
    
    Args:
        job_id: 指定任务ID（优先使用）
        scene: 场景名称（fallback，用于无job_id时查询最新）
    
    Returns:
        对练结果JSON
        
    返回格式（job_id查询）：
        {
            "status": "success",
            "data": {
                "job_id": "xxx",
                "status": "running" | "completed",
                "result": null | [样本列表]
            }
        }
    """
    import requests
    
    url = API_ENDPOINTS["sparring_status"]
    
    # 优先使用 job_id 查询指定任务（GET请求）
    if job_id:
        resp = requests.get(url, params={"jobId": job_id}, timeout=30)
    else:
        # 无 job_id 时，GET请求获取最新结果
        resp = requests.get(url, timeout=30)
    
    return resp.json()


def extract_sparring_results(data: Dict[str, Any]) -> tuple:
    """
    从对练结果中提取样本列表（兼容新旧格式）
    
    返回: (results, task_status, error_message)
        - results: 样本列表（完成后有数据）
        - task_status: 任务状态 (pending/running/completed/failed)
        - error_message: 错误信息（失败时有）
    
    新格式（job_id查询）：
        {"data": {"job_id": "xxx", "status": "completed", "result": [样本列表]}}
    
    旧格式（无job_id查询）：
        {"data": [样本列表]}
    """
    # 任务状态常量
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    
    payload = data.get("data")
    
    # 新格式：data = {"job_id": "xxx", "status": "...", "result": [...]}
    if isinstance(payload, dict):
        task_status = payload.get("status", RUNNING)
        error_message = payload.get("error_message")
        
        # 失败
        if task_status == FAILED:
            return [], task_status, error_message or "任务失败"
        
        # 等待中或执行中
        if task_status in (PENDING, RUNNING):
            return [], task_status, None
        
        # 完成
        if task_status == COMPLETED:
            result = payload.get("result")
            if isinstance(result, list):
                results = [r for r in result if isinstance(r, dict) and "score" in r]
                return results, task_status, None
        
        return [], task_status, None
    
    # 旧格式：data = [样本列表]（已完成）
    if isinstance(payload, list):
        results = [r for r in payload if isinstance(r, dict) and "score" in r]
        return results, COMPLETED, None
    
    return [], RUNNING, None


def now_ts() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def make_run_id(prefix: str = "pe-opt") -> str:
    return f"{prefix}-{now_ts()}"


def run_manifest_path(run_id: str) -> str:
    return os.path.join(RUNS_DIR, f"{run_id}.json")


def default_manifest(run_id: str, target_scene: str = "S3", source_type: str = "sparring") -> Dict[str, Any]:
    return {
        "run_id": run_id,
        "target_scene": target_scene,
        "source_type": source_type,
        "status": "INIT",
        "base_version": None,
        "candidate_version": None,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "job_refs": {
            "sparring_before_job_id": None,
            "verify_job_id": None,
        },
        "artifacts": {
            "original_pe": None,
            "sparring_before": None,
            "optimized_pe": None,
            "submit_log": None,
            "verify_after": None,
        },
        "evaluation": {
            "score_before": None,
            "score_after": None,
            "score_delta": None,
            "adopted": None,
            "rollback_required": None,
        },
        "memory_updates": {
            "issues": [],
            "learnings": [],
            "candidates": [],
            "evidence": [],
            "hot_promotions": [],
            "demotions": [],
        },
        "notes": [],
    }


def save_manifest(manifest: Dict[str, Any]) -> str:
    manifest["updated_at"] = datetime.now().isoformat()
    path = run_manifest_path(manifest["run_id"])
    with open(path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    return path


def load_manifest(run_id: str) -> Dict[str, Any]:
    path = run_manifest_path(run_id)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def create_run(target_scene: str = "S3", source_type: str = "sparring") -> Dict[str, Any]:
    run_id = make_run_id()
    manifest = default_manifest(run_id, target_scene=target_scene, source_type=source_type)
    save_manifest(manifest)
    return manifest


def append_note(manifest: Dict[str, Any], note: str) -> None:
    manifest.setdefault("notes", []).append({
        "time": datetime.now().isoformat(),
        "note": note,
    })


def update_manifest(
    run_id: str,
    *,
    status: Optional[str] = None,
    base_version: Optional[Any] = None,
    candidate_version: Optional[Any] = None,
    job_refs: Optional[Dict[str, Any]] = None,
    artifacts: Optional[Dict[str, Any]] = None,
    evaluation: Optional[Dict[str, Any]] = None,
    memory_updates: Optional[Dict[str, Any]] = None,
    note: Optional[str] = None,
) -> Dict[str, Any]:
    manifest = load_manifest(run_id)
    if status:
        manifest["status"] = status
    if base_version is not None:
        manifest["base_version"] = base_version
    if candidate_version is not None:
        manifest["candidate_version"] = candidate_version
    if job_refs:
        manifest.setdefault("job_refs", {}).update(job_refs)
    if artifacts:
        manifest.setdefault("artifacts", {}).update(artifacts)
    if evaluation:
        manifest.setdefault("evaluation", {}).update(evaluation)
    if memory_updates:
        mu = manifest.setdefault("memory_updates", {})
        for key, value in memory_updates.items():
            if isinstance(value, list):
                mu.setdefault(key, [])
                mu[key].extend(value)
            else:
                mu[key] = value
    if note:
        append_note(manifest, note)
    save_manifest(manifest)
    return manifest


def latest_run_id() -> Optional[str]:
    files = [f for f in os.listdir(RUNS_DIR) if f.endswith(".json")]
    if not files:
        return None
    files.sort(reverse=True)
    return files[0].rsplit(".", 1)[0]
