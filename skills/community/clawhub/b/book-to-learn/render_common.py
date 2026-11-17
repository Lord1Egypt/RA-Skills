#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""render_common.py — 渲染公共工具库（纯工具，不含任何版式决策）

设计原则
--------
1. **只管跨引擎共用的机械动作**：字体探测、破折号兜底、转义、markdown/MDX 处理、
   图片解析嵌入、PDF→PNG 光栅化、裁白、产物校验。
   卡片版式（区块顺序 / 字号 / 配色 / 分页）留在各引擎脚本里，互不干扰。
2. **依赖懒加载**：模块顶层不 import weasyprint / PIL / numpy 等重依赖，
   因此任何依赖缺失的环境都能 `import render_common` 做体检（见 runtime_report）。
3. **默认行为与 1.4.1 逐字一致**（裁白阈值 235 / 留白 21px / dpi 150 / 转义策略），
   便于用同一输入做回归对比。
4. **平台无关**：路径不写死；光栅化优先 PyMuPDF（纯 pip 安装，无需系统库），
   poppler 仅作回退；字体按 Windows / macOS / Linux 三平台候选探测。

被谁使用
--------
  gen_card_pdf.py / gen_card_pdf_large.py / gen_image.py   三个渲染引擎
  render.py                                                按类型调度引擎
  setup_verify.py                                          环境体检
"""
import os
import re
import sys
import html as html_mod
import urllib.parse

# --------------------------------------------------------------------------
# 字体
# --------------------------------------------------------------------------
# 三平台候选（顺序即 CSS font-family 的优先级；generic 兜底放最后）
FONT_CANDIDATES = [
    "Microsoft YaHei", "微软雅黑", "SimSun", "宋体",              # Windows
    "PingFang SC", "Hiragino Sans GB", "Heiti SC", "STHeiti",      # macOS
    "Noto Sans CJK SC", "Source Han Sans SC",                      # Linux / 通用
    "WenQuanYi Micro Hei", "WenQuanYi Zen Hei",
    "sans-serif",
]

# 用于「破折号兜底」的 TrueType 字体（必须能渲染 U+2014 / U+2013）
_DASH_FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",             # Debian/Ubuntu
    "/usr/share/fonts/dejavu/DejaVuSans.ttf",                      # Fedora
    "/usr/share/fonts/TTF/DejaVuSans.ttf",                         # Arch
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",                # macOS
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/Library/Fonts/Arial.ttf",
    r"C:\Windows\Fonts\arial.ttf",                                 # Windows
    r"C:\Windows\Fonts\segoeui.ttf",
    r"C:\Windows\Fonts\msyh.ttc",
]

_CJK_MARKERS = ["yahei", "msyh", "simsun", "simhei", "pingfang", "hiragino",
                "heiti", "noto sans cjk", "source han", "wqy", "wenquanyi"]


def _file_url(path):
    """本地绝对路径 → CSS 可用的 file:// URL（兼容 Windows 盘符；percent-encode 空格/中文）。"""
    if re.match(r'^[A-Za-z]:[\\/]', path):
        path = 'file:///' + path.replace('\\', '/')
    else:
        path = 'file://' + path
    return urllib.parse.quote(path, safe='/:')


def find_dash_font():
    """找一个本机可用的 TrueType 字体用于破折号兜底；找不到返回 None。"""
    for p in _DASH_FONT_CANDIDATES:
        if os.path.exists(p):
            return p
    return None


