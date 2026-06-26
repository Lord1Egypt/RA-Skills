#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


BUILDER_URL = "https://scraperapi.dataify.com/builder?platform=1"
DASHBOARD_URL = "https://dashboard.dataify.com?utm_source=skill"
LOGIN_URL = "https://dashboard.dataify.com/login?utm_source=skill"
MIN_PYTHON = (3, 6)
DEFAULT_URL = "https://www.youtube.com/watch?v=_SdpvpvVrLY"
DEFAULT_KILOHERTZ = "48000"
DEFAULT_KILOHERTZ_DIRECTION = "<="
DEFAULT_AUDIO_FORMAT = "opus"
DEFAULT_BITRATE = "320"
DEFAULT_BITRATE_DIRECTION = "<="
DEFAULT_SUBTITLES_LANGUAGE = "ab"
DEFAULT_IS_SUBTITLES = "false"
DEFAULT_SELECTED_ONLY = "false"
DEFAULT_FILE_NAME = "{{TasksID}}"

KILOHERTZ_OPTIONS = [
    ("48kHz", "48000"), ("44.1kHz", "44100"), ("32kHz", "32000"), ("22.5kHz", "22500"), ("16kHz", "16000"), ("8kHz", "8000"),
]
AUDIO_FORMAT_OPTIONS = [("Opus格式", "opus"), ("AAC格式", "m4a")]
BITRATE_OPTIONS = [
    ("48Kbps", "48"), ("64 Kbps", "64"), ("128 Kbps", "128"), ("160 Kbps", "160"), ("256 Kbps", "256"), ("320 Kbps", "320"),
]
DIRECTION_OPTIONS = [("Less than or equal to", "<="), ("Greater than or equal to", ">=")]
BOOLEAN_OPTIONS = [("False", "false"), ("True", "true")]

