#!/usr/bin/env python3
"""
_engine.py — CSS 主题引擎解析层

easy-html 不自带 19 套主题 CSS，而是复用 `html-golive` 提供的 CSS 引擎
（同一作者的开源项目，PyPI: https://pypi.org/project/html-golive/）。
本模块负责按优先级找到那个引擎并返回模块对象。

需要的三个符号：
  STYLE_MAP      样式 key → 中文名
  load_css(key)  读取某个样式的 CSS 文本
  enhance(...)   打 data-role 标注 + 注入 CSS（重做路径用）
  FONT_PRELOADS  字体预加载 URL 映射（可选，缺失时自动跳过）

查找优先级（高 → 低）：
  1. EASY_HTML_CSS_ENGINE 环境变量 —— 直接指向 css_style_enhancer.py 文件路径
  2. `import golive.core.css_style_enhancer` —— pip install html-golive
  3. 本地已 clone 的 html-golive 源码目录（EASY_HTML_GOLIVE_HOME 或 ./html-golive）
  4. 都找不到 → 明确报错并给出安装指引（不静默下载任何东西）
"""
import importlib
import importlib.util
import os
import sys

INSTALL_HINT = (
    "❌ 未找到 CSS 主题引擎。easy-html 的 19 套主题来自 html-golive。\n"
    "   安装（任选其一）：\n"
    "     pip install html-golive\n"
    "     git clone https://github.com/Songhonglei/html-golive && "
    "export EASY_HTML_GOLIVE_HOME=$PWD/html-golive\n"
    "   或直接指定引擎文件：\n"
    "     export EASY_HTML_CSS_ENGINE=/path/to/css_style_enhancer.py"
)


def _log(msg):
    print(msg, file=sys.stderr)


def _load_from_file(path):
    """从任意 css_style_enhancer.py 文件路径加载模块。"""
    parent = os.path.dirname(os.path.abspath(path))
    # 让引擎内部的相对 import（data_role_tagger 等）能被找到
    for p in (parent, os.path.dirname(os.path.dirname(parent))):
        if p and p not in sys.path:
            sys.path.insert(0, p)
    spec = importlib.util.spec_from_file_location("css_style_enhancer", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_engine():
    """按优先级返回 CSS 引擎模块；找不到时 sys.exit(1) 并打印安装指引。"""
    # 1. 显式指定引擎文件
    explicit = os.environ.get("EASY_HTML_CSS_ENGINE")
    if explicit:
        if not os.path.exists(explicit):
            _log(f"❌ EASY_HTML_CSS_ENGINE 指向的文件不存在：{explicit}")
            sys.exit(1)
        return _load_from_file(explicit)

    # 2. 已 pip 安装的 html-golive
    try:
        return importlib.import_module("golive.core.css_style_enhancer")
    except Exception:  # noqa: BLE001 —— 包缺失或导入失败都继续往下找
        pass

    # 3. 本地 clone 的源码目录
    candidates = []
    home = os.environ.get("EASY_HTML_GOLIVE_HOME")
    if home:
        candidates.append(home)
    candidates += [
        os.path.join(os.getcwd(), "html-golive"),
        os.path.expanduser("~/html-golive"),
    ]
    for root in candidates:
        engine = os.path.join(root, "golive", "core", "css_style_enhancer.py")
        if os.path.exists(engine):
            if root not in sys.path:
                sys.path.insert(0, root)
            try:
                return importlib.import_module("golive.core.css_style_enhancer")
            except Exception:  # noqa: BLE001
                return _load_from_file(engine)

    _log(INSTALL_HINT)
    sys.exit(1)