def detect_cjk_fonts():
    """尽力探测本机可用的 CJK 字体族名（返回命中的候选列表，可能为空）。"""
    found = []
    try:
        import subprocess
        out = subprocess.run(['fc-list'], capture_output=True, text=True, timeout=8).stdout.lower()
        if out:
            for fam in FONT_CANDIDATES:
                if fam == 'sans-serif':
                    continue
                key = fam.lower()
                if key in out or any(k for k in _CJK_MARKERS if k in out and k in key):
                    found.append(fam)
            # 命中标记但家族名未直接出现时，给出通用命中结论
            if not found and any(k in out for k in _CJK_MARKERS):
                found.append('Noto Sans CJK SC')
            return found
    except Exception:
        pass
    # 回退：直接看字体目录
    dirs = {
        'win32': [r'C:\Windows\Fonts'],
        'darwin': ['/System/Library/Fonts', '/Library/Fonts', os.path.expanduser('~/Library/Fonts')],
    }.get(sys.platform, ['/usr/share/fonts', os.path.expanduser('~/.fonts')])
    try:
        present = []
        for d in dirs:
            if os.path.isdir(d):
                for root, _dirs, files in os.walk(d):
                    present.extend(f.lower() for f in files)
        if any(k in ' '.join(present) for k in _CJK_MARKERS):
            found.append('PingFang SC' if sys.platform == 'darwin' else 'Noto Sans CJK SC')
    except Exception:
        pass
    return found


# 各平台兜底候选：仅当探测不到任何真实 CJK 字体时使用（**保持简短**，见下）
_PLATFORM_FALLBACK = {
    'win32': ['Microsoft YaHei', 'SimSun'],
    'darwin': ['PingFang SC', 'Hiragino Sans GB'],
}
_LINUX_FALLBACK = ['Noto Sans CJK SC', 'WenQuanYi Micro Hei']


def body_font_family(prefix_dashfix=True, max_families=2):
    """生成 body 的 font-family 值。

    ⚠️ **必须保持简短（建议总长 <= 4）**。实测结论：当家族列表过长时，
    weasyprint 的「逐字回退」会整体退化为「全段用同一个字体」——
    例如 14 个家族的列表会让整段都落到 Noto Serif，且 `DashFix`（unicode-range
    破折号兜底）被直接忽略；同样的 @font-face 配上 3 个家族的短列表则完全正常。
    因此这里只在「探测到的真实可用字体」里取前 max_families 个，绝不堆砌全平台候选。

    `DashFix` 放在**首位**：它只接管 U+2014 / U+2013（见 dash_fix_css），
    其余字符继续按后面的家族渲染。
    """
    fams = []
    if prefix_dashfix and find_dash_font():
        fams.append('DashFix')
    found = [f for f in detect_cjk_fonts() if f and f != 'sans-serif']
    if found:
        fams.extend(found[:max_families])
    else:
        fams.extend(_PLATFORM_FALLBACK.get(sys.platform, _LINUX_FALLBACK)[:max_families])
    fams.append('sans-serif')
    return ", ".join(f if f == 'sans-serif' else ('"%s"' % f) for f in fams)


def dash_fix_css(family='DashFix'):
    """破折号/CJK CFF 字形兜底 CSS（无可用字体时返回空串）。

    背景：部分 PDF 阅读器/知识库预览对 CJK CFF 字形里的破折号（U+2014 / U+2013）
    渲染异常（显示为空白或方框），虽然 PDF 本身嵌了字体、本地编辑器正常。
    做法：用 `unicode-range` 把这两个码位单独交给一份 TrueType 字体渲染。
    """
    p = find_dash_font()
    if not p:
        return ''
    return ("@font-face { font-family: '%s'; src: url('%s'); "
            "unicode-range: U+2014, U+2013; }" % (family, _file_url(p)))


_FONT_DECL_RE = re.compile(r'font-family\s*:\s*[^;}]+(?=[;}])', re.I)


# 是否**已定义** DashFix 的 @font-face（注意：font-family 里提到 DashFix 不算）
_HAVE_DASH_FACE = re.compile(r'@font-face[^}]*DashFix', re.I)


