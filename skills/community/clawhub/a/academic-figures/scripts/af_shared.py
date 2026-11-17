# -*- coding: utf-8 -*-
"""af_shared — 生成器与主流程共享的底层工具（v4.0.0 模块化第四刀）。

叶模块：不依赖 gen_figure/af_draw，被两者共同导入。
"""
import json
import os
import re
import sys

from matplotlib.transforms import BboxBase  # v4.5 P0-1：_ensure_ylabel_clear 依赖（缺失致 KM-ylabel/dual_axis/composite 硬崩溃）

_STYLE_NO_GRID = [False]  # v3.3 --style nature-clean：图型级网格关闭开关
_SKETCH_MODE = [False]    # v7.6 --style sketch：手绘模式全局旗标（数值黑粗/标签不旋转/皇冠立体）

# v3.0.0 模块化：wizard 与异常诊断系统拆至独立模块（原名在此命名空间可用）
from af_wizard import _run_wizard
from af_diagnostics import (_EXIT_DATA_CLASSES, _EXIT_ENV_CLASSES,
                            _classify_exit_code, _diagnose_exception,
                            _print_v3_error, _EXC_ZH_V3, _DIAG_PATTERNS,
                            _KNOWN_DATA_FIELDS)

try:
    import af_v23_stats as _afstats
    import af_v23_charts as _afcharts
except ImportError:  # v2.3 新图型/统计模块不在同目录时降级
    _afstats = None
    _afcharts = None

HATCH_PATTERNS = ['//', '\\\\', '||', '--', '++', 'xx', '..', 'oo', '**', 'oo']

def has_cjk(text):
    """Check if text contains CJK characters (incl. supplementary-plane ideographs)."""
    if not text:
        return False
    for ch in str(text):
        o = ord(ch)
        if 0x4e00 <= o <= 0x9fff or 0x3400 <= o <= 0x4dbf:  # BMP: CJK Unified + Ext-A
            return True
        if 0x3000 <= o <= 0x303f or 0xff00 <= o <= 0xffef:  # CJK 标点 + 全角形式（（）：等）
            return True
        if 0x20000 <= o <= 0x2ebef:  # Ext-B..F (rare, but real ideographs)
            return True
        if 0x30000 <= o <= 0x3134f:  # Ext-G
            return True
    return False


# v7.9.0 AF3：CJK 探测脚本路径（与 af_shared 同目录；gen_figure 委托本模块加载）
DETECT_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "detect_cjk_font.py")


def load_cjk_font(font_path=None):
    """Load CJK font. Returns (FontProperties, font_name) or (None, None).

    v7.9.0 AF3：探测链重构——进程内加载探测模块优先（agent 嵌套/嵌入式解释器场景
    sys.executable 可能为空串，旧 subprocess 路径失败曾被 except 静默吞掉→rc=0 中文
    全豆腐块）；进程内失败再回退子进程（sys.executable 非空 → python3）。"""
    if font_path is None:
        try:
            import importlib.util as _ilu
            _sp = _ilu.spec_from_file_location("af_detect_cjk", DETECT_SCRIPT)
            _md = _ilu.module_from_spec(_sp)
            _sp.loader.exec_module(_md)
            font_path = _md.detect_cjk_font()
        except Exception:
            font_path = None
        if not font_path:
            import subprocess
            for _py in ([sys.executable] if sys.executable else []) + ["python3"]:
                try:
                    _r = subprocess.run([_py, DETECT_SCRIPT], capture_output=True,
                                        text=True, timeout=10)
                    _i = json.loads(_r.stdout)
                    font_path = _i.get("path") if _i.get("found") else None
                    if font_path:
                        break
                except Exception:
                    continue
    if font_path and os.path.exists(font_path):
        from matplotlib import font_manager as _fm
        _fm.fontManager.addfont(font_path)
        fp = _fm.FontProperties(fname=font_path)
        return fp, fp.get_name()
    return None, None


def advise_colorblind(theme, n_series, stream=None):
    """v7.9.0 AF29：非色盲安全主题×≥3 系列时 stderr 一行提示（默认主题 glm-brand
    为品牌钦定不动，仅提示不强制；色盲安全场景建议 --theme okabe-ito）。永不抛异常。"""
    try:
        if n_series is not None and n_series >= 3 and not theme.get("colorblind_safe"):
            print("NOTICE: 当前主题未按色盲安全设计（红绿对/相近明度在 3+ 系列下风险升高）——"
                  "投稿或色盲读者场景建议 --theme okabe-ito", file=stream or sys.stderr)
    except Exception:
        pass


def cell_text_color(bg):
    """v7.9.1 AF32/AF38：按底色选黑/白文字（WCAG 对比度判据，单一真源）。

    bg 接受 hex 字符串（"#RRGGBB"）或 0~1 (r, g, b[, a]) 元组；返回 "#000000"
    或 "#ffffff"。判据=相对亮度（WCAG 2.x 线性化），选对比度更高的一侧——
    heatmap 格内数值（按格底色而非数值阈值）与 diagram 块内文字共用。"""
    try:
        if isinstance(bg, str):
            bg = bg.strip()
            if bg.startswith("#") and len(bg) >= 7:
                bg = tuple(int(bg[i:i + 2], 16) / 255.0 for i in (1, 3, 5))
            else:
                return "#000000"
        r, g, b = (float(v) for v in bg[:3])

        def _lin(c):
            return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
        lum = 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)
        # 对白文字对比度 = (1.05)/(lum+0.05)；对黑文字 = (lum+0.05)/0.05
        return "#ffffff" if (1.05 / (lum + 0.05)) >= ((lum + 0.05) / 0.05) else "#000000"
    except Exception:
        return "#000000"


