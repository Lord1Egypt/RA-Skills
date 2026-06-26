"""OpenAPI 凭据场景：首次开通 / 续期 / 重置。"""

from __future__ import annotations

from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

SCENARIO_SETUP = "setup"
SCENARIO_RENEW = "renew"
SCENARIO_RESET = "reset"

ACTION_SETUP = SCENARIO_SETUP
ACTION_RENEW = SCENARIO_RENEW
ACTION_RESET = SCENARIO_RESET
ACTION_CONTACT_SUPPORT = "contact_support"

CONTACT_SUPPORT_USER_MESSAGE = (
    "您的 OpenAPI 账号当前无法继续使用。"
    "请联系星财富客服处理，暂无法通过扫码自助恢复。"
)

FORGET_API_PARAMS_HINT = (
    "若您之前已经开通过 OpenAPI（凭据丢失、换设备等场景无法区分），"
    "请在页面上点击「忘记 API 参数」按钮完成重置；"
    "若是首次开通，则直接按开通流程操作，无需点击该按钮。"
)

SETUP_USER_MESSAGE = (
    "二维码已通过附件发送，请在附件中查看并扫描；也可点击下方链接打开完成 OpenAPI 开通。"
    f"{FORGET_API_PARAMS_HINT}"
    "首次开通完成后请回复「开通好了」，我会再次验证凭证。"
    "若您点击了「忘记 API 参数」并完成重置，请把页面上显示的 API Key 与服务端公钥"
    "（两段 PEM 原文）一并发给我，我会写入本地凭证后再验证。"
    "请您确认：能否在附件中看到二维码图片？如看不到（只有链接/报错等），请告诉我，我会换方式重发。"
)

RENEW_USER_MESSAGE = (
    "您的 OpenAPI 账号已过期，需要续期。"
    "二维码已通过附件发送，请在附件中查看并扫描；也可点击下方链接打开完成续期，完成后请重试刚才的操作。"
    "续期只会延长您原有 API Key 的有效期，不需要更换或重新填写 API Key。"
    "请您确认：能否在附件中看到二维码图片？如看不到（只有链接/报错等），请告诉我，我会换方式重发。"
)

RESET_USER_MESSAGE = (
    "您的 OpenAPI 对接凭证需要重新设置。"
    "二维码已通过附件发送，请在附件中查看并扫描；也可点击下方链接打开，在页面上点击「忘记 API 参数」完成参数重置。"
    "完成后，请把页面上显示的 API Key 与服务端公钥（两段 PEM 原文）一并复制发送给我，"
    "我会帮您更新本地凭证。"
    "注意：扫码重置不会自动更新您电脑里的凭据，必须同时提供页面上的 API Key 与服务端公钥。"
    "请您确认：能否在附件中看到二维码图片？如看不到（只有链接/报错等），请告诉我，我会换方式重发。"
)

UPDATE_API_KEY_COMMAND = (
    "python3 fosun-env-setup/code/ensure_fosun_env.py "
    "--api-key <页面 API Key> --server-public-key '<页面服务端公钥 PEM 全文>'"
)


def build_open_url(url: str, *, is_expired: bool | None = None) -> str:
    """解析并重写 hash 片段 query；续期设 isExpired=1，重置/开通移除 isExpired。"""
    url = str(url or "").strip()
    if not url:
        return url

    parts = urlsplit(url)
    fragment = parts.fragment
    if "?" in fragment:
        route, query = fragment.split("?", 1)
    else:
        route, query = fragment, ""

    params = dict(parse_qsl(query, keep_blank_values=True))
    if is_expired is True:
        params["isExpired"] = "1"
    elif is_expired is False:
        params.pop("isExpired", None)

    new_query = urlencode(params)
    if new_query:
        new_fragment = f"{route}?{new_query}"
    else:
        new_fragment = route
    return urlunsplit((parts.scheme, parts.netloc, parts.path, parts.query, new_fragment))


