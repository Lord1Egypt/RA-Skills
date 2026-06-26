# DMP 用户画像洞察技能 - 安装与使用指南

## 安装

### 使用 ClawHub CLI 安装

确认已安装 OpenClaw，然后运行以下命令安装 ClawHub CLI：

```bash
npm install -g clawhub
```

验证是否安装成功：

```bash
clawhub --version
```

### 查看已安装的 Skill 列表

```bash
clawhub list
```

安装后会在 OpenClaw Gateway Dashboard 中的 Skills 页面显示所安装的技能。

### 安装最新版本

```bash
clawhub install dmp-persona-insight
```

如需指定版本：

```bash
clawhub install dmp-persona-insight --version <版本号>
```

安装后，Skill 文件将存放于 OpenClaw workspace 的 `skills/` 目录下。

**备注：** 由于近期 Clawhub 使用人数过多和国内网络限制，建议直接下载文件压缩包，并放置在 workspace/skills 目录下面。

## 验证安装

安装完成后，在 ClawHub 平台访问 Skill 详情页，查看名称、作者、版本、描述等信息。

## 配置 API 密钥

### 申请明日开放平台密钥

在 [明日开放平台](https://open.mingdata.com) 申请人群洞察模块的任务查看与下载权限，申请通过后会生成对应的密钥：

- **DMP_AK**（Access Key）：`xxxxx`
- **DMP_SK**（Secret Key）：`yyyyy`

### 两种密钥输入方式

#### 方式 1：OpenClaw Skill 配置

将生成的 key 保存到 OpenClaw skill 配置中：

在 OpenClaw Gateway Dashboard 的 Skills 页面，找到 dmp-persona-insight 技能，将密钥(例如：{"ak": "your_access_key", "sk": "your_secret_key"})填入对应的配置字段。

#### 方式 2：自然语言对话

通过自然语言对话的形式输入密钥：

```
我要在 dmp-persona-insight 技能中配置密钥
DMP_AK: xxxxx
DMP_SK: yyyyy
```

OpenClaw 会将其自动放在规定的位置。

## 开始使用

与 OpenClaw 对话使用该技能，对话示例：

```
帮我查找人群洞察任务 ID 为 [任务ID] 的任务，并生成分析报告，并生成 ppt。
```

### 主要功能

1. **本地文件分析** - 上传 Excel/CSV 文件分析用户画像
2. **查询洞察任务** - 查询已提交的明日DMP洞察任务状态
3. **获取分析结果** - 拉取已完成洞察任务的分析结果
4. **生成报告** - 自动生成分析报告和 PPT 演示文稿

### 常见使用场景

- 互联网产品用户画像分析
- APP/小程序运营决策支持
- 精准营销和投放策略制定
- 产品定位与竞品对标
- 管理层汇报和融资演示

## 后续文档

- 详细的操作步骤和示例，请参考 `operation-guide.md`
- 快速开始指南，请参考 `quickstart.md`
- 分析方法论，请参考 `analysis-framework.md`
- 洞察 API 集成指南，请参考 `insight-integration.md`
- API 集成说明，请参考 `api-integration.md`
- PPT 设计规范，请参考 `ppt-design-guide.md`
