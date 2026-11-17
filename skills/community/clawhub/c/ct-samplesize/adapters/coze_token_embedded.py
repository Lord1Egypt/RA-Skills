# NOTE: This file contains an obfuscated PUBLIC shared credential (XOR+base64). It is NOT a secret. See user authorization 2026-08-18.
"""ct-samplesize 公共凭据库（XOR+base64 混淆内嵌，镜像 ct-advisor 的 OBFUSCATION 模式）。

背景（2026-08-18）：用户授权将 coze 长期 token 随技能**公开发布**，避免每次经环境变量
注入，并规避「推送 config.json 泄露 JWT」的风险（token 不在 config.json 明文、也不在
memory/笔记）。

重要：
- 这是 OBFUSCATION，NOT real encryption。混淆密钥随脚本发布，仅防目录浏览时的明文暴露；
  持脚本者即可还原。但本库只放**公开的、随技能发布**的共用凭据（访问公共 ct-samplesize
  精算端点的 token），**必须随技能原样保留**，请勿用私有凭据覆盖。
- **切勿把私有凭据内嵌进来**：私有凭据请走 CLI(--token) / env(CTSS_COZE_TOKEN)，不要写进
  EMBEDDED_SECRETS。
- 历史实现曾把 coze token 落盘到 `config/coze.dat`；但 SkillHub 为窄白名单打包（仅
  .svg/.py/.md/.json/.yaml/.txt/.toml/.csv），`.dat` 不在白名单，发布时被静默剥离 →
  已安装技能读不到文件、连不上 coze。故改为**统一内嵌**（见 EMBEDDED_SECRETS），不再依赖
  外部 .dat 文件。本地仍可用 store_token() 写覆盖文件（可选，优先级介于 env 与内嵌之间）。

读取优先级（通用 get_secret / get_token）：CLI > env > 局部落盘文件 > 内嵌 blob。皆无回退空串。
端点读取优先级（get_endpoint）：env(CTSS_COZE_ENDPOINT / COZE_ENDPOINT) > 内嵌常量。
"""
from __future__ import annotations

import base64
import os

# 单份混淆密钥（所有公开凭据共用；都是公开凭据，无横向泄露风险）。
# 注：必须与生成 blob 时使用的密钥一致，否则无法还原。
OBFUSCATION_KEY = b"ct-samplesize-coze-obf-v1-7f2a"

# 内嵌公共凭据库：name -> XOR+base64 混淆 blob。
# 新增 key：store_token(plain) 生成 blob 后抄此一行（不要内嵌私有凭据）。
EMBEDDED_SECRETS = {
    "ct_samplesize_coze": (
        "Bg1nGwMqEwUqGiMpMFcqXjQMZBwrC1kGa25-UHsLNkViNysHPgE_GSUuPB4uAjcRYysOD2AlAER5MXgILyNrHy8HNgcoNwERK1c2Xzc2Z1ZMA1Q8QU4EK1suCj5CFyk_Bw8fHB82V2sUDilQRw1RFkE6XGNCL1sWCi11JQokGhwHOgUvVnkJAykGaS0hMB4SQXgHIEUzCAx-PVEjQiExKVsoVUUINkk3fw4JPH0_XR1EL183VxduOlciNCUdPi0zV2MJCEkrRwxXKX4BWExgIAIoCRtVPRsKQyEhNhE1IXwZIzkvVws1L0Q5WGdNBXUNDi5AJlchCVUNEC4REHRRVkw_floIBERPAk8ELEADJE1FKSdUADYiJRweIkFTCilcXTUmCR44W3QCKWY4UDtpPhYiJDkSPC0ZHWA3LgAsRBgLBR48W2RdCVsANEFEEVI7BTYjSgEePX8MN0gjRzZQMFcVABQHBAAVDxZBShE3NANWPQMZVGA3OkkraSZTKWkjRmBjMwMsJzEZOg9dXgMrIDhMERhOXBsPd1gbABUgXBkaUgszKVlIRCcmQAsCRggINmwaDDYcbgsKJ3IYXX1bP2AYOkBKGCBUQDUCLBgbV2QzJjEsZAw6N2YjSF9wE34tJC1vPTADHTgtLCIZSGMUKyIhHQAmDFUOCBtREkEQPDZDADkaIAcPNjsvUHlWBCpVVQkEV0kHSFhtUgEmEiJCQiNUQFksCzA5MBowCR0xXVkAPHI1fXdSE0smJBgVOSMdBxQTBhwJEngEABQkWAwRFhkhBU5VFAAjJT9yJyYhAUEiPBkCCh88Ix0wZD4GBVcQeF10AlUUISB8SyAvGz0DIERJVnwpBjMIa0IAVR85CR5-DXVTFxxrISNYIwdVGg09DG4sXUMASC42DlgbWXddVEpZLzZoJAZcCSUgBChNPR8zGg8HGDYYNF8HBUZGM1AgET5BIQkPJyI_Nh88IkoCIiwhWg=="
    ),
    # "another_public_key": "<obfuscated blob>",
}

# 已部署的公共端点（随技能发布）。用户授权 2026-08-18。
# 备用域名（同一部署的不同 CNAME）：https://xj34hpzqgq.coze.site/run
ENDPOINT = "https://ct-samplesize.coze.site/run"

# 局部落盘绝对路径（兼容历史：允许用户/作者用私有 key 覆盖内嵌默认值）。
DEFAULT_TOKEN_PATH = os.path.expanduser(
    "~/.workbuddy/skills/ct-samplesize/config/coze.dat"
)

# coze token 的环境变量名。
TOKEN_ENV = "CTSS_COZE_TOKEN"


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
    """coze 便捷封装：等价于 get_secret("ct_samplesize_coze", ...)。"""
    return get_secret("ct_samplesize_coze", cli_token, token_env,
                      token_path or DEFAULT_TOKEN_PATH)


def get_endpoint(cli_endpoint: str = None, endpoint_env: str = "CTSS_COZE_ENDPOINT") -> str:
    """取公共端点：CLI(env) > 内嵌常量。二者皆无回退空串。

    兼容旧变量名 COZE_ENDPOINT。
    """
    if cli_endpoint:
        return cli_endpoint
    env = os.environ.get(endpoint_env) or os.environ.get("COZE_ENDPOINT")
    if env:
        return env
    return ENDPOINT
