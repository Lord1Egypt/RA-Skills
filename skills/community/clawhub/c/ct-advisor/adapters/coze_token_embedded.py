# ╔═════════════════════════════════════════════════════════════════════════╗
# ║ FILE ROLE · 本文件 = ct-advisor 全部 **Coze 连接凭据** 的唯一存放处          ║
# ║   · ct_advisor_coze  → 后端精校端点 ct-advisor.coze.site/run              ║
# ║       get_token()          由 adapters/refiner.py 调用                    ║
# ║   · ct_bugreport_coze → 错误报告端点 ct-bugreport.coze.site/run           ║
# ║       get_bugreport_token() 由 adapters/bug_report.py 调用               ║
# ║   · 两者均为项目共享的**公开**凭据（XOR+base64 混淆内嵌，非加密），           ║
# ║     随技能发布（2026-08-03 用户授权）。                                     ║
# ║   · 旧的 config/coze_token.py 已于 2026-09-09 删除，凭据全部收敛到本文件。   ║
# ║   · ⚠️ 本文件只放公开共享凭据，**绝不内嵌用户私有 LLM key**。               ║
# ║     前端私有 LLM key 由用户在 workbench 设置框另行填入（不随技能发布）。     ║
# ╚═════════════════════════════════════════════════════════════════════════╝
# NOTE: This file contains obfuscated PUBLIC shared credentials (XOR+base64). They are NOT secrets. See user authorization 2026-08-03.
"""ct-advisor 公共凭据库（XOR+base64 混淆内嵌，镜像 ct-registry 的 OBFUSCATION 模式）。

背景（2026-08-02）：用户授权将 coze 长期 token 随技能**公开发布**，避免每次经环境变量
注入，并规避「推送 config.json 泄露 JWT」的风险（token 不在 config.json 明文、也不在
memory/笔记）。

重要：
- 这是 OBFUSCATION，NOT real encryption。混淆密钥随脚本发布，仅防目录浏览时的明文暴露；
  持脚本者即可还原。但本库只放**公开的、随技能发布**的共用凭据（如访问公共精校端点的
  token），**必须随技能原样保留**，请勿用私有凭据覆盖。
- **切勿把私有凭据内嵌进来**：私有凭据请走 CLI(--token) / env(变量名自定)，不要写进
  EMBEDDED_SECRETS。
- 历史实现曾把 coze token 落盘到 `config/coze.dat`；但 SkillHub 为窄白名单打包（仅
  .svg/.py/.md/.json/.yaml/.txt/.toml/.csv），`.dat` 不在白名单，发布时被静默剥离 →
  已安装技能读不到文件、连不上 coze。故改为**统一内嵌**（见 EMBEDDED_SECRETS），不再依赖
  外部 .dat 文件。本地仍可用 store_token() 写覆盖文件（可选，优先级介于 env 与内嵌之间）。

读取优先级（通用 get_secret）：CLI > env > 局部落盘文件 > 内嵌 blob。三者皆无回退空串。
coze token 走便捷函数 get_token()，等价于 get_secret("ct_advisor_coze", ...)。

新增一个公开 key：把混淆 blob 抄进 EMBEDDED_SECRETS 即可（一行；blob 可用
store_token(plain) 生成后复制其输出）。
"""
from __future__ import annotations

import base64
import os

# 单份混淆密钥（所有公开凭据共用；都是公开凭据，无横向泄露风险）。
OBFUSCATION_KEY = b"ct-advisor-coze-obf-v1-3d9b"

