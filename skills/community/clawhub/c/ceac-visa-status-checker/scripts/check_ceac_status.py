import base64
import json
import os
import re
import time
from typing import Dict, Optional

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv


ROOT = "https://ceac.state.gov"
STATUS_URL = f"{ROOT}/ceacstattracker/status.aspx?App=NIV"
POST_URL = f"{ROOT}/ceacstattracker/status.aspx"
CAPTCHA_IMG_ID = "c_status_ctl00_contentplaceholder1_defaultcaptcha_CaptchaImage"


def _normalize(text: str) -> str:
    return " ".join((text or "").strip().upper().split())


def _extract_hidden_inputs(soup: BeautifulSoup) -> Dict[str, str]:
    result: Dict[str, str] = {}
    for inp in soup.find_all("input", attrs={"type": "hidden"}):
        name = inp.get("name")
        if not name:
            continue
        result[name] = inp.get("value", "")
    return result


def _find_location_value(soup: BeautifulSoup, location_text: str) -> Optional[str]:
    dropdown = soup.find("select", id="Location_Dropdown")
    if not dropdown:
        return None

    target = _normalize(location_text)
    fallback = None

    for option in dropdown.find_all("option"):
        value = option.get("value", "")
        label = _normalize(option.get_text(" ", strip=True))
        if not value:
            continue

        if label == target:
            return value

        if target in label and fallback is None:
            fallback = value

    return fallback


def _solve_captcha_with_zhipu(image_bytes: bytes, api_key: str, model: str) -> str:
    image_b64 = base64.b64encode(image_bytes).decode("ascii")
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Read the captcha in this image. Reply with only the captcha text, no spaces, no punctuation.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"},
                    },
                ],
            }
        ],
        "temperature": 0,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    resp = requests.post(
        "https://open.bigmodel.cn/api/paas/v4/chat/completions",
        headers=headers,
        data=json.dumps(payload),
        timeout=45,
    )
    resp.raise_for_status()
    data = resp.json()

    text = (
        data.get("choices", [{}])[0]
        .get("message", {})
        .get("content", "")
    )

    # Keep only uppercase letters and digits for captcha.
    cleaned = re.sub(r"[^A-Za-z0-9]", "", str(text)).upper()
    return cleaned