def normalize_font_stack(html_str, stack=None):
    """把页面里**第一处 CJK 字体声明**收敛成「短栈」（DashFix 优先）。

    为什么需要：各引擎历史上各自写着一长串跨平台字体名，而长列表会让逐字回退
    失效、破折号兜底被忽略（详见 body_font_family 的实测说明）。这里统一收敛，
    只改第一处带 CJK 标记的声明（即 body），不碰 code / pre 等等宽字体规则。
    """
    stack = stack or body_font_family()
    state = {'done': False}

    def _rep(m):
        decl = m.group(0)
        if state['done'] or not any(k in decl.lower() for k in _CJK_MARKERS):
            return decl
        state['done'] = True
        return 'font-family: ' + stack

    return _FONT_DECL_RE.sub(_rep, html_str)


def patch_style(html_str, extra_css=None):
    """渲染前的统一样式处理（幂等）：

    1. 把 body 的 CJK 字体声明收敛为「短栈」（首位是 DashFix）；
    2. 注入破折号 `@font-face`（`unicode-range` 限定 U+2014 / U+2013）。

    各引擎不必各自维护这些细节，写 PDF / PNG 之前统一过一道即可——
        HTML(string=rc.patch_style(html_str)).write_pdf(out)
    """
    html_str = normalize_font_stack(html_str)
    css = dash_fix_css()
    if extra_css:
        css = (css + '\n' + extra_css) if css else extra_css
    # 幂等判断必须精确到「@font-face 定义」本身：normalize_font_stack 会把 DashFix
    # 写进 font-family；若只用 'DashFix' in html_str 判断，会误判成已注入而跳过，
    # 结果 DashFix 只有引用、没有定义 → 破折号兜底静默失效。
    if not css or _HAVE_DASH_FACE.search(html_str):
        return html_str
    m = re.search(r'<style[^>]*>', html_str, re.I)
    if not m:
        return html_str
    return html_str[:m.end()] + '\n' + css + html_str[m.end():]


# --------------------------------------------------------------------------
# 转义 / markdown 内联
# --------------------------------------------------------------------------
_MD_LINK = re.compile(r'\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)')


def esc(s):
    """HTML 文本转义（不转义引号，用于文本节点）。"""
    return html_mod.escape(s or '', quote=False)


def esc_attr(s):
    """HTML 属性转义（转义引号，用于属性值）。"""
    return html_mod.escape(s or '', quote=True)


def md_inline(s, links='text'):
    """markdown 行内语法 → HTML（先转义，再识别加粗/行内代码）。

    links:
      'text'  链接转纯文本（默认；知识库/IM 里链接不可点，纯文本可复制）
      'keep'  保留 [文字](url) 原样（交给下游自行处理）
    """
    s = s or ''
    s = re.sub(r'<a\s[^>]*?>', '', s, flags=re.I)
    s = s.replace('</a>', '')
    if links == 'text':
        s = _MD_LINK.sub(lambda m: m.group(1), s)
    s = html_mod.escape(s, quote=False)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = s.replace('\n', '<br>')
    return s


# --------------------------------------------------------------------------
# MDX / JSX 组件标签清理
# --------------------------------------------------------------------------
_IMG_TAG = re.compile(r'<img\s[^<>]*?/?>', re.I)
_MDX_OPEN = re.compile(r'<([A-Z][A-Za-z0-9]*)((?:\s+[^<>]*?)?)(/?)>')
_MDX_CLOSE = re.compile(r'</[A-Z][A-Za-z0-9]*>')
IMG_PLACEHOLDER = '@@IMG:%s@@'
_IMG_PH_RE = re.compile(r'@@IMG:([^@]+)@@')


def _attr_of(tag, name):
    m = re.search(name + r'\s*=\s*["\']([^"\']*)["\']', tag or '')
    return m.group(1) if m else ''


