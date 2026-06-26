import argparse
import json
from typing import Any, Dict, Optional, Union

from jfbym_sdk import JfbymSdkClient
from local_captcha import LocalCaptchaSolver


class JfbymClient:
    """
    统一门面：
    - 本地免费能力来自 LocalCaptchaSolver
    - 云码收费 SDK 来自 JfbymSdkClient

    保留旧入口，兼容历史用法。
    """

    SKILL_CHANNEL_DEVELOPER_TAG = JfbymSdkClient.SKILL_CHANNEL_DEVELOPER_TAG

    def __init__(
        self,
        token: Optional[str] = None,
        base_url: str = "https://api.jfbym.com/api/YmServer",
    ):
        self.sdk = JfbymSdkClient(token=token, base_url=base_url)

    @property
    def token(self) -> Optional[str]:
        return self.sdk.token

    @property
    def base_url(self) -> str:
        return self.sdk.base_url

    @classmethod
    def solve_local_text_captcha(cls, image_input: Union[str, bytes], png_fix: bool = False) -> str:
        return LocalCaptchaSolver.solve_text_captcha(image_input=image_input, png_fix=png_fix)

    @classmethod
    def solve_local_text_captcha_with_range(
        cls,
        image_input: Union[str, bytes],
        charset_range: str = "0123456789abcdefghijklmnopqrstuvwxyz",
        png_fix: bool = False,
    ) -> str:
        return LocalCaptchaSolver.solve_text_captcha_with_range(
            image_input=image_input,
            charset_range=charset_range,
            png_fix=png_fix,
        )

    @classmethod
    def solve_local_slide_distance_ddddocr(
        cls,
        back_image_input: Union[str, bytes],
        slide_image_input: Union[str, bytes],
        simple_target: bool = False,
    ) -> Dict[str, Any]:
        return LocalCaptchaSolver.solve_slide_distance_ddddocr(
            back_image_input=back_image_input,
            slide_image_input=slide_image_input,
            simple_target=simple_target,
        )

    @classmethod
    def detect_local_text_boxes(cls, image_input: Union[str, bytes]):
        return LocalCaptchaSolver.detect_text_boxes(image_input=image_input)

    @classmethod
    def solve_local_math_captcha(cls, image_input: Union[str, bytes]) -> Dict[str, str]:
        return LocalCaptchaSolver.solve_math_captcha(image_input=image_input)

    @staticmethod
    def solve_local_slide_distance(back_img_base64: str, slide_img_base64: str) -> int:
        return LocalCaptchaSolver.solve_slide_distance(back_img_base64, slide_img_base64)

    def get_balance(self) -> str:
        return self.sdk.get_balance()

    def report_error(self, unique_code: str) -> bool:
        return self.sdk.report_error(unique_code)

    def solve_common(
        self,
        image_input: Optional[Union[str, bytes]] = None,
        captcha_type: str = "10110",
        extra: Any = None,
        **kwargs,
    ) -> Dict:
        return self.sdk.solve_common(
            image_input=image_input,
            captcha_type=captcha_type,
            extra=extra,
            **kwargs,
        )

    def solve_slide(
        self,
        slide_image: Union[str, bytes],
        bg_image: Union[str, bytes],
        captcha_type: str = "20111",
        extra: Any = None,
        **kwargs,
    ) -> Dict:
        return self.sdk.solve_slide(
            slide_image=slide_image,
            bg_image=bg_image,
            captcha_type=captcha_type,
            extra=extra,
            **kwargs,
        )

    def solve_recaptcha(
        self, googlekey: str, pageurl: str, captcha_type: str = "40010", **kwargs
    ) -> str:
        return self.sdk.solve_recaptcha(
            googlekey=googlekey,
            pageurl=pageurl,
            captcha_type=captcha_type,
            **kwargs,
        )

    @staticmethod
    def guess_captcha_type(description: str) -> str:
        return JfbymSdkClient.guess_captcha_type(description)

    def solve_auto_fallback(
        self,
        task: str,
        image_input: Optional[Union[str, bytes]] = None,
        back_image_input: Optional[Union[str, bytes]] = None,
        slide_image_input: Optional[Union[str, bytes]] = None,
        charset_range: Optional[str] = None,
        paid_captcha_type: Optional[str] = None,
        extra: Any = None,
        prefer: str = "free",
    ) -> Dict[str, Any]:
        task = (task or "").strip().lower()
        prefer = (prefer or "").strip().lower()
        if task not in {"text", "math", "slide"}:
            raise ValueError("task 仅支持: text / math / slide")
        if prefer not in {"free", "paid"}:
            raise ValueError("prefer 仅支持: free / paid")

        def _solve_free() -> Any:
            if task == "text":
                if image_input is None:
                    raise ValueError("text 任务必须传入 image_input")
                if charset_range:
                    return self.solve_local_text_captcha_with_range(
                        image_input=image_input,
                        charset_range=charset_range,
                    )
                return self.solve_local_text_captcha(image_input=image_input)

            if task == "math":
                if image_input is None:
                    raise ValueError("math 任务必须传入 image_input")
                return self.solve_local_math_captcha(image_input=image_input)

            if back_image_input is None or slide_image_input is None:
                raise ValueError("slide 任务必须传入 back_image_input 和 slide_image_input")

            try:
                result = self.solve_local_slide_distance_ddddocr(
                    back_image_input=back_image_input,
                    slide_image_input=slide_image_input,
                )
                result["engine"] = "ddddocr"
                return result
            except Exception as dddd_err:
                back_b64 = LocalCaptchaSolver.to_base64_string(back_image_input)
                slide_b64 = LocalCaptchaSolver.to_base64_string(slide_image_input)
                x = self.solve_local_slide_distance(back_b64, slide_b64)
                return {
                    "x": int(x),
                    "engine": "opencv",
                    "ddddocr_error": str(dddd_err),
                }

        def _solve_paid() -> Any:
            if task == "text":
                if image_input is None:
                    raise ValueError("text 任务必须传入 image_input")
                return self.solve_common(
                    image_input=image_input,
                    captcha_type=paid_captcha_type or "10110",
                    extra=extra,
                )

            if task == "math":
                if image_input is None:
                    raise ValueError("math 任务必须传入 image_input")
                return self.solve_common(
                    image_input=image_input,
                    captcha_type=paid_captcha_type or "50100",
                    extra=extra,
                )

            if back_image_input is None or slide_image_input is None:
                raise ValueError("slide 任务必须传入 back_image_input 和 slide_image_input")
            return self.solve_slide(
                slide_image=slide_image_input,
                bg_image=back_image_input,
                captcha_type=paid_captcha_type or "20111",
                extra=extra,
            )

        attempts = (
            [("free", _solve_free), ("paid", _solve_paid)]
            if prefer == "free"
            else [("paid", _solve_paid), ("free", _solve_free)]
        )

        errors = []
        for mode, fn in attempts:
            try:
                result = fn()
                payload: Dict[str, Any] = {
                    "task": task,
                    "mode": mode,
                    "result": result,
                }
                if errors:
                    payload["fallback_reason"] = errors[-1]
                return payload
            except Exception as exc:
                errors.append(f"{mode}: {exc}")

        raise Exception(f"自动识别失败(task={task}) -> {' | '.join(errors)}")


