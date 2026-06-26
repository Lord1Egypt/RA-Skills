"""Step2b image processing through the 1688 common image gateway."""
from __future__ import annotations

import base64
import copy
import hashlib
import hmac
import json
import os
import sys
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable
from urllib.parse import parse_qs, quote, urlparse

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from scripts.common import dump, env

IMAGE_GATEWAY_BASE = "https://skills-gateway.1688.com/api"
IMAGE_SKILL_VERSION = "1.0.0"
MAX_IMAGE_PROCESSING_ATTEMPTS = 3


@dataclass(frozen=True)
class ImageOperation:
    name: str
    path: str
    async_task: bool = False


@dataclass(frozen=True)
class ImagePipelineStep:
    name: str
    params: dict[str, Any] = field(default_factory=dict)


IMAGE_OPERATIONS: dict[str, ImageOperation] = {
    "translate": ImageOperation("translate", "/ai_image_translateImage/1.0.0"),
    "translate-pro": ImageOperation("translate-pro", "/ai_image_translateImagePro/1.0.0"),
    "enlarge": ImageOperation("enlarge", "/ai_image_imageEnlargement/1.0.0"),
    "extract-object": ImageOperation("extract-object", "/ai_image_imageObjectExtraction/1.0.0"),
    "detect-elements": ImageOperation("detect-elements", "/ai_image_imageElementDetect/1.0.0"),
    "remove-elements": ImageOperation("remove-elements", "/ai_image_imageElementRemove/1.0.0"),
    "crop": ImageOperation("crop", "/ai_image_imageCut/1.0.0"),
    "virtual-try-on": ImageOperation("virtual-try-on", "/ai_image_submitVirtualModelTask/1.0.0", async_task=True),
    "query-try-on": ImageOperation("query-try-on", "/ai_image_queryImageGenerateVirtualModelTask/1.0.0"),
    "change-model": ImageOperation("change-model", "/ai_image_submitImageChangeModelTask/1.0.0", async_task=True),
    "query-change-model": ImageOperation("query-change-model", "/ai_image_queryImageChangeModelTask/1.0.0"),
}

DEFAULT_PRODUCT_TYPE_PIPELINES: dict[str, list[str]] = {
    "SCREEN_PROTECTOR": ["white_background", "crop_4_3"],
    "HANDBAG": ["white_background"],
    "DRINKING_CUP": ["white_background"],
}


def _decode_ak(raw_input: str) -> tuple[str, str]:
    try:
        decoded = base64.urlsafe_b64decode(raw_input).decode("utf-8")
        if decoded:
            raw_input = decoded
    except Exception:
        pass
    if not raw_input or len(raw_input) < 32:
        raise RuntimeError("Missing or invalid ALI_1688_AK for image gateway")
    return raw_input[32:], raw_input[:32]


def _content_md5(body: str) -> str:
    if not body:
        return ""
    return base64.b64encode(hashlib.md5(body.encode("utf-8")).digest()).decode("utf-8")


def _canonicalized_resource(uri: str) -> str:
    parsed = urlparse(uri)
    if not parsed.query:
        return parsed.path
    params = parse_qs(parsed.query)
    pairs: list[str] = []
    for key in sorted(params):
        for value in sorted(params[key]):
            pairs.append(f"{quote(key, safe='')}={quote(value, safe='')}")
    return f"{parsed.path}?{'&'.join(pairs)}"


