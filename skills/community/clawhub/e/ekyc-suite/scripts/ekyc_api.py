#!/usr/bin/env python3
"""
eKYC Suite — Main API Module / 主API模块
==============================================
8 capabilities with 1:1 CLI-to-MCP naming consistency.
8项能力，CLI命令与MCP Tool名称完全一致.

# SECURITY MANIFEST:
#   Environment variables accessed: KYC_APPID, KYC_SECRET (caps 1-7), LABEL_APPID, LABEL_SECRET (cap 8)
#   External endpoints called:
#     https://kyc1.qcloud.com (caps 2,3,4,5)
#     https://miniprogram-kyc.tencentcloudapi.com (caps 1,6,7)
#     https://kyc2.qcloud.com (cap 8)
#   Local files read: user-provided image/video files (passed as CLI arguments)
#   Local files written: none

Commands / 命令:
  face_compare            — Cap 1: Face comparison / 人脸比对
  photo_liveness_detect   — Cap 2: Photo liveness detection / 图片活体检测
  video_liveness_detect   — Cap 3: Video liveness detection / 视频活体检测
  id_card_ocr             — Cap 4: ID card OCR / 身份证OCR
  bank_card_ocr           — Cap 5: Bank card OCR / 银行卡OCR
  driver_license_ocr      — Cap 6: Driver's license OCR / 驾驶证OCR
  vehicle_license_ocr     — Cap 7: Vehicle license OCR / 行驶证OCR
  media_labeling          — Cap 8: Media labeling (async) / 图像标签识别（异步）
"""

import sys, os, json, base64, time, argparse, ipaddress, urllib.parse, io, requests

# Fix stdout encoding for Windows (prevents Chinese garbled output)
if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kyc_auth import (
    get_full_auth, generate_nonce, generate_order_no, parse_response,
    KYC_BASE_MAIN, KYC_BASE_MINI
)
from label_auth import (
    get_label_auth, generate_order_no as label_order_no,
    generate_nonce as label_nonce, LABEL_BASE
)

# Max file size: 20MB (API limit) / 最大文件: 20MB（API限制）
_MAX_RAW_BYTES = 20 * 1024 * 1024

# ============================================================
# Input handling with SSRF protection / 输入处理（含SSRF防护）
# ============================================================

def _is_private_url(url_str: str) -> bool:
    """Block private/internal network URLs to prevent SSRF / 拦截私网URL防止SSRF"""
    try:
        hostname = urllib.parse.urlparse(url_str).hostname
        if not hostname:
            return True
        try:
            ip = ipaddress.ip_address(hostname)
            return ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved
        except ValueError:
            return hostname.lower() in ("localhost", "metadata.google.internal", "169.254.169.254")
    except Exception:
        return True

