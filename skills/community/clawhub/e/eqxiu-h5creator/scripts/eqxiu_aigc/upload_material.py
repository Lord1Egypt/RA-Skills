"""
易企秀素材上传：COS 临时凭证 → PutObject → saveFile 登记素材库。
流程对齐投票鸭 `toupiaoya/commands/upload_cmd.py`，API 域名使用 eqxiu.com。
"""

from __future__ import annotations

from hashlib import md5
from pathlib import Path
from typing import Any, Mapping, MutableMapping

import requests

from .constants import (
    ASSET_PUBLIC_BASE,
    BROWSER_CHROME_UA,
    DEFAULT_COS_BUCKET,
    DEFAULT_COS_PREFIX,
    DEFAULT_MATERIAL_SOURCE,
    DEFAULT_UPLOAD_TIMEOUT,
    EQXIU_COS_TOKEN_API_BASE,
    EQXIU_MATERIAL_API_BASE,
    EQXIU_UPLOAD_PAGE_ORIGIN,
)

try:
    from qcloud_cos.cos_exception import CosClientError, CosServiceError
except ImportError:

    class CosClientError(Exception):
        pass

    class CosServiceError(Exception):
        pass


def _http_get(
    url: str,
    *,
    access_token: str | None = None,
    params: Mapping[str, Any] | None = None,
    extra_headers: MutableMapping[str, str] | None = None,
    timeout: int = DEFAULT_UPLOAD_TIMEOUT,
) -> requests.Response:
    headers: dict[str, str] = dict(extra_headers or {})
    if access_token:
        headers["X-Openclaw-Token"] = access_token
    return requests.get(url, params=dict(params) if params else None, headers=headers or None, timeout=timeout)


def _http_post_json(
    url: str,
    json_body: Mapping[str, Any],
    *,
    access_token: str | None = None,
    extra_headers: MutableMapping[str, str] | None = None,
    timeout: int = DEFAULT_UPLOAD_TIMEOUT,
) -> requests.Response:
    headers: dict[str, str] = dict(extra_headers or {})
    if access_token:
        headers["X-Openclaw-Token"] = access_token
    return requests.post(url, json=dict(json_body), headers=headers or None, timeout=timeout)


_COS_TOKEN_HEADERS = {
    "accept": "application/json, text/plain, */*",
    "origin": EQXIU_UPLOAD_PAGE_ORIGIN,
    "user-agent": BROWSER_CHROME_UA,
}

_MATERIAL_SAVE_HEADERS = {
    "accept": "application/json, text/plain, */*",
    "user-agent": BROWSER_CHROME_UA,
}

_MATERIAL_LIST_HEADERS = {
    "accept": "application/json, text/plain, */*",
    "origin": EQXIU_UPLOAD_PAGE_ORIGIN,
    "user-agent": BROWSER_CHROME_UA,
}

_PASSPORT_USER_INFO_HEADERS = {
    "accept": "application/json, text/plain, */*",
    "origin": EQXIU_UPLOAD_PAGE_ORIGIN,
    "user-agent": BROWSER_CHROME_UA,
}


def _rows_from_list2_body(body: Mapping[str, Any]) -> list[dict[str, Any]]:
    """list2 成功响应：列表在根级 list；兼容旧形态 obj 为数组或 obj.list。"""
    top = body.get("list")
    if isinstance(top, list) and all(isinstance(x, dict) for x in top):
        return list(top)
    obj = body.get("obj")
    if isinstance(obj, list):
        return [x for x in obj if isinstance(x, dict)]
    if isinstance(obj, dict):
        for key in ("list", "records", "rows"):
            v = obj.get(key)
            if isinstance(v, list) and all(isinstance(x, dict) for x in v):
                return list(v)
    return []


def _slim_upload_material_row(row: Mapping[str, Any]) -> dict[str, Any]:
    tag_ids = row.get("tagIds")
    if tag_ids is None:
        tid = row.get("tagId")
        if tid is None:
            tag_ids = []
        elif isinstance(tid, list):
            tag_ids = list(tid)
        else:
            tag_ids = [tid]
    return {
        "id": row.get("id"),
        "path": row.get("path"),
        "name": row.get("name"),
        "tagIds": tag_ids,
    }


def fetch_user_info(access_token: str, *, timeout: int = DEFAULT_UPLOAD_TIMEOUT) -> dict[str, Any]:
    """GET /user/info — 获取当前登录用户信息。"""
    res = _http_get(
        "https://passport.eqxiu.com/user/info",
        access_token=access_token,
        extra_headers=dict(_PASSPORT_USER_INFO_HEADERS),
        timeout=timeout,
    )
    res.raise_for_status()
    body = res.json()
    if not isinstance(body, dict):
        raise RuntimeError("user/info 返回非 JSON 对象")
    if not body.get("success") or body.get("code") != 200:
        raise RuntimeError(str(body.get("msg") or "获取用户信息失败"))
    return body


