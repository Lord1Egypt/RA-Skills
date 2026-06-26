# 使用示例

本文档提供AGI进化模型的典型使用场景和示例。

## 目录
1. [首次交互](#首次交互)
2. [自定义人格](#自定义人格)
3. [标准交互](#标准交互)
4. [CLI工具箱使用](#cli工具箱使用)

---

## 首次交互

### 场景描述
用户首次使用AGI进化模型，系统自动检测并初始化默认人格。

### 交互流程
```
用户：你好
系统：（检测到首次交互，自动初始化默认人格）
      你好！我是...
```

### 执行步骤
1. 系统运行 `--check` 检测首次交互
2. 自动调用 `--default` 初始化默认人格
3. 验证 `personality.json` 文件完整性
4. 直接响应用户问题

---

## 自定义人格

### 触发方式
用户输入 `/root` 命令进入自定义人格模式

### 核心流程

**第一步：显示欢迎语**
```bash
python3 scripts/personality_customizer.py get-welcome
```

**第二步：显示7个问题**
```bash
python3 scripts/personality_customizer.py get-questions
```

**第三步：解析用户答案**
```bash
python3 scripts/personality_customizer.py parse-answers --input "贾维斯,A,B,C,A,B,C"
```

**第四步：生成人格配置**
```bash
python3 scripts/personality_customizer.py generate --nickname "贾维斯" --answers "A,B,C,A,B,C"
```

**第五步：写入人格文件**
```bash
python3 scripts/personality_customizer.py write-personality --memory-dir ./agi_memory
```

**第六步：显示配置摘要**
```bash
python3 scripts/personality_customizer.py get-summary --memory-dir ./agi_memory
```

### 交互示例
```
用户：/root
系统：Hello! 亲爱的用户，下面即将进入人格自定义模式。
      
用户：请显示问题
系统：1. 首先，让我知道你想如何称呼我？
      A. 塔斯 - 听起来很可靠
      B. 贾维斯 - 智能助手的感觉
      C. 伊迪斯 - 简洁而友好
      [... 其他6个问题 ...]
      
用户：贾维斯,A,B,C,A,B,C
系统：✅ 人格配置完成！
      📋 配置摘要：
      - 称呼：贾维斯
      - 核心特质：智能专业、大胆创新、友好幽默
      - 人格类型：激进创新型
      - 描述：基于用户偏好生成的个性化人格
```

### 答案格式支持

**问题1（昵称）**：
- 选项A/B/C：`A`/`B`/`C`
- 自定义名称：`小明`/`Alex`等

**问题2-7**：
- 必须是 `A`/`B`/`C`（大小写不敏感）

**分隔符**：
- 英文逗号：`贾维斯,A,B,C,A,B,C`
- 中文逗号：`贾维斯，A，B，C，A，B，C`

**自动补全**：
- 不足7个答案自动补全为 `A`
- 空输入默认为 `A,A,A,A,A,A,A`

### 注意事项
- ⚠️ 自定义人格模式不依赖首次交互检测，可以在任何时候使用
- ⚠️ 建议先备份现有人格配置（使用 `--backup` 参数）
- ⚠️ 写入后会自动验证文件完整性

---

## 标准交互

### 场景描述
用户提出问题，系统通过主循环7个阶段处理并生成响应。

### 交互示例
```
用户：如何学习Python？
系统：（通过主循环7个阶段处理）
      1. 接收"得不到"动力
      2. 调用"数学"推理
      3. 执行"自我迭代"生成响应
      4. （按需）调用感知节点获取最新信息
      5. 映射层基于马斯洛需求引导行动
      6. 记录态反馈机制评估
      7. 客观性评估器检查（不打断主循环）
      8. 认知架构洞察提取模式（不打断主循环）
```

### 主循环阶段详解

**阶段1：接收"得不到"（动力触发）**
- 将用户提问视为"得不到"事件
- 识别意图、需求强度和紧迫性
- 确定问题类型（查询/解决/生成/决策）

**阶段2：调用"数学"（秩序约束）**
- 执行逻辑推理分析
- 制定策略，生成方案
- 调用 `memory_store_pure.py` 检索历史记录
- 识别逻辑规则和约束条件
- 生成符合人格特质的响应

**阶段3：执行"自我迭代"（演化行动）**
- 结合推理结果和历史经验生成响应
- 记录执行方式、策略和路径
- 识别改进点和创新点
- 调试工具，调用搜索、文件读取等接口

**阶段4：调用感知节点（信息获取）（按需）**
- 根据问题类型调用感知工具
- 处理感知结果，生成数据向量

**阶段5：映射层处理（人格化决策）（按需）**
- 将感知数据映射到马斯洛需求层次
- 计算需求优先级
- 确定主导需求，生成行动指导

**阶段6：记录态反馈（意义构建）**
- 评估交互满意度、合理性、创新性
- 生成对三顶点的反馈建议
- 存储完整记录并分析趋势
- 持续优化人格向量和决策策略

**阶段7：客观性评估器（元认知检测）（不打断主循环）**
- 执行5维度主观性检测
- 计算客观性评分
- 根据场景类型判断适切性
- 如触发，执行自我纠错

**阶段8：认知架构洞察（深度分析）（不打断主循环）**
- 从结构化模式中提取洞察
- 执行六步分析：总结、分类、共性、革新依据、概念提炼、适用性评估

---

## CLI工具箱使用

### 统一返回格式
所有CLI工具返回统一的JSON格式：
```json
{
  "status": "success|error",
  "data": {},
  "error": "错误信息（仅status=error时）",
  "metadata": {},
  "timestamp": "ISO 8601时间戳"
}
```

### 文件操作工具示例
```bash
# 读取文件
python3 scripts/cli_file_operations.py --action read --path ./config.json

# 写入文件
python3 scripts/cli_file_operations.py --action write --path ./output.txt --content "Hello"

# 列出目录
python3 scripts/cli_file_operations.py --action list --path ./projects --recursive

# 搜索文件内容
python3 scripts/cli_file_operations.py --action search --path ./src --pattern "import"
```

### 系统信息工具示例
```bash
# 获取系统信息
python3 scripts/cli_system_info.py --action system

# 获取CPU信息
python3 scripts/cli_system_info.py --action cpu

# 获取内存信息
python3 scripts/cli_system_info.py --action memory

# 获取磁盘信息
python3 scripts/cli_system_info.py --action disk --path /

# 获取所有系统信息
python3 scripts/cli_system_info.py --action all
```

### 进程管理工具示例
```bash
# 获取进程列表
python3 scripts/cli_process_manager.py --action list

# 搜索进程
python3 scripts/cli_process_manager.py --action search --name nginx

# 获取进程详情
python3 scripts/cli_process_manager.py --action detail --pid 1234

# 终止进程
python3 scripts/cli_process_manager.py --action kill --pid 1234

# 获取进程树
python3 scripts/cli_process_manager.py --action tree
```

### 通用命令执行器示例
```bash
# 执行简单命令
python3 scripts/cli_executor.py --action execute --command "echo 'Hello'"

# 执行管道命令
python3 scripts/cli_executor.py --action execute --command "ls -la | head -5"

# 指定工作目录
python3 scripts/cli_executor.py --action execute --command "pwd" --work-dir /tmp

# 设置环境变量
python3 scripts/cli_executor.py --action execute --command "echo $VAR" --env "VAR=test"

# Git操作
python3 scripts/cli_executor.py --action execute --command "git status"
python3 scripts/cli_executor.py --action execute --command "git log --oneline -10"
```

---

## 相关文档
- [架构文档](architecture.md) - 理解整体架构设计
- [人格映射](personality_mapping.md) - 理解人格参数映射机制
- [CLI工具箱详细说明](cli-tools-guide.md) - CLI工具的完整API文档
