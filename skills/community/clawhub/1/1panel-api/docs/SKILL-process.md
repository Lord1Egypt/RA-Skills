# Process - 1Panel API

## 模块说明
Process 模块提供进程管理功能，包括实时进程监控、进程终止、端口监听查询等。

## 接口列表 (4 个)

---

### GET /process/ws
**功能**: WebSocket 实时进程监控
**描述**: 建立 WebSocket 连接，实时获取系统进程信息

**参数**: 无

**WebSocket 消息格式**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| type | string | 是 | 请求类型 | `ps`, `wget`, `ssh`, `net` |
| pid | int32 | 否 | 按 PID 过滤 | > 0 |
| name | string | 否 | 按进程名过滤（模糊匹配） | - |
| username | string | 否 | 按用户名过滤（模糊匹配） | - |

**type=ps 请求示例**:
```json
{"type":"ps","pid":0,"name":"","username":""}
```

**type=net 请求示例**:
```json
{"type":"net","port":0,"processName":"","processID":0}
```

**WebSocket 响应 (type=ps)**:
```json
[
  {
    "PID": 1234,
    "name": "nginx",
    "PPID": 1,
    "username": "root",
    "status": "R",
    "startTime": "2024-01-01 12:00:00",
    "numThreads": 10,
    "numConnections": 5,
    "cpuPercent": "2.50%",
    "cpuValue": 2.5,
    "diskRead": "1.5 MB",
    "diskWrite": "512 KB",
    "cmdLine": "/usr/sbin/nginx -g 'daemon off;'",
    "rss": "50 MB",
    "rssValue": 52428800,
    "vms": "200 MB",
    "hwm": "80 MB",
    "data": "30 MB",
    "stack": "1 MB",
    "locked": "0 B",
    "swap": "0 B",
    "dirty": "0 B",
    "pss": "45 MB",
    "uss": "35 MB",
    "shared": "10 MB",
    "text": "5 MB",
    "envs": ["PATH=/usr/local/bin", ...],
    "openFiles": [...],
    "connects": [...]
  }
]
```

---

### POST /process/stop
**功能**: 终止指定进程
**描述**: 根据 PID 终止进程

**参数 (Body)**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| PID | int32 | 是 | 进程 ID | > 0 |

**请求示例**:
```json
{"PID": 1234}
```

**响应**: 
```json
{"status":"success","message":""}
```

**错误响应**:
```json
{"status":"error","message":"process not found"}
```

---

### POST /process/listening
**功能**: 获取监听端口的进程列表
**描述**: 查询所有正在监听网络端口的进程，返回进程 ID、端口号、协议和进程名

**参数**: 无

**响应**:
```json
[
  {
    "PID": 1234,
    "Port": { "80": {}, "443": {} },
    "Protocol": 1,
    "Name": "nginx"
  }
]
```

**响应字段说明**:

| 字段 | 类型 | 说明 |
|------|------|------|
| PID | int32 | 进程 ID |
| Port | map[uint32]struct{} | 监听的端口号集合 |
| Protocol | uint32 | 协议类型 (1=SOCK_STREAM/TCP, 2=SOCK_DGRAM/UDP) |
| Name | string | 进程名称 |

---

### GET /process/{pid}
**功能**: 获取指定进程的详细信息
**描述**: 根据 PID 获取进程的详细属性信息

**参数 (Path)**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| pid | int32 | 是 | 进程 ID | > 0 |

**响应**:
```json
{
  "PID": 1234,
  "name": "nginx",
  "PPID": 1,
  "username": "root",
  "status": "R",
  "startTime": "2024-01-01 12:00:00",
  "numThreads": 10,
  "numConnections": 5,
  "cpuPercent": "2.50%",
  "cpuValue": 2.5,
  "diskRead": "1.5 MB",
  "diskWrite": "512 KB",
  "cmdLine": "/usr/sbin/nginx -g 'daemon off;'",
  "rss": "50 MB",
  "rssValue": 52428800,
  "vms": "200 MB",
  "hwm": "80 MB",
  "data": "30 MB",
  "stack": "1 MB",
  "locked": "0 B",
  "swap": "0 B",
  "dirty": "0 B",
  "pss": "45 MB",
  "uss": "35 MB",
  "shared": "10 MB",
  "text": "5 MB",
  "envs": ["PATH=/usr/local/bin", ...],
  "openFiles": [...],
  "connects": [...]
}
```

**响应字段说明**:

| 字段 | 类型 | 说明 |
|------|------|------|
| PID | int32 | 进程 ID |
| name | string | 进程名称 |
| PPID | int32 | 父进程 ID |
| username | string | 进程所属用户 |
| status | string | 进程状态 (R=运行, S=睡眠, Z=僵尸等) |
| startTime | string | 进程启动时间 (格式: YYYY-MM-DD HH:mm:ss) |
| numThreads | int32 | 线程数 |
| numConnections | int | 网络连接数 |
| cpuPercent | string | CPU 占用百分比 (格式化字符串) |
| cpuValue | float64 | CPU 占用数值 |
| diskRead | string | 磁盘读取量 (格式化字符串) |
| diskWrite | string | 磁盘写入量 (格式化字符串) |
| cmdLine | string | 进程命令行完整参数 |
| rss | string | 实际物理内存占用 (Resident Set Size) |
| rssValue | uint64 | 实际物理内存字节数 |
| vms | string | 虚拟内存大小 (Virtual Memory Size) |
| hwm | string | 物理内存峰值 (High Water Mark) |
| data | string | 数据段大小 |
| stack | string | 栈大小 |
| locked | string | 锁定的内存大小 |
| swap | string | 交换空间使用量 |
| dirty | string | 脏页大小 |
| pss | string | Proportional Set Size (比例分配内存) |
| uss | string | Unique Set Size (独占内存) |
| shared | string | 共享内存大小 |
| text | string | 代码段大小 |
| envs | []string | 进程环境变量列表 |
| openFiles | []OpenFilesStat | 打开的文件列表 |
| connects | []ProcessConnect | 网络连接详情列表 |

**ProcessConnect 结构**:
| 字段 | 类型 | 说明 |
|------|------|------|
| type | string | 连接类型 (tcp, tcp6, udp, udp6, unknown) |
| status | string | 连接状态 (LISTEN, ESTABLISHED, TIME_WAIT 等) |
| localaddr | net.Addr | 本地地址 (IP:Port) |
| remoteaddr | net.Addr | 远程地址 (IP:Port) |
| PID | int32 | 进程 ID |
| name | string | 进程名称 |

---

## 使用示例

### 1. WebSocket 实时监控进程列表
```javascript
const ws = new WebSocket('ws://your-1panel-host:65432/api/v1/process/ws');
ws.onopen = () => {
    ws.send(JSON.stringify({ type: 'ps', pid: 0, name: '', username: '' }));
};
ws.onmessage = (event) => {
    const processes = JSON.parse(event.data);
    console.log(processes);
};
```

### 2. 终止进程
```bash
curl -X POST http://your-1panel-host:65432/api/v1/process/stop \
  -H "Content-Type: application/json" \
  -d '{"PID": 1234}'
```

### 3. 查询监听端口的进程
```bash
curl -X POST http://your-1panel-host:65432/api/v1/process/listening
```

### 4. 查看指定进程详情
```bash
curl http://your-1panel-host:65432/api/v1/process/1234
```
