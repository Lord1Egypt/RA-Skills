# ct-registry 端点凭据模块（endpoint_token.py，位于 adapters/）—— 随技能包发布（.py 后缀，不会被发布平台静默剥离）。
# 命名与位置对齐已发布技能 ct-base 的 adapters/coze/src/endpoint_token.py / ct-advisor 的 adapters/coze_token_embedded.py。
#
# 为什么必须放 .py：
#   SkillHub / ClawHub 等平台对打包文件有后缀白名单，.dat / .cfg / .key 等非白名单
#   后缀会被服务端**静默剥离**（不像 .R/.png 那样报 400）。若公开凭据只以
#   config/*.dat 形式存在，发布后安装环境读不到文件、连不上端点（ct-base §5.243）。
#   统一用 .py 存放，任何平台都不会丢。
#
# coze key 是什么：
#   访问统一外部端点 ct-search.coze.site/run 的**公用负载身份 token**（Bearer）。
#   它是公开共用凭据（绑定端点、无个人归属），随包发布给所有用户，不存在
#   "真实私密凭据泄露"问题。按 ct-base §5，明文凭据禁止落盘，故以 XOR+base64 混淆
#   blob 内嵌（非明文），仅防目录浏览 / 扫描命中明文；发布等同公开该公用 token。
#
# 解析优先级（全库统一，ct-base §5.236）：
#   CLI(--token) > env(CT_REGISTRY_COZE_TOKEN，遗留别名 ICTRP_WORKFLOW_TOKEN)
#   > 内嵌混淆 blob（本文件）
# 历史遗留：本机若存在 config/ictrp.dat（旧机制残留），仅作为**最后回退读取**，绝不写入。
#
# 红线：绝不把 token 明文输出到日志 / 报错 / 回复 / 任何面向用户的文本（ct-base §5）。

import base64
import os

# 轻混淆密钥（XOR key，非保密；与旧 extsvc_client 保持一致以兼容旧 blob）。
OBFUSCATION_KEY = b"ct-registry-extsvc-obf-v1-9c4d2a"


def _obf_encode(plain: str) -> str:
    data = plain.encode("utf-8")
    key = OBFUSCATION_KEY
    xored = bytes(b ^ key[i % len(key)] for i, b in enumerate(data))
    return base64.urlsafe_b64encode(xored).decode("ascii")


def _obf_decode(blob: str) -> str:
    data = base64.urlsafe_b64decode(blob.strip())
    key = OBFUSCATION_KEY
    plain = bytes(b ^ key[i % len(key)] for i, b in enumerate(data))
    return plain.decode("utf-8")


