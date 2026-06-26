---
name: ecloud-eos
description: 移动云对象存储(EOS)技能。当用户需要上传、下载、管理云存储文件等操作时使用此技能。
metadata:
  {
    "openclaw":
      {
        "emoji": "☁️",
        "requires": {},
        "install":
          [
            {
              "id": "eos-s3-client",
              "kind": "node",
              "package": "@aws-sdk/client-s3",
              "label": "Install S3 Node.js SDK",
            },
            {
              "id": "eos-s3-request-presigner",
              "kind": "node",
              "package": "@aws-sdk/s3-request-presigner",
              "label": "Install S3 Request Presigner",
            },
            {
              "id": "eos-smithy-hash-node",
              "kind": "node",
              "package": "@smithy/hash-node",
              "label": "Install Smithy Hash Node",
            },
            {
              "id": "eos-smithy-protocol-http",
              "kind": "node",
              "package": "@smithy/protocol-http",
              "label": "Install Smithy Protocol HTTP",
            },
          ],
      },
  }
---

# 移动云 EOS 技能

通过 Node.js SDK 脚本管理移动云对象存储。

## 首次使用 — 自动设置

当用户首次要求操作 EOS 时，按以下流程操作：

### 步骤 1：检查当前状态

**检测操作系统并运行相应的检查脚本：**

- **Windows 系统：**
  ```powershell
  {baseDir}\scripts\setup.ps1 -CheckOnly
  ```

- **Linux/macOS 系统：**
  ```bash
  {baseDir}/scripts/setup.sh --check-only
  ```

检查脚本会验证以下内容：

1. **基础环境**：Node.js 和 npm 是否已安装
2. **Node.js SDK**：相关 Node.js SDK 依赖是否已安装
3. **环境变量配置**：检查以下环境变量是否已设置且有值：
   - `EOS_ACCESS_KEY` — 移动云对象存储 API 密钥 ID
   - `EOS_SECRET_KEY` — 移动云对象存储 API 密钥 Key
   - `EOS_REGION` — 存储桶区域
   - `EOS_BUCKET` — 存储桶名称
   - `EOS_ENDPOINT` — 存储桶公网域名

**判断标准：**

- ✅ **所有检查项都显示 OK**：配置已完成，可以直接使用 EOS 操作
- ⚠️ **部分环境变量缺失但可继续操作**：
  - 如果仅缺失 `EOS_BUCKET`，仍可执行部分操作：
    - `list-buckets`（列出所有存储桶）
    - `create-bucket`（创建新存储桶，需要手动指定桶名）
    - `delete-bucket`（删除存储桶，需要手动指定桶名）
- ❌ **其他环境变量缺失**：进入步骤 2，引导用户配置

**如果输出显示一切 OK（nodejs sdk 已安装、环境变量已配置），跳到「执行策略」。**

### 步骤 2：如果未配置，引导用户提供凭证

**方式一：直接提供凭证信息**

