#!/usr/bin/env python3
"""build_db.py — 高职院校内部质量保证体系诊改场景：生成确定性 SQLite 物理库（domain.db）。

业务故事：一所高职院校按「五横五纵」建内部质量保证体系，诊改平台沉淀两张表：
  diag_tasks    —— 诊改任务明细表（一行一条指标任务；任务由规划指标层层分解而来，
                   挂在 学校/专业/课程/教师/学生 五个层面，带目标值/实际值/达标策略/状态）
  diag_warnings —— 预警记录表（一行一条预警；倒计时/逾期两类，引用任务主键）
口径与字段参照真实文件：《高等职业院校内部质量保证体系诊断与改进指导方案（试行）》
（教职成司函〔2015〕168号）、《职业院校数字基座高职数据标准及接口规范（试行）V3.0.3》
（教育部职成司指导，2024-09）、目标管理与诊改平台需求说明书 V3.0（指标来源内置：
双高任务/职教本科/ISO质量管理；标准类型：国标/省标/市标/校标；达标策略：＞＜＝≥≤属于）。
造数完全确定（无随机数），gold 期望可用 SQL 复算。
"""
import os
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, "domain.db")

LEVELS = ["学校", "专业", "课程", "教师", "学生"]
PLAN_GROUP = {
    "学校": "学校发展规划",
    "专业": "专业建设规划",
    "课程": "课程建设规划",
    "教师": "教师队伍建设规划",
    "学生": "学生综合素质发展规划",
}
SOURCES = ["双高任务", "职教本科", "ISO质量管理", "校内自定义"]
DEPTS = ["教务处", "人事处", "学工部", "质管办", "信息中心"]

# 每个层面 12 条指标任务的名称（真实诊改指标风格，虚构校无关通用）
NAMES = {
    "学校": ["专业群数量", "双高建设任务完成数", "信息化标杆校指标完成数", "生均教学经费",
             "实训基地数", "校企合作项目数", "国际交流项目数", "专利授权数",
             "社会培训人次", "技术服务到款额", "数字资源总量", "平安校园系统覆盖率"],
    "专业": ["专业标准制定数", "人才培养方案修订数", "1+X证书试点数", "订单班数量",
             "专业群课程共享数", "企业导师人数", "实训工位数", "现代学徒制试点数",
             "毕业生对口就业率", "技能竞赛获奖数", "产教融合基地数", "岗位实习覆盖率"],
    "课程": ["在线精品课程数", "课程思政示范课数", "活页式教材数", "虚拟仿真实训项目数",
             "达标课时数", "数字课程资源更新数", "混合式教学课程数", "企业案例引入数",
             "课程考核改革数", "题库建设数", "教学做一体课程数", "课程达标率"],
    "教师": ["双师型教师人数", "教师企业实践人次数", "教学能力比赛获奖数", "数字化教学培训人次",
             "骨干教师培养人数", "教学创新团队数", "教师下企业天数", "课题立项数",
             "教学成果奖数", "教师诊改报告提交数", "名师工作室数", "教师培训覆盖率"],
    "学生": ["技能竞赛参与人次", "证书获取率", "社团活动参与人次", "体质测试达标率",
             "心理健康普查率", "创新创业项目数", "志愿服务人次", "二课堂活动数",
             "实习合格率", "就业去向落实率", "奖学金覆盖率", "学生满意度"],
}
# 每层面 12 条任务的状态布局（达=已达标 未=未达标 逾=已逾期 提=未提交）：
# 前 6 条属 2025 年度诊改体系，后 6 条属 2026 年度诊改体系
STATUS = {
    "学校": ["达", "达", "达", "达", "未", "达", "达", "达", "达", "达", "未", "逾"],
    "专业": ["达", "达", "达", "未", "达", "提", "达", "达", "达", "未", "达", "逾"],
    "课程": ["达", "达", "未", "达", "未", "提", "达", "达", "未", "达", "达", "逾"],
    "教师": ["达", "未", "达", "未", "达", "提", "未", "达", "达", "逾", "达", "逾"],
    "学生": ["达", "未", "达", "提", "达", "未", "达", "提", "达", "逾", "达", "提"],
}
STATUS_MAP = {"达": "已达标", "未": "未达标", "逾": "已逾期", "提": "未提交"}
WEIGHTS = [0.2, 0.4, 0.6, 0.8, 1.0]


