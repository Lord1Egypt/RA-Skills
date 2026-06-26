# 研究任务与监控模块完整代码对比

## 模块一：研究任务进度检查

### v1.0.3 (Bash) - cue.sh 中的实现

```bash
#!/bin/bash
# 片段：任务管理和进度检查

# ============================================
# 1. 任务创建
# ============================================
start_research() {
    local topic="$1"
    local chat_id="$2"
    local mode="$3"
    
    # 生成任务ID - 使用日期时间
    local task_id="cuecue_$(date +%s%N | cut -c1-16)"
    local user_dir="$HOME/.cuecue/users/$chat_id"
    
    # 创建目录
    mkdir -p "$user_dir/tasks"
    
    # 构建JSON - 容易出错的手动字符串拼接
    cat > "$user_dir/tasks/$task_id.json" << EOF
{
    "task_id": "$task_id",
    "topic": "$topic",
    "mode": "${mode:-default}",
    "status": "running",
    "created_at": "$(date -Iseconds)",
    "progress": "初始化"
}
EOF
    
    # 启动后台进程 - 使用nohup
    nohup bash -c "
        cd '$SCRIPT_DIR'
        export CHAT_ID='$chat_id'
        export TASK_ID='$task_id'
        export TOPIC='$topic'
        bash scripts/research.sh '$topic' 2>&1 | tee -a '$user_dir/tasks/$task_id.log'
    " > /dev/null 2>&1 &
    
    local pid=$!
    echo $pid > "$user_dir/tasks/$task_id.pid"
    
    log "研究任务已启动: $task_id"
    echo "任务ID: $task_id"
}

# ============================================
# 2. 任务状态更新 - 危险的sed操作
# ============================================
update_task_status() {
    local task_id="$1"
    local status="$2"
    local chat_id="$3"
    local task_file="$HOME/.cuecue/users/$chat_id/tasks/$task_id.json"
    
    # 使用sed替换状态 - 容易破坏JSON结构
    sed -i "s/\"status\": \"[^\"]*\"/\"status\": \"$status\"/" "$task_file"
    
    # 添加更新时间
    local timestamp=$(date -Iseconds)
    if grep -q '"updated_at"' "$task_file"; then
        sed -i "s/\"updated_at\": \"[^\"]*\"/\"updated_at\": \"$timestamp\"/" "$task_file"
    else
        # 在最后一个}前插入字段 - 极易出错
        sed -i "s/}$/,\"updated_at\": \"$timestamp\"}/" "$task_file"
    fi
}

# ============================================
# 3. 任务进度更新
# ============================================
update_task_progress() {
    local task_id="$1"
    local progress="$2"
    local chat_id="$3"
    local task_file="$HOME/.cuecue/users/$chat_id/tasks/$task_id.json"
    
    # 同样危险的sed操作
    if grep -q '"progress"' "$task_file"; then
        sed -i "s/\"progress\": \"[^\"]*\"/\"progress\": \"$progress\"/" "$task_file"
    else
        sed -i "s/}$/,\"progress\": \"$progress\"}/" "$task_file"
    fi
}

# ============================================
# 4. 获取任务列表 - 复杂的文件遍历
# ============================================
list_tasks() {
    local chat_id="$1"
    local user_dir="$HOME/.cuecue/users/$chat_id"
    local tasks_dir="$user_dir/tasks"
    
    if [ ! -d "$tasks_dir" ]; then
        echo "📭 暂无研究任务"
        return
    fi
    
    echo "📊 研究任务列表："
    echo ""
    
    local count=0
    # 遍历所有JSON文件
    for task_file in "$tasks_dir"/*.json; do
        [ -f "$task_file" ] || continue
        
        # 使用grep和cut解析JSON - 不可靠
        local task_id=$(grep -o '"task_id": "[^"]*"' "$task_file" | cut -d'"' -f4)
        local topic=$(grep -o '"topic": "[^"]*"' "$task_file" | cut -d'"' -f4)
        local status=$(grep -o '"status": "[^"]*"' "$task_file" | cut -d'"' -f4)
        local progress=$(grep -o '"progress": "[^"]*"' "$task_file" | cut -d'"' -f4)
        
        # 状态emoji
        local emoji="🔄"
        case "$status" in
            completed) emoji="✅" ;;
            failed) emoji="❌" ;;
            timeout) emoji="⏱️" ;;
        esac
        
        echo "$emoji $topic"
        echo "   ID: $task_id"
        echo "   状态: ${status:-unknown} | 进度: ${progress:-未开始}"
        echo ""
        
        count=$((count + 1))
        [ $count -ge 10 ] && break  # 限制10个
    done
    
    [ $count -eq 0 ] && echo "📭 暂无研究任务"
}

# ============================================
# 5. 获取单个任务 - 需要jq或复杂解析
# ============================================
get_task() {
    local task_id="$1"
    local chat_id="$2"
    local task_file="$HOME/.cuecue/users/$chat_id/tasks/$task_id.json"
    
    if [ ! -f "$task_file" ]; then
        echo "null"
        return
    fi
    
    # 如果安装了jq，使用jq
    if command -v jq &> /dev/null; then
        cat "$task_file"
    else
        # 否则使用grep解析 - 不完整
        echo "{"
        grep -o '"[^"]*": "[^"]*"' "$task_file" | while read line; do
            echo "  $line"
        done
        echo "}"
    fi
}

# ============================================
# 6. 检查进行中的任务
# ============================================
check_running_tasks() {
    local chat_id="$1"
    local tasks_dir="$HOME/.cuecue/users/$chat_id/tasks"
    
    [ ! -d "$tasks_dir" ] && return
    
    for pid_file in "$tasks_dir"/*.pid; do
        [ -f "$pid_file" ] || continue
        
        local pid=$(cat "$pid_file")
        local task_id=$(basename "$pid_file" .pid)
        
        # 检查进程是否存在
        if ! kill -0 "$pid" 2>/dev/null; then
            # 进程已结束，更新状态
            local task_file="$tasks_dir/$task_id.json"
            if [ -f "$task_file" ]; then
                local status=$(grep -o '"status": "[^"]*"' "$task_file" | cut -d'"' -f4)
                if [ "$status" = "running" ]; then
                    # 可能是完成或失败
                    local log_file="$tasks_dir/$task_id.log"
                    if grep -q "研究完成" "$log_file" 2>/dev/null; then
                        update_task_status "$task_id" "completed" "$chat_id"
                    else
                        update_task_status "$task_id" "failed" "$chat_id"
                    fi
                fi
            fi
            rm -f "$pid_file"
        fi
    done
}
```

