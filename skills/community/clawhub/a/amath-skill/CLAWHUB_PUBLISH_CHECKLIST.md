# ClawHub 发布清单

目标：把 `amath_skill` 作为独立 skill bundle 发布到 ClawHub，让 OpenClaw 官方生态可以搜索、安装和传播。

官方参考：

- ClawHub：<https://clawhub.ai>
- 文档：<https://docs.openclaw.ai/tools/clawhub>

## 一次性执行命令

```bash
npm i -g clawhub
clawhub login
cd amath_skill
./preflight_check.sh
./publish_clawhub.sh
```

如果你想显式传参：

```bash
./publish_clawhub.sh amath-skill 1.0.0 "Initial public release" "latest,education,math,olympiad,socratic,learning"
```

## 发布前检查表

### 1. bundle 结构

必须确认这些文件存在：

- [amath_skill/SKILL.md](amath_skill/SKILL.md)
- [amath_skill/README.md](amath_skill/README.md)
- [amath_skill/run_amath_cli.sh](amath_skill/run_amath_cli.sh)
- [amath_skill/run_openclaw.sh](amath_skill/run_openclaw.sh)
- [amath_skill/openclaw_skills/amath-socthink/SKILL.md](amath_skill/openclaw_skills/amath-socthink/SKILL.md)

### 2. 信息表达

发布前确认这几点：

- 名称不要只像技术组件
- 描述要突出课程树、题目、Socratic tutoring、quiz
- 官网链接必须明确：<https://amath.socthink.cn>
- README 要有 demo、转化路径、对外传播文案

### 3. 安全检查

发布前确认：

- 不包含 `.env`
- 不包含 token、密码、私钥
- 不包含机器绝对路径泄漏
- 公开仓库里只包含 `amath_skill`

### 4. 账号与权限

- GitHub 账号已注册满 1 周
- 可以正常登录 ClawHub
- 可以使用 `clawhub whoami` 确认身份

## 推荐发布参数

### 推荐 slug

- `amath-skill`

如果已被占用，可选：

- `amath-socthink`
- `socthink-amath`
- `socthink-math-skill`

### 推荐 tags

- `education`
- `math`
- `olympiad`
- `socratic`
- `learning`
- `latest`

### 推荐 changelog

首发版本可直接使用：

> Initial public release with curriculum discovery, problem lookup, Socratic tutoring flow, and quiz entry points for Socthink.

## 发布后立即检查

发布后立刻做这 5 步：

1. 打开 ClawHub 页面，确认名称、描述、标签正确
2. 检查 `SKILL.md` 是否被正常解析展示
3. 用另一台机器或新 workspace 测试安装
4. 在 README 和官网中添加 ClawHub 链接
5. 去 OpenClaw Discord 发第一条展示帖

## 推荐验证命令

```bash
clawhub whoami
clawhub search "amath"
clawhub search "socthink"
```

## 发布后 24 小时动作

### 0-2 小时

- 发 OpenClaw Discord 首帖
- 发 GitHub 仓库动态
- 发 X / Telegram / 微信群短帖

### 2-12 小时

- 收集安装反馈
- 修正描述、标签、README 表达
- 补截图或录屏

### 12-24 小时

- 再发一次 demo 内容
- 引导用户收藏、评论、安装
- 把官网入口和 ClawHub 链接一起传播

## 成功标准

以下至少满足 4 项，说明首发有效：

- ClawHub 可搜索到 skill
- 有用户能成功安装
- 有用户实际跑通课程树或 chat demo
- 有社区互动或评论
- 有人从 skill 跳转到官网 <https://amath.socthink.cn>
