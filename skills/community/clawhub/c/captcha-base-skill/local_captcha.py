import base64
import os
import re
import tempfile
from io import BytesIO
from typing import Any, Dict, Union


class LocalCaptchaSolver:
    """本地免费验证码能力。"""

    _ddddocr_text_model = None
    _ddddocr_slide_model = None
    _ddddocr_det_model = None

    @staticmethod
    def _base64_to_image(base64_str: str, file_name: str) -> None:
        from PIL import Image

        base64_data = re.sub(r"^data:image/.+;base64,", "", base64_str)
        byte_data = base64.b64decode(base64_data)
        image_data = BytesIO(byte_data)
        img = Image.open(image_data)
        img.save(file_name)

    @staticmethod
    def to_image_bytes(image_input: Union[str, bytes]) -> bytes:
        if isinstance(image_input, bytes):
            return image_input
        if isinstance(image_input, str):
            if os.path.exists(image_input):
                with open(image_input, "rb") as f:
                    return f.read()
            base64_data = re.sub(r"^data:image/.+;base64,", "", image_input.strip())
            try:
                return base64.b64decode(base64_data)
            except Exception as exc:
                raise ValueError("本地识别仅支持文件路径、bytes 或 base64 字符串") from exc
        raise ValueError("本地识别仅支持文件路径、bytes 或 base64 字符串")

    @staticmethod
    def to_base64_string(image_input: Union[str, bytes]) -> str:
        image_bytes = LocalCaptchaSolver.to_image_bytes(image_input)
        return base64.b64encode(image_bytes).decode()

    @classmethod
    def _get_ddddocr_text_model(cls):
        if cls._ddddocr_text_model is None:
            try:
                import ddddocr
            except ImportError as exc:
                raise ImportError("缺少本地 OCR 依赖，请安装: pip install ddddocr") from exc
            try:
                cls._ddddocr_text_model = ddddocr.DdddOcr(show_ad=False)
            except TypeError:
                cls._ddddocr_text_model = ddddocr.DdddOcr()
        return cls._ddddocr_text_model

    @classmethod
    def _get_ddddocr_slide_model(cls):
        if cls._ddddocr_slide_model is None:
            try:
                import ddddocr
            except ImportError as exc:
                raise ImportError("缺少本地 OCR 依赖，请安装: pip install ddddocr") from exc
            try:
                cls._ddddocr_slide_model = ddddocr.DdddOcr(ocr=False, det=False, show_ad=False)
            except TypeError:
                cls._ddddocr_slide_model = ddddocr.DdddOcr(ocr=False, det=False)
        return cls._ddddocr_slide_model

    @classmethod
    def _get_ddddocr_det_model(cls):
        if cls._ddddocr_det_model is None:
            try:
                import ddddocr
            except ImportError as exc:
                raise ImportError("缺少本地 OCR 依赖，请安装: pip install ddddocr") from exc
            try:
                cls._ddddocr_det_model = ddddocr.DdddOcr(ocr=False, det=True, show_ad=False)
            except TypeError:
                cls._ddddocr_det_model = ddddocr.DdddOcr(ocr=False, det=True)
        return cls._ddddocr_det_model

    @classmethod
    def solve_text_captcha(cls, image_input: Union[str, bytes], png_fix: bool = False) -> str:
        image_bytes = cls.to_image_bytes(image_input)
        ocr = cls._get_ddddocr_text_model()
        try:
            result = ocr.classification(image_bytes, png_fix=png_fix)
        except TypeError:
            result = ocr.classification(image_bytes)
        text = str(result).strip()
        if not text:
            raise ValueError("本地文本识别失败，返回为空")
        return text

    @classmethod
    def solve_text_captcha_with_range(
        cls,
        image_input: Union[str, bytes],
        charset_range: str = "0123456789abcdefghijklmnopqrstuvwxyz",
        png_fix: bool = False,
    ) -> str:
        image_bytes = cls.to_image_bytes(image_input)
        try:
            import ddddocr
        except ImportError as exc:
            raise ImportError("缺少本地 OCR 依赖，请安装: pip install ddddocr") from exc

        try:
            ocr = ddddocr.DdddOcr(show_ad=False)
        except TypeError:
            ocr = ddddocr.DdddOcr()
        if charset_range:
            ocr.set_ranges(charset_range)
        try:
            result = ocr.classification(image_bytes, png_fix=png_fix)
        except TypeError:
            result = ocr.classification(image_bytes)
        text = str(result).strip()
        if not text:
            raise ValueError("本地文本识别失败，返回为空")
        return text

    @classmethod
    def solve_slide_distance_ddddocr(
        cls,
        back_image_input: Union[str, bytes],
        slide_image_input: Union[str, bytes],
        simple_target: bool = False,
    ) -> Dict[str, Any]:
        back_bytes = cls.to_image_bytes(back_image_input)
        slide_bytes = cls.to_image_bytes(slide_image_input)
        matcher = cls._get_ddddocr_slide_model()
        try:
            result = matcher.slide_match(
                target_bytes=slide_bytes,
                background_bytes=back_bytes,
                simple_target=simple_target,
            )
        except Exception as exc:
            raise ValueError(f"ddddocr 滑块匹配异常: {exc}") from exc
        target = result.get("target") if isinstance(result, dict) else None
        if not target or len(target) < 2:
            raise ValueError(f"ddddocr 滑块匹配失败: {result}")
        return {
            "x": int(target[0]),
            "y": int(target[1]),
            "target": target,
            "raw": result,
        }

    @classmethod
    def detect_text_boxes(cls, image_input: Union[str, bytes]):
        image_bytes = cls.to_image_bytes(image_input)
        detector = cls._get_ddddocr_det_model()
        return detector.detection(img_bytes=image_bytes)

    @staticmethod
    def _normalize_math_expression(text: str) -> str:
        expr = text.strip()
        replacements = {
            "×": "*",
            "x": "*",
            "X": "*",
            "÷": "/",
            "＋": "+",
            "－": "-",
            "—": "-",
            "＝": "",
            "=": "",
            "？": "",
            "?": "",
        }
        for src, dst in replacements.items():
            expr = expr.replace(src, dst)
        expr = re.sub(r"\s+", "", expr)
        expr = re.sub(r"[^0-9+\-*/()]", "", expr)
        return expr

    @staticmethod
    def _safe_eval_math_expression(expression: str):
        import ast
        import operator as op

        operators = {
            ast.Add: op.add,
            ast.Sub: op.sub,
            ast.Mult: op.mul,
            ast.Div: op.truediv,
            ast.USub: op.neg,
            ast.UAdd: op.pos,
        }

        def _eval(node):
            if isinstance(node, ast.Expression):
                return _eval(node.body)
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                return node.value
            if isinstance(node, ast.Num):
                return node.n
            if isinstance(node, ast.BinOp) and type(node.op) in operators:
                return operators[type(node.op)](_eval(node.left), _eval(node.right))
            if isinstance(node, ast.UnaryOp) and type(node.op) in operators:
                return operators[type(node.op)](_eval(node.operand))
            raise ValueError("不支持的数学表达式")

        parsed = ast.parse(expression, mode="eval")
        value = _eval(parsed)
        if isinstance(value, float) and value.is_integer():
            return int(value)
        return value

    @classmethod
    def solve_math_captcha(cls, image_input: Union[str, bytes]) -> Dict[str, str]:
        raw_text = cls.solve_text_captcha(image_input, png_fix=True)
        expression = cls._normalize_math_expression(raw_text)
        if not expression:
            raise ValueError(f"无法提取算术表达式，OCR原文: {raw_text}")
        result = cls._safe_eval_math_expression(expression)
        return {
            "raw_text": raw_text,
            "expression": expression,
            "result": str(result),
        }

    @staticmethod
    def _trim_slide_image(slideimg: str) -> None:
        from PIL import Image, ImageChops

        im = Image.open(slideimg)
        bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
        diff = ImageChops.difference(im, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        if bbox:
            new_im = im.crop(bbox)
            new_im.save(slideimg)

    @staticmethod
    def solve_slide_distance(back_img_base64: str, slide_img_base64: str) -> int:
        try:
            import cv2
            import numpy as np
        except ImportError as exc:
            raise ImportError(
                "缺少本地滑块依赖，请安装: pip install opencv-python-headless numpy Pillow"
            ) from exc

        with tempfile.TemporaryDirectory() as tmp_dir:
            backimg = os.path.join(tmp_dir, "backimg.png")
            slideimg = os.path.join(tmp_dir, "slideimg.png")
            block_name = os.path.join(tmp_dir, "block.jpg")
            template_name = os.path.join(tmp_dir, "template.jpg")

            LocalCaptchaSolver._base64_to_image(back_img_base64, backimg)
            LocalCaptchaSolver._base64_to_image(slide_img_base64, slideimg)

            LocalCaptchaSolver._trim_slide_image(slideimg)
            template = cv2.imread(slideimg, 0)
            block = cv2.imread(backimg, 0)
            if block is None or template is None:
                raise ValueError("滑块图片解析失败，请检查 base64 输入")

            cv2.imwrite(block_name, block)
            cv2.imwrite(template_name, template)

            block = cv2.imread(block_name)
            block = cv2.GaussianBlur(block, (3, 3), 0)
            block = cv2.cvtColor(block, cv2.COLOR_RGB2GRAY)
            block = abs(255 - block)
            cv2.imwrite(block_name, block)
            block = cv2.imread(block_name)

            template = cv2.imread(template_name)
            template = cv2.GaussianBlur(template, (3, 3), 0)
            template = cv2.cvtColor(template, cv2.COLOR_RGB2GRAY)
            template = abs(255 - template)
            cv2.imwrite(template_name, template)
            template = cv2.imread(template_name)

            result = cv2.matchTemplate(block, template, cv2.TM_CCOEFF_NORMED)
            _, y = np.unravel_index(result.argmax(), result.shape)
            return int(y)
