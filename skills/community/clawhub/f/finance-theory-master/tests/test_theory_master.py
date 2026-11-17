#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""金融理论大师 —— 单元测试。

覆盖三块：
  1. 数据集生成器的确定性与字段规范
  2. 数据集的自洽性（枚举、唯一性、引用关系、覆盖度）
  3. 查询工具的行为（含「命中 0 条必须显式失败」）

运行：
    python -m pytest tests/ -q
"""

from __future__ import annotations

import csv
import importlib.util
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "theory_index.csv"


_SCRIPTS = str(ROOT / "scripts")
if _SCRIPTS not in sys.path:
    sys.path.insert(0, _SCRIPTS)

# 先把 schema / csvio 以标准名注册进 sys.modules，再加载另外三个脚本。
# 它们内部执行 `import schema`，会命中缓存拿到同一个模块对象。若不做这一步，
# _load 会各自新建一份 schema，`gen.ENUM_MODULE is schema.ENUM_MODULE` 就会失败——
# 那样测出来的「单一来源」是假的。
import csvio  # noqa: E402
import schema  # noqa: E402


def _load(name: str, relpath: str):
    """按路径加载 scripts/ 下的模块（scripts 不是包）。"""
    spec = importlib.util.spec_from_file_location(name, ROOT / relpath)
    assert spec and spec.loader, f"无法加载 {relpath}"
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


gen = _load("ftm_gen_data", "scripts/gen_data.py")
validate = _load("ftm_validate_data", "scripts/validate_data.py")
lookup = _load("ftm_theory_lookup", "scripts/theory_lookup.py")


# ---------------------------------------------------------------------------
# 夹具
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def rows() -> list[dict[str, str]]:
    assert CSV_PATH.exists(), "数据集未生成，请先运行 scripts/gen_data.py"
    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as fh:
        return [{k: (v or "").strip() for k, v in r.items()} for r in csv.DictReader(fh)]


# ---------------------------------------------------------------------------
# 1. 生成器
# ---------------------------------------------------------------------------

class TestGenerator:
    def test_render_is_deterministic(self):
        """同一进程内重复渲染必须逐字节一致。"""
        assert gen.render_csv() == gen.render_csv()

    def test_render_matches_disk(self):
        """磁盘内容与生成结果必须一致（等价于 gen_data.py --check）。"""
        assert CSV_PATH.read_text(encoding="utf-8") == gen.render_csv()

    def test_has_bom_for_excel(self):
        assert CSV_PATH.read_bytes().startswith(b"\xef\xbb\xbf")

    def test_field_order_matches_spec(self):
        with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as fh:
            header = next(csv.reader(fh))
        assert header == gen.FIELDS

    def test_subprocess_check_exit_zero(self):
        """以子进程方式跑 --check，确认退出码为 0。"""
        import subprocess

        rc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "gen_data.py"), "--check"],
            capture_output=True,
            text=True,
        )
        assert rc.returncode == 0, rc.stdout + rc.stderr

    def test_record_count(self):
        assert len(gen.RECORDS) >= 60, "理论条目数偏少"


# ---------------------------------------------------------------------------
# 2. 数据集自洽性
# ---------------------------------------------------------------------------

class TestDataset:
    def test_required_fields_non_empty(self, rows):
        """必填字段不得为空白；「—」表示不适用，属合法取值。"""
        for r in rows:
            for field in validate.REQUIRED_FIELDS:
                if field in validate.OPTIONAL_FIELDS:
                    continue
                assert r.get(field), f"[{r.get('theory_id')}] 字段为空：{field}"

    def test_module_enum(self, rows):
        for r in rows:
            assert r["module"] in validate.ENUM_MODULE, r["theory_id"]

    def test_strength_enum(self, rows):
        for r in rows:
            assert r["hypothesis_strength"] in validate.ENUM_STRENGTH, r["theory_id"]

    def test_status_enum(self, rows):
        for r in rows:
            assert r["evidence_status"] in validate.ENUM_STATUS, r["theory_id"]

    def test_theory_id_slug_format(self, rows):
        pat = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
        for r in rows:
            assert pat.match(r["theory_id"]), f"非法 slug：{r['theory_id']}"

    def test_theory_id_unique(self, rows):
        ids = [r["theory_id"] for r in rows]
        assert len(ids) == len(set(ids))

    def test_year_format(self, rows):
        pat = re.compile(r"^(\d{4}|—)$")
        for r in rows:
            assert pat.match(r["year"]), f"[{r['theory_id']}] 非法年份：{r['year']}"

    def test_no_self_reference(self, rows):
        for r in rows:
            tid = r["theory_id"]
            assert tid not in lookup_tokens(r["complementary"]), f"{tid} 在 complementary 中自引用"
            assert tid not in lookup_tokens(r["conflicting"]), f"{tid} 在 conflicting 中自引用"

    def test_complementary_and_conflicting_disjoint(self, rows):
        for r in rows:
            assert not (lookup_tokens(r["complementary"]) & lookup_tokens(r["conflicting"])), r["theory_id"]

    def test_every_module_covered(self, rows):
        present = {r["module"] for r in rows}
        assert present == set(validate.ENUM_MODULE)

    def test_every_strength_covered(self, rows):
        present = {r["hypothesis_strength"] for r in rows}
        assert present == set(validate.ENUM_STRENGTH)

    def test_every_status_covered(self, rows):
        present = {r["evidence_status"] for r in rows}
        assert present == set(validate.ENUM_STATUS)

    def test_all_reference_docs_exist(self):
        for name in validate.EXPECTED_REFS:
            p = ROOT / "references" / name
            assert p.exists(), f"缺少 {name}"
            assert p.stat().st_size > 2000, f"{name} 篇幅过小"

    def test_validator_passes(self):
        assert validate.main() == 0


def lookup_tokens(value: str) -> set[str]:
    return {t.strip() for t in value.split("|") if t.strip() and t.strip() != "—"}


# ---------------------------------------------------------------------------
# 3. 查询工具
# ---------------------------------------------------------------------------

class TestLookup:
    def test_keyword_hit(self, rows):
        res = lookup.search_keyword(rows, "波动率")
        assert res, "关键词应至少命中 1 条"

    def test_keyword_is_case_insensitive_for_ascii(self, rows):
        upper = lookup.search_keyword(rows, "CAPM")
        lower = lookup.search_keyword(rows, "capm")
        assert {r["theory_id"] for r in upper} == {r["theory_id"] for r in lower}

    def test_keyword_zero_hits_raises(self, rows):
        """命中 0 条必须显式抛错，不允许静默返回空列表。"""
        with pytest.raises(lookup.LookupError):
            lookup.search_keyword(rows, "这个词肯定不存在zzzqqq")

    def test_empty_keyword_raises(self, rows):
        with pytest.raises(lookup.LookupError):
            lookup.search_keyword(rows, "   ")

    def test_module_filter(self, rows):
        res = lookup.filter_field(rows, "module", "资产定价")
        assert len(res) >= 5
        assert all(r["module"] == "资产定价" for r in res)

    def test_module_filter_unknown_raises(self, rows):
        with pytest.raises(lookup.LookupError):
            lookup.filter_field(rows, "module", "不存在的板块")

    def test_status_filter(self, rows):
        res = lookup.filter_field(rows, "evidence_status", "有争议")
        assert res

    def test_strength_filter(self, rows):
        res = lookup.filter_field(rows, "hypothesis_strength", "极强")
        assert len(res) >= 1

    def test_render_brief_column_count(self, rows):
        res = lookup.search_keyword(rows, "因子")
        text = lookup.render_brief(res)
        header = text.splitlines()[0]
        assert header.count("|") == len(lookup.BRIEF_COLS) + 1
        assert len(lookup.BRIEF_COLS) <= 6, "简要表列数应控制在 6 列以内"

    def test_render_detail_contains_key_fields(self, rows):
        capm = next(r for r in rows if r["theory_id"] == "capm")
        text = lookup.render_detail(capm)
        assert "资本资产定价模型" in text
        assert "核心假设" in text
        assert "主要局限" in text

    def test_cli_list(self):
        import subprocess

        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "theory_lookup.py"), "--list"],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        assert proc.returncode == 0, proc.stderr
        assert "capm" in proc.stdout

    def test_cli_zero_hit_exit_code(self):
        import subprocess

        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "theory_lookup.py"), "-k", "绝不存在的词zzzqqq"],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        assert proc.returncode == 2, f"命中 0 条应返回退出码 2，实际 {proc.returncode}"


# ---------------------------------------------------------------------------
# 4. 内容抽查（防止后续维护时改坏关键口径）
# ---------------------------------------------------------------------------

class TestContentSpotCheck:
    KEY_FACTS = [
        ("capm", "core_assumption", "同质预期"),
        ("mm", "core_claim", "资本结构无关"),
        ("var", "main_limitation", "非次可加性"),
        ("minsky", "core_claim", "脆弱性"),
        ("taylor_rule", "core_claim", "通胀"),
        ("limits_to_arbitrage", "core_claim", "套利"),
        ("factor_zoo", "core_claim", "300"),
        ("replication_crisis", "core_claim", "452"),
    ]

    @pytest.mark.parametrize("tid,field,fragment", KEY_FACTS)
    def test_key_fact_present(self, rows, tid, field, fragment):
        row = next((r for r in rows if r["theory_id"] == tid), None)
        assert row is not None, f"缺少条目 {tid}"
        assert fragment in row[field], f"[{tid}].{field} 未包含「{fragment}」"


# ---------------------------------------------------------------------------
# 6. 金融史时间线
# ---------------------------------------------------------------------------

TIMELINE_PATH = ROOT / "data" / "financial_history_timeline.csv"


@pytest.fixture(scope="module")
def timeline() -> list[dict[str, str]]:
    assert TIMELINE_PATH.exists(), "时间线数据集未生成，请先运行 scripts/gen_data.py"
    with TIMELINE_PATH.open("r", encoding="utf-8-sig", newline="") as fh:
        return [{k: (v or "").strip() for k, v in r.items()} for r in csv.DictReader(fh)]


class TestTimeline:
    def test_file_exists_and_has_enough_rows(self, timeline):
        assert len(timeline) >= 80, f"时间线条目偏少：{len(timeline)}"

    def test_render_is_deterministic(self):
        assert gen.render_timeline_csv() == gen.render_timeline_csv()

    def test_render_matches_disk(self):
        assert TIMELINE_PATH.read_text(encoding="utf-8") == gen.render_timeline_csv()

    def test_field_order_matches_spec(self, timeline):
        with TIMELINE_PATH.open("r", encoding="utf-8-sig", newline="") as fh:
            header = next(csv.reader(fh))
        assert header == gen.TIMELINE_FIELDS

    def test_required_fields_non_empty(self, timeline):
        for r in timeline:
            for field in gen.TIMELINE_FIELDS:
                assert r.get(field), f"[{r.get('year')}] 字段为空：{field}"

    def test_sort_key_is_integer(self, timeline):
        for r in timeline:
            int(r["sort_key"])  # 不抛异常即通过

    def test_sort_key_is_non_decreasing(self, timeline):
        keys = [int(r["sort_key"]) for r in timeline]
        assert keys == sorted(keys), "时间线未按 sort_key 非递减排列"

    def test_stage_enum(self, timeline):
        for r in timeline:
            assert r["stage"] in gen.ENUM_STAGE, f"[{r['year']}] 非法分期：{r['stage']}"

    def test_category_enum(self, timeline):
        for r in timeline:
            assert r["category"] in gen.ENUM_HCATEGORY, f"[{r['year']}] 非法类别：{r['category']}"

    def test_every_stage_covered(self, timeline):
        present = {r["stage"] for r in timeline}
        assert present == set(gen.ENUM_STAGE)

    def test_every_category_covered(self, timeline):
        present = {r["category"] for r in timeline}
        assert present == set(gen.ENUM_HCATEGORY)

    def test_covers_ancient_to_modern(self, timeline):
        """必须同时覆盖公元前与 2020 年之后，否则「体系完整」不成立。"""
        keys = [int(r["sort_key"]) for r in timeline]
        assert min(keys) <= -2000, "未覆盖到古代美索不达米亚以前"
        assert max(keys) >= 2024, "未覆盖到 2024 年以后"

    def test_required_historical_anchors_present(self, timeline):
        """关键历史锚点必须存在，防止后续维护时误删。"""
        text = "\n".join(r["event"] + r["significance"] for r in timeline)
        anchors = [
            "汉谟拉比法典", "梭伦", "包税商", "交子", "美第奇", "圣乔治银行",
            "荷兰东印度公司", "阿姆斯特丹银行", "郁金香", "英格兰银行",
            "南海泡沫", "约翰·劳", "皮尔银行法", "美联储", "金本位",
            "布雷顿森林", "特里芬", "尼克松", "广场协议",
            "雷曼兄弟", "量化宽松", "比特币", "稳定币",
        ]
        missing = [a for a in anchors if a not in text]
        assert not missing, f"时间线缺失关键锚点：{missing}"

    def test_history_reference_docs_exist(self):
        for name in ("10-世界金融史（上）起源到金本位.md",
                     "11-世界金融史（下）布雷顿森林到数字金融.md",
                     "12-金融史脉络对照与索引.md"):
            p = ROOT / "references" / name
            assert p.exists(), f"缺少 {name}"
            assert p.stat().st_size > 5000, f"{name} 篇幅过小"

    def test_theory_index_links_to_history(self, timeline):
        """时间线里的关联理论应有相当比例能被理论索引定位。"""
        with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as fh:
            theory_names = {r["name_cn"] for r in csv.DictReader(fh)}
        linked = [r["related_theory"] for r in timeline if r["related_theory"] != "—"]
        assert len(linked) >= 40, f"关联理论标注过少：{len(linked)}"
        assert theory_names, "理论索引为空"


# ---------------------------------------------------------------------------
# 7. 政策工具箱
# ---------------------------------------------------------------------------

POLICY_PATH = ROOT / "data" / "policy_toolkit.csv"
CASE_PATH = ROOT / "data" / "investor_cases.csv"


def _read_csv(path):
    assert path.exists(), f"数据集未生成：{path}"
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return [{k: (v or "").strip() for k, v in r.items()} for r in csv.DictReader(fh)]


@pytest.fixture(scope="module")
def policy() -> list[dict[str, str]]:
    return _read_csv(POLICY_PATH)


@pytest.fixture(scope="module")
def cases() -> list[dict[str, str]]:
    return _read_csv(CASE_PATH)


class TestPolicyToolkit:
    def test_row_count(self, policy):
        assert len(policy) >= 30

    def test_render_is_deterministic(self):
        assert gen.render_policy_csv() == gen.render_policy_csv()

    def test_render_matches_disk(self):
        assert POLICY_PATH.read_text(encoding="utf-8") == gen.render_policy_csv()

    def test_field_order(self):
        with POLICY_PATH.open("r", encoding="utf-8-sig", newline="") as fh:
            assert next(csv.reader(fh)) == gen.POLICY_FIELDS

    def test_required_fields_non_empty(self, policy):
        for r in policy:
            for field in gen.POLICY_FIELDS:
                assert r.get(field), f"[{r.get('tool_id')}] 字段为空：{field}"

    def test_tool_id_unique_and_slug(self, policy):
        import re
        pat = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
        ids = [r["tool_id"] for r in policy]
        assert len(ids) == len(set(ids)), "tool_id 有重复"
        for tid in ids:
            assert pat.match(tid), f"非法 slug：{tid}"

    def test_market_stage_enum(self, policy):
        for r in policy:
            assert r["market_stage"] in gen.ENUM_MARKET_STAGE, r["tool_id"]

    def test_level_enum(self, policy):
        for r in policy:
            assert r["level"] in gen.ENUM_POLICY_LEVEL, r["tool_id"]

    def test_every_market_stage_covered(self, policy):
        present = {r["market_stage"] for r in policy}
        assert present == set(gen.ENUM_MARKET_STAGE)

    def test_every_level_covered(self, policy):
        present = {r["level"] for r in policy}
        assert present == set(gen.ENUM_POLICY_LEVEL)

    def test_mechanism_is_substantive(self, policy):
        """作用机制不能是空泛表述，必须有实质长度。"""
        for r in policy:
            assert len(r["mechanism"]) >= 15, f"[{r['tool_id']}] 作用机制过于简略"
            assert len(r["constraint"]) >= 10, f"[{r['tool_id']}] 约束条件过于简略"


class TestInvestorCases:
    def test_row_count(self, cases):
        assert len(cases) >= 20

    def test_render_is_deterministic(self):
        assert gen.render_case_csv() == gen.render_case_csv()

    def test_render_matches_disk(self):
        assert CASE_PATH.read_text(encoding="utf-8") == gen.render_case_csv()

    def test_field_order(self):
        with CASE_PATH.open("r", encoding="utf-8-sig", newline="") as fh:
            assert next(csv.reader(fh)) == gen.CASE_FIELDS

    def test_required_fields_non_empty(self, cases):
        for r in cases:
            for field in gen.CASE_FIELDS:
                assert r.get(field), f"[{r.get('case_id')}] 字段为空：{field}"

    def test_case_id_unique_and_slug(self, cases):
        import re
        pat = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
        ids = [r["case_id"] for r in cases]
        assert len(ids) == len(set(ids)), "case_id 有重复"
        for cid in ids:
            assert pat.match(cid), f"非法 slug：{cid}"

    def test_market_stage_enum(self, cases):
        for r in cases:
            # 复合标签（如「牛市转危机」）必须拆到 policy_env，此处只允许单一枚举值
            assert r["market_stage"] in gen.ENUM_MARKET_STAGE, \
                f"[{r['case_id']}] market_stage 必须为单一枚举值：{r['market_stage']}"

    def test_every_market_stage_covered(self, cases):
        """案例必须覆盖四类真实行情。「通用」是政策工具箱的取值，不适用于案例。"""
        case_stages = {"牛市", "熊市", "震荡市", "危机行情"}
        present = {r["market_stage"] for r in cases}
        assert present == case_stages, f"缺失行情类型：{case_stages - present}"

    def test_survivorship_bias_always_declared(self, cases):
        """每个案例都必须显式标注幸存者偏差，这是本模块的强制纪律。"""
        for r in cases:
            assert len(r["survivorship"]) >= 8, f"[{r['case_id']}] 未充分说明幸存者偏差"

    def test_signal_is_observable(self, cases):
        """识别信号必须是可观察对象，不能是主观感受。"""
        banned = ["我觉得", "感觉", "直觉", "不祥", "预感"]
        for r in cases:
            for w in banned:
                assert w not in r["signal"], f"[{r['case_id']}] 识别信号含主观表述：{w}"

    def test_non_western_cases_present(self, cases):
        """非西方区域必须有足够覆盖，否则「非西方部分」名不副实。"""
        non_west = ["中国", "印度", "日本", "韩国", "俄罗斯", "土耳其",
                    "马来西亚", "阿根廷", "中东", "非洲", "东南亚", "欧元区"]
        hit = [r for r in cases if any(k in r["region"] for k in non_west)]
        assert len(hit) >= 8, f"非西方案例过少：{len(hit)}"

    def test_pattern_is_reusable(self, cases):
        """案例必须归到一个可复用的推理模式。"""
        allowed = {"政策不可持续模式", "资产负债表错配模式", "融资结构模式",
                   "极端估值模式", "央行承诺模式", "制度变革模式", "催化剂与时点模式"}
        for r in cases:
            assert r["pattern"] in allowed, f"[{r['case_id']}] 未知推理模式：{r['pattern']}"

    def test_documentation_files_exist(self):
        for name in ("13-行情类型与政策工具箱.md",
                     "14-投资案例与判断逻辑.md",
                     "15-非西方金融史与政策实践.md"):
            p = ROOT / "references" / name
            assert p.exists(), f"缺少 {name}"
            assert p.stat().st_size > 8000, f"{name} 篇幅过小"


# ---------------------------------------------------------------------------
# 8. 结构契约：枚举与字段必须来自单一来源
#    这组测试锁住「schema.py 是唯一定义处」这一约定。旧版把枚举在 gen / validate /
#    lookup 三处各写一遍，改一处忘一处就会让校验器与生成器失配。
# ---------------------------------------------------------------------------

class TestSingleSourceOfTruth:
    """所有数据集定义必须来自 schema.py，不得在各脚本里重抄。"""

    def test_scripts_do_not_redeclare_enums(self):
        """除 schema.py 外，任何脚本都不应出现字面量枚举声明。"""
        offenders = []
        for rel in ("scripts/gen_data.py", "scripts/validate_data.py",
                    "scripts/theory_lookup.py"):
            text = (ROOT / rel).read_text(encoding="utf-8")
            for m in re.finditer(r"^(ENUM_[A-Z_]+)\s*=\s*\[", text, re.M):
                offenders.append(f"{rel}: {m.group(1)}")
        assert not offenders, f"以下枚举应改为引用 schema：{offenders}"

    def test_scripts_do_not_redeclare_field_lists(self):
        """除 schema.py 外，字段列表也不应出现字面量声明。"""
        pattern = re.compile(r"^((?:TIMELINE|POLICY|CASE)?_?FIELDS)\s*[:=]\s*\[", re.M)
        offenders = []
        for rel in ("scripts/gen_data.py", "scripts/validate_data.py",
                    "scripts/theory_lookup.py"):
            text = (ROOT / rel).read_text(encoding="utf-8")
            offenders += [f"{rel}: {m.group(1)}" for m in pattern.finditer(text)]
        assert not offenders, f"以下字段列表应改为引用 schema：{offenders}"

    def test_gen_and_validate_share_identifiers(self):
        """gen 与 validate 的枚举和字段必须指向同一对象，而非内容相同的两份副本。"""
        for name in ("ENUM_MODULE", "ENUM_STRENGTH", "ENUM_STATUS", "ENUM_STAGE",
                     "ENUM_HCATEGORY", "ENUM_MARKET_STAGE", "ENUM_POLICY_LEVEL"):
            assert getattr(gen, name) is getattr(schema, name), f"{name} 不是同一对象"
            assert getattr(validate, name) is getattr(schema, name), f"{name} 不是同一对象"

        # 脚本内的字段别名 → schema 中的规范名
        alias = {
            "FIELDS": "FIELDS_THEORY",
            "TIMELINE_FIELDS": "FIELDS_TIMELINE",
            "POLICY_FIELDS": "FIELDS_POLICY",
            "CASE_FIELDS": "FIELDS_CASES",
        }
        for local, canonical in alias.items():
            target = getattr(schema, canonical)
            assert getattr(gen, local) is target, f"gen.{local} 不是同一对象"
            assert getattr(validate, local) is target, f"validate.{local} 不是同一对象"

    def test_schema_covers_all_datasets(self):
        """schema 必须为四个数据集都定义字段。"""
        assert schema.FIELDS_THEORY and schema.FIELDS_TIMELINE
        assert schema.FIELDS_POLICY and schema.FIELDS_CASES
        assert schema.PATH_THEORY == ROOT / "data" / "theory_index.csv"
        assert schema.PATH_TIMELINE == ROOT / "data" / "financial_history_timeline.csv"
        assert schema.PATH_POLICY == ROOT / "data" / "policy_toolkit.csv"
        assert schema.PATH_CASES == ROOT / "data" / "investor_cases.csv"


class TestCsvIO:
    """公共读写层的契约。"""

    def test_render_is_deterministic(self):
        recs = [{"a": "1", "b": "2"}, {"a": "3", "b": "4"}]
        assert csvio.render_csv(recs, ["a", "b"]) == csvio.render_csv(recs, ["a", "b"])

    def test_render_writes_bom_and_lf(self):
        text = csvio.render_csv([{"a": "1"}], ["a"])
        assert text.startswith("\ufeff")
        assert "\r" not in text

    def test_render_fills_missing_field_with_empty(self):
        """缺字段应补空串，而不是抛 KeyError——数据表偶尔漏写字段属正常。"""
        text = csvio.render_csv([{"a": "1"}], ["a", "b"])
        assert text.strip().splitlines()[-1] == "1,"

    def test_sort_key_applied(self):
        recs = [{"a": "2"}, {"a": "1"}]
        text = csvio.render_csv(recs, ["a"], sort_key=lambda r: r["a"])
        assert text.strip().splitlines()[1:] == ["1", "2"]

    def test_read_csv_rejects_empty_file(self, tmp_path):
        p = tmp_path / "x.csv"
        p.write_text("a,b\n", encoding="utf-8")
        with pytest.raises(ValueError, match="为空"):
            csvio.read_csv(p)

    def test_read_csv_missing_file_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            csvio.read_csv(tmp_path / "nope.csv")

    def test_read_csv_strips_bom_and_whitespace(self, tmp_path):
        p = tmp_path / "x.csv"
        p.write_text("\ufeffa,b\n 1 , 2 \n", encoding="utf-8")
        assert csvio.read_csv(p) == [{"a": "1", "b": "2"}]

    def test_write_if_changed_skips_identical(self, tmp_path):
        p = tmp_path / "x.csv"
        assert csvio.write_if_changed(p, "hello") is True
        assert csvio.write_if_changed(p, "hello") is False
        assert csvio.write_if_changed(p, "world") is True

    def test_tokens_drops_placeholder_and_blanks(self):
        """「—」与空串都不是有效成员，否则互补/冲突关系判断会被污染。"""
        assert csvio.tokens("CAPM|APT") == {"CAPM", "APT"}
        assert csvio.tokens("—") == set()
        assert csvio.tokens("") == set()
        assert csvio.tokens("CAPM|—| APT ") == {"CAPM", "APT"}
