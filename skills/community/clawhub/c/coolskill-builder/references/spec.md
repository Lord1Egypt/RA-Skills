# ZeroSkill-Forge 完整规格说明

## 核心原则

### 1. 零依赖原则
impl.py 仅允许使用 Python 标准库内置模块。白名单：
sys, json, os, re, math, random, datetime, itertools, collections, typing, inspect, hashlib, base64, urllib.request, http.client, socket, ssl, time, uuid, string, warnings, traceback, io, csv, html.parser, pathlib, fnmatch, glob, copy, functools, enum, dataclasses, contextlib, builtins

禁止：requests, numpy, pandas, bs4, lxml, scipy, sklearn, flask, django, fastapi, sqlalchemy, pydantic, python-dotenv, pytest, unittest 及任何第三方库。

### 2. 极致省 Token 原则
- 公共接口保留命名（run, skill.yaml 键名），内部变量/函数使用 1-2 字符
- 删除所有非必要空格、空行、类型提示、文档字符串
- 统一单引号；使用 and/or 短路替代 if/else；列表推导替代 for
- 字典访问用 d['k']，除非需要默认值才用 .get()
- 异常处理单行压缩；impl.py 零注释
- YAML 键名压缩至最短可识别形式

### 3. 版本隔离原则
- 每个 Skill 全局唯一 ID: `{domain}-{func}-{rand3}`
- 同一 ID 迭代自动递增 Semver
- 不同 Skill 禁止共享状态、文件句柄、全局变量、临时文件
- 测试环境隔离：test.py 独立运行，不导入其他 Skill 模块

### 4. 跨生态兼容原则
- 输出必须包含 `manifest.json`，声明 OpenAI Function、Claude Tool、通用 HTTP 三种调用格式
- impl.py 只包含纯逻辑，manifest.json 包含各生态的 schema 映射
- 禁止硬编码任何特定平台的 SDK 或认证方式

## 工作流（6 步标准化）

```
1. 解析资源 → 提取功能意图、输入输出、边界规则
2. 生成 4 文件（skill.yaml + impl.py + test.py + manifest.json）
3. 5 层安全校验 → 任一失败则阻断，仅输出修复指令（不写入 Registry）
4. 原生测试 → 在隔离进程中执行 test.py，失败则阻断
5. 版本隔离注册 → 写入 registry/{skill-id}/{version}/，更新全局索引
6. GitHub 同步 → 推送至用户仓库（如配置）
```

## 版本隔离机制

### 目录结构
```
registry/
├── index.json                    # 全局索引：只存元数据，不存代码
└── {skill-id}/
    ├── v1.0.0/                   # 版本 1.0.0（只读归档）
    ├── v1.0.1/                   # 版本 1.0.1（当前 latest）
    └── latest -> v1.0.1
```

### 版本递增规则
- 首次生成：v1.0.0
- 迭代/修复：Patch +1
- 功能重大变更：Minor +1（用户声明）
- 破坏性重构：Major +1（用户声明）
- 历史版本永久保留，禁止覆盖

### 索引格式（index.json）
```json
{
  "skills": {
    "data-parse-7a2": {
      "name": "parse-csv",
      "latest": "1.0.1",
      "versions": {
        "1.0.0": {"st": "stable", "t": "2026-06-09T10:00:00Z", "path": "data-parse-7a2/v1.0.0"},
        "1.0.1": {"st": "draft", "t": "2026-06-09T11:00:00Z", "path": "data-parse-7a2/v1.0.1"}
      }
    }
  }
}
```

## GitHub 同步（可选）

环境变量：
- `GITHUB_TOKEN`: GitHub Personal Access Token
- `GITHUB_REPO`: 格式 `owner/repo`

同步逻辑使用 urllib.request + json + os + base64，零第三方依赖。
