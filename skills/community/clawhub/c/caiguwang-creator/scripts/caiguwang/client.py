# -*- coding: utf-8 -*-
"""才谷网投票 Skill HTTP 客户端：统一携带 X-Caigu-Token，统一解析 {success, code, msg, data}"""
import requests

from . import config


def _headers(token=None):
    t = token or config.load_token()
    headers = {"Accept": "application/json"}
    if t:
        headers["X-Caigu-Token"] = t
    return headers


def _parse(resp):
    try:
        payload = resp.json()
    except ValueError:
        payload = {"success": False, "code": -1, "msg": "接口返回异常（HTTP %s）" % resp.status_code, "data": None}
    if not isinstance(payload, dict) or "code" not in payload:
        payload = {"success": False, "code": -1, "msg": "接口返回异常（HTTP %s）" % resp.status_code, "data": None}
    return payload


def _call(method, path, token=None, params=None, json_body=None):
    url = config.get_api_base() + path
    try:
        resp = requests.request(
            method, url,
            params=params,
            json=json_body,
            headers=_headers(token),
            timeout=config.DEFAULT_TIMEOUT,
        )
    except requests.RequestException as e:
        return {"success": False, "code": -1, "msg": "网络请求失败：%s" % e.__class__.__name__, "data": None}
    return _parse(resp)


def upload_image(file_path=None, image_url=None, crop="", token=None):
    url = config.get_api_base() + "/api/openapi/upload_image"
    try:
        if file_path:
            with open(file_path, "rb") as f:
                resp = requests.post(url, files={"file": f}, data={"crop": crop or ""},
                                     headers=_headers(token), timeout=120)
        else:
            resp = requests.post(url, json={"image_url": image_url or "", "crop": crop or ""},
                                 headers=_headers(token), timeout=120)
    except requests.RequestException as e:
        return {"success": False, "code": -1, "msg": "网络请求失败：%s" % e.__class__.__name__, "data": None}
    return _parse(resp)


def auth_status(token=None):
    return _call("GET", "/api/openapi/auth_status", token=token)


def search_templates(keyword="", page=1, size=10, token=None):
    return _call("GET", "/api/openapi/search_templates",
                 token=token, params={"keyword": keyword, "page": page, "size": size})


def create_vote(body, token=None):
    return _call("POST", "/api/openapi/create_vote", token=token, json_body=body)


def update_vote(body, token=None):
    return _call("POST", "/api/openapi/update_vote", token=token, json_body=body)


def item_add(body, token=None):
    return _call("POST", "/api/openapi/item_add", token=token, json_body=body)


def item_update(body, token=None):
    return _call("POST", "/api/openapi/item_update", token=token, json_body=body)


def list_activities(page=1, size=10, keyword="", status="all", token=None):
    return _call("GET", "/api/openapi/list_activities",
                 token=token, params={"page": page, "size": size, "keyword": keyword, "status": status})


def vote_data(activity_id, page=1, size=20, token=None):
    return _call("GET", "/api/openapi/vote_data",
                 token=token, params={"id": activity_id, "page": page, "size": size})


def view_data(activity_id, token=None):
    return _call("GET", "/api/openapi/view_data", token=token, params={"id": activity_id})


def group_update(body, token=None):
    return _call("POST", "/api/openapi/group_update", token=token, json_body=body)


def list_material(cate=None, page=1, size=20, token=None):
    params = {"page": page, "size": size}
    if cate is not None and cate != "":
        params["cate"] = cate
    return _call("GET", "/api/openapi/list_material", token=token, params=params)
