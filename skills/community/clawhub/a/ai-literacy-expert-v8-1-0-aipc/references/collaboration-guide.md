> **V7 兼容性说明**：本文件从 V6 完整继承。V7 保留所有 V6 能力，本文件内容完全有效。
> V7 新增 references 见 `references/edge-cloud-architecture.md` / `references/zero-upload-privacy.md` / `references/npu-scheduling-guide.md` / `references/edge-cloud-protocol.md` / `references/audit-report-v7.md`。
> 原始文件版本：V6 · 继承版本：V7 · 继承日期：2026-08-15

# 协作备课室指南（V5 新增）

> 本文是 V5 能力六「协作备课室」的设计与实现手册，支持多人实时协作、版本管理、批注讨论。

## 一、核心理念

- **角色分工**：主讲、助教、出题等多角色协同
- **版本管理**：每次修改留档，可追溯可回滚
- **实时同步**：多人同时编辑，变更即时可见
- **批注讨论**：针对内容直接讨论，减少沟通成本

## 二、能力触发

### 2.1 触发词
- 「团队备课」「协作」「多人编辑」
- 「版本管理」「历史记录」「回滚」
- 「批注」「评论」「讨论」

### 2.2 协作模式

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| 实时协同 | 多人同时编辑 | 快速头脑风暴 |
| 分工编辑 | 各人负责不同模块 | 大型课程开发 |
| 审核流程 | 主讲编辑 → 助教审核 | 规范课程发布 |
| 离线协作 | 各自编辑后合并 | 时区差异团队 |

## 三、协作流程

### Phase 1 · 创建备课室
```
用户：创建协作备课室
AI：请设置备课室信息：
     - 名称：[数学老师AI备课组]
     - 描述：[初中数学AI辅助教学]
     - 课程范围：A1, A2, C1, C2
     - 成员（可选邀请）：[email1, email2]
```

### Phase 2 · 角色分配
```
AI：请为团队成员分配角色：
     ① 主讲（1人）：负责课程大纲和主要内容
     ② 助教（1-2人）：负责补充材料和练习题
     ③ 审核（1人）：负责质量把控
     ④ 观察者（不限）：可查看和批注，不可直接编辑
```

### Phase 3 · 分工编辑
- 主讲创建课程大纲
- 助教分配模块
- 各自编辑对应内容
- 实时同步变更

### Phase 4 · 批注讨论
- 针对具体内容添加批注
- 回复讨论串
- @提及团队成员

### Phase 5 · 版本发布
- 提交审核
- 审核通过后发布
- 生成最终备课包

## 四、技术架构

### 4.1 数据模型

```javascript
// 备课室
class PreparationRoom {
  id: string;           // UUID
  name: string;
  description: string;
  modules: string[];   // 涉及模块
  members: Member[];
  roles: Role[];
  currentVersion: string;
  createdAt: Date;
  updatedAt: Date;
}

// 成员
class Member {
  id: string;
  name: string;
  email: string;
  role: 'owner' | 'editor' | 'reviewer' | 'viewer';
  avatar?: string;
  joinedAt: Date;
}

// 版本
class Version {
  id: string;
  roomId: string;
  version: number;      // semver
  content: Content;
  changes: Change[];
  author: string;
  message: string;      // 变更说明
  createdAt: Date;
  status: 'draft' | 'review' | 'published';
}

// 内容
class Content {
  outline: Outline;     // 大纲
  modules: ModuleContent[];
  questions: Question[];
  presentations: Presenter[];
  attachments: Attachment[];
}

// 批注
class Comment {
  id: string;
  targetType: 'outline' | 'module' | 'question' | 'slide';
  targetId: string;
  position: Selection;  // 选区位置
  content: string;
  author: string;
  replies: Reply[];
  resolved: boolean;
  createdAt: Date;
}
```

### 4.2 实时同步架构

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client A  │◄───►│   Server    │◄───►│   Client B  │
│  (主讲)     │     │  (协调者)   │     │   (助教)    │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │
       │    ┌──────────────┴──────────────┐    │
       │    │        IndexedDB            │    │
       │    │  ┌───────────────────────┐   │    │
       │    │  │ localChanges         │   │    │
       │    │  │ pendingOperations     │   │    │
       │    │  │ conflictQueue         │   │    │
       │    │  └───────────────────────┘   │    │
       │    └──────────────────────────────┘    │
       │                                       │
       └───────────────────────────────────────┘
              离线支持：本地操作 + 后台同步
