---
name: coolskill-builder
description: >
  Skill 生成与治理节点。将任何资源（GitHub 仓库、API 文档、自然语言需求、代码片段）
  转化为零外部依赖、极致省 Token、可被任意生态（Kimi/OpenAI/Claude/自研 Agent）直接调用的标准化 Skill。
  触发条件：(1) 用户要求创建/生成/编写一个 Skill，(2) 用户提供资源要求转化为可调用模块，
  (3) 用户提到零依赖、跨生态兼容、版本隔离等关键词，(4) 用户要求将代码/功能封装为标准化 Skill，
  (5) 用户要求实现 skill registry、版本管理或安全扫描，(6) 任何涉及 Agent 工具/函数生成的需求。
  使用时加载此 Skill，严格按 6 步工作流执行，生成 4 文件（skill.yaml + impl.py + test.py + manifest.json）
  并通过 5 层安全校验。
---

# CoolSkill Builder

将任意资源转化为标准化、零依赖、跨生态兼容的 Skill 模块。

## 核心原则

1. **零依赖**：impl.py 仅使用 Python 标准库白名单模块（详见 references/spec.md）
2. **极致省 Token**：内部变量 1-2 字符，零注释，短路求值，列表推导优先
3. **版本隔离**：每个 Skill 全局唯一 ID `{domain}-{func}-{rand3}`，Semver 递增，历史版本只读
4. **跨生态兼容**：manifest.json 声明 OpenAI Function / Claude Tool / HTTP 三种调用格式

## 6 步工作流

收到资源后，严格按以下顺序执行：

### Step 1: 解析资源

提取以下信息，整理为结构化需求：

| 字段 | 说明 |
|------|------|
| 功能意图 | 该 Skill 的核心功能是什么 |
| 输入 schema | 参数名、类型、是否必填、默认值 |
| 输出 schema | 返回值结构、成功/错误格式 |
| 边界规则 | 长度限制、取值范围、异常场景 |
| domain | 功能领域（data, text, web, file, api, calc...）|

如果用户提供的是：
- **自然语言描述** → 自行推导输入输出 schema，必要时反问确认
- **代码片段** → 提取函数签名、参数、返回值，转化为 run() 接口
- **API 文档** → 将 endpoint 映射为 run() 入参，response 映射为返回值
- **GitHub 仓库** → 提取核心逻辑，重写为标准库实现

### Step 2: 生成 4 文件

基于解析结果，生成以下文件。详细模板见 `references/file-templates.md`。

#### skill.yaml（元数据）

- 键名压缩：`v` 替代 version, `d` 替代 description, `src` 替代 source, `pf` 替代 platforms, `props.dom` 替代 domain, `props.st` 替代 status
- `meta.id` 使用 `scripts/generate_skill_id.py` 生成，或按 `{domain}-{func}-{rand3}` 规则
- `meta.src` 标记来源：github|registry|custom|api
- `schema.in` / `schema.out` 为 JSON Schema 格式
- `perms` 按需声明：net（网络）、fs（文件系统）、env（环境变量）、exec（执行命令）

#### impl.py（零依赖实现）

- 固定签名：`def run(a):` 其中 `a` 为 dict
- 固定返回：`{'s': 'ok|err', 'd': result, 'e': error_string}`
- 导入行只保留实际使用的模块
- 内部变量/函数 1-2 字符（`_e`=raise, `_j`=json.dumps, `_p`=json.loads, `_h`=hash, `_t`=time, `_u`=url, `_f`=file, `_s`=string, `_m`=math）
- 零类型提示、零文档字符串、零注释
- 统一单引号；分号连接相关语句；列表推导替代 for
- 字典访问用 `d['k']`，除非需要默认值才用 `.get()`
- 错误处理：`try/except` 包围全部逻辑，`r['s']='err';r['e']=str(x)`
- 禁止 `if __name__=='__main__'` 之外的任何 I/O（测试/调试代码除外）

#### test.py（隔离测试）

- 首行：`sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))`
- 从 `impl import run`，禁止相对导入其他 Skill
- 测试类 `T` 提供 `a()`（断言）、`r()`（运行并断言）、`x()`（汇总退出）
- 用例覆盖：t1 正常输入、t2 必填缺失、t3 类型错误、t4 边界值、t5 异常恢复
- 性能测试可选：检查运行时间是否超过阈值

#### manifest.json（跨生态适配）

- `universal`: entry=run, input=dict, output=dict
- `openai_function`: name/description/parameters/strict=true
- `claude_tool`: name/description/input_schema
- `http_api`: POST /skill/{skill-id}, headers 含 X-Skill-Version

### Step 3: 5 层安全校验

运行 `scripts/security_scan.py <impl.py>` 执行自动扫描。任一失败则阻断，仅输出修复指令，不写入 Registry。

手工复核要点：