# 内嵌公共凭据库：name -> XOR+base64 混淆 blob。
# 新增 key：store_token(plain) 生成 blob 后抄此一行（不要内嵌私有凭据）。
EMBEDDED_SECRETS = {
    "ct_advisor_coze": (
        "Bg1nCQYxChogG2cwOgAsHCELL14_XFlDPnorVT1HOw45LSpaP0A5BTYydwIvVHQCf2lfD3Yh"
        "U0FjJSFCJScuQGI3BxMrRypRKEckW3RKLgBMBg1nEQdFJBogG2cMCzI3WgwYCVs6A2tEBWpXC"
        "RYeEQg6BD0aO0QUBiM9ewQrDF0UeEZLNWhSViN4NxQcPBk1Jn4kKRIzZQsuNXs4cnReIk0sUU1"
        "BAAo8AREBGmIqA0oWZAI0Uk41eBt8IHAaLjBkUyocDkAhGE5WICkSRA41IB0_W0JLKkMFUjpXM"
        "B45PToYPm4pFR4yZAYtD2cMUmpfCWMPNkJhGF0eCjQEB3RRVkw_floIBERPAk8ALksAJE1FOyJ"
        "PGSkoJFgHKBZVSDxbFncyXh59DmBXLTBkVCkMIAohJmRXIj48VyE2Ix0_WFpaBwooCT1HDg0XP"
        "kYGEB41GiAjFAcGPn8ZaR91DmBQNQ5OUF1GC0EbHk8PVgo_aQBRKEcvBGNJIUEsGTkZLB4_Hj0"
        "VNxwsKzscZAFSSEw_eFhiFH0PDC14Uwk1MEQDRnItPUkvZiAjN1gDYWpwUGZVNTNLNCcOXUUWQ"
        "kUvDTYxQSwMDhsVA1l3LEwDBTVLMiczKBkiM1xOWk4odRhTUV4acx1XIX9SETllBFYdPzQABHV"
        "RDkkTVy5QIlw5d1UGM1ASUw5MAC85KD0fA0lOLRkAeiNPLxoxAkNcFGYKNiR3BgweKwsNJVwKOD"
        "0DYFZSAnVOHF5sFE5WGx8bMz49IERfOkciDEwUazA6LVsSBUReEgs9AARaGwcmJSMjORw2XUMfA"
        "CwlLkUlSW5VNQk7ISJaKhYCChc6MBQrJy4XRV4UIXgRU3kBEHQ4OyZCJTAeJks8NUJVIBgAeCY"
        "hP1wfdWNXMXsaVkVeJSAeLwIrCF81WxYqdzBUIWQvY1hBFGgmITl0JycvOEY8SnkaLhxTbBtRV"
        "WxPQEEGHlMxBRdOOCc7USQmIw=="
    ),
    # 错误报告端点 ct-bugreport.coze.site/run 的共享公开凭据。
    # 与 ct-base/adapters/coze/src/endpoint_token.py::EMBEDDED_SECRETS["ct_bugreport_coze"]
    # 同源同值（全家族共用一份公共凭据，见 ct-base §5）。2026-09-09 由 config/coze_token.py 迁入。
    "ct_bugreport_coze": (
        "Bg1nCQYxChogG2cwOgAsHCELL14_XFlDPnorVT1AOFc4PTEDP0A6FzYyfBYsVGACf2p6HHQh"
        "U0FjGzYcJSQiQGMnDAA8eiUOP1cdAndaLgBMBg1nEQdFJBogG2cMCzI3WgwYCVs6A2tEBWpXCR"
        "YeEQg6BD0aO0QUBiM9ewQrDF0UeEZ5MHQYMT9JJgwXOBgfHEglHxMzeykVNWg_BX4DFHwBUjZ"
        "9Ox4gECpfS3sqA0oWZAI0Uk41eBt8IHAaLjBkUyocDkAhGE5WICkSRA41IB0_W0JLKkMFUDlHA"
        "lY5PTpePm4pFR4yZAYtD2cMUmpfCWMPNkJhGF0eCjQEB3RRVkw_floIBERPAk8ALksAJE1FOyJ"
        "PGSkoJFgHKBZVSDxbFncyXh59DlpQLh5KUyoMKEMiGGBWIS4kGCE2I1c_WFpaBwooCT1HDg0XP"
        "kYGEB41GiAjFAcGPn8ZaR91DmBQNQ5OUF1GC0EbHk8PVgo_aQBRKEcVA2BZDwgtNyUcLDA7XT0"
        "rEVosOyMcZAFSSEtDV2tJIXQGURBDBgoHL0QaPmYkWw43ZRgWFHsHA2FyMmgQCUVFIlcBHjUhB"
        "GYbOjcRTyw0UhsXRH9_PlM2Agx5PiUfGl4XEU8RJE8XGiAFEGUiendXHGAtVCxXNiMRJxsmHRt"
        "TKRZWGSgTBGUOR39gL0sXFU0bWTwjRD4HRl4mXgM8ZFslAFUZVn9KVE82ABJMNxY1ID48ImwmB"
        "gs_egUJUG4pdx1SInRWUQwUVTEzOyMhO34hIjAPX1YGVkU6a0RfA34SCRJMI1YiLycuHx4kDA0"
        "3WCsqCHoRYl12PFA6Ni5eID0FPkEfHU8XWh4uR1chU3QyaXp9UXQJBhh1UCsBIyYIIWMQPxs9S"
        "D4IJHcyRXV3MwpVMz9BFggkXDEYPlQCAz8HTgRTDmEadml2EHY4M0F4MC8iJDIGSxQ3XyIPWgE"
        "2EhwcHG53KGkuFhB0GDBOHiRcFQ=="
    ),
    # ct-search 统一检索端点（ct-registry/coze）的共享公开凭据，2026-11-09 迁入。
    # 与 ct-registry/adapters/endpoint_token.py::EMBEDDED_SECRETS["coze_unified"]
    # 同源同值，但用本文件自己的 OBFUSCATION_KEY 重新编码，避免引入第二套解码逻辑。
    # 用途：ct-advisor 的 brief 速览通道（scripts/cloud_brief.py）直连 ct-search，
    # 使本地不再依赖 ct-registry 技能已安装。仍是公开共享凭据，非个人密钥。
    #
    # ── 🔴 给代码维护者：凭据轮换（非运行时用户提示）──────────────────
    # 本 blob 是 ct-search 共享公开凭据，**只**保存在本地技能 / 工作台；
    # Coze 云端包内不含任何凭据、不读取凭据、不发起需凭据的外部调用
    # （2026-11-09 用户拍板：调用点全部收敛到调用方）。
    # 轮换：① 真源 ct-registry/adapters/endpoint_token.py::coze_unified；
    #   ② 用 store_token() 重新生成 blob 后同步本文件的 ct_search_coze；
    #   ③ 跑 ct-advisor/scripts/test_cloud_brief.py 校验三方一致；
    #   ④ 更新本地技能 / 工作台发布物即可 —— **无需重新打包或重新发布
    #      Coze 云端包**。应急覆盖：本地 env CT_ADVISOR_BRIEF_TOKEN。
    # 完整 SOP 另见 ct-advisor/config/brief_contract.json 的
    # credential_governance 段。这是 XOR+base64 混淆（非加密）的公开凭据。
    "ct_search_coze": (
        "Bg1nCQYxChogG2cwOgAsHCELL14_XFlDPnorVT1ALBwsAxBaPGk1AjYxZwcvImwCf2lUE2ALUhx0"
        "Cw8OJSc6RmInBE88Hz4bK2keWmBKLgBMBg1nEQdFJBogG2cMCzI3WgwYCVs6A2tEBWpXCRYeEQg6"
        "BD0aO0QUBiM9ewQrDF0UeEF5MFgJUjZ_JSlFC0A5JHkNCAMoHgs7PGk4Y2ABHEkvCRBaAw4eWCpc"
        "I1QqA0oWZAI0Uk41eBt8IHAaLjBkUyocDkAhGE5WICkSRA41IB0_W0JLKkMFUjl5NFY5LSpbPm4p"
        "FR4yZAYtD2cMUmpfCWMPNkJhGF0eCjQEB3RRVkw_floIBERPAk8ALksAJE1FOyJPGSkoJFgHKBZV"
        "SDxbFncyXh59DmBTLCBKUysiOEMiNkYZIC4gVyI2Ix0_WFpaBwooCT1HDg0XPkYGEB41GiAjFAcG"
        "Pn8ZaR91DmBQNQ5OUF1GC0EbHk8PVgo_aQBRKEcvAmBnD04vGS0eLCA_Wjw7FR8tKysdZAFSSGBG"
        "UhtsE2MALQRDUgM5ORQ8E04KBFcKQAExK0k1dmZ6I1ILFT19MCIdDkM2E2M2FgArSSERX3cRAGdE"
        "AlNXE1kVUzxAGAcXCkM2DQAtQV8yVGAvVnQCAn0tMC1jIBAnAyIYM34zVz4KGR4MB3ckW3RXMAwu"
        "KzxaWREOLhIgAGsaV0sfYgsUVW83QnpsJn5UEEBVAyAbOCNXGWcuHTY2fycwC2wfW31FK341BicV"
        "TFZFWEAaAmMaHCpWZgozKBonZUNcVFIoDzFEED0dOSsHIRsyAwhXVTkaUHcSAmhKMm8OMjFpEw40"
        "OwJfNFcyBUopSisUF1k1A3gDXG1SWgEcGxRANkUiBBo5XxIfWR4rVHsbAEkEXGkaGwJ-Gw4gJwYY"
        "I2cADRYASSVbV10uQGZcFHAmVzxZJyohGkM1H1s3NygsFFsGAEMmRnhpUAA7CjhHLAgAKkI3BQ=="
    ),
    # "another_public_key": "<obfuscated blob>",
}

