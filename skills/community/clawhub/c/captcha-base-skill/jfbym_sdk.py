import base64
import os
import time
from typing import Any, Dict, Optional, Union

import requests


class JfbymSdkClient:
    """云码 API SDK。"""

    SKILL_CHANNEL_DEVELOPER_TAG = "ce469e48ee0435c34c170ea3d2a1ab0f"

    def __init__(
        self,
        token: Optional[str] = None,
        base_url: str = "https://api.jfbym.com/api/YmServer",
    ):
        self.token = token or os.environ.get("JFBYM_TOKEN")
        self.skill_channel_developer_tag = self.SKILL_CHANNEL_DEVELOPER_TAG
        self.base_url = base_url.rstrip("/")
        self._headers = {"Content-Type": "application/json"}

    def _require_token(self) -> str:
        if not self.token:
            raise ValueError(
                "当前调用为云端收费接口，需要提供 token。"
                "请在构造时传入 token，或设置环境变量 JFBYM_TOKEN。"
            )
        return self.token

    def _prepare_image(self, img_input: Union[str, bytes]) -> str:
        if isinstance(img_input, str):
            if os.path.exists(img_input):
                with open(img_input, "rb") as f:
                    return base64.b64encode(f.read()).decode()
            return img_input
        if isinstance(img_input, bytes):
            return base64.b64encode(img_input).decode()
        raise ValueError("不支持的图片输入格式")

    def get_balance(self) -> str:
        url = f"{self.base_url}/getUserInfoApi"
        res = requests.post(
            url,
            json={"token": self._require_token(), "type": "score"},
            headers=self._headers,
        ).json()
        if res.get("code") == 10001:
            return res["data"]["score"]
        raise Exception(f"获取余额失败: {res}")

    def report_error(self, unique_code: str) -> bool:
        url = f"{self.base_url}/refundApi"
        res = requests.post(
            url,
            json={"token": self._require_token(), "uniqueCode": unique_code},
            headers=self._headers,
        ).json()
        return res.get("code") == 200

    def solve_common(
        self,
        image_input: Optional[Union[str, bytes]] = None,
        captcha_type: str = "10110",
        extra: Any = None,
        **kwargs,
    ) -> Dict:
        payload = {
            "token": self._require_token(),
            "type": str(captcha_type),
            "developer_tag": self.skill_channel_developer_tag,
        }
        if image_input is not None:
            payload["image"] = self._prepare_image(image_input)
        if extra is not None:
            payload["extra"] = extra
        if kwargs:
            payload.update(kwargs)

        url = f"{self.base_url}/customApi"
        res = requests.post(url, json=payload, headers=self._headers).json()
        if res.get("code") == 10000:
            return res["data"]
        raise Exception(f"打码失败: {res}")

    def solve_slide(
        self,
        slide_image: Union[str, bytes],
        bg_image: Union[str, bytes],
        captcha_type: str = "20111",
        extra: Any = None,
        **kwargs,
    ) -> Dict:
        payload = {
            "token": self._require_token(),
            "type": str(captcha_type),
            "slide_image": self._prepare_image(slide_image),
            "background_image": self._prepare_image(bg_image),
            "developer_tag": self.skill_channel_developer_tag,
        }
        if extra is not None:
            payload["extra"] = extra
        if kwargs:
            payload.update(kwargs)

        url = f"{self.base_url}/customApi"
        res = requests.post(url, json=payload, headers=self._headers).json()
        if res.get("code") == 10000:
            return res["data"]
        raise Exception(f"滑块打码失败: {res}")

    def solve_recaptcha(
        self, googlekey: str, pageurl: str, captcha_type: str = "40010", **kwargs
    ) -> str:
        create_url = f"{self.base_url}/funnelApi"
        payload = {
            "token": self._require_token(),
            "type": str(captcha_type),
            "googlekey": googlekey,
            "pageurl": pageurl,
            "enterprise": kwargs.get("enterprise", 0),
            "invisible": kwargs.get("invisible", 0),
            "developer_tag": self.skill_channel_developer_tag,
        }
        if captcha_type == "40011":
            payload["action"] = kwargs.get("action", "")
            payload["min_score"] = kwargs.get("min_score", "0.8")

        res = requests.post(create_url, json=payload, headers=self._headers).json()
        if res.get("code") != 10000:
            raise Exception(f"创建 ReCAPTCHA 任务失败: {res}")

        captcha_id = res["data"]["captchaId"]
        record_id = res["data"]["recordId"]

        result_url = f"{self.base_url}/funnelApiResult"
        result_payload = {
            "token": self._require_token(),
            "captchaId": captcha_id,
            "recordId": record_id,
        }

        for _ in range(24):
            time.sleep(5)
            poll_res = requests.post(
                result_url, json=result_payload, headers=self._headers
            ).json()
            if poll_res.get("code") == 10001:
                return poll_res["data"]["data"]
            if poll_res.get("code") in [10004, 10009]:
                continue
            if poll_res.get("code") == 10010:
                raise Exception(f"服务层识别任务结束，状态失败: {poll_res}")

        raise Exception("等待 ReCAPTCHA 结果超时")

    @staticmethod
    def guess_captcha_type(description: str) -> str:
        desc = (description or "").lower()

        if any(
            k in desc
            for k in ["空间推理", "方位", "大写", "小写", "上方", "下方", "朝向", "侧对", "空间关系"]
        ):
            if any(k in desc for k in ["无确定", "无按钮", "不需要确定"]):
                return "50009"
            if any(k in desc for k in ["有确定", "确定按钮", "按钮确认"]):
                return "30340"
            return "50009"

        if any(k in desc for k in ["推理拼图", "拼图", "交换图块"]):
            return "30108"
        if "九宫格" in desc or "宫格" in desc:
            return "30008"
        if "轨迹" in desc:
            return "22222"
        if "旋转" in desc:
            if any(k in desc for k in ["双图", "内圈", "外圈"]):
                return "90015"
            return "90007"
        if "问答" in desc:
            return "50103"
        if "滑块" in desc:
            if "单图" in desc or "截图" in desc or "轨迹" in desc:
                return "22222"
            return "20111"
        if "点选" in desc or "点击" in desc:
            if "文字" in desc or "字" in desc:
                return "30100"
            if "图标" in desc or "icon" in desc:
                if "有确定" in desc or "确定按钮" in desc:
                    return "30340"
                return "30104"
            if "成语" in desc or "语序" in desc:
                return "30106"
            if "九宫格" in desc or "宫格" in desc:
                return "30008"
            return "30009"
        if "计算" in desc or "算术" in desc:
            if "中文" in desc:
                return "50101"
            return "50100"
        if "汉字" in desc or "中文" in desc:
            return "10114"
        if "recaptcha" in desc or "谷歌" in desc:
            if "v3" in desc:
                return "40011"
            return "40010"
        if "hcaptcha" in desc:
            return "50013"
        return "10110"
