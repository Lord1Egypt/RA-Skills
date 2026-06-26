# core.py — 消金信披采集引擎（唯一真相源）
# 所有 Phase-1 脚本共享此模块，禁止复制粘贴 extract_from_text / normalize_date
"""
设计原则：
1. 日期提取是玄学：各消金公司日期格式差异极大（30家30种），
   统一用「两遍扫描双向最近邻」算法，零硬编码。
2. 正文提取只做标题+日期，不解析内容（Phase 2 负责）。
3. 无状态：纯函数，输入文本+URL，输出公告列表。
"""
import re
from typing import Optional

# ─── 跳过词 ──────────────────────────────────────────────────────────────────
SKIP_TITLES: set[str] = {
    "首页", "关于我们", "联系我们", "版权", "Copyright", "Registered", "客服", "办公地址",
    "关注我们", "下载APP", "加入我们", "网站地图", "企业名称", "点击查看", "更多",
    "网站标识码", "ICP证", "可信网站", "网络文化经营许可证", "网络文化", "95137",
    "layui-laypage", "layui-box", "layui-laypage-default",
}

# ─── 日期正则 ─────────────────────────────────────────────────────────────────
# 覆盖所有消金公司格式，按优先级排列（长模式优先，避免短模式抢先）
DATE_PAT = re.compile(
    # 时间：前缀（马上消金：时间：2025-07-22 浏览量：1278）
    r"^时间[：:]\s*\d{4}[\s\-/.年][\s\-/月]?\d{0,2}[\s\-/日]?\d{0,2}|"
    # 日期：前缀（晋商col23：日期：2025-09-24）
    r"^日期[：:]\s*\d{4}[\s\-/.年][\s\-/月]?\d{0,2}[\s\-/日]?\d{0,2}|"
    # 发布时间：前缀（盛银）
    r"^发布时间[：:]\s*\d{4}[\s\-/.年][\s\-/月]?\d{0,2}[\s\-/日]?\d{0,2}|"
    # 标准 YYYY年MM月DD日 HH:mm:ss（盛银/尚诚）
    r"^\d{4}年\d{1,2}月\d{1,2}日|"
    # 标准 YYYY年MM月（阳光消金嵌入标题）
    r"^\d{4}年\d{1,2}月|"
    # 标准 YYYY-MM-DD / YYYY/MM/DD / YYYY.MM.DD
    r"^\d{4}[\-/.年]\d{1,2}[\-/.月]\d{1,2}|"
    # YYYY.MM.DD / YYYY/MM/DD（晋商）
    r"^\d{4}[/.]\d{1,2}[/.]\d{1,2}|"
    # YYYY.MM（蒙商/晋商 partial，月在标题后）
    r"^\d{4}\.\d{1,2}|"
    # YYYY/MM（海尔斜杠）
    r"^\d{4}/\d{1,2}|"
    # DD-MM-YYYY / DD.MM.YYYY / DD YYYY.MM（蒙商，DD>12 是判断依据）
    r"^\d{1,2}[-\. ]\d{1,2}[-\. ]\d{4}|"
    # DD-MM-YY（河北幸福：26-04-02 → 2026-04-02，g1>12 则 g1 是年）
    r"^\d{1,2}[-\.]\d{1,2}[-\.]\d{2}|"
    # MM-DD（杭银/中原 split-line：03-14 + 2026）
    r"^\d{1,2}[-\.]\d{1,2}|"
    # 单独年份（杭银 split-line：2026 + 03-14）
    r"^(?:20)?(19|20)\d{2}$|"
    # MM/DD（杭银双行：12/05 + 2026）
    r"^\d{1,2}/\d{1,2}|"
    # DD YYYY.MM 蒙商双行（14 + 2026.01）
    r"^\d{1,2}\s+\d{4}[/\.]\d{1,2}"
)

BODY_PAT = re.compile(
    r"^(根据|为了|按照|近来|任何|如您|本|特此|本公司|兹有)"
)

