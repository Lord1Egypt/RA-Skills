#!/usr/bin/env python3
"""
validate_employee_params.py
对 agentSubmitTask 请求体做结构与取值层的硬约束校验（pre-flight gate）。
覆盖 AiWa / Frank / Fran / Lisa 的所有结构强约束与固定值规则。

注：数字员工 Toby（TikTok 视频生成与发布）已抽离到独立技能 deepsop-tiktokflow，本脚本不再支持。

用法:
  python3 validate_employee_params.py '<完整请求体 JSON 字符串>'

输入：和 POST /ai/presetEmployee/submitTask 完全一致的请求体（含 collaborationSubmitTaskParam + completed）。

输出（stdout，单行 JSON）:
  {
    "ok": false,
    "summary": "X 项结构/取值校验失败，禁止提交",
    "errors": [
      {"path":"...employeeList","code":"INTERNAL_VAR_LEAK",
       "msg":"...","suggestion":"..."}
    ]
  }

退出码:
  0 — 全部通过
  1 — 至少一项失败
  2 — 输入格式错误

注意：
- 本脚本只覆盖 LLM 高频犯错点（key 大小写、必填漏字段、固定值、类型、Step1 内部变量泄漏）。
- Lisa 的 templateParamList 内容校验（time/unit_name 等具体格式）由 validate_sms_template_params.py 完成，本脚本只验数组结构与每项三键齐全。
- 业务级校验（如 templateCode 是否存在于用户账号）需要调接口，不在本脚本范围。
"""

import json
import sys
from typing import Any


VALID_EMPLOYEES = {"AiWa", "Frank", "Fran", "Lisa"}
INTERNAL_VARS = {"employeeList", "language", "totalTarget"}


# ── 通用工具 ────────────────────────────────────────────────────────────────


def err(errors: list, path: str, code: str, msg: str, suggestion: str | None = None) -> None:
    item: dict[str, Any] = {"path": path, "code": code, "msg": msg}
    if suggestion:
        item["suggestion"] = suggestion
    errors.append(item)


def require_key(d: Any, key: str, path: str, errors: list) -> bool:
    if not isinstance(d, dict):
        err(errors, path, "NOT_OBJECT", f"{path} 必须是对象")
        return False
    if key not in d:
        err(errors, f"{path}.{key}", "MISSING_KEY", f"缺少必填字段 {key!r}")
        return False
    return True


def require_type(value: Any, path: str, expected: type | tuple, errors: list, *, type_label: str) -> bool:
    if not isinstance(value, expected):
        err(errors, path, "WRONG_TYPE", f"{path} 必须是 {type_label}，当前为 {type(value).__name__}")
        return False
    return True


def require_value(value: Any, path: str, expected: Any, errors: list) -> bool:
    if value != expected:
        err(
            errors,
            path,
            "WRONG_VALUE",
            f"{path} 必须固定为 {expected!r}，当前为 {value!r}",
            f"改为 {expected!r}",
        )
        return False
    return True


def detect_camel_typo(actual: str, valid_set: set[str]) -> str | None:
    """对疑似拼写/大小写错误的员工 key，定位最可能的正确名。"""
    a = actual.lower().strip()
    for v in valid_set:
        vl = v.lower()
        if a == vl or a.startswith(vl) or vl.startswith(a):
            return v
    return None


# ── 顶层结构校验 ─────────────────────────────────────────────────────────────


