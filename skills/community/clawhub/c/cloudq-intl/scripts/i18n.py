#!/usr/bin/env python3
"""CloudQ skill 轻量 i18n 模块（中文即键模型）

设计要点：
- 零外部依赖（stdlib only），兼容 Python 3.7+
- 中文文案即字典键：脚本内 T("中文模板") 内联调用
  - zh 模式：T() 返回模板本身 → 中文版行为零变化
  - en 模式：查 locales/en.py 的 MESSAGES；缺失回退中文（降级规则）
- 语言解析优先级：set_lang() 显式 > --lang CLI 参数 > CLOUDQ_LANG 环境变量 > DEFAULT_LANG
- 国际站独立树固定值：DEFAULT_LANG = "en"（默认英文）

T() 硬规则（check_i18n_sync.py AST 扫描强制）：
- 首参必须是字符串字面量（保证静态可抽取）
- 脚本内含中文的输出字符串必须 T() 包装
"""

import os
import sys

# 国际站固定值（独立源码树，非构建注入；同步自 cloudq 时禁止改回）
DEFAULT_LANG = "en"   # 国际站默认英文输出
EDITION = "intl"      # 国际站标识（构建断言 / SYNC_SPEC 差异基线锚点）
_VALID_LANGS = ("zh", "en")

_lang_cache = None
_lang_explicit = None


def _normalize_lang(value):
    """归一化语言标识：小写、去空白；空值/非法值回退 zh"""
    if not value:
        return DEFAULT_LANG
    normalized = str(value).strip().lower()
    return normalized if normalized in _VALID_LANGS else DEFAULT_LANG


def _lang_from_argv(argv):
    """从 CLI 参数解析 --lang en / --lang=en；未出现或空值返回 None（回退环境变量）"""
    for i, arg in enumerate(argv):
        if arg == "--lang":
            if i + 1 < len(argv):
                return argv[i + 1]
            return None
        if arg.startswith("--lang="):
            value = arg[len("--lang="):]
            return value if value else None
    return None


def _resolve_lang():
    """按优先级解析当前语言：set_lang > --lang > CLOUDQ_LANG > DEFAULT_LANG"""
    if _lang_explicit is not None:
        return _lang_explicit
    from_arg = _lang_from_argv(sys.argv)
    if from_arg is not None:
        return _normalize_lang(from_arg)
    from_env = os.environ.get("CLOUDQ_LANG")
    if from_env:
        return _normalize_lang(from_env)
    return DEFAULT_LANG


def get_lang():
    """获取当前生效语言（zh/en），结果缓存"""
    global _lang_cache
    if _lang_cache is None:
        _lang_cache = _resolve_lang()
    return _lang_cache


def set_lang(lang):
    """显式设置语言（优先级最高），供测试与嵌入方使用

    传 None 表示清除显式设置，恢复常规解析链（--lang > CLOUDQ_LANG > DEFAULT_LANG）。
    """
    global _lang_explicit, _lang_cache
    if lang is None:
        _lang_explicit = None
        _lang_cache = None
        return
    _lang_explicit = _normalize_lang(lang)
    _lang_cache = _lang_explicit


def _reset_cache():
    """重置语言解析缓存（测试用）"""
    global _lang_cache, _lang_explicit
    _lang_cache = None
    _lang_explicit = None


def _get_messages():
    """惰性加载 en 映射（zh 即键，无需 zh 字典）"""
    from locales import en
    return en.MESSAGES


def T(template, **kwargs):
    """翻译并格式化文案

    - zh 模式：返回 template 本身
    - en 模式：查 locales/en.py MESSAGES，缺失回退 template（降级规则）
    - kwargs 非空时 format；占位符不匹配抛异常（翻译缺陷必须暴露，禁止静默吞错）
    - 无 kwargs 时模板原样返回（调用方保证：模板含占位符时必须传 kwargs）
    """
    if get_lang() == "en":
        text = _get_messages().get(template, template)
    else:
        text = template
    if kwargs:
        return text.format(**kwargs)
    return text
