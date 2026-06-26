#!/usr/bin/env python3
"""
validate_employee_params.py（TikTokFlow / Toby 专用版）
对 agentSubmitTask 请求体做结构与取值层的硬约束校验（pre-flight gate）。
仅覆盖数字员工 Toby 的全部结构强约束与固定值规则。

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
- 本脚本只校验 Toby 一个员工。其他数字员工（AiWa/Frank/Fran/Lisa）若出现在请求体中视作未知员工拦截。
- 业务级校验（如账号 id 是否真实存在）需要调接口，不在本脚本范围。
"""

import json
import sys
from typing import Any


VALID_EMPLOYEES = {"Toby"}
INTERNAL_VARS = {"employeeList", "language", "tiktokContent", "totalTarget"}


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


def detect_camel_typo(actual: str, valid_set: set[str]) -> str | None:
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

    # Step 1 内部变量泄漏到根级
    for k in INTERNAL_VARS:
        if k in body:
            err(
                errors,
                f"<root>.{k}",
                "INTERNAL_VAR_LEAK",
                f"{k!r} 是 Step 1 内部解析变量，禁止出现在请求体根级",
                "删除该字段；其值应只流入 employeeParams.Toby 的指定字段",
            )

    # completed 应为 true
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
                f"{k!r} 是 Step 1 内部解析变量，禁止出现在 collaborationSubmitTaskParam 层",
                "删除该字段；其值应下沉到 employeeParams.Toby 内",
            )

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

    # sourceSettings 必须为 null（Toby 单独执行）
    if "sourceSettings" in cstp and cstp["sourceSettings"] is not None:
        err(
            errors,
            "collaborationSubmitTaskParam.sourceSettings",
            "WRONG_VALUE",
            f"Toby 单独执行时 sourceSettings 必须为 null，当前为 {cstp['sourceSettings']!r}",
            "改为 null",
        )

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
            "employeeParams 不能为空对象，必须包含 Toby 子对象",
        )
        return ep

    # key 校验：本技能只允许 Toby
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
                f"未知员工 key {k!r}，本技能仅支持 Toby；如需多员工协作请使用 deepsop-humabot 技能",
            )

    if "Toby" not in ep:
        err(
            errors,
            "...employeeParams.Toby",
            "MISSING_KEY",
            "本技能必须包含 Toby 员工子对象",
        )
    return ep


# ── Toby ────────────────────────────────────────────────────────────────────


TOBY_REQUIRED = [
    "totalTarget", "incrementalTarget", "upperLimitTarget", "content",
    "staffId", "param", "videoItems", "publishTemplates", "accountConfigList",
]

TOBY_PARAM_KEYS = {
    "methodType", "multiShot", "generationType", "text", "multiPrompt",
    "negativePrompt", "imageUrlList", "firstImageUrl", "lastImageUrl",
    "firstClipUrl", "elementList", "videoUrlList", "audioUrl",
    "keepOriginalSound", "durationList", "mode", "resolution", "ratio",
    "generateAudio", "enhancePrompt", "n", "personGeneration",
    "resizeMode", "promptExtend", "shotType", "durationSwitch", "duration",
}

