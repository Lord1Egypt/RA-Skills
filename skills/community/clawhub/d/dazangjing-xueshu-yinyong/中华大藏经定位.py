# -*- coding: utf-8 -*-
"""
中华大藏经（中华书局版）全文定位器
=================================
数据源：中华书局《佛学典籍文献数据库》fo.ancientbooks.cn（古联公司）
        —— 收录《中华大藏经（汉文部分）》全帙（106 册），含册/页/卷级定位。

重要前提：
  * 该站提供检索 API（POST https://fo.ancientbooks.cn/v1/search），
    但**必须登录**（试用会员或正式会员）才能返回结果；
    未登录时返回 {"code":500,"message":"参数错误."}。
  * Cookie 通过环境变量 FO_COOKIE 或本文件同目录 fo_cookie.txt 提供，
    切勿把 Cookie 写死进脚本或提交到仓库。

用法：
  set FO_COOKIE=你的fo登录Cookie
  python 中华大藏经定位.py "前两醍醐是权非实故有教而无人"
  python 中华大藏经定位.py "妙法莲华经玄义" --经

输出：册 / 页 / 卷 / 部经名 + 原文片段；并附带原始 JSON 便于校准字段。
"""
import sys, os, json, subprocess, urllib.request, urllib.error, time, re

BASE = "https://fo.ancientbooks.cn"
SEARCH_EP = BASE + "/v1/search"

# ---- 登录态 Cookie（仅运行时提供，绝不硬编码）----
def 取Cookie():
    env = os.environ.get("FO_COOKIE", "").strip()
    if env:
        return env
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fo_cookie.txt")
    if os.path.exists(p):
        return open(p, encoding="utf-8").read().strip()
    return ""

# ---- 网络请求（urllib，失败回退 curl，含 3 次退避重试）----
def 请求(url, data=None, headers=None, cookie=""):
    hd = {"Content-Type": "application/json",
          "Accept": "application/json",
          "Referer": BASE + "/",
          "Origin": BASE}
    if cookie:
        hd["Cookie"] = cookie
    if headers:
        hd.update(headers)
    last = None
    for i in range(3):
        try:
            if data is not None:
                body = json.dumps(data, ensure_ascii=False).encode("utf-8")
                req = urllib.request.Request(url, data=body, headers=hd, method="POST")
            else:
                req = urllib.request.Request(url, headers=hd, method="GET")
            with urllib.request.urlopen(req, timeout=25) as r:
                return r.read().decode("utf-8", "ignore")
        except urllib.error.URLError as e:
            last = str(e)
            time.sleep(1.5 * (i + 1))
        except Exception as e:
            last = str(e)
            time.sleep(1.5 * (i + 1))
    # 回退 curl
    try:
        import shutil
        if shutil.which("curl"):
            cmd = ["curl", "-s", "-m", "25", url,
                   "-H", "Content-Type: application/json",
                   "-H", "Accept: application/json",
                   "-H", "Referer: " + BASE + "/",
                   "-H", "Origin: " + BASE]
            if cookie:
                cmd += ["-H", "Cookie: " + cookie]
            if data is not None:
                cmd += ["-X", "POST", "-d", json.dumps(data, ensure_ascii=False)]
            return subprocess.run(cmd, capture_output=True, text=True,
                                  timeout=30).stdout
    except Exception as e:
        last = str(e)
    raise RuntimeError("请求失败: " + (last or "未知错误"))

# ---- 构造检索载荷（还原网页 search 页 e 对象）----
def 构造载荷(词, 页码=1, 每页=10):
    return {
        "libId": 1,            # 1 = 全部文献（含中华大藏经）
        "modelId": 5,          # 5 = ARTICLE（全文模式）
        "sortMethod": 1,
        "catId": None,
        "foxueCatId": None,
        "yearCatId": None,
        "rootId": None,
        "isAdvance": False,
        "distance": False,
        "useSynonyms": True,
        "useProperNouns": False,
        "conditionJson": "",
        "myBookSelf": False,
        "crossingZhu": False,
        "ignorePunc": True,
        "orderByColumn": "CAT",
        "hasBuy": False,
        "isAsc": "asc",
        "needRecord": False,
        "content": 词,         # 检索词（无标点匹配更稳，脚本已忽略标点）
        "pageNum": 页码,
        "pageSize": 每页,
    }