# ─── 日期归一化 ───────────────────────────────────────────────────────────────
def normalize_date(s: str) -> str:
    """
    将任意日期格式统一为 ISO 字符串。
    无法解析时返回空字符串。
    特殊返回值（待合并）：
      PARTIAL:YYYY  — 只有年份（需与后续行的月日合并）
      PARTIAL:MM-DD — 只有月日（需与后续行的年份合并）
      PARTIAL:YYYY.MM — 只有年月（需与后续行的日合并）
    """
    s = re.sub(r"\s+\d{2}:\d{2}(:\d{2})?$", "", s)   # 去掉 HH:mm[:ss] 后缀
    s = re.sub(r"\s+", "", s)                        # 去掉所有空格
    s = s.replace("\xa0", "").replace(" ", "")
    s = s.replace("年", "-").replace("月", "-").replace("日", " ")
    s = re.sub(r"^时间[：:]\s*", "", s)
    s = re.sub(r"^日期[：:]\s*", "", s)
    s = re.sub(r"^发布时间[：:]\s*", "", s)
    s = re.sub(r'\s+(?:浏览量|访问量|点击量|pv)[：:]*[\d]*.*$', "", s)  # 马上消金

    # ── 优先长模式 ──────────────────────────────────────────────────────────
    # 找 ISO 完整日期（允许前导非数字）
    for pat in [
        r"(?:^|[^\d])(\d{4}-\d{2}-\d{2})(?!\d|-)",
        r"(?:^|[^\d])(\d{4}-\d{2})(?!\d|-)",
    ]:
        m = re.search(pat, s)
        if m:
            parts = m.group(1).split("-")
            if len(parts) == 3:
                return f"{int(parts[0]):04d}-{int(parts[1]):02d}-{int(parts[2]):02d}"
            elif len(parts) == 2:
                return f"{int(parts[0]):04d}-{int(parts[1]):02d}"

    # YYYY年MM月DD日 HH:mm:ss（盛银/尚诚）
    m = re.match(r"^(\d{4})-(\d{1,2})-(\d{1,2}) (\d{2}):(\d{2})", s)
    if m:
        return f"{int(m.group(1)):04d}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"

    # YYYY.MM（蒙商 partial：2026.04，需与后续行合并）
    m = re.match(r"^(\d{4})\.(\d{1,2})$", s)
    if m:
        return f"PARTIAL:{m.group(1)}.{m.group(2)}"

    # YYYY年MM月（阳光：2026年3月）
    t = s.replace("（", "").replace("(", "").replace("）", "").replace(")", "")
    t = re.sub(r"[^\d-]", "", t).rstrip("-")
    m = re.match(r"^(\d{4})-(\d{1,2})$", t)
    if m:
        return f"{int(m.group(1)):04d}-{int(m.group(2)):02d}"

    # 标准 YYYY/MM/DD
    m = re.match(r"^(\d{4})/(\d{1,2})/(\d{1,2})$", s)
    if m:
        return f"{int(m.group(1)):04d}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"

    # YYYY.MM.DD
    m = re.match(r"^(\d{4})\.(\d{1,2})\.(\d{1,2})$", s)
    if m:
        return f"{int(m.group(1)):04d}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"

    # 单独年份 → PARTIAL
    m = re.match(r"^(20\d{2})$", s)
    if m:
        return f"PARTIAL:{m.group(1)}"

    # DD-MM-YYYY / DD.MM.YYYY / DD YYYY.MM（蒙商）
    m = re.match(r"^(\d{1,2})[-\. ](\d{1,2})[-\. ](\d{4})$", s)
    if m:
        d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if d > 12 and mo <= 12:
            return f"{y:04d}-{mo:02d}-{d:02d}"   # 蒙商：14 2026.01
        elif mo > 12 and d <= 12:
            return f"{y:04d}-{d:02d}-{mo:02d}"
        else:
            return f"{y:04d}-{mo:02d}-{d:02d}"

    # DD-MM-YY（河北幸福：26-04-02 → 2026-04-02）
    m = re.match(r"^(\d{1,2})-(\d{1,2})-(\d{2})$", s)
    if m:
        g1, g2, yy = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if g1 > 12:        # g1=年(YY)，g2=月
            return f"{2000+g1:04d}-{g2:02d}-{yy:02d}"
        elif g2 > 12:      # g2=年(YY)，g1=日
            return f"{2000+g2:04d}-{g1:02d}-{yy:02d}"
        else:
            return f"{2000+yy:04d}-{g1:02d}-{g2:02d}"

    # MM-DD → PARTIAL（杭银/中原 split-line）
    m = re.match(r"^(\d{1,2})/(\d{1,2})$", s)
    if m:
        return f"PARTIAL:{int(m.group(1)):02d}/{int(m.group(2)):02d}"
    m = re.match(r"^(\d{1,2})-(\d{1,2})$", s)
    if m:
        return f"PARTIAL:{int(m.group(1)):02d}-{int(m.group(2)):02d}"

    # YYYY/MM（海尔斜杠）
    m = re.match(r"^(\d{4})/(\d{1,2})$", s)
    if m:
        return f"{int(m.group(1)):04d}-{int(m.group(2)):02d}"

    return ""