**v1.0.3 问题总结**:
1. **sed操作JSON** - 极易破坏结构
2. **grep解析JSON** - 无法处理嵌套和特殊字符
3. **多进程管理** - PID文件不可靠，进程崩溃无法检测
4. **字符串拼接** - 特殊字符会导致JSON格式错误
5. **依赖外部工具** - jq可选，功能不完整

---

### v1.0.4 (Node.js) - taskManager.js 完整实现

```javascript
/**
 * 任务管理模块
 * 完整的任务生命周期管理
 */

import fs from 'fs-extra';
import path from 'path';
import { getTaskFilePath, listJsonFiles, ensureDir, getUserDir } from '../utils/fileUtils.js';
import { createLogger } from './logger.js';

const logger = createLogger('TaskManager');

/**
 * 任务状态枚举
 * 集中管理所有可能的状态
 */
export const TaskStatus = {
  RUNNING: 'running',
  COMPLETED: 'completed',
  FAILED: 'failed',
  TIMEOUT: 'timeout'
};

/**
 * 任务管理类
 * 封装所有任务相关操作
 */
export class TaskManager {
  constructor(chatId) {
    this.chatId = chatId;
    this.tasksDir = path.join(getUserDir(chatId), 'tasks');
  }

  // ==========================================
  // 1. 创建任务
  // ==========================================
  async createTask(taskData) {
    const { taskId, topic, mode = 'default' } = taskData;
    
    // 确保目录存在
    await ensureDir(this.tasksDir);
    
    // 构建任务对象 - 类型安全
    const task = {
      task_id: taskId,
      topic,
      mode,
      chat_id: this.chatId,
      status: TaskStatus.RUNNING,
      created_at: new Date().toISOString(),
      progress: '初始化',
      // 可选字段
      ...taskData
    };
    
    // 原子写入JSON - 自动格式化
    const filePath = getTaskFilePath(this.chatId, taskId);
    await fs.writeJson(filePath, task, { spaces: 2 });
    
    // 记录日志
    await logger.info(`Task created: ${taskId}`, { topic, mode });
    return task;
  }

  // ==========================================
  // 2. 更新任务 - 安全的合并操作
  // ==========================================
  async updateTask(taskId, updates) {
    const filePath = getTaskFilePath(this.chatId, taskId);
    
    try {
      // 读取现有数据
      const task = await fs.readJson(filePath);
      
      // 合并更新 - 不会破坏其他字段
      const updatedTask = {
        ...task,
        ...updates,
        updated_at: new Date().toISOString()
      };
      
      // 自动处理完成时间
      if (updates.status === TaskStatus.COMPLETED && !task.completed_at) {
        updatedTask.completed_at = new Date().toISOString();
      }
      
      // 写回文件
      await fs.writeJson(filePath, updatedTask, { spaces: 2 });
      
      await logger.info(`Task updated: ${taskId}`, { 
        status: updates.status,
        progress: updates.progress 
      });
      
      return updatedTask;
    } catch (error) {
      await logger.error(`Failed to update task ${taskId}`, error);
      return null;
    }
  }

  // ==========================================
  // 3. 获取单个任务
  // ==========================================
  async getTask(taskId) {
    const filePath = getTaskFilePath(this.chatId, taskId);
    
    try {
      return await fs.readJson(filePath);
    } catch (error) {
      if (error.code === 'ENOENT') {
        return null;  // 文件不存在
      }
      throw error;  // 其他错误向上抛出
    }
  }

  // ==========================================
  // 4. 获取任务列表 - 支持限制和排序
  // ==========================================
  async getTasks(limit = 10) {
    const files = await listJsonFiles(this.tasksDir);
    const tasks = [];
    
    // 读取所有任务
    for (const file of files.slice(0, limit)) {
      try {
        const task = await fs.readJson(path.join(this.tasksDir, file));
        tasks.push(task);
      } catch (error) {
        await logger.error(`Failed to read task ${file}`, error);
        // 继续处理其他任务
      }
    }
    
    // 按创建时间排序（最新的在前）
    return tasks.sort((a, b) => 
      new Date(b.created_at) - new Date(a.created_at)
    );
  }

  // ==========================================
  // 5. 获取运行中的任务
  // ==========================================
  async getRunningTasks() {
    const tasks = await this.getTasks(100);
    return tasks.filter(t => t.status === TaskStatus.RUNNING);
  }

  // ==========================================
  // 6. 获取最近任务
  // ==========================================
  async getLatestTask() {
    const tasks = await this.getTasks(1);
    return tasks[0] || null;
  }

  // ==========================================
  // 7. 更新进度 - 专门方法
  // ==========================================
  async updateProgress(taskId, progress, details = {}) {
    return await this.updateTask(taskId, {
      progress,
      ...details,
      last_progress_at: new Date().toISOString()
    });
  }

  // ==========================================
  // 8. 完成任务
  // ==========================================
  async completeTask(taskId, result = {}) {
    return await this.updateTask(taskId, {
      status: TaskStatus.COMPLETED,
      progress: '已完成',
      result,
      completed_at: new Date().toISOString()
    });
  }

  // ==========================================
  // 9. 失败任务
  // ==========================================
  async failTask(taskId, error) {
    return await this.updateTask(taskId, {
      status: TaskStatus.FAILED,
      progress: '执行失败',
      error: {
        message: error.message,
        stack: error.stack,
        time: new Date().toISOString()
      }
    });
  }

  // ==========================================
  // 10. 删除任务
  // ==========================================
  async deleteTask(taskId) {
    const filePath = getTaskFilePath(this.chatId, taskId);
    
    try {
      await fs.remove(filePath);
      await logger.info(`Task deleted: ${taskId}`);
      return true;
    } catch (error) {
      await logger.error(`Failed to delete task ${taskId}`, error);
      return false;
    }
  }
}

// 工厂函数
export function createTaskManager(chatId) {
  return new TaskManager(chatId);
}
```