> 我需要您的移动云凭证来连接 EOS 存储服务。请提供：
> 1. **AccessKey** — 移动云对象存储 API 密钥 ID
> 2. **SecretKey** — 移动云对象存储 API 密钥 Key
> 3. **Region** — 存储桶区域
> 4. **Bucket** — 存储桶名称
> 5. **Endpoint** — 存储桶公网域名
>
> 您可以参考 [移动云控制台-首页](https://ecloud.10086.cn/op-help-center/doc/category/729) 订购对象存储。
> 您可以参考 [移动云控制台-创建认证信息](https://ecloud.10086.cn/op-help-center/doc/article/24501) 获取 AK/SK 认证信息。
> 您可以参考 [移动云控制台-地域和访问域名](https://ecloud.10086.cn/op-help-center/doc/article/48082) 获取最新的地域和域名信息。

**方式二：使用配置文件**

告诉用户：
> 您也可以提供一个配置文件，包含凭证信息。配置文件格式如下：
>
> ```properties
> accessKey=your-access-key
> secretKey=your-secret-key
> region=anhui1  # 请根据最新地域列表选择合适的region
> bucket=your-bucket-name
> endpoint=https://eos-anhui-1.cmecloud.cn  # 请根据最新地域列表选择对应endpoint
> ```
>
> 配置文件模板位于：`references/config_template.properties`
>
> 请将配置文件路径提供给我，我会使用它来设置环境。

### 步骤 3：用户提供凭证后，运行自动设置

**方式一：使用命令行参数**

**Windows 系统：**
```powershell
{baseDir}\scripts\setup.ps1 -AccessKey "<AccessKey>" -SecretKey "<SecretKey>" -Region "<Region>" -Bucket "<Bucket>" -Endpoint "<Endpoint>"
```

**Linux/macOS 系统：**
```bash
{baseDir}/scripts/setup.sh --access-key "<AccessKey>" --secret-key "<SecretKey>" --region "<Region>" --bucket "<Bucket>" --endpoint "<Endpoint>"
```

**方式二：使用配置文件**

**Windows 系统：**
```powershell
{baseDir}\scripts\setup.ps1 -CopyConfigFile "<path-to-config-file>"
```

**Linux/macOS 系统：**
```bash
{baseDir}/scripts/setup.sh --copy-config-file "<path-to-config-file>"
```

脚本会自动：

- 检查并安装 nodejs sdk（如果未安装）
- 从配置文件读取凭证并设置环境变量
- 验证 EOS 连接

**重要说明：**
- 您提供的配置文件不会被修改
- 环境变量会持久化保存（Windows 设置为 User 级别，Linux/macOS 写入 shell 配置文件）
- 重新打开终端后无需重新设置，新会话会自动使用这些环境变量
- **agent 必须更新自己的 process.env**：调用 setup.ps1 后，agent 应该根据传递的参数更新自己的 `process.env`，以便后续子进程能够读取到最新的环境变量：
  ```javascript
  // agent 更新自己的 process.env
  process.env.EOS_ACCESS_KEY = accessKey;
  process.env.EOS_SECRET_KEY = secretKey;
  process.env.EOS_REGION = region;
  process.env.EOS_BUCKET = bucket;
  process.env.EOS_ENDPOINT = endpoint;
  ```

### 步骤 4：执行策略

配置完成后，按照以下策略执行 EOS 操作：

1. **检查配置状态**：每次执行 EOS 操作前，先运行环境检查脚本确认配置正常
2. **直接执行操作**：确认配置正常后，直接执行相应的 EOS 操作命令
3. **环境变量管理**：
   - 所有操作凭证从环境变量读取
   - 切换桶操作通过 setup 脚本更新环境变量
   - 环境变量已持久化，新会话会自动使用

## 方式一：Node.js SDK 脚本

> 官方文档: https://ecloud.10086.cn/op-help-center/doc/outline/56247

通过 `scripts/eos_node.mjs` 执行存储操作。凭证从环境变量读取。

### 常用命令

> 以下省略 `node {baseDir}/scripts/eos_node.mjs` 前缀。完整格式：`node {baseDir}/scripts/eos_node.mjs <action> [options]`

```bash
# 列出所有存储桶
list-buckets

# 创建桶（需要手动指定桶名）
create-bucket --bucket my-new-bucket

# 删除桶（需要手动指定桶名，注意：桶必须为空才能删除）
delete-bucket --bucket my-old-bucket

# 清空桶（删除桶内所有文件，⚠️ 高危操作，必须使用 --confirm 参数确认）
empty-bucket --bucket my-bucket --confirm

# 切换存储桶（使用 setup 脚本）
#
# 切换存储桶需要调用 setup 脚本，因为需要更新系统环境变量。
# 调用方式如下：
#
# Windows 系统：
#   {baseDir}\scripts\setup.ps1 -SetBucket <bucket-name>
#
# Linux/macOS 系统：
#   {baseDir}/scripts/setup.sh --set-bucket <bucket-name>
#
# 示例：
#   Windows: {baseDir}\scripts\setup.ps1 -SetBucket my-new-bucket
#   Linux/macOS: {baseDir}/scripts/setup.sh --set-bucket my-new-bucket
#
# 说明：
#   - 切换桶后，系统环境变量会被更新，新会话会自动使用新的桶
#   - 切换操作会验证新桶是否可访问
#   - 如果新桶不存在或无权限，会显示警告信息
#   - **agent 必须更新自己的 process.env.EOS_BUCKET**：调用 setup.ps1 -SetBucket 后，agent 应该更新自己的 `process.env.EOS_BUCKET`，以便后续子进程能够读取到新的桶名

# 查询桶访问权限
get-bucket-acl

# 设置桶访问权限（private、public-read、public-read-write）
set-bucket-acl --acl private

# 设置防盗链（白名单模式，只允许指定域名访问）
set-referer --referers "https://example.com,https://www.example.com" --type allow

# 设置防盗链（黑名单模式，拒绝指定域名访问）
set-referer --referers "https://evil.com" --type deny

# 查询防盗链设置
get-referer

# 删除防盗链
delete-referer

# 上传文件
upload-object --file /path/to/file.jpg --key remote/path/file.jpg

# 下载文件
download-object --key remote/path/file.jpg --output /path/to/save/file.jpg

# 复制文件（同一桶内）
copy-object --source-key remote/path/source.jpg --dest-key remote/path/destination.jpg

# 复制文件（跨桶）
copy-object --source-key remote/path/source.jpg --dest-key remote/path/destination.jpg --dest-bucket target-bucket

# 列出文件（⚠️ 高危操作，遵循安全规范）
list-objects

# 带前缀列出文件（推荐做法：缩小查询范围）
list-objects --prefix "images/"

# 限制每页返回数量（默认100，最大100）
list-objects --max-keys 50

# 分页获取下一页（使用上一次返回的 nextMarker，每次翻页需用户确认）
list-objects --max-keys 50 --marker "file50.jpg"

# 查看文件信息
head-object --key remote/path/file.jpg

# 判断文件是否存在
exists-object --key remote/path/file.jpg

# 查询文件访问权限
get-object-acl --key remote/path/file.jpg

# 设置文件访问权限（private、public-read、public-read-write）
set-object-acl --key remote/path/file.jpg --acl public-read

# 生成文件共享外链（默认过期时间3600秒）
generate-url --key remote/path/file.jpg

# 生成文件共享外链（自定义过期时间，单位：秒）
generate-url --key remote/path/file.jpg --expires 7200

# 删除文件
delete-object --key remote/path/file.jpg
```

所有命令输出 JSON 格式，`success: true` 表示成功，退出码 0。

### 图片处理说明

图片处理扩展能力见下方“图片处理能力（新增）”章节。

---

## 使用规范

1. **禁止修改脚本文件**：agent 禁止修改 `scripts/` 目录下的任何文件
   - 只能通过约定的方式调用脚本
   - 不得读取、编辑或修改 `scripts/eos_node.mjs`、`scripts/setup.ps1`、`scripts/setup.sh` 等文件
   - 不得创建新的脚本文件
2. **操作前检查配置**：每次执行 EOS 操作前，先运行环境检查脚本
   - Windows: `{baseDir}\scripts\setup.ps1 -CheckOnly`
   - Linux/macOS: `{baseDir}/scripts/setup.sh --check-only`
   - 确认环境变量已设置后再执行操作
   - **特殊情况**：如果仅缺失 `EOS_BUCKET`，仍可执行以下操作：
     - `list-buckets`（列出所有存储桶）
     - `create-bucket`（创建新存储桶，需要手动指定桶名）
     - `delete-bucket`（删除存储桶，需要手动指定桶名）
3. **首次使用先运行环境检查**：
   - Windows: `{baseDir}\scripts\setup.ps1 -CheckOnly`
   - Linux/macOS: `{baseDir}/scripts/setup.sh --check-only`
4. **凭证不明文展示**：引导用户自行通过 setup 脚本设置环境变量，避免在对话中明文展示敏感信息
5. **所有文件路径**（`objectKey`/`EOSpath`/`--key`）为存储桶内的相对路径，如 `images/photo.jpg`
6. **错误处理**：调用失败时先用 setup 脚本检查环境和环境变量
7. **方式一脚本源码**见 `scripts/eos_node.mjs`
8. **跨平台兼容**：根据操作系统选择对应的 setup 脚本（Windows 用 .ps1，Linux/macOS 用 .sh）
9. **环境变量管理**：
   - 首次使用时，通过 setup 脚本设置环境变量
   - 环境变量会持久化保存（Windows 设置为 User 级别，Linux/macOS 写入 shell 配置文件）
   - 切换桶操作通过 setup 脚本更新环境变量
   - 新会话会自动使用这些环境变量，无需重新设置
10. **安全提示**：避免将包含敏感信息的配置文件提交到版本控制系统
11. **列举文件操作安全规范**（高危操作）：
   - **默认只查询一页数据**：默认每页返回 100 条，用户可指定 `--max-keys`（最大 100）
   - **分页查询需要用户确认**：返回第一页后，检查 `isTruncated` 字段，如果有更多数据，提示用户可以继续查询下一页，每次翻页都需要用户确认
   - **自动查询后续所有数据需二次确认**：
     - 如果用户要求自动查询后续所有数据，必须提示该操作可能造成较大开销
     - 必须等待用户明确确认后才能继续查询
     - 最多连续查询 10 页（最多 1000 条数据）
   - **分批查询机制**：如果查询 10 页后还有剩余数据，再次提示用户是否需要继续查询，每次最多连续查询 10 页
   - **推荐使用前缀过滤**：对于大型桶，强烈建议使用 `--prefix` 参数缩小查询范围，避免全量列举
   - **示例流程**：
     ```bash
     # 第一页查询
     node {baseDir}/scripts/eos_node.mjs list-objects --max-keys 100
     # 如果返回 isTruncated=true，记录 nextMarker 值
     # 第二页查询（需用户确认）
     node {baseDir}/scripts/eos_node.mjs list-objects --max-keys 100 --marker "file100.jpg"
     ```
   - **安全提示**：避免在对象数量巨大的桶上执行全量列举，优先使用 `--prefix` 参数缩小查询范围
12. **清空桶操作安全规范**（极高危操作）：
   - **必须使用 --confirm 参数**：执行清空桶操作时，必须显式传递 `--confirm` 参数，否则脚本会拒绝执行
   - **删除桶时的提示**：如果桶不为空，`delete-bucket` 操作会失败，错误消息会明确告知用户需要使用 `empty-bucket --confirm` 命令清空桶
   - **禁止自动执行清空操作**：脚本不会自动执行清空桶的操作，必须用户主动要求并确认
   - **操作流程**：
     ```bash
     # 尝试删除非空桶（会失败）
     node {baseDir}/scripts/eos_node.mjs delete-bucket --bucket my-bucket
     # 返回错误：桶不为空，无法删除。请先使用 empty-bucket 命令清空桶内的所有文件。
     # 注意：清空桶是高危操作，需要使用 --confirm 参数确认。

     # 用户决定清空桶（必须使用 --confirm 参数）
     node {baseDir}/scripts/eos_node.mjs empty-bucket --bucket my-bucket --confirm

     # 清空完成后，再删除桶
     node {baseDir}/scripts/eos_node.mjs delete-bucket --bucket my-bucket
     ```
   - **安全提示**：清空桶操作不可逆，删除后无法恢复。在执行清空前，建议先使用 `list-objects` 确认要删除的文件，对于生产环境的桶，建议先备份重要数据
13. **图片处理参数规范**：见下方“图片处理能力（新增）”章节

## 图片处理能力（新增）

以下内容为 EOS skill 新增的图片处理扩展，集中维护，避免与原有对象存储操作说明耦合。

### 依赖

- 图片处理沿用现有 EOS 凭证与环境变量
- 新增脚本依赖：`@smithy/hash-node`、`@smithy/protocol-http`

### 脚本边界

- `scripts/eos_node.mjs`
  - 仍负责通用 EOS 对象操作
  - 图片处理仅保留“生成带 `x-eos-process` 的签名访问链接”的轻量能力
- `scripts/eos_image.mjs`
  - 负责图片处理专属流程
  - 包括生成图片处理签名 URL、下载处理结果、通过 `sys/saveas` 持久化回桶

### 常用命令

```bash
# 生成图片处理签名链接
node {baseDir}/scripts/eos_image.mjs generate-url --key images/avatar.jpg --process "image/resize,w_400,h_400"

# 下载处理后的图片
node {baseDir}/scripts/eos_image.mjs download-object --key images/avatar.jpg --process "image/resize,w_400,h_400/rounded-corners,r_24" --output /tmp/avatar.png

# 持久化处理结果到当前桶
node {baseDir}/scripts/eos_image.mjs saveas-object --key images/avatar.jpg --process "image/resize,w_800,h_800/format,png" --target-key derived/avatar-800.png

# 持久化处理结果到指定桶
node {baseDir}/scripts/eos_image.mjs saveas-object --bucket source-bucket --key images/avatar.jpg --process "image/watermark,text_SGVsbG8" --target-bucket target-bucket --target-key outputs/avatar-watermark.jpg
```

### 能力边界

- 图片处理只针对 EOS 中已经存在的图片对象
- 图片处理请求统一使用 GET
- 处理型动作返回图片字节流，查询型动作如 `info`、`average-hue` 返回文本结果
- 私有对象必须把 `x-eos-process` 纳入签名 URL
- EOS 默认不保存处理结果；只有显式追加 `|sys/saveas,...` 时才会回写到桶
- 水印图片只能引用同桶内对象；网络图片或本地图片需先上传到 EOS
- 图片处理能力只在指定可用资源池内生效；其他资源池即使在 URL 后追加处理参数也不会生效
- 图片处理要求目标桶已为 `data_deliver` 用户开启 bucket policy 中的 `GetObject` 和 `PutObject` 权限；未开启时禁止使用图片处理

### 资源池

图片处理仅支持以下资源池：

- fenhu1    （华东-苏州3）
- beijing7  （华北-北京6）
- ningbo1   （华东-杭州）
- zhengzhou1（华中-郑州）
- zhengzhou4（华中-郑州2）
- fujian1   （福建-厦门）
- fujian2   （福建-厦门2）
- fujian3   （福建-厦门3）

除以上资源池外，其他资源池均不支持图片处理，表现为对象 URL 后拼接的处理参数无效。

### 调用规则

- agent 在执行任何图片处理前，必须先确认当前桶所属资源池是否在上述支持列表中；如果不在支持列表中，必须停止图片处理并明确告知用户“当前资源池不支持图片处理”
- agent 在执行任何图片处理前，必须检测目标桶是否已为 `data_deliver` 用户开启 bucket policy 中的 `GetObject` 和 `PutObject` 权限；若未开启，必须停止图片处理，并提示用户先完成 bucket policy 配置
- 未通过“资源池支持性检查”或“data_deliver bucket policy 检查”时，不允许生成图片处理签名 URL，不允许下载处理结果，也不允许执行 `sys/saveas`
- 处理串格式：`image/<action>[,<param>_<value>...]/<action>[,<param>_<value>...]`
- 多个处理 step 必须按顺序拼接，agent 不应重排用户已明确给出的 step
- 持久化格式：`image/...|sys/saveas,o_<object-key-base64url>,b_<bucket-base64url>`
- `sys/saveas` 中的对象 key 和桶名都需要使用 URL-safe Base64 编码
- `resize`、`crop`、`circle`、`info`、`rounded-corners`、`rotate`、`average-hue`、`watermark` 等都视为 `--process` 里的子动作，不单独定义为 CLI 一级命令
- 当用户已经明确给出完整处理串时，agent 应直接透传，不擅自改写参数名、参数顺序或分隔格式

### 常见处理串示例

```text
image/resize,w_200,h_200
image/crop,w_100,h_100,g_center
image/circle
image/info
image/rounded-corners,r_20
image/rotate,90
image/average-hue
image/resize,w_800,h_800/crop,w_400,h_400,g_center/rotate,90
image/resize,w_1024,h_1024/format,png|sys/saveas,o_ZGVyaXZlZC9hLTAxLnBuZw,b_bXktYnVja2V0
```

### 参考文档

- 图片处理参数字典：`references/image_process_reference.md`
