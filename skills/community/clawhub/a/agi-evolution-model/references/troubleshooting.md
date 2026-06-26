# 故障排查指南

本文档提供常见问题的诊断和解决方案。

## 目录
1. [常见问题](#常见问题)
2. [调试技巧](#调试技巧)
3. [获取帮助](#获取帮助)

---

## 常见问题

| 问题 | 症状 | 原因 | 解决方案 |
|------|------|------|---------|
| 初始化失败 | `is_first_interaction` 一直为 `True` | 权限不足 | 检查 `agi_memory` 目录权限：`chmod 755 ./agi_memory` |
| C扩展未启用 | 性能下降15-28倍 | 路径错误 | 检查 `scripts/personality_core/` 目录是否存在 |
| 人格文件损坏 | JSON 解析错误 | 原子写入失败 | 删除文件重新初始化：`rm ./agi_memory/personality.json` |
| Shell调用慢 | 初始化耗时>1秒 | 重复调用 | 使用 `--auto-init` 参数替代多次调用 |
| 并发初始化冲突 | 初始化失败或数据损坏 | 多进程同时写入 | 使用文件锁机制（代码已实现） |
| 磁盘空间不足 | 保存失败 | 存储空间不足 | 清理磁盘空间或更换存储路径 |
| CLI工具执行失败 | 返回错误状态码 | 命令语法错误 | 检查命令语法，参考 [CLI工具箱完整指南](cli-tools-guide.md) |
| 进程终止失败 | 进程仍然运行 | 权限不足 | 使用 `--signal KILL` 强制终止 |
| 文件搜索超时 | 命令长时间无响应 | 搜索范围过大 | 限制搜索路径或文件模式 |

---

## 调试技巧

### 查看初始化状态
```bash
python3 scripts/init_dialogue_optimized.py --check --memory-dir ./agi_memory
```

### 检查人格文件内容
```bash
cat ./agi_memory/personality.json | grep initialized
```

### 验证C扩展是否加载
```python
from scripts.personality_layer_pure import USE_C_EXT
print(f"C扩展已启用: {USE_C_EXT}")
```

### 手动测试初始化
```bash
python3 scripts/init_dialogue_optimized.py --auto-init --memory-dir ./agi_memory
```

### 查看系统日志
```bash
# Linux/macOS
tail -f /var/log/syslog

# Windows
Get-EventLog -LogName Application -Newest 50
```

### 测试CLI工具
```bash
# 测试文件操作
python3 scripts/cli_file_operations.py --action list --path ./

# 测试系统信息
python3 scripts/cli_system_info.py --action system

# 测试进程管理
python3 scripts/cli_process_manager.py --action list
```

### 检查Python环境
```bash
# 检查Python版本
python3 --version

# 检查已安装包
pip3 list | grep -E "aiofiles|pytest"

# 测试导入
python3 -c "import aiofiles; print('aiofiles已安装')"
```

---

## 获取帮助

### 文档资源
- [架构文档](architecture.md) - 理解整体架构设计
- [初始化指南](init_dialogue_optimized_guide.md) - 详细的初始化流程说明
- [C扩展使用说明](c_extension_usage.md) - C扩展的加载和降级机制
- [智能体响应规则](intelligence-agent-response-rules.md) - 响应流程和错误处理
- [使用示例](usage-examples.md) - 典型使用场景和示例
- [CLI工具箱完整指南](cli-tools-guide.md) - CLI工具的完整API文档

### 环境要求
- Python 3.11+
- （可选）aiofiles >= 23.0.0（用于异步I/O）
- （可选）预编译的C扩展模块（personality_core.so）

### 常见环境问题

#### aiofiles未安装
```bash
pip3 install aiofiles>=23.0.0
```

#### Python版本过低
```bash
# Ubuntu/Debian
sudo apt-get install python3.11

# macOS (使用Homebrew)
brew install python@3.11

# Windows
# 从 https://www.python.org/downloads/ 下载安装
```

#### 权限问题
```bash
# 检查目录权限
ls -la ./agi_memory

# 修改权限
chmod 755 ./agi_memory
chmod 644 ./agi_memory/*.json
```

#### 磁盘空间不足
```bash
# 检查磁盘空间
df -h

# 清理缓存
rm -rf ~/.cache

# 清理临时文件
rm -rf /tmp/*
```

---

## 高级调试

### 启用详细日志
```bash
# 设置环境变量启用详细日志
export DEBUG=1
python3 scripts/init_dialogue_optimized.py --check --memory-dir ./agi_memory
```

### 运行测试套件
```bash
# 运行所有测试
python3 -m pytest scripts/test_*.py -v

# 运行特定测试
python3 -m pytest scripts/test_memory_async.py -v

# 运行测试并显示输出
python3 -m pytest scripts/test_intentionality_daemon.py -v -s
```

### 性能分析
```bash
# 使用cProfile分析性能
python3 -m cProfile -s tottime scripts/init_dialogue_optimized.py --check --memory-dir ./agi_memory

# 使用timeit测量执行时间
python3 -m timeit "import scripts.memory_store_pure as ms; ms.MemoryStorePure('./test')"
```

---

## 日志和监控

### 启用日志记录
```python
import logging

# 配置日志级别
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='./agi_memory/debug.log'
)
```

### 监控系统资源
```bash
# 持续监控CPU和内存
watch -n 1 'ps aux | grep python'

# 监控磁盘I/O
iostat -x 1

# 监控网络连接
netstat -an | grep ESTABLISHED
```

---

## 相关文档
- [架构文档](architecture.md) - 理解整体架构设计
- [初始化指南](init_dialogue_optimized_guide.md) - 详细的初始化流程说明
- [C扩展使用说明](c_extension_usage.md) - C扩展的加载和降级机制
