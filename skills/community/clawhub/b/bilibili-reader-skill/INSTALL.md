# bilibili-reader 接入指南

## 一、接入 Hermes Agent

### 方式一：手动安装到用户 skill 目录（推荐）

```bash
# 1. 复制整个项目到 ~/.hermes/skills/ 目录
cp -r /path/to/bilibili-reader ~/.hermes/skills/bilibili-reader

# 2. 安装 Python 依赖
cd ~/.hermes/skills/bilibili-reader
pip install -r requirements.txt

# 3. 配置 B站 Cookie（见第二节）
```

### 方式二：放到 Hermes Agent 仓库（贡献为官方 Skill）

```bash
# 1. 克隆 Hermes Agent 仓库
git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent

# 2. 将 Skill 放到 optional-skills 目录
cp -r /path/to/bilibili-reader optional-skills/bilibili-reader

# 3. 提交 PR 到官方仓库
```

### 方式三：通过 Hermes CLI 安装

```bash
# 从本地路径安装
hermes skills install /path/to/bilibili-reader

# 或从 GitHub 安装（如果已发布）
hermes skills install github:NousResearch/hermes-agent/optional-skills/bilibili-reader
```

---

## 二、配置 B站 Cookie

### 获取 Cookie 步骤

1. 打开浏览器，登录 [bilibili.com](https://www.bilibili.com)
2. 按 `F12` 打开开发者工具
3. 点击 `Application`（应用程序）标签
4. 左侧找到 `Cookies` -> `https://www.bilibili.com`
5. 复制以下三个值：

| Cookie 名称 | 说明 |
|-----------|------|
| `SESSDATA` | 会话数据，用于 API 认证 |
| `bili_jct` | CSRF 令牌 |
| `buvid3` | 设备标识 |

### 配置方式

**方式 A：通过 hermes 交互式配置**

首次使用 Skill 时，Hermes 会自动提示输入 Cookie 值。

**方式 B：手动创建 .env 文件**

```bash
cd ~/.hermes/skills/bilibili-reader
cp .env.example .env
```

编辑 `.env` 文件：

```env
BILIBILI_SESSDATA=你的SESSDATA值
BILIBILI_BILI_JCT=你的bili_jct值
BILIBILI_BUVID3=你的buvid3值
```

### Cookie 有效期

- B站 Cookie 通常有效期约 30 天
- 过期后需要重新获取并更新 `.env` 文件
- 症状：API 返回 "请先登录" 或 code=-101

---

## 三、使用方式

### CLI 方式

```bash
# 启动 hermes
hermes

# 方式 1：使用 skill 命令
> /bilibili-reader

# 方式 2：自然语言触发
> 从收藏夹随机选个视频总结一下

# 方式 3：直接运行
> 今天推送一个 B站视频总结
```

### 消息平台方式（Telegram / Discord 等）

```
/bilibili-reader
```

---

## 四、定时任务（Cron）

### 什么是 Hermes Cron？

Hermes Agent 内置了定时任务系统，由 gateway 的后台线程驱动，**每 60 秒检查一次**是否有到期任务。

### ⚠️ 安全注意事项

**Cron 任务会在后台持续运行**，即使你没有主动发起对话。这意味着：
- 如果配置了 Cron 任务，技能会**按计划自动执行**，持续使用你的 B站 Cookie 处理视频
- 你需要有意识地**主动管理**已配置的定时任务，不再需要时应及时移除
- 查看当前 Cron 任务列表：`hermes cron list`
- 移除不需要的任务：`hermes cron remove <任务名>`

### 是否需要一直打开 Hermes？

**是的，Hermes 需要保持运行状态，Cron 才会生效。**

| 运行方式 | 是否需要保持运行 | 推荐程度 |
|---------|---------------|---------|
| **Docker 模式** | 容器在后台运行 | 强烈推荐 |
| **Serverless 模式** | 平台自动管理 | 一般 |
| **Gateway 模式** | 需要保持进程 | 一般 |
| **CLI 模式** | 交互式运行 | 不适合 |

如果你需要每天自动推送视频总结，**必须用 Docker 模式部署 Hermes**。

### Docker 部署步骤（推荐）

```bash
# 1. 克隆 Hermes Agent
git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent

# 2. 启动 Docker 容器（后台运行）
HERMES_UID=$(id -u) HERMES_GID=$(id -g) docker compose up -d

# 3. 查看运行状态
docker compose ps

# 4. 查看日志
docker compose logs -f hermes

# 5. 进入容器配置
docker exec -it hermes bash
```

### 设置 Cron 任务

#### 方式一：通过对话设置

```
hermes
> 设置每天上午 9 点运行 bilibili-reader skill
```

#### 方式二：使用 Hermes Cron 命令

```bash
# 创建定时任务
hermes cron add \
  --name "bilibili-daily" \
  --schedule "0 9 * * *" \
  --skill bilibili-reader

# 查看所有定时任务
hermes cron list

# 删除定时任务
hermes cron remove bilibili-daily

# 手动触发一次（测试用）
hermes cron run bilibili-daily
```

### Cron 表达式示例

| 表达式 | 含义 |
|-------|------|
| `0 9 * * *` | 每天上午 9:00 |
| `0 9 * * 1-5` | 工作日上午 9:00 |
| `0 12 * * *` | 每天中午 12:00 |
| `0 20 * * 0` | 每周日晚上 8:00 |
| `0 9,21 * * *` | 每天上午 9 点和晚上 9 点 |

---

## 五、v2.0 新增功能

### ChromaDB 语义搜索

处理视频时自动向量化存入本地向量库，支持语义相似搜索：

```
你：搜索我之前总结过的关于 Docker 的内容
Agent：找到 2 个相关内容：
       [技术教程] Docker 从入门到实践
       [技术教程] Docker Compose 实战
```

不安装 `chromadb` 也不影响核心功能，只是搜索降级为关键词匹配。

### Topic 依赖图

自动从视频总结中提取核心概念作为 Topic 标签，推荐满足前置知识的视频：

```
📚 基于知识图谱推荐: Python 异步编程完全指南
   💡 前置知识已满足，可直接学习
```

### 学习路径推荐

替代随机选择，优先级：
1. Topic 依赖图满足 → 前置已掌握
2. ChromaDB 语义相似 → 与已看视频相关
3. 随机 fallback → 任何状态都有结果

---

## 六、常见问题

**Q: Skill 没有出现在 Hermes 的 skill 列表中？**

```bash
# 检查 skill 是否正确安装
ls ~/.hermes/skills/bilibili-reader/SKILL.md

# 重新加载 skills
hermes skills reload
```

**Q: 如何查看已处理的视频？**

```bash
cat ~/.hermes/skills/bilibili-reader/data/processed.json
```

**Q: 如何重置已处理记录？**

```bash
# 清空已处理记录
echo '{"processed":[],"stats":{"total_processed":0,"last_processed_at":null}}' > ~/.hermes/skills/bilibili-reader/data/processed.json

# 清除 Topic 图谱
rm ~/.hermes/skills/bilibili-reader/data/topic_graph.json

# 清除向量库
rm -rf ~/.hermes/skills/bilibili-reader/data/chroma_db/
```

**Q: PDF 中的中文显示为方块？**

```bash
# Ubuntu/Debian
apt install fonts-noto-cjk

# macOS
brew install --cask font-noto-sans-cjk
```

**Q: 如何更新 Skill？**

```bash
cd ~/.hermes/skills/bilibili-reader
git pull
pip install -r requirements.txt
```