_HEX_RE = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")


def parse_palette(spec):
    """v7.9.1 G1：--palette 外部配色注入解析——逗号/分号分隔的 hex 序列
    （"#C1121F,#669BBC,..."，3~6 位 hex 均可）。非法即抛 ValueError（exit 3）。
    分类图=按序替换主题色；heatmap=构建连续色阶（浅端对齐低值=按给定顺序）。"""
    if not spec or not str(spec).strip():
        raise ValueError("palette: 需要 hex 序列（如 \"#C1121F,#669BBC,#003049\"）")
    out = []
    for tok in re.split(r"[,;]", str(spec)):
        t = tok.strip()
        if not t:
            continue
        if not _HEX_RE.match(t):
            raise ValueError(f"palette: 非法颜色 '{t}'——请给 #RRGGBB 或 #RGB hex")
        out.append(t if len(t) == 7 else "#" + "".join(c * 2 for c in t[1:]))
    if len(out) < 2:
        raise ValueError("palette: 至少 2 个颜色（分类系列或色阶两端）")
    return out



def _ensure_ylabel_clear(ax, fig=None, max_pad=24.0):
    """Mechanism-level: auto-increase y-label labelpad until it clears tick labels.

    Rotated (90°) y-axis titles -- especially long CJK+English mixes like
    "最高研发阶段 (max phase)" -- can collide with the top/bottom tick labels
    even when tick-vs-tick overlaps are handled. Measures real rendered
    bounding boxes; only grows the pad when a collision exists, so figures
    that already look right are left untouched.
    """
    fig = fig or ax.figure
    label = ax.yaxis.get_label()
    if not label.get_text().strip():
        return
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    label_bb = label.get_window_extent(renderer)
    tick_bbs = [t.get_window_extent(renderer) for t in ax.get_yticklabels()
                if t.get_text().strip() and t.get_visible()]
    if not tick_bbs:
        return
    cur = ax.yaxis.labelpad

    def collides():
        for tb in tick_bbs:
            inter = BboxBase.intersection(label_bb, tb)
            if inter is not None and inter.width > 0 and inter.height > 0:
                return True
        return False

    while collides() and cur <= max_pad:
        cur += 1.0
        ax.yaxis.labelpad = cur
        fig.canvas.draw()
        label_bb = label.get_window_extent(renderer)
    if collides():
        # Pad exhausted: shrink the label font as a last resort.
        label.set_fontsize(max(5, label.get_fontsize() - 1))
        fig.canvas.draw()
        print(f"WARNING: y-label '{label.get_text()[:20]}...' still near ticks "
              f"after pad={cur:.0f}, font shrunk", file=sys.stderr)



# ── v5.6 自 gen_figure.py 迁入的纯数据表（编排逻辑留主文件，行预算纪律） ──

_INLINE_DATA_RE = re.compile(r"^\s*[^=,]+=[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?(\s*,\s*[^=,]+=[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)*\s*$")


def parse_inline_data(path):
    """v7.7.2 AF1：--data inline 简写 "A=10,B=8,C=5" → 单系列 bar 数据 dict。

    规则收紧=整体匹配「名称=数值(,名称=数值)*」才当 inline（数值=严格十进制/
    科学计数，正则字符类不含点号乱序），不匹配返回 None（调用方走原文件路径，
    坏文件名的原报错保持不变）。系列名固定 value；int/float/负数/中文名均可。
    """
    if not _INLINE_DATA_RE.match(path.strip()):
        return None
    labels, values = [], []
    for _item in path.strip().split(","):
        _k, _v = _item.split("=", 1)
        labels.append(_k.strip())
        values.append(float(_v))
    return {"labels": labels, "series": {"value": values}}


def fmt_ratio_ci(est, lo, hi, measure="RR"):
    """v7.8.1 AF11：效应量 CI 自适应格式化（临床判读保护门）。

    比值类（RR/OR/HR）无效值=1；CI 边界舍入到 2 位若恰成 1.00，读者会把
    「上界 0.997=CI 不含 1=显著」误读成「含 1=不显著」（Fleiss93 实锤：RR
    上界 0.997 被印成 1.00，与引擎自身结论相反）。连续类（MD/SMD/RD）无效
    值=0，round==0.00 同理升位。规则：任一边界 round(·,2)==无效值且本身不
    等于无效值 → 三位小数；否则维持两位。第 4 元=CI 是否不含无效值（显著）。
    返回 (est_s, lo_s, hi_s, sig)。
    """
    null_v = 0.0 if str(measure).upper() in ("MD", "SMD", "RD") else 1.0
    dec = 2
    for v in (lo, hi):
        if round(v, 2) == null_v and abs(v - null_v) >= 1e-12:
            dec = 3
    sig = (lo > null_v + 1e-12) or (hi < null_v - 1e-12)
    return (f"{est:.{dec}f}", f"{lo:.{dec}f}", f"{hi:.{dec}f}", sig)