def unit_of(name):
    """按指标名称确定性推数据单位（诊改设置-数据单位字典：个/人/%/万元/门/天）。"""
    if "率" in name or "满意度" in name:
        return "%"
    if "经费" in name or "到款" in name:
        return "万元"
    if "人次" in name or "人数" in name:
        return "人"
    if "课程" in name or "课时" in name:
        return "门"
    if "天数" in name:
        return "天"
    return "个"


def build():
    if os.path.exists(DB):
        os.remove(DB)
    conn = sqlite3.connect(DB)
    conn.executescript("""
    CREATE TABLE diag_tasks (
        task_id TEXT PRIMARY KEY,
        level TEXT NOT NULL,
        plan_group TEXT NOT NULL,
        source TEXT NOT NULL,
        indicator_name TEXT NOT NULL,
        unit TEXT NOT NULL,
        strategy TEXT NOT NULL,
        target_value REAL NOT NULL,
        actual_value REAL,
        status TEXT NOT NULL,
        dept TEXT NOT NULL,
        system_name TEXT NOT NULL,
        end_date TEXT NOT NULL,
        weight REAL NOT NULL
    );
    CREATE TABLE diag_warnings (
        warn_id TEXT PRIMARY KEY,
        task_id TEXT NOT NULL,
        warn_type TEXT NOT NULL,
        warn_status TEXT NOT NULL,
        warn_date TEXT NOT NULL
    );
    """)
    g = 0  # 全局任务序号 1..60
    for level in LEVELS:
        for k in range(12):
            g += 1
            name = NAMES[level][k]
            st = STATUS_MAP[STATUS[level][k]]
            strategy = "≥" if g % 2 == 1 else "≤"
            target = float(5 + (g * 7) % 45)
            delta = g % 4 + 1
            if st == "已达标":
                actual = target + delta if strategy == "≥" else max(target - delta, 0.0)
            elif st == "未达标":
                actual = max(target - delta, 0.0) if strategy == "≥" else target + delta
            else:
                actual = None  # 未提交/已逾期暂无实际值（诊改平台真实形态）
            system_name = "2025年度诊改" if k < 6 else "2026年度诊改"
            end_date = "2025-12-31" if k < 6 else "2026-12-31"
            conn.execute(
                "INSERT INTO diag_tasks VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (f"T{g:04d}", level, PLAN_GROUP[level], SOURCES[(g - 1) % 4], name,
                 unit_of(name), strategy, target, actual, st,
                 DEPTS[(g - 1) % 5], system_name, end_date, WEIGHTS[(g - 1) % 5]))
    # 24 条预警：关联任务按序号轮转散开；每 3 条 1 条未处理 → 未处理 8 条
    for w in range(1, 25):
        conn.execute(
            "INSERT INTO diag_warnings VALUES (?,?,?,?,?)",
            (f"W{w:04d}", f"T{((w - 1) * 5) % 60 + 1:04d}",
             "倒计时预警" if w % 2 == 1 else "逾期预警",
             "未处理" if w % 3 == 0 else "已处理",
             f"2026-08-{(w - 1) % 28 + 1:02d}"))
    conn.commit()
    n_t = conn.execute("SELECT COUNT(*) FROM diag_tasks").fetchone()[0]
    n_w = conn.execute("SELECT COUNT(*) FROM diag_warnings").fetchone()[0]
    conn.close()
    print(f"建库完成：{DB}（diag_tasks {n_t} 行 / diag_warnings {n_w} 行）")


if __name__ == "__main__":
    build()