def validate_top_level(body: dict, errors: list) -> dict | None:
    if not isinstance(body, dict):
        err(errors, "<root>", "NOT_OBJECT", "请求体必须是对象")
        return None

    # Step 1/2 内部变量泄漏到根级
    for k in INTERNAL_VARS:
        if k in body:
            err(
                errors,
                f"<root>.{k}",
                "INTERNAL_VAR_LEAK",
                f"{k!r} 是 Step 1/2 内部解析变量，禁止出现在请求体根级",
                "删除该字段；其值应只流入 employeeParams 对应员工子对象的指定字段",
            )

    # completed 应为 true（按示例）
    if body.get("completed") is not True:
        err(errors, "<root>.completed", "WRONG_VALUE", "completed 必须是布尔 true", "改为 true")

    if not require_key(body, "collaborationSubmitTaskParam", "<root>", errors):
        return None
    cstp = body["collaborationSubmitTaskParam"]
    if not isinstance(cstp, dict):
        err(errors, "collaborationSubmitTaskParam", "NOT_OBJECT", "必须是对象")
        return None

    # cstp 内部不能再出现内部变量
    for k in INTERNAL_VARS:
        if k in cstp:
            err(
                errors,
                f"collaborationSubmitTaskParam.{k}",
                "INTERNAL_VAR_LEAK",
                f"{k!r} 是 Step 1/2 内部解析变量，禁止出现在 collaborationSubmitTaskParam 层",
                "删除该字段；其值应下沉到对应员工子对象内",
            )

    # cstp 必填基本字段
    require_key(cstp, "taskName", "collaborationSubmitTaskParam", errors)
    require_key(cstp, "taskDescription", "collaborationSubmitTaskParam", errors)

    # executionMode 必须是数字 1
    if "executionMode" in cstp:
        em = cstp["executionMode"]
        if em != 1 or isinstance(em, bool):
            err(
                errors,
                "collaborationSubmitTaskParam.executionMode",
                "EXECMODE_NOT_1",
                f"executionMode 必须是数字 1，当前为 {em!r}（type={type(em).__name__}）",
                "改为整数 1（不要用字符串 \"1\" / 布尔 true / 中文 \"定额任务\"）",
            )
    else:
        err(errors, "collaborationSubmitTaskParam.executionMode", "MISSING_KEY", "缺少 executionMode")

    # currentModule 固定为 "content"
    if "currentModule" in cstp:
        if cstp["currentModule"] != "content":
            err(
                errors,
                "collaborationSubmitTaskParam.currentModule",
                "WRONG_VALUE",
                f"currentModule 必须固定为 \"content\"，当前为 {cstp['currentModule']!r}",
                '改为 "content"',
            )
    else:
        err(errors, "collaborationSubmitTaskParam.currentModule", "MISSING_KEY", "缺少 currentModule")

    return cstp


def validate_employee_params_dict(cstp: dict, errors: list) -> dict | None:
    if not require_key(cstp, "employeeParams", "collaborationSubmitTaskParam", errors):
        return None
    ep = cstp["employeeParams"]
    if not isinstance(ep, dict):
        err(errors, "...employeeParams", "NOT_OBJECT", "employeeParams 必须是对象")
        return None
    if not ep:
        err(
            errors,
            "...employeeParams",
            "EMPTY",
            "employeeParams 不能为空对象，至少包含一个员工子对象",
        )
        return ep

    # key 大小写 / 别名检查
    for k in list(ep.keys()):
        if k in VALID_EMPLOYEES:
            continue
        guess = detect_camel_typo(k, VALID_EMPLOYEES)
        if guess:
            err(
                errors,
                f"...employeeParams.{k}",
                "WRONG_CASE_KEY",
                f"员工子对象 key 必须是 PascalCase {guess!r}，当前为 {k!r}",
                f"把 {k!r} 改为 {guess!r}（保留大小写原样）",
            )
        else:
            err(
                errors,
                f"...employeeParams.{k}",
                "UNKNOWN_EMPLOYEE",
                f"未知员工 key {k!r}，合法集合为 {sorted(VALID_EMPLOYEES)}",
            )
    return ep


# ── sourceSettings 形状（依赖员工组合） ─────────────────────────────────────