def clean_mdx(s, resolve_img=None):
    """把 MDX/JSX 组件标签转成可读文本，并把 <img> 换成图片占位符。

    背景：文档站（Mintlify / Docusaurus / MDX 类）的正文里混着组件标签，
    如 `<Steps>`、`<Step title="设置模式">`、`<Frame>`、`<Accordion>`、`<Info>`。
    若原样输出，卡片上会出现一堆尖括号噪声；若直接拼进 HTML，还会被浏览器
    当成标签吞掉（内容丢失）。

    规则：
      - 带 `title` / `caption` / `label` 的开标签 → 提升为加粗引子（独占一行）
      - 其余组件开/闭标签 → 直接剥离
      - `<img src="...">` → 交给 resolve_img 映射成本地文件，成功则替换为占位符

    resolve_img: callable(src) -> 本地绝对路径 | None
    """
    s = s or ''
    if resolve_img is not None:
        def _img(m):
            local = resolve_img(_attr_of(m.group(0), 'src'))
            return ('\n' + IMG_PLACEHOLDER % local + '\n') if local else ''
        s = _IMG_TAG.sub(_img, s)
    else:
        s = _IMG_TAG.sub('', s)

    def _open(m):
        attrs = m.group(2) or ''
        for name in ('title', 'caption', 'label'):
            v = _attr_of('<' + m.group(1) + attrs + '>', name)
            if v:
                return '\n**%s**\n' % v
        return ''
    s = _MDX_OPEN.sub(_open, s)
    s = _MDX_CLOSE.sub('', s)
    return s


def render_inline_text(s, links='text'):
    """**卡片正面文字专用**（金句 / 核心观点 / 要点 / 术语）。

    先清 MDX，再转义 + 行内渲染。解决形如
    `openclaw plugins install <plugin-spec>`、`<workspace>` 这类尖括号占位符
    被 HTML 解析吞掉导致的缺字问题。
    """
    return md_inline(clean_mdx(s), links=links)


def md_table(text, links='text'):
    """整块是 markdown 表格时 → HTML 表格；否则返回 None。"""
    lines = [l for l in (text or '').split('\n') if l.strip()]
    if len(lines) < 3:
        return None
    if not all(l.strip().startswith('|') for l in lines):
        return None
    if not re.match(r'^\|[\s:\-|]+\|$', lines[1].strip()):
        return None
    rows = [[c.strip() for c in l.strip().strip('|').split('|')] for l in lines]
    head, body = rows[0], rows[2:]
    th = ''.join('<th>%s</th>' % md_inline(c, links) for c in head)
    trs = ''.join('<tr>' + ''.join('<td>%s</td>' % md_inline(c, links) for c in r) + '</tr>'
                  for r in body)
    return '<table class="mdtable"><thead><tr>%s</tr></thead><tbody>%s</tbody></table>' % (th, trs)


# --------------------------------------------------------------------------
# 图片：资源路径 → 本地文件 → 内嵌
# --------------------------------------------------------------------------
def make_img_resolver(search_dirs):
    """构造 resolve_img。

    文档站正文里的图片路径形如 `/assets/macos-onboarding/01-warning.png`，
    抓取阶段通常已把文件落到某个目录（如下划线扁平化命名
    `_assets_macos-onboarding_01-warning.png`）。本函数按三种命名约定依次尝试，
    命中即返回本地绝对路径。
    """
    def resolve(src):
        if not src:
            return None
        clean = src.split('?')[0].split('#')[0]
        rel = clean.lstrip('/').replace('/', '_')
        names = ['_' + rel, rel, os.path.basename(clean)]
        for d in search_dirs:
            for n in names:
                p = os.path.join(d, n)
                if os.path.exists(p):
                    return p
        return None
    return resolve


def img_html(local_path, css_class='fig-img', max_width='100%'):
    """本地图片 → <img> 标签。"""
    return ('<img class="%s" src="%s" style="max-width:%s" />'
            % (css_class, _file_url(local_path), max_width))


def apply_images(html_str, css_class='fig-img', wrap_class='fig'):
    """把 clean_mdx 产生的占位符替换成真实 <img>（须在转义之后调用）。"""
    def _rep(m):
        return '<div class="%s">%s</div>' % (wrap_class, img_html(m.group(1), css_class))
    return _IMG_PH_RE.sub(_rep, html_str)


