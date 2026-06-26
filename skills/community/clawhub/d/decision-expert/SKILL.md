---
name: decision-expert
description: A decision support skill that helps users analyze options, weigh trade-offs, and apply decision frameworks (SWOT, decision matrix, pros/cons, etc.) across various scenarios like shopping, career, investment, and daily life.
---

# Decision Expert Skill

A comprehensive decision support system that helps users make better choices by providing structured analysis, decision frameworks, and objective evaluation of options.

## When to Use This Skill

Use this skill when the user:

- Asks for help making a decision (e.g., "Should I buy X or Y?", "Which job should I take?", "Is this investment good?")
- Wants to weigh pros and cons of different options
- Needs a structured framework to evaluate choices
- Is facing a complex decision with multiple factors
- Wants to document and track their decision-making process
- Needs to compare alternatives systematically

Common trigger phrases:
- "帮我决定..." (help me decide...)
- "哪个更好？" (which is better?)
- "应该选哪个？" (which should I choose?)
- "买什么手机？" (what phone should I buy?)
- "该不该换工作？" (should I change jobs?)
- "投资这个项目好吗？" (is this investment good?)

## Command Design

The skill provides a CLI command `decision` with the following structure:

### Basic Commands

```bash
# Get help and list available frameworks
decision help

# Analyze a decision with automatic framework selection
decision analyze "买什么手机" --options "iPhone 15, Samsung Galaxy S24, Google Pixel 8"

# Create a pros/cons list
decision pros-cons "换工作到上海" --pros "高薪, 发展机会" --cons "高房价, 离家远"

# Use a specific decision framework
decision swot "开咖啡店" --strengths "热爱咖啡, 有经验" --weaknesses "资金有限" --opportunities "社区需求" --threats "竞争激烈"

# Create a decision matrix
decision matrix "买车" --criteria "价格, 油耗, 安全性, 空间" --options "SUV, 轿车, 电动车" --weights "30, 20, 25, 25"

# Compare multiple options
decision compare "度假地点" --options "巴厘岛, 日本, 欧洲" --factors "预算, 时间, 兴趣, 便利性"
```

### Interactive Mode

```bash
# Start an interactive decision-making session
decision interactive

# Guided decision workflow
decision guide "职业选择"
```

### Scenario-Specific Commands

```bash
# Shopping decisions
decision shopping "笔记本电脑" --budget 8000 --needs "编程, 设计, 便携"

# Career decisions  
decision career "offer选择" --offers "公司A: 高薪但忙, 公司B: 平衡但薪低"

# Investment decisions
decision investment "买房 vs 租房" --timeframe "5年" --risk "中等"

# Daily life decisions
decision daily "早上锻炼还是晚上锻炼" --factors "精力水平, 时间安排, 坚持难度"
```

### Output Formats

```bash
# Export decision analysis to different formats
decision analyze "买手机" --format markdown --output decision.md
decision analyze "买手机" --format json --output decision.json
decision analyze "买手机" --format table --display
```

## Decision Frameworks Design

The skill implements several proven decision-making frameworks:

### 1. Pros & Cons List (利弊分析)
- Simple listing of advantages and disadvantages
- Weighted scoring option
- Visual balance display

### 2. SWOT Analysis (SWOT分析)
- Strengths, Weaknesses, Opportunities, Threats
- Internal vs. external factors
- Strategic implications

### 3. Decision Matrix (决策矩阵)
- Multiple criteria with weights
- Option scoring (1-5 or 1-10 scale)
- Weighted total calculation
- Sensitivity analysis

### 4. Cost-Benefit Analysis (成本效益分析)
- Quantitative evaluation of costs vs. benefits
- ROI calculation
- Time value of money consideration

### 5. Decision Tree (决策树)
- Branching scenarios with probabilities
- Expected value calculation
- Risk assessment

### 6. Eisenhower Matrix (艾森豪威尔矩阵)
- Urgent vs. important classification
- Priority setting
- Time management decisions

### 7. Weighted Scoring Model (加权评分模型)
- Custom criteria with importance weights
- Objective scoring rubrics
- Comparative analysis

### 8. Six Thinking Hats (六顶思考帽)
- Parallel thinking framework
- Multiple perspective consideration
- Emotionally intelligent decision making

