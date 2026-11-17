# API 文档撰写实战手册（api-doc-generator 增量方法论）

> 子技能 `api-doc-generator` 负责「从代码生成 OpenAPI」。本文档补它**装不下**的部分：
> 生成的 spec 怎么写才算好文档、REST 与 GraphQL 文档策略差异、版本演进怎么不破坏调用方、示例质量怎么保证。

## 1. 决策树：这份 API 文档该怎么组织？

```text
要写 API 文档
├─ 是 REST / JSON 接口？
│   ├─ 是 → OpenAPI 3.x，按「资源」分组（见第 3 节）
│   └─ 否 ↓
├─ 是 GraphQL？
│   ├─ 是 → Schema + Playground + 按 Query/Mutation 注释（见第 2 节）
│   └─ 否 ↓
├─ 是 WebSocket / 流式？
│   └─ 是 → 消息协议文档（事件表 + 字段说明），非 OpenAPI
└─ 内部 RPC？ → 注明「内部」，不必全套 OpenAPI
```

## 2. REST vs GraphQL 文档策略

| 维度 | REST (OpenAPI) | GraphQL |
|------|----------------|---------|
| 文档单位 | 端点（path+method） | 类型与字段 |
| 自动生成 | 扫路由/注解 |  introspection + schema 注释 |
| 示例组织 | 每端点请求/响应 | 每 Query/Mutation 示例 |
| 版本策略 | URL 或 header 版本 | 演进式（少版本，加字段不删） |
| 痛点在 | path 爆炸、参数散 | 字段说明缺失、N+1 隐蔽 |

> GraphQL 没有「端点」概念，硬套 OpenAPI 会丢失 resolver 语义。按类型写字段级说明才是正路。

## 3. OpenAPI 撰写质量矩阵

| 要素 | 劣质文档 | 优质文档 |
|------|----------|----------|
| 描述 | 「获取用户」 | 「按 ID 获取用户资料，不含私密字段；不存在返回 404」 |
| 参数 | 只列名 | 列类型、必填、约束、示例值 |
| 响应 | 只给 200 | 覆盖 4xx/5xx 与错误体结构 |
| 示例 | 无 / 占位 | 可复制的 curl + 真实响应片段 |
| 鉴权 | 一句「需登录」 | 写明 Bearer 位置与获取方式 |

**铁律**：每个端点至少要有「一句说清语义的描述 + 一个可复制请求示例 + 错误响应结构」。三者缺一是半成品。

## 4. 版本演进不破坏调用方

```text
接口要改
├─ 新增字段 / 新端点？ → 向后兼容，MINOR 或 PATCH，旧调用方无感
├─ 改字段含义 / 改响应结构？ → 标 deprecated，保留旧版一段时间
├─ 删字段 / 改路径？ → 破坏性，MAJOR，旧版 URL 并行保留一个周期
└─ 同步更新 OpenAPI 的 info.version 与 Changelog
```

示例：在 OpenAPI 里标记弃用而非删除：

```yaml
paths:
  /v1/users/{id}:
    get:
      deprecated: true
      description: 请改用 /v2/users/{id}
```

## 5. 示例质量：可复制优先

差的示例：`{ "data": "..." }`（调用方还要猜）。好的示例：

```http
GET /v1/users/42 HTTP/1.1
Authorization: Bearer <token>
```

```json
{
  "id": 42,
  "name": "Ada",
  "roles": ["reader"]
}
```

提供 **curl 命令**让调用方一键试，比长篇说明更有效。OpenAPI 的 `examples` 字段直接承载这些。

## 6. 与脚本的闭环

仓库文档门禁可防止 API 文档回归（死链、未标注块）：

```bash
python3 scripts/check_md_links.py openapi.md docs/api/
python3 scripts/check_code_blocks.py openapi.md docs/api/
```

> 注意：OpenAPI 常是 `.yaml` 而非 `.md`，上述脚本默认只扫 `.md`。API 文档若以 Markdown 承载（如 `docs/api.md` 内含示例），才进脚本范围；纯 YAML spec 请用专用 linter（如 spectral）另行校验。

## 7. 典型坑与规避

1. **只生成不润色**：自动生成的 spec 描述常为空 → 每个端点补一句人类语义。
2. **示例用假数据且不自洽**：示例里 user id=42 但响应写 id=7 → 调用方困惑，务必一致。
3. **错误响应不建模**：只写 200，4xx 靠调用方猜 → 用 `responses` 覆盖关键错误。
4. **版本靠 URL 硬分又不维护旧版**：`/v1` 说弃用却立刻下线 → 保留并行周期并写进 Changelog。
5. **鉴权写「详见后台」**：调用方无法自服务 → 写明 token 获取与携带方式。
6. **GraphQL 当 REST 写**：用 OpenAPI 硬套 resolver → 按类型与字段组织文档。

## 8. 实战：一个端点的完整 OpenAPI 片段

