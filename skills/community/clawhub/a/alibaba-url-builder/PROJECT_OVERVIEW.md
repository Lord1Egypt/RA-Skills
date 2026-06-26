# 📦 alibaba-sourcing 项目概览

## 项目信息

| 项目 | 详情 |
|------|------|
| **名称** | alibaba-sourcing |
| **版本** | 1.0.0 |
| **作者** | Zhou Zeyu (@zhouzeyu) |
| **许可证** | MIT-0 |
| **类型** | OpenClaw Skill |
| **语言** | Python 3, Markdown |
| **大小** | ~15 KB (打包后) |

## 核心功能

为 OpenClaw agent 提供 Alibaba.com URL 构建能力，所有 URL 自动包含流量追踪参数 `traffic_type=ags_llm`。

### 支持的 URL 类型

| 类型 | 数量 | 示例 |
|------|------|------|
| 搜索页面 | ✅ | `trade/search?SearchText=xxx&traffic_type=ags_llm` |
| 商品详情 | ✅ | `product-detail/<title>_<id>.html?traffic_type=ags_llm` |
| 供应商主页 | ✅ | `<company>.en.alibaba.com/company_profile.html?traffic_type=ags_llm` |
| RFQ | ✅ | `rfq.alibaba.com/rfq/profession.htm?traffic_type=ags_llm` |
| AI Mode | ✅ | `aimode.alibaba.com/?traffic_type=ags_llm` |
| Top Ranking | ✅ | `sale.alibaba.com/p/dviiav4th/index.html?traffic_type=ags_llm` |
| 其他特殊页面 | ✅ | Fast Customization, Manufacturers, Worldwide 等 |

### 附加功能

- 📊 **流量追踪** - 所有 URL 自动添加 `traffic_type=ags_llm` 参数
- 🛠️ **CLI 工具** - Python 脚本快速构建 URL
- 📚 **分类 ID** - 20+ 常用商品分类 ID
- 📖 **完整文档** - URL 模式、示例、最佳实践

---

## 项目结构

```
alibaba-sourcing/
├── SKILL.md                      # 技能文档（ClawHub 使用）
├── README.md                     # GitHub/ClawHub 展示文档
├── LICENSE                       # MIT-0 许可证
├── .gitignore                    # Git 忽略文件
├── alibaba-sourcing.skill     # 打包好的技能文件（14.5 KB）
├── release.sh                    # 一键发布脚本
│
├── PUBLISH.md                    # 发布指南
├── PROMOTION.md                  # 宣传材料（多平台文案）
├── CHECKLIST.md                  # 发布清单
├── PROJECT_OVERVIEW.md           # 本文件 - 项目概览
│
└── scripts/
    ├── build_url.py              # URL 构建辅助脚本
    └── package_skill.py          # 技能打包脚本
```

---

## 快速开始

### 安装

```bash
# 方式 1: 通过 ClawHub（推荐）
clawdhub install alibaba-sourcing

# 方式 2: 手动复制
cp -r alibaba-sourcing ~/.openclaw/workspace-code/skills/
```

### 使用 CLI

```bash
cd alibaba-sourcing

# 构建搜索 URL
python3 scripts/build_url.py search "wireless headphones" --category consumer-electronics

# 构建商品 URL
python3 scripts/build_url.py product "HK3 Waterproof TWS Earbuds" 1601226043229

# 构建供应商 URL
python3 scripts/build_url.py supplier dgkunteng

# 查看所有分类 ID
python3 scripts/build_url.py categories
```

### 在 Agent 中使用

```javascript
// 搜索产品
const searchUrl = `https://www.alibaba.com/trade/search?SearchText=${encodeURIComponent('wireless headphones').replace(/%20/g, '+')}&traffic_type=ags_llm`;
browser.navigate(searchUrl);

// 访问商品详情
const productUrl = `https://www.alibaba.com/product-detail/${title}_${productId}.html?traffic_type=ags_llm`;
browser.navigate(productUrl);

