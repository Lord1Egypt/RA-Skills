#!/usr/bin/env python3
"""
validate_script_params.py
对 createOrModifyScriptAndSubmitScriptReview 请求体做结构与取值层的硬约束校验
（pre-flight gate）。覆盖 agentParams（机器人设定）+ scriptParams（场景+TTS）的全部
高频犯错点。

为什么要单独做这层校验：
  - 后端阿里云 NLU/Chatbot 审核接口对 promptJson / labelsJson / variablesJson 的字符串
    化结构非常敏感，一旦类型/键名错就静默拒绝，错误信息几乎无法回溯；
  - LLM 在拼装 agentParams 时常见错误：把已经是字符串的字段再 stringify 一次、
    把数组对象塞成对象映射、漏 valueList 二次 stringify、误将 openingPrompt 留空等；
  - 这一层在调 HTTP 之前一刀拦截，结果机器可读，让上层 SKILL 直接据此回报用户。

用法（**禁止**用 argv 传中文 JSON，避免 Windows cp936 转码歧义）：

  python3 validate_script_params.py <<'BODY_EOF'
  {"agentParams": {...}, "scriptParams": {...}}
  BODY_EOF

也支持文件路径：

  python3 validate_script_params.py --file /tmp/script_body.json

输出（stdout 单行 JSON）:
  {
    "ok": bool,
    "summary": "...",
    "errors": [
      {"path":"agentParams.promptJson","code":"...","msg":"...","suggestion":"..."}
    ]
  }

退出码:
  0 — 全部通过
  1 — 至少一项失败
  2 — 输入格式错误（stdin 非 UTF-8 / JSON 不可解析）

注意：
- 本脚本只做"形状级"校验（键名、类型、必填、固定值、JSON-string 字段二次解析能否解出）。
- 业务级校验（如 voice 是否在用户账号可选音色范围内、industry 是否合法）需要调接口，
  不在本脚本范围。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


# 机器人设定 promptJson 内部必填项（其他字段允许空字符串）
PROMPT_REQUIRED = {"openingPrompt", "goals"}
# promptJson 允许出现的全部键（多余键放过，不报错；必填键按 PROMPT_REQUIRED 检查）
PROMPT_KNOWN_KEYS = {
    "name", "gender", "age", "role", "communicationStyle",
    "goals", "background", "skills", "workflow", "constraint",
    "openingPrompt", "output", "aiHangupOutput", "aiSilenceTimeoutOutput",
}
# 与前端 Vue 表单 maxlength 严格一致（Vue: ContentPhone.vue → <TextareaVariable :maxlength="...">）
# 这 6 个字段是用户在 UI 上能直接编辑的"可见字段"，必须强约束长度，否则后端会截断或拒绝。
PROMPT_MAX_LENGTH = {
    "openingPrompt": 200,
    "goals":         1000,
    "background":    2000,
    "skills":        1000,
    "workflow":      4000,
    "constraint":    3000,
}

# scriptParams.ttsConfig 内部必填项
TTS_REQUIRED = {"voice", "engine"}
TTS_KNOWN_KEYS = {
    "voice", "voiceShow", "volume", "speechRate", "pitchRate",
    "globalInterruptible", "engine", "nlsServiceType",
    "scriptId",  # 修改场景时阿里云会要求 ttsConfig 里也带 scriptId
}

# 仅这两个引擎被前端 Vue 接受
VALID_TTS_ENGINES = {"ali", "bailian"}


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


def parse_json_string(value: Any, path: str, errors: list, *, expected: str = "object") -> Any:
    """
    agentParams.promptJson / labelsJson / variablesJson 是 *JSON 字符串*（不是直接对象）。
    本工具尝试解析并按 expected="object"/"array" 校验，返回解析结果或 None。
    """
    if not isinstance(value, str):
        err(
            errors,
            path,
            "NOT_JSON_STRING",
            f"{path} 必须是 JSON 字符串（请先 JSON.stringify 再放入），当前为 {type(value).__name__}",
            "对应位置先把对象/数组用 JSON.stringify 转成字符串再放入；不要直接传对象/数组",
        )
        return None
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        err(
            errors,
            path,
            "INVALID_JSON_STRING",
            f"{path} 不是合法 JSON：{exc}",
        )
        return None
    if expected == "object" and not isinstance(parsed, dict):
        err(
            errors,
            path,
            "JSON_SHAPE_MISMATCH",
            f"{path} 解析后必须是对象，当前为 {type(parsed).__name__}",
        )
        return None
    if expected == "array" and not isinstance(parsed, list):
        err(
            errors,
            path,
            "JSON_SHAPE_MISMATCH",
            f"{path} 解析后必须是数组，当前为 {type(parsed).__name__}",
        )
        return None
    return parsed


def validate_prompt_json(prompt_str: Any, errors: list) -> None:
    base = "agentParams.promptJson"
    parsed = parse_json_string(prompt_str, base, errors, expected="object")
    if parsed is None:
        return

    # openingPrompt / goals 必填且非空字符串（与 SKILL.md Step 1.7.1 对齐）
    for key in sorted(PROMPT_REQUIRED):
        value = parsed.get(key)
        if value is None:
            err(errors, f"{base}::{key}", "MISSING_KEY", f"promptJson 缺少 {key} 字段")
        elif not isinstance(value, str) or not value.strip():
            suggestion = (
                "至少填写一句开场白，例如「您好，我是XX公司的客服助理...」"
                if key == "openingPrompt"
                else "必须填写此次呼叫目的，例如「确认客户是否有采购意向」"
            )
            err(
                errors,
                f"{base}::{key}",
                "EMPTY_VALUE",
                f"{key} 必须是非空字符串，当前为 {value!r}",
                suggestion,
            )

    # role：阿里云后端期望字符串；Vue 在拉取后会做 role = role?.[0] || '' 兼容数组返回
    if "role" in parsed and not isinstance(parsed["role"], str):
        err(
            errors,
            f"{base}::role",
            "WRONG_TYPE",
            f"role 必须是字符串，当前为 {type(parsed['role']).__name__}",
            "若来自阿里云模板的数组，取第一项后再 stringify",
        )

    # age：允许整数；其他场景下为字符串/None 也放过
    if "age" in parsed:
        age = parsed["age"]
        if age is not None and not isinstance(age, (int, str)) or isinstance(age, bool):
            err(
                errors,
                f"{base}::age",
                "WRONG_TYPE",
                f"age 必须是整数或字符串，当前为 {age!r}",
            )

    # maxlength 强约束：与 Vue 表单 :maxlength 完全一致，超长会被后端拒绝或截断
    for key, max_len in PROMPT_MAX_LENGTH.items():
        if key not in parsed:
            continue
        val = parsed[key]
        if val is None:
            continue
        if not isinstance(val, str):
            # 其他错误（类型）已在前面 / 不在这里重复报，但若不是 str 直接跳过长度检查
            continue
        # 使用 Python len()（字符数）与 Vue maxlength 行为对齐
        # Vue 的 maxlength 按 UTF-16 code unit 计；常见汉字/英文 ASCII 都是 1 unit，emoji
        # 可能 2 unit。这里用 Python str 长度做近似保守约束，已经够拦住明显超长的输入。
        if len(val) > max_len:
            err(
                errors,
                f"{base}::{key}",
                "TOO_LONG",
                f"{key} 长度 {len(val)} 超过上限 {max_len}（与前端 Vue maxlength 对齐）",
                f"将 {key} 内容压缩到 {max_len} 字符内再提交（可让用户精简描述或拆段）",
            )


def validate_labels_json(labels_str: Any, errors: list) -> None:
    base = "agentParams.labelsJson"
    if labels_str in (None, "", "[]"):
        # 允许无线索（空数组的 JSON 字符串）
        return
    parsed = parse_json_string(labels_str, base, errors, expected="array")
    if parsed is None:
        return

    for i, item in enumerate(parsed):
        ip = f"{base}[{i}]"
        if not isinstance(item, dict):
            err(errors, ip, "WRONG_TYPE", "线索元素必须是对象")
            continue
        for k in ("name", "description", "valueList"):
            if k not in item:
                err(errors, f"{ip}.{k}", "MISSING_KEY", f"线索元素缺少 {k!r}")
        name = item.get("name")
        if not isinstance(name, str) or not name.strip():
            err(
                errors,
                f"{ip}.name",
                "EMPTY_VALUE",
                f"name 必须是非空字符串，当前为 {name!r}",
            )
        vl = item.get("valueList", "<missing>")
        if vl == "<missing>":
            continue
        # valueList 必须是 *再次 stringify* 过的 JSON 数组字符串（与 Vue getProcessData 对齐）
        if not isinstance(vl, str):
            err(
                errors,
                f"{ip}.valueList",
                "NOT_JSON_STRING",
                f"valueList 必须是 JSON 字符串（如 '[\"v1\",\"v2\"]'），当前为 {type(vl).__name__}",
                "构造时对每个线索的 valueList 数组单独 JSON.stringify 后再写入",
            )
            continue
        try:
            inner = json.loads(vl)
        except json.JSONDecodeError as exc:
            err(
                errors,
                f"{ip}.valueList",
                "INVALID_JSON_STRING",
                f"valueList 不是合法 JSON 数组：{exc}",
            )
            continue
        if not isinstance(inner, list):
            err(
                errors,
                f"{ip}.valueList",
                "JSON_SHAPE_MISMATCH",
                f"valueList 解析后必须是数组，当前为 {type(inner).__name__}",
            )


def validate_variables_json(vars_str: Any, errors: list) -> None:
    base = "agentParams.variablesJson"
    if vars_str in (None, "", "[]"):
        return
    parsed = parse_json_string(vars_str, base, errors, expected="array")
    if parsed is None:
        return
    for i, item in enumerate(parsed):
        ip = f"{base}[{i}]"
        if not isinstance(item, dict):
            err(errors, ip, "WRONG_TYPE", "变量元素必须是对象 {name, description}")
            continue
        for k in ("name", "description"):
            if k not in item:
                err(errors, f"{ip}.{k}", "MISSING_KEY", f"变量元素缺少 {k!r}")


def validate_agent_params(agent: Any, errors: list) -> None:
    base = "agentParams"
    if not isinstance(agent, dict):
        err(errors, base, "NOT_OBJECT", "agentParams 必须是对象")
        return

    # model 字段允许缺省/空，但若存在必须是字符串
    if "model" in agent and not isinstance(agent["model"], str):
        err(errors, f"{base}.model", "WRONG_TYPE", "model 必须是字符串（如 'model_001'）")

    # promptJson 必填
    if "promptJson" not in agent:
        err(
            errors,
            f"{base}.promptJson",
            "MISSING_KEY",
            "agentParams 缺少 promptJson 字段（机器人 prompt 的 JSON 字符串）",
        )
    else:
        validate_prompt_json(agent["promptJson"], errors)

    # labelsJson / variablesJson：可选，但若存在必须是 JSON 字符串
    if "labelsJson" in agent:
        validate_labels_json(agent["labelsJson"], errors)
    if "variablesJson" in agent:
        validate_variables_json(agent["variablesJson"], errors)


def validate_tts_config(tts_str: Any, errors: list) -> None:
    base = "scriptParams.ttsConfig"
    parsed = parse_json_string(tts_str, base, errors, expected="object")
    if parsed is None:
        return

    for k in TTS_REQUIRED:
        if k not in parsed:
            err(errors, f"{base}::{k}", "MISSING_KEY", f"ttsConfig 缺少必填 {k!r}")

    voice = parsed.get("voice")
    if voice is not None and (not isinstance(voice, str) or not voice.strip()):
        err(
            errors,
            f"{base}::voice",
            "EMPTY_VALUE",
            f"voice 必须是非空字符串（如 'CosyVoice:longcheng'），当前为 {voice!r}",
        )

    engine = parsed.get("engine")
    if engine is not None and engine not in VALID_TTS_ENGINES:
        err(
            errors,
            f"{base}::engine",
            "WRONG_VALUE",
            f"engine 必须是 {sorted(VALID_TTS_ENGINES)} 之一，当前为 {engine!r}",
            "标准 TTS 用 'ali'；克隆音色用 'bailian'",
        )

    # 数值类字段范围（与 Vue 滑块上下限对齐）
    range_specs = [
        ("volume", 0, 100),
        ("speechRate", -500, 500),
        ("pitchRate", -500, 500),
    ]
    for key, lo, hi in range_specs:
        if key not in parsed:
            continue
        v = parsed[key]
        if isinstance(v, bool) or not isinstance(v, int):
            err(
                errors,
                f"{base}::{key}",
                "WRONG_TYPE",
                f"{key} 必须是整数（不是字符串/布尔），当前为 {v!r}",
            )
            continue
        if v < lo or v > hi:
            err(
                errors,
                f"{base}::{key}",
                "OUT_OF_RANGE",
                f"{key} 必须在 [{lo}, {hi}] 区间，当前为 {v}",
            )


def validate_script_params(script: Any, errors: list) -> None:
    base = "scriptParams"
    if not isinstance(script, dict):
        err(errors, base, "NOT_OBJECT", "scriptParams 必须是对象")
        return

    script_name = script.get("scriptName")
    if script_name is None:
        err(
            errors,
            f"{base}.scriptName",
            "MISSING_KEY",
            "scriptParams 缺少 'scriptName'（场景库名称）",
        )
    elif not isinstance(script_name, str) or not script_name.strip():
        err(
            errors,
            f"{base}.scriptName",
            "EMPTY_VALUE",
            f"scriptName 必须是非空字符串，当前为 {script_name!r}",
        )
    elif len(script_name) > 30:
        err(
            errors,
            f"{base}.scriptName",
            "TOO_LONG",
            f"scriptName 长度 {len(script_name)} 超过上限 30（与前端 Vue maxlength 对齐）",
            "将场景库名称压缩到 30 字符内再提交",
        )

    for k in ("industry", "scene"):
        if k not in script:
            err(
                errors,
                f"{base}.{k}",
                "MISSING_KEY",
                f"scriptParams 缺少 {k!r}（默认填 '通用'）",
                "若没有特定行业/场景需求，统一填字符串 '通用'",
            )
        elif not isinstance(script[k], str) or not script[k].strip():
            err(
                errors,
                f"{base}.{k}",
                "EMPTY_VALUE",
                f"{k} 必须是非空字符串，当前为 {script[k]!r}",
            )

    # nluEngine / nluAccessType：与 Vue 默认值对齐，只允许这一组
    if script.get("nluEngine") not in (None, "Prompts"):
        err(
            errors,
            f"{base}.nluEngine",
            "WRONG_VALUE",
            f"nluEngine 必须固定为 'Prompts'，当前为 {script.get('nluEngine')!r}",
        )
    if script.get("nluAccessType") not in (None, "Managed"):
        err(
            errors,
            f"{base}.nluAccessType",
            "WRONG_VALUE",
            f"nluAccessType 必须固定为 'Managed'，当前为 {script.get('nluAccessType')!r}",
        )

    if "ttsConfig" not in script:
        err(
            errors,
            f"{base}.ttsConfig",
            "MISSING_KEY",
            "scriptParams 缺少 ttsConfig（TTS 配置 JSON 字符串）",
        )
    else:
        validate_tts_config(script["ttsConfig"], errors)


# ── 主入口 ────────────────────────────────────────────────────────────────


def run(body: Any) -> dict:
    errors: list[dict[str, Any]] = []
    if not isinstance(body, dict):
        err(errors, "<root>", "NOT_OBJECT", "请求体必须是对象 {agentParams, scriptParams}")
        return {
            "ok": False,
            "summary": "顶层结构错误，禁止提交",
            "errors": errors,
        }

    if not require_key(body, "agentParams", "<root>", errors):
        return {
            "ok": False,
            "summary": "缺少 agentParams，禁止提交",
            "errors": errors,
        }
    if not require_key(body, "scriptParams", "<root>", errors):
        return {
            "ok": False,
            "summary": "缺少 scriptParams，禁止提交",
            "errors": errors,
        }

    validate_agent_params(body["agentParams"], errors)
    validate_script_params(body["scriptParams"], errors)

    ok = len(errors) == 0
    summary = (
        "全部结构/取值校验通过，可提交 createOrModifyScriptAndSubmitScriptReview"
        if ok
        else f"{len(errors)} 项结构/取值校验失败，禁止提交场景审核"
    )
    return {"ok": ok, "summary": summary, "errors": errors}


def read_body(args: argparse.Namespace) -> str:
    if args.file:
        path = Path(args.file)
        if not path.is_file():
            raise FileNotFoundError(f"--file 指定的文件不存在: {path}")
        return path.read_text(encoding="utf-8-sig")

    if sys.stdin.isatty():
        raise ValueError(
            "未通过 stdin 提供 body 数据。请使用 heredoc:\n"
            "  python3 scripts/validate_script_params.py <<'BODY_EOF'\n"
            "  { ...JSON... }\n"
            "  BODY_EOF\n"
            "或使用 --file <path> 指定 UTF-8 文件。"
        )
    raw = sys.stdin.buffer.read()
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        # 兜底 cp936（Windows 极少数环境）
        return raw.decode("cp936")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="DeepSOP 场景+TTS+机器人设定 创建/审核请求体的 pre-flight 校验"
    )
    parser.add_argument(
        "--file",
        help="从 UTF-8 编码文件读取 body（不传则从 stdin 读取）",
    )
    args = parser.parse_args()

    try:
        raw = read_body(args)
    except (FileNotFoundError, ValueError, UnicodeDecodeError) as exc:
        sys.stdout.write(json.dumps(
            {"ok": False, "summary": str(exc), "errors": []},
            ensure_ascii=False,
        ) + "\n")
        return 2

    try:
        body = json.loads(raw)
    except json.JSONDecodeError as exc:
        sys.stdout.write(json.dumps(
            {"ok": False, "summary": f"body JSON 解析失败：{exc}", "errors": []},
            ensure_ascii=False,
        ) + "\n")
        return 2

    result = run(body)
    sys.stdout.write(json.dumps(result, ensure_ascii=False) + "\n")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
