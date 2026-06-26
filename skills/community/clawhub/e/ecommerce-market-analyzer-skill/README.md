# E-commerce Market Analyzer Skill

## 📦 Skill目录结构（标准格式）

```
ecommerce-market-analyzer-skill/
├── SKILL.md                          # 核心工作流程文档（必需）
├── scripts/                          # 可执行脚本
│   └── scrape_websites.py           # Playwright爬虫主脚本
├── references/                       # 参考文档
│   ├── popup_patterns.md            # 弹窗选择器库
│   └── html_parsing_patterns.md     # HTML解析模式
├── assets/                           # 输出模板
│   └── report_template.md           # 市场分析报告模板
├── README.md                         # 本文件（使用说明）
└── SKILL_SUMMARY.md                  # 详细文档和示例
```

## 🚀 安装方法

### 方法1：复制整个文件夹到Claude skills目录
```bash
cp -r ecommerce-market-analyzer-skill ~/.claude/skills/
```

### 方法2：创建符号链接
```bash
ln -s /Users/anpuqiang/Documents/code/gitlab/scraper/ecommerce-market-analyzer-skill \
      ~/.claude/skills/ecommerce-market-analyzer-skill
```

安装后，在Claude Code中查看可用skills：
```bash
ls ~/.claude/skills/
```

## 📖 使用方法

安装后，在Claude Code中直接说：

```
"分析德国电商市场"
"Analyze UK e-commerce market"
"查找法国热门商品"
"Generate market report for US"
```

技能会自动激活并引导你完成4步工作流程：
1. Setup & Scraping - 运行爬虫脚本
2. Visual Analysis - 分析截图
3. Data Extraction - 提取HTML数据
4. Report Generation - 生成市场报告

## 🎯 触发条件

Skill会在以下情况自动激活：
- "analyze [market] e-commerce market"
- "scrape e-commerce websites"
- "find hot products in [country]"
- "analyze product trends"
- "generate market report for [region]"

## 📂 文件说明

### SKILL.md（核心）
- Skill的主要工作流程文档
- 包含YAML frontmatter（name + description）
- 4步工作流程详细说明
- 故障排查指南
- 市场配置方法

### scripts/scrape_websites.py
- Playwright自动化爬虫脚本
- 自动弹窗处理（12种类型）
- 多市场支持（德/英/美等）
- 可直接运行：`uv run python scripts/scrape_websites.py`

### references/popup_patterns.md
- Cookie同意弹窗选择器（德语/英语/通用）
- 区域选择器模式
- Newsletter关闭按钮
- 平台特定选择器（如Kleinanzeigen）

### references/html_parsing_patterns.md
- JSON-LD schema提取策略
- 平台特定解析规则（Amazon、eBay、REWE、Otto等）
- 价格标准化工具
- 兜底提取策略

### assets/report_template.md
- 结构化市场分析报告模板
- 包含所有章节占位符
- 支持双语输出
- 复制填充即可使用

## 💡 实际应用案例

基于本项目的德国市场分析：

**输入：** 25个德国电商网站
```python
WEBSITES = [
    "amazon.de", "ebay.de", "otto.de", "lidl.de",
    "rewe.de", "zalando.de", "ikea.com", ...
]
```

**成果：**
- ✅ 成功率92%（23/25网站）
- ✅ 弹窗处理100%（12个网站）
- ✅ 提取验证价格（Nutella饼干 2,69€）
- ✅ 13大商品类别识别
- ✅ 600+行综合报告

**输出文件：**
```
screenshots_clean/
├── *.png          # 23张清晰截图
├── *.html         # 23个HTML文件
└── ...

德国热门商品综合分析报告_2026.md  # 最终报告
```

## 🌍 支持的市场

### 预配置
- 🇩🇪 **德国** (de-DE, Europe/Berlin)
- 🇬🇧 **英国** (en-GB, Europe/London)
- 🇺🇸 **美国** (en-US, America/New_York)

### 自定义其他市场
在脚本中修改：
```python
context = await browser.new_context(
    locale="fr-FR",              # 法语
    timezone_id="Europe/Paris",  # 巴黎时区
)
```

## 📈 预期成功率

基于实际测试：
- **网站爬取：** 85-95%
- **弹窗处理：** 90-100%（已知模式）
- **数据提取：** 70-90%（视HTML复杂度）
- **报告生成：** 100%

常见失败原因：
- 反爬虫机制（CAPTCHA、验证码）
- HTTP/2协议限制
- 动态加载超时

## 🛠️ 技术要求

### 运行环境
- Python 3.12+
- Playwright 1.58+
- uv（虚拟环境管理）
- 2GB+磁盘空间

### 安装依赖
```bash
# 使用uv创建虚拟环境
uv venv
source .venv/bin/activate

# 安装依赖
uv pip install playwright
playwright install chromium
```

## 🎓 技能学习价值

这个Skill封装了以下专业知识：

1. **Web自动化**
   - Playwright浏览器控制
   - 页面等待策略
   - 元素定位技术

2. **反爬虫对抗**
   - Cookie弹窗处理
   - User-Agent伪装
   - 地区本地化设置

3. **数据提取**
   - 正则表达式匹配
   - JSON-LD schema解析
   - 多策略兜底机制

4. **市场分析**
   - 产品分类方法
   - 价格趋势识别
   - 竞品对比分析

5. **技术文档**
   - Skill标准格式
   - 渐进式披露设计
   - 可复用资源组织

## 📝 开发与维护

### 添加新平台支持
1. 访问目标网站，识别弹窗模式
2. 在 `references/popup_patterns.md` 添加选择器
3. 分析HTML结构，添加解析规则到 `references/html_parsing_patterns.md`
4. 测试并更新文档

### 调试技巧
```python
# 在脚本中启用headful模式查看浏览器
browser = await p.chromium.launch(headless=False)

# 增加等待时间调试
await asyncio.sleep(10)  # 观察页面状态
```

### 贡献改进
- 发现新的弹窗类型→更新 popup_patterns.md
- 支持新平台→更新 html_parsing_patterns.md
- 优化报告模板→更新 report_template.md

## 🔒 使用规范

### 道德准则
✅ **允许：**
- 市场研究和竞品分析
- 价格监控（个人使用）
- 学习和教育目的

❌ **禁止：**
- 商业转售抓取数据
- 高频率恶意请求
- 绕过付费墙内容
- 侵犯用户隐私

### 最佳实践
1. 遵守 robots.txt
2. 设置合理请求间隔（脚本已内置2秒延迟）
3. 尊重网站服务条款
4. 不抓取敏感个人信息

## 📚 相关文档

- **SKILL_SUMMARY.md** - 完整使用指南和案例
- **弹窗处理报告.md** - 技术实现细节（项目根目录）
- **德国热门商品综合分析报告_2026.md** - 完整输出示例

## 🤝 反馈与支持

遇到问题时：
1. 检查 SKILL.md 的"Troubleshooting"章节
2. 查看 references/ 目录下的参考文档
3. 阅读 SKILL_SUMMARY.md 的详细示例

## 📄 版本信息

- **版本：** 1.0
- **创建日期：** 2026-03-19
- **基于项目：** 德国电商市场分析
- **测试状态：** 已验证（23个网站，92%成功率）

---

**这是一个标准的Claude Code Skill目录**
- 符合官方Skill规范
- 包含必需的SKILL.md和可选的scripts/references/assets
- 可直接安装到 ~/.claude/skills/