# ---- 从返回里抽取 册/页/卷/经名/原文 ----
KEY_PATTERNS = {
    "册": re.compile(r"(册|volume|vol|ce|ceid)", re.I),
    "页": re.compile(r"(页|page|ye|pagenum)", re.I),
    "卷": re.compile(r"(卷|juan|juanhao)", re.I),
    "经名": re.compile(r"(书名|经名|bookname|book_name|title|name|典籍|文献)", re.I),
    "原文": re.compile(r"(content|text|正文|原文|snippet|fragment|excerpt)", re.I),
}

def 抽取(节点, 路径=""):
    """深度遍历 JSON，找含 册/页/卷 的兄弟字段。"""
    out = []
    if isinstance(节点, dict):
        flat = {str(k).lower(): v for k, v in 节点.items()}
        rec = {}
        for 中文, pat in KEY_PATTERNS.items():
            for k, v in flat.items():
                if pat.search(k) and v not in (None, "", []):
                    rec[中文] = v
                    break
        if rec:
            rec["_路径"] = 路径
            # 优先抓原文片段
            for k, v in flat.items():
                if KEY_PATTERNS["原文"].search(k) and isinstance(v, str) and len(v) > 4:
                    rec["原文"] = v
                    break
            out.append(rec)
        for k, v in 节点.items():
            out += 抽取(v, 路径 + "/" + str(k))
    elif isinstance(节点, list):
        for i, v in enumerate(节点):
            out += 抽取(v, 路径 + f"[{i}]")
    return out

def 主(词, 仅经名=False):
    cookie = 取Cookie()
    if not cookie:
        print("⚠️ 未检测到 fo.ancientbooks.cn 登录 Cookie。")
        print("   请先登录 fo.ancientbooks.cn（试用/正式会员），然后：")
        print("   1) 浏览器 F12 → Application → Cookies → 复制 fo.ancientbooks.cn 的 Cookie 整串；")
        print("   2) 设环境变量：  set FO_COOKIE=粘贴的Cookie   （或写入本目录 fo_cookie.txt）")
        print("   之后重跑本脚本即可。")
        return
    净词 = re.sub(r"[\s，。、；：“”‘’（）()《》]", "", 词)
    载荷 = 构造载荷(净词)
    print(f"🔍 检索词：{净词}（已忽略标点）")
    try:
        raw = 请求(SEARCH_EP, 载荷, cookie=cookie)
    except Exception as e:
        print("请求异常：", e)
        return
    try:
        js = json.loads(raw)
    except Exception:
        print("返回非 JSON：", raw[:300])
        return
    if js.get("code") not in (200, None) or js.get("success") is False:
        print("⚠️ 接口返回异常：", json.dumps(js, ensure_ascii=False)[:400])
        print("   若显示『参数错误』，多为 Cookie 失效或权限不足，请重新复制登录 Cookie。")
        return
    data = js.get("data", {})
    # 兼容两种返回结构
    lst = data.get("list") or data.get("records") or data.get("result") or []
    total = data.get("total") or js.get("total") or "?"
    print(f"✅ 命中 {total} 条，展示前 {min(len(lst), 10)} 条：\n")
    if not lst:
        print("（无结果。可换更短的特征词，或确认该句确在中华大藏经内。）")
        return
    for i, it in enumerate(lst[:10], 1):
        抽 = 抽取(it)
        主记录 = 抽[0] if 抽 else {}
        print(f"【{i}】" + "  ".join(f"{k}={v}" for k, v in 主记录.items() if k != "_路径"))
        if i < 10:
            print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    词 = sys.argv[1]
    主(词)