### 9. Pareto Analysis (帕累托分析)
- 80/20 principle application
- Focus on high-impact factors
- Resource allocation decisions

### 10. Scenario Planning (情景规划)
- Multiple future scenarios
- Contingency planning
- Robustness testing

## Supported Decision Scenarios

### Shopping & Purchases (购物决策)
- Electronics (phones, laptops, gadgets)
- Vehicles (cars, bikes)
- Real estate (buying, renting)
- Appliances and home goods
- Fashion and personal items
- Subscription services

### Career & Education (职业与教育)
- Job offers and career moves
- Education paths and courses
- Skill development investments
- Business opportunities
- Freelance vs. employment
- Promotion decisions

### Investment & Finance (投资与财务)
- Stock and investment choices
- Real estate investments  
- Business investments
- Savings and retirement planning
- Loan and debt decisions
- Insurance choices

### Daily Life & Personal (日常生活)
- Health and fitness choices
- Relationship decisions
- Time management
- Habit formation
- Travel planning
- Home improvement

### Business & Strategy (商业与战略)
- Product development choices
- Market entry decisions
- Hiring and team building
- Vendor selection
- Technology adoption
- Strategic partnerships

### Project & Technical (项目与技术)
- Technology stack selection
- Architecture decisions
- Tool and platform choices
- Implementation approaches
- Resource allocation
- Risk management

## Technical Implementation Suggestions

### Core Architecture

```
decision-expert/
├── cli/                    # Command-line interface
│   ├── index.js           # Main CLI entry point
│   ├── commands/          # Individual command implementations
│   └── utils/             # CLI utilities
├── lib/                   # Core decision logic
│   ├── frameworks/        # Decision framework implementations
│   ├── models/           # Data models (Decision, Option, Criterion, etc.)
│   ├── analysis/         # Analysis algorithms
│   └── visualization/    # Output formatting and display
├── scenarios/            # Scenario-specific logic
│   ├── shopping.js
│   ├── career.js
│   ├── investment.js
│   └── daily.js
├── storage/              # Decision history and templates
│   ├── history/
│   ├── templates/
│   └── exports/
└── interactive/          # Interactive session manager
    ├── prompts.js
    ├── workflows.js
    └── ui.js
```

### Key Implementation Components

1. **Decision Engine**: Core logic for applying frameworks and calculating scores
2. **Framework Library**: Modular implementations of each decision framework
3. **Scenario Adapters**: Specialized logic for different decision domains
4. **Interactive Shell**: Guided workflow for complex decisions
5. **Storage System**: Save/load decisions, templates, and history
6. **Export System**: Multiple output formats (Markdown, JSON, HTML, CSV)

### Dependencies

```json
{
  "dependencies": {
    "commander": "^11.0.0",      // CLI framework
    "inquirer": "^9.2.0",        // Interactive prompts
    "chalk": "^5.3.0",           // Terminal styling
    "cli-table3": "^0.6.3",      // Table displays
    "lodash": "^4.17.21",        // Utility functions
    "yaml": "^2.3.0",            // YAML parsing for templates
    "json2csv": "^6.0.0",        // CSV export
    "markdown-table": "^3.0.3"   // Markdown table generation
  },
  "devDependencies": {
    "jest": "^29.7.0",           // Testing
    "eslint": "^8.50.0"          // Code quality
  }
}
```

### API Design

```javascript
// Core decision API
const decisionEngine = {
  createDecision(description, options, criteria),
  applyFramework(decision, framework, params),
  calculateScores(decision, weights),
  generateRecommendation(decision),
  exportDecision(decision, format)
};

// Framework implementations
const frameworks = {
  prosCons: { analyze(options, pros, cons) },
  swot: { analyze(strengths, weaknesses, opportunities, threats) },
  decisionMatrix: { analyze(options, criteria, weights, scores) },
  costBenefit: { analyze(costs, benefits, timeframe, discountRate) }
};
```

### Interactive Features

1. **Step-by-step guidance**: Walk users through decision process
2. **Template system**: Pre-built decision templates for common scenarios
3. **History tracking**: Record and learn from past decisions
4. **Collaboration support**: Share decisions and get input from others
5. **Reminder system**: Follow up on decision outcomes
6. **Learning system**: Improve suggestions based on user preferences