```

### 4.3 操作转换（OT）算法

```javascript
// 简化版 OT 实现
class OperationalTransform {
  // 客户端发起操作
  clientOp(op) {
    // 1. 立即应用到本地
    this.applyLocally(op);
    
    // 2. 发送到服务器
    this.sendToServer(op);
    
    // 3. 保存到待确认队列
    this.pendingOps.push(op);
  }

  // 服务器广播操作
  serverBroadcast(op, excludeClientId) {
    // 1. 广播给其他客户端
    clients
      .filter(c => c.id !== excludeClientId)
      .forEach(c => c.receiveOp(op));
    
    // 2. 保存到版本历史
    this.versionHistory.push(op);
  }

  // 客户端接收远程操作
  receiveRemoteOp(remoteOp) {
    // 1. 转换本地待确认操作
    const transformedOps = this.pendingOps.map(localOp => 
      this.transform(localOp, remoteOp)
    );
    
    // 2. 应用转换后的远程操作
    this.applyRemotely(remoteOp);
    
    // 3. 更新本地待确认队列
    this.pendingOps = transformedOps;
  }

  // 操作转换
  transform(op1, op2) {
    // 简单字符串 OT
    if (op1.type === 'insert' && op2.type === 'insert') {
      if (op1.pos < op2.pos) return op1;
      if (op1.pos > op2.pos) return { ...op1, pos: op1.pos + op2.text.length };
    }
    // ... 其他转换规则
    return op1;
  }
}
```

## 五、版本管理

### 5.1 版本控制策略

```javascript
// Git-like 版本控制
class VersionControl {
  constructor() {
    this.versions = [];
    this.current = null;
  }

  // 创建快照
  createSnapshot(content, message, author) {
    const version = {
      id: uuid(),
      parent: this.current?.id,
      version: this.nextVersion(),
      content: deepClone(content),
      message,
      author,
      timestamp: Date.now(),
      hash: this.hash(content)
    };
    this.versions.push(version);
    this.current = version;
    return version;
  }

  // 查看历史
  history(limit = 20) {
    return this.versions
      .slice(-limit)
      .reverse()
      .map(v => ({
        version: v.version,
        message: v.message,
        author: v.author,
        timestamp: v.timestamp,
        shortHash: v.hash.substring(0, 7)
      }));
  }

  // 回滚到指定版本
  rollback(versionId) {
    const target = this.versions.find(v => v.id === versionId);
    if (!target) throw new Error('Version not found');
    
    // 创建新版本记录回滚
    return this.createSnapshot(
      target.content,
      `回滚到 v${target.version}`,
      'system'
    );
  }

  // 比较两个版本
  diff(versionId1, versionId2) {
    const v1 = this.versions.find(v => v.id === versionId1);
    const v2 = this.versions.find(v => v.id === versionId2);
    return this.computeDiff(v1.content, v2.content);
  }
}
```

### 5.2 版本历史 UI

```html
<div id="version-history">
  <h3>📜 版本历史</h3>
  <div class="timeline">
    <div class="version current">
      <div class="badge">v1.3</div>
      <div class="info">
        <div class="message">新增 C3 模块练习题</div>
        <div class="meta">
          <span class="author">张老师</span>
          <span class="time">10分钟前</span>
        </div>
      </div>
      <div class="actions">
        <button onclick="previewVersion('v1.3')">预览</button>
        <button onclick="rollback('v1.3')">回滚</button>
      </div>
    </div>
    
    <div class="version">
      <div class="badge">v1.2</div>
      <div class="info">
        <div class="message">调整课程大纲结构</div>
        <div class="meta">
          <span class="author">李助教</span>
          <span class="time">2小时前</span>
        </div>
      </div>
    </div>
    
    <div class="version">
      <div class="badge">v1.1</div>
      <div class="info">
        <div class="message">初始课程框架</div>
        <div class="meta">
          <span class="author">主讲王老师</span>
          <span class="time">昨天</span>
        </div>
      </div>
    </div>
  </div>