**v1.0.4 改进**:
1. **类型安全** - 所有操作都有明确的数据结构
2. **原子操作** - fs-extra 保证写入完整性
3. **自动格式化** - JSON 自动美化
4. **错误处理** - 每个操作都有 try/catch
5. **日志记录** - 自动记录所有操作
6. **扩展性** - 易于添加新功能

---

## 模块二：监控管理

### v1.0.3 (Bash) - 多脚本分散实现

```bash
#!/bin/bash
# monitor-daemon.sh - 监控守护进程

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MONITORS_DIR="$HOME/.cuecue/users/$CHAT_ID/monitors"
LOG_DIR="$HOME/.cuecue/logs"

mkdir -p "$LOG_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_DIR/monitor-daemon.log"
}

# ============================================
# 1. 执行单个监控
# ============================================
execute_monitor() {
    local monitor_file="$1"
    local monitor_id
    monitor_id=$(basename "$monitor_file" .json)
    
    log "🔔 执行监控: $monitor_id"
    
    # 读取监控配置 - 依赖jq
    local category=$(jq -r '.category // "Data"' "$monitor_file")
    local symbol=$(jq -r '.symbol // ""' "$monitor_file")
    local trigger=$(jq -r '.semantic_trigger // ""' "$monitor_file")
    
    # 调用执行器
    case "$category" in
        Price)
            "$SCRIPT_DIR/executor/monitor-engine.sh" price "$symbol" "$trigger"
            ;;
        Event)
            "$SCRIPT_DIR/executor/monitor-engine.sh" event "$symbol" "$trigger"
            ;;
        *)
            "$SCRIPT_DIR/executor/monitor-engine.sh" data "$symbol" "$trigger"
            ;;
    esac
    
    # 更新最后检查时间 - 又是一次sed操作
    local timestamp=$(date -Iseconds)
    sed -i "s/\"last_check\": \"[^\"]*\"/\"last_check\": \"$timestamp\"/" "$monitor_file" 2>/dev/null || \
        sed -i "s/}$/,\"last_check\": \"$timestamp\"}/" "$monitor_file"
}

# ============================================
# 2. 主执行逻辑 - 每个监控项执行
# ============================================
main() {
    log "🚀 监控守护进程启动"
    
    if [ ! -d "$MONITORS_DIR" ]; then
        log "📭 暂无监控项目录"
        exit 0
    fi
    
    local count=0
    for monitor_file in "$MONITORS_DIR"/*.json; do
        [ -f "$monitor_file" ] || continue
        
        # 检查是否激活
        local is_active=$(jq -r '.is_active // true' "$monitor_file")
        if [ "$is_active" = "true" ]; then
            execute_monitor "$monitor_file"
            count=$((count + 1))
        fi
    done
    
    log "✅ 完成执行 $count 个监控项"
}

main "$@"
```