def validate_source_settings(cstp: dict, ep: dict, errors: list) -> None:
    employees = set(ep.keys()) & VALID_EMPLOYEES
    needs_full = bool(employees & {"Fran", "Lisa"})
    ss = cstp.get("sourceSettings")

    if needs_full:
        if not isinstance(ss, dict):
            err(
                errors,
                "...sourceSettings",
                "WRONG_VALUE",
                f"含 Fran 或 Lisa 时 sourceSettings 必须是完整对象（不能为 null），当前为 {ss!r}",
                "按 SKILL.md 「员工组合 → currentModule / sourceSettings 对照表」填完整对象",
            )
            return
        # 简检几个核心字段类型
        for arr_key in ("groupId", "stageId", "labelId", "level", "seasGroupIds", "addressId", "fileList", "addressFileList"):
            if arr_key in ss and not isinstance(ss[arr_key], list):
                err(
                    errors,
                    f"...sourceSettings.{arr_key}",
                    "WRONG_TYPE",
                    f"{arr_key} 必须是数组",
                )

        # fileList / addressFileList 元素必须是 {name, url} 对象（ExcelFile）
        for arr_key in ("fileList", "addressFileList"):
            items = ss.get(arr_key)
            if not isinstance(items, list):
                continue
            for i, item in enumerate(items):
                ip = f"...sourceSettings.{arr_key}[{i}]"
                if not isinstance(item, dict):
                    err(errors, ip, "WRONG_TYPE",
                        f"{arr_key} 元素必须是对象 {{\"name\":\"...\",\"url\":\"...\"}}，当前为 {type(item).__name__}（值 {item!r}）",
                        "不得传裸 URL 字符串，必须是 {\"name\": \"文件名.xlsx\", \"url\": \"https://...aliyuncs.com/...\"}")
                    continue
                for k in ("name", "url"):
                    if k not in item:
                        err(errors, f"{ip}.{k}", "MISSING_KEY",
                            f"{arr_key} 元素缺少 {k!r}（注意：上传接口返回的是 fileName，装配时须改名为 name）")
                    elif not isinstance(item[k], str) or not item[k]:
                        err(errors, f"{ip}.{k}", "WRONG_VALUE",
                            f"{arr_key}[{i}].{k} 必须是非空字符串，当前为 {item[k]!r}")
                # 禁止多余的 fileName 键（常见错误：把 fileName 和 name 都带上）
                if "fileName" in item:
                    err(errors, f"{ip}.fileName", "EXTRA_KEY",
                        f"{arr_key} 元素不得包含 fileName 键，上传响应的 fileName 应重命名为 name 后装配")


# ── AiWa ────────────────────────────────────────────────────────────────────


AIWA_REQUIRED = [
    "totalTarget", "incrementalTarget", "upperLimitTarget",
    "keywordList", "continent", "country", "countryCodeList",
    "addressObjList", "industryList",
]


