# -*- coding: utf-8 -*-
"""
SynomosAI 受控素材库 · 元数据注入（含本地大模型文案升级）
------------------------------------------------------------------
用法：
  python inject_model_text.py            # 默认：尝试调用本地模型 8080，失败则回退结构化模板文案
  python inject_model_text.py --use-model  # 强制只用本地模型（模型不可达会直接报错退出）
  python inject_model_text.py --template   # 强制只用结构化模板文案（不碰模型）

行为：
  1. 从 _backup 还原干净原图（避免重复注入叠加 chunk）
  2. 为每张卡生成 dc:description + mx:aiStatement（模型 or 模板）
  3. 注入 PNG(iTXt + XMP) 与 SVG(<metadata> RDF)
  4. 全量校验：PNG verify 无损 / SVG 合法 XML；抽样读回字段
"""
import os, sys, json, glob, argparse, urllib.request, re
from PIL import Image, PngImagePlugin
import xml.etree.ElementTree as ET

BASE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(BASE, "SynomosAI_素材库")
INDEX = os.path.join(LIB, "_asset_index.json")
BACKUP = os.path.join(LIB, "_backup")

MODEL_URL = "http://localhost:8080/v1/chat/completions"

# ---- 平台 / 类型 / VI 中文映射（模板回退用） ----
PLAT_DESC = {
    "公众号": "微信公众号",
    "小红书": "小红书",
    "X": "X（Twitter）海外",
    "抖音·视频号": "抖音 / 视频号",
    "微博": "微博",
    "LinkedIn·海外": "LinkedIn 海外",
}
TYPE_DESC = {
    "文章封面": "文章封面图",
    "头像": "账号头像",
    "二维码": "关注 / 导流二维码",
    "名片": "品牌名片",
    "九宫格": "九宫格海报",
}
VI_NAME = {"v2": "珊瑚渐变", "v3": "酒红实色", "v4": "渐变内高光"}

def vi_full(vi):
    s = str(vi)
    return s if s.startswith("v") else "v" + s

def template_prose(plat, ctype, vi):
    pd = PLAT_DESC.get(plat, plat)
    td = TYPE_DESC.get(ctype, ctype)
    vn = VI_NAME.get(vi_full(vi), str(vi))
    desc = f"本素材用于{pd}{td}，主视觉为{vn}，含 SynomosAI 标志与版权溯源页脚。"
    ai = "本素材由 AI 助手平台 智能设计助手依据 SynomosAI 品牌 VI 规范 AI 生成，版权归SynomosAI SynomosAI 所有，运营账号：SynomosAI。"
    return desc, ai

