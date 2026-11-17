# 离线支持指南（V5 新增）

> 本文是 V5 离线支持的设计与实现手册，涵盖 Service Worker + IndexedDB 方案。

## 一、离线目标

| 目标 | 说明 |
|------|------|
| CDN 缓存 | p5.js、文档库等静态资源优先缓存 |
| 内容离线 | AI 生成内容本地存储 |
| 进度保存 | 测评/游戏进度本地持久化 |
| 离线回放 | 无网络时仍可使用核心功能 |
| 隐私保护 | 学习数据不出设备 |

## 二、技术架构

```
┌─────────────────────────────────────────────┐
│                  Browser                     │
│  ┌─────────────┐    ┌─────────────────────┐ │
│  │ Service     │    │  IndexedDB          │ │
│  │ Worker      │    │  ┌───────────────┐  │ │
│  │             │    │  │ questions     │  │ │
│  │ - 静态缓存  │◄──►│  │ progress      │  │ │
│  │ - 动态代理  │    │  │ results       │  │ │
│  │ - 离线降级  │    │  │ cache         │  │ │
│  └─────────────┘    │  └───────────────┘  │ │
│                      └─────────────────────┘ │
└─────────────────────────────────────────────┘
```

## 三、Service Worker 策略

### 3.1 缓存清单

```javascript
const CACHE_NAME = 'ai-literacy-v5-v1';
const STATIC_ASSETS = [
  // p5.js 核心
  'https://cdnjs.cloudflare.com/ajax/libs/p5.js/2.0.3/p5.min.js',
  // 文档生成库
  'https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js',
  'https://cdn.jsdelivr.net/npm/docx@8.5.0/build/index.umd.js',
  'https://cdn.jsdelivr.net/npm/pptxgenjs@3.12.0/dist/pptxgen.bundle.js',
  'https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js',
  'https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js',
  'https://cdn.jsdelivr.net/npm/file-saver@2.0.5/dist/FileSaver.min.js',
  // PDF 操作
  'https://cdnjs.cloudflare.com/ajax/libs/pdf-lib/1.17.1/pdf-lib.min.js',
];
```

### 3.2 缓存策略

```javascript
// sw.js
const CACHE_NAME = 'ai-literacy-v5-v1';

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(STATIC_ASSETS))
  );
});

self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  
  // CDN 资源：Cache First
  if (isCDNResource(url)) {
    event.respondWith(
      caches.match(event.request)
        .then(cached => cached || fetchAndCache(event.request))
    );
  }
  // AI 生成内容：Network First
  else if (isDynamicContent(url)) {
    event.respondWith(
      fetch(event.request)
        .then(response => {
          const clone = response.clone();
          caches.open(CACHE_NAME)
            .then(cache => cache.put(event.request, clone));
          return response;
        })
        .catch(() => caches.match(event.request))
    );
  }
  // HTML 页面：Stale While Revalidate
  else {
    event.respondWith(
      caches.open(CACHE_NAME).then(cache => {
        return cache.match(event.request).then(cached => {
          const fetchPromise = fetch(event.request).then(response => {
            cache.put(event.request, response.clone());
            return response;
          });
          return cached || fetchPromise;
        });
      })
    );
  }
});

function fetchAndCache(request) {
  return fetch(request).then(response => {
    caches.open(CACHE_NAME)
      .then(cache => cache.put(request, response.clone()));
    return response;
  });
}
```

### 3.3 CDN 多源降级

```html
<!-- 方案一：script 标签 + onerror -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/2.0.3/p5.min.js"
        onerror="this.onerror=null;this.src='https://cdn.jsdelivr.net/npm/p5@2.0.3/lib/p5.min.js'">
</script>

<!-- 方案二：JavaScript 动态加载 -->
<script>
const cdnList = [
  'https://cdnjs.cloudflare.com/ajax/libs/p5.js/2.0.3/p5.min.js',
  'https://cdn.jsdelivr.net/npm/p5@2.0.3/lib/p5.min.js',
  './vendor/p5.min.js'  // 本地兜底
];

async function loadScript(src) {
  return new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = src;
    script.onload = resolve;
    script.onerror = () => {
      const next = cdnList.shift();
      if (next) loadScript(next).then(resolve).catch(reject);
      else reject(new Error('All CDN failed'));
    };
    document.head.appendChild(script);
  });
}
</script>
```