# 局部落盘绝对路径（兼容历史：允许用户/作者用私有 key 覆盖内嵌默认值）。
DEFAULT_TOKEN_PATH = os.path.expanduser(
    "~/.workbuddy/skills/ct-advisor/config/coze.dat"
)

# coze token 的环境变量名（与 config.json 的 refiner.token_env 默认一致）。
TOKEN_ENV = "CT_ADVISOR_COZE_TOKEN"


def _obf_encode(plain: str) -> str:
    """XOR 每个字节与滚动密钥，再做 URL-safe base64。"""
    data = plain.encode("utf-8")
    key = OBFUSCATION_KEY
    xored = bytes(b ^ key[i % len(key)] for i, b in enumerate(data))
    return base64.urlsafe_b64encode(xored).decode("ascii")


def _obf_decode(blob: str) -> str:
    """_obf_encode 的逆操作。"""
    data = base64.urlsafe_b64decode(blob.strip())
    key = OBFUSCATION_KEY
    plain = bytes(b ^ key[i % len(key)] for i, b in enumerate(data))
    return plain.decode("utf-8")


def default_token_path() -> str:
    return DEFAULT_TOKEN_PATH


def store_token(plain: str, token_path: str = None) -> str:
    """混淆并落盘 token（可选覆盖文件）；返回实际写入路径。

    - 父目录不存在则创建（exist_ok）。
    - 写入后尝试 chmod 0600（失败忽略，不打断技能）。
    - 说明：发布包不再依赖此文件；它仅作为本地覆盖手段保留。
    """
    path = token_path or DEFAULT_TOKEN_PATH
    os.makedirs(os.path.dirname(path), exist_ok=True)
    blob = _obf_encode(plain.strip())
    with open(path, "w", encoding="utf-8") as f:
        f.write(blob)
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass
    return path