def build_image_auth_headers(method: str, uri: str, body: str) -> dict[str, str]:
    raw_ak = env("ALI_1688_AK")
    ak_id, ak_secret = _decode_ak(raw_ak)
    timestamp = str(int(time.time()))
    content_md5 = _content_md5(body)
    csk_headers = {
        "x-csk-ak": ak_id,
        "x-csk-time": timestamp,
        "x-csk-nonce": uuid.uuid4().hex[:8],
        "x-csk-content-md5": content_md5,
        "x-csk-version": IMAGE_SKILL_VERSION,
    }
    canonicalized_headers = "".join(f"{key}:{csk_headers[key].strip()}\n" for key in sorted(csk_headers))
    content_type = "application/json"
    string_to_sign = (
        method.upper()
        + "\n"
        + content_md5
        + "\n"
        + content_type
        + "\n"
        + timestamp
        + "\n"
        + canonicalized_headers
        + _canonicalized_resource(uri)
    )
    signature = hmac.new(ak_secret.encode("utf-8"), string_to_sign.encode("utf-8"), hashlib.sha256).digest()
    return {
        "Content-Type": content_type,
        "x-csk-sign": base64.b64encode(signature).decode("utf-8"),
        **csk_headers,
    }


def call_image_api(operation_name: str, payload: dict[str, Any], *, timeout: int = 120) -> dict[str, Any]:
    import requests

    operation = IMAGE_OPERATIONS.get(operation_name)
    if not operation:
        raise ValueError(f"Unsupported image operation={operation_name}; expected one of {sorted(IMAGE_OPERATIONS)}")
    body = json.dumps(payload, ensure_ascii=False)
    headers = build_image_auth_headers("POST", operation.path, body)
    response = requests.post(
        f"{IMAGE_GATEWAY_BASE}{operation.path}",
        headers=headers,
        data=body.encode("utf-8"),
        timeout=timeout,
    )
    response.raise_for_status()
    return response.json()


def _success(response: dict[str, Any]) -> bool:
    code = response.get("resultCode")
    if code not in (None, "", "SUCCESS"):
        return False
    if response.get("success") is False:
        return False
    data = response.get("data")
    if isinstance(data, dict) and data.get("isSuccess") in (0, "0", False):
        return False
    return True


def extract_image_url(response: dict[str, Any]) -> str:
    data = response.get("data")
    result = response.get("result")
    candidates: list[Any] = [
        response.get("imageUrl"),
        response.get("translatedImageUrl"),
    ]
    if isinstance(data, dict):
        data_output = data.get("output")
        candidates.extend(
            [
                data.get("imageUrl"),
                data.get("translatedImageUrl"),
                data_output.get("imageUrl") if isinstance(data_output, dict) else None,
                data_output.get("translatedImageUrl") if isinstance(data_output, dict) else None,
            ]
        )
        if isinstance(data_output, dict):
            data_output_result = data_output.get("result")
            candidates.extend(
                [
                    data_output_result.get("imageUrl") if isinstance(data_output_result, dict) else None,
                    data_output_result.get("translatedImageUrl") if isinstance(data_output_result, dict) else None,
                ]
            )
    if isinstance(result, dict):
        result_data = result.get("data")
        result_result = result.get("result")
        candidates.extend(
            [
                result.get("imageUrl"),
                result.get("translatedImageUrl"),
                result_data.get("imageUrl") if isinstance(result_data, dict) else None,
                result_data.get("translatedImageUrl") if isinstance(result_data, dict) else None,
                result_result.get("imageUrl") if isinstance(result_result, dict) else None,
                result_result.get("translatedImageUrl") if isinstance(result_result, dict) else None,
            ]
        )
    for candidate in candidates:
        if isinstance(candidate, str) and candidate.strip():
            return candidate.strip()
    return ""


def translate_image(
    image_url: str,
    *,
    source_language: str,
    target_language: str,
    include_product_area: bool = False,
    use_image_editor: bool = False,
    translate_brand: bool = False,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "imageUrl": image_url,
        "sourceLanguage": source_language,
        "targetLanguage": target_language,
    }
    if include_product_area:
        payload["includingProductArea"] = True
    if use_image_editor:
        payload["useImageEditor"] = True
    if translate_brand:
        payload["translatingBrandInTheProduct"] = True
    return call_image_api("translate", payload)


