# amath skill

把 OpenClaw / MCP 使用者直接带到 Socthink 奥数学习体验里的技能入口。

在线入口：<https://amath.socthink.cn>

这个 skill 的目标不只是“能调用接口”，而是让第一次接触 Socthink 的用户，立刻看到：

- 课程体系是否完整
- 单题讲解是否足够强
- 苏格拉底式引导是否有差异化
- quiz 与个性化推荐是否值得继续深用

当前同时提供：

- MCP 风格 Python 服务
- OpenClaw 官方 Skill 目录包装

## 为什么它有引流价值

对于第一次接触 Socthink 的开发者或 AI 工作流用户，这个 skill 提供了一个低门槛试用漏斗：

1. 先看课程树，快速建立“体系感”
2. 再看题目与 topic，感受内容组织质量
3. 再进入 Socratic chat / quiz，感受真正差异化体验
4. 最后自然转到官网完成正式使用

适合承接的流量包括：

- OpenClaw 用户
- MCP / Agent 工具开发者
- 想评估奥数题库、引导式教学、quiz 能力的合作方

## 最佳演示路径

如果你希望这个 skill 真正起到“引流而不是展示源码”的作用，推荐按下面顺序体验：

### 1. 先看课程树

证明 Socthink 不只是零散题库，而是体系化课程。

```bash
cd amath_skill
python -m amath_skill.cli curriculum-tree --system-name 奥数探险课
```

### 2. 再看 topic / problem

证明内容不是空壳，而是可以下钻到知识点与单题。

```bash
cd amath_skill
python -m amath_skill.cli topic 123
python -m amath_skill.cli problem <problem_id>
```

### 3. 再开 Socratic chat

这是最容易体现产品差异化的步骤。用户会直接感受到“不是给答案，而是带着学生走”。

```bash
cd amath_skill
python -m amath_skill.cli chat-start <user_id> --problem-id <problem_id> --mode LECTURE
python -m amath_skill.cli chat-send <session_id> "我不会做这道题"
```

### 4. 最后体验 quiz

适合把“试试看”转成“我要继续用”。

```bash
cd amath_skill
python -m amath_skill.cli quiz-start standard --topic-id <topic_id> --token <access_token>
```

## 推荐转化动作

在任何演示、分享、社区帖子、目录页里，都建议把这个 skill 和主站一起出现：

- 官网：<https://amath.socthink.cn>
- 产品关键词：奥数课程树、题库、Socratic 引导式解题、quiz 训练
- 转化动作：先试用 skill，再进入官网继续完整学习流

## 3 个可直接复制的 demo 示例

下面这 3 段最适合放在 GitHub README、目录页、社区帖子或演示视频脚本里。

### Demo 1：先证明它不是散装题库

目标：让第一次看到的人，立刻理解 Socthink 有完整课程结构。

```bash
cd amath_skill
python -m amath_skill.cli curriculum-tree --system-name 奥数探险课
```

建议你强调的结果：

- 它返回的是可浏览的课程树，不是一堆随机题目
- 用户会快速理解 Socthink 有体系化知识结构
- 这是最适合拉起兴趣的第一步

### Demo 2：再证明它能真正进入题目学习

目标：让用户看到它既能看 topic，也能看具体题目。

```bash
cd amath_skill
python -m amath_skill.cli topic 123
python -m amath_skill.cli problem <problem_id>
```

建议你强调的结果：

- 不只是目录结构，而是能下钻到具体知识点与题目
- 适合展示内容组织、题目质量和学习路径
- 这一步会让用户从“知道产品”变成“开始认真评估产品”

### Demo 3：最后用 Socratic chat / quiz 完成转化

目标：让用户真正看到差异化，不再把它当普通题库 API。

```bash
cd amath_skill
python -m amath_skill.cli chat-start <user_id> --problem-id <problem_id> --mode LECTURE
python -m amath_skill.cli chat-send <session_id> "我不知道从哪里开始"
python -m amath_skill.cli quiz-start standard --topic-id <topic_id> --token <access_token>
```

