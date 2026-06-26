# dimens-manager 团队上下文章节 上下文来源说明

## 1. 文档目标

这份文档专门解释 `dimens-manager/references/team/overview.md` 里最容易被忽略的一件事：

同一个命令最终使用哪个 `teamId`、`projectId`，不一定只取决于命令行上这一行参数。

在 CLI 场景里，团队和项目上下文通常至少有三类来源：

1. 显式命令参数
2. 本地 profile 默认值
3. 环境变量覆盖

如果不先把这层说清楚，后面“为什么查到的不是我以为的团队 / 项目”这类问题会反复出现。

---

## 2. 默认判断顺序

分析上下文问题时，建议固定按下面顺序检查：

1. 当前命令有没有显式传 `--team-id` / `--project-id`
2. 本地 profile 里是否已经通过 `auth use-team` / `auth use-project` 写过默认值
3. 环境变量是否又覆盖了默认配置

Skill 说明时不要只盯当前命令参数，也不要默认 profile 一定正确。

---

## 3. 三类上下文来源

### 3.1 显式命令参数

最直接，也最适合排查问题时使用。

例如：

```bash
dimens-cli project list --team-id TTFFEN --output json
dimens-cli sheet info --team-id TTFFEN --project-id PUQUNFE --sheet-id sh_ja2IwgaBhV1jUWB4
```

适用场景：

- 排查具体团队 / 项目问题
- 避免被本地默认值误导
- 写案例文档时明确上下文

### 3.2 本地 profile 默认值

通过下面两类命令写入：

```bash
dimens-cli auth use-team TTFFEN
dimens-cli auth use-project PUQUNFE
```

特点：

- 后续很多命令可以省略部分参数
- 日常使用更方便
- 但排查问题时也最容易把人带偏

### 3.3 环境变量

环境变量通常用于脚本或自动化场景。

特点：

- 适合批处理、CI、脚本集成
- 更隐蔽，用户容易忘记自己设置过
- 一旦存在，会让“本地 profile 明明不是这个值，为什么结果还是这样”这类现象更难判断

这里的重点不是穷举变量名，而是提醒 Skill 必须把“环境覆盖”作为排查项。

---

## 4. 为什么 `use-project` 不能脱离团队单独理解

项目不是全局根资源，而是团队下面的业务单元。

因此：

- `projectId` 的解释天然依赖 `teamId`
- “切默认项目”本质上仍然是在某个团队上下文内切换业务单元
- 如果团队上下文本身错了，后续很多表格、文档、AI、工作流命令都会一起偏掉

Skill 解释时建议固定提醒：

1. 先确认当前团队
2. 再确认当前项目
3. 最后再看表、字段、行等下游资源

---

## 5. 排查模板

当用户说“为什么 CLI 查出来不是我那个项目”时，建议按下面模板输出：

```md
先不要直接怀疑接口结果，先检查上下文来源：

1. 当前命令是否显式传了 `teamId` / `projectId`
2. 本地 profile 是否已经通过 `auth use-team` / `auth use-project` 写入默认值
3. 是否存在环境变量覆盖

如果要做稳定排查，建议先显式传入 `--team-id` 和 `--project-id`，把上下文固定住。
```

---

## 6. 与其他 references 的关系

建议按下面顺序组合使用：

1. 先看本文件，确认上下文到底从哪里来。
2. 再看 `project-entry.md`，确认为什么系统建设和表格能力都要先从团队 / 项目入口进入。
3. 最后看 `examples.md`，确认 `project list`、`project info`、`auth use-team`、`auth use-project` 的真实命令和返回结构。