SUBTITLES_LANGUAGE_OPTIONS = [
    ("阿布哈西亚语", "ab"), ("阿尔巴尼亚语", "sq"), ("阿法尔语", "aa"), ("阿肯语", "ak"), ("阿拉伯语", "ar"),
    ("阿姆哈拉语", "am"), ("阿萨姆语", "as"), ("阿塞拜疆语", "az"), ("埃维语", "ee"), ("艾马拉语", "ay"),
    ("爱尔兰语", "ga"), ("爱沙尼亚语", "et"), ("奥克语", "oc"), ("奥里亚语", "or"), ("奥罗莫语", "om"),
    ("奥塞梯语", "os"), ("巴什基尔语", "ba"), ("巴斯克语", "eu"), ("白俄罗斯语", "be"), ("邦板牙语", "pam"),
    ("保加利亚语", "bg"), ("北索托语", "nso"), ("冰岛语", "is"), ("波兰语", "pl"), ("波斯尼亚语", "bs"),
    ("波斯语", "fa"), ("博杰普尔语", "bho"), ("布列塔尼语", "br"), ("藏语", "bo"), ("茨瓦纳语", "tn"),
    ("聪加语", "ts"), ("鞑靼语", "tt"), ("丹麦语", "da"), ("德语", "de"), ("迪维希语", "dv"),
    ("俄语", "ru"), ("法罗语", "fo"), ("法语", "fr"), ("梵语", "sa"), ("菲律宾语", "fil"),
    ("斐济语", "fj"), ("芬兰语", "fi"), ("高棉语", "km"), ("格陵兰语", "kl"), ("格鲁吉亚语", "ka"),
    ("古吉拉特语", "gu"), ("瓜拉尼语", "gn"), ("哈萨克语", "kk"), ("海地克里奥尔语", "ht"), ("韩语", "ko"),
    ("豪萨语", "ha"), ("荷兰语", "nl"), ("吉尔吉斯语", "ky"), ("加利西亚语", "gl"), ("加泰罗尼亚语", "ca"),
    ("加族语", "gaa"), ("捷克语", "cs"), ("卡纳达语", "kn"), ("卡西语", "kha"), ("科萨语", "xh"),
    ("科西嘉语", "co"), ("克罗地亚语", "hr"), ("克丘亚语", "qu"), ("库尔德语", "ku"), ("拉丁语", "la"),
    ("拉脱维亚语", "lv"), ("老挝语", "lo"), ("立陶宛语", "lt"), ("林加拉语", "ln"), ("隆迪语", "rn"),
    ("卢奥语", "luo"), ("卢巴-卢拉语", "lua"), ("卢干达语", "lg"), ("卢森堡语", "lb"), ("卢旺达语", "rw"),
    ("罗马尼亚语", "ro"), ("马恩语", "gv"), ("马耳他语", "mt"), ("马拉地语", "mr"), ("马拉加斯语", "mg"),
    ("马拉雅拉姆语", "ml"), ("马来语", "ms"), ("马其顿语", "mk"), ("毛里求斯克里奥尔语", "mfe"), ("毛利语", "mi"),
    ("蒙古语", "mn"), ("孟加拉语", "bn"), ("缅甸语", "my"), ("苗语", "hmn"), ("南非荷兰语", "af"),
    ("南索托语", "st"), ("尼泊尔语", "ne"), ("尼瓦尔语", "new"), ("挪威语", "no"), ("旁遮普语", "pa"),
    ("葡萄牙语", "pt"), ("葡萄牙语（葡萄牙）", "pt-PT"), ("普什图语", "ps"), ("齐切瓦语", "ny"), ("日语", "ja"),
    ("瑞典语", "sv"), ("萨摩亚语", "sm"), ("塞尔维亚语", "sr"), ("塞舌尔克里奥尔语", "crs"), ("桑戈语", "sg"),
    ("僧伽罗语", "si"), ("绍纳语", "sn"), ("世界语", "eo"), ("斯洛伐克语", "sk"), ("斯洛文尼亚语", "sl"),
    ("斯瓦蒂语", "ss"), ("斯瓦希里语", "sw"), ("苏格兰盖尔语", "gd"), ("宿务语", "ceb"), ("索马里语", "so"),
    ("塔吉克语", "tg"), ("泰卢固语", "te"), ("泰米尔语", "ta"), ("泰语", "th"), ("汤加语", "to"),
    ("提格利尼亚语", "ti"), ("通布卡语", "tum"), ("土耳其语", "tr"), ("土库曼语", "tk"), ("瓦瑞语", "war"),
    ("威尔士语", "cy"), ("维吾尔语", "ug"), ("文达语", "ve"), ("沃洛夫语", "wo"), ("乌尔都语", "ur"),
    ("乌克兰语", "uk"), ("乌兹别克语", "uz"), ("西班牙语", "es"), ("西弗里西亚语", "fy"), ("希伯来语", "iw"),
    ("希腊语", "el"), ("夏威夷语", "haw"), ("信德语", "sd"), ("匈牙利语", "hu"), ("巽他语", "su"),
    ("亚美尼亚语", "hy"), ("伊博语", "ig"), ("意大利语", "it"), ("意第绪语", "yi"), ("因纽特语", "iu"),
    ("印地语", "hi"), ("印度尼西亚语", "id"), ("英语", "en"), ("约鲁巴语", "yo"), ("越南语", "vi"),
    ("爪哇语", "jv"), ("中文（繁体）", "zh-Hant"), ("中文（简体）", "zh-Hans"), ("宗卡语", "dz"), ("祖鲁语", "zu"),
    ("Kri", "kri"),
]
SELECTED_ONLY_OPTIONS = [("否", "false"), ("是", "true")]


def ensure_python_version():
    if sys.version_info < MIN_PYTHON:
        print(
            "Python {}.{} or newer is required. Run this script with a Python 3 interpreter, for example: python3 scripts/submit_dataify_youtube_audio_by_url.py --url \"{}\"".format(
                MIN_PYTHON[0],
                MIN_PYTHON[1],
                DEFAULT_URL,
            ),
            file=sys.stderr,
        )
        return False
    return True


