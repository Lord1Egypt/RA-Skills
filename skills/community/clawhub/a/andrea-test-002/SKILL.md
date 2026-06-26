---
name: alphaclaw
type: SKILL
category: official-1688
description: "AlphaClaw 是 SkillHub 技能商店的 CLI 工具，用于搜索、安装、发布和管理 Claude Code 技能。支持 AK/SK 登录、关键词搜索技能、一键安装/发布技能包、收藏和评论等完整功能。"
metadata:
  version: 1.0.2
  label: 技能商店
  author: 1688官方技术团队
---

# AlphaClaw - SkillHub CLI 工具

AlphaClaw 是 1688 SkillHub 技能商店的命令行工具，让你可以直接在终端搜索、安装、发布和管理openclaw的技能SKILL。

**官网**: https://skill.alphashop.cn/

## 触发条件

当用户提到以下内容时触发：
- "安装 alphaclaw"、"安装技能商店"、"安装 skill 商店"
- "搜索技能"、"安装技能"、"发布技能"
- "alphaclaw login"、"alphaclaw search"、"alphaclaw install" 等命令
- "技能管理"、"skill 管理"

## 前置条件

- Node.js >= 11
- npm

## 安装

```bash
npm install -g 1688alphaclaw
```

安装完成后，终端输入 `alphaclaw --version` 验证是否安装成功。

## 登录认证

AlphaClaw 使用 AK/SK（Access Key / Secret Key）认证。

### 获取密钥

访问遨虾控制台获取：https://www.alphashop.cn/seller-center/apikey-management

> Secret Key 仅在创建时可见，请妥善保管！

### 执行登录

```bash
alphaclaw login
```

执行后会自动打开浏览器访问 API 密钥管理页面，然后在终端输入 Access Key 和 Secret Key（SK 输入时会被隐藏）。

凭证保存在 `~/.alphaclaw/auth.json`，后续请求自动使用 JWT Token 认证（有效期 30 分钟，自动刷新）。

### 查看当前用户

```bash
alphaclaw whoami
```

## 完整命令参考

### 1. login - 登录

```bash
alphaclaw login
```

自动打开浏览器访问密钥管理页面，交互式输入 AK/SK。

### 2. whoami - 查看当前用户

```bash
alphaclaw whoami
```

显示当前登录用户的信息。

### 3. search - 搜索技能

```bash
alphaclaw search <关键词>
```

按关键词模糊搜索技能，返回匹配的技能列表。

**示例：**
```bash
alphaclaw search "小红书"
alphaclaw search "数据处理"
alphaclaw search "1688"
```

### 4. info - 查看技能详情

```bash
alphaclaw info <技能名称>
```

查看指定技能的详细信息，包括版本、描述、下载次数、收藏数等。

**示例：**
```bash
alphaclaw info xiaohongshu-upload
alphaclaw info 1688-ranking
```

### 5. install - 安装技能

```bash
alphaclaw install <技能名称> [选项]
```

下载并安装技能到本地。默认安装到当前项目的 `skills/` 目录下。

**选项：**
| 选项 | 说明 |
|------|------|
| `--version <ver>` | 安装指定版本（默认最新版） |
| `--force` | 强制覆盖已安装的技能 |
| `--dir <path>` | 自定义安装目录 |

**示例：**
```bash
alphaclaw install xiaohongshu-upload
alphaclaw install xiaohongshu-upload --version 1.0.0
alphaclaw install xiaohongshu-upload --force
alphaclaw install xiaohongshu-upload --dir ./my-skills
```

安装记录保存在 `~/.skillhub/skills-lock.json`。

### 6. list - 查看已安装的技能

```bash
alphaclaw list
```

列出本地已安装的所有技能，显示名称、版本、安装路径和安装时间。

### 7. publish - 发布技能

```bash
alphaclaw publish [目录路径] [选项]
```

将技能目录打包为 zip 并上传到 SkillHub。目录中必须包含 `SKILL.md` 文件。

**选项：**
| 选项 | 说明 |
|------|------|
| `--yes, -y` | 跳过确认提示，直接发布 |

**示例：**
```bash
# 发布当前目录
cd my-skill/
alphaclaw publish

# 发布指定目录
alphaclaw publish ./my-skill

# 跳过确认直接发布
alphaclaw publish ./my-skill --yes
```

