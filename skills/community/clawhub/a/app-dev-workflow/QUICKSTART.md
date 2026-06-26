# AppDev Skill 快速入门

10分钟上手通用应用软件开发工作流

---

## 步骤1：创建工作空间（1分钟）

```bash
# 复制AppDev Skill到工作目录
cp -r AppDev-Skill ~/workspace/
cd ~/workspace/AppDev-Skill
```

---

## 步骤2：初始化项目（2分钟）

```bash
bash scripts/init-project.sh ./MyTodoApp TaskManager
```

输出：
```
✅ 项目初始化完成！
项目目录: /workspace/MyTodoApp

下一步:
  1. cd MyTodoApp
  2. bash scripts/prd.sh init '任务管理'
  3. bash scripts/generate.sh model Task
```

---

## 步骤3：生成代码（3分钟）

```bash
cd MyTodoApp

# 生成模型
bash scripts/generate.sh model Task

# 生成服务
bash scripts/generate.sh service TaskService

# 生成页面
bash scripts/generate.sh page Task

# 生成ViewModel
bash scripts/generate.sh viewmodel Task
```

查看生成的代码：
```bash
ls -la src/
# models/Task.ts
# services/TaskService.ts
# pages/TaskPage.ets
# viewmodels/TaskViewModel.ts
```

---

## 步骤4：添加业务逻辑（3分钟）

编辑 `src/services/TaskService.ts`：

```typescript
// 在 process 方法中添加业务逻辑
async addTask(task: Task): Promise<TaskResponse> {
  try {
    hilog.info(DOMAIN, TAG, 'Adding task: %{public}s', task.title);

    // 保存到本地存储
    const tasks = await this.getAllTasks();
    tasks.push(task);
    await this.saveTasks(tasks);

    return {
      success: true,
      data: task
    };
  } catch (error) {
    this.errorHandler.handle(error, 'addTask');
    return {
      success: false,
      error: { code: 'SAVE_ERROR', message: String(error) }
    };
  }
}
```

---

## 步骤5：编译验证（1分钟）

```bash
bash scripts/build-check.sh
```

预期输出：
```
✅ TypeScript类型检查通过
✅ ArkTS语法检查通过
✅ 资源文件检查通过
✅ HAP包生成成功
```

---

## 完整示例：TodoApp

### 项目结构

```
MyTodoApp/
├── src/
│   ├── models/
│   │   └── Task.ts           # 任务数据模型
│   ├── services/
│   │   └── TaskService.ts    # 任务管理服务
│   ├── pages/
│   │   └── TaskPage.ets      # 任务列表页面
│   └── viewmodels/
│       └── TaskViewModel.ts  # 任务状态管理
├── test/
│   └── unittest/
│       └── TaskService.test.ts
└── PROJECT.md
```

### 核心代码

**Task.ts**
```typescript
export interface Task {
  id: string;
  title: string;
  completed: boolean;
  priority: 'low' | 'medium' | 'high';
  createdAt: number;
}
```

**TaskService.ts**
```typescript
export class TaskService {
  async addTask(task: Task): Promise<TaskResponse>;
  async getTasks(): Promise<Task[]>;
  async completeTask(id: string): Promise<boolean>;
}
```

**TaskPage.ets**
```typescript
@Entry
@Component
struct TaskPage {
  @State tasks: Task[] = [];

  build() {
    List() {
      ForEach(this.tasks, (task) => {
        ListItem() {
          TaskItem({ task })
        }
      })
    }
  }
}
```

---

## 下一步

- [完整文档](./README.md)
- [开发流程详解](./docs/workflow.md)
- [API参考](./docs/api.md)

---

**预计总耗时**: 10分钟
**产出**: 可运行的HarmonyOS应用骨架