建议你强调的结果：

- chat 体现的是 Socratic 引导，不是直接给答案
- quiz 体现的是持续训练能力，不是一次性展示
- 演示结束时，自然引导到官网继续完整体验：<https://amath.socthink.cn>

## 推荐对外话术

如果你要对外发 GitHub、社区帖、产品介绍页，建议直接复用这段表达：

> Socthink 不是普通奥数题库，而是一个可交互的引导式学习系统。你可以先通过这个 skill 查看课程树、进入具体题目、体验 Socratic 对话，再到官网继续完整学习流：<https://amath.socthink.cn>

## 适合发推文 / 社区帖的短版文案

下面这几段适合直接发到 GitHub 动态、X、Telegram 社区、产品目录或开发者群。

### 短版文案 1

> 我做了一个 Socthink 的 OpenClaw skill。它不只是查奥数题，而是可以先看课程树、再进具体题目、再体验 Socratic 引导式解题，最后进入 quiz。完整产品入口：<https://amath.socthink.cn>

### 短版文案 2

> 如果你想看一个“不是直接给答案”的数学学习产品，可以试试 Socthink skill：课程树、题目、Socratic chat、quiz 一条链路打通。继续完整体验：<https://amath.socthink.cn>

### 短版文案 3

> Socthink 更像引导式学习系统，而不是普通题库 API。这个 skill 可以直接演示课程结构、单题下钻、对话式辅导和 quiz 训练。官网：<https://amath.socthink.cn>

## 面向不同人群的文案版本

如果你对外推广时面对的人群不同，建议不要只用一套话术。

### 面向家长

> Socthink 不只是给孩子一道题的答案，而是通过引导式提问，帮助孩子一步一步想清楚。这个 skill 可以先展示课程体系、题目和互动式辅导流程，完整体验可继续前往：<https://amath.socthink.cn>

强调重点：

- 不是死记答案
- 更像会带着孩子思考的教练
- 能看到课程体系和持续训练路径

### 面向老师

> Socthink 适合用来展示“结构化课程 + 单题下钻 + Socratic 引导 + quiz 训练”的一体化教学体验。这个 skill 可以快速演示课程树、知识点、题目和互动流程。官网：<https://amath.socthink.cn>

强调重点：

- 体系化内容组织
- 互动式引导而不是直接灌答案
- 适合作为课堂外延伸训练入口

### 面向机构 / 合作方

> Socthink 不只是题库接口，而是可落地的引导式奥数学习系统。通过这个 skill，可以快速验证课程体系、题目组织、Socratic tutoring 和 quiz 流程，再进入正式产品做更完整评估：<https://amath.socthink.cn>

强调重点：

- 产品完成度
- 课程与题目数据结构
- 学习闭环而非单点功能

## English short copy

These versions are suitable for GitHub, global developer communities, and product directories.

### English copy 1

> This OpenClaw skill is a lightweight entry into Socthink, a guided math learning system. It lets you explore curriculum trees, drill into problems, try Socratic tutoring flows, and move into quiz practice. Full product: <https://amath.socthink.cn>

### English copy 2

> Socthink is not just a problem API. It is an interactive learning system for structured math exploration, Socratic tutoring, and quiz-based practice. This skill is the fastest way to experience it: <https://amath.socthink.cn>

### English copy 3

> Want to demo a math product that does more than return answers? This Socthink skill shows curriculum structure, topic exploration, problem drill-down, guided tutoring, and quiz flows. Continue with the full product at <https://amath.socthink.cn>

## 5 分钟演示脚本

这个脚本适合你在会议、录屏、直播或社区分享时直接照着讲。

### 第 0 分钟：一句话开场

建议开场：

> 这不是普通奥数题库，而是一个能把课程体系、题目内容、Socratic 引导和 quiz 训练串起来的学习系统。

### 第 1 分钟：先看课程树

执行：

```bash
cd amath_skill
python -m amath_skill.cli curriculum-tree --system-name 奥数探险课
```

