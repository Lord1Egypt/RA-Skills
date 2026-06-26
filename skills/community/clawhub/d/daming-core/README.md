# 大明朝廷-三省六部中枢系统

## 概述

基于古代中国三省六部架构的完整任务管理系统，巧妙融合传统官僚体系与现代软件设计，实现任务创建、审核、资源管理、调度执行和监控审计的完整工作流程。

## 核心特性

### 🏛️ 传统架构现代化
- **中书省**：任务创建与档案管理
- **门下省**：任务审核与合规检查  
- **户部**：资源预算与账本管理
- **工部**：任务调度与执行管理
- **民夫团队**：实际任务执行
- **锦衣卫**：系统监控与安全审计

### 📊 完整工作流程
```
圣旨（任务指令） → 中书省（创建） → 户部（预算） → 门下省（审核） → 工部（调度） → 民夫团队（执行） → 结果
```

### 🔒 安全与审计
- 完整的操作日志记录
- Token预算控制与审计
- 文件系统级别的数据隔离
- 实时监控与异常预警

## 快速开始

### 安装
```bash
# 1. 复制技能目录到OpenClaw skills目录
cp -r daming_court /path/to/openclaw/skills/

# 2. 安装依赖（如果需要）
pip install -r requirements.txt
```

### 基本使用
```python
# 创建新任务
from skill1.zhongshu.main import create_task_archive

task_id, task_dir = create_task_archive(
    emperor_order="生成山水画",
    token_budget=500
)
print(f"任务创建成功: {task_id}")
print(f"任务目录: {task_dir}")

# 审核任务
from skill1.menxia.main import audit_task_draft
audit_result = audit_task_draft(task_id, "审核通过，可以执行")

# 管理资源
from skill1.bu.hu.main import create_token_ledger
ledger = create_token_ledger(task_id, initial_budget=500)

# 调度执行
from skill1.bu.gong.scheduler import GongBuScheduler
scheduler = GongBuScheduler()
dispatch_result = scheduler.dispatch_with_budget_check(
    task_id,
    {"action": "generate_image", "estimated_tokens": 100}
)

# 执行任务
from skill2.main import MinFuTeam
team = MinFuTeam(task_id, dispatch_result['execution_id'])
result = team.execute_comfyui({
    "action": "generate_image",
    "params": {"prompt": "山水画"},
    "estimated_tokens": 80
})
```

## 目录结构

```
daming_court/
├── SKILL.md              # 技能详细文档
├── skill.json           # 技能元数据
├── README.md            # 使用说明
├── requirements.txt     # Python依赖
├── test_skill.py       # 功能测试脚本
├── active_tasks/       # 任务存储目录
│   └── EXAMPLE_TASK/   # 示例任务
│       ├── task_draft.json
│       └── token_ledger.json
├── skill1/             # 三省六部核心模块
│   ├── __init__.py
│   ├── config.py       # 系统配置
│   ├── zhongshu/       # 中书省 - 任务创建
│   ├── menxia/         # 门下省 - 任务审核
│   ├── bu/             # 六部
│   │   ├── hu/         # 户部 - 资源管理
│   │   ├── gong/       # 工部 - 调度执行
│   │   ├── bing/       # 兵部 - 安全保卫
│   │   ├── xing/       # 刑部 - 审计监察
│   │   └── li_bu/      # 吏部 - 人事管理
│   └── jinyiwei/       # 锦衣卫 - 监控预警
└── skill2/             # 民夫团队 - 实际执行
    ├── __init__.py
    └── main.py
```

## 配置

### skill.json 配置
```json
{
    "skill_name": "daming_court",
    "display_name": "大明朝廷-三省六部中枢系统",
    "description": "基于古代中国三省六部架构的完整任务管理系统",
    "version": "2.0.0",
    "entry_function": "skill1.zhongshu.main.create_task_archive",
    "support_type": ["text"],
    "tags": ["task-management", "workflow", "chinese-history", "bureaucracy"],
    "author": "DaMing Core Team",
    "license": "MIT"
}
```

### 系统配置
编辑 `skill1/config.py` 调整系统参数：
```python
ACTIVE_TASKS_DIR = "{{PROJECT_ROOT}}/active_tasks"  # 任务存储目录（生产环境需要配置）
DEFAULT_TOKEN_BUDGET = 1000  # 默认Token预算
```

## 测试

运行功能测试确保技能正常工作：
```bash
python3 test_skill.py
```

预期输出：
```
🏛️ 大明核心系统技能测试
==================================================
🔧 测试模块导入...
  ✅ 中书省模块导入成功
  ✅ 门下省模块导入成功
  ✅ 户部模块导入成功
  ✅ 工部调度模块导入成功
  ✅ 民夫团队模块导入成功

⚙️ 测试系统配置...
  ✅ 配置模块加载成功
    活动任务目录: {{PROJECT_ROOT}}/active_tasks
  ✅ 活动任务目录存在

📁 测试示例任务...
  ✅ 示例任务目录存在: {{PROJECT_ROOT}}/active_tasks/EXAMPLE_TASK
  ✅ 任务草案文件存在
  ✅ Token账本文件存在

==================================================
🎉 所有测试通过！技能功能正常。
```