def hero_panel_mode(data, panels):
    """v7.8.0 composite hero 模式判定：返回 (ok, idx)。

    合法 = hero_panel 为 0 起始整数面板序号且在界内，且面板数 3-6（hero 规格）。
    非法/缺省返回 (False, None)——调用方回退均等网格（af_draw 打 WARNING，validate 跳过占位检测）。
    """
    hp = data.get("hero_panel")
    if isinstance(hp, int) and not isinstance(hp, bool) \
            and 0 <= hp < len(panels) and 3 <= len(panels) <= 6:
        return True, hp
    return False, (hp if isinstance(hp, int) and not isinstance(hp, bool) else None)


CHART_NOTES = {
    "bar": "bar/hbar: JSON 或 CSV 均可；CSV 首列为 X 标签；labels+datasets/series+可选 significance 显著性列。inline 简写：-d \"A=10,B=8\" 免文件（单系列）。误差棒：JSON errors 字段，或 CSV 后缀列（weight_sd/weight_se 等 v6.0+ 自动配对）。单系列竖向 bar 默认竞技场风格（冠军=最高柱；负面指标 --arena off）；基准榜单场景推荐 --style sketch 手绘风。--hatch 斜纹适合打印/黑白场景。",
    "grouped_bar": "同 bar（labels 类别+datasets/series 多系列自动分组，可选 errors 误差棒/significance 列）；--show-ratio 显示比值标注。",
    "hbar": "同 bar（horizontal）；labels+datasets/series（可选 errors 误差棒）。标签过长时 horizontal 模式更合适。",
    "stacked_bar": "stacked_bar: 构成比堆叠；JSON percentage=true 归一化为 100%，show_total 显示合计柱；CSV 每列为一个 series。",
    "heatmap": "heatmap: JSON matrix 必填+row_labels/col_labels（行列标签）+cbar_label（色标标题）；--cmap/--vmin/--vmax/--annot/--cell-edge/--discrete；大矩阵建议 PNG/SVG。",
    "scatter": "scatter: JSON 或 CSV；groups 字段区分颜色；--no-trend 关闭趋势线。",
    "line": "line: JSON series 或多列 CSV；x 轴标签 JSON labels 或 CSV 首列；series 可带 errors 误差带。",
    "dual_axis": "dual_axis: 需要 JSON 含 left/right 两个 series 定义；CSV 不支持双轴。",
    "box": "box: 箱线图；CSV 每列一分布，或 JSON datasets/series={组名: 数值数组}+labels 组名列表。",
    "forest": "forest: meta 分析森林图；JSON estimates/ci_low/ci_high 必填，可选 weights/overall/heterogeneity/events。",
    "km": "km: Kaplan-Meier；groups={组名:[[时间,事件0/1],...]} 患者级原始数据（≥2 组自动 log-rank+风险表+中位生存）或 {组名:[[时间,生存率],...]} 预计算曲线（此形态跳过自动统计并提示）；可选 log_rank={\"p\":...}/risk_table/median_survival 直接提供。",
    "roc": "roc: ROC 曲线；JSON 需 scores/labels（可多曲线），diagonal=对角参照线，AUC 自动标注。",
    "violin": "violin: 小提琴图；JSON datasets/series={组名: 数值数组}+labels 组名列表，或 CSV 每列一分布。",
    "composite": "composite: 多面板组合图；JSON panels 数组（每面板 type+data，可选 layout/span/pos/hero_panel 主面板索引/panel_labels），参考文档 §组合图。",
    "diagram": "diagram: 架构/流程图（CONSORT 式）；JSON blocks [{id,label,x,y,w,h,color,sublabel}]+arrows、background=light。",
    "flow": "flow: 语义流程图（v8.0.0，第 42 号图型）——只给语义不给坐标：nodes=[{id,label,sublabel,color,shape}]+edges=[{from,to,label,dashed,color}]、layout=chain|layered、direction=TB|LR、groups/annotations 可选；引擎自动布局+磁吸逐段箭头+回边 lane 绕行+标签避让+文本自适应+画布裁剪；--gate strict=三层 bbox 断言（违规 exit 2）。",
    "prisma": "prisma: PRISMA 2020 系统综述流程图；JSON 需 records_identified/studies_included，"
              "数字自洽性自动校验（对不上报 ERROR 拒绝出图）；lang=zh 输出中文标准版；"
              "参考文档 §PRISMA 流程图。",
    "funnel": "funnel: Meta 漏斗图；JSON studies（每项 name/effect/se，效应建议 log 尺度）；"
              "自动 DL 随机效应合并线+95% 伪置信漏斗；--egger 加不对称回归线（<5 研究警告）。",
    "bland_altman": "bland_altman: 一致性分析；JSON methods 恰好两项系列或 a/b 数组；"
                    "自动均值差线与 ±1.96SD 一致性界线。",
    "pca": "pca: PCA 得分图；JSON matrix（行=样本 列=特征），可选 groups（分组椭圆±2SD）与 "
           "feature_names（载荷箭头 top5）；默认标准化（相关矩阵），列上限 200。",
    "paired": "paired: 配对前后图；JSON before/after 或 series 恰好两项（等长）；"
              "--stats auto 加配对检验（配对 t / Wilcoxon 符号秩）括号星号。",
    "venn": "venn: 韦恩图（2~4 集合；4 集合为椭圆布局 v2.8）；JSON sets 为元素列表（自动求交并）或全部区域计数；"
            "默认等圆示意、区域数字精确；--area 按计数比例绘制（Euler，2 集合解析解/"
            "3 集合最优拟合）。",
    "cluster_heatmap": "cluster_heatmap: 聚类热图；数据格式同 heatmap（matrix），行列按 Ward 层次"
                       "聚类重排（顺序写入 stderr/alt）；行数上限 3000；v2.3 暂不含树状图面板。",
    "upset": "upset: UpSet 交集图（≥5 集合推荐，venn 2~4 集合的标准后继；组学多基因集/"
             "多标签共现）；JSON sets 为元素列表（自动求交并）；top_n 展示前 N 个交集"
             "（默认 12，取 1~50）、sort=size|degree、min_size 过滤小交集；标题放 JSON "
             "title 字段；未展示交集只计入 stderr 事实行。",
    "raincloud": "raincloud: 雨云图（v4.9，第 27 号图型；分布三合一：KDE 半小提琴云+箱线五数概括+"
                 "抖动原始点雨）；schema 同 violin；--stats 通用；jitter(0~0.3)/cloud_scale(0~2.0，0=藏云)；零方差/单点组云退化并告知。",
    "slope": "slope: 斜率图（两时点/两组对比）；JSON items={名称:[前值,后值]}+left_label/right_label；--show-gap 标差值。",
    "volcano": "volcano: 火山图；JSON log2fc+pvalue 两数组必填（names/fc_cut/p_cut/top 可选）；阈值线与 top 基因标注自动；轴标默认组学口径（log2 fold change / -log10 p-value），其他数据域可用 --xlabel/--ylabel 覆盖。",
    "rmst": "rmst: RMST 限制平均生存时间；JSON groups={臂名: [[时间,事件 0/1]...]} 恰好两臂（契约同 km）+time_unit 时间单位；--rmst-tau 指定 τ（缺省=最小最大随访之半，与 stderr 披露一致）；自动输出每臂 RMST(95%CI)+ΔRMST。",
    "labbe": "labbe: L'Abbé 图（Meta 四件套）；JSON studies=[{name,events_t,n_t,events_c,n_c}...]（2x2 四格，非 trials）；est_measure=RR/OR；气泡面积∝研究权重；合并线=DL 随机效应。",
    "dumbbell": "dumbbell: 哑铃图（v5.1，第 30 号图型；每行两点 from→to+连接线，横向形态，"
                 "强调逐条目差距）；JSON from/to 必填等长、labels 可选、from_label/to_label 图例名；"
                 "sort=gap|input|to；show_values/show_gap 可选；严格两时点，>2 用 slope/line。",
    "calibration": "calibration: 校准曲线（v5.2，第 31 号图型；临床预测模型三件套之一，与 ROC/DCA 同生态）；"
                   "JSON bins=[{predicted,observed,n?,ci_lo?,ci_hi?}] 或 predicted/observed 平行数组；"
                   "hl_p 标注 Hosmer-Lemeshow p；smooth=true 插值参考线；等比坐标+理想对角线。",
    "dca": "dca: 决策曲线分析（v5.2，第 32 号图型；净收益 vs 阈值概率）；JSON thresholds 严格升序"
           "(0,1)+models=[{name,net_benefit}]（1~6 个）；prevalence 画理论全部干预线或 treat_all "
           "显式数组；show_none 默认画不干预 0 线；净收益定义 Vickers。",
    "nomogram": "nomogram: 列线图（v5.3，第 33 号图型；预测模型查表尺：变量计分→Total Points→结局概率）；"
                "JSON variables=[{name,ticks[2~12],labels?,points_at?}]（points_at 缺省线性 0~100）+outcome_scales="
                "[{label,ticks,points_at}]（1~3，总积分口径）；total_points_max 可选；引擎只可视化不拟合，"
                "points 请来自已拟合模型（R rms::nomogram 等）。",
    "rcs": "rcs: 限制性立方样条/非线性剂量反应曲线（v5.4，第 34 号图型）；JSON points=[{value,est,ci_lo,ci_hi}]"
           "（≥5 网格点，来自已拟合样条模型，引擎不拟合）；ref 参照值、log_y 默认对数轴（HR/OR）、"
           "hline_at 覆盖参照水平、hist=false 关底部 rug；曲线偏离参照水平=存在非线性关联。",
    "subgroup": "subgroup: 亚组分析森林图（v5.5，第 35 号图型；各层效应+P 交互一图呈现）；"
                "JSON subgroups=[{name,p_interaction?,levels=[{name,est,ci_low,ci_high,n?,p?}]}]"
                "（1~12 组×2~8 层）+overall 可选（底部菱形）；est_label 定无效线（HR/OR/RR=1，MD/SMD=0）；"
                "log_x 默认 true；引擎只可视化不拟合。",
    "ridgeline": "ridgeline: 山脊图/joyplot（v5.0，第 29 号图型；多组 KDE 密度纵向堆叠部分重叠，"
                 "一屏看分布逐组移动/变形）；JSON: {\"labels\": [组名自上而下], \"datasets\": "
                 "{组名: [数值数组]}}（datasets=组名→数组的字典，与 violin 系列字典同构）；"
                 "overlap(0~0.95) 调重叠、sort=median 按中位数排；单值组退化为标记线并告知。",
    "swimmer": "swimmer: 游泳图（v4.10，第 28 号图型；临床试验逐例时长）；JSON end 必填（>0，单位自定）、"
               "start/names/group 可选（RECIST 类别着色同 waterfall）、milestones 里程碑圆点（可晚于条端）、"
               "ongoing 端部箭头（持续中）、ref_lines 地标虚线；sort=duration|input。",
    "waterfall": "waterfall: 肿瘤缓解瀑布图（v4.8，第 26 号图型；每例自基线最佳变化%）；"
                 "JSON change 必填（缩小为负）、names/group 可选（RECIST 类别着色+图例）、"
                 "pr_cut=-30/pd_cut=20 阈值虚线、sort=desc|input；--show-values 柱端数值；"
                 "着色未给 group 时按阈值分桶（缓解蓝/稳定灰/进展橙）。",
    "galbraith": "galbraith: Galbraith 径向图（Meta 异质性，漏斗图姊妹图）；JSON 同 funnel（studies name/effect/se，效应取 log 值）；est_label=OR/HR/RR 默认画效应量弧线，MD/SMD 自动关；stderr 报固定效应 b/DL 合并/I²/离群名单。",
    "rob": "rob: 偏倚风险交通灯图（v6.1，第 39 号图型；robvis 同款）；JSON 需 studies=[{name, judgements:{域: 判定}}]（2~50 项，判定 Low/Some concerns/High/No information 中英均可），domains 可选（缺省取自首研究键序），weights 可选各域摘要权重；Overall 列只入网格不入摘要；stderr 报各域加权占比。真实示例 examples/realworld/evidence_rob2_metformin.json。",
    "cif": "cif: 竞争风险累计发生率（Aalen-Johansen）；JSON 需 time+event 两等长数组（0=删失 1=目标事件 ≥2=竞争事件编号），cause_labels 命名各因、time_unit 时间单位；compare_km（auto=有竞争事件才画）叠加 1−KM 高估对照虚线，percent 百分轴；多臂分组请用 -t km。",
}


