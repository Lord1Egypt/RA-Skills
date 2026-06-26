from __future__ import annotations

from typing import List, Dict, Any, Optional, Tuple
import time
import json
import sqlite3
import os
import sys
import requests
import collections
import argparse
from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# SQLite 缓存（有效期 7 天）
# ---------------------------------------------------------------------------
DEFAULT_CACHE_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache.db")
DEFAULT_CACHE_TTL_SECONDS = 7 * 24 * 3600  # 7 天


def _get_cache_conn(db_path: str = DEFAULT_CACHE_DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS kv_cache (
            key   TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            ts    REAL NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS attendance_history (
            work_date    TEXT NOT NULL,
            user_id      TEXT NOT NULL,
            user_name    TEXT NOT NULL,
            result_type  TEXT NOT NULL,
            count        INTEGER NOT NULL,
            queried_at   REAL NOT NULL,
            PRIMARY KEY (work_date, user_id, result_type)
        )
        """
    )
    conn.commit()
    return conn


def _cache_get(key: str, db_path: str = DEFAULT_CACHE_DB_PATH) -> Optional[Any]:
    """从缓存读取，如果过期或不存在返回 None。"""
    conn = _get_cache_conn(db_path)
    try:
        row = conn.execute(
            "SELECT value, ts FROM kv_cache WHERE key = ?", (key,)
        ).fetchone()
        if row is None:
            return None
        value_json, ts = row
        if time.time() - ts > DEFAULT_CACHE_TTL_SECONDS:
            conn.execute("DELETE FROM kv_cache WHERE key = ?", (key,))
            conn.commit()
            return None
        return json.loads(value_json)
    finally:
        conn.close()


def _cache_set(key: str, value: Any, db_path: str = DEFAULT_CACHE_DB_PATH) -> None:
    """写入/更新缓存。"""
    conn = _get_cache_conn(db_path)
    try:
        conn.execute(
            "INSERT OR REPLACE INTO kv_cache (key, value, ts) VALUES (?, ?, ?)",
            (key, json.dumps(value, ensure_ascii=False), time.time()),
        )
        conn.commit()
    finally:
        conn.close()

def _save_attendance_history(
    fail_table: Dict[str, "collections.Counter"],
    user_names: Dict[str, str],
    work_date: str,
    db_path: str = DEFAULT_CACHE_DB_PATH,
) -> None:
    """将异常打卡记录保存到 attendance_history 表。"""
    conn = _get_cache_conn(db_path)
    try:
        now = time.time()
        for userid, counter in fail_table.items():
            name = user_names.get(userid, userid)
            for result_type, count in counter.items():
                conn.execute(
                    """INSERT OR REPLACE INTO attendance_history
                       (work_date, user_id, user_name, result_type, count, queried_at)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (work_date, userid, name, result_type, count, now),
                )
        conn.commit()
    finally:
        conn.close()


def _load_attendance_history(
    date_from: str,
    date_to: str,
    db_path: str = DEFAULT_CACHE_DB_PATH,
) -> List[Tuple[str, str, str, str, int]]:
    """读取日期范围内的历史打卡记录。返回 (work_date, user_id, user_name, result_type, count)。"""
    conn = _get_cache_conn(db_path)
    try:
        rows = conn.execute(
            """SELECT work_date, user_id, user_name, result_type, count
               FROM attendance_history
               WHERE work_date >= ? AND work_date <= ?
               ORDER BY work_date, user_name, result_type""",
            (date_from, date_to),
        ).fetchall()
        return rows
    finally:
        conn.close()


def _list_history_dates(
    db_path: str = DEFAULT_CACHE_DB_PATH,
) -> List[Tuple[str, int, str]]:
    """返回所有已存储日期的 (work_date, record_count, last_queried)。"""
    conn = _get_cache_conn(db_path)
    try:
        rows = conn.execute(
            """SELECT work_date, SUM(count), MAX(queried_at)
               FROM attendance_history
               GROUP BY work_date
               ORDER BY work_date""",
        ).fetchall()
        return rows
    finally:
        conn.close()


sign_result_mapping = {
    "NotSigned": "旷工",
    "Normal": "正常打卡",
    "Early": "早退",
    "Late": "迟到",
    "SeriousLate": "严重迟到",
    "Absenteeism": "旷工迟到",
}

class DingTalkAttendanceError(RuntimeError):
    """Raised when DingTalk attendance/list API returns an error."""

class DingTalkTokenError(RuntimeError):
    """Raised when DingTalk token API returns an error."""


def get_attendance_clock_in_results(
    access_token: str,
    work_date_from: str,
    work_date_to: str,
    user_id_list: List[str],
    *,
    limit: int = 50,
    timeout: float = 10.0,
    max_retries: int = 3,
    retry_backoff_sec: float = 0.8,
    session: Optional[requests.Session] = None,
) -> List[Dict[str, Any]]:
    """
    获取企业内员工打卡结果（旧版接口：attendance/list）。

    POST https://oapi.dingtalk.com/attendance/list?access_token=ACCESS_TOKEN
    Body 必填字段：workDateFrom, workDateTo, userIdList, offset, limit  [oai_citation:2‡Tencent Cloud](https://cloud.tencent.com/developer/article/2195536?utm_source=chatgpt.com)

    参数:
        access_token: 通过 gettoken 获取的企业内部应用 access_token
        work_date_from/work_date_to: 查询时间范围，格式通常为 "YYYY-MM-DD HH:mm:ss"  [oai_citation:3‡Tencent Cloud](https://cloud.tencent.com/developer/article/2195536?utm_source=chatgpt.com)
        user_id_list: 用户 userid 列表
        limit: 单次拉取条数（会自动分页）
        timeout/max_retries/retry_backoff_sec/session: 请求控制参数

    返回:
        打卡结果记录列表（每条为 dict），常见字段包括：
        userId / userCheckTime / timeResult / checkType 等  [oai_citation:4‡Tencent Cloud](https://cloud.tencent.com/developer/article/2195536?utm_source=chatgpt.com)

    异常:
        DingTalkAttendanceError: 业务错误（errcode != 0）或响应不合法
        requests.RequestException: 网络错误/超时等
    """
    if not access_token:
        raise ValueError("access_token 不能为空")
    if not user_id_list:
        return []

    url = "https://oapi.dingtalk.com/attendance/list"
    params = {"access_token": access_token}

    s = session or requests.Session()
    results: List[Dict[str, Any]] = []

    offset = 0
    while True:
        body = {
            "workDateFrom": work_date_from,
            "workDateTo": work_date_to,
            "userIdList": user_id_list,
            "offset": offset,
            "limit": limit,
        }

        last_err: Optional[Exception] = None
        for attempt in range(1, max_retries + 1):
            try:
                resp = s.post(url, params=params, json=body, timeout=timeout)
                resp.raise_for_status()
                data = resp.json()

                errcode = data.get("errcode")
                errmsg = data.get("errmsg")

                # 成功：返回 recordresult（list）
                if errcode == 0:
                    page = data.get("recordresult", [])
                    if not isinstance(page, list):
                        raise DingTalkAttendanceError(f"响应格式异常: {data}")

                    results.extend(page)

                    # 分页：如果本页数量 < limit，认为结束；否则 offset 递增继续拉
                    if len(page) < limit:
                        return results
                    offset += limit
                    break

                # 常见“系统繁忙” errcode=-1：退避重试
                if errcode == -1 and attempt < max_retries:
                    time.sleep(retry_backoff_sec * (2 ** (attempt - 1)))
                    continue

                raise DingTalkAttendanceError(
                    f"DingTalk API error: errcode={errcode}, errmsg={errmsg}, raw={data}"
                )

            except (requests.RequestException, ValueError, DingTalkAttendanceError) as e:
                last_err = e
                if attempt < max_retries:
                    time.sleep(retry_backoff_sec * (2 ** (attempt - 1)))
                    continue
                raise

        # 理论上不会到这；防御式处理
        if last_err:
            raise DingTalkAttendanceError(f"获取打卡结果失败: {last_err}")

    # unreachable

def get_dingtalk_orgapp_token(
    appkey: str,
    appsecret: str,
    *,
    timeout: float = 10.0,
    max_retries: int = 3,
    retry_backoff_sec: float = 0.8,
    session: Optional[requests.Session] = None,
) -> Tuple[str, int]:
    """
    获取钉钉企业内部应用 access_token。

    API: GET https://oapi.dingtalk.com/gettoken?appkey=...&appsecret=...&grant_type=client_credential
    成功返回示例：{"errcode":0,"errmsg":"ok","access_token":"xxx","expires_in":7200}
    access_token 默认有效期通常为 7200 秒（2小时）。 [oai_citation:1‡Aliyun Developer Community](https://developer.aliyun.com/ask/532363?utm_source=chatgpt.com)

    参数:
        appkey/appsecret: 钉钉开放平台应用的 AppKey/AppSecret
        timeout: 单次请求超时（秒）
        max_retries: 遇到可重试错误时的最大重试次数（含首次，共 max_retries 次尝试）
        retry_backoff_sec: 重试退避基准时间（秒），指数退避
        session: 可选，复用 requests.Session

    返回:
        (access_token, expires_in)

    异常:
        DingTalkTokenError: 接口返回 errcode != 0 或响应不合法
        requests.RequestException: 网络/超时等请求异常
    """
    if not appkey or not appsecret:
        raise ValueError("appkey/appsecret 不能为空")

    url = "https://oapi.dingtalk.com/gettoken"
    params = {
        "appkey": appkey,
        "appsecret": appsecret,
        "grant_type": "client_credential",
    }

    s = session or requests.Session()

    last_err: Optional[Exception] = None
    for attempt in range(1, max_retries + 1):
        try:
            resp = s.get(url, params=params, timeout=timeout)
            resp.raise_for_status()
            data = resp.json()

            errcode = data.get("errcode")
            errmsg = data.get("errmsg")

            # 成功
            if errcode == 0:
                token = data.get("access_token")
                expires_in = data.get("expires_in")
                if not token or not isinstance(expires_in, int):
                    raise DingTalkTokenError(f"响应缺少字段: {data}")
                return token, expires_in

            # 系统繁忙：官方错误码示例为 errcode=-1，建议稍后重试（一般最多重试几次）。 [oai_citation:2‡open.dingtalk.com](https://open.dingtalk.com/document/app/server-api-error-codes-1?utm_source=chatgpt.com)
            if errcode == -1 and attempt < max_retries:
                time.sleep(retry_backoff_sec * (2 ** (attempt - 1)))
                continue

            raise DingTalkTokenError(f"DingTalk API error: errcode={errcode}, errmsg={errmsg}, raw={data}")

        except (requests.RequestException, ValueError, DingTalkTokenError) as e:
            last_err = e
            # 网络/解析错误也做有限重试
            if attempt < max_retries:
                time.sleep(retry_backoff_sec * (2 ** (attempt - 1)))
                continue
            raise

    # 理论上不会走到这里
    raise DingTalkTokenError(f"获取 token 失败: {last_err}")

class DingTalkDepartmentError(RuntimeError):
    """Raised when DingTalk department/list API returns an error."""


def get_department_list(
    access_token: str,
    *,
    dept_id: int = 1,
    language: str = "zh_CN",
    fetch_all: bool = False,
    timeout: float = 10.0,
    max_retries: int = 3,
    retry_backoff_sec: float = 0.8,
    session: Optional[requests.Session] = None,
) -> List[Dict[str, Any]]:
    """
    获取部门列表（旧版：根据父部门ID获取下一级部门列表）。
    GET https://oapi.dingtalk.com/department/list?access_token=...&id=...&language=...

    - 该接口只返回“当前部门的下一级部门”，不直接返回全部层级子部门。 [oai_citation:2‡DingTalk Open Platform](https://open.dingtalk.com/document/development/user-management-acquires-the-list-departments?utm_source=chatgpt.com)
    - 根部门通常传 dept_id=1。 [oai_citation:3‡FanRuan Help Document](https://help.fanruan.com/finedatalink/doc-view-516.html)

    参数:
        access_token: 应用 access_token
        dept_id: 父部门ID（根部门通常为1）
        language: 返回语言，常用 "zh_CN"
        fetch_all: True 时自动遍历所有子部门，返回全量部门（通过循环调用实现）
        timeout/max_retries/retry_backoff_sec/session: 请求控制参数

    返回:
        部门列表，每个元素是 dict（包含 dept_id / name / parentid 等字段，具体以接口返回为准）
    """
    if not access_token:
        raise ValueError("access_token 不能为空")

    url = "https://oapi.dingtalk.com/department/list"
    s = session or requests.Session()

    def _call_once(parent_id: int) -> List[Dict[str, Any]]:
        params = {
            "access_token": access_token,
            "id": parent_id,
            "language": language,
        }

        last_err: Optional[Exception] = None
        for attempt in range(1, max_retries + 1):
            try:
                resp = s.get(url, params=params, timeout=timeout)
                resp.raise_for_status()
                data = resp.json()

                errcode = data.get("errcode")
                errmsg = data.get("errmsg")

                if errcode == 0:
                    dept_list = data.get("department", [])
                    if not isinstance(dept_list, list):
                        raise DingTalkDepartmentError(f"响应格式异常: {data}")
                    return dept_list

                # 系统繁忙（常见 -1）：退避重试
                if errcode == -1 and attempt < max_retries:
                    time.sleep(retry_backoff_sec * (2 ** (attempt - 1)))
                    continue

                raise DingTalkDepartmentError(
                    f"DingTalk API error: errcode={errcode}, errmsg={errmsg}, raw={data}"
                )

            except (requests.RequestException, ValueError, DingTalkDepartmentError) as e:
                last_err = e
                if attempt < max_retries:
                    time.sleep(retry_backoff_sec * (2 ** (attempt - 1)))
                    continue
                raise

        raise DingTalkDepartmentError(f"获取部门列表失败: {last_err}")

    # 只取一层
    if not fetch_all:
        return _call_once(dept_id)

    # 拉全量：BFS 遍历
    all_depts: List[Dict[str, Any]] = []
    seen: set[int] = set()
    queue: List[int] = [dept_id]

    while queue:
        parent = queue.pop(0)
        children = _call_once(parent)

        for d in children:
            # 兼容 dept_id 字段可能是 "id"/"dept_id"
            cid = d.get("id", d.get("dept_id"))
            if isinstance(cid, int) and cid not in seen:
                seen.add(cid)
                all_depts.append(d)
                queue.append(cid)

    return all_depts

class DingTalkDeptUserIdsError(RuntimeError):
    """Raised when DingTalk topapi/user/listid returns an error."""


def get_department_userids(
    access_token: str,
    dept_id: int,
    *,
    cursor: int = 0,
    size: int = 100,
    fetch_all: bool = True,
    timeout: float = 10.0,
    max_retries: int = 3,
    retry_backoff_sec: float = 0.8,
    session: Optional[requests.Session] = None,
) -> List[str]:
    """
    获取部门用户 userId 列表（topapi/user/listid）。

    Endpoint:
      POST https://oapi.dingtalk.com/topapi/user/listid?access_token=ACCESS_TOKEN  [oai_citation:1‡dalianhg.com](https://dalianhg.com/confluence/display/PROD/01-Dingtalk%2BSettings/?utm_source=chatgpt.com)
    Body（常用）:
      dept_id: 部门ID
      cursor: 分页游标
      size: 分页大小  [oai_citation:2‡DingTalk Open Platform](https://open.dingtalk.com/document/development/query-the-list-of-department-userids?utm_source=chatgpt.com)

    参数:
      access_token: gettoken 获取的 token
      dept_id: 部门ID（根部门通常为 1）
      cursor/size: 分页参数（fetch_all=False 时使用）
      fetch_all: True 自动分页拉取该部门下全部 userid
    返回:
      userid 列表
    """
    if not access_token:
        raise ValueError("access_token 不能为空")
    if not isinstance(dept_id, int) or dept_id <= 0:
        raise ValueError("dept_id 必须为正整数")

    url = "https://oapi.dingtalk.com/topapi/user/listid"
    params = {"access_token": access_token}
    s = session or requests.Session()

    def _post_once(cur: int) -> tuple[List[str], Optional[int], Optional[bool]]:
        body = {"dept_id": dept_id, "cursor": cur, "size": size}

        last_err: Optional[Exception] = None
        for attempt in range(1, max_retries + 1):
            try:
                resp = s.post(url, params=params, json=body, timeout=timeout)
                resp.raise_for_status()
                data = resp.json()

                errcode = data.get("errcode")
                errmsg = data.get("errmsg")
                if errcode == 0:
                    result = data.get("result") or {}
                    userid_list = result.get("userid_list") or []
                    if not isinstance(userid_list, list):
                        raise DingTalkDeptUserIdsError(f"响应格式异常: {data}")

                    # 不同版本字段可能略有差异：可能有 next_cursor/has_more，也可能没有
                    next_cursor = result.get("next_cursor")
                    has_more = result.get("has_more")
                    if next_cursor is not None and not isinstance(next_cursor, int):
                        next_cursor = None
                    if has_more is not None and not isinstance(has_more, bool):
                        has_more = None

                    return [str(x) for x in userid_list], next_cursor, has_more

                # 系统繁忙：常见 errcode=-1，退避重试
                if errcode == -1 and attempt < max_retries:
                    time.sleep(retry_backoff_sec * (2 ** (attempt - 1)))
                    continue

                raise DingTalkDeptUserIdsError(
                    f"DingTalk API error: errcode={errcode}, errmsg={errmsg}, raw={data}"
                )

            except (requests.RequestException, ValueError, DingTalkDeptUserIdsError) as e:
                last_err = e
                if attempt < max_retries:
                    time.sleep(retry_backoff_sec * (2 ** (attempt - 1)))
                    continue
                raise

        raise DingTalkDeptUserIdsError(f"请求失败: {last_err}")

    if not fetch_all:
        userids, _, _ = _post_once(cursor)
        return userids

    # 自动分页
    all_ids: List[str] = []
    cur = cursor
    while True:
        page_ids, next_cur, has_more = _post_once(cur)
        all_ids.extend(page_ids)

        # 优先使用 has_more/next_cursor；如果响应没给，就用“返回数量 < size”判断结束
        if has_more is False:
            break
        if has_more is True and next_cur is not None:
            cur = next_cur
            continue
        if next_cur is not None and next_cur != cur:
            cur = next_cur
            continue
        if len(page_ids) < size:
            break

        # 兜底：避免死循环
        cur += size

    return all_ids

class DingTalkAttendanceGroupMembersError(RuntimeError):
    """Raised when DingTalk attendance group memberusers/list API returns an error."""


def get_attendance_group_userids(
    access_token: str,
    *,
    group_id: int,
    op_user_id: str,
    cursor: int = 0,
    size: int = 100,
    fetch_all: bool = True,
    timeout: float = 10.0,
    max_retries: int = 3,
    retry_backoff_sec: float = 0.8,
    session: Optional[requests.Session] = None,
) -> List[str]:
    """
    获取某个考勤组下参与考勤人员的 userId 列表（分页）。

    Endpoint:
      POST https://oapi.dingtalk.com/topapi/attendance/group/memberusers/list?access_token=ACCESS_TOKEN  [oai_citation:2‡s.apifox.cn](https://s.apifox.cn/apidoc/docs-site/467052/api-9093263)

    说明:
      - 接口用于“分页获取某个考勤组下所有员工的 userId”。 [oai_citation:3‡s.apifox.cn](https://s.apifox.cn/apidoc/docs-site/467052/api-9093263)
      - 若考勤组里配置了部门参与考勤，接口会返回部门（含子部门）下员工的 userId（不返回部门ID）。 [oai_citation:4‡s.apifox.cn](https://s.apifox.cn/apidoc/docs-site/467052/api-9093263)

    参数:
      access_token: 企业内部应用 token
      group_id: 考勤组ID
      op_user_id: 操作人 userId（接口示例字段） [oai_citation:5‡s.apifox.cn](https://s.apifox.cn/apidoc/docs-site/467052/api-9093263)
      cursor/size: 分页参数（fetch_all=False 时可手动控制；fetch_all=True 时自动推进）
      fetch_all: 是否自动分页拉全量
    返回:
      userId 列表
    """
    if not access_token:
        raise ValueError("access_token 不能为空")
    if not isinstance(group_id, int) or group_id <= 0:
        raise ValueError("group_id 必须为正整数")
    if not op_user_id:
        raise ValueError("op_user_id 不能为空")

    url = "https://oapi.dingtalk.com/topapi/attendance/group/memberusers/list"
    params = {"access_token": access_token}
    s = session or requests.Session()

    def _post_once(cur: int) -> Tuple[List[str], Optional[int], Optional[bool]]:
        body = {
            "op_user_id": op_user_id,
            "group_id": group_id,
            "cursor": cur,
            "size": size,
        }

        last_err: Optional[Exception] = None
        for attempt in range(1, max_retries + 1):
            try:
                resp = s.post(url, params=params, json=body, timeout=timeout)
                resp.raise_for_status()
                data = resp.json()

                errcode = data.get("errcode")
                errmsg = data.get("errmsg")
                if errcode == 0:
                    result_obj = data.get("result") or {}
                    # 响应示例：result.cursor / result.has_more / result.result(=userId数组)  [oai_citation:6‡s.apifox.cn](https://s.apifox.cn/apidoc/docs-site/467052/api-9093263)
                    userids = result_obj.get("result") or []
                    if not isinstance(userids, list):
                        raise DingTalkAttendanceGroupMembersError(f"响应格式异常: {data}")

                    next_cursor = result_obj.get("cursor")
                    has_more = result_obj.get("has_more")

                    if next_cursor is not None and not isinstance(next_cursor, int):
                        next_cursor = None
                    if has_more is not None and not isinstance(has_more, bool):
                        has_more = None

                    return [str(x) for x in userids], next_cursor, has_more

                # 系统繁忙常见 errcode=-1：退避重试（与其他钉钉接口一致的处理策略）
                if errcode == -1 and attempt < max_retries:
                    time.sleep(retry_backoff_sec * (2 ** (attempt - 1)))
                    continue

                raise DingTalkAttendanceGroupMembersError(
                    f"DingTalk API error: errcode={errcode}, errmsg={errmsg}, raw={data}"
                )

            except (requests.RequestException, ValueError, DingTalkAttendanceGroupMembersError) as e:
                last_err = e
                if attempt < max_retries:
                    time.sleep(retry_backoff_sec * (2 ** (attempt - 1)))
                    continue
                raise

        raise DingTalkAttendanceGroupMembersError(f"请求失败: {last_err}")

    if not fetch_all:
        userids, _, _ = _post_once(cursor)
        return userids

    all_ids: List[str] = []
    cur = cursor
    seen_guard = 0

    while True:
        page_ids, next_cur, has_more = _post_once(cur)
        all_ids.extend(page_ids)

        if has_more is False:
            break

        # 优先用服务端返回的 cursor 推进（响应示例里存在 cursor/has_more） [oai_citation:7‡s.apifox.cn](https://s.apifox.cn/apidoc/docs-site/467052/api-9093263)
        if has_more is True and next_cur is not None:
            if next_cur == cur:
                # 防死循环
                seen_guard += 1
                if seen_guard >= 3:
                    break
            cur = next_cur
            continue

        # 兜底：如果没给 has_more，就用“本页数量 < size”判断结束
        if len(page_ids) < size:
            break

        # 再兜底：按 size 推进
        cur += size

    return all_ids

class DingTalkGetByMobileError(RuntimeError):
    """Raised when DingTalk topapi/v2/user/getbymobile returns an error."""


def get_userid_by_mobile(
    access_token: str,
    mobile: str,
    *,
    timeout: float = 10.0,
    max_retries: int = 3,
    retry_backoff_sec: float = 0.8,
    session: Optional[requests.Session] = None,
) -> Dict[str, Any]:
    """
    根据手机号查询企业账号用户的 userid。

    POST https://oapi.dingtalk.com/topapi/v2/user/getbymobile?access_token=ACCESS_TOKEN
    Body: {"mobile": "185xxxx7676"}  [oai_citation:1‡dingtalk.apifox.cn](https://dingtalk.apifox.cn/api-9093156)

    返回:
      {
        "userid": str,  # 主 userid
        "exclusive_account_userid_list": List[str] | None  # 若存在专属账号 userid 列表
      }

    注意:
      - 只能查询“在职员工”；员工离职时无法通过手机号获取 userid。 [oai_citation:2‡dingtalk.apifox.cn](https://dingtalk.apifox.cn/api-9093156)
      - 常见错误码：40104(企业中无效手机号)、60121(未找到用户)、-1(系统繁忙)。 [oai_citation:3‡dingtalk.apifox.cn](https://dingtalk.apifox.cn/api-9093156)
    """
    if not access_token:
        raise ValueError("access_token 不能为空")
    if not mobile:
        raise ValueError("mobile 不能为空")

    url = "https://oapi.dingtalk.com/topapi/v2/user/getbymobile"
    params = {"access_token": access_token}
    body = {"mobile": mobile}

    s = session or requests.Session()

    last_err: Optional[Exception] = None
    for attempt in range(1, max_retries + 1):
        try:
            resp = s.post(url, params=params, json=body, timeout=timeout)
            resp.raise_for_status()
            data = resp.json()

            errcode = data.get("errcode")
            errmsg = data.get("errmsg")

            # 文档示例里 errcode 可能是字符串 "0"，因此兼容 str/int  [oai_citation:4‡dingtalk.apifox.cn](https://dingtalk.apifox.cn/api-9093156)
            if str(errcode) == "0":
                result = data.get("result") or {}
                userid = result.get("userid")
                if not userid:
                    raise DingTalkGetByMobileError(f"响应缺少 userid: {data}")

                exclusive_raw = result.get("exclusive_account_userid_list")
                exclusive_list: Optional[List[str]] = None
                # 示例中该字段是字符串形式的 JSON 数组，例如 "[\"zxxxx\",\"lixxxi\"]"  [oai_citation:5‡dingtalk.apifox.cn](https://dingtalk.apifox.cn/api-9093156)
                if isinstance(exclusive_raw, str) and exclusive_raw.strip():
                    try:
                        parsed = json.loads(exclusive_raw)
                        if isinstance(parsed, list):
                            exclusive_list = [str(x) for x in parsed]
                    except Exception:
                        # 不强制失败：保留 None
                        exclusive_list = None

                return {"userid": str(userid), "exclusive_account_userid_list": exclusive_list}

            # 系统繁忙：-1，退避重试  [oai_citation:6‡dingtalk.apifox.cn](https://dingtalk.apifox.cn/api-9093156)
            if str(errcode) == "-1" and attempt < max_retries:
                time.sleep(retry_backoff_sec * (2 ** (attempt - 1)))
                continue

            raise DingTalkGetByMobileError(
                f"DingTalk API error: errcode={errcode}, errmsg={errmsg}, raw={data}"
            )

        except (requests.RequestException, ValueError, DingTalkGetByMobileError) as e:
            last_err = e
            if attempt < max_retries:
                time.sleep(retry_backoff_sec * (2 ** (attempt - 1)))
                continue
            raise

    raise DingTalkGetByMobileError(f"查询失败: {last_err}")

class DingTalkAttendanceGroupsError(RuntimeError):
    """Raised when DingTalk attendance/getsimplegroups API returns an error."""


def batch_get_attendance_group_details(
    access_token: str,
    *,
    offset: int = 0,
    size: int = 10,
    fetch_all: bool = True,
    timeout: float = 10.0,
    max_retries: int = 3,
    retry_backoff_sec: float = 0.8,
    session: Optional[requests.Session] = None,
) -> List[Dict[str, Any]]:
    """
    批量获取考勤组详情（topapi/attendance/getsimplegroups），支持自动分页。

    POST https://oapi.dingtalk.com/topapi/attendance/getsimplegroups?access_token=ACCESS_TOKEN  [oai_citation:3‡jaq-doc.alibaba.com](https://jaq-doc.alibaba.com/docs/api.htm?apiId=36983)

    Body:
      offset: 偏移位置（默认 0）  [oai_citation:4‡jaq-doc.alibaba.com](https://jaq-doc.alibaba.com/docs/api.htm?apiId=36983)
      size: 分页大小（默认 10，最大 10）  [oai_citation:5‡jaq-doc.alibaba.com](https://jaq-doc.alibaba.com/docs/api.htm?apiId=36983)

    Response:
      result.has_more: 是否还有下一页  [oai_citation:6‡jaq-doc.alibaba.com](https://jaq-doc.alibaba.com/docs/api.htm?apiId=36983)
      result.groups: 考勤组详情列表  [oai_citation:7‡jaq-doc.alibaba.com](https://jaq-doc.alibaba.com/docs/api.htm?apiId=36983)
    """
    if not access_token:
        raise ValueError("access_token 不能为空")
    if size <= 0:
        raise ValueError("size 必须为正整数")
    if size > 10:
        raise ValueError("size 最大为 10（钉钉接口限制）")

    url = "https://oapi.dingtalk.com/topapi/attendance/getsimplegroups"
    params = {"access_token": access_token}
    s = session or requests.Session()

    def _post_once(off: int) -> Tuple[List[Dict[str, Any]], Optional[bool]]:
        body = {"offset": off, "size": size}

        last_err: Optional[Exception] = None
        for attempt in range(1, max_retries + 1):
            try:
                resp = s.post(url, params=params, json=body, timeout=timeout)
                resp.raise_for_status()
                data = resp.json()

                errcode = data.get("errcode")
                errmsg = data.get("errmsg")

                if errcode == 0:
                    result = data.get("result") or {}
                    groups = result.get("groups") or []
                    has_more = result.get("has_more")

                    if not isinstance(groups, list):
                        raise DingTalkAttendanceGroupsError(f"响应格式异常: {data}")
                    if has_more is not None and not isinstance(has_more, bool):
                        has_more = None

                    return groups, has_more

                # 系统繁忙常见 errcode=-1：退避重试（与钉钉其他接口一致的处理策略）
                if errcode == -1 and attempt < max_retries:
                    time.sleep(retry_backoff_sec * (2 ** (attempt - 1)))
                    continue

                raise DingTalkAttendanceGroupsError(
                    f"DingTalk API error: errcode={errcode}, errmsg={errmsg}, raw={data}"
                )

            except (requests.RequestException, ValueError, DingTalkAttendanceGroupsError) as e:
                last_err = e
                if attempt < max_retries:
                    time.sleep(retry_backoff_sec * (2 ** (attempt - 1)))
                    continue
                raise

        raise DingTalkAttendanceGroupsError(f"请求失败: {last_err}")

    # 只取一页
    if not fetch_all:
        groups, _ = _post_once(offset)
        return groups

    # 自动分页：offset 递增 size
    all_groups: List[Dict[str, Any]] = []
    off = offset
    while True:
        groups, has_more = _post_once(off)
        all_groups.extend(groups)

        # 优先根据 has_more 判断；如果没给 has_more，就用“本页条数 < size”判断
        if has_more is False:
            break
        if has_more is True:
            off += size
            continue
        if len(groups) < size:
            break

        off += size

    return all_groups

class DingTalkUserDetailsError(RuntimeError):
    """Raised when DingTalk topapi/v2/user/get returns an error."""


def get_user_details(
    access_token: str,
    userid: str,
    *,
    language: str = "zh_CN",
    timeout: float = 10.0,
    max_retries: int = 3,
    retry_backoff_sec: float = 0.8,
    session: Optional[requests.Session] = None,
) -> Dict[str, Any]:
    """
    查询用户详情（topapi/v2/user/get）。

    POST https://oapi.dingtalk.com/topapi/v2/user/get?access_token=ACCESS_TOKEN  [oai_citation:1‡DingTalk Open Platform](https://open.dingtalk.com/document/orgapp-server/query-user-details?utm_source=chatgpt.com)
    Body:
      - userid: 用户userid（必填）
      - language: 返回语言（可选，常用 zh_CN）  [oai_citation:2‡DingTalk API](https://dingtalk.apifox.cn/api-139715614?utm_source=chatgpt.com)

    返回:
      用户详情 dict（即响应中的 result 字段）。
    """
    if not access_token:
        raise ValueError("access_token 不能为空")
    if not userid:
        raise ValueError("userid 不能为空")

    url = "https://oapi.dingtalk.com/topapi/v2/user/get"
    params = {"access_token": access_token}
    body = {"userid": userid, "language": language}

    s = session or requests.Session()

    last_err: Optional[Exception] = None
    for attempt in range(1, max_retries + 1):
        try:
            resp = s.post(url, params=params, json=body, timeout=timeout)
            resp.raise_for_status()
            data = resp.json()

            errcode = data.get("errcode")
            errmsg = data.get("errmsg")

            # errcode 有时是 int/str，统一按字符串判断
            if str(errcode) == "0":
                result = data.get("result")
                if not isinstance(result, dict):
                    raise DingTalkUserDetailsError(f"响应缺少/异常 result: {data}")
                return result

            # 系统繁忙（常见 -1）：退避重试
            if str(errcode) == "-1" and attempt < max_retries:
                time.sleep(retry_backoff_sec * (2 ** (attempt - 1)))
                continue

            raise DingTalkUserDetailsError(
                f"DingTalk API error: errcode={errcode}, errmsg={errmsg}, raw={data}"
            )

        except (requests.RequestException, ValueError, DingTalkUserDetailsError) as e:
            last_err = e
            if attempt < max_retries:
                time.sleep(retry_backoff_sec * (2 ** (attempt - 1)))
                continue
            raise

    raise DingTalkUserDetailsError(f"查询用户详情失败: {last_err}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-time", type=str, default="2026-03-03 07:00:00", help="查询打卡记录的开始时间，格式 YYYY-MM-DD HH:MM:SS")
    parser.add_argument("--end-time", type=str, default="2026-03-03 18:59:59", help="查询打卡记录的结束时间，格式 YYYY-MM-DD HH:MM:SS")
    parser.add_argument("--cache-file", type=str, default=DEFAULT_CACHE_DB_PATH, help="本地缓存文件路径，用于缓存 token/userid 等信息，避免重复调用接口")
    parser.add_argument("--history", action="store_true", help="从本地 SQLite 历史记录中读取，不调用 API")
    parser.add_argument("--list-history", action="store_true", help="列出本地已查询过的日期及记录数")
    args = parser.parse_args()

    # --- --list-history：列出已有历史数据，不需要 API ---
    if args.list_history:
        rows = _list_history_dates(db_path=args.cache_file)
        if not rows:
            print("暂无历史查询记录。")
        else:
            print(f"{'日期':<14} {'异常次数':<10} {'最后查询时间'}")
            print("-" * 50)
            for work_date, total_count, last_ts in rows:
                last_time = datetime.fromtimestamp(last_ts).strftime("%Y-%m-%d %H:%M:%S")
                print(f"{work_date:<14} {int(total_count):<10} {last_time}")
        sys.exit(0)

    # --- --history：从本地数据库读取，不调用 API ---
    if args.history:
        date_from = args.start_time[:10]
        date_to = args.end_time[:10]
        rows = _load_attendance_history(date_from, date_to, db_path=args.cache_file)
        if not rows:
            print(f"本地无 {date_from} 至 {date_to} 的历史记录。可去掉 --history 参数从 API 查询。")
            sys.exit(0)

        # 检查范围内是否有缺失日期并警告
        stored_dates = set(r[0] for r in rows)
        d = datetime.strptime(date_from, "%Y-%m-%d")
        d_end = datetime.strptime(date_to, "%Y-%m-%d")
        missing = []
        while d <= d_end:
            ds = d.strftime("%Y-%m-%d")
            if ds not in stored_dates:
                missing.append(ds)
            d += timedelta(days=1)
        if missing:
            print(f"[警告] 以下日期在本地无记录（可能未查询过或当日全员正常）: {', '.join(missing)}")
            print()

        # 聚合并输出（与 API 模式输出格式一致）
        by_user: Dict[str, collections.Counter] = {}
        user_name_map: Dict[str, str] = {}
        for work_date, user_id, user_name, result_type, count in rows:
            if user_id not in by_user:
                by_user[user_id] = collections.Counter()
            by_user[user_id][result_type] += count
            user_name_map[user_id] = user_name
        for user_id, counter in by_user.items():
            for result, count in counter.most_common():
                print(f"{user_name_map[user_id]} 打卡结果 {result} 出现 {count} 次")
        sys.exit(0)

    # --- 正常 API 查询模式 ---
    appkey = os.getenv("DINGTALK_APPKEY")
    appsecret = os.getenv("DINGTALK_APPSECRET")
    admin_phone = os.getenv("ADMIN_PHONE")
    token, expires_in = get_dingtalk_orgapp_token(appkey, appsecret)

    # --- 管理员用户 ID（缓存 key: admin_userid:<phone>）---
    cache_key_admin = f"admin_userid:{admin_phone}"
    my_userid = _cache_get(cache_key_admin)
    if my_userid is None:
        my_userid = get_userid_by_mobile(token, admin_phone)["userid"]
        _cache_set(cache_key_admin, my_userid)

    # --- 考勤组 group_id（缓存 key: attendance_group_id）---
    cache_key_group = "attendance_group_id"
    group_id = _cache_get(cache_key_group)
    if group_id is None:
        group_id = batch_get_attendance_group_details(token, fetch_all=True)[0]['group_id']
        _cache_set(cache_key_group, group_id)

    # --- 考勤组用户 ID 列表（缓存 key: attendance_group_userids:<group_id>）---
    cache_key_userids = f"attendance_group_userids:{group_id}"
    userid_list = _cache_get(cache_key_userids)
    if userid_list is None:
        userid_list = get_attendance_group_userids(token, group_id=group_id, op_user_id=my_userid, fetch_all=True)
        _cache_set(cache_key_userids, userid_list)

    records = get_attendance_clock_in_results(token, args.start_time, args.end_time, userid_list)

    # 按日期分组统计异常
    fail_by_date: Dict[str, Dict[str, collections.Counter]] = {}
    for record in records:
        if record["checkType"] == "OnDuty" and record['timeResult'] != "Normal":
            work_dt = datetime.fromtimestamp(record["workDate"] / 1000)
            date_str = work_dt.strftime("%Y-%m-%d")
            if date_str not in fail_by_date:
                fail_by_date[date_str] = {}
            if record["userId"] not in fail_by_date[date_str]:
                fail_by_date[date_str][record["userId"]] = collections.Counter()
            fail_by_date[date_str][record["userId"]][sign_result_mapping[record["timeResult"]]] += 1

    # 收集所有异常用户的姓名
    all_fail_userids = set()
    for date_fails in fail_by_date.values():
        all_fail_userids.update(date_fails.keys())

    user_names: Dict[str, str] = {}
    for userid in all_fail_userids:
        cache_key_user = f"user_name:{userid}"
        user_name = _cache_get(cache_key_user)
        if user_name is None:
            user = get_user_details(token, userid)
            user_name = user['name']
            _cache_set(cache_key_user, user_name)
        user_names[userid] = user_name

    # 输出结果（保持原有格式兼容）
    merged_fail: Dict[str, collections.Counter] = {}
    for date_str in sorted(fail_by_date):
        for userid, counter in fail_by_date[date_str].items():
            if userid not in merged_fail:
                merged_fail[userid] = collections.Counter()
            merged_fail[userid] += counter
    for userid, counter in merged_fail.items():
        for result, count in counter.most_common():
            print(f"{user_names[userid]} 打卡结果 {result} 出现 {count} 次")

    # 自动保存到历史记录
    for date_str, date_fails in fail_by_date.items():
        _save_attendance_history(date_fails, user_names, date_str, db_path=args.cache_file)
        