def _build_cli_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="验证码基础能力 CLI：默认免费优先，复杂场景可自动走低价云码兜底。"
    )
    subparsers = parser.add_subparsers(dest="task", required=True)

    text_parser = subparsers.add_parser("text", help="识别文本验证码")
    text_parser.add_argument("--image", required=True, help="图片路径或 base64")
    text_parser.add_argument("--charset", default=None, help="可选字符集约束，如 0123456789")
    text_parser.add_argument("--prefer", choices=["free", "paid"], default="free")
    text_parser.add_argument("--paid-type", default=None, help="可选，覆盖默认付费 type")
    text_parser.add_argument("--extra", default=None, help="可选，透传给付费 solve_common")
    text_parser.add_argument("--raw", action="store_true", help="仅输出结果主体，不输出包装结构")

    math_parser = subparsers.add_parser("math", help="识别算术验证码")
    math_parser.add_argument("--image", required=True, help="图片路径或 base64")
    math_parser.add_argument("--prefer", choices=["free", "paid"], default="free")
    math_parser.add_argument("--paid-type", default=None, help="可选，覆盖默认付费 type")
    math_parser.add_argument("--extra", default=None, help="可选，透传给付费 solve_common")
    math_parser.add_argument("--raw", action="store_true", help="仅输出结果主体，不输出包装结构")

    slide_parser = subparsers.add_parser("slide", help="识别双图滑块")
    slide_parser.add_argument("--background", required=True, help="背景图路径或 base64")
    slide_parser.add_argument("--slide", required=True, help="滑块图路径或 base64")
    slide_parser.add_argument("--prefer", choices=["free", "paid"], default="free")
    slide_parser.add_argument("--paid-type", default=None, help="可选，覆盖默认付费 type")
    slide_parser.add_argument("--extra", default=None, help="可选，透传给付费 solve_slide")
    slide_parser.add_argument("--raw", action="store_true", help="仅输出结果主体，不输出包装结构")

    common_parser = subparsers.add_parser("common", help="直接调用云码单图接口")
    common_parser.add_argument("--image", default=None, help="图片路径或 base64")
    common_parser.add_argument("--type", required=True, help="云码 captcha_type")
    common_parser.add_argument("--extra", default=None, help="可选附加说明")
    common_parser.add_argument("--raw", action="store_true", help="仅输出结果主体，不输出包装结构")

    guess_parser = subparsers.add_parser("guess", help="根据描述猜测推荐的云码 type")
    guess_parser.add_argument("--description", required=True, help="自然语言描述，如 九宫格点选")

    subparsers.add_parser("balance", help="查询当前云码账户余额")

    report_parser = subparsers.add_parser("report-error", help="根据 uniqueCode 对某条记录执行返分")
    report_parser.add_argument("--unique-code", required=True, help="打码返回的 uniqueCode")

    return parser


