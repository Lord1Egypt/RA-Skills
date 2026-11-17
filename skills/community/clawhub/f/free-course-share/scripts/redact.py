#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""证书敏感信息打码：OCR/精确文本框定位、嵌套图同步修复和逐目标状态清单。

安全默认值（v1.1.5-full）：
1. 任一 --text 未命中，默认退出非零且不写成品；--allow-unmatched 才可放行。
2. 任一 target 匹配分低于 --min-target-score，默认退出非零，且不写任何成功图片。
   --allow-low-score-targets 仅允许跳过低分目标，不会把低分目标标成成功。
3. --text-box TEXT=x1,y1,x2,y2 将指定文本精确映射到源图坐标；所有坐标先验证。
4. manifest 记录每个 target 的 pending/matched/low_score/written/skipped/error 状态。
5. 验证图默认只来自已打码图；未打码验证图必须显式启用。
"""
import argparse
import hashlib
import json
import os
import sys
import tempfile
import time

import numpy as np
from PIL import Image

try:
    import cv2
except ImportError:
    sys.exit("缺少 opencv-python-headless==4.13.0.92")
try:
    import pytesseract
except ImportError:
    sys.exit("缺少 pytesseract==0.3.13")


def ocr_words(img_pil):
    data = pytesseract.image_to_data(
        img_pil, lang="chi_sim", output_type=pytesseract.Output.DICT
    )
    words = []
    for i in range(len(data["text"])):
        text = (data["text"][i] or "").strip()
        try:
            conf = float(data["conf"][i])
        except (TypeError, ValueError):
            conf = -1
        if text and conf > 20:
            words.append(
                dict(
                    t=text,
                    x=data["left"][i],
                    y=data["top"][i],
                    w=data["width"][i],
                    h=data["height"][i],
                )
            )
    return words


def group_lines(words):
    if not words:
        return []
    med_h = float(np.median([w["h"] for w in words]))
    lines, current, center_y = [], [], None
    for word in sorted(words, key=lambda w: w["y"] + w["h"] / 2):
        cy = word["y"] + word["h"] / 2
        if center_y is None or abs(cy - center_y) <= med_h * 0.7:
            current.append(word)
            center_y = cy if center_y is None else center_y * 0.6 + cy * 0.4
        else:
            lines.append(current)
            current, center_y = [word], cy
    if current:
        lines.append(current)
    return lines


def merge_boxes(boxes):
    return (
        int(min(b[0] for b in boxes)),
        int(min(b[1] for b in boxes)),
        int(np.ceil(max(b[2] for b in boxes))),
        int(np.ceil(max(b[3] for b in boxes))),
    )


def find_text_boxes(img_pil, target):
    hits, fuzzy_hits = [], []
    for line in group_lines(ocr_words(img_pil)):
        chars = []
        line = sorted(line, key=lambda w: w["x"])
        for index, word in enumerate(line):
            char_width = word["w"] / max(1, len(word["t"]))
            for char_index, char in enumerate(word["t"]):
                x1 = word["x"] + char_index * char_width
                chars.append(
                    (char, (x1, word["y"], x1 + char_width, word["y"] + word["h"]))
                )
            if (
                index < len(line) - 1
                and line[index + 1]["x"] - (word["x"] + word["w"]) > 2
            ):
                chars.append((" ", None))
        joined = "".join(char for char, _ in chars)
        hit_index = joined.find(target)
        if hit_index >= 0:
            boxes = [
                box
                for _, box in chars[hit_index : hit_index + len(target)]
                if box is not None
            ]
            if boxes:
                hits.append(merge_boxes(boxes))
            continue
        no_spaces = [(char, box) for char, box in chars if char != " "]
        joined = "".join(char for char, _ in no_spaces)
        hit_index = joined.find(target)
        if hit_index >= 0:
            boxes = [
                box
                for _, box in no_spaces[hit_index : hit_index + len(target)]
                if box is not None
            ]
            if boxes:
                hits.append(merge_boxes(boxes))
            continue
        if len(target) >= 2:
            hit_index = joined.find(target[:-1])
            if hit_index >= 0:
                boxes = [
                    box
                    for _, box in no_spaces[
                        hit_index : hit_index + len(target) - 1
                    ]
                    if box is not None
                ]
                if boxes:
                    merged = merge_boxes(boxes)
                    average_width = (merged[2] - merged[0]) / (len(target) - 1)
                    fuzzy_hits.append(
                        (
                            merged[0],
                            merged[1],
                            int(merged[2] + average_width),
                            merged[3],
                        )
                    )
    if fuzzy_hits:
        print(
            f"警告：模糊命中 {len(fuzzy_hits)} 处（允许一个字符 OCR 误差），"
            "必须人工确认验证图"
        )
    return hits + fuzzy_hits


def parse_box(value, option):
    parts = value.split(",")
    if len(parts) != 4:
        raise ValueError(f"{option} 坐标必须是 x1,y1,x2,y2：{value!r}")
    try:
        return tuple(int(part.strip()) for part in parts)
    except ValueError as exc:
        raise ValueError(f"{option} 坐标必须全部是整数：{value!r}") from exc


def validate_box(box, size, option):
    x1, y1, x2, y2 = box
    width, height = size
    if x1 < 0 or y1 < 0:
        raise ValueError(f"{option} 坐标不得为负数：{box}")
    if x1 >= x2 or y1 >= y2:
        raise ValueError(f"{option} 必须满足 x1 < x2 且 y1 < y2：{box}")
    if x2 > width or y2 > height:
        raise ValueError(f"{option} 超出图像范围 {width}x{height}：{box}")
    return box


def parse_text_box(value, size):
    if "=" not in value:
        raise ValueError("--text-box 必须是 TEXT=x1,y1,x2,y2")
    text, raw_box = value.rsplit("=", 1)
    text = text.strip()
    if not text:
        raise ValueError("--text-box 的 TEXT 不得为空")
    box = validate_box(parse_box(raw_box, "--text-box"), size, "--text-box")
    return text, box


def pixelate(img, box, block=None):
    x1, y1, x2, y2 = box
    if block is None:
        block = max(10, (y2 - y1) // 3)
    if block <= 0:
        raise ValueError("--block 必须大于 0")
    region = img.crop(box)
    width, height = region.size
    small = region.resize(
        (max(1, width // block), max(1, height // block)), Image.BILINEAR
    )
    img.paste(small.resize((width, height), Image.NEAREST), box)
    return img


def expand(box, pad, size):
    width, height = size
    x1, y1, x2, y2 = box
    return (
        max(0, int(x1 - pad)),
        max(0, int(y1 - pad)),
        min(width, int(np.ceil(x2 + pad))),
        min(height, int(np.ceil(y2 + pad))),
    )


def resize_rgb(img_pil, scale):
    array = np.array(img_pil)
    height, width = array.shape[:2]
    new_width, new_height = max(1, int(width * scale)), max(1, int(height * scale))
    return Image.fromarray(
        cv2.resize(array, (new_width, new_height), interpolation=cv2.INTER_AREA)
    )


def match_transform(src_gray, tgt_gray, roi, s_lo=0.25, s_hi=0.9):
    x1, y1, x2, y2 = roi
    template_full = src_gray[y1:y2, x1:x2]
    best = None
    for scale in np.arange(s_lo, s_hi, 0.005):
        width = int(template_full.shape[1] * scale)
        height = int(template_full.shape[0] * scale)
        if (
            width < 24
            or height < 16
            or width >= tgt_gray.shape[1]
            or height >= tgt_gray.shape[0]
        ):
            continue
        template = cv2.resize(
            template_full, (width, height), interpolation=cv2.INTER_AREA
        )
        result = cv2.matchTemplate(tgt_gray, template, cv2.TM_CCOEFF_NORMED)
        _, score, _, location = cv2.minMaxLoc(result)
        if best is None or score > best[0]:
            best = (
                score,
                float(scale),
                location[0] - int(x1 * scale),
                location[1] - int(y1 * scale),
            )
            if score > 0.995:
                break
    if best is None:
        raise RuntimeError("模板匹配失败：尺度范围内找不到嵌入图")
    score, scale, offset_x, offset_y = best
    source = src_gray.astype(np.float32)
    best_mse, refined = None, (scale, offset_x, offset_y)
    target_height, target_width = tgt_gray.shape
    for delta_scale in np.arange(-0.010, 0.0105, 0.0025):
        candidate_scale = round(scale + float(delta_scale), 4)
        scaled_width = int(source.shape[1] * candidate_scale)
        scaled_height = int(source.shape[0] * candidate_scale)
        if scaled_width < 10 or scaled_height < 10:
            continue
        resized = cv2.resize(
            source, (scaled_width, scaled_height), interpolation=cv2.INTER_AREA
        )
        rx1, ry1 = int(x1 * candidate_scale), int(y1 * candidate_scale)
        rx2, ry2 = int(x2 * candidate_scale), int(y2 * candidate_scale)
        reference = resized[ry1:ry2, rx1:rx2]
        if reference.size == 0:
            continue
        for delta_y in range(-8, 9, 2):
            for delta_x in range(-8, 9, 2):
                ox, oy = offset_x + delta_x, offset_y + delta_y
                px1, py1 = rx1 + ox, ry1 + oy
                if (
                    px1 < 0
                    or py1 < 0
                    or py1 + reference.shape[0] > target_height
                    or px1 + reference.shape[1] > target_width
                ):
                    continue
                patch = tgt_gray[
                    py1 : py1 + reference.shape[0],
                    px1 : px1 + reference.shape[1],
                ].astype(np.float32)
                mse = float(((patch - reference) ** 2).mean())
                if best_mse is None or mse < best_mse:
                    best_mse, refined = mse, (candidate_scale, ox, oy)
    return refined[0], refined[1], refined[2], score


def _chmod_quiet(path, mode):
    try:
        os.chmod(path, mode)
    except OSError:
        pass


def make_verify_dir(explicit):
    if explicit:
        os.makedirs(explicit, exist_ok=True)
        directory = os.path.abspath(explicit)
        _chmod_quiet(directory, 0o700)
        return directory, False
    directory = tempfile.mkdtemp(prefix="redact-verify-")
    _chmod_quiet(directory, 0o700)
    return directory, True


def save_verify(img_pil, box, path, ctx=90, zoom=3):
    from PIL import ImageDraw

    if os.path.exists(path):
        raise FileExistsError(f"验证图路径已存在，拒绝覆盖：{path}")
    width, height = img_pil.size
    x1, y1, x2, y2 = expand(box, ctx, (width, height))
    crop = img_pil.crop((x1, y1, x2, y2))
    crop = crop.resize((crop.width * zoom, crop.height * zoom), Image.LANCZOS)
    draw = ImageDraw.Draw(crop)
    draw.rectangle(
        [
            (box[0] - x1) * zoom,
            (box[1] - y1) * zoom,
            (box[2] - x1) * zoom,
            (box[3] - y1) * zoom,
        ],
        outline=(255, 0, 0),
        width=max(2, zoom),
    )
    crop.save(path)
    _chmod_quiet(path, 0o600)
    return path


def _mask(text):
    text = text.strip()
    if len(text) <= 1:
        return "*" * max(1, len(text))
    return text[0] + "*" * (len(text) - 1)


def _digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:8]


def _target_output_path(args, target_path):
    if args.inplace:
        return os.path.abspath(target_path)
    if args.target_out:
        return os.path.abspath(
            os.path.join(args.target_out, os.path.basename(target_path))
        )
    return None


def write_manifest(manifest, verify_dir, run_id):
    path = os.path.join(verify_dir, f"{run_id}_verification-manifest.json")
    if os.path.exists(path):
        raise FileExistsError(f"manifest 已存在，拒绝覆盖：{path}")
    with open(path, "w", encoding="utf-8") as file:
        json.dump(manifest, file, ensure_ascii=False, indent=2)
    _chmod_quiet(path, 0o600)
    return path


def build_parser():
    parser = argparse.ArgumentParser(description="敏感信息打码一条龙")
    parser.add_argument("--src", required=True, help="含敏感信息的原始截图")
    parser.add_argument("--text", action="append", default=[], help="要打码的文字，可多次")
    parser.add_argument(
        "--text-box",
        action="append",
        default=[],
        metavar="TEXT=x1,y1,x2,y2",
        help="把指定 TEXT 精确映射到源图坐标，可多次；可替代该 TEXT 的 OCR",
    )
    parser.add_argument(
        "--box",
        action="append",
        default=[],
        help="额外手动框 x1,y1,x2,y2（不代表任何 --text 已命中）",
    )
    parser.add_argument("--pad", type=int, default=8, help="框外扩像素（默认 8）")
    parser.add_argument("--block", type=int, default=None, help="马赛克块大小")
    parser.add_argument("--targets", nargs="*", default=[], help="嵌套源图的成品图")
    parser.add_argument("--out", default=None, help="打码后源图输出路径")
    parser.add_argument("--inplace", action="store_true", help="targets 原地覆盖")
    parser.add_argument("--target-out", default=None, help="targets 修复后输出目录")
    parser.add_argument("--verify-dir", default=None, help="验证图输出目录")
    parser.add_argument("--clean-box", action="append", default=[])
    parser.add_argument(
        "--min-target-score",
        type=float,
        default=0.85,
        help="target 最低匹配分，默认 0.85",
    )
    parser.add_argument(
        "--allow-unmatched",
        action="store_true",
        help="危险：显式允许部分 --text 未命中",
    )
    parser.add_argument(
        "--allow-low-score-targets",
        action="store_true",
        help="危险：显式允许跳过低分 target；低分目标仍不会写出",
    )
    parser.add_argument(
        "--include-unredacted-verification",
        action="store_true",
        help="危险：显式输出未打码验证裁剪",
    )
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.inplace and args.target_out:
        raise SystemExit("--inplace 与 --target-out 不能同时使用")
    if args.pad < 0:
        raise SystemExit("--pad 不得为负数")
    if args.block is not None and args.block <= 0:
        raise SystemExit("--block 必须大于 0")
    if not 0 <= args.min_target_score <= 1:
        raise SystemExit("--min-target-score 必须在 0 到 1 之间")

    source = Image.open(args.src).convert("RGB")
    source_size = source.size
    width, height = source_size
    source_gray = cv2.cvtColor(np.array(source), cv2.COLOR_RGB2GRAY)

    try:
        manual_boxes = [
            validate_box(parse_box(raw, "--box"), source_size, "--box")
            for raw in args.box
        ]
        clean_boxes = [
            validate_box(parse_box(raw, "--clean-box"), source_size, "--clean-box")
            for raw in args.clean_box
        ]
        exact_pairs = [parse_text_box(raw, source_size) for raw in args.text_box]
    except ValueError as exc:
        raise SystemExit(f"参数错误：{exc}") from exc

    exact_by_text = {}
    for text, box in exact_pairs:
        exact_by_text.setdefault(text, []).append(box)

    boxes = list(manual_boxes)
    requested, unmatched = [], []
    for text in args.text:
        if text in exact_by_text:
            hits = exact_by_text[text]
            method = "text-box"
        else:
            hits = find_text_boxes(source, text)
            method = "ocr"
        if not hits:
            unmatched.append(text)
            requested.append(
                dict(label=_mask(text), digest=_digest(text), status="unmatched", hits=0)
            )
            continue
        for hit in hits:
            try:
                boxes.append(validate_box(hit, source_size, f"--text {text!r}"))
            except ValueError as exc:
                raise SystemExit(f"定位结果无效：{exc}") from exc
        requested.append(
            dict(
                label=_mask(text),
                digest=_digest(text),
                status="matched",
                method=method,
                hits=len(hits),
            )
        )

    extra_text_boxes = sorted(set(exact_by_text) - set(args.text))
    if extra_text_boxes:
        raise SystemExit(
            "--text-box 中的 TEXT 必须同时通过 --text 声明："
            + "、".join(repr(text) for text in extra_text_boxes)
        )
    if not boxes:
        raise SystemExit("没有任何打码框，退出（未写入任何成功输出）")
    if unmatched and not args.allow_unmatched:
        raise SystemExit(
            "打码中止：存在未命中文本，未写入任何成功输出："
            + "、".join(repr(text) for text in unmatched)
        )

    union = (
        min(box[0] for box in boxes),
        min(box[1] for box in boxes),
        max(box[2] for box in boxes),
        max(box[3] for box in boxes),
    )
    context = max(60, (union[3] - union[1]) * 3)
    roi = expand(union, context, source_size)
    target_states = []
    target_images = {}
    for target_path in args.targets:
        state = dict(
            path=os.path.abspath(target_path),
            output=_target_output_path(args, target_path),
            status="pending",
        )
        try:
            target = Image.open(target_path).convert("RGB")
            target_gray = cv2.cvtColor(np.array(target), cv2.COLOR_RGB2GRAY)
            scale, offset_x, offset_y, score = match_transform(
                source_gray, target_gray, roi
            )
            state.update(
                scale=scale,
                offset=[offset_x, offset_y],
                score=score,
                threshold=args.min_target_score,
            )
            if score < args.min_target_score:
                state["status"] = "low_score"
            else:
                state["status"] = "matched"
                target_images[target_path] = target
                for box in boxes + clean_boxes:
                    mapped = (
                        int(box[0] * scale) + offset_x,
                        int(box[1] * scale) + offset_y,
                        int(box[2] * scale) + offset_x,
                        int(box[3] * scale) + offset_y,
                    )
                    validate_box(mapped, target.size, f"target 映射 {target_path}")
        except Exception as exc:
            state["status"] = "error"
            state["error"] = str(exc)
        target_states.append(state)

    blocking_targets = [
        state
        for state in target_states
        if state["status"] == "error"
        or (
            state["status"] == "low_score"
            and not args.allow_low_score_targets
        )
    ]
    verify_dir, is_temp = make_verify_dir(args.verify_dir)
    run_id = time.strftime("%m%d-%H%M%S")
    manifest = dict(
        version="1.1.5-full",
        generatedAt=time.strftime("%Y-%m-%dT%H:%M:%S"),
        runId=run_id,
        status="preflight",
        source=os.path.abspath(args.src),
        sourceSize=[width, height],
        requestedTexts=requested,
        manualBoxes=[list(box) for box in manual_boxes],
        textBoxes=[
            dict(label=_mask(text), digest=_digest(text), box=list(box))
            for text, box in exact_pairs
        ],
        boxes=[],
        targets=target_states,
        verificationFiles=[],
        allowUnmatched=bool(args.allow_unmatched),
        allowLowScoreTargets=bool(args.allow_low_score_targets),
        unredactedVerification=bool(args.include_unredacted_verification),
        verifyDir=verify_dir,
        verifyDirIsTemporary=is_temp,
    )
    if blocking_targets:
        manifest["status"] = "failed"
        manifest["reason"] = "target_preflight_failed"
        manifest_path = write_manifest(manifest, verify_dir, run_id)
        details = "；".join(
            f"{os.path.basename(state['path'])}={state['status']}"
            + (
                f"({state.get('score', 0):.3f}<{args.min_target_score:.3f})"
                if state["status"] == "low_score"
                else f"({state.get('error', '')})"
            )
            for state in blocking_targets
        )
        raise SystemExit(
            "target 预检失败，未写入任何成功图片，退出码非零："
            + details
            + f"\n失败 manifest：{manifest_path}"
        )

    source_redacted = source.copy()
    box_sources = ["box"] * len(manual_boxes)
    for text in args.text:
        if text in exact_by_text:
            box_sources.extend(["text-box"] * len(exact_by_text[text]))
        else:
            hit_count = next(
                (
                    item["hits"]
                    for item in requested
                    if item["digest"] == _digest(text) and item["status"] == "matched"
                ),
                0,
            )
            box_sources.extend(["ocr"] * hit_count)
    for box in boxes:
        pixelate(source_redacted, expand(box, args.pad, source_size), args.block)

    def verification_path(kind, index, box, suffix=""):
        x1, y1, x2, y2 = box
        return os.path.join(
            verify_dir,
            f"{run_id}_{kind}_{index:03d}_{x1}-{y1}-{x2}-{y2}{suffix}.png",
        )

    for index, box in enumerate(boxes):
        expanded = expand(box, args.pad, source_size)
        entry = dict(
            index=index,
            box=list(box),
            expandedBox=list(expanded),
            source=box_sources[index] if index < len(box_sources) else "text",
        )
        if args.include_unredacted_verification:
            path = verification_path("src-UNREDACTED", index, box)
            entry["unredactedVerification"] = save_verify(source, box, path)
            manifest["verificationFiles"].append(path)
        path = verification_path("src-redacted", index, box)
        entry["redactedVerification"] = save_verify(source_redacted, box, path)
        manifest["verificationFiles"].append(path)
        manifest["boxes"].append(entry)

    staged_targets = []
    for target_index, (target_path, state) in enumerate(zip(args.targets, target_states)):
        if state["status"] != "matched":
            state["status"] = "skipped"
            continue
        target = target_images[target_path]
        scale = state["scale"]
        offset_x, offset_y = state["offset"]
        clean_resized = resize_rgb(source, scale)
        redacted_resized = resize_rgb(source_redacted, scale)
        for clean_box in clean_boxes:
            expanded = expand(clean_box, 4, source_size)
            destination = (
                int(expanded[0] * scale) + offset_x,
                int(expanded[1] * scale) + offset_y,
            )
            patch = clean_resized.crop(
                tuple(int(value * scale) for value in expanded)
            )
            target.paste(patch, destination)
        for box_index, box in enumerate(boxes):
            expanded = expand(box, args.pad, source_size)
            mapped = (
                int(expanded[0] * scale) + offset_x,
                int(expanded[1] * scale) + offset_y,
                int(expanded[2] * scale) + offset_x,
                int(expanded[3] * scale) + offset_y,
            )
            patch = redacted_resized.crop(
                tuple(int(value * scale) for value in expanded)
            )
            target.paste(patch, mapped[:2])
            path = verification_path(
                "target",
                target_index * 1000 + box_index,
                mapped,
                "_" + os.path.splitext(os.path.basename(target_path))[0],
            )
            save_verify(target, mapped, path)
            manifest["verificationFiles"].append(path)
        output_path = state["output"]
        if output_path:
            staged_targets.append((target, output_path, state))
        else:
            state["status"] = "processed_no_output"

    # 所有计算与验证均成功后，才写成功图片。
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        source_redacted.save(args.out)
    for target, output_path, state in staged_targets:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        target.save(output_path)
        state["status"] = "written"
    manifest["status"] = "completed"
    manifest["sourceOutput"] = os.path.abspath(args.out) if args.out else None
    manifest_path = write_manifest(manifest, verify_dir, run_id)
    print("完成：所有写出目标均通过预检")
    print(f"manifest：{manifest_path}")
    print(f"验证目录：{verify_dir}")
    return 0


if __name__ == "__main__":
    main()
