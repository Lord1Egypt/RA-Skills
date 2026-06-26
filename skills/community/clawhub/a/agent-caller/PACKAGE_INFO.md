# Agency Agents Caller - ClawHub 技能包

## 📦 技能包内容

```
agency-agents-caller/
├── SKILL.md                    # 技能主文档（ClawHub格式）
├── README.md                   # 详细说明文档
├── package.json                # 包配置文件
├── scripts/
│   └── agent_caller.py        # 核心调用脚本
├── examples/
│   └── usage_demo.py          # 使用示例
├── publish.py                  # 发布脚本（Python）
└── create_package.ps1          # 打包脚本（PowerShell）
```

---

## 🚀 发布到ClawHub

### 方法1: 使用ClawHub CLI (推荐)

```bash
# 1. 安装ClawHub CLI
npm install -g clawhub-cli

# 2. 登录
clawhub login

# 3. 发布
cd C:\Users\Administrator\.openclaw\workspace\skills\agency-agents-caller
clawhub publish
```

### 方法2: 使用Web UI

1. 访问: https://clawhub.com/publish
2. 上传技能包: `agency-agents-caller.tar.gz`
3. 填写信息:
   - Name: `agency-agents-caller`
   - Version: `1.0.0`
   - Description: `Call 179 professional agents on-demand from database`
   - Category: `productivity`
   - Keywords: `agents, ai, collaboration, database, search, multi-agent`

### 方法3: 手动发布

```bash
# 复制技能到本地ClawHub目录
cp -r skills/agency-agents-caller ~/.clawhub/skills/

# 注册
clawhub register agency-agents-caller
```

---

## 📝 技能信息

- **名称**: agency-agents-caller
- **版本**: 1.0.0
- **作者**: Erbing
- **许可**: MIT
- **Agent数量**: 179个
- **分类数**: 15个

---

## ✅ 功能特性

- ✅ 从数据库按需调用179个专业Agent
- ✅ 支持关键词搜索
- ✅ 支持分类浏览
- ✅ 支持随机获取
- ✅ 支持获取完整prompt
- ✅ 支持多Agent协作

---

## 📊 Agent分类

| 分类 | 数量 | 说明 |
|------|------|------|
| marketing | 29 | 市场营销 |
| specialized | 28 | 专业领域 |
| engineering | 26 | 工程开发 |
| game-development | 20 | 游戏开发 |
| strategy | 16 | 战略规划 |
| testing | 8 | 测试 |
| sales | 8 | 销售 |
| design | 8 | 设计 |
| paid-media | 7 | 付费媒体 |
| support | 6 | 客户支持 |
| spatial-computing | 6 | 空间计算 |
| project-management | 6 | 项目管理 |
| product | 5 | 产品 |
| academic | 5 | 学术 |
| integrations | 1 | 集成 |

---

## 🔗 链接

- **GitHub**: https://github.com/717986230/openclaw-workspace
- **ClawHub**: https://clawhub.com/skills/agency-agents-caller (发布后)
- **文档**: `README.md`
- **示例**: `examples/usage_demo.py`

---

## 📦 打包命令

```powershell
# 创建压缩包
.\create_package.ps1
```

输出: `skills/packages/agency-agents-caller_YYYYMMDD_HHMMSS.tar.gz`

---

## ✨ 发布后

用户可以通过以下命令安装:

```bash
clawhub install agency-agents-caller
```

---

*创建时间: 2026-04-11*
*准备发布: ✅ 就绪*