## File Structure Recommendations

### Minimum Viable Structure

```
~/.openclaw/workspace/skills/decision-expert/
├── SKILL.md                      # This file
├── README.md                     # User documentation
├── package.json                  # Node.js package definition
├── cli.js                        # Main CLI entry point
├── lib/
│   ├── index.js                  # Main library export
│   ├── decision-engine.js        # Core decision logic
│   ├── frameworks/               # Framework implementations
│   │   ├── pros-cons.js
│   │   ├── swot.js
│   │   ├── decision-matrix.js
│   │   └── index.js
│   └── utils/
│       ├── formatters.js         # Output formatting
│       └── validators.js         # Input validation
├── templates/                    # Decision templates
│   ├── shopping/
│   ├── career/
│   └── investment/
├── examples/                     # Example usage
│   ├── phone-decision.md
│   ├── job-offer-decision.json
│   └── investment-analysis.csv
└── scripts/                      # Utility scripts
    ├── setup.sh                  # Installation script
    └── test-decision.sh          # Test script
```

### Advanced Structure (Full Implementation)

```
~/.openclaw/workspace/skills/decision-expert/
├── .github/                      # GitHub workflows
│   └── workflows/
│       └── test.yml
├── bin/                          # Executable scripts
│   └── decision
├── src/                          # TypeScript source
│   ├── cli/
│   ├── lib/
│   ├── types/
│   └── utils/
├── tests/                        # Comprehensive test suite
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── docs/                         # Detailed documentation
│   ├── frameworks/
│   ├── scenarios/
│   └── api/
├── config/                       # Configuration files
│   ├── default-config.yaml
│   └── scenario-config.yaml
├── data/                         # Sample data and templates
│   ├── templates/
│   ├── examples/
│   └── benchmarks/
├── public/                       # Web assets (if any)
│   ├── css/
│   └── js/
└── dist/                         # Compiled output (for TypeScript)
```

## Integration with OpenClaw

The decision assistant skill can integrate with OpenClaw in several ways:

1. **Direct CLI usage**: Users run `decision` commands directly
2. **Agent integration**: Pearl can call the decision assistant when users need help with decisions
3. **API mode**: Other skills can use the decision engine via JavaScript API
4. **Template sharing**: Decision templates can be shared across the OpenClaw ecosystem

### Example Agent Integration

```javascript
// Pearl agent can use the decision assistant like this:
const { analyzeDecision } = require('decision-expert');

async function helpWithDecision(userQuery, options) {
  const analysis = await analyzeDecision(userQuery, options);
  return `Based on my analysis: ${analysis.recommendation}\n\n${analysis.summary}`;
}
```

## Getting Started

### Quick Start

```bash
# Install the skill
npx skills add <owner/repo>@decision-expert

# Or install locally for development
cd ~/.openclaw/workspace/skills/decision-expert
npm install
npm link  # Makes 'decision' command available globally

# Test with a simple decision
decision help
decision analyze "晚饭吃什么" --options "中餐, 西餐, 日料"
```

### Development Setup

```bash
# Clone and setup
git clone <repository> ~/.openclaw/workspace/skills/decision-expert
cd ~/.openclaw/workspace/skills/decision-expert
npm install

# Run tests
npm test

# Build (if TypeScript)
npm run build

# Run in development mode
node cli.js help
```

## Learning Resources

- **Decision Theory**: Understanding rational choice models
- **Behavioral Economics**: Cognitive biases in decision making
- **Operations Research**: Quantitative decision analysis methods
- **Psychology of Choice**: How people actually make decisions
- **Business Strategy**: Strategic decision frameworks

## Contributing

This skill welcomes contributions! Areas needing improvement:

1. Additional decision frameworks
2. More scenario-specific templates
3. Better visualization options
4. Integration with other tools (calendar, task managers, etc.)
5. Multi-language support
6. Accessibility improvements

## License

[MIT License] - Open for use and modification within the OpenClaw ecosystem.

---

*"Good decisions come from experience, and experience comes from bad decisions."* - This skill helps you get more experience without the bad decisions.