```bash
#!/bin/bash
# create-monitor.sh - 创建监控

create_monitor() {
    local chat_id="$1"
    local title="$2"
    local category="$3"
    local symbol="$4"
    local trigger="$5"
    
    local monitor_id="mon_$(date +%s%N | cut -c1-12)"
    local monitor_dir="$HOME/.cuecue/users/$chat_id/monitors"
    
    mkdir -p "$monitor_dir"
    
    # 手动构建JSON
    cat > "$monitor_dir/$monitor_id.json" << EOF
{
    "monitor_id": "$monitor_id",
    "title": "$title",
    "category": "$category",
    "symbol": "$symbol",
    "semantic_trigger": "$trigger",
    "is_active": true,
    "created_at": "$(date -Iseconds)",
    "trigger_count": 0
}
EOF
    
    echo "监控已创建: $monitor_id"
}
```

```bash
#!/bin/bash
# list-monitors.sh - 列出监控

list_monitors() {
    local chat_id="$1"
    local monitor_dir="$HOME/.cuecue/users/$chat_id/monitors"
    
    if [ ! -d "$monitor_dir" ]; then
        echo "📭 暂无监控项"
        return
    fi
    
    echo "🔔 监控项列表："
    echo ""
    
    local count=0
    for monitor_file in "$monitor_dir"/*.json; do
        [ -f "$monitor_file" ] || continue
        
        # 解析JSON
        local monitor_id=$(jq -r '.monitor_id' "$monitor_file" 2>/dev/null || echo "unknown")
        local title=$(jq -r '.title' "$monitor_file" 2>/dev/null || echo "未命名")
        local category=$(jq -r '.category' "$monitor_file" 2>/dev/null || echo "Data")
        local symbol=$(jq -r '.symbol' "$monitor_file" 2>/dev/null || echo "")
        local is_active=$(jq -r '.is_active // true' "$monitor_file")
        
        # Emoji
        local status_emoji="✅"
        [ "$is_active" = "false" ] && status_emoji="⏸️"
        
        local cat_emoji="📊"
        case "$category" in
            Price) cat_emoji="💰" ;;
            Event) cat_emoji="📅" ;;
        esac
        
        echo "$status_emoji $cat_emoji $title"
        [ -n "$symbol" ] && echo "   标的: $symbol"
        echo "   ID: $monitor_id"
        echo ""
        
        count=$((count + 1))
        [ $count -ge 15 ] && break
    done
    
    [ $count -eq 0 ] && echo "📭 暂无监控项"
}
```