DEMO_DATA = {
    "bar": {"labels": ["TNF抑制剂", "IL-6抑制剂", "JAK抑制剂", "IL-1抑制剂", "CTLA-4融合"], "series": {"应答率(%)": [62, 55, 48, 40, 35], "缓解率(%)": [28, 22, 20, 15, 10]}},
    "hbar": {"labels": ["TNF抑制剂", "IL-6抑制剂", "JAK抑制剂", "IL-1抑制剂", "CTLA-4融合"], "series": {"ACR50应答率(%)": [62, 55, 48, 40, 35]}},
    "stacked_bar": {"labels": ["队列A", "队列B", "队列C"], "percentage": True, "series": {"缓解": [45, 38, 30], "部分缓解": [25, 30, 28], "无缓解": [30, 32, 42]}},
    "heatmap": {"rows": ["IL-6", "TNF-α", "CRP", "ESR"], "cols": ["IL-6", "TNF-α", "CRP", "ESR"],
                "matrix": [[1.0, 0.72, 0.85, 0.68], [0.72, 1.0, 0.65, 0.60], [0.85, 0.65, 1.0, 0.75], [0.68, 0.60, 0.75, 1.0]]},
    "line": {"labels": ["0周", "4周", "8周", "12周", "16周"], "series": {"TNF抑制剂": [5.8, 4.2, 3.5, 3.0, 2.6], "联合治疗": [5.9, 3.8, 2.8, 2.2, 1.8]}},
    "scatter": {"x": [2, 4, 8, 12, 16, 20, 24, 28], "y": [45, 38, 28, 22, 18, 15, 12, 10], "groups": ["应答者"] * 4 + ["非应答者"] * 4},
    "forest": {"labels": ["Smith 2023", "Tanaka 2023", "Brown 2022", "王明 2024"], "estimates": [0.72, 0.80, 0.75, 0.65], "ci_low": [0.55, 0.62, 0.56, 0.48], "ci_high": [0.94, 1.03, 1.00, 0.84], "overall": {"estimate": 0.73, "ci_low": 0.6, "ci_high": 0.88}},
    "km": {"groups": {"治疗组": [[0, 1], [6, 0.8], [12, 0.7], [18, 0.6], [24, 0.55]], "对照组": [[0, 1], [6, 0.9], [12, 0.75], [18, 0.6], [24, 0.45]]}, "log_rank": {"p": 0.03}},
    "roc": {"curves": [{"fpr": [0.0, 0.1, 0.2, 0.4, 0.6, 1.0], "tpr": [0.0, 0.6, 0.8, 0.9, 0.95, 1.0], "label": "模型A", "auc": 0.92}, {"fpr": [0.0, 0.2, 0.4, 0.6, 0.8, 1.0], "tpr": [0.0, 0.4, 0.6, 0.75, 0.85, 1.0], "label": "模型B", "auc": 0.85}]},
    "violin": {"datasets": {"组A": [1.2, 2.3, 2.1, 3.0, 2.8, 3.5], "组B": [2.0, 2.4, 3.1, 3.8, 4.2, 4.0], "组C": [3.0, 3.2, 3.8, 4.5, 4.8, 5.2]}},
    "box": {"datasets": {"组A": [1.2, 2.3, 2.1, 3.0, 2.8, 3.5], "组B": [2.0, 2.4, 3.1, 3.8, 4.2, 4.0]}},
    "slope": {"left_label": "基线", "right_label": "12 周", "items": {"药物A": [72, 85], "药物B": [65, 61], "对照": [70, 71]}},
    "volcano": {"log2fc": [-2.3, -1.4, -1.1, -0.4, 0.2, 0.6, 1.2, 1.6, 2.4], "pvalue": [3e-4, 0.012, 0.04, 0.5, 0.8, 0.3, 0.02, 3e-5, 8e-7], "names": ["SLC6A4", "MAOA", "FKBP5", "NR3C1", "CRH", "AVP", "BDNF", "COMT", "HTR1A"]},
    "raincloud": {"labels": ["活动期", "低活动", "对照"], "datasets": {"活动期": [12.1, 14.2, 15.8, 13.4, 16.1, 12.9, 14.8, 13.9], "低活动": [6.2, 7.1, 5.8, 6.9, 7.5, 6.4, 5.5, 7.0], "对照": [3.1, 2.8, 3.5, 3.0, 2.6, 3.3, 3.2, 2.9]}},
    "upset": {"title": "五组学平台差异基因交集", "sets": {
        "转录组": ["TP53", "KRAS", "EGFR", "BRCA1", "MYC", "PTEN", "NRAS", "PIK3CA", "ALK"], "蛋白组": ["TP53", "EGFR", "MYC", "AKT1", "KRAS", "ERBB2", "PTEN"],
        "甲基化": ["TP53", "BRCA1", "CDKN2A", "MGMT", "PTEN", "RB1"], "eQTL": ["KRAS", "PIK3CA", "PTEN", "AKT1", "MAP2K1", "EGFR"], "GWAS": ["TP53", "BRCA1", "ERBB2", "ATM", "CHEK2", "PALB2"]}},
    "dumbbell": {"labels": ["中心A", "中心B", "中心C", "中心D", "中心E", "中心F"], "from": [32, 41, 28, 45, 38, 24], "to": [58, 63, 49, 66, 60, 47], "from_label": "基线", "to_label": "12周", "show_gap": True},
    "calibration": {"predicted": [0.06, 0.14, 0.24, 0.35, 0.47, 0.58, 0.71, 0.85], "observed": [0.08, 0.11, 0.28, 0.33, 0.51, 0.55, 0.76, 0.81],
                    "ci_lo": [0.02, 0.05, 0.19, 0.24, 0.40, 0.43, 0.63, 0.67], "ci_hi": [0.19, 0.21, 0.40, 0.45, 0.62, 0.67, 0.86, 0.90], "n": [58, 64, 71, 77, 69, 61, 52, 38], "hl_p": 0.42},
    "dca": {"thresholds": [0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85],
            "models": [{"name": "模型A+年龄", "net_benefit": [0.152, 0.133, 0.124, 0.112, 0.095, 0.073, 0.048, 0.022, -0.001]},
                       {"name": "模型B", "net_benefit": [0.148, 0.126, 0.110, 0.093, 0.072, 0.050, 0.027, 0.006, -0.011]}],
            "prevalence": 0.18},
    "nomogram": {"variables": [
        {"name": "年龄（岁）", "ticks": [40, 50, 60, 70, 80]}, {"name": "肿瘤大小（cm）", "ticks": [1, 2, 3, 5, 8], "points_at": [0, 25, 45, 70, 100]},
        {"name": "分化程度", "ticks": ["高", "中", "低"], "points_at": [0, 35, 100]}, {"name": "淋巴结转移", "ticks": ["无", "有"], "points_at": [0, 60]}],
        "outcome_scales": [
        {"label": "3 年无病生存", "ticks": [0.9, 0.7, 0.5, 0.3], "points_at": [55, 120, 190, 260]},
        {"label": "5 年无病生存", "ticks": [0.9, 0.7, 0.5, 0.3], "points_at": [45, 100, 160, 230]}],
        "total_points_max": 320},
    "rcs": {"points": [{"value": 40, "est": 1.02, "ci_lo": 0.72, "ci_hi": 1.45}, {"value": 45, "est": 0.94, "ci_lo": 0.74, "ci_hi": 1.19}, {"value": 50, "est": 0.88, "ci_lo": 0.76, "ci_hi": 1.02}, {"value": 55, "est": 1.05, "ci_lo": 0.93, "ci_hi": 1.19}, {"value": 60, "est": 1.38, "ci_lo": 1.15, "ci_hi": 1.66}, {"value": 65, "est": 1.79, "ci_lo": 1.36, "ci_hi": 2.36}],
            "ref": 50, "x_label": "年龄（岁）", "y_label": "HR（对数轴）"},
    "subgroup": {"subgroups": [
        {"name": "年龄", "p_interaction": 0.48, "levels": [
            {"name": "<65 岁", "n": 120, "est": 0.72, "ci_low": 0.55, "ci_high": 0.94, "p": 0.015}, {"name": "≥65 岁", "n": 98, "est": 0.81, "ci_low": 0.58, "ci_high": 1.13, "p": 0.22}]},
        {"name": "性别", "p_interaction": 0.71, "levels": [
            {"name": "男", "n": 126, "est": 0.69, "ci_low": 0.52, "ci_high": 0.91, "p": 0.008}, {"name": "女", "n": 92, "est": 0.84, "ci_low": 0.60, "ci_high": 1.18, "p": 0.32}]},
        {"name": "PD-L1 表达", "p_interaction": 0.03, "levels": [
            {"name": "TPS≥50%", "n": 84, "est": 0.55, "ci_low": 0.39, "ci_high": 0.78, "p": 0.001}, {"name": "TPS<50%", "n": 134, "est": 0.86, "ci_low": 0.67, "ci_high": 1.10, "p": 0.23}]}],
        "overall": {"n": 218, "est": 0.75, "ci_low": 0.61, "ci_high": 0.92, "p": 0.007}, "est_label": "HR", "x_label": "PFS HR（免疫治疗 vs 化疗）"},
    "ridgeline": {"labels": ["基线", "4周", "8周", "12周"], "overlap": 0.55,
                  "datasets": {"基线": [42, 48, 52, 55, 58, 60, 63, 65, 68, 72, 78, 85, 42, 50, 56, 61, 66, 70, 74, 80], "4周": [28, 33, 38, 41, 45, 48, 52, 55, 58, 62, 68, 30, 36, 43, 49, 54, 60, 65], "8周": [18, 22, 26, 30, 33, 37, 41, 45, 49, 54, 20, 25, 31, 39, 47, 52], "12周": [12, 15, 19, 23, 27, 31, 36, 41, 46, 14, 18, 24, 33, 43]}},
    "waterfall": {"change": [-72.4, -65.1, -58.9, -52.0, -41.8, -32.1, -24.5, -15.2, -8.9, -3.4, 0.8, 12.6, 25.3, 41.7, 52.0],
                   "names": [f"P{i:03d}" for i in range(1, 16)],
                   "group": ["PR", "CR", "PR", "PR", "PR", "PR", "SD", "SD", "SD", "SD", "SD", "SD", "PD", "PD", "PD"]},
    "swimmer": {"end": [38.9, 34.2, 30.5, 26.1, 22.4, 18.7, 15.9, 12.3, 9.8, 6.4, 4.1, 2.2],
                "names": [f"P{i:03d}" for i in range(1, 13)],
                "group": ["CR", "CR", "PR", "PR", "PR", "PR", "SD", "SD", "SD", "PD", "PD", "PD"],
                "milestones": [[8.2], [9.5], [6.1], [7.0], [10.2], [], [5.5], [], [], [], [], []], "ongoing": [True, True, True, False, True, False, False, False, False, False, False, False], "ref_lines": [12, 24]},
    "dual_axis": {"labels": ["0周", "4周", "8周", "12周"], "left": {"DAS28": [5.8, 4.2, 3.5, 3.0]}, "right": {"CRP(mg/L)": [42, 30, 22, 16]}},
    "flow": {"layout": "chain", "nodes": [{"id": "A", "label": "纳入", "sublabel": "n=240", "color": "#2E5E8F"}, {"id": "B", "label": "随机分组", "sublabel": "1:1", "color": "#FFB627"}, {"id": "C", "label": "干预", "sublabel": "12 周", "color": "#6BA776"}, {"id": "D", "label": "随访", "sublabel": "48 周", "color": "#5BA0A0"}], "edges": [{"from": "A", "to": "B"}, {"from": "B", "to": "C", "label": "ITT"}, {"from": "C", "to": "D"}, {"from": "D", "to": "B", "label": "脱落再入组", "dashed": True}]},
    "prisma": {"records_identified": 128, "duplicates_removed": 23, "records_excluded": 61, "reports_not_retrieved": 3, "exclusion_reasons": {"人群不符": 5, "干预不符": 7, "数据不可用": 4}, "studies_included": 25},
}


