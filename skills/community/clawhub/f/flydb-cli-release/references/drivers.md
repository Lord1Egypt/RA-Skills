# JDBC 驱动接入与 FLYDB-1003 排查

> 本文件随 `flydb-cli-release` 打包，按 CLI 0.3.x 维护。配置与来源优先级见 [configuration.md](configuration.md)，新数据库/SPI 接入见 [jdbc-integration.md](jdbc-integration.md)。

## 发行包不捆绑驱动

发行包的 `drivers/` 是空目录（附说明文件）。任何数据库连接都要求先落实对应数据库的 JDBC 驱动，Flydb 按下面的顺序解析。

## 驱动解析顺序（从先到后）

1. 安装目录 `drivers/*.jar`
2. 运行时 classpath
3. Maven 本地仓库：显式 `--maven-local-repository` / `maven.repo.local` → `settings.xml` 的 `localRepository` → `~/.m2/repository`
4. Flydb 驱动缓存 `~/.flydb/drivers`（`--driver-cache` 可改）
5. 按 Maven 有效配置远程下载（`--driver-download auto` 默认允许；`never` 禁止；`--offline` 禁止一切远程解析）

远程解析遵循 `settings.xml` 的 `mirrors`、激活 Profile 的 `repositories`、`servers` 基本认证和活动 `proxy`。配置了 `mirrorOf=*` 时 Central 会被镜像替换，Flydb 不会绕过企业私服直连公网。自动下载写入独立的 `~/.flydb/drivers` 缓存，不修改 Maven 本地仓库。

## 常用选项

| 选项 | 用途 |
|---|---|
| `--driver <class>` | URL 无法自动推断驱动类名时显式指定 |
| `--driver-coordinate <gav>` | 显式 Maven 坐标 `groupId:artifactId:version` |
| `--driver-download auto\|never` | 是否允许远程下载缺失驱动 |
| `--maven-settings <path>` | 指定 settings.xml（私服、镜像、认证、代理） |
| `--offline` | 禁止联网解析，只用本地来源 |

## 内置坐标与厂商驱动

- 内置固定坐标覆盖 **MySQL、PostgreSQL、Oracle、OceanBase**，常规使用无需配置驱动项。
- 达梦、KingbaseES、openGauss 以及小众数据库的实际版本通常由厂商交付或企业私服决定，需配置完整坐标：

```properties
flydb.driver=com.vendor.jdbc.Driver
flydb.driver-coordinate=com.company.jdbc:vendor-driver:3.2.1
```

- 厂商不提供 Maven 制品时，把驱动 JAR 手工放入发行包 `drivers/` 目录。

## 已知限制

- 轻量解析器只下载坐标对应的主驱动 JAR，**不解析 Maven 传递依赖**；需要伴随 JAR 的厂商驱动应把这些 JAR 一并放入 `drivers/`。
- 不解密 Maven 加密密码（`{...}` 形式）；此类环境用受控环境变量插值提供凭据，或预先把驱动发布到本地仓库/`drivers/`。
- 语法兼容不等于迁移语义兼容：复用 `mysql`/`oracle` 方言前确认 DDL 事务、历史表、锁、引号/大小写和过程切分。不确定时先核对厂商语义或接入独立 SPI；显式 `--database-type` 本身不能证明兼容。
- MCP 数据库工具固定 `--driver-download never`，不会在调用期间补下载。GUI 则沿用配置的下载/离线策略，并可使用登记的驱动目录；不能把 CLI 自动下载行为套到 MCP。

## FLYDB-1003 排查步骤

1. 读取错误消息中的**解析轨迹**——它会列出实际尝试过的每个来源，从轨迹入手最直接。
2. 核对 `drivers/` 是否放了 JAR、`--driver-coordinate` 坐标与 `--driver` 类名是否正确。
3. 检查 `settings.xml` 的私服/镜像认证、网络与代理配置。
4. 离线环境确认 `--offline` 与本地制品是否匹配。
5. 修正后重试；仍失败则把解析轨迹与脱敏后的配置报告给用户，不要反复盲试。

## 安全边界

- 不下载、提交或重新分发厂商 JDBC 驱动；遵守厂商许可证和企业制品库规则。
- 不为绕过 `FLYDB-1002` 探测错误而把未识别的数据库强行标记为 `mysql`/`oracle`。
