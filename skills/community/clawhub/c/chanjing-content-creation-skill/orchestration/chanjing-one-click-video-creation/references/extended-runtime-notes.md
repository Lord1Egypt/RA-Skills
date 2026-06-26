# 安全、凭据与运行时契约（扩展说明）

**若与 [`../manifest.yaml`](../manifest.yaml) 或源码冲突，以 manifest 与源码为准。** 本文供阅读 `run_render` 与子 skill 时的补充说明。

## 安全、凭据与信任边界

环境变量与二进制以 **`manifest.yaml`** 为据。审阅时可对照技能包 **`description`** 与 **`manifest.yaml`**（含 **`agentPolicy`**）。

- **能力与管道**：步骤级说明见 [`workflow-orchestration.md`](workflow-orchestration.md)；`run_render` 职责见 [`run-render.md`](run-render.md)。
- **敏感与合规**：勿回显完整密钥；权限建议 **`0700` / `0600`**（配置脚本尽量设置）。
- **信任与出站**：HTTPS、按返回 URL 拉取媒体、`--output-dir` 落盘等须自行判断是否信任目标主机与链接。
- **浏览器**：本编排不负责触发登录页；凭证由顶层入口统一保证。
- **Agent 策略**：**`manifest.yaml`** · **`agentPolicy`**。

## 运行时契约（环境变量、二进制、副作用与落盘）

与 **`scripts/run_render.py`** 及同仓库子 skill 对齐；与 **`manifest.yaml`** 一致。

### 环境变量（常见，与 manifest 合并阅读）

命名以仓库根 **`合规规则.md`** §3 为准；环境变量以 manifest 与 [`../../../references/top-level-runtime-contract.md`](../../../references/top-level-runtime-contract.md) 为准。

| 变量 | 说明 |
|------|------|
| **`CHANJING_API_BASE`** | 默认 `https://open-api.chanjing.cc`。 |
| **`CHANJING_APP_ID`** | 鉴权应用标识（推荐在项目 `.env` 配置）。 |
| **`CHANJING_SECRET_KEY`** | 鉴权密钥（推荐在项目 `.env` 配置）。 |
| **`CHAN_SKILLS_DIR`** | 含 `skills/chanjing-tts` 等的仓库根；未设时由 `run_render.py` 从脚本路径向上推断。 |
| **`AI_VIDEO_PROMPT_MAX_CHARS`** | 默认 **8000**。 |
| **`AI_VIDEO_MODEL`** | 文生视频 `model_code` 缺省。 |

> 外部文档中的 **`FIRST_DIGITAL_HUMAN_MAX_CHARS`** 等变量，**若当前 `run_render.py` 未读取**，以源码为准；若日后增加 `os.environ` 读取，应同步 manifest 与本文。

### 外部二进制

| 二进制 | 说明 |
|--------|------|
| **`ffmpeg`** | 跑 **`run_render.py` 一键成片路径时必需**：拼接、转码、封装。 |
| **`ffprobe`** | **同上**：分辨率、时长、旋转等元数据对齐。 |
| **`chan-skill`** | 可选；或与同仓库 **`python`** 直接调用子技能 CLI 等价。 |

### 典型副作用（类）

| 类型 | 说明 |
|------|------|
| **出站 HTTPS** | Open API 与接口/CDN 返回的媒体 URL 拉取。 |
| **本地文件** | **`run_render.py --output-dir`** 下 **`final_one_click.mp4`**、**`workflow_result.json`**、**`work/`** 等；细节以 **`templates/render-rules.md`** 为准。 |
| **子进程** | **`ffmpeg` / `ffprobe`**；`subprocess` 调用 **`chanjing-tts`**、**`chanjing-video-compose`**、**`chanjing-ai-creation`** 等脚本。 |
| **浏览器** | 本编排不触发登录页；由顶层入口统一处理凭证。 |

### 持久性与用户可控性

一键成片工件由 **`--output-dir`** 控制；凭据持久化路径以 **`manifest.yaml`** 与顶层入口约定为准，**勿将密钥提交版本库**。
