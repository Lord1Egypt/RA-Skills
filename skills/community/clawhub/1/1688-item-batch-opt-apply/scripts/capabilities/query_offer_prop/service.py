"""调用 query_offer_prop 并返回原始业务数据，对比和澄清由主 Agent 完成。"""

import json
import os
import re
import shutil
import subprocess
import tempfile

from _errors import ParamError, ServiceError


def unwrap_result(raw):
    """仅解开 CLI/MCP 包装，保留工具的完整业务响应供主 Agent 判断。"""
    value = raw
    for _ in range(10):
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except ValueError:
                raise ServiceError("属性查询返回非 JSON 数据，不能据此判断核对通过")
        if isinstance(value, list):
            return value
        if not isinstance(value, dict):
            raise ServiceError("属性查询返回结构异常")
        if value.get("isError") is True:
            # 不回显原始报错，避免泄露宿主凭证、店铺信息或内部 URL。
            raise ServiceError("属性查询失败，请检查宿主登录态、工具权限及查询参数")
        if "result" in value and set(value) <= {"result", "jsonrpc", "id"}:
            value = value["result"]
        elif "structuredContent" in value:
            value = value["structuredContent"]
        elif "content" in value and isinstance(value["content"], list):
            blocks = value["content"]
            if not isinstance(blocks, list):
                raise ServiceError("属性查询返回的 MCP 内容格式异常")
            texts = [b.get("text") for b in blocks if isinstance(b, dict)
                     and b.get("type") == "text" and isinstance(b.get("text"), str)]
            if len(texts) != 1:
                raise ServiceError("属性查询未返回唯一的 JSON 结果")
            value = texts[0]
        else:
            return value
    raise ServiceError("属性查询响应嵌套异常")


def query_offer_properties(items):
    """调用 query_offer_prop；不重试、不写商品、不自行补充身份字段。"""
    executable = shutil.which("accio-mcp-cli")
    if not executable:
        raise ServiceError("accio-mcp-cli 不可用，请在 Accio 宿主环境中运行")
    path = None
    try:
        fd, path = tempfile.mkstemp(prefix="batch-cpv-", suffix=".json")
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump({"items": items}, stream, ensure_ascii=False)
        result = subprocess.run(
            [executable, "call", "query_offer_prop", "--json-file", path, "--raw"],
            shell=False, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace",
            timeout=60, check=False,
        )
        if result.returncode != 0:
            raise ServiceError("属性查询调用失败，请检查宿主登录态及 CLI 是否支持 --json-file")
        return unwrap_result(result.stdout)
    except subprocess.TimeoutExpired:
        raise ServiceError("属性查询超时，当前商品尚未通过应用前核对")
    except OSError:
        raise ServiceError("属性查询启动失败，请检查 CLI 和临时目录权限")
    finally:
        if path:
            try:
                os.unlink(path)
            except OSError:
                pass


def normalize_items(items_json):
    """校验最多 20 个唯一商品及非空匹配词；避免意外查询全量 CPV。"""
    try:
        items = json.loads(items_json)
    except (TypeError, ValueError):
        raise ParamError("--items 必须是 JSON 数组")
    if not isinstance(items, list) or not 1 <= len(items) <= 20:
        raise ParamError("每次查询必须包含 1 至 20 个商品，更多商品请分批")
    result, seen = [], set()
    for index, item in enumerate(items, 1):
        if not isinstance(item, dict):
            raise ParamError("第 {} 项必须是商品对象".format(index))
        raw_id = item.get("offerId")
        if isinstance(raw_id, bool) or not isinstance(raw_id, (str, int)):
            raise ParamError("第 {} 项缺少合法 offerId".format(index))
        offer_id = str(raw_id).strip()
        if not re.fullmatch(r"[0-9]+", offer_id) or int(offer_id) <= 0:
            raise ParamError("offerId 必须是正整数商品 ID")
        canonical_id = str(int(offer_id))
        if canonical_id in seen:
            raise ParamError("同一商品不能重复，请合并该商品各任务的匹配词")
        names = item.get("propertyNames")
        if (not isinstance(names, list) or not names
                or any(not isinstance(name, str) or not name.strip() for name in names)):
            raise ParamError("propertyNames 必须是非空匹配词数组，不允许意外读取全量属性")
        result.append({"offerId": offer_id,
                       "propertyNames": list(dict.fromkeys(name.strip() for name in names))})
        seen.add(canonical_id)
    return result


def query_offer_prop(items_json):
    """返回定向查询数据；查询成功不代表无差异或可以写入。"""
    items = normalize_items(items_json)
    return {"items": items, "properties": query_offer_properties(items)}
