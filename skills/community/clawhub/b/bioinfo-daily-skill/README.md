# Bioinfo Daily - OpenClaw Skill

📰 **每日生物信息学与肿瘤学研究进展日报生成器**

## 功能特点

- 🔍 **自动搜索**: 使用 PubMed API 搜索前一天新增文献（限定 cancer 相关）
- 📊 **高影响力筛选**: 仅筛选 CNS 及 Nature Index 期刊
- 🎯 **精准分类**: 生物信息学、肿瘤免疫、单细胞测序、空间转录组、临床进展
- 💡 **中文亮点**: 每篇文献 30 字左右中文亮点介绍
- 📝 **智能摘要**: 日报抬头自动生成精选文章 summary
- 🔥 **智能优选**: 文章多时会自动优选创新性强、方向有区分的文章（最多10篇）

## 安装

### 1. 安装到 OpenClaw

```bash
# 克隆仓库
git clone https://github.com/WangLabCSU/bioinfo-daily-skill.git

# 复制到 OpenClaw skills 目录
cp -r bioinfo-daily-skill ~/.openclaw/workspace/skills/bioinfo-daily
```

### 2. 配置 PubMed API（重要）

**注意：API Key 不应硬编码在代码中，请使用环境变量配置**

#### 方式 1：OpenClaw 配置文件（推荐）

在 `~/.openclaw/openclaw.json` 中添加：

```json
{
  "env": {
    "NCBI_EMAIL": "your@email.com",
    "NCBI_API_KEY": "your_api_key"
  }
}
```

#### 方式 2：环境变量

```bash
export NCBI_EMAIL="your@email.com"
export NCBI_API_KEY="your_api_key"
```

#### 方式 3：.env 文件

在项目目录创建 `.env` 文件：

```
NCBI_EMAIL=your@email.com
NCBI_API_KEY=your_api_key
```

> ⚠️ **安全提示**: `.env` 文件只放 NCBI 相关凭证，不要放其他无关的 secrets。该文件已在 `.gitignore` 中，不会提交到 Git。

**获取 API Key**: https://ncbiinsights.ncbi.nlm.nih.gov/2017/11/02/new-api-keys-for-the-e-utilities/

### 3. 设置定时任务

```bash
openclaw cron add \
  --name "生物信息学日报" \
  --cron "0 19 * * *" \
  --tz "Asia/Shanghai" \
  --channel feishu \
  --message "请运行 ~/.openclaw/workspace/skills/bioinfo-daily/scripts/pubmed_search.py 生成日报"
```

## 使用方法

### 手动生成日报

```bash
python3 ~/.openclaw/workspace/skills/bioinfo-daily/scripts/pubmed_search.py
```

### 查看定时任务

```bash
openclaw cron list
```

## 数据源

- **PubMed API**: https://eutils.ncbi.nlm.nih.gov/entrez/eutils
- **搜索范围**: Cancer 相关的生物信息学、肿瘤免疫、单细胞测序、空间转录组、临床进展
- **期刊筛选**: CNS 主刊及子刊、Nature Index 期刊、其他高影响力期刊

## 输出格式

日报包含：
1. 📅 日期和精选文献 summary
2. 📚 每篇文献：标题、期刊、作者、中文亮点、链接
3. 🔥 创新性标记（评分>25的文章）
4. 📊 数据来源说明

## 项目结构

```
bioinfo-daily/
├── SKILL.md              # Skill 说明文档
├── README.md             # 项目说明
├── scripts/
│   ├── pubmed_search.py  # PubMed API 搜索脚本（主脚本）
│   └── search_bioinfo.py # 备用搜索脚本
└── LICENSE               # MIT 许可证
```

## 配置说明

### 高影响力期刊列表

脚本内置 50+ 高影响力期刊，包括：
- **CNS 主刊**: Nature, Science, Cell
- **Nature 子刊**: Nature Medicine, Nature Genetics, Nature Biotechnology 等
- **Science 子刊**: Science Translational Medicine, Science Immunology 等
- **Cell 子刊**: Cell Research, Cancer Cell, Immunity 等
- **其他**: Lancet, JAMA, PNAS, Genome Research, Bioinformatics 等

### 搜索主题

```python
SEARCH_TOPICS = [
    ("生物信息学 AND cancer", "🧬 生物信息学"),
    ("肿瘤免疫", "🦠 肿瘤免疫"),
    ("单细胞测序 AND cancer", "🔬 单细胞测序"),
    ("空间转录组 AND cancer", "🧪 空间转录组"),
    ("临床进展 AND cancer", "💊 临床进展"),
]
```

## 创新性评分算法

根据以下因素计算创新性得分：
- **期刊级别**: Nature/Science/Cell (+30), PNAS/Lancet/JAMA (+25)
- **创新关键词**: novel (+5), breakthrough (+8), first (+5), single-cell (+4), AI (+5) 等
- **技术方法**: CRISPR (+5), CAR-T (+5), multi-omics (+5) 等

## 作者

- **王诗翔** (Shixiang Wang) - 中南大学
- Email: wangshx@csu.edu.cn
- GitHub: [@ShixiangWang](https://github.com/ShixiangWang)

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## ⚠️ 安全注意事项

### 网络活动
- `pubmed_search.py`: 直接调用 PubMed API（ncbi.nlm.nih.gov）
- `search_bioinfo.py`: 调用 OpenClaw 的 `web_search` 工具（会发送到外部搜索提供商）
- 如需限制网络访问，请在隔离环境中运行

### 飞书自动发布
- `generate_daily.sh` 包含飞书文档创建步骤
- 需要配置飞书 API 凭证才能自动上传到飞书
- 如未配置凭证，脚本会生成文件供手动上传

### .env 文件
- 只放置 NCBI 相关凭证
- 不要在同一文件放其他不相关的 secrets
- 已加入 `.gitignore`，不会提交到 Git

## 致谢

- OpenClaw 团队提供的优秀 AI Agent 框架
- NCBI 提供的 PubMed API
- 生物信息学和肿瘤学研究社区
