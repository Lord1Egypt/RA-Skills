# 术语与返回语义字典

用于统一根路由、L2/L3 子技能、编排契约中的命名，减少跨文档歧义。

## ID/URL 命名

| 术语 | 含义 | 典型来源 |
|---|---|---|
| `task_id` | 异步任务 ID | TTS、对口型、AI 创作等 submit 接口 |
| `video_id` | 视频合成任务 ID | video-compose/avatar create video |
| `person_id` | 数字人形象 ID | customised-person / list_figures |
| `voice_id` | 克隆音色 ID | tts-voice-clone |
| `output_url` | 通用远端产物地址 | AI 创作任务输出 |
| `video_url` | 远端视频地址 | poll_video / poll_task |
| `audio_url` | 远端音频地址 | tts poll 结果 |

## outcome_code 统一语义

| code | 含义 | 典型触发 |
|---|---|---|
| `ok` | 执行成功 | 拿到可交付 URL 或本地路径 |
| `need_param` | 缺少必要参数 | 必填参数缺失、脚本参数校验失败 |
| `auth_required` | 鉴权不可用 | `10400`、凭据缺失或过期 |
| `upstream_error` | 上游调用失败 | `50000`、第三方接口失败 |
| `timeout` | 任务超时 | 轮询超过上限仍未完成 |

## 使用要求

1. 新增或修改子技能时，优先复用本字典命名。
2. 若必须引入新术语，先在本字典登记，再在对应 `*-SKILL.md` 使用。
3. 禁止在不同文档对同一对象使用多个不兼容名称。