def print_option_table(title, options):
    print("\n{} options:\n".format(title))
    print("| Label | Value |")
    print("| --- | --- |")
    for label, value in options:
        print("| {} | `{}` |".format(label, value))


def list_options():
    print_option_table("kilohertz", KILOHERTZ_OPTIONS)
    print_option_table("kilohertz_direction", DIRECTION_OPTIONS)
    print_option_table("audio_format", AUDIO_FORMAT_OPTIONS)
    print_option_table("bitrate", BITRATE_OPTIONS)
    print_option_table("bitrate_direction", DIRECTION_OPTIONS)
    print_option_table("subtitles_language", SUBTITLES_LANGUAGE_OPTIONS)
    print_option_table("is_subtitles", BOOLEAN_OPTIONS)
    print_option_table("selected_only", SELECTED_ONLY_OPTIONS)


def normalize_text(value, field_name):
    clean = str(value).strip()
    if not clean:
        raise ValueError("{} cannot be empty".format(field_name))
    return clean


def normalize_choice(value, options, field_name):
    clean = str(value).strip()
    allowed = {option_value for _, option_value in options}
    if clean not in allowed:
        raise ValueError("Unsupported {}: {}. Use an allowed dropdown value.".format(field_name, clean))
    return clean


def normalize_url(value):
    clean = normalize_text(value, "url")
    if not clean.startswith("https://www.youtube.com/"):
        raise ValueError("url must start with https://www.youtube.com/")
    return clean


def normalize_direction(value, field_name):
    return normalize_choice(value, DIRECTION_OPTIONS, field_name)


def with_direction(direction, value):
    return "{}{}".format(direction, value)


def normalize_file_name(value):
    if value is None:
        return DEFAULT_FILE_NAME
    clean = str(value).strip()
    if not clean:
        raise ValueError("File name cannot be empty")
    return clean


def normalize_group(group):
    return {
        "url": normalize_url(group.get("url", DEFAULT_URL)),
    }


def normalize_universal(args):
    kilohertz = normalize_choice(args.kilohertz, KILOHERTZ_OPTIONS, "kilohertz")
    kilohertz_direction = normalize_direction(args.kilohertz_direction, "kilohertz_direction")
    bitrate = normalize_choice(args.bitrate, BITRATE_OPTIONS, "bitrate")
    bitrate_direction = normalize_direction(args.bitrate_direction, "bitrate_direction")
    return {
        "bitrate": with_direction(bitrate_direction, bitrate),
        "audio_format": normalize_choice(args.audio_format, AUDIO_FORMAT_OPTIONS, "audio_format"),
        "subtitles_language": normalize_choice(args.subtitles_language, SUBTITLES_LANGUAGE_OPTIONS, "subtitles_language"),
        "kilohertz": with_direction(kilohertz_direction, kilohertz),
        "is_subtitles": normalize_choice(args.is_subtitles, BOOLEAN_OPTIONS, "is_subtitles"),
        "selected_only": normalize_choice(args.selected_only, SELECTED_ONLY_OPTIONS, "selected_only"),
    }


def load_groups_from_json(raw):
    try:
        payload = json.loads(raw)
    except ValueError as exc:
        raise ValueError("params-json must be valid JSON: {}".format(exc))
    if not isinstance(payload, list) or not payload:
        raise ValueError("params-json must be a non-empty JSON array")
    groups = []
    for item in payload:
        if not isinstance(item, dict):
            raise ValueError("Each params-json item must be an object")
        groups.append(normalize_group(item))
    return groups


def build_groups(args):
    if args.params_json:
        return load_groups_from_json(args.params_json)
    urls = args.url or [DEFAULT_URL]
    return [normalize_group({"url": url}) for url in urls]