def extract_user_id_from_user_info(body: Mapping[str, Any]) -> str:
    """从 user/info 响应中提取 userId。"""
    obj = body.get("obj")
    if not isinstance(obj, dict):
        raise RuntimeError("user/info 返回缺少 obj")

    score_info = obj.get("userScoreInfo")
    if isinstance(score_info, dict):
        uid = str(score_info.get("userId") or "").strip()
        if uid:
            return uid

    members = obj.get("members")
    if isinstance(members, list):
        for m in members:
            if not isinstance(m, dict):
                continue
            uid = str(m.get("userId") or "").strip()
            if uid:
                return uid
    raise RuntimeError("user/info 未返回有效 userId")


def list_user_upload_materials(
    access_token: str,
    *,
    file_type: int = 1,
    page_no: int = 1,
    page_size: int = 30,
    tag_id: int = -1,
    material_api_base: str = EQXIU_MATERIAL_API_BASE,
    timeout: int = DEFAULT_UPLOAD_TIMEOUT,
) -> dict[str, Any]:
    """
    GET /m/material/user/upload/list2 — 当前用户已上传素材分页列表（fileType=1 一般为图片）。
    与投票鸭 material_api.fetch_user_upload_list 一致，域名为 material-api.eqxiu.com。
    成功响应形如根级 success/code/msg、obj（可为 null）、map（分页）、list（数组）；
    返回时保留该结构，且 list 内每条仅含 id、path、name、tagIds（无 tagIds 时由 tagId 归一化）。
    """
    url = f"{material_api_base.rstrip('/')}/m/material/user/upload/list2"
    res = _http_get(
        url,
        access_token=access_token,
        params={
            "fileType": file_type,
            "pageNo": page_no,
            "pageSize": page_size,
            "tagId": tag_id,
        },
        extra_headers=dict(_MATERIAL_LIST_HEADERS),
        timeout=timeout,
    )
    res.raise_for_status()
    body = res.json()
    if not isinstance(body, dict):
        raise RuntimeError("list2 返回非 JSON 对象")
    if not body.get("success") or body.get("code") != 200:
        raise RuntimeError(str(body.get("msg") or "素材列表 list2 失败"))
    slim = [_slim_upload_material_row(r) for r in _rows_from_list2_body(body)]
    out: dict[str, Any] = {
        "success": bool(body.get("success")),
        "code": body.get("code"),
    }
    if "msg" in body:
        out["msg"] = body["msg"]
    if "obj" in body:
        out["obj"] = body["obj"]
    if "map" in body:
        out["map"] = body["map"]
    out["list"] = slim
    return out


def _cos_bucket_for_sdk(inner: Mapping[str, Any]) -> str:
    name = str(inner.get("bucket") or "")
    aid = str(inner.get("appId") or "").strip()
    if aid and not name.endswith("-" + aid):
        return f"{name}-{aid}"
    return name


def build_object_key(prefix: str, object_name: str) -> str:
    p = prefix.strip().replace("\\", "/")
    if not p.endswith("/"):
        p += "/"
    dir_part = p.lstrip("/")
    name = object_name.lstrip("/")
    if not dir_part:
        return name
    return f"{dir_part}{name}"


def fetch_cos_token(
    access_token: str,
    *,
    bucket: str = DEFAULT_COS_BUCKET,
    prefix: str = DEFAULT_COS_PREFIX,
    cos_api_base: str = EQXIU_COS_TOKEN_API_BASE,
    timeout: int = DEFAULT_UPLOAD_TIMEOUT,
) -> dict[str, Any]:
    url = f"{cos_api_base.rstrip('/')}/cos/user/token-upload"
    res = _http_get(
        url,
        access_token=access_token,
        params={"bucket": bucket, "prefix": prefix},
        extra_headers=dict(_COS_TOKEN_HEADERS),
        timeout=timeout,
    )
    res.raise_for_status()
    body = res.json()
    if not isinstance(body, dict):
        raise ValueError("token-upload 返回非 JSON 对象")
    if not body.get("success") or body.get("code") != 200:
        raise RuntimeError(str(body.get("msg") or "获取 COS 凭证失败"))
    inner = body.get("obj")
    if not isinstance(inner, dict):
        raise RuntimeError("token-upload 返回缺少 obj")
    if inner.get("success") is False and inner.get("msg"):
        raise RuntimeError(str(inner.get("msg")))
    for k in ("tmpSecretId", "tmpSecretKey", "sessionToken", "region", "bucket"):
        if not inner.get(k):
            raise RuntimeError(f"COS 凭证字段缺失: {k}")
    return dict(inner)


