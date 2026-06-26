# Auto Config Skiller (自动配置助手)

该技能旨在为 OpenClaw 用户提供一键式的环境初始化、基础技能安装及核心配置服务。

## 场景描述
当你刚刚安装好基础的 OpenClaw 后，可以使用此技能快速补全“小龙虾”生态所需的核心 Skill 和 Python 依赖库，避免手动克隆仓库和配置 `.env` 的繁琐过程。

## 核心分类编排
为了让 OpenClaw 更具战斗力，我们将技能分为以下四个核心维度：

1. **通讯 (Communication)**
   - `Feishu-OpenClaw`: 飞书官方插件，支持文档、群聊、日历及 Meego 深度集成。
2. **基础工具 (Basic Tools)**
   - `CN-Life Toolkit`: 国内生活服务（天气、快递、油价等）。
   - `Exec Tool / Web Search`: 核心执行与搜索能力。
3. **优化工具 (Optimization Tools)**
   - `Skill-Self-Improving`: 让 AI 在交互中自我优化。
   - `ClawRouter`: 智能路由，优化成本。
4. **安全工具 (Security Tools) - [必装]**
   - `Skill-Vetter`: 技能审计大师，安装其他技能前的第一道防线。
   - `Clawscan`: 安全扫描。

## 工作流 (Workflows)
1. **环境诊断 (Diagnosis)**
   - **官方通道**: 集成飞书诊断与修复工具 `openclaw-lark-tools`。
   - **配置自检**: 自动识别 `.env` 配置文件状态及目录写入权限。
   - **资源评估**: 检测磁盘空间等基础硬件状态。
2. **分类调研 (Research)**
   - 自动拉取 ClawHub 推荐列表，识别核心工具。
3. **全流程自动化安装 (Full Auto-Install)**
   - **一键启动**: 通过 `./setup.sh` 开启傻瓜化配置流。
   - **多源加速**: 集成 ClawHub 与 Tencent SkillHub，自动绕过登录限制与网络障碍。
   - **交互配环境**: 告别 `.env.example` 手动修改，实现对话式参数配置。
   - **灵魂注入**: 预设 `agency-agents` 库，一键下载高分 AI 人设 Prompt。

详细的操作指引与场景说明请参阅：[使用指南 (USAGE_GUIDE.md)](./docs/USAGE_GUIDE.md)


## 维护者
Antigravity
