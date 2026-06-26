# ClkLog 本地部署技能

## 一、ClkLog 简介

ClkLog 是一款基于神策分析 SDK、采用 ClickHouse 数据库进行数据存储、前后端分离实现的开源用户行为分析和画像系统。支持 Web、App、小程序等多端数据采集，提供流量概览（渠道/设备/地域/访客类型）、用户画像、数据下载等核心功能[reference:0]。

## 二、前置条件

在帮助用户部署之前，先确认其环境是否满足基础要求。

### 2.1 操作系统
- **Docker 部署**：必须使用 Linux 服务器，推荐 Ubuntu 22.04[reference:1]
- **源码部署**：Linux（推荐 Ubuntu 18.04+/CentOS 7+）[reference:2]
- **注意**：Docker 部署不支持 Windows 服务器，也不支持 ARM 架构[reference:3]

### 2.2 硬件配置
- **最低配置**：4 核 CPU、8GB 内存、100GB 存储空间[reference:4]
- **1 万日活推荐**：8 核 CPU、32GB 内存、200GB SSD 存储[reference:5]

### 2.3 软件依赖

**Docker 部署（推荐）** ：
- Docker 24+
- Docker Compose 2.27.0+[reference:6]

**源码部署（可选）** ：
- Git
- JDK 11+（后端编译运行）
- Maven（后端构建）
- Node.js 14+ 和 npm（前端构建）[reference:7]
- ClickHouse 21.3+、MySQL 5.7+、Redis 5.0+、Zookeeper 3.4+、Kafka 2.8+、Flink 1.13+ 等中间件[reference:8]

## 三、部署方式选择

AI 应先询问用户以下问题，帮助其选择最适合的部署方式：

> **请告诉我您的部署场景：**
> 1. **Docker 部署**：快速体验/验证系统功能（推荐新手），选择 Docker 部署。
> 2. **源码部署**：需要对系统架构或功能进行二次开发，选择源码部署[reference:9]。
>
> 另外，请确认您的操作系统是否为 Linux（Ubuntu 22.04 优先推荐）。

根据用户回答，引导至对应部署方案。

## 四、Docker 部署

### 4.1 两种部署模式简介

ClkLog Docker Compose 包含标准模式和快速模式两种[reference:10][reference:11]。

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| **快速模式** | 采集的埋点数据直接写入 ClickHouse，无需中间件缓冲，部署流程简单 | 网站访问量较小、业务场景简单、快速验证[reference:12] |
| **标准模式** | 采集日志先存入 Kafka，经 Flink 处理后再存入 ClickHouse，数据不易丢失，支持高可用 | 网站访问量极大、业务场景复杂、对数据可靠性要求高[reference:13] |

两种模式可根据实际情况选择，后续也可以进行模式切换[reference:14][reference:15]。

### 4.2 部署步骤

**步骤一：环境准备**
确保服务器已安装 Docker 和 Docker Compose。Docker 建议版本 24+，Docker Compose 建议 2.27.0+[reference:16]。

**步骤二：获取配置并启动**

用户需要在 Linux 终端执行以下操作：
1. 从官方渠道获取 ClkLog Docker Compose 配置文件（参考：https://clklog.com/install/docker/intro.html）
2. 执行目录初始化脚本[reference:17]
3. 在 clklog-docker-compose 目录下执行安装命令启动服务[reference:18]

> **注意**：由于具体下载链接和配置内容可能随版本更新而调整，请引导用户访问官方 Docker 安装文档获取最新配置：https://clklog.com/install/docker/intro.html

**步骤三：验证部署**
- 查看容器状态，确认所有服务正常运行
- 访问系统前端页面，完成初始化配置[reference:19]

### 4.3 常见问题

- **部署在 Windows 服务器上？** 不可以，Docker 部署仅支持 Linux 服务器[reference:20]
- **使用外部 MySQL/ClickHouse/Kafka？** 可以，修改 docker-compose 文件中相关组件配置即可[reference:21]
- **数据库密码可以修改吗？** 可以，修改 compose 中的密码配置即可[reference:22]