def translate_image_pro(
    image_url: str,
    *,
    source_language: str = "auto",
    target_language: str = "en",
    include_product_area: bool = False,
    use_image_editor: bool = False,
    translate_brand: bool = False,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "imageUrl": image_url,
        "sourceLanguage": source_language,
        "targetLanguage": target_language,
    }
    if include_product_area:
        payload["includingProductArea"] = True
    if use_image_editor:
        payload["useImageEditor"] = True
    if translate_brand:
        payload["translatingBrandInTheProduct"] = True
    return call_image_api("translate-pro", payload)


def enlarge_image(image_url: str, *, factor: int | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {"imageUrl": image_url}
    if factor:
        payload["upscaleFactor"] = factor
    return call_image_api("enlarge", payload)


def extract_object(
    image_url: str,
    *,
    transparent: bool,
    bg_color: str | None = None,
    target_width: int | None = None,
    target_height: int | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {"imageUrl": image_url, "transparentFlag": transparent}
    if bg_color:
        payload["bgColor"] = bg_color
    if target_width:
        payload["targetWidth"] = target_width
    if target_height:
        payload["targetHeight"] = target_height
    return call_image_api("extract-object", payload)


def detect_elements(
    image_url: str,
    *,
    object_elements: list[int] | None = None,
    non_object_elements: list[int] | None = None,
    return_character: bool = False,
    return_border_pixel: bool = False,
    return_product_prop: bool = False,
    return_product_num: bool = False,
    return_character_prop: bool = False,
) -> dict[str, Any]:
    payload: dict[str, Any] = {"imageUrl": image_url}
    if object_elements:
        payload["objectDetectElements"] = object_elements
    if non_object_elements:
        payload["nonObjectDetectElements"] = non_object_elements
    if return_character:
        payload["returnCharacter"] = 1
    if return_border_pixel:
        payload["returnBorderPixel"] = 1
    if return_product_prop:
        payload["returnProductProp"] = 1
    if return_product_num:
        payload["returnProductNum"] = 1
    if return_character_prop:
        payload["returnCharacterProp"] = 1
    return call_image_api("detect-elements", payload)


def remove_elements(image_url: str, **flags: int) -> dict[str, Any]:
    payload: dict[str, Any] = {"imageUrl": image_url}
    flag_map = {
        "obj_watermark": "objRemoveWatermark",
        "obj_character": "objRemoveCharacter",
        "obj_logo": "objRemoveLogo",
        "obj_npx": "objRemoveNpx",
        "obj_qrcode": "objRemoveQrcode",
        "noobj_watermark": "noobjRemoveWatermark",
        "noobj_character": "noobjRemoveCharacter",
        "noobj_logo": "noobjRemoveLogo",
        "noobj_npx": "noobjRemoveNpx",
        "noobj_qrcode": "noobjRemoveQrcode",
    }
    for flag, key in flag_map.items():
        if flags.get(flag):
            payload[key] = flags[flag]
    return call_image_api("remove-elements", payload)


def crop_image(image_url: str, *, target_width: int | None = None, target_height: int | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {"imageUrl": image_url}
    if target_width:
        payload["targetWidth"] = target_width
    if target_height:
        payload["targetHeight"] = target_height
    return call_image_api("crop", payload)


def submit_virtual_try_on(
    clothes_info_list: list[dict[str, Any]],
    *,
    generate_count: int,
    model_image_list: list[str] | None = None,
) -> dict[str, Any]:
    return call_image_api(
        "virtual-try-on",
        {
            "modelImageList": model_image_list or [],
            "clothesInfoList": clothes_info_list,
            "generateCount": generate_count,
        },
    )


def query_virtual_try_on(task_id: str) -> dict[str, Any]:
    return call_image_api("query-try-on", {"taskId": task_id})


def submit_change_model(
    image_url: str,
    *,
    model: str,
    bg_style: str,
    age: str,
    gender: str,
    image_num: int,
    mask_keep_bg: bool | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "imageUrl": image_url,
        "model": model,
        "bgStyle": bg_style,
        "age": age,
        "gender": gender,
        "imageNum": image_num,
    }
    if mask_keep_bg is not None:
        payload["maskKeepBg"] = mask_keep_bg
    return call_image_api("change-model", payload)


def query_change_model(task_id: str) -> dict[str, Any]:
    return call_image_api("query-change-model", {"taskId": task_id})


def _int_env(name: str, default: int) -> int:
    try:
        return int(env(name, str(default)))
    except ValueError:
        return default


def _image_retry_delay_seconds() -> float:
    raw = env("AMAZON_IMAGE_RETRY_DELAY_SECONDS", "1")
    try:
        return max(float(raw), 0.0)
    except ValueError:
        return 1.0


def _image_processing_attempts() -> int:
    raw_attempts = _int_env("AMAZON_IMAGE_PROCESSING_MAX_ATTEMPTS", MAX_IMAGE_PROCESSING_ATTEMPTS)
    return min(max(raw_attempts, 1), MAX_IMAGE_PROCESSING_ATTEMPTS)


def _pipeline_names_from_env() -> list[str]:
    raw = env("AMAZON_IMAGE_PIPELINE")
    if not raw:
        return []
    return [item.strip() for item in raw.replace("|", ",").split(",") if item.strip()]


def build_image_pipeline(category: dict[str, Any] | None = None, *, extra_steps: list[str] | None = None) -> list[ImagePipelineStep]:
    category = category or {}
    names = _pipeline_names_from_env()
    if not names:
        product_type = str(category.get("productType") or category.get("ptType") or "").upper()
        names = DEFAULT_PRODUCT_TYPE_PIPELINES.get(product_type, ["white_background"])
    if extra_steps:
        for step in extra_steps:
            if step and step not in names:
                names.append(step)
    return [ImagePipelineStep(name) for name in names]


def _payload_for_step(step: ImagePipelineStep, image_url: str) -> tuple[str, dict[str, Any]]:
    params = dict(step.params)
    if step.name == "white_background":
        return (
            "extract-object",
            {
                "imageUrl": image_url,
                "transparentFlag": False,
                "bgColor": str(params.get("bgColor") or env("AMAZON_WHITE_BG_COLOR", "255,255,255")),
                **(
                    {"targetWidth": params.get("targetWidth") or _int_env("AMAZON_WHITE_BG_TARGET_WIDTH", 0)}
                    if params.get("targetWidth") or _int_env("AMAZON_WHITE_BG_TARGET_WIDTH", 0)
                    else {}
                ),
                **(
                    {"targetHeight": params.get("targetHeight") or _int_env("AMAZON_WHITE_BG_TARGET_HEIGHT", 0)}
                    if params.get("targetHeight") or _int_env("AMAZON_WHITE_BG_TARGET_HEIGHT", 0)
                    else {}
                ),
            },
        )
    if step.name == "crop_4_3":
        return (
            "crop",
            {
                "imageUrl": image_url,
                "targetWidth": int(params.get("targetWidth") or env("AMAZON_MAIN_IMAGE_TARGET_WIDTH", "1200")),
                "targetHeight": int(params.get("targetHeight") or env("AMAZON_MAIN_IMAGE_TARGET_HEIGHT", "900")),
            },
        )
    if step.name == "translate_to_en":
        return (
            "translate-pro",
            {
                "imageUrl": image_url,
                "sourceLanguage": str(params.get("sourceLanguage") or env("AMAZON_IMAGE_SOURCE_LANGUAGE", "auto")),
                "targetLanguage": str(params.get("targetLanguage") or env("AMAZON_IMAGE_TARGET_LANGUAGE", "en")),
                "includingProductArea": bool(params.get("includingProductArea", True)),
            },
        )
    raise ValueError(f"Unsupported image pipeline step={step.name}")


def _run_pipeline_step_with_retry(
    step: ImagePipelineStep,
    operation: str,
    payload: dict[str, Any],
) -> tuple[dict[str, Any], str, int]:
    max_attempts = _image_processing_attempts()
    delay_seconds = _image_retry_delay_seconds()
    last_error = ""
    for attempt in range(1, max_attempts + 1):
        try:
            response = call_image_api(operation, payload)
            if not _success(response):
                last_error = f"Image processing step {step.name} failed: {response}"
            else:
                next_url = extract_image_url(response)
                if next_url:
                    return response, next_url, attempt
                last_error = f"Image processing step {step.name} returned no image URL: {response}"
        except Exception as exc:
            last_error = f"Image processing step {step.name} raised {type(exc).__name__}: {exc}"
        if attempt < max_attempts:
            print(
                f"[WARN] {step.name} attempt {attempt}/{max_attempts} failed; retrying: {last_error}",
                file=sys.stderr,
            )
            if delay_seconds:
                time.sleep(delay_seconds)
    raise RuntimeError(last_error)


def apply_image_pipeline_to_offer(offer_info: dict[str, Any], pipeline: list[ImagePipelineStep]) -> dict[str, Any]:
    main_images = list(offer_info.get("mainImages") or [])
    if not main_images:
        raise RuntimeError("Offer has no mainImages to process")
    source_url = main_images[0]
    current_url = source_url
    records: list[dict[str, Any]] = []
    for step in pipeline:
        operation, payload = _payload_for_step(step, current_url)
        response, next_url, attempts = _run_pipeline_step_with_retry(step, operation, payload)
        records.append(
            {
                "step": step.name,
                "operation": operation,
                "attempts": attempts,
                "api": f"{IMAGE_GATEWAY_BASE}{IMAGE_OPERATIONS[operation].path}",
                "request": payload,
                "response": response,
                "sourceImageUrl": current_url,
                "imageUrl": next_url,
            }
        )
        current_url = next_url
    updated_offer = copy.deepcopy(offer_info)
    updated_main_images = list(updated_offer.get("mainImages") or [])
    updated_main_images[0] = current_url
    updated_offer["mainImages"] = updated_main_images
    updated_offer["imageProcessing"] = records
    if records:
        updated_offer["whiteBackgroundMainImage"] = {
            "sourceImageUrl": source_url,
            "imageUrl": current_url,
            "api": records[0]["api"],
        }
    return {
        "sourceImageUrl": source_url,
        "processedImageUrl": current_url,
        "imagePipeline": records,
        "offer": updated_offer,
    }


def apply_default_image_pipeline_to_offer(
    offer_info: dict[str, Any],
    category: dict[str, Any] | None = None,
    *,
    extra_steps: list[str] | None = None,
) -> dict[str, Any]:
    return apply_image_pipeline_to_offer(offer_info, build_image_pipeline(category, extra_steps=extra_steps))


PIPELINE_FUNCTIONS: dict[str, Callable[..., dict[str, Any]]] = {
    "translate": translate_image,
    "translate-pro": translate_image_pro,
    "enlarge": enlarge_image,
    "extract-object": extract_object,
    "detect-elements": detect_elements,
    "remove-elements": remove_elements,
    "crop": crop_image,
    "virtual-try-on": submit_virtual_try_on,
    "query-try-on": query_virtual_try_on,
    "change-model": submit_change_model,
    "query-change-model": query_change_model,
}


if __name__ == "__main__":
    from scripts.common import read_session, write_session

    if len(sys.argv) < 2:
        print("Usage: python scripts/process_images.py <session_dir> [--extra-steps step1,step2]", file=sys.stderr)
        sys.exit(1)
    session_dir = sys.argv[1]
    extra_steps: list[str] = []
    for idx, arg in enumerate(sys.argv):
        if arg == "--extra-steps" and idx + 1 < len(sys.argv):
            extra_steps = [item.strip() for item in sys.argv[idx + 1].split(",") if item.strip()]

    offer = read_session(session_dir, "query_offer.json", required_keys=["mainImages"])
    try:
        category = read_session(session_dir, "map_category.json")
    except FileNotFoundError:
        category = {}
    result = apply_default_image_pipeline_to_offer(offer, category, extra_steps=extra_steps)
    write_session(session_dir, "image_processing.json", result)
    print(dump(result))