def validate_aiwa(p: dict, errors: list) -> None:
    base = "...employeeParams.AiWa"
    for k in AIWA_REQUIRED:
        if k not in p:
            err(errors, f"{base}.{k}", "MISSING_KEY", f"AiWa 缺少必填 {k!r}")

    # 固定值
    if p.get("incrementalTarget") != 5000:
        err(
            errors,
            f"{base}.incrementalTarget",
            "WRONG_VALUE",
            f"AiWa.incrementalTarget 必须固定为 5000，当前为 {p.get('incrementalTarget')!r}",
            "改为整数 5000",
        )
    if p.get("upperLimitTarget") != 5000:
        err(
            errors,
            f"{base}.upperLimitTarget",
            "WRONG_VALUE",
            f"AiWa.upperLimitTarget 必须固定为 5000，当前为 {p.get('upperLimitTarget')!r}",
            "改为整数 5000",
        )

    # totalTarget：定额模式整数，周期模式 null（这里按整数或 None 任一通过）
    tt = p.get("totalTarget", "<missing>")
    if tt != "<missing>" and tt is not None and not (isinstance(tt, int) and not isinstance(tt, bool)):
        err(
            errors,
            f"{base}.totalTarget",
            "WRONG_TYPE",
            f"AiWa.totalTarget 必须是整数或 null，当前为 {tt!r}",
        )

    # 数组类字段
    for k in ("keywordList", "countryCodeList", "addressObjList", "industryList"):
        v = p.get(k, "<missing>")
        if v == "<missing>":
            continue
        if not isinstance(v, list):
            err(
                errors,
                f"{base}.{k}",
                "WRONG_TYPE",
                f"AiWa.{k} 必须是数组，当前为 {type(v).__name__}（值 {v!r}）",
                "若来源是逗号字符串，必须先 .split(',') 拆分成数组；空时填 [] 而不是 \"\"",
            )

    # continent / country：null 或非空字符串，禁止 ""
    for k in ("continent", "country"):
        if k not in p:
            continue
        v = p[k]
        if v is not None and not (isinstance(v, str) and v != ""):
            err(
                errors,
                f"{base}.{k}",
                "WRONG_VALUE",
                f"AiWa.{k} 必须是非空字符串或 null，当前为 {v!r}",
                "无值时填 null（不要填 \"\"）",
            )

    # countryCodeList 是数组（上面已检），且空时为 [] 而非 ""
    if isinstance(p.get("countryCodeList"), str):
        # 已经在上面报过 WRONG_TYPE，这里附加 suggestion
        pass

    # addressObjList：必须有占位项（即使无地址也是 [{type:1, province:"", city:"", county:"", address:""}]）
    aol = p.get("addressObjList")
    if isinstance(aol, list):
        if len(aol) == 0:
            err(
                errors,
                f"{base}.addressObjList",
                "EMPTY",
                "addressObjList 不能为 []，无地址也要填占位 [{\"type\":1,\"province\":\"\",\"city\":\"\",\"county\":\"\",\"address\":\"\"}]",
            )
        for i, item in enumerate(aol):
            ip = f"{base}.addressObjList[{i}]"
            if not isinstance(item, dict):
                err(errors, ip, "WRONG_TYPE", "数组元素必须是对象")
                continue
            for k in ("type", "province", "city", "county", "address"):
                if k not in item:
                    err(errors, f"{ip}.{k}", "MISSING_KEY", f"缺少 {k!r}")
            t = item.get("type")
            if t not in (0, 1):
                err(
                    errors,
                    f"{ip}.type",
                    "WRONG_VALUE",
                    f"type 必须是 1（中文结构化）或 0（自由文本），当前为 {t!r}",
                )
            # 不得 type=1 时还填 address，反之亦然
            if t == 1 and item.get("address"):
                err(
                    errors,
                    f"{ip}",
                    "TYPE_ADDRESS_CONFLICT",
                    "type=1 时 address 必须为 \"\"，省/市/县才填值",
                )
            if t == 0 and any(item.get(k) for k in ("province", "city", "county")):
                err(
                    errors,
                    f"{ip}",
                    "TYPE_ADDRESS_CONFLICT",
                    "type=0 时 province/city/county 必须全为 \"\"，地址放在 address 字段",
                )


# ── Frank ───────────────────────────────────────────────────────────────────


FRANK_REQUIRED = [
    "incrementalTarget", "upperLimitTarget", "senderEmail",
    "language", "templateId", "emailPlanList",
]


def validate_frank(p: dict, errors: list) -> None:
    base = "...employeeParams.Frank"
    for k in FRANK_REQUIRED:
        if k not in p:
            err(errors, f"{base}.{k}", "MISSING_KEY", f"Frank 缺少必填 {k!r}")

    require_value(p.get("incrementalTarget"), f"{base}.incrementalTarget", 1000, errors)
    require_value(p.get("upperLimitTarget"), f"{base}.upperLimitTarget", 1000, errors)

    if "senderEmail" in p and not isinstance(p["senderEmail"], str):
        err(
            errors,
            f"{base}.senderEmail",
            "WRONG_TYPE",
            f"senderEmail 必须是字符串，当前为 {type(p['senderEmail']).__name__}",
            "不得写成对象 {email: \"...\"}，也不得改名为 email/fromEmail/mailFrom",
        )

    if "language" in p and p["language"] not in ("中文", "英文"):
        err(
            errors,
            f"{base}.language",
            "WRONG_VALUE",
            f"Frank.language 必须是 \"中文\" 或 \"英文\"，当前为 {p['language']!r}",
        )

    if "templateId" in p and p["templateId"] is not None:
        err(
            errors,
            f"{base}.templateId",
            "WRONG_VALUE",
            f"Frank.templateId 必须固定为 null，当前为 {p['templateId']!r}",
            "改为 null（JSON 字面量）",
        )

    epl = p.get("emailPlanList")
    if epl is not None:
        if not isinstance(epl, list):
            err(
                errors,
                f"{base}.emailPlanList",
                "WRONG_TYPE",
                "emailPlanList 必须是数组（即使只有 1 个对象也得用数组包起来）",
            )
        elif len(epl) != 1:
            err(
                errors,
                f"{base}.emailPlanList",
                "WRONG_LENGTH",
                f"emailPlanList 必须是长度为 1 的数组，当前长度 {len(epl)}",
            )
        else:
            item = epl[0]
            ip = f"{base}.emailPlanList[0]"
            if not isinstance(item, dict):
                err(errors, ip, "WRONG_TYPE", "元素必须是对象")
            else:
                for k in ("delayDay", "emailSubject", "emailText", "loading"):
                    if k not in item:
                        err(errors, f"{ip}.{k}", "MISSING_KEY", f"emailPlanList[0] 缺少 {k!r}")
                if item.get("delayDay") != 0:
                    err(errors, f"{ip}.delayDay", "WRONG_VALUE", "delayDay 必须为 0")
                if item.get("loading") != 0:
                    err(errors, f"{ip}.loading", "WRONG_VALUE", "loading 必须为 0")


