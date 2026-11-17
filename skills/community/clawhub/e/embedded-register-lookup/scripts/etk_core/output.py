"""输出封装：证据标签、来源信息、统一的 JSON 信封。"""

from __future__ import annotations

import os

LABEL_VERIFIED = "已核验"
LABEL_MANUAL = "需查手册"
LABEL_MEASURE = "需实测"
LABEL_UNDETERMINED = "未判定"
LABELS = (LABEL_VERIFIED, LABEL_MANUAL, LABEL_MEASURE, LABEL_UNDETERMINED)

# SVD modifiedWriteValues / readAction 的中文提示（未知取值原样显示）
WRITE_SEMANTICS = {
    "oneToClear": "写 1 清零",
    "oneToSet": "写 1 置位",
    "oneToToggle": "写 1 翻转",
    "zeroToClear": "写 0 清零",
    "zeroToSet": "写 0 置位",
    "zeroToToggle": "写 0 翻转",
    "clear": "写 0",
    "set": "写 1",
    "modify": "写时修改",
}
READ_SEMANTICS = {
    "clear": "读后清零",
    "set": "读后置位",
    "modify": "读时修改",
    "modifyExternal": "读后由硬件修改",
}


def write_semantics(raw):
    return WRITE_SEMANTICS.get(raw, raw or "")


def read_semantics(raw):
    return READ_SEMANTICS.get(raw, raw or "")


def source_meta(device):
    return {
        "file": os.path.basename(device.path),
        "path": device.path,
        "device": device.name,
        "version": device.version,
    }


def envelope(tool, version, results=None, warnings=None, errors=None):
    errs = list(errors or [])
    return {
        "ok": not errs,
        "tool": tool,
        "version": version,
        "results": list(results or []),
        "warnings": list(warnings or []),
        "errors": errs,
    }
