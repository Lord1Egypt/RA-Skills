# 项目简介/Project Introduction

ClkLog是一款记录并分析用户行为和画像的开源软件，技术人员可快速完成私有化部署。
ClkLog is an open-source system that records and analyzes user online behaviors to build a user profile. Technical personnel can quickly complete private deployment.

ClkLog基于神策分析SDK，采用ClickHouse数据库对采集数据进行存储，使用前后端分离的方式来实现。在这里，你可以轻松看到用户访问网页、APP、小程序或业务系统的行为轨迹，同时也可以从时间、地域、渠道、用户访客类型等多维度了解用户的全方位信息。
ClkLog is based on the Sensors Analysis SDK. It uses the ClickHouse database to store collected data by using the front-end and back-end separation method. Here, you can easily see the users’ behavior track when they access the web pages, mobile apps, Wechat mini-programs or other business systems. You can also collect the users’ all-round information from multiple dimensions such as time, region, channel, visitor type, etc.

# 核心功能/Core Functions

- **数据采集**：支持网页、小程序、IOS、Android等多端数据采集
- **Data collection**: supports data collection from multiple channels such as web pages, Wechat mini-programs, IOS, Android, etc.

- **流量概览**：提供流量渠道、设备、地域、访客类型多维度分析
- **Traffic overview**: provides multi-dimensional analysis from channels, devices, regions to visitor types.
- **用户画像**：解析用户唯一ID，定位追踪用户全生命周期画像
- **User Profile**: analyzes user unique IDs to locate and track full life cycle user profile.
- **数据下载**：支持各项汇总数据、明细数据的下载
- **Data Summary**: supports downloading of various summarized data and detailed data.

# 技术栈选择/Technology Selection

- **后端/Backend**：Redis 、Zookeeper、Kafka 、Flink

- **前端/Frontend**：vue、vue-element-admin、element-ui 、echarts

- **数据/Database**：Clickhouse、mysql


# 快速接入/Quick Start Tutorial

官方文档/Official Documents<a href="https://clklog.com">https://clklog.com</a>

# 协议许可​/License Agreement​

## 开源协议/Open-source agreement：AGPLv3.0

使用的组织或个人在复制、分发、转发或修改时请遵守相关条款。任何分发或通过网络提供服务的版本（包括衍生版本）必须开源，并保留原版权和协议信息。如有违反，ClkLog将保留对侵权者追究责任的权利。
Organizations or individuals using this software must comply with relevant terms when copying, distributing, ​​redistributing​​, or modifying it.Any distributed versions or versions provided as a network service (including derivative versions) must be open source with original copyright and license information preserved.ClkLog reserves the right to take legal action against infringers for any violations.

## ​​免费使用 | Free Usage​​

**​​适用范围​​**：个人开发者、学术研究及非商业项目可免费使用

**​​Scope​**​: Free for individual developers, academic research, and non-commercial projects.

**​​商业限制**​​：若将ClkLog集成到闭源商业产品中，任何修改、二开、集成须遵循 AGPLv3.0 协议开源衍生产品

**​​Commercial Restrictions​**​: If integrated into closed-source commercial products, ​​any modification, secondary development, or integration shall open-source derivative works​​ under AGPLv3.0.

**​​授权方式​**​：遵循 AGPLv3.0 协议

**​​Licensing Mode**​​: Subject to AGPLv3.0 license.

## ​​商业授权 | Commercial License​​

**​​适用范围**​​：商业项目集成可闭源使用

**​​Scope**​​: Permits closed-source integration for commercial projects.

**​​授权方式​**​：需购买商业授权

**​​Licensing Mode​​**: Requires purchasing a commercial license.

## ​​特别提醒 | Special Notice

​​在AGPL V3.0协议中​​，“衍生产品”是指：在 ClkLog 源代码基础上进行任何修改、扩展、适配、重构，或与其他软件、系统组合后形成的作品，包括但不限于：

​​Under AGPLv3.0​​, ​​"Derivative Works"​​ refer to any works created through modification, extension, adaptation, refactoring of ClkLog source code, or combination with other software/systems, including but not limited to:

• 修改、删除或新增源代码的版本；

• Versions with modified, deleted, or added source code;

• 增加功能模块、插件或集成接口的版本；

• Versions adding functional modules, plugins, or integration interfaces;

• 将 ClkLog 嵌入或整合进其他产品、系统或服务的版本；

• Versions embedding or integrating ClkLog into other products, systems, or services;

• 改变数据结构、接口协议或运行架构的版本。

• Versions altering data structures, interface protocols, or runtime architectures.

无论改动大小，只要衍生产品包含 ClkLog 的代码或核心逻辑，即视为衍生产品，并适用本协议的相关条款。

​​Regardless of modification scale, any work containing ClkLog's code or core logic shall constitute a Derivative Work and is subject to relevant terms of AGPLv3.0.​