# ── Fran ────────────────────────────────────────────────────────────────────


FRAN_REQUIRED = [
    "ringingDuration", "incrementalTarget", "upperLimitTarget",
    "minConcurrency", "priority", "callingNumber",
    "scriptId", "agentProfileId",
]


def validate_fran(p: dict, errors: list) -> None:
    base = "...employeeParams.Fran"
    for k in FRAN_REQUIRED:
        if k not in p:
            err(errors, f"{base}.{k}", "MISSING_KEY", f"Fran 缺少必填 {k!r}")

    require_value(p.get("ringingDuration"), f"{base}.ringingDuration", 25, errors)
    require_value(p.get("incrementalTarget"), f"{base}.incrementalTarget", 1000, errors)
    require_value(p.get("upperLimitTarget"), f"{base}.upperLimitTarget", 1000, errors)
    require_value(p.get("minConcurrency"), f"{base}.minConcurrency", 1, errors)
    require_value(p.get("priority"), f"{base}.priority", "Daily", errors)

    cn = p.get("callingNumber")
    if cn is not None:
        if not isinstance(cn, list):
            err(
                errors,
                f"{base}.callingNumber",
                "WRONG_TYPE",
                f"callingNumber 必须是数组（即使单号码也得是 [\"30350903\"]），当前为 {type(cn).__name__}",
            )
        elif len(cn) == 0:
            err(errors, f"{base}.callingNumber", "EMPTY", "callingNumber 不能是空数组")
        else:
            for i, n in enumerate(cn):
                if not isinstance(n, str) or not n:
                    err(
                        errors,
                        f"{base}.callingNumber[{i}]",
                        "WRONG_TYPE",
                        f"号码必须是非空字符串，当前为 {n!r}",
                    )

    for k in ("scriptId", "agentProfileId"):
        v = p.get(k)
        if v is not None and (not isinstance(v, str) or not v.strip()):
            err(
                errors,
                f"{base}.{k}",
                "WRONG_VALUE",
                f"{k} 必须是接口返回的非空字符串原值，当前为 {v!r}",
            )


# ── Lisa ────────────────────────────────────────────────────────────────────


LISA_REQUIRED = [
    "incrementalTarget", "upperLimitTarget", "signName", "qualificationName",
    "templateCode", "templateContent", "templateType", "templateParamList",
]