def put_local_file(inner: dict[str, Any], local_path: Path, object_key: str) -> dict[str, Any]:
    try:
        from qcloud_cos import CosConfig, CosS3Client
    except ImportError as e:
        raise ImportError("请先安装腾讯云 COS SDK：pip install cos-python-sdk-v5") from e
    region = str(inner["region"])
    secret_id = str(inner["tmpSecretId"])
    secret_key = str(inner["tmpSecretKey"])
    session_token = str(inner["sessionToken"])
    bucket = _cos_bucket_for_sdk(inner)

    config = CosConfig(
        Region=region,
        SecretId=secret_id,
        SecretKey=secret_key,
        Token=session_token,
        Scheme="https",
    )
    client = CosS3Client(config)

    key = object_key.lstrip("/")
    with local_path.open("rb") as fp:
        resp = client.put_object(Bucket=bucket, Body=fp, Key=key, EnableMD5=False)

    etag = (resp.get("ETag") or resp.get("Etag") or "").strip('"')
    out: dict[str, Any] = {
        "success": True,
        "code": 200,
        "msg": "ok",
        "bucket": bucket,
        "region": region,
        "key": key,
        "etag": etag,
        "assetUrl": f"{ASSET_PUBLIC_BASE.rstrip('/')}/{key}",
    }
    return out


def build_save_file_payload(
    *,
    cos_key: str,
    local_path: Path,
    logical_bucket: str,
    source: str,
    tag_id: int,
    file_type: int,
    tmb_path: str | None,
) -> dict[str, Any]:
    key = cos_key.lstrip("/")
    tmb = (tmb_path or key).lstrip("/")
    ext = local_path.suffix or ""
    return {
        "path": key,
        "tmbPath": tmb,
        "name": local_path.name,
        "size": local_path.stat().st_size,
        "extName": ext,
        "tagId": tag_id,
        "fileType": file_type,
        "storageType": 0,
        "uploadType": 0,
        "providerType": 1,
        "source": source,
        "bucket": logical_bucket,
    }


def save_material_file(
    access_token: str,
    payload: Mapping[str, Any],
    *,
    material_api_base: str = EQXIU_MATERIAL_API_BASE,
    timeout: int = DEFAULT_UPLOAD_TIMEOUT,
) -> dict[str, Any]:
    url = f"{material_api_base.rstrip('/')}/m/material/info/saveFile"
    res = _http_post_json(
        url,
        dict(payload),
        access_token=access_token,
        extra_headers=dict(_MATERIAL_SAVE_HEADERS),
        timeout=timeout,
    )
    res.raise_for_status()
    body = res.json()
    if not isinstance(body, dict):
        raise RuntimeError("saveFile 返回非 JSON 对象")
    if not body.get("success") or body.get("code") != 200:
        raise RuntimeError(str(body.get("msg") or "素材库 saveFile 失败"))
    obj = body.get("obj")
    if not isinstance(obj, dict):
        raise RuntimeError("saveFile 返回缺少 obj")
    return {
        "id": obj.get("id"),
        "path": obj.get("path"),
        "name": obj.get("name"),
        "tagIds": obj.get("tagIds"),
        "createTime": obj.get("createTime"),
    }


def upload_local_material(
    access_token: str,
    file_path: Path | str,
    *,
    bucket: str = DEFAULT_COS_BUCKET,
    prefix: str = DEFAULT_COS_PREFIX,
    object_name: str | None = None,
    tmb_path: str | None = None,
    source: str = DEFAULT_MATERIAL_SOURCE,
    tag_id: int = -1,
    file_type: int = 1,
    cos_api_base: str = EQXIU_COS_TOKEN_API_BASE,
    material_api_base: str = EQXIU_MATERIAL_API_BASE,
    timeout: int = DEFAULT_UPLOAD_TIMEOUT,
) -> dict[str, Any]:
    """
    上传本地文件到 COS 并登记素材库；返回含 cos、material 字段的字典（与投票鸭 CLI 输出结构一致）。
    """
    path = Path(file_path).expanduser()
    if not path.is_file():
        raise FileNotFoundError(f"文件不存在或不是普通文件: {path}")

    oname = (object_name or path.name).strip()
    if not oname:
        raise ValueError("对象名不能为空")
    user_info = fetch_user_info(access_token, timeout=timeout)
    user_id = extract_user_id_from_user_info(user_info)
    ext = path.suffix.lstrip(".")
    hashed_name = md5(oname.encode("utf-8")).hexdigest()
    filename = f"{hashed_name}.{ext}" if ext else hashed_name
    object_key = build_object_key(prefix, f"{user_id}/{filename}")
    inner = fetch_cos_token(access_token, bucket=bucket, prefix=prefix, cos_api_base=cos_api_base, timeout=timeout)
    cos_result = put_local_file(inner, path, object_key)

    save_payload = build_save_file_payload(
        cos_key=cos_result["key"],
        local_path=path,
        logical_bucket=bucket,
        source=source,
        tag_id=tag_id,
        file_type=file_type,
        tmb_path=tmb_path,
    )
    material_obj = save_material_file(
        access_token, save_payload, material_api_base=material_api_base, timeout=timeout
    )

    return {
        "success": True,
        "code": 200,
        "msg": "ok",
        "cos": {k: cos_result.get(k) for k in ("bucket", "region", "key", "etag", "assetUrl")},
        "material": material_obj,
    }
