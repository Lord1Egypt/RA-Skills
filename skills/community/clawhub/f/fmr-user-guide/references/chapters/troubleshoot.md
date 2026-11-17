# 排障

## 进入条件

- 症状话术族：router 挂了/起不来/转圈、4xx、切了没生效、模型不可用、503。
- 分发进入：install、upgrade 章失败时自动跳入。

## 固定开局

1. 跑 SKILL.md 全探针（P1→P2→P3），确定当前状态；**接口面不符态也是合法开局**（按 SKILL.md 判定表后注处置，探针按证据层级执行）；
2. `event-check` 一次——通知事件是诊断输入（输出解读见 `${CLAUDE_SKILL_DIR}/references/data/events.md`；`modelFailover`/`modelRescue`/`modelDisabled`/`modelUnavailable` 标"已自动处理"，但它们正是掉线/切换询问的答案）。

## 症状 → 处置

按 `${CLAUDE_SKILL_DIR}/references/data/failure-modes.md`（21 条起步）匹配。三条高价值条目单独强调：

- **假成功**：5678 被旧进程占用时，新进程因端口冲突退出，但安装器/CLI 的轮询会拿到旧进程的 200 应答而误报"已启动"。识破法 = 版本门 P4 比对应答方版本（`/api/status` 的 `version` vs 安装版本目录 `package.json`）；不一致即当前在跟旧进程说话。
- **明文 key 雷区**：运行期手改 `data/router-config.json` 有回退风险——手改出格式错误 Router 会回落默认配置，key"看似丢失"，实际在自动备份 `router-config.json.bak-*` 里。恢复：停 Router → 用 `.bak` 回滚 → 平台拉起面重启。
- **旧版 core 误拉起**：机器上有 Skill 形态 CLI 时，Router 停止状态下跑它会拉起旧版 core（写共享数据、占端口）——判活走探针，勿拿 CLI 当探针（见 usage 章③类陷阱）。

## 清单未命中（未知故障）

症状与清单均不匹配时，**不硬套最像的条目下结论**，按有界探索处理：

1. **只读探索不设限**：排障三件套、只读 REST（GET）、`/admin` 面板观测，必要时读本机安装源码（安装目录 `current/core/*.js`，只读——FMR 侧事实以源码为准，它是未知故障时信号最高的诊断资源）；交叉验证形成假设；
2. **写探索过三道门、单变量**：REST 直调优先，每个假设只动一个变量——动前回读基线，动后按完成判据回读验证。不改安装目录与源码（补丁属 upgrade 章地盘，乱补会让版本门失真）、不碰 data-map 禁区；
3. **探索有预算**：连续两轮"假设→验证"未收敛即停，转下方完成判据的"修不好"分支如实上交，不无限试错——探索烧的是用户的真实故障窗口；
4. **确诊即提议回写**：确认根因与处置后，向用户提议把该故障模式回写 failure-modes（格式对齐表内六列，内部判据须机器可观测；**用户确认后才改本仓库**）；若探明的是 FMR 侧事实与技能记载不符，不进清单，提议勘误回写（须用户确认），由仓库维护层落账。

## 处置纪律

- 写操作按三级写阶梯（REST ＞ 面板 ＞ 白名单手改）；写入位置先查 `${CLAUDE_SKILL_DIR}/references/data/data-map.md` 禁区表。
- 排障数据三件套：`data/router.pid`（判活）、`logs/request-journal-<date>.jsonl`（哪次请求走了哪个 provider、为何失败；保留 7 天 + 100MB 上限）、`data/events.json`（近期故障/切换/救援事件）。
- **logs/ 全量清单**（`~/.free-model-router/logs/`，三件套不够时按问题类别选用）：
  - `router.log` / `router-error.log`：Router 进程 stdout / stderr（standalone 启动器重定向落盘）——启动失败、端口占用、watcher 降级、更新 drain 等运行叙事；超 10MB 在下次拉起时轮转为 `.1`；
  - `monitor-error-<date>.log`：逐请求监控记录（JSON 行，含 attempts 尝试链与延迟）——查"某次请求内部经历了什么"，与 request-journal 互补；
  - `server-client.log`：与控制服务器的注册/同步通信——`lastSync` 失联、设备注册类问题主战场；
  - `standalone.log`：standalone 引导日志（数据目录定位、隐藏启动模式）——"服务为什么没起来"先看这里；
  - `reasoning-content-errors.jsonl`：默认关闭（环境变量 `FMR_REASONING_DIAG_LOG=1` 或配置 `reasoningDiagnosticLogEnabled:true` 开启），仅在排查 reasoning_content 类问题时建议用户开启，不代改配置。
- 读日志注意：日志文件为 UTF-8，直读若见乱码是终端码页伪象而非文件损坏——按时间戳与 ASCII 结构判读，或用按 UTF-8 解码的工具读；勿按 GBK 转码，会得到错误文本。
- 内容自撰：官网无排障文档页、FAQ 有误（配置文件名、CLI 命令名均与源码不符），排障内容不引用官网。

## 完成判据

- 修复成立：**故障前失败的那类请求现在成功**（机器可观测），且根因能在事件/日志中找到对应条目佐证。
- 修不好：如实报告当前所处状态（哪些探针过/不过、已尝试什么），给出人工升级指引——`/admin` 面板反馈入口或官网首页微信群。不谎称已修复。
