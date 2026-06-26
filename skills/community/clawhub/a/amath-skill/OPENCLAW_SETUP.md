# OpenClaw 接入说明

如果你的目标不只是“接入成功”，而是让这个 skill 成为 Socthink 的对外试用入口，那么安装完成后，务必优先演示以下路径：

1. 课程树
2. topic / 单题
3. Socratic chat
4. quiz

这样用户会从“知道有这个项目”变成“想继续去官网使用”。

基于官方文档：

- 官网：https://openclaw.ai/
- 文档：https://docs.openclaw.ai/
- Skills 文档：https://docs.openclaw.ai/tools/skills

当前仓库已经把 `amath_skill` 补齐成两层结构：

1. `amath_skill`：Python API / CLI / MCP 能力层
2. `openclaw_skills/amath-socthink`：OpenClaw 原生 Skill 目录

对 OpenClaw 来说，真正需要安装的是第 2 层，也就是 `SKILL.md` 所在的技能目录。

## 1. 安装并确认 OpenClaw Gateway

官方最短路径：

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
openclaw onboard --install-daemon
openclaw gateway status
openclaw dashboard
```

默认信息：

- Gateway UI: http://127.0.0.1:18789/
- 配置文件: `~/.openclaw/openclaw.json`

## 2. 安装本项目依赖

当前仓库使用已有虚拟环境即可：

```bash
cd /path/to/amath_skill
../.venv/bin/pip install -r requirements.txt
```

## 3. 配置环境变量

复制环境变量文件：

```bash
cd /path/to/amath_skill
cp .env.example .env
```

默认值已经指向：

- `AMATH_BASE_URL=https://amath.socthink.cn`
- `AMATH_API_PREFIX=/api`

如需默认登录态，可在 `.env` 中填写：

```env
AMATH_ACCESS_TOKEN=你的token
```

## 4. 安装 OpenClaw 原生 Skill

官方 Skills 加载优先级：

1. `<workspace>/skills`
2. `~/.openclaw/skills`
3. bundled skills

当前 skill 目录：

- [amath_skill/openclaw_skills/amath-socthink/SKILL.md](amath_skill/openclaw_skills/amath-socthink/SKILL.md)

推荐直接执行安装脚本：

```bash
cd /path/to/amath_skill
./install_openclaw_skill.sh
```

它会安装到：

- `~/.openclaw/skills/amath-socthink`

如果想手动复制，也可以：

```bash
mkdir -p ~/.openclaw/skills
cp -R /path/to/amath_skill/openclaw_skills/amath-socthink ~/.openclaw/skills/
```

## 5. Skill 的实际执行方式

这个 OpenClaw 原生 Skill 会通过 host `bash` 工具调用：

- [amath_skill/run_amath_cli.sh](amath_skill/run_amath_cli.sh)

该脚本进一步调用：

- [amath_skill/amath_skill/cli.py](amath_skill/amath_skill/cli.py)

所以当前方案已经不是“仅 MCP stdio 进程注册”，而是对齐官方 Skills 机制的原生技能目录方案。

## 6. 验证方式

建议在 OpenClaw 中新开一个 session 后测试：

1. 让它使用 `amath-socthink`
2. 执行 health check
3. 拉取奥数探险课课程树
4. 拉取某个 topic 详情
5. 拉取单题详情
6. 启动 chat 或 quiz

推荐的引流式演示脚本：

1. 先让它拉课程树，建立体系感
2. 再打开一个 topic 或单题，证明内容可下钻
3. 再启动 chat，让用户看到 Socratic 引导体验
4. 最后进入 quiz，把试用转成深度体验
5. 演示结束后，引导到官网继续使用：<https://amath.socthink.cn>

重要说明：

- OpenClaw 会在 **session 开始时** 快照可用 skills
- 新安装或新修改的 skill，最好在 **新 session** 中验证
- 如果旧 session 里看不到新 skill，不代表安装失败

当前已实测：

- `openclaw skills list` 可见 `amath-socthink`
- `openclaw skills info amath-socthink` 显示状态为 `Ready`
- 新 session 中已成功调用该 skill 执行 health check

## 7. 当前结论

当前对 OpenClaw 最重要的交付物是：

- [amath_skill/openclaw_skills/amath-socthink/SKILL.md](amath_skill/openclaw_skills/amath-socthink/SKILL.md)
- [amath_skill/run_amath_cli.sh](amath_skill/run_amath_cli.sh)
- [amath_skill/amath_skill/cli.py](amath_skill/amath_skill/cli.py)
- [amath_skill/install_openclaw_skill.sh](amath_skill/install_openclaw_skill.sh)

这套结构已经与 OpenClaw 官方 Skill 机制对齐，并已完成本机安装与实测。

如果用于对外传播，建议始终把以下两项放在一起：

- skill 体验入口
- 官网入口：<https://amath.socthink.cn>

这样这个 skill 就不只是技术接入件，而是一个可持续导流到 Socthink 主产品的前置体验入口。