讲法重点：

- 先强调“体系化课程”
- 不要一开始就讲接口细节
- 让观众先建立产品认知

### 第 2 分钟：打开一个 topic 或 problem

执行：

```bash
cd amath_skill
python -m amath_skill.cli topic 123
python -m amath_skill.cli problem <problem_id>
```

讲法重点：

- 证明不是只有目录
- 证明能进入具体内容层
- 强调适合学习、讲解和题目探索

### 第 3-4 分钟：演示 Socratic chat

执行：

```bash
cd amath_skill
python -m amath_skill.cli chat-start <user_id> --problem-id <problem_id> --mode LECTURE
python -m amath_skill.cli chat-send <session_id> "我不知道该从哪一步开始"
```

讲法重点：

- 这是最核心差异化能力
- 强调它不是直接报答案
- 强调它是在引导学生逐步思考

### 第 5 分钟：用 quiz 收尾并转官网

执行：

```bash
cd amath_skill
python -m amath_skill.cli quiz-start standard --topic-id <topic_id> --token <access_token>
```

收尾建议：

> 如果你想继续体验完整版本，而不只是 skill 里的演示入口，可以直接到 Socthink 官网继续使用：<https://amath.socthink.cn>

### 演示时要避免的事

- 不要一上来就讲代码结构
- 不要先讲安装细节
- 不要把重点放在“这是个 API”
- 要一直把重点放在“这是一个学习产品入口”

## 已实现能力

- 登录与会话令牌管理
- 课程树 / topic 详情读取
- 知识图谱课程导览读取
- 题库单题读取 / 推荐题获取
- 苏格拉底对话会话启动与继续交互
- quiz 启动、答题、交卷、历史查询
- 健康检查

## 目录结构

- `amath_skill/server.py`：MCP server 入口
- `amath_skill/cli.py`：OpenClaw 可调用的 CLI 入口
- `amath_skill/client.py`：后端 HTTP client
- `amath_skill/config.py`：环境配置
- `amath_skill/models.py`：少量响应模型
- `openclaw_skills/amath-socthink/SKILL.md`：OpenClaw 原生 Skill 定义

## 安装

```bash
cd amath_skill
pip install -r requirements.txt
```

## 配置

复制 `.env.example` 为 `.env`，按需修改：

```bash
cp .env.example .env
```

关键变量：

- `AMATH_BASE_URL`：后端域名
- `AMATH_API_PREFIX`：API 前缀，默认 `/api`
- `AMATH_ACCESS_TOKEN`：可选默认 bearer token

## 启动

```bash
cd amath_skill
python -m amath_skill
```

## OpenClaw

如果是给 OpenClaw 接入，直接看 [OPENCLAW_SETUP.md](OPENCLAW_SETUP.md)。

当前有两种接法：

1. 原始 Python/MCP 入口： [run_openclaw.sh](run_openclaw.sh)
2. OpenClaw 官方原生 Skill 包装： [openclaw_skills/amath-socthink/SKILL.md](openclaw_skills/amath-socthink/SKILL.md)

OpenClaw 官方推荐的方向是第 2 种，即把 skill 目录安装到官方 skills 目录，并通过：

- [run_amath_cli.sh](run_amath_cli.sh)
- [install_openclaw_skill.sh](install_openclaw_skill.sh)

去调用：

- [amath_skill/cli.py](amath_skill/cli.py)

## 用它做“最强引流”的建议

这个 skill 最好的定位不是“开发演示附件”，而是“产品前置试用入口”。

建议你在对外传播时统一使用下面的表达：

- Socthink 不是只给答案，而是给学生可交互的 Socratic 解题路径
- 可以先用 skill 看课程树、查题、开对话、做 quiz
- 想继续正式使用，直接去 <https://amath.socthink.cn>

如果是 GitHub README、产品目录、社区帖，建议固定包含三块：