def submit_builder(api_token, groups, spider_universal, file_name):
    form = {
        "spider_name": "youtube.com",
        "spider_id": "youtube_audio_by-url",
        "spider_parameters": json.dumps(groups, ensure_ascii=False, separators=(",", ":")),
        "spider_universal": json.dumps(spider_universal, ensure_ascii=False, separators=(",", ":")),
        "spider_errors": "true",
        "file_name": file_name,
    }
    body = urllib.parse.urlencode(form).encode("utf-8")
    request = urllib.request.Request(
        BUILDER_URL,
        data=body,
        headers={
            "Authorization": "Bearer {}".format(api_token),
            "Content-Type": "application/x-www-form-urlencoded",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError("Builder request failed with HTTP {}: {}".format(exc.code, detail))
    except urllib.error.URLError as exc:
        raise RuntimeError("Builder request failed: {}".format(exc.reason))

    try:
        payload = json.loads(raw)
    except ValueError:
        raise RuntimeError("Builder returned non-JSON response: {}".format(raw))

    data = payload.get("data", {})
    if not isinstance(data, dict):
        data = {}
    task_id = data.get("task_id")
    if not task_id:
        raise RuntimeError("Builder did not return task_id. Response: {}".format(json.dumps(payload, ensure_ascii=False)))
    status = data.get("status") or payload.get("status") or payload.get("message") or "submitted"
    return task_id, status


def main():
    if not ensure_python_version():
        return 2

    parser = argparse.ArgumentParser(description="Submit a Dataify YouTube audio file by URL Builder task.")
    parser.add_argument("--list-options", action="store_true", help="Print dropdown options as Markdown tables and exit.")
    parser.add_argument("--url", action="append", help="YouTube URL. Repeat for multiple URLs.")
    parser.add_argument("--kilohertz", default=DEFAULT_KILOHERTZ, help="Shared kilohertz value. Default: 48000.")
    parser.add_argument("--kilohertz-direction", default=DEFAULT_KILOHERTZ_DIRECTION, help="Shared kilohertz direction. Default: <=.")
    parser.add_argument("--audio-format", default=DEFAULT_AUDIO_FORMAT, help="Shared audio_format value. Default: opus.")
    parser.add_argument("--bitrate", default=DEFAULT_BITRATE, help="Shared bitrate value. Default: 320.")
    parser.add_argument("--bitrate-direction", default=DEFAULT_BITRATE_DIRECTION, help="Shared bitrate direction. Default: <=.")
    parser.add_argument("--subtitles-language", default=DEFAULT_SUBTITLES_LANGUAGE, help="Shared subtitles_language value. Default: ab.")
    parser.add_argument("--is-subtitles", default=DEFAULT_IS_SUBTITLES, help="Shared is_subtitles value. Default: false.")
    parser.add_argument("--selected-only", default=DEFAULT_SELECTED_ONLY, help="Shared selected_only value. Default: false.")
    parser.add_argument("--file-name", default=DEFAULT_FILE_NAME, help="Builder file_name field. Default: {{TasksID}}.")
    parser.add_argument("--params-json", help="JSON array of url parameter objects.")
    parser.add_argument("--api-token", default=os.environ.get("DATAIFY_API_TOKEN"), help="Dataify token. Defaults to DATAIFY_API_TOKEN.")
    args = parser.parse_args()

    if args.list_options:
        list_options()
        return 0

    if not args.api_token:
        print(
            "Missing Dataify API TOKEN. Enter your Dataify API TOKEN to continue. If you want to reuse it later, save it as DATAIFY_API_TOKEN. If you do not have one, log in at {} to get one.".format(LOGIN_URL),
            file=sys.stderr,
        )
        return 2

    try:
        groups = build_groups(args)
        spider_universal = normalize_universal(args)
        file_name = normalize_file_name(args.file_name)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    try:
        task_id, status = submit_builder(args.api_token, groups, spider_universal, file_name)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(json.dumps(
        {
            "task_id": task_id,
            "status": status,
            "parameters": groups,
            "spider_universal": spider_universal,
            "file_name": file_name,
            "dashboard_url": DASHBOARD_URL,
            "message": "Task submitted. Visit {} to view results.".format(DASHBOARD_URL),
        },
        ensure_ascii=False,
        indent=2,
    ))
    return 0


if __name__ == "__main__":
    sys.exit(main())