| 层级 | 规则 | 自动扫描 | 人工复核 |
|------|------|---------|---------|
| L1 依赖扫描 | 仅标准库白名单 | ✅ | 检查 import 行 |
| L2 注入检测 | 禁止 eval/exec/os.system/subprocess | ✅ | 检查危险调用 |
| L3 密钥检测 | 禁止硬编码 API Key/Token | ✅ | 检查常量字符串 |
| L4 网络边界 | perms 无 net 则禁止 urllib/http/socket | ✅ | 核对 perms 声明 |
| L5 信息泄露 | 禁止返回 traceback/os.environ/密钥 | ✅ | 检查错误返回内容 |

详细规则见 `references/security-rules.md`。

阻断后行为：
1. 输出失败层级和具体问题
2. 给出修复指令（原生代码重写/安全等价实现/参数化/脱敏）
3. 返回 Step 2 重新生成
4. 不执行 Step 4-6

### Step 4: 原生测试

在隔离进程中执行 test.py：

```bash
cd registry/{skill-id}/{version} && python test.py
```

- 失败则阻断，返回修复指令
- 通过标准：`ALL_OK` 输出，F=0
- 测试进程必须独立，不加载其他 Skill 模块

### Step 5: 版本隔离注册

#### 生成/获取 Skill ID

首次生成：
- 运行 `python scripts/generate_skill_id.py {domain} {func}`
- 或按 `{domain}-{func}-{rand3}` 规则自行生成

迭代生成：
- 读取 `registry/index.json` 找到该 ID 的最新版本
- 按规则递增：修复→Patch+1, 功能变更→Minor+1, 破坏性重构→Major+1

#### 写入 Registry

```
registry/
├── index.json
└── {skill-id}/
    └── v{version}/
        ├── skill.yaml
        ├── impl.py
        ├── test.py
        └── manifest.json
```

更新 `index.json`：
- 添加/更新该 skill-id 的 versions 记录
- 更新 latest 指向
- 时间戳使用 ISO8601 格式

详细格式见 `references/registry-format.md`。

### Step 6: GitHub 同步（可选）

检测环境变量：
- `GITHUB_TOKEN`: GitHub Personal Access Token
- `GITHUB_REPO`: 格式 `owner/repo`

若缺失：输出 `[CONFIG REQUIRED]` 提示，继续本地注册。

若存在：使用 urllib.request + base64 + json 推送 4 文件到 `skills/{skill-id}/{version}/`。

同步代码模板（零依赖）：
```python
import urllib.request,json,os,base64
GH='https://api.github.com'
G=os.environ.get('GITHUB_TOKEN')
R=os.environ.get('GITHUB_REPO')
```

## 输出报告格式

所有 Skill 生成完成后，输出以下报告：

```
=== SKILL REPORT ===
ID: {skill_id}
Name: {name}
Version: {version}
Domain: {dom}

--- skill.yaml ---
{yaml}

--- impl.py ---
{code}

--- test.py ---
{code}

--- manifest.json ---
{json}

--- SECURITY ---
L1: PASS/FAIL {detail}
L2: PASS/FAIL {detail}
L3: PASS/FAIL {detail}
L4: PASS/FAIL {detail}
L5: PASS/FAIL {detail}

--- TEST ---
P {pass} F {fail}
{case list}

--- REGISTRY ---
Local: registry/{skill_id}/{version}/ (isolated)
Latest: {version}
History: [v1.0.0, v1.0.1, ...]

--- CROSS-PLATFORM CALL ---
Kimi: import ...
OpenAI: function name={skill_name}
Claude: tool name={skill_name}
HTTP: POST /skill/{skill_id}

--- GITHUB ---
Status: PUSHED_or_SKIP
URL: {commit_url_or_none}
=== END ===
```

## 内部工具

| 脚本 | 用途 |
|------|------|
| `scripts/security_scan.py <impl.py>` | L1-L5 安全扫描，输出 JSON |
| `scripts/generate_skill_id.py [dom] [func]` | 生成全局唯一 Skill ID |
| `scripts/validate_impl.py <impl.py>` | 校验语法/run签名/返回格式/Token密度 |

## 参考文档

| 文件 | 内容 |
|------|------|
| `references/spec.md` | 完整规格：零依赖、省Token、版本隔离、跨生态兼容 |
| `references/file-templates.md` | 4 文件完整模板及跨生态调用示例 |
| `references/security-rules.md` | 5 层安全校验详细规则 |
| `references/registry-format.md` | Registry 目录结构、索引格式、版本递增规则 |

## 关键约束速查

- **导入白名单**：仅 sys,json,os,re,math,random,datetime,itertools,collections,typing,inspect,hashlib,base64,urllib.request,http.client,socket,ssl,time,uuid,string,warnings,traceback,io,csv,html.parser,pathlib,fnmatch,glob,copy,functools,enum,dataclasses,contextlib,builtins
- **固定签名**：`def run(a):` → `{'s':'ok|err','d':result,'e':error}`
- **版本格式**：Semver `{major}.{minor}.{patch}`，历史版本只读
- **Skill ID**：`{domain}-{func}-{rand3}`，全局唯一，生成后固定
- **阻断规则**：L1-L5 任一失败、test.py 失败 → 阻断，不写入 Registry
- **生态兼容**：必须输出 manifest.json（OpenAI/Claude/HTTP 三种格式）
