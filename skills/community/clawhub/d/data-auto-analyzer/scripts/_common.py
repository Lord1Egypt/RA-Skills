"""
共享工具模块 - data-auto-analyzer
供 analyze.py / diagnose.py / ab_test.py / daily_report.py 共用
"""
import os
import pandas as pd
import warnings
warnings.filterwarnings("ignore")


def load_file(path):
    """统一读取 xlsx/xls/csv 文件，自动识别编码，自动剔除汇总行"""
    ext = os.path.splitext(path)[1].lower()
    df = None
    if ext in (".xlsx", ".xlsm"):
        df = pd.read_excel(path, engine="openpyxl")
    elif ext == ".xls":
        df = pd.read_excel(path, engine="xlrd")
    elif ext == ".csv":
        for enc in ("utf-8", "utf-8-sig", "gbk", "gb2312"):
            try:
                df = pd.read_csv(path, encoding=enc)
                break
            except Exception:
                continue
    if df is None:
        raise ValueError(f"不支持的格式: {ext}")
    return _drop_summary_rows(df)


def _drop_summary_rows(df):
    """识别并剔除报表中的汇总/合计/总计/小计/平均行"""
    summary_markers = {
        "汇总", "合计", "总计", "小计", "平均", "均值", "求和",
        "total", "sum", "subtotal", "summary", "avg", "average", "mean",
        "总合", "总和"
    }

    def is_summary_row(row):
        for v in row.values:
            if pd.isna(v):
                continue
            s = str(v).strip().lower()
            if s in summary_markers:
                return True
            # 多人名堆叠：超过 5 个逗号且无空格，很可能是汇总行
            if s.count(",") >= 5 and len(s) > 20 and " " not in s:
                return True
        return False

    before = len(df)
    mask = df.apply(is_summary_row, axis=1)
    if mask.any():
        df = df[~mask].reset_index(drop=True)
        print(f"  [自动清理] 移除 {before - len(df)} 行汇总/合计类数据")
    return df


# 常见列名识别规则
COL_KEYWORDS = {
    "cost": ["消耗", "花费", "成本", "费用", "预算", "cost", "spend", "spent"],
    "impression": ["展示", "曝光", "展现", "impression", "show"],
    "click": ["点击", "click", "tap"],
    "conversion": ["转化", "注册", "下单", "成交", "激活", "conversion", "convert"],
    "ctr": ["ctr", "点击率"],
    "cpc": ["cpc", "点击单价"],
    "cpa": ["cpa", "转化成本"],
    "cpm": ["cpm", "千次展示"],
    "revenue": ["收入", "营收", "gmv", "revenue", "income"],
    "roi": ["roi", "roas"],
    "campaign": ["计划", "广告", "campaign", "adgroup", "creative", "ad name", "广告组"],
}


def find_column(df, key, exclude=None):
    """
    在 df.columns 中找关键词对应的列，优先完全匹配，其次部分匹配
    exclude: 已识别的列，避免重复
    """
    exclude = exclude or set()
    keywords = COL_KEYWORDS.get(key, [])

    # 优先：完全匹配（忽略大小写和空格）
    for col in df.columns:
        if col in exclude:
            continue
        col_norm = str(col).lower().strip().replace(" ", "")
        for kw in keywords:
            if col_norm == kw.lower().strip().replace(" ", ""):
                return col

    # 其次：包含匹配
    for col in df.columns:
        if col in exclude:
            continue
        col_norm = str(col).lower().strip()
        for kw in keywords:
            if kw.lower() in col_norm:
                return col

    return None


def auto_detect_columns(df):
    """
    自动识别广告报表中的关键列，返回 dict
    包含: cost/impression/click/conversion/ctr/cpc/cpa/cpm/revenue/roi/campaign
    """
    result = {}
    used = set()
    for key in ["campaign", "cost", "impression", "click", "conversion",
                "ctr", "cpc", "cpa", "cpm", "revenue", "roi"]:
        col = find_column(df, key, exclude=used)
        if col is not None:
            result[key] = col
            used.add(col)
    return result


def to_numeric_safe(series):
    """安全转数值：处理千分位逗号和百分号"""
    cleaned = series.astype(str).str.replace(",", "").str.replace("%", "").str.strip()
    return pd.to_numeric(cleaned, errors="coerce")