def query_ceac_status(
    location: str,
    number: str,
    passport_number: str,
    surname: str,
    zhipu_api_key: str,
    zhipu_model_vision: str = "glm-4v-flash",
    max_retries: int = 5,
    retry_delay_seconds: int = 5,
) -> Dict[str, str]:
    session = requests.Session()
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "ceac.state.gov",
    }

    last_error = "unknown"

    for attempt in range(1, max_retries + 1):
        if attempt > 1:
            time.sleep(retry_delay_seconds)

        try:
            page = session.get(STATUS_URL, headers=headers, timeout=45)
            page.raise_for_status()
            soup = BeautifulSoup(page.text, "lxml")

            location_value = _find_location_value(soup, location)
            if not location_value:
                available = []
                dropdown = soup.find("select", id="Location_Dropdown")
                if dropdown:
                    for option in dropdown.find_all("option"):
                        label = option.get_text(" ", strip=True)
                        if label:
                            available.append(label)
                return {
                    "success": False,
                    "error": "LOCATION_NOT_FOUND",
                    "message": "Location not found in CEAC dropdown.",
                    "available_locations_sample": available[:20],
                }

            captcha_img = soup.find("img", id=CAPTCHA_IMG_ID)
            if not captcha_img or not captcha_img.get("src"):
                raise RuntimeError("Captcha image not found on CEAC page.")

            image_url = ROOT + captcha_img["src"]
            image_resp = session.get(image_url, headers=headers, timeout=45)
            image_resp.raise_for_status()

            captcha_text = _solve_captcha_with_zhipu(
                image_resp.content,
                api_key=zhipu_api_key,
                model=zhipu_model_vision,
            )
            if not captcha_text:
                raise RuntimeError("Empty captcha text returned by Zhipu vision model.")

            form_data = _extract_hidden_inputs(soup)
            form_data.update(
                {
                    "ctl00$ToolkitScriptManager1": "ctl00$ContentPlaceHolder1$UpdatePanel1|ctl00$ContentPlaceHolder1$btnSubmit",
                    "__EVENTTARGET": "ctl00$ContentPlaceHolder1$btnSubmit",
                    "__EVENTARGUMENT": "",
                    "__LASTFOCUS": "",
                    "ctl00$ContentPlaceHolder1$Visa_Application_Type": "NIV",
                    "ctl00$ContentPlaceHolder1$Location_Dropdown": location_value,
                    "ctl00$ContentPlaceHolder1$Visa_Case_Number": number,
                    "ctl00$ContentPlaceHolder1$Captcha": captcha_text,
                    "ctl00$ContentPlaceHolder1$Passport_Number": passport_number,
                    "ctl00$ContentPlaceHolder1$Surname": surname,
                    "LBD_BackWorkaround_c_status_ctl00_contentplaceholder1_defaultcaptcha": "1",
                    "__ASYNCPOST": "true",
                }
            )

            post_headers = dict(headers)
            post_headers.update(
                {
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "X-MicrosoftAjax": "Delta=true",
                    "X-Requested-With": "XMLHttpRequest",
                    "Origin": ROOT,
                    "Referer": STATUS_URL,
                }
            )

            submit = session.post(POST_URL, headers=post_headers, data=form_data, timeout=45)
            submit.raise_for_status()

            result_soup = BeautifulSoup(submit.text, "lxml")
            status_tag = result_soup.find(
                "span", id="ctl00_ContentPlaceHolder1_ucApplicationStatusView_lblStatus"
            )
            if not status_tag:
                last_error = "STATUS_NOT_FOUND_MAYBE_CAPTCHA_FAILED"
                continue

            case_no_tag = result_soup.find(
                "span", id="ctl00_ContentPlaceHolder1_ucApplicationStatusView_lblCaseNo"
            )
            visa_type_tag = result_soup.find(
                "span", id="ctl00_ContentPlaceHolder1_ucApplicationStatusView_lblAppName"
            )
            created_tag = result_soup.find(
                "span", id="ctl00_ContentPlaceHolder1_ucApplicationStatusView_lblSubmitDate"
            )
            updated_tag = result_soup.find(
                "span", id="ctl00_ContentPlaceHolder1_ucApplicationStatusView_lblStatusDate"
            )
            message_tag = result_soup.find(
                "span", id="ctl00_ContentPlaceHolder1_ucApplicationStatusView_lblMessage"
            )

            return {
                "success": True,
                "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                "visa_type": visa_type_tag.get_text(strip=True) if visa_type_tag else "",
                "status": status_tag.get_text(strip=True),
                "case_created": created_tag.get_text(strip=True) if created_tag else "",
                "case_last_updated": updated_tag.get_text(strip=True) if updated_tag else "",
                "description": message_tag.get_text(" ", strip=True) if message_tag else "",
                "application_num": case_no_tag.get_text(strip=True) if case_no_tag else number,
                "application_num_origin": number,
                "location": location,
            }
        except Exception as exc:
            last_error = str(exc)

    return {
        "success": False,
        "error": "QUERY_FAILED",
        "message": f"Failed after {max_retries} attempts.",
        "last_error": last_error,
    }


def _require_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required env var: {name}")
    return value


def main() -> None:
    load_dotenv()

    location = _require_env("LOCATION")
    number = _require_env("NUMBER")
    passport_number = _require_env("PASSPORT_NUMBER")
    surname = _require_env("SURNAME")
    zhipu_api_key = _require_env("ZHIPU_API_KEY")
    zhipu_model_vision = os.getenv("ZHIPU_MODEL_VISION", "glm-4v-flash").strip() or "glm-4v-flash"

    max_retries = int(os.getenv("MAX_RETRIES", "5"))
    retry_delay_seconds = int(os.getenv("RETRY_DELAY_SECONDS", "5"))

    result = query_ceac_status(
        location=location,
        number=number,
        passport_number=passport_number,
        surname=surname,
        zhipu_api_key=zhipu_api_key,
        zhipu_model_vision=zhipu_model_vision,
        max_retries=max_retries,
        retry_delay_seconds=retry_delay_seconds,
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not result.get("success"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