# ── v6.7.0：旗标域注册表（--list-flags 数据源；与 limits.md 冲突表同源对齐） ──
# 域内=旗标对该图型生效；域外=传了会被 [ignored] 显式告知或拒绝（见 limits §〇/§二）。
def add_sig_auto_arg(parser):
    """
    v7.0.0：--sig-auto 注册（两两全自动检验+bracket；封装在 af_shared 同 sig-bracket）。
    """
    parser.add_argument("--sig-auto", action="store_true",
                        help="全自动组间显著性（box/violin/raincloud）：自动两两检验（Shapiro 判常态 → Welch t / Mann-Whitney U）并画分层 bracket；bar 等聚合图请用 comparisons + --sig-bracket")

def add_sig_bracket_arg(parser):
    """
    v6.9.0：--sig-bracket 旗标注册（封装在 af_shared，gen_figure 行预算零压力）。
    """
    parser.add_argument("--sig-bracket", action="store_true",
                        help="组间显著性括号（bar/grouped_bar/box/violin）：数据携带 comparisons=[{a,b,p}] 时自动画分层 bracket+星号")

_FLAG_DOMAINS = {
    "--stats": (("box", "violin", "raincloud", "forest", "subgroup"),
                "box/violin/raincloud=auto|multi|bootstrap；forest/subgroup=cox"),
    "--compare": (("roc",), None),
    "--egger": (("funnel",), None),
    "--hatch": (("bar", "grouped_bar", "stacked_bar", "hbar"), "bar 系"),
    "--order": (("bar", "grouped_bar", "stacked_bar", "hbar", "line", "scatter"), "按族"),
    "--normalize": (("bar", "grouped_bar", "hbar", "horizontal_bar", "stacked_bar", "line"), "bar 系/line"),
    "--arena": (("bar",), "仅单系列竖向 bar；v7.7 默认启用竞技场风格（冠军=最高柱；负面指标 --arena off 关闭；--arena \"名称\" 指定冠军）"),
    "--sig-auto": (("box", "violin", "raincloud"), "全自动两两检验+bracket（原始分布数据）"),
    "--sig-bracket": (("bar", "grouped_bar", "box", "violin"), "组间显著性括号（comparisons 字段）"),
    "--peak-label": (("line",), None),
    "--cmap": (("heatmap", "cluster_heatmap"), None),
    "--vmin": (("heatmap", "cluster_heatmap"), None),
    "--vmax": (("heatmap", "cluster_heatmap"), None),
    "--annot": (("heatmap",), "on|auto|off：格内数值标注（auto=大矩阵自动隐藏，v7.9.1）"),
    "--cell-edge": (("heatmap",), "格线描边（v7.9.1；低对比色阶下保结构）"),
    "--discrete": (("heatmap",), "离散色阶（ListedColormap+BoundaryNorm，有序离散标度；v7.9.1）"),
    "--trend": (("scatter",), None),
    "--show-ratio": (("grouped_bar",), None),
    "--ratio-base": (("grouped_bar",), None),
    "--downsample": (("cluster_heatmap",), None),
    "--rmst-tau": (("rmst",), None),
    "--gate": (("diagram", "flow"), "basic|strict：strict=三层 bbox 断言（节点×边标签×箭头），违规 exit 2"),
    "--cox-time": (("forest", "subgroup"), None),
    "--cox-event": (("forest", "subgroup"), None),
    "--cox-cols": (("forest", "subgroup"), None),
    "--subgroup-vars": (("subgroup",), None),
    "--treatment": (("subgroup",), None),
    "--cut": (("subgroup",), None),
    "--no-risk-table": (("km",), None),
    "--risk-times": (("km",), None),
    "--no-median": (("km",), None),
}
_FLAGS_UNIVERSAL = ("--title --xlabel --ylabel --subtitle --source --style --theme --journal "
                    "--column --size --width --height --dpi --format --multi-format --cjk "
                    "--legend/--no-legend --legend-loc --legend-outside --show-values --summary "
                    "--verify --doctor --audit --repro --pub-ready --timeout --retries --debug --palette "
                    "--explain --suggest --list-types --list-themes --batch --pipeline")


