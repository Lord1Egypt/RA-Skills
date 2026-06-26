# 📝 微信公众号专业写作+发布技能包

> Markdown 语法 + 爆款写作方法论 + 94种排版主题库 + 完整发布流程

## 📦 技能内容

| 模块 | 文件 | 内容 |
|:-----|:-----|:-----|
| **Markdown 语法** | `knowledge/markdown-syntax-guide.md` | 38个知识点（基本+扩展+高级） |
| **爆款写作法** | `knowledge/viral-writing-methodology.md` | 标题/结构/钩子/金句/评分 |
| **排版主题库** | `knowledge/theme-catalog.md` | 94种主题，按场景分类 |
| **发布指南** | `knowledge/wechat-publishing-guide.md` | API接口/图片上传/草稿/发布/排查 |

## 🚀 快速使用

### 1. 安装到 OpenClaw

```bash
clawhub install wechat-writing-pro
```

### 2. 知识文件位置

```
~/.openclaw/skills/wechat-writing-pro/
├── SKILL.md                              # 技能主文件
├── package.json                          # 元数据
├── README.md                             # 说明文档
└── knowledge/
    ├── markdown-syntax-guide.md          # Markdown 完整语法
    ├── viral-writing-methodology.md      # 爆款写作方法论
    ├── theme-catalog.md                  # 94种排版主题
    └── wechat-publishing-guide.md        # 发布完整指南
```

### 3. Agent 使用方式

当 Agent 需要创作并发布公众号内容时：

```
步骤1: 读取 knowledge/markdown-syntax-guide.md    → 掌握语法
步骤2: 读取 knowledge/viral-writing-methodology.md → 掌握写作方法
步骤3: 读取 knowledge/theme-catalog.md             → 选择排版主题
步骤4: 读取 knowledge/wechat-publishing-guide.md   → 了解发布流程
步骤5: 搜集热点 → 筛选价值点 → 选择主题 → 撰写文章
步骤6: 排版优化 → 上传图片 → 创建草稿 → 发布
```

## 🎯 核心能力

### Markdown 语法（38知识点）
- 基本语法14项（标题、段落、粗体、引用、列表、代码、链接、图片、转义...）
- 扩展语法10项（删除线、任务列表、脚注、表格、高亮、上标下标...）
- 高级技巧14项（提示框、图片标题、颜色、居中、视频嵌入、手动目录...）

### 爆款写作方法论
- **5种标题公式** — 价值型、社会关联、情感共鸣
- **五段式深度结构** — 现象→解析→共鸣→输出→升华
- **4种开篇钩子** — 数据冲击/故事开场/提问引导/悬念反转
- **4种金句公式** — 对比句/排比句/反问句/总结句
- **3种情感共鸣** — 痛点/希望/价值观
- **内容评分系统** — 5维度100分，门槛70分

### 94种排版主题
- 🌑 暗色主题（8种）
- ☀️ 亮色主题（8种）
- 🌈 优雅主题（11种）
- 🌸 文艺主题（5种）
- 🎮 游戏动漫（5种）
- 🔧 科技主题（5种）
- 🎄 节日主题（10种+）
- 🏔️ 自然风景（10种+）
- 🎭 特色主题（15种+）
- 🏢 品牌主题（3种）

### 发布功能（v2.0 新增）
- **API 接口** — Access Token、上传图片、创建草稿、发布、状态查询
- **图片处理** — 封面图上传（add_material）、正文图上传（uploadimg）
- **草稿管理** — 创建、预览、发布
- **错误排查** — 错误码对照表、常见问题解决方案
- **最佳实践** — 发布时机、检查清单、安全注意事项

## 📊 场景匹配速查

| 文章类型 | 推荐主题 |
|:---------|:---------|
| 科技类 | 科技蓝、赛博朋克、Atom Dark |
| 财经类 | 经典蓝(优雅)、石墨黑(优雅) |
| 情感类 | 樱花粉(优雅)、雾中诗、水彩 |
| 生活类 | 春天/夏天/秋天/冬天、锤子便签 |
| 教育类 | 清雅蓝、森林、那拉提 |
| 节日类 | 春节/清明/端午/中秋/圣诞 |

## 📤 发布流程速查

```
获取Access Token → 上传封面图 → 上传正文图 → Markdown排版为HTML → 创建草稿 → 发布
```

| 步骤 | API |
|:-----|:----|
| 获取Token | `GET /cgi-bin/token` |
| 上传封面 | `POST /cgi-bin/material/add_material` |
| 上传正文图 | `POST /cgi-bin/media/uploadimg` |
| 创建草稿 | `POST /cgi-bin/draft/add` |
| 发布 | `POST /cgi-bin/freepublish/submit` |
| 查询状态 | `POST /cgi-bin/freepublish/get` |

## ⚠️ 公众号特殊限制

1. 仅 `mp.weixin.qq.com` 域名链接可直接跳转
2. 外链以脚注形式展示
3. 图片宽度最大 677px，建议源图 900px
4. 文内不重复一级标题
5. 每段 ≤ 3行，每300字小标题+配图
6. 封面图尺寸：头条 900×383px，次条 200×200px

## 🔒 安全说明

- 本技能包**不含任何 API Key 或敏感凭证**
- 使用时需自行配置公众号 App ID 和 App Secret
- 建议使用环境变量存储凭证

## 📚 数据来源

- [Markdown 语法参考](https://blog.axiaoxin.com/post/markdown-guide/) — 阿小信
- [人言兑.md 排版工具](https://md.axiaoxin.com) — 94种主题
- [微信公众号开发文档](https://developers.weixin.qq.com/doc/offiaccount) — 官方API
- 爆款写作方法论 — 实战经验总结

## 📄 更新日志

| 版本 | 日期 | 更新内容 |
|:-----|:-----|:---------|
| **2.0.0** | 2026-04-02 | 集成完整发布功能（API/图片/草稿/排查） |
| **1.0.0** | 2026-04-02 | 初始版本（Markdown+写作+主题） |

## 📄 License

MIT

---

*版本 2.0.0 | 2026-04-02 | JARVIS AI Agent*