def get_secret(name: str, cli_value: str = None, env_name: str = None,
               secret_path: str = None) -> str:
    """按名字取公开凭据：CLI > env > 局部文件 > 内嵌 blob。皆无回退空串。

    - 局部文件损坏 / 非法 base64 / 编码错误 / 权限不足 → 跳过该来源，继续尝试内嵌 blob。
    - 内嵌 blob 解析失败 → 回退空串。
    - 绝不向上抛：契约是「解析不到就返回空串」。
    """
    if cli_value:
        return cli_value
    if env_name:
        env = os.environ.get(env_name)
        if env:
            return env
    if secret_path and os.path.exists(secret_path):
        try:
            with open(secret_path, encoding="utf-8") as f:
                return _obf_decode(f.read())
        except Exception:
            # 文件来源损坏 → 不回退空串，继续尝试内嵌 blob（更健壮）。
            pass
    blob = EMBEDDED_SECRETS.get(name)
    if blob:
        try:
            return _obf_decode(blob)
        except Exception:
            return ""
    return ""


def get_token(cli_token: str = None, token_path: str = None,
              token_env: str = TOKEN_ENV) -> str:
    """coze 便捷封装：等价于 get_secret("ct_advisor_coze", ...)。

    参数与旧版一致（保持 refiner.py / refine_answer.py 的调用不变）。
    """
    return get_secret("ct_advisor_coze", cli_token, token_env,
                      token_path or DEFAULT_TOKEN_PATH)


def get_bugreport_token(cli_token: str = None, token_path: str = None,
                        token_env: str = "CT_BUGREPORT_COZE_TOKEN") -> str:
    """错误报告端点便捷封装：等价于 get_secret("ct_bugreport_coze", ...)。

    由 adapters/bug_report.py 调用（替代原 config/coze_token.py::COZE_TOKEN）。
    与 ct_advisor_coze 共用同一混淆密钥与读取优先级（CLI > env > 局部文件 > 内嵌 blob）。
    """
    return get_secret("ct_bugreport_coze", cli_token, token_env,
                      token_path or DEFAULT_TOKEN_PATH)


def get_search_token(cli_token: str = None) -> str:
    """ct-search 统一检索端点（ct-registry/coze）的共享公开凭据。

    由 ``scripts/cloud_brief.py`` 调用，用于 ct-advisor 的 brief 速览通道。
    读取优先级：CLI > env ``CT_ADVISOR_BRIEF_TOKEN`` > 内嵌 blob。
    契约：解析不到一律返回空串（调用方据此回落本地 need_tool 执行卡），绝不抛异常。
    """
    return get_secret("ct_search_coze", cli_token, "CT_ADVISOR_BRIEF_TOKEN",
                      DEFAULT_TOKEN_PATH)