def validate_lisa(p: dict, errors: list) -> None:
    base = "...employeeParams.Lisa"
    for k in LISA_REQUIRED:
        if k not in p:
            err(errors, f"{base}.{k}", "MISSING_KEY", f"Lisa 缺少必填 {k!r}")

    require_value(p.get("incrementalTarget"), f"{base}.incrementalTarget", 100, errors)
    require_value(p.get("upperLimitTarget"), f"{base}.upperLimitTarget", 100, errors)

    # signName / qualificationName 必须是非空字符串
    for k in ("signName", "qualificationName", "templateCode", "templateContent"):
        v = p.get(k)
        if v is not None and (not isinstance(v, str) or not v):
            err(
                errors,
                f"{base}.{k}",
                "WRONG_VALUE",
                f"{k} 必须是非空字符串，当前为 {v!r}",
            )

    tt = p.get("templateType")
    if tt is not None and (isinstance(tt, bool) or not isinstance(tt, int)):
        err(
            errors,
            f"{base}.templateType",
            "WRONG_TYPE",
            f"templateType 必须是数字（取自模板对象的 outerTemplateType），当前为 {tt!r}",
            "不要写成字符串 \"1\"，去掉引号",
        )

    tpl = p.get("templateParamList")
    if tpl is None:
        return
    if not isinstance(tpl, list):
        err(
            errors,
            f"{base}.templateParamList",
            "WRONG_TYPE",
            f"templateParamList 必须是数组（无变量时填 []，不能写成对象映射形式）",
        )
        return
    for i, item in enumerate(tpl):
        ip = f"{base}.templateParamList[{i}]"
        if not isinstance(item, dict):
            err(errors, ip, "WRONG_TYPE", "数组元素必须是对象 {variableLabel,variableAttribute,variableValue}")
            continue
        for k in ("variableLabel", "variableAttribute", "variableValue"):
            if k not in item:
                err(
                    errors,
                    f"{ip}.{k}",
                    "MISSING_KEY",
                    f"templateParamList 元素缺少 {k!r}（即使值同名也必须显式写出 variableAttribute）",
                )
            elif not isinstance(item[k], str) or item[k] == "":
                err(
                    errors,
                    f"{ip}.{k}",
                    "WRONG_VALUE",
                    f"{k} 必须是非空字符串，当前为 {item[k]!r}",
                )

    # 提示：本脚本不做 variableValue 的内容级校验（time 含「年」等）。
    # 调用方必须在调用本脚本之前/之后**单独**调用 validate_sms_template_params.py
    # 对 templateParamList 做内容校验。


# ── Toby (REMOVED) ──────────────────────────────────────────────────────────
# Toby（TikTok 视频生成与发布）已抽离到独立技能 deepsop-tiktokflow，本脚本不再校验。
# 若请求体里出现 Toby key，会在 employee key 检查处直接走 UNKNOWN_EMPLOYEE 分支拦截。


# ── 主流程 ────────────────────────────────────────────────────────────────────


EMPLOYEE_VALIDATORS = {
    "AiWa": validate_aiwa,
    "Frank": validate_frank,
    "Fran": validate_fran,
    "Lisa": validate_lisa,
}


def run(body: Any) -> dict:
    errors: list[dict[str, Any]] = []

    cstp = validate_top_level(body, errors)
    if cstp is None:
        return {
            "ok": False,
            "summary": f"{len(errors)} 项结构校验失败，禁止提交（顶层不通过，未进入员工子对象校验）",
            "errors": errors,
        }

    ep = validate_employee_params_dict(cstp, errors)
    if ep is None:
        return {
            "ok": False,
            "summary": f"{len(errors)} 项结构校验失败，禁止提交（employeeParams 不通过）",
            "errors": errors,
        }

    validate_source_settings(cstp, ep, errors)

    for name, validator in EMPLOYEE_VALIDATORS.items():
        if name in ep:
            sub = ep[name]
            if not isinstance(sub, dict):
                err(
                    errors,
                    f"...employeeParams.{name}",
                    "WRONG_TYPE",
                    f"{name} 子对象必须是对象，当前为 {type(sub).__name__}",
                )
                continue
            validator(sub, errors)

    ok = len(errors) == 0
    summary = (
        "全部结构/取值校验通过，可继续提交（注意：Lisa 还需另跑 validate_sms_template_params.py 做内容校验）"
        if ok
        else f"{len(errors)} 项结构/取值校验失败，禁止提交"
    )
    return {"ok": ok, "summary": summary, "errors": errors}


def main() -> int:
    if len(sys.argv) < 2:
        print(json.dumps({"ok": False, "summary": "缺少参数：需传入完整请求体 JSON 字符串"}, ensure_ascii=False))
        return 2
    try:
        body = json.loads(sys.argv[1])
    except json.JSONDecodeError as exc:
        print(json.dumps({"ok": False, "summary": f"JSON 解析失败：{exc}"}, ensure_ascii=False))
        return 2

    result = run(body)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
