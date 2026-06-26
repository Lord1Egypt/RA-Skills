# OpenClaw 中国招聘搜索技能

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue.svg)](https://openclaw.ai)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-green.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

专门为 OpenClaw 智能体设计的中国招聘平台搜索技能，支持 BOSS直聘、智联招聘、前程无忧三大主流平台。

## ✨ 功能特性

- 🔍 **多平台搜索**: 同时搜索三大招聘平台
- 🎯 **智能解析**: 自动提取岗位核心信息
- 📊 **结构化展示**: 表格化结果，便于比较
- ⚡ **快速响应**: 优化请求策略，提高搜索效率
- 🔧 **易于扩展**: 模块化设计，支持新平台接入
- 🇨🇳 **本土化设计**: 专门针对中国招聘市场优化

## 🚀 快速开始

### 安装依赖

```bash
pip install -r scripts/requirements.txt
```

### 基本使用

在 OpenClaw 中，智能体会自动识别以下命令格式：

```bash
# 基础搜索
搜索 Python开发 北京

# 高级搜索
搜索 Java开发 上海 15-30K 3-5年

# 平台指定搜索
搜索 boss Python 北京
搜索 智联 前端 上海
搜索 前程无忧 测试 广州
```

## 📦 技能安装

### 方法一：通过 ClawHub（推荐）

```bash
# 安装 clawhub CLI
npm install -g clawhub

# 搜索技能
clawhub search china-job-search

# 安装技能
clawhub install china-job-search
```

### 方法二：手动安装

1. 克隆或下载本仓库
2. 将整个 `china-job-search` 目录复制到 OpenClaw 技能目录：
   ```
   ~/.openclaw/workspace/skills/china-job-search/
   ```
3. 安装 Python 依赖：
   ```bash
   pip install requests beautifulsoup4 fake-useragent
   ```

## 🛠️ 技术架构

### 文件结构

```
china-job-search/
├── SKILL.md              # 技能主文档（OpenClaw识别）
├── package.json          # 技能元数据
├── README.md             # 项目说明
├── LICENSE               # MIT许可证
├── scripts/              # Python脚本目录
│   ├── run_search.py     # OpenClaw入口脚本
│   ├── job_searcher.py   # 主搜索逻辑
│   ├── boss_parser.py    # BOSS直聘解析器
│   ├── zhilian_parser.py # 智联招聘解析器
│   ├── qiancheng_parser.py # 前程无忧解析器
│   ├── config.json       # 配置文件
│   ├── requirements.txt  # 依赖列表
│   └── test_openclaw.py  # 测试脚本
└── references/           # 参考文档
    ├── API_REFERENCE.md  # API接口说明
    └── 其他文档文件
```

### 核心组件

1. **JobSearcher**: 搜索调度器，管理多平台搜索
2. **BaseParser**: 解析器基类，定义统一接口
3. **平台解析器**: 各平台专用的HTML解析器
4. **配置系统**: JSON配置文件，支持灵活调整

## 📖 使用示例

### 示例1：简单搜索

```
用户：搜索 Python开发 北京

智能体：正在搜索BOSS直聘、智联招聘、前程无忧的Python开发岗位（北京）...

结果：
| 平台 | 职位 | 公司 | 薪资 | 地点 | 经验 |
|------|------|------|------|------|------|
| BOSS直聘 | Python开发工程师 | 字节跳动 | 25-50K·15薪 | 北京 | 3-5年 |
| 智联招聘 | Python后端开发 | 腾讯 | 20-40K | 北京 | 5年以上 |
| 前程无忧 | Python开发 | 阿里巴巴 | 30-60K | 北京 | 3-8年 |
```

### 示例2：高级筛选

```
用户：搜索 Java开发 上海 20-40K 5-8年

智能体：正在搜索Java开发岗位（上海），薪资20-40K，经验5-8年...
```

## ⚙️ 配置说明

### 配置文件 (scripts/config.json)

```json
{
  "request": {
    "timeout": 10,
    "delay": 1.5,
    "max_retries": 3,
    "user_agent": "random"
  },
  "platforms": {
    "boss": {
      "enabled": true,
      "base_url": "https://www.zhipin.com"
    },
    "zhilian": {
      "enabled": true,
      "base_url": "https://sou.zhaopin.com"
    },
    "qiancheng": {
      "enabled": true,
      "base_url": "https://search.51job.com"
    }
  }
}
```

## 🔧 开发指南

### 添加新平台

1. 创建新的解析器类（继承 `BaseParser`）
2. 实现 `parse_search_results` 方法
3. 在 `job_searcher.py` 中注册新平台
4. 更新配置文件

### 示例代码

```python
class NewPlatformParser(BaseParser):
    def parse_search_results(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        jobs = []
        # 解析逻辑...
        return jobs
```

## ⚠️ 注意事项

1. **遵守平台规则**: 尊重各平台的 `robots.txt` 文件
2. **合理使用**: 避免高频请求，设置适当延迟
3. **数据用途**: 仅用于个人学习研究
4. **隐私保护**: 不收集用户个人信息

## 📄 开源协议

本项目采用 MIT 协议开源，详见 [LICENSE](LICENSE) 文件。

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

## 📞 支持与反馈

- 问题反馈: [GitHub Issues](https://github.com/yourusername/openclaw-skill-china-job-search/issues)
- 功能建议: 通过 Issue 提交
- 技术讨论: [OpenClaw Discord](https://discord.com/invite/clawd)

## 🌟 致谢

感谢所有贡献者和用户的支持！

---

**Made with ❤️ for OpenClaw Community**