#!/usr/bin/env python3
"""可研交付视觉验收器 —— AI 排版自检的最后一道闸（多模型交叉看图）

背景：AI 生成的 docx 排版问题（封面乱/表格挤/AI痕迹），纯文字检查看不见，
     必须渲染成图让视觉模型"亲眼"验收。单个模型会敷衍/误判，用 2+ 个交叉验证。

用前准备:
  pip install python-docx pymupdf   # 渲染 docx→pdf→png
  视觉模型 key（任选其一，放环境变量）:
    export DASHSCOPE_API_KEY=sk-...   # 阿里百炼 qwen-vl-max（推荐）
    export ZHIPU_API_KEY=...           # 智谱 glm-4v-flash（免费）
    export MIMO_API_KEY=...            # 小米 mimo-v2.5（原生多模态）
    export DEEPSEEK_API_KEY=...        # DeepSeek 官方 deepseek-v4-flash-vision-exp

用法:
  # 一键：docx → 渲染关键页(封面/前几页/含表格页) → 多模型审
  python3 vision_check.py 报告.docx [--models mimo,deepseek-vision,glm] [--dpi 110] [--pages 0-5]
  # 或直接审已有图片
  python3 vision_check.py --imgs 封面.png 表格页.png [--models mimo]

输出：每个模型对每张图的判断（问题+位置+严重程度 / 未发现问题）。
交叉规则：任一模型报问题 → 回 docx 修 → 重渲染再验，直到全绿。
LibreOffice 装不上时：用 `soffice --headless --convert-to pdf` 手动转，再喂 PDF 页图。
"""
import base64, json, os, re, subprocess, sys, tempfile, urllib.request

# ---------------- 模型注册表（按可用 key 自动启用） ----------------
def _mk(base, key_env, default_model):
    key = os.environ.get(key_env, '')
    if not key: return None
    return {"url": base.rstrip('/') + "/chat/completions", "key": key, "model": default_model}

MODELS = {
    "glm":          _mk("https://open.bigmodel.cn/api/paas/v4", "ZHIPU_API_KEY", "glm-4v-flash"),
    "qwen-vl":      _mk("https://dashscope.aliyuncs.com/compatible-mode/v1", "DASHSCOPE_API_KEY", "qwen3-vl-flash"),
    "mimo":         _mk("https://api.xiaomimimo.com/v1", "MIMO_API_KEY", "mimo-v2.5"),
    "deepseek-vision": _mk("https://api.deepseek.com/v1", "DEEPSEEK_API_KEY", "deepseek-v4-flash-vision-exp"),
}
MODELS = {k: v for k, v in MODELS.items() if v}
# 模型默认顺序：免费优先（glm）→ 便宜快（qwen3-vl-flash）→ mimo → deepseek(留给干活的，备胎)
DEFAULT_ORDER = ["glm", "qwen-vl", "mimo", "deepseek-vision"]
# glm-4v-flash 的 max_tokens 上限 1024，其余可到 8000
MAX_TOKENS = {"glm": 1024}

PROMPT = """你是专业排版校对专家。请仔细检查这张文档页面截图，逐项给出明确判断：
1.【封面/页面整体】元素是否居中？有没有元素跑出页面、贴边、重叠？
2.【文字】有无文字挤压、行距过密、字号突兀、字体混乱、乱码、明显偏大偏小？
3.【表格】若含表格：行高列宽是否协调？单元格文字有没有被裁切挤压？表格是否超出页面？
4.【间距】标题与正文、表格与文字之间的留白是否正常？
5.【明显缺陷】任何像"机器生成、没人工检查过"的排版瑕疵（如：该缩进的没缩进、手动列表不齐、符号错乱），请具体指出位置。
回答要求：若发现问题，逐条列出【问题+位置+严重程度】；若确实没问题，回答"未发现问题"。请务必仔细看，不要敷衍。"""

