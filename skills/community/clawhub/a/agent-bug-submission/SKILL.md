---
name: agent-bug-submission
description: 提交缺陷到TeamCycle平台，跟踪缺陷生命周期。支持飞书多维表格记录、飞书文档写入。
  Use when: 用户说"提交缺陷"、"创建缺陷单"、"提bug"、"记录缺陷"。
allowed-tools: [read, write, exec, feishu_create_doc, feishu_update_doc, feishu_doc_media, feishu_bitable_app_table_record, message]
---

# Agent Bug Submission - 智能体缺陷提交

## 飞书文档写入位置

```
知识库: 7616288931050507220
节点: 效果评测/缺陷报告
```

## 飞书多维表格写入位置

```
缺陷跟踪表: https://my.feishu.cn/wiki/FWYmwGwgziQGzBkxETHctCg5nDK?table=tblt64TGQqsHqcSu&view=vewqJU0Fv4
```

提交缺陷到TeamCycle平台，跟踪缺陷生命周期。

## 触发条件

当用户需要以下操作时触发：
- "提交缺陷"
- "创建缺陷单"
- "提bug"
- "记录缺陷"
- "缺陷跟踪"

## 功能

提供缺陷全生命周期管理：
- 缺陷信息收集与格式化
- 缺陷提交到TeamCycle平台
- 缺陷状态跟踪
- 缺陷信息查询

## 依赖

此 skill 依赖 **bug-reporter** skill 进行实际的缺陷提交：
- 路径: `C:\Users\zhanju.zhang\.openclaw\workspace\skills\bug-reporter`
- 功能: 调用 TeamCycle API 提交缺陷

## 使用方法

### 1. 提交缺陷到 TeamCycle

```
提交缺陷:
- 项目ID: [TeamCycle项目ID，如58]
- 缺陷标题: [简明描述]
- 缺陷描述: [详细描述，支持HTML]
- 缺陷类型ID: [TeamCycle缺陷类型ID，如211]
- 优先级: [高级/中级/低级]
- 所处阶段: [需求阶段/设计阶段/开发阶段/测试阶段]
- 关注人: [可选]

示例:
python scripts/bug_reporter.py zhanju.zhang "密码" 58 "登录功能异常" "<p>用户在登录时偶尔出现白屏</p>" 211 "高级" "测试阶段"
```

### 2. 缺陷信息模板

```
【缺陷标题】[一句话描述问题]

【缺陷描述】
[详细描述问题现象]

【重现步骤】
1. [步骤1]
2. [步骤2]
3. [步骤3]

【预期结果】[预期行为]
【实际结果】[实际行为]

【环境信息】
- 版本: [版本号]
- 环境: [测试环境]
- 浏览器: [浏览器版本]

【附件】[截图/日志]
```

## TeamCycle 配置

### 系统信息
- **平台地址**: https://teamcycle.100credit.cn
- **登录接口**: POST /api/login
- **缺陷提交接口**: POST /api/projectBug/save

### 必需参数
| 参数 | 说明 | 示例 |
|------|------|------|
| username | 用户名 | zhanju.zhang |
| password | 密码 | [用户密码] |
| projectId | 项目ID | 58 |
| title | 缺陷标题 | 登录功能异常 |
| desc | 缺陷描述 | <p>详细描述</p> |
| bugTypeId | 缺陷类型ID | 211 |

### 可选参数
| 参数 | 说明 | 示例 |
|------|------|------|
| priority | 优先级 | 高级/中级/低级 |
| phase | 所处阶段 | 需求阶段/测试阶段 |
| focustors | 关注人 | ["user1","user2"] |

## 缺陷类型ID参考

| 类型 | ID |
|------|-----|
| 功能缺陷 | 211 |
| UI缺陷 | 212 |
| 性能缺陷 | 213 |
| 安全缺陷 | 214 |
| 兼容性缺陷 | 215 |
| 其他 | 216 |

## 严重程度映射

| 严重程度 | TeamCycle优先级 |
|----------|----------------|
| 致命 | 高级 |
| 严重 | 高级 |
| 一般 | 中级 |
| 轻微 | 低级 |

## 工作流程

```
1. 收集缺陷信息
   ↓
2. 格式化缺陷描述（HTML）
   ↓
3. 调用 bug-reporter 提交
   ↓
4. 获取缺陷ID
   ↓
5. 记录到本地跟踪
```

## 输出

- TeamCycle 缺陷链接
- 缺陷ID
- 本地缺陷记录

## 示例

### 提交功能缺陷
```
项目ID: 58
标题: 智能问答Agent意图识别失败
描述: <p>当用户输入"查一下北京天气"时，系统未能正确识别"查天气"意图</p><p><b>重现步骤：</b></p><p>1. 进入智能问答Agent</p><p>2. 输入"查一下北京天气"</p><p>3. 观察返回结果</p><p><b>预期结果：</b>返回北京天气信息</p><p><b>实际结果：</b>返回"我不理解您的问题"</p>
缺陷类型ID: 211
优先级: 高级
阶段: 测试阶段
```

### 提交性能缺陷
```
项目ID: 58
标题: 高并发下响应时间超过阈值
描述: <p>在10并发用户场景下，首字响应时间超过6秒，不符合性能要求</p><p>详见性能测试报告附件</p>
缺陷类型ID: 213
优先级: 高级
阶段: 测试阶段
```
