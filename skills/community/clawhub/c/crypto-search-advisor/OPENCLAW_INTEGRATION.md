# OpenClaw 集成指南

## 架构

```
用户输入 → OpenClaw Agent
              │
              ├─ web_search ────── 搜索行情（系统搜索能力）
              ├─ image_recognition ── 识别截图（系统图像能力）
              └─ crypto_advisor.py ── 全部分析逻辑（单脚本）
                    │
                    ├─ classify_coin()      币种分类
                    ├─ detect_conflict()    价格冲突检测
                    ├─ assess_quality()     截图质量评估
                    ├─ quick_scan_text()    秒级风险警报
                    ├─ compute_indicator_signals() 指标信号
                    ├─ calculate_input_reliability() 数据可信度
                    ├─ analyze()            完整深度分析
                    └─ format_*_output()   格式化输出
```

## 调用方式

### CLI（推荐）

```bash
# 币种分类
python scripts/crypto_advisor.py classify --symbol BTC

# 交易意图检测
python scripts/crypto_advisor.py detect_trade_intent --message "帮我买BTC"

# 价格冲突检测
python scripts/crypto_advisor.py conflict \
  --screenshot-price 65000 \
  --search-min 64000 \
  --search-max 66000

# 完整分析
python scripts/crypto_advisor.py analyze \
  --symbol BTC \
  --real-min 96800 \
  --real-max 97200
```

### Python Import

```python
import sys
sys.path.insert(0, './scripts')
from crypto_advisor import classify_coin, detect_conflict, analyze

# 币种分类
result = classify_coin('BTC')
print(result['category'])  # mainstream

# 完整分析
analysis = analyze(symbol='BTC', real_min=96800, real_max=97200)
print(analysis)
```

## 依赖

```bash
pip install -r requirements.txt
# 即 pip install requests>=2.28.0
```

## 测试

```bash
cd scripts
pytest tests/ -v
# 91 tests, all passing
```
