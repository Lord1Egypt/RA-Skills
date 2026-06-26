#!/usr/bin/env python3
"""
合规规则三层语义编码
将现有40条规则映射到三层编码体系：
  {法规类型}-{违规大类}-{序号}
同时补充 law_reference 和 severity_score

运行方式:
  python3 tools/compliance_hierarchy.py   # 执行迁移
"""

import sys
import json
from pathlib import Path
from db import get_conn, close_conn

SKILL_DIR = Path(__file__).parent.parent


# ─────────────────────────────────────────
# 三层编码体系定义
# ─────────────────────────────────────────

RULE_HIERARCHY = {
    # 广告法 - 绝对化用语
    "C001": {"hierarchy": "GA-A-001", "law": "《广告法》第九条", "severity": 10,
              "note": "使用'最佳'等绝对化用语"},
    "C002": {"hierarchy": "GA-A-002", "law": "《广告法》第九条", "severity": 10,
              "note": "使用'第一'、'首选'等绝对化表述"},
    "C003": {"hierarchy": "GA-A-003", "law": "《广告法》第九条", "severity": 8,
              "note": "使用'极品'、'万能'等夸大用语"},
    "C004": {"hierarchy": "GA-A-004", "law": "《广告法》第九条", "severity": 10,
              "note": "使用'国家级'等禁止表述"},

    # 广告法 - 疗效承诺
    "C005": {"hierarchy": "GA-B-001", "law": "《广告法》第十六条", "severity": 10,
              "note": "声称'根治'、'完全治愈'"},
    "C006": {"hierarchy": "GA-B-002", "law": "《广告法》第十六条", "severity": 10,
              "note": "说明治愈率或有效率"},
    "C007": {"hierarchy": "GA-B-003", "law": "《广告法》第十六条", "severity": 9,
              "note": "'无效退款'等保证治愈表述"},
    "C008": {"hierarchy": "GA-B-004", "law": "《广告法》第十六条", "severity": 9,
              "note": "'药到病除'等保证疗效表述"},
    "C009": {"hierarchy": "GA-B-005", "law": "《广告法》第十六条", "severity": 8,
              "note": "'完全愈合'等绝对化疗效承诺"},
    "C010": {"hierarchy": "GA-B-006", "law": "《广告法》第十六条", "severity": 10,
              "note": "'包治百病'等虚假承诺"},

    # 处方药管理
    "C011": {"hierarchy": "RP-A-001", "law": "《药品管理法》第八十九条", "severity": 10,
              "note": "处方药在大众媒体发布广告"},
    "C012": {"hierarchy": "RP-A-002", "law": "《处方药与非处方药分类管理办法》", "severity": 9,
              "note": "处方药使用代言人"},
    "C013": {"hierarchy": "RP-A-003", "law": "《广告法》第十六条", "severity": 7,
              "note": "处方药适应症夸大"},

    # 竞品比较
    "C014": {"hierarchy": "GA-C-001", "law": "《广告法》第十二条", "severity": 8,
              "note": "贬低其他生产经营者商品"},
    "C015": {"hierarchy": "GA-C-002", "law": "《广告法》第十二条", "severity": 6,
              "note": "绝对化价格比较表述"},

    # 数据引用
    "C016": {"hierarchy": "GA-D-001", "law": "《广告法》第十一条", "severity": 7,
              "note": "数据引用无来源"},
    "C017": {"hierarchy": "GA-D-002", "law": "《广告法》第十一条", "severity": 6,
              "note": "统计数据夸大或编造"},
    "C018": {"hierarchy": "GA-D-003", "law": "《广告法》第十一条", "severity": 9,
              "note": "虚假排名数据"},

    # 患者证言
    "C019": {"hierarchy": "GA-E-001", "law": "《广告法》第十三条", "severity": 7,
              "note": "患者证言暗示保证疗效"},
    "C020": {"hierarchy": "GA-E-002", "law": "《广告法》第十三条", "severity": 5,
              "note": "患者前后对比缺乏个体差异说明"},

    # 平台特定规则
    "C021": {"hierarchy": "PLT-DY-001", "law": "抖音医疗内容规范", "severity": 9,
              "note": "无资质医生看诊/开药"},
    "C022": {"hierarchy": "PLT-XHS-001", "law": "小红书医药内容规范", "severity": 7,
              "note": "OTC/处方药在线购药引导"},
    "C023": {"hierarchy": "PLT-WX-001", "law": "微信医疗内容外链规范", "severity": 6,
              "note": "不当购买引导"},

    # 季节性内容
    "C024": {"hierarchy": "GA-B-007", "law": "《广告法》第十六条", "severity": 7,
              "note": "流感季节'特效药'声称"},
    "C025": {"hierarchy": "GA-B-008", "law": "《广告法》第十六条", "severity": 9,
              "note": "过敏季'根治'声称"},

    # KOL合作
    "C026": {"hierarchy": "KOL-A-001", "law": "KOL合作合规指南", "severity": 7,
              "note": "KOL代言含疗效承诺"},
    "C027": {"hierarchy": "KOL-A-002", "law": "KOL合作合规指南", "severity": 5,
              "note": "KOL推广内容夸大宣传"},

    # 通用红线
    "C028": {"hierarchy": "GN-F-001", "law": "《广告法》第三条", "severity": 10,
              "note": "涉及政治敏感话题"},
    "C029": {"hierarchy": "GN-F-002", "law": "《广告法》第九条", "severity": 9,
              "note": "含封建迷信表述"},
    "C030": {"hierarchy": "GN-F-003", "law": "《药品管理法》第九十八条", "severity": 10,
              "note": "发布虚假医药信息"},

    # 成分/专利夸大
    "C031": {"hierarchy": "GA-F-001", "law": "《广告法》第二十八条", "severity": 7,
              "note": "专利夸大宣传"},
    "C032": {"hierarchy": "GA-F-002", "law": "《广告法》第二十八条", "severity": 5,
              "note": "'纯天然无副作用'等夸大表述"},

    # 用法用量
    "C033": {"hierarchy": "GA-G-001", "law": "《药品管理法》第九十七条", "severity": 8,
              "note": "用法用量错误引导"},
    "C034": {"hierarchy": "GA-G-002", "law": "《药品说明书和标签管理规定》", "severity": 9,
              "note": "适用人群错误引导（孕妇/儿童）"},
    "C035": {"hierarchy": "GA-H-001", "law": "《广告法》第二十八条", "severity": 5,
              "note": "有效期夸大表述"},

    # 科室细分
    "C036": {"hierarchy": "GA-I-001", "law": "《广告法》第十六条", "severity": 7,
              "note": "皮肤科'根治/一次美白'绝对化表述"},
    "C037": {"hierarchy": "GA-I-002", "law": "《广告法》第十六条", "severity": 9,
              "note": "眼科'恢复视力/治愈近视'声称"},
    "C038": {"hierarchy": "GA-I-003", "law": "《广告法》第十六条+儿科规范", "severity": 9,
              "note": "儿科用药安全声称"},
    "C039": {"hierarchy": "GA-I-004", "law": "《广告法》第十六条", "severity": 7,
              "note": "慢病管理'停药不反弹'夸大"},
    "C040": {"hierarchy": "GA-J-001", "law": "《广告法》第二十八条", "severity": 9,
              "note": "保健品宣传疗效"},
}