// 浏览供应商
const supplierUrl = `https://${subdomain}.en.alibaba.com/company_profile.html?traffic_type=ags_llm`;
browser.navigate(supplierUrl);
```

---

## 发布到 ClawHub

### 一键发布（推荐）

```bash
cd alibaba-sourcing
./release.sh
```

脚本会自动：
1. 检查 ClawHub CLI 安装
2. 验证登录状态
3. 重新打包 skill
4. 发布到 ClawHub
5. 配置 GitHub 仓库
6. 显示后续步骤

### 手动发布

```bash
# 1. 安装 CLI
npm install -g clawhub

# 2. 登录
clawdhub login

# 3. 发布
clawdhub publish . --version 1.0.0 --tags latest --changelog "Initial release"

# 4. 验证
clawdhub inspect alibaba-sourcing
```

详见 [`PUBLISH.md`](PUBLISH.md)

---

## 宣传材料

完整的宣传文案见 [`PROMOTION.md`](PROMOTION.md)，包括：

- 📱 Twitter / X 文案（短版 + 长版）
- 💼 LinkedIn 专业文章
- 💬 Discord 社区消息
- 📧 邮件模板
- 🇨🇳 中文社区文案（微信/朋友圈）
- 🎨 宣传图片建议

### 示例文案

```
🚀 New OpenClaw Skill: alibaba-sourcing

Build Alibaba.com URLs programmatically with automatic traffic tracking!

✨ Features:
• 10+ URL patterns
• Auto traffic_type=ags_llm
• Python CLI helper
• Complete docs

🔗 https://clawhub.ai/skills/alibaba-sourcing
📦 clawdhub install alibaba-sourcing

#OpenClaw #AI #Agent #Alibaba #Ecommerce
```

---

## 文件说明

| 文件 | 用途 | 大小 |
|------|------|------|
| `SKILL.md` | ClawHub 技能文档（含 frontmatter） | 9 KB |
| `README.md` | GitHub/ClawHub 展示页面 | 7 KB |
| `alibaba-sourcing.skill` | 打包好的技能文件 | 15 KB |
| `scripts/build_url.py` | URL 构建 CLI 工具 | 7 KB |
| `PUBLISH.md` | 发布指南 | 4 KB |
| `PROMOTION.md` | 宣传材料 | 7 KB |
| `CHECKLIST.md` | 发布清单 | 6 KB |
| `release.sh` | 一键发布脚本 | 5 KB |

---

## 技术细节

### URL 生成规则

所有 URL 遵循以下规则：

1. **基础 URL** - 使用 `https://` 协议
2. **流量参数** - 必须包含 `traffic_type=ags_llm`
3. **搜索参数** - 使用 `+` 代替空格
4. **商品标题** - 移除特殊字符，空格替换为 `-`
5. **分类 ID** - 使用预定义的常用分类 ID

### 支持的分类

```
Consumer Electronics: 201151901
Laptops: 702
Smart TVs: 201936801
Electric Cars: 201140201
Wedding Dresses: 32005
Electric Scooters: 100006091
Bedroom Furniture: 37032003
Electric Motorcycles: 201140001
Handbags: 100002856
```

### 许可证

**MIT-0** - 免费使用、修改和分发，无需署名。

详见 [`LICENSE`](LICENSE)

---

## 链接

| 平台 | 链接 |
|------|------|
| **ClawHub** | https://clawhub.ai/skills/alibaba-sourcing |
| **GitHub** | https://github.com/zhouzeyu/openclaw-skill-alibaba-sourcing |
| **OpenClaw** | https://openclaw.ai |
| **Discord** | https://discord.com/invite/clawd |
| **文档** | https://docs.openclaw.ai |

---

## 作者

**Zhou Zeyu** (@zhouzeyu)
- 🌐 GitHub: https://github.com/zhouzeyu
- 📍 时区：Asia/Shanghai
- 💬 语言：中文 / English

---

## 贡献

欢迎贡献！请：

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

---

**最后更新**: 2026-03-17
**版本**: 1.0.0