# ─── 分类 ─────────────────────────────────────────────────────────────────────
def classify(title: str) -> str:
    if not title:
        return "其他"
    if any(x in title for x in ["关联交易", "关联授信", "关联方", "统一交易协议"]):
        return "关联交易"
    if any(x in title for x in ["三支柱", "资本信息", "资本充足", "风险加权", "资本管理"]):
        return "资本信息"
    if any(x in title for x in ["合作催收", "合作机构", "委外催收", "增信服务"]):
        return "合作机构"
    if any(x in title for x in ["社会责任", "社责报告"]):
        return "社会责任"
    if any(x in title for x in ["年度信息", "年度披露", "年报", "年度审计"]):
        return "年度信披"
    if any(x in title for x in ["服务内容", "价格公示", "价目", "服务价格", "收费公示"]):
        return "服务价格"
    if any(x in title for x in ["债权转让", "不良贷款", "个人不良", "不良资产"]):
        return "债权转让"
    if any(x in title for x in ["投诉", "消费者权益", "消保", "保护金融消费者"]):
        return "消费者保护"
    if any(x in title for x in ["公司名称", "注册地址", "法定代表人", "经营范围", "营业执照"]):
        return "营业执照"
    return "重要公告"


# ─── 核心提取算法 ─────────────────────────────────────────────────────────────
def extract_from_text(text: str, url: str, max_dist: int = 8) -> list[dict]:
    """
    两遍扫描双向最近邻提取。

    Pass1: 扫描所有行，建立 date_map {line_idx: date_str}
           PARTIAL 日期（只有年月日之一）标记后留待合并

    Pass2: 非日期行，计算到最近日期行的距离
           同距离时正向优先（dj > i 胜出）
           距离 ≤ max_dist 才配对
    """
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    results: list[dict] = []
    seen: set[str] = set()
    date_map: dict[int, str] = {}

    # ── Pass1：建立日期索引 ────────────────────────────────────────────────
    for i, line in enumerate(lines):
        if DATE_PAT.match(line):
            ds = normalize_date(line)
            if ds:
                date_map[i] = ds
        else:
            # MM-DD 或 MM/DD（杭银/中原 split-line）
            mmdd_m = re.match(r"^(\d{1,2})[-\./](\d{1,2})$", line)
            if mmdd_m:
                date_map[i] = f"PARTIAL:{int(mmdd_m.group(1)):02d}-{int(mmdd_m.group(2)):02d}"

    # ── PARTIAL 合并 ────────────────────────────────────────────────────────
    final_dates: dict[int, str] = {}
    for i, ds in list(date_map.items()):
        if ds.startswith("PARTIAL:"):
            body = ds[8:]   # e.g. "03-14" 或 "2026" 或 "2026.04"

            # PARTIAL:2026.04（蒙商 YYYY.MM → 找后续行 "14"）
            if "." in body:
                ym = body
                for j in range(i + 1, min(i + 4, len(lines))):
                    day_m = re.match(r"^(\d{1,2})$", lines[j])
                    if day_m:
                        y, mo = ym.split(".")
                        final_dates[i] = f"{int(y):04d}-{int(mo):02d}-{int(day_m.group(1)):02d}"
                        break
                else:
                    final_dates[i] = ds   # 无法合并，保留 PARTIAL
                continue

            # PARTIAL:2026（年份 → 找后续 MM-DD）
            if re.match(r"^\d{4}$", body):
                year = int(body)
                for j in range(i + 1, min(i + 4, len(lines))):
                    mmdd_m = re.match(r"^(\d{1,2})[-\.](\d{1,2})$", lines[j])
                    if mmdd_m:
                        mo, day = int(mmdd_m.group(1)), int(mmdd_m.group(2))
                        if mo <= 12:
                            final_dates[i] = f"{year:04d}-{mo:02d}-{day:02d}"
                            break
                        elif day <= 12:
                            final_dates[i] = f"{year:04d}-{day:02d}-{mo:02d}"
                            break
                else:
                    final_dates[i] = ds
                continue

            # PARTIAL:03-14（月日 → 找后续年份 2026）
            if re.match(r"^\d{1,2}-\d{1,2}$", body) or re.match(r"^\d{1,2}/\d{1,2}$", body):
                parts = re.split(r"[-./]", body)
                g1, g2 = int(parts[0]), int(parts[1])
                for j in range(i + 1, min(i + 4, len(lines))):
                    year_m = re.match(r"^(19|20)(\d{2})$", lines[j])
                    if year_m:
                        year = int(year_m.group(1) + year_m.group(2))
                        if g1 <= 12:    # g1=月，g2=日
                            final_dates[i] = f"{year:04d}-{g1:02d}-{g2:02d}"
                        else:           # g2=月，g1=日
                            final_dates[i] = f"{year:04d}-{g2:02d}-{g1:02d}"
                        break
                else:
                    final_dates[i] = ds
                continue

            final_dates[i] = ds
        else:
            final_dates[i] = ds

    # ── Pass2：非日期行找最近日期 ──────────────────────────────────────────
    for i, line in enumerate(lines):
        # 长度过滤
        if len(line) < 4:
            continue
        # 固定跳过词
        if line in SKIP_TITLES:
            continue
        # 纯数字/符号行（非日期）
        if re.match(r"^[\d\-\/\.\:\s]+$", line) and not DATE_PAT.match(line):
            continue
        # Email
        if re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", line):
            continue
        # 开头词（"根据..."/"为了..."）
        if BODY_PAT.match(line):
            continue
        # HTML 标签残留
        if "<" in line or ">" in line:
            continue
        # 时间：前缀但有日期 → 当日期行处理，跳过
        if re.match(r"^时间[：:]", line):
            if normalize_date(line):
                continue
        # 日期行本身 → 跳过
        if DATE_PAT.match(line):
            continue
        # 跳过描述行："3月15日下午..." 或 "3月15日上午..."
        if re.match(r"^\d{1,2}月\d{1,2}(日[上下晚]午|日)[^日}\n]{0,20}[，,]", line):
            continue
        if re.match(r"^[上下晚]午\d", line):
            continue
        # 超长描述行（>50字，以公司名开头，含2个以上"，"）
        if len(line) > 50 and line.startswith(("中原消费金融",)) and line.count("，") >= 2:
            continue
        # 导航/版权类
        if re.match(r"^[\u4e00-\u9fa5]{0,3}(首页|关于我们|联系我们|版权|客服)", line):
            continue

        # 计算到最近日期的距离
        best_date, best_dist = None, 999
        for dj in sorted(final_dates.keys()):
            d = abs(dj - i)
            if d < best_dist or (d == best_dist and dj > i):
                best_dist, best_date = d, final_dates[dj]

        if best_date and best_dist <= max_dist:
            key = f"{line[:30]}|{best_date}"
            if key not in seen:
                seen.add(key)
                results.append({
                    "title": line[:200],
                    "date": best_date,
                    "url": url,
                    "category": classify(line),
                })

    return results
