# Configure Workflow

修改新闻聚合 Skill 的配置。

## 工作流程

### 步骤 1：显示当前配置

读取并显示当前的配置：

```bash
# 读取配置文件
cat ~/.daily-news-brief/config.json
```

输出示例：

```text
当前配置：

【新闻源】
✓ 36氪 (科技)
✓ 虎嗅网 (科技)
✓ 财新网 (财经)
✓ 机器之心 (AI)

【定时任务】
- 时间：每天 21:00

【本地文档】
- 保存：是
- 路径：~/daily-news-brief/每日新闻/

【推送渠道】
- 启用：是
- 渠道：telegram, feishu

【其他】
- 每类最多新闻数：10
- 每类每来源最多：3
- 摘要每类最多：5
- 摘要每类每来源最多：2
```

### 步骤 2：选择要修改的配置项

```text
请选择要修改的配置项：

1. 新闻源（添加/删除）
2. 定时任务时间
3. 推送渠道设置（OpenClaw）
4. 本地文档保存设置
5. 每类新闻数量限制
6. 恢复默认配置
7. 查看配置文件内容
8. 退出

请输入选项编号（1-8）：
```

### 步骤 3：执行修改操作

#### 选项 1：修改新闻源

```text
当前新闻源列表：

【科技类】
[1] ✓ 36氪 (36kr.com)
[2] ✓ 虎嗅网 (huxiu.com)

【财经类】
[3] ✓ 财新网 (caixin.com)

【AI 类】
[4] ✓ 机器之心 (jiqizhixin.com)

操作：
a. 添加新闻源
d. 删除新闻源
l. 列出所有可用新闻源
r. 返回上级菜单

请选择操作：
```

**添加新闻源**：
```text
请输入新闻源信息：
- 名称：例如：新智元
- URL：https://xinzhiyuan.ai/feed
- 类型：RSS / 网页抓取
- 分类：科技 / 财经 / AI / 智能体
```

**删除新闻源**：
```text
请输入要删除的新闻源序号（可多选，用逗号分隔）：
```

#### 选项 2：修改定时任务时间

```text
当前定时时间：每天 21:00

请输入新的定时时间（格式：HH:MM，例如：08:30）：
```

**更新 cron 任务**：
```bash
# macOS/Linux
crontab -l > /tmp/crontab.bak
sed -i 's/0 21 \* \* \*/0 8 \* \* \*/' /tmp/crontab.bak
crontab /tmp/crontab.bak
```

#### 选项 3：修改推送渠道（OpenClaw）

```text
当前推送渠道：telegram, feishu

请选择要启用的渠道（可多选，用逗号分隔）：
1. Telegram
2. 飞书（Feishu）
3. WhatsApp
4. Slack
5. Discord
```

**执行（按用户选择）**：
```bash
# 例如启用 Telegram 与飞书
openclaw channels login --channel telegram
openclaw channels login --channel feishu
```

**配置文件更新**：
```json
{
  "push": {
    "enabled": true,
    "channels": ["telegram", "feishu"]
  }
}
```

**可选：为通道指定目标（仅当 OpenClaw 未配置默认目标时）**：
```json
{
  "push": {
    "targets": {
      "telegram": "@mychannel",
      "feishu": "oc_123456"
    }
  }
}
```

#### 选项 4：修改本地文档保存设置

```text
当前设置：
- 保存本地文档：是
- 保存路径：~/daily-news-brief/每日新闻/

操作：
1. 修改保存状态（是/否）
2. 修改保存路径
3. 清空历史文档
4. 返回上级菜单

请选择操作（1-4）：
```

**清空历史文档**：
```bash
# 警告提示
echo "⚠️  警告：这将删除所有历史新闻文档！"
echo "确认删除？(yes/no)"

read confirm

if [ "$confirm" = "yes" ]; then
  rm -rf ~/daily-news-brief/每日新闻/*
  echo "✅ 历史文档已清空"
fi
```

#### 选项 5：修改每类新闻数量限制

```text
当前设置：每类最多 10 条新闻

请输入新的数量限制（1-50）：
```

**配置文件更新**：
```json
{
  "maxNewsPerCategory": 20
}
```

#### 选项 6：恢复默认配置

```text
⚠️  警告：这将恢复到初始配置，所有自定义设置将丢失！

确认恢复默认配置？(yes/no)：
```