_ALIAS_TO_CANON = {"horizontal_bar": "hbar", "boxplot": "box", "survival": "km"}


def list_flags_query(chart_type, valid_types):
    """--list-flags：输出某图型的专属旗标（域内）与域外旗标（[ignored] 预告）。

    chart_type=None 时输出全图型专属旗标速览；未知图型抛 ValueError（调用方 exit 1）。
    valid_types=引擎注册表清单（GENerators 键），由调用方传入避免循环依赖。"""
    if chart_type is None:
        lines = ["各图型专属旗标（通用旗标对所有图型可用：" + _FLAGS_UNIVERSAL + "）："]
        for f, (dom, note) in _FLAG_DOMAINS.items():
            lines.append(f"  {f}: {'/'.join(dom)}" + (f"（{note}）" if note else ""))
        return "\n".join(lines)
    canon = _ALIAS_TO_CANON.get(chart_type, chart_type)
    if chart_type not in valid_types:
        raise ValueError(f"未知图型 '{chart_type}'——用 --list-types 查看全部图型")
    mine, others = [], []
    for f, (dom, note) in _FLAG_DOMAINS.items():
        if canon in dom:
            mine.append(f + (f"（{note}）" if note else ""))
        else:
            others.append(f"{f}[{'/'.join(dom)}]")
    lines = [f"图型 {chart_type} 的旗标域：",
             f"  专属/生效：{' '.join(mine) if mine else '（无专属旗标）'}",
             "  域外（传入会被 [ignored] 显式告知，不生效）：",
             f"    {' '.join(others)}",
             f"  通用旗标：{_FLAGS_UNIVERSAL}"]
    return "\n".join(lines)



_FLAG_CHART_TYPES = tuple({t for dom, _ in _FLAG_DOMAINS.values() for t in dom})
