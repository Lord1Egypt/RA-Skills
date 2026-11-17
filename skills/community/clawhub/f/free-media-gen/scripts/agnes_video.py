#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Agnes 文生视频 / 图生视频 (free-media-gen)，支持两套模型流程并自动取片。

Agnes 有**两套互不兼容**的视频接口，脚本按 model 自动分支：

【A】agnes-video-2.5-flash（新版，官方推荐）
  提交  POST {base}/videos
        {"model":..,"prompt":..,"mode":"text","seconds":"5","size":"720P","aspect_ratio":"16:9"}
        -> {"id","task_id","video_id"}
  轮询  GET {root}/agnesapi?video_id={vid}&model_name={model}
        -> status / internal_status == "completed" | "failed"
  mode 取值：text（纯文本）| keyframe（首尾帧，需 first_frame/last_frame）
            | reference（参考图，images<=5，不支持 videos）

【B】agnes-video-v2.0（旧版）
  提交  POST {base}/video/generations  {"model":..,"prompt":..,"n":1}
        -> {"task_id","video_id"}
  轮询  GET {base}/video/generations/{task_id}  -> data.status == "SUCCESS"

取片（两者通用）：
  GET {root}/agnesapi?video_id={video_id}&model_name={model}
  -> metadata.url 即 MP4 直链（**必须带 model_name**，否则该字段不返回）

base = https://api.agnes-ai.cn/v1 ；root = https://api.agnes-ai.cn
凭证经 _common 从 models.json 解析；不硬编码绝对路径。

用法:
  python agnes_video.py --prompt "猫在草地上走" [--model agnes-video-v2.0|agnes-video-2.5-flash]
                        [--mode text] [--seconds 5] [--aspect-ratio 16:9]
                        [--out DIR] [--timeout 300] [--no-poll] [--task-id TID]