</div>
```

## 六、批注系统

### 6.1 批注数据结构

```javascript
class Annotation {
  id: string;
  type: 'comment' | 'suggestion' | 'question' | 'issue';
  target: {
    type: 'outline' | 'module' | 'question' | 'slide',
    id: string,
    selection?: { start: number, end: number }
  };
  content: string;
  author: {
    id: string,
    name: string,
    avatar?: string
  };
  mentions: string[];    // @提及的成员
  replies: Reply[];
  status: 'open' | 'resolved';
  priority: 'low' | 'medium' | 'high';
  createdAt: Date;
  resolvedAt?: Date;
  resolvedBy?: string;
}
```

### 6.2 批注 UI

```html
<div class="annotation-layer">
  <!-- 选区高亮 -->
  <div class="highlight" style="..." data-annotation-id="ann-001"></div>
  
  <!-- 批注气泡 -->
  <div class="annotation-popup" id="ann-001">
    <div class="header">
      <img src="avatar.jpg" class="avatar">
      <span class="author">张老师</span>
      <span class="time">5分钟前</span>
    </div>
    <div class="content">
      <p>这个定义需要更精确，建议参考 Module F1 安全伦理</p>
    </div>
    <div class="mentions">
      <span class="mention">@李助教</span>
    </div>
    <div class="replies">
      <div class="reply">
        <strong>李助教：</strong>收到，我来补充相关内容
      </div>
    </div>
    <div class="actions">
      <button>回复</button>
      <button>解决</button>
      <button>删除</button>
    </div>
  </div>
</div>
```

### 6.3 批注交互

```javascript
// 添加选区批注
function addSelectionAnnotation(text, selection) {
  const annotation = {
    id: uuid(),
    type: 'comment',
    target: { type: 'current', selection },
    content: text,
    author: currentUser,
    mentions: extractMentions(text),
    replies: [],
    status: 'open',
    createdAt: Date.now()
  };
  
  // 保存到数据库
  db.put('annotations', annotation);
  
  // 高亮显示
  highlightSelection(selection, annotation.id);
  
  // 通知被@成员
  if (annotation.mentions.length > 0) {
    notifyMentionedUsers(annotation);
  }
}

// 解决批注
function resolveAnnotation(annotationId) {
  const annotation = db.get('annotations', annotationId);
  annotation.status = 'resolved';
  annotation.resolvedAt = Date.now();
  annotation.resolvedBy = currentUser.id;
  db.put('annotations', annotation);
  
  // 移除高亮
  removeHighlight(annotationId);
}
```

## 七、离线协作

### 7.1 冲突检测与解决

```javascript
class ConflictResolver {
  // 检测冲突
  detectConflict(localOp, remoteOp) {
    // 如果两个操作修改了同一区域，则冲突
    return this.overlaps(localOp.range, remoteOp.range);
  }

  // 自动解决策略
  async resolve(localOp, remoteOp) {
    // 策略一：最后写入胜出（LWW）
    if (remoteOp.timestamp > localOp.timestamp) {
      return { resolution: 'remote-wins', op: remoteOp };
    } else {
      return { resolution: 'local-wins', op: localOp };
    }
    
    // 策略二：合并（Merging）- 适用于非重叠修改
    if (!this.detectConflict(localOp, remoteOp)) {
      return { resolution: 'merged', ops: [localOp, remoteOp] };
    }
    
    // 策略三：提示用户手动解决
    return { resolution: 'manual', conflict: { localOp, remoteOp } };
  }
}
```

### 7.2 离线操作队列

```javascript
class OfflineQueue {
  constructor() {
    this.queue = [];
    this.loadFromStorage();
  }

  add(operation) {
    this.queue.push({
      ...operation,
      id: uuid(),
      timestamp: Date.now(),
      synced: false
    });
    this.saveToStorage();
  }

  async sync() {
    if (!navigator.onLine) return;
    
    for (const op of this.queue.filter(o => !o.synced)) {
      try {
        await this.sendToServer(op);
        op.synced = true;
      } catch (e) {
        // 网络错误，稍后重试
        console.error('Sync failed:', e);
      }
    }
    
    this.cleanup();
    this.saveToStorage();
  }
}

// 网络状态变化时自动同步
window.addEventListener('online', () => {
  offlineQueue.sync();
});
```

## 八、与能力三联动

| 联动场景 | 说明 |
|----------|------|
| 协作 → 备课 | 协作完成的内容可直接生成备课包 |
| 备课 → 协作 | 备课过程可开启协作多人编辑 |
| 版本发布 | 发布后自动生成版本化备课包 |

## 九、强制测试门控（协作专项）

| 检查项 | 标准 |
|--------|------|
| 实时同步延迟 | <500ms（局域网）/ <2s（跨地域） |
| 冲突检测 | 相同区域编辑必须检测到冲突 |
| 版本历史 | 每次保存生成版本记录 |
| 回滚功能 | 可回滚到任意历史版本 |
| 批注功能 | 支持增删改查和@提及 |
| 离线编辑 | 断网可继续编辑，联网自动同步 |
| 权限控制 | 不同角色操作权限正确限制 |
| 多设备同步 | 同一账号在不同设备数据一致 |