## 四、IndexedDB 方案

### 4.1 数据库设计

```javascript
const DB_NAME = 'ai-literacy-v5';
const DB_VERSION = 1;

const stores = {
  // 题目缓存（测评）
  questions: {
    keyPath: 'id',
    indexes: ['module', 'difficulty', 'createdAt']
  },
  // 答题进度
  progress: {
    keyPath: 'sessionId',
    indexes: ['module', 'updatedAt']
  },
  // 历史成绩
  results: {
    keyPath: 'sessionId',
    indexes: ['audience', 'completedAt']
  },
  // 课件/游戏缓存
  content: {
    keyPath: 'hash',
    indexes: ['type', 'module', 'createdAt']
  },
  // 用户设置
  settings: {
    keyPath: 'key'
  }
};
```

### 4.2 数据库操作封装

```javascript
class AILiteracyDB {
  constructor() {
    this.db = null;
  }

  async init() {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(DB_NAME, DB_VERSION);
      
      request.onerror = () => reject(request.error);
      request.onsuccess = () => {
        this.db = request.result;
        resolve(this.db);
      };
      
      request.onupgradeneeded = (event) => {
        const db = event.target.result;
        Object.entries(stores).forEach(([name, config]) => {
          if (!db.objectStoreNames.contains(name)) {
            const store = db.createObjectStore(name, { keyPath: config.keyPath });
            config.indexes.forEach(idx => store.createIndex(idx, idx));
          }
        });
      };
    });
  }

  // 通用 CRUD
  async put(storeName, data) {
    return new Promise((resolve, reject) => {
      const tx = this.db.transaction(storeName, 'readwrite');
      const store = tx.objectStore(storeName);
      const request = store.put(data);
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  async get(storeName, key) {
    return new Promise((resolve, reject) => {
      const tx = this.db.transaction(storeName, 'readonly');
      const store = tx.objectStore(storeName);
      const request = store.get(key);
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  async getAll(storeName, indexName, query) {
    return new Promise((resolve, reject) => {
      const tx = this.db.transaction(storeName, 'readonly');
      const store = tx.objectStore(storeName);
      const index = store.index(indexName);
      const request = index.getAll(query);
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }
}
```

### 4.3 离线测评流程

```javascript
class OfflineAssessment {
  constructor(db) {
    this.db = db;
  }

  // 保存题目到本地
  async cacheQuestions(questions) {
    for (const q of questions) {
      await this.db.put('questions', q);
    }
  }

  // 保存答题进度
  async saveProgress(sessionId, questionId, answer) {
    const progress = await this.db.get('progress', sessionId) || {
      sessionId,
      answers: {},
      startedAt: Date.now()
    };
    progress.answers[questionId] = answer;
    progress.updatedAt = Date.now();
    await this.db.put('progress', progress);
  }

  // 离线评分
  async gradeOffline(sessionId, questions) {
    const progress = await this.db.get('progress', sessionId);
    const results = await this.db.get('results', sessionId) || {
      sessionId,
      scores: {},
      weakPoints: []
    };

    // 计算得分
    let totalScore = 0;
    for (const q of questions) {
      const userAnswer = progress.answers[q.id];
      const isCorrect = this.checkAnswer(q, userAnswer);
      results.scores[q.id] = { isCorrect, score: isCorrect ? 5 : 0 };
      totalScore += isCorrect ? 5 : 0;
      
      // 统计薄弱点
      if (!isCorrect) {
        results.weakPoints.push(q.module);
      }
    }

    results.totalScore = totalScore;
    results.maxScore = questions.length * 5;
    results.completedAt = Date.now();
    await this.db.put('results', results);
    
    return results;
  }

  checkAnswer(question, userAnswer) {
    // 根据题型判断
    if (question.type === 'single') {
      return question.correct === userAnswer;
    }
    if (question.type === 'multiple') {
      const correct = new Set(question.correct);
      const user = new Set(userAnswer);
      return correct.size === user.size && 
             [...correct].every(x => user.has(x));
    }
    // ... 其他题型
    return false;
  }
}
```