输出: {"ok":true,"stage":"completed","task_id":..,"saved_mp4":..,"video_url":..}
"""
import argparse
import json
import os
import sys
import time
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402

NEW_API_MODELS = {"agnes-video-2.5-flash", "agnes-video-2.5"}


def get(url, headers, timeout=60):
    try:
        req = urllib.request.Request(url, headers=headers, method="GET")
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.getcode(), r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")
    except Exception as e:
        return 0, str(e)


def dig_url(obj):
    """递归寻找响应中任何 .mp4 直链（兜底：metadata.url 缺失时）。"""
    acc = []

    def walk(o):
        if isinstance(o, dict):
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
        elif isinstance(o, str) and (".mp4" in o or "http" in o):
            acc.append(o)
    walk(obj)
    mp4s = [u for u in acc if ".mp4" in u]
    return mp4s[0] if mp4s else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", default="")
    ap.add_argument("--model", default="agnes-video-v2.0")
    ap.add_argument("--mode", default="text", help="新版模型：text|keyframe|reference")
    ap.add_argument("--seconds", default="5", help="新版模型：字符串 4–12")
    ap.add_argument("--aspect-ratio", default="16:9")
    ap.add_argument("--size", default=None, help="新版 Flash 固定 720P；通常无需指定")
    ap.add_argument("--out", default=None)
    ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--interval", type=int, default=4)
    ap.add_argument("--no-poll", action="store_true")
    ap.add_argument("--task-id", default=None, help="仅对已有任务取片")
    args = ap.parse_args()

    entry = C.get_model_entry(args.model)
    if not entry:
        print(json.dumps({"ok": False, "error": "未知模型 id：%s" % args.model},
                         ensure_ascii=False))
        sys.exit(1)

    key = C.resolve_api_key(entry.get("api_key_ref"), entry.get("provider"))
    headers = {"Authorization": "Bearer %s" % key, "Content-Type": "application/json"}

    endpoint = entry.get("endpoint", "")
    base = endpoint[: -len("/videos")] if endpoint.endswith("/videos") else endpoint.rstrip("/")
    root = base[:-3] if base.endswith("/v1") else base

    out_dir = args.out or C.resolve()["outputs_dir"]
    C.ensure_dir(out_dir)

    is_new = args.model in NEW_API_MODELS
    tid, vid = args.task_id, None

    if not tid:
        if not args.prompt:
            print(json.dumps({"ok": False, "error": "缺少 --prompt（或改用 --task-id 取片）"},
                             ensure_ascii=False))
            sys.exit(1)

        if is_new:
            payload = {
                "model": args.model,
                "prompt": args.prompt,
                "mode": args.mode,
                "seconds": str(args.seconds),
                "size": args.size or "720P",
                "aspect_ratio": args.aspect_ratio,
                "n": 1,
            }
            status, body = C.http_json(base + "/videos", payload, headers,
                                       method="POST", retries=3)
            if status != 200 or not isinstance(body, dict) or not (
                    body.get("video_id") or body.get("task_id")):
                print(json.dumps({"ok": False, "http": status, "stage": "submit",
                                  "error": body}, ensure_ascii=False))
                sys.exit(1)
            tid = body.get("task_id") or body.get("id")
            vid = body.get("video_id")
        else:
            payload = {"model": args.model, "prompt": args.prompt, "n": 1}
            status, body = C.http_json(base + "/video/generations", payload, headers,
                                       method="POST", retries=4)
            if status != 200 or not isinstance(body, dict) or "task_id" not in body:
                print(json.dumps({"ok": False, "http": status, "stage": "submit",
                                  "error": body}, ensure_ascii=False))
                sys.exit(1)
            tid = body["task_id"]
            vid = body.get("video_id")

        print(json.dumps({"ok": True, "stage": "submitted", "task_id": tid,
                          "video_id": vid}, ensure_ascii=False), flush=True)
        if args.no_poll:
            print(json.dumps({"ok": True, "stage": "submitted_only", "task_id": tid,
                              "video_id": vid,
                              "note": "已提交未轮询；稍后用 --task-id 取片"}, ensure_ascii=False))
            return

        # 轮询
        deadline = time.time() + args.timeout
        done = False
        while time.time() < deadline:
            if is_new and vid:
                q = urllib.parse.urlencode({"video_id": vid, "model_name": args.model})
                st, b = get(root + "/agnesapi?" + q, headers)
            elif is_new:
                st, b = get(base + "/videos/" + urllib.parse.quote(str(tid)), headers)
            else:
                st, b = get(base + "/video/generations/" + urllib.parse.quote(str(tid)), headers)
            try:
                j = json.loads(b)
            except Exception:
                j = {}
            status_val = (j.get("status")
                          or j.get("internal_status")
                          or (j.get("data") or {}).get("status"))
            if status_val in ("completed", "SUCCESS", "COMPLETED"):
                done = True
                break
            if status_val in ("failed", "FAILED", "FAIL", "ERROR"):
                print(json.dumps({"ok": False, "stage": "failed", "detail": j},
                                 ensure_ascii=False))
                sys.exit(1)
            time.sleep(args.interval)
        if not done:
            print(json.dumps({"ok": False, "error": "等待视频生成超时",
                              "task_id": tid}, ensure_ascii=False))
            sys.exit(1)

    # 取 video_id（若尚未拿到）
    if not vid:
        st3, b3 = get(base + "/videos/" + urllib.parse.quote(str(tid)), headers)
        try:
            j3 = json.loads(b3)
            vid = j3.get("video_id")
        except Exception:
            pass

    # 取直链：必须带 model_name
    video_url = None
    if vid:
        q = urllib.parse.urlencode({"video_id": vid, "model_name": args.model})
        st4, b4 = get(root + "/agnesapi?" + q, headers)
        try:
            j4 = json.loads(b4)
            video_url = (j4.get("metadata") or {}).get("url") or dig_url(j4)
        except Exception:
            pass

    if not video_url:
        print(json.dumps({"ok": False, "stage": "completed_no_url", "task_id": tid,
                          "video_id": vid,
                          "note": "任务已完成但未取到直链；确认 model_name 是否正确"},
                         ensure_ascii=False))
        sys.exit(1)

    out_path = os.path.join(out_dir, "agnes_video_%s.mp4" % str(tid))
    ok = C.download(video_url, out_path, retries=3, timeout=300)
    print(json.dumps({"ok": bool(ok), "stage": "completed", "task_id": tid,
                      "video_id": vid, "video_url": video_url,
                      "saved_mp4": out_path if ok else None}, ensure_ascii=False))


if __name__ == "__main__":
    main()