# 编码前缀解释（用于知识库文档）
HIERARCHY_LEGEND = """
## 合规规则三层编码体系

### 编码格式
`{法规类型}-{违规大类}-{序号}`

### 第一位：法规类型
| 前缀 | 法规/类别 | 说明 |
|------|-----------|------|
| GA | 广告法 | 《广告法》相关条款 |
| RP | 处方药规定 | 处方药特殊管理规范 |
| KOL | KOL合作规范 | KOL推广专项规定 |
| PLT | 平台特定规则 | 各平台医药内容专项规范 |
| GN | 通用红线 | 所有内容通用合规要求 |

### 第二位（大类）
| 代码 | 大类 | 说明 |
|------|------|------|
| A | 绝对化用语 | '最佳'、'第一'等禁用表述 |
| B | 疗效承诺 | '根治'、'治愈'等保证治愈表述 |
| C | 竞品比较 | 贬低竞品、价格比较等 |
| D | 数据引用 | 统计数据、排名等 |
| E | 患者证言 | 患者案例使用规范 |
| F | 虚假信息 | 虚假宣传、封建迷信等 |
| G | 用法用量 | 剂量、适用人群误导 |
| H | 有效期 | 有效期夸大表述 |
| I | 科室细分 | 各科室专项（如皮肤科、眼科） |
| J | 保健品 | 保健品宣传疗效 |

### 第三位：序号
- 从 001 起始，同一类下多条规则顺延

### 编码示例
- `GA-A-001` → 广告法(GA) → 绝对化用语(A) → 第1条
- `RP-A-001` → 处方药规定(RP) → 大众媒体宣传(A) → 第1条
- `GA-B-003` → 广告法(GA) → 疗效承诺(B) → 第3条
"""


