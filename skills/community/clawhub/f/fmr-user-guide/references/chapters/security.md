# 数据流向与安全

## 进入条件

- 用户询问数据流向/隐私："会上传我的数据吗""对话会不会被收集"。
- 强制前置：access 章跨机改绑定之前，先向用户交代本告警，用户知悉后才动。

## 数据流向自白

以 FMR 源码包内 SKILL.md「数据流向说明」与 `_meta.json` 的 security 块为权威源（官网口径不完整，不作契约出处）。三层：

1. 用户 → 接入层 harness → `127.0.0.1:5678` 本地 Router——请求处理在本机；
2. 本地 Router → 外部模型 Provider——**提示词和模型响应会经过 Provider 的服务器**（用任何云端模型皆然，非 FMR 收集）；
3. 本地 Router ↔ freemodel 控制服务器——注册匿名设备 API Key、拉取渠道列表与模型元数据、可选的匿名健康上报（模型延迟/可用性；**默认关闭**，`POST /api/reporting {enabled:false}` 或面板可关，重开只能面板）。同步内容不含对话内容。设备指纹 = SHA256(hostname+homedir+platform+arch)，不可逆，仅用于区分设备。

## 风险清单（改绑定/远程暴露前逐条告知）

- `/v1` 未注册设备时**免鉴权**：绑 `0.0.0.0` 的未注册实例在公网上等于无密码代理（`/v1/models` 则任何情况免鉴权）；
- 无 TLS：全程明文 HTTP，远程接入时设备 Key 明文传输；
- 无按-harness 凭证：整个 Router 只有一把设备 Key，无法给多个（尤其远程）harness 分别发证、单独吊销；
- 渠道 API key 明文存于 `data/router-config.json`：本机文件权限即 key 权限（agent 代配 key 前的声明即指此）。

## 公告渠道与渠道动态

公告无官网页：机制与事件类型见 `${CLAUDE_SKILL_DIR}/references/data/events.md`；渠道注册以运行时 `GET /api/providers` 为准（渠道动态原则见 SKILL.md，模板见 provider-registration.md）。版本号不从官网读（站点版本信息失真），以 `GET /api/status` 与版本目录 `package.json` 为准。

## 完成判据

- 用户在获知上述风险清单**之后**才执行改绑定/远程暴露决策（对话顺序可观测：告警在前，操作建议在后）；
- 本章只陈述与指引，不改任何数据。
