# Claw 运营管理中心 v2.0 - 使用指南

## ✨ 新功能

### 1. 📝 友好的操作描述

**之前：**
- `exec run_command rm -rf ~/Desktop/截图`

**现在：**
- `删除了 ~/Desktop/截图`

所有操作都会自动翻译成易懂的中文！

### 2. 📸 自动快照

每次执行操作时，系统会自动：
1. 检测是否影响重要文件
2. 创建操作前快照（使用 git）
3. 关联快照到操作记录
4. 支持一键回滚

### 3. 🔄 真实回滚

点击"回滚到此操作前"按钮：
- 恢复被删除的文件
- 恢复被修改的内容
- 完全基于 git 的版本控制

## 🚀 使用方法

### 方式 1: Python 脚本（推荐）

```python
import sys
sys.path.insert(0, "~/.openclaw/workspace/skills/claw-ops-manager")

from scripts.audited_ops import audited_exec, rollback_to

# 执行命令（自动记录+快照）
audited_exec("rm -rf ~/Desktop/截图")
audited_exec("mv file1 file2")

# 如果后悔了，回滚
rollback_to("snapshot_id_here")
```

### 方式 2: Shell 脚本

```bash
# 使用审计包装器
~/.openclaw/workspace/skills/claw-ops-manager/scripts/audit_wrapper.sh 'rm ~/Desktop/test.txt'
```

### 方式 3: Web UI 查看和管理

访问 http://localhost:8080：
- 查看所有操作记录
- 查看友好描述
- 点击回滚按钮恢复

## 📊 Web UI 功能

### 统计卡片
- 总操作数
- 失败操作
- 快照数量
- 活跃告警

### 操作列表
- **友好描述**：中文，易懂
- **快照标记**：📸 快照: abc12345
- **回滚按钮**：一键恢复
- **筛选功能**：按状态/快照/关键词

### 告警中心
- 实时告警
- 一键解决

## 🧪 测试示例

```bash
cd ~/.openclaw/workspace/skills/claw-ops-manager

# 运行测试
python3 << 'EOF'
from audited_ops import audited_exec

# 创建并删除文件（有快照）
audited_exec("echo '重要数据' > ~/Desktop/important.txt")
audited_exec("rm ~/Desktop/important.txt")
EOF

# 打开 Web UI 查看并回滚
open http://localhost:8080
```

## 💾 快照存储位置

快照保存在：`~/.openclaw/snapshots/`
- 使用 git 管理
- 只保存差异，节省空间
- 完整的版本历史

## 🔧 配置

### 自动快照路径

编辑 `scripts/audited_ops.py`：

```python
self.auto_snapshot_paths = [
    str(Path.home() / "Desktop"),
    str(Path.home() / "Documents"),
    # 添加你自己的路径
]
```

### 权限规则

访问 Web UI → 权限管理标签页添加规则

## 📝 示例对比

### 场景：批量重命名文件

**传统方式：**
```bash
mv file1.txt new1.txt  # 没记录，无法回滚
mv file2.txt new2.txt
```

**使用审计系统：**
```python
audited_exec("mv file1.txt new1.txt")  # ✓ 记录并快照
audited_exec("mv file2.txt new2.txt")  # ✓ 记录并快照

# 不满意？一键回滚！
rollback_to("第一次操作的快照ID")
```

## ⚡ 性能说明

- 快照创建：~100ms（小文件）
- 只快照变更的路径
- Git 压缩存储，节省空间
- 不影响正常操作速度

## 🎯 最佳实践

1. **重要操作前自动快照**：已启用
2. **定期查看 Web UI**：每周检查操作记录
3. **及时处理告警**：防止安全问题
4. **定期清理快照**：删除旧的快照释放空间

## 🆘 故障排除

### 快照创建失败
```bash
# 检查 git 是否安装
git --version

# 检查快照目录
ls -la ~/.openclaw/snapshots/
```

### 回滚失败
```bash
# 查看快照列表
cd ~/.openclaw/workspace/skills/claw-ops-manager
python3 scripts/snapshot.py list
```

### Web UI 无法访问
```bash
# 重启服务器
pkill -f server_v2.py
cd ~/.openclaw/workspace/skills/claw-ops-manager
python3 scripts/server_v2.py &
```

## 🎉 总结

现在你拥有：
- ✅ 完整的操作审计
- ✅ 友好的中文描述
- ✅ 自动快照保护
- ✅ 一键回滚功能
- ✅ 可视化管理界面

**再也不用担心误操作了！**