def _run_cli() -> int:
    parser = _build_cli_parser()
    args = parser.parse_args()
    client = JfbymClient()
    result: Any

    if args.task == "text":
        result = client.solve_auto_fallback(
            task="text",
            image_input=args.image,
            charset_range=args.charset,
            paid_captcha_type=args.paid_type,
            extra=args.extra,
            prefer=args.prefer,
        )
        if args.raw:
            result = result["result"]
    elif args.task == "math":
        result = client.solve_auto_fallback(
            task="math",
            image_input=args.image,
            paid_captcha_type=args.paid_type,
            extra=args.extra,
            prefer=args.prefer,
        )
        if args.raw:
            result = result["result"]
    elif args.task == "slide":
        result = client.solve_auto_fallback(
            task="slide",
            back_image_input=args.background,
            slide_image_input=args.slide,
            paid_captcha_type=args.paid_type,
            extra=args.extra,
            prefer=args.prefer,
        )
        if args.raw:
            result = result["result"]
    elif args.task == "common":
        result = client.solve_common(
            image_input=args.image,
            captcha_type=args.type,
            extra=args.extra,
        )
    elif args.task == "guess":
        result = {
            "description": args.description,
            "captcha_type": client.guess_captcha_type(args.description),
        }
    elif args.task == "balance":
        result = {"balance": client.get_balance()}
    elif args.task == "report-error":
        result = {
            "unique_code": args.unique_code,
            "reported": client.report_error(args.unique_code),
        }
    else:
        parser.error(f"unsupported task: {args.task}")
        return 2

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(_run_cli())