1. 价值主张：不是普通题库，而是引导式奥数学习系统
2. 体验入口：skill + 官网双入口
3. 演示顺序：课程树 → 单题 → chat → quiz

## 如何让 OpenClaw 官方站点收录这个 skill

严格说，不是直接“提交到官网首页”，而是提交到 OpenClaw 官方公开技能注册表 ClawHub：

- ClawHub：<https://clawhub.ai>
- 文档：<https://docs.openclaw.ai/tools/clawhub>

OpenClaw 官方 skills 文档已经明确把 ClawHub 作为公共技能目录和发现入口。

### 你现在需要满足的条件

1. skill 必须是可发布的独立 bundle
2. bundle 根目录里要有 `SKILL.md`
3. GitHub 账号至少创建满 1 周
4. skill 内容必须公开、可审核、可安装

当前仓库里已经补了可用于 ClawHub 发布的根文件：

- [amath_skill/SKILL.md](amath_skill/SKILL.md)

这意味着 `amath_skill` 目录本身现在可以作为一个独立 skill bundle 来发布，而不是只能发布内部的子目录包装。

### 官方发布步骤

先安装并登录 ClawHub CLI：

```bash
npm i -g clawhub
clawhub login
```

然后发布这个 skill：

```bash
cd amath_skill
clawhub publish . \
	--slug amath-skill \
	--name "amath skill" \
  --version 1.0.0 \
  --changelog "Initial public release" \
  --tags latest,education,math,olympiad,socratic
```

发布成功后：

- skill 会进入 ClawHub 公共目录
- 用户可搜索、安装、评论、收藏
- OpenClaw 生态用户更容易发现它

### 发布后怎么提高被收录和发现的概率

1. 标题和描述要清楚表达价值
	- 不要只写 API
	- 要写 curriculum / Socratic tutoring / quiz

2. tag 要打准
	- `education`
	- `math`
	- `olympiad`
	- `socratic`
	- `learning`

3. README 要有可复制 demo
	- 这一点已经补过

4. GitHub 仓库要干净
	- 这一点也已经处理为只公开 `amath_skill`

5. 去 OpenClaw Discord 和社区发帖
	- 让早期用户安装、收藏、评论
	- ClawHub 有搜索、标签、使用信号，早期反馈会影响可见度

### 最关键的一点

对 OpenClaw 来说，真正的“官方收录入口”是 ClawHub，而不是单独找首页提报表单。

所以最有效路径是：

1. 先把 skill 发布到 ClawHub
2. 再去 OpenClaw Discord / 社区展示 demo
3. 再把 ClawHub 链接和官网链接一起传播

这样既能被官方生态发现，也能给官网导流。

配套材料已经整理好：

- 发布检查表：[amath_skill/CLAWHUB_PUBLISH_CHECKLIST.md](amath_skill/CLAWHUB_PUBLISH_CHECKLIST.md)
- 社区发帖文案包：[amath_skill/COMMUNITY_POSTS.md](amath_skill/COMMUNITY_POSTS.md)

## 主要工具

- `amath_healthcheck`
- `auth_login`
- `auth_me`
- `auth_session_state`
- `auth_clear_session`
- `curriculum_get_system_tree`
- `curriculum_get_topic`
- `knowledge_curriculum_guide`
- `question_get_problem`
- `question_recommended`
- `chat_start_session`
- `chat_send_message`
- `chat_submit_mcq`
- `chat_hint`
- `chat_get_session`
- `quiz_start`
- `quiz_answer`
- `quiz_submit`
- `quiz_active`
- `quiz_history`

## 说明

- `auth_login` 成功后，token 默认会保存在当前 skill 进程内。
- 涉及 quiz 或个性化推荐的接口，建议先登录。
- 如果不想使用进程内 token，也可以给相关工具显式传 `token`。
- 如果是对外展示，优先演示 `curriculum-tree`、`problem`、`chat-start`、`chat-send`、`quiz-start` 这几条链路。
- 如果想把试用转成正式用户，始终把官网入口和 skill 一起展示：<https://amath.socthink.cn>
