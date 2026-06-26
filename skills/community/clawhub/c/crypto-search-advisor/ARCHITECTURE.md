# 工程架构

## 组件结构

```
crypto-search-advisor/
├── README.md              # 用户入门
├── RULES.md               # 核心规则（含六模分类）
├── FORMAT.md              # 输出格式规范
├── EXAMPLES.md            # CLI 示例
├── ARCHITECTURE.md        # 工程架构（本文件）
├── SKILL.md               # OpenClaw 技能入口
├── system_prompt.md       # Agent 引导
├── OPENCLAW_INTEGRATION.md # OpenClaw 集成指南
├── tools.json             # 工具配置
├── requirements.txt       # Python 依赖
├── skill.yaml             # 技能元数据
├── VERSION                # 版本号
├── scripts/
│   ├── crypto_advisor.py  # 主控脚本（classify/analyze/conflict/quality/format 全合一）
│   ├── quick_scan.py      # Quick Scan v3 秒级风险警报
│   └── tests/             # 91 项测试
└── references/
    └── archive/            # 归档（旧版独立脚本）
```

## 数据流转

```
用户输入 → Agent 意图识别
              │
              ├─ 交易意图？ → reject（拒绝，返回安全提示）
              │
              ├─ 币种？ → classify_coin()
              │
              ├─ 有截图？ → image_recognition → analyze_screenshot()
              │
              ├─ 需要搜索？ → web_search → search_crypto_info()
              │
              ├─ 有截图+搜索？ → detect_conflict() → assess_quality()
              │
              ├─ 秒级输出 → quick_scan_text()
              │
              ├─ 深度分析 → analyze() → format_*_output()
              │
              └─ → 结构化 JSON → 自然语言回复
```

## 核心函数

### classify_coin(symbol, price)

分类逻辑：
- 稳定币：符号匹配 USDT/USDC/DAI 等，或价格 0.95-1.05
- Meme币：符号匹配 DOGE/SHIB/PEPE 等，或价格 < 0.01
- 主流币：其他

### detect_conflict(screenshot_price, search_min, search_max)

冲突检测：
- 偏差 < 1% → low
- 1-3% → medium
- > 3% → high

### calculate_input_reliability(category, conflict, quality, search_data)

数据可信度评分（0-10）：
- data_credibility 25%（截图质量+冲突）
- completeness 20%（搜索完整性）
- feasibility 25%（币种类别+置信度）
- risk_controllability 20%（冲突级别）
- freshness 10%（时效性）

## CLI 接口

```bash
# 币种分类
python crypto_advisor.py classify --symbol BTC [--price 65000]

# 交易意图检测
python crypto_advisor.py detect_trade_intent --message "帮我买BTC"

# 冲突检测
python crypto_advisor.py conflict \
  --screenshot-price 65000 \
  --search-min 64000 \
  --search-max 66000

# 完整分析
python crypto_advisor.py analyze \
  --symbol BTC \
  [--screenshot-price 65000] \
  [--clarity clear|blurry] \
  [--confidence high|medium|low] \
  [--missing "volume,indicators"]
```

## 依赖

```
requests>=2.28.0
```

## 故障排查

| 问题 | 排查方法 |
|------|---------|
| 分类错误 | 检查 symbol 是否在 classify_coin() 的预设集合中 |
| 冲突检测异常 | 检查价格和单位是否为数字 |
| 质量评估为 C 级 | 检查 clarity 是否为 blurry |
| 输出 JSON 错误 | 检查输入参数是否完整 |
| 脚本找不到 | 确认 `pip install requests>=2.28.0` 已执行 |

## 安全机制

1. **交易意图拦截**：检测到 "帮我买"/"下单"/"开多" 等关键词 → 直接拒绝
2. **敏感信息保护**：索要密码/助记词 → 拒绝并提示诈骗风险
3. **免责声明**：所有输出强制包含 disclaimer 字段
4. **评分诚实性**：明确说明 input_reliability 仅评估数据质量，不预测价格
