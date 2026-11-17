"""
pii_redactor.py
V7 端侧 4 级 PII 自动脱敏工具（仅依赖标准库 re）

4 级 PII：
  L1 姓名    - 2~4 个汉字，常用姓氏开头
  L2 身份证  - 18 位 / 15 位
  L3 手机    - 11 位中国手机号
  L4 家庭住址 - 包含"省/市/区/县/路/街/号/室"等关键字

参考：references/zero-upload-privacy.md
"""


# --- UTF-8 stdout/stderr (Windows 中文输出防乱码) -----------------------------
def _configure_stream_encoding(stream):
    reconfigure = getattr(stream, "reconfigure", None)
    if callable(reconfigure):
        reconfigure(encoding="utf-8")

import sys as _sys
_configure_stream_encoding(_sys.stdout)
_configure_stream_encoding(_sys.stderr)
del _sys
# ----------------------------------------------------------------------------

from log_util import get_logger

log = get_logger("pii")

import hashlib
import random
import re
import time
import uuid


# ---------------------------------------------------------------------------
# 姓氏表（用于 L1 姓名检测，避免任意 2~4 字汉字组合的误报）
# ---------------------------------------------------------------------------
_COMMON_SURNAMES = (
    "赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜"
    "戚谢邹喻柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳酆鲍史唐"
    "费廉岑薛雷贺倪汤滕殷罗毕郝邬安常乐于时傅皮卞齐康伍余元卜顾孟平黄"
    "和穆萧尹姚邵湛汪祁毛禹狄米贝明臧计伏成戴谈宋茅庞熊纪舒屈项祝董梁"
    "杜阮蓝闵席季麻强贾路娄危江童颜郭梅盛林刁钟徐邱骆高夏蔡田樊胡凌霍"
    "虞万支柯昝管卢莫经房裘缪干解应宗丁宣贲邓郁单杭洪包诸左石崔吉钮龚"
    "程嵇邢滑裴陆荣翁"
)

# 姓氏字符类
_SURNAME_CLASS = "[" + _COMMON_SURNAMES + "]"

# 复姓表（用于 L1 姓名检测，支持欧阳、司马等常见复姓）
_COMPOUND_SURNAMES = (
    "欧阳", "司马", "诸葛", "上官", "司徒", "司空", "尉迟",
    "慕容", "申屠", "东方", "独孤", "皇甫", "令狐", "宇文",
    "长孙", "万俟", "夏侯", "闻人", "端木", "南宫",
)

# 复姓正则：复姓 + 1~2 个汉字
_COMPOUND_SURNAME_RE = (
    "(?:" + "|".join(_COMPOUND_SURNAMES) + r")[\u4e00-\u9fa5]{1,2}"
)


# ---------------------------------------------------------------------------
# 4 级 PII 正则
# ---------------------------------------------------------------------------
# L1 姓名：复姓 + 1~2 字名，或单姓 + 1~3 字名
# 复姓优先匹配（避免"欧阳"被拆成"欧"+"阳..."）
L1_NAME_RE = re.compile(
    _COMPOUND_SURNAME_RE + "|" + _SURNAME_CLASS + r"[\u4e00-\u9fa5]{1,3}"
)

# L2 身份证：18 位（含最后一位 X/x）或 15 位
# 使用零宽断言替代 \b，解决中文上下文中 \b 失效问题
L2_ID_RE = re.compile(r"(?<!\d)\d{17}[\dXx](?!\d)|(?<!\d)\d{15}(?!\d)")

# L3 手机：11 位中国手机号
# 使用零宽断言替代 \b，解决中文上下文中 \b 失效问题
L3_PHONE_RE = re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")

# L4 家庭住址：以"省/市/区/县/路/街/号/室"等关键字结尾
_ADDRESS_KEYWORDS = (
    r"(?:省|自治区|市|区|县|旗|镇|乡|路|街|大道|巷|弄|号|室|楼|栋|单元|院|村|屯|里)"
)
L4_ADDRESS_RE = re.compile(
    r"[\u4e00-\u9fa5A-Za-z0-9]{2,20}(?:"
    + _ADDRESS_KEYWORDS
    + r"(?:[\u4e00-\u9fa5A-Za-z0-9]{0,15}(?:"
    + _ADDRESS_KEYWORDS
    + r"))?)"
)


