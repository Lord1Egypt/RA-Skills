---
name: douyin-scraper
description: 抖音内容爬虫，支持自然语言搜索视频内容，基于浏览器自动化实现
metadata:
  emoji: "🎬"
  author: OpenClaw
  version: 1.0.0
  requires:
    commands: ["agent-browser"]
---

# 抖音内容爬虫 Skill

基于浏览器自动化的抖音内容爬虫，支持**自然语言直接搜索**视频内容。

## 功能特性

✅ **自然语言搜索** - 直接说"搜索一下海鲜视频"即可执行搜索
✅ 视频列表抓取 - 获取搜索结果的视频标题、作者、点赞数等信息
✅ 无代码交互 - 纯自然语言驱动
✅ 会话持久化 - 自动保存浏览器状态

## 快速开始

### 安装依赖

```bash
npm install -g agent-browser
agent-browser install
```

### 使用方式 - 自然语言驱动

直接用自然语言发出指令即可：

```
搜索一下海鲜视频
帮我找一下美食探店视频
搜索搞笑段子
查找Python教程视频
```

## 工作原理

当用户输入自然语言搜索请求时，Skill 会：

1. **意图识别** - 解析用户输入中的搜索关键词（如"海鲜视频"→关键词：海鲜）
2. **浏览器导航** - 自动打开抖音搜索页面
3. **自动输入** - 在搜索框输入关键词并提交
4. **结果抓取** - 提取视频列表信息（标题、作者、点赞数等）
5. **结果返回** - 格式化输出搜索结果

## 支持的自然语言句式

```
搜索一下[关键词]视频
帮我搜[关键词]
查找[关键词]内容
找一下[关键词]的视频
搜索[关键词]
```

更多示例见：`examples/search_requests.txt`

## 执行流程 (Agent 执行协议)

当用户请求抖音搜索时，按以下步骤执行：

### 步骤 1: 解析搜索关键词

从用户输入中提取搜索关键词：
- 输入："搜索一下海鲜视频" → 关键词：海鲜
- 输入："帮我找美食探店" → 关键词：美食探店
- 输入："搞笑段子" → 关键词：搞笑段子

### 步骤 2: 初始化浏览器会话

```bash
agent-browser --session douyin open "https://www.douyin.com/search"
agent-browser wait --load networkidle
agent-browser snapshot -i --json
```

### 步骤 3: 定位并填写搜索框

从 snapshot 中找到搜索框 ref，然后：

```bash
agent-browser fill @ref "关键词"
agent-browser press Enter
agent-browser wait --load networkidle
agent-browser wait 2000
```

### 步骤 4: 抓取搜索结果

```bash
agent-browser snapshot -i -d 4 --json
```

### 步骤 5: 提取并返回结果

从 snapshot 中提取：
- 视频标题
- 作者名称
- 点赞/评论/收藏数
- 视频链接

## 边界条件处理

- **搜索框未找到**：等待重试或刷新页面
- **登录弹窗**：自动关闭或跳过（抖音未登录也可搜索）
- **页面加载缓慢**：增加等待时间
- **结果为空**：提示用户更换关键词

## 示例对话

```
用户：搜索一下海鲜视频

Agent：正在搜索海鲜视频...

✅ 搜索完成！找到以下海鲜相关视频：

1. 【渔民阿峰】今天赶海收获大，抓到超大波士顿龙虾 | 12.5万赞
2. 海鲜大排档，帝王蟹这样吃才叫过瘾 | 8.3万赞
3. 挑战1000元吃海鲜自助，能回本吗？ | 15.2万赞
...
```

## 进阶用法

### 保存认证状态（登录后抓取更多内容）

```bash
# 登录后保存状态
agent-browser --session douyin state save douyin-auth.json

# 下次直接加载状态
agent-browser --session douyin state load douyin-auth.json
```

### 滚动加载更多结果

```bash
agent-browser scroll down 1000
agent-browser wait 1000
agent-browser snapshot -i --json
```

---

**使用方式总结：想说什么就说什么，Skill 会自动理解并执行！** 🎬