# --------------------------------------------------------------------------
# PDF → PNG 光栅化 / 裁白 / 校验
# --------------------------------------------------------------------------
def _load_pymupdf():
    """返回 PyMuPDF 模块；未安装返回 None。

    新版包名是 `pymupdf`，旧版是 `fitz`（新版仍保留 fitz 别名但会打弃用告警），
    两个都试，优先无告警的 `pymupdf`。
    """
    for name in ('pymupdf', 'fitz'):
        try:
            mod = __import__(name)
            if not hasattr(mod, 'open'):
                # PyPI 上存在与 fitz 同名的无关垃圾包，没有 open 就不是真 PyMuPDF
                continue
            return mod
        except ImportError:
            continue
    return None


def rasterize_pdf(pdf_path, dpi=150):
    """PDF → [PIL.Image]。返回 (images, engine)。

    优先 **PyMuPDF**（`pip install pymupdf`，纯 wheel，无需系统库）；
    回退 **pdf2image**（需要系统 poppler + pdftoppm）。
    """
    from PIL import Image
    fitz = _load_pymupdf()
    if fitz is not None:
        zoom = dpi / 72.0
        doc = fitz.open(pdf_path)
        try:
            imgs = []
            for page in doc:
                pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
                imgs.append(Image.frombytes('RGB', (pix.width, pix.height), pix.samples))
        finally:
            doc.close()
        return imgs, 'pymupdf'
    from pdf2image import convert_from_path
    return convert_from_path(pdf_path, dpi=dpi), 'pdf2image'


def stitch_vertical(images, bg='white'):
    """多页纵向拼接成一张长图（页数=1 时原样返回）。"""
    if len(images) == 1:
        return images[0]
    from PIL import Image as _I
    total_h = sum(i.height for i in images)
    max_w = max(i.width for i in images)
    canvas = _I.new('RGB', (max_w, total_h), bg)
    y = 0
    for i in images:
        canvas.paste(i, (0, y))
        y += i.height
    return canvas


def crop_whitespace(png_path, threshold=235, pad=21):
    """裁掉底部空白（保持 1.4.1 语义：任一分量 < threshold 视为有内容）。

    默认参数与 1.4.1 一致（阈值 235、留白 21px），保证回归零差异。
    有 numpy 时走精确路径；无 numpy 时走 PIL 近似路径（±1px）。
    返回 (width, height)。
    """
    try:
        import numpy as np
        from PIL import Image
        img = Image.open(png_path).convert('RGB')
        arr = np.asarray(img)
        is_content = (arr[:, :, 0] < threshold) | (arr[:, :, 1] < threshold) | (arr[:, :, 2] < threshold)
        rows = np.any(is_content, axis=1)
        if rows.any():
            last = int(np.where(rows)[0][-1])
            bottom = min(last + pad, img.height)
            img.crop((0, 0, img.width, bottom)).save(png_path, 'PNG')
            return (img.width, bottom)
        return img.size
    except ImportError:
        return _crop_whitespace_pil(png_path, threshold=threshold, pad=pad)


def _crop_whitespace_pil(png_path, threshold=235, pad=21):
    """无 numpy 时的近似实现。"""
    from PIL import Image, ImageChops
    img = Image.open(png_path).convert('RGB')
    r, g, b = img.split()
    masks = [ch.point(lambda v, t=threshold: 255 if v < t else 0) for ch in (r, g, b)]
    mask = ImageChops.lighter(ImageChops.lighter(masks[0], masks[1]), masks[2])
    bbox = mask.getbbox()
    if bbox:
        bottom = min(bbox[3] + pad, img.height)
        img.crop((0, 0, img.width, bottom)).save(png_path, 'PNG')
        return (img.width, bottom)
    return img.size


