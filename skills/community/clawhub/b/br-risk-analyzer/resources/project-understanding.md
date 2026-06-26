# BR Project Understanding Repository

This file stores accumulated knowledge about the BR (Business Risk) project to provide context for future risk analyses.

## Project Overview
BR system processes business requirements through code changes, requiring systematic risk analysis against documented requirements.

## Technical Context
Based on DTS architecture with 7 Maven modules:
- **dts-platform** (Web management layer, port 8202)
- **dts-core** (Execution engine, port 8201)  
- **dts-parser** (Pulsar message consumption and API calling)
- **dts-writer** (Result file writing and HDFS upload)
- **dts-db** (Database entities and mappers)
- **dts-common** (Constants, enums, utilities)
- **dts-caller** (API calling SDK wrapper)

## Critical Business Concepts

### API Types (ApiTypeEnum)
hx, hn, zh, cldq, cldz, qyzx, yx, dcproxy, hl, tzgc, hxYz

### Task States (TaskStatusEnum)
0-9 state progression from 新建 to 文件压缩中

### Order States (OrderStatusEnum)  
0,1,2,3,60,51,10,20,30,45 covering full order lifecycle

## High-Risk Code Areas
- Entry points: Controllers, scheduled tasks, MQ consumers
- Core services: Business logic implementation
- Data persistence: Database operations and transactions
- Message handling: Pulsar producer/consumer logic
- Configuration management: System settings and feature flags
- External integrations: Feign clients for CRM, OA, BI, Auth systems
- Security controls: Authorization and validation logic

## Integration Points
- CRM system (order synchronization)
- OA system (approval workflows)
- BI system (analytics task sync)  
- Auth system (user permissions)
- File storage systems (HDFS, FTP)
- Notification systems (Email, WeCom, DingTalk)

## Review Focus Areas
Following codeReview.md protocol:
- Interface contracts and parameter validation
- Concurrency control and transaction boundaries
- Exception handling and failure recovery
- Configuration safety and default behaviors
- Security controls and data protection
- Performance characteristics and resource usage
- Observability and monitoring coverage
- Backward compatibility and rollback support

---
*This file will be updated after each risk analysis session to maintain current project understanding.*