# 内嵌公共凭据混淆 blob（XOR+base64，非明文）。
# 统一端点所有 source（who / chinadrugtrials / isrctn / drks / chictr）共用同一份 token。
# 规范名按"统一端点"语义命名，不再绑定 ictrp.dat 文件方式。
EMBEDDED_SECRETS = {
    # bug-report 统一端点公共凭据（§5 公用凭据；并入后 bug_report.py 不再自持 XOR blob）。
    # 已用本文件统一 OBFUSCATION_KEY 重新编码，消除「两套 XOR key + 两套 blob」(架构评审#3)。
    "ct_bugreport_coze": "Bg1nGgcgCho7GzN-MAI9QjgKZBwrC1kGa25wVX0Ja1ItIG8eKAowCzglKFQrSjkHOCRkFy8lHUN_V2sJeDN_Uy0wTgg8MCMfLQgSHj8RPkpYBlQlEgUeO1hiUClbAHozFBdXHRMrWzUDEyoYDxpHAxovQCEXL0QBWHRhNV8tWBEBPUY4MSoTIT8WPkUEKR8DGAZrHwswezBGfnwqADcCESYXHDA1PRMlDStJFDMxGEMFKkA5VgVuPwdifSpMKXYoUTpHFVYpAxBBPSpaDBkjNUYqRwAaKFcRAmBTAAYrZihSOG44HwM-Oh09EGcfGzMfGzlAOlQqVE9ZTn4IQT0AWFUufkcPBQBKRxBKZxcaM0oeOWtWEjxqIERJfg8EAWFYEy5pHVYpAxBGPxNKVzYOMkYuRyJXKHk3BGNtJk4tWxYKFx44Dy4DHB0TLhgMGkclAzlrVgoCdSRedQslXj0ANxkXHEtVBVsHGBAVFBUiMBxFLUcMUCtHHQBibTIFKWYsVzppERIoPSoNOxcdSx5BFTAZaCIGVEkYVkNIJQMRfiokQFkgLRAdASIDS2EkLiUBHFJFLFERWjB_W3IbYSlGAyAiGUQEEjs_LhgtTB0sKzIfEAAXAQRfPQRfDixTEno1KC5JCjwoXisOJT5KKxA9HEBTawNRUmoHU2VBFWY3eRMWAhREXT88XjkaTV4gSQ0qP1dqCRoJSiRIHU83VwJTNxE3ZD82Nyg2HQMjeg8TQjApJR0OJCsZREkUDTZxNmIvKidvPy8NG0oQQhFhPxEYFDETRwkDJB8id3l4DgcjURYxAWk6CzAOIAQ3IUQ9LS4ANzpeOFAWQhRFGF0oXlxxVDowdSUrUiQYER4hHCoPPiYRMGMcMgd1E2BHezlwEGolNEcaIi4LHh8mRztaKQEVHzMBTgRTDmEadml8F3s-YlQ2JWYmKCYASk0mSXUPDxonAlJHQiEiYSZ9WF06TTAKFjRHSg==",
    "coze_unified": "Bg1nGgcgCho7GzN-MAI9QjgKZBwrC1kGa25wVX0Jfxk5Hk5HKyM_HjgmM0UoPDUHOCdKGDsPHB5oR1IbeDBnVSwwRkc8VTgKOTYRRigBPkpYBlQlEgUeO1hiUClbAHozFBdXHRMrWzUDEyoYDxpHAxovQCEXL0QBWHRhNV8tWBEBPUE4MQYCQjYgPWBWGkclIDdDCBsrHhJod30tZikAGRM5RxYSBQMbRStKfBwxGEMFKkA5VgVuPwdifSpMKXYoUTpHFVYpAxBBPSpaDBkjNUYqRwAaKFcRAGBtNgYrdjhXOG44HwM-Oh09EGcfGzMfGzlAOlQqVE9ZTn4IQT0AWFUufkcPBQBKRxBKZxcaM0oeOWtWEjxqIERJfg8EAWFYEy5pHVYpAypFPS1KVzcgIkYuaQQYKXkzS2BtJgQtWxYKFx44Dy4DHB0TLhgMGkclAzlrVgoCdSRedQslXj0ANxkXHEtVBVsHGBAVFBUiMBxFLUc2USt5HUZgQzoHKXYoUDt5FVcpLSIMOxcdSzVEEEA8WjUAKF0YAkp2M1M3UwIKHwAdCAk6PhAxPmYsPx8aACp9PiQNSkZoTHc2TR58BS0HFCgCViMEEhhMXUhARitAElkXGgh4FEtlVVNkVn84BC0cFCEoOio6Mw18DykDMiUzFSsNUlwYUHdrCW0AZlQvPGUFXRIRNBU9C2scQEUJOQdbXCAnXiFub35VR1BKAycZfCJdDCM-Bj4qfy0qGTIfCX0ZLSF6E2IVFFEHVQEUEzpUATVUIhYlPE58MRYbQx0pQSoLF3QdYXVRMAI1XhNRDHsKUz0NQDELL3sJKTE3BAlvPRNWawxgRwkvUyBEEBc3HydVXz1DTQdIVxVOK0U7FRo1Ug5XAkBkCzVZVVZWWyRVChM0ExkiPAxaNDIXERoGSSVbV10uQGZWE30gBikXMmMlFlczHgImIX8sQUAXEA19GDc8GU9oRHUJeQhEIlIsWg==",
    # 历史别名，兼容旧调用 get_secret("ictrp" / "who" / ...)
    "ictrp": "Bg1nGgcgCho7GzN-MAI9QjgKZBwrC1kGa25wVX0Jfxk5Hk5HKyM_HjgmM0UoPDUHOCdKGDsPHB5oR1IbeDBnVSwwRkc8VTgKOTYRRigBPkpYBlQlEgUeO1hiUClbAHozFBdXHRMrWzUDEyoYDxpHAxovQCEXL0QBWHRhNV8tWBEBPUE4MQYCQjYgPWBWGkclIDdDCBsrHhJod30tZikAGRM5RxYSBQMbRStKfBwxGEMFKkA5VgVuPwdifSpMKXYoUTpHFVYpAxBBPSpaDBkjNUYqRwAaKFcRAGBtNgYrdjhXOG44HwM-Oh09EGcfGzMfGzlAOlQqVE9ZTn4IQT0AWFUufkcPBQBKRxBKZxcaM0oeOWtWEjxqIERJfg8EAWFYEy5pHVYpAypFPS1KVzcgIkYuaQQYKXkzS2BtJgQtWxYKFx44Dy4DHB0TLhgMGkclAzlrVgoCdSRedQslXj0ANxkXHEtVBVsHGBAVFBUiMBxFLUc2USt5HUZgQzoHKXYoUDt5FVcpLSIMOxcdSzVEEEA8WjUAKF0YAkp2M1M3UwIKHwAdCAk6PhAxPmYsPx8aACp9PiQNSkZoTHc2TR58BS0HFCgCViMEEhhMXUhARitAElkXGgh4FEtlVVNkVn84BC0cFCEoOio6Mw18DykDMiUzFSsNUlwYUHdrCW0AZlQvPGUFXRIRNBU9C2scQEUJOQdbXCAnXiFub35VR1BKAycZfCJdDCM-Bj4qfy0qGTIfCX0ZLSF6E2IVFFEHVQEUEzpUATVUIhYlPE58MRYbQx0pQSoLF3QdYXVRMAI1XhNRDHsKUz0NQDELL3sJKTE3BAlvPRNWawxgRwkvUyBEEBc3HydVXz1DTQdIVxVOK0U7FRo1Ug5XAkBkCzVZVVZWWyRVChM0ExkiPAxaNDIXERoGSSVbV10uQGZWE30gBikXMmMlFlczHgImIX8sQUAXEA19GDc8GU9oRHUJeQhEIlIsWg==",
}