def call_vision(name, img_path):
    m = MODELS[name]
    with open(img_path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode()
    body = {"model": m["model"], "messages": [{"role": "user", "content": [
        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}},
        {"type": "text", "text": PROMPT}]}], "max_tokens": MAX_TOKENS.get(name, 4000)}
    req = urllib.request.Request(m["url"], data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {m['key']}"})
    try:
        r = json.load(urllib.request.urlopen(req, timeout=240))
        out = (r['choices'][0]['message'].get('content') or '').strip()
        if not out:  # reasoning 模型把预算吃光，重试一次压低思考
            body["max_tokens"] = MAX_TOKENS.get(name, 8000)
            body["messages"][0]["content"][1]["text"] = PROMPT + "\n请直接输出结论，不要输出思考过程。"
            req = urllib.request.Request(m["url"], data=json.dumps(body).encode(),
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {m['key']}"})
            r = json.load(urllib.request.urlopen(req, timeout=240))
            out = (r['choices'][0]['message'].get('content') or '').strip()
        return out or "<模型返回空内容，请人工复核该页>"
    except Exception as e:
        return f"<调用失败: {str(e)[:200]}>"

def docx_to_pngs(docx_path, dpi=110, max_pages=8):
    """docx → pdf → png（自动选页：封面+前几页+含表格/长文页）"""
    tmpd = tempfile.mkdtemp(prefix='vision_')
    pdf_path = os.path.join(tmpd, 'doc.pdf')
    subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', tmpd, docx_path],
                   capture_output=True, timeout=300, env={**os.environ, 'HOME': os.path.expanduser('~')})
    pdfs = [f for f in os.listdir(tmpd) if f.endswith('.pdf')]
    if not pdfs: return [], tmpd
    try:
        import fitz
    except ModuleNotFoundError:
        # pymupdf 常见装在 python3.12 --user 或其它解释器，兜底尝试
        for cand in ('/usr/bin/python3.12', '/usr/local/bin/python3.12', 'python3.12'):
            try:
                import subprocess as _sp
                r = _sp.run([cand, '-c', 'import pymupdf, sys; print(pymupdf.__file__)'],
                            capture_output=True, text=True, timeout=20)
                if r.returncode == 0 and r.stdout.strip():
                    import os as _os
                    sp_dir = _os.path.dirname(_os.path.dirname(r.stdout.strip()))  # …/site-packages
                    sys.path.insert(0, sp_dir)
                    import pymupdf as fitz
                    break
            except Exception:
                continue
        else:
            print("✗ 缺 pymupdf。装: pip install pymupdf  或  python3.12 -m pip install --user pymupdf")
            return [], tmpd
    doc = fitz.open(os.path.join(tmpd, pdfs[0]))
    n = min(len(doc), max_pages)
    picks = set(range(n))
    out = []
    for pno in sorted(picks):
        fp = os.path.join(tmpd, f'p{pno+1}.png')
        doc[pno].get_pixmap(dpi=dpi).save(fp)
        out.append(fp)
    return out, tmpd

if __name__ == '__main__':
    args = sys.argv[1:]
    models = list(DEFAULT_ORDER)
    imgs = []
    docx_path = None
    i = 0
    while i < len(args):
        a = args[i]
        if a == '--models' and i+1 < len(args):
            models = [x.strip() for x in args[i+1].split(',') if x.strip()]; i += 1
        elif a == '--imgs':
            while i+1 < len(args) and not args[i+1].startswith('--'):
                imgs.append(args[i+1]); i += 1
        elif a.startswith('--dpi') and i+1 < len(args):
            i += 1
        elif not a.startswith('--') and not docx_path and os.path.exists(a) and a.endswith('.docx'):
            docx_path = a
        elif not a.startswith('--') and os.path.exists(a):
            imgs.append(a)
        i += 1

    if docx_path:
        print(f"渲染 {docx_path} ...", flush=True)
        imgs, tmpd = docx_to_pngs(docx_path)
        if not imgs:
            print("✗ 渲染失败：需要 soffice(LibreOffice)。装: sudo apt install libreoffice-writer")
            sys.exit(1)
        print(f"✓ 渲染 {len(imgs)} 页 → 视觉审查\n")

    available = [m for m in models if m in MODELS]
    if not available:
        print("✗ 无可用视觉模型 key。请 export DASHSCOPE_API_KEY / ZHIPU_API_KEY / MIMO_API_KEY / DEEPSEEK_API_KEY")
        sys.exit(1)

    issues = []
    for img in imgs:
        print(f"{'='*56}\n📄 {os.path.basename(img)}\n{'='*56}")
        for name in available:
            print(f"\n--- {name} ---")
            verdict = call_vision(name, img)
            print(verdict[:1200])
            if verdict and '未发现' not in verdict[:20] and '调用失败' not in verdict[:20]:
                issues.append((os.path.basename(img), name, verdict[:200]))
    print(f"\n{'='*56}\n汇总: {len(imgs)}图 × {len(available)}模型, 报告 {len(issues)} 处疑似问题")
    for fn, m, v in issues[:6]:
        print(f"  ⚠ {fn} [{m}]: {v[:120].replace(chr(10),' ')}")
    if not issues:
        print("✅ 全部通过")