# ---------------------------------------------------------------------------
# 单字段脱敏策略
# ---------------------------------------------------------------------------
def _mask_name(name: str) -> str:
    """张三 -> 张**  ；欧阳娜娜 -> 欧**  （保留姓，名部分用 *）"""
    if not name:
        return name
    return name[0] + "*" * (len(name) - 1)


def _mask_id_card(id_card: str) -> str:
    """18 位身份证 -> 前 6 位 + 8 个 * + 后 4 位
    15 位身份证 -> 前 6 位 + 5 个 * + 后 4 位
    """
    if len(id_card) == 18:
        return id_card[:6] + "*" * 8 + id_card[14:]
    if len(id_card) == 15:
        return id_card[:6] + "*" * 5 + id_card[11:]
    return id_card


def _mask_phone(phone: str) -> str:
    """13812345678 -> 138****5678"""
    if len(phone) != 11:
        return phone
    return phone[:3] + "*" * 4 + phone[7:]


def _mask_address(address: str) -> str:
    """北京市朝阳区XX路1号 -> 北京市朝阳区XX路**号
    规则：把"号/室/楼/栋"前紧邻的数字替换为 **，保留量词关键字。
    """
    # 先处理"数字 + 关键字"组合，例如 "1号" / "302室" / "A栋"
    masked = re.sub(
        r"(\d+)(号|室|楼|栋)",
        r"**\2",
        address,
    )
    # 再把孤立的纯数字门牌也遮蔽
    masked = re.sub(r"\d+", "**", masked)
    return masked


# ---------------------------------------------------------------------------
# PII 检测
# ---------------------------------------------------------------------------
def detect_pii(text: str) -> dict[str, list[str]]:
    """返回 4 级 PII 命中列表：
        {
            "L1_name":   [...],
            "L2_id":     [...],
            "L3_phone":  [...],
            "L4_address":[...],
        }
    """
    if not isinstance(text, str):
        text = str(text)
    return {
        "L1_name": L1_NAME_RE.findall(text),
        "L2_id": L2_ID_RE.findall(text),
        "L3_phone": L3_PHONE_RE.findall(text),
        "L4_address": L4_ADDRESS_RE.findall(text),
    }


# ---------------------------------------------------------------------------
# 文本级脱敏
# ---------------------------------------------------------------------------
def _redact_text(text: str) -> tuple[str, bool]:
    """内部：替换 4 级 PII，返回 (脱敏后文本, pii_detected)。"""
    if not isinstance(text, str):
        text = str(text)
        return text, False

    detected_any = False

    # L1 姓名
    if L1_NAME_RE.search(text):
        detected_any = True
        text = L1_NAME_RE.sub(lambda m: _mask_name(m.group(0)), text)

    # L2 身份证
    if L2_ID_RE.search(text):
        detected_any = True
        text = L2_ID_RE.sub(lambda m: _mask_id_card(m.group(0)), text)

    # L3 手机
    if L3_PHONE_RE.search(text):
        detected_any = True
        text = L3_PHONE_RE.sub(lambda m: _mask_phone(m.group(0)), text)

    # L4 住址
    if L4_ADDRESS_RE.search(text):
        detected_any = True
        text = L4_ADDRESS_RE.sub(lambda m: _mask_address(m.group(0)), text)

    return text, detected_any


def redact(text: str) -> tuple[str, bool]:
    """单段文本脱敏。返回 (脱敏后文本, pii_detected)。"""
    return _redact_text(text)


# ---------------------------------------------------------------------------
# 字典级递归脱敏
# ---------------------------------------------------------------------------
def _recursive_redact(node, flag_holder: list) -> tuple[object, bool]:
    """递归脱敏内部实现。

    返回 (新节点, pii_detected)
    flag_holder: 长度 1 列表，用于跨层级累加命中标记
    """
    if isinstance(node, str):
        new_text, hit = _redact_text(node)
        if hit:
            flag_holder[0] = True
        return new_text, hit
    if isinstance(node, dict):
        new_dict = {}
        hit_any = False
        for k, v in node.items():
            new_v, hit = _recursive_redact(v, flag_holder)
            new_dict[k] = new_v
            hit_any = hit_any or hit
        return new_dict, hit_any
    if isinstance(node, list):
        new_list = []
        hit_any = False
        for item in node:
            new_item, hit = _recursive_redact(item, flag_holder)
            new_list.append(new_item)
            hit_any = hit_any or hit
        return new_list, hit_any
    if isinstance(node, tuple):
        new_tuple = tuple(
            _recursive_redact(item, flag_holder)[0] for item in node
        )
        return new_tuple, False
    # 其他基础类型（int / float / bool / None）原样返回
    return node, False