def fmt_number(n):
    """格式化数字显示"""
    if pd.isna(n) or n is None:
        return "-"
    if isinstance(n, str):
        return n
    if abs(n) >= 1e8:
        return f"{n / 1e8:.2f}亿"
    if abs(n) >= 1e4:
        return f"{n / 1e4:.2f}万"
    if isinstance(n, float) and not n.is_integer():
        return f"{n:,.2f}"
    return f"{int(n):,}"


def pct_change(new, old):
    """计算环比变化百分比，返回 (百分比, 箭头符号)"""
    if old is None or pd.isna(old) or old == 0:
        return None, "→"
    change = (new - old) / abs(old) * 100
    if abs(change) < 0.5:
        return change, "→"
    return change, "↑" if change > 0 else "↓"


# ── 统一输出目录 ──────────────────────────────────────────────────
# 默认所有生成文件（HTML / TXT）都放到一个 data-auto-analyzer 文件夹下。
# 优先级：
#   1. 环境变量 DATA_AUTO_ANALYZER_OUTDIR（用户/部署方显式指定）
#   2. 当前工作目录下的 ./data-auto-analyzer
# 这样既不依赖 /mnt/user-data、/home/claude 等特定沙箱路径，
# 在本地、云端沙箱、CI 等任意环境都能正常工作。
DEFAULT_OUTPUT_DIRNAME = "data-auto-analyzer"


def get_output_dir():
    """返回统一输出目录的绝对路径，目录不存在时自动创建。"""
    out_dir = os.environ.get("DATA_AUTO_ANALYZER_OUTDIR", "").strip()
    if not out_dir:
        out_dir = os.path.join(os.getcwd(), DEFAULT_OUTPUT_DIRNAME)
    out_dir = os.path.abspath(out_dir)
    os.makedirs(out_dir, exist_ok=True)
    return out_dir


