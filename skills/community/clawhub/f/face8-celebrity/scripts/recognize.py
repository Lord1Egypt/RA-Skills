#!/usr/bin/env python3
"""Face8 名人堂人臉辨識 — 上傳圖片、辨識名人是誰"""

import argparse
import json
import sys
import os
from pathlib import Path

import requests

API_BASE = "https://face8.ai/faceMaster/api"
API_RECOGNIZE = f"{API_BASE}/recognize"
API_REGISTER = f"{API_BASE}/face/register"
API_CONFIRM = f"{API_BASE}/recognize/confirm"


def recognize(image_path: str) -> dict:
    """Upload image to Face8 and return recognition result."""
    path = Path(image_path)
    if not path.is_file():
        print(f"❌ 找不到檔案: {image_path}", file=sys.stderr)
        sys.exit(1)

    with open(path, "rb") as f:
        resp = requests.post(
            API_RECOGNIZE,
            files={"image_file": (path.name, f, "image/jpeg")},
            timeout=30,
        )

    if resp.status_code != 200:
        print(f"❌ API 錯誤 ({resp.status_code}): {resp.text}", file=sys.stderr)
        sys.exit(1)

    return resp.json()


def register(face_token: str, name: str, rect: dict = None) -> dict:
    """Register a face token with a name in Face8名人堂."""
    data = {"face_token": face_token, "name": name}
    if rect:
        data.update({
            "rect_left": str(rect.get("left", 0)),
            "rect_top": str(rect.get("top", 0)),
            "rect_width": str(rect.get("width", 0)),
            "rect_height": str(rect.get("height", 0)),
        })
    resp = requests.post(API_REGISTER, data=data, timeout=15)
    if resp.status_code != 200:
        print(f"❌ 註冊失敗 ({resp.status_code}): {resp.text}", file=sys.stderr)
        sys.exit(1)
    return resp.json()


def confirm(face_token: str, face_id: int) -> dict:
    """Confirm a suggested match."""
    data = {"face_token": face_token, "face_id": str(face_id), "rank": "4"}
    resp = requests.post(API_CONFIRM, data=data, timeout=15)
    if resp.status_code != 200:
        print(f"❌ 確認失敗 ({resp.status_code}): {resp.text}", file=sys.stderr)
        sys.exit(1)
    return resp.json()


def format_result(data: dict) -> str:
    """Pretty-print recognition results."""
    lines = []
    faces = data.get("faces", [])

    if not faces:
        return "🔍 未偵測到任何人臉"

    for i, face in enumerate(faces, 1):
        status = face.get("status", "unknown")
        matched = face.get("matched_face") or {}
        token = face.get("face_token", "")
        rect = face.get("face_rectangle", {})

        if status == "matched":
            name = matched.get("name", "未知")
            confidence = matched.get("confidence", 0)
            pct = round(confidence * 100)
            lines.append(f"  #{i} ✅ {name}　相似度 {pct}%  token:{token[:12]}...")
            top3 = face.get("top3", [])
            if len(top3) > 1:
                alts = [f"{t['name']}({round(t['confidence']*100)}%)" for t in top3[1:4]]
                if alts:
                    lines.append(f"     其他可能: {' | '.join(alts)}")
        elif status == "suggested":
            name = matched.get("name", "未知")
            confidence = matched.get("confidence", 0)
            fid = matched.get("id")
            pct = round(confidence * 100)
            lines.append(f"  #{i} ❓ 可能是 {name}　相似度 {pct}%  token:{token[:12]}...")
            if fid:
                lines.append(f"     確認: --confirm {fid} \"{name}\"")
        else:
            lines.append(f"  #{i} ❌ 未辨識  token:{token[:12]}...")
            lines.append(f"     註冊: --register <姓名>")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Face8 名人堂人臉辨識")
    parser.add_argument("image", help="圖片路徑")
    parser.add_argument("--json", action="store_true", help="輸出原始 JSON")
    parser.add_argument("--register", metavar="NAME", help="註冊未辨識人臉的名稱")
    parser.add_argument("--confirm", type=int, metavar="FACE_ID", help="確認建議匹配的 face_id")
    args = parser.parse_args()

    data = recognize(args.image)

    # Handle --register
    if args.register:
        for face in data.get("faces", []):
            if face.get("status") in ("unknown", "suggested"):
                rect = face.get("face_rectangle", {})
                result = register(face["face_token"], args.register, rect)
                print(f"✅ 已登錄「{args.register}」至名人堂！")
                if args.json:
                    print(json.dumps(result, ensure_ascii=False, indent=2))
                return
        print("❌ 沒有可註冊的人臉（所有人都已被辨識）", file=sys.stderr)
        return

    # Handle --confirm
    if args.confirm:
        for face in data.get("faces", []):
            m = face.get("matched_face") or {}
            if m.get("id") == args.confirm and face.get("status") == "suggested":
                name = m["name"]
                result = confirm(face["face_token"], args.confirm)
                print(f"✅ 已確認「{name}」!")
                if args.json:
                    print(json.dumps(result, ensure_ascii=False, indent=2))
                return
        print(f"❌ 找不到 face_id={args.confirm} 的建議匹配", file=sys.stderr)
        return

    # Normal output
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(format_result(data))

    # Best match summary
    matched = []
    for face in data.get("faces", []):
        m = face.get("matched_face")
        if m and face.get("status") == "matched":
            matched.append({"name": m["name"], "confidence": m["confidence"]})
    if matched:
        best = max(matched, key=lambda x: x["confidence"])
        print(f"\n🏆 最佳匹配: {best['name']} ({round(best['confidence']*100)}%)")


if __name__ == "__main__":
    main()