def verify_image(png_path, samples=40):
    """校验 PNG 有效且非纯色空白。

    注意：这里**缩略后全图采样**，而不是只看开头若干个像素——宽图（如 750px 宽、
    dpi=150 ≈ 1172px/行）下「前 1000 像素」连一整行都不到，若卡片顶部恰好是白底
    就会被误判成「空白」，进而中断推送。缩略采样对纯色图仍然判为空白。
    """
    from PIL import Image
    try:
        img = Image.open(png_path)
        w, h = img.size
        if w < 10 or h < 10:
            return {'ok': False, 'error': 'image too small: %dx%d' % (w, h)}
        thumb = img.convert('RGB').resize((samples, samples))
        colors = set(thumb.getdata())
        if len(colors) <= 1:
            return {'ok': False, 'error': 'image appears blank (single color)'}
        return {'ok': True, 'width': w, 'height': h, 'mode': img.mode}
    except Exception as e:
        return {'ok': False, 'error': str(e)}


def html_to_png(html_str, out_png, dpi=150, crop=True, crop_opts=None):
    """HTML →（weasyprint）PDF → PNG，可选裁掉底部空白。

    返回 dict：{'image','pages','rasterizer','size','verification'}
    """
    import tempfile
    from weasyprint import HTML
    # 远程图片抓取带 30s 超时（默认 fetcher 无超时，图床挂起会卡死整条渲染链路）
    try:
        from weasyprint.default_url_fetcher import default_url_fetcher

        def _fetcher(url, timeout=30, *a, **k):
            return default_url_fetcher(url, timeout=30, *a, **k)
    except ImportError:
        _fetcher = None
    fd, tmp_pdf = tempfile.mkstemp(suffix='.pdf')
    os.close(fd)
    try:
        if _fetcher is not None:
            HTML(string=html_str).write_pdf(tmp_pdf, url_fetcher=_fetcher)
        else:
            HTML(string=html_str).write_pdf(tmp_pdf)
        images, engine = rasterize_pdf(tmp_pdf, dpi=dpi)
        if not images:
            raise RuntimeError('rasterizer returned no images')
        img = stitch_vertical(images)
        img.save(out_png, 'PNG')
        pages = len(images)
    finally:
        if os.path.exists(tmp_pdf):
            os.remove(tmp_pdf)
    size = crop_whitespace(out_png, **(crop_opts or {})) if crop else None
    return {'image': out_png, 'pages': pages, 'rasterizer': engine,
            'size': size, 'verification': verify_image(out_png)}


# --------------------------------------------------------------------------
# 环境体检（供 setup_verify.py 调用；本模块不依赖任何重依赖也能运行）
# --------------------------------------------------------------------------
def runtime_report():
    import platform
    report = {
        'python': sys.version.split()[0],
        'platform': '%s %s' % (sys.platform, platform.machine()),
        'has_fc_list': False,
        'cjk_fonts_found': [],
        'dash_font': find_dash_font(),
        'deps': {},
        'rasterizer_available': None,
    }
    try:
        import subprocess
        report['has_fc_list'] = subprocess.run(['fc-list'], capture_output=True, timeout=8).returncode == 0
    except Exception:
        pass
    report['cjk_fonts_found'] = detect_cjk_fonts()
    import importlib.util
    for mod in ('weasyprint', 'pymupdf', 'fitz', 'pdf2image', 'PIL', 'numpy', 'bs4', 'requests'):
        try:
            # 用 find_spec 而不是 __import__：只探测是否安装，不真正导入，
            # 避免旧包名（如 fitz）在探测时打出弃用告警污染输出。
            report['deps'][mod] = importlib.util.find_spec(mod) is not None
        except Exception:
            report['deps'][mod] = False
    if _load_pymupdf() is not None:
        report['rasterizer_available'] = 'pymupdf'
    elif report['deps'].get('pdf2image'):
        report['rasterizer_available'] = 'pdf2image(needs poppler)'
    else:
        report['rasterizer_available'] = None
    return report


if __name__ == '__main__':
    import json
    print(json.dumps(runtime_report(), ensure_ascii=False, indent=2))