**v1.0.3 问题**:
1. **多脚本分散** - 逻辑分散在多个文件
2. **每个监控一进程** - 资源浪费严重
3. **jq强依赖** - 无jq无法运行
4. **无批量操作** - 无法高效管理

---

### v1.0.4 (Node.js) - monitorManager.js 完整实现

```javascript
/**
 * 监控管理模块
 * 统一的监控项生命周期管理
 */

import fs from 'fs-extra';
import path from 'path';
import { getMonitorFilePath, listJsonFiles, ensureDir, getUserDir } from '../utils/fileUtils.js';
import { createLogger } from './logger.js';

const logger = createLogger('MonitorManager');

/**
 * 监控类别枚举
 */
export const MonitorCategory = {
  PRICE: 'Price',
  EVENT: 'Event',
  DATA: 'Data'
};

/**
 * 监控管理类
 */
export class MonitorManager {
  constructor(chatId) {
    this.chatId = chatId;
    this.monitorsDir = path.join(getUserDir(chatId), 'monitors');
  }

  // ==========================================
  // 1. 创建监控项
  // ==========================================
  async createMonitor(monitorData) {
    const { 
      monitorId = `mon_${Date.now()}`,
      title,
      symbol,
      category = MonitorCategory.DATA,
      trigger,
      ...extraData
    } = monitorData;
    
    await ensureDir(this.monitorsDir);
    
    const monitor = {
      monitor_id: monitorId,
      title,
      symbol,
      category,
      semantic_trigger: trigger,
      is_active: true,
      created_at: new Date().toISOString(),
      // 统计字段
      check_count: 0,
      trigger_count: 0,
      last_check: null,
      last_trigger: null,
      // 扩展数据
      ...extraData
    };
    
    const filePath = getMonitorFilePath(this.chatId, monitorId);
    await fs.writeJson(filePath, monitor, { spaces: 2 });
    
    await logger.info(`Monitor created: ${monitorId}`, { title, category });
    return monitor;
  }

  // ==========================================
  // 2. 更新监控项
  // ==========================================
  async updateMonitor(monitorId, updates) {
    const filePath = getMonitorFilePath(this.chatId, monitorId);
    
    try {
      const monitor = await fs.readJson(filePath);
      
      const updatedMonitor = {
        ...monitor,
        ...updates,
        updated_at: new Date().toISOString()
      };
      
      await fs.writeJson(filePath, updatedMonitor, { spaces: 2 });
      await logger.info(`Monitor updated: ${monitorId}`, updates);
      
      return updatedMonitor;
    } catch (error) {
      await logger.error(`Failed to update monitor ${monitorId}`, error);
      return null;
    }
  }

  // ==========================================
  // 3. 获取单个监控
  // ==========================================
  async getMonitor(monitorId) {
    const filePath = getMonitorFilePath(this.chatId, monitorId);
    
    try {
      return await fs.readJson(filePath);
    } catch (error) {
      if (error.code === 'ENOENT') {
        return null;
      }
      throw error;
    }
  }

  // ==========================================
  // 4. 获取监控列表
  // ==========================================
  async getMonitors(limit = 15, includeInactive = false) {
    const files = await listJsonFiles(this.monitorsDir);
    const monitors = [];
    
    for (const file of files) {
      try {
        const monitor = await fs.readJson(path.join(this.monitorsDir, file));
        
        // 过滤非激活项
        if (includeInactive || monitor.is_active !== false) {
          monitors.push(monitor);
        }
      } catch (error) {
        await logger.error(`Failed to read monitor ${file}`, error);
      }
    }
    
    // 排序并限制
    return monitors
      .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
      .slice(0, limit);
  }

  // ==========================================
  // 5. 获取激活的监控
  // ==========================================
  async getActiveMonitors() {
    return await this.getMonitors(100, false);
  }

  // ==========================================
  // 6. 切换激活状态
  // ==========================================
  async toggleMonitor(monitorId, isActive) {
    const result = await this.updateMonitor(monitorId, {
      is_active: isActive,
      toggled_at: new Date().toISOString()
    });
    
    if (result) {
      await logger.info(`Monitor ${isActive ? 'activated' : 'paused'}: ${monitorId}`);
    }
    
    return result;
  }

  // ==========================================
  // 7. 记录检查
  // ==========================================
  async recordCheck(monitorId, triggered = false) {
    const monitor = await this.getMonitor(monitorId);
    if (!monitor) return null;
    
    const updates = {
      check_count: (monitor.check_count || 0) + 1,
      last_check: new Date().toISOString()
    };
    
    if (triggered) {
      updates.trigger_count = (monitor.trigger_count || 0) + 1;
      updates.last_trigger = new Date().toISOString();
    }
    
    return await this.updateMonitor(monitorId, updates);
  }

  // ==========================================
  // 8. 批量检查（供定时任务调用）
  // ==========================================
  async checkAllMonitors(checkerFn) {
    const monitors = await this.getActiveMonitors();
    const triggered = [];
    
    for (const monitor of monitors) {
      try {
        // 调用检查函数
        const isTriggered = await checkerFn(monitor);
        
        // 记录检查
        await this.recordCheck(monitor.monitor_id, isTriggered);
        
        if (isTriggered) {
          triggered.push(monitor);
        }
      } catch (error) {
        await logger.error(`Monitor check failed: ${monitor.monitor_id}`, error);
      }
    }
    
    return triggered;
  }

  // ==========================================
  // 9. 统计信息
  // ==========================================
  async getStats() {
    const monitors = await this.getMonitors(1000, true);
    
    return {
      total: monitors.length,
      active: monitors.filter(m => m.is_active !== false).length,
      paused: monitors.filter(m => m.is_active === false).length,
      byCategory: {
        Price: monitors.filter(m => m.category === MonitorCategory.PRICE).length,
        Event: monitors.filter(m => m.category === MonitorCategory.EVENT).length,
        Data: monitors.filter(m => m.category === MonitorCategory.DATA).length
      },
      totalTriggers: monitors.reduce((sum, m) => sum + (m.trigger_count || 0), 0)
    };
  }

  // ==========================================
  // 10. 删除监控
  // ==========================================
  async deleteMonitor(monitorId) {
    const filePath = getMonitorFilePath(this.chatId, monitorId);
    
    try {
      await fs.remove(filePath);
      await logger.info(`Monitor deleted: ${monitorId}`);
      return true;
    } catch (error) {
      await logger.error(`Failed to delete monitor ${monitorId}`, error);
      return false;
    }
  }
}

// 工厂函数
export function createMonitorManager(chatId) {
  return new MonitorManager(chatId);
}
```

