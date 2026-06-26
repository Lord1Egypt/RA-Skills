#!/usr/bin/env python3
"""
DeckCraft v6.0.0 — Extended Chart Tests

9 tests, one per new chart type.
Validates that each chart method:
  1. Creates a valid PPTX (no crash)
  2. Produces exactly 1 slide
  3. Raises ValueError on bad input

Run:
    pytest tests/test_charts_extended.py -v
"""
import sys, os, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import pytest
from pptx import Presentation
from engine import DeckEngine


@pytest.fixture
def engine():
    return DeckEngine(theme_name="business", canvas="16:9")


def _save_and_verify(engine, tmp_path):
    """Save PPTX and verify it's valid."""
    out = os.path.join(tmp_path, "test.pptx")
    engine.save(out)
    assert os.path.isfile(out)
    assert engine.slide_count == 1
    # Verify it can be opened
    prs = Presentation(out)
    assert len(prs.slides) == 1
    return out


# ── 1. Funnel ─────────────────────────────────────────────────────

def test_chart_funnel(engine, tmp_path):
    engine.chart_funnel(
        title="转化漏斗",
        stages=["访客", "注册", "试用", "付费", "续费"],
        values=[10000, 5000, 2000, 800, 600],
    )
    _save_and_verify(engine, str(tmp_path))


def test_chart_funnel_empty_raises(engine):
    with pytest.raises(ValueError):
        engine.chart_funnel(title="X", stages=[], values=[])


def test_chart_funnel_mismatch_raises(engine):
    with pytest.raises(ValueError):
        engine.chart_funnel(title="X", stages=["A", "B"], values=[1])


# ── 2. Gantt ──────────────────────────────────────────────────────

def test_chart_gantt(engine, tmp_path):
    engine.chart_gantt(
        title="项目甘特图",
        tasks=[
            {"name": "调研", "start": "2026-01-01", "end": "2026-01-15"},
            {"name": "设计", "start": "2026-01-10", "end": "2026-02-01"},
            {"name": "开发", "start": "2026-01-20", "end": "2026-03-01"},
        ],
    )
    _save_and_verify(engine, str(tmp_path))


def test_chart_gantt_empty_raises(engine):
    with pytest.raises(ValueError):
        engine.chart_gantt(title="X", tasks=[])


# ── 3. SWOT ───────────────────────────────────────────────────────

def test_chart_swot(engine, tmp_path):
    engine.chart_swot(
        title="SWOT 分析",
        strengths=["品牌知名度高", "技术领先"],
        weaknesses=["成本偏高"],
        opportunities=["新市场", "政策支持"],
        threats=["竞争加剧"],
    )
    _save_and_verify(engine, str(tmp_path))


def test_chart_swot_all_empty_raises(engine):
    with pytest.raises(ValueError):
        engine.chart_swot(title="X", strengths=[], weaknesses=[],
                         opportunities=[], threats=[])


# ── 4. Porter ─────────────────────────────────────────────────────

def test_chart_porter(engine, tmp_path):
    engine.chart_porter(
        title="波特五力分析",
        forces={
            "new_entrants": "进入门槛中等",
            "suppliers": "供应商集中度高",
            "buyers": "客户议价能力强",
            "substitutes": "替代品较少",
            "rivalry": "竞争激烈",
        },
    )
    _save_and_verify(engine, str(tmp_path))


def test_chart_porter_empty_raises(engine):
    with pytest.raises(ValueError):
        engine.chart_porter(title="X", forces={})


def test_chart_porter_missing_key_raises(engine):
    with pytest.raises(ValueError):
        engine.chart_porter(title="X", forces={"new_entrants": "a"})


# ── 5. Sankey ─────────────────────────────────────────────────────

def test_chart_sankey(engine, tmp_path):
    engine.chart_sankey(
        title="流量分布",
        nodes=["搜索", "社交", "直接访问", "转化", "流失"],
        links=[
            {"source": "搜索", "target": "转化", "value": 10},
            {"source": "搜索", "target": "流失", "value": 5},
            {"source": "社交", "target": "转化", "value": 8},
            {"source": "直接访问", "target": "转化", "value": 3},
        ],
    )
    _save_and_verify(engine, str(tmp_path))


def test_chart_sankey_empty_raises(engine):
    with pytest.raises(ValueError):
        engine.chart_sankey(title="X", nodes=[], links=[])


# ── 6. Heatmap ────────────────────────────────────────────────────

def test_chart_heatmap(engine, tmp_path):
    engine.chart_heatmap(
        title="季度产品销售热力图",
        rows=["Q1", "Q2", "Q3", "Q4"],
        cols=["产品A", "产品B", "产品C"],
        values=[[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]],
    )
    _save_and_verify(engine, str(tmp_path))


def test_chart_heatmap_empty_raises(engine):
    with pytest.raises(ValueError):
        engine.chart_heatmap(title="X", rows=[], cols=[], values=[])


def test_chart_heatmap_mismatch_raises(engine):
    with pytest.raises(ValueError):
        engine.chart_heatmap(title="X", rows=["A", "B"], cols=["X"],
                             values=[[1]])  # 2 rows expected, 1 given


# ── 7. Radar ──────────────────────────────────────────────────────

def test_chart_radar(engine, tmp_path):
    engine.chart_radar(
        title="产品对比雷达图",
        axes=["性能", "价格", "易用", "支持", "生态"],
        series_data=[[8, 7, 9, 6, 8], [6, 9, 7, 8, 5]],
        series_names=["产品A", "产品B"],
    )
    _save_and_verify(engine, str(tmp_path))


def test_chart_radar_empty_raises(engine):
    with pytest.raises(ValueError):
        engine.chart_radar(title="X", axes=[], series_data=[])


def test_chart_radar_dimension_mismatch(engine):
    with pytest.raises(ValueError):
        engine.chart_radar(title="X", axes=["A", "B", "C"],
                           series_data=[[1, 2]])  # expected 3


# ── 8. Treemap ────────────────────────────────────────────────────

def test_chart_treemap(engine, tmp_path):
    engine.chart_treemap(
        title="产品收入占比",
        items=[("产品A", 50), ("产品B", 30), ("产品C", 20)],
    )
    _save_and_verify(engine, str(tmp_path))


def test_chart_treemap_empty_raises(engine):
    with pytest.raises(ValueError):
        engine.chart_treemap(title="X", items=[])


# ── 9. Waterfall ──────────────────────────────────────────────────

def test_chart_waterfall(engine, tmp_path):
    engine.chart_waterfall(
        title="利润瀑布图",
        categories=["期初", "收入", "成本", "税费", "期末"],
        values=[100, 50, -30, -10, 110],
        is_total=[True, False, False, False, True],
    )
    _save_and_verify(engine, str(tmp_path))


def test_chart_waterfall_empty_raises(engine):
    with pytest.raises(ValueError):
        engine.chart_waterfall(title="X", categories=[], values=[])


def test_chart_waterfall_mismatch_raises(engine):
    with pytest.raises(ValueError):
        engine.chart_waterfall(title="X", categories=["A", "B"], values=[1])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
