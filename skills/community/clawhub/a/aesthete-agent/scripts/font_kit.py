# -*- coding: utf-8 -*-
"""font_kit.py — 字体资产管线(0.18.0,typography-aesthetics.md 第五节落地)。

三档:scaffold --fonts none|preset|auto
  none  现状(系统栈,禁 900)
  preset 复制随包预置子集(零依赖,OFL)→ 输出旁 woff2 + @font-face
  auto  收集页面用字 → fonttools 现场子集(VF 实例化)→ 同 preset 落盘;
        缺 fonttools/字体源时优雅降级 preset 并提示一行 pip 命令。
@font-face 家族名 Aesthete Serif(font-weight 900),插到产出页 <style> 头部,
并把 --serif 栈前缀替换为 'Aesthete Serif'(原降级链保留在后)。
被 palette_forge.py 的 cmd_scaffold 调用。纯 stdlib + 可选 fontTools。
"""
import os
import re
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
PRESET_DIR = os.path.join(HERE, "..", "assets", "fonts")
PRESET_FILES = ("serif-black-headline.woff2", "serif-black-common500.woff2")
FAMILY = "Aesthete Serif"
SERIF_ANCHOR = "--serif:'Noto Serif SC'"
# VF 候选字体源(按序探测;Linux 常见路径列入但以实际存在为准)
VF_CANDIDATES = (
    r"C:\Windows\Fonts\NotoSerifSC-VF.ttf",
    os.path.expanduser("~/.fonts/NotoSerifSC-VF.ttf"),
    "/usr/share/fonts/opentype/noto/NotoSerifSC-VF.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifSC-VF.ttf",
)
CJK_RE = re.compile(r"[\u2E80-\u2EFF\u3000-\u303F\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF\uFF00-\uFFEF]")
DEFAULT_PUNCT = "，。：；！？·—｜、（）「」『』“”‘’…0123456789"


def collect_chars(html):
    """剥标签后收集 CJK 用字(保序去重)+ 默认标点数字。"""
    text = re.sub(r"<style[\s\S]*?</style>|<script[\s\S]*?</script>|<[^>]+>", " ", html)
    chars = "".join(dict.fromkeys(CJK_RE.findall(text)))
    return chars + DEFAULT_PUNCT


def find_vf():
    for p in VF_CANDIDATES:
        if os.path.exists(p):
            return p
    return None


def subset_vf(vf_path, weight, chars, out_path):
    """VF 实例化 + 子集化 → woff2。缺 fontTools/失败返回 False(调用方降级)。"""
    try:
        from fontTools import subset as ft_subset
        from fontTools.varLib.instancer import instantiateVariableFont
        from fontTools.ttLib import TTFont
    except ImportError:
        return False
    try:
        font = TTFont(vf_path)
        if "fvar" in font:
            axes = {"wght": weight}
            for a in font["fvar"].axes:
                if a.axisTag not in axes:
                    axes[a.axisTag] = a.defaultValue
            instantiateVariableFont(font, axes, inplace=True)
        opts = ft_subset.Options()
        opts.flavor = "woff2"
        opts.layout_features = ["*"]
        opts.hinting = False
        ss = ft_subset.Subsetter(options=opts)
        ss.populate(text="".join(sorted(set(chars))))
        ss.subset(font)
        font.save(out_path)
        return os.path.exists(out_path) and os.path.getsize(out_path) > 1000
    except Exception:
        return False


def emit_faces(out_dir, mode, html, log=None):
    """→ (html_with_faces, copied_font_files)。mode∈{none,preset,auto}。"""
    if mode == "none":
        return html, []
    faces = []
    copied = []
    os.makedirs(out_dir, exist_ok=True)
    if mode == "auto":
        chars = collect_chars(html)
        vf = find_vf()
        target = os.path.join(out_dir, "page-serif-900.woff2")
        if vf and subset_vf(vf, 900, chars, target):
            copied.append(target)
            faces.append(f'@font-face{{font-family:"{FAMILY}";src:url("page-serif-900.woff2") '
                         f'format("woff2");font-weight:900;font-display:swap}}')
        else:
            if log:
                log("auto 降级 preset(缺 fontTools 或字体源;pip install fonttools brotli 升级全文覆盖)")
            mode = "preset"
    if mode == "preset" and not faces:
        for fn in PRESET_FILES:
            src = os.path.join(PRESET_DIR, fn)
            if not os.path.exists(src):
                continue
            dst = os.path.join(out_dir, fn)
            if not os.path.exists(dst):
                shutil.copy2(src, dst)
            copied.append(dst)
            faces.append(f'@font-face{{font-family:"{FAMILY}";src:url("{fn}") '
                         f'format("woff2");font-weight:900;font-display:swap}}')
    if not faces:
        return html, []
    block = "\n".join(faces)
    if "<style>" in html:
        html = html.replace("<style>", "<style>\n" + block, 1)
    else:
        html = html.replace("<style ", "<style data-fonts=\"1\" ", 1)
    html = html.replace(SERIF_ANCHOR, f"--serif:'{FAMILY}'," + SERIF_ANCHOR.split(":", 1)[1])
    return html, copied
