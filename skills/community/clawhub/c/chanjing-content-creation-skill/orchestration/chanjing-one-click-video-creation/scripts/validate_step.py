#!/usr/bin/env python3
"""
程序化校验：替代 LLM 自检门控，对 Workflow 每步输出做硬性校验。

用法:
    python validate_step.py --step 2 --input params.json
    python validate_step.py --step 4 --input workflow.json
    cat workflow.json | python validate_step.py --step 5

输出 JSON:
    {"valid": true,  "step": 4, "errors": [], "warnings": []}
    {"valid": false, "step": 5, "errors": ["scenes 条数(3) != scene_count(5)"], "warnings": [...]}

退出码: 0 = 通过, 1 = 不通过, 2 = 参数/IO 错误
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any

FIRST_DH_MAX_CHARS = int(
    __import__("os").environ.get("FIRST_DIGITAL_HUMAN_MAX_CHARS", "20")
)
INTERACTIVE_TERMS = (
    "点赞", "评论", "关注", "转发", "收藏", "私信", "进群",
    "点个赞", "点点赞", "关注我", "评论区",
)


def _count_chars(text: str) -> int:
    return len(text.replace(" ", ""))


def _errs(data: dict, step: int) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if step == 2:
        _validate_step2(data, errors, warnings)
    elif step == 3:
        _validate_step3(data, errors, warnings)
    elif step == 4:
        _validate_step4(data, errors, warnings)
    elif step == 5:
        _validate_step5(data, errors, warnings)
    elif step == 6:
        _validate_step6(data, errors, warnings)
    else:
        errors.append(f"未知 step: {step}（支持 2-6）")

    return errors, warnings


def _validate_step2(data: dict, errors: list, warnings: list):
    """Step 2 → 3: input_params 校验"""
    topic = (data.get("topic") or "").strip()
    if len(topic) < 5:
        errors.append(f"topic 太短（{len(topic)} 字 < 5）: '{topic}'")

    placeholders = {"你好", "test", "测试", "hello", "hi", "xxx", "aaa"}
    if topic.lower() in placeholders:
        errors.append(f"topic 疑似占位串: '{topic}'")

    dur = data.get("duration_sec")
    if dur is not None:
        try:
            dur = int(dur)
            if not (15 <= dur <= 300):
                errors.append(f"duration_sec={dur} 不在 [15, 300]")
        except (TypeError, ValueError):
            errors.append(f"duration_sec 无法解析为整数: {dur!r}")

    allowed_fields = {
        "topic", "full_script", "industry", "platform", "style",
        "duration_sec", "use_avatar", "subtitle_required",
    }
    extra = set(data.keys()) - allowed_fields
    if extra:
        warnings.append(f"schema 外字段将被忽略: {sorted(extra)}")


def _validate_step3(data: dict, errors: list, warnings: list):
    """Step 3 → 4: video_plan 校验"""
    sc = data.get("scene_count")
    if sc is None:
        errors.append("video_plan 缺少 scene_count")
    else:
        try:
            sc = int(sc)
            if not (3 <= sc <= 10):
                errors.append(f"scene_count={sc} 不在 [3, 10]")
        except (TypeError, ValueError):
            errors.append(f"scene_count 无法解析: {sc!r}")

    tone = (data.get("tone") or "").strip()
    if not tone:
        errors.append("video_plan 缺少 tone")

    presenter_gender = (data.get("presenter_gender") or "").strip().lower()
    if not presenter_gender:
        errors.append("video_plan 缺少 presenter_gender")
    elif presenter_gender not in {"male", "female", "unspecified"}:
        errors.append(
            "presenter_gender 仅允许 male / female / unspecified，"
            f"当前为 {presenter_gender!r}"
        )

    application_context = (data.get("application_context") or "").strip()
    if not application_context:
        errors.append("video_plan 缺少 application_context")

    vtype = (data.get("video_type") or "").lower()
    use_avatar = data.get("use_avatar")
    if vtype and use_avatar is not None:
        if vtype in ("纯ai", "pure_ai", "ai_only") and use_avatar is True:
            warnings.append(
                f"video_type='{vtype}' 但 use_avatar=true，可能不一致"
            )


def _validate_step4(data: dict, errors: list, warnings: list):
    """Step 4 → 5: script_result 校验"""
    hook = data.get("hook", "")
    if hook:
        hook_len = _count_chars(hook)
        if hook_len > FIRST_DH_MAX_CHARS:
            errors.append(
                f"hook 超长: {hook_len} 字 > {FIRST_DH_MAX_CHARS}（'{hook}'）"
            )

    full_script = (data.get("full_script") or "").strip()
    if not full_script:
        errors.append("full_script 为空")
    else:
        hits = [w for w in INTERACTIVE_TERMS if w in full_script]
        if hits:
            errors.append(f"full_script 含互动引导词，需改写: {sorted(set(hits))}")

    closing_line = (data.get("closing_line") or data.get("cta") or "").strip()
    if closing_line:
        hits = [w for w in INTERACTIVE_TERMS if w in closing_line]
        if hits:
            errors.append(f"closing_line 含互动引导词，需改写: {sorted(set(hits))}")

    scenes = data.get("scenes") or data.get("storyboard") or []
    if isinstance(scenes, list) and scenes:
        first_vo = (scenes[0].get("voiceover") or "").strip()
        if first_vo:
            first_vo_len = _count_chars(first_vo)
            if first_vo_len > FIRST_DH_MAX_CHARS:
                warnings.append(
                    f"首镜 voiceover 已 {first_vo_len} 字"
                    f"（限 {FIRST_DH_MAX_CHARS}），将在 Step 5 硬性拦截"
                )


def _validate_step5(data: dict, errors: list, warnings: list):
    """Step 5 → 6: storyboard 校验"""
    scenes = data.get("scenes") or []
    sc = data.get("scene_count")

    if not isinstance(scenes, list) or not scenes:
        errors.append("scenes 为空或非数组")
        return

    if sc is not None:
        try:
            sc = int(sc)
            if len(scenes) != sc:
                errors.append(
                    f"scenes 条数({len(scenes)}) != scene_count({sc})"
                )
        except (TypeError, ValueError):
            pass

    scenes_sorted = sorted(scenes, key=lambda x: int(x.get("scene_id", 0)))
    has_dh = any(s.get("use_avatar") is True for s in scenes_sorted)
    has_ai = any(s.get("use_avatar") is False for s in scenes_sorted)

    # 一键成片强约束：必须包含 AI 分镜
    if not has_ai:
        errors.append("必须至少包含 1 个 AI 分镜（use_avatar=false）")

    # 开启数字人时，分镜需符合奇偶混剪规则（见 storyboard-prompt）
    if has_dh:
        if len(scenes_sorted) < 3:
            errors.append("开启数字人时，scene_count 至少为 3 才能满足混剪规则")
        for idx, s in enumerate(scenes_sorted, start=1):
            expected = True if (idx == 1 or idx == len(scenes_sorted) or idx % 2 == 1) else False
            actual = s.get("use_avatar")
            if actual is None:
                errors.append(f"scenes[{idx-1}] 缺少 use_avatar")
                continue
            if actual is not expected:
                role = "数字人镜(use_avatar=true)" if expected else "AI镜(use_avatar=false)"
                errors.append(
                    f"scenes[{idx-1}]（scene_id={s.get('scene_id')}）应为{role}，当前为 use_avatar={actual}"
                )

    first = scenes_sorted[0]
    first_vo = (first.get("voiceover") or "").strip()
    if first_vo:
        first_vo_len = _count_chars(first_vo)
        if first_vo_len > FIRST_DH_MAX_CHARS:
            errors.append(
                f"首镜 voiceover 超长: {first_vo_len} 字"
                f" > {FIRST_DH_MAX_CHARS}（'{first_vo}'）"
            )

    for i, s in enumerate(scenes_sorted):
        vo = (s.get("voiceover") or "").strip()
        if not vo:
            warnings.append(f"scenes[{i}] voiceover 为空")

        ua = s.get("use_avatar")
        rp = (s.get("ref_prompt") or "").strip()
        if ua is False and not rp:
            errors.append(
                f"scenes[{i}] use_avatar=false 但 ref_prompt 为空"
            )


def _validate_step6(data: dict, errors: list, warnings: list):
    """Step 6 → 7: render 结果校验"""
    status = (data.get("status") or "").lower()
    if status not in ("success", "partial"):
        errors.append(f"status='{status}'（期望 success 或 partial）")

    vf = data.get("video_file") or data.get("video_path") or ""
    if not vf:
        rr = data.get("render_result") or {}
        vf = rr.get("video_file") or ""
    if status == "success" and not vf:
        errors.append("status=success 但 video_file 为空")
    if status == "success" and vf:
        if not os.path.exists(str(vf)):
            errors.append(f"status=success 但视频文件不存在: {vf}")

    if status == "partial":
        warnings.append("status=partial: 部分产出可用，检查 scene_video_urls")


def main():
    parser = argparse.ArgumentParser(
        description="一键成片 Workflow 程序化门控校验"
    )
    parser.add_argument(
        "--step", type=int, required=True,
        help="校验哪一步（2=参数提取, 3=Plan, 4=Script, 5=Storyboard, 6=Render）",
    )
    parser.add_argument(
        "--input", default="-",
        help="JSON 文件路径（默认 stdin）",
    )
    args = parser.parse_args()

    try:
        if args.input == "-":
            raw = sys.stdin.read()
        else:
            with open(args.input, encoding="utf-8") as f:
                raw = f.read()
        data = json.loads(raw)
    except (OSError, json.JSONDecodeError) as exc:
        result = {"valid": False, "step": args.step,
                  "errors": [f"输入解析失败: {exc}"], "warnings": []}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(2)

    errors, warnings = _errs(data, args.step)
    valid = len(errors) == 0
    result = {
        "valid": valid,
        "step": args.step,
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
