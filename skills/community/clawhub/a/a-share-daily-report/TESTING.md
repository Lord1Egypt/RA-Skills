
# A股日报 - 测试方案

&gt; 本文档定义项目的测试策略、测试用例和验证标准

---

## 🎯 测试策略

| 测试类型 | 说明 | 覆盖率目标 |
|---------|------|-----------|
| **单元测试** | 各模块独立测试 | ≥ 80% |
| **集成测试** | 模块间协作测试 | 完整流程 |
| **端到端测试** | 从数据采集到发布完整流程 | 每日验证 |

---

## 🔧 测试环境

### Python环境
```bash
# 激活venv
source /Users/yibiao/.openclaw/workspace-trader/venv/bin/activate

# 安装测试依赖
python3 -m pip install pytest pytest-cov pytest-mock
```

### 测试数据目录
```
tests/
├── __init__.py
├── fixtures/           # 测试夹具
│   ├── sample_index_data.json
│   ├── sample_sentiment_data.json
│   └── sample_news_data.json
├── test_data_fetcher.py
├── test_analyzer.py
├── test_renderer.py
├── test_publisher.py
└── test_integration.py
```

---

## 🧪 单元测试用例

### 1. DataFetcher 测试

```python
# tests/test_data_fetcher.py
import pytest
from scripts.data_fetcher import DataFetcher

class TestDataFetcher:
    @pytest.fixture
    def config(self):
        return {
            "data_sources": {
                "akshare": {"enabled": True, "cache_ttl": 3600},
                "sina": {"enabled": True}
            }
        }

    @pytest.fixture
    def fetcher(self, config):
        return DataFetcher(config)

    def test_get_index_data_success(self, fetcher):
        """测试获取指数数据成功"""
        result = fetcher.get_index_data("000001.SH", "2026-03-27")
        assert result["success"] is True
        assert "close" in result["data"]
        assert "change_pct" in result["data"]

    def test_get_index_data_fallback(self, fetcher, mocker):
        """测试数据源降级"""
        # mock akshare失败，应该自动降级到下一个源
        mocker.patch.object(fetcher, '_get_akshare_index', side_effect=Exception("akshare failed"))
        result = fetcher.get_index_data("000001.SH", "2026-03-27")
        assert result["success"] is True  # 降级后应该成功

    def test_get_market_sentiment(self, fetcher):
        """测试获取市场情绪数据"""
        result = fetcher.get_market_sentiment("2026-03-27")
        assert result["success"] is True
        assert "limit_up_count" in result["data"]
        assert "limit_down_count" in result["data"]

    def test_get_money_flow(self, fetcher):
        """测试获取资金流向数据"""
        result = fetcher.get_money_flow("2026-03-27")
        assert result["success"] is True
        assert "northbound" in result["data"]
        assert "main_capital" in result["data"]

    def test_get_us_market(self, fetcher):
        """测试获取美股数据"""
        result = fetcher.get_us_market()
        assert result["success"] is True
        assert "nasdaq" in result["data"]["indices"]
        assert "sp500" in result["data"]["indices"]

    def test_get_news(self, fetcher):
        """测试获取新闻数据"""
        result = fetcher.get_news("2026-03-27", limit=10)
        assert result["success"] is True
        assert len(result["data"]) &lt;= 10
```

### 2. Analyzer 测试

```python
# tests/test_analyzer.py
import pytest
from scripts.analyzer import Analyzer

class TestAnalyzer:
    @pytest.fixture
    def sample_data(self):
        return {
            "index": {"000001.SH": {"close": 3050.25, "change_pct": 0.34}},
            "sentiment": {"limit_up_count": 85, "limit_down_count": 12},
            "money_flow": {"northbound": {"total_net_inflow": 4430000000}}
        }

    @pytest.fixture
    def watchlist(self):
        return [
            {"code": "600519.SH", "name": "贵州茅台"},
            {"code": "300750.SZ", "name": "宁德时代"}
        ]

    @pytest.fixture
    def analyzer(self):
        return Analyzer({})

    def test_generate_summary_morning(self, analyzer, sample_data):
        """测试生成早报30秒总览"""
        result = analyzer.generate_summary(sample_data, mode="morning")
        assert result["success"] is True
        assert "one_sentence" in result["data"]
        assert "core_opportunities" in result["data"]
        assert "risk_warnings" in result["data"]

    def test_generate_summary_evening(self, analyzer, sample_data):
        """测试生成晚报30秒总览"""
        result = analyzer.generate_summary(sample_data, mode="evening")
        assert result["success"] is True
        assert "one_sentence" in result["data"]

    def test_analyze_watchlist_morning(self, analyzer, sample_data, watchlist):
        """测试早报自选股分析"""
        result = analyzer.analyze_watchlist_morning(sample_data, watchlist)
        assert result["success"] is True
        assert len(result["data"]) == len(watchlist)
        for item in result["data"]:
            assert "view" in item  # bullish/bearish/sideways
            assert "reason" in item

    def test_generate_trading_strategy(self, analyzer, sample_data):
        """测试交易策略生成"""
        result = analyzer.generate_trading_strategy(sample_data)
        assert result["success"] is True
        assert result["data"]["strategy"] in ["offensive", "defensive", "waiting"]
        assert 0 &lt;= result["data"]["confidence"] &lt;= 1

    def test_classify_news(self, analyzer):
        """测试新闻重要性分级"""
        news_list = [
            {"title": "央行降准", "content": "..."},
            {"title": "某公司年报", "content": "..."},
            {"title": "行业小新闻", "content": "..."}
        ]
        result = analyzer.classify_news(news_list)
        assert result["success"] is True
        for news in result["data"]:
            assert news["importance"] in ["high", "medium", "low"]
```