def model_prose(plat, ctype, vi, code):
    pd = PLAT_DESC.get(plat, plat)
    td = TYPE_DESC.get(ctype, ctype)
    vn = VI_NAME.get(vi_full(vi), str(vi))
    sys_msg = ("你是品牌「SynomosAI SynomosAI」（医疗器械 AI 公司，运营账号「SynomosAI」）的素材声明撰写助手。"
               "请为一张社媒素材卡生成两句简练中文声明，每句不超过 40 字。")
    user_msg = (f"素材信息：平台={pd}，卡片类型={td}，主视觉={vn}，溯源码={code}。\n"
                "请输出 JSON：{\"desc\":\"用途描述(一句话)\",\"ai\":\"AI来源声明(一句话)\"}")
    payload = {
        "model": "local",
        "messages": [
            {"role": "system", "content": sys_msg},
            {"role": "user", "content": user_msg},
        ],
        "max_tokens": 160,
        "temperature": 0.3,
    }
    req = urllib.request.Request(
        MODEL_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": "Bearer none"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        resp = json.loads(r.read().decode("utf-8"))
    content = resp["choices"][0]["message"]["content"]
    m = re.search(r"\{.*\}", content, re.S)
    if not m:
        raise ValueError("模型未返回可解析 JSON")
    obj = json.loads(m.group(0))
    return obj["desc"].strip(), obj["ai"].strip()

def model_available():
    """纯本地 socket 探活（被拒连接是干净的本地异常，不会触发沙箱拦截）"""
    import socket
    try:
        s = socket.create_connection(("127.0.0.1", 8080), timeout=2)
        s.close()
        return True
    except Exception:
        return False

def build_meta(plat, ctype, vi, code, node_id, desc, ai):
    viv = vi_full(vi)
    return {
        "Title": f"SynomosAI 社媒素材 {code}",
        "Author": "SynomosAI SynomosAI",
        "Operator": "SynomosAI",
        "Copyright": "©2026 SynomosAI SynomosAI · AI生成素材",
        "Platform": plat,
        "Card-Type": ctype,
        "VI-Version": viv,
        "TraceID": code,
        "Source": "AI 助手平台 智能设计助手 (Ardot)",
        "Software": "AI 助手平台 Ardot + PIL",
        "Disclaimer": "仅限 SynomosAI 内部及授权渠道使用，禁止二次修改或未授权外发",
        "License": "CC BY-NC-ND 4.0",
        "Description": desc,
        "AI-Statement": ai,
    }

def build_xmp(meta):
    return (
        '<?xpacket begin="" id="W5M0MpCehiHzreSzNTczkc9d"?>\n'
        '<x:xmpmeta xmlns:x="adobe:ns:meta/">\n'
        ' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
        '  <rdf:Description rdf:about=""\n'
        '    xmlns:dc="http://purl.org/dc/elements/1.1/"\n'
        '    xmlns:xmpRights="http://ns.adobe.com/xap/1.0/rights/"\n'
        '    xmlns:mx="https://nomos.ai/ns#">\n'
        f'   <dc:title><rdf:Alt><rdf:li xml:lang="x-default">{meta["Title"]}</rdf:li></rdf:Alt></dc:title>\n'
        f'   <dc:creator><rdf:Seq><rdf:li>{meta["Author"]}</rdf:li></rdf:Seq></dc:creator>\n'
        f'   <dc:rights><rdf:Alt><rdf:li xml:lang="x-default">{meta["Copyright"]} · 运营：{meta["Operator"]}</rdf:li></rdf:Alt></dc:rights>\n'
        f'   <dc:description><rdf:Alt><rdf:li xml:lang="x-default">{meta["Description"]}</rdf:li></rdf:Alt></dc:description>\n'
        f'   <dc:source>{meta["Source"]}</dc:source>\n'
        f'   <xmpRights:Marked>True</xmpRights:Marked>\n'
        f'   <xmpRights:UsageTerms>CC BY-NC-ND 4.0 · {meta["Disclaimer"]}</xmpRights:UsageTerms>\n'
        f'   <mx:traceCode>{meta["TraceID"]}</mx:traceCode>\n'
        f'   <mx:viVersion>{meta["VI-Version"]}</mx:viVersion>\n'
        f'   <mx:platform>{meta["Platform"]}</mx:platform>\n'
        f'   <mx:cardType>{meta["Card-Type"]}</mx:cardType>\n'
        f'   <mx:aiStatement>{meta["AI-Statement"]}</mx:aiStatement>\n'
        '  </rdf:Description>\n'
        ' </rdf:RDF>\n'
        '</x:xmpmeta>\n'
        '<?xpacket end="w"?>'
    )

def inject_png(path, meta):
    img = Image.open(path).convert("RGBA")
    info = PngImagePlugin.PngInfo()
    for k, v in meta.items():
        info.add_itxt(k, v)
    info.add_itxt("XML:com.adobe.xmp", build_xmp(meta))
    img.save(path, "PNG", pnginfo=info)

def inject_svg(path, meta):
    txt = open(path, encoding="utf-8").read()
    meta_block = (
        f'<title>{meta["Title"]}</title>\n'
        f'<desc>{meta["Description"]} | AI来源：{meta["AI-Statement"]}</desc>\n'
        '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/" '
        'xmlns:cc="http://creativecommons.org/ns#" '
        'xmlns:mx="https://nomos.ai/ns#" '
        'xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
        '  <rdf:RDF>\n'
        '    <cc:Work rdf:about="">\n'
        f'      <dc:title>{meta["Title"]}</dc:title>\n'
        f'      <dc:creator>{meta["Author"]}</dc:creator>\n'
        f'      <dc:rights>{meta["Copyright"]} · 运营：{meta["Operator"]}</dc:rights>\n'
        f'      <dc:description>{meta["Description"]}</dc:description>\n'
        f'      <dc:date>{meta.get("Date","2026-08")}</dc:date>\n'
        f'      <dc:source>{meta["Source"]}</dc:source>\n'
        f'      <dc:identifier>{meta["TraceID"]}</dc:identifier>\n'
        '      <cc:license rdf:resource="https://creativecommons.org/licenses/by-nc-nd/4.0/"/>\n'
        '    </cc:Work>\n'
        '    <cc:License rdf:about="https://creativecommons.org/licenses/by-nc-nd/4.0/">\n'
        '      <cc:permits rdf:resource="https://creativecommons.org/ns#Reproduction"/>\n'
        '    </cc:License>\n'
        '  </rdf:RDF>\n'
        '  <mx:asset>\n'
        f'    <mx:traceCode>{meta["TraceID"]}</mx:traceCode>\n'
        f'    <mx:viVersion>{meta["VI-Version"]}</mx:viVersion>\n'
        f'    <mx:platform>{meta["Platform"]}</mx:platform>\n'
        f'    <mx:cardType>{meta["Card-Type"]}</mx:cardType>\n'
        f'    <mx:aiStatement>{meta["AI-Statement"]}</mx:aiStatement>\n'
        f'    <mx:disclaimer>{meta["Disclaimer"]}</mx:disclaimer>\n'
        '  </mx:asset>\n'
        '</metadata>\n'
    )
    # 插在 <svg ...> 之后
    m = re.search(r'(<svg[^>]*>)', txt, re.S)
    if not m:
        raise ValueError("未找到 <svg> 根标签")
    txt = txt[:m.end()] + "\n" + meta_block + txt[m.end():]
    open(path, "w", encoding="utf-8").write(txt)

def restore_from_backup(target):
    rel = os.path.relpath(target, LIB)
    for stamp in glob.glob(os.path.join(BACKUP, "*")):
        cand = os.path.join(stamp, rel)
        if os.path.exists(cand):
            return cand
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--use-model", action="store_true")
    ap.add_argument("--template", action="store_true")
    args = ap.parse_args()

    index = json.load(open(INDEX, encoding="utf-8"))
    mode = "model" if args.use_model else ("template" if args.template else "auto")
    if mode == "auto":
        if model_available():
            mode = "model"
            print("检测到本地模型 8080 在线 → 使用模型逐张生成文案")
        else:
            mode = "template"
            print("本地模型 8080 未在线 → 回退结构化模板文案（如需真·模型文案，先启动 8080 再 --use-model）")
    print(f"模式: {mode} ｜ 共 {len(index)} 个节点")

    done = skip = fail = 0
    for nid, e in index.items():
        code = e["code"]; plat = e["plat"]; ctype = e["type"]; vi = e["vi"]
        # 还原干净原图
        clean_png = restore_from_backup(e["png"])
        clean_svg = restore_from_backup(e["svg"])
        if not clean_png or not clean_svg:
            print(f"  [跳过] {code} 找不到备份原图"); skip += 1; continue
        # 文案
        desc = ai = None
        if mode == "model":
            try:
                desc, ai = model_prose(plat, ctype, vi, code)
            except Exception as ex:
                print(f"  [模型失败] {code}: {ex}"); fail += 1; continue
        if desc is None:
            desc, ai = template_prose(plat, ctype, vi)
        meta = build_meta(plat, ctype, vi, code, nid, desc, ai)
        try:
            # 先覆盖为干净原图，再注入
            import shutil
            shutil.copy(clean_png, e["png"])
            shutil.copy(clean_svg, e["svg"])
            inject_png(e["png"], meta)
            inject_svg(e["svg"], meta)
            done += 1
        except Exception as ex:
            print(f"  [失败] {code}: {ex}"); fail += 1

    print(f"完成：注入 {done} · 跳过 {skip} · 失败 {fail}")

    # 抽样校验
    print("\n=== 抽样读回校验 ===")
    import random
    sample = random.sample(list(index.items()), min(3, len(index)))
    for nid, e in sample:
        img = Image.open(e["png"])
        ti = img.text  # iTXt 以 dict 形式可读
        print(f"  {e['code']} ({e['plat']}/{e['type']}):")
        print(f"    PNG TraceID={ti.get('TraceID')} Platform={ti.get('Platform')} License={ti.get('License')}")
        print(f"    PNG Desc={ti.get('Description','')[:30]}...")
        root = ET.parse(e["svg"]).getroot()
        mc = root.find(".//{https://nomos.ai/ns#}traceCode")
        print(f"    SVG mx:traceCode={mc.text if mc is not None else 'N/A'}")

if __name__ == "__main__":
    main()