def operation_guide(scenario: str) -> list[str]:
    common = [
        "按 show_qr_rule 一次多发二维码（deliver_attachments + 链接必做，media/data URI 可选），"
        "用 deliver_attachments 时须在回复中提醒用户在附件中查看二维码，发完问用户能否看到",
        "逐字符发送 exact_open_url（禁止改域名）",
    ]
    if scenario == SCENARIO_RENEW:
        return common + [
            "告知用户：OpenAPI 账号已过期，扫码续期即可，无需更换 API Key",
            "用户扫码续期完成后，直接重试之前失败的操作；禁止要求用户回填 API Key",
        ]
    if scenario == SCENARIO_RESET:
        return common + [
            "告知用户：必须在页面上点击「忘记 API 参数」完成重置",
            "用户必须把页面上 API Key 与服务端公钥（PEM 全文）一并发给你，缺一不可",
            f"收到后执行：{UPDATE_API_KEY_COMMAND}",
            "禁止只回填 apikey、不得省略服务端公钥；写入后验证或让用户重试原业务命令",
        ]
    return common + [
        FORGET_API_PARAMS_HINT,
        "首次开通：用户在页面完成开通后回复「开通好了」，再次运行 ensure_fosun_env.py 验证",
        "换设备/点击「忘记 API 参数」：必须等用户发来页面上 API Key **与**服务端公钥（PEM），"
        f"再执行 {UPDATE_API_KEY_COMMAND}（写入 apikey、页面服务端公钥，并晋升本次 ticket 客户端私钥）后验证",
        "硬性规则：用户发来 apikey 时，若尚未收到同页面的服务端公钥，先向用户索要公钥，"
        "凑齐两者后一次性执行回填；禁止只执行 --api-key。工具会在 finalize 时自动识别"
        "有效/过期/无效并路由（过期→自动续期）。换设备且原 apikey 已过期时，"
        "须先回填 apikey+服务端公钥，才能被识别为过期并进入续期。",
    ]


def scenario_fields(scenario: str) -> dict[str, object]:
    """返回 pending / 错误分派共用的结构化引导字段。"""
    if scenario == SCENARIO_RENEW:
        return {
            "credential_scenario": SCENARIO_RENEW,
            "account_action": ACTION_RENEW,
            "user_message": RENEW_USER_MESSAGE,
            "hint": (
                "apikey 已过期，走 TicketCreate 续期（URL 带 isExpired=1）。"
                "续期只延长原 apikey 有效期，不覆盖 fosun.env 中的 API Key 与服务端公钥。"
            ),
            "next_action": (
                "按 show_qr_rule 一次多发二维码并发链接；"
                "告知用户扫码续期；续期完成后让用户重试原命令。本地已有 apikey 时无需回填。"
                "例外：若续期报「需要本地已有 API Key」（换新设备、本地无 apikey），"
                "改走开通/重置签码并让用户回填 apikey，工具会自动识别过期再转续期。"
            ),
            "requires_api_key_from_user": False,
            "renew_only": True,
        }
    if scenario == SCENARIO_RESET:
        return {
            "credential_scenario": SCENARIO_RESET,
            "account_action": ACTION_RESET,
            "user_message": RESET_USER_MESSAGE,
            "hint": (
                "本地 apikey 无效或密钥不匹配，已轮换客户端密钥并走 TicketCreate 重置。"
                "用户必须在页面上点击「忘记 API 参数」；扫码不会自动更新 fosun.env 中的 API Key。"
            ),
            "next_action": (
                "① 按 show_qr_rule 一次多发二维码并发链接，提醒用户点击「忘记 API 参数」；"
                f"② 收到页面 API Key **与**服务端公钥后执行 {UPDATE_API_KEY_COMMAND}；"
                "③ 再运行 ensure_fosun_env.py 或让用户重试原命令。禁止只回填 apikey。"
            ),
            "requires_api_key_from_user": True,
            "requires_server_public_key_from_user": True,
            "update_api_key_command": UPDATE_API_KEY_COMMAND,
        }
    return {
        "credential_scenario": SCENARIO_SETUP,
        "account_action": ACTION_SETUP,
        "user_message": SETUP_USER_MESSAGE,
        "hint": (
            "首次开通、换设备、凭据丢失三者无法区分；过期 apikey 也可能叠加在换设备上。"
            "若用户曾开通过 OpenAPI，须提醒其在页面上点击「忘记 API 参数」；首次开通则直接走开通流程。"
            "换设备时本地没有 apikey，无法直接续期；只能先开通/重置签码、由用户回填 apikey，"
            "工具会在 finalize 时自动判定是否过期并转续期。"
        ),
        "next_action": (
            "按 show_qr_rule 一次多发二维码并发链接；"
            "首次开通：用户回复「开通好了」后再次运行 ensure_fosun_env.py；"
            "换设备/点击「忘记 API 参数」：等用户发来页面上 API Key 与服务端公钥，"
            f"执行 {UPDATE_API_KEY_COMMAND} 后验证。禁止只回填 apikey。"
            "硬性规则：apikey 与服务端公钥凑齐后一次性回填；首次开通仍回复「开通好了」即可。"
        ),
        "requires_api_key_from_user": False,
        "conditional_api_key_backfill": True,
        "requires_server_public_key_on_backfill": True,
        "update_api_key_command": UPDATE_API_KEY_COMMAND,
    }
