# 指令罗盘技能文件适配报告

生成时间：2026-06-23

## 本次适配范围

- 技能文件源码目录：`D:\MyFiles\Work\javisHUD\备份-指令罗盘技能包-20260622\技能源码`
- 已改造文件：
  - `SKILL.md`
  - `skill-card.md`
  - `examples\daily-file-index-cards.example.json`
- 改造前备份：
  - `D:\MyFiles\Work\javisHUD\优化工作包-指令罗盘客户端-20260622\备份文件\指令罗盘技能包-改造前备份-20260623-165314`

## 依据的当前项目事实

Windows 客户端当前导入逻辑位置：

- `D:\MyFiles\Work\javisHUD\优化工作包-指令罗盘客户端-20260622\源码\prototype-sidebar\app.js`
- 核心函数：`normalizeCard()`、`parseImportedText()`、`targetBundleFromOpenTarget()`、`resourceKindForCard()`、`preferredOpenTarget()`

客户端当前可直接识别的核心字段：

- `schemaVersion`
- `id`
- `type`
- `title`
- `summary`
- `category`
- `libraryCategory`
- `libraryFolder`
- `tags`
- `instruction`
- `delivery`
- `permissions`
- `openTarget`
- `localFilePath`
- `localFolderPath`
- `resourceUrl`
- `resourceKind`
- `resourceMeta`
- `iconId`
- `accent`
- `deep`
- `risk`
- `riskReasons`
- `syncSource`
- `remoteId`
- `lastSyncedAt`
- `aiScore`
- `recommendationReason`
- `intentType`

官网当前相关标准：

- `D:\MyFiles\Work\javisHUD\优化工作包-指令罗盘客户端-20260622\源码\docs\command-compass-integration-standard.md`
- `D:\MyFiles\Work\javisHUD\备份-指令罗盘网站-20260622\data\card-schema-v1.json`
- `D:\MyFiles\Work\javisHUD\备份-指令罗盘网站-20260622\api\_lib\store.js`

## 原技能文件主要不兼容点

1. 原技能文件把客户端字段主要放在 `xCommandCompass` 内，但当前 Windows 客户端导入时优先读取顶层字段。
2. 原示例使用 `xCommandCompass.localPath`，但客户端实际识别的是 `openTarget`、`localFilePath`、`localFolderPath`、`resourceUrl`。
3. 原示例缺少 `resourceKind`，导致文件、文件夹、链接、网站收藏、下载目录等资源类型无法稳定区分。
4. 原示例 `delivery` 只有 `copyField` 和 `format`，客户端实际还使用 `delivery.targets`、`delivery.requiresConfirmation`。
5. 原说明中 `category: 本地资源` 不是当前客户端内置主分类，容易进入兜底分类。
6. 原说明没有明确“公开网站不能上传本地路径”，存在网站同步误用风险。

## 本次统一后的规则

1. CardSchema v1 公共字段保持官网兼容。
2. 客户端实际需要的字段放在顶层，确保 Windows 客户端直接导入可用。
3. 同时保留 `xCommandCompass` 镜像字段，方便官网和未来 API round-trip。
4. `instruction` 是唯一复制字段。
5. `openTarget` 是统一打开地址。
6. 本地文件使用：
   - `resourceKind: "file"`
   - `openTarget`
   - `localFilePath`
7. 本地文件夹使用：
   - `resourceKind: "folder"`
   - `openTarget`
   - `localFolderPath`
8. 网络链接和网站收藏使用：
   - `resourceKind: "url"` 或 `"webFavorite"`
   - `openTarget`
   - `resourceUrl`
9. 下载目录使用：
   - `resourceKind: "downloads"`
   - `openTarget`
   - `localFolderPath`
10. 云端同步必须默认 `syncMode: "confirm"`。

## 安全边界

- 不扫描全盘。
- 不自动读取本地文件正文。
- 不上传用户本地路径、本地文件名、文件内容、使用历史。
- 不在技能文件内保存 Token、Cookie、密码、API Key。
- 可执行文件、快捷方式、脚本类资源只作为打开地址记录，`permissions.shell` 保持 `false`，由客户端打开前确认。

## 验收标准

- `examples\daily-file-index-cards.example.json` 能被 JSON 解析。
- 示例卡片均包含 CardSchema v1 必填字段。
- 示例卡片均包含客户端顶层资源字段。
- 中部复制内容只来自 `instruction`。
- 文件、文件夹、链接在尾部使用 `openTarget` 打开。
- 网站同步字段不包含真实本地隐私数据。
- 官网 Agent 可按 `WEBSITE_AGENT_INSTRUCTIONS.md` 完成网站侧 API/schema 对齐。