**默认配置**：
```json
{
  "newsSources": [
    {
      "name": "36氪",
      "url": "https://36kr.com/feed",
      "type": "rss",
      "category": "科技"
    },
    {
      "name": "虎嗅网",
      "url": "https://www.huxiu.com/rss/0.xml",
      "type": "rss",
      "category": "科技"
    },
    {
      "name": "财新网",
      "url": "https://www.caixin.com/rss/rss_newstech.xml",
      "type": "rss",
      "category": "财经"
    },
    {
      "name": "机器之心",
      "url": "https://www.jiqizhixin.com/rss",
      "type": "rss",
      "category": "AI"
    }
  ],
  "schedule": "0 21 * * *",
  "saveLocalDoc": true,
  "localDocPath": "~/daily-news-brief/每日新闻/",
  "maxNewsPerCategory": 10,
  "maxPerSourcePerCategory": 3,
  "summaryMaxPerCategory": 5,
  "summaryMaxPerSource": 2,
  "push": {
    "enabled": true,
    "channels": ["telegram", "feishu"]
  }
}
```

#### 选项 7：查看配置文件内容

```bash
cat ~/.daily-news-brief/config.json
```

#### 选项 8：退出

返回上级菜单或完成配置。

### 步骤 4：保存配置

修改完成后，保存配置文件：

```bash
# 备份旧配置
cp ~/.daily-news-brief/config.json ~/.daily-news-brief/config.json.backup

# 保存新配置
cat > ~/.daily-news-brief/config.json << 'EOF'
{
  "newsSources": [...],
  "schedule": "0 8 * * *",
  "saveLocalDoc": true,
  "localDocPath": "~/daily-news-brief/每日新闻/",
  "maxNewsPerCategory": 15,
  "maxPerSourcePerCategory": 3,
  "summaryMaxPerCategory": 5,
  "summaryMaxPerSource": 2,
  "push": {
    "enabled": true,
    "channels": ["telegram", "feishu"]
  }
}
EOF
```

### 步骤 5：测试新配置

运行一次新闻抓取，测试新配置是否正常：

```bash
node tools/FetchNews.ts --test
```

**检查项**：
- [ ] 配置文件格式正确
- [ ] 能够抓取新闻
- [ ] 新闻数量符合新设置
- [ ] 本地文档保存路径正确
- [ ] 定时任务已更新

### 步骤 6：完成确认

输出配置更新信息：

```text
✅ 配置更新成功！

新配置摘要：
- 新闻源：36氪、虎嗅网、财新网、机器之心、新智元
- 定时时间：每天 08:30
- 本地文档：保存到 ~/daily-news-brief/每日新闻/
- 每类新闻数：15 条

下次执行时间：明天 08:30
```

## 快捷命令（CLI，可选）

```bash
# 快速修改定时表达式
node tools/Configure.ts --schedule "0 8 * * *"

# 添加新闻源
node tools/Configure.ts --add-source "新智元,https://xinzhiyuan.ai/feed,rss,AI"

# 删除新闻源
node tools/Configure.ts --remove-source "新智元"

# 修改每类新闻数
node tools/Configure.ts --max-news 20

# 修改每类每来源上限
node tools/Configure.ts --max-per-source 3

# 修改摘要每类条数
node tools/Configure.ts --summary-max 5

# 修改摘要每类每来源上限
node tools/Configure.ts --summary-max-per-source 2

# 设置推送渠道
node tools/Configure.ts --channels "telegram,feishu"

# 开启/关闭推送
node tools/Configure.ts --push on
node tools/Configure.ts --push off

# 恢复默认配置
node tools/Configure.ts --reset
```

## 快捷操作（手动）

```bash
# 打开配置文件（手动修改）
vim ~/.daily-news-brief/config.json

# 修改后快速验证 JSON 格式
node -e "console.log(JSON.parse(require('fs').readFileSync(process.env.HOME + '/.daily-news-brief/config.json','utf-8')))"
```

## 常见问题

**Q1: 修改配置后定时任务没更新？**
A: 需要手动更新 cron 任务或重启任务计划程序。

**Q2: 如何批量添加新闻源？**
A: 可以编辑配置文件直接修改，或使用 `--add-source` 命令批量添加。

**Q3: 配置文件格式错误怎么办？**
A: 恢复备份：`cp ~/.daily-news-brief/config.json.backup ~/.daily-news-brief/config.json`

**Q4: 保存路径有权限问题？**
A: 检查目录权限：`ls -la ~/daily-news-brief/`，确保有写入权限。

## 配置文件验证

在保存前验证 JSON 格式：

```bash
# 验证 JSON 格式
node -e "console.log(JSON.parse(require('fs').readFileSync(process.env.HOME + '/.daily-news-brief/config.json','utf-8')))"
```