# methodType → (generationType 可选, resolution 可选, ratio 可选, duration 范围/步长, shotType 可选)
TOBY_METHOD_CONSTRAINTS: dict[str, dict[str, Any]] = {
    "auto": {"gt": {"FIRST&LAST"}, "res": {"720p"}, "ratio": {"16:9", "9:16"}, "dur": (None, None, None, 8), "shot": {"single"}},
    "1":    {"gt": {"TEXT", "FIRST&LAST"}, "res": {"720p"}, "ratio": {"16:9", "9:16"}, "dur": (5, 10, 15, 10), "shot": {"single"}},
    "2":    {"gt": {"TEXT", "FIRST&LAST"}, "res": {"480p", "720p", "1080p"}, "ratio": {"adaptive","1:1","3:4","4:3","16:9","9:16","21:9"}, "dur": (1, 4, 12, 4), "shot": {"single"}},
    "3":    {"gt": {"TEXT", "FIRST&LAST", "REFERENCE"}, "res": {"720p","1080p","4K"}, "ratio": {"adaptive","16:9","9:16"}, "dur": (1, 8, 8, 8), "shot": {"single"}},
    "4":    {"gt": {"TEXT", "FIRST&LAST"}, "res": {"720p","1080p","4K"}, "ratio": {"adaptive","16:9","9:16"}, "dur": (1, 8, 8, 8), "shot": {"single"}},
    "5":    {"gt": {"TEXT", "FIRST&LAST"}, "res": {"720p","1080p","4K"}, "ratio": {"adaptive","16:9","9:16"}, "dur": (2, 4, 8, 4), "shot": {"single"}},
    "6":    {"gt": {"TEXT", "FIRST&LAST"}, "res": {"720p","1080p","4K"}, "ratio": {"adaptive","16:9","9:16"}, "dur": (2, 4, 8, 4), "shot": {"single"}},
    "7":    {"gt": {"TEXT"}, "res": {"720p","1080p"}, "ratio": {"1:1","3:4","4:3","16:9","9:16"}, "dur": (1, 3, 15, 3), "shot": {"single","multi"}},
    "8":    {"gt": {"FIRST&LAST"}, "res": {"720p","1080p"}, "ratio": None, "dur": (1, 3, 15, 3), "shot": {"single","multi"}},
    "9":    {"gt": {"REFERENCE"}, "res": {"720p","1080p"}, "ratio": {"1:1","3:4","4:3","16:9","9:16"}, "dur": (1, 3, 10, 3), "shot": {"single","multi"}},
    "10":   {"gt": {"TEXT","FIRST&LAST","REFERENCE","EDIT","FEATURE"}, "res": None, "ratio": {"1:1","16:9","9:16"}, "dur": (1, 3, 15, 3), "shot": {"single","multi","customize"}},
    "11":   {"gt": {"TEXT","FIRST&LAST"}, "res": {"720p"}, "ratio": {"16:9","9:16"}, "dur": (4, 4, 12, 4), "shot": {"single"}},
    "12":   {"gt": {"TEXT","FIRST&LAST"}, "res": {"720p","2K"}, "ratio": {"16:9","9:16","7:4","4:7"}, "dur": (4, 4, 12, 4), "shot": {"single"}},
    "14":   {"gt": {"FIRST&LAST","CONTINUATION"}, "res": {"720p","1080p"}, "ratio": None, "dur": (1, 3, 15, 3), "shot": {"single"}},
    "15":   {"gt": {"TEXT"}, "res": {"720p","1080p"}, "ratio": {"1:1","3:4","4:3","16:9","9:16"}, "dur": (1, 3, 15, 3), "shot": {"single"}},
    "16":   {"gt": {"REFERENCE"}, "res": {"720p","1080p"}, "ratio": {"1:1","3:4","4:3","16:9","9:16"}, "dur": (1, 3, 15, 3), "shot": {"single"}},
    "17":   {"gt": {"TEXT","FIRST&LAST","REFERENCE"}, "res": {"480p","720p","1080p"}, "ratio": {"adaptive","1:1","3:4","4:3","16:9","9:16","21:9"}, "dur": (1, 4, 15, 4), "shot": {"single"}},
    "18":   {"gt": {"TEXT","FIRST&LAST","REFERENCE"}, "res": {"480p","720p"}, "ratio": {"adaptive","1:1","3:4","4:3","16:9","9:16","21:9"}, "dur": (1, 4, 15, 4), "shot": {"single"}},
}


def validate_toby_param(param: dict, errors: list) -> None:
    base = "...employeeParams.Toby.param"

    if not isinstance(param, dict):
        err(errors, base, "WRONG_TYPE", "Toby.param 必须是嵌套对象")
        return

    # 27 key 全量校验
    actual = set(param.keys())
    missing = TOBY_PARAM_KEYS - actual
    extra = actual - TOBY_PARAM_KEYS
    for k in sorted(missing):
        err(
            errors,
            f"{base}.{k}",
            "MISSING_KEY",
            f"Toby.param 必须包含全部 27 个键，当前缺失 {k!r}",
            "即使当前 methodType 下该字段不生效，也必须传默认值（参考 SKILL.md Toby 默认值表）",
        )
    for k in sorted(extra):
        err(
            errors,
            f"{base}.{k}",
            "UNKNOWN_KEY",
            f"Toby.param 出现未知键 {k!r}（合法集合见 SKILL.md），不得自行添加",
        )

    mt = param.get("methodType")
    if not isinstance(mt, str):
        err(
            errors,
            f"{base}.methodType",
            "WRONG_TYPE",
            f"methodType 必须是字符串（如 \"3\"），当前为 {type(mt).__name__}",
        )
        return

    cons = TOBY_METHOD_CONSTRAINTS.get(mt)
    if cons is None:
        err(
            errors,
            f"{base}.methodType",
            "WRONG_VALUE",
            f"methodType 取值不在合法集合，当前为 {mt!r}",
            f"合法值: {sorted(TOBY_METHOD_CONSTRAINTS.keys())}",
        )
        return

    # generationType
    gt = param.get("generationType")
    if gt not in cons["gt"]:
        err(
            errors,
            f"{base}.generationType",
            "WRONG_VALUE",
            f"methodType={mt!r} 时 generationType 必须 ∈ {sorted(cons['gt'])}，当前 {gt!r}",
        )

    # resolution
    if cons["res"] is not None:
        res = param.get("resolution")
        if res not in cons["res"]:
            err(
                errors,
                f"{base}.resolution",
                "WRONG_VALUE",
                f"methodType={mt!r} 时 resolution 必须 ∈ {sorted(cons['res'])}，当前 {res!r}",
            )

    # ratio
    if cons["ratio"] is not None:
        ratio = param.get("ratio")
        if ratio not in cons["ratio"]:
            err(
                errors,
                f"{base}.ratio",
                "WRONG_VALUE",
                f"methodType={mt!r} 时 ratio 必须 ∈ {sorted(cons['ratio'])}，当前 {ratio!r}",
            )

    # duration（仅在有范围时校验，"auto" 跳过）
    step, lo, hi, _default = cons["dur"]
    if step is not None and lo is not None and hi is not None:
        d = param.get("duration")
        if not (isinstance(d, int) and not isinstance(d, bool)):
            err(
                errors,
                f"{base}.duration",
                "WRONG_TYPE",
                f"duration 必须是整数，当前 {d!r}",
            )
        elif d < lo or d > hi or (d - lo) % step != 0:
            err(
                errors,
                f"{base}.duration",
                "OUT_OF_RANGE",
                f"methodType={mt!r} 时 duration 须在 [{lo},{hi}] 且 (d-{lo}) mod {step} == 0，当前 {d}",
            )

    # shotType
    shot = param.get("shotType")
    if shot not in cons["shot"]:
        err(
            errors,
            f"{base}.shotType",
            "WRONG_VALUE",
            f"methodType={mt!r} 时 shotType 必须 ∈ {sorted(cons['shot'])}，当前 {shot!r}",
        )