## 数据模型

### 任务档案 (task_draft.json)
```json
{
    "task_id": "T20260325-xxxx",
    "emperor_order": "任务描述",
    "created_at": "2026-03-25T00:00:00",
    "token_budget": 1000,
    "status": "draft"
}
```

### Token账本 (token_ledger.json)
```json
{
    "task_id": "T20260325-xxxx",
    "initial_budget": 1000,
    "current_balance": 1000,
    "transactions": []
}
```

## 扩展开发

### 添加新功能模块
1. 在 `skill1/` 下创建新目录
2. 实现 `main.py` 入口文件
3. 定义清晰的接口函数
4. 更新相关部门的调用逻辑

### 自定义执行器
1. 扩展 `MinFuTeam` 类
2. 实现新的执行方法
3. 在工部调度中注册新执行器

## 许可证

MIT License - 详见 LICENSE 文件

## 支持

- 问题报告：请提交GitHub Issue
- 功能建议：欢迎提交Pull Request
- 文档改进：随时欢迎贡献

---

**大明永昌！** 🏛️

*巧妙融合传统智慧与现代技术，打造可靠的任务管理系统。*
## 🚀 生产环境配置指南

### 📋 需要自行配置的项

本技能已移除所有个人化配置，以下配置项需要在生产环境中根据实际情况进行设置：

#### 1. 项目根目录配置
- **配置文件**: `skill1/config.py`
- **配置项**: `PROJECT_ROOT`
- **说明**: 设置 `daming_core` 系统的安装目录
- **示例**: `PROJECT_ROOT = Path("/opt/daming_core")`

#### 2. ComfyUI服务器配置
- **配置文件**: `config/external_agents.yaml` 和 `config/external_agents.json`
- **配置项**: 
  - `base_url`: ComfyUI服务器地址
  - `api_endpoints`: API端点配置
- **说明**: 配置连接到您的ComfyUI服务器
- **示例**: 
  ```yaml
  base_url: "http://192.168.1.100:8188"
  ```

#### 3. 虚拟环境路径
- **配置文件**: `skill2/main.py`
- **配置项**: 通过环境变量 `VENV_PATH` 或直接修改代码
- **说明**: 设置Python虚拟环境的site-packages路径
- **示例**: `venv_path = "/path/to/venv/lib/python3.x/site-packages"`

#### 4. 日志和任务目录
- **配置文件**: 多个文件中的路径配置
- **配置项**: 所有包含 `{{PROJECT_ROOT}}` 占位符的路径
- **说明**: 根据实际部署位置调整所有文件路径

### 🔧 配置方式

#### 方式一：环境变量（推荐）
```bash
export PROJECT_ROOT="/opt/daming_core"
export VENV_PATH="/opt/daming_core/venv/lib/python3.13/site-packages"
export COMFYUI_SERVER_IP="192.168.1.100"
export COMFYUI_SERVER_PORT="8188"
```

#### 方式二：直接修改配置文件
1. 编辑 `skill1/config.py`，设置 `PROJECT_ROOT`
2. 编辑 `config/external_agents.yaml`，设置服务器地址
3. 编辑相关Python文件中的硬编码路径

#### 方式三：使用配置管理工具
可以结合Ansible、Docker环境变量等工具进行配置管理。

### 🛡️ 安全注意事项

1. **敏感信息保护**：
   - 不要将包含真实IP、路径的配置文件提交到版本控制
   - 使用环境变量或配置文件模板
   - 定期检查日志文件是否包含敏感信息

2. **网络配置**：
   - 确保ComfyUI服务器可访问
   - 配置适当的防火墙规则
   - 使用HTTPS进行安全通信（如果支持）

3. **权限管理**：
   - 设置适当的文件系统权限
   - 使用非root用户运行服务
   - 定期审计访问日志

### 📁 目录结构说明

```
daming_core/
├── config/                    # 配置文件目录
│   ├── external_agents.yaml   # 外部代理配置（需要配置）
│   ├── external_agents.json   # JSON格式配置（需要配置）
│   ├── departments.yaml       # 部门配置
│   └── audit.yaml            # 审计配置
├── skill1/                    # 核心技能模块
│   ├── config.py             # 基础配置（需要配置）
│   ├── zhongshu/             # 中书省
│   ├── menxia/               # 门下省
│   ├── shangshu/             # 尚书省
│   └── bu/                   # 六部
├── skill2/                   # 民夫团队（外部执行）
│   └── main.py              # 执行器（需要配置）
├── active_tasks/             # 任务存储目录（自动创建）
├── logs/                     # 日志目录（自动创建）
└── README.md                # 本文档
```

### 🚨 故障排除

1. **导入错误**：检查 `PROJECT_ROOT` 和 `VENV_PATH` 配置
2. **连接失败**：检查ComfyUI服务器地址和端口
3. **权限错误**：检查目录权限和用户权限
4. **路径错误**：确保所有路径配置正确

### 📞 支持与反馈

如有问题，请检查日志文件或联系系统管理员。

---
**注意**：本技能已进行安全清理，移除了所有个人化配置。部署前请务必完成上述配置。
