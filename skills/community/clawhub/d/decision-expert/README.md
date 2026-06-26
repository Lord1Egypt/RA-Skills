# Decision Expert Skill

A decision support tool for OpenClaw that helps users make better choices through structured analysis and proven decision frameworks.

## Quick Start

```bash
# Basic decision analysis
decision analyze "买什么手机" --options "iPhone 15, Samsung Galaxy S24, Google Pixel 8"

# Pros and cons analysis
decision pros-cons "换工作到上海" --pros "高薪, 发展机会" --cons "高房价, 离家远"

# Decision matrix with custom criteria
decision matrix "买车" --criteria "价格, 油耗, 安全性, 空间" --options "SUV, 轿车, 电动车" --weights "30, 20, 25, 25"
```

## Features

### Multiple Decision Frameworks
- **Pros & Cons**: Simple advantages/disadvantages listing
- **SWOT Analysis**: Strengths, Weaknesses, Opportunities, Threats
- **Decision Matrix**: Weighted criteria scoring
- **Cost-Benefit Analysis**: Quantitative financial evaluation
- **Decision Tree**: Scenario branching with probabilities
- **Eisenhower Matrix**: Urgent vs. important prioritization

### Scenario Support
- **Shopping Decisions**: Electronics, vehicles, real estate
- **Career Choices**: Job offers, education paths, promotions
- **Investment Analysis**: Stocks, real estate, business opportunities
- **Daily Life**: Health, relationships, time management
- **Business Strategy**: Product development, hiring, partnerships

### Interactive Guidance
```bash
# Start interactive decision session
decision interactive

# Guided workflow for complex decisions
decision guide "职业选择"
```

### Export Options
- Markdown reports
- JSON data
- CSV tables
- HTML visualizations

## Installation

```bash
# Install via skills CLI
npx skills add <owner/repo>@decision-expert

# Or install locally
cd ~/.openclaw/workspace/skills/decision-expert
npm install
npm link
```

## Usage Examples

### Example 1: Phone Purchase Decision
```bash
decision analyze "买什么手机" \
  --options "iPhone 15 Pro, Samsung S24 Ultra, Google Pixel 8 Pro" \
  --criteria "价格, 相机, 电池, 系统, 保值" \
  --weights "25, 30, 20, 15, 10" \
  --format table
```

### Example 2: Career Move Analysis
```bash
decision swot "换工作到科技公司" \
  --strengths "技术强项, 学习能力" \
  --weaknesses "缺乏大公司经验" \
  --opportunities "行业增长, 技能提升" \
  --threats "工作压力, 竞争激烈" \
  --output career-analysis.md
```

### Example 3: Investment Comparison
```bash
decision compare "投资选项" \
  --options "股票基金, 房地产, 数字货币, 债券" \
  --factors "风险, 收益, 流动性, 时间投入" \
  --timeframe "5年"
```

## Decision Frameworks Explained

### Decision Matrix
The most powerful tool for complex decisions with multiple criteria:

1. Define criteria (factors that matter)
2. Assign weights (importance percentages)
3. Score each option on each criterion (1-10)
4. Calculate weighted scores
5. Compare results

### SWOT Analysis
Best for strategic decisions:
- **Strengths**: Internal advantages
- **Weaknesses**: Internal limitations  
- **Opportunities**: External positive factors
- **Threats**: External challenges

### Pros & Cons
Simplest framework for binary decisions:
- List all advantages
- List all disadvantages
- Optionally assign importance weights
- See which side outweighs

## Integration with OpenClaw

The decision assistant integrates seamlessly with Pearl (OpenClaw's main agent):

1. **Direct CLI access**: Users can run commands directly
2. **Agent assistance**: Pearl can invoke decision analysis when users need help
3. **Template sharing**: Common decision templates available across the ecosystem
4. **History tracking**: Learn from past decisions

## Development

```bash
# Clone repository
git clone <url> ~/.openclaw/workspace/skills/decision-expert

# Install dependencies
npm install

# Run tests
npm test

# Build (if TypeScript)
npm run build

# Run in development
node cli.js help
```

## Contributing

We welcome contributions! Areas needing work:

1. Additional decision frameworks
2. More scenario templates
3. Better visualization
4. Integration with calendar/task apps
5. Multi-language support

## License

MIT License - Free to use and modify within the OpenClaw ecosystem.

---

*"In any moment of decision, the best thing you can do is the right thing, the next best thing is the wrong thing, and the worst thing you can do is nothing."* - Theodore Roosevelt