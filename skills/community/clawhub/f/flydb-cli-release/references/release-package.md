# 发布包：获取、安装与 Java 运行环境

> 本文件随 `flydb-cli-release` 打包，按 CLI 0.3.x 维护。源码同步版本见 [upstream-sync.json](upstream-sync.json)；该记录不证明公开 Release 已存在。

## 发布包形态

Flydb CLI 以 Release ZIP 分发，不依赖安装器，解压即用。先核验用户指定版本的实际资产，再使用下载 URL；GitHub 与 Gitee 镜像的可用性分别检查：

```text
https://github.com/zzxCoding/Flydb/releases/download/v<version>/flydb-cli-<version>.zip
# 国内镜像（同型 URL）：
https://gitee.com/zzhenxuan/Flydb/releases/download/v<version>/flydb-cli-<version>.zip
```

tag `v<version>` 必须对应同版本 `flydb-cli-<version>.zip`，不能混用 tag 与资产版本。解压后得到基目录 `flydb-cli-<version>/`，布局如下：

| 路径 | 内容 |
|---|---|
| `bin/flydb` | POSIX sh 启动器（负责解析 Java 并启动 CLI） |
| `bin/flydb.bat` | Windows 启动器 |
| `lib/` | 全部运行时 JAR |
| `conf/flydb.conf.sample` | 配置模板 |
| `drivers/` | JDBC 驱动目录（附说明；**不捆绑任何 JDBC 驱动**） |
| `docs/` | 与版本匹配的 CLI/配置/错误码文档 |
| `flydb-skills/` | 与版本匹配的 Agent Skills |
| `README.md`、`AGENTS.md`、`LICENSE`、`NOTICE` 等 | 项目说明与许可 |

安装即解压，没有其他步骤；升级等于解压新版本目录并切换引用路径。两个自动化小提示：

- 解压到新的安装目录；已有目录时先核对是否为同一完整发行包，避免用 `unzip -o` 覆盖已有配置或驱动。
- 搜索无命中与命令失败分开处理；先查已知路径，再按需扩大搜索，避免遍历整个主目录。

## 获取策略（按顺序尝试）

1. **探测已有安装**：先检查用户给定路径、`FLYDB_HOME/bin/flydb`、PATH 和项目工具目录，再在必要范围搜索：
   ```bash
   command -v flydb
   # 根据已知安装根目录使用 rg --files --hidden 搜索 bin/flydb
   ```
   找到后运行 `<该目录>/bin/flydb version` 验证可用，直接复用，不重复下载。
2. **复用本地 ZIP**：本机已有发行包（如 `~/Downloads/flydb-cli-*.zip`）时优先解压复用：
   ```bash
   # FLYDB_ZIP 和 FLYDB_INSTALL_PARENT 为已确认的本地 ZIP 与新安装父目录
   unzip -t "$FLYDB_ZIP"
   unzip -q "$FLYDB_ZIP" -d "$FLYDB_INSTALL_PARENT"
   ```
3. **按 URL 模式下载**：前两步都没有时，从 Release 下载——GitHub 优先；国内网络访问 GitHub 慢或失败时改用 Gitee 镜像同型 URL。下载是运行时动作；离线或网络不可达时如实报告缺少发行包，不要猜测替代来源或把源码目录当作已安装的 CLI：
   ```bash
   # FLYDB_VERSION 由用户指定或从已核验的 Release 选定，不从源码 pom 自动推断
   : "${FLYDB_VERSION:?先选择已核验的发行版本}"
   curl -fL -o "flydb-cli-${FLYDB_VERSION}.zip" \
     "https://github.com/zzxCoding/Flydb/releases/download/v${FLYDB_VERSION}/flydb-cli-${FLYDB_VERSION}.zip"
   # GitHub 不可达且镜像确有同版本资产时，改用上述 Gitee URL 模式
   ```

下载后先 `unzip -t` 检查完整性；Release 提供校验文件时核对其中同名 ZIP 的 SHA-256（macOS `shasum -a 256`，Linux `sha256sum`）。只有自己计算的哈希不能证明来源一致。选择一个精确版本 ZIP，避免通配符混入多个版本。缺少可信校验值时如实报告验证范围。

## Java 运行环境（前置条件）

Flydb CLI 是 Java 程序，**要求 Java 8 或更高版本**（JDK 或 JRE 均可）。执行任何 `bin/flydb` 命令前先预检：

```bash
java -version          # 或设置了 JAVA_HOME 时：
"$JAVA_HOME/bin/java" -version
```

注意版本信息输出在 stderr。启动器 `bin/flydb` 的行为：

- **解析顺序**：优先 `$JAVA_HOME/bin/java`；未设置 `JAVA_HOME` 时用 PATH 上的 `java`。
- **版本校验**：自动处理 `1.8` 旧式版本号；主版本低于 8 时拒绝启动。
- **失败表现**（退出码 4，配置错误类）：
  - 未找到 Java：`错误：未找到 Java。请安装 Java 8 或更高版本，或正确设置 JAVA_HOME。`
  - 版本过低：`错误：Flydb 要求 Java 8 或更高版本，当前为 <version>。`
- **JVM 参数**：通过 `FLYDB_JAVA_OPTS` 环境变量按词拆分传入，例如：
  ```bash
  FLYDB_JAVA_OPTS='-Xmx1g -Dfile.encoding=UTF-8' bin/flydb migrate
  ```

Java 缺失或版本过低时：明确报告缺失并停止后续步骤；用户安装任意 JDK 8+ 发行版（如 Temurin、Zulu 或系统包管理器提供的 OpenJDK）并正确设置 `JAVA_HOME` 后重试，不要试图绕过校验。

## 配置文件查找顺序

`--config` 显式指定的文件 → 当前目录 `flydb.conf` → 安装目录 `conf/flydb.conf`。发行包自带的 `conf/flydb.conf.sample` 是配置模板，可复制改名后使用；各配置键含义见 [configuration.md](configuration.md)。

## 验证安装

```bash
bin/flydb version        # 输出 CLI 版本，证明 Java 与发行包均就绪
bin/flydb init --help    # 所有子命令都支持 --help
```

`bin/flydb version` 不连接数据库，是环境预检的最后一步；它成功后才开始涉及数据库的任务。

需要 Web 时再检查 `bin/flydb web --help`：入口自 0.3.5 提供，仅需 Java 8+ 与浏览器。MCP Adapter 是独立分发，宿主另需 Node.js 20+，定位与握手见 [mcp-tools.md](mcp-tools.md)；不能把 MCP 的运行依赖套到普通 CLI/Web 上。