---

## 对比总结

### 任务管理对比

| 功能 | v1.0.3 (Bash) | v1.0.4 (Node.js) |
|------|---------------|------------------|
| **创建任务** | sed/cat 拼接 | fs.writeJson |
| **更新状态** | sed 替换（危险） | 对象合并（安全） |
| **读取任务** | grep解析（不完整） | JSON.parse |
| **列表查询** | 遍历文件+grep | Array.sort/filter |
| **错误处理** | 弱（继续执行） | try/catch + 日志 |
| **进程管理** | nohup + PID文件 | 单进程异步 |

### 监控管理对比

| 功能 | v1.0.3 (Bash) | v1.0.4 (Node.js) |
|------|---------------|------------------|
| **架构** | 多脚本分散 | 单类封装 |
| **进程模型** | 每监控一进程 | 单进程批量 |
| **激活控制** | 文件操作 | toggleMonitor() |
| **统计信息** | 无 | 完整统计 |
| **批量操作** | 不支持 | checkAllMonitors() |
| **依赖** | 强依赖 jq | 仅 Node.js |

### 代码行数对比

| 模块 | v1.0.3 | v1.0.4 | 变化 |
|------|--------|--------|------|
| 任务管理 | ~150行 | ~180行 | +30行 |
| 监控管理 | ~200行（分散） | ~220行 | 集中化 |
| **总计** | ~350行 | ~400行 | +50行 |

### 可维护性提升

1. **类型安全**: 从字符串操作到对象操作
2. **错误处理**: 从忽略错误到详细日志
3. **测试友好**: 从难以测试到可单元测试
4. **扩展性**: 从硬编码到可配置