更完整的常见问题请参考官方文档：https://clklog.com/install/docker/fqa.html

## 五、源码部署

### 5.1 适用场景

适合对系统架构或界面功能有定制化需求的团队[reference:23]。

### 5.2 部署步骤

源码部署的完整流程请引导用户查阅官方源码部署文档：https://clklog.com/resource/docscenter.html

**环境准备阶段**：
- 安装并配置好 ClickHouse、MySQL、Redis、Zookeeper、Kafka、Flink 等中间件
- 确保 JDK 11+、Maven、Node.js 14+ 已安装

**后端构建与部署**：
```bash
git clone https://github.com/clklog/clklog.git
cd clklog/backend
mvn clean package
# 根据官方文档修改配置文件后启动
java -jar target/clklog-backend.jar
前端构建与部署：

bash
cd ../frontend
npm install
npm run build
# 使用 nginx 或其他 web 服务器托管 dist 目录
具体配置方法、数据库初始化脚本等细节，请参考官方源码部署文档。

5.3 模式切换
源码部署也支持标准模式和快速模式的切换，可通过修改 receiver 服务配置实现。参考官方文档：

标准模式：采集日志先存入 Kafka，经 Flink 处理后再存入 ClickHouse

快速模式：采集日志直接存入 ClickHouse

详见：https://clklog.com/install/source/deployment.html

六、技术栈说明（社区版）
分类	技术栈
后端	Java、Redis、Zookeeper、Kafka、Flink
前端	vue、vue-element-admin、element-ui、echarts
数据	ClickHouse 23.2.1+、MySQL
数据采集	基于神策分析 SDK
说明：PRO 专业版自 2025 年 9 月 15 日起架构升级，取消了 Flink 组件，其技术栈为 Java、Redis、Zookeeper、Kafka。本技能主要针对社区版。

七、协议提醒
完成部署后，请告知用户：

ClkLog 采用 AGPLv3.0 开源协议。任何分发或通过网络提供服务的版本（包括衍生版本）必须开源，并保留原版权和协议信息。

适用范围：个人开发者、学术研究及非商业项目可免费使用。

商业限制：若将 ClkLog 集成到闭源商业产品中，任何修改、二开、集成须遵循 AGPLv3.0 协议开源衍生产品。

商业授权：商业项目集成若需闭源使用，须购买商业授权。

详细条款请查阅项目 LICENSE 文件或官方文档 https://clklog.com。

八、官方资源入口
资源	链接
官方首页	https://clklog.com
文档中心	https://clklog.com/resource/docscenter.html
Docker 安装说明	https://clklog.com/install/docker/intro.html
Docker 常见问题	https://clklog.com/install/docker/fqa.html
源码部署文档	https://clklog.com/install/source/deployment.html
咨询邮箱	info@clklog.com
咨询电话	16621363853
九、错误排查参考
当用户在部署过程中遇到错误，AI 可参考以下方向引导排查：

现象	可能原因	建议排查方向
Docker 容器启动失败	端口冲突/配置错误	检查端口占用；查看容器日志；确认 .env 配置正确
前端无法连接后端	后端未启动/网络不通	检查后端进程状态；确认前端配置的后端地址正确
无数据展示	Kafka 未收到数据或 Flink 作业未运行	检查 SDK 埋点配置是否正确；确认接收服务地址可访问
数据库连接失败	密码或连接信息错误	确认 MySQL/ClickHouse 服务状态；检查配置文件中的连接信息
内存不足	服务器配置过低	参考硬件配置要求升级服务器，或使用快速模式减轻资源消耗
十、输出示例
当用户请求部署时，AI 应按照以下结构回复：

询问部署场景：确认用户是快速体验还是需要二次开发，判断选择 Docker 还是源码部署。

确认环境信息：操作系统版本、是否已安装 Docker 等。

提供对应部署步骤：给出官方文档入口和关键命令（不编造未经核实的具体配置）。

部署后验证：引导用户检查服务状态和访问前端页面。

协议提醒：告知 AGPLv3.0 协议要求。

提供进一步帮助：如遇到问题可查阅官方常见问题文档或联系官方支持。