def validate_toby(p: dict, errors: list) -> None:
    base = "...employeeParams.Toby"
    for k in TOBY_REQUIRED:
        if k not in p:
            err(errors, f"{base}.{k}", "MISSING_KEY", f"Toby 缺少必填 {k!r}")

    if "staffId" in p and p["staffId"] != "":
        err(
            errors,
            f"{base}.staffId",
            "WRONG_VALUE",
            f"Toby.staffId 必须固定为 \"\"，当前为 {p['staffId']!r}",
        )

    if "videoItems" in p and p["videoItems"] != []:
        err(
            errors,
            f"{base}.videoItems",
            "WRONG_VALUE",
            f"Toby.videoItems 必须固定为 []，当前为 {p['videoItems']!r}",
        )

    if "upperLimitTarget" in p and p["upperLimitTarget"] != 10:
        err(
            errors,
            f"{base}.upperLimitTarget",
            "WRONG_VALUE",
            f"Toby.upperLimitTarget 必须固定为 10，当前为 {p['upperLimitTarget']!r}",
        )

    # publishTemplates
    pt = p.get("publishTemplates")
    if pt is not None:
        if not isinstance(pt, list) or not pt:
            err(
                errors,
                f"{base}.publishTemplates",
                "WRONG_VALUE",
                "publishTemplates 必须是非空数组（每个选中账号一条）",
            )
        else:
            for i, item in enumerate(pt):
                ip = f"{base}.publishTemplates[{i}]"
                if not isinstance(item, dict):
                    err(errors, ip, "WRONG_TYPE", "元素必须是对象")
                    continue
                for k in ("publishCount","releaseType","timeZone","intervalType","startTime","accountId","publishInterval"):
                    if k not in item:
                        err(errors, f"{ip}.{k}", "MISSING_KEY", f"缺少 {k!r}")
                for k_fix, v_fix in (("releaseType","1"),("timeZone","1"),("intervalType","1")):
                    if k_fix in item and item[k_fix] != v_fix:
                        err(errors, f"{ip}.{k_fix}", "WRONG_VALUE", f"{k_fix} 必须固定为 {v_fix!r}")

    # accountConfigList
    acl = p.get("accountConfigList")
    if acl is not None:
        if not isinstance(acl, list) or len(acl) != 1:
            err(
                errors,
                f"{base}.accountConfigList",
                "WRONG_VALUE",
                "accountConfigList 必须是长度为 1 的数组",
            )
        else:
            item = acl[0]
            ip = f"{base}.accountConfigList[0]"
            if not isinstance(item, dict):
                err(errors, ip, "WRONG_TYPE", "元素必须是对象")
            else:
                required_keys = ("accountId","privacyLevel","disableDuet","disableStitch","disableComment","expand","brandContentToggle","brandOrganicToggle","isPublicAccount","commentDisabled","duetDisabled","stitchDisabled")
                for k in required_keys:
                    if k not in item:
                        err(errors, f"{ip}.{k}", "MISSING_KEY", f"accountConfigList[0] 缺少 {k!r}")

    # param
    if "param" in p:
        validate_toby_param(p["param"], errors)


# ── 主流程 ────────────────────────────────────────────────────────────────────


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

    if "Toby" in ep:
        sub = ep["Toby"]
        if not isinstance(sub, dict):
            err(
                errors,
                "...employeeParams.Toby",
                "WRONG_TYPE",
                f"Toby 子对象必须是对象，当前为 {type(sub).__name__}",
            )
        else:
            validate_toby(sub, errors)

    ok = len(errors) == 0
    summary = (
        "全部结构/取值校验通过，可继续提交"
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