**发布流程：**
1. 读取并校验 `SKILL.md` 的 YAML frontmatter
2. 如果未设置 category，交互式选择分类
3. 显示元数据预览，确认后打包上传
4. 上传后进入"待审批"状态，管理员审批通过后上线

### 8. comment - 发表评论

```bash
alphaclaw comment <技能名称>
```

对指定技能发表评论，执行后在终端输入评论内容。

**示例：**
```bash
alphaclaw comment xiaohongshu-upload
```

### 9. favorite - 收藏/取消收藏

```bash
alphaclaw favorite <技能名称> [选项]
```

**选项：**
| 选项 | 说明 |
|------|------|
| `--remove` | 取消收藏 |

**示例：**
```bash
alphaclaw favorite xiaohongshu-upload          # 收藏
alphaclaw favorite xiaohongshu-upload --remove  # 取消收藏
```

## 全局选项

所有命令均支持以下全局选项：

| 选项 | 说明 |
|------|------|
| `--api <url>` | 覆盖 API 基础 URL |
| `--version, -v` | 显示版本号 |
| `--help, -h` | 显示帮助信息 |
| `--debug` | 显示调试信息（排查问题时使用） |

## 技能包格式

发布技能时，目录中必须包含 `SKILL.md`，格式如下：

```markdown
---
name: my-skill
version: 1.0.0
type: SKILL
category: other
description: "技能描述"
github-url: https://github.com/example/repo
---

# 技能标题

详细说明...
```

### 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| name | Y | 技能名称，小写字母+数字+连字符，3-50字符 |
| description | Y | 技能描述 |
| version | N | 语义化版本号，如 `1.0.0`（省略则自动递增） |
| type | N | `SKILL`（默认）或 `EXPERIENCE` |
| category | N | 分类编码（发布时可交互选择） |
| github-url | N | GitHub 仓库链接 |

### 技能分类

| 分类编码 | 名称 |
|---------|------|
| official-1688 | 官方 |
| product-selection | 选品 |
| pricing | 定价 |
| inquiry | 询盘 |
| material | 素材 |
| distribution | 铺货 |
| other | 其他 |

## 目录结构推荐

```
my-skill/
├── SKILL.md              # 必需 - 技能声明和指令
├── scripts/              # 可选 - 可执行脚本
├── references/           # 可选 - 参考文档
├── assets/               # 可选 - 模板、资源文件
└── prompts/              # 可选 - Prompt 模板
```

## 配置文件位置

| 文件 | 路径 | 说明 |
|------|------|------|
| 认证凭证 | `~/.alphaclaw/auth.json` | AK/SK 存储 |
| 安装锁文件 | `~/.skillhub/skills-lock.json` | 已安装技能记录 |
| 技能目录 | `./skills/` | 默认安装位置 |

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `SKILLHUB_API` | API 地址 | `https://api.alphashop.cn` |
| `NO_COLOR` | 禁用彩色输出 | - |

## 常见工作流

### 安装一个技能

```bash
alphaclaw login                          # 首次使用需要登录
alphaclaw search "小红书"                 # 搜索技能
alphaclaw info xiaohongshu-upload         # 查看详情
alphaclaw install xiaohongshu-upload      # 安装
alphaclaw list                            # 确认已安装
```

### 创建并发布一个技能

```bash
mkdir my-skill && cd my-skill

# 创建 SKILL.md（包含 frontmatter 和指令内容）
cat > SKILL.md << 'EOF'
---
name: my-skill
version: 1.0.0
type: SKILL
description: "我的技能描述"
---

# My Skill

技能使用说明...
EOF

# 添加脚本等资源
mkdir scripts
# ... 添加你的文件

# 发布
alphaclaw login    # 确保已登录
alphaclaw publish  # 发布到 SkillHub
```

## 故障排查

遇到问题时，使用 `--debug` 查看详细信息：

```bash
alphaclaw install some-skill --debug
alphaclaw publish --debug
```

常见问题：
- **认证失败**：重新执行 `alphaclaw login`
- **安装失败**：检查网络连接，或加 `--force` 重试
- **发布被拒绝**：检查 SKILL.md 格式是否正确，name 字段是否符合命名规范