def redact_abstract_data(abstract_data: dict) -> tuple[dict, bool]:
    """对整个 dict 递归脱敏。
    - 字符串值：调用 redact() 脱敏
    - list / tuple 元素：逐个递归
    - dict 值：递归处理
    返回 (脱敏后 dict 副本, pii_detected)
    """
    if abstract_data is None:
        return {}, False
    flag_holder = [False]
    new_data, _ = _recursive_redact(abstract_data, flag_holder)
    return new_data, flag_holder[0]


# ---------------------------------------------------------------------------
# 5% 抽样审计（V7 §12.1 漏检响应协议）
# ---------------------------------------------------------------------------
def _collect_leaves(node, path: str, out: list) -> None:
    """递归收集 dict 中所有叶子节点，path 是字段路径。"""
    if isinstance(node, dict):
        if not node:
            out.append((path or "<root>", node))
            return
        for k, v in node.items():
            new_path = f"{path}.{k}" if path else str(k)
            _collect_leaves(v, new_path, out)
    elif isinstance(node, list):
        if not node:
            out.append((path or "<root>", node))
            return
        for i, item in enumerate(node):
            new_path = f"{path}[{i}]" if path else f"[{i}]"
            _collect_leaves(item, new_path, out)
    else:
        out.append((path or "<root>", node))


def sample_audit(abstract_data: dict, rate: float = 0.05) -> dict:
    """V7 §12.1 漏检响应协议：5% 随机抽样审计。

    返回审计报告：
        {
            "audit_id":        "audit-uuid-xxx",
            "sample_size":     int,
            "sampled_keys":    [...],
            "pii_detected":    bool,
            "pii_hits":        { "L1_name": [...], ... },
            "audit_method":    "regex_strict_sampling",
            "audit_timestamp": "2026-08-16T...",
            "compliance":      "pass" | "fail",
        }
    """
    if not isinstance(abstract_data, dict):
        abstract_data = {"_value": abstract_data}

    # 收集所有叶子节点
    leaves: list[tuple[str, object]] = []
    _collect_leaves(abstract_data, path="", out=leaves)

    total = len(leaves)
    sample_n = max(1, int(round(total * rate))) if total > 0 else 0

    # 用 abstract_data 的字符串表示作为种子，保证同一数据抽样稳定
    seed_src = repr(sorted(abstract_data.items())).encode("utf-8")
    rng = random.Random(hashlib.md5(seed_src).hexdigest())

    if total > 0:
        sample_idx = sorted(rng.sample(range(total), min(sample_n, total)))
    else:
        sample_idx = []

    sampled_keys = [leaves[i][0] for i in sample_idx]
    hits_all: dict[str, list[str]] = {
        "L1_name": [],
        "L2_id": [],
        "L3_phone": [],
        "L4_address": [],
    }
    for i in sample_idx:
        _path, value = leaves[i]
        if not isinstance(value, str):
            continue
        d = detect_pii(value)
        for k, v in d.items():
            hits_all[k].extend(v)

    pii_detected = any(len(v) > 0 for v in hits_all.values())

    return {
        "audit_id": "audit-" + uuid.uuid4().hex[:12],
        "sample_size": len(sample_idx),
        "total_size": total,
        "sample_rate": rate,
        "sampled_keys": sampled_keys,
        "pii_detected": pii_detected,
        "pii_hits": hits_all,
        "audit_method": "regex_strict_sampling",
        "audit_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "compliance": "fail" if pii_detected else "pass",
    }


if __name__ == "__main__":
    log = get_logger("pii")
    # 测试样例
    tests = [
        "学生张三的身份证是110101199001011234，手机13812345678",
        "地址是北京市朝阳区XX路1号",
        "本节课讲机器学习基础",
    ]
    for t in tests:
        masked, detected = redact(t)
        log.info(f"原: {t}")
        log.info(f"改: {masked}")
        log.info(f"PII: {detected}")
        print()