def apply_hierarchy(conn):
    """将三层编码写入数据库"""
    updated = 0
    for rule_code, meta in RULE_HIERARCHY.items():
        conn.execute("""
            UPDATE compliance_rules
            SET rule_hierarchy = ?,
                law_reference = ?,
                severity_score = ?
            WHERE rule_code = ?
        """, (meta["hierarchy"], meta["law"], meta["severity"], rule_code))
        updated += 1
    conn.commit()
    return updated


def get_hierarchy_tree(conn) -> dict:
    """构建合规规则层级树（用于知识库生成）"""
    rows = conn.execute("""
        SELECT rule_hierarchy, rule_code, rule_name, law_reference, severity_score,
               action_level, pattern, description
        FROM compliance_rules
        WHERE rule_hierarchy IS NOT NULL
        ORDER BY rule_hierarchy
    """).fetchall()

    tree = {}
    for row in rows:
        h = row[0]
        if not h:
            continue
        parts = h.split("-", 2)
        if len(parts) < 3:
            continue
        cat1, cat2, seq = parts[0], parts[1], parts[2]

        if cat1 not in tree:
            tree[cat1] = {}
        if cat2 not in tree[cat1]:
            tree[cat1][cat2] = []
        tree[cat1][cat2].append({
            "code": row[1],
            "name": row[2],
            "law": row[3],
            "severity": row[4],
            "level": row[5],
            "pattern": row[6],
            "description": row[7],
        })
    return tree


def generate_markdown_tree(tree: dict) -> str:
    """生成 Markdown 格式的规则树文档"""
    cat1_names = {
        "GA": "广告法相关",
        "RP": "处方药规定",
        "KOL": "KOL合作规范",
        "PLT": "平台特定规则",
        "GN": "通用红线",
    }
    cat2_names = {
        "A": "绝对化用语", "B": "疗效承诺", "C": "竞品比较",
        "D": "数据引用", "E": "患者证言", "F": "虚假信息",
        "G": "用法用量", "H": "有效期", "I": "科室细分",
        "J": "保健品宣传",
    }

    lines = ["# 合规规则层级索引\n", "## 编码体系\n", HIERARCHY_LEGEND, "\n## 规则索引\n"]

    for cat1 in ["GA", "RP", "KOL", "PLT", "GN"]:
        if cat1 not in tree:
            continue
        lines.append(f"### {cat1} — {cat1_names.get(cat1, cat1)}\n")
        for cat2 in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]:
            if cat2 not in tree[cat1]:
                continue
            rules = tree[cat1][cat2]
            lines.append(f"#### {cat1}-{cat2} {cat2_names.get(cat2, cat2)}\n")
            lines.append(f"| 规则编码 | 规则名称 | 法规依据 | 严重度 | 操作级别 |\n")
            lines.append(f"|----------|---------|---------|--------|\n")
            for r in sorted(rules, key=lambda x: x["code"]):
                lines.append(
                    f"| `{r['code']}` | {r['name']} | {r['law']} | "
                    f"{r['severity']}/10 | {r['level']} |\n"
                )
            lines.append("\n")

    return "".join(lines)


def main():
    dry_run = "--dry" in sys.argv

    conn = get_conn()
    
    try:
        # 应用编码
        updated = apply_hierarchy(conn)
        print(f"✅ 已更新 {updated} 条规则的三层编码")

        # 生成层级树
        tree = get_hierarchy_tree(conn)

        # 生成 Markdown 文档
        md_content = generate_markdown_tree(tree)

        # 写入知识库
        out_path = Path(__file__).parent.parent / "knowledge" / "compliance" / "03-rule-hierarchy.md"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"✅ 层级索引文档已写入: {out_path}")

        # 验证
        rows = conn.execute("""
            SELECT rule_code, rule_hierarchy, law_reference, severity_score
            FROM compliance_rules
            WHERE rule_hierarchy IS NOT NULL
            LIMIT 5
        """).fetchall()
        print("\n验证示例：")
        for r in rows:
            print(f"  {r[0]}: {r[1]} | {r[2]} | severity={r[3]}")

        total_hierarchied = conn.execute(
            "SELECT COUNT(*) FROM compliance_rules WHERE rule_hierarchy IS NOT NULL"
        ).fetchone()[0]
        print(f"\n总计: {total_hierarchied}/40 条规则已编码")

    finally:
        close_conn(conn)


if __name__ == "__main__":
    main()
