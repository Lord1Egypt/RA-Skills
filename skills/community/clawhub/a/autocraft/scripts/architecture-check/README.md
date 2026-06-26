# 架构检查工具

## 概述

架构检查工具用于检查代码的架构合理性，确保代码符合以下设计原则：
1. **单一职责原则（SRP）** - 每个文件只负责一个功能
2. **关注点分离** - 代码分层合理，职责清晰
3. **功能边界分明** - 不同功能之间耦合度低

## 安装与使用

### 直接运行
```bash
# 基本用法
python3 architecture_check.py --path /path/to/code

# 生成详细报告
python3 architecture_check.py --path /path/to/code --report architecture_report.json

# 显示详细输出
python3 architecture_check.py --path /path/to/code --verbose
```

### 集成到验证流程

在验证子代理中集成架构检查：

```python
import subprocess
import json

def check_architecture_quality(code_path: str) -> Dict:
    """检查架构质量"""
    try:
        result = subprocess.run(
            ['python3', 'architecture_check.py', '--path', code_path, '--report', '/tmp/architecture_report.json'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            # 读取报告
            with open('/tmp/architecture_report.json', 'r') as f:
                report = json.load(f)
            
            # 检查是否有高危问题
            if report['summary']['high_severity'] > 0:
                return {
                    "status": "FAIL",
                    "issues": ["发现架构高危问题，违反SRP原则"],
                    "report": report
                }
            else:
                return {
                    "status": "PASS",
                    "report": report
                }
        else:
            return {
                "status": "FAIL",
                "issues": ["架构检查失败"],
                "error": result.stderr
            }
    except Exception as e:
        return {
            "status": "ERROR",
            "issues": [f"架构检查异常：{str(e)}"]
        }
```

## 检查维度

### 1. 文件职责单一性（SRP）
- **检查项**：文件是否包含多个不相关功能
- **判定标准**：文件包含2个以上不相关功能 → FAIL
- **示例**：
  - ✅ `user_service.py` - 只包含用户相关的业务逻辑
  - ❌ `user_router_and_service.py` - 包含路由和服务逻辑

### 2. 代码结构合理性
- **检查项**：代码分层是否合理
- **判定标准**：路由文件中包含业务逻辑 → FAIL
- **示例**：
  - ✅ `user_router.py` - 只处理HTTP请求
  - ❌ `user_router.py` - 包含数据库查询逻辑

### 3. 功能边界分明性
- **检查项**：功能之间耦合度是否过高
- **判定标准**：导入过多外部模块（>15个） → WARNING
- **示例**：
  - ✅ `email_service.py` - 只依赖email相关模块
  - ❌ `user_service.py` - 依赖10+个不相关模块

## 报告格式

### JSON报告
```json
{
  "srp_checks": [
    {
      "file": "backend/api/routers/data_processor.py",
      "issues": [
        {
          "type": "SRP_VIOLATION",
          "description": "文件包含多个不相关功能：数据上传、查询、存储",
          "severity": "HIGH"
        }
      ],
      "function_count": 15,
      "class_count": 3
    }
  ],
  "structure_checks": [...],
  "boundary_checks": [...],
  "summary": {
    "total_files": 25,
    "issues_found": 3,
    "high_severity": 1,
    "medium_severity": 1,
    "low_severity": 1
  }
}
```

### 文本报告
```
==================================================
架构检查报告
==================================================

📊 检查摘要
   检查文件数: 25
   发现问题数: 3
   高危问题: 1
   中危问题: 1
   低危问题: 1

🔍 SRP原则检查（文件职责单一性）
   ❌ 发现 1 个SRP违规：
      • backend/api/routers/data_processor.py: 文件包含多个不相关功能

🏗️  代码结构检查
   ✅ 代码结构良好

💡 重构建议
   1. 优先处理 1 个高危问题
   2. 拆分职责混淆的文件（1个）

==================================================
```

## 集成到验证流程

### 验证子代理配置

在验证子代理的验证维度中增加"架构合理性"维度：

```python
# 验证代码时
def verify_code_architecture(task_info, output_files):
    """验证代码架构合理性"""
    architecture_check_result = check_architecture_quality(task_info["project_path"])
    
    if architecture_check_result["status"] == "FAIL":
        return {
            "dimension": "架构合理性",
            "result": "FAIL",
            "details": architecture_check_result["issues"],
            "report": architecture_check_result.get("report")
        }
    else:
        return {
            "dimension": "架构合理性",
            "result": "PASS",
            "details": "代码架构符合设计原则"
        }
```

### 验证维度更新

验证维度现在为6个：
1. ✅ 完整性
2. ✅ 正确性
3. ✅ 可运行性
4. ✅ 一致性
5. ✅ 安全性
6. ✅ **架构合理性**（新增）

## 常见问题与修复建议

### 问题1：SRP违规
**症状**：一个文件包含多个不相关功能
**修复**：拆分为多个职责单一的文件
```bash
# 拆分前
data_processor.py          # 包含数据上传、查询、存储、分析、报告

# 拆分后
data_upload_router.py       # 数据上传
data_query_service.py       # 数据查询  
data_store_repository.py    # 数据存储
data_analysis_service.py    # 数据分析
report_generator.py         # 报告生成
```

### 问题2：业务逻辑在路由文件中
**症状**：路由文件中包含数据库操作或复杂计算
**修复**：将业务逻辑移动到服务层
```python
# 错误示例
@router.post("/upload")
async def upload_file(file: UploadFile):
    # 直接在路由中处理文件
    content = await file.read()
    # ... 业务逻辑
    
# 正确示例
@router.post("/upload")
async def upload_file(file: UploadFile):
    # 调用服务层
    result = await file_service.process_upload(file)
    return result
```

### 问题3：高耦合度
**症状**：文件导入过多不相关模块
**修复**：提取公共功能，减少依赖
```python
# 错误示例
from database import User, Order, Product, Inventory
from email import send_email
from cache import cache_set, cache_get
from utils import format_date, calculate_price, validate_input

# 正确示例
from services.user_service import UserService
from services.order_service import OrderService
# 每个服务只依赖自己需要的模块
```

## 性能考虑

- **检查速度**：中等规模项目（100个文件）约5-10秒
- **内存使用**：低内存占用，流式读取文件
- **可扩展性**：支持增量检查，只检查变更文件

## 局限性

1. **静态分析**：只能进行静态代码分析，无法检查运行时行为
2. **假阳性**：某些情况下可能误报（如大型工具类文件）
3. **语言特定**：当前主要针对Python，其他语言需要适配

## 未来改进

1. **机器学习辅助**：使用AI识别代码模式和架构问题
2. **实时监控**：集成到IDE中，实时提示架构问题
3. **自定义规则**：允许用户自定义架构检查规则
4. **多语言支持**：支持JavaScript/TypeScript/Java等语言

## 贡献指南

欢迎提交问题和改进建议。请确保：
1. 新功能有完整的测试用例
2. 保持向后兼容性
3. 更新文档和示例