# 规范环境变量名（ct-base §5.236）
DEFAULT_TOKEN_ENV = "CT_REGISTRY_COZE_TOKEN"

# bug-report 统一端点（§20.3.5 全库共用）；原硬编码于 bug_report.py，现已集中至此（架构评审#3）。
BUG_REPORT_ENDPOINT = "https://ct-bugreport.coze.site/run"
# 统一检索端点（Tier-1/Tier-2 共用）；原硬编码于 search_ictrp.py，现已集中至此（架构评审#2/#4 端点单一真源）。
CT_SEARCH_ENDPOINT = "https://ct-search.coze.site/run"
# 遗留环境变量别名（兼容旧调用方）
LEGACY_TOKEN_ENVS = ("ICTRP_WORKFLOW_TOKEN",)

# 统一端点所有 source 共用同一份 token（旧 _UNIFIED_SOURCES 语义保留）
_UNIFIED_SOURCES = {"ictrp", "who", "chictr", "isrctn", "drks", "chinadrugtrials", "coze_unified"}

# 历史遗留 .dat 路径（仅回退读取，绝不写入；SkillHub 已静默剥离）
LEGACY_DAT_PATH = os.path.expanduser(
    "~/.workbuddy/skills/ct-registry/config/ictrp.dat")


def _resolve_secret_key(name: str) -> str:
    """统一端点所有 source 都映射到同一个内嵌 blob 键。"""
    n = (name or "").lower()
    if n in _UNIFIED_SOURCES:
        return "coze_unified"
    return n


def get_secret(name: str, cli_token: str = None, token_env: str = None, fallback: str = "") -> str:
    """按名字取公共凭据。解析优先级：CLI > env > 内嵌混淆 blob > 遗留 .dat 回退。

    绝不在此函数内打印 token 明文（ct-base §5）。
    """
    if cli_token:
        return cli_token
    # 环境变量：规范名优先，再试遗留别名与 <SRC>_WORKFLOW_TOKEN
    src_key = _resolve_secret_key(name)
    env_candidates = [token_env, DEFAULT_TOKEN_ENV,
                      f"{src_key.upper()}_WORKFLOW_TOKEN"] + list(LEGACY_TOKEN_ENVS)
    seen = set()
    for e in env_candidates:
        if not e or e in seen:
            continue
        seen.add(e)
        v = os.environ.get(e)
        if v:
            return v
    # 内嵌混淆 blob
    blob = EMBEDDED_SECRETS.get(src_key)
    if blob:
        return _obf_decode(blob)
    # 遗留兼容：本机旧 ictrp.dat（SkillHub 已剥离，仅本地残留时回退）
    if os.path.exists(LEGACY_DAT_PATH):
        try:
            with open(LEGACY_DAT_PATH, encoding="utf-8") as f:
                return _obf_decode(f.read().strip())
        except Exception:
            pass
    return fallback


def get_token(cli_token: str = None, token_env: str = None) -> str:
    """统一端点（coze）token。等价于 get_secret('coze_unified', ...)。"""
    return get_secret("coze_unified", cli_token, token_env)


def get_bugreport_token(cli_token: str = None, token_env: str = None) -> str:
    """bug-report 统一端点 token。等价于 get_secret('ct_bugreport_coze', ...)。"""
    return get_secret("ct_bugreport_coze", cli_token, token_env)