def smart_input(input_str: str) -> str:
    """
    Handle file path, URL, or raw base64. Includes SSRF protection and size check.
    支持文件路径、URL或原始base64三种输入。含SSRF防护和大小检查。
    """
    if os.path.isfile(input_str):
        size = os.path.getsize(input_str)
        if size > _MAX_RAW_BYTES:
            raise ValueError(f"File too large: {size/1024/1024:.1f}MB, max {_MAX_RAW_BYTES//1024//1024}MB / 文件过大")
        with open(input_str, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    if input_str.startswith(("http://", "https://")):
        if _is_private_url(input_str):
            raise ValueError("Private/internal URLs are not allowed / 不允许使用内网URL")
        resp = requests.get(input_str, timeout=30)
        resp.raise_for_status()
        if len(resp.content) > _MAX_RAW_BYTES:
            raise ValueError(f"Downloaded file too large: {len(resp.content)/1024/1024:.1f}MB / 下载文件过大")
        return base64.b64encode(resp.content).decode("utf-8")
    return input_str

def _safe_json(resp):
    """Parse JSON response safely. Returns error dict if response is not valid JSON.
    安全解析JSON响应，上游返回非JSON时不崩溃。"""
    try:
        return resp.json()
    except (ValueError, requests.exceptions.JSONDecodeError):
        return {"code": "JSON_PARSE_ERROR", "msg": f"API returned non-JSON response (HTTP {resp.status_code}). Please retry. / API返回格式异常，请稍后重试。"}

def _api_post_with_retry(url, payload, max_retries=3, base_wait=3):
    """POST with auto-retry on network errors (999999/999998/999997) and transport exceptions / 网络错误自动重试"""
    data = None
    for attempt in range(max_retries):
        try:
            resp = requests.post(url, json=payload, timeout=60)
            data = _safe_json(resp)
        except requests.RequestException:
            if attempt < max_retries - 1:
                time.sleep(base_wait * (attempt + 1))
                continue
            raise
        code = str(data.get("code", ""))
        if code in ("999999", "999998", "999997") and attempt < max_retries - 1:
            time.sleep(base_wait * (attempt + 1))
            continue
        return data
    return data

# ============================================================
# Cap 1: Face Comparison / 人脸比对
# ============================================================

def face_compare(photo1: str, photo2: str, source_photo_type: str = "2") -> dict:
    """Compare two face photos -> similarity 0-100 / 比对两张人脸照片"""
    app_id, sign_fn = get_full_auth(capability="face_compare")
    order_no = generate_order_no()
    nonce = generate_nonce()
    sign = sign_fn(order_no, nonce)
    url = f"{KYC_BASE_MINI}/api/paas/easycompare?orderNo={order_no}"
    payload = {
        "appId": app_id, "nonce": nonce, "version": "1.0.0", "sign": sign,
        "orderNo": order_no, "photoStr": smart_input(photo1),
        "sourcePhotoStr": smart_input(photo2), "sourcePhotoType": source_photo_type
    }
    data = _safe_json(requests.post(url, json=payload, timeout=30))
    r = parse_response(data, "code", "msg", "similarity", "orderNo")
    if str(r.get("code")) != "0":
        return {"success": False, "error": r.get("msg", "Unknown error"), "code": r.get("code")}
    return {"success": True, "similarity": r.get("similarity"), "orderNo": r.get("orderNo")}

# ============================================================
# Cap 2-3: Liveness Detection / 活体检测
# ============================================================

def _liveness_detect_impl(file_input: str, input_type: str) -> dict:
    face_input_type = 1 if input_type == "image" else 2
    cap = "photo_liveness_detect" if input_type == "image" else "video_liveness_detect"
    app_id, sign_fn = get_full_auth(capability=cap)
    order_no = generate_order_no()
    nonce = generate_nonce()
    sign = sign_fn(order_no, nonce)
    url = f"{KYC_BASE_MAIN}/api/v2/paas/detectAIFakeFace?orderNo={order_no}"
    payload = {
        "appId": app_id, "orderNo": order_no, "nonce": nonce,
        "version": "1.0.0", "sign": sign,
        "faceInputType": face_input_type, "faceInput": smart_input(file_input)
    }
    data = _api_post_with_retry(url, payload) if input_type == "video" else _safe_json(requests.post(url, json=payload, timeout=30))
    r = parse_response(data, "code", "msg", "livenessInfoLevel", "livenessInfoTag", "orderNo")
    if str(r.get("code")) != "0":
        return {"success": False, "error": r.get("msg", "Unknown error"), "code": r.get("code")}
    level, tag = r.get("livenessInfoLevel"), r.get("livenessInfoTag")
    level_map = {"1": "No attack risk / 无攻击风险", "2": "Medium suspicion / 中度疑似攻击", "3": "High suspicion / 高度疑似攻击"}
    tag_map = {
        "01": "Eyes closed / 全程闭眼", "02": "Action not completed / 未完成指定动作",
        "03": "Suspected replay attack / 疑似翻拍攻击", "04": "Suspected synthetic attack / 疑似合成攻击",
        "05": "Suspected fraud template / 疑似黑产模板", "06": "Suspected watermark / 疑似存在水印",
        "07": "Reflection check failed / 反光校验未通过", "08": "Multiple faces / 出现多张人脸",
        "09": "Poor face quality / 人脸质量过差", "10": "Distance check failed / 距离校验不通过",
        "11": "Suspected adversarial attack / 疑似对抗样本攻击", "12": "Attack traces on face / 脸部区域疑似存在攻击痕迹"
    }
    return {
        "success": True, "riskLevel": level, "riskTag": tag,
        "riskLevelText": level_map.get(str(level), f"Unknown({level})"),
        "riskTagText": tag_map.get(str(tag), f"Tag({tag})"),
        "orderNo": r.get("orderNo")
    }

def photo_liveness_detect(file_input: str) -> dict:
    return _liveness_detect_impl(file_input, "image")

def video_liveness_detect(file_input: str) -> dict:
    return _liveness_detect_impl(file_input, "video")

# ============================================================
# Cap 4: ID Card OCR / 身份证OCR
# NOTE: Original docs had typo "qcoud" — correct domain is qcloud
# ============================================================

def id_card_ocr(image: str, card_type: str = "0") -> dict:
    app_id, sign_fn = get_full_auth(capability="id_card_ocr")
    order_no = generate_order_no()
    nonce = generate_nonce()
    sign = sign_fn(order_no, nonce)
    url = f"{KYC_BASE_MAIN}/api/paas/idcardocrapp?orderNo={order_no}"
    payload = {"appId": app_id, "version": "1.0.0", "nonce": nonce, "sign": sign,
               "orderNo": order_no, "cardType": card_type, "idcardStr": smart_input(image)}
    data = _safe_json(requests.post(url, json=payload, timeout=30))
    r = parse_response(data, "code", "msg", "name", "sex", "nation", "birth", "idcard", "address", "authority", "validDate", "orderNo")
    if str(r.get("code")) != "0":
        return {"success": False, "error": r.get("msg", "Unknown error"), "code": r.get("code")}
    return {"success": True, **{k: v for k, v in r.items() if v is not None}}

# ============================================================
# Cap 5: Bank Card OCR / 银行卡OCR
# ============================================================

def bank_card_ocr(image: str) -> dict:
    app_id, sign_fn = get_full_auth(capability="bank_card_ocr")
    order_no = generate_order_no()
    nonce = generate_nonce()
    sign = sign_fn(order_no, nonce)
    url = f"{KYC_BASE_MAIN}/api/paas/bankcardocrapp"
    payload = {"appId": app_id, "version": "1.0.0", "nonce": nonce, "sign": sign,
               "orderNo": order_no, "bankcardStr": smart_input(image)}
    data = _safe_json(requests.post(url, json=payload, timeout=30))
    r = parse_response(data, "code", "msg", "bankcardNo", "bankcardValidDate", "orderNo")
    if str(r.get("code")) != "0":
        return {"success": False, "error": r.get("msg", "Unknown error"), "code": r.get("code")}
    return {"success": True, **{k: v for k, v in r.items() if v is not None}}

# ============================================================
# Cap 6: Driver's License OCR / 驾驶证OCR
# NOTE: API requires "webankAppId" field name (upstream API convention, not a brand reference)
# ============================================================

def driver_license_ocr(image: str) -> dict:
    app_id, sign_fn = get_full_auth(capability="driver_license_ocr")
    order_no = generate_order_no()
    nonce = generate_nonce()
    sign = sign_fn(order_no, nonce)
    url = f"{KYC_BASE_MINI}/api/v2/ocrpaas/driverlicenseupload"
    payload = {"webankAppId": app_id, "version": "1.0.0", "nonce": nonce, "sign": sign,
               "orderNo": order_no, "imageStr": smart_input(image)}
    data = _safe_json(requests.post(url, json=payload, timeout=30))
    r = parse_response(data, "code", "msg", "licenseNo", "name", "sex", "nationality",
                       "address", "birth", "fetchDate", "driveClass", "validDateFrom", "validDateTo", "orderNo")
    if str(r.get("code")) != "0":
        return {"success": False, "error": r.get("msg", "Unknown error"), "code": r.get("code")}
    return {"success": True, **{k: v for k, v in r.items() if v is not None}}

# ============================================================
# Cap 7: Vehicle License OCR / 行驶证OCR
# NOTE: API requires "webankAppId" field name (upstream API convention)
# ============================================================

def vehicle_license_ocr(image: str, side: str = "1") -> dict:
    app_id, sign_fn = get_full_auth(capability="vehicle_license_ocr")
    order_no = generate_order_no()
    nonce = generate_nonce()
    sign = sign_fn(order_no, nonce)
    url = f"{KYC_BASE_MINI}/api/v2/ocrpaas/vehiclelicenseupload"
    payload = {"webankAppId": app_id, "version": "1.0.0", "nonce": nonce, "sign": sign,
               "orderNo": order_no, "imageStr": smart_input(image), "vehicleLicenseSide": side}
    data = _safe_json(requests.post(url, json=payload, timeout=30))
    r = parse_response(data, "code", "msg", "plateNo", "vehicleType", "owner", "useCharacter",
                       "address", "model", "vin", "engineNo", "registeDate", "issueDate", "orderNo",
                       "authorizedCarryCapacity", "authorizedLoadQuality", "fileNumber", "total",
                       "inspectionRecord", "externalDimensions",
                       "curbWeright")  # Upstream API typo: should be "curbWeight"
    if str(r.get("code")) != "0":
        return {"success": False, "error": r.get("msg", "Unknown error"), "code": r.get("code")}
    return {"success": True, **{k: v for k, v in r.items() if v is not None}}

# ============================================================
# Cap 8: Media Labeling / 图像标签识别 (async)
# ============================================================

def media_labeling(file_input: str, label_list: str, file_type: str = "image",
                   do_live: str = "1", do_compare: str = "1",
                   max_retries: int = 3, wait_seconds: int = 5) -> dict:
    app_id, sign_fn = get_label_auth()
    order_no = label_order_no()
    nonce = label_nonce()
    unix_ts = str(int(time.time()))
    sign = sign_fn(order_no, nonce, unix_ts)
    file_type_code = "0" if file_type == "image" else "1"

    submit_url = f"{LABEL_BASE}/idap-ac/server/fileModeration?orderNo={order_no}"
    submit_payload = {
        "appId": app_id, "orderNo": order_no, "nonce": nonce, "version": "1.0.0", "sign": sign,
        "fileStr": smart_input(file_input), "fileType": file_type_code,
        "doLive": do_live, "doCompare": do_compare, "labelList": label_list, "unixTimeStamp": unix_ts
    }
    data = _safe_json(requests.post(submit_url, json=submit_payload, timeout=30))
    if str(data.get("code", "")) != "0":
        return {"success": False, "error": data.get("msg", "Submit failed"), "code": data.get("code")}

    for attempt in range(max_retries):
        time.sleep(wait_seconds)
        q_nonce, q_ts = label_nonce(), str(int(time.time()))
        q_sign = sign_fn(order_no, q_nonce, q_ts)
        query_url = f"{LABEL_BASE}/idap-ac/server/getFileModeration?orderNo={order_no}"
        query_payload = {"appId": app_id, "orderNo": order_no, "nonce": q_nonce,
                         "version": "1.0.0", "sign": q_sign, "unixTimeStamp": q_ts}
        data = _safe_json(requests.post(query_url, json=query_payload, timeout=30))
        code = str(data.get("code", ""))
        if code == "0":
            result = data.get("result", data)
            return {"success": True, "fileLabel": result.get("fileLabel", []),
                    "liveStatus": result.get("liveStatus"), "compareStatus": result.get("compareStatus"), "orderNo": order_no}
        elif code == "66661015":
            if attempt < max_retries - 1: continue
            return {"success": False, "error": "Processing timeout, please retry / 处理超时", "code": code}
        else:
            return {"success": False, "error": data.get("msg", "Query failed"), "code": code}
    return {"success": False, "error": "Query timeout / 查询超时", "code": "TIMEOUT"}

# ============================================================
# CLI Interface / 命令行接口
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="eKYC Suite API Client")
    sub = parser.add_subparsers(dest="command", help="Available commands")
    p1 = sub.add_parser("face_compare"); p1.add_argument("--photo1", required=True); p1.add_argument("--photo2", required=True)
    p2 = sub.add_parser("photo_liveness_detect"); p2.add_argument("--file", required=True)
    p3 = sub.add_parser("video_liveness_detect"); p3.add_argument("--file", required=True)
    p4 = sub.add_parser("id_card_ocr"); p4.add_argument("--image", required=True); p4.add_argument("--side", choices=["0","1"], default="0")
    p5 = sub.add_parser("bank_card_ocr"); p5.add_argument("--image", required=True)
    p6 = sub.add_parser("driver_license_ocr"); p6.add_argument("--image", required=True)
    p7 = sub.add_parser("vehicle_license_ocr"); p7.add_argument("--image", required=True); p7.add_argument("--side", choices=["1","2"], default="1")
    p8 = sub.add_parser("media_labeling"); p8.add_argument("--file", required=True); p8.add_argument("--labels", required=True); p8.add_argument("--type", choices=["image","video"], default="image")

    args = parser.parse_args()
    if not args.command: parser.print_help(); sys.exit(1)
    try:
        dispatch = {
            "face_compare": lambda: face_compare(args.photo1, args.photo2),
            "photo_liveness_detect": lambda: photo_liveness_detect(args.file),
            "video_liveness_detect": lambda: video_liveness_detect(args.file),
            "id_card_ocr": lambda: id_card_ocr(args.image, args.side),
            "bank_card_ocr": lambda: bank_card_ocr(args.image),
            "driver_license_ocr": lambda: driver_license_ocr(args.image),
            "vehicle_license_ocr": lambda: vehicle_license_ocr(args.image, args.side),
            "media_labeling": lambda: media_labeling(args.file, args.labels, args.type),
        }
        print(json.dumps(dispatch[args.command](), ensure_ascii=False, indent=2))
    except ValueError as e:
        print(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False, indent=2)); sys.exit(1)
    except Exception as e:
        print(json.dumps({"success": False, "error": f"Exception: {str(e)}"}, ensure_ascii=False, indent=2)); sys.exit(1)

if __name__ == "__main__":
    main()