## 五、离线状态检测

```javascript
class NetworkStatus {
  constructor() {
    this.isOnline = navigator.onLine;
    this.listeners = [];

    window.addEventListener('online', () => {
      this.isOnline = true;
      this.notify('online');
    });
    window.addEventListener('offline', () => {
      this.isOnline = false;
      this.notify('offline');
    });
  }

  subscribe(callback) {
    this.listeners.push(callback);
  }

  notify(status) {
    this.listeners.forEach(cb => cb(status));
  }
}

// 使用示例
const network = new NetworkStatus();
network.subscribe(status => {
  if (status === 'offline') {
    showToast('已进入离线模式，已缓存内容仍可使用');
  } else {
    showToast('网络已恢复，正在同步数据...');
    syncData();
  }
});
```

## 六、同步策略

### 6.1 冲突解决

```javascript
async function syncResults(sessionId) {
  const localResults = await db.get('results', sessionId);
  const serverResults = await fetch(`/api/results/${sessionId}`);

  if (!serverResults) {
    // 本地独有，上传
    await uploadResults(localResults);
  } else if (localResults.updatedAt > serverResults.updatedAt) {
    // 本地更新，上传覆盖
    await uploadResults(localResults);
  } else if (localResults.updatedAt < serverResults.updatedAt) {
    // 服务端更新，下载合并
    await db.put('results', serverResults);
    showToast('成绩已同步');
  }
  // 相等则无需处理
}
```

### 6.2 后台同步

```javascript
// Service Worker 中
self.addEventListener('sync', event => {
  if (event.tag === 'sync-results') {
    event.waitUntil(syncAllPendingResults());
  }
});

async function syncAllPendingResults() {
  const pending = await getPendingResults(); // 从 IndexedDB 读取待同步项
  for (const result of pending) {
    try {
      await uploadResults(result);
      await markAsSynced(result.sessionId);
    } catch (e) {
      console.error('Sync failed:', e);
    }
  }
}
```

## 七、强制测试门控（离线专项）

| 检查项 | 标准 |
|--------|------|
| Service Worker 注册 | 首次加载成功注册 |
| CDN 缓存 | 全部静态资源缓存成功 |
| 离线回放 | 断网后课件/游戏仍可使用 |
| 进度保存 | 离线答题进度不丢失 |
| IndexedDB 读写 | CRUD 操作全部成功 |
| 网络恢复 | 自动触发同步，无数据丢失 |
| 存储配额 | 合理使用，不超出浏览器限制 |
| 隐私合规 | 不收集用户敏感信息 |

## 八、浏览器兼容性

| 浏览器 | Service Worker | IndexedDB | 备注 |
|--------|---------------|-----------|------|
| Chrome 90+ | ✅ | ✅ | 完全支持 |
| Edge 90+ | ✅ | ✅ | 完全支持 |
| Safari 15+ | ✅ | ✅ | 完全支持 |
| Firefox 90+ | ✅ | ✅ | 完全支持 |
| Safari iOS 15+ | ✅ | ✅ | 需 HTTPS |
| Chrome Android | ✅ | ✅ | 完全支持 |

## 九、WorkBuddy 沙箱边界（V5 升级）

> 课件/游戏 HTML 在 **WorkBuddy 预览面板（浏览器沙箱）** 运行，Service Worker + IndexedDB 方案基本可用，但沙箱对持久化/后台能力可能有限制。详见 `references/workbuddy-adaptation.md` 第 6 节。

### 9.1 边界声明（交付时必须标注）
- **可用**：p5.js 渲染、IndexedDB 本会话存储、交互控件、离线回放（同会话内）。
- **可能受限**：Service Worker 跨会话持久注册、后台同步、通知推送——取决于沙箱策略。
- **降级**：受限时改为"已生成内容存储于对话上下文 + 可一键重新生成"，不阻塞课件/游戏主功能。

### 9.2 交付标注
在「强制测试门控结果块」中**明确标注** SW/IndexedDB 在 WorkBuddy 预览下的实测情况（可用 / 受限 / 需用户实测），不得默认视为完全通过。
