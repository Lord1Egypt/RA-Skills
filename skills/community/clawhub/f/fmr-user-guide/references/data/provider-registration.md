# 渠道注册与 key 录入（动态流程模板）

**渠道动态原则**：渠道随时增减——渠道名、数量、注册链接、额度一律以运行时接口下发为准，不硬编码任何一项。调研材料与官网上的渠道清单（"9 内置渠道""7 渠道指引"等）均为时点快照，只作背景。

## 流程

### 1. 拉权威列表

```
curl http://127.0.0.1:5678/api/providers
```

响应 `{ok: true, data: {<渠道id>: {...}}}`，每渠道关注字段：`id`（标识）、`website`（注册入口 URL）、`hasApiKey`（是否已配 key）、`enabled`（启停）、`status`（运行状态）。CLI `providers` 命令仅作人读辅助——打印层没有 `website` 列，注册链接以本接口为准。

### 2. 选渠道

用户未指定时，呈现未配 key（`hasApiKey=false`）且未删除的渠道清单供其挑选；`GET /v1/models` 返回的虚拟名可作"当前已可路由"的辅助参照。候选唯一时直接指定该渠道进入下一步，仍向用户如实呈现其状态。

### 3. 交人工注册（停下等待）

向用户逐渠道输出：注册链接（取该渠道 `website` 字段），并提示注册与创建 API key 的具体方式以该站实际为准（接口不下发此信息，不猜测、不代查站）。**输出后停下等待**用户自行完成注册拿 key——这是全技能唯一必须人工的环节，不代填、不声称已注册。

`website` 为空时的兜底：给 `https://community.freemodel.eu.org/#providers`。该站准确性差（版本号/渠道政策均有时滞），仅作链接兜底，不作事实源。

### 4. 录入 key（双通道，先声明风险）

先向用户声明：**渠道 key 以明文存于 `data/router-config.json`**，本机文件权限即 key 权限（要点即此句；security 章有展开，仅用户追问隐私细节时加载，不因本模板跨章）。由用户选择：

- **agent 代配**（REST）：

  ```
  curl -X POST http://127.0.0.1:5678/api/provider-key \
       -H "Content-Type: application/json" \
       -d '{"provider":"<渠道id>","apiKey":"<key>"}'
  ```

  （Skill 形态 CLI 同义命令 `providerApiKey <渠道id> <key>`。单 key **替换**语义；多 key 轮换 CLI 无对应命令，走面板或 REST `/api/provider-keys/*`。）

- **用户自助**：浏览器打开 `http://127.0.0.1:5678/admin`，渠道页录入（支持多 key 管理）。

### 5. 回读

`GET /api/providers` 核对该渠道 `hasApiKey=true`；`GET /api/models?provider=<id>` 返回非空模型列表（录入端点写后会自动拉模型，失败静默——回读是兜底判据）。**不回读即视为未完成。**

## 完成判据

输出给用户的注册链接逐条存在于本次 `GET /api/providers` 的 `website` 字段；会话内未代填 key、未声称已注册；录入后回读成立。