### 3. Renderer 测试

```python
# tests/test_renderer.py
import pytest
from scripts.renderer import Renderer

class TestRenderer:
    @pytest.fixture
    def analysis_result(self):
        return {
            "summary": {
                "one_sentence": "今日市场整体偏暖",
                "core_opportunities": ["AI产业链"],
                "risk_warnings": []
            },
            "watchlist": [],
            "strategy": {},
            "market": {}
        }

    @pytest.fixture
    def renderer(self):
        return Renderer({})

    def test_render_morning_report(self, renderer, analysis_result):
        """测试渲染早报"""
        markdown = renderer.render_morning_report(analysis_result)
        assert "# A股日报 - 早报预测版" in markdown
        assert "【30秒总览】" in markdown
        assert len(markdown) &gt; 100  # 确保有内容

    def test_render_evening_report(self, renderer, analysis_result):
        """测试渲染晚报"""
        markdown = renderer.render_evening_report(analysis_result)
        assert "# A股日报 - 晚报复盘版" in markdown
        assert "【30秒总览】" in markdown

    def test_render_with_missing_data(self, renderer):
        """测试数据缺失时的渲染"""
        incomplete_result = {
            "summary": None,  # 数据缺失
            "watchlist": [],
            "strategy": {},
            "market": {}
        }
        markdown = renderer.render_morning_report(incomplete_result)
        # 应该显示「数据获取失败」而不是崩溃
        assert "数据获取失败" in markdown or "# A股日报" in markdown
```

---

## 🔄 集成测试用例

```python
# tests/test_integration.py
import pytest
from scripts.generate_report import ReportGenerator

class TestIntegration:
    @pytest.fixture
    def generator(self):
        return ReportGenerator("config/config.yaml")

    def test_morning_report_complete_flow(self, generator):
        """测试早报完整流程"""
        # 1. 生成早报
        markdown = generator.generate_morning_report(date="2026-03-28")

        # 2. 验证输出
        assert "# A股日报 - 早报预测版" in markdown
        assert "【30秒总览】" in markdown
        assert "【昨夜今晨】" in markdown

        # 3. 验证保存
        with open("reports/morning/A股早报-20260328.md", "r", encoding="utf-8") as f:
            saved_content = f.read()
        assert saved_content == markdown

    def test_evening_report_complete_flow(self, generator):
        """测试晚报完整流程"""
        markdown = generator.generate_evening_report(date="2026-03-28")
        assert "# A股日报 - 晚报复盘版" in markdown
        assert "【今日复盘】" in markdown

    def test_data_source_fallback_integration(self, generator, mocker):
        """集成测试：数据源降级"""
        # mock主数据源失败
        mocker.patch.object(generator.data_fetcher, '_get_akshare_index', 
                           side_effect=Exception("akshare down"))

        # 应该能降级成功并生成报告
        markdown = generator.generate_morning_report(date="2026-03-28")
        assert "# A股日报" in markdown  # 不应该崩溃

    def test_non_trading_day_handling(self, generator):
        """测试非交易日处理"""
        # 2026-03-29 是周日
        markdown = generator.generate_morning_report(date="2026-03-29")
        # 应该使用最近一个交易日（03-28）的数据
        assert "2026-03-28" in markdown or "20260328" in markdown
```

---

## 🏃 运行测试

```bash
# 运行所有测试
cd /Users/yibiao/.openclaw/workspace-trader/skills/a-share-daily-report
source ../../venv/bin/activate
python -m pytest tests/ -v

# 运行特定模块测试
python -m pytest tests/test_data_fetcher.py -v

# 生成覆盖率报告
python -m pytest tests/ --cov=scripts --cov-report=html

# 运行集成测试
python -m pytest tests/test_integration.py -v --tb=short
```

---

## ✅ 验收标准

### 功能验收
- [ ] 早报能在1分钟内生成完成
- [ ] 晚报能在1分钟内生成完成
- [ ] 单数据源失败时能自动降级，报告仍能生成
- [ ] 非交易日能正确使用最近一个交易日数据
- [ ] 报告内容符合 STRUCTURE.md 规范

### 性能验收
- [ ] 数据采集时间 &lt; 30秒
- [ ] 完整报告生成时间 &lt; 60秒
- [ ] 缓存命中率 &gt; 70%

### 稳定性验收
- [ ] 连续7天无崩溃
- [ ] 数据源降级成功率 100%
- [ ] 异常数据处理成功率 100%

---

*本文档定义了完整的测试方案，开发过程中同步更新测试用例*