```yaml
/users/{id}:
  get:
    summary: 按 ID 获取用户
    description: 返回公开资料字段；用户不存在返回 404；无令牌返回 401。
    parameters:
      - name: id
        in: path
        required: true
        schema: { type: integer }
        example: 42
    responses:
      '200':
        description: 成功
        content:
          application/json:
            example:
              id: 42
              name: Ada
              roles: ["reader"]
      '401':
        description: 缺少或无效令牌
      '404':
        description: 用户不存在
```

这段满足第 3 节质量矩阵：语义描述、参数约束+示例、错误响应、自洽示例。

## 9. 鉴权文档模式（最常写错的部分）

| 鉴权方式 | 文档应写清 |
|----------|------------|
| API Key | 放在哪（header/query）、如何申请、轮换方式 |
| Bearer Token | 获取端点、有效期、刷新机制 |
| OAuth2 | 授权码流程、scope 含义、回调地址 |
| 签名（HMAC） | 签名算法、时间戳防重放、密钥保管 |

> 通用错误：只写「需鉴权」。调用方要的是「把 token 放在 `Authorization: Bearer` 头里」这种可操作指令。

## 10. CI 中的 API 文档校验

```yaml
# 生成 + 校验 OpenAPI，破坏结构则失败
- run: python3 -m skills.api_doc_generator --check openapi.yaml
- run: spectral lint openapi.yaml        # 第三方 OpenAPI linter
- run: python3 scripts/check_md_links.py docs/api.md   # 文档内链接
```

> 纯 YAML spec 的结构校验用 spectral 等专用工具；本仓库的 `check_md_links` / `check_code_blocks` 只覆盖 Markdown 载体（如 `docs/api.md` 里的示例与说明），二者职责互补，不互相替代。

## 11. 典型坑与规避（续）

7. **info.version 不更新**：spec 改了但版本号没动 → 调用方无法判断是否破坏，每次发布同步版本。
8. **示例只覆盖成功路径**：调用方最怕错误处理，4xx/5xx 必须有可复制示例。
9. **分页/游标不说明**：列表接口不写 `next_cursor` 含义 → 调用方实现轮询出错。
10. **字段类型与代码不符**：spec 写 `string` 代码返回 `number` → 客户端解析崩，spec 须来自真类型。

## 12. 可勾选清单

- [ ] REST 用 OpenAPI 3.x 按资源分组；GraphQL 按类型写字段说明
- [ ] 每个端点有语义描述 + 可复制请求 + 错误响应结构
- [ ] 参数含类型/必填/约束/示例
- [ ] 示例数据自洽（id 一致、可复制）
- [ ] 破坏性变更已标 deprecated 并保留旧版周期
- [ ] OpenAPI info.version 与 Changelog 同步
- [ ] 文档内链接存活、代码块已标注（脚本核查通过）
- [ ] 内部 RPC 明确标注「内部」，不混入对外 spec
- [ ] 鉴权文档含可操作指令（头/获取/轮换）
- [ ] 分页/游标/错误路径均有示例
- [ ] spec 字段类型源自代码真类型，非手编

## 13. 文档站集成与本地预览

生成的 OpenAPI 不只给人读，更要可交互：

```bash
# 本地起 Swagger UI 预览
npx swagger-ui-serve openapi.yaml
# 或 Redoc
npx redoc-cli serve openapi.yaml
```

交付建议：把 OpenAPI 推到文档站（如 Redocly / Stoplight），让调用方能「试一试」。纯静态 `docs/api.md` 适合进 Git 但缺乏交互；两者并存最佳——spec 为权威，Markdown 为入门。

> 一致性提醒：若同时维护 `openapi.yaml` 与 `docs/api.md`，任一处改了端点，另一处要同步，否则出现「文档说支持、实际不支持」。把生成接进 CI 是唯一可持续解法。

## 相关子技能与层次边界

本文补 [skills/api-doc-generator/](../skills/api-doc-generator/SKILL.md) **装不下**的判断层：`api-doc-generator` 负责「从代码提取端点生成 OpenAPI」，本文负责「生成的 spec 怎么写才算好文档、REST vs GraphQL 策略、版本演进不破坏调用方、示例质量怎么保证」。

- 直接服务子技能：[skills/api-doc-generator/](../skills/api-doc-generator/SKILL.md)
- 兄弟参考：
  - [references/doc-lifecycle-and-pipeline.md](doc-lifecycle-and-pipeline.md)（API 文档在生成顺序中的位置与一致性）
  - [references/diagram-selection-guide.md](diagram-selection-guide.md)（API 文档里的架构图/时序图选区）
- 配套确定性资产：
  - [scripts/check_md_links.py](../scripts/check_md_links.py) — 文档内链接存活核查（第 6/10 节，仅覆盖 `.md` 载体）
  - [scripts/check_code_blocks.py](../scripts/check_code_blocks.py) — 代码块语言标注核查（第 6/10 节）
  - [assets/markdown-lint-rules.json](../assets/markdown-lint-rules.json) — 脚本规则源
- 边界提示：纯 YAML spec（`.yaml`）结构校验请用 spectral 等专用工具，本仓库脚本只覆盖 Markdown 载体（如 `docs/api.md` 内示例），二者职责互补。