def resolve_output_path(path):
    """把输出路径解析到统一输出目录。

    - 若传入的是纯文件名（不含目录分隔符），放到统一输出目录下；
    - 若用户显式给了带目录的路径（绝对或相对），尊重用户选择，
      仅确保其父目录存在。
    返回最终的绝对路径。
    """
    if os.path.dirname(path):
        abs_path = os.path.abspath(path)
        parent = os.path.dirname(abs_path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        return abs_path
    return os.path.join(get_output_dir(), path)


# 通用 HTML 样式（暗色主题）
COMMON_CSS = """
:root {
  --bg-primary: #0f1117;
  --bg-card: #1a1d2e;
  --bg-card-hover: #222640;
  --border: #2a2e42;
  --text-primary: #e8eaf0;
  --text-secondary: #8b90a5;
  --text-dim: #5c6078;
  --accent-blue: #4e7cff;
  --accent-green: #22c493;
  --accent-orange: #f5a623;
  --accent-red: #f25757;
  --accent-purple: #9370ff;
  --accent-cyan: #22d3ee;
  --gradient-1: linear-gradient(135deg, #4e7cff 0%, #9370ff 100%);
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Roboto, sans-serif;
  background: var(--bg-primary);
  color: var(--text-primary);
  line-height: 1.6;
  min-height: 100vh;
}
.container { max-width: 1400px; margin: 0 auto; padding: 32px 24px; }
.header {
  text-align: center;
  padding: 48px 24px;
  background: linear-gradient(180deg, rgba(78,124,255,0.08) 0%, transparent 100%);
  border-bottom: 1px solid var(--border);
}
.header h1 {
  font-size: 2rem; font-weight: 700;
  background: var(--gradient-1);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 8px;
  letter-spacing: -0.02em;
}
.header .subtitle { color: var(--text-secondary); font-size: 0.95rem; }
.section-title {
  font-size: 1.2rem; font-weight: 600;
  margin: 40px 0 20px;
  padding-left: 14px;
  border-left: 3px solid var(--accent-blue);
}
.footer {
  text-align: center; padding: 32px;
  color: var(--text-dim); font-size: 0.78rem;
  border-top: 1px solid var(--border); margin-top: 40px;
}
"""


# ══════════════════════════════════════════════════════════════════
#  v4 共享：通用预处理 · 动态列识别 · 角色/派生指标 · 浅色主题页面框架
# ══════════════════════════════════════════════════════════════════
import html as _html
import json as _json


def preprocess(df):
    """删除整行/整列全空的脏数据，去列名首尾空格。"""
    df = df.dropna(axis=0, how="all").dropna(axis=1, how="all").reset_index(drop=True)
    df.columns = [str(c).strip() for c in df.columns]
    return df


def _is_date_name(c):
    s = str(c).lower()
    return any(k in s for k in ["日期", "时间", "date", "time", "day", "month", "year", "周", "月", "年"])


def _is_id_name(c):
    s = str(c).lower().strip()
    if s in {"排名", "序号", "编号", "id", "rank", "no", "no.", "#"}:
        return True
    return any(s.endswith(suf) for suf in ("id", "_id", "编号", "序号", "编码", "rank no."))


def detect_columns(df):
    """动态识别 date_col, dim_cols, metric_cols, pct_cols（原地转换数值/日期列）。"""
    date_col, dim_cols, metric_cols, pct_cols = None, [], [], set()
    for col in df.columns:
        s = df[col]
        if _is_id_name(str(col)):
            dim_cols.append(col)
            continue
        is_dt = pd.api.types.is_datetime64_any_dtype(s)
        if date_col is None and (is_dt or _is_date_name(str(col))):
            try:
                if not pd.api.types.is_numeric_dtype(s):
                    conv = pd.to_datetime(s, errors="coerce")
                    if conv.notna().sum() > len(df) * 0.5:
                        date_col = col; df[col] = conv; continue
                elif is_dt:
                    date_col = col; continue
            except Exception:
                pass
        raw = s.astype(str)
        had_pct = raw.str.contains("%", na=False).any()
        num = pd.to_numeric(raw.str.replace(",", "").str.replace("%", "").str.strip(), errors="coerce")
        if num.notna().sum() >= len(df) * 0.6 or pd.api.types.is_numeric_dtype(s):
            df[col] = num; metric_cols.append(col)
            if had_pct:
                pct_cols.add(col)
        else:
            dim_cols.append(col)
    if date_col is None:  # 兜底：列名不含日期词但内容是日期
        for col in list(dim_cols):
            if pd.api.types.is_numeric_dtype(df[col]):
                continue
            conv = pd.to_datetime(df[col], errors="coerce")
            if conv.notna().sum() >= len(df) * 0.6 and conv.nunique() > 1:
                date_col = col; df[col] = conv; dim_cols.remove(col); break
    return date_col, dim_cols, metric_cols, pct_cols


def pick_main_dim(df, dim_cols):
    cands = [(df[c].nunique(), c) for c in dim_cols if not _is_id_name(str(c)) and df[c].nunique() > 1]
    if cands:
        cands.sort(key=lambda x: -x[0]); return cands[0][1]
    return dim_cols[0] if dim_cols else None


def entity_dims(df, dim_cols):
    """实体分组维度（用于 B/D）：取“会重复出现(非逐行唯一)且非全表恒定”的维度——
    含账户ID 等业务标识，这样每个实体(如每个账户)成一组；都不满足时退回最高基数维度。"""
    cands = [c for c in dim_cols if 1 < df[c].nunique(dropna=False) < len(df)]
    if cands:
        return cands
    md = pick_main_dim(df, dim_cols)
    return [md] if md else []


def entity_label(key, gdims):
    """把 groupby 的键拼成简洁标签（整数型ID去掉多余的 .0）。"""
    if not isinstance(key, tuple):
        key = (key,)
    def s(x):
        try:
            if isinstance(x, float) and float(x).is_integer():
                return str(int(x))
        except (TypeError, ValueError):
            pass
        return str(x)
    return "_".join(s(x) for x in key)


# 角色关键词（智能识别消耗/转化/点击/曝光等；“成本”归为 cpa 而非消耗，计数类列排除）
_ROLE_KW = {
    "cost":       ["消耗", "花费", "spend", "spent", "cost"],
    "conversion": ["转化", "成交", "下单", "注册", "激活", "订单", "conversion", "convert"],
    "click":      ["点击", "click", "tap"],
    "impression": ["展示", "曝光", "展现", "impression", "show", "exposure"],
    "revenue":    ["收入", "营收", "gmv", "revenue", "income", "流水"],
    "cpa":        ["cpa", "转化成本", "获客成本", "单次转化成本", "成本"],
    "ctr":        ["ctr", "点击率"],
    "cvr":        ["cvr", "转化率"],
    "cpc":        ["cpc", "点击单价"],
    "roi":        ["roi", "roas"],
}
_COUNT_HINT = ["数量", "个数", "广告数", "计划数", "素材数", "账户数", "客户数", "帐户数"]


def detect_roles(metric_cols, pct_cols=None):
    """从指标列里智能匹配业务角色，返回 {role: col}。计数类列(广告数量等)不当作 曝光/点击/转化。"""
    pct_cols = pct_cols or set()
    used, roles = set(), {}
    def norm(x): return str(x).lower().strip().replace(" ", "")
    for role, kws in _ROLE_KW.items():
        count_sensitive = role in ("impression", "click", "conversion")
        best = None
        for col in metric_cols:
            if col in used:
                continue
            cn = norm(col)
            if count_sensitive and any(h in str(col) for h in _COUNT_HINT):
                continue
            # 比例类角色优先取百分比列；绝对量角色跳过百分比列
            if role in ("ctr", "cvr", "roi") and col not in pct_cols and "%" not in str(col) and not any(k in cn for k in kws):
                pass
            if any(k in cn for k in [norm(k) for k in kws]):
                # 绝对量角色(cost/conv/click/impression/revenue)不要选到百分比列
                if role in ("cost", "conversion", "click", "impression", "revenue") and col in pct_cols:
                    continue
                best = col; break
        if best is not None:
            roles[role] = best; used.add(best)
    return roles


def html_escape(s):
    return _html.escape(str(s))


def json_dumps(obj):
    return _json.dumps(obj, ensure_ascii=False, default=str)


# ── 浅色高级主题（与模式 A 统一）──────────────────────────────────
PAGE_CSS = r"""
:root{--bg-page:#f3f5f9;--bg-card:#fff;--bg-soft:#f7f9fc;--bg-hover:#eef3ff;--border:#e9ecf2;--border-soft:#f0f2f6;
--text-primary:#1d2433;--text-secondary:#5a6478;--text-dim:#9aa3b2;--accent-blue:#3b6cff;--accent-green:#10b981;
--accent-orange:#f59e0b;--accent-red:#ef4444;--accent-purple:#7c5cff;--accent-cyan:#0ea5b7;
--shadow:0 1px 2px rgba(20,28,48,.04),0 8px 24px rgba(20,28,48,.06);--shadow-sm:0 1px 2px rgba(20,28,48,.05);
--gradient-1:linear-gradient(135deg,#3b6cff 0%,#7c5cff 100%);}
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:-apple-system,BlinkMacSystemFont,"SF Pro Display","Segoe UI",Roboto,"PingFang SC","Microsoft YaHei",sans-serif;
background:var(--bg-page);color:var(--text-primary);line-height:1.6;min-height:100vh;-webkit-font-smoothing:antialiased;}
.container{max-width:1320px;margin:0 auto;padding:24px 28px 60px;}
.header{text-align:center;padding:46px 24px 30px;}
.header h1{font-size:2rem;font-weight:800;background:var(--gradient-1);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-bottom:8px;letter-spacing:-.02em;}
.header .subtitle{color:var(--text-secondary);font-size:.92rem;}
.sidenav{position:fixed;left:18px;top:50%;transform:translateY(-50%);z-index:80;display:flex;flex-direction:column;gap:4px;background:var(--bg-card);border:1px solid var(--border);border-radius:14px;padding:10px 8px;box-shadow:var(--shadow);}
.sidenav a{display:flex;align-items:center;gap:8px;font-size:.82rem;color:var(--text-secondary);text-decoration:none;padding:7px 14px;border-radius:9px;white-space:nowrap;cursor:pointer;transition:.18s;}
.sidenav a .dot{width:6px;height:6px;border-radius:50%;background:var(--border);transition:.18s;}
.sidenav a:hover{background:var(--bg-soft);color:var(--text-primary);}
.sidenav a.active{background:var(--bg-hover);color:var(--accent-blue);font-weight:600;}
.sidenav a.active .dot{background:var(--accent-blue);}
@media(max-width:1180px){.sidenav{display:none;}}
.sec{margin-bottom:26px;scroll-margin-top:20px;}
.sec-head{display:flex;align-items:center;gap:10px;margin-bottom:16px;user-select:none;}
.sec-head .bar{width:4px;height:18px;border-radius:3px;background:var(--gradient-1);}
.sec-head .sec-title{font-size:1.15rem;font-weight:700;}
.sec-head .chev{margin-left:auto;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;width:42px;height:42px;border-radius:10px;border:1px solid var(--border);background:var(--bg-card);box-shadow:var(--shadow-sm);transition:transform .3s,background .2s,color .2s;color:var(--text-secondary);font-size:1.5rem;line-height:1;}
.sec-head .chev:hover{background:var(--bg-hover);color:var(--accent-blue);border-color:var(--accent-blue);}
.sec.sec-collapsed .chev{transform:rotate(-90deg);}
.sec-body{display:grid;grid-template-rows:1fr;transition:grid-template-rows .35s ease;}
.sec.sec-collapsed .sec-body{grid-template-rows:0fr;}
.sec-inner{overflow:hidden;min-height:0;}
.grid{display:grid;gap:16px;}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:16px;}
.card{background:var(--bg-card);border:1px solid var(--border);border-radius:14px;padding:20px;box-shadow:var(--shadow);transition:.2s;}
.card:hover{transform:translateY(-2px);box-shadow:0 10px 28px rgba(20,28,48,.10);}
.card .label{font-size:.78rem;color:var(--text-dim);letter-spacing:.04em;margin-bottom:6px;}
.card .value{font-size:1.6rem;font-weight:800;word-break:break-all;}
.card .sub{font-size:.78rem;color:var(--text-dim);margin-top:4px;}
.card .sub.up{color:var(--accent-green);} .card .sub.down{color:var(--accent-red);}
.info-box{background:var(--bg-card);border:1px solid var(--border);border-radius:12px;padding:15px 18px;margin-bottom:12px;font-size:.88rem;box-shadow:var(--shadow-sm);}
.info-box.red{border-left:4px solid var(--accent-red);} .info-box.yellow{border-left:4px solid var(--accent-orange);}
.info-box.green{border-left:4px solid var(--accent-green);} .info-box.tip{border-left:4px solid var(--accent-purple);}
.pill{display:inline-block;padding:2px 10px;border-radius:20px;font-size:.74rem;font-weight:700;}
.pill.red{background:#fde8e8;color:#c0392b;} .pill.yellow{background:#fef3d7;color:#a26b00;} .pill.green{background:#dcf5ec;color:#0a7a57;}
.table-wrap{background:var(--bg-card);border:1px solid var(--border);border-radius:14px;box-shadow:var(--shadow);overflow:hidden;}
.table-toolbar{display:flex;gap:10px;align-items:center;flex-wrap:wrap;padding:14px 18px;border-bottom:1px solid var(--border);}
.search-box{background:var(--bg-soft);border:1px solid var(--border);border-radius:9px;padding:8px 14px;font-size:.85rem;outline:none;width:230px;color:var(--text-primary);}
.search-box:focus{border-color:var(--accent-blue);background:#fff;}
.seg{display:inline-flex;border:1px solid var(--border);border-radius:9px;overflow:hidden;}
.seg button{background:var(--bg-card);border:none;color:var(--text-secondary);padding:7px 14px;font-size:.8rem;cursor:pointer;}
.seg button.on{background:var(--accent-blue);color:#fff;}
.table-container{overflow-x:auto;}
table.dt{width:100%;border-collapse:collapse;font-size:.82rem;}
table.dt th{background:var(--bg-soft);color:var(--text-secondary);font-weight:700;font-size:.74rem;padding:11px 14px;text-align:left;white-space:nowrap;cursor:pointer;user-select:none;border-bottom:1px solid var(--border);position:sticky;top:0;}
table.dt th:hover{color:var(--accent-blue);}
table.dt td{padding:9px 14px;border-bottom:1px solid var(--border-soft);white-space:nowrap;max-width:280px;overflow:hidden;text-overflow:ellipsis;}
table.dt td.num,table.dt th.num{text-align:right;font-variant-numeric:tabular-nums;}
table.dt tbody tr:hover td{background:var(--bg-hover);}
.pagination{display:flex;justify-content:center;align-items:center;gap:6px;padding:14px;border-top:1px solid var(--border);}
.pagination button{background:var(--bg-card);border:1px solid var(--border);color:var(--text-secondary);padding:6px 12px;border-radius:8px;cursor:pointer;font-size:.82rem;}
.pagination button:hover{border-color:var(--accent-blue);color:var(--accent-blue);}
.pagination button.active{background:var(--accent-blue);border-color:var(--accent-blue);color:#fff;}
.pagination button:disabled{opacity:.4;cursor:not-allowed;}
.chart-card{background:var(--bg-card);border:1px solid var(--border);border-radius:14px;padding:18px 20px;margin-bottom:20px;box-shadow:var(--shadow);}
.chart-head{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:10px;}
.chart-head .ctitle{font-size:1rem;font-weight:700;margin-right:auto;}
.chart-box{width:100%;height:430px;}
.chart2{display:grid;grid-template-columns:1fr 1fr;gap:20px;}
@media(max-width:860px){.chart2{grid-template-columns:1fr;}}
.footer{text-align:center;padding:30px;color:var(--text-dim);font-size:.78rem;}
"""

PAGE_JS = r"""
function toggleSec(h){const s=h.closest('.sec');s.classList.toggle('sec-collapsed');
  if(s.querySelector('.chart-box')&&!s.classList.contains('sec-collapsed'))setTimeout(()=>{window.__charts&&window.__charts.forEach(c=>{try{c.resize()}catch(e){}})},360);}
(function(){const NAV=[...document.querySelectorAll('.sec')].map(s=>[s.id,s.dataset.nav||s.id]);
  const navEl=document.getElementById('sidenav'); if(navEl){navEl.innerHTML=NAV.map(([id,t])=>`<a data-target="${id}"><span class="dot"></span>${t}</a>`).join('');
  document.querySelectorAll('.sidenav a').forEach(a=>a.onclick=()=>{const el=document.getElementById(a.dataset.target);el.classList.remove('sec-collapsed');el.scrollIntoView({behavior:'smooth',block:'start'});});
  function upd(){const off=140;let cur=NAV[0]&&NAV[0][0];for(const[id]of NAV){const el=document.getElementById(id);if(el&&el.getBoundingClientRect().top<=off)cur=id;}
    if(window.innerHeight+window.scrollY>=document.documentElement.scrollHeight-4)cur=NAV[NAV.length-1][0];
    document.querySelectorAll('.sidenav a').forEach(a=>a.classList.toggle('active',a.dataset.target===cur));}
  window.addEventListener('scroll',upd,{passive:true});upd();}
  window.__charts=[];window.addEventListener('resize',()=>window.__charts.forEach(c=>{try{c.resize()}catch(e){}}));})();
"""

# ECharts 浅色主题常量（供各模式图表统一配色）
EC_THEME = {"text": "#5a6478", "sub": "#9aa3b2", "axis": "#e3e7ef", "split": "#eef1f6",
            "tipBg": "#ffffff", "tipText": "#1d2433", "tipBorder": "#e9ecf2"}
CHART_COLORS = ['#3b6cff', '#10b981', '#f59e0b', '#ef4444', '#7c5cff', '#0ea5b7', '#ec4899', '#06b6d4', '#84cc16', '#f97316']


def render_page(title, subtitle, sections, body_scripts=""):
    """生成浅色主题整页 HTML。
    sections: [{"id":..., "nav":..., "title":..., "html":...}, ...]
    body_scripts: 追加在末尾的 <script> 内容（各模式的图表初始化）。
    """
    secs = []
    for s in sections:
        secs.append(
            f'<div class="sec" id="{s["id"]}" data-nav="{html_escape(s.get("nav", s["title"]))}">'
            f'<div class="sec-head"><span class="bar"></span><span class="sec-title">{html_escape(s["title"])}</span>'
            f'<span class="chev" onclick="toggleSec(this)" title="展开/收起">▾</span></div>'
            f'<div class="sec-body"><div class="sec-inner">{s["html"]}</div></div></div>'
        )
    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_escape(title)}</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/echarts/5.5.0/echarts.min.js"></script>
<style>{PAGE_CSS}</style></head><body>
<nav class="sidenav" id="sidenav"></nav>
<div class="header"><h1>{html_escape(title)}</h1><p class="subtitle">{html_escape(subtitle)}</p></div>
<div class="container">{''.join(secs)}</div>
<div class="footer">Generated by data-auto-analyzer · 数据本地处理</div>
<script>{PAGE_JS}</script>
<script>{body_scripts}</script>
</body></html>"""
